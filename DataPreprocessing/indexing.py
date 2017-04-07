#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: Jyoti
"""

#inputs: First argument - entity/non-entity vocab file (Indexed 0 to n..)
#       Second argument - entity/non-entity-list file one line per article (Indexed 0 to n..)
#output: term-index.txt indexed terms according to index in vocab files
    
    
import sys
import os
import string


# In[2]:

file_train = sys.argv[2]
file_label = sys.argv[1]

dict_labels = {}

filename = open(file_label,'r')

lines = filename.readlines()
for line in lines:
    words = line.split()
    LB = int(words[0])
    key = words[1] 
    dict_labels[key] = LB

dict_words = {}
filename.close()

filename2 = open(file_train, 'r')

lines = filename2.readlines()

for line in lines:
    words = line.split()
    key = int(words[0])
    wordlist = words[1::]
    #wordlist = filter(lambda i: not str.isdigit(i), wordlist)
    dict_words[key] = wordlist
filename2.close()

output_words = {}
for k in dict_words.keys():
    numbers = dict_words[k]
    
    words = []
    for number in numbers:
        word = dict_labels[number]
        words.append(word)
    
    output_words[k] = words
    

test_file = open(file_train, 'r')
output = open('term-index.txt', 'w+')    
lines = test_file.readlines()

i = 0
for line in lines:
    words = line.split()
    key = int(words[0])
    temp = ' '.join(map(str, output_words[key]))
    output.write(temp) 
    output.write('\n')
    i = i + 1
test_file.close()
output.close()  

        
        
        
