import networkx as nx
import igraph as ig
import numpy as np
import pandas as pd
import os
import sys
import copy
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

import community as cluster_louvain
from graphs import Graphs

# Colour by cluster
# CHECK IF IT ONLY DOES FIRST PASS
# ==============================Louvain Cluster Detection==============================

"""
Method for Louvain cluster detection on igraph and networkx graphs.
- Uses self.graphs from super Graphs.
"""


class Louvain(Graphs):
    def __init__(self, path, graph_type, attributes_bool):
        super().__init__(path, graph_type, attributes_bool)

        self.path_to_dict = path
        self.path_to_plots = "./" + path.split("/")[1] + "/plots/Clustering/Louvain/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.num_total_slices = len(self.graphs.keys())

        if graph_type == "nx":
            self.nx_louvain()

        if graph_type == "ig":
            self.ig_louvain()

    def nx_louvain(self):
        # Loading graph
        self.partition_dict = {}
        # ratios = []
        for i in range(1, self.num_total_slices + 1):
            self.slice_num = str(i)
            G = self.graphs[str(i)]["graph"]
            # print(f"Number of nodes = {G.number_of_nodes()}")
            # compute the best partition
            partition = cluster_louvain.best_partition(G)
            self.nx_make_partition_dict(G, partition)
            print("done with slice ", i)

            """
            vals = list(partition.values())
            for i in range(len(vals)):
                vals[i] = int(vals[i])
            print(f"number of clusters = {max(vals)}")
            modularity = cluster_louvain.modularity(partition, G)
            print(f"Modularity = {modularity:0.5f}")
            ratio = G.number_of_nodes()/max(vals)
            print(f"Ratio nodes/parts = {ratio:0.5f}")
            ratios.append(ratio)
            print(" ")
            """

            # self.plot_louvain(G,partition)

        with open(self.path_to_dict + "partitions_louvain.json", "w") as fp:
            json.dump(self.partition_dict, fp)
        # mean = np.mean(ratios)
        # std = np.std(ratios)
        # print(f"Avg ratio  = {mean:0.5f}, std = {std:0.5f} ")

        # vals = partition

    def nx_make_partition_dict(self, G, partition):
        self.partition_dict[self.slice_num] = {}
        s = self.partition_dict[self.slice_num]

        vals = list(partition.values())
        partition_num = []
        for v in vals:
            if v not in partition_num:
                partition_num.append(v)

        keys = list(partition.keys())

        for p in partition_num:
            s[p] = []
            for key in keys:
                if partition[key] == p:
                    s[p].append(key)

    def plot_louvain(self, G, partition):
        # draw the graph
        pos = nx.kamada_kawai_layout(G)

        # color the nodes according to their partition
        cmap = cm.get_cmap("viridis", max(partition.values()) + 1)
        nx.draw_networkx_nodes(
            G,
            pos,
            partition.keys(),
            node_size=1,
            cmap=cmap,
            node_color=list(partition.values()),
        )
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.savefig(
            self.path_to_plots
            + "NetworkX_colored_partition_slice"
            + self.slice_num
            + ".pdf"
        )
        plt.close()

        induced_G = cluster_louvain.induced_graph(partition, G)
        nx.draw_networkx(induced_G)
        plt.savefig(
            self.path_to_plots + "NetworkX_induced_slice" + self.slice_num + ".pdf"
        )
        plt.close()

    def ig_louvain(self):

        # Loading graph
        g = self.graphs["1"]["graph"]
        G = g.to_networkx()

        # compute the best partition
        partition = cluster_louvain.best_partition(G)

        # draw the graph
        pos = nx.spring_layout(G)
        # color the nodes according to their partition
        cmap = cm.get_cmap("viridis", max(partition.values()) + 1)
        nx.draw_networkx_nodes(
            G,
            pos,
            partition.keys(),
            node_size=40,
            cmap=cmap,
            node_color=list(partition.values()),
        )
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()
