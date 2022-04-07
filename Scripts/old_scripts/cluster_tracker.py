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
                self.num_slices = len(os.listdir(self.path_to_clusters)) 
        else:
            self.num_slices = len(os.listdir(self.path_to_clusters))

        self.path_to_save_stats = self.path + "statistics/Cluster_tracker/Java/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Cluster_tracker/Java/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "LabelProp/"
        
        #self.track_largest()
        #NL = 10 #num largest clusters
        #self.plot_track_largest()
        self.table_biggest_cluster_size() 
        #self.compare_clusters(NL, expnum)
        #self.compare_N_largest_across_slices(NL)
        #self.track_reid_largest_from_im12i()
        #self.track_largest_branch()

    def track_largest(self):
        print("\ntrack Largest\n")
        open_time_start = time.perf_counter()
        # Finds largest cluster in Sim1 and compare to all other clusters in Si
        # Find largest intersects
        # The one with most intersect becomes the next one to be compared in the next round


        #TC = Tracked Cluster
        
        with open(self.path_to_clusters + "c_1.json", "r") as inf:
            sim1 =  json.load(inf)

        
        TC_size = 0
        TC_idx = "a"
        for k in range(len(sim1.keys())): 
            num_nodes = len(sim1[str(k)]["uid"])
            if num_nodes > TC_size:
                TC_size = num_nodes
                TC_idx = str(k)
                #print(f"New TC_size = {TC_size}, New idx = {L_idx}")
            #elif num_nodes == TC_size:
                #print("oops, same size clusters")


        TC_vertices = set(sim1[TC_idx]["uid"])
        TC_sizes = []
        TC_idxs = []
        intersects = []
        inters_3_ids = []
        inters_3 = []
        TC_sizes.append(TC_size)
        TC_idxs.append(TC_idx)
        for s in range(2,self.num_slices +1):
            print(s)

            with open(self.path_to_clusters + "c_" + str(s) +".json","r") as innf:
                si = json.load(innf)
            
            intersects_arr = np.zeros(len(si.keys()))

            for ci in si.keys():
                vi = set(si[ci]["uid"])
                inters = TC_vertices.intersection(vi)
                intersects_arr[int(ci)] = len(inters)/TC_size

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
            
     
            TC_idx = str(max_intersect_id)
            TC_size = len(si[TC_idx]["uid"])
            TC_vertices = set(si[TC_idx]["uid"])
            TC_sizes.append(TC_size)
            TC_idxs.append(TC_idx)


        open_time_end = time.perf_counter()
        print(f"Time spent tracking largest cluster: {open_time_end-open_time_start:0.4f} s")
        with open(self.path_to_save_stats + "tracking_largest_cluster.txt","w") as ouf:
            ouf.write("Slice i -> i+1      Cluster ID i,i+1      Cluster size i,i+1                             Intersects                           Intersect ids\n")
            for l in range(len(TC_idxs)-1):
                int_3 = inters_3[l]
                int_3_idx = inters_3_ids[l]
                ouf.write(f"{l+1}->{l+2}                     {TC_idxs[l]},{TC_idxs[l+1]}               {TC_sizes[l]},{TC_sizes[l+1]}            {int_3[0]},{int_3[1]},{int_3[2]}            {int_3_idx[0]},{int_3_idx[1]},{int_3_idx[2]}\n")     #{intersects[l]}\n")


    def compare_N_largest_across_slices(self,N):
        print("\nCompare N largest across slices\n")
        # - Identify N largest clusters in si
        # - Identify N largest clusters in sip1
        # - Compare the N and calculate intersect
        #    - That is, for every cluster we will have N-1 intersects,
        #      the 3 largest are stored as well as which clusters that was,
        #      also their size 0-N
        #  Slice number - Cluster id for i - Cluster id for im1 - Intersect - Sizes for i - Sizes for im1 - Ranked size i - Ranked size im1
        # - Makes file with Sim1->Si [Cid_im10,Cid_im11,Cid_im12] [Cid_i0,Cid_i1,Cid_i2]  [IS_0, IS_1, IS_2] [Sz_im10,Sz_im11,Sz_im12] [Sz_i0,Sz_i1,Sz_i2]
        maxN = 3

        with open(self.path_to_save_stats + f"finding_{maxN}_largest_intersects_from_{N}_largest_clusters.txt","w") as ouf:
            ouf.write("[Sim1->Si] [Cid_im10,Cid_im11,Cid_im12] [Cid_i0,Cid_i1,Cid_i2] [IS_0, IS_1, IS_2] [Sz_im10,Sz_im11,Sz_im12] [Sz_i0,Sz_i1,Sz_i2]]\n")
            
            with open(self.path_to_clusters + "c_1.json", "r") as inf:
                sim1 =  json.load(inf)

            L_sizes = []
            L_idxs = []
            for k in range(len(sim1.keys())): 
                num_nodes = len(sim1[str(k)]["uid"])
                L_sizes.append(num_nodes)
                L_idxs.append(str(k))

            L_sizes, L_idxs = zip(*sorted(zip(L_sizes, L_idxs),reverse = True))
            L_sizes = L_sizes[:N]  #Num nodes in N-largest clusters
            L_idxs = L_idxs[:N]    #IDs of N-largest clusters

            for s in range(2,self.num_slices +1):
                
                print(s)
                with open(self.path_to_clusters + "c_" + str(s) + ".json", "r") as inf:
                    si =  json.load(inf)

                intersect_mat = np.zeros([len(sim1.keys()),len(si.keys())])
                Li_sizes = []
                Li_idxs = []
                for k in range(len(si.keys())): 
                    num_nodes = len(si[str(k)]["uid"])
                    Li_sizes.append(num_nodes)
                    Li_idxs.append(str(k))

                Li_sizes, Li_idxs = zip(*sorted(zip(Li_sizes, Li_idxs),reverse = True))
                Li_sizes = Li_sizes[:N]  #Num nodes in N-largest clusters
                Li_idxs = Li_idxs[:N]    #IDs of N-largest clusters
                
                t_s = time.perf_counter()
                for im1 in range(N):
                    im1_idx = L_idxs[im1]   #Cluster id
                    vim1 = set(sim1[im1_idx]["uid"])
                    for i in si.keys():
                        vi = set(si[i]["uid"])

                        inters_n = vim1.intersection(vi)
                        inters_per = len(inters_n)/L_sizes[im1]
                        intersect_mat[int(im1_idx),int(i)] = inters_per
            

                t_e = time.perf_counter()
                print(f"Time spent comparing {t_e-t_s:0.4f} s")

                t_s = time.perf_counter()
                intersect_mat_idx = np.argsort(intersect_mat.ravel())[::-1]  #flatten and sorted after arguments

                #result = [(int(k//intersect_mat.shape[1]), int(k%intersect_mat.shape[1])) for k in intersect_mat_idx][:maxN] #unravel indexes, pick out 3 largest

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
                
                sim1 = si
                L_sizes = Li_sizes
                L_idxs = Li_idxs


    def plot_track_largest(self):
        print("\nplot track largest\n")
        # plot showing result from track_largest
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
        print("\nTable biggest cluster size\n")
        slice_num = []
        c_size = []
        c_idx = []

        for s in range(1,self.num_slices+1):
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
        c_df.to_csv(self.path_to_save_stats + "largest_clusters.csv",index=True)

        print(c_df)

    def compare_clusters(self, N_largest, expnum):
        print("\nCompare clusters\n")
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
                pers90 = int((len(cim1)/100)*10)
                counter = 0
                for c_id_i in N_idx_si:
                    ci = i_list_of_sets[str(c_id_i)]
                    r = cim1 - ci  #All nodes in cim1 NOT in ci
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
            ouf.write(f"N/{N_largest}    Si    Sim1    [ID_im1, ID_i]\n")
            for p in range(len(reqz)):
                ouf.write(f"{reqz[p]}        {p+1}      {p+2}             {reqz_id[p]}\n")
                #ouf.write(f"We re-identified {reqz[p]} of the 100 largest clusters from slice_{p+1} in slice_{p+2}\n")
                #diffs.append(recog/num_nodes_cim1)
                #print(recog/num_nodes_cim1)

        #with open(self.path_to_save_stats+f"{N_largest}_cluster_IDs_experiment{expnum}.txt", "w") as ouf:
            #ouf.write("s_im1 -> s_i             [ID_im1, ID_i]\n")
            #for p in range(len(reqz)):
                #ouf.write(f"{p+1} -> {p+2}             {reqz_id[p]}\n")

    def track_reid_largest_from_im12i(self):
        print("\nTrack reID largest from im1 to i\n")
        # planen her er å finne den største i s1, reidentifisere den i slice 2, se på intersect
        # så skal jeg finne den største i slice 2, om dette ikke er den samme så skal punktet sikifte farge,
        # også skal jeg reidentifisere den største slik som før (aka det må ikke være den samme som i slice 1)
        with open(self.path_to_clusters + "c_1.json", "r") as inf:
            sim1 =  json.load(inf)

        all_intersects = []
        all_ids = []
        colours = ["r","b","k","c","g","y","m"]
        color_id = 0
        match_counter = []

        L_size = 0
        L_idx = "a"
        for k in range(len(sim1.keys())):
            num_nodes = len(sim1[str(k)]["uid"])
            if num_nodes > L_size:
                L_size = num_nodes 
                L_idx = str(k)

        L_vertices = set(sim1[L_idx]["uid"])
        L_size = len(L_vertices)


        for s in range(2,self.num_slices +1):
            print(s)
            with open(self.path_to_clusters + "c_" + str(s) +".json","r") as innf:
                si = json.load(innf)
            match_idx = "a"
            Li_size = 0
            Li_idx = "a"
            max_intersect = 0

            for k_i in si.keys():
                ci = set(si[k_i]["uid"])
                c_sz = len(ci)
                intersect_n = L_vertices.intersection(ci)
                intersect_per = len(intersect_n)/L_size 
                #if intersect_per == max_intersect and intersect_per != 0:   #Checked that we dont have copies of clusters
                    #print("hmm cluster have more than one match??")
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
            L_vertices = set(sim1[Li_idx]["uid"])
            L_idx = Li_idx 
            L_size = len(L_vertices)


        slices_nums = [i for i in range(2,self.num_slices+1)]
        for i in range(len(slices_nums)):
            plt.scatter(slices_nums[i],all_intersects[i],color = colours[match_counter[i]])
        plt.xlabel("Slice")
        plt.ylabel("Intersect")
        plt.savefig(self.path_to_plots + "Largest_intersect_when_comparing_largest_cluster_in_slice_im1_with_all_clusters_in_slice_i.pdf")
        plt.savefig(self.path_to_overleaf_plots + "Largest_intersect_when_comparing_largest_cluster_in_slice_im1_with_all_clusters_in_slice_i.pdf")
            

  

    def track_largest_branch(self):
        # Lage en algo som tracker den største fra slice 1
        # Når den med størst intersect ikke lenger er den største 
        # så brancher vi og tracker den med størst intersect til den også
        # slik fortsetter det 
        
        MASTER_MATCHES = []
        MASTER_INTERSECTS = []
        NUM_SLICES_IN_ROUND = []
        MASTER_SIZES = []
        for ss in range(1, self.num_slices): #Last slice has no following slices and so cant be tracked. 
            print("STARTED NEW ROUND AT SLICE : ", ss)
            with open(self.path_to_clusters + "c_" + str(ss) +".json","r") as innf:
                sim1 = json.load(innf)

            im1_size = 0
            Lim1_idx = -1
            Matches = []
            Lsizes = []
            per_intersects = []
            for k in range(len(sim1.keys())):
                num_nodes = len(sim1[str(k)]["uid"])
                if num_nodes > im1_size:
                    im1_size = num_nodes 
                    Lim1_idx = int(k)

            Matches.append(Lim1_idx)   #Save for tracking
            per_intersects.append(0)   #No intersect since first slice
            Lsizes.append(im1_size)
            cim1 = set(sim1[str(Lim1_idx)]["uid"])
            for s in range(ss+1, self.num_slices+1):         #begins at slice after start slice of this round
                with open(self.path_to_clusters + "c_" + str(s) +".json","r") as innf:
                    si = json.load(innf)

                max_intersect = 0
                M_id = -1
                ci_size = 0
                for c in si.keys():
                    ci = set(si[c]["uid"])
                    intersect_set = cim1.intersection(ci)
                    intersect_per = len(intersect_set)/im1_size
                    if intersect_per > max_intersect:
                        max_intersect = intersect_per
                        M_id = int(c)
                        ci_size = len(ci)

                Matches.append(M_id)
                per_intersects.append(max_intersect)
                Lsizes.append(ci_size)
                cim1 = set(si[str(M_id)]["uid"])
                im1_size = len(cim1)

            
            MASTER_MATCHES.append(Matches)
            MASTER_INTERSECTS.append(per_intersects)
            NUM_SLICES_IN_ROUND.append(len(Matches))
            MASTER_SIZES.append(Lsizes)
        
        with open(self.path_to_save_stats + "tracking_all_branches_largest_cluster_in_each_slice.txt","w") as ouf:
            ouf.write("startS:ids:intersects:sizes:num_slices\n")
            for i in range(len(MASTER_INTERSECTS)):
                ids_i = MASTER_MATCHES[i]
                ints_i = MASTER_INTERSECTS[i]
                n_slices =  NUM_SLICES_IN_ROUND[i]
                sizes_i = MASTER_SIZES[i]
                ouf.write(f"{i+1}:{ids_i}:{ints_i}:{sizes_i}:{n_slices}\n")





        