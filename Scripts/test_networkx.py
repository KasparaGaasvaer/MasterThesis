import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
G = nx.Graph()
G.add_node(1)
G.add_nodes_from([2, 3])
G.add_nodes_from([ (4,{"color":"red"}), (5,{"color":"green"}) ])
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_edges_from([(1, 2), (1, 3)])

G.clear()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

print(G.number_of_nodes())
print(G.number_of_edges())

print(list(G.nodes))

G.clear()

G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()


G = nx.Graph()
G.add_node("Kaspara")
G.add_nodes_from(["Maria", "Marte"])
G.add_node("René")
G.add_edge(1,2)
G.add_edge(1,4)
G.add_edge(1,3)

nx.draw(G, with_labels = True)
plt.show()


people = ['Kaspara', 'Marte', 'Maria', 'René']
num_pop = len(people)
subjects = ["Mat4110", "Ast3000"]
num_subj = len(subjects)
G = nx.Graph()
G.add_nodes_from(people)

for i in range(num_pop):
    for j in range(num_subj):
        fromm = people[i]
        too = subjects[j]
        if fromm != "Marte" and too == "Mat4110":
            G.add_edge(fromm,too, color="m")
        if fromm == "Marte" and too == "Ast3000":
            G.add_edge(fromm,too, color = "m")

for i in range(num_pop):
    for j in range(i+1,num_pop):
            fromm = people[i]
            too = people[j]
            G.add_edge(fromm,too, color = "c")

edges = G.edges()
nodes = G.nodes()
edge_colors = [G[u][v]['color'] for u,v in edges]
for n in nodes:
    nodes[n]['color'] = 'm' if n in subjects else 'c'

node_colors = [nodes[n]["color"] for n in nodes]

subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, edge_color=edge_colors, node_color = node_colors)
subax2 = plt.subplot(122)
nx.draw(G, pos = nx.circular_layout(G), with_labels=True, edge_color=edge_colors, node_color = node_colors)
plt.show()

G.add_edge('René', 'Kaspara')
G.add_edge('René', 'Marte')
G.remove_edge('Kaspara','Marte')
G.remove_edge('Maria','Marte')
G.add_node('Mat4110')
G.add_weighted_edges_from([('Mat4110','René',2),('Mat4110','Kaspara',2),('Mat4110','Maria',2)])
G.add_edge('Ast3000', 'Marte',weight = 2)
carac = carac.set_index('ID')
carac = carac.reindex(G.nodes())
carac['type'] = pd.Categorical(carac['type'])
carac['type'].cat.codes

print(carac.type)

cmap = plt.set_cmap("jet_r")

node_sizes = [4000 if entry == 'Subj' else 1000 for entry in carac.type]
edge_colors = nx.get_edge_attributes(G,'weight').values()
print(edge_colors)

nx.draw(G, with_labels=True, node_color=carac['type'].cat.codes, cmap=cmap, node_size=node_sizes, edge_color = edge_colors)
plt.show()
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
