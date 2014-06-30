#!/usr/bin/env python2

""" Class that represent state of T05 program during execution. """

import t05_InputStream
import t05_Lexer
import t05_Parser
import t05_Object
import t05_Protos
import t05_Options
import t05_Vm
import t05_ErrorReporter

class State:
    
    def __init__(self):
        self.inputStream = None
        self.lexer = None
        self.parser = None
        self.globals = None
        self.parser = None
        self.protos = None
        self.opt = None
        self.vm = None
        self.errorReporter = None
        
    def init(self):
        self.inputStream = t05_InputStream.InputStream()
        self.lexer = t05_Lexer.Lexer()
        self.parser = t05_Parser.Parser()
        self.globals = None
        self.protos = t05_Protos.Protos()
        self.opt = t05_Options.Options()
        self.vm = t05_Vm.Vm()
        self.errorReporter = t05_ErrorReporter.ErrorReporter()
        self.protos.init(self)
        self.lexer.inputStream = self.inputStream
        self.parser.lexer = self.lexer
        self.parser.init(self)
        self.vm.init(self)

    def doFile(self, fileName):
        program = self.parser.parseFile(fileName)
        returnValue = self.vm.run(program)
        return returnValue
