import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

from parse_slices import *


#Figure out how to save nx.graphs

class ExtractSlices():
    def __init__(self, slice_file, common_attributes_file):

        with open(slice_file, 'r') as fp:
            self.slices = json.load(fp)

        with open(common_attributes_file, 'r') as fp:
            self.common_attributes = json.load(fp)


        self.graphs = {}
        self.do_stuff()
        print(self.graphs)

    def do_stuff(self):
        for slice in self.slices:
            self.slice_num = int(slice)
            self.node_attributes = self.slices[slice]['node_attributes']
            self.make_graph()
            self.find_clustering_coef()



    def make_graph(self):
        path ="./experiment6/experiment_6/slice_" + str(self.slice_num) + "/"
        filename = path + "graph_" + str(self.slice_num) + ".mat"
        types = ["source", "target", "weight"]
        dataframe = pd.read_csv(filename, names = types, delim_whitespace = True)
        self.G = nx.from_pandas_edgelist(dataframe, types[0], types[1], edge_attr = types[2])
        nx.set_node_attributes(self.G, self.node_attributes)
        #print(self.G)
        #nodes = self.G.nodes()
        #for n in nodes:
            #nodes[n]['color'] = 'm' if nodes[n]["statuses_count"] > 100000 else "c"
        #node_colors = [nodes[n]["color"] for n in nodes]
        #nx.draw(self.G, with_labels=True, node_color = node_colors)
        #plt.show()

        self.graphs[str(self.slice_num)] = {'graph' :self.G}

    def find_clustering_coef(self):
        CC = nx.average_clustering(self.graphs[str(self.slice_num)]['graph'])
        self.graphs[str(self.slice_num)]['CC'] = CC
