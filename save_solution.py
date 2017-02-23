#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:00:39 2017

@author: f.forest
"""

import numpy as np

def save_solution(sol, filename):
    with open(filename, 'w') as f:
        n_servers = (np.sum(sol, axis=1) != 0).sum()
        f.write(str(n_servers)+'\n')
        
        for i in range(sol.shape[0]):
            l = str(i) + ' '
            for j in range(sol.shape[1]):
                if sol[i,j] == 1:
                    l += str(j) + ' '
            l += '\n'
            f.write(l)