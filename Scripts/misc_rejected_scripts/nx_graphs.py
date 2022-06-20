import networkx as nx
import numpy as np
import pandas as pd
import os
import sys
import copy
import json


class NX_Graphs:
    def __init__(self, path):

        self.outer_path = path

        with open(self.outer_path + "all_slices.json", "r") as fp:
            self.slices = json.load(fp)

        with open(self.outer_path + "graph_all_slices.json", "r") as fp:
            self.graphs = json.load(fp)

        self.nx_graphs = {}
        self.make_graphs()

    def make_graphs(self):
        for slice in self.slices.keys():
            self.node_attributes = self.slices[slice]["node_attributes"]
            graph = self.graphs[slice]
            sources = graph["source"]
            targets = graph["target"]
            weights = graph["weight"]
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append(
                    (str(sources[i]), str(targets[i]), {"weight": weights[i]})
                )

            G = nx.Graph()
            G.add_edges_from(list_of_edges)
            nx.set_node_attributes(G, self.node_attributes)
            self.nx_graphs[slice] = {"graph": G}
