import os
import sys
import json


# ==============================Access and Open Dictionaries==============================
#
# Class for opening dictionaries
#

class OpenDict:
    def __init__(self,path):
        """Method for constructing dictionary of filenames from json files

        Args:
            path (string): path to experiment data
        """

        self.path = path + "parsed_dictionaries/"
        if not os.path.exists(self.path):
            k_value = input("Is this a k-value experiment? Please input k-value\nIf this is NOT a k-value experiment please input no\n")
            if int(k_value):
                self.path = path + "k_" + str(k_value) + "/parsed_dictionaries/"

        self.dictionary_filenames = {
            "slices" : "all_slices.json",
            "attributes" : "attributes_to_all_slices.json",
            "graphs" : "graph_all_slices.json",
            "part_louvain" : "partitions_louvain.json",
            "part_leiden" : "partitions_leiden.json"
        }


    def open_dicts(self, dicts):
        """Method for opening dictionaries

        Args:
            dicts (list): list of strings indicating which dictionaries to open
        """
        d_out = []
        for key in dicts:
            with open(self.path + self.dictionary_filenames[key],"r") as d:
                d_out.append(json.load(d))

        if len(d_out) == 1:
            return d_out[0]
        else:
            return d_out
