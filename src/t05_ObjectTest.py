#!/usr/bin/env python2

""" Unit tests for t05_Object.py """

import t05_Object
import t05_Integer
import t05_String
import unittest

state = "state"

class t05_ObjectTest(unittest.TestCase):

    def testObjectCreation(self):
        o1 = t05_Object.create(state)
        self.assertEqual(o1.state, state)

    def testSettersAndGetters1(self):
        o1 = t05_Object.create(state)
        key = t05_Object.create(state)
        val = t05_Object.create(state)
        o1.addSlot(key, val)
        r = o1.getSlot(key)
        self.assertEqual(r, val)

        key2 = t05_Object.create(state)
        val2 = t05_Object.create(state)
        o1.addSlot(key2, val2)
        r = o1.getSlot(key)
        r2 = o1.getSlot(key2)
        self.assertEqual(r, val)
        self.assertEqual(r2, val2)

    def testDeleteSlot(self):
        o1 = t05_Object.create(state)
        key = t05_Object.create(state)
        val = t05_Object.create(state)
        o1.addSlot(key, val)
        key2 = t05_Object.create(state)
        val2 = t05_Object.create(state)
        o1.addSlot(key2, val2)

        o1.deleteSlot(key)
        r = o1.getSlot(key)
        r2 = o1.getSlot(key2)
        self.assertEqual(r, None)
        self.assertEqual(r2, val2)

    def testSettersAndGetters2(self):
        o1 = t05_Object.create(state)
        key = t05_String.create(state, "pera")
        val = t05_Integer.create(state, 22)
        o1.addSlot(key, val)
        key2 = t05_String.create(state, "pera")
        r = o1.getSlot(key2)
        ri = t05_Integer.get(r)
        self.assertEqual(ri, 22)


if __name__ == '__main__':
	unittest.main()

