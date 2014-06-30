#!/usr/bin/env python2

""" Unit tests for t05_Integer.py """

import t05_Integer
import unittest


state = "state"


class t05_IntegerTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Integer.create(state, 10)

    def testGetSet(self):
        x = t05_Integer.create(state, 5)
        r = t05_Integer.get(x)
        self.assertEqual(r, 5)

        t05_Integer.set(x, 3)
        r2 = t05_Integer.get(x)
        self.assertEqual(r2, 3)
        

if __name__ == '__main__':
	unittest.main()
