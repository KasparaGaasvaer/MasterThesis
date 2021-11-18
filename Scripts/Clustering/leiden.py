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

# from cdlib import algorithms
sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

import leidenalg as la
from graphs import Graphs

# ==============================Leiden Cluster Detection==============================

"""
Method for Leiden cluster detection on igraph and networkx graphs.
- Uses self.graphs from super Graphs.
"""


class Leiden(Graphs):
    def __init__(self, path, graph_type):
        super().__init__(path, graph_type)

        self.path_to_dict = path
        self.path_to_plots = "./" + path.split("/")[1] + "/plots/Clustering/Leiden/"
        self.num_total_slices = len(self.graphs.keys())

        if graph_type == "nx":
            self.nx_leiden()

        if graph_type == "ig":
            self.ig_leiden()

    def nx_leiden(self):
        self.partition_dict = {}
        # leidenalg only works with igraph?
        for i in range(1, self.num_total_slices + 1):
            self.slice_num = str(i)
            g = self.graphs[str(i)]["graph"]
            G = ig.Graph.from_networkx(g)

            partition = la.find_partition(G, la.ModularityVertexPartition)
            self.nx_make_partition_dict(G, partition)
            # print(partition)
            # print(len(partition))
        # partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter = 0.05)

        # ig.plot(partition)

        # layout = G.layout(layout='auto')
        # ig.plot(G, layout = layout)
        # plt.show()

        with open(self.path_to_dict + "nx_partitions_leiden.json", "w") as fp:
            json.dump(self.partition_dict, fp)

    def ig_leiden(self):
        G = self.graphs["1"]["graph"]

        # partition = algorithms.leiden(G)
        partition = la.find_partition(G, la.ModularityVertexPartition)

        # partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter = 0.05)
        ig.plot(partition)

        # layout = G.layout(layout='auto')
        # ig.plot(G, layout = layout)
        plt.show()

    def nx_make_partition_dict(self, G, partition):
        self.partition_dict[self.slice_num] = {}
        s = self.partition_dict[self.slice_num]

        for i in range(len(partition)):
            s[str(i)] = []
            for j in partition[i]:
                s[str(i)].append(str(j))
