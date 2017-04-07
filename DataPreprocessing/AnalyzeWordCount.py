#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
vocab = {}
with open('non-entity-vocab') as f:
    list = [line.rstrip() for line in f]
for elem in list:
    vocab[elem.decode('utf-8')] = 0
with open('non-entity-term-index') as f:
    ent_list = [line.rstrip() for line in f]
for line in ent_list:
    words = line.split()
    for word in words:
        vocab[list[int(word)].decode('utf-8')]+=1

f = open('count.txt', 'w+');
for v in vocab:
    f.write(v.encode('utf-8'))
    f.write(":"+str(vocab[v]))
    f.write('\n')
f.close()
print(1)