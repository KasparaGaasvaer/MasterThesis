import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from parse_slices import *
from extract_from_slice import *
exp_num = 40

#path = "./Scripts/slice_"+str(exp_num)+"/"
#path = "./Scripts/"
path = "./experiment6/experiment_6/"

my_class = Slices(path)
#print(my_class.G)
print(my_class.slices)
