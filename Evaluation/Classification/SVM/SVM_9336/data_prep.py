import numpy as np

dir_labels = "docs/category-labels"
dir_theta_csv =""

def prep(k,algo):

    dir_theta = "docs/" + algo + "_op/" + algo + "_theta_k_" + str(k)

    file = open(dir_theta, 'rb')
    table_theta = [row.strip().split(' ') for row in file]

    dir_psi = "docs/" + algo + "_op/" + algo + "_psi_k_" + str(k)

    file = open(dir_psi, 'rb')
    table_psi = [row.strip().split(' ') for row in file]

    theta_psi = np.matmul(np.asarray(table_theta,dtype=float),np.asarray(table_psi,dtype=float))


    meta = ""
    for i in range(1, 2*k + 1):
        meta += 'F' + str(i) + ','
    meta += 'Label'

    dir_theta_csv = "docs/" + algo + "_op/csv/" + algo + "_theta_k_" + str(k) + ".csv"

    f1 = open(dir_theta_csv, "w")
    f1.write(meta)
    f1.write("\n")

    f_lab = open(dir_labels, "r")

    with open(dir_theta) as f:
        i = 0
        for line in f:
            label = f_lab.readline()
            line = line.strip()
            if ' ' in line:
                words = line.split(" ")
                for word in words:
                    f1.write(word + ",")
            else:
                f1.write(line + ",")

            for x in theta_psi[i]:
                f1.write(str(x)+",")

            f1.write(label)
            i += 1


    f_lab.close()
    f.close()
    f1.close()



list_ectm = [1,5,10,15,20,25,30]
algo = "ECTM"

for k in list_ectm:
    prep(k,algo)

list_corr = [1,5,10,15,20,25,30,35]
algo = "CorrLDA2"

for k in list_corr:
    prep(k, algo)