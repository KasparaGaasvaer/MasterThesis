import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from Utils.parse_slices import *
from Utils.extract_from_slice import *
from Utils.plot_graph_stats import *
from Utils.restore_graph_node_id import *
from Utils.re_ordering_k_experiments import *

from Clustering.louvain import *
from Clustering.leiden import *
from Clustering.partition_worker import *
from Clustering.PlotScripts.plot_cluster_graphs import *
from Clustering.PlotScripts.plot_cluster_stats import *
from Clustering.cluster_tracker import *
from Clustering.cluster_tracker_SharedDict import *
from Clustering.mass_velocity import *
#from Clustering.largest_clusters import * #Fjerner denne når den ikke brukes, blir noe tull med matplotlib pga importene i den

#exp6 = ["accumulative", 6]
#fix_graph_class = Labels2GraphNodeId(exp6[0],exp6[1])
#exp7 = ["accumulative",7]
#fix_graph_class = Labels2GraphNodeId(exp7[0],exp7[1])
#exp12 = ["k_value", 12]
#fix_graph_class = Labels2GraphNodeId(exp12[0],exp12[1])

#fix_k_order = ReOrderKexperiment(12) DO NOT!! run this unless 10000% certain that it has not been run before!!


#path = "./experiment7/experiment_7/"
#path = "./experiment6/experiment_6/"
#path = "./experiment100/experiment_100/"
#path = "./experiment12/experiment_12/"
#my_class = Slices(path)

#path = "./experiment6/"
#path = "./experiment7/"
#path = "./experiment100/"
path = "./experiment12/experiment_12/"
##my_class = ExtractSlices(path)
##my_class.extract()  #for now called by constructor, aka not necessary

#my_class = Leiden(path,"nx", attributes_bool = True)    #these take a lot longer with attributes? #done for k800/600
#my_class = Louvain(path,"nx", attributes_bool = True) #done for k800/600
##my_class = Graphs(path,"nx", attributes_bool = True)
#my_class = PartitionWorker(path,"louvain")  #done for 800LouvainLeiden 600Louvain, 6leiden,louvain
#my_class = PlotClusterGraphs(path,"leiden","all", attributes_bool=True)
#my_class = PlotClusterStats(path,"louvain") #done for 800LeidenLouvain 600LouvainLeiden, 6leidenlouvain
##my_class = PlotGraph(path, ["num_edges"])
my_class = ClusterTracker(path)  #done 800 NL = 10, done for 600 NL=10 
#my_class = ClusterTracker_SD(path,"louvain") #done 800leidenlouvain, 600leidenlouvain, 6louvainleiden
#my_class = MassVelocity(path,"java",50) #done for 800java 100200300400600 #MISSING PLOTS FOR ALL
#my_class = LargestClusters(path,"leiden#") #Leiden800/600/6/7, Louvain800/600/6/7, Java800/600
#59-76 large num edges? Critical area?


# TRACKING LARGEST BRANCH CODE NOT WORKING FOR EXP7 LOUVAIN, THE LARGEST CLUSTER IN SLICE 3 HAS 0 INTERSECT WITH ALL SLICES IN SLICE 4