
# coding: utf-8

# In[37]:

import nltk
nltk.download('stopwords','tokenizers')


# In[1]:

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


# In[2]:

#Strip the words in doc of any characters that are not alphabets
def makeVal(word):
    word = word.strip(string.punctuation)
    regex=re.compile('[^a-zA-Z]')
    regex.sub('',word)
    word = word.split()
    out_word=''
    for letter in word:
        if letter.isalpha():
            out_word = out_word+letter
    return out_word


# In[3]:

#return list of words in the file
def getPosTokens(filename):
    file = open(filename,'r')
    html = file.read()
    doc = BeautifulSoup(html,'lxml').get_text()
    #doc = ''
    #for para in soup.find_all('p'):
        #para = para.find_all(text=True)
        #text = ''
        #for line in para:
            #text = text+line+' '
        #doc = doc+text+' '
    doc = doc.lower()
    doc = doc.split(' ')
    tokens = []
    for word in doc:
        word = makeVal(word)
        if len(word)>1 and word != 'html':
            tokens.append(word)
    return tokens


# In[4]:

#return list of words in the file, remove stop words
def getFreqTokens(filename):
    file = open(filename,'r')
    html = file.read()
    doc = BeautifulSoup(html,'lxml').get_text()
    #doc = ''
    #for para in soup.find_all('p'):
        #para = para.find_all(text=True)
        #text = ''
        #for line in para:
           #text = text+line+' '
        #doc = doc+text+' '
    doc = doc.lower()
    doc = doc.split(' ')
    tokens = []
    for word in doc:
        word = makeVal(word)
        if word not in stopwords.words('english') and len(word)>1 and word != 'html':
            tokens.append(word)
    return tokens


# In[5]:

def makeFilePath(path):
    if not os.path.exists(path):
        os.makedirs(path)


# In[6]:

#Alphabetically sort the inverted index
def getSortedList(inv_index):
    sorted_index = []
    for word in inv_index:
        value = str(tuple(inv_index[word]))
        sorted_index.append(word + " : " + value)
    sorted_index = sorted(sorted_index)
    return sorted_index


# In[7]:

#Create the list of unique words in the index
def getUniqueList(inv_index):
    num_uni_words = len(inv_index)
    sorted_index = []
    makeFilePath('Indexer_Aneesh/')
    path = 'Indexer_Aneesh/Vocabulary_Aneesh.txt'
    file = open(path,'w+')
    file.write('Number of unique words: '+str(num_uni_words)+'\n')
    for word in inv_index:
        sorted_index.append(word)
    sorted_index = sorted(sorted_index)
    for entry in sorted_index:
        file.write(entry + '\n')
    file.close()


# In[8]:

#Writes the index to file
def getInvertedIndex(inv_index,name):
    makeFilePath('Indexer_Aneesh/')
    path = 'Indexer_Aneesh/' + name + '.txt'
    file = open(path,'w+')
    sorted_index = getSortedList(inv_index)
    for entry in sorted_index:
        file.write(entry + '\n')
    file.close()


# In[9]:

#Creates the frequency based index
def freqIndex(folder):
    #Create the index storage dictionary
    inv_index = {}
    doc_num = 0
    #Read all the files in the crawled pages folder
    path = folder + '/'
    for filename in glob.glob(os.path.join(path,'*.html')):
        doc_num += 1
        #Create temp dictionary
        d_freq = {}
        #Convert the file to a list of tokens, or words
        tokens = getFreqTokens(filename)
        for word in tokens:
            if word not in d_freq:
                #add the word to the dictionary as a key, with value 0
                d_freq[word]=1
            else:
                #increment the value of the word in dictionary by 1
                d_freq[word]+=1
        #write the values of d_temp to inv_index
        for word in d_freq:
            value = [doc_num,d_freq[word]]
            if word not in inv_index:
                inv_index[word] = []
                inv_index[word].append(value)
            else:
                inv_index[word].append(value)
    #Write the inverted index to file
    getInvertedIndex(inv_index,'Frequency Index_Aneesh')
    getUniqueList(inv_index)
    print('Frequency index created!')


# In[10]:

#Creates the index report
def createReport():
    makeFilePath('Indexer_Aneesh/')
    path = 'Indexer_Aneesh/' + 'Report_Aneesh' + '.txt'
    file = open(path,'w+')
    file.write('This program works by reading the crawled web pages, '+'\n')
    file.write('parsing the text using BeautifulSoup package, '+'\n')
    file.write('and tokenising it, creating a list of words. '+'\n')
    file.write('It then removes the stopwords using the nltk package. '+'\n')
    file.write('Afterword, it creates an index file of all the words '+'\n')
    file.write('and their frequencies. It also creates an index with '+'\n')
    file.write('the positions of the words within the documents.')
    file.close()
    print('Wrote the report!')


# In[ ]:

#Creates the position based index
def posIndex(folder):
    #Create the index storage dictionary
    inv_index = {}
    doc_num = 0
    #Read all the files in the crawled pages folder
    path = folder + '/'
    for filename in glob.glob(os.path.join(path,'*.html')):
        doc_num += 1
        #Convert the file to a list of tokens, or words
        tokens = getPosTokens(filename)
        #Get the postion of the word in the file
        word_pos = 0
        for word in tokens:
            value = str(tuple([doc_num,word_pos]))
            if word not in stopwords.words('english'):
                if word not in inv_index:
                    #add the word to the dictionary as a key, with first position
                    inv_index[word]= []
                    inv_index[word].append(value)
                else:
                    #add the current postion to index
                    inv_index[word].append(value)
                #increment word position
                word_pos += 1
            else:
                continue
                #increment word position
                word_pos += 1
    #Write the inverted index to file
    getInvertedIndex(inv_index,'Position Index_Aneesh')
    print ('Position index created!')


# In[ ]:

freqIndex('Crawled_Pages')
posIndex('Crawled_Pages')
createReport()


# In[ ]:



