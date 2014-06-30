#!/usr/bin/env python2

""" Unit tests for InputStream.py """

import t05_InputStream
import t05_SourceCodePosition
import unittest

scp = t05_SourceCodePosition.SourceCodePosition()
scp.unitName = "test"

class InputStreamTest(unittest.TestCase):

    def test01(self):
        istr = t05_InputStream.InputStream()
        istr.openString("AB", scp)
        c1 = istr.getChar()
        self.assertEqual(c1, "A")
        c2 = istr.getChar()
        self.assertEqual(c2, "B")
        istr.putBackChar()
        istr.putBackChar()
        c1 = istr.getChar()
        self.assertEqual(c1, "A")
        pos = istr.getStreamPosition()
        c2 = istr.getChar()
        self.assertEqual(c2, "B")
        c3 = istr.getChar()
        self.assertEqual(c3, "EOF")
        istr.setStreamPosition(pos)
        c2 = istr.getChar()
        self.assertEqual(c2, "B")
        c3 = istr.getChar()
        self.assertEqual(c3, "EOF")


if __name__ == '__main__':
    unittest.main()
