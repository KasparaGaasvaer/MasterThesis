import networkx as nx
import numpy as np
import pandas as pd
import os
import sys
import copy
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

from Utils.dict_opener import OpenDict

class PartitionWorker():
    def __init__(self, path, method):
        """[summary]

        Args:
            path (string): [description]
            method (string): [description]
        """
        self.path = path
        self.path_to_partitions = path + "parsed_dictionaries/"
        if not os.path.exists(self.path_to_partitions):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.path_to_partitions= self.path + "parsed_dictionaries/"
            if k_value == "no":
                print("This experiment has no parsed dictionaries yet")
                sys.exit()

        OpenDicts = OpenDict(self.path)
        self.path_to_stats_results = self.path + "statistics/partition_worker/"
        if not os.path.exists(self.path_to_stats_results):
            os.makedirs(self.path_to_stats_results)
      
        self.method = method
        self.filename_largest_partition = "largest_partitions_" + self.method + ".txt"
        self.filename_num_partitions = "number_partitions_" + self.method +".txt"
        self.filename_cluster_size_dist = "cluster_size_distribution_" + self.method + ".json"

        self.partition_dict = OpenDicts.open_dicts(["part_" + self.method])

        self.num_total_slices = len(self.partition_dict.keys())

        #self.compare_partitions()
        self.identify_largest_cluster()
        self.extract_number_of_clusters()
        self.extract_cluster_size_dist()

    def compare_partitions(self):
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

                print(
                    f"Some of the nodes from slice {slice_num1} have moved to another clusters in slice {slice_num2}! This is the case for partition {k1}"
                )
                print(f"Static nodes in partiton are {static_nodes}\n")

    def identify_largest_cluster(self):
        largest_partitions = []
        number_of_nodes = []
        total_num_nodes = []
        for slice in self.partition_dict.keys():
            s = self.partition_dict[slice]
            all_nodes = 0
            for vals in s.values():
                all_nodes += len(vals)
            max_nodes = max(len(vals) for vals in s.values())
            part = [key for key, value in s.items() if len(value) == max_nodes]
            part = part[0]
            largest_partitions.append(part)
            number_of_nodes.append(max_nodes)
            total_num_nodes.append(all_nodes)

        sttr = " "
        with open(self.path_to_stats_results + self.filename_largest_partition, "w") as outfile:
            outfile.write("Slice        Partition num         Num nodes         Num nodes/Total num nodes         Num nodes/(Total num nodes - Num nodes)\n")
            s = 1
            for i in range(len(largest_partitions)):
                p = largest_partitions[i]
                n = number_of_nodes[i]
                t = total_num_nodes[i]
                outfile.write(f"{s:>2}{p:>18}{n:>21}{sttr:<20s}{n/t:.6f}{sttr:<20s}{n/(t-n):.6f}\n")
                s += 1

    def extract_number_of_clusters(self):
        slices = []
        num_clusters = []
        for slice in self.partition_dict.keys():
            s = self.partition_dict[slice]
            n_clusters = len(s.keys())
            slices.append(slice)
            num_clusters.append(n_clusters)

        with open(self.path_to_stats_results + self.filename_num_partitions, "w") as outfile:
            outfile.write("Slice num         Num partitions\n")
            for s, c in zip(slices, num_clusters):
                outfile.write(f"    {s:20}{c}\n")

    def extract_cluster_size_dist(self):
        """ Produces dict with key = slice number, value = list where index is size and value is number of clusters with that size """
        slices = {}
        for slice in self.partition_dict.keys():
            s = self.partition_dict[slice]
            max_nodes = max(len(vals) for vals in s.values())
            slices[slice] = [0] * (max_nodes + 1)
            for k in s.keys():
                n = len(s[k])
                slices[slice][n] += 1

        with open(self.path_to_stats_results + self.filename_cluster_size_dist, "w") as fp:
            json.dump(slices, fp)



