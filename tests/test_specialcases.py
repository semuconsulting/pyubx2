'''
Created on 3 Oct 2020

Special case tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest

import pyubx2


class SpecialTest(unittest.TestCase):

    def setUp(self):
        self.cfg_rinv2 = b'\xb5b\x06\x34\x03\x00\x03\x07\x04\x4b\x8c'
        self.cfg_rinv7 = b'\xb5b\x06\x34\x08\x00\x03\x01\x02\x03\x04\x05\x06\x07\x61\x40'
        self.cfg_rinv0 = b'\xb5b\x06\x34\x01\x00\x03\x3e\xf4'

    def tearDown(self):
        pass

    def testCfg_Rinv2(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv2, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testCfg_Rinv2ID(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv2, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv2Str(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv2, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03', data_01=7, data_02=4)>")

    def testCfg_Rinv7(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv7, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testCfg_Rinv7ID(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv7, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv7Str(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv7, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03', data_01=1, data_02=2, data_03=3, data_04=4, data_05=5, data_06=6, data_07=7)>")

    def testCfg_Rinv0(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv0, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testCfg_Rinv0ID(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv0, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv0Str(self):
        res = pyubx2.UBXMessage.parse(self.cfg_rinv0, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03')>")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
