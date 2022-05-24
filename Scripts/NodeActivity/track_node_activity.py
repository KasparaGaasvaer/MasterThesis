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

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "UnderlyingGraph/"
        if not os.path.exists(self.path_to_overleaf_plots):
            os.makedirs(self.path_to_overleaf_plots)



        """
        self.make_graphs()

        self.make_NAC_dict()

        self.sort_NAC_dict()

        self.plot_NAC_distribution(make_dist_dict=True)

        self.mapping_dict()
        
        self.plot_NAC()

        self.compare_NAC_2_contacts()
        """
        

    def make_graphs(self):
        
        self.path_to_dict = self.path + "parsed_dictionaries/"

        attributes_bool = False
        graph_type = "nx"

        super().__init__(self.path, graph_type, attributes_bool)

        self.num_slices = len(self.graphs.keys())

    def make_NAC_dict(self):
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]
            nn = G.number_of_nodes() - 1

            start_s = time.perf_counter()
            s_dict = nx.degree_centrality(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating activity {end_s-start_s:0.4f} s\n")

            s_dict.update((x, y*nn) for x, y in s_dict.items()) #NX gives out degree/num nodes, we want full degree

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "activity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def compare_NAC_2_contacts(self):

        methods = ["Java"]#"Leiden", "Louvain", "Java"]
        #std_n = 4

        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)

        self.num_slices = [i for i in range(1,len(master_dict.keys())+1)]

        stds = [3]#[1,2,3,4,5]
        for std_n in stds:
            for method in methods:
                method_name = method
                if method == "Java":
                    method_name = "Lprop"
                print(method_name)
                max_acts = []
                top_acts = []
                num_top_acts = []
                for s in master_dict.keys():
                    #print("Slice ", s)
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
                size_of_largest_cluster = pd.read_csv(self.path + f"statistics/Cluster_tracker/{method_name}/largest_clusters.csv", header = 0, usecols=[2])
                size_of_largest_cluster = size_of_largest_cluster.to_numpy()[:,0]
                

                perc_in_top  = (num_top_acts/nodes) *100
                
                plt.plot(self.num_slices,max_acts, label = "Activity of most active vertex")
                plt.plot(self.num_slices, contacts, label = "Total number of contacts")
                plt.plot(self.num_slices, size_of_largest_cluster, label = f"Size of largest cluster ({method_name})")
                plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
                plt.xlabel("Slice")
                plt.legend()
                plt.savefig(self.path_to_plots + f"max_NAC_vs_num_contacts_clusters_{method_name}.pdf")
                plt.savefig(self.path_to_overleaf_plots + f"max_NAC_vs_num_contacts_clusters_{method_name}.pdf")
                plt.clf()
                
                
                fz = 12
                fig, ax = plt.subplots()
                plt.plot(self.num_slices,max_acts, label = "Activity of most active vertex")
                plt.plot(self.num_slices, size_of_largest_cluster, label = f"Size of largest cluster ({method_name})")
                plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
                plt.xlabel("Slice", fontsize = fz)
                plt.tick_params(labelsize = fz)
                plt.legend()
                ax.yaxis.get_offset_text().set_fontsize(fz)
                plt.savefig(self.path_to_plots + f"max_NAC_and_largest_cluster_{method_name}.pdf")
                plt.savefig(self.path_to_overleaf_plots + f"max_NAC_and_largest_cluster_{method_name}.pdf")
                plt.clf()
                
                
                
                fz = 14
                fig, axs = plt.subplots(1, 2,figsize=(10, 6), dpi=80)
                axs[0].plot(self.num_slices, top_acts, label = "Activity of most active vertex")
                axs[0].plot(self.num_slices, contacts, label = "Total number of contacts")
                axs[0].set_title(f"Cut off = mean + {std_n}std", fontsize = fz+2)
                axs[0].set_xlabel("Slice", fontsize = fz)#, ylabel = "Nodes")
                axs[0].ticklabel_format(axis='y', style='scientific',scilimits=(0,0))
                axs[0].yaxis.get_offset_text().set_fontsize(fz)
                axs[0].legend(loc = 2, fontsize = fz)
                axs[0].tick_params(labelsize = fz)
                

                axs[1].plot(self.num_slices, perc_in_top)
                axs[1].set_xlabel("Slice", fontsize = fz)#, ylabel = "Nodes")
                axs[1].set_title("% Most active vertices", fontsize = fz+2)
                axs[1].set(ylim = [0,10])#, ylabel = "Contacts")
                #axs[1].ticklabel_format(axis='y', style='scientific',scilimits=(0,0))
                plt.gca().set_yticklabels([f'{x/100:.0%}' for x in plt.gca().get_yticks()], fontsize = fz) 
                axs[1].yaxis.get_offset_text().set_fontsize(fz)
                axs[1].tick_params(labelsize = fz)
                
                fig.tight_layout(pad=1.0)
                plt.savefig(self.path_to_plots + f"{std_n}std_NAC_vs_num_contacts.pdf")
                plt.savefig(self.path_to_overleaf_plots + f"{std_n}std_NAC_vs_num_contacts.pdf")
                plt.clf()
                
                

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

    def make_dist_dict_ind_slices(self):
        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)
        
        dist_dict = {}
        for s in master_dict.keys():
            slice = master_dict[s]
            dist_dict[s] = []
            entry_s = dist_dict[s]
            for id in slice.keys():
                degree = slice[id]
                entry_s.append(degree)

        with open(self.path_to_stats + "activity_lists_for_slices.json", "w") as ouff:
            json.dump(dist_dict,ouff)

    def measures_of_dist_to_file(self):
        with open(self.path_to_stats + "activity_lists_for_slices.json", "r") as inff:
            master_dict = json.load(inff)

        with open(self.path_to_stats + "activity_dist_measures.txt","w") as ouff:
            ouff.write("Mean      Std         Max      Min\n")
            for s in master_dict.keys():
                vals = np.array(master_dict[s])
                mean = np.mean(vals)
                std = np.std(vals)
                max_v = np.max(vals)
                min_v = np.min(vals)
                ouff.write(f"{mean:.2f}     {std:.2f}       {max_v:.2f}     {min_v:.2f}\n")

    def plot_mean_std_of_activity_dist(self):

        with open(self.path_to_stats + "activity_lists_for_slices.json", "r") as inff:
            master_dict = json.load(inff)

        means = []
        stds = []
        slices = []
        for s in master_dict.keys():
            slices.append(int(s))
            vals = np.array(master_dict[s])
            mean = np.mean(vals)
            std = np.std(vals)
            means.append(mean)
            stds.append(std)
        

        means = np.array(means)
        stds = np.array(stds)
        slices = np.array(slices)

        plt.errorbar(slices[:100], means[:100], stds[:100], linestyle='None', marker='o', mfc='red')
        plt.xlabel("Slice")
        plt.ylabel("Mean vertex activity")
        plt.savefig(self.path_to_plots + "mean_std_NAC_dist.pdf")
        plt.clf()


    def make_distribution_dict(self):
        if self.path == "./experiment6/":
            with open(self.path_to_stats + "activity_dict.json","r") as inff:
                master_dict = json.load(inff)

            dist_dict = {}
            s = "99"
            slice = master_dict[s]
            for id in slice.keys():
                degree = round(slice[id])
                try:
                    dist_dict[str(degree)] += 1
                except KeyError:
                    dist_dict[str(degree)] = 1
        else:
            with open(self.path_to_stats + "activity_dict.json","r") as inff:
                master_dict = json.load(inff)

            dist_dict = {}
            for s in master_dict.keys():
                slice = master_dict[s]
                for id in slice.keys():
                    degree = round(slice[id])
                    try:
                        dist_dict[str(degree)] += 1
                    except KeyError:
                        dist_dict[str(degree)] = 1
            
        with open(self.path_to_stats + "activity_distribution_dict.json", "w") as ouf:
            json.dump(dist_dict,ouf)

    def plot_NAC_distribution(self, make_dist_dict = False):
        from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, inset_axes
        from mpl_toolkits.axes_grid1.inset_locator import mark_inset

        if make_dist_dict:
            self.make_distribution_dict()
            

        with open(self.path_to_stats + "activity_distribution_dict.json","r") as inff:
                dist_dict = json.load(inff)

        values = []
        frequencies = []
        for num_n in dist_dict.keys():
            values.append(int(num_n))
            frequencies.append(int(dist_dict[num_n]))

        values, frequencies = zip(*sorted(zip(values, frequencies)))

        fig, ax = plt.subplots(figsize=(16,10), facecolor='white', dpi= 80)
        fz = 25
        for v,f in zip(values,frequencies):
            ax.vlines(x=v, ymin=0, ymax=f, color='forestgreen', alpha=0.7, linewidth=20)


        ax.set_ylabel("Frequency", fontsize = fz)
        ax.set_xlabel("Num Neighbours", fontsize = fz)
        labels = ax.get_xticks().tolist()
        labels = [int(l) for l in labels]
        labels[1] = 1
        

        ax.set_xticklabels(labels)
        plt.xticks(fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.yscale("log")   

        frequencies, values = np.array(frequencies), np.array(values)
        end_value = 1000
        end_id = np.where(values > end_value)[0][0]
        
        zoomed_f = frequencies[:end_id]
        zoomed_v = values[:end_id]
        print(np.min(zoomed_v))

        
        right_inset_ax = fig.add_axes([.45, .35, .4, .4], facecolor='white')
        for v,f in zip(zoomed_v,zoomed_f):
            right_inset_ax.vlines(x=v, ymin=0, ymax=f, color='forestgreen', alpha=0.7, linewidth=20)

        labels_in = right_inset_ax.get_xticks().tolist()
        labels_in[1] = 1
        labels_in = [int(l) for l in labels_in]

        right_inset_ax.set_xticklabels(labels_in)
        plt.yscale("log")
        plt.xticks(fontsize = fz-2)
        plt.yticks(fontsize = fz-2)
        
    
        plt.savefig(self.path_to_plots + "node_activity_distribution.pdf")
        plt.savefig(self.path_to_overleaf_plots + "node_activity_distribution.pdf")
        plt.clf()


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
        centrality_measure = "9_mean"#"0.9_median" #

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
        plt.savefig(self.path_to_overleaf_plots + f"{centrality_measure}_ids.pdf")
        plt.clf()

    def mean_min_val(self, values, cut_off):
        return np.mean(values) + cut_off*np.std(values)

    def median_min_val(self, values, cut_off):
        return np.quantile(values, cut_off)