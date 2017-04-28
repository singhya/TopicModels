import sys
import numpy as np
import operator
import time

num_topics = 10
vocab_ents = []
vocab_non_ents = []
ranked_entity_matrix = []


# read matrix from file
def grab_matrix(fn):
    prob_matrix = []
    with open(fn, "r") as fo:
        rows = fo.readlines()
        for line in rows:
            prob_matrix.append(map(float, line.strip().split()))
    return prob_matrix


# extract vocabulary from file
def grab_vocabulary(vocab):
        with open(vocab, 'r') as vocab_fo:
            vocab_list = [word.strip() for word in vocab_fo]
        return vocab_list


def topic_given_currdoc(phiw, word_idx):
    p_t_dn = np.zeros(len(phiw))
    for wt_idx, wt in enumerate(phiw):
        p_w = 1.0
        for word in word_idx:
            p_w *= phiw[wt_idx, word_idx[word]]
        p_t_dn[wt_idx] = p_w
    return p_t_dn


def get_doc_term_idx(doc):
    term_index = {}
    for w_idx, w in enumerate(vocab_non_ents):
        if w in doc:
            term_index[w.decode('utf-8')] = w_idx
    return term_index


# ranking all entities in vocab according to P(e|d)
def rank_entities(doc_new, phiw, e_wt):
    p_e_dn = {}
    word_idx = get_doc_term_idx(doc_new)
    p_t_dn = topic_given_currdoc(phiw, word_idx)
    for e_idx, e in enumerate(vocab_ents):
        p_e_dn[e] = sum(e_wt[:, e_idx] * p_t_dn[:])
    return p_e_dn


def entities_given_wt(phie, psi):
    p_e_tw = np.zeros(shape=(len(psi), len(phie[0,:])))
    for ent_idx, ent in enumerate(phie[0, :]):
        for wt_idx, wt in enumerate(psi[:, 0]):
            sum_over_te = sum(phie[:, ent_idx] * psi[wt_idx, :])
            p_e_tw[wt_idx, ent_idx] = sum_over_te
    return p_e_tw


def main():
    global vocab_non_ents, vocab_ents

    try:
        test_fn = sys.argv[1]
        # test_fn = "test-v2/op-word.txt"
        test_fe = sys.argv[2]
        fn_vocab_e = sys.argv[3]
        fn_vocab_w = sys.argv[4]
        fn_phie = sys.argv[5]
        fn_phiw = sys.argv[6]
        fn_psi = sys.argv[7]
    except IndexError:
        print "Cmd usage: python ectm_entity_predict.py <TEST-DOCUMENT> <ENTITY-VOCAB> <NON-ENTITY-VOCAB> <PHIE> <PHIW> <PSI>"
        sys.exit(0)

    # timer start
    start = time.time()

    # read test doc
    with open(test_fn, "r") as test_fo:
        test_data = test_fo.readlines()
    with open(test_fe, "r") as test_fo:
        test_e = test_fo.readlines()

    # grab required vocabularies and model files
    vocab_ents = grab_vocabulary(fn_vocab_e)
    vocab_non_ents = grab_vocabulary(fn_vocab_w)

    phie = grab_matrix(fn_phie)
    phie = np.array(phie)
    phiw = grab_matrix(fn_phiw)
    phiw = np.array(phiw)
    psi = grab_matrix(fn_psi)
    psi = np.array(psi)

    best_sum = 0
    median_sum = 0
    count = 0

    # compute probability p(e|tw)
    e_wt = entities_given_wt(phie, psi)

    for test_idx, test_doc_line in enumerate(test_data):
        print "processing document " + str(test_idx)
        test_doc = test_doc_line.strip().split()
        ent_giv_doc_scores = rank_entities(test_doc, phiw, e_wt)
        entities = [(key, ent_giv_doc_scores[key]) for key in ent_giv_doc_scores.keys()]
        entities.sort(key=operator.itemgetter(1), reverse=True)
        actual_ent = set(test_e[test_idx].split())
        result = []
        np_res = []
        ent = ""
        for i, item in enumerate(entities):
            if item[0] in actual_ent:
                result.append(i+1)
                np_res = np.array(result)
            if i < 20:
                ent += str(item[0])+" "
        # print result
        if len(result) > 0 and result[0] < 100:
            median_sum += np.median(np_res)
            best_sum += result[0]
            count += 1
            f = open("ECTMWordv2.txt", "a")
            f.write(str(test_data[test_idx]))
            f.close()
            f = open("ECTMEntityv2.txt", "a")
            f.write(test_e[test_idx])
            f.close()

        f = open("ECTMPredictionsWordsv2.txt", "a")
        f.write(ent + "\n")
        f.close()
        f = open("ECTMPredictionsResultsv2.txt", "a")
        f.write(str(result)+"\n")
        f.close()

    print "Avg best sum : "+str((best_sum*1.0)/count)
    print "Avg median sum : "+str((median_sum*1.0)/count)
    print count
    print "elapsed {} seconds...".format(time.time() - start)

main()
