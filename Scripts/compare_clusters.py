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

    sim1_csize = []
    sim1_idx = []
    for k in range(len(sim1.keys())): 
            sim1_idx.append(k)
            num_nodes = len(sim1[str(k)]["uid"])
            sim1_csize.append(num_nodes)
    
    sim1_csize, sim1_idx = zip(*sorted(zip(sim1_csize,sim1_idx)))
    #N_largest_sim1 = sim1_csize[-100:]
    N_idx_sim1 = sim1_idx[-N_largest:]
    im1_list_of_sets = []*N_largest

    for indx in range(N_largest):
            N = N_idx_sim1[indx]
            verts = sim1[str(N)]["uid"]
            verts = set(verts)
            im1_list_of_sets.append(verts)

    reqz = []
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
        i_list_of_sets = []*N_largest

        #print(N_idx_si)
        #print(N_idx_sim1)

        for indx in range(N_largest):
            N = N_idx_si[indx]
            verts = si[str(N)]["uid"]
            verts = set(verts)
            i_list_of_sets.append(verts)


        recogs = 0
        for qim1 in range(N_largest):
            cim1 = im1_list_of_sets[qim1]
            pers90 = int((len(cim1)/100)*9)
            counter = 0
            for qi in range(N_largest):
                ci = i_list_of_sets[qi]
                r = cim1 - ci
                if not len(r) > pers90:
                    counter +=1
                    recogs +=1
            if counter >= 2:
                print("More than one match")
            #elif counter == 1:
                #print("one match")
            #else:
                #print("Could not reidentify")


        """
        for cim1 in im1_list_of_sets:
            len_cim1 = len(cim1)
            #print(len_cim1)
            for ci in i_list_of_sets:
                #print(len(ci))
                r = 0
                for v in cim1:
                    if v in ci:
                        r +=1
                #print(r/len_cim1)
                if r/len_cim1 > 0.1:
                    recogs +=1
        """

        reqz.append(recogs)
        im1_list_of_sets = deepcopy(i_list_of_sets)
        #print(len(im1_list_of_sets[0])) #Just to see that it actually changes
        #print(recogs)

    


   # print(f"We re-identified {recogs} of the 100 largest clusters from slice_{i-1} in slice_{i}")
    with open(f"{N_largest}_largestCluster_reID_experiment{expnum}.txt","w") as ouf:
        ouf.write(f"N/{N_largest}    Si    Sim1\n")
        for p in range(len(reqz)):
            ouf.write(f"{reqz[p]}        {p+1}      {p+2}\n")
            #ouf.write(f"We re-identified {reqz[p]} of the 100 largest clusters from slice_{p+1} in slice_{p+2}\n")
            #diffs.append(recog/num_nodes_cim1)
            #print(recog/num_nodes_cim1)









compare_clusters(N_largest = 200, path_to_clusters = "./experiment100/parsed_dictionaries/Clusters/", expnum = 100)




