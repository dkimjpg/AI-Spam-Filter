############################################################
# CMPSC442: Classification
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import email.iterators
#import email.policy
import math
import os, os.path
#import collections
from collections import Counter

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokenList = []
    #policy = email.policy.EmailPolicy(utf8=True)

    openMessage = open(email_path, encoding="utf8") #without this, none of the other email methods work. Would've been good to know beforehand.
    emailMessage = email.message_from_file(openMessage) 

    for part in email.iterators.body_line_iterator(emailMessage): #traverses the message line by line, and each line is an str
        line = part.split() #part is an str, so it can be split into a list
        tokenList.extend(line)
    return tokenList
    #pass

def log_probs(email_paths, smoothing):
    #need to build a dictionary and fill the values with calculations
    #floatSmoothing = float(smoothing) #converts string for smoothing into a float, if it is not already a float
    probDict = {}
    fullTokenList = []
    for path in email_paths:
        #print(f'path: {path}')
        emailTokenList = load_tokens(path)
        fullTokenList.extend(emailTokenList)
    fullTokenSet = set(fullTokenList)
    sigmaCount = len(fullTokenList)     #this is the value of Sigma count(w')
    fullCount = len(fullTokenSet)       #this is the value of |V|
    #print(sigmaCount)
    #print(fullCount)

    #From here, I should iterate through emailTokenList and run the Laplace probabilities and put the results in a dictionary (if the key is not already in the dictionary, I think)
    # Ok, so count(w) is just the number of occurances of a single word, which I already knew.
    # But |V| is the count of all unique words, while Sigma count(w') is just the length of the entire list (or in other words, the count of EVERY word, whether it's unique or not).
    # And a (which is really alpha) is just the smoothing var.
    
    #Use Counter() from collections for a faster token count. The old code that iterated through the list I created
    # and then used .count() to count the total number of tokens took minutes to execute, but using Counter() to create
    # a Counter object and then putting the entire fullTokenList into it sped up the entire counting process to take only
    # seconds to execute. A Counter object is basically a dictionary that's optimized for counting, anyway, so I just needed
    # to convert it into a dict object.
    fastCount = Counter()
    fastCount.update(fullTokenList)
    fastCount = dict(fastCount)

    for token in fastCount:
        tokenCount = fastCount.get(token) #this is the value of count(w)
        calcProb = (tokenCount + smoothing) / (sigmaCount + (smoothing * (fullCount + 1))) #this is the equation for P(w)
        calcProb = math.log(calcProb)
        probDict.update({token: calcProb})

    #old code that I wrote before I learned how to use Counter() for a faster count(w)
    """
    for token in fullTokenSet: #if this doesn't work well, use fullTokenList
        #print(token)
        tokenCount = fullTokenList.count(token) #this is the value of count(w)
        #print(token)
        calcProb = (tokenCount + smoothing) / (sigmaCount + (smoothing * (fullCount + 1))) #this is the equation for P(w)        
        #print(calcProb)
        sumCount = sumCount + calcProb
        calcProb = math.log(calcProb)
        #print(f'calcProb: {calcProb}')
        probDict.update({token: calcProb})
    """

    #doing the calculations for <UNK> and adding it to the probDict
    calcUNK = smoothing / (sigmaCount + (smoothing * (fullCount + 1)))                     #this is the equation for P(<UNK>)
    calcUNK = math.log(calcUNK)    
    probDict.update({"<UNK>": calcUNK})
    return probDict
    #pass

