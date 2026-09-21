import itertools as itool
import pandas as pd
import numpy as np
import random as random
import matplotlib.pyplot as plt

l = range(0, 24)
infile = pd.read_csv("european_cities.csv", sep =";", skiprows = 1, names = l )

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

def Generate_children(parrent1, dna, parrent2):
    child = parrent2
    for i in dna:
        for j in range(0, len(parrent1)):
            if child[j] == i:
                a = parrent1.index(i)
                b = child.index(i)
                child[a], child[b] = parrent1[a], child[a]
    return child
            

def Genetic_algorithm(infile, N, G, parents):
    max_evaluations = 100
    gen = G
    x, y = 0,0
    children = [0]*2*max_evaluations
    distances = [0]*G
    child1 = []
    child2 = []
    children_fitness = [0]*2*max_evaluations
    route_fitness = [0]*max_evaluations
    routes = [0]*parents
    new_children = [0]*2*max_evaluations
    
    p = [_ for _ in range(N)]
    
    for i in range(parents):
        np.random.shuffle(p)
        routes[i] = p.copy()

    for _ in range(gen):
        evaluations = 0
      
        while evaluations < max_evaluations:
            parrent1, parrent2 = random.sample(routes, 2)
            
            x, y = np.random.randint(0, N), np.random.randint(0, N)
            if (x==y):
                y=np.random.randint(0, N)
                
            if x < y:
                DNA = parrent1[x:y+1]
            else:
                DNA = parrent1[y:x+1]
            

            child1 = Generate_children(parrent1, DNA, parrent2)
            child2 = Generate_children(parrent2, DNA, parrent1)
            
            g, h = random.randint(0, N-1), random.randint(0, N-1)
            while (g==h):
                h=np.random.randint(0, N-1)
            
            child1[g], child1[h] = child1[h], child1[g]
            child2[g], child2[h] = child2[h], child2[g]
            
            children[evaluations] = child1
            children[evaluations+max_evaluations] = child2
            evaluations += 1
            
        children_fitness = [TSP(infile, children[i], N) for i in range(len(children))]
        route_fitness = [TSP(infile, routes[i], N) for i in range(len(routes))]
        
        children_combined = sorted([(distance, child) for distance, child in zip(children_fitness, children)])
        new_children = [child for distance, child in children_combined]
        
        route_combined = sorted([(distance, route) for distance, route in zip(route_fitness, routes)])
        new_routes = [route for distance, route in route_combined]
        
        new_pop = []
        
        for i in range(20):
            new_pop.append(new_routes[i])
             
        for i in range(80):
            new_pop.append(new_children[i])
        
        pop_fitness = [TSP(infile, routes[i], N) for i in range(len(routes))]
        
        pop_combined = sorted([(distance, route) for distance, route in zip(pop_fitness, routes)])
        routes = [route for distance, route in pop_combined]
        
        distances[_] = TSP(infile, routes[0], N)

    return distances

x = np.linspace(0, 20, 20)
for i in range(5):
    dist = Genetic_algorithm(infile, 24, 20, 100)
    plt.plot(x, dist)