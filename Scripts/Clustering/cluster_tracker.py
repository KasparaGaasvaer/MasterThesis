import json, os, time
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
import numpy as np 


class ClusterTracker:
    def __init__(self, path):

        self.path = path
        self.path_to_clusters = self.path + "parsed_dictionaries/Clusters/"

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

    

        if not os.path.exists(self.path_to_clusters):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.path_to_clusters = self.path + "parsed_dictionaries/Clusters/"
                expnum = str(expnum) + "_k" + str(k_value)
                self.num_slices = len(os.listdir(self.path_to_clusters)) - 1 #last slice has no cluster for k = 800
        else:
            self.num_slices = len(os.listdir(self.path_to_clusters))

        self.path_to_save_stats = self.path + "statistics/cluster_stats/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Java/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        
        #self.track_largest()
        NL = 100 #num largest clusters
        self.plot_track_largest()
        self.table_biggest_cluster_size() 
        #self.compare_clusters(NL, expnum)
        #self.does_any_id_change(filename = self.path_to_save_stats + str(NL) + "_cluster_IDs_experiment" + str(expnum) + ".txt")
    
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
            L_size = len(si[L_idx]["uid"])
            L_vertices = set(si[L_idx]["uid"])
            L_sizes.append(L_size)
            L_idxs.append(L_idx)


        open_time_end = time.perf_counter()
        print(f"Time spent tracking largest cluster: {open_time_end-open_time_start:0.4f} s")
        with open(self.path_to_save_stats + "tracking_largest_cluster.txt","w") as ouf:
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

    def compare_clusters(self, N_largest, expnum):
        # 1. Open clusters
        # 2. Identify 100 largest cluster in slice i
        # 3. Re identify those in slice i-1

        with open(self.path_to_clusters + "c_1.json", "r") as inf:
            sim1 =  json.load(inf)

        sim1_csize = []
        sim1_idx = []
        for k in range(len(sim1.keys())): 
            sim1_idx.append(k)
            num_nodes = len(sim1[str(k)]["uid"])
            sim1_csize.append(num_nodes)
        
        sim1_csize, sim1_idx = zip(*sorted(zip(sim1_csize,sim1_idx)))
        #N_largest_sim1 = sim1_csize[-100:]
        N_idx_sim1 = sim1_idx[-N_largest:]
        im1_list_of_sets = {}

        
        for indx in range(N_largest):
            N = str(N_idx_sim1[indx])
            verts = sim1[N]["uid"]
            verts = set(verts)
            im1_list_of_sets[N] = verts

        reqz = []
        reqz_id = []
        for i in range(2,self.num_slices+1):
            print(i)
            with open(self.path_to_clusters + "c_" + str(i) +".json","r") as inf:
                si = json.load(inf)
                
            si_csize = []
            si_idx = []
            for k in range(len(si.keys())): 
                si_idx.append(k)
                num_nodes = len(si[str(k)]["uid"])
                si_csize.append(num_nodes)


            si_csize, si_idx = zip(*sorted(zip(si_csize,si_idx)))
            #N_largest_si = si_csize[-100:]
            N_idx_si = si_idx[-N_largest:]
            i_list_of_sets = {}

            #print(N_idx_si)
            #print(N_idx_sim1)

            for indx in range(N_largest):
                N = str(N_idx_si[indx])
                verts = si[N]["uid"]
                verts = set(verts)
                i_list_of_sets[N] = verts
            
            #print(i_list_of_sets.keys())


            recogs = 0
            re_identified_id = []
            for c_id_im1 in N_idx_sim1:
                cim1 = im1_list_of_sets[str(c_id_im1)]
                pers90 = int((len(cim1)/100)*9)
                counter = 0
                for c_id_i in N_idx_si:
                    ci = i_list_of_sets[str(c_id_i)]
                    r = cim1 - ci
                    if not len(r) > pers90:
                        counter +=1
                        recogs +=1
                        ids = [c_id_im1,c_id_i]
                        re_identified_id.append(ids)

                if counter >= 2:
                    print("More than one match")
                #elif counter == 1:
                    #print("one match")
                #else:
                    #print("Could not reidentify")


            reqz.append(recogs)
            reqz_id.append(re_identified_id)
            im1_list_of_sets = deepcopy(i_list_of_sets)
            N_idx_sim1 = N_idx_si
            #print(im1_list_of_sets.keys) #Just to see that it actually changes
            #print(recogs)

        


    # print(f"We re-identified {recogs} of the 100 largest clusters from slice_{i-1} in slice_{i}")
        with open(self.path_to_save_stats+f"{N_largest}_largestCluster_reID_experiment{expnum}.txt","w") as ouf:
            ouf.write(f"N/{N_largest}    Si    Sim1\n")
            for p in range(len(reqz)):
                ouf.write(f"{reqz[p]}        {p+1}      {p+2}\n")
                #ouf.write(f"We re-identified {reqz[p]} of the 100 largest clusters from slice_{p+1} in slice_{p+2}\n")
                #diffs.append(recog/num_nodes_cim1)
                #print(recog/num_nodes_cim1)

        with open(self.path_to_save_stats+f"{N_largest}_cluster_IDs_experiment{expnum}.txt", "w") as ouf:
            ouf.write("s_im1 -> s_i             [ID_im1, ID_i]\n")
            for p in range(len(reqz)):
                ouf.write(f"{p+1} -> {p+2}             {reqz_id[p]}\n")


    def does_any_id_change(self,filename):
        with open(filename,"r") as innf:
            innf.readline()
            lines = innf.readlines()
            counter = 1
            for line in lines:
                same_ID = 0
                changed_ID = 0
                ll = line.split("  ")[-1]
                ll = ll.replace("]","")
                ll = ll.replace("[","")
                ll = ll.split(",")
                for i in range(0,len(ll),2):
                    a = int(ll[i])
                    b = int(ll[i+1])
                    #if a != b:
                        #print(f"cluster {a} became cluster {b} from slice {counter} to {counter+1}")
                        #same_ID +=1 
                    #else:
                        #changed_ID += 1
                counter +=1

                #ll = ll.strip("[[")
                #ll = ll.split("], [")
                #ll = ll.split("]]")[0]
            # print(ll)





    