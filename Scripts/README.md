# Instructions for Running Scripts

### Requirements
#### Slice-folders
`Slice_i` folder must contain attributes to nodes stored in `labels_i.csv` files and edges (from - to) in `graph_i.mat` files.



## Parse Slices
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
  -`attributes_to_slice_set` -> `attributes_to_all_slices.json`

##### Node attributes:
- blablbalba

##### Timeline:
- blablabla


> Block quote


*italics*
**bold**
