import sys, os, json, time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy.optimize import curve_fit

from Utils.graphs import Graphs
sys.path.append("..")  # Adds higher directory to python modules path, looking for Graphs-class one level up

class Centrality(Graphs):
    def __init__(self,path):

        self.path = path 
        self.expnum = self.path.strip("./")

        self.path_to_stats = self.path + "statistics/Centrality/"
        if not os.path.exists(self.path_to_stats):
            os.makedirs(self.path_to_stats)

        self.path_to_plots = self.path + "plots/Centrality/"
        if not os.path.exists(self.path_to_plots):
            os.makedirs(self.path_to_plots)

        self.path_to_overleaf_plots = "./p_2_overleaf" + self.path.strip(".") + "UnderlyingGraph/"
        if not os.path.exists(self.path_to_overleaf_plots):
            os.makedirs(self.path_to_overleaf_plots)


        #self.make_graphs()
        self.calculate_centralities()


    def make_graphs(self):
        
        self.path_to_dict = self.path + "parsed_dictionaries/"

        attributes_bool = False
        graph_type = "nx"

        super().__init__(self.path, graph_type, attributes_bool)

        self.num_slices = len(self.graphs.keys())


    def calculate_centralities(self):
        
        #self.deg_c()
        #self.avg_nhood_degree()
        #self.degdeg_plot() #denne som gir de stygge plottene
        #self.avg_degree_connectivity()
        #self.N_phases_deg_connectivity_plot()
        #self.is_scale_free()
        #self.deg_connectivity_plot()
        #self.assortativity_coeff()
        #self.closeness_c() #takes forever?
        #self.betweenness_c()
        self.deg_con_all_slices()
   
 
    def deg_c(self):
        print("DEGREE CENTRALITY\n")
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]
            nn = G.number_of_nodes() - 1

            start_s = time.perf_counter()
            s_dict = nx.degree_centrality(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating centrality {end_s-start_s:0.4f} s\n")

            s_dict.update((x, y*nn) for x, y in s_dict.items())

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "deg_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def closeness_c(self):
        print("CLOSENESS CENTRALITY\n")
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True)
            end_s = time.perf_counter()

            print(f"Time spent calculating closeness centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "closeness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def betweenness_c(self):
        print("BETWEENNESS CENTRALITY\n")
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
            end_s = time.perf_counter()

            print(f"Time spent calculating betweenness centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "betweenness_c_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def assortativity_coeff(self):
        print("ASSORTITIVIY COEFFICIENT")
        master_dict = {}
        for s in range(1,self.num_slices+1):
            G = self.graphs[str(s)]["graph"]
            start_s = time.perf_counter()
            s_dict = nx.degree_pearson_correlation_coefficient(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating assortivity {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "degree_assortivity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)


    def avg_nhood_degree(self):
        print("AVG NHOOD DEG")
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.average_neighbor_degree(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating avg centrality {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "avg_nhood_deg_dict.json","w") as ouf:
            json.dump(master_dict, ouf)

    def avg_degree_connectivity(self):
        print("AVG DEG CONNECTIVITY")
        master_dict = {}

        for s in range(1,self.num_slices+1):
            print("Slice ", s)
            G = self.graphs[str(s)]["graph"]

            start_s = time.perf_counter()
            s_dict = nx.average_degree_connectivity(G)
            end_s = time.perf_counter()

            print(f"Time spent calculating avg degree connectivity {end_s-start_s:0.4f} s\n")

            master_dict[str(s)] = s_dict 
        
        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","w") as ouf:
            json.dump(master_dict, ouf)


    def degdeg_plot(self):
        print("DEGDEG PLOT")
        path_to_these_plots = self.path_to_plots + "kk-correlation/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "deg_c_dict.json","r") as inff:
            ind_deg = json.load(inff)
        
        with open(self.path_to_stats + "avg_nhood_deg_dict.json","r") as inff:
            nhood_deg = json.load(inff)

        self.num_slices = len(ind_deg.keys())

        
        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            i_deg = ind_deg[s]
            n_deg = nhood_deg[s]

            print(len(i_deg))
            if len(i_deg) != len(n_deg):
                print("problem")

            
            k = []
            k_means = []
            for n in i_deg.keys():
                k.append(i_deg[n])
                k_means.append(n_deg[n])

            plt.scatter(k,k_means)
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel("k")
            plt.ylabel("k_mean")
            plt.savefig(path_to_these_plots + f"s{s}_k_vs_kmean.pdf")
            plt.savefig(self.path_to_overleaf_plots + f"s{s}_k_vs_kmean.pdf")
            plt.clf()


    def deg_con_all_slices(self):
        print("DEGCON PLOT ALL SLICES")
        path_to_these_plots = self.path_to_plots + "degree_connectivity/annd_all_slices/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        fz = 14

        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            dc = deg_con[s]
            
            key_list = [int(k) for k in dc.keys()]
            value_list = list(dc.values())

            x,y = zip(*sorted(zip(key_list,value_list)))

            plt.scatter(x, y)
            plt.title(f"Slice {ss}")
            plt.ylabel("ANND K(k)", fontsize = fz)
            plt.xlabel("Degree k", fontsize = fz)
            plt.xticks(fontsize =fz)
            plt.yticks(fontsize =fz)
            plt.yscale("log")
            plt.xscale("log")
            plt.tight_layout()
            plt.savefig(path_to_these_plots + f"jpgs/slice_{ss}.jpg")
            plt.clf()

            
    def deg_connectivity_plot(self):
        print("DEGCON PLOT")
        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        all_dict = {}

        self.num_slices = len(deg_con.keys())

        for ss in range(1,self.num_slices+1):
            print("Slice ", ss)
            s = str(ss)
            dc = deg_con[s]
            
            kv = []
            kavg = []
            for k in dc.keys():
                #kv.append(int(k))
                #kavg.append(dc[k])
                try:
                    all_dict[k].append(dc[k])
                except KeyError:
                    all_dict[k] = []
                    all_dict[k].append(dc[k])

            """
            x = np.log10(np.array(kv))
            y = np.log10(np.array(kavg))

            plt.scatter(x, y)

            x_2d = x.reshape((-1, 1))
            model = linear_model.LinearRegression().fit(x_2d,y)
            y_pred = model.predict(x_2d)

            plt.plot(x,y_pred, label = "Prediction from OLS", color = "r")
            plt.xlabel("k")
            plt.ylabel("average degree connectivity")
            plt.savefig(path_to_these_plots + f"s{s}_degree_connectivity.pdf")
            plt.clf()
            """
            

        kv = []
        kavg = []
        for k in all_dict.keys():
            kv.append(int(k))
            kavg.append(np.mean(all_dict[k]))


        """
        # Test for K(k) = a*k^b fit, not good
        x_t = np.array(kv)
        y_t = np.array(kavg)
        from scipy.optimize import curve_fit
        f = lambda x,a,b: a*x**b
        popt, pcov = curve_fit(f, x_t, y_t)
        plt.scatter(x_t,y_t)
        plt.plot(x_t, f(x_t, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()
        plt.savefig(f"degcontest_{self.expnum}.pdf")
        plt.clf()
        """


        #x = np.log10(np.array(kv))
        #y = np.log10(np.array(kavg))
        x = np.array(kv)
        y = np.array(kavg)

  
        fz = 14
        #fig, ax = plt.subplots()
        #ax.scatter(x,y)

        #x_2d = x.reshape((-1, 1))
        #model = linear_model.LinearRegression().fit(x_2d,y)
       # y_pred = model.predict(x_2d)

        #ax.plot(x,y_pred, label = f"K(k) ~ {model.coef_[0]:.4f}k + {model.intercept_:.4f}", color = "r")

        #ax.set_xticks(ax.get_xticks()[1::2])
        #ax.set_yticks(ax.get_yticks()[1::2])

        #x_l = ax.get_xticks()
        #new_x = [r"$10^{%.1f}$"%x for x in x_l]
        #ax.set_xticklabels(new_x)

        #y_l = ax.get_yticks()
        #new_y = [r"$10^{%.1f}$"%y for y in y_l]
        #ax.set_yticklabels(new_y)

        #plt.legend(fontsize = fz)
        plt.scatter(x,y)
        plt.xlabel("Degree k", fontsize = fz)
        plt.ylabel("ANND K(k)", fontsize = fz)
        plt.xticks(fontsize = fz)
        plt.yticks(fontsize = fz)
        plt.yscale("log")
        plt.xscale("log")
        plt.tight_layout()
        plt.savefig(path_to_these_plots + "over_all_slices_degree_connectivity.pdf")
        plt.savefig(self.path_to_overleaf_plots + "over_all_slices_degree_connectivity.pdf")
        plt.clf()
        
    
        



    def N_phases_deg_connectivity_plot(self):
        print("PHASE PLOT")
        path_to_these_plots = self.path_to_plots + "degree_connectivity/" 
        if not os.path.exists(path_to_these_plots):
            os.makedirs(path_to_these_plots)

        with open(self.path_to_stats + "avg_deg_connectivity_dict.json","r") as inff:
            deg_con = json.load(inff)

        self.num_slices = len(deg_con.keys())
        all_dict = {}

        phases_slice = np.load(self.path_to_stats + "slice_phases.npy")
 

        s_list = [i for i in range(1,self.num_slices+1)]
        s_list = np.array(s_list)
        phases = [s_list[:int(phases_slice[0])], s_list[int(phases_slice[0]):int(phases_slice[1])], s_list[int(phases_slice[1]):]]
        print(phases)

        m_dict = {}
        i = 0
        for phase in phases:
            m_dict[str(i)] = {}
            print("NEW PHASE ")
            for ss in phase:
                print("Slice ", ss)
                s = str(ss)
                dc = deg_con[s]
                kv = []
                kavg = []
                for k in dc.keys():
                    try:
                        m_dict[str(i)][k].append(dc[k])
                    except KeyError:
                        m_dict[str(i)][k] = []
                        m_dict[str(i)][k].append(dc[k])
            i += 1

        for j in range(len(phases)):
            all_dict = m_dict[str(j)]

            kv = []
            kavg = []
            for k in all_dict.keys():
                kv.append(int(k))
                kavg.append(np.mean(all_dict[k]))
            
            x = np.array(kv)#np.log10(np.array(kv))
            y = np.array(kavg)#np.log10(np.array(kavg))


            fz = 14
            # fig, ax = plt.subplots()
            # ax.scatter(x,y)

            # x_2d = x.reshape((-1, 1))
            # lin_model = linear_model.LinearRegression().fit(x_2d,y)
            # y_pred = lin_model.predict(x_2d)

            # ax.plot(x,y_pred, label = f"K(k) ~ {lin_model.coef_[0]:.4f}k + {lin_model.intercept_:.4f}", color = "r")

            # ax.set_xticks(ax.get_xticks()[1::2])
            # ax.set_yticks(ax.get_yticks()[1::2])

            # x_l = ax.get_xticks()
            # new_x = [r"$10^{%.1f}$"%x for x in x_l]
            # ax.set_xticklabels(new_x)

            # y_l = ax.get_yticks()
            # new_y = [r"$10^{%.1f}$"%y for y in y_l]
            # ax.set_yticklabels(new_y)

            #plt.legend(fontsize = fz)
            plt.scatter(x,y)
            plt.xlabel("Degree k", fontsize = fz)
            plt.ylabel("ANND K(k)", fontsize = fz)
            plt.title(f"Phase {j}", fontsize = fz)
            plt.yscale("log")
            plt.xscale("log")
            plt.xticks(fontsize = fz)
            plt.yticks(fontsize = fz)
            plt.tight_layout()
            plt.savefig(path_to_these_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.savefig(self.path_to_overleaf_plots + f"over_all_slices_degree_connectivity_phase_{j}.pdf")
            plt.clf()

            #f = lambda x,a: x**a
            #pow_coeff, cov = curve_fit(f, x, y)

            #plt.plot(x,f(x,*pow_coeff),"g.", label = f"K(k) ~ k^{pow_coeff[0]}")
        

    def is_scale_free(self):

        from scipy.optimize import curve_fit
        with open(self.path_to_stats + "deg_c_dict.json","r") as inff:
            degree = json.load(inff)

        distribution = {}
        num_nodes = 0
        for s in degree.keys():
            d = degree[s]
            for n in d.keys():
                num_nodes += 1
                d_n = d[n]
                try:
                    distribution[str(d_n)] +=1 
                except KeyError:
                    distribution[str(d_n)] = 1
        

        degrees = list(distribution.keys())
        count = list(distribution.values())

        degrees = np.array([float(i) for i in degrees])
        count = np.array([int(i) for i in count])/num_nodes

        degrees, count = zip(*sorted(zip(degrees,count)))

        f = lambda x,a: x**a

        coeff, cov = curve_fit(f, degrees, count)
        plt.plot(degrees, count, "b-", label = "Data")
        plt.plot(degrees,f(degrees,coeff),"r*", label = f"Power Fit: k^{coeff[0]}")
        plt.legend()
        plt.ylim([1e-7,1])
        plt.xscale("log")
        plt.yscale("log")
        plt.savefig("TEST_scale_free.pdf")



        




        

    


        





