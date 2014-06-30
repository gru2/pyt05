#!/usr/bin/env python2

""" Implementation of T05 integer object. """

import types
import os
import t05_Tag
import t05_Object
import t05_SourceCodePosition


NODE_UNINITIALIZED = "UNINITIALIZED"
NODE_SELECT = "SELECT"
NODE_UNOP = "UNOP"
NODE_GROUP = "GROUP"
NODE_SLOT = "SLOT"
NODE_BRACKET = "BRACKET"
NODE_IDENTIFIER = "IDENTIFIER"
NODE_LITERAL = "LITERAL"
NODE_BLOCK = "BLOCK"
NODE_ARGUMENTS = "ARGUMENTS" 
NODE_OPERATION = "OPERATION"
NODE_OBJECT_LITERAL = "OBJECT_LITERAL" 

class Node:
    
    def __init__(self):
        self.type = 0
        self.args = []
        self.value = None
        self.next = None;
        self.literal = None
        self.object = None   # Object which contains this node.
        self.sourceCodePosition = t05_SourceCodePosition.SourceCodePosition();


class t05_NodeTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return lhs.data == rhs.data

    def name(self):
        return "node"

tag = t05_NodeTag()

def create(state):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.data = Node()
    r.state = state
    return r

def proto(state):
    r = create(state)
    return r

def new(state):
    r = create(state)
    r.addParent(state.protos.node)
    return r

def get(x):
    assert(x.tag == tag)
    return x.data

def set(x, val):
    assert(x.tag == tag)
    x.data = val
