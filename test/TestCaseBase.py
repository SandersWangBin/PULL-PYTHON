#!/usr/bin/env python

import re
import sys
sys.path.append('../src/')
from PullObj import PullObj

class TestCasePull:
    TC_DETAIL_INDENT = "    "
    TC_NEWLINE = "\n"
    TC_HEADER = "> TESTCASE: %s" + TC_NEWLINE
    TC_SUM = "==== TEST SUITE (%s) RESULT: SUCCESS (%d/%d => %s%%), FAIL (%d/%d)" + TC_NEWLINE

    def __init__(self, name):
        self.tsName = name
        self.tcList = list()

    def genResult(self, tcName, description, status):
        return self.TC_HEADER % (tcName) + description + \
               self.TC_DETAIL_INDENT + "====> TEST CASE RESULT: " + str(status) + self.TC_NEWLINE + self.TC_NEWLINE

    def genDescription(self, texts):
        result = ''
        for text in texts: result += self.TC_DETAIL_INDENT + text + self.TC_NEWLINE
        return result
    
    def checkUsePull(self, tcName, pullExp, text, expect):
        try:
            p = PullObj(pullExp)
            r = p.check(text)
            self.tcList.append((self.genResult(tcName, \
                                self.genDescription(["PULL REGEXP EXPRESSION: " + pullExp, \
                                                     "CHECKED TEXT          : " + text, \
                                                     "PULL EXECUTE RESULT   : " + str(r)]), \
                                (r==expect)), 
                                (r==expect)))
        except Exception as e:
            self.tcList.append(self.genResult(tcName, str(e), False), False)

    def __str__(self):
        result = ''
        total = len(self.tcList)
        success = 0
        fail = 0
        for tc in self.tcList:
            result += tc[0]
            if tc[1]: success += 1
            else: fail += 1
        return self.TC_SUM % (self.tsName, success, total, success*1.0/total*100, fail, total) + \
               result