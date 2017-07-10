#!/usr/bin/env python

import re
from PullObj import PullObj

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




    def readPullChainFile(self, fileName):
        with open(fileName, 'r') as f:
            for l in f.readlines():
                self.readPullChainLine(l.strip())

    def readPullChainLine(self, line):
        m = re.search(self.REG_PULL_OBJ_EXP, line)
        if m:
            if PullObj.test(m.group(2).strip()):
                self.pullObjs[m.group(1).strip()] = PullObj(m.group(2).strip(), m.group(1).strip())
            else:
                self.pullObjRefs[m.group(1).strip()] = m.group(2).strip()

    def genPullChains(self, pullChainString): pass

    def __str__(self):
        result = "==== Pull Chain ====\n"
        if self.pullChainFile != None:       result += "Pull Chain File      : " + self.pullChainFile + "\n"
        if self.pullChainMultilines != None: result += "Pull Chain MultiLines: " + self.pullChainMultilines + "\n"
        if self.pullChain != None:           result += "Pull Chain           : " + self.pullChain + "\n"
        #if self.pullChainRoot != None:       result += "Pull Chain Root      : " + toStringChainRoot() + "\n";
        result += "Pull Chain Result: " + str(self.result) + "\n"
        result += "Pull Objs: \n"
        for k, v in self.pullObjs.iteritems(): result += str(v)
        result += "Pull Obj Refs: \n"
        for k, v in self.pullObjRefs.iteritems(): result += "  key: " + k + " -> " + v + "\n"
        return result
