
# Justin Alexis
# stuId: 89335275
# netId: jmalexis
#
# Assignment 1
# Part A
#
# General Constraints and Notes
# Important: At certain points, the assignment may be
# underspecified, this is by design, simply explain your
# assumptions and defend them.
# 
# Exceptions: handle exceptions for bad inputs
#             ex. different languages, undefined chars
# 
# Input Note: get file names from cmd line args
#
# Testing: Test the code at the uci.ics labs in discussion
# 
# COMPLEXITY: all time complexities are gathered and certified
#             from the python documentation


# import sys to get info from the cmd line arguments
import sys
# import regular expressions to help process text
import re
# import defaultdict to make it easier to create a dict
# Might not be used, (see COMPLEXITY sections)
from collections import defaultdict


from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# Method / Function    -- tokenize
# List<Token> tokenize(textFilePath)
#
# summary: parameter is a file (alphanumeric characters)
#          returns a list of tokens in that file.
#          Must handle bad characters gracefully
#          Note: encoding = 'utf8'
#
# COMPLEXITY: technically O(N)
#             where N are the NUMBER OF LINES in the file.
#             AND N is never entirely stored into memory (readlines())
#             
#             See COMPLEXITY section for how they were modified to
#             be more efficient

def tokenize(textFilePath):
    
    ps = PorterStemmer()
    
    # first, we should probably open the file
    # COMPLEXITY: opening a file is O(1)
    reStringList = []
    stopList = []
    [reStringList.append(ps.stem(i.lower())) for i in re.findall(r'([a-zA-Z0-9]+)' , textFilePath) if ((i.lower() not in stopList)) ]
    

    return reStringList
        


# Method / Function    -- computeWordFrequencies
# Map<Token, Count> computeWordFrequencies(tokenList)
#
# summary: the compute function calculates the number of
#          values in the tokenList. Uses a dict because
#          it will be nice for hashing later
#
# COMPLEXITY: Time complexity theta(n)
#             The reason is that you only iterate over tokenList once
#             Otherwise, the dict simply hashes the values for you
#             More information on the time complexity of setdefault below 

def computeWordFrequencies(tokenList):
    tokenDict = {}

    # iterate through tokenList

    for i in tokenList:

        # COMPLEXITY: the time complexity of setdefault is O(1)
        # thus, it is better to use setdefault over defaultdict
        # because you will eventually need to convert defaultdict
        # into a dict, which increases time complexity

        if (tokenDict.setdefault(i, None) == None):
            tokenDict[i] = 1
        else:
            tokenDict[i] += 1
    return tokenDict


# Method / Function    -- printTokens (Note: TA said it was fine to alter name)
# Map<Token, Count> computeWordFrequencies(tokenList)
#
# summary: prints out the frequencies of tokens based 
#          on the highest-to-lowest frequency
#
# COMPLEXITY: the complexity is theta(n) because sorted() properly
#             abuses lambda while sorting, not to mention,
#             we can tag sorted() with reverse

def printTokens(frequencies):

    # NOTE: sorted() does not sort, then resort to account for the lambda and reverse function
    # Thus the function is theta(n)
    for (k,v) in sorted(frequencies.items(),key = lambda x:(x[1]), reverse = True):
        print(str(k) + " = " + str(v))


# Note: For testing only, run this file 
#       Otherwise, these lines will not print or be run



#print(sys.argv[1])
#print(tokenize(sys.argv[1]))
#print(computeWordFrequencies(tokenize(sys.argv[1])))
#printTokens(computeWordFrequencies(tokenize(sys.argv[1])))
