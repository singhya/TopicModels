#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: Jyoti
"""
#inputs: testing.txt testing file with an alphanumeric key uniquely identifying each article
#output: nboutput.txt with each row identifying the article by its key followed by its predicted label


import sys
import string
import json
import math

o = open('nbmodel.txt', 'r')
data = json.load(o)
o.close()

file_name = sys.argv[1]

test_file = open(file_name, 'r')

dict_words = {}

lines = test_file.readlines()

for line in lines:
    words = line.split()
    key = words[0]
    wordlist = words[1::]
    wordlist = filter(lambda i: not str.isdigit(i), wordlist)
    dict_words[key] = wordlist

test_file.close()
#stop_words =[" "]

#stop_words = set([" ", "a","about","above","all","am","an","and","are","as","at","be","been","being","between","both","by","could","did","do","does","doing","during","each","for","from","further","had","has","have","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","it","it's","its","itself","let's","me","my","myself","of","on","once","only","or","other","ought","our","ours    ourselves","out","own","same","shan't","she","she'd","she'll","she's","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","until","up","was","we","we'd","we'll","we're","we've","were","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","would","you","you'd","you'll","you're","you've","your","yours""yourself","yourselves"])

output_words = {}

classes = data['class']
prob = {}

for key in dict_words.keys():
    words = dict_words[key]
    for i in range(len(classes)):    
        label = classes[i]
        prob[label] = 0
    
        for word in words:
            word = word.translate(None, string.punctuation)
            #word = word.lower()
           
           	#if word in stop_words:
            	#continue
           
            if word in data[label]:
                prob[label] += math.log(data[label][word], 10)
        prob[label] += math.log(data['Prior'][label], 10)
    maximum = max(prob.values())    
    for i in prob.keys():
        if prob[i] == maximum:
            output_words[key] = i.split("_")[0]    

test_file = open(file_name, 'r')
output = open('nboutput.txt', 'w+')    
lines = test_file.readlines()

for line in lines:
    words = line.split()
    key = words[0]
    output.write(key + ' ' + output_words[key] + '\n')   
    
test_file.close()
output.close()       