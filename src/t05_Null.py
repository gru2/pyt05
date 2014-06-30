#!/usr/bin/env python2

""" Implementation of T05 null object. """

import types
import os
import t05_Tag
import t05_Object


class t05_NullTag(t05_Tag.t05_Tag):

    def equal(self, lhs, rhs):
        return True

    def name(self):
        return "null"

tag = t05_NullTag()

def create(state):
    r = t05_Object.t05_Object()
    r.tag = tag
    r.state = state
    return r

def proto(state):
    r = create(state)
    return r
