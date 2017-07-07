#!/usr/bin/env python

import re

class PullVar:
    REG_PULL_VAR = r"\{([0-9]+)\}\s*([!<=>]+)\s*(.*)"
    REG_TYPE_STRING = r"^[\'\"](.*)[\'\"]$"
    REG_TYPE_INTEGER = r"^[0-9\.\,]+$"
    REG_TYPE_LIST = r"^\[(.*)\]$"

    SEPERATE_COMMA = ",";
    SYMBOL_QUOTE = "'"
    OP_MATCHED = "<>"
    OP_UNMATCHED = "><"
    TYPE_STRING = "STRING"
    TYPE_INTEGER = "INTEGER"

    def __init__(self, pullArg):
        self.index = -1
        self.op = None
        self.values = list()
        self.expects = list()
        self.result = False

        match = re.search(self.REG_PULL_VAR, pullArg)
        if match:
            self.index = int(match.group(1).strip())
            self.op = match.group(2).strip()
            self.genExpects(match.group(3).strip())
        else:
            raise Exception("ERROR: wrong PULL variable expression.")


    def getIndex(self): return self.index
    def setValue(self, value): self.values.append(value)
    def getValues(self): return self.values
    def getResult(self): return self.checkResult()

    def genExpects(self, expectExpress):
        expectExpress = expectExpress.strip()
        m = re.search(self.REG_TYPE_LIST, expectExpress)
        if m:
            expectExpress = m.group(1)
            for e in expectExpress.split(self.SEPERATE_COMMA): self.addExpect(e)
        else:
            self.addExpect(expectExpress)

    def addExpect(self, expect):
        expect = expect.strip()
        if re.search(self.REG_TYPE_INTEGER, expect):
            self.type = self.TYPE_INTEGER
        else:
            self.type = self.TYPE_STRING
            m = re.search(self.REG_TYPE_STRING, expect)
            if m: expect = m.group(1).strip()
        if len(expect) > 0: self.expects.append(expect)

    def clean(self):
        self.result = False
        del self.values[:]

    def safeGet(self, lst, i):
        if i < len(lst): return lst[i]
        else: return lst[-1]

    def formatValue(self, value):
        return value if self.type == self.TYPE_INTEGER else self.SYMBOL_QUOTE + value + self.SYMBOL_QUOTE

    def checkValue(self, i):
        if self.op == self.OP_MATCHED:
            return True if re.search(self.safeGet(self.expects,i), self.values[i]) else False
        elif self.op == self.OP_UNMATCHED:
            return False if re.search(self.safeGet(self.expects,i), self.values[i]) else True
        else:
            return eval(self.formatValue(self.values[i]) + self.op + \
                        self.formatValue(self.safeGet(self.expects,i)))

    def checkResult(self):
        if (len(self.expects) == 0 or len(self.values) == 0): return self.result
        localResult = True
        for i in range(0, len(self.values)):
            localResult = localResult and self.checkValue(i)
        self.result = localResult
        return self.result


    def __str__(self):
        return "---- PullVar Debug Info ----\n" + \
        "    - index   : " + str(self.index) + "\n" + \
        "    - operator: " + str(self.op) + "\n" + \
        "    - values  : " + str(self.values) + "\n" + \
        "    - expects : " + str(self.expects) + "\n" + \
        "    - result  : " + str(self.result) + "\n"
