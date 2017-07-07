#!/usr/bin/env python

import re
from PullVar import PullVar

class PullObj:
    REG_PULL_OBJ_EXP = r"r'(.*)'.PULL\((.*)\)"
    SPLIT_SEMICOLON = ";"

    def __init__(self, pullExp, objName=None):
        self.pullObjName = objName
        self.regExp = None
        self.pullVarsNum = 0
        self.pullVars = dict()
        self.result = False
        self.match = False

        self.initPullObj(pullExp)


    def initPullObj(self, pullExp):
        match = re.search(self.REG_PULL_OBJ_EXP, pullExp)
        if match:
            self.regExp = match.group(1)
            self.pullVarsNum = re.compile(self.regExp).groups
            self.parserPullVars(match.group(2))
        else:
            raise Exception("ERROR: wrong PULL expression.")

    def parserPullVars(self, argvExp):
        for a in argvExp.split(self.SPLIT_SEMICOLON):
            try:
                v = PullVar(a.strip())
                self.pullVars[v.getIndex()] = v
            except Exception as error:
                raise error
        return

    def cleanPullVars(self):
        for k, v in self.pullVars.iteritems():
            v.clean()

    def resultPullVars(self):
        localResult = True
        for k, v in self.pullVars.iteritems():
            localResult = localResult and v.checkResult()
        return localResult

    def check(self, text):
        self.cleanPullVars()
        matches = re.findall(self.regExp, text)
        for m in matches:
            self.match = True
            for i in range(0, len(m)):
                if (i in self.pullVars.keys()):
                    self.pullVars[i].setValue(m[i])
        self.result = self.resultPullVars()
        return self.result


    def printPullVars(self):
        result = str()
        for k, v in self.pullVars.iteritems():
            result += "key: " + str(k) + "\n" + str(v) + "\n"
        return result

    def __str__(self):
        return "==== PullObj Debug Info ====\n" + \
        "= objName : " + str(self.pullObjName) + "\n" + \
        "= regExp  : " + str(self.regExp) + "\n" + \
        "= result  : " + str(self.result) + "\n" + \
        "= matched : " + str(self.match) + "\n" + \
        "= PullVars: \n" + self.printPullVars() + "\n"
