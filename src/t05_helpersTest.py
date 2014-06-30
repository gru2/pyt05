#!/usr/bin/env python2

""" Unit tests for t05_Null.py """

import t05_Object
import t05_Null
import t05_Bool
import t05_Integer
import t05_String
import t05_helpers
import unittest


state = "state"


class t05_HelperTest(unittest.TestCase):

    def testToString1(self):
        x = t05_Null.create(state)
        r = t05_helpers.toString(x)
        self.assertEqual(r, "null")

    def testToString2(self):
        x = t05_Bool.create(state, True)
        r = t05_helpers.toString(x)
        self.assertEqual(r, "true")

    def testToString3(self):
        x = t05_Bool.create(state, False)
        r = t05_helpers.toString(x)
        self.assertEqual(r, "false")

    def testToString4(self):
        x = t05_Integer.create(state, 841)
        r = t05_helpers.toString(x)
        self.assertEqual(r, "841")

    def testToString5(self):
        x = t05_String.create(state, "pera")
        r = t05_helpers.toString(x)
        self.assertEqual(r, "'pera'")

    def testToString6(self):
        x = t05_Object.create(state)
        x.addSlot(t05_String.create(state, "pera"), t05_Integer.create(state, 12))
        x.addSlot(t05_String.create(state, "ww"), t05_Integer.create(state, 5))
        print("x = " + t05_helpers.toString(x))

    def testToString7(self):
        x2 = t05_Object.create(state)
        for i in range(1, 16):
            x2.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i))
        print("x2 = " + t05_helpers.toString(x2))

    def testToString7(self):
        x3 = t05_Object.create(state)
        for i in range(1, 20):
            x3.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i))
        x4 = t05_Object.create(state)
        for i in range(1, 20):
            x4.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i*i))
        x5 = t05_Object.create(state)
        for i in range(1, 5):
            x5.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i*i*i))
        x3.addSlot(t05_String.create(state, "x4"), x4)
        x3.addSlot(t05_String.create(state, "x5"), x5)
        print("x3 = " + t05_helpers.toString(x3))

    def testToString8(self):
        x3 = t05_Object.create(state)
        for i in range(1, 20):
            x3.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i))
        x4 = t05_Object.create(state)
        for i in range(1, 20):
            x4.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i*i))
        x5 = t05_Object.create(state)
        for i in range(1, 5):
            x5.addSlot(t05_Integer.create(state, i), t05_Integer.create(state, i*i*i*i))
        x3.addSlot(t05_String.create(state, "x4"), x4)
        x3.addSlot(t05_String.create(state, "x5"), x5)
        x3.addSlot(t05_String.create(state, "x5.1"), x5)
        print("x3 = " + t05_helpers.toString(x3))


if __name__ == '__main__':
	unittest.main()
