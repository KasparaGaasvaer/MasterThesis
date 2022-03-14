from doctest import master
import sys, os, time, json
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
        self.path_to_stats = self.path + "/statistics/NodeActivity/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        #self.make_graphs()

        #self.make_NAC_dict()

        #self.sort_NAC_dict()

        #self.mapping_dict()
        
        self.plot_NAC()

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

    """
    def plot_NAC(self):
        with open(self.path_to_stats + "sorted_activity_dict.json","r") as inff:
            s_dict = json.load(inff)

        colours = cm.get_cmap("cool",1000)#len(s_dict.keys()))
        #print(colours(0))

        i = 0
        for n in s_dict.keys():
            print(i)
            activ = s_dict[n]
            maxx = max(activ)
            if maxx > 100:
                x = [z + 1 for z in range(len(activ))]
                plt.scatter(x,activ, color = colours(i))
                i += 1
            if i > 1000:
                break
            

        plt.savefig("testplot.pdf")
    """  

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

    def get_num_unique_ids(self, filename):
        with open(self.path_to_stats + filename,"r") as inff:
            s_dict = json.load(inff)
            
    def find_ids(self, centrality_measure, num_std):
        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)

        #with open(self.path_to_stats + "mapping_dict.json","r") as inff:
            #mapping_dict = json.load(inff)


        if centrality_measure == "mean":
            c_meas = lambda x: np.mean(x)

        if centrality_measure == "median":
            c_meas = lambda x: np.median(x) 

        #colours = cm.get_cmap("gist_rainbow",len(mapping_dict.keys()))

        ids = [None] * (len(master_dict.keys()) + 1)
        
        for s in master_dict.keys():
            print("Slice ", s)
            x = int(s)
            ids[x] = []
            
            slice = master_dict[s]
            vals = list(slice.values())
            mean = np.mean(vals)
            #median = np.median(vals)
            std = np.std(vals)
            min_val = mean + num_std*std
            print("Min_val = ", min_val)
            points = 0
            for n in slice.keys():
                activity = slice[n]
                if activity > min_val:
                    #c = mapping_dict[n]
                    #plt.scatter(x, activity, color = colours(c))
                    ids[x].append(int(n))
                    points +=1 
            print("Num points = ", points)

            #plt.savefig("testplot.pdf")

        id_dict = {}
        for s in master_dict.keys():
            id_dict[s] = []
            for n in ids[int(s)]:
                id_dict[s].append(n)

            

        with open(self.path_to_stats + f"{centrality_measure}_p_{num_std}std_ids.json", "w") as ouf:
            json.dump(id_dict,ouf)
            

            
    def plot_NAC(self):
        centrality_measure = "mean"
        num_std = 3

        #self.find_ids(centrality_measure, num_std)

        with open(self.path_to_stats + f"{centrality_measure}_p_{num_std}std_ids.json", "r") as inff:
            ids = json.load(inff)

        unique_ids = list(set().union(*ids.values()))
        num_unique_ids = len(unique_ids)


        colours = cm.get_cmap("gist_rainbow",num_unique_ids)


        
        with open(self.path_to_stats + "activity_dict.json","r") as inff:
            master_dict = json.load(inff)
        
        for s in master_dict.keys():
            print("Slice ", s)
            x = int(s)

            slice = master_dict[s]
            nodes = ids[s]

            for n in nodes:
                activity = slice[str(n)]
                c = unique_ids.index(n)
                plt.scatter(x, activity, color = colours(c))

            plt.text(x,-1, f"Active users\n{len(nodes)}", size = 6, ha = 'center')
        
        plt.savefig("testplot.pdf")

        








