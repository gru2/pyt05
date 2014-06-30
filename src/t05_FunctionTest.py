#!/usr/bin/env python2

""" Unit tests for t05_CFunction.py """

import t05_Function
import t05_Node
import unittest


state = "state"

node = t05_Node.create(state)
node2 = t05_Node.create(state)

class t05_CFunctionTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Function.create(state, node)

    def testGetSet(self):
        x = t05_Function.create(state, node)
        r = t05_Function.get(x)
        self.assertEqual(r, node)

        t05_Function.set(x, node2)
        r2 = t05_Function.get(x)
        self.assertEqual(r2, node2)

        self.assertEqual(r, node)
        self.assertEqual(r2, node2)
        

if __name__ == '__main__':
	unittest.main()
