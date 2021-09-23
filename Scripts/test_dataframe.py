
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import copy


df = pd.DataFrame({'col1': [0, 1], 'col2': [1, 0], 'col3':[2,2]})
df = df.to_dict(header = None)
print(df)
