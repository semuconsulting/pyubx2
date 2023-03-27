"""
Bitfield parse method tests for pyubx2.UBXMessage

Created on 16 Oct 2021

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, UBXReader, GET


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nav_sat2 = b"\xb5b\x015\x14\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00+*\xf0\x00\xfd\xff\x07\x07\x00\x00\x9bt"  # qualityInd = 7, orbitSource = 7
        self.nav_sat3 = b"\xb5b\x015\x14\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00+*\xf0\x00\xfd\xff\x03\x04\x02\x00\x96_"  # rtcmCorrUsed = 1
        self.nav_sat4 = b"\xb5b\x015\x14\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00+*\xf0\x00\xfd\xff\x0a\x15\x5f\x00\x0bh"  # svUsed = 1, almUsed = 1

    def tearDown(self):
        pass

    def testNavSat2(
        self,
    ):  # check X4 bitfield correctly parsed (remember little-endian)
        res = UBXReader.parse(self.nav_sat2)
        self.assertEqual(
            str(res),
            "<UBX(NAV-SAT, iTOW=23:59:42, version=1, numSvs=1, reserved0=0, gnssId_01=GPS, svId_01=0, cno_01=43, elev_01=42, azim_01=240, prRes_01=-0.3, qualityInd_01=7, svUsed_01=0, health_01=0, diffCorr_01=0, smoothed_01=0, orbitSource_01=7, ephAvail_01=0, almAvail_01=0, anoAvail_01=0, aopAvail_01=0, sbasCorrUsed_01=0, rtcmCorrUsed_01=0, slasCorrUsed_01=0, spartnCorrUsed_01=0, prCorrUsed_01=0, crCorrUsed_01=0, doCorrUsed_01=0)>",
        )

    def testNavSat3(
        self,
    ):  # check X4 bitfield correctly parsed (remember little-endian)
        res = UBXReader.parse(self.nav_sat3)
        self.assertEqual(
            str(res),
            "<UBX(NAV-SAT, iTOW=23:59:42, version=1, numSvs=1, reserved0=0, gnssId_01=GPS, svId_01=0, cno_01=43, elev_01=42, azim_01=240, prRes_01=-0.3, qualityInd_01=3, svUsed_01=0, health_01=0, diffCorr_01=0, smoothed_01=0, orbitSource_01=4, ephAvail_01=0, almAvail_01=0, anoAvail_01=0, aopAvail_01=0, sbasCorrUsed_01=0, rtcmCorrUsed_01=1, slasCorrUsed_01=0, spartnCorrUsed_01=0, prCorrUsed_01=0, crCorrUsed_01=0, doCorrUsed_01=0)>",
        )

    def testNavSat4(
        self,
    ):  # check X4 bitfield correctly parsed (remember little-endian)
        res = UBXReader.parse(self.nav_sat4)
        self.assertEqual(
            str(res),
            "<UBX(NAV-SAT, iTOW=23:59:42, version=1, numSvs=1, reserved0=0, gnssId_01=GPS, svId_01=0, cno_01=43, elev_01=42, azim_01=240, prRes_01=-0.3, qualityInd_01=2, svUsed_01=1, health_01=0, diffCorr_01=0, smoothed_01=0, orbitSource_01=5, ephAvail_01=0, almAvail_01=1, anoAvail_01=0, aopAvail_01=0, sbasCorrUsed_01=1, rtcmCorrUsed_01=1, slasCorrUsed_01=1, spartnCorrUsed_01=1, prCorrUsed_01=1, crCorrUsed_01=0, doCorrUsed_01=1)>",
        )

    def testNavSat5(self):  # check message bytes match original byte stream
        res = UBXReader.parse(self.nav_sat4)
        self.assertEqual(res.serialize(), self.nav_sat4)

    def testNavSat6(
        self,
    ):  # check message correctly constructed from individual bit flags
        res = UBXMessage(
            "NAV",
            "NAV-SAT",
            GET,
            version=1,
            numSvs=1,
            gnssId_01=0,
            svId_01=0,
            cno_01=43,
            elev_01=42,
            azim_01=240,
            prRes_01=-0.30000000000000004,
            qualityInd_01=2,
            svUsed_01=1,
            health_01=0,
            diffCorr_01=0,
            smoothed_01=0,
            orbitSource_01=5,
            ephAvail_01=0,
            almAvail_01=1,
            anoAvail_01=0,
            aopAvail_01=0,
            sbasCorrUsed_01=1,
            rtcmCorrUsed_01=1,
            slasCorrUsed_01=1,
            spartnCorrUsed_01=1,
            prCorrUsed_01=1,
            crCorrUsed_01=0,
            doCorrUsed_01=1,
        )
        self.assertEqual(
            str(res),
            "<UBX(NAV-SAT, iTOW=23:59:42, version=1, numSvs=1, reserved0=0, gnssId_01=GPS, svId_01=0, cno_01=43, elev_01=42, azim_01=240, prRes_01=-0.30000000000000004, qualityInd_01=2, svUsed_01=1, health_01=0, diffCorr_01=0, smoothed_01=0, orbitSource_01=5, ephAvail_01=0, almAvail_01=1, anoAvail_01=0, aopAvail_01=0, sbasCorrUsed_01=1, rtcmCorrUsed_01=1, slasCorrUsed_01=1, spartnCorrUsed_01=1, prCorrUsed_01=1, crCorrUsed_01=0, doCorrUsed_01=1)>",
        )
        self.assertEqual(res.serialize(), self.nav_sat4)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
