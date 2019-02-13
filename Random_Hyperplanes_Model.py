import random
import sys

from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

'''Get feature data from file as a matrix with a row per data instance'''
def getFeatureData(featureFile):
    x=[]
    dFile = open(featureFile, 'r')
    for line in dFile:
        row = line.split()
        rVec = [float(item) for item in row]
        x.append(rVec)
    dFile.close()
    return x
'''Get label data from file as a dictionary with key as data instance index
and value as the class index
'''
def getLabelData(labelFile):
    lFile = open(labelFile, 'r')
    lDict = {}
    for line in lFile:
        row = line.split()
        lDict[int(row[1])] = int(row[0])
    lFile.close()
    return lDict

feature_file = sys.argv[1]
train_label_file = sys.argv[2]
k = int(sys.argv[3])

feature_data = getFeatureData(feature_file)
train_labels = getLabelData(train_label_file)

#Separate training data from feature data, and create r vector of labels:
def getTrainData(feature_data,train_indexes):
    test_data = []
    train_data = []
    r_vec = []
    for data_index in range(len(feature_data)):
        if data_index in train_indexes:
            train_data.append(feature_data[data_index])
            if train_indexes[data_index]==0:
                r_vec.append(0)
            else:
                r_vec.append(train_indexes[data_index])
        else:
            test_data.append(feature_data[data_index])
    return test_data, train_data, r_vec
test_data, train_data, r_vec = getTrainData(feature_data,train_labels)

def InitWeights(num_attrs):
    w_vec = [0]*(num_attrs)
    for i in range(num_attrs):
        weight = random.uniform(-1,1)
        w_vec[i] = weight
    return w_vec

def dotProduct(u,v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum

def getW0(train_data,w_vec):
    wtxj_vec = []
    for i in range(len(train_data)):
        wtxj = dotProduct(w_vec,train_data[i])
        wtxj_vec.append(wtxj)
    w_0 = random.choice([min(wtxj_vec),max(wtxj_vec)])
    return w_0

def getZVec(dataset,w_vec,w_0):
    z_vec = []
    for i in range(len(dataset)):
        wtxj = dotProduct(w_vec,train_data[i])
        z_i = wtxj+w_0
        if z_i>=0:
            z_vec.append(1)
        else:
            z_vec.append(0)
    #print(z_vec)
    return z_vec

def matrixTranspose(a):
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]

#Run the random hyperplanes on the train and test data
def randomHyperPlanes(train_data,test_data,r_vec,k):
    num_attrs = len(train_data[0])
    Z_train = []
    Z_test = []
    #print(len(test_data[0]))
    for i in range(k):
        #Initialise random weight vector
        w_vec = InitWeights(num_attrs)

        #Choose a W_0
        w_0 = getW0(train_data,w_vec)

        #Get Prediction Vector Z_train
        z_i_train = getZVec(train_data,w_vec,w_0)
        z_i_test = getZVec(test_data,w_vec,w_0)

        Z_train.append(z_i_train)
        Z_test.append(z_i_test)


    Z_train = matrixTranspose(Z_train)
    Z_test = matrixTranspose(Z_test)

    return Z_train, Z_test

Z_train, Z_test = randomHyperPlanes(train_data,test_data,r_vec,k)

svm = LinearSVC(max_iter=10000)
model = svm.fit(Z_train,r_vec)
pred_vec = model.predict(Z_test)

predictions = {}
pred_vec_index = 0
for i in range(len(feature_data)):
    if i not in train_labels:
        predictions[i] = pred_vec[pred_vec_index]
        pred_vec_index = pred_vec_index+1

for i in predictions:
    print('( '+ str(i)+' : '+str(predictions[i])+' )')
