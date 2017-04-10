#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: Jyoti
"""
#inputs: list of all training input files
#output: nbmodel.txt containing naive bayes parameters - priors, probabilities per word per class


import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import string
import json
import math
from collections import Counter

dict_labels = {}
dict_words = {}

model = {}
model['Prior'] = {}  
model['class'] = {}
l = []

for i in range(1,len(sys.argv)):
    filelabel = sys.argv[i]
    x = filelabel.split(".")
    label = x[0]
    l.append(label)
    filename = open(filelabel, 'r')
    lines = filename.readlines() 
    key = 1
    for line in lines:
        wordlist = line.split()
        wordlist = filter(lambda i: not str.isdigit(i), wordlist)
        key2 = x[0] + str(key)
        key += 1
        dict_labels[key2] = label
        dict_words[key2] = wordlist
    
    filename.close()

model['class'] = l
prior = {} 
file_stop = open('stop-words.txt', 'r')
stop_words = [word.rstrip('\n') for word in file_stop.read().splitlines()]

c = Counter(dict_labels.values())
classes = {}
vocab = []
for i in range(1,len(sys.argv)):
    filelabel = sys.argv[i]
    x = filelabel.split(".")
    label = x[0]
    model
    model['Prior'][label] = (c[label])*1.0/sum(c.values())
           
    classes[label] = []
            
    for key in dict_labels.keys():
                if dict_labels[key] == label:
                    words = dict_words[key];
                    words = [x for x in words if x not in stop_words]
                    for word in words:
                        word = word.translate(None, string.punctuation)
                        word = word.decode('utf-8').replace(u'\u00A0', '').encode('utf-8')
                        #word = ''.join(x for x in word if x not in string.punctuation)
                        classes[label].append(word)
    
    temp = list(set(classes[label]))
    vocab = vocab + temp 
    
vocab = list(set(vocab)) 
   
for i in range(1,len(sys.argv)):
    filelabel = sys.argv[i]
    x = filelabel.split(".")
    label = x[0]
    count = Counter(classes[label])  
    
    model[label] = {}
    
    for word in vocab:
            
            countf = 1 + count[word]
            
            model[label][word] = (countf * 1.0) /(len(classes[label]) +len(vocab))
            
        
o = open('nbmodel.txt', 'w+');
json.dump(model, o)
o.close()