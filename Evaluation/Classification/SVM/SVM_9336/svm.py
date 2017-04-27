from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
import pandas as pd

def svm(file):
    Meta = pd.read_csv(file)
    y = Meta.pop('Label')
    x = Meta

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    x_train = x_train.astype(float)
    y_train = y_train.astype(float)

    svm1 = OneVsRestClassifier(LinearSVC(random_state=0)).fit(x_train, y_train)
    #pred = svm1.predict(x_test)
    return svm1.score(x_test, y_test)

list_ectm = [1,5,10,15,20,25,30]
algo = "ECTM"

for k in list_ectm:
    sc = svm("docs/" + algo + "_op/csv/" + algo + "_theta_k_" + str(k) + ".csv")
    print algo + "_k_" + str(k) + ": "+str(sc)

list_corr = [1,5,10,15,20,25,30,35]
algo = "CorrLDA2"

for k in list_corr:
    sc = svm("docs/" + algo + "_op/csv/" + algo + "_theta_k_" + str(k) + ".csv")
    print algo + "_k_" + str(k) + ": "+str(sc)