# Justin Alexis
# 89335275

import gc
import os
import json
import linecache
import re
import math
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from PartAm1 import *



# create a global index for hashing
# this way we do not mix up documents and their hash
# regardless of what directory you are searching

hashIndex = 0  # hashIndex = also number of unique documents
searchDir = "DEV"
invertedIndexLength = 0 # length of the Inverted Index
reportCounter = 0 # count of total files made to write to


# parameters: Documents, inverted List to add everything to
# We include a second section for inverted List (hashMap) because
# it enables us to continue using the inverted List on
# separate sets of documents. This separates our concerns.

# this is the general outline/theory of the inverted index but NOT what was used

# NOT USED, GO TO NEXT FUNCTION
def buildInvertedIndex(documents: list, invertedIndex: dict = {}) -> dict :
    global hashIndex
    
    for docs in documents:
        hashIndex += 1
        
        for tokeni in docs:
            
            # check if hashDict contains token, if not set equal to empty list
            if (invertedIndex.setdefault(i, None) == None):
                invertedIndex[tokeni] = []
            
            # always add where the word is stored, do not use else-statement
            invertedIndex[tokeni].append(Postings(hashIndex, count))
        
    return invertedIndex


# searches for documents through the directory, essentially skipping a step
# THIS WAS USED in the final product.

def buildInvertedIndexReal(dirPaths: str, invertedIndex: dict = {}) -> dict :
    global hashIndex
    global searchDir
    global invertedIndexLength
    global reportCounter
    
    docs = 0
    
    try:
        for file in os.listdir(searchDir + "/" + dirPaths):
            with open(searchDir+ "/" + dirPaths + "/" + file,"r") as tempJson:
                #print(json.load(tempJson))

                hashIndex += 1
                
                tempDict = json.load(tempJson)
                
                
                
                # create a file where you contain the documentID to URL
                hashWrite(hashIndex, tempDict['url'])

                bs = BeautifulSoup(tempDict['content'], "lxml")
                #print(bs.prettify())
                jsonDict = getHeaders(bs)
                
                    
                    
                    
                
                bsContent = bs.get_text(separator=' ')
                
                # dict of words in each document
                content = computeWordFrequencies(tokenize(bsContent))
                #print(content)
                
                for (tokeni, count) in content.items():

                    # check if hashDict contains token, if not set equal to empty list
                    if (invertedIndex.setdefault(tokeni, None) == None):
                        invertedIndexLength += 1
                        invertedIndex[tokeni] = []

                    # always add where the word is stored, do not use else-statement
                    fieldsOfToken = []
                    if (tokeni in jsonDict):
                        fieldsOfToken = jsonDict[tokeni]
                    positionsOfToken = [p.start() for p in re.finditer(tokeni, bsContent)]
                    invertedIndex[tokeni].append(Postings(hashIndex, math.log(1+count), fieldsOfToken, positionsOfToken))
                
                # if there are too many documents, in a subfolder, then write them to disk early
                docs += 1
                if (docs >= 40):
                    batchWrite(reportCounter, invertedIndex)
                    invertedIndex.clear()
                    gc.collect()
                    docs = 0
                    reportCounter += 1
            
    except IsADirectoryError:
        pass
        # WE NEED 2 exception catchers.
        # this is because it allows us to search mutliple directories
        # and catch exceptions without interrupting the tokenizing/hashing
        # process when in a different directory, thus skipping it accidentally
        # due to the caught error.
    
    
    
        
    return invertedIndex

# This function obtains the headers of all the important words

def getHeaders(bs):
    
    jsonDict = {}
    prioFields = ["h1", "h2","h3", "h4","h5", "h6", "strong"]
    for i in prioFields:
        jsonStringFinder = '^' + i + '$'
        
        jsonTempList = tokenize(str(bs.find_all(re.compile(jsonStringFinder))))
        for j in jsonTempList:
            if (jsonDict.setdefault(j, None) == None):
                jsonDict[j] = []
            if (i not in jsonDict[j]):
                jsonDict[j].append(i)
    return jsonDict

# simply write the index and url to a file, this way we know which index goes to 
# which document

def hashWrite(hashIndex, url):
    hashIndexWriter = open('indexToURL.txt','a')
    hashIndexWriter.write(str(hashIndex) + ":" + str(url) + "\n")
    hashIndexWriter.close()
    return

