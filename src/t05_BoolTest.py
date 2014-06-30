#!/usr/bin/env python2

""" Unit tests for t05_Bool.py """

import t05_Bool
import unittest


state = "state"


class t05_BoolTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Bool.create(state, False)

    def testGetSet(self):
        x = t05_Bool.create(state, False)
        r = t05_Bool.get(x)
        self.assertEqual(r, False)

        t05_Bool.set(x, True)
        r2 = t05_Bool.get(x)
        self.assertEqual(r2, True)
        

if __name__ == '__main__':
	unittest.main()
