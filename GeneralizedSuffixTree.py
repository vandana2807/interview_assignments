class Edge:
    def __init__(self,label,dest):
        self.label = label
        self.dest = dest
    def getLabel(self):
        return self.label
    def getDest(self):
        return self.dest
    def setLabel(self,label):
        self.label=label


class Node:
    def __init__(self):
        self.data=set()
        self.suffixData=set()
        self.suffix=None
        self.edges={}
        self.resC=-1
        self.suffC=-1
    
    def _contains(self,index):
        if index in self.data:
            return True
        else:
            return False
        
        
    def _getData(self,numElements=-1):
        #else:
        output=set()
        
        for i in self.data:
            output.add(i)
            if len(output)==numElements:
                opVec=[]
                opVec.append(output)
                #print("1st loop")
                return opVec
        for ch,edge in self.edges.items():
            if numElements==-1 or len(output)<numElements:
                for num in edge.getDest()._getData():
                    output.add(num)
                    if len(output)==numElements:
                        opVec=[]
                        opVec.append(output)
                        #print("second loop")
                        return opVec
        op=output
        return op
    
    def getSuffixData(self):
        return (self.suffixData)
    
    def addRef(self,index):
        
        if index in self.data:
            return

        self.data.add(index)
        #print("data")
        #print(self.data)

        iter1 = self.suffix
        #print("iter1",iter1)
        while(iter1 != None):
            if self._contains(index):
                break
            iter1.addRef(index)
            iter1=iter1.suffix
            
    def addSuffix(self,index):
        if index in self.suffixData:
             return
        else:
            self.suffixData.add(index)
        
    def _computeAndCacheCountRecursive(self):
        ret = self.data
        #print("self.edges")
        #for k,v in self.edges.items():
            #print(k,v)
        for ch, edge in self.edges.items():
            for n in edge.getDest()._computeAndCacheCountRecursive():
                ret.add(n)

        self.resC = len(ret)
        return ret
        
    def _calculateAndCacheSuffixCountRecursive(self):
        self.suffC = len(self.suffixData)
        for ch, edge in self.edges.items():
            edge.getDest()._calculateAndCacheSuffixCountRecursive()
        
    def calculateAndCacheSubstringCount(self):
        self._computeAndCacheCountRecursive()
        return self.resC
        
    def calculateAndCacheSuffixCount(self):
        self._calculateAndCacheSuffixCountRecursive()
        return self.suffC
        
    def addEdge(self,ch,e):
        self.edges[ch] = e
        
    def getEdge(self, ch):
        #print("self.edges",self.edges)
        if ch in self.edges:
            return self.edges[ch]
        else:
            return None
