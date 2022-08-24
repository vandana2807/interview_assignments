from PrefixTree import *
from GeneralizedSuffixTree import *
from ModernDictionary import *
import re

def preProcessText(s):
    s=(re.sub("[^a-zA-Z]+", "",s))
    s=s.lower()
    return s
    
test_tree=ModernDictionary()
file=open("input.txt","r")
for f in file.readlines():
    word=preProcessText(f.rstrip('\n'))
    #word=preProcessText(f.rstrip('\n'))
    test_tree.insertWord(word)
test_tree.calculateAndCacheCounts()
file.close()

fileop=open("operations.txt","r")
fileres="res.txt"
for f in fileop.readlines():
    op=f.rstrip('\n')
    #please make sure to remove rstrip part as per txt file you are giving as input
    word=preProcessText(op.split(" ")[1].rstrip('\n'))
    #word=preProcessText(op.split(" ")[1])
    r=test_tree.processOperations(op.split(" ")[0],word)
    res=open(fileres, "a") 
    res.write(str(r))
    res.write("\n")
    res.close()
fileop.close()    
