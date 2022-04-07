import numpy as np
import os, json
import pandas as pd



class Centrality:
    def __init__(self, path, type):

        self.methods = ["leiden", "louvain", "lprop"]
        self.path = path

    
        self.num_slices = os.listdir(self.path)
        self.slice_nums = np.linspace(1, len(self.num_slices) + 1, len(self.num_slices) + 1).astype(int)[:-1]

        self.path_to_stats = self.path.rsplit("/",2)[0] + "/statistics/Centrality/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        self.path_to_save_all = self.path_to_stats + "all_each_slice/"
        if not os.path.exists(self.path_to_save_all):
            os.makedirs(self.path_to_save_all)

        self.path_to_save_top = self.path_to_stats + "top/"
        if not os.path.exists(self.path_to_save_top):
            os.makedirs(self.path_to_save_top)

        self.path_to_save_compare = self.path_to_stats + "compare_to_largest/"
        if not os.path.exists(self.path_to_save_compare):
            os.makedirs(self.path_to_save_compare)
     
        #self.calculate_centrality()
        #self.get_top_5_nodes()
        #self.get_top_1_node()
        #self.compare_centrality_and_largest_cluster()
        self.find_id_of_top_5()


    def calculate_centrality(self):

        # num_nodes = len(labels) - 1 # n-1
        # for every time a node is part of a contact add one to centrality score 
        
        for s in self.slice_nums:
            print(s)
            path_to_slice = self.path + "slice_" + str(s) + "/"
            
            labels = path_to_slice + "labels_" + str(s) + ".csv"
            graph = path_to_slice + "graph_" + str(s) + ".csv"

            labels_df = pd.read_csv(labels, header = 0, usecols=[1]) #pick out only node id 
            N_users = len(labels_df)
            labels_vec = labels_df.to_numpy()
            labels_vec = labels_vec[:,0]

            user_dict = {}
            for u in labels_vec:
                user_dict[str(u)] = 0
            #print(user_dict)

            types = ["source", "target", "weight"]
            graph_df = pd.read_csv(graph, names = types)
            graph_mat = graph_df.to_numpy()
            N_contacts = len(graph_mat[:,0])

            for j in range(2):
                for i in range(N_contacts):
                    id = str(graph_mat[i][j])
                    try:
                        user_dict[id] += 1
                    except KeyError:
                        user_dict[id] = 1
            
            for k in user_dict.keys():
                user_dict[k] /= (N_users - 1)
                
            with open(self.path_to_save_all + "s_" + str(s)+ ".json", "w") as ouf:
                json.dump(user_dict,ouf)

    def get_top_5_nodes(self):

        M_ids, M_c_score = [], []

        for s in self.slice_nums:
            print(s)
            ids, c_score = [],[]
            with open(self.path_to_save_all + "s_" + str(s)+ ".json", "r") as inff:
                dictt = json.load(inff)
            
            top_5 = sorted(dictt, key=dictt.get, reverse=True)[:5]
            
            for k in top_5:
                ids.append(k)
                c_score.append(dictt[k])

            M_ids.append(ids)
            M_c_score.append(c_score)

        with open(self.path_to_save_top + "top5_centrality.txt","w") as ouf:
            ouf.write("s:id:C\n")
            for i in range(len(M_ids)):
                ouf.write(f"{i+1}:{M_ids[i]}:{M_c_score[i]}\n")


    def get_top_1_node(self):

        M_ids, M_c_score = [], []

        for s in self.slice_nums:
            print(s)
            id, c_score = 0,0
            with open(self.path_to_save_all + "s_" + str(s)+ ".json", "r") as inff:
                dictt = json.load(inff)
            
            top1 = sorted(dictt, key=dictt.get, reverse=True)[0]
            
            id = top1
            c_score = dictt[top1]

            M_ids.append(id)
            M_c_score.append(c_score)

        with open(self.path_to_save_top + "top1_centrality.txt","w") as ouf:
            ouf.write("s:id:C\n")
            for i in range(len(M_ids)):
                ouf.write(f"{i+1}:{M_ids[i]}:{M_c_score[i]}\n")

    def compare_centrality_and_largest_cluster(self):

        M_info = []
        num_methods = 3
        central_node_ids = []
        path_2_exp = self.path.rsplit("/",2)[0] + "/"
        path_2_partitions = path_2_exp + "parsed_dictionaries/"

        file_centrality = self.path_to_save_top + "top1_centrality.txt"
        with open(file_centrality,"r") as inf:
            inf.readline()
            lines = inf.readlines()
            for line in lines: 
                central_node_ids.append(line.split(":")[1])

        for method in self.methods:
            print("new method")
            largest_cluster_ids = []
            central_node_clusters = []

            file_largest_c = path_2_exp + "statistics/Largest_clusters/" + method.title() + "/stats_LC_Nnodes_Nclusters.txt"
            with open(file_largest_c,"r") as inf:
                inf.readline()
                lines = inf.readlines()
                for line in lines:
                    largest_cluster_ids.append(line.split()[1])

            
            clusters_file = path_2_partitions + "partitions_" + method + ".json"
            with open(clusters_file, "r") as inf:
                clusters = json.load(inf)

            for s in self.slice_nums:
                C_node = central_node_ids[s-1]
                si = clusters[str(s)]
                for k in si.keys():
                    ci = set(si[k])
                    if C_node in ci:
                        central_node_clusters.append(k)
                        break
            
            slice_info = []
            for i in range(len(central_node_clusters)):
                slice_info.append(f"{central_node_clusters[i]},{largest_cluster_ids[i]}")


            M_info.append(slice_info)

        df = pd.DataFrame() 
        for m in range(num_methods):
            df.insert(m, f"{self.methods[m]}", M_info[m], True)
        
        
        df.to_csv(self.path_to_save_compare + "compare_Lc_2_CNc.txt", index=False, sep = " ")


        # leiden louvain evt java 
        # last inn fil av største cluster for alle 
        # loop over alle clustere i hver slice, finn cluster hvor mest sentral node er
        # largre cluster id 

        # får da | leiden | louvain (| java |)
        #      s1|id, id_L|id, id_L (|  id, id_L   |)
        #      -------------------------------
        #      -------------------------------
        #      sN|id, id_L|id, id_L (|  id, id_L   |)


    def find_id_of_top_5(self):
        # Find Cid and size of 5 largest
        m =0
        M_info = []
        num_methods = 3
        central_node_ids = []
        path_2_exp = self.path.rsplit("/",2)[0] + "/"
        path_2_partitions = path_2_exp + "parsed_dictionaries/"

        file_centrality = self.path_to_save_top + "top5_centrality.txt"
        with open(file_centrality,"r") as inf:
            inf.readline()
            lines = inf.readlines()
            for line in lines: 
                tmp = line.split(":")[1]
                tmp = tmp.replace("'","")
                tmp = tmp.strip("[]").split(",")
                ids = []
                for t in tmp:
                    ids.append(int(t))

                central_node_ids.append(ids)

        
        for method in self.methods:
            print("new method")
            largest_cluster_ids = []
            largest_cluster_sizes = []
            central_node_clusters = []
            central_node_c_sizes = []

            file_largest_c = path_2_exp + "statistics/Largest_clusters/" + method.title() + "/stats_LC_Nnodes_Nclusters.txt"
            with open(file_largest_c,"r") as inf:
                inf.readline()
                lines = inf.readlines()
                for line in lines:
                    largest_cluster_ids.append(int(line.split()[1]))

            
            clusters_file = path_2_partitions + "partitions_" + method + ".json"
            with open(clusters_file, "r") as inf:
                clusters = json.load(inf)

            for s in self.slice_nums:
                si = clusters[str(s)]
                C_nodes = central_node_ids[s-1]
                tmp_c = []
                tmp_s = []
                for n in C_nodes:
                    c_k = str(n)
                    for k in si.keys():
                        ci = set(si[k])
                        if c_k in ci:
                            tmp_c.append(int(k))
                            tmp_s.append(len(ci))
                            break
                central_node_clusters.append(tmp_c)
                central_node_c_sizes.append(tmp_s)
                largest_cluster_sizes.append(len(set(si[str(largest_cluster_ids[s-1])])))

            slice_info = []
            for i in range(len(central_node_clusters)):
                p = [central_node_clusters[i],largest_cluster_ids[i],central_node_c_sizes[i],largest_cluster_sizes[i]]
                slice_info.append(p)

            M_info.append(slice_info)
        
        print(M_info)
        df = pd.DataFrame() 
        for m in range(num_methods):
            df.insert(m, f"{self.methods[m]}", M_info[m], True)
        
        print(df)
        df.to_csv(self.path_to_save_compare + "compare_Lc_2_CNc_top5.csv", index=False, sep = " ")
        
        

        


