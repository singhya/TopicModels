# pre-process.py - (author:Abhi Karmakar)
# input: 
#   dataset with one article/document per line;
#   number of lines to process
# output: 
#   entity-vocab.txt - list of all entities found in dataset;
#   non-entity-vocab.txt - list of all non-entities found in dataset;
#   output-entity.txt - list of entities per document per line;
#   output-non-entity - list of non-entities per document per line


import sys
import re
from polyglot.text import Text


# command-line arguments
fn_dataset = sys.argv[1]
num_lines = int(sys.argv[2])

# output filenames: all vars prefixed by fn: file name
fn_ne_vocab = 'entity-vocab.txt'
fn_nne_vocab = 'non-entity-vocab.txt'
fn_index_ne = 'entity-index.txt'
fn_index_nne = 'non-entity-index.txt'
fn_op_ne = 'output-entity.txt'
fn_op_nne = 'output-non-entity.txt'
fn_swl = 'hindi-stop-words.txt'

# global lists for named entities and non-named entities(regular words that are not named entities)
l_entity = []
l_non_entity = []

# list of stop words from file
l_stop_words = []


# retrieve list of stop words
def extract_stop_words():
    global l_stop_words
    with open(fn_swl, 'r') as swl_file:
        l_stop_words = [word.rstrip('\n') for word in swl_file.read().splitlines()]


# remove stop words from document
def filter_stop_words(doc):
    doc_terms = doc.split()
    return " ".join([item for item in doc_terms if item not in l_stop_words])


# write lists to vocab files
def output_list(target_file, target_list):
    with open(target_file, 'w') as named_file:
        for num, elem in enumerate(target_list):
            named_file.write("{} {}\n".format(num, elem))


# replace all English characters and numerals using regex
def replace_english_chars_nums(txt):
    return re.sub(r'[a-zA-Z0-9]', r'', txt)


# used to update vocabulary list
def store_set(my_list, my_new_term):
    if my_new_term not in my_list:
        my_list.append(my_new_term)


# returns entities for the document
def get_entities(doc, line_idx):
    # use this to find which lines have zero entities
    #   fo_filename = "zero-entity-list.txt"
    #   fo_mode = ("w", "a")[line_idx > 0]
    #   fo = open(fo_filename, fo_mode)
    #   if len(current_entity_list) == 0:
    #       fo.write("{0} ".format(line_idx))
    #   fo.close()
    current_entity_list = doc.entities
    return current_entity_list


# finds entities per article and replaces them with asterisk
# returns modified article string, current article entity list
def process_article(article, line_num):
    current_article_nel = []
    terms = [term.encode('utf-8') for term in article.split()]
    list_ents = get_entities(article, line_num)
    for entity in list_ents:
        entity_terms = [elem.encode('utf-8') for elem in entity]
        entire_entity = " ".join(entity_terms)
        current_article_nel.append(entire_entity)

    this_article = " ".join(terms)
    for token in set(current_article_nel):
        rule = re.compile(token)
        this_article = rule.sub("*", this_article)

    return this_article, current_article_nel


# process each document up to given number of lines
def process_lines():
    with open(fn_dataset, 'r') as all_docs:
        file_line_index = 0
        for line in all_docs:
            # replacing all punctuation before processing
            line = line.replace('.', ' ')
            line = line.decode('utf-8').replace(u'\u2018', '').encode('utf-8')  # for quotation mark
            line = line.decode('utf-8').replace(u'\u2019', '').encode('utf-8')  # for quotation mark
            line = line.replace('!', '')
            line = line.replace('-', '')
            line = line.replace('&', '')
            line = line.replace(':', '')
            line = line.replace('\'', '')
            line = line.replace('\"', '')
            line = line.replace(')', '')
            line = line.replace('(', '')
            line = line.replace('\\', '')
            line = line.replace('/', '')
            line = replace_english_chars_nums(line)

            sentence = Text(line, hint_language_code='hi')
            processed_str, this_entity_list = process_article(sentence, file_line_index)
            processed_str = processed_str.decode('utf-8').replace(u'\u0964', '').encode('utf-8')  # for devanagari full stop (danda)
            cleaned_str = re.sub(r'[*?,]', r'', processed_str)
            cleaned_str_wo_sw = filter_stop_words(cleaned_str)
            curr_non_ent_list = cleaned_str_wo_sw.split()

            curr_ent_list = []
            for elem in this_entity_list:
                dashed_entity_term = '-'.join(elem.split())
                curr_ent_list.append(dashed_entity_term)
                store_set(l_entity, dashed_entity_term)

            for elem in curr_non_ent_list:
                store_set(l_non_entity, elem)

            # writing entities and non-entities per line to respective output file
            fo_mode = ("w", "a")[file_line_index > 0]
            with open(fn_op_ne, fo_mode) as ne_file, open(fn_op_nne, fo_mode) as nne_file:
                ne_file.write("{} {}\n".format(file_line_index, " ".join(curr_ent_list)))
                nne_file.write("{} {}\n".format(file_line_index, " ".join(curr_non_ent_list)))

            file_line_index += 1
            if file_line_index == num_lines and num_lines != 0:
                break

            # to wait after each line
            # check_continue = raw_input("next sentence > ")
            # if check_continue in ['n', 'N']:
            #     break


# program starts here
extract_stop_words()
process_lines()
output_list(fn_ne_vocab, l_entity)  # writes named entity vocabulary list l_entity
output_list(fn_nne_vocab, l_non_entity)     # writes non-named entity vocabulary list l_non_entity

# THIS SNIPPET IS FOR INDEXING - NEEDS TO BE UPDATED
# with open(data_file, 'r') as sentence_file, open(ne_dict_file, 'r') as ner_file, open(nc_file, 'w') as encoded_file:
#     ner_content = [entity.strip() for entity in ner_file.readlines()]
#     for line in sentence_file:
#         ner_encoded = []
#         words = line.split()
#         for current_word in words:
#             if current_word in list_of_entities:
#                 for idx, token in enumerate(ner_content):
#                     if token == current_word:
#                         ner_encoded.append(str(idx))
#
#         encoded_line = " ".join(ner_encoded)
#         encoded_file.write("{}\n".format(encoded_line))

