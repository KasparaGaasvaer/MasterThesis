import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime as dt
from matplotlib.dates import date2num
import json


#==============================Loading and storing slices==============================
"""
Class for reading and parsing twitter slice objects.
Purpose is to collect and store information from slices in dictionaries for easy extraction.
"""


class Slices:
    """
    Initialize class:
    - Create dicts for storing
    - Call methods for reading and sorting
    - Save dicts to .json files
    """
    def __init__(self, path_to_directory):
        self.path2dir = path_to_directory
        all_files = os.listdir(self.path2dir)     #List all files in dir = self.path2dir
        self.all_slices = []                      #Container for all filenames to be used
        self.graphs = {}                          #Container for graphs made from all slices in dir
        self.slices = {}                          #Container for all information about all slices in dir
        self.attributes_to_slice_set = {}         #Container for information about the entire set of slices in dir

        #Find all slice folders and sort after number
        nums = []
        for file in all_files:
            if "slice_" in file:
                self.all_slices.append(file)
                s, num = file.split("_")
                nums.append(int(num))
        nums, self.all_slices = zip(*sorted(zip(nums,self.all_slices)))

        #Calls function for reading slices and extracting information
        self.ReadSlice()

        path2save = self.path2dir.split("/")[1]
        path2save = "./" + path2save +"/"

        dict_dir = path2save + "parsed_dictionaries/"
        if not os.path.exists(dict_dir):
            os.makedirs(dict_dir)

        #Saves graphs to .json file
        with open(dict_dir + 'graph_all_slices.json', 'w') as fp:
           json.dump(self.graphs, fp)

        #Saves slices with attributes to .json file
        with open(dict_dir + 'all_slices.json', 'w') as fp:
            json.dump(self.slices, fp)

        #Saves common attributes of all slices to .json file
        with open(dict_dir + 'attributes_to_all_slices.json', 'w') as fp:
            json.dump(self.attributes_to_slice_set, fp)

    def ReadSlice(self):
        #Loops over all slices in dir
        for slices in self.all_slices:
            folder = slices
            self.slice_num = int(slices.replace("slice_",""))   #Extracts slice number
            print("Working on slice_",self.slice_num)
            self.path = self.path2dir + folder +"/"             #Sets path
            self.make_node_attributes()                         #Calls function for producing dict with node attributes from corresponding labels.csv file
            self.make_graph_dict()                                   #Calls function for producing networkx graph from corresponding graph.mat file
            self.find_timeline()                               #Calls function for extracting first and last tweet in slice
            self.find_num_nodes()                              #Calls function for extracting number of nodes (tweets) in slice
        self.find_timeline_of_set()                            #Calls function for extracting first and last tweet in the entire set of slices in dir



    def make_node_attributes(self):
        """
        Function for reading .csv file containing node attributes.
        Stores attributes in dictionary accessable by key = node number
        in main dictionary self.slices
        """

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

        self.slices[str(self.slice_num)] = {'node_attributes':self.node_attributes}

    def make_graph_dict(self):
        """
        Function for reading .mat file containg edges between nodes.
        Utilizes networkx package to create graph objects.
        Stores graph objects in self.graphs.
        """
        filename = self.path + "graph_" + str(self.slice_num) + ".mat"
        types = ["source", "target", "weight"]
        dataframe = pd.read_csv(filename, names = types, delim_whitespace = True)
        dataframe = dataframe.to_dict(orient='list')
        self.graphs[str(self.slice_num)] = dataframe

    def find_timeline_of_set(self):
        """
        Function for finding the first and last tweets posted in set of slices.
        Adds findings as attribute to dict self.attributes_to_slice_set.
        """
        first_date = "2100-06-10-20-38-27-000"
        first_date = dt.datetime.strptime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
        first_node = 0
        last_node = 0
        last_date = "1900-06-10-20-38-27-000"
        last_date = dt.datetime.strptime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
        first_slice = '1'
        last_slice = '1'
        for slice in self.slices:
            date = self.slices[slice]['start_date']
            date = dt.datetime.strptime(date,"%Y-%m-%d-%H-%M-%S-%f")
            if date < first_date:
                first_date = date
                first_node = self.slices[slice]['start_date_node_index']
                first_slice = slice
            date = self.slices[slice]['end_date']
            date = dt.datetime.strptime(date,"%Y-%m-%d-%H-%M-%S-%f")
            if date > last_date:
                last_date = date
                last_node = self.slices[slice]['end_date_node_index']
                last_slice = slice

        first_date = dt.datetime.strftime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
        last_date = dt.datetime.strftime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
        self.attributes_to_slice_set['start_date'] = first_date
        self.attributes_to_slice_set['end_date'] = last_date
        self.attributes_to_slice_set['start_date_node_index'] = first_node
        self.attributes_to_slice_set['end_date_node_index'] = last_node
        self.attributes_to_slice_set['start_slice'] = first_slice
        self.attributes_to_slice_set['end_slice'] = last_slice

    def find_timeline(self):
        """
        Function for finding the first and last tweet posted in slice.
        Adds findings as attribute to dict self.slices.
        """
        first_date = "2100-06-10T20:38:27.000"
        first_date = dt.datetime.strptime(first_date,"%Y-%m-%dT%H:%M:%S.%f")
        first_node = 0
        last_node = 0
        last_date = "1900-06-10T20:38:27.000"
        last_date = dt.datetime.strptime(last_date,"%Y-%m-%dT%H:%M:%S.%f")

        for n in self.node_attributes:
            date = self.node_attributes[n]["date"]
            date = dt.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f")
            if date <= first_date:
                first_date = date
                first_node = n
            if date >= last_date:
                last_date = date
                last_node = n


        first_date = dt.datetime.strftime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
        last_date = dt.datetime.strftime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
        self.slices[str(self.slice_num)]['start_date'] = first_date
        self.slices[str(self.slice_num)]['end_date'] = last_date
        self.slices[str(self.slice_num)]['start_date_node_index'] = first_node
        self.slices[str(self.slice_num)]['end_date_node_index'] = last_node

    def find_num_nodes(self):
        """Function for finding number of nodes in a slice"""
        self.slices[str(self.slice_num)]['num_nodes'] = len(self.slices[str(self.slice_num)]['node_attributes'].keys())







# What to do with metrics and components?  num components, num deleted users, clustering coefficient, slices over time starts somewhere and the networks expands
# from one source or severeal sources. Whiche source grows faster/bigger?
#bot or not?
# How "important" is a very active user?
#
