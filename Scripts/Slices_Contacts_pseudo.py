
"""
I = total number of edges in G
a = scalar int to determine initial K
N = total number of nodes
"""

def create_slices(I,a, N, E, Sc, e):
    i = 0
    K = [a]*N 
    N = 0
    K_holder = [k_old,k_new]
    j = 1
    while [len( E[n] ) <= K[n] for n in N]:
        Sc[j] += e[i]
        if [any len(E[n]) > K[n] for n in N]: #Can insted just check the affected nodes by e_i
            check_agreement([nodes affected by e_i])
            if agreement:
                Sc[j+1] = Sc[j] - find_eno() 
                K_holder[j-1] = Mean_num_edges() #func that returns list*N of num edges to nodes
                j+= 1
        else:
            i+1

    while i < I:
        K = ( K_holder[0] + K_holder[1] )/( j-1 )
        while [len( E[n] ) <= K[n] for n in N]:
            Sc[j] += e[i]
            if [any len(E[n]) > K[n] for n in N]: #Can insted just check the affected nodes by e_i
                check_agreement([nodes affected by e_i])
                if agreement:
                    Sc[j+1] = Sc[j] - find_eno() 
                    K_holder[0] += K_holder[1]
                    K_holder[1] = Mean_num_edges() #func that returns list*N of num edges to nodes
                    j+=1
            else:
                i+1







    #Something to add nodes to N end E