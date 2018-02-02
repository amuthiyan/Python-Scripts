
# coding: utf-8

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


# In[2]:

#Get Seed URLs and URLs from the seed URL
def getQueue(url_lst):
    q = queue.Queue()
    for url in url_lst:
        r = requests.get("http://" + url)
        data = r.text
        soup = BeautifulSoup(data,"lxml")
        for link in soup.find_all('a'):
            link = link.get('href')
            if link!=None:
                q.put(link)
    return q


# In[3]:

#Determine if page is relevant (before downloading)
def classRel(url,html,rel_list):
    soup = BeautifulSoup(html,"lxml")
    text = soup.get_text()
    text=text.lower()
    rel_count=0
    for item in rel_list:
        item=item.lower()
        if item in text:
            rel_count += 1
        else:
            continue
    if rel_count>=2:
        return True
    else:
        return False


# In[4]:

#Make sure the url is valid before crawling
def makeVal(url):
    if 'redlink' in url:
        return None
    name = getName(url)
    name = re.sub("[^a-zA-Z]","",name)
    if name == None:
        return None
    try:
        if '#' in url:
            return None
        elif url[1]=='w':
            url = "http://en.wikipedia.org" + url
            return url
        else:
            return None
    except IndexError:
        print ("bad page name")


# In[5]:

#Create a valid file name for the downloaded page
def getName(url):
    name = url.split('/')[-1]
    if '.' in name:
        name = name.split('.')[0]
    return name


# In[6]:

#Download pages from the urls in the queue
def getPage(url,rel_list,path):
    html = urlopen(url).read()
    name = getName(url)
    try:
        if classRel(url,html,rel_list):
            file = open(path+name+'.html',"w")
            file.write(str(html))
            file.close()
            file_vis = open('Report_Crawler.txt','a')
            file_vis.write(url + '\n')
    except OSError as e:
        print (e)


# In[7]:

#Get the relevant search terms from the user
def getRelList():
    rel_list = []
    counter = 0
    b = True
    while b==True:
        term = input('Enter a search term(Leave blank to end): ')
        if term=="" and counter>=2:
            b=False
        elif term=="" and counter<2:
            print('You need at least 2 search terms')
            continue
        else:
            rel_list.append(term)
            counter+=1
    return rel_list


# In[8]:

#Get the Seed URLs fromt the user
def getSeeds():
    seed_URLs = []
    counter = 0
    b = True
    while b==True:
        term = input('Enter a seed URL(Leave blank to end):')
        if term=="" and counter>=1:
            b=False
        elif term=="" and counter<1:
            print('You need at least 1 seed URL')
            continue
        else:
            seed_URLs.append(term)
            counter+=1
    return seed_URLs


# In[9]:

def makefile(path):
    if not os.path.exists(path):
        os.makedirs(path)


# In[10]:

#below lists are hard-coded seed urls and relevant terms
seed_URLs = ['en.wikipedia.org/wiki/Cricket','en.wikipedia.org/wiki/Cricket_World_Cup']
rel_list = ['kapil','kohli','Dhoni','test','pitch','t20','world cup','wicket','ganguly','tendulkar']
#Below functions can be activated if user input is desired.
#seed_URLs = getSeeds()
#rel_list = getRelList()
q=getQueue(seed_URLs)
vis_URLs = []
#Create a folder to put the crawled pages in
path = "Crawled_Pages/"
makefile(path)
#Create the report of the crawled pages
file_vis = open('Report_Crawler.txt','w')
file_vis.write('Topic: Cricket in India')
file_vis.write('Seed URLs: ')
for url in seed_URLs:
    file_vis.write(url + ', ')
file_vis.write('\n')
file_vis.write('Related Terms: ')
for term in rel_list:
    file_vis.write(term + ', ')
file_vis.write('\n')
file_vis.write("This crawler works by utilizing the urllib library to go to the webpage,")
file_vis.write('\n')
file_vis.write("then using the package BeautifulSoup to create a queue of urls,") 
file_vis.write('\n')
file_vis.write("and then save the pages to the crawled collection")
file_vis.write('\n')
file_vis.write('URLs visited by the crawler:' + '\n')
file_vis.close()
#Crawl all the URLs in the queue
while not q.empty():
    url = q.get()
    url = makeVal(url)
    if url != None and url not in vis_URLs:
        getPage(url,rel_list,path)
        vis_URLs.append(url)
    else:
        continue
#Add the number of crawled pages to the report
file_vis = open('Report_Crawler.txt','r')
rep_lines = file_vis.readlines()
num_lines = len(rep_lines)
file_vis.close()
file_vis = open('Report_Crawler.txt','a')
file_vis.write('Number of files crawled = ')
file_vis.write(str(num_lines-6))
file_vis.close()
print('All Done!')


# In[ ]:



