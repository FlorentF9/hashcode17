#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:25:34 2017

@author: florent
"""

from six.moves import cPickle as pickle

file = 'big_findNtile'

with open(file+'.pickle', 'rb') as f:
    solution = pickle.load(f)
    
solution = solution['solution']

n_slices = len(solution)

with open(file+'_2.out', 'w') as f:
    f.write(str(n_slices)+'\n')
    #for s in solution.items():
        #f.write('{} {} {} {}\n'.format(s[0][0],s[0][1],s[0][0]+s[1][0]-1,s[0][1]+s[1][1]-1))
    for s in solution:
        f.write('{} {} {} {}\n'.format(s[0],s[1],s[2],s[3]))