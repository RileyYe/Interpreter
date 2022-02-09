#! /usr/bin/env python
#coding=utf-8
class Node:

    def __init__(self, data):
        self._data = data
        self._children = []
        self.value=None
 
    def getdata(self):
        return self._data
    
    def getchild(self,i):
        return self._children[i]
 
    def getchildren(self):
        return self._children
 
    def add(self, node):
        self._children.append(node)
 
    def print_node(self, prefix):
        print '  '*prefix,'+',self._data
        for child in self._children:
            child.print_node(prefix+1)
    def to_string(self):
        string = self._data
        for child in self._children:
            string += child.to_string()
        return string
def num_node(data):
    t=Node(data)
    t.setvalue(float(data))
    return t