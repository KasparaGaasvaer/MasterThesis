import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

from parse_slices import *

class ExtractSlices():
    def __init__(self, slice_file, common_attributes_file):

        with open(slice_file, 'r') as fp:
            self.slices = json.load(fp)

        with open(common_attributes_file, 'r') as fp:
            self.common_attributes = json.load(fp)

        
