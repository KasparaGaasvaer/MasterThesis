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
        self.path_to_stats = path + "statistics/partition_worker/"
        self.method = method
        self.path_to_plots = self.path + "plots/Clustering/Plot_cluster_stats/" + self.method.title() + "/"
        self.path_to_overleaf = "./p_2_overleaf/" + self.path.strip("./") + "/" + self.method.title() + "/"

        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

 
        self.filename_nodes_in_largest_cluster = "largest_partitions_" + self.method + ".txt"
        self.filename_number_of_clusters = "number_partitions_" + self.method + ".txt"
        self.filename_cluster_size_dist = "cluster_size_distribution_" + self.method + ".json"

        #self.nodes_in_largest_cluster()
        #self.cluster_size_dist_experiment()
        #self.cluster_size_dist()
        self.plot_combined_cluster_size_dist()

        

    def nodes_in_largest_cluster(self):
        print("Nodes in Largest Cluster")
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


    def cluster_size_dist_experiment(self):
        print("Cluster Size Dist Experiment\n")
        with open(self.path_to_stats + self.filename_cluster_size_dist, "r") as fp:
            all_data = json.load(fp)
        
        path = self.path_to_plots + "Cluster_Size_Dist/all_slices/"
        if not os.path.exists(path):
            os.makedirs(path)

        dist = all_data["1"]
  
        for k in range(1,len(all_data.keys())+1):
            ks = str(k)
            
            new_dist = all_data[ks]

            diff = len(dist)-len(new_dist) # = 0 if same lenght, < 0 if new dist is larger, > 0 if old dist is larger

            if diff < 0:
                for m in range(abs(diff)):
                    dist.append(0)
            
            if diff > 0:
                for m in range(diff):
                    new_dist.append(0)

            dist = [sum(x) for x in zip(dist, new_dist)]
        

        plt.xlabel("Num nodes in cluster", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.bar(range(len(dist)), dist)
        plt.savefig(path + "cluster_size_distribution.pdf")
        plt.yscale("log")
        plt.savefig(path + "yLOG_cluster_size_distribution_slice.pdf")
        plt.xscale("log")
        plt.savefig(path + "LOG_cluster_size_distribution.pdf")
        plt.clf()


        


    def cluster_size_dist(self):
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
            int_nums = np.array(int_nums)/num_slices    #Since num nodes is the sum over all slices
            comp_order[m][1].append(np.sum(int_nums))

            plt.plot(int_sizes,int_nums,".",label = f"{m.title()}")

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


        #in_ax = fig.add_axes([.45, .35, .4, .4], facecolor='white')

        plt.savefig(path_to_these_plots + "cluster_size_vs_num_nodes_ALL_METHODS.pdf")
        plt.savefig(this_path_to_overleaf + "cluster_size_vs_num_nodes_ALL_METHODS.pdf")
        plt.clf()


        leiden,louvain,lprop = np.array(comp_order["leiden"][0])/comp_order["leiden"][1][0], np.array(comp_order["louvain"][0])/comp_order["louvain"][1][0], np.array(comp_order["lprop"][0])/comp_order["lprop"][1][0]

        """
        le_lo = leiden - louvain 
        le_lp = leiden - lprop
        lo_lp = louvain - lprop

        ref_dict = {
            "Leiden - Louvain" : [le_lo,"forestgreen"],
            "Leiden - Label Propagation" : [le_lp,"cornflowerblue"],
            "Louvain - Label Propagation": [lo_lp, "gold"]
        }
        """

        new_labels = ["1-9", "10-99", "100-999", "1000-"]
        new_ax_vals = [1, 2, 3, 4]
    
        ref_dict = {
            "Leiden" : [leiden,"forestgreen"],
            "Label Propagation" : [lprop,"cornflowerblue"],
            "Louvain": [louvain, "gold"]
        }

        lw = 20
        for oo in range(len(leiden)):
            vals = []
            keyss = []
            for k in ref_dict.keys():
                vals.append(abs(ref_dict[k][0][oo]))
                keyss.append(k)
            
            vals, keyss = zip(*sorted(zip(vals,keyss),reverse = True))
            for nk in keyss:
                plt.vlines(x = new_ax_vals[oo], ymin=0, ymax=abs(ref_dict[nk][0][oo]), color=ref_dict[nk][1],linewidth=lw, label = nk)

            if oo == 0:
                plt.legend([keyss[0],keyss[1], keyss[2]], fontsize = fz-2)

        plt.xticks(new_ax_vals, new_labels, fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.xlabel("Cluster sizes", fontsize = fz)
        plt.ylabel("Nodes in size-bin / total nodes", fontsize = fz)
        plt.yscale("log")
        plt.savefig(path_to_these_plots + "cluster_size_vs_percent_nodes_ALL_METHODS.pdf")
        plt.savefig(this_path_to_overleaf + "cluster_size_vs_percent_nodes_ALL_METHODS.pdf")
        plt.clf()

        """
        for oo in range(len(leiden)):
            vals = []
            keyss = []
            for k in ref_dict.keys():
                vals.append(abs(ref_dict[k][0][oo]))
                keyss.append(k)
            
            vals, keyss = zip(*sorted(zip(vals,keyss),reverse = True))
            for nk in keyss:
                plt.vlines(x = new_ax_vals[oo], ymin=0, ymax=abs(ref_dict[nk][0][oo]), color=ref_dict[nk][1],linewidth=lw, label = nk)


            #plt.vlines(x = new_ax_vals[oo], ymin=0, ymax=abs(le_lo[oo]), color='forestgreen',linewidth=20)
            #plt.vlines(x = new_ax_vals[oo], ymin=0, ymax=abs(le_lp[oo]), color='cornflowerblue',linewidth=20)
            #plt.vlines(x = new_ax_vals[oo], ymin=0, ymax=abs(lo_lp[oo]), color='gold', linewidth=20)

            if oo == 0:
                plt.legend([keyss[0],keyss[1], keyss[2]], fontsize = fz-2)

        #plt.legend() #Just tested if i got the right labels + color combo each time
        plt.xticks(new_ax_vals, new_labels, fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.xlabel("Cluster sizes", fontsize = fz)
        plt.ylabel("Absolute difference in number of nodes", fontsize = fz)
        plt.yscale("log")
        plt.savefig(path_to_these_plots + "cluster_size_vs_diff_nodes_ALL_METHODS.pdf")
        plt.savefig(this_path_to_overleaf + "cluster_size_vs_diff_nodes_ALL_METHODS.pdf")
        plt.clf()
        """


    
