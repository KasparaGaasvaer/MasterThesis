import json
import os
import time

class ClusterTracker:
    def __init__(self, path):
        self.path_to_clusters = path + "parsed_dictionaries/Clusters/"
        self.path_to_save_stats = path + "statistics/cluster_stats/"
        
        self.track_largest()
    
    def track_largest(self):
        open_time_start = time.perf_counter()
        # 1. Open C-1, identify the one largest cluster, save ID and Size
        # 2. Loop trough all vertices in LC1, identify them in clusters in C-2
        #     -- Either go through all clusters, see how many of the Vs are there, remove them from list, when list is empty stop checking
        #     -- Or for every node check every cluster, then remove nodes from list and stop when list is empty 
        # 3. Store IDs of clusters as keys in dict, value +=1 for every "hit"
        # 4. Identify largest value from dict, store ID as LC2 ,divide by size(LC1)
        # 5. Do the same for LC2 and so on
        
        num_slices = len(os.listdir(self.path_to_clusters))

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
        L_sizes.append(L_size)
        L_idxs.append(L_idx)
        for s in range(2,10):#num_slices +1):
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
            intersect = si_hit_dict[max_intersect]/L_size
            intersects.append(intersect)

            L_idx = max_intersect
            L_size = len(si[L_idx]["uid"])
            L_vertices = set(si[L_idx]["uid"])
            L_sizes.append(L_size)
            L_idxs.append(L_idx)

        open_time_end = time.perf_counter()
        print(f"Time spent tracking largest cluster: {open_time_end-open_time_start:0.4f} s")
        with open(self.path_to_save_stats + "tracking_largest_cluster.txt","w") as ouf:
            ouf.write("Slice i -> i+1      Cluster ID i,i+1      Cluster size i,i+1      Intersect\n")
            for l in range(len(L_idxs)-1):
                ouf.write(f"{l+1}->{l+2}                     {L_idxs[l]},{L_idxs[l+1]}               {L_sizes[l]},{L_sizes[l+1]}       {intersects[l]}\n")
            
            


