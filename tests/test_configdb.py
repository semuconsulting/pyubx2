"""
Sanity check of configdb key definitions

Does a simple comparison between the active ubxtypes_configdb key definitions and a
baselined copy to check for inadvertant corruption.

Created on 19 Apr 2021 

@author: semuadmin
"""

import unittest

from pyubx2 import UBXMessage, SET, POLL
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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
