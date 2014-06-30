#!/usr/bin/env python2

""" Implementation of T05 string object. """

import types
import os
import t05_Tag
import t05_Object


class t05_StringTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return lhs.data == rhs.data

    def name(self):
        return "string"

tag = t05_StringTag()

def create(state, x):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.data = x
    r.state = state
    return r

def proto(state):
    r = create(state, "")
    t05_Object.addMethod(r, "write", write_)
    return r

def new(state, x):
    r = create(state, x)
    r.addParent(state.protos.string)
    return r

def get(x):
    assert(x.tag == tag)
    return x.data

def set(x, val):
    assert(x.tag == tag)
    assert(type(val) == types.StringType)
    x.data = val

def write_(vm, self, acob, node):
    os.sys.stdout.write(get(self))
