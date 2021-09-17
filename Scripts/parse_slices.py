import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime as dt
from matplotlib.dates import date2num
import json

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
        #self.all_slices = ["slice_1","slice_2"]
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


        with open(path2save + 'all_slices.json', 'w') as fp:
            json.dump(self.slices, fp)

        with open(path2save + 'attributes_to_all_slices.json', 'w') as fp:
            json.dump(self.attributes_to_slice_set, fp)

    def ReadSlice(self):
        #Loops over all slices in dir
        for slices in self.all_slices:
            folder = slices
            self.slice_num = int(slices.replace("slice_",""))   #Extracts slice number
            print("Working on slice_",self.slice_num)
            self.path = self.path2dir + folder +"/"             #Sets path
            self.make_node_attributes()                         #Calls function for producing dict with node attributes from corresponding labels.csv file
            self.make_graph()                                   #Calls function for producing networkx graph from corresponding graph.mat file
            #self.find_timeline()                               #Calls function for extracting first and last tweet in slice
            #self.find_num_nodes()                              #Calls function for extracting number of nodes (tweets) in slice
        #self.find_timeline_of_set()                            #Calls function for extracting first and last tweet in the entire set of slices in dir
        #self.plot_dates_dist()                                 #Calls function for plotting time distribution of tweets in slices  (one plot for each slice)
        #self.find_num_deleted_users()                          #Calls function for finding the number of deleted users from first to last slice
        #self.plot_tweets_before_2020()                         #Calls function for plotting tweets before 2020 in all slices (same plot)
        #self.simple_information_txt()

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

        #print(self.node_attributes)
        self.slices[str(self.slice_num)] = {'node_attributes':self.node_attributes}




    def make_graph(self):
        """
        Function for reading .mat file containg edges between nodes.
        Utilizes networkx package to create graph objects.
        Stores graph objects in self.graphs.
        FIND WAY TO STORE!!
        """
        filename = self.path + "graph_" + str(self.slice_num) + ".mat"
        types = ["source", "target", "weight"]
        dataframe = pd.read_csv(filename, names = types, delim_whitespace = True)
        self.G = nx.from_pandas_edgelist(dataframe, types[0], types[1], edge_attr = types[2])
        nx.set_node_attributes(self.G, self.node_attributes)
        #print(self.G)
        #nodes = self.G.nodes()
        #for n in nodes:
        #    nodes[n]['color'] = 'm' if nodes[n]["statuses_count"] > 100000 else "c"
        #node_colors = [nodes[n]["color"] for n in nodes]
        nx.draw(self.G, with_labels=True, node_color = node_colors)
        plt.show()

        self.graphs[str(self.slice_num)] = self.G


    def plot_tweets_before_2020(self):
        """
        Function for plotting histogram of number of tweets (normalized and not normalized)
        before 2020. Produces one plot.
        """
        tweets = []
        slice_arange = []
        boundary = dt.datetime(2020,1,1)
        for slice in self.slices:
            nodes = self.slices[slice]['node_attributes']
            num_nodes = self.slices[slice]['num_nodes']
            counter = 0
            for n in nodes:
                date = dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f")
                if date < boundary:
                    counter += 1
            tweets.append(counter/num_nodes)
            #tweets.append(counter)
            slice_arange.append(int(slice))

        slice_arange,tweets = zip(*sorted(zip(slice_arange,tweets)))

        zeros = [0 for i in range(len(tweets))]

        plt.vlines(x = slice_arange, ymin = zeros, ymax = tweets, lw = 2)
        plt.ylim(ymin=0)
        plt.title("Tweets before 2020",fontsize = 14)
        plt.xlabel("Slice number", fontsize = 12)
        plt.ylabel("$\\frac{\mathrm{Number\,of\,tweets\,<\,2020}}{\mathrm{Total\,number\,of\,tweets\,in\,slice}}$", fontsize = 14)
        #plt.ylabel("Number of tweets before 2020", fontsize = 12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        plt.savefig("./experiment6/plots/num_tweets_before_2020/normalized_bins.jpg")
        #plt.savefig("./experiment6/plots/num_tweets_before_2020/bins.jpg")
        plt.clf()




    def plot_dates_dist(self):
        """
        Function for plotting time distibution of tweets.
        Produces one plot for each slice.
        """
        three_months = dt.timedelta(days = 90)
        bin_size_in_days = 90
        for slice in self.slices:
            date_list = []
            nodes = self.slices[slice]['node_attributes']
            for n in nodes:
                date_list.append(dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f"))

            date_list_num = date2num(date_list)
            bins = np.arange(date_list_num.min(), date_list_num.max()+1, bin_size_in_days)

            plt.title("Slice "+slice,fontsize = 14)
            plt.xlabel("Date", fontsize = 14)
            plt.ylabel("Number of tweets", fontsize = 14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.hist(date_list,bins = bins)
            plt.savefig("./experiment6/plots/num_tweets_three_month_bins/Slice_" +slice + ".jpg")
            plt.clf()

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


    def find_num_deleted_users(self):
        """
        Functions for locating missing users in slice_x, x!= 1, based on users in slice_1.
        """
        ids_first_slice = []
        users = self.slices['1']['node_attributes']
        for user in users:
            ids_first_slice.append(users[user]['id'])

        self.deleted_users  = []
        self.deleted_users_slice = []
        for slice in self.slices:
            ids = []
            if slice != '1':
                users = self.slices[slice]['node_attributes']
                for user in users:
                    ids.append(users[user]['id'])
                #print("\n\n",len(ids),"\n\n")
                for index in ids_first_slice:
                    if index not in ids:
                        self.deleted_users.append(index)
                        self.deleted_users_slice.append(int(slice))
                        print("user %s was deleted in slice %s" % (index, slice))
                    #else:
                        #print("user %s still in set in slice %s" %(index, slice))

        """
        count_deleted_users = np.zeros(max(self.deleted_users_slice)+1)
        for i in range(len(self.deleted_users)):
            idx = self.deleted_users_slice[i]
            count_deleted_users[idx] += 1

        print(count_deleted_users)
        """


    def simple_information_txt(self):
        #for key in sorted(self.slices):
        #    print("%s: %s" % (key, self.slices[key]))
        sorted_slices = (sorted(self.slices.keys()))
        start = []
        end = []
        s = []
        print("       Start date                          End date                 Slice num     Num nodes in slice")
        for i in sorted_slices:
            #print("%s        %s           %s" %(self.slices[i]['start_date'],self.slices[i]['end_date'],i))
            start.append(self.slices[i]['start_date'])
            end.append(self.slices[i]['end_date'])
            s.append(int(i))
        #print(s)

        #print(sorted(zip(s,start,end)))

        with open("./experiment6/dates.txt","w") as outfile:
            outfile.write("       Start date                          End date                 Slice num     Num nodes in slice\n")
            for sl, st, ed in sorted(zip(s,start,end)):
                outfile.write("%s        %s           %i               %i\n" %(st, ed, sl, int(self.slices[str(sl)]['num_nodes'])))








# What to do with metrics and components?  num components, num deleted users, clustering coefficient, slices over time starts somewhere and the networks expands
# from one source or severeal sources. Whiche source grows faster/bigger?
#bot or not?
# How "important" is a very active user?
#
