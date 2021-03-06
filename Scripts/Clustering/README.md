# Instructions for Running Scripts

## Requirements

# Louvain (sub-class of Graphs)
This script is intended to be used for cluster detection in the graphs provided by the `Graphs` class. The constructor of the super is automatically called when the `Louvain` constructor is called and so the graphs do not have to be made beforehand. To initialize the class `Louvain` you must provide a *path* to where you can find the files containing the dictionaries (same path as needed when running `Graphs`), the graph type you wish to produce partitions for as well as a boolean value (both the same options as with `Graphs`) [See ReadMe for Graphs here](https://github.com/KasparaGaasvaer/MasterThesis/blob/main/Scripts/README.md). All graph types are converted to NetworkX graphs before partitioning. 

```python
my_class = Louvain(path, graph_type, attributes_bool)
```

The class then calls a method for partitioning the graph after the Louvain algoritm provided by [NetworkX](https://python-louvain.readthedocs.io/en/latest/api.html). These partitions are stored in a dictionary "nx_partitions_louvain.json".


# Leiden (sub-class of Graphs)
This script is intended to be used for cluster detection in the graphs provided by the `Graphs` class. The constructor of the super is automatically called when the `Leiden` constructor is called and so the graphs do not have to be made beforehand. To initialize the class `Leiden` you must provide a *path* to where you can find the files containing the dictionaries (same path as needed when running `Graphs`), the graph type you wish to produce partitions for as well as a boolean value (both the same options as with `Graphs`) [See ReadMe for Graphs here](https://github.com/KasparaGaasvaer/MasterThesis/blob/main/Scripts/README.md). All graph types are converted to iGraph graphs before partitioning. 

```python
my_class = Leiden(path, graph_type, attributes_bool)
```

The class then calls a method for partitioning the graph after the Leiden algoritm provided by [Vincent Traag](https://github.com/vtraag/leidenalg). These partitions are stored in a dictionary "nx_partitions_leiden.json".


# Partition Worker
This script is intended to be used for extracting statistics about the partitions of graphs provided by the `Louvain` and `Leiden` classes or any partitions from other community detection algorithms stored as dictionaries called "partitions_[method].json" where the keys are partition numbers and the values are lists of the vertex ids belonging to the corresponding partitions (NB! This relies on the `Graph` class being extended to more community detection algorithms, default is `leiden, louvain, lprop`). To initialize the class `PartitionWorker` you must provide a *path* to where you can find the files containing the dictionaries containing the partitions as well as the *method* for community detection.

```python
my_class = PartitionWorker(path, method)
```

From here you can choose from a selection of methods (MORE COMING):

1. `identify_largest_cluster`
    * Identifies the largest cluster in each slice and stores information about the cluster : Slice num / Partition num / Num nodes / (Num nodes/Total num nodes) / (Num nodes/(Total num nodes - Num nodes).
    * Outfile name "largest_partitions_[method].txt"


<!-- # Plot Cluster (sub-class of Graphs)
This script is intended to be used for vizualisation of the partitions and subsequently induced new graphs from partitions provided by the `Louvain` and `Leiden` classes.  To initialize the class `PlotCluster` you must provide a *path* to where you can find the files containing the dictionaries containing the partitions as well as the graph type you wish to examine the partitions for (same options as with `Graphs`). You must also specify how many of the slices you wish to visualize, *selection* can be either "10" for the first 10 slices or "all".



```python
my_class = PartitionWorker(path, graph_type, selection)
```

The constructor then calls a method for plotting the original graphs of the selected slices where nodes have been colored after which partition they belong to. It will also produce plots of the induced graphs from the partitions where each node is a cluster from the original graph.  -->
