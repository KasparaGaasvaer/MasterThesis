import sys, os, json, time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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
        #self.closeness_c()
        #self.betweenness_c()
        #self.avg_nhood_degree()
        self.degdeg_plot()

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


    def degdeg_plot(self):

        self.path_to_these_plots = self.path_to_plots + "kk-correlation/" 
        if not os.path.exists(self.path_to_these_plots):
            os.makedirs(self.path_to_these_plots)

        with open(self.path_to_stats + "deg_c_dict.json","r") as inff:
            ind_deg = json.load(inff)
        
        with open(self.path_to_stats + "avg_nhood_deg_dict.json","r") as inff:
            nhood_deg = json.load(inff)

        
        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            i_deg = ind_deg[s]
            n_deg = nhood_deg[s]

            print(len(i_deg))
            if len(i_deg) != len(n_deg):
                print("problem")

            """
            k = []
            k_means = []
            for n in i_deg.keys():
                k.append(i_deg[n])
                k_means.append(n_deg[n])

            plt.plot(k,k_means, "*")
            plt.xlabel("k")
            plt.ylabel("k_mean")
            plt.savefig(self.path_to_these_plots + f"s{s}_k_vs_kmean.pdf")
            """




        

    


        





