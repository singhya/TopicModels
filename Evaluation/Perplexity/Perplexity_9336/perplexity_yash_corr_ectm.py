import math

dir_entity_ind = "docs/term-index-entity"
dir_non_entity_ind = "docs/term-index-non-entity"


docs_entity = []
with open(dir_entity_ind) as f:
    i =0
    for line in f:
        line = line.strip()
        if ' ' in line:
            docs_entity.append(line.split(" "))
            i += 1
        else:
            temp = [line]
            docs_entity.append(temp)
            i += 1

docs_non_entity = []
with open(dir_non_entity_ind) as f:
    i =0
    for line in f:
        line = line.strip()
        if ' ' in line:
            docs_non_entity.append(line.split(" "))
            i += 1
        else:
            temp = [line]
            docs_non_entity.append(temp)
            i += 1

def prep(k,algo):
    dir_phie = "docs/" + algo + "_op/" + str(k) + "/" + algo + "_phie"
    dir_phiw = "docs/" + algo + "_op/" + str(k) + "/" + algo + "_phiw"
    dir_theta = "docs/" + algo + "_op/" + str(k) + "/" + algo + "_theta"

    phie = []
    phiw = []
    theta = []

    with open(dir_phie) as f:
        i = 0
        for line in f:
            line = line.strip()
            if ' ' in line:
                phie.append(line.split(" "))
                i += 1
            else:
                phie.append(line)
                i += 1

    with open(dir_phiw) as f:
        i = 0
        for line in f:
            line = line.strip()
            if ' ' in line:
                phiw.append(line.split(" "))
                i += 1
            else:
                phiw.append(line)
                i += 1

    with open(dir_theta) as f:
        i = 0
        for line in f:
            line = line.strip()
            if ' ' in line:
                theta.append(line.split(" "))
                i += 1
            else:
                theta.append(line)
                i += 1

    sum = 0
    for m in range(0, 10):
        if m != 9:
            sum += perplexity(m * 1000, (m + 1) * 1000,phie,phiw,theta, algo)
        else:
            sum += perplexity(9000, len(docs_entity),phie,phiw,theta, algo)
    #sum += perplexity(0, len(docs_entity), phie, phiw, theta, algo)
    print algo+"_k_"+ str(k) +": "+ str(sum/10)

def perplexity(I,N,phie,phiw,theta,algo):
    perplexity = 0.0
    total_length = 0

    for i in range(I, N):
        if(algo=="ECTM"):
            total_length += len(docs_entity[i])
        else:
            total_length += len(docs_non_entity[i])

    for i in range(I, N):
        if(algo=="ECTM"):
            for j in range(0, len(docs_entity[i])):
                prob = 0.0
                for k in range(0, len(phie)):
                    prob += float(theta[i][k]) * float(phie[k][int(docs_entity[i][j])])
                perplexity += math.log(prob)
        else:
            for j in range(0, len(docs_non_entity[i])):
                prob1 = 0.0
                for k in range(0, len(phiw)):
                    prob1 += float(theta[i][k]) * float(phiw[k][int(docs_non_entity[i][j])])
                perplexity += math.log(prob1)

    perplexity = math.exp(-1 * perplexity / total_length)
    return perplexity

list_ectm = [1,5,10,15,20,25,30]
algo = "ECTM"

for k in list_ectm:
    prep(k,algo)

list_corr = [1,5,10,15,20,25,30,35]
algo = "CorrLDA2"

for k in list_corr:
    prep(k,algo)