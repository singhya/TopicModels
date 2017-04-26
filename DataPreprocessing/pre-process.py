# pre-process.py - (author: Abhi Karmakar)
#
# input: 
#   dataset with one article/document per line;
#   number of lines to process
#
# output:
#   vocab-entity - list of all entities found in dataset;
#   vocab-non-entity - list of all non-entities found in dataset;
#   output-entity - list of entities per document per line;
#   output-non-entity - list of non-entities per document per line
#   term-index-entity - entities per document substituted by index in vocabulary
#   term-index-non-entity - entities per document substituted by index in vocabulary
#
# output files only include documents that contain at least one non-named-entity occuring above the low frequency threshold
# documents with zero named entities have been filtered out by filter-legit-articles.py module
# indexing is performed after final output files are generated, and sorted vocabulary files are written out

import sys
import re
import os
import document_clean
import indexing
from polyglot.text import Text

# output filenames: all vars prefixed by fn: file name
fn_class_labels = "category-labels"
fn_class_key = "category-key"
fn_ne_vocab = 'vocab-entity'
fn_nne_vocab = 'vocab-non-entity'
fn_op_ne = 'output-entity'
fn_op_nne = 'output-non-entity'
fn_swl = 'updated-stop-words.txt'

# global lists for named entities and non-named entities(regular words that are not named entities)
coll_stop_words = []    # list of stop words from file
coll_doc_labels = []
coll_entity = []
coll_non_entity = []
d_entity_vocab = {}
d_non_entity_vocab = {}
d_doc_entity_tokens = {}
d_doc_non_entity_tokens = {}


# retrieve list of stop words
def extract_stop_words():
    global coll_stop_words
    with open(fn_swl, 'r') as swl_file:
        coll_stop_words = [word.rstrip('\n') for word in swl_file.read().splitlines()]


# remove stop words from document
def filter_stop_words(doc):
    doc_terms = doc.split()
    return " ".join([item for item in doc_terms if item not in coll_stop_words])


# write lists to vocab files
def write_vocab_file(target_file, token_list):
    with open(target_file, 'w') as named_file:
        for elem in token_list:
            named_file.write("{}\n".format(elem))


# returns entities for the document
def get_entities(doc, line_idx):
    try:
        current_entity_list = doc.entities
        return current_entity_list
    except ValueError:
        print str(line_idx)


# filter infrequently occuring non-named-entities from vocabulary and per-document-tokens
# write out label for each document avoiding discarded indexes
def begin_output_generation():
    low_freq_threshold = 1
    discarded_idx = []
    with open(fn_op_nne, "w") as fo, open(fn_class_labels, "w") as fo_label:
        for line_idx, token_list in d_doc_non_entity_tokens.items():
            valid_doc_non_entities = []
            for token in token_list:
                unusable_beginning = document_clean.starts_with_matra(token)
                if not unusable_beginning and d_non_entity_vocab[token] > low_freq_threshold:
                    valid_doc_non_entities.append(token)
                    coll_non_entity.append(token)
            if len(valid_doc_non_entities) == 0:
                discarded_idx.append(line_idx)
            else:
                fo_label.write("{}\n".format(coll_doc_labels[line_idx]))
                fo.write("{}\n".format(" ".join(valid_doc_non_entities)))
    write_output_entity(discarded_idx)


# write entities to output file avoiding invalid line index
def write_output_entity(invalid_ids):
    with open(fn_op_ne, "w") as fo:
        for idx, token_list in d_doc_entity_tokens.items():
            if idx not in invalid_ids:
                coll_entity.extend(token_list)
                fo.write("{}\n".format(" ".join(token_list)))


