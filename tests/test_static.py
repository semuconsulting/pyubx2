'''
Created on 3 Oct 2020

Static method tests for pyubx2.UBXMessage

@author: semuadmin
'''

import unittest

from pyubx2 import UBXMessage, UBX_CLASSES


class StaticTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUBX2Bytes(self):
        res = UBXMessage.msgstr2bytes('CFG', 'CFG-MSG')
        self.assertEqual(res, (b'\x06', b'\x01'))

    def testBytes2Len(self):
        res = UBXMessage.bytes2len(b'\x18\x00')
        self.assertEqual(res, 24)

    def testLen2Bytes(self):
        res = UBXMessage.len2bytes(24)
        self.assertEqual(res, (b'\x18\x00'))

    def testKeyfromVal(self):
        res = UBXMessage.key_from_val(UBX_CLASSES, 'MON')
        self.assertEqual(res, (b'\x0A'))

    def testCalcChecksum(self):
        res = UBXMessage.calc_checksum(b'\x06\x01\x02\x00\xf0\x05')
        self.assertEqual(res, b'\xfe\x16')

    def testGoodChecksum(self):
        res = UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x16')
        self.assertTrue(res)

    def testBadChecksum(self):
        res = UBXMessage.isvalid_checksum(b'\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x15')
        self.assertFalse(res)

    def testitow2utc(self):
        res = str(UBXMessage.itow2utc(387092000))
        self.assertEqual(res, '11:31:16')

    def testgnss2str(self):
        GNSS = {0: 'GPS', 1: 'SBAS', 2: 'Galileo', 3: 'BeiDou',
                4: 'IMES', 5: 'QZSS', 6: 'GLONASS', 7: "7"}
        for i in range (0, 8):
            res = UBXMessage.gnss2str(i)
            self.assertEqual(res, GNSS[i])

    def testgps2str(self):
        fixs = ['NO FIX', 'DR', '2D', '3D', 'GPS + DR', 'TIME ONLY']
        for i, fix in enumerate(range (0, 6)):
            res = UBXMessage.gpsfix2str(fix)
            self.assertEqual(res, fixs[i])

    def testdop2str(self):
        dops = ['Ideal', 'Excellent', 'Good', 'Moderate', 'Fair', 'Poor']
        i = 0
        for dop in (1, 2, 5, 10, 20, 30):
            res = UBXMessage.dop2str(dop)
            self.assertEqual(res, dops[i])
            i += 1

    def testcfgname2key(self):
        (key, typ) = UBXMessage.cfgname2key("CFG-NMEA-PROTVER")
        self.assertEqual(key, 0x20930001)
        self.assertEqual(typ, "E01")
        (key, typ) = UBXMessage.cfgname2key("CFG-UART1-BAUDRATE")
        self.assertEqual(key, 0x40520001)
        self.assertEqual(typ, "U04")

    def testcfgkey2type(self):
        (key, typ) = UBXMessage.cfgkey2name(0x20510001)
        self.assertEqual(key, "CFG-I2C-ADDRESS")
        self.assertEqual(typ, "U01")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
