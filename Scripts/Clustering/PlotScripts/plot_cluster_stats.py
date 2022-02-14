import matplotlib.pyplot as plt
import sys
import json
import numpy as np
import os

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up


class PlotClusterStats:
    def __init__(self, path, method):
        
        self.path = path
        self.path_to_stats = path + "statistics/"
        if not os.path.exists(self.path_to_stats):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.path_to_stats = self.path + "statistics/"
            if k_value == "no":
                print("This experiment has no statistics yet")
                sys.exit()


        self.method = method
        self.path_to_plots = self.path + "plots/Clustering/" + self.method.title() + "/"

        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

 
        self.filename_nodes_in_largest_cluster = "largest_partitions_" + self.method + ".txt"
        self.filename_number_of_clusters = "number_partitions_" + self.method + ".txt"
        self.filename_cluster_size_dist = "cluster_size_distribution_" + self.method + ".json"

        self.nodes_in_largest_cluster()
        self.cluster_size_dist()

    def nodes_in_largest_cluster(self):
        clusters = []
        num_nodes = []
        slices = []
        normed = []
        normed_m = []
        with open(
            self.path_to_stats + self.filename_nodes_in_largest_cluster, "r"
        ) as infile:
            infile.readline()
            lines = infile.readlines()
            for line in lines:
                vals = line.split()
                slices.append(int(vals[0]))
                clusters.append(int(vals[1]))
                num_nodes.append(int(vals[2]))
                normed.append(float(vals[3]))
                normed_m.append(float(vals[-1]))

        clusters = np.array(clusters)
        num_nodes = np.array(num_nodes)
        slices = np.array(slices)

        path = self.path_to_plots + "Largest_Cluster/"
        if not os.path.exists(path):
            os.makedirs(path)

        zeros = [0 for i in range(len(clusters))]
        plt.vlines(x=slices, ymin=zeros, ymax=num_nodes, lw=2)
        plt.xlabel("Slice number", fontsize=12)
        plt.ylabel("Number of nodes in largest cluster", fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        plt.savefig(path + "num_nodes_in_largest_cluster.pdf")
        plt.clf()

        plt.vlines(x=slices, ymin=zeros, ymax=normed, lw=2)
        plt.xlabel("Slice number", fontsize=12)
        plt.ylabel(
            "Number of nodes in largest cluster /\nAll nodes in slice", fontsize=12
        )
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        plt.savefig(path + "normalized_num_nodes_in_largest_cluster.pdf")
        plt.clf()

        plt.vlines(x=slices, ymin=zeros, ymax=normed_m, lw=2)
        plt.xlabel("Slice number", fontsize=12)
        plt.ylabel(
            "Number of nodes in largest cluster /\nAll nodes in slice - Num nodes largest",
            fontsize=12,
        )
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        plt.savefig(path + "normalized_m_num_nodes_in_largest_cluster.pdf")
        plt.clf()

    def cluster_size_dist(self):
        with open(self.path_to_stats + self.filename_cluster_size_dist, "r") as fp:
            all_data = json.load(fp)
        
        path = self.path_to_plots + "Cluster_Size_Dist/"
        if not os.path.exists(path):
            os.makedirs(path)
        
        for s in all_data.keys():
            print("Slice ", s)
            data = all_data[s]
            plt.xlabel("Num nodes in cluster", fontsize=14)
            plt.ylabel("Frequency", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.bar(range(len(data)), data)
            plt.yscale("log")
            plt.xscale("log")
            plt.savefig(path + "LOG_cluster_size_distribution_slice" + s + ".pdf")
            plt.clf()

    
