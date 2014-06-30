#!/usr/bin/env python2

""" Unit tests for t05_Parser.py """

import t05_Parser
import t05_SourceCodePosition
import t05_State
import t05_Node
import t05_Integer
import t05_String
import t05_helpers
import unittest


scp = t05_SourceCodePosition.SourceCodePosition()
scp.label = "test"


class t05_ParserTest(unittest.TestCase):

    def test01(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("123;", scp)
        self.assertEqual(program.type, t05_Node.NODE_LITERAL)
        self.assertEqual(program.literal.tag, t05_Integer.tag)
        self.assertEqual(program.literal.data, 123)

    def test02(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("abcd;", scp)
        self.assertEqual(program.type, t05_Node.NODE_IDENTIFIER)
        self.assertEqual(program.literal.tag, t05_String.tag)
        self.assertEqual(program.literal.data, "abcd")

    def test03(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("\"1 2 3 x\";", scp)
        self.assertEqual(program.type, t05_Node.NODE_LITERAL)
        self.assertEqual(program.literal.tag, t05_String.tag)
        self.assertEqual(program.literal.data, "1 2 3 x")

    def test04(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo bar;", scp)
        self.assertEqual(program.type, t05_Node.NODE_IDENTIFIER)
        self.assertEqual(program.literal.tag, t05_String.tag)
        self.assertEqual(program.literal.data, "foo")
        self.assertEqual(len(program.args), 1)
        n2 = program.args[0]
        self.assertEqual(n2.type, t05_Node.NODE_IDENTIFIER)
        self.assertEqual(n2.literal.tag, t05_String.tag)
        self.assertEqual(n2.literal.data, "bar")

    def test05(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo bar;", scp)
        print(t05_helpers.nodeToString(program))

    def test06(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo + 44;", scp)
        print(t05_helpers.nodeToString(program))

    def test07(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        #program = parser.parseString("$foo = 1234; $x;", scp)
        program = parser.parseString("$xyz;", scp)
        print(t05_helpers.nodeToString(program))

    def test08(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        #program = parser.parseString("if (10 < 20) {11 + 4;} 133;", scp)
        program = parser.parseString("{11;};", scp)
        print(t05_helpers.nodeToString(program))

    def test09(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("$n = 0; while (n < 3) { n = n + 1; };", scp)
        print(t05_helpers.nodeToString(program))

    def test10(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("$bar = { $x = 7; foo;  };", scp)
        print(t05_helpers.nodeToString(program))

    def test11(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("if (x > 1) (x * (fact x - 1)) 1;", scp)
        print(t05_helpers.nodeToString(program))

    def test12(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo 1 + 2 3;", scp)
        print(t05_helpers.nodeToString(program))

    def test13(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("${ 42 };", scp)
        print(t05_helpers.nodeToString(program))

if __name__ == '__main__':
    unittest.main()
