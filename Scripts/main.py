import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from Utils.parse_slices import *
from Utils.extract_from_slice import *
from Utils.plot_graph_stats import *
from Utils.restore_graph_node_id import *

from Clustering.louvain import *
from Clustering.leiden import *
from Clustering.partition_worker import *
from Clustering.PlotScripts.plot_cluster_graphs import *
from Clustering.PlotScripts.plot_cluster_stats import *
from Clustering.cluster_tracker import *
from Clustering.cluster_tracker_SharedDict import *
from Clustering.mass_velocity import *

#exp6 = ["accumulative", 6]
#fix_graph_class = Labels2GraphNodeId(exp6[0],exp6[1])
#exp7 = ["accumulative",7]
#fix_graph_class = Labels2GraphNodeId(exp7[0],exp7[1])
exp12 = ["k_value", 12]
fix_graph_class = Labels2GraphNodeId(exp12[0],exp12[1])





#path = "./experiment7/experiment_7/"
#path = "./experiment6/experiment_6/"
#path = "./experiment100/experiment_100/"
#path = "./experiment12/experiment_12/"
#my_class = Slices(path)

#path = "./experiment6/"
#path = "./experiment7/"
#path = "./experiment100/"
#path = "./experiment12/experiment_12/"
#my_class = ExtractSlices(path)
#my_class.extract()  for now called by constructor, aka not necessary

#my_class = Leiden(path,"nx", attributes_bool = True)    #these take a lot longer with attributes?
#my_class = Louvain(path,"nx", attributes_bool = True)
#my_class = Graphs(path,"nx", attributes_bool = True)
#my_class = PartitionWorker(path,"leiden")
#my_class = PlotClusterGraphs(path,"leiden","all", attributes_bool=True)
#my_class = PlotClusterStats(path,"leiden")
#my_class = PlotGraph(path, ["num_edges"])
#my_class = ClusterTracker(path)
#my_class = ClusterTracker_SD(path,"leiden")
#my_class = MassVelocity(path,"leiden")

#59-76 large num edges? Critical area?
