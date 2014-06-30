#!/usr/bin/env python2

""" Unit tests for t05_String.py """

import t05_String
import unittest


state = "state"

class t05_StringTest(unittest.TestCase):

    def testCreation(self):
        x = t05_String.create(state, "test string")

    def testStringWrite(self):
        x = t05_String.create(state, "\ntest string\n")
        t05_String.write_(None, x, None, None)

    def testGetSet(self):
        x = t05_String.create(state, "xyz")
        r = t05_String.get(x)
        self.assertEqual(r, "xyz")

        t05_String.set(x, "foo bar")
        r = t05_String.get(x)
        self.assertEqual(r, "foo bar")


if __name__ == '__main__':
	unittest.main()
