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
def dotProduct(u,v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum

#Extract features and labels from breast cancer dataset
#feature_file = 'test_data.data'
#label_file = 'test_labels.labels'

#Import indexes of the training data

feature_file = sys.argv[1] #args["data_file"]
label_file = sys.argv[2] #args["labels"]

feature_data = getFeatureData(feature_file)
#train_indexes = getLabelData(training_file)
feature_labels = getLabelData(label_file)

#Separate training data from feature data, and create r vector of labels:
def getTrainData(feature_data,train_indexes):
    train_data = []
    r_vec = []
    for data_index in train_indexes:
        train_data.append(feature_data[data_index])
        if train_indexes[data_index]==0:
            r_vec.append(-1)
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

def getError(train_data,r_vec,w_vec):
    loss_vec = []
    for i in range(len(train_data)):
        poss_loss = 1 - (r_vec[i]*(dotProduct(w_vec,train_data[i])))
        loss_vec.append(max([0,poss_loss]))
    return sum(loss_vec)

def getDelGrad(train_data,r_vec,w_vec):
    del_grad = [0]*len(train_data[0])
    for row_num in range(len(train_data)):
        dp = r_vec[row_num]*(dotProduct(w_vec,train_data[row_num]))
        #print(dp)
        for col_num in range(len(train_data[0])):
            if dp<1:
                del_grad[col_num] += -1*train_data[row_num][col_num]*r_vec[row_num]
            else:
                del_grad[col_num] += 0
    return del_grad

def getLenW(w_vec):
    sum_w = sum([(w_vec[i]**2) for i in range(len(w_vec))])
    return sum_w**0.5

def runSubGradient(train_data,r_vec):
    #Give each x in train_data a bias term at x[0]
    for x in train_data:
        x.insert(0,1)

    num_attrs = len(train_data[0])
    w_vec = InitWeights(num_attrs)
    #print(w_vec)
    #print(w_vec)

    theta = 0.001
    learning_rate = 0.001
    prev_error = 0

    while(True):

        error = getError(train_data,r_vec,w_vec)
        #print(error)

        if abs(prev_error - error)<=theta:
            break

        del_grad_vec = getDelGrad(train_data,r_vec,w_vec)
        #print(del_grad_vec)

        del_grad_vec = [-1*learning_rate*del_grad_vec[i] for i in range(num_attrs)]


        w_vec = [w_vec[i] + del_grad_vec[i] for i in range(num_attrs)]
        #print(w_vec)

        #print(abs(prev_error-error))
        prev_error = error


    #print("Final Error: "+str(error))
    #print(w_vec)
    return w_vec

def classify(test_data,w_vec,feature_labels,len_h):
    pred_vec = {}
    for i in range(len(test_data)):
        if i not in feature_labels:
            test_data[i].insert(0,1)
            pred = dotProduct(test_data[i],w_vec)/len_h
            #print(pred)
            if pred>0:
                #pred_vec.append(1)
                pred_vec[i] = 1
            else:
                #pred_vec.append(0)
                pred_vec[i] = -1
    return pred_vec

#Calculate the distance of the Hyperplane from the origin
def calcDistanceToOrigin(w_vec):
    rest_w = w_vec[1::]
    weights_sqr = [rest_w[i]**2 for i in range(len(rest_w))]
    weights_sum = sum(weights_sqr)
    distance = w_vec[0]/((weights_sum)**0.5)
    return distance

final_weights = runSubGradient(train_data,r_vec)
hyperplane = final_weights[1::]
len_h = getLenW(hyperplane)
distance_to_origin = calcDistanceToOrigin(final_weights)
print("Hyperplane: "+str(hyperplane))
print("w[0]: "+str(final_weights[0]))
print("Distance to Origin: "+str(abs(distance_to_origin)))

pred_vec = classify(feature_data,final_weights,feature_labels,len_h)
for i in pred_vec:
    print('( '+ str(i)+' : '+str(pred_vec[i])+' )')
