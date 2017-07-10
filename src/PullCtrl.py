#!/usr/bin/env python

class PullCtrl:
    def __init__(self):
        self.children = list()
        self.next = None

    def getChildren(self): return self.children
    def getNext(self): return self.next
    def setNext(self, next): self.next = next

    def __str__(self):
        result = '('
        for c in self.children: result += c.getName() + ' + '
        if result.endswith(' + '): result = result[:-3]
        return result + ')'