#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: Jyoti
"""
#inputs: First argument - entity-term-index
#       Second argument - entity-vocab
#       Third argument - non-entity-index
#       Fourth argument - non-entity-vocab
#output: svmvector.csv file with 1 row per article for counts of non-entities followed by entities in the columns
import sys
import csv

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

vector = [[]]*(len(dicte) + 1)
vector1 = [[]]*len(dicte)
vector2 = [[]]*len(dicte)

for i in range(lines_e+lines_ne):
    vector[0].append("F"+str(i))
    
for j in range(len(dicte)):
    temp1 = dicte[j]
    temp2 = dictne[j]   
    vector1[j] = [0]*(lines_e)
    vector2[j] = [0]*(lines_ne)
    
    for i in temp1:
        vector1[j][i] += 1
    
    for k in temp2:     
        vector2[j][k] += 1

    vector[j+1] = vector2[j] + vector1[j]
# In[2]:
    
with open("svmvector1.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(vector)
        

