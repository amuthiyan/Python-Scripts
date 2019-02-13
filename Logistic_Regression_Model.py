import math
import random
import sys

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

feature_file = sys.argv[1] #args["data_file"]
label_file = sys.argv[2] #args["labels"]
#label_file = 'breast_cancer.labels'
#label_file = args["labels"]

feature_data = getFeatureData(feature_file)
#feature_labels = getLabelData(label_file)
feature_labels = getLabelData(label_file)

def dotProduct(u,v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum

#Separate training data from feature data, and create r vector of labels:
def getTrainData(feature_data,train_indexes):
    train_data = []
    r_vec = []
    for data_index in train_indexes:
        train_data.append(feature_data[data_index])
        if train_indexes[data_index]==0:
            r_vec.append(0)
        else:
            r_vec.append(train_indexes[data_index])
    return train_data, r_vec
train_data, r_vec = getTrainData(feature_data,feature_labels)

def InitWeights(num_attrs):
    w_vec = [0]*(num_attrs)
    for i in range(num_attrs):
        weight = random.uniform(-0.01,0.01)
        w_vec[i] = weight
    return w_vec

def getLenW(w_vec):
    sum_w = sum([(w_vec[i]**2) for i in range(1,len(w_vec))])
    return sum_w**0.5

def sigmoid(x):
    return 1.0/(1+math.exp(-x))

def getError(train_data,r_vec,w_vec,lamb):
    loss_vec = []
    for i in range(len(train_data)):
        try:
            sig = sigmoid(dotProduct(w_vec,train_data[i]))
        except OverflowError:
            sig = 1
        if (sig <= 0 or sig == 1):
            continue
        loss = ((-1*r_vec[i]*math.log(sigmoid(dotProduct(w_vec,train_data[i])))) - ((1-r_vec[i])*math.log(1-sigmoid(dotProduct(w_vec,train_data[i])))))
        #print(loss)
        loss_vec.append(loss)
    #print(loss_vec)
    sum_loss = sum(loss_vec)
    #print(sum_loss)
    sum_w = sum([(w_vec[i]**2) for i in range(1,len(w_vec))])
    regularized_error = sum_loss + ((lamb/2)*sum_w)#sum([w_vec[i]**2 for i in range(1,len(w_vec))]))
    return regularized_error

def getDelGrad(train_data,r_vec,w_vec,lamb):
    del_grad = [0]*len(train_data[0])
    for row_num in range(len(train_data)):
        try:
            dp = r_vec[row_num] - (sigmoid(dotProduct(w_vec,train_data[row_num])))
        except OverflowError:
            dp = 0
        for col_num in range(len(train_data[0])):
            del_grad[col_num] += train_data[row_num][col_num]*dp

    del_grad = [del_grad[i]+(lamb*w_vec[i]) for i in range(1,len(w_vec))]
    del_grad = [-1*del_grad[i] for i in range(len(del_grad))]

    try:
        del_grad_0 = sum([r_vec[i] - (sigmoid(dotProduct(w_vec,train_data[i]))) for i in range(len(train_data))])
        del_grad_0 = -1*del_grad_0
    except OverflowError:
        del_grad_0 = 0
    del_grad.insert(0,del_grad_0)

    return del_grad

#Calculate the distance of the Hyperplane from the origin
def calcDistanceToOrigin(w_vec):
    rest_w = w_vec[1::]
    weights_sqr = [rest_w[i]**2 for i in range(len(rest_w))]
    weights_sum = sum(weights_sqr)
    distance = w_vec[0]/((weights_sum)**0.5)
    return distance

def runGradientDescent(train_data,r_vec,lamb):
    #Give each x in train_data a bias term at x[0]
    for x in train_data:
        x.insert(0,1)

    num_attrs = len(train_data[0])
    w_vec = InitWeights(num_attrs)
    #print(len(w_vec))
    #print(w_vec)
    #print(w_vec)

    theta = 0.001
    learning_rate = 0.001
    prev_error = 0

    while(True):

        error = getError(train_data,r_vec,w_vec,lamb)
        #print(error)

        if abs(prev_error - error)<=theta:
            break

        del_grad_vec = getDelGrad(train_data,r_vec,w_vec,lamb)
        #print(del_grad_vec)

        del_grad_vec = [-1*learning_rate*del_grad_vec[i] for i in range(num_attrs)]


        w_vec = [w_vec[i] + del_grad_vec[i] for i in range(num_attrs)]
        #print(w_vec)


        #print(abs(prev_error-error))
        prev_error = error
        #print(error)

    #print("Final Error: "+str(error))
    #print(w_vec)
    return w_vec



final_weights = runGradientDescent(train_data,r_vec,0)
hyperplane = final_weights[1::]
len_h = getLenW(final_weights)
distance_to_origin = calcDistanceToOrigin(final_weights)

def classify(test_data,w_vec,feature_labels):
    pred_vec = {}
    for i in range(len(test_data)):
        if i not in feature_labels:
            test_data[i].insert(0,1)
            pred = sigmoid(dotProduct(w_vec,test_data[i]))
            #print(pred)
            if pred>0.5:
                #pred_vec.append(1)
                pred_vec[i] = 1
            else:
                #pred_vec.append(0)
                pred_vec[i] = 0
    return pred_vec

pred_vec = classify(feature_data,final_weights,feature_labels)
for i in pred_vec:
    print('( '+ str(i)+' : '+str(pred_vec[i])+' )')
