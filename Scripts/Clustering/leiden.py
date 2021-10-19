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
#from cdlib import algorithms
sys.path.append("..") # Adds higher directory to python modules path, looking for Graphs-class one level up

import leidenalg as la
from graphs import Graphs

#==============================Leiden Cluster Detection==============================

"""
Method for Leiden cluster detection on igraph and networkx graphs.
- Uses self.graphs from super Graphs.
"""

class Leiden(Graphs):
    def __init__(self, path, graph_type):
        super().__init__(path, graph_type)

        if graph_type == "nx":
            self.nx_leiden()

        if graph_type == "ig":
            self.ig_leiden()


    def nx_leiden(self):
        # leidenalg only works with igraph?
        g = self.graphs["1"]["graph"]
        G = ig.Graph.from_networkx(g)

        partition = la.find_partition(G, la.ModularityVertexPartition)
        #partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter = 0.05)

        ig.plot(partition)

        #layout = G.layout(layout='auto')
        #ig.plot(G, layout = layout)
        plt.show()



    def ig_leiden(self):
        G = self.graphs["1"]["graph"]

        #partition = algorithms.leiden(G)
        partition = la.find_partition(G, la.ModularityVertexPartition)

        #partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter = 0.05)
        ig.plot(partition)

        #layout = G.layout(layout='auto')
        #ig.plot(G, layout = layout)
        plt.show()
