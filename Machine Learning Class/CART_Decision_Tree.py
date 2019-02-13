import sys
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
            r_vec.append(0)
        else:
            r_vec.append(train_indexes[data_index])
    return train_data, r_vec
train_data, r_vec = getTrainData(feature_data,feature_labels)
print(r_vec)

def SortCol(train_data,col_num):
    #print(train_data)
    #sorted_data = train_data.sort(key = lambda x:x[col_num])
    sorted_data = sorted(train_data, key=lambda x: x[col_num])
    #print(sorted_data)
    return sorted_data

def getSplitData(train_data,i):
    l_data = train_data[0:i]
    r_data = train_data[i::]
    return l_data,r_data

def getLabelP(s_data):
    #Last column is the label vector (reminder)
    num_0s = 0
    for i in range(len(s_data)):
        if s_data[i][-1] == 0:
            num_0s+=1
    labelp = num_0s/len(s_data)
    return labelp

def getGiniImpurity(l_data,r_data,train_data):
    p_left = len(l_data)/len(train_data)
    p_right = len(r_data)/len(train_data)

    if len(l_data)==0:
        p_0_left = 0
    else:
        p_0_left = getLabelP(l_data)

    if len(r_data)==0:
        p_0_right = 0
    else:
        p_0_right = getLabelP(r_data)

    gini_impurity = ((p_left)*(p_0_left)*(1-p_0_left)) + ((p_right)*(p_0_right)*(1-p_0_right))
    return gini_impurity

def getBestSplit(train_data):
    best_split = 0
    lowest_impurity = 100000000000000000000000000
    #print("Splits: ")
    for i in range(len(train_data)):
        #print(i)
        l_data, r_data = getSplitData(train_data,i)
        #print(l_data)
        gini_impurity = getGiniImpurity(l_data,r_data,train_data)
        if gini_impurity < lowest_impurity:
            best_split = i
            lowest_impurity = gini_impurity
    return lowest_impurity,best_split

def CART(train_data,r_vec):
    #get number of columns (num_attrs)
    num_attrs = len(train_data[0])

    #Add the label as the last column in the data
    for i in range(len(train_data)):
        train_data[i].append(r_vec[i])

    best_split = 0
    lowest_impurity = 100000000000000000000000000
    best_col = 0

    #Iterate through each column:
    for i in range(num_attrs):
        #print(i)
        #Sort the column from highest to lowest values
        sorted_data = SortCol(train_data,i)
        #print(sorted_data)

        #Determine the best split for that column:
        lowest_impurity_col, best_split_for_col = getBestSplit(sorted_data)
        #print(lowest_impurity_col)

        if lowest_impurity_col < lowest_impurity:
            best_split = best_split_for_col
            lowest_impurity = lowest_impurity_col
            best_col = i

    print('Gini Impurity: '+str(lowest_impurity))
    return best_col, best_split

best_col, best_split = CART(train_data,r_vec)
print("Best Column is column number "+str(best_col))
print("Best Split value is: "+str(best_split))
