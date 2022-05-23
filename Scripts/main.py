import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


#from Clustering.PlotScripts.plot_cluster_graphs import *
#from Clustering.cluster_tracker import *
#from Utils.plot_graph_stats import *

#---------------------------SWITCH LABELS IN GRAPH--------------------------------
"""
from Utils.restore_graph_node_id import *
fix_ids_exps = [["delta",7]]
#fix_ids_exps = ["accumulative", 6], ["delta",8], ["delta",9]] 
for exp in fix_ids_exps:
    fix_graph_class = Labels2GraphNodeId(exp[0],exp[1])
"""
#---------------------------------------------------------------------------------



#----------------------FIX LABELPROP CLUSTER STRUCTURE--------------------------------
"""
from Utils.sync_cluster_structure import *
#p = "./experiment12/experiment_12/k_800/"

sync_paths = ["./experiment7/"]#["./experiment8/", "./experiment9/"]
for p in sync_paths:
    testt = SyncCluster(p)
"""
#-------------------------------------------------------------------------------------


#--------------------------------PARSE SLICES-------------------------------------

"""
from Utils.parse_slices import *
outer_paths = ["./experiment7/experiment_7/"] #["./experiment6/experiment_6/","./experiment8/experiment_8/","./experiment9/experiment_9/"] 

for outer in outer_paths:
    my_class = Slices(outer) 
"""

#----------------------------------------------------------------------------------





#------------------------------LEIDEN & LOUVAIN------------------------------------
"""
from Clustering.louvain import *
from Clustering.leiden import *

#inner_paths = ["./experiment6/","./experiment8/","./experiment9/"]
inner_paths = ["./experiment7/"]
for inner in inner_paths:
    #my_class = Leiden(inner,"nx", attributes_bool = False)
    my_class = Louvain(inner,"nx", attributes_bool = False)
"""
#----------------------------------------------------------------------------------





#--------------------------------PARTITION WORKER----------------------------------

"""
from Clustering.partition_worker import *

inner_paths = ["./experiment7/"]#["./experiment800/", "./experiment600/","./experiment6/","./experiment8/","./experiment9/"]
methods = ["leiden", "louvain", "lprop"]

for inner in inner_paths:
    print("new exp")
    for method in methods:
        print("New method\n")
        my_class = PartitionWorker(inner,method) 

#my_class.extract_combined_total_size_dists()
"""
#----------------------------------------------------------------------------------





#--------------------------------PLOT CLUSTER STATS--------------------------------

"""
from Clustering.PlotScripts.plot_cluster_stats import *

inner_paths = ["./experiment7/","./experiment800/","./experiment600/","./experiment6/","./experiment8/","./experiment9/"]
methods = ["leiden", "louvain", "lprop"]

for inner in inner_paths:
    for method in methods:
        print("new method\n")
        my_class = PlotClusterStats(inner,method)


for inner in inner_paths:
    my_class = PlotClusterStats(inner,"lprop")
    my_class.plot_combined_cluster_size_dist()

"""
#----------------------------------------------------------------------------------





#--------------------------------CLUSTER TRACKER----------------------------------

"""
from Clustering.cluster_tracker import *

inner_paths = ["./experiment7/"]#,"./experiment800/","./experiment600/","./experiment8/","./experiment9/"]
methods = ["leiden", "louvain", "lprop"]

for inner in inner_paths:
    print(inner)
    for method in methods:
        print(method, "\n")
        my_class = ClusterTracker(inner,method)
"""
#----------------------------------------------------------------------------------




#--------------------------------MASS VELOCITY-------------------------------------



"""
from Clustering.mass_velocity import *
#min_cluster_sizes = [1000,800,600,400,300,200,100,50,10]#10,50,100,200,300,400,600,800,1000]
inner_paths = ["./experiment7/"]#["./experiment6/","./experiment800/","./experiment600/"]
methods = ["leiden","louvain", "lprop"]

mi = 1
for inner in inner_paths:
    print(inner)
    for me in methods:
        print(f"Method = {me}\n")
        my_class = MassVelocity(inner,me,mi)
"""

#------------------------------------------------------------------------------------







#--------------------------------LARGEST CLUSTER-------------------------------------

"""
from Clustering.largest_clusters import *

inner_paths = ["./experiment7/"]#,"./experiment9/"]
methods = ["leiden", "louvain", "lprop"]

for inner in inner_paths:
    for method in methods:
        my_class = LargestClusters(inner,method)

"""
#-------------------------------------------------------------------------------------







#---------------------------------NODE ACTIVITY & CENTRALITY--------------------------


"""
from NodeActivity.track_node_activity import *
#from NodeActivity.centrality import *
#from NodeActivity.extract_from_centrality import *

inner_paths = ["./experiment6/"]#["./experiment7/","./experiment8/", "./experiment9/"]

for inner in inner_paths:
    activity_class = NodeActivity(inner)
    #activity_class.make_graphs()
    #activity_class.make_NAC_dict()
    #activity_class.sort_NAC_dict()
    activity_class.plot_NAC_distribution(make_dist_dict= False)#True)
    #activity_class.mapping_dict()
    #activity_class.plot_NAC()
    #activity_class.compare_NAC_2_contacts()


#for inner in inner_paths:
   #my_class = Centrality(inner) 
   #my_class = ExtractCentrality(inner)
"""

#-------------------------------------------------------------------------------------


from Clustering.compare_methods import *

inner_paths = ["./experiment7/","./experiment800/","./experiment600/","./experiment6/","./experiment8/","./experiment9/"]

for path in inner_paths:
    my_class = CompareMethods(path)
    #my_class.size_largest_clusters()
    my_class.plot_size_largest_clusters()
