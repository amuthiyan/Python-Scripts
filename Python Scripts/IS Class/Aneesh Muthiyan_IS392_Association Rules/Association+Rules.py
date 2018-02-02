
# coding: utf-8

# In[125]:

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import types
import time
import re
import queue
import string
import os
import glob
from nltk.corpus import stopwords
import nltk
import string


# In[126]:

#Read the inverted frequency index from file
def ReadIndex(filename):
    path = 'Indexer_Aneesh/'
    file = open(path+filename,'r')
    inv_index = {}
    doc = file.readlines()
    for line in doc:
        line = line.split(':')
        word = line[0].strip(' ')
        line = line[1].strip(' ').split(', [')
        clean_line = []
        for term in line:
            term = term.strip(',( \n)[]').split(', ')
            clean_line.append(term) 
        inv_index[word] = clean_line
    return inv_index


# In[127]:

#Get ocurrence based partial index
def getPartIndex(inv_index):
    temp = inv_index.copy()
    for word in inv_index:
        temp[word] = []
        for record in inv_index[word]:
            temp[word].append(record[0])
    return temp


# In[128]:

#Returns the intersect of the terms of inv_lists
def Intersect(inv_lists):
    sect_terms = inv_lists[0]
    for term in inv_lists:
        sect_terms = set(sect_terms).intersection(term)
    return sect_terms


# In[129]:

#Calculates the support of every itemset
def GetSup(itemset,par_index,sup_vals,num_docs):
    if tuple(itemset) in d_sup_vals:
        return d_sup_vals[tuple(itemset)]
    inv_lists = []
    for term in itemset:
        inv_lists.append(par_index[term])
    else:
        sup = len(Intersect(inv_lists))/num_docs
        d_sup_vals[tuple(itemset)] = sup
    return sup


# In[130]:

#Determine if two sets need to be joined
def NeedJoin(set1,set2):
    for i in range(0,len(set1)-1):
        if set1[i] != set2[i]:
            return False
    return True


# In[131]:

#Joins two sets
def Join(set1,set2):
    set3 = list(set1)
    set3.append(set2[-1])
    return set3


# In[132]:

#Creates an empty list to fill in with frequent itemsets
def getFreqSets(num_terms):
    freq_itemsets = []
    for i in range(0,num_terms+1):
        temp = []
        freq_itemsets.append(temp)
    return freq_itemsets


# In[133]:

#Saves the rules to a text file
def SaveRules(rules,num_rules):
    file = open('Association Rules.txt','w')
    file.write('Number of rules generated: '+str(num_rules)+'\n')
    for rule in rules:
        file.write(str(rule[0])+' => '+str(rule[1])+'; support='+str(rule[2])+', confidence='+str(rule[3])+'\n')
    file.close()


# In[134]:

#Count the number of crawled documents
def getNumDocs(par_index,path):
    num_docs = 0
    for filename in glob.glob(os.path.join(path,'*.html')):
        num_docs += 1
    return num_docs


# In[135]:

#Load the related terms to be searched
def getRelTerms():
    return ['india','cricket','pakistan','additional','ball','africa','american','test','pitch',            'world','wicket','accepted','tendulkar','player','bowler','australia','bcci','defeats','loss',           'win']


# In[136]:

#Get the top ten association rules:
def getTop(rules):
    top_rules = sorted(rules, key=lambda x:x[2],reverse=True)
    top_rules = top_rules[0:10]
    top_rules = sorted(top_rules, key=lambda x:x[3],reverse=True)
    return top_rules


# In[137]:

#Generate the report for the assignment:
def createReport(rules,num_rules,min_sup,min_conf):
    top_rules = getTop(rules)
    file = open('Association_Report.txt','w')
    file.write('1) This program was developed in Python, and generates a set of Association rules '+'\n')
    file.write('from a provided index file, so as to find useful patterns within the text.'+'\n'+'\n')
    file.write('2) With a minimum support of '+str(min_sup)+' and a minimun confidence of '+str(min_conf)+'\n')
    file.write('the algorithm generated '+str(num_rules)+' Association Rules, of which the top ten are:'+'\n' +'\n')
    for rule in top_rules:
        file.write(str(rule[0])+' => '+str(rule[1])+'; support='+str(rule[2])+', confidence='+str(rule[3])+'\n')
    file.write('\n')
    file.write('3) Overall, decreasing the minimun support or the minimum confidence gave me more association'+'\n')
    file.write('rules, but of a lesser quality. However, having the minimum thresholds be too high led to few rules'+'\n')
    file.write('and at the same time they were so obvious as to be useless. In the end I chose the current'+'\n')
    file.write('thresholds because they appear the ideal combination of quantity and quality.')
    file.close()


# In[138]:

rel_terms = getRelTerms()
min_sup = 0.25
min_conf = 0.7
inv_index = ReadIndex('Frequency Index_Aneesh.txt')
par_index = getPartIndex(inv_index)
d_sup_vals = {}
path = 'Crawled_Pages'+'/'
num_terms = len(rel_terms)
num_docs = getNumDocs(par_index,path)
freq_itemsets = getFreqSets(num_terms)
#Collection of frequent 1-itemsets
for term in rel_terms:
    itemset = [term]
    if GetSup(itemset,par_index,d_sup_vals,num_docs)>min_sup:
        freq_itemsets[1].append(itemset)


# In[139]:

#Find frequent 2 to K-itemsets
for k in range(2,num_terms+1):
    prev_itemsets = freq_itemsets[k-1]
    n = len(prev_itemsets)
    for i in range(1,n-1):
        for j in range(i+1,n):
            set1 = prev_itemsets[i]
            set2 = prev_itemsets[j]
            if NeedJoin(set1,set2):
                set3 = Join(set1,set2)
                if GetSup(set3,par_index,d_sup_vals,num_docs)>min_sup:
                    freq_itemsets[k].append(set3)
    if len(freq_itemsets) == 1:
        break


# In[140]:

#Generate the Association Rules
rules = []
for k in range(2,num_terms+1):
    if not freq_itemsets:
        break
    for itemset in freq_itemsets[k]:
        for i in range(0,k):
            itemset2 = list(itemset)
            itemset2.remove(itemset2[i])
            sup1 = GetSup(itemset2,par_index,d_sup_vals,num_docs)
            sup2 = GetSup(itemset,par_index,d_sup_vals,num_docs)
            conf = sup2/sup1
            if conf>min_conf:
                rule = []
                rule.append(itemset2)
                rule.append(itemset[i])
                rule.append(sup2)
                rule.append(conf)
                rules.append(rule)
num_rules = len(rules)
SaveRules(rules,num_rules)
createReport(rules,num_rules,min_sup,min_conf)


# In[ ]:



