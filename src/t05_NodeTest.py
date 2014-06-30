#!/usr/bin/env python2

""" Unit tests for t05_Node.py """

import t05_Node
import unittest


state = "state"


class t05_NodeTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Node.create(state)

    def testGetSet(self):
        x = t05_Node.create(state)
        r = t05_Node.get(x)

        n2 = t05_Node.Node()
        t05_Node.set(x, n2)
        r2 = t05_Node.get(x)
        self.assertEqual(r2, n2)
        

if __name__ == '__main__':
    unittest.main()
