import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import datetime as dt
from matplotlib.dates import date2num



class Slices:
    def __init__(self, path_to_directory):
        self.path2dir = path_to_directory
        all_files = os.listdir(self.path2dir)
        #self.all_slices = ["slice_1","slice_2"]
        self.all_slices = []
        self.graphs = []
        self.slices = {} #Add first and llast date as keys
        self.attributes_to_slice_set = {}


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
        self.find_timeline_of_set()
        #self.plot_dates_dist()
        #self.find_num_deleted_users()
        self.plot_tweets_before_2020()

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

    def plot_tweets_before_2020(self):
        tweets = []
        for slice in self.slices:
            tweets.append(0)
        tweets.append(0)

        boundary = dt.datetime(2020,1,1)
        for slice in self.slices:
            nodes = self.slices[slice]['node_attributes']
            num_nodes = self.slices[slice]['num_nodes']
            #print("Number of nodes in slice %s = %i" %(slice,num_nodes))
            for n in nodes:
                date = dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f")
                if date < boundary:
                    tweets[int(slice)] += 1
            #tweets[int(slice)]/=num_nodes

        tweets.pop(0)
        #print(tweets)

        names = sorted([slice for slice in self.slices])
        x_pos = [int(i) for i in names]
        zeros = [0 for i in range(len(tweets))]

        plt.vlines(x = x_pos, ymin = zeros, ymax = tweets, lw = 2)
        #for i in range(len(tweets)):
        #    plt.text(x_pos[i],tweets[i],names[i])
        plt.ylim(ymin=0)
        plt.title("Tweets before 2020",fontsize = 14)
        plt.xlabel("Slice number", fontsize = 12)
        #plt.ylabel("$\\frac{\mathrm{Number\,of\,tweets\,<\,2020}}{\mathrm{Total\,number\,of\,tweets\,in\,slice}}$", fontsize = 14)
        plt.ylabel("Number of tweets before 2020", fontsize = 12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        plt.savefig("./experiment6/plots/num_tweets_before_2020/bins.jpg")
        plt.clf()





    def plot_dates_dist(self):
        three_months = dt.timedelta(days = 90)
        for slice in self.slices:
            start = dt.datetime.strptime(self.slices[slice]['start_date'],"%Y-%m-%d-%H-%M-%S-%f")
            end = dt.datetime.strptime(self.slices[slice]['end_date'],"%Y-%m-%d-%H-%M-%S-%f")
            date_list = []
            nodes = self.slices[slice]['node_attributes']
            for n in nodes:
                date_list.append(dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f"))

            date_list.remove(start)
            date_list_num = date2num(date_list)
            bins = np.arange(date_list_num.min(), date_list_num.max()+1, 90)

            plt.title("Slice "+slice,fontsize = 14)
            plt.xlabel("Date", fontsize = 14)
            plt.ylabel("Number of tweets", fontsize = 14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.hist(date_list,bins = bins)
            plt.savefig("./experiment6/plots/num_tweets_three_month_bins/Slice_" +slice + ".jpg")
            plt.clf()

    def find_timeline_of_set(self):
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


    def find_clustering_coef(self):
        a = 1








# What to do with metrics and components? Number of nodes, num components, num deleted users, clustering coefficient, slices over time starts somewhere and the networks expands
# from one source or severeal sources. Whiche source grows faster/bigger?
#bot or not?
# How "important" is a very active user?
#
