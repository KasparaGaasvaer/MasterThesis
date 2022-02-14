import json, os
import matplotlib.pyplot as plt
import numpy as np



class MassVelocity:
    def __init__(self, path, method):
        
        self.path = path
        self.method = method 

        if self.method == "leiden" or self.method == "louvain":
            self.setup_modularity()
        
        if self.method == "java":
            self.setup_labelprop()


        N_largest = 3
        self.track_growth_modularity(N_largest)
        self.plot_growth_track(N_largest)


    def setup_modularity(self):

        expnum = self.path.split("/")[1]
        expnum = int(expnum.split("t")[1])   

        self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
        if not os.path.exists(self.clusters):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/"
                self.clusters = self.path + "parsed_dictionaries/partitions_" + self.method + ".json"
                expnum = str(expnum) + "_k" + str(k_value)
              
        

        self.path_to_save_stats = self.path + "statistics/" + self.method.title() + "/MassVelocity/"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/"+ self.method.title() + "/MassVelocity/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)



    def setup_labelprop(self):
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

        self.path_to_save_stats = self.path + "statistics/cluster_stats/MassVelocity"
        if not os.path.exists(self.path_to_save_stats):
            os.makedirs(self.path_to_save_stats)


        self.path_to_plots = self.path + "plots/Clustering/Java/MassVelocity"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        


    def track_growth_modularity(self,N):

        outfile_name = f"tracking_{N}_clusters_with_largest_absolute_growth_"+ self.method +".txt "
        Min_size_cluster_im1 = 50 #minimum size of a cluster in Sim1 must have to be concidered
        with open(self.clusters, "r") as inf:
            clusters = json.load(inf)

        self.num_slices = len(clusters.keys())
        sim1 = clusters["1"]

        with open(self.path_to_save_stats+outfile_name,"w") as ouf:
            ouf.write(f"[s1,s2] [Largest Intersects] [Value Intersect] [Largest Growth ABS] [Values Growth ABS] [Largest Growth REL] [Value Growth REL]\n")
            
            ID_LARGEST = []
            SIZE_LARGEST = []

            keyid = []
            lenghts = []
            for k in sim1.keys():
                lenghts.append(len(sim1[k]))
                keyid.append(k)

            lenghts,keyid = zip(*sorted(zip(lenghts,keyid), reverse = True))

            ID_LARGEST.append(keyid[:N])
            SIZE_LARGEST.append(lenghts[:N])
            
            for s in range(2,self.num_slices+1):
                ss = str(s)
                print(ss)
                si = clusters[ss]

                
                keyid = []
                lenghts = []
                for k in si.keys():
                    lenghts.append(len(si[k]))
                    keyid.append(k)

                lenghts,keyid = zip(*sorted(zip(lenghts,keyid), reverse = True))
                ID_LARGEST.append(keyid[:N])
                SIZE_LARGEST.append(lenghts[:N])
                

                si_num_new =  np.zeros([len(sim1.keys()), len(si.keys())])
                si_rel_growth = np.zeros([len(sim1.keys()), len(si.keys())])
                si_intersect = np.zeros([len(sim1.keys()), len(si.keys())])

                im1_l_min = 0
                num_intersect_l_min = 0
                for im1_k in sim1.keys():
                    v_im1 = set(sim1[im1_k])
                    num_nodes_vim1 = len(v_im1)
                    if num_nodes_vim1 >= Min_size_cluster_im1:  #checks if cluster is large enough to be concidered
                        im1_l_min += 1
                        for i_k in si.keys():
                            v_i = set(si[i_k])
                            num_nodes_vi = len(v_i)

                            inters_n = v_im1.intersection(v_i)
                            #inters_n = v_im1 & v_i
                            inters_per = float(len(inters_n))/num_nodes_vim1
                            num_new = num_nodes_vi - num_nodes_vim1
                            #print(inters_per)
                            if inters_per > 0.9: #and num_new > 0:   #only growing clusters
                                num_intersect_l_min += 1
                                si_intersect[int(im1_k)][int(i_k)] = inters_per
                                
                                #print("im1:", im1_k , " ", v_im1)
                                #print("i:", i_k , " ", v_i)
                                
                                #print(num_new)
                                rel_growth = num_new/num_nodes_vim1
                                #print(rel_growth)
                                #print(" ")

                                si_num_new[int(im1_k)][int(i_k)] = num_new
                                si_rel_growth[int(im1_k)][int(i_k)] = rel_growth
                
            
                #print(im1_l_min)
                #print(num_intersect_l_min)
                # Sjekk alle exp for små clusters i starten


                if num_intersect_l_min == 0:
                    print(f"None of the {im1_l_min} clusters from slice {s-1} that had a minimum size of {Min_size_cluster_im1} were found in slice {s}")
                    ouf.write("NODATA\n")

                if num_intersect_l_min != 0 and num_intersect_l_min < N: 
                    N = num_intersect_l_min
                    print("N updated to ", num_intersect_l_min)

                    intersect_idx_tmp = np.argsort(si_intersect.ravel())[::-1]  #flatten and sorted after arguments
                    intersect_idx = [(int(k//si_intersect.shape[1]), int(k%si_intersect.shape[1])) for k in intersect_idx_tmp][:N] #unravel indexes, pick out 3 largest

                    max_new_nodes_tmp = np.argsort(si_num_new.ravel())[::-1]  #flatten and sorted after arguments
                    max_new_nodes = [(int(k//si_num_new.shape[1]), int(k%si_num_new.shape[1])) for k in max_new_nodes_tmp][:N] #unravel indexes, pick out num_new

                    max_rel_growth_tmp = np.argsort(si_rel_growth.ravel())[::-1]  #flatten and sorted after arguments
                    max_new_nodes = [(int(k//si_rel_growth.shape[1]), int(k%si_rel_growth.shape[1])) for k in max_rel_growth_tmp][:N] 


                if num_intersect_l_min == N or num_intersect_l_min > N: 
                    intersect_idx_tmp = np.argsort(si_intersect.ravel())[::-1]  #flatten and sorted after arguments
                    intersect_idx = [(int(k//si_intersect.shape[1]), int(k%si_intersect.shape[1])) for k in intersect_idx_tmp][:N] #unravel indexes, pick out 3 largest
                   
                    max_new_nodes_tmp = np.argsort(si_num_new.ravel())[::-1]  #flatten and sorted after arguments
                    max_new_nodes = [(int(k//si_num_new.shape[1]), int(k%si_num_new.shape[1])) for k in max_new_nodes_tmp][:N] 

                    max_rel_growth_tmp = np.argsort(si_rel_growth.ravel())[::-1]  #flatten and sorted after arguments
                    max_rel_growth = [(int(k//si_rel_growth.shape[1]), int(k%si_rel_growth.shape[1])) for k in max_rel_growth_tmp][:N] 

               
                intersects_2_file = []
                #intersect_id_to_file = []
                max_new_to_file = []
                #max_new_id_= []
                max_rel_g_to_file = []
                #max_rel_g_id = []

                for itm in range(N):
                    intersects_2_file.append(si_intersect[intersect_idx[itm]])
                    max_new_to_file.append(si_num_new[max_new_nodes[itm]])
                    max_rel_g_to_file.append(si_rel_growth[max_rel_growth[itm]])

                ouf.write(f"[{s-1},{s}] {intersect_idx} {intersects_2_file} {max_new_nodes} {max_new_to_file} {max_rel_growth} {max_rel_g_to_file}\n")

                sim1 = si


    def plot_growth_track(self,N):

        intersect_ids = []
        intersect_vals = []

        num_new_ids = []
        num_new_vals = []

        rel_g_ids = []
        rel_g_vals = []

        infile_name = f"tracking_{N}_clusters_with_largest_absolute_growth_"+ self.method +".txt "
        with open(self.path_to_save_stats + infile_name,"r") as inf:
            inf.readline()
            lines = inf.readlines()
            for line in lines:
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

        
        n = len(intersect_ids)
        slices = [i for i in range(2,n+2)]
        colours = ["r","b","g"]

        #Plot value of N largest rel growth in each slice
        for i in range(n):
            rel_g_vals_sep = rel_g_vals[i].split(",")
            num_vals = len(rel_g_vals_sep)
            for j in range(num_vals):
                plt.plot(slices[i],float(rel_g_vals_sep[j]),".", color = colours[j])
            
        plt.xlabel("Slice Number")
        plt.ylabel("(Size C_si - Size C_sim1)/Size C_sim1")
        plt.savefig(self.path_to_plots + f"{N}_largest_relative_growth_in_each_slice.pdf")
        
        for i in range(n):
            num_g_vals = num_new_vals[i].split(",")
            num_vals = len(num_g_vals)
            for j in range(num_vals):
                int_val = int(num_g_vals[j].split(".")[0])
                plt.plot(slices[i],int_val,".", color = colours[j])

        plt.xlabel("Slice Number")
        plt.ylabel("Size C_si - Size C_sim1")
        plt.savefig(self.path_to_plots + f"{N}_largest_absolute_growth_in_each_slice.pdf" )
                






    

