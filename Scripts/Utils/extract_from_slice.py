import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import os
import sys
import copy
import json
sys.path.append(
    ".."
)  # Adds higher directory to python modules path

# from parse_slices import *

from Utils.dict_opener import OpenDict

# ==============================Extracting from slices dictionaries==============================
    #
    # Class for extracting simple information from slices dictionaries (from Slices class)
    # - Produce NetworkX graphs
    # - Visualize NetworkX graphs
    # - Find clustering coefficient from NetworkX graphs
    # - Produce delta slices
    # - Find number of deleted users from one slice to another
    # - Plot distribution of tweets (3 month intervals for now)
    # - Plot distribution of tweets before 2020


class ExtractSlices():

    def __init__(self, path):
        """Contructor

        Args:
            path (string): path to experiment data
        """
        self.path = path
        self.outer_path = self.path + "parsed_dictionaries/"
        if not os.path.exists(self.outer_path):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment pleae input no")
            if int(k_value):
                self.path = self.path + "k_" + str(k_value) + "/"
                self.outer_path = self.path + "parsed_dictionaries/"

        OpenDicts = OpenDict(self.path)
        #self.slices, self.common_attributes, self.graphs = OpenDicts.open_dicts(["slices", "attributes","graphs"])
        self.graphs = OpenDicts.open_dicts(["graphs"])

        self.nx_graphs = {}
        # self.all_slices_graphs()
        self.extract()

    def extract(self):
        """Call-method for looping over all slices in experiment data"""

        for slice in self.slices.keys(): #This is safe for all slices
        #for slice in range(1,101):  #Specific for exp7
            slice = str(slice)
            self.slice_num = int(slice)
            # self.node_attributes = self.slices[slice]['node_attributes']
            self.make_graph()
            self.find_clustering_coef(self.nx_graphs[str(self.slice_num)])
            print("finished slice ", slice)
        self.plot_nx_graph(self.nx_graphs['1'])#[str(self.slice_num)])
        # self.produce_deltas()
        #self.load_delta_graphs()
        #print("Deltas graphs loaded")
        #self.test_delta_lenght()
        # self.produce_delta_graph_dict_v2()
        # print("delta graphs produced")
        # self.find_num_nodes(self.delta_slices)
        # self.find_num_deleted_users(self.slices)
        # self.plot_dates_dist(self.delta_slices, plot_folder = "delta_slices/")
        # self.plot_tweets_before_2020(self.delta_slices, plot_folder = "delta_slices/")

    def all_slices_graphs(self):
        for slice in self.slices.keys():
            self.slice_num = int(slice)
            self.node_attributes = self.slices[slice]["node_attributes"]
            self.make_graph()

    def load_delta_graphs(self):
        with open(self.outer_path + "delta_graphs_v2.json", "r") as fp:
            self.delta_graphs = json.load(fp)

    def load_deltas(self):
        with open(self.outer_path + "delta_slices.json", "r") as fp:
            self.delta_slices = json.load(fp)

    def find_num_nodes(self, slices_dict):
        for slice in slices_dict:
            slices_dict[slice]["num_nodes"] = len(
                slices_dict[slice]["node_attributes"].keys()
            )

    def make_graph(self):
        """Method for producing NetworkX graph.

           - Adds node attributes from slices dict and edges/nodes from graph dict.
          """

        graph = self.graphs[str(self.slice_num)]
        sources = graph["source"]
        targets = graph["target"]
        weights = graph["weight"]
        list_of_edges = []
        for i in range(len(sources)):
            list_of_edges.append(
                (str(sources[i]), str(targets[i]), {"weight": weights[i]})
            )

        G = nx.Graph()
        G.add_edges_from(list_of_edges)
        #nx.set_node_attributes(G, self.node_attributes)
        self.nx_graphs[str(self.slice_num)] = {"graph": G}

    def plot_nx_graph(self, graph):
        """Method for plotting NetworkX graph.

        Args:
            graph (NetworkX graph object): Graph to be plotted
        """

        graph_obj = graph["graph"]
        nodes = graph_obj.nodes()
        #for n in nodes:
            #nodes[n]["color"] = "m" if nodes[n]["followers_count"] > 10000 else "c"
        #node_colors = [nodes[n]["color"] for n in nodes]
        nx.draw(graph_obj)#, node_color=node_colors)
        #plt.show()
        plt.savefig("test_delta_plot.pdf")

    def find_clustering_coef(self, graph):
        CC = nx.average_clustering(graph["graph"])
        graph["CC"] = CC

    def find_num_components(self):
        a = 1

    def plot_dates_dist(self, slices_dict, plot_folder):
        """Method for plotting time distribution of tweets.

        - Produces N-plots (N = number of slices in experiment) with time period on the x-axis
          number of tweets in time period on y-axis.

        Args:
            slices_dict (dictionary): Dictionary of slices
            plot_folder (string): Name of folder to save plots
        """

        days_delta = 90  # Bin size in days
        for slice in slices_dict:
            date_list = []
            nodes = slices_dict[slice]["node_attributes"]
            for n in nodes:
                date_list.append(
                    dt.datetime.strptime((nodes[n]["date"]), "%Y-%m-%dT%H:%M:%S.%f")
                )

            date_list_num = date2num(date_list)
            bins = np.arange(date_list_num.min(), date_list_num.max() + 1, days_delta)

            plt.title("Slice " + slice, fontsize=14)
            plt.xlabel("Date", fontsize=14)
            plt.ylabel("Number of tweets", fontsize=14)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)
            plt.hist(date_list, bins=bins)
            plt.savefig(
                "./experiment6/plots/"
                + plot_folder
                + "num_tweets_three_month_bins/Slice_"
                + slice
                + ".jpg"
            )
            plt.clf()

    def plot_tweets_before_2020(self, slices_dict, plot_folder):
        """Method for plotting tweets before 2020.

        - Produces one plot with slices on x-axis and normalized or not normalized
          number of tweets before 2020 in that slice.

        Args:
            slices_dict (dictionary): Dictionary of slices
            plot_folder (string): Name of folder to save plots
        """


        tweets = []
        slice_arange = []
        boundary = dt.datetime(2020, 1, 1)
        for slice in slices_dict:
            nodes = slices_dict[slice]["node_attributes"]
            num_nodes = slices_dict[slice]["num_nodes"]
            counter = 0
            for n in nodes:
                date = dt.datetime.strptime((nodes[n]["date"]), "%Y-%m-%dT%H:%M:%S.%f")
                if date < boundary:
                    counter += 1
            # tweets.append(counter/num_nodes)
            tweets.append(counter)
            slice_arange.append(int(slice))

        slice_arange, tweets = zip(*sorted(zip(slice_arange, tweets)))

        zeros = [0 for i in range(len(tweets))]

        plt.vlines(x=slice_arange, ymin=zeros, ymax=tweets, lw=2)
        plt.ylim(ymin=0)
        plt.title("Tweets before 2020", fontsize=14)
        plt.xlabel("Slice number", fontsize=12)
        # plt.ylabel("$\\frac{\mathrm{Number\,of\,tweets\,<\,2020}}{\mathrm{Total\,number\,of\,tweets\,in\,slice}}$", fontsize = 14)
        plt.ylabel("Number of tweets before 2020", fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        # plt.savefig("./experiment6/plots/"+plot_folder+"num_tweets_before_2020/normalized_bins.jpg")
        plt.savefig(
            "./experiment6/plots/" + plot_folder + "num_tweets_before_2020/bins.jpg"
        )
        plt.clf()
        # plt.show()

    def find_timeline(self, slices_dict):
        """Method for finding the first and last tweet posted in slice.

        - Adds findings as attribute to dict self.slices.

        Args:
            slices_dict (dictionary): Dictionary of slices
        """


        for slice in slices_dict.keys():
            atts = slices_dict[slice]["node_attributes"]
            first_date = "2100-06-10T20:38:27.000"
            first_date = dt.datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S.%f")
            first_node = 0
            last_node = 0
            last_date = "1900-06-10T20:38:27.000"
            last_date = dt.datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S.%f")

            for n in atts.keys():
                date = atts[n]["date"]
                date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
                if date <= first_date:
                    first_date = date
                    first_node = n
                if date >= last_date:
                    last_date = date
                    last_node = n

            first_date = dt.datetime.strftime(first_date, "%Y-%m-%d-%H-%M-%S-%f")
            last_date = dt.datetime.strftime(last_date, "%Y-%m-%d-%H-%M-%S-%f")
            slices_dict[slice]["start_date"] = first_date
            slices_dict[slice]["end_date"] = last_date
            slices_dict[slice]["start_date_node_index"] = first_node
            slices_dict[slice]["end_date_node_index"] = last_node

    def find_num_deleted_users(self, slices_dict):
        """Method for locating missing users in slice_x, x!= 1, based on users in slice_1.

        Args:
            slices_dict (dictionary): Dictionary of slices
        """


        ids_first_slice = []
        users = slices_dict["1"]["node_attributes"]
        for user in users:
            ids_first_slice.append(users[user]["id"])

        self.deleted_users = []
        self.deleted_users_slice = []
        for slice in slices_dict:
            ids = []
            if slice != "1":
                users = slices_dict[slice]["node_attributes"]
                for user in users:
                    ids.append(users[user]["id"])
                for index in ids_first_slice:
                    if index not in ids:
                        self.deleted_users.append(index)
                        self.deleted_users_slice.append(int(slice))
                        print("user %s was deleted in slice %s" % (index, slice))
                    # else:
                    # print("user %s still in set in slice %s" %(index, slice))

        """
        count_deleted_users = np.zeros(max(self.deleted_users_slice)+1)
        for i in range(len(self.deleted_users)):
            idx = self.deleted_users_slice[i]
            count_deleted_users[idx] += 1

        print(count_deleted_users)
        """




    """
        # Should this be in parse_slices instead? Difficult since parse slices is optimized for parsing self.slices, not functions who takes dicts or files
        def produce_deltas(self):
            #
            # Function for producing delta slices.
            # Each delta slice is slice i+1 - slice i for all slices in experiment.
            #

            self.delta_slices = copy.deepcopy(self.slices)
            for i in range(1, len(self.slices.keys())):
                id_in_1 = []
                j = i + 1
                slice1 = self.slices[str(i)]
                slice2 = self.slices[str(j)]
                for user in slice1["node_attributes"]:
                    id_in_1.append(slice1["node_attributes"][user]["id"])

                for user in slice2["node_attributes"]:
                    if slice2["node_attributes"][user]["id"] in id_in_1:
                        self.delta_slices[str(j)]["node_attributes"].pop(user)

                print(
                    "OG slice ",
                    j,
                    " len = ",
                    len(self.slices[str(j)]["node_attributes"].keys()),
                )
                print(
                    "Delta slice ",
                    j,
                    " len =",
                    len(self.delta_slices[str(j)]["node_attributes"].keys()),
                )

            self.find_num_nodes(self.delta_slices)
            self.find_timeline(self.delta_slices)
            with open(self.outer_path + "delta_slices.json", "w") as fp:
                json.dump(self.delta_slices, fp)

        def produce_delta_graph_dict_v2(self):
            self.delta_graphs = copy.deepcopy(self.graphs)
            slices = list(self.slices.keys())
            slices = [int(s) for s in slices]
            slices.pop(0)
            for s in slices:
                idx = []
                g1 = self.graphs[str(s - 1)]
                g2 = self.graphs[str(s)]
                dg = self.delta_graphs[str(s)]
                delta_source = dg["source"]
                delta_target = dg["target"]
                delta_weight = dg["weight"]
                source1 = g1["source"]
                source2 = g2["source"]
                target1 = g1["target"]
                target2 = g2["target"]
                weight1 = g1["weight"]
                weight2 = g2["weight"]
                for i in range(len(source2)):
                    for j in range(len(source1)):
                        if (source1[j] == source2[i]) and (target1[j] == target2[i]):
                            if weight1[j] != weight2[i]:
                                weight2[i] -= weight1[j]

                            else:
                                idx.append(i)

                # print(sorted(idx))
                for i in sorted(idx, reverse=True):
                    delta_source.pop(i)
                    delta_target.pop(i)
                    delta_weight.pop(i)
                print("Done with slice ", s)

            self.test_dict_conservation(self.delta_graphs)

            # n1 =self.slices["1"]["num_nodes"]
            # n2 = self.slices["2"]["num_nodes"]
            # print(f"num_nodes s1 {n1}")
            # print(f"num_nodes s2 {n2}")

            # print("len all graphs 2 = ", len(self.graphs["2"]["source"]))
            # print("len delta graphs 2 = ", len(self.delta_graphs["2"]["source"]))

            with open(self.outer_path + "delta_graphs_v2.json", "w") as fp:
                json.dump(self.delta_graphs, fp)

        def produce_delta_graph_dict(self):
            # Insanely slow, but all other methods I've tried have failed.
            self.delta_graphs = {}
            for s in self.slices.keys():
                self.delta_graphs[s] = {"source": [], "target": [], "weight": []}
            for k in ["source", "target", "weight"]:
                self.delta_graphs["1"][k] = copy.deepcopy(self.graphs["1"][k])

            slices = list(self.slices.keys())
            slices = [int(s) for s in slices]
            slices.pop(0)
            for s in slices:
                g1 = self.graphs[str(s - 1)]
                g2 = self.graphs[str(s)]
                source1 = g1["source"]
                source2 = g2["source"]
                target1 = g1["target"]
                target2 = g2["target"]
                diff_s = np.setdiff1d(source2, source1, assume_unique=False)
                diff_t = np.setdiff1d(target2, target1, assume_unique=False)
                for v in range(len(source2)):
                    for d in diff_s:
                        if source2[v] == d:
                            for k in ["source", "target", "weight"]:
                                self.delta_graphs[str(s)][k].append(g2[k][v])
                    for t in diff_t:
                        if target2[v] == t:
                            for k in ["source", "target", "weight"]:
                                self.delta_graphs[str(s)][k].append(g2[k][v])

                print("Done with slice ", s)

            self.test_dict_conservation(self.delta_graphs)

            with open(self.outer_path + "delta_graphs.json", "w") as fp:
                json.dump(self.delta_graphs, fp)

        def test_dict_conservation(self, graph_dict):
            for s in graph_dict.keys():
                slice = graph_dict[s]
                assert len(slice["source"]) == len(slice["target"])
                assert len(slice["source"]) == len(slice["weight"])

        def test_delta_lenght(self):
            for s in self.slices.keys():
                d = self.delta_graphs[s]
                a = self.graphs[s]
                assert len(d["source"]) == len(d["target"])
                assert len(d["source"]) == len(d["weight"])
                ds = d["source"]
                ass = a["source"]
                print("slice ", s)
                print(f"delta len source {len(ds)}")
                print(f"original len source {len(ass)}\n")
        """
