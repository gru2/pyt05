#!/usr/bin/env python2

""" Implementation of source code position class. """

class SourceCodePosition:

    def __init__(self):
        self.startOffset = 0
        self.endOffset = 0
        self.startLine = 0
        self.startColumn = 0
        self.endLine = 0
        self.endColumn = 0
        self.unitName = ""

    def copy(self, x):
        self.startOffset = x.startOffset
        self.endOffset = x.endOffset
        self.startLine = x.startLine
        self.startColumn = x.startColumn
        self.endLine = x.endLine
        self.endColumn = x.endColumn
        self.unitName = x.unitName

    def clone(self):
        x = SourceCodePosition()
        x.copy(self)
        return x
