#!/usr/bin/env python2

""" Implementation of T05 Operator class. """

import t05_String


ASSOC_LEFT = 0
ASSOC_RIGHT = 1

POSITION_PREFIX = 1
POSITION_POSTFIX = 2
POSITION_INFIX = 4
POSITION_DELIMITER = 8

PRECEDENCE_MIN = 0
PRECEDENCE_SLOT = 1
PRECEDENCE_COMMA = 2
PRECEDENCE_ASSIGNMENT = 3
PRECEDENCE_GROUP = 4
PRECEDENCE_COMPARE = 5
PRECEDENCE_ADD_SUB = 6
PRECEDENCE_MUL_DIV = 7
PRECEDENCE_UNARY_NEG = 8
PRECEDENCE_INDEX = 10
PRECEDENCE_DOT = 11

class Operator:

    def __init__(self):
        self.name = ""
        self.nameAsObject = None
        self.tokenType = None
        self.precedence = PRECEDENCE_MIN
        self.associativity = ASSOC_LEFT
        self.position = POSITION_INFIX

    def setName(self, opName, state):
        self.name = opName
        self.nameAsObject = t05_String.new(state, opName)
