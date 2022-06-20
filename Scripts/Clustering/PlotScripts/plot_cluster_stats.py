import matplotlib.pyplot as plt
from matplotlib import cm
import sys
import json
import numpy as np
import os
from scipy.optimize import curve_fit

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up


class PlotClusterStats:
    def __init__(self, path, method):
        """Constructor. Sets global paths and filenames.

        Args:
            path (string): Path to experiment folder.
            method (string): Name of chosen community detection algorithm. 
        """
        
        self.path = path
        self.path_to_stats = path + "statistics/partition_worker/"
        self.method = method
        self.path_to_plots = self.path + "plots/Clustering/Plot_cluster_stats/" + self.method.title() + "/"
        self.path_to_overleaf = "./p_2_overleaf/" + self.path.strip("./") + "/" + self.method.title() + "/"

        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

 
        self.filename_nodes_in_largest_cluster = "largest_partitions_" + self.method + ".txt"
        self.filename_number_of_clusters = "number_partitions_" + self.method + ".txt"
        self.filename_cluster_size_dist = "cluster_size_distribution_" + self.method + ".json"
        

    def nodes_in_largest_cluster(self):
        """Method for retrieving and plotting node distributions. 
        """
      
        clusters = []
        num_nodes = []
        slices = []
        normed = []
        normed_m = []
        with open(self.path_to_stats + self.filename_nodes_in_largest_cluster, "r") as infile:
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

        path = self.path_to_plots + "Plot_cluster_stats/Nodes_in_largest_cluster/"
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
        """Method for retrieving and plotting cluster size distributions.
        """
        with open(self.path_to_stats + self.filename_cluster_size_dist, "r") as fp:
            all_data = json.load(fp)
        
        path = self.path_to_plots + "Cluster_Size_Dist/"
        if not os.path.exists(path):
            os.makedirs(path)

        loglog_path = path + "LOGLOG/"
        if not os.path.exists(loglog_path):
            os.makedirs(loglog_path)

        nolog_path = path + "not_scaled/"
        if not os.path.exists(nolog_path):
            os.makedirs(nolog_path)
        
        ylog_path = path + "y_LOG/"
        if not os.path.exists(ylog_path):
            os.makedirs(ylog_path)
        
        for s in all_data.keys():
            print("Slice ", s)
            data = all_data[s]
            
            plt.xlabel("Num nodes in cluster", fontsize=14)
            plt.ylabel("Frequency", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.bar(range(len(data)), data)
            plt.savefig(nolog_path + "cluster_size_distribution_slice" + s + ".pdf")
            plt.yscale("log")
            plt.savefig(ylog_path + "yLOG_cluster_size_distribution_slice" + s + ".pdf")
            plt.xscale("log")
            plt.savefig(loglog_path + "LOG_cluster_size_distribution_slice" + s + ".pdf")
            plt.clf()

    
    def plot_combined_cluster_size_dist(self):
        """Method for retrieving and plotting cluster size distributions for all methods combined.
        """
        path_to_these_plots = self.path + "plots/Clustering/Plot_cluster_stats/"
        this_path_to_overleaf = "./p_2_overleaf/" + self.path.strip("./") + "/"
        print("\n NEW EXP \n")
        with open(self.path_to_stats + "cluster_size_distribution_leiden.json","r") as test_f:
            reference_dict = json.load(test_f)

        num_slices = len(reference_dict.keys())

        with open(self.path_to_stats + "cluster_size_distribution_all_slices_all_methods.json","r") as inff:
            comb_dict = json.load(inff)


        comp_order = {}
        orders = [1, 10, 10**2, 10**3, 10**18] 
  
        cmap = cm.get_cmap('plasma')
        color_dict = {"leiden":cmap(0), "louvain":cmap(0.5), "lprop":cmap(0.8)}

        fz = 14
        for m in comb_dict.keys():
            comp_order[m] = [[],[]]
            m_dict = comb_dict[m]
            sizes = m_dict.keys()
            int_sizes = []
            int_nums = []
            for s in sizes:
                int_sizes.append(int(s))
                int_nums.append(int(m_dict[s]))

            int_sizes, int_nums = zip(*sorted(zip(int_sizes,int_nums)))
            int_sizes = np.array(int_sizes)
            int_nums = np.array(int_nums)/num_slices    #Num nodes is the sum over all slices
            comp_order[m][1].append(np.sum(int_nums))
            f = lambda x,a,b: a*x**(b)

            popt, pcov = curve_fit(f, int_sizes[1:], int_nums[1:])
            plt.scatter(int_sizes,int_nums, color = color_dict[m], label = f"{m.title()}")
        
            for o in range(len(orders)-1):
                start = np.where(orders[o] <= int_sizes)[0][0]
                end = np.where(int_sizes < orders[o+1])[0][-1]
                comp_order[m][0].append(np.sum(int_nums[start:end+1]))
        
            


        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Cluster size", fontsize = fz)
        plt.ylabel("Mean number of clusters", fontsize = fz)
        plt.xticks(fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.legend(fontsize = fz)

        plt.savefig(path_to_these_plots + "cluster_size_vs_num_clusters_ALL_METHODS.pdf")
        plt.savefig(this_path_to_overleaf + "cluster_size_vs_num_clusters_ALL_METHODS.pdf")
        plt.clf()


        leiden,louvain,lprop = np.array(comp_order["leiden"][0])/comp_order["leiden"][1][0], np.array(comp_order["louvain"][0])/comp_order["louvain"][1][0], np.array(comp_order["lprop"][0])/comp_order["lprop"][1][0]
        

        new_labels = ["1-9", "10-99", "100-999", "1000-"]
        
        X_axis = np.arange(len(new_labels))
        
        plt.bar(X_axis, leiden, 0.2,label = "Leiden", color = color_dict["leiden"])
        plt.bar(X_axis - 0.2, louvain, 0.2, label = 'Louvain', color = color_dict["louvain"])
        plt.bar(X_axis + 0.2, lprop, 0.2, label = 'Label Propagation', color = color_dict["lprop"])
        
        plt.xticks(X_axis, new_labels, fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.xlabel("Size bins", fontsize =fz)
        plt.ylabel("Fraction of total number of clusters", fontsize = fz)
        plt.yscale("log")
        plt.legend(fontsize = fz)
        plt.tight_layout()
        plt.savefig(path_to_these_plots + "cluster_size_vs_percent_clusters_ALL_METHODS_separate.pdf")
        plt.savefig(this_path_to_overleaf + "cluster_size_vs_percent_clusters_ALL_METHODS_separate.pdf")
        plt.clf()

      


    
