#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 03:18:00 2017

@author: Jyoti
"""
import sys
import io

data = {}
test = []
dict_labels = {}
dict_words = {}
for i in range(1,len(sys.argv)):
    filelabel = sys.argv[i]
    x = filelabel.split("_")
    label = x[0]
    filename = io.open(filelabel, 'r', encoding='utf8')
    lines = filename.readlines() 
    key =  1
    for line in lines:
        key2 = x[0] + str(key)
        key += 1
        dict_labels[key2] = label
        dict_words[key2] = line
    filename.close()

test = io.open("testing.txt", 'w', encoding = 'utf8')
test_label = open("test-labels.txt", 'w+')

for key in dict_words.keys():
    test.write(key + " " + dict_words[key])
    test_label.write(key)
    test_label.write("\n")

    