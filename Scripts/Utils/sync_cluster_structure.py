import numpy as np
import json, os


class SyncCluster:
    def __init__(self, path):

        self.path = path
        self.path_to_lp_cluster = self.path + "parsed_dictionaries/Clusters/"
        self.path_to_save = self.path + "parsed_dictionaries/partitions_lprop.json"

        self.make_similar()

    def make_similar(self):
        partitions = {}
        num_slices = len(os.listdir(self.path_to_lp_cluster)) + 1
        for p in range(1,num_slices):
            partitions[str(p)] = {}

        for s in range(1, num_slices):
            print("Slice ",s)
            c = str(s)
            slice = partitions[c]
            with open(self.path_to_lp_cluster + "c_" + c + ".json", "r") as infile:
                clusters = json.load(infile)

            for k in clusters.keys():
                users = clusters[k]["uid"]
                slice[k] = users

        
        with open(self.path_to_save, "w") as outfile:
            json.dump(partitions,outfile)

