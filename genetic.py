#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 20:01:49 2017

@author: f.forest

PLNE
"""

from save_solution import *
from score import *

#%%
pb_name = 'me_at_the_zoo'
#pb_name = 'videos_worth_spreading'
#pb_name = 'trending_today'
#pb_name = 'kittens'

file = 'data/'+pb_name+'.in'

with open(file, 'r') as f:
    header = f.readline().replace('\n', '').split()
    V = int(header[0]) # number of videos
    E = int(header[1]) # number of endpoints
    R = int(header[2]) # number of requests descriptions
    C = int(header[3]) # number of cache servers
    X = int(header[4]) # capacity of cache servers
    
    S = [int(x) for x in f.readline().replace('\n', '').split()] #sizes
    
    Ld = [] # latency to data center
    K = [] # number of cache servers
    
    cacheLatencies = [] # list of dictionnaries reprensenting latencies to caches of all endpoints
    requests = [] # list of requests. A request is a tuple containing : videoID, endpointID, number of request
    
    for e in range(E):
        l = f.readline().replace('\n', '').split()
        Ld.append(int(l[0]))
        K.append(int(l[1]))
        
        d = dict()
        for k in range(K[e]):
            l2 = f.readline().replace('\n', '').split()
            d[int(l2[0])] = int(l2[1])
        cacheLatencies.append(d)
    
    
    for r in range(R):
        l3 = f.readline().replace('\n', '').split()
        
        requests.append((int(l3[0]), int(l3[1]), int(l3[2])))

#%%

import numpy as np

def line_ok(line):
    return sum(int(S[i]) for i in range(len(line)) if line[i] == 1) <= X

n_pop = 100
population = np.zeros((n_pop,C,V))

for k in range(n_pop):
    # pour chaque cache server
    M = np.zeros((C,V))
    
    for i in range(C):
        shuffled_videos = np.arange(V)
        np.random.shuffle(shuffled_videos)
        for v in shuffled_videos:
            tmp = M[i].copy()
            tmp[v] = 1
            if line_ok(tmp):
                M[i,v] = 1

    population[k] = M

    
#%%
# Reproduction
epochs = 1000

for _ in range(epochs):
    scores = np.zeros(n_pop)
    
    for k in range(n_pop):
        scores[k] = score(population[k], cacheLatencies, requests, C, Ld)
     
    population = population[np.argsort(-scores)]
                            
    """
    # modification des plus mauvais individus
    for k in range(1, n_pop):    
        for i in range(C):
            for j in range(V):
                tmp = population[k,i,:].copy()
                change = np.random.randint(2)
                if change == 1:
                    tmp[j] = 1-tmp[j]
                    if line_ok(tmp):
                        population[k,i,j] = tmp[j]
    """
    
    # reproduction et mutation parmi les 10 meilleurs individus
    n_selec = 10
    for k in range(n_selec,n_pop):
        male,femelle = np.random.randint(n_selec), np.random.randint(n_selec)
        enfant = population[femelle].copy()
        # selection aléatoire d'une ligne
        c = np.random.randint(C)
        enfant[c] = population[male][c]
        # mutation
        ok = False
        while not ok:
            c,v = np.random.randint(C), np.random.randint(V)
            tmp = enfant[c].copy()
            tmp[v] = 1-tmp[v]
            if line_ok(tmp):
                ok = True
                enfant[c,v] = tmp[v]
        population[k] = enfant
    
    best_score = 0
    for k in range(n_pop):
        sco = score(population[k], cacheLatencies, requests, C, Ld)
        if sco > best_score:
            best_score = sco
    print('Best score = {}'.format(best_score))

#%%
best_score = 0
best_indiv = np.zeros((C,V))

for k in range(n_pop):
    sco = score(population[k], cacheLatencies, requests, C, Ld)
    if sco > best_score:
        best_score = sco
        best_indiv = population[k]

print('Best score = {}'.format(best_score))

                
#%%
save_solution(best_indiv, pb_name+'_genetic.out')