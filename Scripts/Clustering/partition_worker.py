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
    
        #self.identify_largest_cluster()
        #self.extract_number_of_clusters()
        #self.extract_cluster_size_dist()
        #self.extract_combined_total_size_dists()
        self.fit_cluster_size_dist()

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


    def fit_cluster_size_dist(self):
        """Fit distribution of cluster sizes as exponential
        """
        from scipy.optimize import curve_fit

        with open(self.path_to_stats_results + self.filename_cluster_size_dist,"r") as inff:
            dist_dict = json.load(inff)

        f_exp = lambda x,a,b: np.exp(a*x + b)
        fit_var = {}

        for s in dist_dict.keys():

            slice = dist_dict[s]
            print(s)

            freq = np.array(slice)
            sizes = np.where(freq != 0)
            
                
            freq = freq[sizes]
            if s == "68":
                print(freq)
            sizes = sizes[0]

            popt, pcov = curve_fit(f_exp, sizes, freq, maxfev = 2000)
            fit_var[s] = [popt[0],popt[1]]

            if s == "1":
                #plt.plot(sizes, f_exp(sizes, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
                print(popt)
                plt.plot(sizes, freq, "*",label = "Datapoints")
                plt.legend()
                plt.xlabel("Sizes")
                plt.ylabel("Frequency")
                plt.savefig(f"s{s}_test_{self.method}.pdf")
                plt.clf()

        
        with open(self.path_to_stats_results + f"dist_fit_variables_{self.method}.json","w") as ouf:
            json.dump(fit_var,ouf)


            #plt.plot(sizes, f_exp(sizes, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
            # print(popt)
            # plt.plot(sizes, freq, "*",label = "Datapoints")
            # plt.legend()
            # plt.xlabel("Sizes")
            # plt.ylabel("Frequency")
            # plt.savefig("lol_test.pdf")
            # plt.clf()
            #print(freq)
            
            #log_freq = np.log(freq)
            #log_size = np.log(sizes)

            #plt.plot(log_size,log_freq,"*")
            #plt.savefig("lol_test.pdf")
            #plt.clf()

            # exps = np.polyfit(sizes,log_freq, deg = 1)
            # plt.plot(sizes, freq)
            # plt.plot(sizes, np.exp(exps[1])*np.exp(exps[0]*sizes))
            # plt.savefig("lol_test.pdf")
            # plt.clf()
            #print(slice)
    



    def extract_combined_total_size_dists(self):
        methods = ["leiden", "louvain", "lprop"]
        comb_dict = {}
        for m in methods:
            comb_dict[m] = {}
            with open(self.path_to_stats_results + f"cluster_size_distribution_{m}.json", "r") as inff:
                m_dict = json.load(inff)

            for s in m_dict.keys():   #Loop over all slices
                slice = m_dict[s]     #Extract list where idx = size, value = num clusters with that size
                num_sizes = len(slice)
                for size in range(num_sizes):  #Loop over all indices/sizes 
                    num_clusters = slice[size]
                    if num_clusters > 0:
                        try:
                            comb_dict[m][str(size)] += slice[size]  #If already exists add on
                        except KeyError:
                            comb_dict[m][str(size)] = slice[size]   #If new idx make new


        with open(self.path_to_stats_results + "cluster_size_distribution_all_slices_all_methods.json", "w") as ouf:
            json.dump(comb_dict,ouf)



          



