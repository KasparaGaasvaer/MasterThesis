

import numpy as np
import matplotlib.pyplot as plt
from Utils.dict_opener import OpenDict



class PlotGraph:
    def __init__(self, path, parameters):
       
        self.path = path
        self.path_to_plots = self.path + "plots/GraphStats/"
        if not os.path.exists(self.path_to_plots):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.path_to_plots = self.path + "plots/GraphStats/"
            elif k_value == "no":
                os.makedirs(self.path_to_plots)
                
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)
            

        OpenDicts = OpenDict(self.path)
        self.graphs = OpenDicts.open_dicts(["graphs"])

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
