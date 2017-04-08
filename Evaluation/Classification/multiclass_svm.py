import numpy as np

f = open("data.csv","r")
content  = f.read()
f.close()
list_text = content.splitlines()
list_text = np.array([x.split(',') for x in list_text])
with open("label.csv") as f:
    label = [line.strip() for line in f]
label = np.array([label])
print(list_text.shape)
print(label.shape)
data = np.concatenate((list_text, label.T), axis=1)

x = np.random.permutation(data.shape[0])

training, testing = data[x[:int(.8*data.shape[0])]], data[x[int(.8*data.shape[0]):]]



print(training.shape)
print(testing.shape)

