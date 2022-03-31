import sys, os, json, time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

sys.path.append("..")  # Adds higher directory to python modules path, looking for Graphs-class one level up

class ExtractCentrality:
    def __init__(self,path):

        self.path = path 

        if path == "./experiment12/experiment_12/":
            k_value = input("Input k_value\n")
            if int(k_value):
                self.path = self.path + "k_" + str(k_value) + "/"
                self.path_to_plots = self.path + "plots/Centrality/"
                if not os.path.exists(self.path_to_plots):
                    os.makedirs(self.path_to_plots)
                
                self.path_to_stats = self.path + "statistics/Centrality/"
                if not os.path.exists(self.path_to_stats):
                    os.makedirs(self.path_to_stats)

                self.path_to_overleaf_plots = "./p_2_overleaf/k_" + k_value + "/UnderlyingGraph/"
                if not os.path.exists(self.path_to_overleaf_plots):
                    os.makedirs(self.path_to_overleaf_plots)


        else:
            self.path_to_stats = self.path + "statistics/Centrality/"
            if not os.path.exists(self.path_to_stats):
                os.makedirs(self.path_to_stats)

            self.path_to_plots = self.path + "plots/Centrality/"
            if not os.path.exists(self.path_to_plots):
                os.makedirs(self.path_to_plots)

            self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "UnderlyingGraph/"
            if not os.path.exists(self.path_to_overleaf_plots):
                os.makedirs(self.path_to_overleaf_plots)


        #self.avg_assortativity()
        self.degree_distibution()



    def avg_assortativity(self):

        num_phases = 3

        with open(self.path_to_stats + "degree_assortivity_dict.json","r") as inff:
            assorts = json.load(inff)

        num_slices = [i for i in range(1,len(assorts.keys())+1)]
        num_slices = np.array(num_slices)
        phases = np.array_split(num_slices, num_phases)

        ass_phases = [[] for i in range(num_phases)]
        all = []
        p = 0
        for phase in phases:
            for s in phase:
                ass_phases[p].append(assorts[str(s)])
                all.append(assorts[str(s)])
            p +=1

        means = []
        stds = []
        
        for ph in ass_phases:
            ph = np.array(ph)
            means.append(np.mean(ph))
            stds.append(np.std(ph))

        all = np.array(all)
        all_mean = np.mean(all)
        all_std = np.std(all)

        with open(self.path_to_stats + "avg_assortativity.txt","w") as ouf:
            ouf.write("Phase       Mean             Std\n")
            ouf.write(f"ALL       {all_mean:4f}        {all_std:4f}\n")
            for j in range(num_phases):
                ouf.write(f"{j}         {means[j]:4f}        {stds[j]:4f}\n")



    def degree_distibution(self):
        # inte alle vals i deg_c dict, telle hvor mange ganger en hver oppstår 

        with open(self.path_to_stats + "deg_c_dict.json", "r") as inff:
            cents = json.load(inff)

        num_slices = len(cents.keys()) 

        count_dict = {}
        l = 0
        all = []
        for s in range(1,num_slices + 1):
            C = cents[str(s)]

            for i in C.keys():
                k = C[i]
                all.append(int(k))
                try:
                    count_dict[str(k)] += 1
                except KeyError:
                    count_dict[str(k)] = 1

        
        x_vals = np.array(list(count_dict.keys())).astype("float")
        y_vals = np.array(list(count_dict.values()))
        y_vals = y_vals/len(x_vals)
        
        import seaborn as sns
        import pdb


        #pdb.set_trace()
        all = np.array(all)

        sns.histplot(all, binwidth=10)
        #plt.bar(x_vals, y_vals)
        #plt.xscale("log")
        plt.xlabel("Number of neighbours")
        plt.yscale("log")
        plt.savefig("TEST.pdf")

        



