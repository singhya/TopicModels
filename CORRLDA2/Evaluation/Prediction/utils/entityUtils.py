import re
import sys
from polyglot.text import Text

sys.path.insert(0, '/home/akarmakar/projects/ectm-project/my-topic-models-project/DataPreprocessing')
import document_clean

coll_stop_words = []
fn_swl = '../../../DataPreprocessing/utils/updated-stop-words.txt'


# retrieve list of stop words
def extract_stop_words():
    global coll_stop_words
    with open(fn_swl, 'r') as swl_file:
        coll_stop_words = [word.rstrip('\n') for word in swl_file.read().splitlines()]


# remove stop words from document
def filter_stop_words(doc):
    doc_terms = doc.split()
    return " ".join([item for item in doc_terms if item not in coll_stop_words])


def get_entities(doc):
    try:
        current_entity_list = doc.entities
        return current_entity_list
    except ValueError:
        print "error: could not find entities for document\n{}".format(doc)
        sys.exit(0)


def process_non_entities(processed):
    processed = processed.replace(u'\u0964'.encode('utf-8'), ' ')  # remove Devanagari danda
    processed = processed.replace(u'\u0965'.encode('utf-8'), ' ')  # remove Devanagari double danda
    cleaned_str = re.sub(r'[*?,|;]', r'', processed)  # remove asterisks and remaining punctuations marks
    cleaned_str_wo_sw = filter_stop_words(cleaned_str)  # remove stop words from non-entity list
    return cleaned_str_wo_sw.split()


def hide_entities(ent_list, txt):
    cleaned = txt
    for token in set(ent_list):
        cleaned = re.sub(re.escape(token), "*", cleaned)
    return cleaned


def process_entities(document):
    entity_list = []
    entities_found = get_entities(document)
    for entity in entities_found:
        entity_terms = [elem.encode('utf-8') for elem in entity if elem not in [u'?', u'\u0964']]
        entity_str = "-".join(entity_terms)
        entity_list.append(entity_str) if entity_str is not "" else None
    return entity_list


def process_article(line):
    extract_stop_words()
    doc = document_clean.repl_unusable_chars(line)
    doc2 = document_clean.repl_char_nums_en(doc)
    article_str = " ".join(doc2.split())
    article_txt = Text(article_str, hint_language_code='hi')
    curr_article_ents = process_entities(article_txt)
    terms = [term.encode('utf-8') for term in article_txt.split()]
    curr_article_str = hide_entities(curr_article_ents, " ".join(terms))
    curr_article_non_ents = process_non_entities(curr_article_str)
    return curr_article_ents, curr_article_non_ents
