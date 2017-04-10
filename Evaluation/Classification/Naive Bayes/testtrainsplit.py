#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 00:45:06 2017

@author: Jyoti
"""
#input: training file to be split
#outputs: label_train.txt and label_test.txt

import random
import sys
import io

data = []

filelabel = sys.argv[1]
filename = io.open(filelabel, 'r', encoding = 'utf8')
lines = filename.readlines() 

for line in lines:
    data.append(line)
filename.close()
 
random.shuffle(data)
training = data[:int((len(data)+1)*.80)] 
testing = data[int(len(data)*.80+1):] 

with io.open("eighteen-plus_train.txt", 'w', encoding = 'utf8') as f:
    f.write("".join(training))

with io.open("eighteen-plus_test.txt", 'w', encoding = 'utf8') as f:
    f.write("".join(testing))                 