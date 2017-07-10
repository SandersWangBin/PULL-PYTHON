#!/usr/bin/env python

import re
from PullObj import PullObj
from PullCtrl import PullCtrl

class PullChain:
    REG_PULL_CHAIN_FILE_EXP = r"f'(.*)'.PULL\((.*)\)"
    REG_PULL_CHAIN_MULTILINES_EXP = r"m'(.*)'.PULL\((.*)\)"

    REG_PULL_OBJ_EXP = r"^([a-zA-Z0-9\\._-]+)\s*:\s*(.*)"

    SEPERATOR_NEWLINE = "\n"
    SYMBOL_NEXT = ">"
    SYMBOL_PLUS = "+"

    def __init__(self, pullExp):
        self.pullChainFile = None
        self.pullChainMultilines = None
        self.pullChain = None
        self.pullChainRoot = None
        self.pullChainCurrent = None
        self.pullObjs = dict()
        self.pullObjRefs = dict()
        self.result = False

        m = re.search(self.REG_PULL_CHAIN_FILE_EXP, pullExp)
        if m:
            self.pullChainFile = m.group(1)
            self.readPullChainFile(self.pullChainFile)
            self.genPullChains(m.group(2))




    def readPullChainFile(self, fileName):
        with open(fileName, 'r') as f:
            for l in f.readlines():
                if len(l.strip())>0: self.readPullChainLine(l.strip())

    def readPullChainLine(self, line):
        m = re.search(self.REG_PULL_OBJ_EXP, line)
        if m:
            if PullObj.test(m.group(2).strip()):
                self.pullObjs[m.group(1).strip()] = PullObj(m.group(2).strip(), m.group(1).strip())
            else:
                self.pullObjRefs[m.group(1).strip()] = m.group(2).strip()

    def checkRef(self, pullChainString):
        return True if self.pullObjRefs.get(pullChainString, None) != None else False

    def checkObj(self, pullChainString):
        return True if self.pullObjs.get(pullChainString, None) != None else False

    def updateUsedPullChainName(self, pullChainString):
        if self.checkRef(pullChainString): return self.pullObjRefs[pullChainString]
        else: return pullChainString

    def genPullChains(self, pullChainString):
        if self.checkObj(pullChainString):
            self.pullChain = pullChainString
            ctrl = PullCtrl()
            self.pullChainRoot = ctrl
            ctrl.getChildren().append(self.pullObjs[pullChainString])
        else:
            self.pullChain = self.updateUsedPullChainName(pullChainString)
            previous = None
            for l in self.pullChain.split(self.SYMBOL_NEXT):
                 ctrl = PullCtrl()
                 if self.pullChainRoot == None: self.pullChainRoot = ctrl
                 if previous != None: previous.setNext(ctrl)
                 previous = ctrl
                 for m in l.split(self.SYMBOL_PLUS):
                     if self.checkObj(m.strip()):
                         ctrl.getChildren().append(self.pullObjs[m.strip()])

        self.pullChainCurrent = self.pullChainRoot
        return self.pullChain

    def checkLine(self, ctrl, line):
        result = False
        if ctrl != None and len(line) > 0:
            for obj in ctrl.getChildren():
                r = obj.check(line)
                result = result or r
        return result

    def check(self, text):
        self.result = self.checkLine(self.pullChainCurrent, text)
        if (self.result == False and self.pullChainCurrent.getNext() != None):
            self.result = self.checkLine(self.pullChainCurrent.getNext(), text)
            if self.result == true: self.pullChainCurrent = self.pullChainCurrent.getNext()
        return self.result


    def toStringChainRoot(self):
        result = ''
        next = self.pullChainRoot
        while next != None:
            result += str(next) + ' > '
            next = next.getNext()
        if result.endswith(' > '): result = result[:-3]
        return result

    def __str__(self):
        result = "==== Pull Chain ====\n"
        if self.pullChainFile != None:       result += "Pull Chain File      : " + self.pullChainFile + "\n"
        if self.pullChainMultilines != None: result += "Pull Chain MultiLines: " + self.pullChainMultilines + "\n"
        if self.pullChain != None:           result += "Pull Chain           : " + self.pullChain + "\n"
        if self.pullChainRoot != None:       result += "Pull Chain Root      : " + self.toStringChainRoot() + "\n";
        result += "Pull Chain Result: " + str(self.result) + "\n"
        result += "Pull Objs: \n"
        for k, v in self.pullObjs.iteritems(): result += str(v)
        result += "Pull Obj Refs: \n"
        for k, v in self.pullObjRefs.iteritems(): result += "  key: " + k + " -> " + v + "\n"
        return result
