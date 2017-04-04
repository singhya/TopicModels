import sys
import CorpusReader
import random
import numpy as np

ITERATIONS = 1000
BURN_IN = 100
THIN_INTERVAL = 20
SAMPLE_LAG = 10
#thetasum
#phisum
#phisum
#psisum
#numstats

def initialize(wordDoc, entityDoc, KW, KE):
    M = len(wordDoc["doc"])
    E = len(entityDoc["vocab"])
    W = len(wordDoc["vocab"])
    zw = [[]]*M
    ze = [[]]*M
    x = [[]]*M
    cwt = np.zeros((W, KW))
    cet = np.zeros((E, KE))
    ctd = np.zeros((M, KE))
    ctt = np.zeros((KE, KW))
    sumcwt = np.zeros(KW)
    sumcet = np.zeros(KE)
    sumctd = np.zeros(M)
    sumctt = np.zeros(KE)

    for m,doc in enumerate(wordDoc["doc"]):
        N = len(doc)
        zw[m] = [0]*N
        x[m] = [0]*N
        for n, word in enumerate(doc):
            topic = random.randint(0, KW-1)
            zw[m][n] = topic;
            cwt[word][topic]=cwt[word][topic]+1
            sumcwt[topic]+=1

            super_topic = random.randint(0, KE-1)
            x[m][n] = super_topic
            ctt[super_topic][topic]+=1
            sumctt[super_topic]+=1

    for m,doc in enumerate(entityDoc["doc"]):
        N = len(doc)
        ze[m] = [0]*N
        for n, word in enumerate(doc):
            topic = random.randint(0,KE-1)
            ze[m][n] = topic
            cet[entityDoc["doc"][m][n]][topic]+=1
            ctd[m][topic]+=1
            sumcet[topic]+=1
        sumctd[m] = N


def gibbs(wordDoc, entityDoc, KW, KE, alpha, betaW, betaE, gamma):
    if(SAMPLE_LAG>0):
        thetasum = [[]]
        phisum = [[]]
        phiesum = [[]]
        psisum = [[]]
        numstats = 0
    initialize(wordDoc, entityDoc, KW, KE)


def main():
    wordFile = sys.argv[1]
    wordVocab = sys.argv[2]
    wordDoc = CorpusReader.readFiles(wordFile, wordVocab)
    entityFile = sys.argv[3]
    entityVocab = sys.argv[4]
    entityDoc = CorpusReader.readFiles(entityFile, entityVocab)
    KW = int(sys.argv[5])
    KE = int(sys.argv[6])
    alpha = float(sys.argv[7])
    betaW = float(sys.argv[8])
    betaE = float(sys.argv[9])
    gamma = float(sys.argv[10])

    gibbs(wordDoc, entityDoc, KW, KE, alpha, betaW, betaE, gamma)

main()
