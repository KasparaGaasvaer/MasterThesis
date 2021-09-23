import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from parse_slices import *
from extract_from_slice import *
exp_num = 40


#path = "./experiment6/experiment_6/"

#my_class = Slices(path)



path = "./experiment6/parsed_dictionaries/"
my_class = ExtractSlices("all_slices.json","attributes_to_all_slices.json", path)

"""
x = [1,2,3,4]
l = [2,8,5,6]
names = ["one", "two", "three","four"]
zeros = [0 for i in range(len(l))]
plt.vlines(x = x,ymin = zeros,ymax = l,lw=40)
for i in range(len(l)):
    plt.text(x[i]-0.1, l[i], names[i])
plt.ylim(ymin=0)
plt.ylabel("$\\frac{\mathrm{Number\,of\,tweets\,<\,2020}}{\mathrm{Total\,number\,of\,tweets\,in\,slice}}$", fontsize = 12)
plt.show()
"""
