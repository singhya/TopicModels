#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 01:10:59 2017

@author: Jyoti
"""

import sys
import CorpusReader
import random
import numpy as np
import TopicUtils

ITERATIONS = 1000
BURN_IN = 100
THIN_INTERVAL = 20
SAMPLE_LAG = 10


class Corrlda2GibbsSample(object):
    def __init__(self, wordDoc, entityDoc):
        self.documentWords = wordDoc
        self.documentEntities = entityDoc
        self.W = len(wordDoc["vocab"])
        self.E = len(entityDoc["vocab"])
        self.M  = len(wordDoc["doc"])
    
    def initialize(self, KW, KE):
        self.zw = [[]] * self.M
        self.ze = [[]] * self.M
        self.x = [[]] * self.M
        self.cwt = np.zeros((self.W, KW))
        self.cet = np.zeros((self.E, KE))
        self.ctd = np.zeros((self.M, KW))
        self.ctt = np.zeros((KW, KE))
        self.sumcwt = np.zeros(KW)
        self.sumcet = np.zeros(KE)
        self.sumctd = np.zeros(self.M)
        self.sumctt = np.zeros(KW)
        
        for m, doc in enumerate(self.documentWords["doc"]):
            N = len(doc)
            Nw = len(doc)
            self.zw[m] = [0] * N
            for n, word in enumerate(doc):
                topic = random.randint(0, KW - 1)
                self.zw[m][n] = topic;
                self.cwt[word][topic] = self.cwt[word][topic] + 1
                self.ctd[m][topic] += 1
                self.sumcwt[topic] += 1
                self.ctd[m][topic] += 1
    
        for m, doc in enumerate(self.documentEntities["doc"]):
            N = len(doc)
            self.ze[m] = [0] * N
            self.x[m] = [0] * N
            for n, word in enumerate(doc):
             
                topic = random.randint(0, KE - 1)
                self.ze[m][n] = topic
                self.cet[self.documentEntities["doc"][m][n]][topic] += 1
                super_topic = random.randint(0, KW - 1)
                self.x[m][n] = super_topic
                self.ctt[super_topic][topic] += 1
                self.sumctt[super_topic] += 1
                self.sumcet[topic] += 1
                self.sumctd[m] =
        self.numstats = 0
    
    def sampleWFullConditional(self, m, n, KW, KE, alpha, betaW, betaE, gamma):
        
        topic = self.zw[m][n]
        self.cwt[self.documentWords["doc"][m][n]][topic] -= 1
        self.ctd[m][topic] -= 1
        self.sumcwt[topic] -= 1
        self.sumctd[m] -= 1
        p = np.zeros(KW)
        
        for k in range(KW):
            p[k] = (self.cwt[self.documentWords["doc"][m][n]][k] + betaW) / (self.sumcwt[k] + self.W * betaW) * (self.ctd[m][k] + alpha) / (self.sumctd[m] + KW * alpha)
        
        for i in range(1, KE):
            p[i] += p[i - 1]
        
        u = random.uniform(0, p[KW - 1])
        topic = 0
        for t, prob in enumerate(p):
            if (u < prob):
                topic = t
                break
    
        self.cwt[self.documentWords["doc"][m][n]][topic] += 1
        self.ctd[m][topic] += 1
        self.sumcwt[topic] += 1
        self.sumctd[m] += 1
    return topic
    
    def sampleEFullConditional(self, m, n, KW, KE, alpha, betaW, betaE, gamma):
        topic = self.ze[m][n]
        self.cet[self.documentEntities["doc"][m][n]][topic] -= 1
        self.sumcet[topic] -= 1
        
        super_topic = self.x[m][n]
        self.ctt[super_topic][topic] -= 1
        self.sumctt[super_topic] -= 1
        
        p = np.zeros((KE, KW))
        W = len(self.documentWords["vocab"])
        for xk in range(0, KE):
            for zk in range(0, KW):
                p[xk][zk] = (self.cwt[self.documentEntities["doc"][m][n]][zk] + betaE) / (self.sumcet[zk] + E * betaE) * (self.ctd[m][xk]) / (
                                                                                                                                               len(self.documentWords["doc"][m]) + KE) * (self.ctt[xk][zk] + gamma) / (self.sumctt[xk] + KE * gamma);
    
    
        cump = 0
        for xk in range(0, KW):
            for zk in range(0, KE):
                p[xk][zk] += cump
                cump = p[xk][zk]
        
        u = random.uniform(0, p[KW - 1][KE - 1])
        breakflag = False
        for xk in range(0, KW):
            for zk in range(0, KE):
                if (u < p[xk][zk]):
                    super_topic = xk
                    topic = zk
                    breakflag = True
                    break
            if breakflag:
                break

        self.cet[self.documentEntities["doc"][m][n]][topic] += 1
        self.sumcet[topic] += 1;
        self.ctt[super_topic][topic] += 1
        self.sumctt[super_topic] += 1
        return super_topic, topic
    
    def updateParams(self,KW, KE, alpha, betaW, betaE, gamma):
        for m, doc in enumerate(self.ctd):
            for k, count in enumerate(doc):
                self.thetasum[m][k] += (self.ctd[m][k] + alpha) / (self.sumctd[m] + KW * alpha)
    
        for r in range(KW):
            for c in range(self.W):
                self.phiwsum[r][c] += (self.cwt[c][r] + betaW) / (self.sumcwt[r] + self.W * betaW);

        for r in range(KE):
            for c in range(self.E):
                self.phiesum[r][c] += (self.cet[c][r] + betaE) / (self.sumcet[r] + self.E * betaE);
        
        for supertopic in range(KW):
            for topic in range(KE):
                self.psisum[supertopic][topic] += (self.ctt[supertopic][topic] + gamma) / (self.sumctt[supertopic] + KE * gamma);
        self.numstats += 1;
    
    def gibbs(self,KW, KE, alpha, betaW, betaE, gamma):
        if (SAMPLE_LAG > 0):
            self.thetasum = np.zeros((self.M, KW))
            self.phiwsum = np.zeros((KW, self.W))
            self.phiesum = np.zeros((KE, self.E))
            self.psisum = np.zeros((KW, KE))
            self.numstats = 0
        
        self.initialize(KW, KE)
        dispcol = 0
        for i in range(ITERATIONS):
            for m, doc in enumerate(self.zw):
                for n, topic in enumerate(doc):
                    topic = self.sampleWFullConditional(m, n, KW, KE, alpha, betaW,
                                                                     betaE, gamma)
                    self.zw[m][n] = topic
                for n, topic in enumerate(self.ze[m]):
                    super_topic, topic = self.sampleEFullConditional(m, n, KW, KE, alpha, betaW,
                                                                     betaE, gamma)
                    self.x[m][n] = super_topic
                    self.ze[m][n] = topic
                print "Iteration : "+str(i)+", doc : "+str(m)+", word : "+str(n)
            if ((i < BURN_IN) and (i % THIN_INTERVAL == 0)):
                print("B")
                dispcol += 1
            
            if ((i > BURN_IN) and (i % THIN_INTERVAL == 0)):
                print("S")
                dispcol += 1
            
            if ((i > BURN_IN) and (SAMPLE_LAG > 0) and (i % SAMPLE_LAG == 0)):
                self.updateParams(KW, KE, alpha, betaW, betaE, gamma)
                if (i % THIN_INTERVAL != 0):
                    dispcol += 1
        
            if (dispcol >= 100):
                print("New Line")
                dispcol = 0

    def getTheta(self,KW, KE, alpha):
        theta = np.zeros((self.M, KE))
        
        if (SAMPLE_LAG > 0):
            for m, doc in enumerate(self.documentEntities):
                for k in range(KE):
                    theta[m][k] = self.thetasum[m][k] / self.numstats;
        else:
            for m, doc in enumerate(self.documentEntities):
                for k in range(KE):
                    theta[m][k] = (self.ctd[m][k] + alpha) / (self.sumctd[m] + KE * alpha);
        return theta

    def getPhiW(self, KW, betaW):
        phiw = np.zeros((KW, self.W))
        if (SAMPLE_LAG > 0):
            for k in range(KW):
                for w in range(self.W):
                    phiw[k][w] = self.phiwsum[k][w] / self.numstats;
        else:
            for k in range(KW):
                for w in range(self.W):
                    phiw[k][w] = (self.cwt[w][k] + betaW) / (self.sumcwt[k] + self.W * betaW);
        return phiw;

    def getPsi(self, KE, KW, gamma):
        psi = np.zeros((KE, KW))
        if (SAMPLE_LAG > 0):
            for super_topic in range(KE):
                for topic in range(KW):
                    psi[super_topic][topic] = self.psisum[super_topic][topic] / self.numstats;
        else:
            for super_topic in range(KE):
                for topic in range(KW):
                    psi[super_topic][topic] = (self.ctt[super_topic][topic] + gamma) / (self.sumctt[super_topic] + KW * gamma);
        return psi

    def getPhiE(self, KE, betaE):
        phie = np.zeros((KE, self.E));
        if (SAMPLE_LAG > 0):
            for k in range(KE):
                for e in range(self.E):
                    phie[k][e] = self.phiesum[k][e] / self.numstats;
        else:
            for k in range(KE):
                for e in range(self.E):
                    phie[k][e] = (self.cet[e][k] + betaE) / (self.sumcet[k] + self.E * betaE);
        return phie;

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
    
    gibb_sample = Corrlda2GibbsSample(wordDoc, entityDoc)
    gibb_sample.gibbs(KW, KE, alpha, betaW, betaE, gamma)
    theta = gibb_sample.getTheta(KW, KE, alpha);
    phiw = gibb_sample.getPhiW(KW, betaW);
    phie = gibb_sample.getPhiE(KE, betaE);
    psi = gibb_sample.getPsi(KE, KW, gamma);
    
    TopicUtils.saveCSV(theta, "./CorrLDA2_theta");
    TopicUtils.saveCSV(phiw, "./CorrLDA2_phiw");
    TopicUtils.saveCSV(phie, "./CorrLDA2_phie");
    TopicUtils.saveCSV(psi, "./CorrLDA2_psi");
    TopicUtils.saveCSV(gibb_sample.cwt, "./CorrLDA2_cwt");
    TopicUtils.saveCSV(gibb_sample.cet, "./CorrLDA2_cet");
    TopicUtils.saveCSV(gibb_sample.ctt, "./CorrLDA2_ctt");
    TopicUtils.saveTopTopicWords(phiw, wordDoc["vocab"], "./CorrLDA2_top-topic-words", 10);
    TopicUtils.saveTopTopicWords(phie, entityDoc["vocab"], "./CorrLDA2_top-topic-entities", 10);
    TopicUtils.saveTopTopicsOfSupertopics(psi, "./CorrLDA2_top-Supertopic-topics", 5);


main()
