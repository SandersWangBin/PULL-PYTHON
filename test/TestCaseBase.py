#!/usr/bin/env python

import re
import sys
sys.path.append('../src/')
from PullObj import PullObj

TC_DETAIL_INDENT = "    "
TC_NEWLINE = "\n"
TC_HEADER = "> TESTCASE: %s" + TC_NEWLINE
TC_SUM = "==== TEST SUITE (%s) RESULT: SUCCESS (%d/%d => %s%%), FAIL (%d/%d)" + TC_NEWLINE

def genResult(tcName, description, status):
    return TC_HEADER % (tcName) + description + \
           TC_DETAIL_INDENT + "====> TEST CASE RESULT: " + str(status) + TC_NEWLINE + TC_NEWLINE

def genDescription(texts):
    result = ''
    for text in texts: result += TC_DETAIL_INDENT + text + TC_NEWLINE
    return result

def checkUsePull(tcName, pullExp, text, expect):
    try:
        p = PullObj(pullExp)
        r = p.check(text)
        return genResult(tcName, \
                         genDescription(["PULL REGEXP EXPRESSION: " + pullExp, \
                                         "CHECKED TEXT          : " + text, \
                                         "PULL EXECUTE RESULT   : " + str(r)]), \
                         (r==expect))
    except Exception as e:
        return genResult(tcName, str(e), False)