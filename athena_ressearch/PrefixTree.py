class PNode:
    def __init__(self):
        self.prefixCount=0
        self.isWord=False        
        self.children={}
        self.word=""
class PrefixTree:
    def __init__(self):
        self.head = PNode()

    def insert(self, word):
        current = self.head
        current.prefixCount+=1

        for letter in word:
            if letter not in current.children:
                current.children[letter] = PNode()
            current.children[letter].prefixCount+=1
            current= current.children[letter]
        current.isWord = True
        current.word = word
        
    def prefixWordCount(self,prefix):
        current = self.head
        for letter in prefix:
            if letter not in current.children:
                return 0
            else:
                current= current.children[letter]
        return current.prefixCount
            

    def prefixWordList(self,prefix):
        current = self.head

        for letter in prefix:
            if letter not in current.children:
                return []
            else:
                current= current.children[letter]
        return self._DFS(current, prefix)

    def _DFS(self, node, prefix):
        words = []
        if node.isWord:
            words.append(prefix)
        for letter in node.children:
            words.append(self._DFS(node.children[letter], prefix+letter))
            #print(words)
        return words

    def wordExists(self,word):
        current = self.head
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        if current.isWord:
            return True
        return False
