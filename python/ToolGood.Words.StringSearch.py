####!/usr/bin/env python
# -*- coding:utf-8 -*-
# ToolGood.Words.Translate.js
# 2020, Lin Zhijun, https://github.com/toolgood/ToolGood.Words
# Licensed under the Apache License 2.0

__all__ = ['StringSearch']
__author__ = 'Lin Zhijun'
__date__ = '2020.04.06'

class TrieNode():
    def __init__(self):
        self.Index = 0
        self.Index = 0
        self.Layer = 0
        self.End = False
        self.Char = ''
        self.Results = []
        self.m_values = {}
        self.Failure = None
        self.Parent = None

    def Add(self,c):
        if c in self.m_values :
            return self.m_values[c]
        node = TrieNode()
        node.Parent = self
        node.Char = c
        self.m_values[c] = node
        return node

    def SetResults(self,index):
        if (self.End == False):
            self.End = True
        self.Results.append(index)

class TrieNode2():
    def __init__(self):
        self.End = False
        self.Results = []
        self.m_values = {}
        self.minflag = 0xffff
        self.maxflag = 0

    def Add(self,c,node3):
        if (self.minflag > c):
            self.minflag = c
        if (self.maxflag < c):
             self.maxflag = c
        self.m_values[c] = node3

    def SetResults(self,index):
        if (self.End == False) :
            self.End = True
        if (index in  self.Results )==False : 
            self.Results.append(index)

    def HasKey(self,c):
        return c in self.m_values;
        
 
    def TryGetValue(self,c):
        if (self.minflag <= c and self.maxflag >= c):
            return self.m_values[c]
        return None


