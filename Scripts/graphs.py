import numpy as np
import pandas as pd
import os
import sys
import copy
import json
import matplotlib.pyplot as plt


#==============================Produce Graphs Using NetworkX / Igraph==============================

class Graphs():
    def __init__(self, path, graph_type):
        self.open_dicts(path)

        self.graphs = {}
        if graph_type == "nx":
            self.make_nx_graphs()

        if graph_type == "ig":
            self.make_ig_graphs()

        if graph_type == "skn":
            self.make_skn_graphs()

    def open_dicts(self, path):
        print("Opening dicts")
        with open(path + "all_slices.json", 'r') as fp:
            self.slices = json.load(fp)

        with open(path + "graph_all_slices.json", 'r') as fp:
            self.graphs_from_file = json.load(fp)


    def make_skn_graphs(self):
        print("started skn")
        #from IPython.display import SVG
        from sknetwork.utils import edgelist2adjacency, edgelist2biadjacency
        from sknetwork.data import convert_edge_list, load_edge_list, load_graphml
        from sknetwork.visualization import svg_graph, svg_digraph, svg_bigraph

        for slice in self.slices.keys():
            if slice == "1":
                self.node_attributes = self.slices[slice]['node_attributes']
                graph = self.graphs_from_file[slice]
                sources = graph['source']
                targets = graph['target']
                weights = graph['weight']
                list_of_edges = []
                for i in range(len(sources)):
                    list_of_edges.append((int(sources[i]),int(targets[i]),float(weights[i])))

                #G = edgelist2adjacency(list_of_edges, undirected=True)
                G = convert_edge_list(list_of_edges, directed=False)
                names = G.names
                
                print(G)


    def make_nx_graphs(self):
        import networkx as nx
        for slice in self.slices.keys():
            self.node_attributes = self.slices[slice]['node_attributes']
            graph = self.graphs_from_file[slice]
            sources = graph['source']
            targets = graph['target']
            weights = graph['weight']
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((str(sources[i]),str(targets[i]),{'weight': weights[i]}))

            G = nx.Graph()
            G.add_edges_from(list_of_edges)
            nx.set_node_attributes(G, self.node_attributes)
            self.graphs[slice] = {'graph':G}


    def make_ig_graphs(self):
        import igraph as ig
        for slice in self.slices.keys():
            node_attributes = self.slices[slice]['node_attributes']
            graph = self.graphs_from_file[slice]
            sources = graph['source']
            targets = graph['target']
            weights = graph['weight']
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((sources[i],targets[i]))

            G = ig.Graph(edges = list_of_edges)
            for n in G.vs:
                try:
                    #Some node attributes don't exist because of bad lines in labels file
                    atts = node_attributes[str(n.index)]
                    for att in atts:
                        n[str(att)] = atts[str(att)]
                except KeyError:
                    continue


            self.graphs[slice] = {'graph':G}
