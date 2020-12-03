'''
Created on 3 Oct 2020

Special case tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest

from pyubx2 import UBXMessage
import pyubx2.ubxtypes_configdb as ubxcdb


class SpecialTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.cfg_rinv2 = b'\xb5b\x06\x34\x03\x00\x03\x07\x04\x4b\x8c'
        self.cfg_rinv7 = b'\xb5b\x06\x34\x08\x00\x03\x01\x02\x03\x04\x05\x06\x07\x61\x40'
        self.cfg_rinv0 = b'\xb5b\x06\x34\x01\x00\x03\x3e\xf4'

    def tearDown(self):
        pass

    def testCfg_Rinv2(self):
        res = UBXMessage.parse(self.cfg_rinv2, True)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv2ID(self):
        res = UBXMessage.parse(self.cfg_rinv2, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv2Str(self):
        res = UBXMessage.parse(self.cfg_rinv2, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03', data_01=7, data_02=4)>")

    def testCfg_Rinv7(self):
        res = UBXMessage.parse(self.cfg_rinv7, True)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv7ID(self):
        res = UBXMessage.parse(self.cfg_rinv7, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv7Str(self):
        res = UBXMessage.parse(self.cfg_rinv7, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03', data_01=1, data_02=2, data_03=3, data_04=4, data_05=5, data_06=6, data_07=7)>")

    def testCfg_Rinv0(self):
        res = UBXMessage.parse(self.cfg_rinv0, True)
        self.assertIsInstance(res, UBXMessage)

    def testCfg_Rinv0ID(self):
        res = UBXMessage.parse(self.cfg_rinv0, True)
        self.assertEqual(res.identity, 'CFG-RINV')

    def testCfg_Rinv0Str(self):
        res = UBXMessage.parse(self.cfg_rinv0, True)
        self.assertEqual(str(res), "<UBX(CFG-RINV, flags=b'\\x03')>")

    def testConfigSet(self):  # test creation of CFG-VALSET message with single key
        cfgData = [("CFG_UART1_BAUDRATE", 9600)]
        res = UBXMessage.config_set(ubxcdb.SET_LAYER_RAM, ubxcdb.TXN_NONE, cfgData)
        self.assertEqual(str(res), "<UBX(CFG-VALSET, version=0, layers=b'\\x01', transaction=0, reserved0=0, cfgData_01=1, cfgData_02=0, cfgData_03=82, cfgData_04=64, cfgData_05=128, cfgData_06=37, cfgData_07=0, cfgData_08=0)>")

    def testConfigSet2(self):  # test creation of CFG-VALSET message with multiple keys as transaction
        cfgData = [("CFG_UART1_BAUDRATE", 9600), (0x40530001, 115200)]
        res = UBXMessage.config_set(ubxcdb.SET_LAYER_BBR, ubxcdb.TXN_START, cfgData)
        self.assertEqual(str(res), "<UBX(CFG-VALSET, version=1, layers=b'\\x02', transaction=1, reserved0=0, cfgData_01=1, cfgData_02=0, cfgData_03=82, cfgData_04=64, cfgData_05=128, cfgData_06=37, cfgData_07=0, cfgData_08=0, cfgData_09=1, cfgData_10=0, cfgData_11=83, cfgData_12=64, cfgData_13=0, cfgData_14=194, cfgData_15=1, cfgData_16=0)>")

    def testConfigDel(self):  # test creation of CFG-VALSET message with single key
        keys = ["CFG_UART1_BAUDRATE", ]
        res = UBXMessage.config_del(ubxcdb.SET_LAYER_BBR, ubxcdb.TXN_NONE, keys)
        self.assertEqual(str(res), "<UBX(CFG-VALDEL, version=0, layers=b'\\x02', transaction=b'\\x00', reserved0=0, keys_01=1079115777)>")

    def testConfigDel2(self):  # test creation of CFG-VALSET message with multiples keys as transaction
        keys = ["CFG_UART1_BAUDRATE", 0x40530001]
        res = UBXMessage.config_del(ubxcdb.SET_LAYER_FLASH, ubxcdb.TXN_START, keys)
        self.assertEqual(str(res), "<UBX(CFG-VALDEL, version=1, layers=b'\\x04', transaction=b'\\x01', reserved0=0, keys_01=1079115777, keys_02=1079181313)>")

    def testConfigPoll(self):  # test creation of CFG-VALGET message with multiple keys
        keys = ["CFG_UART1_BAUDRATE", 0x40530001]
        res = UBXMessage.config_poll(ubxcdb.POLL_LAYER_FLASH, 0, keys)
        self.assertEqual(str(res), "<UBX(CFG-VALGET, version=0, layer=2, position=0, keys_01=1079115777, keys_02=1079181313)>")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
