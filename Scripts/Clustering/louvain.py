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
sys.path.append("..") # Adds higher directory to python modules path, looking for Graphs-class one level up

import community as cluster_louvain
from graphs import Graphs

#==============================Louvain Cluster Detection==============================

"""
Method for Louvain cluster detection on igraph and networkx graphs.
- Uses self.graphs from super Graphs.
"""

class Louvain(Graphs):
    def __init__(self, path, graph_type):
        super().__init__(path, graph_type)

        if graph_type == "nx":
            self.nx_louvain()

        if graph_type == "ig":
            self.ig_louvain()

    def nx_louvain(self):
        # Loading graph
        G = self.graphs["1"]["graph"]

        # compute the best partition
        partition = cluster_louvain.best_partition(G)

        # draw the graph
        pos = nx.spring_layout(G)
        # color the nodes according to their partition
        cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
        nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()

    def ig_louvain(self):

        # Loading graph
        g = self.graphs["1"]["graph"]
        G = g.to_networkx()

        # compute the best partition
        partition = cluster_louvain.best_partition(G)

        # draw the graph
        pos = nx.spring_layout(G)
        # color the nodes according to their partition
        cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
        nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40, cmap=cmap, node_color=list(partition.values()))
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()
