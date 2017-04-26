#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Jyoti
"""

# inputs:
# First argument - entity/non-entity vocab file (Indexed 0 to n..)
# Second argument - entity/non-entity-list file one line per article (Indexed 0 to n..)
# output: term-index.txt indexed terms according to index in vocab files

import sys

vocab_list = []


# extract vocabulary from file
def grab_vocabulary(vocab):
    with open(vocab, 'r') as vocab_fo:
        global vocab_list
        vocab_list = [word.strip() for word in vocab_fo]


# begin indexing process
def start_indexing(raw, target):
    with open(raw, 'r') as raw_fo, open(target, 'w') as target_fo:
        for line in raw_fo:
            wordlist = line.split()
            indexes = [vocab_list.index(word) for word in wordlist]
            indexed_wordlist = " ".join(map(str, indexes))
            target_fo.write("{}\n".format(indexed_wordlist))


# call this function from main module
def index_output_documents(vocab_filename, raw_filename, target_filename):
    print "indexing: {} {} => {}".format(vocab_filename, raw_filename, target_filename)
    grab_vocabulary(vocab_filename)
    start_indexing(raw_filename, target_filename)


if __name__ == "__main__":
    fn_vocab = sys.argv[1]  # filename must be vocab-[entity/non-entity][.txt]
    fn_docs = sys.argv[2]  # filename must be output-[entity/non-entity][.txt]
    fn_target = "term-index-"+fn_vocab[6:]
    index_output_documents(fn_vocab, fn_docs, fn_target)