
import os,sys,json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
class LargestClusters:
    def __init__(self, path, method):

        self.method = method
        self.path = path

   
        self.setup()
        self.extract_largest_cluster()
        self.plot_largest_cluster()


    def setup(self):

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

        self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
        if not os.path.exists(self.clusters):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = self.path + "k_" + str(k_value) + "/"
                self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
                expnum = str(expnum) + "_k" + str(k_value)
                
        

        self.path_to_save_stats = self.path + "statistics/Largest_clusters/" + self.method.title() + "/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Largest_clusters/"+ self.method.title() + "/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + self.method.title() + "/"


   
    def extract_largest_cluster(self):

        outfile_name = "stats_LC_Nnodes_Nclusters.txt"

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)
        
        self.num_slices = len(clusters.keys())

        with open(self.path_to_save_stats+outfile_name,"w") as ouf:
            ouf.write(f"[Slice_i] [Largest cluster id] [Largest cluster size] [Num nodes in slice] [Num clusters in slice] [size/nodes] [size/clusters]\n")

            for s in range(1,self.num_slices+1):
                print(s)
                si = clusters[str(s)]

                LC_id = "a"
                LC_size = 0
                num_clusters = len(si.keys())
                num_nodes = 0
                for c in si.keys():
                    cluster = si[c]
                    nodes_in_c = len(cluster)
                    num_nodes += nodes_in_c
                    if nodes_in_c == LC_size:
                        print(f"Two equally large clusters {LC_size}, {nodes_in_c}")
                    if nodes_in_c > LC_size:
                        LC_id = c
                        LC_size = nodes_in_c

                size_div_nodes = LC_size/num_nodes
                size_div_clusters = LC_size/num_clusters

                ouf.write(f"{s} {LC_id} {LC_size} {num_nodes} {num_clusters} {size_div_nodes} {size_div_clusters}\n")
                    


    def plot_largest_cluster(self):

        infile_name = self.path_to_save_stats + "stats_LC_Nnodes_Nclusters.txt"

        slice = []
        c_id = []
        c_size = []
        num_n = []
        num_c = []
        s_div_n = []
        s_div_c = []
        with open(infile_name, "r") as inf:
            inf.readline()
            lines = inf.readlines()
            for line in lines:
                itms = line.split(" ")
                slice.append(int(itms[0]))
                c_id.append(int(itms[1]))
                c_size.append(int(itms[2]))
                num_n.append(int(itms[3]))
                num_c.append(int(itms[4]))
                s_div_n.append(float(itms[5]))
                s_div_c.append(float(itms[6]))


        slice, c_id, c_size, num_n, num_c, s_div_n, s_div_c = np.array(slice), np.array(c_id), np.array(c_size), np.array(num_n), np.array(num_c), np.array(s_div_n), np.array(s_div_c)  

        
        #Plot size/nodes
        plt.plot(slice, s_div_n,".k")
        plt.ylabel(r"$\frac{\text{Largest cluster}}{\text{Nodes in slice}}$", fontsize=16)
        plt.xlabel("Slice", fontsize=14)
        plt.savefig(self.path_to_plots + "LC_div_Nnodes.pdf")
        plt.savefig(self.path_to_overleaf_plots + "LC_div_Nnodes.pdf")
        plt.clf()

        #plot size/clusters
        plt.plot(slice, s_div_c,".k")
        plt.ylabel(r"$\frac{\text{Largest cluster}}{\text{Clusters in slice}}$", fontsize=16)
        plt.xlabel("Slice", fontsize=14)
        plt.savefig(self.path_to_plots + "LC_div_Nclusters.pdf")
        plt.savefig(self.path_to_overleaf_plots + "LC_div_Nclusters.pdf")
        plt.clf()

        #plot size
        plt.plot(slice, c_size,".k")
        plt.ylabel("Size of largest cluster", fontsize=16)
        plt.xlabel("Slice", fontsize=14)
        plt.savefig(self.path_to_plots + "LC_size.pdf")
        plt.savefig(self.path_to_overleaf_plots + "LC_size.pdf")
        plt.clf()
        

        #mean_LC_div_n = np.mean(s_div_n)
        #std_LC_div_n = np.std(s_div_c)
        #print(f"mean : {mean_LC_div_n}, std : {std_LC_div_n}")

        #standard_error = np.std(s_div_c)/np.sqrt(len(s_div_c))
        #plt.errorbar(slice, s_div_n, yerr=standard_error, capsize=2, fmt = ".k")
        #plt.savefig(self.path_to_plots + "TEST.pdf")


        






