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
import time
import numba as nb

# from cdlib import algorithms
sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

import leidenalg as la
from Utils.graphs import Graphs

# ==============================Leiden Cluster Detection==============================


class Leiden(Graphs):
    """Class for Leiden cluster detection on igraph and networkx graphs.

    Args:
        Graphs (super class): Produces NetworkX-graph objects to be utilised
    """
    def __init__(self, path, graph_type, attributes_bool):
        """Constructor

        Args:
            path (string): Outer path to experiment
            graph_type (string): NetworkX (nx) or iGraph (ig)
            attributes_bool (bool): True if experiment comes with node-labels
        """

        self.path = path
        self.path_to_dict = self.path + "parsed_dictionaries/"
        if not os.path.exists(self.path_to_dict):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.path_to_dict = self.path + "parsed_dictionaries/"
            if k_value == "no":
                print("This experiment has no parsed dictionaries yet")
                sys.exit()

        super().__init__(self.path, graph_type, attributes_bool)

        self.path_to_plots = self.path +  "plots/Clustering/Leiden/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.num_total_slices = len(self.graphs.keys())

        if graph_type == "nx":
            self.nx_leiden()

        if graph_type == "ig":
            self.ig_leiden()

    def nx_leiden(self):
        """Leiden algorithm for NetworkX-graphs
        """
        self.partition_dict = {}
        for i in range(1, self.num_total_slices + 1):
            print("Starting with with slice ", i)
            self.slice_num = str(i)
            g = self.graphs[str(i)]["graph"]

            trans_s = time.perf_counter()
            G = ig.Graph.from_networkx(g) # leidenalg only works with igraph, 
            trans_e = time.perf_counter()
            print(f"Time spent nx -> ig is {trans_e-trans_s:0.4f} s")
            

            part_s = time.perf_counter()
            partition = la.find_partition(G, la.ModularityVertexPartition)
            part_e = time.perf_counter()
            print(f"Time spent making partitions is {part_e-part_s:0.4f} s")

            dict_s = time.perf_counter()
            self.nx_make_partition_dict(G, partition)
            dict_e = time.perf_counter()
            print(f"Time spent making dict is {dict_e-dict_s:0.4f} s")
        
            # print(partition)
            # print(len(partition))
        # partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter = 0.05)

        # ig.plot(partition)

        # layout = G.layout(layout='auto')
        # ig.plot(G, layout = layout)
        # plt.show()

        with open(self.path_to_dict + "partitions_leiden.json", "w") as fp:
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
        """Method for constructing dictionaries woth partitions from Leiden-alg

        Args:
            G (iGraph-object): iGraph graph
            partition (list): List containing partitions from Leiden algorithm
        """
        
        self.partition_dict[self.slice_num] = {}
        s = self.partition_dict[self.slice_num]

  
        for i in range(len(partition)):
            s[str(i)] = []
            p_i = partition[i]
            for j in p_i:
                s[str(i)].append(str(G.vs[j]["_nx_name"]))
  

            
