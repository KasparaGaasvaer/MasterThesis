# Louvain

# nx_louvain
"""
            ratios = [] 
            
            vals = list(partition.values())
            for i in range(len(vals)):
                vals[i] = int(vals[i])
            print(f"number of clusters = {max(vals)}")
            modularity = cluster_louvain.modularity(partition, G)
            print(f"Modularity = {modularity:0.5f}")
            ratio = G.number_of_nodes()/max(vals)
            print(f"Ratio nodes/parts = {ratio:0.5f}")
            ratios.append(ratio)
            print(" ")
            mean = np.mean(ratios)
            std = np.std(ratios)
            print(f"Avg ratio  = {mean:0.5f}, std = {std:0.5f} ")

            vals = partition
"""