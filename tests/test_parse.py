'''
Created on 3 Oct 2020

Parse method tests for pyubx2.UBXMessage

@author: semuadmin
'''
# pylint: disable=line-too-long, no-member

import unittest

import pyubx2


class ParseTest(unittest.TestCase):

    def setUp(self):
        self.ack_ack = b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38'
        self.ack_ack_badck = b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37'
        self.cfg_msg = b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036'
        self.cfg_prt = b'\xb5b\x06\x00\x00\x00\x06\x18'
        self.nav_velned = b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6'
        self.nav_svinfo = b''
        self.mga_health = b'\xb5b\x13\x03\x44\x00\x04\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x01\x02\x03\x04\x05\x06\x07\x08\xef\x83'
        self.maxDiff = None

    def tearDown(self):
        pass

    def testAck(self):
        res = pyubx2.UBXMessage.parse(self.ack_ack, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testAckID(self):
        res = pyubx2.UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(res.identity, 'ACK-ACK')

    def testAckStr(self):
        res = pyubx2.UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(str(res), '<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>')

    def testAckRepr(self):
        res = pyubx2.UBXMessage.parse(self.ack_ack, True)
        self.assertEqual(repr(res), "'UBXMessage(b'\\x05', b'\\x01', b'\\x06\\x01')'")

    def testAckCkF(self):
        pyubx2.UBXMessage.parse(self.ack_ack_badck, False)

    @unittest.expectedFailure
    def testAckCkT(self):
        pyubx2.UBXMessage.parse(self.ack_ack_badck, True)

    def testCfg(self):
        res = pyubx2.UBXMessage.parse(self.ack_ack, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testCfgID(self):
        res = pyubx2.UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.identity, 'CFG-MSG')

    def testCfgStr(self):
        res = pyubx2.UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(str(res), '<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>')

    def testCfgRepr(self):
        res = pyubx2.UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(repr(res), "'UBXMessage(b'\\x06', b'\\x01', b'\\xf0\\x01\\x00\\x01\\x01\\x01\\x00\\x00')'")

    def testCfgProp1(self):
        res = pyubx2.UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.rateUART1, 1)

    def testCfgProp2(self):
        res = pyubx2.UBXMessage.parse(self.cfg_msg, True)
        self.assertEqual(res.rateSPI, 0)

    def testNavVelNed(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testNavVelNedID(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.identity, 'NAV-VELNED')

    def testNavVelNedStr(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(str(res), '<UBX(NAV-VELNED, iTOW=16:01:50, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=128387, sAcc=65, cAcc=8052720)>')

    def testNavVelNedRepr(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(repr(res), "'UBXMessage(b'\\x01', b'\\x12', b'0D\\n\\x18\\xfd\\xff\\xff\\xff\\xf1\\xff\\xff\\xff\\xfc\\xff\\xff\\xff\\x10\\x00\\x00\\x00\\x0f\\x00\\x00\\x00\\x83\\xf5\\x01\\x00A\\x00\\x00\\x00\\xf0\\xdfz\\x00')'")

    def testNavVelNedProp1(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.iTOW, 403326000)

    def testNavVelNedProp2(self):
        res = pyubx2.UBXMessage.parse(self.nav_velned, True)
        self.assertEqual(res.cAcc, 8052720)

    def testCfgPrt(self):  # POLL example with null payload
        res = pyubx2.UBXMessage.parse(self.cfg_prt, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testCfgPrtID(self):
        res = pyubx2.UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(res.identity, 'CFG-PRT')

    def testCfgPrtStr(self):
        res = pyubx2.UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(str(res), '<UBX(CFG-PRT)>')

    def testCfgPrtRepr(self):
        res = pyubx2.UBXMessage.parse(self.cfg_prt, True)
        self.assertEqual(repr(res), "'UBXMessage(b'\\x06', b'\\x00')'")

    def testMga(self):  # POLL example with null payload
        res = pyubx2.UBXMessage.parse(self.mga_health, True)
        self.assertIsInstance(res, pyubx2.UBXMessage)

    def testMgaID(self):
        res = pyubx2.UBXMessage.parse(self.mga_health, True)
        self.assertEqual(res.identity, 'MGA-BDS-HEALTH')

    def testMgaStr(self):
        res = pyubx2.UBXMessage.parse(self.mga_health, True)
        self.assertEqual(str(res), '<UBX(MGA-BDS-HEALTH, type=4, version=2, reserved1=1027, healthCode01=1541, healthCode02=2055, healthCode03=4105, healthCode04=513, healthCode05=1027, healthCode06=1541, healthCode07=2055, healthCode08=4105, healthCode09=513, healthCode10=1027, healthCode11=1541, healthCode12=2055, healthCode13=4105, healthCode14=513, healthCode15=1027, healthCode16=1541, healthCode17=2055, healthCode18=4105, healthCode19=513, healthCode20=1027, healthCode21=1541, healthCode22=2055, healthCode23=4105, healthCode24=513, healthCode25=1027, healthCode26=1541, healthCode27=2055, healthCode28=4105, healthCode29=513, healthCode30=1027, reserved2=134678021)>')

    def testMgaRepr(self):
        res = pyubx2.UBXMessage.parse(self.mga_health, True)
        self.assertEqual(repr(res), "'UBXMessage(b'\\x13', b'\\x03', b'\\x04\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08')'")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
