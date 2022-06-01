import json, os
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np 



class CompareMethods:
    def __init__(self, path_to_experiment):

        self.path = path_to_experiment

        self.path_to_stats = self.path + "statistics/"
        self.path_to_dicts = self.path + "parsed_dictionaries/"

        self.path_to_results = self.path + "plots/CompareMethods/"
        self.path_to_save_stats = self.path_to_stats + "CompareMethods/"
        self.path_to_results_overleaf = "p_2_overleaf/" +self.path.strip("./") + "/CompareMethods/"

        if not os.path.exists(self.path_to_results):
            os.makedirs(self.path_to_results)

        if not os.path.exists(self.path_to_results_overleaf):
            os.makedirs(self.path_to_results_overleaf)

        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)
        
        self.methods = ["leiden", "louvain", "lprop"]

        self.cmap = cm.get_cmap('plasma')
        self.colors = {"leiden":self.cmap(0), "louvain":self.cmap(0.5), "lprop":self.cmap(0.8)}


    
    def size_largest_clusters(self):
        # one plot with only relative largest
        # one plot with small plot of top 10% largest clusters

        pn_largest = "n_in_largest_c_vs_num_n_in_slice.pdf"
        pn_N_largest = "n_in_N_largest_c_vs_num_n_in_slice.pdf"

        # Calculate top 10% of cluster sizes
        # get list of all idx ! = 0 from cluster_size_dist

        info_dict = {}
    
        for method in self.methods:
            info_dict[method] = {}
            info_dict[method]["nn_top_10"] = []
            info_dict[method]["nn_top_1"] = []
            info_dict[method]["nn_tot"] = []
            

            with open(self.path_to_stats + f"partition_worker/cluster_size_distribution_{method}.json","r") as inff:
                cs_dist = json.load(inff)

            for slice in cs_dist.keys():
                slice_dist = np.array(cs_dist[slice])
                total_num_nodes_in_slice = 0
                for j in range(len(slice_dist)):
                    total_num_nodes_in_slice += j*slice_dist[j]

                cluster_sizes = np.where(slice_dist != 0)[0]
                sorted_sizes = sorted(cluster_sizes)
                cut_off = int(np.ceil(len(sorted_sizes)/10))
                sizes = sorted_sizes[-cut_off:]  #size of clusters accepted as 10% largest in slice

                nn_10 = 0
                for i in sizes:
                    nn_10 += i*slice_dist[i]   # i = size of cluster, slice_dist[i] = num clusters with that size, i*slice_dist[i] = num nodes in all those clusters

                nn_1L = slice_dist[-1]*(len(slice_dist)-1)
                nn_1L = nn_1L.item()
                nn_10 = nn_10.item()
                total_num_nodes_in_slice = total_num_nodes_in_slice.item()
        
                info_dict[method]["nn_top_10"].append(nn_10)
                info_dict[method]["nn_top_1"].append(nn_1L)
                info_dict[method]["nn_tot"].append(total_num_nodes_in_slice)


        with open(self.path_to_save_stats + "size_largest_clusters.json","w") as ouff:
            json.dump(info_dict,ouff)

    
    def plot_size_largest_clusters(self):

        with open(self.path_to_save_stats + "size_largest_clusters.json","r") as inff:
            info_dict = json.load(inff)

        num_slices = len(info_dict[self.methods[0]]["nn_tot"])
        slices_ref = [s+1 for s in range(num_slices)]

        
        plot_dict = {
            "leiden" : ["Leiden", self.colors["leiden"]],
            "lprop" : ["Label Propagation", self.colors["lprop"]],
            "louvain": ["Louvain", self.colors["louvain"]]
        }

        # Top 1
        top_size = {
            "leiden" : [["Leiden", self.colors["leiden"]],[],[]],
            "lprop" : [["Label Propagation", self.colors["lprop"]],[],[]],
            "louvain": [["Louvain", self.colors["louvain"]],[],[]]
        }

        for method in self.methods:
            top = info_dict[method]["nn_top_1"]
            all_n = info_dict[method]["nn_tot"]
            for i in range(len(top)):
                top_size[method][1].append(top[i]/all_n[i])

            plt.plot(slices_ref,top_size[method][1],".",color = plot_dict[method][1], label = plot_dict[method][0])
        
        plt.legend()
        plt.xlabel("Slice")
        #plt.ylabel("Vertices in largest cluster / vertices in slice")
        plt.ylabel("Fraction of vertices in largest cluster")
        plt.savefig(self.path_to_results + "rel_size_largest_c.pdf")
        plt.savefig(self.path_to_results_overleaf + "rel_size_largest_c.pdf")
        plt.clf()


        for method in self.methods:
            top = info_dict[method]["nn_top_10"]
            all_n = info_dict[method]["nn_tot"]
            for i in range(len(top)):
                top_size[method][2].append(top[i]/all_n[i])

            plt.plot(slices_ref,top_size[method][2],".",color = plot_dict[method][1], label = plot_dict[method][0])
        
        plt.legend()
        plt.xlabel("Slice")
        #plt.ylabel("Vertices in 10% largest clusters / vertices in slice")
        plt.ylabel("Fraction of vertices in top 10% largest clusters")
        plt.savefig(self.path_to_results + "rel_size_top10p_largest_c.pdf")
        plt.savefig(self.path_to_results_overleaf + "rel_size_top10p_largest_c.pdf")
        plt.clf()


         

        #for slice in range(num_slices):



        


        




                



