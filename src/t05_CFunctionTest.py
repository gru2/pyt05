#!/usr/bin/env python2

""" Unit tests for t05_CFunction.py """

import t05_CFunction
import unittest


state = "state"


def foo(x):
    return x + 5;


def bar(x):
    return x + 12;


class t05_CFunctionTest(unittest.TestCase):

    def testCreation(self):
        x = t05_CFunction.create(state, foo)

    def testGetSet(self):
        x = t05_CFunction.create(state, foo)
        r = t05_CFunction.get(x)
        self.assertEqual(r, foo)

        t05_CFunction.set(x, bar)
        r2 = t05_CFunction.get(x)
        self.assertEqual(r2, bar)

        self.assertEqual(r(3), 8)
        self.assertEqual(r2(10), 22)
        

if __name__ == '__main__':
	unittest.main()
