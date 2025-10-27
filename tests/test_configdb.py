"""
Sanity check of configdb key definitions

Does a simple comparison between the active ubxtypes_configdb key definitions and a
baselined copy to check for inadvertant corruption.

Created on 19 Apr 2021

@author: semuadmin
"""

import unittest

from pyubx2 import UBXMessage, SET, POLL, SET_LAYER_FLASH, TXN_NONE, SET_LAYER_BBR
from pyubx2.ubxtypes_configdb import UBX_CONFIG_DATABASE
from tests.configdb_baseline import UBX_CONFIG_DATABASE_BASELINE


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testConfigDB(self):  # sanity check against baselined configdb definitions
        for keyname, keytuple in UBX_CONFIG_DATABASE.items():
            keyid, _ = keytuple
            try:
                keytuple2 = UBX_CONFIG_DATABASE_BASELINE[keyname]
                keyid2, _ = keytuple2
                self.assertEqual(keyid, keyid2)
            except KeyError:
                pass  # ignore any keys added since baseline

    def testFill_CFGVALGET(self):  #  test CFG-VALGET POLL constructor
        EXPECTED_RESULT = "<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=1079115777, keys_02=1079181313)>"
        res = UBXMessage(
            "CFG",
            "CFG-VALGET",
            POLL,
            payload=b"\x00\x01\x00\x00\x01\x00\x52\x40\x01\x00\x53\x40",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGVALDEL(self):  #  test CFG-VALDEL SET constructor
        EXPECTED_RESULT = "<UBX(CFG-VALDEL, version=0, bbr=1, flash=0, action=0, reserved0=0, keys_01=1079115777, keys_02=16798528)>"
        res = UBXMessage(
            "CFG",
            "CFG-VALDEL",
            SET,
            payload=b"\x00\x03\x00\x00\x01\x00\x52\x40\x40\x53\x00\x01",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGVALSET(self):  #  test CFG-VALSET SET constructor
        EXPECTED_RESULT = "<UBX(CFG-VALSET, version=0, ram=1, bbr=1, flash=0, action=0, reserved0=0, CFG_UART1_BAUDRATE=9600)>"
        res = UBXMessage(
            "CFG",
            "CFG-VALSET",
            SET,
            payload=b"\x00\x03\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testGOODConfigSet(self):
        EXPECTED_RESULT = "<UBX(CFG-VALSET, version=0, ram=0, bbr=0, flash=1, action=0, reserved0=0, CFG_NAVSPG_USRDAT_ROTZ=0.0, CFG_NAVSPG_USRDAT_ROTY=0.10000000149011612)>"
        msg = UBXMessage.config_set(
            layers=SET_LAYER_FLASH,
            transaction=TXN_NONE,
            cfgData=[(0x40110069, 0), (0x40110068, 0.1)],
        )
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT)

    def testHYPHENConfigSet(self):
        EXPECTED_RESULT1 = "<UBX(CFG-VALSET, version=0, ram=0, bbr=1, flash=0, action=0, reserved0=0, CFG_MSGOUT_UBX_RXM_RAWX_UART1=1, CFG_MSGOUT_UBX_RXM_SFRBX_UART1=1)>"
        EXPECTED_RESULT2 = "<UBX(CFG-VALGET, version=0, layer=2, position=0, keys_01=546374309, keys_02=546374194)>"
        EXPECTED_RESULT3 = "<UBX(CFG-VALDEL, version=0, bbr=1, flash=0, action=0, reserved0=0, keys_01=546374309, keys_02=546374194)>"
        layers = SET_LAYER_BBR  # battery-backed RAM (non-volatile)
        transaction = TXN_NONE
        cfgdata = [
            ("CFG-MSGOUT-UBX_RXM_RAWX_UART1", 1),
            ("CFG-MSGOUT-UBX_RXM_SFRBX_UART1", 1),
        ]
        msg = UBXMessage.config_set(layers, transaction, cfgdata)
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT1)
        cfgdata = [nam for (nam, val) in cfgdata]
        msg = UBXMessage.config_poll(layers, transaction, cfgdata)
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT2)
        msg = UBXMessage.config_del(layers, transaction, cfgdata)
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
