import os, json
import numpy as np
import matplotlib.pyplot as plt


def compare_clusters(N_largest, path_to_clusters, expnum):
   # 1. Open clusters
    # 2. Identify 100 largest cluster in slice i
    # 3. Re identify those in slice i-1
    num_slices = len(os.listdir(path_to_clusters))

    with open(path_to_clusters + "c_1.json", "r") as inf:
        sim1 =  json.load(inf)
    reqz = []
    for i in range(2,num_slices+1):
        print(i)
        with open(path_to_clusters + "c_" + str(i) +".json","r") as inf:
            si = json.load(inf)
            sim1_csize = []
            sim1_idx = []
        for k in range(len(sim1.keys())):
            sim1_idx.append(k)
            num_nodes = len(sim1[str(k)]["uid"])
            sim1_csize.append(num_nodes)

        sim1_csize, sim1_idx = zip(*sorted(zip(sim1_csize,sim1_idx)))
        #N_largest_si = si_csize[-100:]
        N_idx_sim1 = sim1_idx[-N_largest:]

        #recogs = []
        recogs = 0
        for c in N_idx_sim1:
            cim1 = sim1[str(c)]["uid"]
            num_nodes_cim1 = len(cim1)
            ci = si[str(c)]["uid"]

            recog = sum(el in cim1 for el in ci)

            thresh = int(num_nodes_cim1/10)
            if recog > thresh:
                recogs += 1

        reqz.append(recogs)
   # print(f"We re-identified {recogs} of the 100 largest clusters from slice_{i-1} in slice_{i}")
    with open(f"{N_largest}_largestCluster_reID_experiment{expnum}.txt","w") as ouf:
        ouf.write(f"N/{N_largest}    Si    Sim1")
        for p in range(len(reqz)):
            ouf.write(f"{reqz[p]}    {p+1}    {p+2}\n")
            #ouf.write(f"We re-identified {reqz[p]} of the 100 largest clusters from slice_{p+1} in slice_{p+2}\n")
            #diffs.append(recog/num_nodes_cim1)
            #print(recog/num_nodes_cim1)









compare_clusters(N_largest = 100, path_to_clusters = "./experiment100/parsed_dictionaries/Clusters/", expnum = 100)
