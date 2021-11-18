import numpy as np
import os
import pandas as pd
from IPython.display import display


types = ["source", "target", "weight"]
df = pd.read_csv("graph_7.mat", delim_whitespace=True, names=types)
display(df)
