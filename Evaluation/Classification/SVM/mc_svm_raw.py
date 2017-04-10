from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
import pandas as pd

Meta = pd.read_csv("datav1.csv")
y = Meta.pop('Label')
x = pd.read_csv("svmvector0.csv")
#print x.shape
#print y.shape

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

x_train = x_train.astype(float)
y_train = y_train.astype(float)

svm1 = OneVsRestClassifier(LinearSVC(random_state=0)).fit(x_train, y_train)
pred =  svm1.predict(x_test)
print svm1.score(x_test,y_test)