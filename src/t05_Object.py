#!/usr/bin/env python2

""" Implementation of T05 Objects. """

import types
import t05_Tag
import t05_String
import t05_CFunction
import t05_Acob
import t05_Vm
import t05_Bool
import sys


# Define exceptions
class t05_Error(Exception): pass


class t05_ObjectTag(t05_Tag.t05_Tag):

    def __init__(self):
        self.idCount = 0

    def equal(self, lhs, rhs):
        return lhs == rhs

    def name(self):
        return "object"

    def getNewId(self):
        t = self.idCount
        self.idCount = self.idCount + 1
        return t

tag = t05_ObjectTag()


class t05_Object:

    def __init__(self):
        self.tag = tag
        self.data = None
        self.slots = []
        self.parents = []
        self.state = None
        self.id = tag.getNewId()

    def getSlotLocal(self, key):
        key = toObj(key)
        for s in self.slots:
            if key.equal(s[0]):
                return s[1]
        return None

    def getSlot(self, key):
        r = self.getSlotLocal(key)
        if r != None:
            return r
        for s in self.parents:
            r = s.getSlot(key)
            if r != None:
                return r
        return None

    def getSlotSafe(self, key):
        r = self.getSlot(key)
        if r == None:
            raise t05_Error("unable to find slot")
        return r

    def addSlot(self, key, value):
        key = toObj(key)
        value = toObj(value)
        for s in self.slots:
            if key.equal(s[0]):
                return False
        self.slots.append((key, value))
        return True

    def updateSlotLocal(self, key, value):
        key = toObj(key)
        value = toObj(value)
        for i in range(len(self.slots)):
            s = self.slots[i]
            if key.equal(s[0]):
                self.slots[i] = (s[0], value)
                return True
        return False

    def updateSlot(self, key, value):
        if self.updateSlotLocal(key, value):
            return True
        for s in self.parents:
            if s.updateSlot(key, value):
                return True
        return False

    def deleteSlot(self, key):
        key = toObj(key)
        for i in range(len(self.slots)):
            s = self.slots[i]
            if key.equal(s[0]):
                a1 = self.slots[:i]
                a2 = self.slots[i+1:]
                a1.extend(a2)
                self.slots = a1
                return True
        return False

    def addParent(self, parent):
        self.parents.append(parent);

    def equal(self, x):
        x = toObj(x)
        if self.tag != x.tag:
            return False
        return self.tag.equal(self, x)

    def checkSlot(self, key):
        r = self.getSlot(key)
        return r != None

    def checkSlotLocal(self, key):
        r = self.getSlotLocal(key)
        return r != None
    
    def setSlot(self, key, value):
        if self.checkSlotLocal(key):
            self.updateSlot(key, value)
        else:
            self.addSlot(key, value)

def create(state):
    r = t05_Object()
    r.state = state
    return r

def proto(state):
    r = create(state)
    addMethod(r, "getSlot", getSlot_)
    addMethod(r, "addSlot", addSlot_)
    addMethod(r, "updateSlot", updateSlot_)
    addMethod(r, "setSlot", setSlot_)
    addMethod(r, "new", new_)
    addMethod(r, "if", if_)
    addMethod(r, "while", while_)
    addMethod(r, "abort", abort_)
    addMethod(r, "break", break_)
    addMethod(r, "continue", continue_)
    return r

def new(state):
    r = create(state)
    r.addParent(state.protos.object)
    return r

def clone(x):
    return x

def addMethod(obj, methodName, method):
    key = t05_String.create(obj.state, methodName)
    value = t05_CFunction.create(obj.state, method)
    obj.addSlot(key, value)

def addStdProtos(obj):
    state = obj.state
    protos = state.protos
    key = t05_String.create(state, "Object")
    obj.addSlot(key, protos.object)
    key = t05_String.create(state, "CFunction")
    obj.addSlot(key, protos.cFunction)
    key = t05_String.create(state, "Integer")
    obj.addSlot(key, protos.integer)
    key = t05_String.create(state, "null")
    obj.addSlot(key, protos.null)

