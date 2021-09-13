import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime as dt



class Slices:
    def __init__(self, path_to_directory):
        self.path2dir = path_to_directory
        all_files = os.listdir(self.path2dir)
        #self.all_slices = ["slice_1","slice_2"]
        self.all_slices = []
        self.graphs = []
        self.slices = {} #Add first and llast date as keys


        for file in all_files:
            if "slice_" in file:
                self.all_slices.append(file)

        self.ReadSlice()


    def ReadSlice(self):
        for slices in self.all_slices:
            self.folder = slices
            self.slice_num = int(slices.replace("slice_",""))
            self.path = self.path2dir + self.folder +"/"
            self.make_node_attributes()
            self.make_graph()
            self.find_timeline()
            self.find_num_nodes()

        self.find_num_deleted_users()

    def make_node_attributes(self):
        filename = self.path + "labels_" + str(self.slice_num) + ".csv"
        self.node_at = pd.read_csv(filename,header = 0, quotechar='"', error_bad_lines=False, warn_bad_lines=True,false_values= ['false'], true_values= ['true'])
        #self.node_at = self.node_at.fillna(value=False)
        self.node_at = self.node_at.to_dict(orient='list')
        self.node_attributes = {}
        nodes = len(self.node_at['index'])
        keyss = len(self.node_at.keys())
        key_list = list(self.node_at)
        for idx,i in enumerate(self.node_at['index']):
            self.node_attributes[i] = {}
            for key in self.node_at.keys():
                self.node_attributes[i][key] = self.node_at[key][idx]

        #print(self.node_attributes)




    def make_graph(self):
        filename = self.path + "graph_" + str(self.slice_num) + ".mat"
        types = ["source", "target", "weight"]
        dataframe = pd.read_csv(filename, names = types, delim_whitespace = True)
        self.G = nx.from_pandas_edgelist(dataframe, types[0], types[1], edge_attr = types[2])
        nx.set_node_attributes(self.G, self.node_attributes)
        #print(self.G)
        #nodes = self.G.nodes()
        #for n in nodes:
            #nodes[n]['color'] = 'm' if nodes[n]["statuses_count"] > 100000 else "c"
        #node_colors = [nodes[n]["color"] for n in nodes]
        #nx.draw(self.G, with_labels=True, node_color = node_colors)
        #plt.show()

        self.graphs.append(self.G)
        self.slices[str(self.slice_num)] = {'graph':self.G}
        self.slices[str(self.slice_num)]['node_attributes'] = self.node_attributes


    def find_timeline(self):

        print("Working on slice_",self.slice_num)
        first_date = "2100-06-10T20:38:27.000"
        first_date = dt.datetime.strptime(first_date,"%Y-%m-%dT%H:%M:%S.%f")
        first_node = 0
        last_node = 0
        last_date = "1900-06-10T20:38:27.000"
        last_date = dt.datetime.strptime(last_date,"%Y-%m-%dT%H:%M:%S.%f")

        for n in self.node_attributes:
            date = self.node_attributes[n]["date"]
            date = dt.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f")
            if date < first_date:
                first_date = date
                first_node = n
            if date > last_date:
                last_date = date
                last_node = n


        first_date = dt.datetime.strftime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
        last_date = dt.datetime.strftime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
        self.slices[str(self.slice_num)]['start_date'] = first_date
        self.slices[str(self.slice_num)]['end_date'] = last_date
        self.slices[str(self.slice_num)]['start_date_node_index'] = first_node
        self.slices[str(self.slice_num)]['end_date_node_index'] = last_node
        #VERY SLOW, MUST FIND BETTER WAY

        first_date = "2100-06-10T20:38:27.000"
        first_date = dt.datetime.strptime(first_date,"%Y-%m-%dT%H:%M:%S.%f")
        first_node = 0
        last_node = 0
        last_date = "1900-06-10T20:38:27.000"
        last_date = dt.datetime.strptime(last_date,"%Y-%m-%dT%H:%M:%S.%f")


    def find_num_nodes(self):
        self.slices[str(self.slice_num)]['num_nodes'] = len(self.slices[str(self.slice_num)]['node_attributes'].keys())

    def find_num_components(self):
        a = 1

    def find_num_deleted_users(self):
        #for key in sorted(self.slices):
        #    print("%s: %s" % (key, self.slices[key]))
        sorted_slices = (sorted(self.slices.keys()))
        start = []
        end = []
        s = []
        print("       Start date                          End date                 Slice num")
        for i in sorted_slices:
            #print("%s        %s           %s" %(self.slices[i]['start_date'],self.slices[i]['end_date'],i))
            start.append(self.slices[i]['start_date'])
            end.append(self.slices[i]['end_date'])
            s.append(int(i))
        #print(s)

        #print(sorted(zip(s,start,end)))

        for sl, st, ed in sorted(zip(s,start,end)):
            print("%s        %s           %i" %(st, ed, sl))


    def find_clustering_coef(self):
        a = 1








# What to do with metrics and components? Number of nodes, num components, num deleted users, clustering coefficient, slices over time starts somewhere and the networks expands
# from one source or severeal sources. Whiche source grows faster/bigger?
#bot or not?
# How "important" is a very active user?
#
