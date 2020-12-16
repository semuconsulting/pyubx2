'''
Created on 21 Oct 2020

Constructor method tests for pyubx2.UBXMessage

@author: semuadmin
'''
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, SET, POLL


class FillTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testFill_CFGMSG(self):  # test POLL constructor fill, format 1
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG2(self):  # test POLL constructor fill, format 2
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage(b'\x06', b'\x01', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG3(self):  # test POLL constructor fill, format 3
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>"
        res = UBXMessage(6, 1, POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGMSG4(self):  # test SET constructor fill
        EXPECTED_RESULT = "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=1, rateSPI=0, reserved=0)>"
        res = UBXMessage('CFG', 'CFG-MSG', SET, msgClass=240, msgID=1, rateUART1=1, rateUSB=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEA(self):  # test SET constructor fill, set all values
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=b'E', nmeaVersion=64, numSV=4, flags=b'\\x14', gnssToFilter=b'\\x00\\x00\\x00\\x00', svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage('CFG', 'CFG-NMEA', SET, filter=b'\x45', nmeaVersion=64, numSV=4, flags=b'\x14')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEA2(self):  # test SET constructor fill, set some values, default others
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=35, numSV=1, flags=b'\\x00', gnssToFilter=b'\\x00\\x00\\x00\\x00', svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage('CFG', 'CFG-NMEA', SET, nmeaVersion=35, numSV=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPARSE(self):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=35, numSV=1, flags=b'\\x00', gnssToFilter=b'\\x00\\x00\\x00\\x00', svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId=b'\\x00\\x00', reserved1=0)>"
        res = UBXMessage('CFG', 'CFG-NMEA', SET, nmeaVersion=35, numSV=1)
        res2 = UBXMessage.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL(self):  # test POLL constructor, no payload
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage('CFG', 'CFG-NMEA', POLL)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGNMEAPOLL2(self):  # test POLL constructor, no payload
        EXPECTED_RESULT = "<UBX(CFG-NMEA)>"
        res = UBXMessage('CFG', 'CFG-NMEA', POLL)
        res2 = UBXMessage.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDOSC(self):  # multiple repeats in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=23, numOsc=2, reserved1=0, oscId_01=4, reserved2_01=0, flags_01=b'\\x00\\x00', freq_01=22, phaseOffset_01=0, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=0, gainUncertainty_01=0, reserved4_01=0, oscId_02=7, reserved2_02=0, flags_02=b'\\x00\\x00', freq_02=44, phaseOffset_02=0, withTemp_02=0, withAge_02=0, timeToTemp_02=0, reserved3_02=0, gainVco_02=0, gainUncertainty_02=0, reserved4_02=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', SET, version=23, numOsc=2, oscId_01=4, freq_01=22, oscId_02=7, freq_02=44)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSC1(self):  # single repeat in group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=1, reserved1=0, oscId_01=8, reserved2_01=0, flags_01=b'\\x00\\x00', freq_01=53, phaseOffset_01=26, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=4, gainUncertainty_01=123, reserved4_01=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', SET, version=37, numOsc=1, oscId_01=8, freq_01=53, phaseOffset_01=26, gainVco_01=4, gainUncertainty_01=123)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDOSCPARSE(self):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=1, reserved1=0, oscId_01=8, reserved2_01=0, flags_01=b'\\x00\\x00', freq_01=53, phaseOffset_01=26, withTemp_01=0, withAge_01=0, timeToTemp_01=0, reserved3_01=0, gainVco_01=4, gainUncertainty_01=123, reserved4_01=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', SET, version=37, numOsc=1, oscId_01=8, freq_01=53, phaseOffset_01=26, gainVco_01=4, gainUncertainty_01=123)
        res2 = UBXMessage.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDOSC2(self):  # empty group
        EXPECTED_RESULT = "<UBX(CFG-DOSC, version=37, numOsc=0, reserved1=0)>"
        res = UBXMessage('CFG', 'CFG-DOSC', SET, version=37, numOsc=0)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDAT(self):  # floating point attribute, single and double precision
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=4, datumName=b'WGS-84', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654, dZ=0, rotX=0, rotY=0, rotZ=0, scale=0)>"
        res = UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=b'WGS-84', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGDATPARSE(self):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=4, datumName=b'WGS-84', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345677614212036, dY=27.406539916992188, dZ=0.0, rotX=0.0, rotY=0.0, rotZ=0.0, scale=0.0)>"
        res = UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=b'WGS-84', majA=4321.123456789128, flat=-2964.00469836, dX=-1.2345678, dY=27.40654)
        res2 = UBXMessage.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_CFGDATPARSE2(self):  # check that raw payload is correctly populated and parses back to original message
        EXPECTED_RESULT = "<UBX(CFG-DAT, datumNum=4, datumName=b'WGS-84', majA=0.0, flat=0.0, dX=-1.2345677614212036, dY=27.406539916992188, dZ=0.0, rotX=0.0, rotY=0.0, rotZ=0.0, scale=0.0)>"
        res = UBXMessage('CFG', 'CFG-DAT', SET, datumNum=4, datumName=b'WGS-84', dX=-1.2345678, dY=27.40654)
        res2 = UBXMessage.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testEVAL(self):  # test eval of repr
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        reseval = eval(repr(res))
        assert type(reseval) is UBXMessage

    def testEVAL2(self):  # test eval of repr
        res = UBXMessage('CFG', 'CFG-MSG', SET, msgClass=240, msgID=5, rateUART1=1, rateUSB=1)
        reseval = eval(repr(res))
        assert type(reseval) is UBXMessage

    def testFill_CFGVALGET(self):  #  test CFG-VALGET POLL constructor
        EXPECTED_RESULT = "<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=1079115777, keys_02=1079181313)>"
        res = UBXMessage('CFG', 'CFG-VALGET', POLL, payload=b'\x00\x01\x00\x00\x01\x00\x52\x40\x01\x00\x53\x40')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGVALDEL(self):  #  test CFG-VALDEL SET constructor
        EXPECTED_RESULT = "<UBX(CFG-VALDEL, version=0, layers=b'\\x03', transaction=b'\\x00', reserved0=0, keys_01=1079115777, keys_02=16798528)>"
        res = UBXMessage('CFG', 'CFG-VALDEL', SET, payload=b'\x00\x03\x00\x00\x01\x00\x52\x40\x40\x53\x00\x01')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_CFGVALSET(self):  #  test CFG-VALSET SET constructor
        EXPECTED_RESULT = "<UBX(CFG-VALSET, version=0, layers=b'\\x03', transaction=0, reserved0=0, cfgData_01=1, cfgData_02=0, cfgData_03=82, cfgData_04=64, cfgData_05=128, cfgData_06=37, cfgData_07=0, cfgData_08=0)>"
        res = UBXMessage('CFG', 'CFG-VALSET', SET, payload=b'\x00\x03\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMREQSET(self):  #  test RXM-PMREQ SET constructor long version with payload keyword
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, version=0, reserved0=0, duration=67305985, flags=b'\\x01\\x02\\x03\\x04', wakeupSources=b'\\x01\\x02\\x03\\x04')>"
        res = UBXMessage('RXM', 'RXM-PMREQ', SET, payload=b'\x00\x00\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMREQSET2(self):  #  test RXM-PMREQ SET constructor long version with version keyword
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, version=0, reserved0=0, duration=67305985, flags=b'\\x01\\x02\\x03\\x04', wakeupSources=b'\\x01\\x02\\x03\\x04')>"
        res = UBXMessage('RXM', 'RXM-PMREQ', SET, version=0, duration=67305985, flags=b'\x01\x02\x03\x04', wakeupSources=b'\x01\x02\x03\x04')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_RXMPMREQSET3(self):  #  test RXM-PMREQ SET constructor short version
        EXPECTED_RESULT = "<UBX(RXM-PMREQ, duration=67305985, flags=b'\\x01\\x02\\x03\\x04')>"
        res = UBXMessage('RXM', 'RXM-PMREQ', SET, payload=b'\x01\x02\x03\x04\x01\x02\x03\x04')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_MGABDSSET(self):  #  test MGA-BDS-UTC SET constructor using attribute keywords
        EXPECTED_RESULT = "<UBX(MGA-BDS-UTC, type=5, version=0, reserved1=0, a0UTC=15, a1UTC=0, dtLS=0, reserved2=0, wnRec=23, wnLSF=41, dN=0, dtLSF=0, reserved3=0)>"
        res = UBXMessage(b'\x13', b'\x03', SET, type=5, a0UTC=15, wnRec=23, wnLSF=41)
        self.assertEqual(str(res), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
