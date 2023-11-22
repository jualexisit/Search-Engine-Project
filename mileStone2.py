
import os
import json
import re
import time
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from PartAm1 import *
from mileStone1 import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# format of input 
#
# uniqueWork: [Posting(id, count), . . .]

prioFields = ["h1", "h2","h3", "h4","h5", "h6", "strong"]


t0 = time.time()
ps = PorterStemmer()
argc = len(sys.argv)

# IMPORTANT
#
# here we lowercase all values in the search and then stem them

argv = sorted([ps.stem(i.lower()) for i in sys.argv[1:]])


searchMap = {}

# search this file
with open('report1.txt','r') as file:
    
    # get line one by one
    line = file.readline()
    
    # iterate until everything is searched
    while (line and argv):
        
        # decipher lines
        match = re.search(r':', line)
        mspan = match.span()
        currentWord = line[0:mspan[0]]
        
        if (currentWord == argv[0]):
            
            # decipher the file to and convert Postings() object 
            # to a real object using eval()
            wordToPosting = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
        
            postings = [eval(i) for i in wordToPosting]
            searchMap[currentWord] = postings
            
            # remove word from argv so that way the loop will end early if all
            # the words have found their postings
            
            argv.pop(0)
            
        
        line = file.readline()

tempHashMapSet = {}
allPosts = {}
for (k , posts) in searchMap.items():
    tempHashMapSet[k] = set([i.id for i in posts])
    for p in posts:
        if allPosts.setdefault(p.id, None) == None:
            allPosts[p.id] = [p.count, len(p.fields), p.positions]
        else:
            allPosts[p.id][0] += p.count
            allPosts[p.id][1] += len(p.fields)
            allPosts[p.id][2] += p.positions
totalSet = set()
for v in tempHashMapSet.values():
    if not (totalSet):
        totalSet = v
    else:
        totalSet = totalSet.intersection(v)



# Get the largest counted values from the query
getURLDict= {}
counterOfSet = 0

for (k,(a,b,c)) in sorted(allPosts.items(),key = lambda x:(x[1][1], x[1][0]), reverse = True):
    if (counterOfSet == 5):
        break
    counterOfSet += 1
    getURLDict[k] = v

#print the URLS, get values of document IDs from disk
with open('indexToURL.txt') as indexUrl:
        currentIndex = 0
        
        indexLine = indexUrl.readline()
        
        while (indexLine):
            
            if (currentIndex in getURLDict.keys()):
                match = re.search(r':', indexLine)
                mspan = match.span()
     
                # Print the URLS here
                print(indexLine[mspan[1]:])
            
            currentIndex += 1
            indexLine = indexUrl.readline()
        
        


t1 = time.time()
print("time:" + str(t1-t0))