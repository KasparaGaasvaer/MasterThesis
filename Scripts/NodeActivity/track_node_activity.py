from doctest import master
import sys, os, time, json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

from Utils.graphs import Graphs

sys.path.append(
    ".."
)  # Adds higher directory to python modules path, looking for Graphs-class one level up

class NodeActivity(Graphs):
    def __init__(self,path):

        self.path = path 
        self.path_to_stats = self.path + "statistics/NodeActivity/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        self.path_to_plots = self.path + "plots/NodeActivity/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)


        #self.make_graphs()

        #self.make_NAC_dict()

        #self.sort_NAC_dict()

        #self.mapping_dict()
        
        #self.plot_NAC()

        self.compare_NAC_2_contacts()

    def make_graphs(self):
        
        self.path_to_dict = self.path + "parsed_dictionaries/"

        attributes_bool = False
        graph_type = "nx"

        super().__init__(self.path, graph_type, attributes_bool)

        self.num_slices = len(self.graphs.keys())



    def make_NAC_dict(self):
        # Åpne graf filer 
        # g1: loop gjennom alle linjer 
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]
            nn = G.number_of_nodes() - 1

            start_s = time.perf_counter()
            s_dict = nx.degree_centrality(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating activity {end_s-start_s:0.4f} s\n")

            s_dict.update((x, y*nn) for x, y in s_dict.items())

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "activity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def compare_NAC_2_contacts(self):

        methods = ["Leiden", "Louvain"]
        #std_n = 4

        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)

        self.num_slices = [i for i in range(1,len(master_dict.keys())+1)]

        stds = [1,2,3,4,5]
        for std_n in stds:
            for method in methods:
                max_acts = []
                top_acts = []
                num_top_acts = []
                for s in master_dict.keys():
                    print("Slice ", s)
                    max_a = 0
                    top_a = 0
                    num_top = 0
                    slice = master_dict[s]
                    vals = list(slice.values())
                    cut_off = np.mean(vals) + std_n*np.std(vals)
                    for n in slice.keys():
                        activity = slice[n]
                        if activity > cut_off:
                            num_top += 1
                            top_a += activity
                            if activity > max_a:
                                max_a = activity
                    max_acts.append(max_a)
                    top_acts.append(top_a)
                    num_top_acts.append(num_top)

                max_acts = np.array(max_acts)    
                top_acts = np.array(top_acts)
                num_top_acts = np.array(num_top_acts)

                contacts = np.load(self.path + "statistics/ExpStats/len_graphs.npy")
                nodes = np.load(self.path + "statistics/ExpStats/len_labels.npy")
                size_of_largest_cluster = pd.read_csv(self.path + f"statistics/Cluster_tracker/{method}/largest_clusters.csv", header = 0, usecols=[2])
                size_of_largest_cluster = size_of_largest_cluster.to_numpy()[:,0]
                

                perc_in_top  = (num_top_acts/nodes) *100

                plt.plot(self.num_slices,max_acts, label = "Activity of most active node")
                plt.plot(self.num_slices, contacts, label = "Total number of contacts")
                plt.plot(self.num_slices, size_of_largest_cluster, label = f"Size of largest cluster ({method})")
                plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
                plt.xlabel("Slice")
                plt.legend()
                plt.savefig(self.path_to_plots + f"max_NAC_vs_num_contacts_clusters_{method}.pdf")
                plt.clf()

                fig, axs = plt.subplots(1, 2)
                axs[0].plot(self.num_slices, top_acts, label = "Activity of most active nodes")
                axs[0].plot(self.num_slices, contacts, label = "Total number of contacts")
                axs[0].set_title(f"Cut off = mean + {std_n}std")
                axs[0].set(xlabel = "Slice")#, ylabel = "Nodes")
                axs[0].ticklabel_format(axis='y', style='scientific',scilimits=(0,0))
                axs[1].plot(self.num_slices, perc_in_top, ".")
                axs[1].set_title("% Most active nodes")
                axs[1].set(xlabel = "Slice")#, ylabel = "Contacts")
                axs[1].ticklabel_format(axis='y', style='scientific',scilimits=(0,0))
                fig.tight_layout(pad=1.0)
                axs[0].legend()
                plt.savefig(self.path_to_plots + f"{std_n}std_NAC_vs_num_contacts.pdf")
                plt.clf()

                """
                plt.plot(self.num_slices, top_acts, label = "Activity of most active nodes")
                plt.plot(self.num_slices, contacts, label = "Total number of contacts")
                plt.title(f"Cut off = mean + {std_n}std")
                plt.xlabel("Slice")
                plt.legend()
                plt.savefig(self.path_to_plots + f"{std_n}std_NAC_vs_num_contacts.pdf")
                plt.clf()
                """

        



    def sort_NAC_dict(self):

        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)

        self.num_slices = len(master_dict.keys())

        sorted_dict = {}
        for s in master_dict.keys():
            idx = int(s)
            slice = master_dict[s]
            for n in slice.keys():
                try:
                    sorted_dict[n][idx] = int(slice[n])
                except KeyError:
                    sorted_dict[n] = [0] * (self.num_slices + 1)
                    sorted_dict[n][idx] = int(slice[n])
            
        print(len(sorted_dict.keys()))
        with open(self.path_to_stats + "sorted_activity_dict.json","w") as ouf:
            json.dump(sorted_dict, ouf)

    def mapping_dict(self):

        with open(self.path_to_stats + "sorted_activity_dict.json","r") as inff:
            s_dict = json.load(inff)

        mapping_dict = {}
        i = 0
        for s in s_dict.keys():
            mapping_dict[s] = i 
            i +=1

        with open(self.path_to_stats + "mapping_dict.json","w") as ouf:
            json.dump(mapping_dict, ouf)

            
    def find_ids(self, centrality_measure):
        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)


        cmes = centrality_measure.split("_")
        if cmes[-1] == "mean":
            cut_off = int(cmes[0])
            c_meas = lambda v,co: self.mean_min_val(v,co)

        if cmes[-1] == "median":
            cut_off = float(cmes[0])
            c_meas = lambda v,co: self.median_min_val(v,co)

        ids = [None] * (len(master_dict.keys()) + 1)
        
        for s in master_dict.keys():
            print("Slice ", s)
            x = int(s)
            ids[x] = []
            
            slice = master_dict[s]
            vals = list(slice.values())
            min_val = c_meas(vals, cut_off)
            print("Min_val = ", min_val)
            points = 0
            for n in slice.keys():
                activity = slice[n]
                if activity > min_val:
                    ids[x].append(int(n))
                    points +=1 
            print("Num points = ", points)

        id_dict = {}
        for s in master_dict.keys():
            id_dict[s] = []
            for n in ids[int(s)]:
                id_dict[s].append(n)

            

        with open(self.path_to_stats + f"{centrality_measure}_ids.json", "w") as ouf:
            json.dump(id_dict,ouf)
    
            
    def plot_NAC(self):
        centrality_measure = "3_mean" #"0.9_median"

        self.find_ids(centrality_measure)

        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)
        
        with open(self.path_to_stats + f"{centrality_measure}_ids.json", "r") as inff:
            ids = json.load(inff)

        unique_ids = list(set().union(*ids.values()))
        num_unique_ids = len(unique_ids)
        colours = cm.get_cmap("gist_rainbow",num_unique_ids)

        
        for s in master_dict.keys():
            print("Slice ", s)
            x = int(s)

            slice = master_dict[s]
            nodes = ids[s]

            for n in nodes:
                activity = slice[str(n)]
                c = unique_ids.index(n)
                plt.scatter(x, activity, color = colours(c))

            #plt.text(x,-1, f"Active users\n{len(nodes)}", size = 6, ha = 'center')
        
        plt.xlabel("Slice")
        plt.ylabel("Activity")
        plt.savefig(self.path_to_plots + f"{centrality_measure}_ids.pdf")

    def mean_min_val(self, values, cut_off):
        return np.mean(values) + cut_off*np.std(values)

    def median_min_val(self, values, cut_off):
        return np.quantile(values, cut_off)