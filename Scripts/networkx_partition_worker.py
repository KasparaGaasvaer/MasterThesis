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

    def __init__(self, path, method):
        self.path_to_partitions = path
        self.path_to_stats_results = "./experiment6/statistics/"
        

        if method == "louvain":
            self.filename_jumpers = "all_slices_partition_jumper_stats_louvain.py"

            with open(self.path_to_partitions + "nx_partitions_louvain.json", 'r') as fp:
                self.partition_dict = json.load(fp)

        if method == "leiden":
            self.filename_jumpers = "all_slices_partition_jumper_stats_leiden.py"

            with open(self.path_to_partitions + "nx_partitions_leiden.json", 'r') as fp:
                self.partition_dict = json.load(fp)

        self.num_total_slices = len(self.partition_dict.keys())

        #self.nx_compare_partitions()
        self.nx_count_jumpers()
        
        

    def nx_compare_partitions(self):


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


    def nx_count_jumpers(self):

        num_jumpers = np.zeros(self.num_total_slices)
        ratio_jumpers_nodes = np.zeros(self.num_total_slices)
        ratio_jumpers_partitions = np.zeros(self.num_total_slices)

        for i in range(1, self.num_total_slices):
            slice_i = str(i)
            slice_ip1 = str(i+1)
            s_i = self.partition_dict[slice_i]
            s_ip1 = self.partition_dict[slice_ip1]

            keys_i = len(s_i.keys())
            keys_ip1 = len(s_ip1.keys())
    
            for k_i in range(keys_i):
                list_i = s_i[str(k_i)]
                list_ip1 = s_ip1[str(k_i)]
                result = all(n in list_ip1 for n in list_i)
                if not result:
                    for n in list_i:
                        if not n in list_ip1:
                            num_jumpers[i] += 1
                
            num_nodes_ip1 = sum(len(v) for v in s_ip1.values())
           # print('NODES',num_nodes_ip1)
            ratio_jumpers_partitions[i] = num_jumpers[i]/keys_ip1
            #print('KEYS',keys_ip1)
            ratio_jumpers_nodes[i] = num_jumpers[i]/num_nodes_ip1

        
        with open(self.path_to_stats_results + self.filename_jumpers,"w") as outfile:
            outfile.write(f'Slice_i to Slice_ip1| Total number of jumpers |  Ratio jumpers/total number of nodes in slice_ip1 | Ratio jumpers/total number of partitions in slice_ip1\n')
            for i in range(1,self.num_total_slices):
                outfile.write(f'       {i}-{i+1:<20} {num_jumpers[i]:<40} {ratio_jumpers_nodes[i]:.6f} {ratio_jumpers_partitions[i]:45.6f}\n')
    
        