class GeneralizedSuffixTree:
    def __init__(self):
        #print("init")
        self.root = Node()
        #print("....")
        self.activeLeaf = self.root
        #print("init ",self.activeLeaf)

        
    def _searchNode(self,word):
        currentNode = self.root
        currentEdge = None
        for i in range(0,len(word)):
            #print("start i,",i)
            ch=word[i]
            if ch in currentNode.edges:
                currentEdge = currentNode.edges[ch]
                #print("currentEdge",currentEdge)

                if currentEdge==None:
                    return None
                else:
                    label = currentEdge.getLabel()
                    #print("label",label)
                    lenToMatch = min(len(word)-i, len(label))
                    #print(len(word)-i,len(label))
                    #print("lenToMatch",lenToMatch)
                    #print("word: ",word,"label: ",label)
                    #print("len(word)",len(word))
                    #print(i,lenToMatch)
                    #print(i,":",lenToMatch,"0 :",lenToMatch)
                    #print(word[i:i+lenToMatch])
                    #print(label[0:lenToMatch])



                    if(word[i:i+lenToMatch] != label[0:lenToMatch]):
                        #print("return None")
                        return None
                    if len(label) >= len(word)-i:
                        #print("currentEdge->getDest() ",currentEdge.getDest())
                        return currentEdge.getDest()
                    else:
                        currentNode = currentEdge.getDest();
                        i+=lenToMatch-1
                        #print("currentNode = currentEdge->getDest()",currentNode)
            
            else:
                return None
    
    def _getRoot(self):
        return self.root
        
    def computeCount(self):
        return self.root.calculateAndCacheSubstringCount()

    def computeSuffixCount(self):
        return self.root.calculateAndCacheSuffixCount()
    
    def searchWithCount(self, word):
        #print("searchWithCount")
        tmpNode = self._searchNode(word)
        #print("tmpNode",tmpNode)
        if(tmpNode == None):
            return 0
        #print(tmpNode.resC)

        return tmpNode.resC
    
    def search(self ,word,results=-1):  
        #print(word,results)
        tmpNode = self._searchNode(word)
        if(tmpNode == None):
            return {}
        return tmpNode._getData(results)
    
    def searchSuffix(self,word):
        #print("here",word)
        tmpNode = self._searchNode(word)
        #print()
        if(tmpNode == None):
            return {}
        return tmpNode.getSuffixData()    
    
    def searchWithSuffixCount(self,word):
        tmpNode = self._searchNode(word)
        if(tmpNode == None):
            return 0
        return tmpNode.suffC
    
    def _update(self, inputNode, stringPart, rest, value):
        #print("update start",self.activeLeaf)
        s = inputNode
        tempstr = stringPart
        newChar = stringPart[len(stringPart)-1]
        oldRoot = self.root
        
        #print("s:",s)
        #print("tempstr :",tempstr)
        #print("newChar:",newChar)
        #print("oldRoot:",oldRoot)
        #print("temp:",tempstr[0:len(tempstr)-1])
        #print("rest: ",rest)
        #print("value: ",value)
        
        is_end_point, split_state = self._testAndSplit(s,tempstr[0:len(tempstr)-1],newChar, rest, value)
        #print("r :",split_state)
        #print("endpoint:",is_end_point)

        r = split_state
        endpoint = is_end_point
        #leaf = Node()
        while not endpoint:
            tempEdge = r.getEdge(newChar)
            #print("tempEdge: ",tempEdge)

            if(tempEdge!=None): 
                leaf = tempEdge.getDest();
                #print("leaf: ",leaf)
            else:         
                leaf = Node()
                leaf.addRef(value)
                leaf.addSuffix(value)
                #print("new leaf: ",leaf)
                #print("new rest: ",rest)
                newEdge = Edge(rest,leaf)
                #print("new leaf newedge",newEdge)
                r.addEdge(newChar, newEdge)
                
            #print(self.activeLeaf)
            #print(leaf)
            #print("oldd: ",oldRoot)
            #print("rr: ",r)
            if(self.activeLeaf!=self.root):
                #print("self.activeLeaf!=self.root",self.activeLeaf.suffix)
                self.activeLeaf.suffix = leaf
            

            self.activeLeaf = leaf;
            #print("self.activeLeaf = leaf")
            

            if(oldRoot != self.root):
                oldRoot.suffix = r
                #print("oldRoot.suffix = r")

            oldRoot = r;
            #print("oldRoot = r")
            #print

            if(s.suffix == None):
                if(s!=self.root) :
                    #print("s.suffix == None, s!=self.root")
                    return {}

                tempstr = tempstr[1:]
                #print("tempstr[1:]",tempstr)
            else:
                canonizeReturn_node, canonizeReturn_str = self._canonize(s.suffix, self._safeCutLastChar(tempstr));
                s = canonizeReturn_node;
                tempstr = canonizeReturn_str+ tempstr[len(tempstr)-1]
                #print("return 2: ",s)
                #print("return 2: ",tempstr)
            
            is_end_point, split_state = self._testAndSplit(s, self._safeCutLastChar(tempstr), newChar, rest, value);
            r = split_state
            endpoint= is_end_point
            #print("return 3: ",r)
            #print("return 3. ",endpoint)
        
        if(oldRoot != self.root):
            #print("2. oldRoot != self.root")
            oldRoot.suffix = r
        
        #print("2. oldRoot=self.root")
        oldRoot = self.root
        #print("update end",self.activeLeaf)

        return s, tempstr

            

                
    def _testAndSplit(self, inputs, stringPart, t, remainder, value):
        
        #print("test and split start",self.activeLeaf)
        #print(inputs)
    
        
        s,str1 =self._canonize(inputs, stringPart)
        #print("test and split")
        #print("node :",s)
        #print("str1 :",str1)
        #print("edges{}")
        #for k,v in s.edges.items():
        #    print(k," : ",v)
        #print("end edges")
        if(str1!=""):
            g = s.getEdge(str1[0])
            label = g.getLabel()
            #print("g :",g)
            #print("label:",label)
            if(len(label) > len(str1) and label[len(str1)] == t):
                #print("1. true",s)
                return True,s
            else:
                #print("initial label: ",label)
                #print("size of str: ", str1, len(str1))
                
                newLabel = label[len(str1):]
                #print("newLabel:" ,newLabel,"label:",label)
                #label=""
                #print("newLabel",newLabel)
                #print("str:",str1,"label:",label)
                #print("else return: ",self._startsWith(str1,label))
            

                if not self._startsWith(str1,label):
                    #print("2. returning empyty",str1,label)
                    return {}
                
                r = Node()
                newEdge = Edge(str1, r)
                #print("r :",r)
                #print("newEdge :",newEdge)
                
                g.setLabel(newLabel)
                r.addEdge(newLabel[0], g)
                s.addEdge(str1[0], newEdge)
                #print("3. false",r)

                return False, r
            
        else:
            #print("else t:",t)
            e = s.getEdge(t)
            #print("e :",e)
            if(e == None):
                #print("4. false",s)
                return False, s
            
            else :
                
                label = e.getLabel()
                #print("else label: ",label)
                #print("else remainder:",remainder)
                
                #print("remainder == e.getLabel()",remainder == e.getLabel())
                if(remainder == e.getLabel()):
                    #print("5.",remainder,e.getLabel())
                    #print("5.",e.getDest())
                    #print("5.",value)
                    e.getDest().addRef(value)
                    
                    e.getDest().addSuffix(value)
                    #print("5. true",s)
                    return True,s
                elif self._startsWith(label,remainder): 
                    #print("6. return :",self._startsWith(label,remainder))
                    #print("6. label",label)
                    #print("6. remainder", remainder)
                    #print("6. true",s)
                    return True,s
                elif self._startsWith(remainder,label):
                    #print("7. return :",self._startsWith(remainder,label))
                    
                    newNode = Node()
                    newNode.addRef(value)
                    newNode.addSuffix(value)
                    newEdge = Edge(remainder, newNode)
                    e.setLabel(e.getLabel()[len(remainder):])
                    newNode.addEdge(e.getLabel()[0], e)
                    s.addEdge(t, newEdge)
                    #print("7. false",s)

                    return False, s
                else:
                    #print("8. true",s)
                    return True,s
        #print("test and split end",self.activeLeaf)
                
    def _startsWith(self,prefix, arg):
        #print("prefix:",prefix)
        #print("arg:",arg)
        #print(len(prefix), len(arg))
        #print("ans",(len(prefix) <= len(arg)) and (prefix==arg))
        #print("return :",((len(prefix) <= len(arg)) and (prefix.startswith(arg[0]))))
        if len(prefix)==1:
            return ((len(prefix) <= len(arg)) and (prefix[:]==arg[0]))
        else:
            return ((len(prefix) <= len(arg)) and (arg.startswith(prefix)))
        #return ((len(prefix) <= len(arg)) and (prefix[:]==arg[0]))
    
    def _safeCutLastChar(self, seq):
        if len(seq) == 0:
            return ""
        return seq[0:len(seq)-1]


    
    def insert(self, key, index):
        #print("key",key)
        #print("root",self.root)
        self.activeLeaf = self.root
        #print("insert start",self.activeLeaf)

        remainder = key
        s = self.root

        text =""
        for i in range(0,len(remainder)):
            #print("\n")
            #print(i)
            
            text=text+remainder[i]
            #print("text: ",text)
            s1,text1 = self._update(s, text, remainder[i:], index)
            #print("in s1",s1)
            #print("in text1",text1)
            s2,text2 = self._canonize(s1, text1)
            s = s2
            text = text2
            #print("in s",s)
            #print("in text",text)
        

        if(self.activeLeaf.suffix == None and self.activeLeaf!=self.root and self.activeLeaf!=s):
            self.activeLeaf.suffix = s
        
        #print("insert end",self.root)
        
        
        
   
    
    def _canonize(self, s, inputstr):
        #print(s)
        #print(inputstr)
        #print("in canonize start",self.activeLeaf)
        if(inputstr==""):
            #print("return ==",s)
            return s,inputstr       
        else:
            currentNode = s
            str1 = inputstr
            #print("node",s,s.edges,str1)
            g = s.getEdge(str1[0])
            #print("canon else getlabel: ",g.getLabel())
            #print("canon else str: ",str1)
            #print("canon else g: ",g)
            #print("canon else return: ",self._startsWith(g.getLabel(), str1))
            while (g!=None and self._startsWith(g.getLabel(), str1)): 
                str1 = str1[len(g.getLabel()):]
                currentNode = g.getDest()
                if(len(str1) > 0):
                    g = currentNode.getEdge(str1[0])
                
            
            #print("currentNode:",currentNode)
            return currentNode, str1
        #print("empty")
        #print("canonize end",self.activeLeaf)
        return {}
    
    
        
    

  