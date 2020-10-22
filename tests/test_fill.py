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
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def testFill_CFGNMEA(self):
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=b'E', nmeaVersion=4.0, numSV=4, flags=b'\\x14')>"
        res = UBXMessage('CFG', 'CFG-NMEA', None, SET)
        res.fill(filter=b'\x45', nmeaVersion=64, numSV=4, flags=b'\x14')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEA2(self):
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=0, nmeaVersion=2.3, numSV=1, flags=0)>"
        res = UBXMessage('CFG', 'CFG-NMEA', None, SET)
        res.fill(nmeaVersion=35, numSV=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL(self):
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage('CFG', 'CFG-NMEA', None, POLL)
        res.fill()
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSC(self):  # multiple repeats in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=23, numOsc=2, reserved1=0, oscId_01=4, reserved2_01=0, flags_01=0, freq_01=22, phaseOffset_01=0, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=0, gainUncertainty_01=0, reserved4_01=0, oscId_02=7, reserved2_02=0, flags_02=0, freq_02=44, phaseOffset_02=0, withTemp_02=0, withAge_02=0, timeToTemp_02=0, reserved3_02=0, gainVco_02=0, gainUncertainty_02=0, reserved4_02=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', None, SET)
        res.fill(version=23, numOsc=2, oscId_01=4, freq_01=22, oscId_02=7, freq_02=44)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSC1(self):  # single repeat in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=1, reserved1=0, oscId_01=8, reserved2_01=0, flags_01=0, freq_01=53, phaseOffset_01=26, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=4, gainUncertainty_01=123, reserved4_01=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', None, SET)
        res.fill(version=37, numOsc=1, oscId_01=8, freq_01=53, phaseOffset_01=26, gainVco_01=4, gainUncertainty_01=123)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSC2(self):  # empty group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=0, reserved1=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', None, SET)
        res.fill(version=37, numOsc=0)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDAT(self):  # floating point attribute, single and double precision
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=4, datumName=WGS-84, majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654, dZ=0, rotX=0, rotY=0, rotZ=0, scale=0)>"
        res = UBXMessage('CFG', 'CFG-DAT', None, SET)
        res.fill(datumNum=4, datumName="WGS-84", majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654)
        self.assertEqual(str(res), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
