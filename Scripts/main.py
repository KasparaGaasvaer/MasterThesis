import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from parse_slices import *
from extract_from_slice import *
from Clustering.louvain import *
from Clustering.leiden import *
from networkx_partition_worker import *

#path = "./experiment6/experiment_6/"
#my_class = Slices(path)


#path = "./experiment6/parsed_dictionaries/"
#my_class = ExtractSlices(path)


path = "./experiment6/parsed_dictionaries/"
my_class = Louvain(path,"nx")
#my_class = Graphs(path,"skn")
#my_class = NetworkX_Partition_Worker(path)
