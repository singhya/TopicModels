dir_labels = "docs/category-labels"
dir_theta_csv =""

def prep(k,algo):

    dir_theta = "docs/" + algo + "_op/" + algo + "_theta_k_" + str(k)

    meta = ""
    for i in range(1, k + 1):
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

            f1.write(label)
            i += 1

    f_lab.close()
    f.close()
    f1.close()

list_ectm = [1,5,10,15,20,25,30,35]
algo = "LDA"

for k in list_ectm:
    prep(k,algo)