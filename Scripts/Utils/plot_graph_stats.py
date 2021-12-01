

import numpy as np
import matplotlib.pyplot as plt
from Utils.dict_opener import OpenDict




class PlotGraph:
    def __init__(self, path, parameters):
       
        OpenDicts = OpenDict(path)
        self.graphs = OpenDicts.open_dicts(["graphs"])
        self.path_to_plots = path + "plots/GraphStats/"

        methods = {
            "num_edges" : self.num_edges
        }

        for p in parameters:
            methods[p]()


    def num_edges(self):
        lens = []
        keys = list(self.graphs.keys())[:-1]
        for key in keys:
            numE = len(self.graphs[key]["source"])
            lens.append(numE)

        for i in range(len(keys)):
            keys[i] = int(keys[i])  


        plt.xlabel('Bins')
        plt.ylabel('Frequency')
        for i in range(len(keys)):
            plt.vlines(keys[i],0,lens[i]) # Here you are drawing the horizontal lines
        plt.savefig(self.path_to_plots + "num_edges_in_slices_dist.pdf")
