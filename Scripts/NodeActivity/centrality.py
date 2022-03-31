import sys, os, json, time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

from Utils.graphs import Graphs
sys.path.append("..")  # Adds higher directory to python modules path, looking for Graphs-class one level up

class Centrality(Graphs):
    def __init__(self,path):

        self.path = path 

        if path == "./experiment12/experiment_12/":
            k_value = input("Input k_value\n")
            if int(k_value):
                self.path = self.path + "k_" + str(k_value) + "/"
                self.path_to_plots = self.path + "plots/Centrality/"
                if not os.path.exists(self.path_to_plots):
                    os.makedirs(self.path_to_plots)
                
                self.path_to_stats = self.path + "statistics/Centrality/"
                if not os.path.exists(self.path_to_stats):
                    os.makedirs(self.path_to_stats)

                self.path_to_overleaf_plots = "./p_2_overleaf/k_" + k_value + "/UnderlyingGraph/"
                if not os.path.exists(self.path_to_overleaf_plots):
                    os.makedirs(self.path_to_overleaf_plots)


        else:
            self.path_to_stats = self.path + "statistics/Centrality/"
            if not os.path.exists(self.path_to_stats):
                os.makedirs(self.path_to_stats)

            self.path_to_plots = self.path + "plots/Centrality/"
            if not os.path.exists(self.path_to_plots):
                os.makedirs(self.path_to_plots)

            self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "UnderlyingGraph/"
            if not os.path.exists(self.path_to_overleaf_plots):
                os.makedirs(self.path_to_overleaf_plots)


        self.make_graphs()
        self.calculate_centralities()

    def make_graphs(self):
        
        self.path_to_dict = self.path + "parsed_dictionaries/"

        attributes_bool = False
        graph_type = "nx"

        super().__init__(self.path, graph_type, attributes_bool)

        self.num_slices = len(self.graphs.keys())


    def calculate_centralities(self):
        
        #self.deg_c()
        #self.avg_nhood_degree()
        #self.degdeg_plot() #denne som gir de stygge plottene
        #self.avg_degree_connectivity()
        #self.N_phases_deg_connectivity_plot()
        #self.deg_connectivity_plot()
        #self.assortativity_coeff()
        #self.closeness_c() #takes forever?
        #self.betweenness_c()
 
    def deg_c(self):
        print("DEGREE CENTRALITY\n")
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
        print("CLOSENESS CENTRALITY\n")
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
        print("BETWEENNESS CENTRALITY\n")
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
        print("ASSORTITIVIY COEFFICIENT")
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
        print("AVG NHOOD DEG")
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
        print("AVG DEG CONNECTIVITY")
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


    def degdeg_plot(self):
        print("DEGDEG PLOT")
        path_to_these_plots = self.path_to_plots + "kk-correlation/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "deg_c_dict.json","r") as inff:
            ind_deg = json.load(inff)
        
        with open(self.path_to_stats + "avg_nhood_deg_dict.json","r") as inff:
            nhood_deg = json.load(inff)

        self.num_slices = len(ind_deg.keys())

        
        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            i_deg = ind_deg[s]
            n_deg = nhood_deg[s]

            print(len(i_deg))
            if len(i_deg) != len(n_deg):
                print("problem")

            
            k = []
            k_means = []
            for n in i_deg.keys():
                k.append(i_deg[n])
                k_means.append(n_deg[n])

            plt.scatter(k,k_means)
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel("k")
            plt.ylabel("k_mean")
            plt.savefig(path_to_these_plots + f"s{s}_k_vs_kmean.pdf")
            plt.savefig(self.path_to_overleaf_plots + f"s{s}_k_vs_kmean.pdf")
            plt.clf()
            
    def deg_connectivity_plot(self):
        print("DEGCON PLOT")
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
                #kv.append(int(k))
                #kavg.append(dc[k])
                try:
                    all_dict[k].append(dc[k])
                except KeyError:
                    all_dict[k] = []
                    all_dict[k].append(dc[k])

            """
            x = np.log10(np.array(kv))
            y = np.log10(np.array(kavg))

            plt.scatter(x, y)

            x_2d = x.reshape((-1, 1))
            model = linear_model.LinearRegression().fit(x_2d,y)
            y_pred = model.predict(x_2d)

            plt.plot(x,y_pred, label = "Prediction from OLS", color = "r")
            plt.xlabel("k")
            plt.ylabel("average degree connectivity")
            plt.savefig(path_to_these_plots + f"s{s}_degree_connectivity.pdf")
            plt.clf()
            """
            

        kv = []
        kavg = []
        for k in all_dict.keys():
            kv.append(int(k))
            kavg.append(np.mean(all_dict[k]))

        
        x = np.log10(np.array(kv))
        y = np.log10(np.array(kavg))

        plt.scatter(x, y)

        x_2d = x.reshape((-1, 1))
        model = linear_model.LinearRegression().fit(x_2d,y)
        y_pred = model.predict(x_2d)

        plt.plot(x,y_pred, label = "Prediction from OLS", color = "r")
        plt.legend()
        plt.xlabel("k")
        plt.ylabel("average degree connectivity")
        plt.savefig(path_to_these_plots + "over_all_slices_degree_connectivity.pdf")
        plt.savefig(self.path_to_overleaf_plots + "over_all_slices_degree_connectivity.pdf")
        plt.clf()


    def N_phases_deg_connectivity_plot(self):
        print("PHASE PLOT")
        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        all_dict = {}

        s_list = [i for i in range(1,self.num_slices+1)]
        s_list = np.array(s_list)
        phases = np.array_split(s_list, 3)

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
            
            x = np.log10(np.array(kv))
            y = np.log10(np.array(kavg))

            print(len(x), len(y))

            plt.scatter(x, y)

            x_2d = x.reshape((-1, 1))
            model = linear_model.LinearRegression().fit(x_2d,y)
            y_pred = model.predict(x_2d)

            print(model.coef_)
                
            plt.plot(x,y_pred, label = "Prediction from OLS", color = "r")
            plt.legend()
            plt.xlabel("k")
            plt.title(f"Phase {j}")
            plt.ylabel("average degree connectivity")
            plt.savefig(path_to_these_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.savefig(self.path_to_overleaf_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.clf()

        




        

    


        





