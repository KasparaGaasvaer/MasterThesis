import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

exp_num = 40

path = "./Scripts/slice_"+str(exp_num)+"/"

def node_attributes():
    filename = path + "labels_" + str(exp_num) + ".csv"
    attributes = pd.read_csv(filename,header = 0, quotechar='"', error_bad_lines=False, warn_bad_lines=True)
    attributes = attributes.fillna(value=False)
    attributes = attributes.to_dict(orient='list')




"""
types = ["source", "target", "weight"]
df = pd.read_csv("graph_1.mat", delim_whitespace = True,names = types)[:100]
G=nx.from_pandas_edgelist(df, types[0], types[1], edge_attr = types[2])
nodes = G.nodes()
edges = G.edges()
for n in nodes:
    nodes[n]['color'] = 'm' if (n==0 or n==1) else 'c'
node_colors = [nodes[n]["color"] for n in nodes]
print(G)
#weights = [G[u][v]['weight'] for u,v in edges]
#node_sizes = [4000 if (n==1 or n==0) else 100 for n in nodes]
nx.draw(G, with_labels=True, font_weight='bold', node_color = node_colors)#, width = weights, node_size = node_sizes)
plt.show()
"""

node_attributes()
