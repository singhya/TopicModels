import pdb
import sys
import operator

num_topics = 10
vocab_ents = []
vocab_non_ents = []
phie = []
phiw = []
psi = []
ranked_entity_matrix = []


# read matrix from file
def grab_matrix(fn, prob_matrix):
    with open(fn, "r") as fo:
        rows = fo.readlines()
        for line in rows:
            prob_matrix.append(map(float, line.strip().split()))


# extract vocabulary from file
def grab_vocabulary(vocab):
    with open(vocab, 'r') as vocab_fo:
        vocab_list = [word.strip() for word in vocab_fo]
    return vocab_list


# ranking all entities in vocab according to P(e|d)
def rank_entities(doc_new):
    p_e_dn = {}
    p_wt_dn = []

    # calculating probability of word topic given new document
    for wt_idx, wt in enumerate(phiw):
        topic_assn = 1.0
        for word in doc_new:
            try:
                word_idx = vocab_non_ents.index(word)
                topic_assn *= phiw[wt_idx][word_idx]
            except ValueError:
                pass
        p_wt_dn.append(topic_assn)

    # calculating probability of each entity given new document
    for ent_idx, ent in enumerate(vocab_ents):
        p_e_dn[ent] = 0.0
        p_e_wt = 0.0
        for wt_idx, wt in enumerate(phiw):
            # calculating probability of entity given word topic
            for et_idx, et in enumerate(phie):
                p_e_wt += phie[et_idx][ent_idx] * psi[wt_idx][et_idx]
            # updating probability of entity given new document
            p_e_dn[ent] += p_e_wt * p_wt_dn[wt_idx]
    return p_e_dn


def main():
    global vocab_non_ents, vocab_ents

    try:
        test_fn = sys.argv[1]
        fn_vocab_e = sys.argv[2]
        fn_vocab_w = sys.argv[3]
        fn_phie = sys.argv[4]
        fn_phiw = sys.argv[5]
        fn_psi = sys.argv[6]
    except IndexError:
        print "Cmd usage: python ectm_entity_predict.py <TEST-DOCUMENT> <ENTITY-VOCAB> <NON-ENTITY-VOCAB> <PHIE> <PHIW> <PSI>"
        sys.exit(0)

    # read test doc
    with open(test_fn, "r") as test_fo:
        test_doc = next(test_fo).strip().split()

    vocab_ents = grab_vocabulary(fn_vocab_e)
    vocab_non_ents = grab_vocabulary(fn_vocab_w)
    grab_matrix(fn_phie, phie)
    grab_matrix(fn_phiw, phiw)
    grab_matrix(fn_psi, psi)
    ent_giv_doc_scores = rank_entities(test_doc)

    # printing top 20 entities
    ranked_ents = dict(sorted(ent_giv_doc_scores.items(), key=operator.itemgetter(1), reverse=True)[:20])
    for item in ranked_ents.keys():
        print item,

main()
