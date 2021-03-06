import json, os, time
import matplotlib.pyplot as plt
import numpy as np



class MassVelocity:
    def __init__(self, path, method, min_size_cluster):
        
        self.path = path
        self.method = method 
        N_largest = 3
        self.min_size_cluster_im1 = min_size_cluster #minimum size of a cluster in Sim1 must have to be concidered

        self.setup()
        #self.track_growth(N_largest)
        self.track_largest_growth()
        
        #self.plot_growth_track(N_largest)


    def setup(self):

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

        self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
     
        self.path_to_save_stats = self.path + "statistics/Mass_velocity/" + self.method.title() + "/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Mass_velocity/"+ self.method.title() + "/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + self.method.title() + "/"


    def track_largest_growth(self):

        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())
        sim1 = clusters["1"]


        L_absolute = []
        S_absolute = []
        L_relative = []   
        ID_A = []
        ID_R = []

        for s in range(2,self.num_slices +1):
            ss = str(s)
            si = clusters[ss]   

            largest_cluster =  max(len(item) for item in si.values())
            crit = largest_cluster//2    #Only check clusters if they are at least 50% the size of the largest

            considered_clusters = 0
            la = 0   #Largest absolute growth
            sa = 0   #Size of la
            lr = 0   #Largest relative growth (relative to size of cluster)
            ida = "lol"
            idr = "lol2"

            t_s = time.perf_counter()
            for im1_k in sim1.keys():
                v_im1 = set(sim1[im1_k])
                num_nodes_vim1 = len(v_im1)
                if num_nodes_vim1 >= crit:  #checks if cluster is large enough to be concidered
                    considered_clusters += 1
                    for i_k in si.keys():
                        v_i = set(si[i_k])
                        num_nodes_vi = len(v_i)

                        inters_a = len(v_im1.intersection(v_i))
                        inters_rel = inters_a/num_nodes_vim1
                        num_new = num_nodes_vi - num_nodes_vim1
                        if inters_rel > 0.5: #and num_new > 0:   #only growing clusters
                            if inters_a > la:
                                la = inters_a
                                sa = num_nodes_vim1
                                ida = i_k
                            if inters_rel > lr:
                                lr = inters_rel
                                idr = i_k

            L_absolute.append(la)
            S_absolute.append(sa)
            L_relative.append(lr)
            ID_A.append(ida)
            ID_R.append(idr)

            t_e = time.perf_counter()
            print(f"Time spent comparing {s-1} to {s} = {t_e-t_s:0.4f} s. Num C considered:  {considered_clusters}")
            sim1 = si

        with open(self.path_to_save_stats + "largest_growth_mass_vel.txt","w") as ouf:
            ouf.write("S : LA,id : SA : LR,id\n")
            for t in range(len(L_absolute)):
                ouf.write(f"{t+1} : {L_absolute[t]},{ID_A[t]} : {S_absolute[t]} : {L_relative[t]},{ID_R[t]}\n")



    def track_growth(self,N):

        #N_max = N
        #outfile_name = f"tracking_{N}_clusters_with_largest_absolute_growth_"+ self.method +".txt "
        outfile_name = "tracking_" + str(N) +"_clusters_with_largest_absolute_growth_"+ self.method +"_min_cluster_size_" + str(self.min_size_cluster_im1) + ".txt"
      
        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())
        sim1 = clusters["1"]

        with open(self.path_to_save_stats+outfile_name,"w") as ouf:
            ouf.write(f"[s1,s2] [Largest Intersects] [Value Intersect] [Largest Growth ABS] [Values Growth ABS] [Largest Growth REL] [Value Growth REL]\n")
            
           
            for s in range(2,self.num_slices+1):
                ss = str(s)
                #print(ss)
                si = clusters[ss]

                si_num_new =  np.zeros([len(sim1.keys()), len(si.keys())])
                si_rel_growth = np.zeros([len(sim1.keys()), len(si.keys())])
                si_intersect = np.zeros([len(sim1.keys()), len(si.keys())])

                im1_l_min = 0
                num_intersect_l_min = 0
                t_s = time.perf_counter()
                for im1_k in sim1.keys():
                    v_im1 = set(sim1[im1_k])
                    num_nodes_vim1 = len(v_im1)
                    if num_nodes_vim1 >= self.min_size_cluster_im1:  #checks if cluster is large enough to be concidered
                        im1_l_min += 1
                        for i_k in si.keys():
                            v_i = set(si[i_k])
                            num_nodes_vi = len(v_i)

                            inters_n = v_im1.intersection(v_i)
                            inters_per = float(len(inters_n))/num_nodes_vim1
                            num_new = num_nodes_vi - num_nodes_vim1
                            if inters_per > 0.5: #and num_new > 0:   #only growing clusters
                                num_intersect_l_min += 1
                                si_intersect[int(im1_k)][int(i_k)] = inters_per
                                rel_growth = num_new/num_nodes_vim1

                                si_num_new[int(im1_k)][int(i_k)] = num_new
                                si_rel_growth[int(im1_k)][int(i_k)] = rel_growth

                t_e = time.perf_counter()
                #print(f"Time spent comparing {t_e-t_s:0.4f} s")
    
                intersects_2_file = []
                max_new_to_file = []
                max_rel_g_to_file = []

                t_s = time.perf_counter()
                if num_intersect_l_min == 0:
                    print(f"None of the {im1_l_min} clusters from slice {s-1} that had a minimum size of {self.min_size_cluster_im1} were found in slice {s}")
                    ouf.write("NODATA\n")

                if num_intersect_l_min != 0 and num_intersect_l_min < N: 
                    N_tmp = num_intersect_l_min
                    print("N updated to ", num_intersect_l_min)

                    intersect_idx_tmp = np.argsort(si_intersect.ravel())[::-1]  #flatten and sorted after arguments
                    #intersect_idx = [(int(k//si_intersect.shape[1]), int(k%si_intersect.shape[1])) for k in intersect_idx_tmp][:N] #unravel indexes, pick out N largest
                    all_result = np.unravel_index(intersect_idx_tmp, si_intersect.shape)
                    intersect_idx = []
                    for i in range(N_tmp):
                        intersect_idx.append((all_result[0][i],all_result[1][i]))

                    max_new_nodes_tmp = np.argsort(si_num_new.ravel())[::-1]  #flatten and sorted after arguments
                    #max_new_nodes = [(int(k//si_num_new.shape[1]), int(k%si_num_new.shape[1])) for k in max_new_nodes_tmp][:N] #unravel indexes, pick out num_new
                    all_result = np.unravel_index(max_new_nodes_tmp, si_num_new.shape)
                    max_new_nodes = []
                    for i in range(N_tmp):
                        max_new_nodes.append((all_result[0][i],all_result[1][i]))

                    max_rel_growth_tmp = np.argsort(si_rel_growth.ravel())[::-1]  #flatten and sorted after arguments
                    #max_rel_growth = [(int(k//si_rel_growth.shape[1]), int(k%si_rel_growth.shape[1])) for k in max_rel_growth_tmp][:N] 
                    all_result = np.unravel_index(max_rel_growth_tmp, si_rel_growth.shape)
                    max_rel_growth = []
                    for i in range(N_tmp):
                        max_rel_growth.append((all_result[0][i],all_result[1][i]))

                    for itm in range(N_tmp):
                        intersects_2_file.append(si_intersect[intersect_idx[itm]])
                        max_new_to_file.append(si_num_new[max_new_nodes[itm]])
                        max_rel_g_to_file.append(si_rel_growth[max_rel_growth[itm]])

                    ouf.write(f"[{s-1},{s}] {intersect_idx} {intersects_2_file} {max_new_nodes} {max_new_to_file} {max_rel_growth} {max_rel_g_to_file}\n")


                if num_intersect_l_min == N or num_intersect_l_min > N: 
                    print("No problems for slice", s)
                    intersect_idx_tmp = np.argsort(si_intersect.ravel())[::-1]  #flatten and sorted after arguments
                    #intersect_idx = [(int(k//si_intersect.shape[1]), int(k%si_intersect.shape[1])) for k in intersect_idx_tmp][:N] #unravel indexes, pick out N largest
                    all_result = np.unravel_index(intersect_idx_tmp, si_intersect.shape)
                    intersect_idx = []
                    for i in range(N):
                        intersect_idx.append((all_result[0][i],all_result[1][i]))
                   
                    max_new_nodes_tmp = np.argsort(si_num_new.ravel())[::-1]  #flatten and sorted after arguments
                    #max_new_nodes = [(int(k//si_num_new.shape[1]), int(k%si_num_new.shape[1])) for k in max_new_nodes_tmp][:N]
                    all_result = np.unravel_index(max_new_nodes_tmp, si_num_new.shape)
                    max_new_nodes = []
                    for i in range(N):
                        max_new_nodes.append((all_result[0][i],all_result[1][i])) 

                    max_rel_growth_tmp = np.argsort(si_rel_growth.ravel())[::-1]  #flatten and sorted after arguments
                    #max_rel_growth = [(int(k//si_rel_growth.shape[1]), int(k%si_rel_growth.shape[1])) for k in max_rel_growth_tmp][:N]
                    all_result = np.unravel_index(max_rel_growth_tmp, si_rel_growth.shape)
                    max_rel_growth = []
                    for i in range(N):
                        max_rel_growth.append((all_result[0][i],all_result[1][i])) 

                    for itm in range(N):
                        intersects_2_file.append(si_intersect[intersect_idx[itm]])
                        max_new_to_file.append(si_num_new[max_new_nodes[itm]])
                        max_rel_g_to_file.append(si_rel_growth[max_rel_growth[itm]])

                    ouf.write(f"[{s-1},{s}] {intersect_idx} {intersects_2_file} {max_new_nodes} {max_new_to_file} {max_rel_growth} {max_rel_g_to_file}\n")
                t_e = time.perf_counter()
                #print(f"Time spent sorting and extracting max ids :  {t_e-t_s:0.4f} s")

                sim1 = si
                

    def plot_growth_track(self,N):

        intersect_ids = []
        intersect_vals = []

        num_new_ids = []
        num_new_vals = []

        rel_g_ids = []
        rel_g_vals = []
        infile_name = "tracking_"+str(N)+"_clusters_with_largest_absolute_growth_"+ self.method +"_min_cluster_size_" + str(self.min_size_cluster_im1) + ".txt"
        with open(self.path_to_save_stats + infile_name,"r") as inf:
            inf.readline()
            lines = inf.readlines()
            slices = []
            for line in lines:
                if not "NODATA" in line:
                    items = line.split("] [")
                    #slices = items[0].strip("[")
                    #print(slices)
                    intersect_ids.append(items[1])
                    intersect_vals.append(items[2])

                    num_new_ids.append(items[3])
                    num_new_vals.append(items[4])

                    rel_g_ids.append(items[5])
                    g_vals = items[-1].strip("]\n")
                    rel_g_vals.append(g_vals)
                    slices.append(1)
                else:
                    slices.append(0)
        
        slices = np.array(slices)
        slices = (np.array(np.where(slices==1))+2)[0]

        n = len(intersect_ids)
        #slices = [i for i in range(2,n+2)]
        colours = ["r","b","g"] #red is largest, blue is second largest, green is third largest

        
        #Plot value of N largest rel growth in each slice
        for i in range(n):
            rel_g_vals_sep = rel_g_vals[i].split(",")
            num_vals = len(rel_g_vals_sep)
            #print(num_vals)
            for j in range(num_vals):
                plt.plot(slices[i],float(rel_g_vals_sep[j]),".", color = colours[j])
            
        plt.xlabel("Slice Number")
        plt.ylabel("(Size C_si - Size C_sim1) / Size C_sim1")
        plt.savefig(self.path_to_plots + str(N) + "_largest_relative_growth_in_each_slice_min_size_cluster_" +str(self.min_size_cluster_im1) +".pdf")
        plt.savefig(self.path_to_overleaf_plots + str(N) + "_largest_relative_growth_in_each_slice_min_size_cluster_" +str(self.min_size_cluster_im1) +".pdf")
        plt.clf()
        
        for i in range(n):
            num_g_vals = num_new_vals[i].split(",")
            num_vals = len(num_g_vals)
            for j in range(num_vals):
                int_val = int(num_g_vals[j].split(".")[0])
                plt.plot(slices[i],int_val,".", color = colours[j])

        plt.xlabel("Slice Number")
        plt.ylabel("Size C_si - Size C_sim1")
        plt.savefig(self.path_to_plots + str(N) + "_largest_absolute_growth_in_each_slice_min_size_cluster_" +str(self.min_size_cluster_im1) +".pdf")
        plt.savefig(self.path_to_overleaf_plots + str(N) + "_largest_absolute_growth_in_each_slice_min_size_cluster_" +str(self.min_size_cluster_im1) +".pdf")
        plt.clf()
        






    

