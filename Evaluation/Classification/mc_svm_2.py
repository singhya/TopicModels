import numpy as np
from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
import pandas as pd

'''
f = open("data.csv","r")
content  = f.read()
f.close()
list_text = content.splitlines()
list_text = np.array([x.split(',') for x in list_text])
with open("label.csv") as f:
    label = [line.strip() for line in f]
label = np.array([label])
#print(list_text.shape)
#print(label.shape)
data = np.concatenate((list_text, label.T), axis=1)

x = np.random.permutation(data.shape[0])

training, testing = data[x[:int(.8*data.shape[0])]], data[x[int(.8*data.shape[0]):]]
'''
Meta = pd.read_csv("data.csv")
y = Meta.pop('Label')
x = Meta
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

x_train = x_train.astype(float)
y_train = y_train.astype(float)

svm1 = OneVsRestClassifier(LinearSVC(random_state=0)).fit(x_train, y_train)
pred =  svm1.predict(x_test)
print svm1.score(x_test,y_test)


#print(X.shape)
#print(y.shape)
#print(testing.shape)

