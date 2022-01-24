import numpy as np
import pandas as pd
import time
import os
import sys
import copy
import json
import matplotlib.pyplot as plt
import cairosvg

from Utils.dict_opener import OpenDict
# ==============================Produce Graphs Using NetworkX / Igraph==============================


class Graphs(OpenDict):
    def __init__(self, path, graph_type, attributes_bool):
        OpenDict.__init__(self,path)

        self.slice_att = attributes_bool
        open_time_start = time.perf_counter()

        if self.slice_att:
            self.slices, self.graphs_from_file = self.open_dicts(["slices", "graphs"])
        else:
            self.graphs_from_file = self.open_dicts(["graphs"])

        open_time_end = time.perf_counter()
        print(f"Time spent opening dictionaries is {open_time_end-open_time_start:0.4f} s")

        self.graphs = {}
        if graph_type == "nx":
            self.make_nx_graphs()

        if graph_type == "ig":
            self.make_ig_graphs()

    def make_nx_graphs(self):
        import networkx as nx

        total_s = time.perf_counter()
        for slice in self.graphs_from_file.keys():
            T_netx_s = time.perf_counter()
            print("Making nx graph for slice: ", slice)
            graph = self.graphs_from_file[slice]
            sources, targets, weights = graph["source"], graph["target"], graph["weight"]
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((str(sources[i]), str(targets[i]), {"weight": weights[i]}))

            G = nx.Graph()
            G.add_edges_from(list_of_edges)

            if self.slice_att:
                self.node_attributes = self.slices[slice]["node_attributes"]
                nx.set_node_attributes(G, self.node_attributes)

            self.graphs[slice] = {"graph": G}
            T_netx_e = time.perf_counter()
            print(f"NetworkX graph maker took {T_netx_e-T_netx_s:0.4f} s")

        total_e = time.perf_counter()
        print(f"TOTAL NetworkX graph maker took {total_e-total_s:0.4f} s")

    def make_ig_graphs(self):
        import igraph as ig

        for slice in self.graphs_from_file.keys():
            graph = self.graphs_from_file[slice]
            sources = graph["source"]
            targets = graph["target"]
            weights = graph["weight"]
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((sources[i], targets[i]))

            G = ig.Graph(edges=list_of_edges)

            if self.slice_att:
                self.node_attributes = self.slices[slice]["node_attributes"]
                for n in G.vs:
                    try:
                        # Some node attributes don't exist because of bad lines in labels file
                        atts = node_attributes[str(n.index)]
                        for att in atts:
                            n[str(att)] = atts[str(att)]
                    except KeyError:
                        continue

            self.graphs[slice] = {"graph": G}

    def find_relation_nodes_edges(self):
        num_slices = len(self.graphs_from_file.keys())
        rels = np.zeros(num_slices + 1)
        for i in range(1, num_slices + 1):
            G = self.graphs[str(i)]["graph"]
            n = G.number_of_nodes()
            m = G.number_of_edges()
            rels[i] = m / n

        with open("relation_edges_nodes.txt", "w") as outfile:
            outfile.write("Slice number       edges/nodes\n")
            for i in range(1, num_slices + 1):
                outfile.write(f"{i}          {rels[i]}\n")
