#The K experiments are not exported in correct order 

import numpy as np
import os

class ReOrderKexperiment:
    def __init__(self, experiment_number):
        self.exp_num  = experiment_number

        path2experiment = "./experiment" + str(self.exp_num) + "/experiment_" + str(self.exp_num) + "/"

        k = "800"

        self.path2k = path2experiment + "k_" + k + "/k" + k + "/"
        
        """
        S, SR = self.get_slice_nums(1)
        #must first add old to their names so i dont get into trouble when hitting 1/2 finish
        
        for i in range(len(S)):
            print(f"Slice {S[i]} is becoming Slice {S[i]} OLD")

            old_name  = self.path2k + "slice_" + str(S[i])
            new_name = self.path2k + "slice_" + str(S[i]) + "_old"
            os.rename(old_name,new_name)
        
        
        S, SR = self.get_slice_nums(2)
        for i in range(len(S)):
            print(f"Slice {S[i]} OLD is becoming Slice {SR[i]}")

            old_name = self.path2k + "slice_" + str(S[i]) + "_old"
            new_name = self.path2k + "slice_" + str(SR[i])
            os.rename(old_name,new_name)
        
        
        S, SR = self.get_slice_nums(1)
        for i in range(len(S)):
            right_num = S[i]
            new_comp = "components_" + str(right_num) + ".csv"
            new_graph = "graph_" + str(right_num) + ".mat"
            new_my_graph = "graph_" + str(right_num) + ".csv"
            new_labels = "labels_" + str(right_num) + ".csv"
            new_metrics = "metrics_" + str(right_num) + ".csv"

            path2slice = self.path2k + "slice_" + str(right_num) + "/"
            wrong_num = self.get_inside_nums(path2slice)
            
            old_comp = "components_" + str(wrong_num) + ".csv"
            old_graph = "graph_" + str(wrong_num) + ".mat"
            old_labels = "labels_" + str(wrong_num) + ".csv"
            old_metrics = "metrics_" + str(wrong_num) + ".csv"
            old_my_graph = "graph_" + str(wrong_num) + ".csv"

            os.rename(path2slice + old_comp, path2slice + new_comp)
            os.rename(path2slice + old_graph, path2slice + new_graph)
            os.rename(path2slice + old_labels, path2slice + new_labels)
            os.rename(path2slice + old_metrics, path2slice + new_metrics)
            os.rename(path2slice + old_my_graph, path2slice + new_my_graph)
        """
        
        


    def get_slice_nums(self, name_num):

        slices_files = os.listdir(self.path2k)
        for s in range(len(slices_files)):
            slices_files[s] = int(slices_files[s].split("_")[-name_num])

        slices_files = sorted(slices_files)
        slices_files_reversed = slices_files[::-1]
        
        return slices_files, slices_files_reversed

    def get_inside_nums(self, path_to_slice):

        files = sorted(os.listdir(path_to_slice))
        num = files[-1].split("_")[-1]
        num = int(num.strip(".csv"))

        return num



