import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from Utils.parse_slices import *
from Utils.extract_from_slice import *
from Utils.plot_graph_stats import *

from Clustering.louvain import *
from Clustering.leiden import *
from Clustering.partition_worker import *
from Clustering.plot_cluster_graphs import *
from Clustering.plot_cluster_stats import *

#path = "./experiment7/experiment_7/"
#path = "./experiment6/experiment_6/"
#my_class = Slices(path)


#path = "./experiment6/"
#path = "./experiment7/"
#my_class = ExtractSlices(path)
#my_class.extract()  for now called by constructor

path = "./experiment7/"
#path = "./experiment6/parsed_dictionaries/"
#my_class = Leiden(path,"nx", attributes_bool = False)
#my_class = Louvain(path,"nx", attributes_bool = False)
#my_class = Graphs(path,"nx", attributes_bool = True)
#my_class = PartitionWorker(path,"louvain")
#my_class = PlotClusterGraphs(path,"louvain","all", attributes_bool=False)
#my_class = PlotClusterStats(path,"louvain")
my_class = PlotGraph(path, ["num_edges"])


#59-76 large num edges? Critical area?
