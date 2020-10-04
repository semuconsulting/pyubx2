'''
Created on 3 Oct 2020

Static method tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest

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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
