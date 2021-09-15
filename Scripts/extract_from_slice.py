import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import copy

from parse_slices import *


#Figure out how to save nx.graphs

class ExtractSlices():
    def __init__(self, slice_file, common_attributes_file):

        with open(slice_file, 'r') as fp:
            self.slices = json.load(fp)

        with open(common_attributes_file, 'r') as fp:
            self.common_attributes = json.load(fp)


        self.graphs = {}
        self.do_stuff()
        #print(self.graphs)


    def do_stuff(self):
        #for slice in self.slices:
            #self.slice_num = int(slice)
            #self.node_attributes = self.slices[slice]['node_attributes']
            #self.make_graph()
            #self.find_clustering_coef()
        #self.produce_deltas()
        self.load_deltas()
        self.plot_dates_dist(self.delta_slices, plot_folder = "delta_slices/")
        self.plot_tweets_before_2020(self.delta_slices, plot_folder = "delta_slices/")

    def load_deltas(self):
        with open("./experiment6/"+ 'delta_slices.json', 'r') as fp:
            self.delta_slices = json.load(fp)


    def find_num_nodes(self,slices_dict):
        for slice in slices_dict:
            slices_dict[slice]['num_nodes'] = len(slices_dict[slice]['node_attributes'].keys())

    def make_graph(self):
        path ="./experiment6/experiment_6/slice_" + str(self.slice_num) + "/"
        filename = path + "graph_" + str(self.slice_num) + ".mat"
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

        self.graphs[str(self.slice_num)] = {'graph' :self.G}

    def find_clustering_coef(self):
        CC = nx.average_clustering(self.graphs[str(self.slice_num)]['graph'])
        self.graphs[str(self.slice_num)]['CC'] = CC

    def find_num_components(self):
        a = 1

    #Should this be in parse_slices instead?
    def produce_deltas(self):
        self.delta_slices = copy.deepcopy(self.slices)
        for i in range(1,len(self.slices.keys())):
            id_in_1 = []
            j = i + 1
            slice1 = self.slices[str(i)]
            slice2 = self.slices[str(j)]
            for user in slice1['node_attributes']:
                id_in_1.append(slice1['node_attributes'][user]['id'])

            for user in slice2['node_attributes']:
                if slice2['node_attributes'][user]['id'] in id_in_1:
                    self.delta_slices[str(j)]['node_attributes'].pop(user)

            print("OG slice ", j," len = ",len(self.slices[str(j)]['node_attributes'].keys()))
            print("Delta slice ", j ," len =", len(self.delta_slices[str(j)]['node_attributes'].keys()))


        self.find_num_nodes(self.delta_slices)
        self.find_timeline(self.delta_slices)
        with open("./experiment6/" + 'delta_slices.json', 'w') as fp:
            json.dump(self.delta_slices, fp)


    def find_timeline(self, slices_dict):
        for slice in slices_dict:
            first_date = "2100-06-10-20-38-27-000"
            first_date = dt.datetime.strptime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
            first_node = 0
            last_node = 0
            last_date = "1900-06-10-20-38-27-000"
            last_date = dt.datetime.strptime(last_date,"%Y-%m-%d-%H-%M-%S-%f")

            attributes = slices_dict[slice]['node_attributes']
            for node in attributes:
                date = attributes[node]['date']
                date = dt.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f")
                if date <= first_date:
                    first_date = date
                    first_node = node
                if date >= last_date:
                    last_date = date
                    last_node = node


            first_date = dt.datetime.strftime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
            last_date = dt.datetime.strftime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
            slices_dict[slice]['start_date'] = first_date
            slices_dict[slice]['end_date'] = last_date
            slices_dict[slice]['start_date_node_index'] = first_node
            slices_dict[slice]['end_date_node_index'] = last_node


    def plot_dates_dist(self, slices_dict,plot_folder):
        #three_months = dt.timedelta(days = 90)
        for slice in slices_dict:
            #start = dt.datetime.strptime(slices_dict[slice]['start_date'],"%Y-%m-%d-%H-%M-%S-%f")
            #end = dt.datetime.strptime(slices_dict[slice]['end_date'],"%Y-%m-%d-%H-%M-%S-%f")
            date_list = []
            nodes = slices_dict[slice]['node_attributes']
            for n in nodes:
                date_list.append(dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f"))

            date_list_num = date2num(date_list)
            bins = np.arange(date_list_num.min(), date_list_num.max()+1, 90)

            plt.title("Slice "+slice,fontsize = 14)
            plt.xlabel("Date", fontsize = 14)
            plt.ylabel("Number of tweets", fontsize = 14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.hist(date_list,bins = bins)
            plt.savefig("./experiment6/plots/"+plot_folder+"num_tweets_three_month_bins/Slice_" +slice + ".jpg")
            plt.clf()

    def plot_tweets_before_2020(self, slices_dict, plot_folder):
        tweets = []
        slice_arange = []
        boundary = dt.datetime(2020,1,1)
        for slice in slices_dict:
            nodes = slices_dict[slice]['node_attributes']
            num_nodes = slices_dict[slice]['num_nodes']
            counter = 0
            for n in nodes:
                date = dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f")
                if date < boundary:
                    counter += 1
            #tweets.append(counter/num_nodes)
            tweets.append(counter)
            slice_arange.append(int(slice))

        slice_arange,tweets = zip(*sorted(zip(slice_arange,tweets)))

        zeros = [0 for i in range(len(tweets))]

        plt.vlines(x = slice_arange, ymin = zeros, ymax = tweets, lw = 2)
        plt.ylim(ymin=0)
        plt.title("Tweets before 2020",fontsize = 14)
        plt.xlabel("Slice number", fontsize = 12)
        #plt.ylabel("$\\frac{\mathrm{Number\,of\,tweets\,<\,2020}}{\mathrm{Total\,number\,of\,tweets\,in\,slice}}$", fontsize = 14)
        plt.ylabel("Number of tweets before 2020", fontsize = 12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        #plt.savefig("./experiment6/plots/"+plot_folder+"num_tweets_before_2020/normalized_bins.jpg")
        plt.savefig("./experiment6/plots/"+plot_folder+"num_tweets_before_2020/bins.jpg")
        plt.clf()
        #plt.show()














        #print(self.slices["1"].keys())


            #finne alle (id) brukere i 1, identifisere de i 2, fjerne de fra to ved å finne indexen og fjerne hele keyen
            #kopier hele nye slice til ny dict
            #Slice[slice_2] = dict_keys(['node_attributes', 'start_date', 'end_date', 'start_date_node_index', 'end_date_node_index', 'num_nodes'])
            #self.slices['1']['node_attributes'].keys() = ['0',...,'1800']
