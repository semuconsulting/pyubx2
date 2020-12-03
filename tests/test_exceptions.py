'''
Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

Exception handling tests for UBXMessage constructor and parse

@author: semuadmin
'''

import unittest

from pyubx2 import UBXMessage, UBXTypeError, UBXParseError, UBXMessageError, GET, SET, POLL


class ExceptionTest(unittest.TestCase):

    def setUp(self):
        self.bad_hdr = b'\xb0b\x05\x01\x02\x00\x06\x01\x0f\x38'
        self.bad_len = b'\xb5b\x05\x01\x03\x00\x06\x01\x0f\x37'
        self.bad_msg = b'\xb5b\x66\x66\x02\x00\x06\x01\xd5\x77'
        self.maxDiff = None

    def tearDown(self):
        pass

    def testAckCkT(self):  # bad checksum
        EXPECTED_ERROR = "Message checksum (.*) invalid - should be (.*)"
        ack_ack_badck = b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37'
        with self.assertRaisesRegex(UBXParseError, EXPECTED_ERROR):
            UBXMessage.parse(ack_ack_badck, True)

    def testFill_CFGNMEA(self):  # incorrect type (integer not binary)
        EXPECTED_ERROR = "Incorrect type for attribute 'filter' in SET message class CFG-NMEA"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-NMEA', SET, filter=45, nmeaVersion='xx', numSV=4, flags=14)

    def testFill_CFGDAT(self):  # incorrect type (string not integer)
        EXPECTED_ERROR = "Incorrect type for attribute 'datumNum' in SET message class CFG-DAT"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-DAT', SET, datumNum='xyz', datumName=123, majA='xcy', flat='xyx', dX='xyz', dY='xyx')

    def testFill_CFGDAT2(self):  # incorrect type (integer not string)
        EXPECTED_ERROR = "Incorrect type for attribute 'datumName' in SET message class CFG-DAT"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=123, majA='xcy', flat='xyx', dX='xyz', dY='xyx')

    def testFill_CFGDAT3(self):  # incorrect type (signed not unsigned integer)
        EXPECTED_ERROR = "Incorrect type for attribute 'datumNum' in SET message class CFG-DAT"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-DAT', SET, datumNum=-4, datumName=b'WGS84', majA=123.45, flat=123.45, dX=123.45, dY=123.45)

    def testFill_CFGDAT4(self):  # incorrect type (string not float)
        EXPECTED_ERROR = "Incorrect type for attribute 'majA' in SET message class CFG-DAT"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=b'WGS84', majA='xxx', flat=123.45, dX=123.45, dY=123.45)

    def testFill_CFGDAT5(self):  # incorrect type (binary not float)
        EXPECTED_ERROR = "Incorrect type for attribute 'flat' in SET message class CFG-DAT"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=b'WGS84', majA=123.45, flat=b'\xffffff', dX=123.45, dY=123.45)

    def testFill_XXX(self):  # test for invalid message type
        EXPECTED_ERROR = "Undefined message, class XXX, id XXX-YYY"
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage('XXX', 'XXX-YYY', POLL)

    def testParseBadHdr(self):  # test for invalid message header in bytes
        EXPECTED_ERROR = "Invalid message header (.*) - should be (.*)"
        with self.assertRaisesRegex(UBXParseError, EXPECTED_ERROR):
            UBXMessage.parse(self.bad_hdr, True)

    def testParseBadLen(self):  # test for invalid message length in bytes
        EXPECTED_ERROR = "Invalid payload length (.*) - should be (.*)"
        with self.assertRaisesRegex(UBXParseError, EXPECTED_ERROR):
            UBXMessage.parse(self.bad_len, True)

    def testFill_NONEXISTCLS(self):  # non existent message class
        EXPECTED_ERROR = "Undefined message, class XXX, id XXX-YYY"
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage('XXX', 'XXX-YYY', SET, filter=45, nmeaVersion='xx', numSV=4, flags=14)

    def testFill_NONEXISTID(self):  # non existent message id
        EXPECTED_ERROR = "Undefined message, class CFG, id CFG-XXX"
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage('CFG', 'CFG-XXX', SET, filter=45, nmeaVersion='xx', numSV=4, flags=14)

    def testFill_INVALIDATTR(self):  # test invalid attribute type with provided values
        EXPECTED_ERROR = "Unknown attribute type Z2"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('FOO', 'FOO-BAR', GET, spam=45, eggs='xx')

    def testFill_INVALIDATTR2(self):  # test invalid attribute type with defaulted values
        EXPECTED_ERROR = "Unknown attribute type Z2"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage('FOO', 'FOO-BAR', GET, eggs=45)

    def testParse_INVALIDATTR(self):  # test for invalid message header in bytes
        EXPECTED_ERROR = "Unknown attribute type Z2"
        with self.assertRaisesRegex(UBXTypeError, EXPECTED_ERROR):
            UBXMessage.parse(self.bad_msg, True)

    def testImmutability(self):  # verify object is immutable after instantiation
        EXPECTED_ERROR = "Object is immutable. Updates to msgClass not permitted after initialisation."
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            res.msgClass = 222

    def testBadCfgValSet(self):  # test for invalid cfgData keyname
        EXPECTED_ERROR = "Undefined configuration database key FOO_BAR"
        cfgData = [("FOO_BAR", 9600)]
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage.build_cfgvalset(0, 0, 0, cfgData)

    def testBadCfgKey(self):  # test for invalid key
        EXPECTED_ERROR = "Undefined configuration database key 0x11223344"
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage.cfgkey2name(0x11223344)

    def testMaxCfgValSet(self):  # test for >64 configuration tuples
        EXPECTED_ERROR = "Number of configuration tuples 65 exceeds maximum of 64"
        cfgData = []
        for i in range(65):
            cfgData.append(('CFG_TEST', i))
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage.build_cfgvalset(0, 0, 0, cfgData)

    def testMaxCfgValDel(self):  # test for >64 configuration keys
        EXPECTED_ERROR = "Number of configuration keys 68 exceeds maximum of 64"
        cfgData = []
        for _ in range(68):
            cfgData.append('CFG_TEST')
        with self.assertRaisesRegex(UBXMessageError, EXPECTED_ERROR):
            UBXMessage.build_cfgvaldel(0, 0, 0, cfgData)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
