import os, json
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def compare_clusters(N_largest, path_to_clusters, expnum):
   # 1. Open clusters
    # 2. Identify 100 largest cluster in slice i
    # 3. Re identify those in slice i-1
    num_slices = len(os.listdir(path_to_clusters))

    with open(path_to_clusters + "c_1.json", "r") as inf:
        sim1 =  json.load(inf)

    sim1_csize = 0
    sim1_idx = "1"
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
    for i in range(2,num_slices+1):
        print(i)
        with open(path_to_clusters + "c_" + str(i) +".json","r") as inf:
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
    with open(f"{N_largest}_largestCluster_reID_experiment{expnum}.txt","w") as ouf:
        ouf.write(f"N/{N_largest}    Si    Sim1\n")
        for p in range(len(reqz)):
            ouf.write(f"{reqz[p]}        {p+1}      {p+2}\n")
            #ouf.write(f"We re-identified {reqz[p]} of the 100 largest clusters from slice_{p+1} in slice_{p+2}\n")
            #diffs.append(recog/num_nodes_cim1)
            #print(recog/num_nodes_cim1)

    with open(f"{N_largest}_cluster_IDs_experiment{expnum}.txt", "w") as ouf:
        ouf.write("s_im1 -> s_i             [ID_im1, ID_i]\n")
        for p in range(len(reqz)):
            ouf.write(f"{p+1} -> {p+2}             {reqz_id[p]}\n")









#compare_clusters(N_largest = 100, path_to_clusters = "./experiment100/parsed_dictionaries/Clusters/", expnum = 100)



def does_any_id_change(filename):
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
                if a != b:
                    #print(f"cluster {a} became cluster {b} from slice {counter} to {counter+1}")
                    changed_ID +=1 
                else:
                    same_ID +=1
            counter +=1

            #ll = ll.strip("[[")
            #ll = ll.split("], [")
            #ll = ll.split("]]")[0]
           # print(ll)





does_any_id_change(filename = "100_cluster_IDs_experiment100.txt")