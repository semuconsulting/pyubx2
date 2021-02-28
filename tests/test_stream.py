'''
Stream method tests for pyubx2.UBXReader

Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
'''
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyubx2 import UBXReader
from pyubx2.exceptions import UBXStreamError


class StreamTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.streamINF = open(os.path.join(dirname, 'pygpsdata-INF.log'), 'rb')
        self.streamMON = open(os.path.join(dirname, 'pygpsdata-MON.log'), 'rb')
        self.streamRXM = open(os.path.join(dirname, 'pygpsdata-RXM.log'), 'rb')
        self.streamMIX = open(os.path.join(dirname, 'pygpsdata-MIXED.log'), 'rb')
        self.streamMIX2 = open(os.path.join(dirname, 'pygpsdata-MIXED2.log'), 'rb')
        self.streamBADHDR = open(os.path.join(dirname, 'pygpsdata-BADHDR.log'), 'rb')
        self.streamBADEOF1 = open(os.path.join(dirname, 'pygpsdata-BADEOF1.log'), 'rb')
        self.streamBADEOF2 = open(os.path.join(dirname, 'pygpsdata-BADEOF2.log'), 'rb')
        self.streamBADEOF3 = open(os.path.join(dirname, 'pygpsdata-BADEOF3.log'), 'rb')

    def tearDown(self):
        self.streamINF.close()
        self.streamMON.close()
        self.streamRXM.close()
        self.streamMIX.close()
        self.streamMIX2.close()
        self.streamBADHDR.close()
        self.streamBADEOF1.close()
        self.streamBADEOF2.close()
        self.streamBADEOF3.close()

    def testMIX2(self):  # test mixed UBX/NMEA stream with validate set to False
        EXPECTED_RESULTS = (
            "<UBX(NAV-EOE, iTOW=09:08:04)>",
            "<UBX(NAV-PVT, iTOW=09:08:09, year=2021, month=2, day=22, hour=9, min=8, second=7, valid=b'\\xf7', tAcc=1071, nano=332985, fixType=3, flags=b'\\x01', flags2=b'\\xa6', numSV=4, lon=-22401762, lat=534506799, height=72728, hMSL=24245, hAcc=55374, vAcc=35349, velN=362, velE=-50, velD=-71, gSpeed=365, headMot=0, sAcc=4508, headAcc=13597116, pDOP=520, reserved1=52016683286528, headVeh=0, magDec=0, magAcc=0)>",
            "<UBX(NAV-ORB, iTOW=09:08:09, version=1, numSv=33, reserved1=0, gnssId_01=GPS, svId_01=1, svFlag_01=b'\\x05', eph_01=b'\\x00', alm_01=b'1', otherOrb_01=b'\\x00', gnssId_02=GPS, svId_02=14, svFlag_02=b'\\r', eph_02=b',', alm_02=b'o', otherOrb_02=b'G', gnssId_03=GPS, svId_03=19, svFlag_03=b'\\x05', eph_03=b'\\x00', alm_03=b'0', otherOrb_03=b'\\x00', gnssId_04=GPS, svId_04=20, svFlag_04=b'\\r', eph_04=b'\\x00', alm_04=b'1', otherOrb_04=b'\\x00', gnssId_05=GPS, svId_05=21, svFlag_05=b'\\x05', eph_05=b'\\x00', alm_05=b'1', otherOrb_05=b'\\x00', gnssId_06=GPS, svId_06=22, svFlag_06=b'\\x05', eph_06=b'\\x00', alm_06=b'1', otherOrb_06=b'\\x00', gnssId_07=GPS, svId_07=23, svFlag_07=b'\\r', eph_07=b'\\x00', alm_07=b'1', otherOrb_07=b'\\x00', gnssId_08=GPS, svId_08=24, svFlag_08=b'\\r', eph_08=b',', alm_08=b'o', otherOrb_08=b'G', gnssId_09=GPS, svId_09=25, svFlag_09=b'\\x01', eph_09=b'\\x00', alm_09=b'1', otherOrb_09=b'\\x00', gnssId_10=GLONASS, svId_10=1, svFlag_10=b'\\x05', eph_10=b'\\x00', alm_10=b'5', otherOrb_10=b'\\x00', gnssId_11=GLONASS, svId_11=2, svFlag_11=b'\\x05', eph_11=b'\\x00', alm_11=b'5', otherOrb_11=b'\\x00', gnssId_12=GLONASS, svId_12=3, svFlag_12=b'\\x05', eph_12=b'\\x00', alm_12=b'5', otherOrb_12=b'\\x00', gnssId_13=GLONASS, svId_13=4, svFlag_13=b'\\r', eph_13=b'\\x00', alm_13=b'5', otherOrb_13=b'\\x00', gnssId_14=GLONASS, svId_14=5, svFlag_14=b'\\r', eph_14=b'&', alm_14=b'5', otherOrb_14=b'G', gnssId_15=GLONASS, svId_15=6, svFlag_15=b'\\r', eph_15=b'\\x00', alm_15=b'5', otherOrb_15=b'\\x00', gnssId_16=GLONASS, svId_16=7, svFlag_16=b'\\x05', eph_16=b'\\x00', alm_16=b'5', otherOrb_16=b'\\x00', gnssId_17=GLONASS, svId_17=8, svFlag_17=b'\\x05', eph_17=b'\\x00', alm_17=b'5', otherOrb_17=b'\\x00', gnssId_18=GLONASS, svId_18=9, svFlag_18=b'\\x05', eph_18=b'\\x00', alm_18=b'5', otherOrb_18=b'\\x00', gnssId_19=GLONASS, svId_19=10, svFlag_19=b'\\x05', eph_19=b'\\x00', alm_19=b'5', otherOrb_19=b'\\x00', gnssId_20=GLONASS, svId_20=11, svFlag_20=b'\\x06', eph_20=b'\\x00', alm_20=b'5', otherOrb_20=b'\\x00', gnssId_21=GLONASS, svId_21=12, svFlag_21=b'\\x05', eph_21=b'\\x00', alm_21=b'5', otherOrb_21=b'\\x00', gnssId_22=GLONASS, svId_22=13, svFlag_22=b'\\t', eph_22=b'\\x00', alm_22=b'5', otherOrb_22=b'\\x00', gnssId_23=GLONASS, svId_23=14, svFlag_23=b'\\r', eph_23=b'\\x00', alm_23=b'5', otherOrb_23=b'\\x00', gnssId_24=GLONASS, svId_24=15, svFlag_24=b'\\r', eph_24=b'&', alm_24=b'5', otherOrb_24=b'G', gnssId_25=GLONASS, svId_25=16, svFlag_25=b'\\r', eph_25=b'\\x00', alm_25=b'5', otherOrb_25=b'\\x00', gnssId_26=GLONASS, svId_26=17, svFlag_26=b'\\x05', eph_26=b'\\x00', alm_26=b'5', otherOrb_26=b'\\x00', gnssId_27=GLONASS, svId_27=18, svFlag_27=b'\\x05', eph_27=b'\\x00', alm_27=b'5', otherOrb_27=b'\\x00', gnssId_28=GLONASS, svId_28=19, svFlag_28=b'\\x05', eph_28=b'\\x00', alm_28=b'5', otherOrb_28=b'\\x00', gnssId_29=GLONASS, svId_29=20, svFlag_29=b'\\x05', eph_29=b'\\x00', alm_29=b'5', otherOrb_29=b'\\x00', gnssId_30=GLONASS, svId_30=21, svFlag_30=b'\\t', eph_30=b'\\x00', alm_30=b'5', otherOrb_30=b'\\x00', gnssId_31=GLONASS, svId_31=22, svFlag_31=b'\\r', eph_31=b'\\x00', alm_31=b'5', otherOrb_31=b'\\x00', gnssId_32=GLONASS, svId_32=23, svFlag_32=b'\\t', eph_32=b'\\x00', alm_32=b'5', otherOrb_32=b'\\x00', gnssId_33=GLONASS, svId_33=24, svFlag_33=b'\\x05', eph_33=b'\\x00', alm_33=b'5', otherOrb_33=b'\\x00')>",
            "<UBX(NAV-SAT, iTOW=09:08:09, version=1, numCh=19, reserved11=0, reserved12=0, gnssId_01=GPS, svId_01=3, cno_01=0, elev_01=-91, azim_01=0, prRes_01=0, flags_01=b'\\x11\\x00\\x00\\x00', gnssId_02=GPS, svId_02=14, cno_02=23, elev_02=50, azim_02=87, prRes_02=31, flags_02=b'\\x1cY\\x00\\x00', gnssId_03=GPS, svId_03=15, cno_03=26, elev_03=-91, azim_03=0, prRes_03=0, flags_03=b'\\x17\\x00\\x00\\x00', gnssId_04=GPS, svId_04=20, cno_04=15, elev_04=24, azim_04=313, prRes_04=0, flags_04=b'\\x14\\x12\\x00\\x00', gnssId_05=GPS, svId_05=23, cno_05=17, elev_05=24, azim_05=315, prRes_05=0, flags_05=b'\\x14\\x12\\x00\\x00', gnssId_06=GPS, svId_06=24, cno_06=36, elev_06=25, azim_06=247, prRes_06=-3, flags_06=b'\\x1fY\\x00\\x00', gnssId_07=GPS, svId_07=30, cno_07=16, elev_07=-91, azim_07=0, prRes_07=0, flags_07=b'\\x14\\x00\\x00\\x00', gnssId_08=SBAS, svId_08=127, cno_08=0, elev_08=10, azim_08=117, prRes_08=0, flags_08=b'\\x01\\x07\\x00\\x00', gnssId_09=BeiDou, svId_09=15, cno_09=0, elev_09=-91, azim_09=0, prRes_09=0, flags_09=b'\\x01\\x00\\x00\\x00', gnssId_10=GLONASS, svId_10=4, cno_10=0, elev_10=38, azim_10=144, prRes_10=0, flags_10=b'\\x10\\x12\\x00\\x00', gnssId_11=GLONASS, svId_11=5, cno_11=22, elev_11=84, azim_11=272, prRes_11=53, flags_11=b'\\x1cY\\x00\\x00', gnssId_12=GLONASS, svId_12=6, cno_12=0, elev_12=23, azim_12=318, prRes_12=0, flags_12=b'\\x10\\x12\\x00\\x00', gnssId_13=GLONASS, svId_13=13, cno_13=0, elev_13=2, azim_13=39, prRes_13=0, flags_13=b'\\x10\\x12\\x00\\x00', gnssId_14=GLONASS, svId_14=14, cno_14=23, elev_14=53, azim_14=47, prRes_14=0, flags_14=b'\\x14\\x12\\x00\\x00', gnssId_15=GLONASS, svId_15=15, cno_15=36, elev_15=67, azim_15=201, prRes_15=9, flags_15=b'\\x1fY\\x00\\x00', gnssId_16=GLONASS, svId_16=16, cno_16=0, elev_16=11, azim_16=216, prRes_16=0, flags_16=b'\\x10\\x12\\x00\\x00', gnssId_17=GLONASS, svId_17=21, cno_17=0, elev_17=4, azim_17=301, prRes_17=0, flags_17=b'\\x10\\x12\\x00\\x00', gnssId_18=GLONASS, svId_18=22, cno_18=0, elev_18=15, azim_18=346, prRes_18=0, flags_18=b'\\x10\\x12\\x00\\x00', gnssId_19=GLONASS, svId_19=23, cno_19=0, elev_19=4, azim_19=47, prRes_19=0, flags_19=b'\\x10\\x12\\x00\\x00')>",
            "<UBX(NAV-SIG, iTOW=09:08:09, version=0, numSigs=12, reserved0=0, gnssId_01=GPS, svId_01=3, sigId_01=0, freqId_01=0, prRes_01=0, cno_01=0, qualityInd_01=1, corrSource_01=0, ionoModel_01=0, sigFlags_01=b'\\x01\\x00', reserved1_01=0, gnssId_02=GPS, svId_02=14, sigId_02=0, freqId_02=0, prRes_02=31, cno_02=23, qualityInd_02=4, corrSource_02=0, ionoModel_02=0, sigFlags_02=b')\\x00', reserved1_02=0, gnssId_03=GPS, svId_03=15, sigId_03=0, freqId_03=0, prRes_03=0, cno_03=26, qualityInd_03=7, corrSource_03=0, ionoModel_03=0, sigFlags_03=b'\\x01\\x00', reserved1_03=0, gnssId_04=GPS, svId_04=20, sigId_04=0, freqId_04=0, prRes_04=0, cno_04=15, qualityInd_04=4, corrSource_04=0, ionoModel_04=0, sigFlags_04=b'\\x01\\x00', reserved1_04=0, gnssId_05=GPS, svId_05=23, sigId_05=0, freqId_05=0, prRes_05=0, cno_05=17, qualityInd_05=4, corrSource_05=0, ionoModel_05=0, sigFlags_05=b'\\x01\\x00', reserved1_05=0, gnssId_06=GPS, svId_06=24, sigId_06=0, freqId_06=0, prRes_06=-3, cno_06=36, qualityInd_06=7, corrSource_06=0, ionoModel_06=0, sigFlags_06=b')\\x00', reserved1_06=0, gnssId_07=GPS, svId_07=30, sigId_07=0, freqId_07=0, prRes_07=0, cno_07=16, qualityInd_07=4, corrSource_07=0, ionoModel_07=0, sigFlags_07=b'\\x01\\x00', reserved1_07=0, gnssId_08=SBAS, svId_08=127, sigId_08=0, freqId_08=0, prRes_08=0, cno_08=0, qualityInd_08=1, corrSource_08=0, ionoModel_08=0, sigFlags_08=b'\\x00\\x00', reserved1_08=0, gnssId_09=BeiDou, svId_09=15, sigId_09=0, freqId_09=0, prRes_09=0, cno_09=0, qualityInd_09=1, corrSource_09=0, ionoModel_09=0, sigFlags_09=b'\\x00\\x00', reserved1_09=0, gnssId_10=GLONASS, svId_10=5, sigId_10=0, freqId_10=8, prRes_10=53, cno_10=22, qualityInd_10=4, corrSource_10=0, ionoModel_10=0, sigFlags_10=b')\\x00', reserved1_10=0, gnssId_11=GLONASS, svId_11=14, sigId_11=0, freqId_11=0, prRes_11=0, cno_11=23, qualityInd_11=4, corrSource_11=0, ionoModel_11=0, sigFlags_11=b'\\x01\\x00', reserved1_11=0, gnssId_12=GLONASS, svId_12=15, sigId_12=0, freqId_12=7, prRes_12=9, cno_12=36, qualityInd_12=7, corrSource_12=0, ionoModel_12=0, sigFlags_12=b')\\x00', reserved1_12=0)>",
            "<UBX(NAV-STATUS, iTOW=09:08:09, gpsFix=3, flags=b']', fixStat=b'\\x00', flags2=b'\\x08', ttff=179368, msss=366244)>",
            "<UBX(NAV-POSECEF, iTOW=09:08:09, ecefX=380363892, ecefY=-14879221, ecefZ=510062895, pAcc=6570)>",
            "<UBX(NAV-POSLLH, iTOW=09:08:09, lon=-22401762, lat=534506799, height=72728, hMSL=24245, hAcc=55374, vAcc=35349)>",
            "<UBX(NAV-DOP, iTOW=09:08:09, gDOP=570, pDOP=520, tDOP=233, vDOP=276, hDOP=441, nDOP=410, eDOP=161)>",
            "<UBX(NAV-VELECEF, iTOW=09:08:09, ecefVX=-25, ecefVY=-4, ecefVZ=27, sAcc=451)>",
            "<UBX(NAV-VELNED, iTOW=09:08:09, velN=36, velE=-5, velD=-7, speed=37, gSpeed=37, heading=0, sAcc=451, cAcc=13597116)>",
            "<UBX(NAV-TIMEGPS, iTOW=09:08:09, fTOW=332986, week=2146, leapS=18, valid=b'\\x07', tAcc=71)>",
            "<UBX(NAV-TIMEGLO, iTOW=09:08:09, TOD=43687, fTOD=332964, Nt=419, N4=7, valid=b'\\x03', tAcc=101)>",
            "<UBX(NAV-TIMEBDS, iTOW=09:08:09, SOW=119291, fSOW=332986, week=790, leapS=4, valid=b'\\x07', tAcc=3406)>",
            "<UBX(NAV-TIMEGAL, iTOW=09:08:09, galTow=119305, fGalTow=332986, galWno=1122, leapS=18, valid=b'\\x07', tAcc=3406)>",
            "<UBX(NAV-TIMEUTC, iTOW=09:08:09, tAcc=1071, nano=332985, year=2021, month=2, day=22, hour=9, min=8, sec=7, validflags=b'\\xf7')>",
            "<UBX(NAV-TIMELS, iTOW=09:08:09, version=0, reserved1=0, srcOfCurrLs=255, currLs=18, srcOfLsChange=6, lsChange=0, timeToLsEvent=-32887, dateOfLsGpsWn=2146, dateOfLsGpsDn=1, reserved2=0, valid=b'\\x03')>",
            "<UBX(NAV-TIMEQZSS, iTOW=09:08:09, qzssTow=119305, fQzssTow=332986, qzssWno=2146, leapS=18, valid=b'\\x07', tAcc=3406)>",
            "<UBX(NAV-CLOCK, iTOW=09:08:09, clkB=667014, clkD=-71, tAcc=71, fAcc=5239)>",
            "<UBX(NAV-SBAS, iTOW=09:08:09, geo=0, mode:=0, sys=0, service=b'\\x00', numCh=0, reserved0=0)>",
            "<UBX(NAV-SLAS, iTOW=09:08:09, version=0, reserved1=0, gmsLon=0, gmsLat=0, gmsCode=0, qzssSvId=0, serviceFlags=b'\\x00', cnt=0)>",
            "<UBX(NAV-AOPSTATUS, iTOW=09:08:09, config=1, status=0, reserved0=0, reserved1=10, avail=0, reserved2=0, reserved3=0)>",
            "<UBX(NAV-ODO, version=0, reserved0=466035, iTOW=09:08:09, distance=0, totalDistance=0, distanceStd=0)>",
            "<UBX(NAV-COV, iTOW=09:08:09, version=0, posCovValid=1, velCovValid=1, reserved0=1172170281114452235776, posCovNN=2530.31201171875, posCovNE=-856.8651123046875, posCovND=-1116.0887451171875, posCovEE=535.9963989257812, posCovED=742.3728637695312, posCovDD=1249.5338134765625, velCovNN=17.608617782592773, velCovNE=-4.361900329589844, velCovND=-5.844054222106934, velCovEE=2.3484761714935303, velCovED=2.9350130558013916, velCovDD=4.592257499694824)>",
            "<UBX(NAV-EELL, iTOW=09:08:09, version=0, reserved1=0, errEllipseOrient=15966, errEllipseMajor=132667, errEllipseMinor=36740)>",
            "<UBX(NAV-GEOFENCE, iTOW=09:08:09, version=0, status=0, numFences=0, combState=0)>",
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMIX2, False)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testMIX2VAL(self):  # test mixed UBX/NMEA stream with validate set to True
        EXPECTED_ERROR = "Unknown data header b'$G'. Looks like NMEA data. Set ubx_only flag to 'False' to ignore."
        ubxreader = UBXReader(self.streamMIX2, True)
        with self.assertRaises(UBXStreamError) as context:
            (_, _) = ubxreader.read()
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testINF(self):
        EXPECTED_RESULTS = (
        "<UBX(INF-NOTICE, message=u-blox AG - www.u-blox.com)>",
        "<UBX(INF-NOTICE, message=HW UBX-M8030 00080000)>",
        "<UBX(INF-NOTICE, message=ROM CORE 3.01 (107888))>",
        "<UBX(INF-NOTICE, message=FWVER=SPG 3.01)>",
        "<UBX(INF-NOTICE, message=PROTVER=18.00)>",
        "<UBX(INF-NOTICE, message=GPS;GLO;GAL;BDS)>",
        "<UBX(INF-NOTICE, message=SBAS;IMES;QZSS)>",
        "<UBX(INF-NOTICE, message=GNSS OTP=GPS;GLO)>",
        "<UBX(INF-NOTICE, message=LLC=FFFFFFFF-FFFFFFFF-FFFFFFFF-FFFFFFFF-FFFFFFFD)>",
        "<UBX(INF-NOTICE, message=ANTSUPERV=AC SD PDoS SR)>",
        "<UBX(INF-NOTICE, message=ANTSTATUS=OK)>",
        "<UBX(INF-NOTICE, message=PF=3FF)>"
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamINF)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testMON(self):
        EXPECTED_RESULTS = (
        "<UBX(MON-MSGPP, msg1_01=0, msg1_02=0, msg1_03=0, msg1_04=0, msg1_05=0, msg1_06=0, msg1_07=0, msg1_08=0, msg2_01=0, msg2_02=0, msg2_03=0, msg2_04=0, msg2_05=0, msg2_06=0, msg2_07=0, msg2_08=0, msg3_01=0, msg3_02=0, msg3_03=0, msg3_04=0, msg3_05=0, msg3_06=0, msg3_07=0, msg3_08=0, msg4_01=69, msg4_02=0, msg4_03=0, msg4_04=0, msg4_05=0, msg4_06=0, msg4_07=0, msg4_08=0, msg5_01=0, msg5_02=0, msg5_03=0, msg5_04=0, msg5_05=0, msg5_06=0, msg5_07=0, msg5_08=0, msg6_01=0, msg6_02=0, msg6_03=0, msg6_04=0, msg6_05=0, msg6_06=0, msg6_07=0, msg6_08=0, skipped_01=0, skipped_02=0, skipped_03=0, skipped_04=0, skipped_05=0, skipped_06=0)>",
        "<UBX(MON-TXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=2, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=12, peakUsage_03=0, peakUsage_04=25, peakUsage_05=0, peakUsage_06=0, tUsage=2, tPeakUsage=25, errors=b'\\x00', reserved1=0)>",
        "<UBX(MON-RXBUF, pending_01=0, pending_02=0, pending_03=0, pending_04=0, pending_05=0, pending_06=0, usage_01=0, usage_02=0, usage_03=0, usage_04=0, usage_05=0, usage_06=0, peakUsage_01=0, peakUsage_02=0, peakUsage_03=0, peakUsage_04=2, peakUsage_05=0, peakUsage_06=0)>",
        "<UBX(MON-IO, rxBytes=0, txBytes=0, parityErrs=0, framingErrs=0, overrunErrs=0, breakCond=0, rxBusy=0, txBusy=0, reserved1=0)>",
        "<UBX(MON-HW, pinSel=b'\\x00\\xf4\\x01\\x00', pinBank=b'\\x00\\x00\\x00\\x00', pinDir=b'\\x00\\x00\\x01\\x00', pinVal=b'\\xef\\xf7\\x00\\x00', noisePerMS=87, agcCnt=3042, aStatus=2, aPower=1, flags=b'\\x01', reserved1=132, usedMask=b'\\xff\\xeb\\x01\\x00', VP_01=b'\\n', VP_02=b'\\x0b', VP_03=b'\\x0c', VP_04=b'\\r', VP_05=b'\\x0e', VP_06=b'\\x0f', VP_07=b'\\x01', VP_08=b'\\x00', VP_09=b'\\x02', VP_10=b'\\x03', VP_11=b'\\xff', VP_12=b'\\x10', VP_13=b'\\xff', VP_14=b'\\x12', VP_15=b'\\x13', VP_16=b'6', VP_17=b'5', VP_18=b'\\x05', VP_19=b'\\xef', VP_20=b'^', VP_21=b'\\x00', VP_22=b'\\x00', VP_23=b'\\x00', VP_24=b'\\x00', VP_25=b'\\x80', jamInd=247, reserved3=0, pinIrq=b'\\x00\\x00\\x00\\x00', pullH=b'', pullL=b'')>",
        "<UBX(MON-HW2, ofsI=4, magI=110, ofsQ=5, magQ=112, cfgSource=111, reserved0=1800, lowLevCfg=b'\\xff\\xff\\xff\\xff', reserved11=4294967295, reserved12=4294967295, postStatus=b'\\x00\\x00\\x00\\x00', reserved2=0)>"
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMON)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testRXM(self):
        EXPECTED_RESULTS = (
        "<UBX(RXM-MEASX, version=1, reserved0=0, gpsTOW=231234000, gloTOW=242016000, bdsTOW=231220000, reserved1=231234000, qzssTOW=1000, gpsTOWacc=0, gloTOWacc=0, bdsTOWacc=0, reserved2=0, qzssTOWacc=0, numSv=9, flags=46, reserved3=0, gnssId_01=QZSS, svId_01=1, cNo_01=12, mpathIndic_01=1, dopplerMS_01=11538, dopplerHz_01=12126, wholeChips_01=809, fracChips_01=24, codePhase_01=1658502, intCodePhase_01=0, pseuRangeRMSErr_01=52, reserved4_01=0, gnssId_02=GPS, svId_02=18, cNo_02=17, mpathIndic_02=1, dopplerMS_02=2646, dopplerHz_02=2781, wholeChips_02=858, fracChips_02=265, codePhase_02=1759434, intCodePhase_02=0, pseuRangeRMSErr_02=46, reserved4_02=0, gnssId_03=GPS, svId_03=28, cNo_03=18, mpathIndic_03=1, dopplerMS_03=10576, dopplerHz_03=11115, wholeChips_03=536, fracChips_03=533, codePhase_03=1099868, intCodePhase_03=0, pseuRangeRMSErr_03=46, reserved4_03=0, gnssId_04=GLONASS, svId_04=8, cNo_04=17, mpathIndic_04=1, dopplerMS_04=11949, dopplerHz_04=12797, wholeChips_04=55, fracChips_04=693, codePhase_04=228499, intCodePhase_04=0, pseuRangeRMSErr_04=46, reserved4_04=0, gnssId_05=GLONASS, svId_05=9, cNo_05=25, mpathIndic_05=1, dopplerMS_05=4320, dopplerHz_05=4614, wholeChips_05=279, fracChips_05=102, codePhase_05=1145429, intCodePhase_05=0, pseuRangeRMSErr_05=27, reserved4_05=0, gnssId_06=GLONASS, svId_06=7, cNo_06=24, mpathIndic_06=1, dopplerMS_06=-3672, dopplerHz_06=-3931, wholeChips_06=100, fracChips_06=156, codePhase_06=411030, intCodePhase_06=0, pseuRangeRMSErr_06=46, reserved4_06=0, gnssId_07=GPS, svId_07=7, cNo_07=13, mpathIndic_07=1, dopplerMS_07=-14783, dopplerHz_07=-15537, wholeChips_07=947, fracChips_07=989, codePhase_07=1943334, intCodePhase_07=0, pseuRangeRMSErr_07=52, reserved4_07=0, gnssId_08=GPS, svId_08=13, cNo_08=28, mpathIndic_08=1, dopplerMS_08=5649, dopplerHz_08=5937, wholeChips_08=239, fracChips_08=545, codePhase_08=491043, intCodePhase_08=0, pseuRangeRMSErr_08=15, reserved4_08=0, gnssId_09=GPS, svId_09=5, cNo_09=32, mpathIndic_09=1, dopplerMS_09=-9606, dopplerHz_09=-10096, wholeChips_09=220, fracChips_09=411, codePhase_09=451825, intCodePhase_09=0, pseuRangeRMSErr_09=18, reserved4_09=0)>",
        "<UBX(RXM-SVSI, iTOW=16:13:38, week=2128, numVis=24, numSV=190, svid=1, svFlag=b'_', azim=82, elev=-49, age=b'\\xf2')>",
        "<UBX(RXM-IMES, numTx=0, version=1, reserved1=0)>",
        "<UBX(RXM-SFRBX, gnssId=GPS, svId=5, reserved0=0, freqId=0, numWords=10, chn=0, version=2, reserved1=0, dwrd_01=583028782, dwrd_02=2463198336, dwrd_03=394902765, dwrd_04=2566867280, dwrd_05=1062207503, dwrd_06=675481840, dwrd_07=616371498, dwrd_08=2740700967, dwrd_09=768066377, dwrd_10=3045061856)>"
        )

        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamRXM)
        while raw is not None:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testIterator(self):  # test iterator function with UBX data stream
        EXPECTED_RESULTS = (
        "<UBX(RXM-MEASX, version=1, reserved0=0, gpsTOW=231234000, gloTOW=242016000, bdsTOW=231220000, reserved1=231234000, qzssTOW=1000, gpsTOWacc=0, gloTOWacc=0, bdsTOWacc=0, reserved2=0, qzssTOWacc=0, numSv=9, flags=46, reserved3=0, gnssId_01=QZSS, svId_01=1, cNo_01=12, mpathIndic_01=1, dopplerMS_01=11538, dopplerHz_01=12126, wholeChips_01=809, fracChips_01=24, codePhase_01=1658502, intCodePhase_01=0, pseuRangeRMSErr_01=52, reserved4_01=0, gnssId_02=GPS, svId_02=18, cNo_02=17, mpathIndic_02=1, dopplerMS_02=2646, dopplerHz_02=2781, wholeChips_02=858, fracChips_02=265, codePhase_02=1759434, intCodePhase_02=0, pseuRangeRMSErr_02=46, reserved4_02=0, gnssId_03=GPS, svId_03=28, cNo_03=18, mpathIndic_03=1, dopplerMS_03=10576, dopplerHz_03=11115, wholeChips_03=536, fracChips_03=533, codePhase_03=1099868, intCodePhase_03=0, pseuRangeRMSErr_03=46, reserved4_03=0, gnssId_04=GLONASS, svId_04=8, cNo_04=17, mpathIndic_04=1, dopplerMS_04=11949, dopplerHz_04=12797, wholeChips_04=55, fracChips_04=693, codePhase_04=228499, intCodePhase_04=0, pseuRangeRMSErr_04=46, reserved4_04=0, gnssId_05=GLONASS, svId_05=9, cNo_05=25, mpathIndic_05=1, dopplerMS_05=4320, dopplerHz_05=4614, wholeChips_05=279, fracChips_05=102, codePhase_05=1145429, intCodePhase_05=0, pseuRangeRMSErr_05=27, reserved4_05=0, gnssId_06=GLONASS, svId_06=7, cNo_06=24, mpathIndic_06=1, dopplerMS_06=-3672, dopplerHz_06=-3931, wholeChips_06=100, fracChips_06=156, codePhase_06=411030, intCodePhase_06=0, pseuRangeRMSErr_06=46, reserved4_06=0, gnssId_07=GPS, svId_07=7, cNo_07=13, mpathIndic_07=1, dopplerMS_07=-14783, dopplerHz_07=-15537, wholeChips_07=947, fracChips_07=989, codePhase_07=1943334, intCodePhase_07=0, pseuRangeRMSErr_07=52, reserved4_07=0, gnssId_08=GPS, svId_08=13, cNo_08=28, mpathIndic_08=1, dopplerMS_08=5649, dopplerHz_08=5937, wholeChips_08=239, fracChips_08=545, codePhase_08=491043, intCodePhase_08=0, pseuRangeRMSErr_08=15, reserved4_08=0, gnssId_09=GPS, svId_09=5, cNo_09=32, mpathIndic_09=1, dopplerMS_09=-9606, dopplerHz_09=-10096, wholeChips_09=220, fracChips_09=411, codePhase_09=451825, intCodePhase_09=0, pseuRangeRMSErr_09=18, reserved4_09=0)>",
        "<UBX(RXM-SVSI, iTOW=16:13:38, week=2128, numVis=24, numSV=190, svid=1, svFlag=b'_', azim=82, elev=-49, age=b'\\xf2')>",
        "<UBX(RXM-IMES, numTx=0, version=1, reserved1=0)>",
        "<UBX(RXM-SFRBX, gnssId=GPS, svId=5, reserved0=0, freqId=0, numWords=10, chn=0, version=2, reserved1=0, dwrd_01=583028782, dwrd_02=2463198336, dwrd_03=394902765, dwrd_04=2566867280, dwrd_05=1062207503, dwrd_06=675481840, dwrd_07=616371498, dwrd_08=2740700967, dwrd_09=768066377, dwrd_10=3045061856)>"
        )

        i = 0
        ubxreader = UBXReader(self.streamRXM, True)
        for (_, parsed) in ubxreader:
            self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
            i += 1

    def testIterator2(self):  # test iterator function with mixed data stream
        EXPECTED_ERROR = "Unknown data header b'$G'. Looks like NMEA data. Set ubx_only flag to 'False' to ignore."
        ubxreader = UBXReader(self.streamMIX, True)
        with self.assertRaises(UBXStreamError) as context:
            i = 0
