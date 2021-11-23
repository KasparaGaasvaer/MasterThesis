import networkx as nx
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import json
import os

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

from graphs import Graphs
import community as cluster_louvain


class PlotClusterGraphs(Graphs):
    def __init__(self, path, method, selection, attributes_bool):
        super().__init__(path, "nx", attributes_bool)
        self.path_to_partitions = path
        self.num_total_slices = len(self.graphs.keys())

        self.pick_selection(selection)

        if method == "louvain":
            with open(
                self.path_to_partitions + "partitions_louvain.json", "r"
            ) as fp:
                self.partition_dict = json.load(fp)

            self.path_to_plots = (
                "./" + path.split("/")[1] + "/plots/Clustering/Louvain/Graphs/"
            )
            if not os.path.exists(self.path_to_plots):
                os.makedirs(self.path_to_plots)
            self.plot_graphs_louvain()

        if method == "leiden":
            with open(self.path_to_partitions + "partitions_leiden.json", "r") as fp:
                self.partition_dict = json.load(fp)

            self.path_to_plots = (
                "./" + path.split("/")[1] + "/plots/Clustering/Leiden/Graphs/"
            )
            if not os.path.exists(self.path_to_plots):
                os.makedirs(self.path_to_plots)
            self.plot_graphs_leiden()

    def plot_graphs_louvain(self):
        for s in range(60, 81):
            G = self.graphs[str(s)]["graph"]
            p = self.partition_dict[str(s)]
            # keys = len(p) + 1
            P = {}

            for part in p.keys():
                for n in p[part]:
                    P[n] = int(part)

            pos = nx.spring_layout(G)
            cmap = cm.get_cmap("viridis", max(P.values()) + 1)
            nx.draw_networkx_nodes(
                G, pos, P.keys(), node_size=1, cmap=cmap, node_color=list(P.values())
            )
            nx.draw_networkx_edges(G, pos, alpha=0.5)
            plt.savefig(
                self.path_to_plots + "Louvain_partitions_slice" + str(s) + ".pdf"
            )
            plt.close()

            induced_G = cluster_louvain.induced_graph(P, G)
            nx.draw_networkx(induced_G)
            plt.savefig(self.path_to_plots + "Louvain_induced_slice" + str(s) + ".pdf")
            plt.close()

    def plot_graphs_leiden(self):
        for s in range(60, 81):
            G = self.graphs[str(s)]["graph"]
            p = self.partition_dict[str(s)]
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
                self.path_to_plots + "Leiden_partitions_slice" + str(s) + ".pdf"
            )
            plt.close()

            induced_G = cluster_louvain.induced_graph(P, G)
            nx.draw_networkx(induced_G)
            plt.savefig(self.path_to_plots + "Leiden_induced_slice" + str(s) + ".pdf")
            plt.close()

    def pick_selection(self, selection):
        if selection == "10":
            self.selection = 11

        elif selection == "all":
            self.selection = self.num_total_slices + 1

        else:
            raise ValueError(selection + " is not a valid selection.")
