# Experiment 7

## Delta Slices (Timebased)

Time increment = 1 day ? 

Slice 1: All tweets in universe before 01/02/2020 (or just the day)

Slice_2: All tweets from 02/02/2020

.

.

.

Slice 64: All tweets from 11/05/2020


## Each slice_i folder contains:
- `components_i.csv` : XXX
- `graph_i.csv` : Sparse adjacancy matrix with IDs = twitter user ID [unique and same across slices]
- `graph_i.mat` : Sparse adjacancy matrix with IDs matching labels file [NOT unique across slices]
- `labels_i.csv` : User labels/information from twitter
- `metrics_i.csv` : XXX
