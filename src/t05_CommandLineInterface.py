#!/usr/bin/env python2

""" Implementation of command line interace. """

import t05_Node
import t05_Acob
import t05_CFunction
import t05_Function
import t05_helpers


class CommandLineInterface:

    def __init__(self):
        self.state = None
        self.inputFiles = []

    def init(self, state, args):
        self.state = state
        self.inputFiles = ["prologue.t05"]

        nArgs = len(args)
        for i in range(1,nArgs):
            arg = args[i]
            if arg[0] != "-":
                self.addInputFile(arg)
                continue
            
            if arg == "-drv":
                state.opt.dumpReturnValue = True
                continue
            
            state.errorReporter.error("unknown option '" + arg + "'")

    def run(self):
        if len(self.inputFiles) == 0:
            self.state.errorReporter.error("no input files")

        nInputFiles = len(self.inputFiles)
        for i in range(0,nInputFiles):
            f = self.inputFiles[i]
            returnValue = self.state.doFile(f)
            if i > 0:
                if self.state.opt.dumpReturnValue:
                    print("rv = "+t05_helpers.toString(returnValue))

    def addInputFile(self, fileName):
        self.inputFiles.append(fileName)
