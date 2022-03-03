import numpy as np


def easy_plot(expnum, method):
    if expnum == 12:
        k = input("input k-value:\n")
        filename = "../../experiment12/experiment_12/k_"+str(k)+"/statistics/Cluster_tracker/"+method.title()+"/"
    else:
        filename = "../../experiment"+str(expnum)+"/statistics/Cluster_tracker/"+method.title()+"/"

    filename += "tracking_all_branches_largest_cluster_in_each_slice.txt"
    
    #with open(filename)


easy_plot(12,"java")
easy_plot(6,"leiden")

