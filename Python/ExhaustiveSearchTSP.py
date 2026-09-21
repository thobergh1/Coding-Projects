import matplotlib.pyplot as plt
import itertools as itool
import pandas as pd
import numpy as np
import time
import math

l = range(0, 24)
infile = pd.read_csv("european_cities.csv", sep =";", skiprows = 1, names = l )

def TSP(infile, N):
    data = infile.loc[:N-1, :N-1]
    comb = list(itool.permutations(data))
    pos = 1
    tmp = 0
    min_val = 10000
    
    for i in comb:
        if(i[0] != 0):
            break
        for j in i:
            if(pos == N):
                pos = 1
                tmp = tmp + data[j][0]
            else:
                tmp = tmp + data[j][i[pos]]
                pos = pos + 1
        if(tmp < min_val):
            min_val = tmp
        tmp = 0
    
    return min_val

total_time = []
for i in range(1, 10):
    start = time.time()
    TSP(infile, i)
    end = time.time()
    total_time.append(end-start)

x = np.linspace(1, 10, 9)

plt.figure()
plt.plot(x, total_time)
plt.xlabel("cities (N)")
plt.ylabel("time (s)")
plt.legend(["Seconds per calculation"])
plt.show()