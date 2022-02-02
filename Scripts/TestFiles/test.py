import json
import networkx as nx
import igraph as ig
import leidenalg as la
"""
si  = {"a": {
    "1" : ["100","200","300","400"],
    "2" : ["101","201","301","401"],
    "3" : ["102","202","302","402"]
    }, "b": {
    "1" : ["103","203","303","403"],
    "2" : ["104","204","304","404"],
    "3" : ["105","205","304","405"]
    }
}

with open("../experiment100/parsed_dictionaries/partitions_leiden.json", "r") as inf:
    si =  json.load(inf)

for key in si.keys():
    slice_list = [] #New list for every slice
    shit = 0
    for k in si[key].keys():
        for val in si[key][k]:
            if val in slice_list:
                shit +=1
            else:
                slice_list.append(val)
    print(f"Number of same nodes for slice {key} was {shit}")

"""
"""
file = "../experiment100/parsed_dictionaries/graph_all_slices.json"

with open(file, "r") as inf:
    g = json.load(inf)

for i in range(6,67):
    del g[str(i)]

with open("test_graph.json","w") as ouf:
    json.dump(g, ouf)
"""
"""
file = "test_graph.json"
with open(file, "r") as inf:
    g = json.load(inf)


for i in range(4,6):
    del g[str(i)]


graphs = {}
partition_dict = {}

for slice in g.keys():
            print("Making nx graph for slice: ", slice)
            graph = g[slice]
            sources, targets, weights = graph["source"], graph["target"], graph["weight"]
            list_of_edges = []
            for i in range(len(sources)):
                list_of_edges.append((str(sources[i]), str(targets[i]), {"weight": weights[i]}))

            G = nx.Graph()
            G.add_edges_from(list_of_edges)

            graphs[slice] = {"graph": G}

            print("Making ig graph for slice: ", slice)
            gg = graphs[slice]["graph"]
            G = ig.Graph.from_networkx(gg) # leidenalg only works with igraph, 
            print("Making partitions for slice: ", slice)
            partition = la.find_partition(G, la.ModularityVertexPartition)
            partition_dict[slice] = {}
            for i in range(len(partition)):
                partition_dict[slice][i] = partition[i]

            

            #self.nx_make_partition_dict(G, partition)

        
with open("test_parts.json","w") as ouf:
    json.dump(partition_dict, ouf)
"""

with open("../experiment100/parsed_dictionaries/partitions_leiden.json", "r") as inf:
    si =  json.load(inf)

s1 = si["1"]
s2 = si["2"]

for k in s1.keys():
    v1 = set(s1[k])
    c = 0
    for kk in s2.keys():
        v2 = set(s2[kk])

        inters_n = v1.intersection(v2)
        inters_p = len(inters_n)/len(v1)
        if inters_p > 0.9:
            c+=1
            print(f"cluster {k} in s1 has {inters_p} intersect with cluster {kk} in s2")
            print(len(inters_n)," / ", len(v1))
            
        if c == 2:
            print("broken")