def countFilesInDir(dir): #counts the number of files in a directory, and returns the number
    return len(os.listdir(dir))
    #return len([name for name in os.listdir('.') if os.path.isfile(name)])

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spamDirList = [spam_dir + "/" + directory for directory in os.listdir(spam_dir)]
        hamDirList = [ham_dir + "/" + directory for directory in os.listdir(ham_dir)]
        self.spamDict = log_probs(spamDirList, smoothing)
        self.hamDict = log_probs(hamDirList, smoothing)
        spamCount = countFilesInDir(spam_dir)
        hamCount = countFilesInDir(ham_dir)

        spamSum = sum(self.spamDict.values())
        #hamSum = sum(self.hamDict.values())
        #for x in self.spamDict:
            #spamSum = spamSum + self.spamDict[x]
        #for x in self.hamDict:
            #hamSum = hamSum + self.hamDict[x]
        
        #calcSpamProb = spamSum / spamCount
        #calcHamProb = hamSum / hamCount

        calcSpamProb = float(spamSum) / (spamCount + hamCount)
        #calcHamProb = float(hamSum) / (spamCount + hamCount)

        """
        #calcSpamProb = (spamCount + smoothing) / ((spamCount + hamCount) + (smoothing * (spamCount + 1)))
        #calcHamProb = (hamCount + smoothing) / ((spamCount + hamCount) + (smoothing * (hamCount + 1)))
        
        #calcSpamProb = (spamCount + smoothing) / ((spamCount + hamCount) + spamCount)
        #calcHamProb = (hamCount + smoothing) / ((spamCount + hamCount) + hamCount)
        """

        self.spamProb = calcSpamProb
        #self.hamProb = calcHamProb
        #pass
    
    def is_spam(self, email_path):
        spamCount = 0
        hamCount = 0
        fullTokenList = load_tokens(email_path)

        #While going through the entire list of tokens, look at each word and see if it is in the spamDict or the hamDict.
        # If a token is in the spamDict, get the value of the token in spamDict and add it to spamCount, otherwise get the
        # value of <UNK> and add it to spamCount.
        # The same should apply for hamCount, check if the token is in hamDict, get value of token in hamDict if it is in
        # hamDict, otherwise, get the value of <UNK> if token is not in hamDict. Whatever the value is, add it to hamCount.
        for token in fullTokenList: 
            checkSpamDict = self.spamDict.get(token)
            if checkSpamDict == None: #if token is not in spamDict, get value of <UNK>
                checkSpamDict = self.spamDict["<UNK>"]
            spamCount = spamCount + checkSpamDict
            
            checkHamDict = self.hamDict.get(token)
            if checkHamDict == None: #if token is not in hamDict, get value of <UNK>
                checkHamDict = self.hamDict["<UNK>"]
            hamCount = hamCount + checkHamDict
        
        #Compare the spamCount and hamCount now that the results have been received
        # A larger spamCount suggests that it is more likely that the email is spam, so return True.
        # But a larger hamCount suggests that it is more likely that the email is not spam, so return False.
        # In the future, I might want to change this to be more of a ratio type comparison, since there
        # could be some instances where having a slightly smaller spamCount compared to hamCount may not be
        # good evidence for concluding that an email is not spam. But this is a naive model for a spam filter,
        # so I guess this might be intentional?
        if spamCount > hamCount: 
            return True
        else:
            return False
        #pass

    def most_indicative_spam(self, n):
        #Since the restriction is set to tokens that appear at least once in both spam and ham (spamDict and hamDict), 
        # I'll need to do something that takes the intersection of both sets. But I don't actually want to make new sets
        # again, so I'll try something else.

        intersectKeys = self.spamDict.keys() & self.hamDict.keys()
        spamIntersectDict = {key: self.spamDict[key] for key in intersectKeys}

        indicateDict = {}
        for token in spamIntersectDict: 
            checkSpamDict = self.spamDict.get(token)
            if checkSpamDict == None: #if token is not in spamDict, get value of <UNK>
                checkSpamDict = self.spamDict["<UNK>"]
            #spamCount = spamCount + checkSpamDict
            
            checkHamDict = self.hamDict.get(token)
            if checkHamDict == None: #if token is not in hamDict, get value of <UNK>
                checkHamDict = self.hamDict["<UNK>"]
            #hamCount = hamCount + checkHamDict
            spamCalc = checkSpamDict - checkHamDict
            indicateDict.update({token: spamCalc})
        #print(indicateList)
        indicateCounter = Counter(indicateDict)
        indicateValues = indicateCounter.most_common(n) #gets the n most indicative words in descending order
        finalIndicateDict = dict(indicateValues)
        finalValues = list(finalIndicateDict.keys())
        return finalValues

        """
        #print(type(spamIntersectDict))
        #print(spamIntersectDict)
        #spamIntersectDict = dict.fromkeys(intersectKeys, self.spamDict.get())
        spamCounterDict = Counter(spamIntersectDict)#Counter(self.spamDict) #= Counter(intersectKeys)
        #print(spamCounterDict)
        hamIntersectDict = {key: self.hamDict[key] for key in intersectKeys}
        hamCounterDict = Counter(hamIntersectDict)
        x = list(spamCounterDict.most_common(n))
        y = list(hamCounterDict.most_common(n))
        print(x)
        print(y)
        """

        #pass

    def most_indicative_ham(self, n):
        #same code as most_indicative_spam, but with a few changes from spam to ham for some variables
        
        intersectKeys = self.spamDict.keys() & self.hamDict.keys()
        hamIntersectDict = {key: self.hamDict[key] for key in intersectKeys}

        indicateDict = {}
        for token in hamIntersectDict: 
            checkSpamDict = self.spamDict.get(token)
            if checkSpamDict == None: #if token is not in spamDict, get value of <UNK>
                checkSpamDict = self.spamDict["<UNK>"]
            
            checkHamDict = self.hamDict.get(token)
            if checkHamDict == None: #if token is not in hamDict, get value of <UNK>
                checkHamDict = self.hamDict["<UNK>"]
            hamCalc = checkHamDict - checkSpamDict
            indicateDict.update({token: hamCalc})
        indicateCounter = Counter(indicateDict)
        indicateValues = indicateCounter.most_common(n)
        finalIndicateDict = dict(indicateValues)
        finalValues = list(finalIndicateDict.keys())
        return finalValues
        #pass



#####################################################
# Test Cases
#####################################################
"""
print("Question 1\n")

ham_dir = "homework5_data/train/ham/"
print(load_tokens(ham_dir+"ham1")[200:204])
#print(load_tokens(ham_dir+"ham1"))
print(load_tokens(ham_dir+"ham2")[110:114])
spam_dir = "homework5_data/train/spam/"
print(load_tokens(spam_dir+"spam1")[1:5])
print(load_tokens(spam_dir+"spam2")[:4])

print("\nQuestion 2\n")

paths = ["homework5_data/train/ham/ham%d" % i for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["the"])
print(p["line"])


print("")
paths = ["homework5_data/train/spam/spam%d" % i for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["Credit"])
print(p["<UNK>"])

print("\nQuestion 4\n")
sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
print(sf.is_spam("homework5_data/train/spam/spam1"))
print(sf.is_spam("homework5_data/train/spam/spam2"))

sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",  1e-5)
print(sf.is_spam("homework5_data/train/ham/ham1"))
print(sf.is_spam("homework5_data/train/ham/ham2"))

print("\nQuestion 5\n")
sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",  1e-5)
print(sf.most_indicative_spam(5))
sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",  1e-5)
print(sf.most_indicative_ham(5))

"""