def process_non_entities(processed, idx):
    # processed = processed.decode('utf-8').replace(u'\u0964', ' ').encode('utf-8')  # remove Devanagari danda
    processed = processed.replace(u'\u0964'.encode('utf-8'), ' ')  # remove Devanagari danda
    processed = processed.replace(u'\u0965'.encode('utf-8'), ' ')  # remove Devanagari double danda
    cleaned_str = re.sub(r'[*?,|;]', r'', processed)  # remove asterisks and remaining punctuations marks
    cleaned_str_wo_sw = filter_stop_words(cleaned_str)  # remove stop words from non-entity list
    curr_non_ent_list = cleaned_str_wo_sw.split()
    for elem in curr_non_ent_list:
        d_non_entity_vocab[elem] = d_non_entity_vocab.setdefault(elem, 0) + 1
    d_doc_non_entity_tokens[idx] = curr_non_ent_list


# store entity list per document and term occurence
def process_entities(entities_found, idx):
    curr_doc_entities = []
    for elem in entities_found:
        term = '-'.join(elem.split())
        curr_doc_entities.append(term)
        d_entity_vocab[term] = d_entity_vocab.setdefault(term, 0) + 1
    d_doc_entity_tokens[idx] = curr_doc_entities


# finds entities per article and replaces them with asterisk
# returns modified article string, current article entity list
def process_article(article, line_num):
    curr_article_ents = []
    terms = [term.encode('utf-8') for term in article.split()]
    curr_article_str = " ".join(terms)
    list_ents = get_entities(article, line_num)
    for entity in list_ents:
        entity_terms = [elem.encode('utf-8') for elem in entity if elem not in [u'?', u'\u0964']]
        entity_str = " ".join(entity_terms)
        curr_article_ents.append(entity_str) if entity_str is not "" else None
    for token in set(curr_article_ents):
        # needed to escape metacharacters in token, or else re.sub fails
        curr_article_str = re.sub(re.escape(token), "*", curr_article_str)
    process_non_entities(curr_article_str, line_num)
    process_entities(curr_article_ents, line_num)


# process each document (optional: up to given number of lines)
def process_documents():
    src_str = sys.argv[1]
    try:
        num_lines = int(sys.argv[2])
    except IndexError:
        num_lines = 0

    # handle if argument is directory or file
    dir_contents = []
    if os.path.isdir(src_str):
        dir_contents = [src_str+"/"+fname for fname in sorted(os.listdir(src_str))]
    elif os.path.isfile(src_str):
        dir_contents.append(src_str)

    # iterate through each file in directory contents (just 1 file if isfile(argv[1]))
    master_idx = 0  # outside all loops to maintain master index of final articles
    for label, fn_dataset in enumerate(dir_contents):
        cls_key_fo_mode = ("w", "a")[label > 0]
        with open(fn_dataset, "r") as all_docs, open(fn_class_key, cls_key_fo_mode) as cls_key_fo:
            print "{} => {}".format(fn_dataset, label)
            cls_key_fo.write("{} => {}\n".format(fn_dataset, label))
            for file_idx, line in enumerate(all_docs):
                if (file_idx+1) % 100 == 0:
                    print "processing line {}".format(file_idx+1)
                doc = document_clean.repl_unusable_chars(line)
                doc = document_clean.repl_char_nums_en(doc)
                doc_contents = " ".join(doc.split())
                article = Text(doc_contents, hint_language_code='hi')
                process_article(article, master_idx)
                coll_doc_labels.append(label)
                master_idx += 1
                if master_idx == num_lines and num_lines:
                    break


# program starts here
if __name__ == "__main__":
    extract_stop_words()
    process_documents()
    begin_output_generation()
    write_vocab_file(fn_ne_vocab, sorted(set(coll_entity)))  # writes named entity vocabulary list l_entity
    write_vocab_file(fn_nne_vocab, sorted(set(coll_non_entity)))  # writes non-named entity vocabulary list l_non_entity
    indexing.index_output_documents(fn_ne_vocab, fn_op_ne, "term-index-entity")
    indexing.index_output_documents(fn_nne_vocab, fn_op_nne, "term-index-non-entity")
