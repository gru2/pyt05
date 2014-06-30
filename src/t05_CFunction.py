#!/usr/bin/env python2

""" Implementation of T05 C (python) function object. """

import types
import os
import t05_Tag
import t05_Object


class t05_CFunctionTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return lhs.data == rhs.data

    def name(self):
        return "cfunction"

tag = t05_CFunctionTag()

def create(state, x):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.data = x
    r.state = state
    return r

def proto(state):
    r = create(state, None)
    return r

def new(state, x):
    r = create(state, x)
    r.addParent(state.protos.cFunction)
    return r

def get(x):
    assert(x.tag == tag)
    return x.data

def set(x, val):
    assert(x.tag == tag)
    #assert(type(val) == types.StringType)
    x.data = val
