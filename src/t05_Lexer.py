#!/usr/bin/env python2

""" Implementation of Lexer class. """


TOKEN_EOF = "EOF"
TOKEN_STRING = "STRING"
TOKEN_INTEGER = "INTEGER"
TOKEN_DOUBLE = "DOUBLE"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_OPERATOR = "OPERATOR"


class Token:

    def __init__(self, type_):
        self.type = type_
        self.sourceCodePosition = None
        self.value = None


class Lexer:

    def __init__(self):
        self.inputStream = None

        self.tokenStream = []
        self.tokenStreamPosition = 0

        self.operators = []
        self.operatorTokens = []
        self.keywords = {}
        self.errorReporter = None
        self.currentTokenSourceCodePosition = None
        self.enableNegativeNumbers = False

        self.startTokenInputStreamPosition = 0

    def init(self, errorReporter):
        self.errorReporter = errorReporter

    def openInputFile(self, fileName):
        assert(self.inputStream != None)
        assert(self.errorReporter != None)
        self.errorReporter.sourceCodePosition = \
            self.inputStream.sourceCodePosition
        return self.inputStream.openFile(fileName)

    def openInputString(self, s, sourceCodePosition):
        assert(self.inputStream != None)
        assert(self.errorReporter != None)
        self.errorReporter.sourceCodePosition = \
            self.inputStream.sourceCodePosition
        self.inputStream.openString(s, sourceCodePosition)

    def closeInput(self):
        assert(self.inputStream != None)
        self.inputStream.close()

    def lex(self):
        assert(self.inputStream != None)
        if len(self.tokenStream) > self.tokenStreamPosition:
            t = self.tokenStream[self.tokenStreamPosition]
            self.tokenStreamPosition += 1
            return t
        else:
            assert(len(self.tokenStream) == self.tokenStreamPosition)
            t = self.getTokenFromStream()
            self.tokenStream.append(t)
            self.tokenStreamPosition += 1
            return t

    def getTokenFromStream(self):
        self.skipComments()
        self.startToken()
        if self.isEof():
            tok = self.newToken(TOKEN_EOF)
            return tok
        r, op = self.isOperator()
        if r:
            #print(">>operator = " + op)
            tok = self.newToken(op)
            return tok
        r, str_ = self.isString()
        if r:
            tok = self.newToken(TOKEN_STRING)
            tok.value = str_
            return tok
        r, x = self.isDouble()
        if r:
            tok = self.newToken(TOKEN_DOUBLE)
            tok.value = x
            return tok
        r, x = self.isInteger()
        if r:
            tok = self.newToken(TOKEN_INTEGER)
            tok.value = x
            return tok
        r, x = self.isIdentifier()
        if r:
            if x in self.keywords:
                tok = self.newToken(self.keywords[x])
                return tok
            tok = self.newToken(TOKEN_IDENTIFIER)
            tok.value = x
            return tok
        self.errorReporter.error("syntax error (lexer)")
        tok = self.newToken(TOKEN_EOF)
        return tok

    def returnToken(self):
        if self.tokenStreamPosition >= 0:
            self.tokenStreamPosition -= 1

    def eatWhite(self):
        while True:
            c = self.inputStream.getChar()
            if c != " " and c != "\t" and c != "\r" and c != "\n":
                self.inputStream.putBackChar()
                return

    def skipComments(self):
        while True:
            self.eatWhite()
            c = self.inputStream.getChar()
            if c != "/":
                self.inputStream.putBackChar()
                break

            c2 = self.inputStream.getChar()
            if c2 == "/":
                while True:
                    c3 = self.inputStream.getChar()
                    if c3 == "\n" or c3 == "EOF":
                        self.inputStream.putBackChar()
                        break
                continue
            if c2 == "*":
                lc = None
                while True:
                    c3 = self.inputStream.getChar()
                    if c3 == "EOF":
                        self.errorReporter.error("comment not finished")
                        break
                    if lc == "*" and c3 == "/":
                        break
                    lc = c3
                continue
            else:
                self.inputStream.putBackChar()
                self.inputStream.putBackChar()

    def isEof(self):
        c = self.inputStream.getChar()
        if c == "EOF":
            return True
        self.inputStream.putBackChar()
        return False

    def isString(self):
        c = self.inputStream.getChar()
        if c != "\"":
            self.inputStream.putBackChar()
            return False, None
        tempBuffer = ""
        while True:
            c = self.inputStream.getChar()
            if c == "\\":
                c = self.inputStream.getChar()
                if c == "n":
                    c = "\n"
                if c == "r":
                    c = "\r"
                if c == "t":
                    c = "\t"
                if c == "EOF":
                    self.errorReporter.error("string not finished")
                    return True, tempBuffer
                tempBuffer += c
                continue
            if c == "\"":
                break
            if c == "EOF":
                self.errorReporter.error("string not finished")
                return True, tempBuffer
            tempBuffer += c
        return True, str(tempBuffer)

    def isInteger(self):
        oldPosition = self.inputStream.getStreamPosition()
        c = self.inputStream.getChar()
        if c < "0" or c > "9":
            self.inputStream.setStreamPosition(oldPosition)
            return False, None
        tempBuffer = ""
        while True:
            if c < "0" or c > "9":
                self.inputStream.putBackChar()
                break
            tempBuffer += c
            c = self.inputStream.getChar()
        return True, int(tempBuffer)

    def isDouble(self):
        oldPosition = self.inputStream.getStreamPosition()
        c = self.inputStream.getChar()
        sign = 1.0
        floatingPoint = False
        number = False
        numberInExp = True
        if self.enableNegativeNumbers:
            if c == "-":
                sign = -1.0
                c = self.inputStream.getChar()
        tempBuffer = ""
        while True:
            if c < "0" or c > "9":
                break
            number = True
            tempBuffer +=c
            c = self.inputStream.getChar()
        if c == ".":
            floatingPoint = True
            tempBuffer += c
            c = self.inputStream.getChar()
            while True:
                if c < "0" or c > "9":
                    break
                number = True
                tempBuffer += c
                c = self.inputStream.getChar()
        if c == "E" or c == "e":
            numberInExp = False
            floatingPoint = True
            tempBuffer += c
            c = self.inputStream.getChar()
            if c == "+" or c == "-":
                tempBuffer += c
                c = self.inputStream.getChar()
            while True:
                if c < "0" or c > "9":
                    break
                numberInExp = True
                tempBuffer += c
                c = self.inputStream.getChar()

        if not floatingPoint or not number or not numberInExp:
            self.inputStream.setStreamPosition(oldPosition)
            return False, None

        self.inputStream.putBackChar()
        return True, sign * float(tempBuffer)

    def isIdentifier(self):
        c = self.inputStream.getChar()
        if not ((c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"):
            self.inputStream.putBackChar()
            return False, None
        tempBuffer = ""
        while True:
            if c == "EOF":
                self.inputStream.putBackChar()
                break
            if not ((c >= "a" and c <= "z") or (c >= "A" and c <= "Z") \
                or (c >= "0" and c <= "9") or c == "_"):
                self.inputStream.putBackChar()
                break
            tempBuffer += c
            c = self.inputStream.getChar()
        return True, str(tempBuffer)

    def isOperator(self):
        oldPosition = self.inputStream.getStreamPosition()
        for j in range(0, len(self.operators)):
            i = 0
            op = self.operators[j]
            while True:
                if i == len(op):
                    return True, self.operatorTokens[j]
                c1 = op[i]
                c2 = self.inputStream.getChar()
                if c1 != c2:
                    self.inputStream.setStreamPosition(oldPosition)
                    break
                i += 1
        return False, None

    def startToken(self):
        self.startTokenInputStreamPosition = self.inputStream.getStreamPosition()

    def newToken(self, type_):
        tok = Token(type_)
        is_ = self.inputStream
        scp = is_.sourceCodePosition.clone()
        scp.startOffset = self.startTokenInputStreamPosition
        scp.endOffset = is_.getStreamPosition()
        scp.startLine, scp.startColumn = is_.getLineAndColumn(scp.startOffset)
        scp.endLine, scp.endColumn = is_.getLineAndColumn(scp.endOffset)
        tok.sourceCodePosition = scp
        return tok
