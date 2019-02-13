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

feature_file = sys.argv[1]
num_clusters = int(sys.argv[2])

feature_data = getFeatureData(feature_file)

def InitClusters(feature_data,num_clusters):
    cluster_dict = {}
    #populate the dict with empty vectors that the features will be appended to.
    for i in range(num_clusters):
        cluster_dict[i] = []

    #Randomly separate the datapoints into clusters
    for i in range(len(feature_data)):
        random_num = random.randrange(0,num_clusters)
        cluster_dict[random_num].append(feature_data[i])

    return cluster_dict

def getClusterMean(cluster_dict,num_attrs):
    #num_attrs = len(cluster_dict[0][0])

    mean_cluster_dict = {}

    for cluster_num in cluster_dict:
        cluster_mean = [0]*num_attrs
        for row_num in range(len(cluster_dict[cluster_num])):
            for col_num in range(len(cluster_dict[cluster_num][row_num])):
                cluster_mean[col_num] += cluster_dict[cluster_num][row_num][col_num]
        cluster_mean = [cluster_mean[i]/len(cluster_dict[cluster_num]) for i in range(len(cluster_mean))]
        mean_cluster_dict[cluster_num] = cluster_mean

    return mean_cluster_dict

def getDiffToMean(x_vec,mean_vec):
    diff_vec = [x_vec[i]-mean_vec[i] for i in range(len(x_vec))]
    diff = sum(diff_vec)
    return abs(diff)

def getDiffForObj(x_vec,mean_vec):
    diff_vec = [(x_vec[i]-mean_vec[i])**2 for i in range(len(x_vec))]
    diff = sum(diff_vec)
    return abs(diff)

def ReclusterData(feature_data,mean_cluster_dict,num_clusters):
    new_cluster_dict = {}
    for i in range(num_clusters):
        new_cluster_dict[i] = []

    for i in range(len(feature_data)):
        cluster_distance = {}
        for cluster_num in mean_cluster_dict:
            diff = getDiffToMean(feature_data[i],mean_cluster_dict[cluster_num])
            cluster_distance[cluster_num] = diff
        closest_cluster = min(cluster_distance, key=cluster_distance.get)
        new_cluster_dict[closest_cluster].append(feature_data[i])

    return new_cluster_dict

def getObjective(cluster_dict,mean_cluster_dict):
    obj = 0
    for cluster_num in cluster_dict:
        cluster_diff = 0
        for i in range(len(cluster_dict[cluster_num])):
            diff = getDiffForObj(cluster_dict[cluster_num][i],mean_cluster_dict[cluster_num])
            cluster_diff += diff
        obj += cluster_diff
    return obj

#Check to make sure no cluster is empty
def anyClustersEmp(cluster_dict,num_clusters):
    clusters_emp = False
    for cluster_num in range(num_clusters):
        if len(cluster_dict[cluster_num]) == 0:
            clusters_emp = True
    return clusters_emp

def getClusters(feature_data,num_clusters):
    num_attrs = len(feature_data[0])

    #Make sure the clusters aren't initialized with zero records
    while(True):
        cluster_dict = InitClusters(feature_data,num_clusters)
        if not anyClustersEmp(cluster_dict,num_clusters):
            break

    mean_cluster_dict = getClusterMean(cluster_dict,num_attrs)
    #print(cluster_dict)
    #print("And now Mean")
    #print(mean_cluster_dict)

    theta = 0.001

    prev_obj = 0

    while(True):

        #print("new Cluster")
        for i in range(5):
            cluster_dict = ReclusterData(feature_data,mean_cluster_dict,num_clusters)
            if not anyClustersEmp(cluster_dict,num_clusters):
                break
        #If after 5 retries, clusters are still empty, just re-initialize:
        if anyClustersEmp(cluster_dict,num_clusters):
            cluster_dict = InitClusters(feature_data,num_clusters)

        #print('Reclustered')

        mean_cluster_dict = getClusterMean(cluster_dict,num_attrs)
        #print(new_mean_cluster_dict)

        obj = getObjective(cluster_dict,mean_cluster_dict)

        #print(obj)
        #print(abs(prev_obj-obj))
        if abs(prev_obj-obj) < theta:
            break

        prev_obj = obj

    return cluster_dict

cluster_dict = getClusters(feature_data,num_clusters)
for i in range(len(feature_data)):
    cluster_assignment = 0
    for cluster_num in cluster_dict:
        if feature_data[i] in cluster_dict[cluster_num]:
            cluster_assignment = cluster_num
    print(str(cluster_assignment)+' '+str(i))
