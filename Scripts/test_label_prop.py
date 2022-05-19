import os
import pandas as pd
path = "../../../daniels/kaspara/experiment_7e_1_days_all/"

slices = os.listdir(path)

count = 0

for s in slices:
    if s != "slice_100":
        print(s)

        ps = path + s +"/cluster/"
        clusters = os.listdir(ps)

        for c in clusters:
            # print(c)
            filename = path + ps + "/" + c 
            f = pd.read_csv(filename)
            if len(f.index) < 2:
                count += 1
            # with open(filename, "r") as inff:
            #     lines = inff.readlines()
            #     if len(lines) < 3:
            #         count += 1


    print(count)
        