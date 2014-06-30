#!/usr/bin/env python2

""" Implementation of ErrorReporter class. """

import t05_helpers
import sys

class ErrorReporter:
    
    def __init__(self):
        self.sourceCodePosition = None

    def error(self, msg, obj = None):
        t = ""
        if obj != None:
            t = t05_helpers.toString(obj)
        scp = self.sourceCodePosition
        #print scp.unitName+":"+str(scp.line)+" error:" + msg + t
        if scp != None:
            print scp.unitName+":"+str(scp.startLine)+" error:" + msg + t
        else:
            print "error:" + msg + t
        sys.exit(1)
