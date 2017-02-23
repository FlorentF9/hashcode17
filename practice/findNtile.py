#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:45:10 2017

@author: florent
"""
#%% Load data

pb_name = 'big'
file = pb_name+'.in'

with open(file, 'r') as f:
    header = f.readline().replace('\n', '').split()
    rows = int(header[0])
    cols = int(header[1])
    min_ingredients = int(header[2])
    max_cells_in_slice = int(header[3])
    pizza = [l.replace('\n', '') for l in f.readlines()]
    
             
#%%
"""
Find acceptable slices

"""
import random
slices = []
max_slices = rows*cols//(2*min_ingredients)

def isOk(i1,j1,i2,j2):
    if (i2-i1+1)*(j2-j1+1) < 2*min_ingredients:
        return False
    if (i2-i1+1)*(j2-j1+1) > max_cells_in_slice:
        return False
    if sum(pizza[i][j] == 'M' for i in range(i1,i2+1) for j in range(j1,j2+1)) \
    < min_ingredients:
        return False
    if sum(pizza[i][j] == 'T' for i in range(i1,i2+1) for j in range(j1,j2+1)) \
    < min_ingredients:
        return False
    return True


def find_slices(max_iter, n_slices):
    slices = []
    it = 0
    while it < max_iter and len(slices) < n_slices:
        it += 1
        if it%100000 == 0:
            print(it)
        i1 = random.randint(0,rows-1)
        i2 = i1 + random.randint(0,rows-i1-1)
        j1 = random.randint(0,cols-1)
        j2 = j1 + random.randint(0,cols-j1-1)
        if isOk(i1,j1,i2,j2):
                slices.append((i1,j1,i2,j2))
    if slices != []:
        print('{}/{} acceptable slices found'.format(len(slices),max_slices))
    else:
        print('No slices found.')
    return slices

n_slices = 2000
max_iter = 10000000
slices = find_slices(max_iter, n_slices)

#%%
from facile import *

def overlap(a, b):
    a_i1,a_j1,a_i2,a_j2 = a
    b_i1,b_j1,b_i2,b_j2 = b
    
    i_overlap = a_i1 <= b_i2+1 and a_i2+1 >= b_i1
    j_overlap = a_j1 <= b_j2+1 and a_j2+1 >= b_j1
    return 1 if i_overlap and j_overlap else 0
    
n = len(slices)
value = np.array([(s[2]-s[0]+1)*(s[3]-s[1]+1) for s in slices])
overlap_matrix = np.zeros((n,n),dtype=int)
for k in range(n):
    for l in range(k+1,n):
        overlap_matrix[k,l] = overlap(slices[k],slices[l])

#%%

overlap_matrix += overlap_matrix.T - np.diag(overlap_matrix.diagonal())
# Trier les parts, et placer toutes les parts qui ne se chevauchent pas
sorted_idx = np.argsort(-value)

solution_idx = []
for l in sorted_idx:
    #print('Ajouter {} ?'.format(l))
    ajouter = True
    # k < l
    for k in solution_idx:
        if overlap_matrix[k,l] == 1:
            ajouter = False
            #print('Non, overlap avec {} !'.format(k))
            break
    if ajouter:
        solution_idx.append(l)
        #print('Oui !')
        
solution = []
for idx in solution_idx:
    solution.append(slices[idx])
    
print(solution)
score = np.sum(value[k] for k in solution_idx)
print('Score : {}'.format(score))
        
#%%
"""
Optimisation (type sac à dos)
"""

n = 50

# choice[i] = 1 si on choisit la part de pizza numéro i
choice = [variable(0,1) for k in range(n)]

# contraintes de non-superposition
for k in range(n):
    for l in range(k+1,n):
        constraint(overlap_matrix[k,l]*choice[k]*choice[l] == 0)
        
loss,sol = minimize(choice, -np.sum(value[k]*choice[k] for k in range(n)))

solution = []
for i in range(n):
    if sol[i] == 1:
        solution.append(slices[i])

print('Score : {}/{}'.format(-loss,rows*cols))
        
#%%
"""
Dump solution
"""

from six.moves import cPickle as pickle

with open(pb_name+'_findNtile.pickle', 'wb') as f:
    pickle.dump({'score': -loss, 'solution': solution}, f)
    
    