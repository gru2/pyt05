#!/usr/bin/env python2

""" Unit tests for t05_Vm.py """

import t05_Vm
import t05_Acob
#import t05_Parser
import t05_SourceCodePosition
import t05_State
#import t05_Node
import t05_Integer
import t05_String
import t05_CFunction
import t05_Bool
#import t05_helpers
import unittest


scp = t05_SourceCodePosition.SourceCodePosition()
scp.label = "test"

def foo(vm, target, acobObj, node):
    acob = t05_Acob.get(acobObj)
    acob.returnValue = t05_String.new(vm.state, "pera")
    acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
    acob.phase = -1

def bar(vm, target, acobObj, node):
    acob = t05_Acob.get(acobObj)
    print("acob.phase = " + str(acob.phase))
    if acob.phase == 0:
        acob.phase = 1
    elif acob.phase == 1:
        acob.returnValue = t05_String.new(vm.state, "milica")
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def buz(vm, target, acobObj, node):
    acob = t05_Acob.get(acobObj)
    print("acob.pahse = " + str(acob.phase))
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        assert(acob.returnValue.tag == t05_Integer.tag)
        t = acob.returnValue.data + 20
        acob.returnValue = t05_Integer.new(vm.state, t)
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False


class t05_ParserTest(unittest.TestCase):

    def test01(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("123;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 123)

    def test02(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("23; 44;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 44)

    def test03(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        globals_ = t05_Acob.new(state)
        val = t05_Integer.create(state, 167)
        key = t05_String.create(state, "foo")
        globals_.addSlot(key, val)
        r = vm.run(program, globals_)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 167)

    def test04(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("foo;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        globals_ = t05_Acob.new(state)
        val = t05_CFunction.create(state, foo)
        key = t05_String.create(state, "foo")
        globals_.addSlot(key, val)
        r = vm.run(program, globals_)
        self.assertEqual(r.tag, t05_String.tag)
        self.assertEqual(r.data, "pera")

    def test05(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("bar;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        globals_ = t05_Acob.new(state)
        val = t05_CFunction.create(state, bar)
        key = t05_String.create(state, "bar")
        globals_.addSlot(key, val)
        r = vm.run(program, globals_)
        self.assertEqual(r.tag, t05_String.tag)
        self.assertEqual(r.data, "milica")

    def test06(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("buz 71;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        globals_ = t05_Acob.new(state)
        val = t05_CFunction.create(state, buz)
        key = t05_String.create(state, "buz")
        globals_.addSlot(key, val)
        r = vm.run(program, globals_)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 91)

    def test07(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("getSlot \"foo\";", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        globals_ = t05_Acob.new(state)
        val = t05_Integer.create(state, 4567)
        key = t05_String.create(state, "foo")
        globals_.addSlot(key, val)
        r = vm.run(program, globals_)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 4567)

    def test08(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("$x = 43; x;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 43)

    def test09(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("23 + 17;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 40)

    def test10(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("6 < 8;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Bool.tag)
        self.assertEqual(r.data, True)

    def test11(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("16 < 12;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Bool.tag)
        self.assertEqual(r.data, False)

    def test12(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("if (16 < 12) 102 103;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 103)

    def test13(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("if (1 < 2) 122 133;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 122)

    def test14(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("if (10 < 20) {11 + 4;} 133;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 15)

    def test15(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        program = parser.parseString("$foo = { x|x+5; }; foo 7;", scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 12)

    def test16(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        code = "$n = 0; while (n < 3) { n = n + 1; }; n;"
        program = parser.parseString(code, scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 3)

    def test17(self):
        state = t05_State.State()
        state.init()
        parser = state.parser
        code = "$n = ${ 23 }; $x = n[0]; x;"
        program = parser.parseString(code, scp)
        vm = t05_Vm.Vm()
        vm.init(state)
        r = vm.run(program)
        self.assertEqual(r.tag, t05_Integer.tag)
        self.assertEqual(r.data, 23)

if __name__ == '__main__':
    unittest.main()
