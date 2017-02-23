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
population = []

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

    population.append(M)

best_sco
for k in range(n_pop):
    

                
                #%%
save_solution(random_sol, pb_name+'_caca.out')