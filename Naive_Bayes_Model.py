'''
Name: Aneesh Muthiyan
Machine Learning
CS675-101
Assignment 1
'''

'''
Write a Python program that implements the Naive Bayes classifier.
Your program should take as input a dataset file and a set of training
labels in the format given in the example datasets on the course website.
As output your program should produce predicted labels for the test
dataset which are feature vectors whose labels are not given for training.

For Multi-Variate Data:
Each data point will be a vector of 'm' features
For this we have to create a covariance matrix of each class instead of just finding the variance of each class
The mean of each class will now be a mean vector
For now, only calculate the std of each attribute, and ignore covariances in the covariance matrix. (These will be 0 for now)
'''

import sys

#Extract features and labels from breast cancer dataset
'''
Below are functions from dataExtractUtil that have been provided by the professor
for extracting the data and label files
'''
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
training_file = sys.argv[2] #args["labels"]
#label_file = 'breast_cancer.labels'
#label_file = args["labels"]

feature_data = getFeatureData(feature_file)
#feature_labels = getLabelData(label_file)
train_indexes = getLabelData(training_file)

'''
Now we need to separate the feature set into different matrices for each of the classes.
We will do this by creating a dictionary of the classes, with the class as the key and the matrix of attributes as the value.
'''
def SepByClass(train_indexes,feature_data):
    #Set up a classwise_data dict to store the datapoints for each class separately
    classwise_data = {}
    for datapoint_num in train_indexes:
        #If the class of the data is not in the classwise dict, add it there
        if train_indexes[datapoint_num] not in classwise_data:
            classwise_data[train_indexes[datapoint_num]] = []
            #Add the datapoint at that index to the set
            classwise_data[train_indexes[datapoint_num]].append(feature_data[datapoint_num])
        else:
            #Add the datapoint at that index to the set
            classwise_data[train_indexes[datapoint_num]].append(feature_data[datapoint_num])
    return classwise_data

class_data = SepByClass(train_indexes, feature_data)
num_classes = len(class_data)

'''
Now we need to create a vector for each class, that contains the mean of every attribute for that class.
Again these means will be place in a dictionary called class_mean with the class_labels as keys
'''
#Create a mean vector of attributes for each of the data classes
def getMeanVec(class_data):
    class_mean = {}
    num_attributes = len(class_data[0][0])
    for i in range(len(class_data)):
        class_mean[i] = [0] * num_attributes #Initialise the mean vector for the class to all ones for each attribute
        temp_sum = [0] * num_attributes #A temp vector created to calculate the sums of the columns before mean is calculated
        for row in range(len(class_data[i])): #Go through each attribute set in the class
            for col in range(len(class_data[i][row])): #Go through each attribute in the attribute set, to get the mean of the entire column
                temp_sum[col] = temp_sum[col] + class_data[i][row][col]
        #Populate the class_mean vector for the class with the actual mean vector for the attributes
        class_mean[i] = [attr_sum/len(class_data[i]) for attr_sum in temp_sum]
    return class_mean

class_mean = getMeanVec(class_data)
#print("mean: ")
print(class_mean)

'''
Now we need to create a vector of the standard deviation of each attribute for each class
'''
#Create a vector of standard deviations of attributes for each data class
def getSTDVec(class_data):
    num_attributes = len(class_data[0][0])
    class_std = {}
    for i in range(len(class_data)):
        class_std[i] = [1] * num_attributes #Initialise the std vector for the class to all zeros for each attribute
        #Create a list for each attribute column, so we can easily find its std
        attribute_cols = {}
        for row in range(len(class_data[i])):
            for col in range(len(class_data[i][row])):
                if col not in attribute_cols:
                    attribute_cols[col] = []
                    attribute_cols[col].append(class_data[i][row][col])
                else:
                    attribute_cols[col].append(class_data[i][row][col])
        #Calculate the std for each attribute, and put it into the std vector for its class
        for attribute_num in range(len(attribute_cols)):
            attribute_mean = sum(attribute_cols[attribute_num])/len(attribute_cols[attribute_num])
            sum_difference_total = 0
            for datapoint in attribute_cols[attribute_num]:
                sum_difference_sqr = (datapoint-attribute_mean)**2
                sum_difference_total = sum_difference_total + sum_difference_sqr
            attribute_var = sum_difference_total/(len(attribute_cols[attribute_num]))
            attribute_std = attribute_var**(1/2)
            #Calculate the standard deviation of the attribute
            class_std[i][attribute_num] = attribute_std
    return class_std

#print("std: ")
class_std = getSTDVec(class_data)
#print(class_std)

'''
Now that we have vectors for the mean and the std of each attribute, we can begin making predictions on new data:
Let us assume that the input is coming to us in the form of a matrix (list of lists) where each row represents a datapoint with the same number of attributes as our training sample (30 in the breast cancer case).
In this case, we will predict on each row individually, and print out the potential label as we go.
'''
def PredictClass(input_data,class_mean,class_std,num_classes):
    print("Output Format: (<class_prediction>, <index_num>)")
    #Predict on each datapoint individually
    prediction_vector = []
    for datapoint_num in range(len(input_data)):
        #Create label probability for each class label, and append to a list
        label_probs = {}
        for class_num in range(num_classes):
            #Start finding ((x-m)/std)^2 for each attribute
            formula_output = []
            for attr_num in range(len(input_data[datapoint_num])):
                answer = ((input_data[datapoint_num][attr_num] - class_mean[class_num][attr_num])/class_std[class_num][attr_num])**2
                formula_output.append(answer)
            class_prob = sum(formula_output)
            label_probs[class_num] = class_prob
        #Find the argmin of all the class probs and print it
        class_prediction = min(label_probs, key=label_probs.get)
        #print(label_probs)
        prediction_vector.append(class_prediction)
        #print(label_probs)
        print("("+str(class_prediction)+", "+str(datapoint_num)+")")
        #print("Index_Num: "+str(datapoint_num) + ", Final Prediction: "+str(class_prediction))
    return prediction_vector

input_data = feature_data
prediction_vector = PredictClass(input_data,class_mean,class_std,num_classes)

'''
Now we will also test this code by checking the accuracy of the predictions by
comparing the predicted labels to the known actual label
'''
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
CheckAcc(prediction_vector,feature_labels)
'''