class StringSearch():
    def __init__(self):
        self._first = []
        self._keywords = []

    def __swap(self,A, i, j):
        t = A[i]
        A[i] = A[j]
        A[j] = t

    def __divide(self,A, p, r):
        x = A[r - 1].Layer
        i = p - 1
        for j in range(p,r - 1): # for (j = p; j < r - 1; j++) 
            if (A[j].Layer <= x):
                i=i+1
                self.__swap(A, i, j)
        self.__swap(A, i + 1, r - 1)
        return i + 1

    def __qsort(self,A, p , r):
        r = r or A.length
        if (p < r - 1):
            q = self.__divide(A, p, r)
            self.__qsort(A, p, q)
            self.__qsort(A, q + 1, r)
        return A
    def __quickSort(self,arr):
        if ( len(arr) <= 1):
            return arr
        return self.__qsort(arr, 0, len(arr))
    
    def SetKeywords(self,keywords):
        self._keywords = keywords
        root = TrieNode()
        allNode = []
        allNode.append(root)

        for i in range(len(self._keywords)): # for (i = 0; i < _keywords.length; i++) 
            p = self._keywords[i]
            nd = root
            for j in range(len(p)): # for (j = 0; j < p.length; j++) 
                nd = nd.Add(ord(p[j]))
                if (nd.Layer == 0):
                    nd.Layer = j + 1
                    allNode.append(nd)
            nd.SetResults(i)

        nodes = []
        for  key in root.m_values.keys() :
            nd = root.m_values[key]
            nd.Failure = root
            for trans in nd.m_values :
                nodes.append(nd.m_values[trans])
            
        while len(nodes) != 0:
            newNodes = []
            for nd in nodes :
                #nd = nodes[key]
                r = nd.Parent.Failure
                c = nd.Char
                while (r != None and (c in r.m_values)==False):
                    r = r.Failure
                if (r == None):
                    nd.Failure = root
                else:
                    nd.Failure = r.m_values[c]
                    for key2 in nd.Failure.Results :
                        result = nd.Failure.Results[key2]
                        nd.SetResults(result)
                    
                
                for key2 in nd.m_values :
                    child = nd.m_values[key2]
                    newNodes.append(child)
            nodes = newNodes
        root.Failure = root

        allNode = self.__quickSort(allNode)
        for i in range(len(allNode)): # for (i = 0; i < allNode.length; i++) 
             allNode[i].Index = i

        allNode2 = []
        for i in range(len(allNode)): # for (i = 0; i < allNode.length; i++) 
            allNode2.append( TrieNode2())
        
        for i in range(len(allNode2)): # for (i = 0; i < allNode2.length; i++) 
            oldNode = allNode[i]
            newNode = allNode2[i]

            for key in oldNode.m_values :
                index = oldNode.m_values[key].Index
                newNode.Add(key, allNode2[index])
            
            for index in range(len(oldNode.Results)): # for (index = 0; index < oldNode.Results.length; index++) 
                item = oldNode.Results[index]
                newNode.SetResults(item)
            

            if (oldNode.Failure != root):
                for key in oldNode.Failure.m_values :
                    if (newNode.HasKey(key) == False):
                        index = oldNode.Failure.m_values[key].Index
                        newNode.Add(key, allNode2[index])
                    
                for index in range(len(oldNode.Failure.Results)): # for (index = 0; index < oldNode.Failure.Results.length; index++) 
                    item = oldNode.Failure.Results[index]
                    newNode.SetResults(item)
        allNode = None
        root = None

        first = []
        for index in range(65535):# for (index = 0; index < 0xffff; index++) 
            first.append(None)
        
        for key in allNode2[0].m_values :
            first[key] = allNode2[0].m_values[key]
        
        self._first = first
    

    def FindFirst(self,text):
        ptr = None
        for index in range(len(text)): # for (index = 0; index < text.length; index++) 
            t =ord(text[index]) # text.charCodeAt(index)
            tn = None
            if (ptr == None):
                tn = self._first[t]
            else:
                tn = ptr.TryGetValue(t)
                if (tn==None):
                    tn = self._first[t]
                
            
            if (tn != None):
                if (tn.End):
                    return self._keywords[tn.Results[0]]
            ptr = tn
        return None

    def FindAll(self,text):
        ptr = None
        list = []

        for index in range(len(text)): # for (index = 0; index < text.length; index++) 
            t =ord(text[index]) # text.charCodeAt(index)
            tn = None
            if (ptr == None):
                tn = self._first[t]
            else:
                tn = ptr.TryGetValue(t)
                if (tn==None):
                    tn = self._first[t]
                
            
            if (tn != None):
                if (tn.End):
                    for j in range(len(tn.Results)): # for (j = 0; j < tn.Results.length; j++) 
                        item = tn.Results[j]
                        list.append(self._keywords[item])
            ptr = tn
        return list


    def ContainsAny(self,text):
        ptr = None
        for index in range(len(text)): # for (index = 0; index < text.length; index++) 
            t =ord(text[index]) # text.charCodeAt(index)
            tn = None
            if (ptr == None):
                tn = self._first[t]
            else:
                tn = ptr.TryGetValue(t)
                if (tn==None):
                    tn = self._first[t]
            
            if (tn != None):
                if (tn.End):
                    return True
            ptr = tn
        return False
    
    def Replace(self,text, replaceChar = '*'):
        result = list(text) 

        ptr = None
        for i in range(len(text)): # for (i = 0; i < text.length; i++) 
            t =ord(text[i]) # text.charCodeAt(index)
            tn = None
            if (ptr == None):
                tn = self._first[t]
            else:
                tn = ptr.TryGetValue(t)
                if (tn==None):
                    tn = self._first[t]
            
            if (tn != None):
                if (tn.End):
                    maxLength = len( self._keywords[tn.Results[0]])
                    start = i + 1 - maxLength
                    for j in range(start,i+1): # for (j = start; j <= i; j++) 
                        result[j] = replaceChar
            ptr = tn
        return ''.join(result) 

if __name__ == "__main__":
    s = "中国|国人|zg人"
    test = "我是中国人"


    search = StringSearch()
    search.SetKeywords(s.split('|'))

    print("-----------------------------------  StringSearch  -----------------------------------" )

    print("StringSearch FindFirst is run.")
    f = search.FindFirst(test)
    if f!="中国" :
        print("StringSearch FindFirst is error.............................")
 
    print("StringSearch FindAll is run.")
    all = search.FindAll(test)
    if all[0]!="中国" :
        print("StringSearch FindAll is error.............................")
    if all[1]!="国人" :
        print("StringSearch FindAll is error.............................")
    if len(all)!=2 :
        print("StringSearch FindAll is error.............................")

    print("StringSearch ContainsAny is run.")
    b = search.ContainsAny(test)
    if b==False :
        print("StringSearch ContainsAny is error.............................")

    print("StringSearch Replace  is run.")
    txt = search.Replace (test)
    if (txt != "我是***"):
        print("StringSearch Replace  is error.............................")

    print("-----------------------------------  Test End  -----------------------------------") 


