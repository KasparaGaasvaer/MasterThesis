import igraph as ig
import json
import matplotlib.pyplot as plt

path = "./experiment6/parsed_dictionaries/"

with open(path + "all_slices.json", 'r') as fp:
    slices = json.load(fp)

with open(path + "graph_all_slices.json", 'r') as fp:
    graphs = json.load(fp)

slice_num = 1
node_attributes = slices[str(slice_num)]['node_attributes']

graph = graphs[str(slice_num)]
sources = graph['source']
targets = graph['target']
weights = graph['weight']
list_of_edges = []
for i in range(len(sources)):
    list_of_edges.append((sources[i],targets[i]))

G = ig.Graph(edges = list_of_edges)
for n in G.vs:
    atts = node_attributes[str(n.index)]
    for att in atts:
        n[str(att)] = atts[str(att)]

layout = G.layout(layout='auto')
ig.plot(G, layout = layout)
plt.show()


#G = ig.Graph()
#G.add_vertices(3)
#G.add_edges([(0,1),(1,2)])
#G.add_edges([(2, 0)])
#G.add_vertices(3)
#G.add_edges([(2, 3), (3, 4), (4, 5), (5, 3)])

#print(G)
