#!/usr/bin/env python2

""" Implementation of T05 integer object. """

import types
import os
import t05_Tag
import t05_Object
import t05_Acob
import t05_Vm
import t05_Bool


class t05_IntegerTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return lhs.data == rhs.data

    def name(self):
        return "bool"

tag = t05_IntegerTag()

def create(state, x):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.data = x
    r.state = state
    return r

def proto(state):
    r = create(state, 0)
    t05_Object.addMethod(r, "+", add_)
    t05_Object.addMethod(r, "-", sub_)
    t05_Object.addMethod(r, "*", mul_)
    t05_Object.addMethod(r, "<", less_)
    t05_Object.addMethod(r, ">", greater_)
    t05_Object.addMethod(r, "==", eq_)
    t05_Object.addMethod(r, "!=", ne_)
    t05_Object.addMethod(r, "neg", neg_)
    return r

def new(state, x):
    r = create(state, x)
    r.addParent(state.protos.integer)
    return r

def get(x):
    assert(x.tag == tag)
    return x.data

def set(x, val):
    assert(x.tag == tag)
    assert(type(val) == types.IntType)
    x.data = val

def add_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        acob.returnValue = new(vm.state, x + y)
        acob.phase = -1
    else:
        assert(False)

def sub_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)

    #Treat this call as block call.
    callerAcob = acob.callerAcob
    acobObj.addParent(callerAcob)

    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        acob.returnValue = new(vm.state, x - y)
        acob.phase = -1
    else:
        assert(False)

def mul_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        acob.returnValue = new(vm.state, x * y)
        acob.phase = -1
    else:
        assert(False)

def less_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        val = False
        if x < y:
            val = True
        acob.returnValue = t05_Bool.new(vm.state, val)
        acob.phase = -1
    else:
        assert(False)

def greater_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        assert(self_.tag == tag)
        rhs = acob.returnValue
        assert(rhs.tag == tag)
        x = get(self_)
        y = get(rhs)
        val = False
        if x > y:
            val = True
        #print("gerater --- x="+str(x)+" y="+ str(y))
        acob.returnValue = t05_Bool.new(vm.state, val)
        acob.phase = -1
    else:
        assert(False)

def eq_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        val = False
        if x == y:
            val = True
        acob.returnValue = t05_Bool.new(vm.state, val)
        acob.phase = -1
    else:
        assert(False)

def ne_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        acob.phase = 1
        vm.getArg(acobObj, node, 0)
    elif acob.phase == 1:
        rhs = acob.returnValue
        x = get(self_)
        y = get(rhs)
        val = False
        if x != y:
            val = True
        acob.returnValue = t05_Bool.new(vm.state, val)
        acob.phase = -1
    else:
        assert(False)

def neg_(vm, self_, acobObj, node):
    acob = t05_Acob.get(acobObj)
    if acob.phase == 0:
        x = get(self_)
        acob.returnValue = new(vm.state, -x)
        acob.phase = -1
    else:
        assert(False)
