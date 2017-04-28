import math

dir_word_ind = "docs/word-index.txt"

docs = []

with open(dir_word_ind) as f:
    i =0
    for line in f:
        line = line.strip()
        if ' ' in line:
            docs.append(line.split(" "))
            i += 1
        else:
            temp = [line]
            docs.append(temp)
            i += 1

def prep(k,algo):
    dir_phi = "docs/" + algo + "_op/" + str(k) + "/" + algo + "_phi"
    dir_theta = "docs/" + algo + "_op/" + str(k) + "/" + algo + "_theta"

    phi = []
    theta = []

    with open(dir_phi) as f:
        i = 0
        for line in f:
            line = line.strip()
            if ' ' in line:
                phi.append(line.split(" "))
                i += 1
            else:
                phi.append(line)
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
            sum += perplexity(m * 1000, (m + 1) * 1000,phi,theta, algo)
        else:
            sum += perplexity(9000, len(docs),phi,theta, algo)
    #sum += perplexity(0, len(docs_entity), phie, phiw, theta, algo)
    print algo+"_k_"+ str(k) +": "+ str(sum/10)

def perplexity(I,N,phi,theta,algo):
    perplexity = 0.0
    total_length = 0

    for i in range(I, N):
        total_length += len(docs[i])


    for i in range(I, N):
        for j in range(0, len(docs[i])):
            prob = 0.0
            for k in range(0, len(phi)):
                prob += float(theta[i][k]) * float(phi[k][int(docs[i][j])])
            perplexity += math.log(prob)


    perplexity = math.exp(-1 * perplexity / total_length)
    return perplexity

list_ectm = [1,5,10,15,20,25,30,35]
algo = "LDA"

for k in list_ectm:
    prep(k,algo)