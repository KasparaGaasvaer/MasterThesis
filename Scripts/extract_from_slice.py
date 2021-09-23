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
    def __init__(self, path):

        self.outer_path = path

        with open(self.outer_path + "all_slices.json", 'r') as fp:
            self.slices = json.load(fp)

        with open(self.outer_path + "attributes_to_all_slices.json", 'r') as fp:
            self.common_attributes = json.load(fp)


        with open(self.outer_path + "graph_all_slices.json", 'r') as fp:
            self.graphs = json.load(fp)

        self.nx_graphs = {}
        self.do_stuff()


    def do_stuff(self):
        for slice in self.slices.keys():
            self.slice_num = int(slice)
            self.node_attributes = self.slices[slice]['node_attributes']
            #self.make_graph()
            #self.find_clustering_coef(self.nx_graphs[str(self.slice_num)])
        #self.plot_nx_graph(self.nx_graph['1'])#[str(self.slice_num)])
        #self.produce_deltas()
        self.load_deltas()
        #self.find_num_deleted_users(self.slices)
        #self.plot_dates_dist(self.delta_slices, plot_folder = "delta_slices/")
        #self.plot_tweets_before_2020(self.delta_slices, plot_folder = "delta_slices/")


    def load_deltas(self):
        with open(self.outer_path + 'delta_slices.json', 'r') as fp:
            self.delta_slices = json.load(fp)


    def find_num_nodes(self,slices_dict):
        for slice in slices_dict:
            slices_dict[slice]['num_nodes'] = len(slices_dict[slice]['node_attributes'].keys())

    def make_graph(self):
        graph = self.graphs[str(self.slice_num)]
        sources = graph['source']
        targets = graph['target']
        weights = graph['weight']
        list_of_edges = []
        for i in range(len(sources)):
            list_of_edges.append((str(sources[i]),str(targets[i]),{'weight': weights[i]}))

        G = nx.Graph()
        G.add_edges_from(list_of_edges)
        nx.set_node_attributes(G, self.node_attributes)
        self.nx_graphs[str(self.slice_num)] = {'graph':G}

    def plot_nx_graph(self, graph):
        graph_obj = graph['graph']
        nodes = graph_obj.nodes()
        for n in nodes:
            nodes[n]['color'] = 'm' if nodes[n]["statuses_count"] > 100000 else "c"
        node_colors = [nodes[n]["color"] for n in nodes]
        nx.draw(graph_obj, with_labels=True, node_color = node_colors)
        plt.show()

    def find_clustering_coef(self,graph):
        CC = nx.average_clustering(graph['graph'])
        graph['CC'] = CC

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
        with open(self.outer_path + 'delta_slices.json', 'w') as fp:
            json.dump(self.delta_slices, fp)


    def plot_dates_dist(self, slices_dict,plot_folder):
        days_delta = 90    #Bin size in days
        for slice in slices_dict:
            date_list = []
            nodes = slices_dict[slice]['node_attributes']
            for n in nodes:
                date_list.append(dt.datetime.strptime((nodes[n]['date']),"%Y-%m-%dT%H:%M:%S.%f"))

            date_list_num = date2num(date_list)
            bins = np.arange(date_list_num.min(), date_list_num.max()+1, days_delta)

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

    def find_timeline(self, slices_dict):
        """
        Function for finding the first and last tweet posted in slice.
        Adds findings as attribute to dict self.slices.
        """
        for slice in slices_dict.keys():
            atts = slices_dict[slice]['node_attributes']
            first_date = "2100-06-10T20:38:27.000"
            first_date = dt.datetime.strptime(first_date,"%Y-%m-%dT%H:%M:%S.%f")
            first_node = 0
            last_node = 0
            last_date = "1900-06-10T20:38:27.000"
            last_date = dt.datetime.strptime(last_date,"%Y-%m-%dT%H:%M:%S.%f")

            for n in atts.keys():
                date = atts[n]["date"]
                date = dt.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f")
                if date <= first_date:
                    first_date = date
                    first_node = n
                if date >= last_date:
                    last_date = date
                    last_node = n


            first_date = dt.datetime.strftime(first_date,"%Y-%m-%d-%H-%M-%S-%f")
            last_date = dt.datetime.strftime(last_date,"%Y-%m-%d-%H-%M-%S-%f")
            slices_dict[slice]['start_date'] = first_date
            slices_dict[slice]['end_date'] = last_date
            slices_dict[slice]['start_date_node_index'] = first_node
            slices_dict[slice]['end_date_node_index'] = last_node


    def find_num_deleted_users(self, slices_dict):
        """
        Functions for locating missing users in slice_x, x!= 1, based on users in slice_1.
        """
        ids_first_slice = []
        users = slices_dict['1']['node_attributes']
        for user in users:
            ids_first_slice.append(users[user]['id'])

        self.deleted_users  = []
        self.deleted_users_slice = []
        for slice in slices_dict:
            ids = []
            if slice != '1':
                users = slices_dict[slice]['node_attributes']
                for user in users:
                    ids.append(users[user]['id'])
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
