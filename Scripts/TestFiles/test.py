
si  = {
    "1" : [100,0,9,7],
    "2" : [100,0,9,7],
    "3" : [100,0,9,7]
}

si_cids = list(si.keys())
si_hit_dict = {}
for d in range(len(si_cids)):
    si_hit_dict[si_cids[d]] = 0

print(si_hit_dict)