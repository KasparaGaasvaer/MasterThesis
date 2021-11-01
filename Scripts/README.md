# Instructions for Running Scripts

### Requirements
#### Slice-folders
`Slice_i` folder must contain attributes to nodes stored in `labels_i.csv` files and edges (from - to) in `graph_i.mat` files.



# Parse Slices
This script is intended to be used for parsing .csv and .mat files containing information about time slices to python dictionaries for easier use and manipulation. To initialize the class `Slices` you must provide a *path* to where you can find the folders containing the time slices.


```python
my_class = Slices(path)
```

From this point (so far) the script is on auto-pilot. The initializer will call a member function `ReadSlice` which will for all slices in the directory specified by *path* do the following

1. Add node attributes in slice as nested dictionary to dictionary `slices` ( key = [slice number][time of interest] )
2. Add all edges in slice to dictionary `graphs` ( key = [slice number] )
3. Find timeline of slice (first and last status posted) and add that to the `slices` dictionary ( key = [slice number][attribute of interest])
4. Find number of nodes in slice and add that to the `slices` dictionary
( key = [slice number]["num_nodes"])

See furter down for specification of keys. After looping through all the slices the `ReadSlice` function will

1. Find the timeline of the set of slices (first and last status in entire set) and add that to dictionary `attributes_to_slice_set` ( key = [time of interest])
2. Save the dictionaries
  - `slices` -> `all_slices.json`
  - `graphs` ->  `graph_all_slices.json`  
  - `attributes_to_slice_set` -> `attributes_to_all_slices.json`


## Keys 
Time of interest:
- 'start_date' : Datetime of first posted status in slice
- 'end_date': Datetime of last posted status in slice
- 'start_date_node_index' : Corresponding node index to 'start date'
- 'end_date_node_index' : Corresponding node index to 'end date'

Attribute of interest:
- 'index' : node index 
- 'id' : Twitter user id
- 'date' : datetime of posting status
- 'verified' : is the user account verified by Twitter (true/false)
- 'protected' : is the user account protected (true/false)
- 'deleted' : has the status been deleted since the first loading of data (true/false)
- 'friends_count' : how many other users is the user following on Twitter
- 'statuses_count' : how many statuses has the user posted in total
- 'followers_count' : how many followers does the user have
- 'favourites_count' : how many times has the user marked a status as a favourite
- 'location' : geotag of posting
- 'screen_name' : users screen name on Twitter

# Extract from slice
This script is intended to be used for reading all the .json files from the `Slices` class and extracting information/metrics from the dictionaries contained in the files. To initialize the class `ExtractSlices` you must provide a path to where you can find the files containing the dictionaries.

```python
my_class = ExtractSlices(path)
```

The first thing that will happen is that the script will try to open the dictionaries from `Slices` which should be provided. From here on you will have some choices. You have the option to call a function `extract()` which contain calls to multiple sub-methods of the class. Before calling the function, you should go into the class and hash out all of the methods you do not wish to call. The methods are well documented with doc-strings and so we redirect you to the script for further information about the methods.

```python
my_class.extract()
```

# Graphs
This script is intended to be used for reading two of the .json files from the `Slices` class, namely `all_slices.json` and `graph_all_slices.json`, and extracting information to produce graph representations. To initialize the class `Graphs` you must provide a path to where you can find the files containing the dictionaries as well as the graph type you wish to produce. Your choices are

- 'nx' : NetworkX 
- 'ig' : iGraph
- 'skn' : Scikit Networks

```python
my_class = Graphs(path, graph_type)
```

the constructor will then open and load the necessary dictionaries before calling the corresponding method for producing graphs of the type specified. These graph-objects are then stored in a dictionary `self.graphs` and can be accessed after slice number by `self.graphs[slice_num]['graph']`.


> Block quote


*italics*
**bold**
