#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 19:10:35 2017

@author: florent

Hash Code Pratice Problem
Let's slice some pizza!
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
from random import randint

def libre(i, j):
    for s in slices.items():
        key,val = s
        x,y = key
        dx,dy = val
        if x <= i < x+dx and y <= j < y+dy:
            return False
    return True
    
def score():
    res = 0
    for s in slices.items():
        _,val = s
        res += val[0]*val[1]
    return res

#%%
best_slices = {}
best_score = 0
max_score = rows*cols

slices = {}
for iter in range(10000):
    print('Iteration {}...'.format(iter))
    for i in range(rows):
        for j in range(cols):
            if libre(i,j):
                slices[i,j] = (1,1)
                r = randint(0,10)
                while(r > 1):
                    r = randint(0,10)
                    h,w = slices[i,j]
                    if i+h < rows and (h+1)*w <= max_cells_in_slice \
                    and all(libre(i+h,j+dw) for dw in range(w)):
                        slices[i,j] = (h+1,w)
                    elif j+w < cols and h*(w+1) <= max_cells_in_slice \
                    and all(libre(i+dh,j+w) for dh in range(h)):
                        slices[i,j] = (h,w+1)
                    else:
                        break
                #print(slices)
                # Check consistency
                h,w = slices[i,j]
                mushrooms = sum(pizza[i+dh][j+dw] == 'M' for dh in range(h) \
                                for dw in range(w))
                tomatos = sum(pizza[i+dh][j+dw] == 'T' for dh in range(h) \
                                for dw in range(w))
                if mushrooms < min_ingredients or tomatos < min_ingredients:
                    slices.pop((i,j))
    sco = score()
    if sco > best_score:
        best_slices = slices.copy()
        best_score = sco
        print('Score : {}'.format(sco))
    if sco == max_score:
        break
    try:
        slices.pop((randint(0,rows-1),randint(0,cols-1)))
        #print('popped!')
    except KeyError:
        pass

print('Number of iterations : {}'.format(iter))