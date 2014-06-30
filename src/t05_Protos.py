#!/usr/bin/env python2

""" Implementation of T05 protos object. """

import t05_Object
import t05_String
import t05_Integer
import t05_Null
import t05_Node
import t05_Acob
import t05_Bool
import t05_CFunction

class Protos:

    def __init__(self):
        self.object = None
        self.string = None
        self.cFunction = None
        self.function = None
        self.integer = None
        self.node = None
        self.acob = None
        self.bool = None
        self.null = None

    def init(self, state):
        self.object = t05_Object.proto(state)
        self.string = t05_String.proto(state)
        self.integer = t05_Integer.proto(state)
        self.null = t05_Null.proto(state)
        self.node = t05_Node.proto(state)
        self.acob = t05_Acob.proto(state)
        self.bool = t05_Bool.proto(state)
        self.cFunction = t05_CFunction.proto(state)

        t05_Object.addStdProtos(self.object)
        t05_Object.addStdSlots(self.object)
