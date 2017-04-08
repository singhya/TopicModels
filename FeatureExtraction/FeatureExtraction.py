import numpy as np
with open('ECTMRawData/ECTM_theta') as f:
    vect = [line.rstrip() for line in f]
vect = np.array([x.split() for x in vect])
vect = vect.astype(np.float)
with open('ECTMRawData/ECTM_psi') as f:
    relation = [line.rstrip() for line in f]
relation = np.array([x.split() for x in relation])
relation = relation.astype(np.float)
feature_vec = []
for vec in vect:
    word_vec = np.matmul(vec, relation)
    feature_vec.append(np.concatenate((vec, word_vec), axis=0))
    #for i in range(relation.shape[1]):
    #    word_vec = vec * relation[:,i]
    #    feature_vec.append(np.concatenate((vec, word_vec), axis=0))
np.savetxt('svm.in', feature_vec, delimiter=',')