# Here we write the SORTED current inverted Index to a file
# this will find where the value belongs and insert the postings at the end

def batchWrite(fileNum, tempInvertedIndex):
    
    fileName = "report" + str(fileNum) + ".txt"
    with open(fileName,'w+') as file:
        for (k,v) in sorted(tempInvertedIndex.items()):
                file.write( str(k) + ":" + str(v) + "\n")
    return
        
    # NOTE: this code is for experimentation purposes only
    """
    line = file.readline()

    # SORT THE CURRENT Inverted Index and store into  tempInvertedIndex

    tempInvertedIndex = sorted(invertedIndex.items())

    # IF the file is empty, insert basic objects
    # NOTE: should always be empty, but checks just in case
    # this is because w+ truncates the file (deletes original)

    if ( not line ):
        for (k,v) in tempInvertedIndex:
            file.write( str(k) + ":" + str(v) + "\n")
        return

    while (line and len(tempInvertedIndex) != 0 and line != "\n"):

        # decipher lines
        print("line:" + str(line))
        match = re.search(r':', line)


        # get number of bytes the line is, just in case we need to go seek backwards
        bytesOfLine = len(line)
        mspan = match.span()
        currentWord = line[0:mspan[0]]

        print(tempInvertedIndex)
        print("currentWord:" + currentWord)
        print(currentWord < tempInvertedIndex[0][0])
        if (currentWord > tempInvertedIndex[0][0]):
            #print("tell:" + file.tell() + " bytes:" + bytesOfLine)

            file.write("inserted:Greater Than\n")
            tempInvertedIndex.pop(0)
        elif (currentWord == tempInvertedIndex[0][0]):

            # decipher the file to and convert Postings() object 
            # to a real object using eval()
            wordToPosting = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")

            postings = [eval(i) for i in wordToPosting]


            # remove word from argv so that way the loop will end early if all
            # the words have found their postings

            file.write("inserted:Equals\n")

            tempInvertedIndex.pop(0)

        line = file.readline()

    if (len(tempInvertedIndex) != 0):
        for (k,v) in tempInvertedIndex:
            file.write( str(k) + ":" + str(v) + "\n")
    """  
def mergeReports(reportCount):
    
    continueMerging = True
    mergeList = None
    currentMergeWord = None
    currentMergePosting = []
    deleteMergeIndex = []
    mergeNone = False
    
    while (continueMerging):
        
        
        
        continueMerging = False
        if (mergeList == None):
            mergeList = []
            for i in range(0, reportCount):
                fileName = "report" + str(i) + ".txt"
                with open(fileName,'r') as file0:
                    line = file0.readline()

                    # check if line exists
                    if (line and line != "\n"):
                        continueMerging = True
                    else:
                        mergeList.append([None, None])
                        continue

                    # parse txt file with words and Postings
                    match = re.search(r':', line)
                    mspan = match.span()
                    currentWord = line[0:mspan[0]]

                    currentMergePosting = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
                    mergeList.append([currentWord, [eval(x) for x in currentMergePosting]])
                
        else:
            for i in range(0,reportCount):
                fileName = "report" + str(i) + ".txt"
                
                currentWord = mergeList[i][0]
                
                if (currentWord != None):
                    
                    if (currentMergeWord == None ):
                        currentMergeWord = currentWord
                        currentMergePosting = mergeList[i][1]

                        deleteMergeIndex.append(i)
                    else:
                        postings =  mergeList[i][1]
                        
                        if (currentMergeWord == currentWord):
                            [currentMergePosting.append(tempPosting) for tempPosting in postings]
                            deleteMergeIndex.append(i)
                        elif (currentMergeWord > currentWord):
                            deleteMergeIndex = [i]
                            currentMergeWord = currentWord
                            currentMergePosting = mergeList[i][1]
                '''
                with open(fileName,'r') as file1:

                    line = file1.readline()

                    # check if line exists
                    if (line and line != "\n"):
                        continueMerging = True
                    else:
                        continue

                    # parse txt file with words and Postings
                    match = re.search(r':', line)
                    mspan = match.span()
                    currentWord = line[0:mspan[0]]

                    # Compare the current posting to the other postings.
                    # This is easy because everything is presorted.

                    if (currentMergeWord == None ):
                        currentMergeWord = currentWord
                        currentMergePosting = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
                        currentMergePosting = [eval(i) for i in currentMergePosting]
                        deleteMergeIndex.append(i)
                    else:
                        postings = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
                        postings = [eval(i) for i in postings]
                        if (currentMergeWord == currentWord):
                            [currentMergePosting.append(tempPosting) for tempPosting in postings]
                            deleteMergeIndex.append(i)
                        elif (currentMergeWord > currentWord):
                            deleteMergeIndex = [i]
                            currentMergeWord = currentWord
                            currentMergePosting = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
                    '''
        # delete first line of files that were detected and written to the final file    
        for i in range(0, reportCount):
            if (i in deleteMergeIndex):
                fileName = "report" + str(i) + ".txt"
                with open(fileName,'r') as file1:
                    replaceFile = file1.read().splitlines(True)
                    
                with open(fileName, 'w') as file2:
                    file2.writelines(replaceFile[1:])
                with open(fileName,'r') as file3:
                    line = file3.readline()
                    
                    if (line and line != "\n"):
                        continueMerging = True
                    else:
                        mergeList[i] = [None,None]
                        continue
                    
                    match = re.search(r':', line)
                    mspan = match.span()
                    
                    mergeList[i][0] = line[0:mspan[0]]
                    postings = line[mspan[1]:].lstrip("[").rstrip("]\n").split(", ")
                    mergeList[i][1] = [eval(x) for x in postings]
                    
                    
        
        # APPEND posting to the end of the reportFinal.txt
        with open("reportFinal.txt",'a') as fileOutput:
            if (mergeNone == True):
                fileOutput.write(str(currentMergeWord) + ":" + str(currentMergePosting) + "\n")
            else:
                mergeNone = True
                
        # reset for while loop or exit loop
        if (continueMerging == False):
            break
        
        deleteMergeIndex = []
        currentMergePosting = []
        currentMergeWord = None
        
        breakOutMerge = True
        for i in mergeList:
            if (i != None):
                breakOutMerge = False
        if (breakOutMerge):
            print("finished Merge")
            break
        
        
