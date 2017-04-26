#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 00:29:33 2017

@author: Jyoti
"""
#inputs: nboutput.txt with each row identifying the article by its key followed by its predicted label


from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from string import digits

# Read output file
with open('nboutput.txt') as f:
    lines = f.readlines()

# First make a list and then a dictionary mapping keys with corresponding labels
test_list = []
true_list = []
for line in lines:
    test_list.append(line.split()[1])
    true_list.append(line.split()[0].translate(None, digits))

dict_num={}
i = 0
for item in true_list:
    if(i>0 and item in dict_num):
        continue
    else:    
       i = i+1
       dict_num[item] = i

test = []
true = []
for item in test_list:
    test.append(dict_num[item])

for item in true_list:   
    true.append(dict_num[item])

f1 = f1_score(true, test, labels=None, pos_label=1, average='weighted', sample_weight=None)
cf = confusion_matrix(true, test)
ac = accuracy_score(true, test)