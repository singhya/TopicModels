import pdb
import sys
import operator
import numpy as np

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

def forAllWords(phiw, psi, word_idx, et_idx):
    p_w = 1.0
    for w in word_idx:
        p_w_wt = sum(phiw[:, word_idx[w]] * psi[et_idx, :])
        p_w *= p_w_wt
    return p_w


# ranking all entities in vocab according to P(e|d)
def rank_entities(doc_new, phie, phiw, psi, doc_id):
    p_e_dn = {}
    word_idx = {}
    for w_idx, w in enumerate(vocab_non_ents):
        if w in doc_new:
            word_idx[w.decode('utf-8')] = w_idx
    print "For document " + str(doc_id)
    # calculating probability of each entity given new document
    p_w = np.zeros(len(phie))
    for et_idx, et in enumerate(phie):
        p_w[et_idx] = forAllWords(phiw, psi, word_idx, et_idx)

    for e_idx, e in enumerate(vocab_ents):
        #print "For document "+str(doc_id)+", processed " + str(e_idx) + " of " + str(len(vocab_ents)) + " entities"
        p_e_dn[e] = sum(phie[:,e_idx] * p_w[:])

    return p_e_dn


def main():
    global vocab_non_ents, vocab_ents
    fn_phie = "../../../ECTM/Results/Dataset 2/25/ECTM_phie"
    fn_phiw = "../../../ECTM/Results/Dataset 2/25/ECTM_phiw"
    fn_psi = "../../../ECTM/Results/Dataset 2/25/ECTM_psi"
    fn_vocab_e = "../../../DataPreprocessing/processedData/ectm/v2/vocab-entity"
    fn_vocab_w = "../../../DataPreprocessing/processedData/ectm/v2/vocab-non-entity"
    test_fn = "test-v2/op-word.txt"
    test_fe = "test-v2/op-ents.txt"
    # test_fn = "../../../DataPreprocessing/processedData/ectm/v2/output-non-entity"
    # test_fe = "../../../DataPreprocessing/processedData/ectm/v2/output-entity"

    # read test doc
    test_data = []
    with open(test_fn, "r") as test_fo:
        test_data = test_fo.readlines()
    test_e = []
    with open(test_fe, "r") as test_fo:
        test_e = test_fo.readlines()

    vocab_ents = grab_vocabulary(fn_vocab_e)
    vocab_non_ents = grab_vocabulary(fn_vocab_w)
    phie = []
    phiw = []
    psi = []
    phie = grab_matrix(fn_phie)
    phie = np.array(phie)
    phiw = grab_matrix(fn_phiw)
    phiw = np.array(phiw)
    psi = grab_matrix(fn_psi)
    psi = np.array(psi)
    output = ""
    best_sum = 0
    median_sum = 0
    count = 0
    for idx,test_doc_line in enumerate(test_data):
        test_doc = test_doc_line.strip().split()

        ent_giv_doc_scores = rank_entities(test_doc, phie, phiw, psi,idx)
        entities = []
        for key in ent_giv_doc_scores:
            entities.append((key, ent_giv_doc_scores[key]))
        entities.sort(key=operator.itemgetter(1), reverse=True)
        # printing top 20 entities
        #ranked_ents = dict(sorted(ent_giv_doc_scores.items(), key=operator.itemgetter(1), reverse=True)[:], \)
        actual_ent = set(test_e[idx].split())
        result = []
        np_res = []
        ent = ""
        for i,item in enumerate(entities):
            if(item[0] in actual_ent):
                result.append(i+1)
                np_res = np.array(result)
            if(i<20):
                ent+=str(item[0])+" "
        print result
        if(len(result)>0 and result[0]<100):
            median_sum+=np.median(np_res)
            best_sum+=result[0]
            count+=1
            f = open("ECTMWordv1.txt", "a")
            f.write(str(test_data[idx]))
            f.close()
            f = open("ECTMEntityv1.txt", "a")
            f.write(test_e[idx])
            f.close()

        f = open("ECTMPredictionsWordsv1.txt", "a")
        f.write(ent + "\n")
        f.close()
        f = open("ECTMPredictionsResultsv1.txt", "a")
        f.write(str(result)+"\n")
        f.close()
    print "Avg best sum : "+str((best_sum*1.0)/count)
    print "Avg median sum : "+str((median_sum*1.0)/count)
    print count
main()