class Postings:
    def __init__(self, id, count, fields = [], positions = []):
        self.id = id
        self.count = count
        self.fields = fields
        self.positions = positions[:5]
        
    def __repr__(self):
        return "Postings({0},{1},{2},{3})".format(self.id, self.count, str(self.fields).replace(" ",""), str(self.positions).replace(" ",""))

    def __str__(self):
        return "Postings({0},{1},{2},{3})".format(self.id,self.count, str(self.fields).replace(" ",""), str(self.positions).replace(" ",""))

    
if __name__ == "__main__":
    
    
    # IMPORTANT FOR RUNNING:
    #
    # NOTE: execute this in the same directory as the ANALYST or DEV file.
    # I am using ANALYST to test, simply switch to DEV if u want DEV
    
    count = 0
    
    # clear contents of some files before starting, this ensures we always start from an empty file
    open('indexToURL.txt','w').close()
    open("reportFinal.txt",'w').close()
    
    invertedIndex = {}
    writeCounter = 0
    
    totalDocuments = 0
    
    for dirPaths in os.listdir(searchDir):
        print(dirPaths)
        try:
            
            invertedIndex = buildInvertedIndexReal(dirPaths, invertedIndex)
            totalDocuments += len(invertedIndex)
            
            writeCounter += 1
            if (writeCounter >= 2):
                # Here we write the current InvertedIndex to a file, this way, our index does not
                # become too big for memory!!
                # batchWrite writes the invertedIndex to a NEW separate file,
                # then we set the invertedIndex to 

                batchWrite(reportCounter, invertedIndex)
                reportCounter += 1

                # NOTE ON CLEARING and GARBAGE COLLECTION:
                # memory is deleted from python when there are no references to that memory space
                # thus, this may not instantly delete the memory, BUT it will eventually because
                # there are no other references to the data
                invertedIndex.clear()
                gc.collect()
                writeCounter = 0
            
        except IsADirectoryError: 
            print(searchDir + " contained an invalid directory, continuing")
    
    if (writeCounter != 0):
        batchWrite(reportCounter, invertedIndex)
        invertedIndex.clear()
        gc.collect()
    
    print("totalDocuments:", totalDocuments)
    '''
    output = open('report.txt','a')
    print("hashIndex:", hashIndex)
    for (k,v) in invertedIndex.items():
        output.write( str(k) + ":" + str(v) + "\n")
    output.close()
    '''
    mergeReports(reportCounter)