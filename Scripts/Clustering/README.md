# Instructions for Running Scripts

## Requirements

# Louvain (sub-class of Graphs)
This script is intended to be used for cluster detection in the graphs provided by the `Graphs` class. The constructor of the super is automatically called when the `Louvain` constructor is called and so the graphs do not have to be made beforehand. To initialize the class `Louvain` you must provide a *path* to where you can find the files containing the dictionaries (same path as needed when running `Graphs`) as well as the graph type you wish to produce (same options as with `Graphs`) [See ReadMe for Graphs here](https://github.com/KasparaGaasvaer/MasterThesis/blob/main/Scripts/README.md).

```python
my_class = Louvain(path, graph_type)
```

# Leiden (sub-class of Graphs)

