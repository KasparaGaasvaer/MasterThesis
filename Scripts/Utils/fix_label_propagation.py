import numpy as np
import json, os



exps = ["6","7","8","9","600","800"]

outer_p = "../"

for exp in exps:
    print("exp ", exp)
    p_2_c = outer_p + "experiment" + exp + "/parsed_dictionaries/"

    old_partitions = p_2_c + "partitions_lprop_source.json"

    new_p = {}

    with open(old_partitions,"r") as inff:
        old_p = json.load(inff)

    num_slices = len(old_p.keys())
    for s in range(1,num_slices+1):
        ss = str(s)
        slice = old_p[ss]
        new_p[ss] = {k: v for k, v in slice.items() if len(v) >= 2}




    final_p = {}
    for s in range(1,num_slices+1):
        ss = str(s)
        slice = new_p[ss]
        final_p[ss] = {}
        counter = 0
        for part in slice.keys():
            final_p[ss][str(counter)] = slice[part]
            counter +=1
        

    with open(p_2_c + "partitions_lprop.json","w") as ouff:
        json.dump(final_p,ouff)