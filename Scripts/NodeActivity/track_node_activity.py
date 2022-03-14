from doctest import master
import sys, os, time, json
import networkx as nx
import matplotlib.pyplot as plt
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

    def plot_NAC(self):
        with open(self.path_to_stats + "sorted_activity_dict.json","r") as inff:
            s_dict = json.load(inff)

        i = 0
        for n in s_dict.keys():
            print(i)
            activ = s_dict[n]
            x = [z + 1 for z in range(len(activ))]
            plt.scatter(activ,x)
            if i > 100:
                break
            i += 1

        plt.savefig("testplot.pdf")
            






