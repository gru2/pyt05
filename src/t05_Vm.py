#!/usr/bin/env python2

""" T05 virtual machine. """

import t05_Node
import t05_Acob
import t05_CFunction
import t05_Function
import t05_Object
import t05_Integer
import t05_String
#import t05_helpers


RETURN_TYPE_NORMAL = "NORMAL"
RETURN_TYPE_BREAK = "BREAK"
RETURN_TYPE_CONTINUE = "CONTINUE"


class Vm:
    
    def __init__(self):
        self.globals = None
        self.currentAcob = None
        self.returnValue = None
        self.returnType = RETURN_TYPE_NORMAL
        self.state = None
        self.tick = 0

    def init(self, state):
        self.state = state

    def run(self, program, globals = None):
        self.start(program, globals)
        while True:
            r = self.step()
            if not r:
                break
        return self.returnValue

    def start(self, program, globals = None):
        if globals == None:
            globals = t05_Acob.new(self.state)
        self.globals = globals
        self.currentAcob = self.globals
        acob = t05_Acob.get(self.currentAcob)
        acob.node = program
        acob.target = globals
        self.tick = 0
    
    def step(self):
        self.tick = self.tick + 1
        acobObj = self.currentAcob
        acob = t05_Acob.get(acobObj)
        """
        depth = 0
        a = acobObj
        while(a != None):
            depth = depth + 1
            ad = t05_Acob.get(a)
            a = ad.callerAcob
        s = "<" + str(acobObj.id) + "> "
        s = s + str(depth)+" "+str(self.tick)+": rtype=" + acob.returnType + " ph="+str(acob.phase)
        s = s + " "+acob.node.type+" cfn="+str(acob.cFunction)
        s = s + " -- " + t05_helpers.nodeToString(acob.node, True)
        print(s)
        """
        if acob.phase == -1:
            if acob.returnType == RETURN_TYPE_NORMAL:
                if acob.node != None and acob.node.next != None:
                    if acob.cFunction == None:
                        acob.node = acob.node.next
                        acob.phase = 0
                        return True
            if acob.callerAcob == None:
                # program has finished
                self.returnType = acob.returnType
                self.returnValue = acob.returnValue
                return False
            callerAcobObj = acob.callerAcob
            callerAcob = t05_Acob.get(callerAcobObj)
            callerAcob.returnType = acob.returnType
            callerAcob.returnValue = acob.returnValue
            self.currentAcob = callerAcobObj
            return True
        if acob.cFunction != None:
            acob.cFunction(self, acob.target, acobObj, acob.node)
            return True
        self.evalNode()
        return True

    def evalNode(self):
        if self.tick == 36:
            self.tick = self.tick
        acobObj = self.currentAcob
        acob = t05_Acob.get(acobObj)
        node = acob.node
        if node.type == t05_Node.NODE_LITERAL:
            acob.phase = -1
            acob.returnValue = node.literal
            acob.returnType = RETURN_TYPE_NORMAL
            return
        elif node.type == t05_Node.NODE_IDENTIFIER:
            if acob.phase == 0:
                acob.phase = 1
                key = node.literal
                x = self.currentAcob.getSlot(key)
                if x == None:
                    self.state.errorReporter.sourceCodePosition = \
                        node.sourceCodePosition
                    self.state.errorReporter.error("unknown slot(1) ", key)
                    return
                self.executeCode(x, acobObj, acobObj, node, False)
                return
            else:
                acob.phase = -1
                return
        elif node.type == t05_Node.NODE_SELECT:
            if acob.phase == 0:
                acob.phase = 1
                val = node.value
                newAcob = self.createNewAcob(acob.target, acobObj, val, True)
                self.currentAcob = newAcob
                return
            elif acob.phase == 1:
                acob.phase = -1
                obj = acob.returnValue
                key = node.literal
                x = obj.getSlot(key)
                if x == None:
                    self.state.errorReporter.sourceCodePosition = \
                        node.sourceCodePosition
                    self.state.errorReporter.error("unknown slot(2) ", key)
                    return
                self.executeCode(x, obj, acobObj, node, True)
                return
            else:
                assert False
        elif node.type == t05_Node.NODE_BLOCK:
            acob.phase = -1
            acob.returnValue = t05_Function.new(self.state, node)
            acob.returnType = RETURN_TYPE_NORMAL
            return
        elif node.type == t05_Node.NODE_ARGUMENTS:
            self.evalArguments(acobObj, node)
        elif node.type == t05_Node.NODE_OBJECT_LITERAL:
            self.evalObjectLiteral(acobObj, node)
        else:
            self.state.errorReporter.error("unknown node type:" + \
                str(node.type))

    def executeCode(self, code, target, acobObj, node, asBlock):
        acob = t05_Acob.get(acobObj)
        if code == None:
            self.returnValue = None
            self.returnType = RETURN_TYPE_NORMAL
            return
        if code.tag == t05_CFunction.tag:
            newAcob = self.createNewAcob(target, acobObj, node, asBlock)
            fn = t05_CFunction.get(code)
            newAcobData = t05_Acob.get(newAcob)
            newAcobData.cFunction = fn
            self.currentAcob = newAcob
            fn(self, target, newAcob, node)
            return
        if code.tag == t05_Function.tag:
            fnNode = t05_Function.get(code)
            bodyNode = fnNode.value
            newAcob = self.createNewAcob(target, acobObj, bodyNode, asBlock)
            self.currentAcob = newAcob
            return
        acob.returnValue = code
        #acob.returnType = RETURN_TYPE_NORMAL
        acob.phase = -1

    def createNewAcob(self, target, oldAcob, node, asBlock, addParent = True):
        newAcob = t05_Acob.new(self.state)
        newAcobData = t05_Acob.get(newAcob)
        oldAcobData = t05_Acob.get(oldAcob)
        newAcobData.callerAcob = oldAcob
        newAcobData.node = node
        newAcobData.target = target
        if addParent:
            if asBlock:
                # Execute code as a block.
                newAcob.addParent(oldAcob)
            else:
                # Execute code as a new function call.
                newAcob.addParent(self.globals)
        return newAcob

    def getArg(self, acob, node, index):
        if index >= len(node.args):
            self.state.errorReporter.error("not enough arguments")
            return
        arg = node.args[index]
        acobData = t05_Acob.get(acob)
        newAcob = self.createNewAcob(acobData.target, acob, arg, True, False)
        self.currentAcob = newAcob
        newAcob.addParent(acobData.callerAcob)

    def evalArguments(self, acobObj, node):
        acob = t05_Acob.get(acobObj)
        if acob.phase == 0:
            acob.userData = (node.value, 0)
            acob.phase = 1
            return
        elif acob.phase == 1:
            callerAcob = acob.callerAcob
            callerAcobData = t05_Acob.get(callerAcob)
            callerNode = callerAcobData.node
            arg, count = acob.userData
            self.getArg(acobObj, callerNode, count)
            acob.phase = 2
            return
        elif acob.phase == 2:
            arg, count = acob.userData
            key = arg.literal
            value = acob.returnValue
            #print("ARGUMENTS: adding slot to object<"+str(acobObj.id)+"> val="+t05_helpers.toString(value))
            acobObj.addSlot(key, value)
            #acob.callerAcob.addSlot(key, value)
            acob.phase = 1
            acob.userData = (arg.next, count + 1)
            if arg.next == None:
                acob.phase = -1
            return
        else:
            assert False

    def evalObjectLiteral(self, acobObj, node):
        acob = t05_Acob.get(acobObj)
        if acob.phase == 0:
            obj = t05_Object.new(self.state)
            if node.value == None:
                acob.returnValue = obj
                acob.phase = -1
                return
            acob.userData = (obj, node.value, 0)
            acob.phase = 1
            return
        elif acob.phase == 1:
            obj, expr, index = acob.userData
            if expr == None:
                acob.returnValue = obj
                acob.phase = -1
                return
            expr2 = expr
            nextExpr = None
            if expr.type == t05_Node.NODE_OPERATION:
                if expr.literal.tag == t05_String.tag and expr.literal.data == ",":
                    expr2 = expr.value
                    nextExpr = expr.args[0]
            key = None
            if expr2.type == t05_Node.NODE_OPERATION:
                if expr2.literal.tag == t05_String.tag and expr2.literal.data == "=":
                    if expr2.value.type != t05_Node.NODE_IDENTIFIER:
                        self.state.errorReporter.error("syntax error: left of = must be identifier")
                    key = expr2.value.literal
                    expr2 = expr.args[0]
            if key == None:
                key = t05_Integer.new(self.state, index)
            newAcob = self.createNewAcob(acob.target, acobObj, expr2, True, False)
            self.currentAcob = newAcob
            newAcob.addParent(acob.callerAcob)
            acob.userData = (obj, expr2, nextExpr, index, key)
            acob.phase = 2
            return
        elif acob.phase == 2:
            obj, expr, nextExpr, index, key = acob.userData
            acob.userData = (obj, nextExpr, index + 1)
            obj.addSlot(key, acob.returnValue)
            acob.phase = 1
            return
        else:
            assert False

