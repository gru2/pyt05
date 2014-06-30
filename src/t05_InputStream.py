#!/usr/bin/env python2

""" Implementation of InputStream class. """


import t05_SourceCodePosition

class InputStream:

    def __init__(self):
        self.streamBuffer = ""
        self.streamPosition = 0
        self.sourceCodePosition = None

    def openFile(self, fileName):
        self.close()
        try:
            f = open(fileName, "r")
            self.streamBuffer = f.read()
            self.streamPosition = 0
            self.sourceCodePosition = t05_SourceCodePosition.SourceCodePosition()
            self.sourceCodePosition.unitName = fileName
            f.close()
        except IOError as (errno, strerror):
            return False
        return True

    def openString(self, string, sourceCodePosition):
        self.close()
        self.streamBuffer = string
        self.sourceCodePosition.copy(sourceCodePosition)

    def close(self):
        self.streamBuffer = ""
        self.streamPosition = 0
        self.sourceCodePosition = t05_SourceCodePosition.SourceCodePosition()

    def getChar(self):
        c = "EOF"
        if len(self.streamBuffer) > self.streamPosition:
            c = self.streamBuffer[self.streamPosition]

        self.changeStreamPosition(1)

        #print("getChar - '" + c +"'")
        return c

    def putBackChar(self):
        self.changeStreamPosition(-1)

    def getStreamPosition(self):
        return self.streamPosition

    def setStreamPosition(self, position):
        self.streamPosition = position
        self.updateSourceCodePosition()

    def changeStreamPosition(self, delta):
        self.streamPosition += delta
        self.updateSourceCodePosition()

    def updateSourceCodePosition(self):
        self.sourceCodePosition.startOffset = self.streamPosition

    def getLineAndColumn(self, offset):
        line = 1
        column = 1
        for i in range(0, offset):
            if i >= len(self.streamBuffer):
                return line, column
            column += 1
            if self.streamBuffer[i] == '\n':
                line += 1
                column = 1
            if self.streamBuffer[i] == '\r':
                column = 1
        return line, column
