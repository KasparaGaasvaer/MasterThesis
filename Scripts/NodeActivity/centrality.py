import sys, os, json, time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import curve_fit

from Utils.graphs import Graphs
sys.path.append("..")  # Adds higher directory to python modules path, looking for Graphs-class one level up


#==============================Centrality==============================

# Class containing methods for calculating vertex centralities : degree, betweenness and closeness.
# Class also contains methods related to network assortativity. 

class Centrality(Graphs):
    def __init__(self,path):
        """Constructor. Sets global paths.

        Args:
            path (string): Path to experiment. 
        """

        self.path = path 
        self.expnum = self.path.strip("./")

        self.path_to_stats = self.path + "statistics/Centrality/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        self.path_to_plots = self.path + "plots/Centrality/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "UnderlyingGraph/"
        if not os.path.exists(self.path_to_overleaf_plots):
            os.makedirs(self.path_to_overleaf_plots)



    def make_graphs(self):
        """Method for generating NetworkX graphs needed for calculating centralities.
        """
        
        self.path_to_dict = self.path + "parsed_dictionaries/"
        attributes_bool = False
        graph_type = "nx"
        super().__init__(self.path, graph_type, attributes_bool)
        self.num_slices = len(self.graphs.keys())

   
 
    def deg_c(self):
        """Method for calculating degree centrality of vertices. 
        """

        self.make_graphs()
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]
            nn = G.number_of_nodes() - 1

            start_s = time.perf_counter()
            s_dict = nx.degree_centrality(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating centrality {end_s-start_s:0.4f} s\n")

            s_dict.update((x, y*nn) for x, y in s_dict.items())

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "deg_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def closeness_c(self):
        """Method for calculating closeness centrality of vertices. 
        """

        self.make_graphs()
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
            end_s = time.perf_counter()

            print(f"Time spent calculating closeness centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "closeness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def betweenness_c(self):
        """Method for calculating betweenness centrality of vertices. 
        """

        self.make_graphs()
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
            end_s = time.perf_counter()

            print(f"Time spent calculating betweenness centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "betweenness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def assortativity_coeff(self):
        """Method for calculating the assortativity coefficient of the network.  
        """

        self.make_graphs()
        master_dict = {}
        for s in range(1,self.num_slices+1):
            G = self.graphs[str(s)]["graph"]
            start_s = time.perf_counter()
            s_dict = nx.degree_pearson_correlation_coefficient(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating assortivity {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "degree_assortivity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)


    def avg_nhood_degree(self):
        """Method for calculating the average nearest neighbour degree of each vertex. 
        """

        self.make_graphs()
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.average_neighbor_degree(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating avg centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "avg_nhood_deg_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def avg_degree_connectivity(self):
        """Method for calculating the average nearest neighbour degree of all vertices in the network. 
        """

        self.make_graphs()
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.average_degree_connectivity(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating avg degree connectivity {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)


    def deg_con_all_slices(self):
        """Method for plotting the degree-degree correlation for each slice.
        """

        path_to_these_plots = self.path_to_plots + "degree_connectivity/annd_all_slices/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        fz = 14

        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            dc = deg_con[s]
            
            key_list = [int(k) for k in dc.keys()]
            value_list = list(dc.values())

            x,y = zip(*sorted(zip(key_list,value_list)))

            plt.scatter(x, y)
            plt.title(f"Slice {ss}")
            plt.ylabel("ANND K(k)", fontsize = fz)
            plt.xlabel("Degree k", fontsize = fz)
            plt.xticks(fontsize =fz)
            plt.yticks(fontsize =fz)
            plt.yscale("log")
            plt.xscale("log")
            plt.tight_layout()
            plt.savefig(path_to_these_plots + f"jpgs/slice_{ss}.jpg")
            plt.clf()

            
    def deg_connectivity_plot(self):
        """Method for plotting the mean degree-degree correlation of all slice.
        """

        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        all_dict = {}

        self.num_slices = len(deg_con.keys())

        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            dc = deg_con[s]
            
            kv = []
            kavg = []
            for k in dc.keys():
                try:
                    all_dict[k].append(dc[k])
                except KeyError:
                    all_dict[k] = []
                    all_dict[k].append(dc[k])
            

        kv = []
        kavg = []
        for k in all_dict.keys():
            kv.append(int(k))
            kavg.append(np.mean(all_dict[k]))
        x = np.array(kv)
        y = np.array(kavg)


        fz = 14
        cmap = cm.get_cmap("plasma")
        plt.scatter(x,y, color = cmap(0))
        plt.xlabel("Degree k", fontsize = fz)
        plt.ylabel("ANND K(k)", fontsize = fz)
        plt.xticks(fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.yscale("log")
        plt.xscale("log")
        plt.tight_layout()
        plt.savefig(path_to_these_plots + "over_all_slices_degree_connectivity.pdf")
        plt.savefig(self.path_to_overleaf_plots + "over_all_slices_degree_connectivity.pdf")
        plt.clf()
        
    

    def N_phases_deg_connectivity_plot(self):
        """Method for plotting the mean degree-degree correlation for each phase.
        """
     
        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        all_dict = {}

        phases_slice = np.load(self.path_to_stats + "slice_phases.npy")
 

        s_list = [i for i in range(1,self.num_slices+1)]
        s_list = np.array(s_list)
        phases = [s_list[:int(phases_slice[0])], s_list[int(phases_slice[0]):int(phases_slice[1])], s_list[int(phases_slice[1]):]]
        print(phases)

        m_dict = {}
        i = 0
        for phase in phases:
            m_dict[str(i)] = {}
            print("NEW PHASE ")
            for ss in phase:
                print("Slice ", ss)
                s = str(ss)
                dc = deg_con[s]
                kv = []
                kavg = []
                for k in dc.keys():
                    try:
                        m_dict[str(i)][k].append(dc[k])
                    except KeyError:
                        m_dict[str(i)][k] = []
                        m_dict[str(i)][k].append(dc[k])
            i += 1

        for j in range(len(phases)):
            all_dict = m_dict[str(j)]

            kv = []
            kavg = []
            for k in all_dict.keys():
                kv.append(int(k))
                kavg.append(np.mean(all_dict[k]))
            
            x = np.array(kv)
            y = np.array(kavg)


            fz = 14
            cmap = cm.get_cmap("plasma")
            plt.scatter(x,y, color = cmap(0))
            plt.xlabel("Degree k", fontsize = fz)
            plt.ylabel("ANND K(k)", fontsize = fz)
            plt.title(f"Phase {j}", fontsize = fz)
            plt.yscale("log")
            plt.xscale("log")
            plt.xticks(fontsize = fz)
            plt.yticks(fontsize = fz)
            plt.tight_layout()
            plt.savefig(path_to_these_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.savefig(self.path_to_overleaf_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.clf()



        

    


        





