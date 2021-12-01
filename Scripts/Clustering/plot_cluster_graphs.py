import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import json
import os

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

from Utils.graphs import Graphs
from Utils.dict_opener import OpenDict
import community as cluster_louvain


class PlotClusterGraphs(Graphs):
    def __init__(self, path, method, selection, attributes_bool):
        super().__init__(path, "nx", attributes_bool)

        OpenDicts = OpenDict(path)
        self.path_to_partitions = path + "parsed_dictionaries/"
        self.num_total_slices = len(self.graphs.keys())
        

        self.pick_selection(selection)

        self.method = method
        self.partition_dict = OpenDicts.open_dicts(["part_"+self.method])
        self.path_to_plots = path + "plots/Clustering/"+self.method.title()+"/Graphs/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.plot_graphs()

    def plot_graphs(self):
        for s in range(1,self.selection):
            G = self.graphs[str(s)]["graph"]
            p = self.partition_dict[str(s)]
            # keys = len(p) + 1
            P = {}

            for part in p.keys():
                for n in p[part]:
                    P[n] = int(part)

            pos = nx.spring_layout(G)
            cmap = cm.get_cmap("Spectral", max(P.values()) + 1)
            nx.draw_networkx_nodes(
                G, pos, P.keys(), node_size=1, cmap=cmap, node_color=list(P.values())
            )
            nx.draw_networkx_edges(G, pos, alpha=0.5)
            plt.savefig(
                self.path_to_plots + "Coloured_Partitions/" + self.method + "_partitions_slice" + str(s) + ".pdf"
            )
            plt.close()

            induced_G = cluster_louvain.induced_graph(P, G)
            nx.draw_networkx(induced_G)
            plt.savefig(self.path_to_plots + "Induced/"+ self.method + "_induced_slice" + str(s) + ".pdf")
            plt.close()

    def pick_selection(self, selection):
        if selection == "10":
            self.selection = 11

        elif selection == "all":
            self.selection = self.num_total_slices + 1

        else:
            raise ValueError(selection + " is not a valid selection.")
