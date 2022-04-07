import networkx as nx
import networkx.algorithms.community as nx_comm
import igraph as ig
import numpy as np
import pandas as pd
import os
import sys
import copy
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import time
from copy import deepcopy

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

import community as cluster_louvain
from Utils.graphs import Graphs

# ==============================Louvain Cluster Detection==============================


# Method for Louvain cluster detection on igraph and networkx graphs.
# - Inherits self.graphs from super Graphs.



class Louvain(Graphs):
    def __init__(self, path, graph_type, attributes_bool):
        """ Constructor
            - Calls method for performing Louvain cluster detection algorithm for specified graph-type

        Args:
            path (string): Path to experiment data
            graph_type (string): 'nx' for NetworkX graph, 'ig' for Igraph
            attributes_bool (boolean): True if graph data is accompanied by node attributes file, False if not
        """

        self.path = path
        self.path_to_dict = self.path + "parsed_dictionaries/"

        super().__init__(self.path, graph_type, attributes_bool)

        self.path_to_plots = self.path + "plots/Clustering/Louvain/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.num_total_slices = len(self.graphs.keys())
        if graph_type == "nx":
            self.nx_louvain()

        if graph_type == "ig":
            self.ig_louvain()

    def nx_louvain(self):

        Modularity_score = {}
        self.partition_dict = {}
        for i in range(1, self.num_total_slices + 1):
            self.slice_num = str(i)
            print("Starting with with slice ", i)
            G = self.graphs[str(i)]["graph"]
            # print(f"Number of nodes = {G.number_of_nodes()}")

            part_s = time.perf_counter()
            partition = cluster_louvain.best_partition(G)
            part_e = time.perf_counter()
            print(f"Time spent making partitions is {part_e-part_s:0.4f} s")

            comp_mod_s = time.perf_counter()
            Q = cluster_louvain.modularity(partition,G)
            comp_mod_e = time.perf_counter()
            print(f"Time spent calculating modularity is {comp_mod_e-comp_mod_s:0.4f} s")
            Modularity_score[self.slice_num] = Q


            dict_s = time.perf_counter()
            self.nx_make_partition_dict(G, partition)
            dict_e = time.perf_counter()
            print(f"Time spent making dict is {dict_e-dict_s:0.4f} s")
        

            # self.plot_louvain(G,partition)
        
        with open(self.path_to_dict + "modularity_score_louvain.json","w") as ouf:
            json.dump(Modularity_score,ouf)

        with open(self.path_to_dict + "partitions_louvain.json", "w") as fp:
            json.dump(self.partition_dict, fp)
       

    def nx_make_partition_dict(self, G, partition):
        """[summary]

        Args:
            G ([type]): [description]
            partition ([type]): [description]
        """
        self.partition_dict[self.slice_num] = {}
        s = self.partition_dict[self.slice_num]

        vals = list(partition.values())
        partition_num = set(vals)
    

        keys = list(partition.keys())
        for p in partition_num:
            s[p] = [k for k,v in partition.items() if v == p]
            for del_key in s[p]:
                partition.pop(del_key)
        

    def plot_louvain(self, G, partition):
        """[summary]

        Args:
            G ([type]): [description]
            partition ([type]): [description]
        """
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
        """[summary]
        """

        # Loading graph
        g = self.graphs["1"]["graph"]
        G = g.to_networkx()

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
