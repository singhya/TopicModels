import numpy as np

def saveCSV(mat, fileName):
    np.savetxt(fileName, mat, delimiter=' ')

def saveTopTopicWords(phi, vocab, fileName, numWordsPerTopic):
    A = phi
    fileStream = open(fileName, 'w')
    for i in range(A.shape[0]):
        sorted_list =sorted(range(len(A[i])), key=lambda k: A[i][k])
        for j in range(numWordsPerTopic):
            fileStream.write(vocab[sorted_list[len(sorted_list) - 1 - j]]+" ");
        fileStream.write("\n");
    fileStream.close();

def saveTopTopicsOfSupertopics(psi, fileName, numTopicsPerSupertopic):
    A = psi;
    fileStream = open(fileName, 'w')
    for i in range(A.shape[0]):
        sorted_list = sorted(range(len(A[i])), key=lambda k: A[i][k])
        for j in range(numTopicsPerSupertopic):
            fileStream.write("T" +str(sorted_list[len(sorted_list) - 1 - j])+" ")
        fileStream.write("\n");
    fileStream.close();
