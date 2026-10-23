"""
Parse method tests for pyubx2.UBXMessage

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, VALCKSUM, VALNONE, SET, SETPOLL


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ack_ack = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38"
        self.ack_ack_badck = b"\xb5b\x05\x01\x02\x00\x06\x01\x0f\x37"
        self.cfg_msg = b"\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036"
        self.cfg_prt = b"\xb5b\x06\x00\x00\x00\x06\x18"
        self.nav_pl = b"\xb5b\x01\x62\x34\x00\x01\x05\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x48\x04\xA9\x14\x6D\x00\x00\x00\x6D\x00\x00\x00\x6D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEF\x88"
        self.nav_velned = b"\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6"
        self.nav_svinfo = b""
        self.cfg_nmeavx = b"\xb5b\x06\x17\x04\x00\x00\x00\x00\x00\x21\xe9"
        self.cfg_nmeav0 = b"\xb5b\x06\x17\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x29\x61"
        self.mga_dbd = b"\xb5b\x13\x80\x0e\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x01\x02\xf2\xc2"
        self.mga_flash_ack = b"\xb5b\x13\x21\x06\x00\x03\x01\x02\x00\x00\x04\x44\x3a"
        self.cfg_valget = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x01\x00\x52\x40\x80\x25\x00\x00\xd5\xd0"
        self.cfg_valget2 = (
            b"\xb5b\x06\x8b\x09\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x61\xc2"
        )
        self.cfg_valget3 = b"\xb5b\x06\x8b\x16\x00\x00\x00\x00\x00\x01\x00\x51\x20\x55\x01\x00\x52\x40\x80\x25\x00\x00\x02\x00\x21\x30\x23\x1c\x92"
        self.cfg_valget4 = b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d"
        self.esf_meas = b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51"
        self.esf_meas2 = b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c"
        self.mga_ini1 = b"\xb5b\x13\x40\x14\x00\x01\x00\x01\x02\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x93\xc8"
        self.mon_span = b"\xb5b\n1\x14\x01\x00\x01\x00\x00-+-,+-.,-.+,+.-..-,..//./00203017?9398:L]<@C;H<>=A@BDCGJNQRVY[_cgpqyz\x7f\x84\x8c\x90\x99\xa0\xa7\xae\xb0\xae\xaa\xa7\xa2\x9b\x97\x96\x94\x91\x90\x8e\x8c\x8c\x8c\x8b\x8b\x89\x88\x89\x89\x89\x8b\x88\x89\x8a\x89\x8a\x8a\x89\x8a\x8b\x8a\x8a\x8b\x8b\x8c\x8a\x8a\x8a\x8b\x88\x88\x87\x87\x86\x85\x85\x85\x84\x89\x84\x85\x83\x84\x84\x84\x85\x88\x87\x87\x88\x8a\x8a\x8a\x8a\x8b\x8e\x8c\x8d\x8d\x8f\x8e\x8d\x8f\x8e\x8f\x8f\x8e\x8f\x8f\x90\x91\x92\x93\x93\x93\x95\x94\x94\x94\x94\x95\x94\x95\x93\x93\x91\x92\x93\x92\x94\x95\x94\x95\x97\x97\x98\x97\x94\x90\x8d\x86\x82\x7fyupmg`]VRLEB?=;99665422202101///-//.-0-.-/..--,.-+-,--+.,,--,,-*\x00 \xa1\x07 \xa1\x07\x00@\xc4`^\x0c\x00\x00\x00\x15j"
        self.tim_tp = b"\xb5b\r\x01\x10\x00\x88gh\x16\x00\x00\x00\x00\x00\x00\x00\x00\x85\x08\x1b\x0fB\xff"
        self.esf_status = b"\xb5b\x10\x10.\x00\x00\x00\x00\x00\x02$\x02\x00\x00\x00\x00\x00\x00\x00\x00\x06\x85\x04\x00\x00\r\x04\n\x00\x8e\x04\n\x00\x00\x04\n\x00\x01\x00\n\x00\x92\x04\x00\x00\x00\x00\x00\x00\x00\x00k4"

    def tearDown(self):
        pass

    def testAck(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testAckID(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(res.identity, "ACK-ACK")

    def testAckStr(self):
        res = UBXReader.parse(self.ack_ack, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>")

    def testAckRepr(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertEqual(
            repr(res), "UBXMessage(b'\\x05', b'\\x01', 0, payload=b'\\x06\\x01')"
        )

    def testAckCkF(self):
        UBXReader.parse(self.ack_ack_badck, validate=VALNONE)

    def testCfg(self):
        res = UBXReader.parse(self.ack_ack)
        self.assertIsInstance(res, UBXMessage)

    def testCfgID(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.identity, "CFG-MSG")

    def testCfgStr(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(
            str(res),
            "<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>",
        )

    def testCfgRepr(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x06', b'\\x01', 0, payload=b'\\xf0\\x01\\x00\\x01\\x01\\x01\\x00\\x00')",
        )

    def testCfgProp1(self):
        res = UBXReader.parse(self.cfg_msg, validate=VALCKSUM)
        self.assertEqual(res.rateUART1, 1)

    def testCfgProp2(self):
        res = UBXReader.parse(self.cfg_msg)
        self.assertEqual(res.rateSPI, 0)

    def testNavPL(self):
        res = UBXReader.parse(self.nav_pl, validate=VALCKSUM)
        self.assertEqual(res.plPos2, 109)

    def testNavVelNed(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertIsInstance(res, UBXMessage)

    def testNavVelNedID(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.identity, "NAV-VELNED")

    def testNavVelNedStr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            str(res),
            "<UBX(NAV-VELNED, iTOW=16:01:48, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=1.28387, sAcc=65, cAcc=80.5272)>",
        )

    def testNavVelNedRepr(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(
            repr(res),
            "UBXMessage(b'\\x01', b'\\x12', 0, payload=b'0D\\n\\x18\\xfd\\xff\\xff\\xff\\xf1\\xff\\xff\\xff\\xfc\\xff\\xff\\xff\\x10\\x00\\x00\\x00\\x0f\\x00\\x00\\x00\\x83\\xf5\\x01\\x00A\\x00\\x00\\x00\\xf0\\xdfz\\x00')",
        )

    def testNavVelNedProp1(self):
        res = UBXReader.parse(self.nav_velned, validate=VALCKSUM)
        self.assertEqual(res.iTOW, 403326000)

    def testNavVelNedProp2(self):
        res = UBXReader.parse(self.nav_velned)
        self.assertEqual(res.cAcc, 80.5272)

    def testCfgPrt(self):  # POLL example with null payload
        res = UBXReader.parse(self.cfg_prt)
        self.assertIsInstance(res, UBXMessage)

    def testCfgPrtID(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(res.identity, "CFG-PRT")

    def testCfgPrtStr(self):
        res = UBXReader.parse(self.cfg_prt, validate=VALCKSUM)
        self.assertEqual(str(res), "<UBX(CFG-PRT)>")

    def testCfgPrtRepr(self):
        res = UBXReader.parse(self.cfg_prt)
        self.assertEqual(repr(res), "UBXMessage(b'\\x06', b'\\x00', 0)")

    def testCfgNmeaVx(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeavx)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=0, numSV=0, compat=0, consider=0, limit82=0, highPrec=0)>",
        )

    def testCfgNmeaV0(self):  # test older NMEA message parse
        res = UBXReader.parse(self.cfg_nmeav0)
        self.assertEqual(
            str(res),
            "<UBX(CFG-NMEA, posFilt=0, mskPosFilt=0, timeFilt=0, dateFilt=0, gpsOnlyFilter=0, trackFilt=0, nmeaVersion=0, numSV=0, compat=0, consider=0, limit82=0, highPrec=0, gps=0, sbas=0, galileo=0, qzss=0, glonass=0, bBeidou=0, svNumbering=0, mainTalkerId=0, gsvTalkerId=0, version=0)>",
        )

    def testMgaDbd(self):
        res = UBXReader.parse(self.mga_dbd)
        self.assertEqual(
            str(res),
            "<UBX(MGA-DBD, reserved1=3727165692135864801209549313, data_01=1, data_02=2)>",
        )

    def testMgaFlashAck(self):
        res = UBXReader.parse(self.mga_flash_ack)
        self.assertEqual(
            str(res),
            "<UBX(MGA-FLASH-ACK, type=3, version=1, ack=2, reserved1=0, sequence=1024)>",
        )

    def testCFGVALGET(self):  # test parser of CFG-VALGET CFG-UART1-BAUDRATE
        res = UBXReader.parse(self.cfg_valget)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_UART1_BAUDRATE=9600)>",
        )

    def testCFGVALGET2(self):  # test parse of CFG-VALGET CFG-I2C-ADDRESS
        res = UBXReader.parse(self.cfg_valget2)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85)>",
        )

    def testCFGVALGET3(
        self,
    ):  # test parse of CFG-VALGET CFG-I2C-ADDRESS, CFG-UART1-BAUDRATE, CFG-RATE-NAV
        res = UBXReader.parse(self.cfg_valget3)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_I2C_ADDRESS=85, CFG_UART1_BAUDRATE=9600, CFG_RATE_NAV=35)>",
        )

    def testCFGVALGET4(self):  # test parser of CFG-VALGET CFG-NAVSPG-USRDAT_ROTY
        res = UBXReader.parse(self.cfg_valget4)
        self.assertAlmostEqual(res.CFG_NAVSPG_USRDAT_ROTY, 1.23, 2)

    def testRXMPMPV0(self):  # test parser of RXM-PMP v0 message
        EXPECTED_RESULT = "<UBX(RXM-PMP, version=0, reserved0=131328, timeTag=33620995, uniqueWord1=33620995, uniqueWord2=33620995, serviceIdentifier=257, spare=0, uniqueWordBitErrors=1, userData=444016576645496696326520967760864414445036530859298786968652454358784692998584832505203835643079882501372094872184008296993704490358249858485479536059990045404322800089603135801782758877491279366249916806135464816187023567604380587287967435515547406675502999914340502206559644252054902614741037493679297834111577017534920153473213525154848211261456751562783303561731419372567316462136507687208239507093416810033003472188364405676607421668823982836214027720745896822989244592540587625547470908433894150213986926953033425405758152051030331834955237367010599011377455090768608063573597336485245670428335984577988287379510075349296298486311442762344455622472331718247507404459805060416700489932334005405002078350234982280474340036367693917645971007712118945121363842445446966924018697350702649493459513217058961606100390487433714382978260350073014949085195059543186225770460804270575108656937717870826510833602125417733896578628099385993250170527046613747278686375415707408420612602163111473345048943554010330878898193280929498383830165656806717725405598029015341089695214580211641242019951845653554090769500271918059054596956882402837903965523563645115810219637129213812338206683994264160821249472117217936158229250, fecBits=1, ebno=0.0, reserved1=0)>"
        rxm_pmpv0 = b"\xb5b\x02\x72\x0e\x02\x00\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x01\x01"
        for i in range(504):
            n = i % 256
            rxm_pmpv0 += n.to_bytes(1, "little", signed=False)
        rxm_pmpv0 += b"\x01\x02\x01\x00\xcf\xa9"
        res = UBXReader.parse(rxm_pmpv0, validate=VALCKSUM, msgmode=SET)
        #print(f'"{res}"')
        self.assertEqual(str(res),EXPECTED_RESULT)

    def testRXMPMPV1(self):  # test parser of RXM-PMP v1 message
        EXPECTED_RESULT = "<UBX(RXM-PMP, version=1, reserved0=0, numBytesUserData=11, timeTag=67305985, uniqueWord1=67305985, uniqueWord2=67305985, serviceIdentifier=513, spare=0, uniqueWordBitErrors=1, fecBits=513, ebno=0.125, reserved1=0, userData=12131907574542231144628480)>"
        rxm_pmpv1 = b"\xb5b\x02\x72\x23\x00\x01\x00\x0b\x00\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x00\x01\x01\x02\x01\x00"
        for i in range(11):
            rxm_pmpv1 += i.to_bytes(1, "little", signed=False)
        rxm_pmpv1 += b"\x00\x20"
        res = UBXReader.parse(rxm_pmpv1, msgmode=SET)
        # print(f'"{res}"')
        self.assertEqual(str(res),EXPECTED_RESULT)

    def testRXMRLMS(self):  # test parser of RXM-RLM-S message
        rxm_rlms = b"\xb5b\x02\x59\x10\x00\x00\x01\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\x00\x8b\xbd"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=1, svId=0, reserved0=0, beacon=506097522914230528, message=0, params=513, reserved1=0)>",
        )

    def testRXMRLML(self):  # test parser of RXM-RLM-L message
        rxm_rlms = b"\xb5b\x02\x59\x1c\x00\x00\x02\x00\x00"
        for i in range(8):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00"
        for i in range(12):
            rxm_rlms += i.to_bytes(1, "little", signed=False)
        rxm_rlms += b"\x00\x01\x02\xda\x81"
        res = UBXReader.parse(rxm_rlms)
        self.assertEqual(
            str(res),
            "<UBX(RXM-RLM, version=0, type=2, svId=0, reserved0=0, beacon=506097522914230528, message=0, params=3416467015609337987117220096, reserved1=131328)>",
        )

    def testMONSPAN2(self):  # test parser of MON-SPAN message (repeating groups empty)
        mon_span = b"\xb5b\x0a\x31\x04\x00\x00\x00\x01\x02"
        mon_span += b"\x42\xc3"
        res = UBXReader.parse(mon_span)
        self.assertEqual(
            str(res), "<UBX(MON-SPAN, version=0, numRfBlocks=0, msgSource=1, reserved0=2)>"
        )

    def testMGAINI1(self):  # test parser of MGA-INI input message with kwargs
        res = UBXReader.parse(self.mga_ini1, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>",
        )

    def testMGAINI2(self):  # test parser of MGA-INI input message with args
        res = UBXReader.parse(self.mga_ini1, validate=VALCKSUM, msgmode=SET)
        self.assertEqual(
            str(res),
            "<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>",
        )

    def testSETPOLL(self):  # test auto detection of SET or POLL mode
        msg = UBXMessage.config_poll(0,0,["CFG_UART1_BAUDRATE", 0x40530001]).serialize()
        res = UBXReader.parse(msg, msgmode=SETPOLL)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, keys_01=1079115777, keys_02=1079181313)>",
        )
        msg = UBXMessage.config_set(0,0,[("CFG_UART1_BAUDRATE", 9600), (0x40530001, 38400)]).serialize()
        res = UBXReader.parse(msg, msgmode=SETPOLL)
        self.assertEqual(
            str(res),
            "<UBX(CFG-VALSET, version=0, ram=0, bbr=0, flash=0, action=0, reserved0=0, CFG_UART1_BAUDRATE=9600, CFG_UART2_BAUDRATE=38400)>",
        )

    def testESFSTATUS(self):  # test parser of ESF-STATUS message
        res = UBXReader.parse(self.esf_status)
        # print(res)
        self.assertEqual(
            str(res),
            #"<UBX(ESF-STATUS, iTOW=23:59:42, version=2, reserved0=548, fusionMode=0, reserved1=0, numSens=6, type_01=5, used_01=0, ready_01=1, calibStatus_01=0, timeStatus_01=1, freq_01=0, badMeas_01=0, badTTag_01=0, missingMeas_01=0, noisyMeas_01=0, type_02=13, used_02=0, ready_02=0, calibStatus_02=0, timeStatus_02=1, freq_02=10, badMeas_02=0, badTTag_02=0, missingMeas_02=0, noisyMeas_02=0, type_03=14, used_03=0, ready_03=1, calibStatus_03=0, timeStatus_03=1, freq_03=10, badMeas_03=0, badTTag_03=0, missingMeas_03=0, noisyMeas_03=0, type_04=0, used_04=0, ready_04=0, calibStatus_04=0, timeStatus_04=1, freq_04=10, badMeas_04=0, badTTag_04=0, missingMeas_04=0, noisyMeas_04=0, type_05=1, used_05=0, ready_05=0, calibStatus_05=0, timeStatus_05=0, freq_05=10, badMeas_05=0, badTTag_05=0, missingMeas_05=0, noisyMeas_05=0, type_06=18, used_06=0, ready_06=1, calibStatus_06=0, timeStatus_06=1, freq_06=0, badMeas_06=0, badTTag_06=0, missingMeas_06=0, noisyMeas_06=0)>",
            "<UBX(ESF-STATUS, iTOW=23:59:42, version=2, wtInitStatus=0, mntAlgStatus=1, insInitStatus=1, imuInitStatus=2, reserved0=0, fusionMode=0, reserved1=0, numSens=6, type_01=5, used_01=0, ready_01=1, calibStatus_01=0, timeStatus_01=1, freq_01=0, badMeas_01=0, badTTag_01=0, missingMeas_01=0, noisyMeas_01=0, type_02=13, used_02=0, ready_02=0, calibStatus_02=0, timeStatus_02=1, freq_02=10, badMeas_02=0, badTTag_02=0, missingMeas_02=0, noisyMeas_02=0, type_03=14, used_03=0, ready_03=1, calibStatus_03=0, timeStatus_03=1, freq_03=10, badMeas_03=0, badTTag_03=0, missingMeas_03=0, noisyMeas_03=0, type_04=0, used_04=0, ready_04=0, calibStatus_04=0, timeStatus_04=1, freq_04=10, badMeas_04=0, badTTag_04=0, missingMeas_04=0, noisyMeas_04=0, type_05=1, used_05=0, ready_05=0, calibStatus_05=0, timeStatus_05=0, freq_05=10, badMeas_05=0, badTTag_05=0, missingMeas_05=0, noisyMeas_05=0, type_06=18, used_06=0, ready_06=1, calibStatus_06=0, timeStatus_06=1, freq_06=0, badMeas_06=0, badTTag_06=0, missingMeas_06=0, noisyMeas_06=0)>",
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
