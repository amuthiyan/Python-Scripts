'''
CS675 Machine Learning
Assignment 2: Build a Least_Squares Classifier
'''

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


def matrixMultiply(a,b):
    result = []
    for i in range(len(a)):
        vec = []
        for j in range(len(b[0])):
            elem = 0
            for k in range(len(b)):
                elem += a[i][k] * b[k][j]
            vec.append(elem)
        result.append(vec)
    return result

def vectorMultiply(a,v):
    result = []
    for row in a:
        result.append(dotProduct(row,v))
    return result

def matrixTranspose(a):
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


#Get Input file names
'''
args  = argparse.ArgumentParser()
args.add_argument("-d", "--data_file", required = True, help="Data_File")
args.add_argument("-t", "--labels", required = True, help="Label_File")
args = vars(args.parse_args())
'''

feature_file = sys.argv[1] #args["data_file"]
label_file = sys.argv[2] #args["labels"]

#Extract features and labels from breast cancer dataset
feature_data = getFeatureData(feature_file)
feature_labels = getLabelData(label_file)

#Separate training data from feature data, and create r vector of labels:
def getTrainData(feature_data,train_indexes):
    train_data = []
    r_vec = []
    for data_index in train_indexes:
        train_data.append(feature_data[data_index])
        r_vec.append(train_indexes[data_index])
    return train_data, r_vec
train_data, r_vec = getTrainData(feature_data,feature_labels)

#Initialize the weights to random values from -0.01 to 0.01:
def InitWeights(num_attrs):
    w_vec = [0]*(num_attrs)
    for i in range(num_attrs):
        weight = random.uniform(-0.01,0.01)
        w_vec[i] = weight
    return w_vec

#Now lets train the model using the gradient descent algorithm:
#Function calculates the final set of weights to use using the gradient descent algorithm
def GradDescent(train_data,r_vec):
    #Give each x in train_data a bias term at x[0]
    for x in train_data:
        x.insert(0,1)

    num_attrs = len(train_data[0])
    w_vec = InitWeights(num_attrs)
    #print(w_vec)

    theta = 0.001
    learning_rate = 0.0001
    prev_error = 0

    while(True):

        out_diff_vec = [(r_vec[i] - dotProduct(train_data[i],w_vec)) for i in range(len(r_vec))]
        #print(w_vec)

        #compute error
        error = 0
        for diff in out_diff_vec:
            error = error + (diff**2)
        error = 0.5*error
        #print(error)


        #If error is lower than theta, stop training
        if abs(prev_error - error)<=theta:
            break

        #compute change in weights
        change_in_weights = [0]*num_attrs
        for row_num in range(len(train_data)):
            x_d = [out_diff_vec[row_num] * train_data[row_num][col] for col in range(num_attrs)]
            for col_num in range(num_attrs):
                change_in_weights[col_num] = change_in_weights[col_num] + x_d[col_num]


        #change_in_weights = learning_rate*sum(change_in_weights)
        change_in_weights = [learning_rate*change_in_weights[i] for i in range(num_attrs)]

        #w_vec = [w_vec[i] + change_in_weights for i in range(num_attrs)]
        w_vec = [w_vec[i] + change_in_weights[i] for i in range(num_attrs)]

        #print(error)
        prev_error = error
        #print(epoch)

    #print("finally!")
    #print("Final Error: "+str(error))
    return w_vec

#Calculate the distance of the Hyperplane from the origin
def calcDistanceToOrigin(w_vec):
    weights_sqr = [w_vec[i]**2 for i in range(1,len(w_vec))]
    weights_sum = sum(weights_sqr)
    distance = w_vec[0]/((weights_sum)**0.5)
    return abs(distance)

final_weights = GradDescent(train_data,r_vec)
hyperplane = final_weights[1::]
distance_to_origin = calcDistanceToOrigin(final_weights)
print("Hyperplane: "+str(hyperplane))
print("w0: "+str(final_weights[0]))
print("Distance to Origin: "+str(distance_to_origin))


def classify(test_data,w_vec,feature_labels):
    pred_vec = {}
    for i in range(len(test_data)):
        if i not in feature_labels:
            test_data[i].insert(0,1)
            pred = dotProduct(test_data[i],w_vec)
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

'''
def CheckAcc(prediction_vector,feature_labels):
    hit_counter = 0
    miss_counter = 0
    for i in range(len(prediction_vector)):
        if prediction_vector[i] == feature_labels[i]:
            hit_counter = hit_counter = hit_counter+1
        else:
            miss_counter = miss_counter = miss_counter+1
    accuracy = hit_counter/len(prediction_vector)
    print("Num Hits: "+str(hit_counter))
    print("Num Misses: "+str(miss_counter))
    print("Accuracy: "+str(accuracy))
CheckAcc(pred_vec,r_vec)
'''
