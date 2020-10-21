'''
Created on 21 Oct 2020

Fill method tests for pyubx2.UBXMessage

@author: semuadmin
'''
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, SET, POLL, GET


class FillTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFill_CFGNMEA(self):
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=0., numSV=0, flags=b'\\x00')>"
        res = UBXMessage('CFG', 'CFG-NMEA', None, SET)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL(self):
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage('CFG', 'CFG-NMEA', None, POLL)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNAV5(self):
        EXPECTED_RESULT = "<UBX(CFG-NAV5, mask=b'\\x00\\x00', dynModel=0, fixMode=0, fixedAlt=0, fixedAltVar=0, minElev=0, drLimit=0, pDop=0, tDop=0, pAcc=0, tAcc=0, staticHoldThresh=0, dgpsTimeOut=0, reserved2=0, reserved3=0, reserved4=0)>"
        res = UBXMessage('CFG', 'CFG-NAV5', None, SET)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNAVX5(self):
        EXPECTED_RESULT = "<UBX(CFG-NAVX5, mask1=b'\\x00\\x00', reserved0=0, reserved1=0, reserved2=0, minSVs=0, maxSVs=0, minCNO=0, reserved5=0, iniFix3D=0, reserved6=0, reserved7=0, reserved8=0, wknRollover=0, reserved9=0, reserved10=0, reserved11=0, usePPP=0, useAOP=0, reserved12=0, reserved13=0, aopOrbMaxErr=0, reserved3=0, reserved4=0)>"
        res = UBXMessage('CFG', 'CFG-NAVX5', None, SET)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_INFNOTICE(self):
        EXPECTED_RESULT = "<UBX(INF-NOTICE, message=b'NOMINAL INFO MESSAGE')>"
        res = UBXMessage('INF', 'INF-NOTICE', None, GET)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
