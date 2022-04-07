import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import json
import os

def plot_size_largest_cluster_louvain():
    paths = ["../experiment600/experiment_600/parsed_dictionaries/partitions_louvain.json", "../experiment800/experiment_800/parsed_dictionaries/partitions_louvain.json", "../experiment7/parsed_dictionaries/partitions_louvain.json", "../experiment6/parsed_dictionaries/partitions_louvain.json", "../experiment8/parsed_dictionaries/partitions_louvain.json", "../experiment9/parsed_dictionaries/partitions_louvain.json"]

    for p in paths:
        with open(p, "r") as inf:
            clusters = json.load(inf)

        slices = []
        #all_L_id = []
        all_L_sz = []

        for k in clusters.keys():
            slices.append(int(k))
            s = clusters[k]
            #largest_cluster_id = "a"
            largest_cluster_size = 0
            for kk in s.keys():
                c = s[kk] 
                if len(c) > largest_cluster_size:
                    largest_cluster_size = len(c)
                    #largest_cluster_id = kk

            #all_L_id.append(largest_cluster_id)
            all_L_sz.append(largest_cluster_size)
    
        path_whole  = p.split("parsed_dictionaries")[0]
        plot_name = path_whole + "plots/Clustering/Louvain/size_of_largest_cluster_in_slices.pdf"
        plot_name_overleaf = "./p_2_overleaf" + path_whole.strip(".") + "Louvain/size_of_largest_cluster_in_slices.pdf"
     
        plt.plot(slices,all_L_sz,"k.")
        plt.xlabel("Slice number")
        plt.ylabel("Size of largest cluster")
        plt.savefig(plot_name)
        plt.savefig(plot_name_overleaf)
        plt.clf()

def plot_size_largest_cluster_leiden():
    paths = ["../experiment600/experiment_600/parsed_dictionaries/partitions_leiden.json", "../experiment800/experiment_800/parsed_dictionaries/partitions_leiden.json", "../experiment7/parsed_dictionaries/partitions_leiden.json", "../experiment6/parsed_dictionaries/partitions_leiden.json", "../experiment8/parsed_dictionaries/partitions_leiden.json", "../experiment9/parsed_dictionaries/partitions_leiden.json"]

    for p in paths:
        with open(p, "r") as inf:
            clusters = json.load(inf)

        slices = []
        #all_L_id = []
        all_L_sz = []

        for k in clusters.keys():
            slices.append(int(k))
            s = clusters[k]
            #largest_cluster_id = "a"
            largest_cluster_size = 0
            for kk in s.keys():
                c = s[kk] 
                if len(c) > largest_cluster_size:
                    largest_cluster_size = len(c)
                    #largest_cluster_id = kk

            #all_L_id.append(largest_cluster_id)
            all_L_sz.append(largest_cluster_size)
    
        path_whole  = p.split("parsed_dictionaries")[0]
        plot_name = path_whole + "plots/Clustering/Leiden/size_of_largest_cluster_in_slices.pdf"
        plot_name_overleaf = "./p_2_overleaf" + path_whole.strip(".") + "Leiden/size_of_largest_cluster_in_slices.pdf"
        """
        fig, ax = plt.subplots()
        ax.scatter(slices, all_L_sz)

        for i, txt in enumerate(all_L_id):
            ax.annotate(txt, (slices[i], all_L_sz[i]))

        plt.savefig(plot_name)
        plt.clf()
        """
        plt.plot(slices,all_L_sz,"k.")
        plt.xlabel("Slice number")
        plt.ylabel("Size of largest cluster")
        plt.savefig(plot_name)
        plt.savefig(plot_name_overleaf)
        plt.clf()

def plot_size_largest_cluster_java():
    paths = ["../experiment100/parsed_dictionaries/Clusters/","../experiment12/experiment_12/k_400/parsed_dictionaries/Clusters/","../experiment12/experiment_12/k_600/parsed_dictionaries/Clusters/", "../experiment12/experiment_12/k_800/parsed_dictionaries/Clusters/"]


    for p in paths:
        num_slices = len(os.listdir(p))

        slices = []
        all_L_sz = []
        for ss in range(1,num_slices+1):
            with open(p + "c_" + str(ss) + ".json", "r") as inf:
                s = json.load(inf)                               #open slice i 

            slices.append(int(ss))
            largest_cluster_size = 0

            for cnum in s.keys():                                #loop through clusters in slice 1
                c = s[cnum]["uid"] 
                if len(c) > largest_cluster_size:
                    largest_cluster_size = len(c)
        
            all_L_sz.append(largest_cluster_size)
        
        path_whole  = p.split("parsed_dictionaries")[0]
        plot_name = path_whole + "plots/Clustering/Java/size_of_largest_cluster_in_slices.pdf"
        plot_name_overleaf = "./p_2_overleaf" + path_whole.strip(".") + "LabelProp/size_of_largest_cluster_in_slices.pdf"
        
        plt.plot(slices,all_L_sz,"k.")
        plt.xlabel("Slice number")
        plt.ylabel("Size of largest cluster")
        plt.savefig(plot_name)
        plt.clf()


plot_size_largest_cluster_leiden()
plot_size_largest_cluster_java()
plot_size_largest_cluster_louvain()