# module to filter out articles that contain positive no of entities as recognized by Polyglot NER library

import os
import sys
import document_clean
from polyglot.text import Text


# copy lines from original file, delete original file and rename updated file
# user probably needs permission to write in target_path if provided?
def transfer_legit_articles(orig_fname, target_path):
    orig_path = target_path + orig_fname
    updated_path = target_path + orig_fname + ".updated"

    with open(orig_path, 'r') as f_init, open(updated_path, 'w') as f_updated:
        for line_idx, doc in enumerate(f_init):
            original_doc = doc
            doc = document_clean.repl_unusable_chars(doc)
            doc = document_clean.repl_char_nums_en(doc)
            doc_text = Text(doc, hint_language_code='hi')
            try:
                current_entities = doc_text.entities
                if len(current_entities) > 0:
                    f_updated.write("{0}".format(original_doc))
                else:
                    print "polyglot-ner did not find entities: {}, line {}".format(orig_fname, line_idx + 1)
            except ValueError:
                print "polyglot-ner failed: {}, line {}".format(orig_fname, line_idx+1)

    # to overwrite old file, need to trigger by some user-given argument
    # os.remove(orig_path)
    # os.rename(updated_path, orig_path)


# start filtering legitimate articles into updated file
def filter_start():
    src_name = sys.argv[1]
    target_path = "./"
    dir_contents = []
    if os.path.isdir(src_name):
        dir_contents = os.listdir(src_name)
        target_path = src_name+"/"
    elif os.path.isfile(src_name):
        dir_contents.append(src_name)
    else:
        print "neither file nor directory, check path name: {}".format(src_name)

    for dataset_file in dir_contents:
        transfer_legit_articles(dataset_file, target_path)


filter_start()