def addStdSlots(obj):
    state = obj.state
    key = t05_String.new(state, "true")
    value = t05_Bool.new(state, True)
    obj.addSlot(key, value)
    key = t05_String.new(state, "false")
    value = t05_Bool.new(state, False)
    obj.addSlot(key, value)

# TODO: This function is to be removed.
def toObj(x):
    return x

def getSlot_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        key = acob.returnValue
        value = self_.getSlot(key)
        if value == None:
            vm.state.errorReporter.error("Object.getSlot: unable to find slot")
        acob.returnValue = value
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def addSlot_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        acob.phase = 2
        acob.userData = acob.returnValue
        vm.getArg(acobObj, node, 1)
    elif acob.phase == 2:
        key = acob.userData
        value = acob.returnValue
        if not self_.addSlot(key, value):
            vm.state.errorReporter.error("Object.addSlot: slot already exits")
        acob.returnValue = self_
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def updateSlot_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        acob.phase = 2
        acob.userData = acob.returnValue
        vm.getArg(acobObj, node, 1)
    elif acob.phase == 2:
        key = acob.userData
        value = acob.returnValue
        if not self_.updateSlot(key, value):
            vm.state.errorReporter.error("Object.updateSlot: unable to find slot")
        acob.returnValue = self_
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def setSlot_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        acob.phase = 2
        acob.userData = acob.returnValue
        vm.getArg(acobObj, node, 1)
    elif acob.phase == 2:
        key = acob.userData
        value = acob.returnValue
        self_.setSlot(key, value)
        acob.returnValue = self_
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def new_(vm, self_, acobObj, node):
    print("this is Object.new()... <<<<<<<<<<<<<<<<<<<<<<<")
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        r = new(vm.state)
        acob.returnValue = r
        acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = -1
    else:
        assert False

def if_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)

    #print("if - acob.phase="+str(acob.phase))
    if acob.phase == 0:
        #Treat this call as a block call.
        callerAcob = acob.callerAcob
        acobObj.addParent(callerAcob)
        #print("adding parent <"+str(callerAcob.id)+"> to <"+str(acobObj.id)+">")

        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        cond = t05_Bool.get(acob.returnValue)
        if cond:
            acob.phase = 2
            vm.getArg(acobObj, node, 1)
        else:
            if len(node.args) <= 2:
                acob.phase = -1
                acob.returnValue = vm.state.protos.null
                acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
            else:
                acob.phase = 2
                vm.getArg(acobObj, node, 2)
    elif acob.phase == 2:
        acob.phase = 3
        code = acob.returnValue
        vm.executeCode(code, acob.target, acobObj, node, 1)
    elif acob.phase == 3:
        acob.phase = -1
    else:
        assert False

def while_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        if acob.returnType == t05_Vm.RETURN_TYPE_BREAK:
            acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
            acob.phase = -1;
            return
        if acob.returnType == t05_Vm.RETURN_TYPE_CONTINUE:
            acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        cond = t05_Bool.get(acob.returnValue)
        if cond:
            acob.phase = 2
            vm.getArg(acobObj, node, 1)
        else:
            acob.phase = -1
            acob.returnValue = vm.state.protos.null
            acob.returnType = t05_Vm.RETURN_TYPE_NORMAL
    elif acob.phase == 2:
        acob.phase = 0
        code = acob.returnValue
        vm.executeCode(code, acob.target, acobObj, node, 1)
    else:
        assert False

def abort_(vm, self_, acobObj, node):
    sys.exit(1)

def break_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = -1
        acob.returnValue = vm.state.protos.null
        acob.returnType = t05_Vm.RETURN_TYPE_BREAK
        print("************************************break")
    else:
        assert False

def continue_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = -1
        acob.returnValue = vm.state.protos.null
        acob.returnType = t05_Vm.RETURN_TYPE_CONTINUE
        print("************************************continue")
    else:
        assert False
