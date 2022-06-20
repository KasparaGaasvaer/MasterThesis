import json, os, time
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
import numpy as np 

# ==============================Cluster Tracker==============================

#Class containing a variety of methods for tracking the movement/dispersion of large clusters.

class ClusterTracker:
    
    def __init__(self, path, method):
        """Constructor. Sets global paths and filenames.

        Args:
            path (string): Path to experiment.
            method (string): Chosen method for community detection.
        """

        self.method = method
        self.path = path 

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

        self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
  
        self.path_to_save_stats = self.path + "statistics/Cluster_tracker/" + self.method.title() + "/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Cluster_tracker/"+ self.method.title() + "/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + self.method.title() + "/"

        self.filename_tracking_largest = self.path_to_save_stats + "tracking_largest_cluster_SD_" + self.method + ".txt"


    def track_reid_largest_from_im12i(self):
        """Method for tracking the largest clusters between slices.
         Produces plots where a shift in color indicates that the largest cluster in slice i is not the same as the larges cluster in slice im1. 
        """
     
        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())

        all_intersects = []
        all_ids = []
        colours = ["r","b","k","c","g","y","m"]
        color_id = 0
        match_counter = []

        L_size = 0
        L_idx = "a"

        sim1 = clusters["1"]
        for k in range(len(sim1.keys())):
            num_nodes = len(sim1[str(k)])
            if num_nodes > L_size:
                L_size = num_nodes 
                L_idx = str(k)

        L_vertices = set(sim1[L_idx])
        L_size = len(L_vertices)


        for s in range(2,self.num_slices +1):
            print(s)
            si = clusters[str(s)]
            match_idx = "a"
            Li_size = 0
            Li_idx = "a"
            max_intersect = 0

            for k_i in si.keys():
                ci = set(si[k_i])
                c_sz = len(ci)
                intersect_n = L_vertices.intersection(ci)
                intersect_per = len(intersect_n)/L_size 
                if intersect_per > max_intersect:
                    max_intersect = intersect_per
                    match_idx = k_i
                if c_sz > Li_size:
                    Li_size = c_sz
                    Li_idx = k_i

            
            all_intersects.append(max_intersect)
            all_ids.append(match_idx)
            if match_idx != Li_idx:                 # If the one with most intersect is not the largest, then the plot will change color.
                color_id+=1                         # This means that from the next iteration we will be comparing it to another cluster.
                print("Another cluster became the largest")
                if color_id == 7:
                    color_id = 0

            match_counter.append(color_id)

            sim1 = si 
            L_vertices = set(sim1[Li_idx])
            L_idx = Li_idx 
            L_size = len(L_vertices)


        slices_nums = [i for i in range(2,self.num_slices+1)]
        for i in range(len(slices_nums)):
            plt.scatter(slices_nums[i],all_intersects[i],color = colours[match_counter[i]])
        plt.xlabel("Slice")
        plt.ylabel("Intersect")
        plt.savefig(self.path_to_plots + "Largest_intersect_when_comparing_largest_cluster_in_slice_im1_with_all_clusters_in_slice_i.pdf")
        plt.savefig(self.path_to_overleaf_plots + "Largest_intersect_when_comparing_largest_cluster_in_slice_im1_with_all_clusters_in_slice_i.pdf")

                
    def track_largest(self):
        """ TRACKING THE LARGEST FROM SLICE 1 AND OUT. NOT FINDING LARGEST IN NEXT BUT USING THE ONE WITH MOST INTERSECT.

         - Identifies the largest cluster in slice 1 (C1).
         - Loops trough all vertices in C1, identifies them in clusters in slice 2.
         - Identifies the cluster with the most intersect in slice 2 (C2)
         - Loops trough all vertices in C2, identifies them in clusters in slice 3.
         ...
         - Identifies the cluster with the most intersect in slice S-1 (CS-1)
         - Loops trough all vertices in CS-1, identifies them in clusters in slice S.
         """

        open_time_start = time.perf_counter()
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
            intersects_arr = np.zeros(len(si.keys()))

            for ci in si.keys():
                vi = set(si[ci])
                inters = L_vertices.intersection(vi)
                intersects_arr[int(ci)] = len(inters)/L_size

            max_intersect = np.max(intersects_arr)
            max_intersect_id = np.argmax(intersects_arr)
            max_3_intersects = sorted(intersects_arr, reverse = True)[:3]
            max_3_intersect_ids = []
            for i3 in max_3_intersects:
                id3 = np.where(intersects_arr == i3)[0][0]
                max_3_intersect_ids.append(id3)

            inters_3_ids.append(max_3_intersect_ids)
            inters_3.append(max_3_intersects)
            intersects.append(max_intersect)
            
     
            L_idx = str(max_intersect_id)
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
                ouf.write(f"{l+1}->{l+2}                     {L_idxs[l]},{L_idxs[l+1]}               {L_sizes[l]},{L_sizes[l+1]}            {int_3[0]},{int_3[1]},{int_3[2]}            {int_3_idx[0]},{int_3_idx[1]},{int_3_idx[2]}\n")

        
    
    def compare_N_largest_across_slices(self,N = 10):
        """Method for comparing the N-largest clusters across slices. 
        - Identifies N-largest clusters in Slice i (Ni)
        - Compares Ni to all clusters in slice i+1, calculates intersect.
        - Store ID and size of the three clusters with most interect with any three from Ni.
        - Finds N-largest clusters in Slice i+1 (Ni+1)
        - Repeats for all slices until Slice S-1


        Args:
            N (int, optional): Nuber of clusters to be compared from slice i-1. Defaults to 10.
        """
        

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)
            
        maxN = 3
        self.num_slices = len(clusters.keys())
        print(self.num_slices)

        with open(self.path_to_save_stats + f"compare_to_all_finding_{maxN}_largest_intersects_from_{N}_largest_clusters_SD.txt","w") as ouf:
            ouf.write("[Sim1->Si] [Cid_im10,Cid_im11,Cid_im12] [Cid_i0,Cid_i1,Cid_i2] [IS_0, IS_1, IS_2] [Sz_im10,Sz_im11,Sz_im12] [Sz_i0,Sz_i1,Sz_i2] \n")
            
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
                si = clusters[str(s)]
               
                intersect_mat = np.zeros([len(sim1.keys()),len(si.keys())])

                Li_sizes = []
                Li_idxs = []
                for k in range(len(si.keys())): 
                    num_nodes = len(si[str(k)])
                    Li_sizes.append(num_nodes)
                    Li_idxs.append(str(k))

                Li_sizes, Li_idxs = zip(*sorted(zip(Li_sizes, Li_idxs),reverse = True))
                Li_sizes = Li_sizes[:N]  
                Li_idxs = Li_idxs[:N]   
                
                t_s = time.perf_counter()
                for im1 in range(N):
                    im1_idx = L_idxs[im1]
                    vim1 = set(sim1[im1_idx])
                    for i in si.keys():
                        vi = set(si[i])
                        inters_n = vim1.intersection(vi)
                        inters_per = len(inters_n)/L_sizes[im1]
                        intersect_mat[int(im1_idx),int(i)] = inters_per      #im1 maps to L_idx
            
                t_e = time.perf_counter()
                print(f"Time spent comparing is {t_e-t_s:0.4f} s")

                t_s = time.perf_counter()
                intersect_mat_idx = np.argsort(intersect_mat.ravel())[::-1]  #Flatten and sort after arguments
                all_result = np.unravel_index(intersect_mat_idx, intersect_mat.shape)
                result = []
                for i in range(3):
                    result.append((all_result[0][i],all_result[1][i]))
                t_e = time.perf_counter()
                print(f"Time spent sorting and extracting max ids :  {t_e-t_s:0.4f} s")
             
                lim1 = " "
                li = " "
                sz_im1 = " "
                sz_i = " "
                final_intersect = " "
                for f in range(maxN):
                    lim1 += str(result[f][0]) +","
                    li += str(result[f][1]) + ","
                    sz_im1 += str(len(sim1[str(result[f][0])])) + ","
                    sz_i += str(len(si[str(result[f][1])])) + ","
                    final_intersect += str(intersect_mat[result[f][0],result[f][1]]) + ","

                lim1 = lim1[:-1]
                li = li[:-1]
                sz_im1 = sz_im1[:-1]
                sz_i = sz_i[:-1]
                final_intersect = final_intersect[:-1]
        
                ouf.write(f"{s-1}->{s}{lim1}{li}{final_intersect}{sz_im1}{sz_i}\n")
                
                sim1 = clusters[str(s)]
                L_sizes = Li_sizes
                L_idxs = Li_idxs 

    def plot_track_largest(self):
        """Plots results from the track_largest method.
        """
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
        plt.savefig(self.path_to_overleaf_plots + "size_largest.pdf")
        plt.clf()

        plt.plot(slices[1:],intersects, ".k")
        plt.xlabel(r"Slice $S_i$")
        plt.ylabel(r"Intersect from slice $S_{i-1} \rightarrow S_i$")
        plt.title(r"Intersect of largest cluster $C_{i-1} \rightarrow C_i$")
        plt.savefig(self.path_to_plots + "intersect_largest.pdf")
        plt.savefig(self.path_to_overleaf_plots + "intersect_largest.pdf")
        plt.clf()

    def table_biggest_cluster_size(self):
        """Method for generating table of the ID and size of the largest cluster in each slice. 
        """
        slice_num = []
        c_size = []
        c_idx = []

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())

        for s in range(1,self.num_slices+1):
            print(s)
            slice_num.append(s)
            si = clusters[str(s)]
            

            L_size = 0
            L_idx = "a"
            for k in range(len(si.keys())): 
                num_nodes = len(si[str(k)])
                if num_nodes > L_size:
                    L_size = num_nodes
                    L_idx = str(k)

                elif num_nodes == L_size:
                    print("Same size")

            c_size.append(L_size)
            c_idx.append(L_idx)


        c_dict = {'Slice num': slice_num, 'Cluster idx' : c_idx, 'Cluster size' : c_size}
        c_df = pd.DataFrame(c_dict)
        c_df.to_csv(self.path_to_save_stats + "largest_clusters.csv",index=False)

        print(c_df)

    def track_largest_branch(self):
        """Method for tracking the paths of the largest cluster from each slice.

        - Tracks the largest cluster (through vertex intersect) from slice i across all remaining slices. 
        """
        
        MASTER_MATCHES = []
        MASTER_INTERSECTS = []
        NUM_SLICES_IN_ROUND = []
        MASTER_SIZES = []
        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        path_breaks = []

        self.num_slices = len(clusters.keys())

        for ss in range(1, self.num_slices): #Last slice has no following slices and so it can't be tracked. 
            print("STARTED NEW ROUND AT SLICE : ", ss)
            sim1 = clusters[str(ss)]

            im1_size = 0
            Lim1_idx = -1
            Matches = []
            Lsizes = []
            per_intersects = []
            for k in range(len(sim1.keys())):
                num_nodes = len(sim1[str(k)])
                if num_nodes > im1_size:
                    im1_size = num_nodes 
                    Lim1_idx = int(k)

            Matches.append(Lim1_idx)   #Save for tracking
            per_intersects.append(0)   #No intersect since first slice
            Lsizes.append(im1_size)
            cim1 = set(sim1[str(Lim1_idx)])
            first = True
            for s in range(ss+1, self.num_slices+1):         #Begins at next slice in set after ss
                si = clusters[str(s)]

                max_intersect = 0
                M_id = -1
                ci_size = 0
                for c in si.keys():
                    ci = set(si[c])
                    intersect_set = cim1.intersection(ci)
                    intersect_per = len(intersect_set)/im1_size
                    if intersect_per > max_intersect:
                        max_intersect = intersect_per
                        M_id = int(c)
                        ci_size = len(ci)

                if max_intersect < 0.5 and first:
                    path_breaks.append([ss,s])
                    first = False
                Matches.append(M_id)
                per_intersects.append(max_intersect)
                Lsizes.append(ci_size)
                try:
                    cim1 = set(si[str(M_id)])
                except KeyError:
                    cim1 = set([-1,-2,-3])    #If there is no cluster meeting the criteria the branch can't be tracked.
                im1_size = len(cim1)

            
            MASTER_MATCHES.append(Matches)
            MASTER_INTERSECTS.append(per_intersects)
            NUM_SLICES_IN_ROUND.append(len(Matches))
            MASTER_SIZES.append(Lsizes)

        with open(self.path_to_save_stats + "break_off_branches.txt","w") as bf:
            for b in range(len(path_breaks)):
                bf.write(f"{path_breaks[b][0]},{path_breaks[b][1]}\n")
        
        with open(self.path_to_save_stats + "tracking_all_branches_largest_cluster_in_each_slice.txt","w") as ouf:
            ouf.write("startS:ids:intersects:sizes:num_slices\n")
            for i in range(len(MASTER_INTERSECTS)):
                ids_i = MASTER_MATCHES[i]
                ints_i = MASTER_INTERSECTS[i]
                n_slices =  NUM_SLICES_IN_ROUND[i]
                sizes_i = MASTER_SIZES[i]
                ouf.write(f"{i+1}:{ids_i}:{ints_i}:{sizes_i}:{n_slices}\n")
        


