import numpy as np
import matplotlib.pyplot as plt
import os, sys
import pandas as pd
from datetime import datetime

path = "./Distributions/"
path_plots = path + "Plots/"
def types_per_user(filename):
    df = pd.read_csv(filename)
    types = list(df)
    df = df.to_numpy()

    dict = {}
    for i in range(len(types)):
        dict[types[i]] = df[:,i]

    for type in dict.keys():
        if type != "otherContacts":
            x = dict[type]
            #x = list(filter(lambda a: a!= 0, x))
            #print(x)
            plt.hist(x, bins = np.linspace(np.min(x), np.max(x)+1, 100))
            plt.yscale("log")
            plt.ylabel("Log(frequency)")
            plt.title(type + ", bins = 100")
            plt.xlabel("Num Contacts")
            plt.savefig(path_plots + type + ".pdf")
            plt.clf()

def types_timedist(filename):
    df = pd.read_csv(filename)
    df["count"] = [1]*len(df["date"])
    types = list(df)

    retweets = df[df[types[1]] == "r"]
    comments = df[df[types[1]] == "c"]
    quotes = df[df[types[1]] == "q"]

    retweets.loc[:,'date'] = pd.to_datetime(retweets.loc[:,'date'], errors='coerce')
    comments.loc[:,'date'] = pd.to_datetime(comments.loc[:,'date'], errors='coerce')
    quotes.loc[:,'date'] = pd.to_datetime(quotes.loc[:,'date'], errors='coerce')

    #plt.figure(figsize=(20, 10))
    #ax = sub
    #ax = (quotes.loc[:,"date"].groupby([quotes.loc[:,"date"].dt.year,quotes.loc[:,"date"].dt.month]).count()).plot(kind="bar", color = "b")
    retweets.loc[:,"date"].groupby([retweets.loc[:,"date"].dt.year,retweets.loc[:,"date"].dt.month]).count().plot(kind = "bar", color = "r", label = "Retweets")
    quotes.loc[:,"date"].groupby([quotes.loc[:,"date"].dt.year,quotes.loc[:,"date"].dt.month]).count().plot(kind = "bar", color = "b", label = "Quotes")
    comments.loc[:,"date"].groupby([comments.loc[:,"date"].dt.year,comments.loc[:,"date"].dt.month]).count().plot(kind = "bar", color = "c", label = "Comments")
    #ax.set_facecolor('#eeeeee')
    #ax.set_xlabel("day")
    #ax.set_ylabel("count")
    #ax.set_title("both?")
    #ax.set_yscale("log")
    plt.legend()
    plt.yscale("log")
    plt.locator_params(axis="x", nbins=20)
    plt.show()


    #quotes = quotes.sort_values('date', ascending=True)
    #plt.plot(quotes['date'], quotes['count'])
    #plt.xticks(rotation='vertical')
    #plt.show()

    #retweets = list(retweets[types[0]])
    #comments = list(comments[types[0]])
    #quotes = list(quotes[types[0]])


def contacts_per_edge(filename):
    with open(filename,"r") as rf:
        nums = []
        rf.readline()
        lines = rf.readlines()
        for line in lines:
            line = int(line)
            nums.append(line)

        maxi = max(nums)
        bins = np.zeros(maxi+1)
        for i in nums:
            bins[i] += 1

        more_than_1 = np.where(bins > 1)
        print(more_than_1)
        #No bins > 1 after idx = 140 ish
        bins = np.log(bins)

        zeros = [0 for i in range(maxi+1)]
        x = np.array([i for i in range(maxi+1)])
        stop = np.where(x == 200)[0]
        stop = stop[0]
        plt.vlines(x=x[:stop], ymin=zeros[:stop], ymax=bins[:stop], lw=2)
        #plt.yscale("log")
        plt.ylabel("Log(frequency)")
        plt.xlabel("Contacts per Edge")
        plt.show()







#types_per_user(path + "all_k_per_user_distribution.csv")
#types_timedist(path + "all_k_distribution.csv")
contacts_per_edge(path + "all_k_per_user_pair_distribution.csv")
