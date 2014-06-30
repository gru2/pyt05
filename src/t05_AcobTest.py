#!/usr/bin/env python2

""" Unit tests for t05_Acob.py """

import t05_Acob
import unittest


state = "state"


class t05_NodeTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Acob.create(state)

    def testGetSet(self):
        x = t05_Acob.create(state)
        r = t05_Acob.get(x)

        n2 = t05_Acob.Acob()
        t05_Acob.set(x, n2)
        r2 = t05_Acob.get(x)
        self.assertEqual(r2, n2)
        

if __name__ == '__main__':
    unittest.main()
