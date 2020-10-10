'''
Created on 3 Oct 2020

Static method tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest
from datetime import datetime, timedelta

import pyubx2


class StaticTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUBX2Bytes(self):
        res = pyubx2.UBXMessage.ubx_str2bytes('CFG', 'CFG-MSG')
        self.assertEqual(res, (b'\x06', b'\x01'))

    def testBytes2Len(self):
        res = pyubx2.UBXMessage.bytes2len(b'\x18\x00')
        self.assertEqual(res, 24)

    def testLen2Bytes(self):
        res = pyubx2.UBXMessage.len2bytes(24)
        self.assertEqual(res, (b'\x18\x00'))

    def testKeyfromVal(self):
        res = pyubx2.UBXMessage.key_from_val(pyubx2.UBX_CLASSES, 'MON')
        self.assertEqual(res, (b'\x0A'))

    def testCalcChecksum(self):
        res = pyubx2.UBXMessage.calc_checksum(b'\x06\x01\x02\x00\xf0\x05')
        self.assertEqual(res, b'\xfe\x16')

    def testGoodChecksum(self):
        res = pyubx2.UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x16')
        self.assertTrue(res)

    def testBadChecksum(self):
        res = pyubx2.UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x15')
        self.assertFalse(res)

    def testitow2utc(self):
        res = str(pyubx2.UBXMessage.itow2utc(387092000))
        self.assertEqual(res, '11:31:16')

    def testgpsfix2str(self):
        fixs = ['NO FIX', 'DR', '2D', '3D', 'GPS + DR', 'TIME ONLY']
        for i, fix in enumerate(range (0, 6)):
            res = pyubx2.UBXMessage.gpsfix2str(fix)
            self.assertEqual(res, fixs[i])

    def testdop2str(self):
        dops = ['Ideal', 'Excellent', 'Good', 'Moderate', 'Fair', 'Poor']
        i = 0
        for dop in (1, 2, 5, 10, 20, 30):
            res = pyubx2.UBXMessage.dop2str(dop)
            self.assertEqual(res, dops[i])
            i += 1


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