#             (raw, parsed) = ubxreader.read()
            for (_, _) in ubxreader:
                i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testIterator3(self):  # test iterator function with mixed data stream
        EXPECTED_RESULTS = (
        "<UBX(NAV-SOL, iTOW=11:33:17, fTOW=52790, week=2128, gpsFix=3, flags=b'\\xdd', ecefX=380364134, ecefY=-14880030, ecefZ=510063062, pAcc=1026, ecefVX=-3, ecefVY=0, ecefVZ=1, sAcc=72, pDOP=135, reserved1=2, numSV=15, reserved2=215776)>",
        "<UBX(NAV-PVT, iTOW=11:33:17, year=2020, month=10, day=23, hour=11, min=33, second=15, valid=b'7', tAcc=17, nano=52792, fixType=3, flags=b'\\x01', flags2=b'\\n', numSV=15, lon=-22402964, lat=534506691, height=75699, hMSL=27215, hAcc=6298, vAcc=8101, velN=27, velE=-4, velD=11, gSpeed=27, headMot=770506, sAcc=715, headAcc=3905453, pDOP=135, reserved1=151580049408, headVeh=0, magDec=0, magAcc=0)>",
        "<UBX(NAV-SVINFO, iTOW=11:33:17, numCh=25, globalFlags=b'\\x04', reserved2=0, chn_01=13, svid_01=1, flags_01=b'\\x0c', quality_01=b'\\x01', cno_01=0, elev_01=4, azim_01=142, prRes_01=0, chn_02=19, svid_02=2, flags_02=b'\\x04', quality_02=b'\\x01', cno_02=0, elev_02=19, azim_02=311, prRes_02=0, chn_03=3, svid_03=3, flags_03=b'\\r', quality_03=b'\\x04', cno_03=24, elev_03=41, azim_03=89, prRes_03=469, chn_04=0, svid_04=4, flags_04=b'\\r', quality_04=b'\\x07', cno_04=26, elev_04=70, azim_04=98, prRes_04=94, chn_05=1, svid_05=6, flags_05=b'\\r', quality_05=b'\\x07', cno_05=29, elev_05=61, azim_05=287, prRes_05=-1023, chn_06=255, svid_06=7, flags_06=b'\\x04', quality_06=b'\\x00', cno_06=0, elev_06=0, azim_06=168, prRes_06=0, chn_07=2, svid_07=9, flags_07=b'\\r', quality_07=b'\\x07', cno_07=32, elev_07=56, azim_07=200, prRes_07=-18, chn_08=23, svid_08=12, flags_08=b'\\x04', quality_08=b'\\x01', cno_08=0, elev_08=1, azim_08=311, prRes_08=0, chn_09=5, svid_09=17, flags_09=b'\\r', quality_09=b'\\x04', cno_09=23, elev_09=26, azim_09=226, prRes_09=505, chn_10=4, svid_10=19, flags_10=b'\\r', quality_10=b'\\x04', cno_10=25, elev_10=35, azim_10=242, prRes_10=1630, chn_11=6, svid_11=22, flags_11=b'\\r', quality_11=b'\\x04', cno_11=21, elev_11=20, azim_11=96, prRes_11=-1033, chn_12=22, svid_12=25, flags_12=b'\\x04', quality_12=b'\\x01', cno_12=0, elev_12=4, azim_12=344, prRes_12=0, chn_13=11, svid_13=31, flags_13=b'\\r', quality_13=b'\\x04', cno_13=14, elev_13=10, azim_13=27, prRes_13=1714, chn_14=18, svid_14=120, flags_14=b'\\x14', quality_14=b'\\x01', cno_14=0, elev_14=28, azim_14=196, prRes_14=0, chn_15=20, svid_15=123, flags_15=b'\\x14', quality_15=b'\\x01', cno_15=0, elev_15=22, azim_15=140, prRes_15=0, chn_16=16, svid_16=136, flags_16=b'\\x14', quality_16=b'\\x01', cno_16=0, elev_16=29, azim_16=171, prRes_16=0, chn_17=14, svid_17=65, flags_17=b'\\r', quality_17=b'\\x04', cno_17=21, elev_17=33, azim_17=252, prRes_17=139, chn_18=8, svid_18=71, flags_18=b'\\r', quality_18=b'\\x04', cno_18=19, elev_18=44, azim_18=53, prRes_18=1941, chn_19=9, svid_19=72, flags_19=b'\\r', quality_19=b'\\x04', cno_19=20, elev_19=76, azim_19=286, prRes_19=-1155, chn_20=15, svid_20=73, flags_20=b'\\r', quality_20=b'\\x06', cno_20=25, elev_20=19, azim_20=81, prRes_20=-115, chn_21=21, svid_21=79, flags_21=b'\\x04', quality_21=b'\\x01', cno_21=0, elev_21=0, azim_21=342, prRes_21=0, chn_22=17, svid_22=80, flags_22=b'\\x04', quality_22=b'\\x04', cno_22=18, elev_22=20, azim_22=29, prRes_22=0, chn_23=7, svid_23=86, flags_23=b'\\r', quality_23=b'\\x04', cno_23=10, elev_23=18, azim_23=177, prRes_23=-149, chn_24=10, svid_24=87, flags_24=b'\\r', quality_24=b'\\x07', cno_24=32, elev_24=65, azim_24=257, prRes_24=169, chn_25=12, svid_25=88, flags_25=b'\\r', quality_25=b'\\x04', cno_25=23, elev_25=40, azim_25=318, prRes_25=-93)>"
        )
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamMIX, False)
        while raw is not None and i < 3:
            (raw, parsed) = ubxreader.read()
            if raw is not None:
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1

    def testBADHDR(self):  # invalid header in data
        EXPECTED_ERROR = "Unknown data header b'\\xb5\\x01'"
        with self.assertRaises(UBXStreamError) as context:
            i = 0
            ubxreader = UBXReader(self.streamBADHDR, True)
            for (_, _) in ubxreader:
                i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testBADEOF1(self):  # premature EOF after header
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF1)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 4)

    def testBADEOF2(self):  # premature EOF after message class and length
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF2)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 3)

    def testBADEOF3(self):  # premature EOF after first byte of header
        i = 0
        raw = 0
        ubxreader = UBXReader(self.streamBADEOF3)
        while raw is not None:
            (raw, _) = ubxreader.read()
            i += 1
        self.assertEqual(i, 3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
