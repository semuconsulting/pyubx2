"""
Helper, Property and Static method tests for pyubx2.UBXMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from datetime import datetime

import pyubx2.ubxtypes_core as ubt
from pyubx2 import POLL, SET, UBX_CLASSES, UBXMessage, UBXReader
from pyubx2.ubxhelpers import (
    attsiz,
    att2idx,
    att2name,
    bytes2val,
    calc_checksum,
    cel2cart,
    cfgkey2name,
    cfgname2key,
    dop2str,
    escapeall,
    get_bits,
    getinputmode,
    gnss2str,
    gpsfix2str,
    hextable,
    isvalid_checksum,
    itow2utc,
    key_from_val,
    msgstr2bytes,
    process_monver,
    protocol,
    utc2itow,
    val2bytes,
    val2sphp,
    val2twoscomp,
    val2signmag,
)


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.streamNAV = open(os.path.join(dirname, "pygpsdata-NAV.log"), "rb")

    def tearDown(self):
        self.streamNAV.close()

    # def testDefinitions(self):  # DEBUG test for possible missing payload definitions
    #     for msg in ubt.UBX_MSGIDS.values():
    #         if (
    #             msg not in (ubp.UBX_PAYLOADS_POLL)
    #             and msg not in (ubg.UBX_PAYLOADS_GET)
    #             and msg not in (ubs.UBX_PAYLOADS_SET)
    #         ):
    #             print(f"Possible missing payload definition {msg}")
    #     for msg in ubg.UBX_PAYLOADS_GET:
    #         if msg not in ubt.UBX_MSGIDS.values():
    #             print(f"Possible missing core definition {msg} GET")
    #     for msg in ubs.UBX_PAYLOADS_SET:
    #         if msg not in ubt.UBX_MSGIDS.values():
    #             print(f"Possible missing core definition {msg} SET")
    #     for msg in ubp.UBX_PAYLOADS_POLL:
    #         if msg not in ubt.UBX_MSGIDS.values():
    #             print(f"Possible missing core definition {msg} POLL")

    def testFill_CFGMSG2(self):  # test msg_cls in bytes property
        EXPECTED_RESULT = "b'\\x06'"
        res = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.msg_cls), EXPECTED_RESULT)

    def testFill_CFGMSG3(self):  # test msg_id in bytes property
        EXPECTED_RESULT = "b'\\x01'"
        res = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.msg_id), EXPECTED_RESULT)

    def testFill_CFGMSG4(self):  # test msg length property
        # EXPECTED_RESULT = "b'\\x02\\x00'"
        EXPECTED_RESULT = 2
        res = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        self.assertEqual(res.length, EXPECTED_RESULT)

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [
            (2345, ubt.U2),
            (2345, ubt.E2),
            (1, ubt.L),
            (-2346789, ubt.I4),
            (b"\x44\x55", ubt.X2),
            (23.12345678, ubt.R4),
            (-23.12345678912345, ubt.R8),
            ([1, 2, 3, 4, 5], "A005"),
        ]
        EXPECTED_RESULTS = [
            b"\x29\x09",
            b"\x29\x09",
            b"\x01",
            b"\xdb\x30\xdc\xff",
            b"\x44\x55",
            b"\xd7\xfc\xb8\x41",
            b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0",
            b"\x01\x02\x03\x04\x05",
        ]
        for i, inp in enumerate(INPUTS):
            (val, att) = inp
            res = val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testBytes2Val(self):  # test conversion of bytes to value
        INPUTS = [
            (b"\x29\x09", ubt.U2),
            (b"\x29\x09", ubt.E2),
            (b"\x01", ubt.L),
            (b"\xdb\x30\xdc\xff", ubt.I4),
            (b"\x44\x55", ubt.X2),
            (b"\xd7\xfc\xb8\x41", ubt.R4),
            (b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0", ubt.R8),
            (b"\x01\x02\x03\x04\x05", "A005"),
        ]
        EXPECTED_RESULTS = [
            2345,
            2345,
            1,
            -2346789,
            b"\x44\x55",
            23.12345678,
            -23.12345678912345,
            [1, 2, 3, 4, 5],
        ]
        for i, inp in enumerate(INPUTS):
            (valb, att) = inp
            res = bytes2val(valb, att)
            if att == ubt.R4:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 6)
            elif att == ubt.R8:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 14)
            else:
                self.assertEqual(res, EXPECTED_RESULTS[i])

    def testUBX2Bytes(self):
        res = msgstr2bytes("CFG", "CFG-MSG")
        self.assertEqual(res, (b"\x06", b"\x01"))

    def testKeyfromVal(self):
        res = key_from_val(UBX_CLASSES, "MON")
        self.assertEqual(res, (b"\x0a"))

    def testCalcChecksum(self):
        res = calc_checksum(b"\x06\x01\x02\x00\xf0\x05")
        self.assertEqual(res, b"\xfe\x16")

    def testGoodChecksum(self):
        res = isvalid_checksum(b"\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x16")
        self.assertTrue(res)

    def testBadChecksum(self):
        res = isvalid_checksum(b"\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x15")
        self.assertFalse(res)

    def testitow2utc(self):
        res = str(itow2utc(387092000))
        self.assertEqual(res, "11:31:14")

    def testitow2utcLEAP(self):
        res = str(itow2utc(387092000, 16))
        self.assertEqual(res, "11:31:16")

    def testutc2itow(self):
        dt = datetime(2024, 2, 8, 11, 31, 14)
        res = utc2itow(dt)
        self.assertEqual(res, (2300, 387092000))

    def testutc2itowLEAP(self):
        dt = datetime(2024, 2, 8, 11, 31, 14)
        res = utc2itow(dt, 10)
        self.assertEqual(res, (2300, 387084000))

    def testgnss2str(self):
        GNSS = {
            0: "GPS",
            1: "SBAS",
            2: "Galileo",
            3: "BeiDou",
            4: "IMES",
            5: "QZSS",
            6: "GLONASS",
            7: "NAVIC",
            8: "8",
        }
        for i in range(0, 9):
            res = gnss2str(i)
            self.assertEqual(res, GNSS[i])

    def testgps2str(self):
        fixs = ["NO FIX", "DR", "2D", "3D", "GPS + DR", "TIME ONLY", "6"]
        for i, fix in enumerate(range(0, 7)):
            res = gpsfix2str(fix)
            self.assertEqual(res, fixs[i])

    def testdop2str(self):
        dops = [
            "N/A",
            "Ideal",
            "Ideal",
            "Excellent",
            "Excellent",
            "Good",
            "Moderate",
            "Fair",
            "Poor",
        ]
        i = 0
        for dop in (0, 0.9, 1, 1.4, 2, 5, 10, 20, 30):
            res = dop2str(dop)
            self.assertEqual(res, dops[i])
            i += 1

    def testcfgname2key(self):
        (key, typ) = cfgname2key("CFG_NMEA_PROTVER")
        self.assertEqual(key, 0x20930001)
        self.assertEqual(typ, ubt.E1)
        (key, typ) = cfgname2key("CFG_UART1_BAUDRATE")
        self.assertEqual(key, 0x40520001)
        self.assertEqual(typ, ubt.U4)

    def testcfgkey2type(self):
        (key, typ) = cfgkey2name(0x20510001)
        self.assertEqual(key, "CFG_I2C_ADDRESS")
        self.assertEqual(typ, ubt.U1)

    def testgetbits(self):
        INPUTS = [
            (b"\x89", 192),
            (b"\xc9", 3),
            (b"\x89", 9),
            (b"\xc9", 9),
            (b"\x18\x18", 8),
            (b"\x18\x20", 8),
        ]
        EXPECTED_RESULTS = [2, 1, 9, 9, 1, 0]
        for i, (vb, mask) in enumerate(INPUTS):
            vi = get_bits(vb, mask)
            self.assertEqual(vi, EXPECTED_RESULTS[i])

    def testgetmsgmode(self):  # test msgmode getter
        EXPECTED_RESULT = 2
        res = UBXMessage("CFG", "CFG-MSG", POLL, msgClass=240, msgID=5)
        self.assertEqual(res.msgmode, EXPECTED_RESULT)

    def testdatastream(self):  # test datastream getter
        EXPECTED_RESULT = "<class '_io.BufferedReader'>"
        res = str(type(UBXReader(self.streamNAV).datastream))
        self.assertEqual(res, EXPECTED_RESULT)

    def testprotocol(self):  # test protocol() method
        res = protocol(b"\xb5b\x06\x01\x02\x00\xf0\x05\xfe\x16")
        self.assertEqual(res, ubt.UBX_PROTOCOL)
        res = protocol(b"$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n")
        self.assertEqual(res, ubt.NMEA_PROTOCOL)
        res = protocol(b"$PGRMM,WGS84*26\r\n")
        self.assertEqual(res, ubt.NMEA_PROTOCOL)
        res = protocol(b"\xd3\x00\x04L\xe0\x00\x80\xed\xed\xd6")
        self.assertEqual(res, ubt.RTCM3_PROTOCOL)
        res = protocol(b"aPiLeOfGarBage")
        self.assertEqual(res, 0)

    def testhextable(self):  # test hextable*( method)
        EXPECTED_RESULT = "000: 2447 4e47 4c4c 2c35 3332 372e 3034 3331  | b'$GNGLL,5327.0431'                                                 |\n016: 392c 532c 3030 3231 342e 3431 3339 362c  | b'9,S,00214.41396,'                                                 |\n032: 452c 3232 3332 3332 2e30 302c 412c 412a  | b'E,223232.00,A,A*'                                                 |\n048: 3638 0d0a                                | b'68\\r\\n'                                                           |\n"
        res = hextable(b"$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n", 8)
        self.assertEqual(res, EXPECTED_RESULT)

    def testattsiz(self):  # test attsiz
        self.assertEqual(attsiz("CH"), -1)
        self.assertEqual(attsiz("C032"), 32)

    def testatt2idx(self):  # test att2idx
        EXPECTED_RESULT = [4, 16, 101, 0, (3, 6), 0]
        atts = ["svid_04", "gnssId_16", "cno_101", "gmsLon", "gnod_03_06", "dodgy_xx"]
        for i, att in enumerate(atts):
            res = att2idx(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testatt2name(self):  # test att2name
        EXPECTED_RESULT = ["svid", "gnssId", "cno", "gmsLon"]
        atts = ["svid_04", "gnssId_16", "cno_101", "gmsLon"]
        for i, att in enumerate(atts):
            res = att2name(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testcel2cart(self):
        (elev, azim) = cel2cart(34, 128)
        self.assertAlmostEqual(elev, -0.510406, 5)
        self.assertAlmostEqual(azim, 0.653290, 5)
        (elev, azim) = cel2cart("xxx", 128)
        self.assertEqual(elev, 0)

    def testescapeall(self):
        EXPECTED_RESULT = "b'\\x68\\x65\\x72\\x65\\x61\\x72\\x65\\x73\\x6f\\x6d\\x65\\x63\\x68\\x61\\x72\\x73'"
        val = b"herearesomechars"
        res = escapeall(val)
        print(res)
        self.assertEqual(res, EXPECTED_RESULT)

    def testval2sphp(self):
        res = val2sphp(100.123456789)
        self.assertEqual(res, (1001234567, 89))
        res = val2sphp(-13.987654321)
        self.assertEqual(res, (-139876543, -21))
        res = val2sphp(5.9876543)
        self.assertEqual(res, (59876543, 0))

    def testgetinputmode(self):
        res = getinputmode(UBXMessage("CFG", "CFG-ODO", POLL).serialize())
        self.assertEqual(res, POLL)
        res = getinputmode(
            UBXMessage.config_poll(0, 0, ["CFG_UART1_BAUDRATE", 0x40530001]).serialize()
        )
        self.assertEqual(res, POLL)
        res = getinputmode(
            UBXMessage.config_set(
                0, 0, [("CFG_UART1_BAUDRATE", 9600), (0x40530001, 115200)]
            ).serialize()
        )
        self.assertEqual(res, SET)
        res = getinputmode(
            UBXMessage.config_del(0, 0, ["CFG_UART1_BAUDRATE", 0x40530001]).serialize()
        )
        self.assertEqual(res, SET)
        res = getinputmode(UBXMessage("CFG", "CFG-INF", POLL, protocolID=1).serialize())
        self.assertEqual(res, POLL)
        res = getinputmode(
            UBXMessage(
                "CFG", "CFG-INF", SET, protocolID=1, infMsgMask_01=1, infMsgMask_02=1
            ).serialize()
        )
        self.assertEqual(res, SET)

    def testprocess_monver(self):
        MONVER = b"\xb5\x62\x0a\x04\xdc\x00\x45\x58\x54\x20\x43\x4f\x52\x45\x20\x31\x2e\x30\x30\x20\x28\x66\x31\x37\x30\x36\x37\x29\x00\x00\x00\x00\x00\x00\x00\x00\x30\x30\x31\x39\x30\x30\x30\x30\x00\x00\x52\x4f\x4d\x20\x42\x41\x53\x45\x20\x30\x78\x31\x31\x38\x42\x32\x30\x36\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x46\x57\x56\x45\x52\x3d\x48\x50\x47\x20\x31\x2e\x35\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x50\x52\x4f\x54\x56\x45\x52\x3d\x32\x37\x2e\x35\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4d\x4f\x44\x3d\x5a\x45\x44\x2d\x46\x39\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x47\x50\x53\x3b\x47\x4c\x4f\x3b\x47\x41\x4c\x3b\x42\x44\x53\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x53\x42\x41\x53\x3b\x51\x5a\x53\x53\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xce\x8b"
        msg = UBXReader.parse(MONVER)
        EXPECTED_RESULT = {
            "swversion": "Flash 1.00 (f17067)",
            "hwversion": "ZED-F9P 00190000",
            "fwversion": "HPG 1.50",
            "romversion": "27.50",
            "gnss": "GPS GLO GAL BDS SBAS QZSS ",
        }
        res = process_monver(msg)
        self.assertEqual(res, EXPECTED_RESULT)

    def testval2twoscomp(self):
        res = val2twoscomp(10, "U24")
        self.assertEqual(res, 0b0000000000000000000001010)
        res = val2twoscomp(-10, "U24")
        self.assertEqual(res, 0b111111111111111111110110)

    def testval2signmag(self):
        res = val2signmag(10, "U24")
        self.assertEqual(res, 0b0000000000000000000001010)
        res = val2signmag(-10, "U24")
        self.assertEqual(res, 0b1000000000000000000001010)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
