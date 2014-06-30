#!/usr/bin/env python2

""" Unit tests for t05_Null.py """

import t05_Null
import unittest


state = "state"


class t05_NullTest(unittest.TestCase):

    def testCreation(self):
        x = t05_Null.create(state)


if __name__ == '__main__':
	unittest.main()
