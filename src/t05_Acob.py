#!/usr/bin/env python2

""" Implementation of T05 activation object. """

import types
import t05_Tag
import t05_Object
import t05_Vm


NODE_UNINITIALIZED = 0
NODE_SELECT = 1
NODE_UNOP = 2
NODE_GROUP = 3
NODE_SLOT = 4
NODE_BRACKET = 5
NODE_IDENTIFIER = 6
NODE_LITERAL = 7
NODE_BLOCK = 8
NODE_ARGUMENTS = 9
NODE_OPERATION = 10
NODE_OBJECT_LITERAL = 11

class Acob:
    
    def __init__(self):
        self.callerAcob = None
        self.node = None
        self.returnType = t05_Vm.RETURN_TYPE_NORMAL
        self.returnValue = None
        self.target = None
        self.phase = 0
        self.cFunction = None
        self.userData = None

class t05_AcobTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return lhs.data == rhs.data

    def name(self):
        return "acob"

tag = t05_AcobTag()

def create(state):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.data = Acob()
    r.state = state
    return r

def proto(state):
    r = create(state)
    r.addParent(state.protos.object)
    return r

def new(state):
    r = create(state)
    r.addParent(state.protos.acob)
    return r

def get(x):
    assert(x.tag == tag)
    return x.data

def set(x, val):
    assert(x.tag == tag)
    x.data = val
