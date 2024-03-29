import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from Utils.parse_slices import *
from Utils.extract_from_slice import *
from old_scripts.plot_graph_stats import *
from Utils.restore_graph_node_id import *
from misc_rejected_scripts.re_ordering_k_experiments import *

from Clustering.louvain import *
from Clustering.leiden import *
from Clustering.partition_worker import *
from Clustering.PlotScripts.plot_cluster_graphs import *
from Clustering.PlotScripts.plot_cluster_stats import *
from Clustering.cluster_tracker import *
from Clustering.cluster_tracker_SharedDict import *
from Clustering.mass_velocity import *
#from Clustering.centrality import *

from NodeActivity.track_node_activity import *
from NodeActivity.centrality import *

#exp6 = ["accumulative", 6]
#fix_graph_class = Labels2GraphNodeId(exp6[0],exp6[1])
#exp7 = ["delta",7]
#fix_graph_class = Labels2GraphNodeId(exp7[0],exp7[1])
#exp8 = ["delta",8]
#fix_graph_class = Labels2GraphNodeId(exp8[0],exp8[1])
#exp9 = ["delta",9]
#fix_graph_class = Labels2GraphNodeId(exp9[0],exp9[1])
#exp12 = ["k_value", 12]
#fix_graph_class = Labels2GraphNodeId(exp12[0],exp12[1])

#fix_k_order = ReOrderKexperiment(12) #DO NOT!! run this unless 10000% certain that it has not been run before!!


#path = "./experiment7/experiment_7/"
#path = "./experiment8/experiment_8/"
#path = "./experiment9/experiment_9/"
#path = "./experiment6/experiment_6/"
#path = "./experiment100/experiment_100/"
#path = "./experiment12/experiment_12/"
#my_class = Slices(path)
#my_class = Centrality(path, 600)

paths = ["./experiment7/", "./experiment6/", "./experiment8/", "./experiment9/"]

for path in paths:
    my_class = Leiden(path,"nx", attributes_bool = False)


#path = "./experiment6/"
#path = "./experiment7/"
#path = "./experiment8/"
#path = "./experiment9/"
#paths = [path8,path9]
#for path in paths:
#path = "./experiment100/"
#path = "./experiment12/experiment_12/"
##my_class = ExtractSlices(path)
##my_class.extract()  #for now called by constructor, aka not necessary

#my_class = NodeActivity(path) 
#my_class = Centrality(path) 

    #my_class = Leiden(path,"nx", attributes_bool = True)    #6, 7, 800,600
    #my_class = Louvain(path,"nx", attributes_bool = True) #6, 7, 800,600
##my_class = Graphs(path,"nx", attributes_bool = True)
    #my_class = PartitionWorker(path,"leiden")  #6LeidenLouvain, 7lovainleiden, 800leidenlouvain, 600leidenlouvain
    #my_class = PartitionWorker(path,"louvain")
#my_class = PlotClusterGraphs(path,"leiden","all", attributes_bool=True)
    #my_class = PlotClusterStats(path,"louvain") # 7louvainleiden, 6leidenlouvain, 800louvainleiden, 600louvainleiden
    #my_class = PlotClusterStats(path,"leiden")
##my_class = PlotGraph(path, ["num_edges"])
#my_class = ClusterTracker(path)  #done 800 NL = 10, done for 600 NL=10 
#my_class = ClusterTracker_SD(path,"louvain") # 6leidenlouvain, 7louvainleiden, 600leidenlouvain , 800leidenlouvain
    #my_class = ClusterTracker_SD(path,"louvain") # 6leidenlouvain, 7louvainleiden, 600leidenlouvain , 800leidenlouvain

"""
min_cluster_sizes = [10,50,100,200,300,400,600,800,1000]
methods = ["leiden","louvain"]
#methods = ["leiden", "louvain", "java"]
for mi in min_cluster_sizes:
    print(f"Min size = {mi}")
    for me in methods:
        print(f"Method = {me}")
        my_class = MassVelocity(path,me,mi) #6,7
"""

#from Clustering.largest_clusters import * #Fjerner denne når den ikke brukes, blir noe tull med matplotlib pga importene i den
#methods = ["leiden","louvain"]
#for method in methods:
    #my_class = LargestClusters(path,method) #6,7,800,600 all
# TRACKING LARGEST BRANCH CODE NOT WORKING FOR EXP7 LOUVAIN, THE LARGEST CLUSTER IN SLICE 3 HAS 0 INTERSECT WITH ALL SLICES IN SLICE 4