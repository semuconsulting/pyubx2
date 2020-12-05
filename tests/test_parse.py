'''
Created on 3 Oct 2020

Parse method tests for pyubx2.UBXMessage

@author: semuadmin
'''
# pylint: disable=line-too-long, no-member

import unittest

from pyubx2 import UBXMessage


class ParseTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.ack_ack = b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38'
        self.ack_ack_badck = b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37'
        self.cfg_msg = b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036'
        self.cfg_prt = b'\xb5b\x06\x00\x00\x00\x06\x18'
        self.nav_velned = b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6'
        self.nav_svinfo = b''
        self.cfg_nmeavx = b'\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9'
        self.cfg_nmeav0 = b'\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61'
        self.mga_dbd = b'\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2'
        self.mga_flash_ack = b'\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a'
        self.cfg_valget = b'\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0'
        self.cfg_valget2 = b'\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2'
        self.cfg_valget3 = b'\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92'
        self.cfg_valget4 = b'\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d'
        self.esf_meas = b'\xb5b\x10\x02\x10\x00\x01\x02\x03\x04\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x50\x8a'
        self.esf_measct = b'\xb5b\x10\x02\x14\x00\x01\x02\x03\x04\x00\x08\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x66\xae'

    def tearDown(self):
        pass

    def testAck(self):
        res = UBXMessage.parse(self.ack_ack, True)
        self.assertIsInstance(res, UBXMessage)

    def testAckID(self):
        res = UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(res.identity, 'ACK-ACK')

    def testAckStr(self):
        res = UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(str(res), '<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>')

    def testAckRepr(self):
        res = UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(repr(res), "UBXMessage(b'\\x05', b'\\x01', 0, payload=b'\\x06\\x01')")

    def testAckCkF(self):
        UBXMessage.parse(self.ack_ack_badck, False)

    def testCfg(self):
        res = UBXMessage.parse(self.ack_ack, True)
        self.assertIsInstance(res, UBXMessage)

    def testCfgID(self):
        res = UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.identity, 'CFG-MSG')

    def testCfgStr(self):
        res = UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(str(res), '<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>')

    def testCfgRepr(self):
        res = UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(repr(res), "UBXMessage(b'\\x06', b'\\x01', 0, payload=b'\\xf0\\x01\\x00\\x01\\x01\\x01\\x00\\x00')")

    def testCfgProp1(self):
        res = UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.rateUART1, 1)

    def testCfgProp2(self):
        res = UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.rateSPI, 0)

    def testNavVelNed(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertIsInstance(res, UBXMessage)

    def testNavVelNedID(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.identity, 'NAV-VELNED')

    def testNavVelNedStr(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(str(res), '<UBX(NAV-VELNED, iTOW=16:01:50, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=128387, sAcc=65, cAcc=8052720)>')

    def testNavVelNedRepr(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(repr(res), "UBXMessage(b'\\x01', b'\\x12', 0, payload=b'0D\\n\\x18\\xfd\\xff\\xff\\xff\\xf1\\xff\\xff\\xff\\xfc\\xff\\xff\\xff\\x10\\x00\\x00\\x00\\x0f\\x00\\x00\\x00\\x83\\xf5\\x01\\x00A\\x00\\x00\\x00\\xf0\\xdfz\\x00')")

    def testNavVelNedProp1(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.iTOW, 403326000)

    def testNavVelNedProp2(self):
        res = UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.cAcc, 8052720)

    def testCfgPrt(self):  # POLL example with null payload
        res = UBXMessage.parse(self.cfg_prt, True)
        self.assertIsInstance(res, UBXMessage)

    def testCfgPrtID(self):
        res = UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(res.identity, 'CFG-PRT')

    def testCfgPrtStr(self):
        res = UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(str(res), '<UBX(CFG-PRT)>')

    def testCfgPrtRepr(self):
        res = UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(repr(res), "UBXMessage(b'\\x06', b'\\x00', 0)")

    def testCfgNmeaVx(self):  # test older NMEA message parse
        res = UBXMessage.parse(self.cfg_nmeavx, True)
        self.assertEqual(str(res), "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=0., numSV=0, flags=b'\\x00')>")

    def testCfgNmeaV0(self):  # test older NMEA message parse
        res = UBXMessage.parse(self.cfg_nmeav0, True)
        self.assertEqual(str(res), "<UBX(CFG-NMEA, filter=b'\\x00', nmeaVersion=0., numSV=0, flags=b'\\x00', gnssToFilter=b'\\x00\\x00\\x00\\x00', svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0)>")

    def testMgaDbd(self):
        res = UBXMessage.parse(self.mga_dbd, True)
        self.assertEqual(str(res), "<UBX(MGA-DBD, reserved1=3727165692135864801209549313, data_01=1, data_02=2)>")

    def testMgaFlashAck(self):
        res = UBXMessage.parse(self.mga_flash_ack, True)
        self.assertEqual(str(res), "<UBX(MGA-FLASH-ACK, type=3, version=1, ack=2, reserved1=0, sequence=1024)>")

    def testCFGVALGET(self):  # test parser of CFG-VALGET CFG-UART1-BAUDRATE
        res = UBXMessage.parse(self.cfg_valget, True)
        self.assertEqual(str(res), "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_UART1_BAUDRATE=9600)>")

    def testCFGVALGET2(self):  # test parse of CFG-VALGET CFG-I2C-ADDRESS
        res = UBXMessage.parse(self.cfg_valget2, True)
        self.assertEqual(str(res), "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85)>")

    def testCFGVALGET3(self):  # test parse of CFG-VALGET CFG-I2C-ADDRESS, CFG-UART1-BAUDRATE, CFG-RATE-NAV
        res = UBXMessage.parse(self.cfg_valget3, True)
        self.assertEqual(str(res), "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85, CFG_UART1_BAUDRATE=9600, CFG_RATE_NAV=35)>")

    def testCFGVALGET4(self):  # test parser of CFG-VALGET CFG-NAVSPG-USRDAT_ROTY
        res = UBXMessage.parse(self.cfg_valget4, True)
        self.assertAlmostEqual(res.CFG_NAVSPG_USRDAT_ROTY, 1.23, 2)

    def testESFMEAS(self):  # test parser of ESF-MEAS without calibTtag data
        res = UBXMessage.parse(self.esf_meas, True)
        self.assertEqual(str(res), "<UBX(ESF-MEAS, timeTag=67305985, flags=b'\\x00\\x00', id=0, data_01=b'\\x01\\x02\\x03\\x04', data_02=b'\\x05\\x06\\x07\\x08')>")

    def testESFMEASCT(self):  # test parser of ESF-MEAS with calibTtag data
        res = UBXMessage.parse(self.esf_measct, True)
        self.assertEqual(str(res), "<UBX(ESF-MEAS, timeTag=67305985, flags=b'\\x00\\x08', id=0, data_01=b'\\x01\\x02\\x03\\x04', data_02=b'\\x05\\x06\\x07\\x08', calibTtag=67305985)>")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
