from GeneralizedSuffixTree import *
from PrefixTree import *
import re
class ModernDictionary:
    def __init__(self):
        self.wordBuffer=[]
        self.lastWordIdx=-1 
        self.trie=PrefixTree()
        self.suffixTree=GeneralizedSuffixTree()
   
    def insertWord(self, word):
        if not self.trie.wordExists(word):
            self.wordBuffer.append(word)
            self.lastWordIdx+=1;
            self.trie.insert(word)
            self.suffixTree.insert(word,self.lastWordIdx)
    def calculateAndCacheCounts(self):
            self.suffixTree.computeCount()
            self.suffixTree.computeSuffixCount()
            
    
    def processOperations(self , op, arg):
        #print(op,arg)
        #arg=preProcessText(arg)
        if op=="S1": 
            return self._searchPrefix(arg)
            
        elif op=="S2": 
            return self._searchSuffix(arg)

        elif op=="S3": 
            return self._searchSubstring(arg)
            
        elif op=="S4": 
            return self._searchChar(arg)
            
        elif op=="C1": 
            return self._countPrefix(arg)
            
        elif op=="C2": 
            return self._countSuffix(arg)
            
        elif op=="C3": 
            return self._countSubstring(arg)
            
        elif op=="C4": 
            return self._countChar(arg)
        
    def _searchPrefix(self, prefix):
        return self._vectostring(self.trie.prefixWordList(prefix))
        
    
    def _countPrefix(self,prefix):
        #print(self.trie.prefixWordCount(prefix))
        return self.trie.prefixWordCount(prefix)
    
    def _searchSuffix(self, suffix):
        #print("_searchSuffix")
        wordIndexes = self.suffixTree.searchSuffix(suffix)
        #print("wordIndexes",wordIndexes)
        wordIndexes=sorted(wordIndexes)
        #print("wordIndexes",wordIndexes)
        suffixWords = []
        #sorted(wordIndexes)
        for i in wordIndexes:
            suffixWords.append(self.wordBuffer[i])
        return self._vectostring(suffixWords)
    
    def _searchSubstring(self, substr):
        wordIndexes = self.suffixTree.search(substr)
        substrWords = []
        wordIndexes=sorted(wordIndexes)
        for i in wordIndexes:
            substrWords.append(self.wordBuffer[i])
        return self._vectostring(substrWords)
    def _searchChar(self, charSubstr):
        wordIndexes = self.suffixTree.search(charSubstr)
        charSubstrWords = []
        wordIndexes=sorted(wordIndexes)
        for i in wordIndexes:
            charSubstrWords.append(self.wordBuffer[i])

        return self._vectostring(charSubstrWords)
    def _countSuffix(self, suffix):
        return self.suffixTree.searchWithSuffixCount(suffix)
        

    def _countSubstring(self, substr):
        return self.suffixTree.searchWithCount(substr)

    def _countChar(self, charSubstr):
        return self.suffixTree.searchWithCount(charSubstr)
    
    def _preProcessText(self,s):
        s=(re.sub("[^a-zA-Z]+", "",s))
        s=s.lower()
        return s
    def _vectostring(self,z):
            z=str(z).translate(str.maketrans('', '','[]'))
            z=re.sub("'", '', str(z))
            z=re.sub(",", '', str(z))
            return z
