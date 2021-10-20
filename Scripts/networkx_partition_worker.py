import networkx as nx
import numpy as np
import pandas as pd
import os
import sys
import copy
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt

class NetworkX_Partition_Worker():

    def __init__(self, path):
        self.path_to_partitions = path
        self.nx_compare_partitions()

    def nx_compare_partitions(self):

        with open(self.path_to_partitions + "nx_partitions.json", 'r') as fp:
            self.partition_dict = json.load(fp)

        slice_num1 = "1"
        slice_num2 = "2"
        s_1 = self.partition_dict[slice_num1]
        s_2 = self.partition_dict[slice_num2]

        keys_1 = list(s_1.keys())
        keys_2 = list(s_2.keys())
        for i in range(len(keys_1)):
            keys_1[i] = int(keys_1[i])
        
        keys_1 = sorted(keys_1)

        for i in range(len(keys_2)):
            keys_2[i] = int(keys_2[i])

        keys_2 = sorted(keys_2)

        for k1 in keys_1:
            list1 = s_1[str(k1)]
            list2 = s_2[str(k1)]
            result = all(n in list2 for n in list1)
            if not result:
                static_nodes = []
                for n in list1:
                    if n in list2:
                        static_nodes.append(n)

                print(f"Some of the nodes from slice {slice_num1} have moved to another clusters in slice {slice_num2}! This is the case for partition {k1}")
                print(f"Static nodes in partiton are {static_nodes}\n")

