import json
import os
import time
import matplotlib.pyplot as plt
import pandas as pd

class ClusterTracker:
    def __init__(self, path):
        self.path_to_clusters = path + "parsed_dictionaries/Clusters/"
        self.path_to_save_stats = path + "statistics/cluster_stats/"

        self.num_slices = len(os.listdir(self.path_to_clusters))
        
        #self.track_largest()
        #self.plot_track_largest()
        self.table_biggest_cluster_size()
    
    def track_largest(self):
        open_time_start = time.perf_counter()
        # 1. Open C-1, identify the one largest cluster, save ID and Size
        # 2. Loop trough all vertices in LC1, identify them in clusters in C-2
        #     -- Either go through all clusters, see how many of the Vs are there, remove them from list, when list is empty stop checking
        #     -- Or for every node check every cluster, then remove nodes from list and stop when list is empty 
        # 3. Store IDs of clusters as keys in dict, value +=1 for every "hit"
        # 4. Identify largest value from dict, store ID as LC2 ,divide by size(LC1)
        # 5. Do the same for LC2 and so on
        
        with open(self.path_to_clusters + "c_1.json", "r") as inf:
            sim1 =  json.load(inf)

        L_size = 0
        L_idx = "a"
        for k in range(len(sim1.keys())): 
            num_nodes = len(sim1[str(k)]["uid"])
            if num_nodes > L_size:
                L_size = num_nodes
                L_idx = str(k)
                #print(f"New L_size = {L_size}, New idx = {L_idx}")
            #elif num_nodes == L_size:
                #print("oops, same size clusters")


        L_vertices = set(sim1[L_idx]["uid"])
        L_sizes = []
        L_idxs = []
        intersects = []
        inters_3_ids = []
        inters_3 = []
        L_sizes.append(L_size)
        L_idxs.append(L_idx)
        for s in range(2,self.num_slices +1):
            print(s)

            with open(self.path_to_clusters + "c_" + str(s) +".json","r") as innf:
                si = json.load(innf)

            si_cids = list(si.keys())
            si_hit_dict = {}
            for d in range(len(si_cids)):
                si_hit_dict[si_cids[d]] = 0
            

            for ci in si.keys():
                vi = set(si[ci]["uid"])
                for v in L_vertices:
                    if v in vi:
                        si_hit_dict[ci] +=1

            max_intersect = max(si_hit_dict, key=si_hit_dict.get)
            max_3_intersects = sorted(si_hit_dict, key=si_hit_dict.get, reverse=True)[:3]
            inters_3_ids.append(max_3_intersects)
            
            inters = []
            for m3 in max_3_intersects:
                inter =  si_hit_dict[m3]/L_size
                inters.append(inter)

            inters_3.append(inters)

            intersect = si_hit_dict[max_intersect]/L_size
            intersects.append(intersect)


            L_idx = max_intersect
            L_size = len(si[L_idx]["uid"])
            L_vertices = set(si[L_idx]["uid"])
            L_sizes.append(L_size)
            L_idxs.append(L_idx)


        open_time_end = time.perf_counter()
        print(f"Time spent tracking largest cluster: {open_time_end-open_time_start:0.4f} s")
        with open(self.path_to_save_stats + "tracking_largest_cluster_test.txt","w") as ouf:
            ouf.write("Slice i -> i+1      Cluster ID i,i+1      Cluster size i,i+1                             Intersects                           Intersect ids\n")
            for l in range(len(L_idxs)-1):
                int_3 = inters_3[l]
                int_3_idx = inters_3_ids[l]
                ouf.write(f"{l+1}->{l+2}                     {L_idxs[l]},{L_idxs[l+1]}               {L_sizes[l]},{L_sizes[l+1]}            {int_3[0]},{int_3[1]},{int_3[2]}            {int_3_idx[0]},{int_3_idx[1]},{int_3_idx[2]}\n")     #{intersects[l]}\n")
            
            

    def plot_track_largest(self):
        
        
        sizes = []
        intersects = []
        with open(self.path_to_save_stats + "tracking_largest_cluster.txt","r") as innf:
            innf.readline()
            lines = innf.readlines()
            for line in lines:
                line = line.split()
                size = line[-2].split(",")[0]
                sizes.append(int(size))
                intersects.append(float(line[-1]))
            
            last = lines[-1]
            last = last.split()
            size = line[-2].split(",")[-1]
            sizes.append(int(size))

        
        slices = [i for i in range(1,len(sizes)+1)]
        
        plt.plot(slices,sizes, "*")
        plt.xlabel("Slice num")
        plt.ylabel("Num vertices in cluster")
        plt.title("Size of cluster when tracking largest from slice 1")
        plt.savefig(self.path_to_save_stats + "size_largest.pdf")
        plt.clf()

        plt.plot(slices[1:],intersects, "*")
        plt.xlabel("Slice num i")
        plt.ylabel("Intersect from slice i-1 -> i")
        plt.title("Intersect of largest cluster i-1 -> i")
        plt.savefig(self.path_to_save_stats + "intersect_largest.pdf")

        
    def table_biggest_cluster_size(self):

        slice_num = []
        c_size = []
        c_idx = []

        for s in range(1,self.num_slices):
            print(s)
            slice_num.append(s)
            with open(self.path_to_clusters + "c_" + str(s) +".json","r") as innf:
                c_s = json.load(innf)

            L_size = 0
            L_idx = "a"
            for k in range(len(c_s.keys())): 
                num_nodes = len(c_s[str(k)]["uid"])
                if num_nodes > L_size:
                    L_size = num_nodes
                    L_idx = str(k)

                elif num_nodes == L_size:
                    print("oopsi, same size")

            c_size.append(L_size)
            c_idx.append(L_idx)


        c_dict = {'Slice num': slice_num, 'Cluster idx' : c_idx, 'Cluster size' : c_size}
        c_df = pd.DataFrame(c_dict)
        c_df.to_csv(self.path_to_save_stats + "largest_clusters.csv",index=False)

        print(c_df)