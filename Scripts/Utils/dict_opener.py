import os
import sys
import json


# ==============================Access and Open Dictionaries==============================
#
# Class for opening dictionaries 
#

class OpenDict:
    def __init__(self,path):
        self.path = path + "parsed_dictionaries/"

        self.dictionary_filenames = {
            "slices" : "all_slices.json",
            "attributes" : "attributes_to_all_slices.json",
            "graphs" : "graph_all_slices.json",
            "part_louvain" : "partitions_louvain.json",
            "part_leiden" : "partitions_leiden.json"
        }

    
    def open_dicts(self, dicts):
        #
        # Open Dictionaries:
        # - Exp : Experiment ID
        # - Dicts : A list of dictionaries to open 
        #
        d_out = []
        for key in dicts:
            with open(self.path + self.dictionary_filenames[key],"r") as d:
                d_out.append(json.load(d))

        if len(d_out) == 1:
            return d_out[0]
        else:
            return d_out