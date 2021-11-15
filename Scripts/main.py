import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from parse_slices import *
from extract_from_slice import *
from Clustering.louvain import *
from Clustering.leiden import *
from Clustering.partition_worker import *
from Clustering.plot_cluster_graphs import *
from Clustering.plot_cluster_stats import *

#path = "./experiment6/experiment_6/"
#my_class = Slices(path)


path = "./experiment6/parsed_dictionaries/"
my_class = ExtractSlices(path)
#my_class.extract()


#path = "./experiment6/parsed_dictionaries/"
#my_class = Leiden(path,"nx")
#my_class = Louvain(path,"nx")
#my_class = Graphs(path,"nx")
#my_class = PartitionWorker(path,"louvain")
#my_class = PlotClusterGraphs(path,"leiden","20")

#path = "./experiment6/statistics/"
#my_class = PlotClusterStats(path,"louvain")
