#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 01:06:23 2017

@author: Jyoti
"""
#inputs: First argument - entity-term-index
#       Second argument - entity-vocab
#       Third argument - non-entity-index
#       Fourth argument - non-entity-vocab
#output: svmvector.txt file with 1 line per article with entities followed by non entities

entity = sys.argv[1]
nonentity = sys.argv[3]
entity_vocab = sys.argv[2]
nonentity_vocab = sys.argv[4]

dicte = {}
dictne = {}

fileentity = open(entity,'r')
lines = fileentity.readlines()
for line in lines:
    words = line.split()
    key = int(words[0]) 
    dicte[key] = map(int, words[1::])

dict_words = {}
fileentity.close()

filenonentity = open(nonentity,'r')
lines = filenonentity.readlines()
for line in lines:
    words = line.split()
    key = int(words[0]) 
    dictne[key] = map(int, words[1::])

dict_words = {}
filenonentity.close()

file_evocab = open(entity_vocab,'r')
lines_e = len(file_evocab.readlines())
file_nevocab = open(nonentity_vocab,'r')
lines_ne = len(file_nevocab.readlines())

vector = {} 
vector1 = {}
vector2 = {}           
for j in range(len(dicte)):
    temp1 = list(set(dicte[j]))
    temp2 = list(set(dictne[j]))   
    vector1[j] = []
    vector2[j] = []
    
    for i in range(lines_e):
        if i in temp1:
            vector1[j].append(1)
        else:
            vector1[j].append(0)
        
        if i in temp2:
            vector2[j].append(1)
        else:
            vector2[j].append(0)
    
    vector[j] = vector1[j] + vector2[j]

# In[2]:
    
o = open('svmvector.txt', 'w+');
for i in range(len(vector)):
    o.write(str(vector[i]))
    o.write('\n')

o.close()
    
        
