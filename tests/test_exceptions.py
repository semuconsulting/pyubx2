'''
Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

Exception handling tests for UBXMessage constructor and parse

@author: semuadmin
'''

import unittest

from pyubx2 import UBXMessage, UBXTypeError, UBXParseError, UBXMessageError, SET, POLL, GET


class ExceptionTest(unittest.TestCase):

    def setUp(self):
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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
