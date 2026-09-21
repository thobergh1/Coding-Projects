import matplotlib.pyplot as plt
import itertools as itool
import pandas as pd
import numpy as np
import random
import time

l = range(0, 24)
infile = pd.read_csv("european_cities.csv", sep =";", skiprows = 1, names = l )
N = 24

def TSP(infile, combination, N):
    data = infile.loc[:N-1, :N-1]
    pos = 1
    tmp = 0
    min_val = 10E5
    
    for j in combination:
        if(pos == N):
            pos = 1
            tmp = tmp + data[j][combination[0]]
        else:
            tmp = tmp + data[j][combination[pos]]
            pos = pos + 1
    if(tmp < min_val):
        min_val = tmp
    tmp = 0
    return min_val


def Hillclimb(infile, N):
    data = infile.loc[:N-1, :N-1]
    run = True
    route = [_ for _ in range(N)]    
    random.shuffle(route)
    
    current_val, new_val, high_val = 0,0,0
    max_evaluations = 100
    x,y = 0,0

    values = []
    
    current_val = TSP(data, route, N)
    count = 0
    while (run == True):
        run = False
        for i in range(max_evaluations):
            x = np.random.choice(route)
            y = np.random.choice(route)
            
            while (x==y):
                y=np.random.choice(route)
                    
            route[x],route[y] = route[y],route[x]
            
            new_val = TSP(data, route, N)
            values.append(new_val)
            
            if (new_val < current_val):
                current_val = new_val
                run = True
                break
            else:
                high_val = new_val
                route[y],route[x] = route[x],route[y]
            count += 1
    
    return current_val, high_val, values, count

total_time = []
for _ in range(0, 20):
    start = time.time()
    low, high, all_val, count = Hillclimb(infile, N)
    print("Run n = %.f | Longest: %.2fkm | shortest: %.2fkm | median: %.2fkm | count: %.2f" \
          %(_, high, low, sum(all_val)/len(all_val), count))
    end = time.time()
    total_time.append(end-start)

x = np.linspace(0, 20, len(total_time))

plt.figure()
plt.plot(x, total_time)
plt.xlabel("runs (N)")
plt.ylabel("time (s)")
plt.legend(["time per run"])
plt.show()

print("Average time is %.2f seconds." %(sum(total_time)/len(total_time)))