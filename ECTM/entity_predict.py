import pdb
import sys
import operator

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


# ranking all entities in vocab according to P(e|d)
def rank_entities(doc_new, phie, phiw, psi):
    p_e_dn = {}
    word_idx = {}
    for w_idx, w in enumerate(vocab_non_ents):
        if w in doc_new:
            word_idx[w.decode('utf-8')] = w_idx
    # calculating probability of each entity given new document
    for e_idx, e in enumerate(vocab_ents):
        print "Processed " + str(e_idx) + " of " + str(len(vocab_ents)) + " entities"
        p_e_dn[e] = 0.0
        for et_idx, et in enumerate(phie):

            p_w = 1.0
            for w in word_idx:
                # calculating probability of entity given word topic
                p_w_wt = 0.0
                for wt_idx, wt in enumerate(phiw):
                    p_w_wt += phiw[wt_idx][word_idx[w]] * psi[et_idx][wt_idx]
                # updating probability of entity given new document
                p_w *= p_w_wt

            p_e_dn[e] += phie[et_idx][e_idx] * p_w

    return p_e_dn


def main():
    global vocab_non_ents, vocab_ents
    fn_phie = "Results/Dataset 2/25/ECTM_phie"
    fn_phiw = "Results/Dataset 2/25/ECTM_phiw"
    fn_psi = "Results/Dataset 2/25/ECTM_psi"
    fn_vocab_e = "../DataPreprocessing/processedData/ectm/v2/vocab-entity"
    fn_vocab_w = "../DataPreprocessing/processedData/ectm/v2/vocab-non-entity"
    test_fn = "predict-test-doc.txt"

    # read test doc
    with open(test_fn, "r") as test_fo:
        test_doc = next(test_fo).strip().split()

    vocab_ents = grab_vocabulary(fn_vocab_e)
    vocab_non_ents = grab_vocabulary(fn_vocab_w)
    phie = []
    phiw = []
    psi = []
    phie = grab_matrix(fn_phie)
    phiw = grab_matrix(fn_phiw)
    psi = grab_matrix(fn_psi)
    ent_giv_doc_scores = rank_entities(test_doc, phie, phiw, psi)

    # printing top 20 entities
    ranked_ents = dict(sorted(ent_giv_doc_scores.items(), key=operator.itemgetter(1), reverse=True)[:20])
    for item in ranked_ents.keys():
        print item,

main()
