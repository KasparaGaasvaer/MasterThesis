import json, os, time
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
import numpy as np 



class ClusterTracker_SD:
    def __init__(self, path, method):

        self.method = method
        self.path = path 

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

        self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
        if not os.path.exists(self.clusters):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
                expnum = str(expnum) + "_k" + str(k_value)
              
        

        self.path_to_save_stats = self.path + "statistics/" + self.method.title() + "/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/"+ self.method.title() + "/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.filename_tracking_largest = self.path_to_save_stats + "tracking_largest_cluster_SD_" + self.method + ".txt"

        #self.track_largest()
        NL = 10
        #self.plot_track_largest()
        self.compare_N_largest_across_slices(NL)

    def track_largest(self):
        open_time_start = time.perf_counter()
        # 1. Open C-1, identify the one largest cluster, save ID and Size
        # 2. Loop trough all vertices in LC1, identify them in clusters in C-2
        #     -- Either go through all clusters, see how many of the Vs are there, remove them from list, when list is empty stop checking
        #     -- Or for every node check every cluster, then remove nodes from list and stop when list is empty 
        # 3. Store IDs of clusters as keys in dict, value +=1 for every "hit"
        # 4. Identify largest value from dict, store ID as LC2 ,divide by size(LC1)
        # 5. Do the same for LC2 and so on

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())
        print(self.num_slices)

        L_size = 0
        L_idx = "a"

        sim1 = clusters["1"]
        for k in range(len(sim1.keys())):
            num_nodes = len(sim1[str(k)])
            if num_nodes > L_size:
                L_size = num_nodes 
                L_idx = str(k)

        L_vertices = set(sim1[L_idx])
        L_sizes = []
        L_idxs = []
        intersects = []
        inters_3_ids = []
        inters_3 = []
        L_sizes.append(L_size)
        L_idxs.append(L_idx)

        for s in range(2,self.num_slices +1):
            print(s)
            si = clusters[str(s)]

            si_cids = list(si.keys())
            si_hit_dict = {}
            for d in range(len(si_cids)):
                si_hit_dict[si_cids[d]] = 0
            

            for ci in si.keys():
                vi = set(si[ci])
                for v in L_vertices:
                    if v in vi:
                        si_hit_dict[ci] +=1

            max_intersect = max(si_hit_dict, key=si_hit_dict.get)
            max_3_intersects = sorted(si_hit_dict, key=si_hit_dict.get, reverse=True)[:3] #three clusters in i whom contain moste of the nodes from largest cluster in im1
            inters_3_ids.append(max_3_intersects)
            
            inters = []
            for m3 in max_3_intersects:
                inter =  si_hit_dict[m3]/L_size
                inters.append(inter)

            inters_3.append(inters)

            intersect = si_hit_dict[max_intersect]/L_size
            intersects.append(intersect)


            L_idx = max_intersect
            L_size = len(si[L_idx])
            L_vertices = set(si[L_idx])
            L_sizes.append(L_size)
            L_idxs.append(L_idx)


        open_time_end = time.perf_counter()
        print(f"Time spent tracking largest cluster: {open_time_end-open_time_start:0.4f} s")
        with open(self.filename_tracking_largest,"w") as ouf:
            ouf.write("Slice i -> i+1      Cluster ID i,i+1      Cluster size i,i+1                             Intersects                           Intersect ids\n")
            for l in range(len(L_idxs)-1):
                int_3 = inters_3[l]
                int_3_idx = inters_3_ids[l]
                ouf.write(f"{l+1}->{l+2}                     {L_idxs[l]},{L_idxs[l+1]}               {L_sizes[l]},{L_sizes[l+1]}            {int_3[0]},{int_3[1]},{int_3[2]}            {int_3_idx[0]},{int_3_idx[1]},{int_3_idx[2]}\n")     #{intersects[l]}\n")
    
    def compare_N_largest_across_slices(self,N):
        # - Identify N largest clusters in si
        # - Identify N largest clusters in sip1
        # - Compare the N and calculate intersect
        #    - That is, for every cluster we will have N-1 intersects,
        #      the 3 largest are stored as well as which clusters that was,
        #      also their size 0-N
        #  Slice number - Cluster id for i - Cluster id for im1 - Intersect - Sizes for i - Sizes for im1 - Ranked size i - Ranked size im1
        # - Makes file with Sim1->Si [Cid_im10,Cid_im11,Cid_im12] [Cid_i0,Cid_i1,Cid_i2]  [IS_0, IS_1, IS_2] [Sz_im10,Sz_im11,Sz_im12] [Sz_i0,Sz_i1,Sz_i2] [RankSz_im10,RankSz_im11,RankSz_im12] [RankSz_i0,RankSz_i1,RankSz_i2] 

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)
            
        maxN = 3
        self.num_slices = len(clusters.keys())
        print(self.num_slices)

        with open(self.path_to_save_stats + f"finding_{maxN}_largest_intersects_from_{N}_largest_clusters_SD.txt","w") as ouf:
            ouf.write("[Sim1->Si] [Cid_im10,Cid_im11,Cid_im12] [Cid_i0,Cid_i1,Cid_i2] [IS_0, IS_1, IS_2] [Sz_im10,Sz_im11,Sz_im12] [Sz_i0,Sz_i1,Sz_i2] [RankSz_im10,RankSz_im11,RankSz_im12] [RankSz_i0,RankSz_i1,RankSz_i2]\n")
            
            sim1 = clusters["1"]

            L_sizes = []
            L_idxs = []
            for k in range(len(sim1.keys())): 
                num_nodes = len(sim1[str(k)])
                L_sizes.append(num_nodes)
                L_idxs.append(str(k))

            L_sizes, L_idxs = zip(*sorted(zip(L_sizes, L_idxs),reverse = True))
            L_sizes = L_sizes[:N]  #Num nodes in N-largest clusters
            L_idxs = L_idxs[:N]    #IDs of N-largest clusters

            for s in range(2,self.num_slices +1):
                intersect_mat = np.zeros([N,N])
                print(s)
                si = clusters[str(s)]

                Li_sizes = []
                Li_idxs = []
                for k in range(len(si.keys())): 
                    num_nodes = len(si[str(k)])
                    Li_sizes.append(num_nodes)
                    Li_idxs.append(str(k))

                Li_sizes, Li_idxs = zip(*sorted(zip(Li_sizes, Li_idxs),reverse = True))
                Li_sizes = Li_sizes[:N]  #Num nodes in N-largest clusters
                Li_idxs = Li_idxs[:N]    #IDs of N-largest clusters
                
                t_s = time.perf_counter()
                for im1 in range(N):
                    im1_idx = L_idxs[im1]
                    vim1 = set(sim1[im1_idx])
                    for i in range(N):
                        i_idx = Li_idxs[i]
                        vi = set(si[i_idx])

                        inters_n = vim1.intersection(vi)
                        inters_per = len(inters_n)/L_sizes[im1]
                        intersect_mat[im1,i] = inters_per
            

                t_e = time.perf_counter()
                print(f"Time spent comparing is {t_e-t_s:0.4f} s")

                maxN_idx = np.argpartition(intersect_mat, intersect_mat.size - maxN, axis=None)[-maxN:]
                result = np.column_stack(np.unravel_index(maxN_idx, intersect_mat.shape))
                
                lim11,lim12,lim13 = L_idxs[result[0][0]], L_idxs[result[1][0]], L_idxs[result[2][0]]
                li1,li2,li3 = Li_idxs[result[0][1]], Li_idxs[result[1][1]], Li_idxs[result[2][1]]

                lsim11,lsim12,lsim13 = L_sizes[result[0][0]], L_sizes[result[1][0]], L_sizes[result[2][0]]
                lsi1,lsi2,lsi3 = Li_sizes[result[0][1]], Li_sizes[result[1][1]], Li_sizes[result[2][1]]


                final_intersects = [intersect_mat[result[0][0],result[0][1]],intersect_mat[result[1][0],result[1][1]],intersect_mat[result[2][0],result[2][1]]]

                rankim11, rankim12,rankim13 = result[0][0],result[1][0],result[2][0]
                ranki1, ranki2,ranki3 = result[0][1],result[1][1],result[2][1]

                ouf.write(f"{s-1}->{s} {lim11},{lim12},{lim13} {li1},{li2},{li3} {final_intersects[0]},{final_intersects[1]},{final_intersects[2]} {rankim11},{rankim12},{rankim13} {ranki1},{ranki2},{ranki3}\n")  
                
                sim1 = clusters[str(s)]
                L_sizes = Li_sizes
                L_idxs = Li_idxs


    def plot_track_largest(self):
        sizes = []
        intersects = []
        with open(self.filename_tracking_largest,"r") as innf:
            innf.readline()
            lines = innf.readlines()
            for line in lines:
                line = line.split()
                size = line[-3].split(",")[0]
                sizes.append(int(size))
                intersects.append(float(line[-2].split(",")[0]))
            
            last = lines[-1]
            last = last.split()
            size = line[-3].split(",")[-1]
            sizes.append(int(size))

        
        slices = [i for i in range(1,len(sizes)+1)]
        
        plt.plot(slices,sizes, ".k")
        plt.xlabel(r"Slice $S_i$")
        plt.ylabel("Num vertices in cluster")
        plt.title("Size of cluster when tracking largest from slice 1")
        plt.savefig(self.path_to_plots + "size_largest.pdf")
        plt.clf()

        plt.plot(slices[1:],intersects, ".k")
        plt.xlabel(r"Slice $S_i$")
        plt.ylabel(r"Intersect from slice $S_{i-1} \rightarrow S_i$")
        plt.title(r"Intersect of largest cluster $C_{i-1} \rightarrow C_i$")
        plt.savefig(self.path_to_plots + "intersect_largest.pdf")
        plt.clf()