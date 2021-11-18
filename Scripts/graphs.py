import numpy as np
import pandas as pd
import time
import os
import sys
import copy
import json
import matplotlib.pyplot as plt
import cairosvg


# ==============================Produce Graphs Using NetworkX / Igraph==============================


class Graphs:
    def __init__(self, path, graph_type):

        open_time_start = time.perf_counter()
        self.open_dicts(path)
        open_time_end = time.perf_counter()
        print(
            f"Time spent opening dictionaries is {open_time_end-open_time_start:0.4f} s"
        )

        self.graphs = {}
        if graph_type == "nx":
            self.make_nx_graphs()

        if graph_type == "ig":
            self.make_ig_graphs()

        if graph_type == "skn":
            self.make_skn_graphs()

    def open_dicts(self, path):
        with open(path + "all_slices.json", "r") as fp:
            self.slices = json.load(fp)

        with open(path + "graph_all_slices.json", "r") as fp:
            self.graphs_from_file = json.load(fp)

    def make_skn_graphs(self):
        # from IPython.display import SVG
        from sknetwork.utils import edgelist2adjacency, edgelist2biadjacency
        from sknetwork.data import convert_edge_list, load_edge_list, load_graphml
        from sknetwork.visualization import svg_graph, svg_digraph, svg_bigraph
        from sknetwork.visualization import svg_graph
        from sknetwork.topology import get_connected_components

        for slice in self.slices.keys():
            if slice == "1":
                self.node_attributes = self.slices[slice]["node_attributes"]
                graph = self.graphs_from_file[slice]
                sources = graph["source"]
                targets = graph["target"]
                weights = graph["weight"]
                list_of_edges = []
                time_edges_start = time.perf_counter()
                for i in range(len(sources)):
                    list_of_edges.append(
                        (int(sources[i]), int(targets[i]), float(weights[i]))
                    )
                time_edges_end = time.perf_counter()
                print(
                    f"Time spent appending edges is {time_edges_end-time_edges_start:0.4f} s"
                )

                T_conv_edge_2_adj_start = time.perf_counter()
                G = edgelist2adjacency(list_of_edges, undirected=True)
                T_conv_edge_2_adj_end = time.perf_counter()
                print(
                    f"Time spent converting edges is {T_conv_edge_2_adj_end-T_conv_edge_2_adj_start:0.4f} s"
                )

                T_CC_start = time.perf_counter()
                labels = get_connected_components(G)
                T_CC_end = time.perf_counter()
                print(
                    f"Time spent getting connected comp is {T_CC_end-T_CC_start:0.4f} s"
                )
                # G = convert_edge_list(list_of_edges, directed=False)

                filename_skn = "skn_graph_test"
                T_save_img_start = time.perf_counter()
                image = svg_graph(G, labels=labels, filename=filename_skn)
                T_save_img_end = time.perf_counter()
                print(
                    f"Time spent saving img is {T_save_img_end-T_save_img_start:0.4f} s"
                )

                cairosvg.svg2pdf(
                    url=filename_skn + ".svg", write_to=filename_skn + ".pdf"
                )

    def make_nx_graphs(self):
        import networkx as nx

        T_netx_s = time.perf_counter()
        for slice in self.slices.keys():
            # if int(slice) <= 10 :
            self.node_attributes = self.slices[slice]["node_attributes"]
            graph = self.graphs_from_file[slice]
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
            self.graphs[slice] = {"graph": G}

        T_netx_e = time.perf_counter()
        print(f"NetworkX graph maker took {T_netx_e-T_netx_s:0.4f} s")

    def make_ig_graphs(self):
        import igraph as ig

        for slice in self.slices.keys():
            node_attributes = self.slices[slice]["node_attributes"]
            graph = self.graphs_from_file[slice]
            sources = graph["source"]
            targets = graph["target"]
            weights = graph["weight"]
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((sources[i], targets[i]))

            G = ig.Graph(edges=list_of_edges)
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
        num_slices = len(self.slices.keys())
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
