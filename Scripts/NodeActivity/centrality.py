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
        self.path_to_stats = self.path + "statistics/Centrality/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        self.path_to_plots = self.path + "plots/Centrality/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        #self.make_graphs()
        self.calculate_centralities()

    def make_graphs(self):
        
        self.path_to_dict = self.path + "parsed_dictionaries/"

        attributes_bool = False
        graph_type = "nx"

        super().__init__(self.path, graph_type, attributes_bool)

        self.num_slices = len(self.graphs.keys())


    def calculate_centralities(self):
        
        #self.deg_c()
        #self.closeness_c()
        #self.betweenness_c()
        #self.avg_nhood_degree()
        #self.degdeg_plot()
        #self.avg_degree_connectivity()
        self.N_phases_deg_connectivity_plot()
        #self.deg_connectivity_plot()

    def deg_c(self):
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
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
            end_s = time.perf_counter()

            print(f"Time spent calculating centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "closeness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def betweenness_c(self):
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
            end_s = time.perf_counter()

            print(f"Time spent calculating centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "betweenness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def avg_nhood_degree(self):
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
            plt.clf()
            
    def deg_connectivity_plot(self):
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

        
        x = np.log(np.array(kv))
        y = np.log(np.array(kavg))

        plt.scatter(x, y)

        x_2d = x.reshape((-1, 1))
        model = linear_model.LinearRegression().fit(x_2d,y)
        y_pred = model.predict(x_2d)

        
        plt.plot(x,y_pred, label = "Prediction from OLS", color = "r")
        plt.legend()
        plt.xlabel("k")
        plt.ylabel("average degree connectivity")
        plt.savefig(path_to_these_plots + "over_all_slices_degree_connectivity_naturalLog.pdf")
        plt.clf()



    def N_phases_deg_connectivity_plot(self):
        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        all_dict = {}

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

        
        x = np.log10(np.array(kv))
        y = np.log10(np.array(kavg))

        x1,x2,x3 = x[:230], x[230:550], x[550:]
        y1,y2,y3 = y[:230], y[230:550], y[550:]

        X = [x1,x2,x3]
        Y = [y1,y2,y3]

        for i in range(len(X)):
            plt.scatter(X[i], Y[i])

            x_2d = X[i].reshape((-1, 1))
            model = linear_model.LinearRegression().fit(x_2d,Y[i])
            y_pred = model.predict(x_2d)

        
            plt.plot(X[i],y_pred, label = "Prediction from OLS", color = "r")
            plt.legend()
            plt.xlabel("k")
            plt.ylabel("average degree connectivity")
            plt.title(f"Phase {i}")
            plt.savefig(path_to_these_plots + f"over_all_slices_degree_connectivity_phase_{i}.pdf")
            plt.clf()






        

    


        





