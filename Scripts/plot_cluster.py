import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import json

sys.path.append("..") # Adds higher directory to python modules path, looking for Graphs-class one level up

from graphs import Graphs
import community as cluster_louvain

class PlotCluster(Graphs):
    def __init__(self, path, method):
        super().__init__(path, "nx")
        self.path_to_partitions = path
        self.num_total_slices = len(self.graphs.keys())

        if method == "louvain":
            with open(self.path_to_partitions + "nx_partitions_louvain.json", 'r') as fp:
                self.partition_dict = json.load(fp)

            
            self.path_to_plots = "./" + path.split("/")[1] + "/plots/Clustering/Louvain/"
            self.plot_louvain()


        if method == "leiden":
            with open(self.path_to_partitions + "nx_partitions_leiden.json", 'r') as fp:
                self.partition_dict = json.load(fp)
            
            self.path_to_plots = "./" + path.split("/")[1] + "/plots/Clustering/Leiden/"
            self.plot_leiden()


        
    def plot_louvain(self):
        for s in range(1,11):
            G = self.graphs[str(s)]["graph"]
            p = self.partition_dict[str(s)]
            #keys = len(p) + 1 
            P = {}

            for part in p.keys():
                for n in p[part]:
                    P[n] = int(part)

            pos = nx.kamada_kawai_layout(G)
            cmap = cm.get_cmap('viridis', max(P.values()) + 1)
            nx.draw_networkx_nodes(G, pos, P.keys(), node_size=1, cmap=cmap, node_color=list(P.values()))
            nx.draw_networkx_edges(G, pos, alpha=0.5)
            plt.savefig(self.path_to_plots + "Louvain_partitions_slice"+str(s)+".pdf")
            plt.close()      

            induced_G = cluster_louvain.induced_graph(P,G)
            nx.draw_networkx(induced_G)
            plt.savefig(self.path_to_plots + "Louvain_induced_slice"+str(s)+".pdf")
            plt.close()  


            

    def plot_leiden(self):
        for s in range(1,11):
            G = self.graphs[str(s)]["graph"]
            p = self.partition_dict[str(s)]
            #keys = len(p) + 1 
            P = {}

            for part in p.keys():
                for n in p[part]:
                    P[n] = int(part)

            pos = nx.kamada_kawai_layout(G)
            cmap = cm.get_cmap('viridis', max(P.values()) + 1)
            nx.draw_networkx_nodes(G, pos, P.keys(), node_size=1, cmap=cmap, node_color=list(P.values()))
            nx.draw_networkx_edges(G, pos, alpha=0.5)
            plt.savefig(self.path_to_plots + "Leiden_partitions_slice"+str(s)+".pdf")
            plt.close()      

            induced_G = cluster_louvain.induced_graph(P,G)
            nx.draw_networkx(induced_G)
            plt.savefig(self.path_to_plots + "Leiden_induced_slice"+str(s)+".pdf")
            plt.close() 