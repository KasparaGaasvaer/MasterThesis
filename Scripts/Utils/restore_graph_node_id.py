import numpy as np
import pandas as pd
import os

class Labels2GraphNodeId:
    def __init__(self, experiment_type, experiment_number):

        self.exp_num = experiment_number

        if experiment_type == "k_value":
            self.labels_2_graph_node_id_k_value()
        
        if experiment_type == "accumulative" or experiment_type == "delta":
            self.labels_2_graph_node_id()

    
    def labels_2_graph_node_id(self):
        path2experiment = "./experiment" + str(self.exp_num) + "/experiment_" + str(self.exp_num) + "/"
        slices_files = os.listdir(path2experiment)
        for i in range(len(slices_files)):
            slices_files[i] = int(slices_files[i].split("_")[-1])

        slices_files = sorted(slices_files)

        with open("./experiment" + str(self.exp_num) + "/bad_ids.txt", "w") as ouf:
            ouf.write("SliceNum           Bad Ids\n")

        for i in slices_files:
            print("Slice ", i)
            badids = []
            path2graph = path2experiment + "slice_" + str(i) + "/graph_" + str(i) + ".mat" 
            path2labels = path2experiment + "slice_" + str(i) + "/labels_" + str(i) + ".csv" 
            path2save = path2experiment + "slice_" + str(i) +"/graph_" + str(i) + ".csv"

            types = ["source", "target", "weight"]
            graph_df = pd.read_csv(path2graph,names = types, delim_whitespace = True)
            graph_mat = graph_df.to_numpy()
            N_contacts = len(graph_mat[:,0])
            
            #Reading only the two first colums from labels files
            labels_df = pd.read_csv(path2labels,header = 0, usecols=[0,1])#, warn_bad_lines=True)
            labels_mat = labels_df.to_numpy()

            id_dict = {}
            graph_ids = labels_mat[:,0]
            labels_ids = labels_mat[:,1]

            for g,l in zip(graph_ids,labels_ids):
                id_dict[g] = l

            for z in range(2):
                for q in range(N_contacts):
                    try:
                        graph_mat[q][z] = id_dict[graph_mat[q][z]]
                    except KeyError:
                        badids.append(graph_mat[q][z])
                        continue
                        
            np.savetxt(path2save, graph_mat, delimiter=',',fmt='%i')
            with open("./experiment" + str(self.exp_num) + "/bad_ids.txt", "a") as ouf:
                ouf.write(f"{i}                    {badids}\n")
            


    def labels_2_graph_node_id_k_value(self):
        path2experiment = "./experiment" + str(self.exp_num) + "/experiment_" + str(self.exp_num) + "/"
        k_values = ["600"]# ["400","600","800"]
        for k in k_values:
            path2k = path2experiment + "k_" + k + "/k" + k + "/"
            slices_files = os.listdir(path2k)
            for s in range(len(slices_files)):
                slices_files[s] = int(slices_files[s].split("_")[-1])

            slices_files = sorted(slices_files)

            with open(path2experiment + "k_" + k + "/bad_ids.txt", "w") as ouf:
                ouf.write("SliceNum           Bad Ids\n")

            for i in slices_files:
                print("Slice ", i)
                badids = []
                path2graph = path2k + "slice_" + str(i) + "/graph_" + str(i) + ".mat" 
                path2labels = path2k + "slice_" + str(i) + "/labels_" + str(i) + ".csv" 
                path2save = path2k + "slice_" + str(i) +"/graph_" + str(i) + ".csv"

                types = ["source", "target", "weight"]
                graph_df = pd.read_csv(path2graph,names = types, delim_whitespace = True)
                graph_mat = graph_df.to_numpy()
                N_contacts = len(graph_mat[:,0])
                
                #Reading only the two first colums from labels files
                labels_df = pd.read_csv(path2labels, header = 0, usecols=[0,1])#, warn_bad_lines=True)
                #N_users = len(labels_df)
                #data = [i for i in range(N_users)]
                #labels_df.insert(0,'G-id',data)
                labels_mat = labels_df.to_numpy()

                id_dict = {}
                graph_ids = labels_mat[:,0]
                labels_ids = labels_mat[:,1]

                for g,l in zip(graph_ids,labels_ids):
                    id_dict[g] = l

                for z in range(2):
                    for q in range(N_contacts):
                        try:
                            graph_mat[q][z] = id_dict[graph_mat[q][z]]
                        except KeyError:
                            badids.append(graph_mat[q][z])
                            continue


                np.savetxt(path2save, graph_mat, delimiter=',',fmt='%i')

                with open(path2experiment + "k_" + k + "/bad_ids.txt", "a") as ouf:
                    ouf.write(f"{i}                    {badids}\n")
       
            
    
        
