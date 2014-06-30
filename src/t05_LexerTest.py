#!/usr/bin/env python2

""" Unit tests for t05_Lexer.py """

import t05_Lexer
import t05_SourceCodePosition
import t05_InputStream
import t05_ErrorReporter
import unittest

scp = t05_SourceCodePosition.SourceCodePosition()
scp.unitName = "test"

def myLexer():
  lex = t05_Lexer.Lexer()
  lex.inputStream = t05_InputStream.InputStream()
  lex.errorReporter = t05_ErrorReporter.ErrorReporter()
  lex.currentTokenSourceCodePosition = t05_SourceCodePosition.SourceCodePosition()
  return lex

class t05_LexerTest(unittest.TestCase):

    def test01(self):
        lex = myLexer()
        lex.openInputString("", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test02(self):
        lex = myLexer()
        lex.openInputString("   \n\r  \t //comment\n  /* comment2 */ ", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test03(self):
        lex = myLexer()
        lex.openInputString("  \"\"", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_STRING)
        self.assertEqual(token.value, "")
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test04(self):
        lex = myLexer()
        lex.openInputString("  127", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_INTEGER)
        self.assertEqual(token.value, 127)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test05(self):
        lex = myLexer()
        lex.openInputString("abcd", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_IDENTIFIER)
        self.assertEqual(token.value, "abcd")
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test06(self):
        lex = myLexer()

        lex.operators = ["++", "+", "**"]
        lex.operatorTokens = ["++", "+", "**"]

        lex.openInputString(" + ++ ** ", scp)
        token = lex.lex()
        self.assertEqual(token.type, "+")
        token = lex.lex()
        self.assertEqual(token.type, "++")
        token = lex.lex()
        self.assertEqual(token.type, "**")

    def test07(self):
        lex = myLexer()

        lex.operators = ["++", "+", "**"]
        lex.operatorTokens = ["++", "+", "**"]

        lex.openInputString(" aaa+ \n \t ++ ** 9\"FOO\" /*comment*/ ", scp)

        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_IDENTIFIER)
        self.assertEqual(token.value, "aaa")

        token = lex.lex()
        self.assertEqual(token.type, "+")

        token = lex.lex()
        self.assertEqual(token.type, "++")

        token = lex.lex()
        self.assertEqual(token.type, "**")

        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_INTEGER)
        self.assertEqual(token.value, 9)

        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_STRING)
        self.assertEqual(token.value, "FOO")

        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test08(self):
        lex = myLexer()
        lex.openInputString("  12.5", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_DOUBLE)
        self.assertEqual(token.value, 12.5)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test09(self):
        lex = myLexer()
        TOK_TRUE = "TRUE"
        TOK_FALSE = "FALSE"
        lex.keywords["True"] = TOK_TRUE
        lex.keywords["False"] = TOK_FALSE
        lex.openInputString("  True False", scp)
        token = lex.lex()
        self.assertEqual(token.type, TOK_TRUE)
        token = lex.lex()
        self.assertEqual(token.type, TOK_FALSE)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)

    def test10(self):
        lex = myLexer()
        lex.openInputString("abc 23", scp)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_IDENTIFIER)
        self.assertEqual(token.value, "abc")
        self.assertEqual(token.sourceCodePosition.startOffset, 0)
        self.assertEqual(token.sourceCodePosition.endOffset, 3)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_INTEGER)
        self.assertEqual(token.value, 23)
        self.assertEqual(token.sourceCodePosition.startOffset, 4)
        self.assertEqual(token.sourceCodePosition.endOffset, 6)
        token = lex.lex()
        self.assertEqual(token.type, t05_Lexer.TOKEN_EOF)


if __name__ == '__main__':
    unittest.main()
