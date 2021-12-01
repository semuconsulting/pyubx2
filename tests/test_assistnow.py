"""
Test MGA-GPS-ALM and MGA-GPS-EPH message payloads created by u-blox uCenter AssistNow Utility

Created on 23 Nov 2020

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, SET


class AssistNowTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.mga_gps_alm_payloads = [  # created using uCenter AssistNow Offline
            b"\x02\x00\x01\x00\x0D\x53\x55\x39\x31\x1A5F\xFD\x37\x0D\xA1\x00\x08\x9D\xF8\xFF\x12\xA7\x21\x00\xF3\xB207\x00\x4B\x03\xFF\xFF\x00\x00\x00\x00",
            b"\x02\x00\x02\x00\xAC\xA4\x55\x39\x64\x0C52\xFD\x1D\x0C\xA1\x00\xE7\x5A\xF5\xFF\x3F\x83\xBF\xFF\xE1\xC910\x00\xC3\xFD\xFF\xFF\x00\x00\x00\x00",
            b"\x02\x00\x03\x00\xAF\x1A\x55\x39\x26\x1043\xFD\x2F\x0D\xA1\x00\xB1\xEF\x22\x00\xE7\xA7\x24\x00\xBC\x07D7\xFF\xF3\xFF\xFD\xFF\x00\x00\x00\x00",
            b"\x02\x00\x04\x00\xAA\x07\x55\x39\x57\x0B57\xFD\x7E\x0C\xA1\x00\xC1\xF1\x4E\x00\x98\x8B\x83\xFF\x1A\xD54C\x00\x5A\xFF\xFF\xFF\x00\x00\x00\x00",
            b"\x02\x00\x05\x00\x9F\x31\x55\x39\xA5\x0735\xFD\xB0\x0D\xA1\x00\x12\x89\x21\x00\x23\x74\x24\x00\xD3\x0D7C\x00\xE4\xFF\x00\x00\x00\x00\x00\x00",
        ]

        self.mga_gps_eph_payloads = [  # created using uCenter AssistNow Online
            b"\x01\x00\x01\x00\x00\x01\x00\x0B\x4F\x00A4\x1F\x00\x00\xDB\xFF\x50\x5C\x1A\x00\x3A\x03\x4F\x2D\x19\x5867\x9E\x80\x02\xE4\x0D\x8D\x2E\x30\x05\xA2\x8E\x0D\xA1\xA4\x1F46\x00\x69\x76\xA5\xF8\xB9\xFF\xC7\x20\x14\x1D\x09\x28\xF4\xD3AA\x21\x2B\xAA\xFF\xFF\xAA\x04\x00\x00\x20\xF1",
            b"\x01\x00\x02\x00\x00\x00\x00\xDA\x42\x00A4\x1F\x00\x00\xD7\xFF\x96\x1B\xEE\xFF\x02\x03\xB4\x30\x65\x7179\xA7\x2A\x03\xA4\x0C\x25\xFB\x49\x0A\xFC\x82\x0C\xA1\xA4\x1F7F\x00\x49\x9C\x63\xF5\x62\x00\x42\x20\xD5\x5E\x2C\x27\x29\x1E7F\xBF\xA6\xAA\xFF\xFF\x16\x04\x00\x00\xBD\xE1",
            b"\x01\x00\x03\x00\x00\x00\x00\x04\x14\x00A4\x1F\x00\x00\xA8\xFF\x3C\xA0\xFF\xFF\x35\xF9\x80\x32\xCF\xAAAC\x6D\xEA\xF9\x35\x0B\x7C\xC7\xAA\x01\xEB\x9F\x0D\xA1\xA4\x1FF0\xFF\x75\xA1\xF8\x22\xEF\xFF\xB2\x22\xC3\xB5\x68\x27\x93\x77BA\x24\xE9\xA6\xFF\xFF\xF8\xFE\x00\x00\x88\x8B",
            b"\x01\x00\x04\x00\x00\x00\x00\xF7\x3E\x02A4\x1F\x00\x00\xE1\xFF\xAB\xD2\xFA\xFF\x1F\xFB\xC7\x2F\xB8\xF560\xE3\x94\xFB\x3B\x16\x65\x55\x7A\x00\x59\xEC\x0C\xA1\xA4\x1F15\x00\xB3\x6D\xFA\x4E\xF7\xFF\xDD\x15\xFC\x36\x1C\x27\x7F\x7AAF\x83\xDB\xA9\xFF\xFF\x73\xFE\x00\x00\x6D\x49",
            b"\x01\x00\x05\x00\x00\x00\x00\xE8\x07\x00A4\x1F\x00\x00\xF8\xFF\xE6\x20\xFF\xFF\xFA\xF9\x71\x36\xB4\x04C4\x12\x28\xFB\x12\x0B\x32\x3A\x1A\x03\x84\x26\x0E\xA1\xA4\x1FF7\xFF\x03\x2F\x92\x21\x0C\x00\x25\x22\xAE\x95\xE0\x26\xCA\x457B\x24\xC4\xA3\xFF\xFF\x2D\xFF\x00\x00\xCD\x1F",
        ]

    def tearDown(self):
        pass

    def testAssistNowALM(self):
        EXPECTED_RESULTS = [
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=1, svHealth=0, e=0.01013803, almWNa=85, toa=233472, deltaI=0.01278877, omegaDot=7e-08, sqrtA=1319334.99853516, omega0=-14.77319336, omega=67.30526721, m0=97.39804077, af0=5.245e-05, af1=0.0, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=2, svHealth=0, e=0.02010155, almWNa=85, toa=233472, deltaI=0.00605011, omegaDot=5e-08, sqrtA=1319299.74853516, omega0=-21.28982544, omega=-128.97460949, m0=99.57720935, af0=4.578e-05, af1=-0.0, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=3, svHealth=0, e=0.00325727, almWNa=85, toa=233472, deltaI=0.00788498, omegaDot=5e-08, sqrtA=1319333.99853516, omega0=69.87258911, omega=73.31173706, m0=136.0604248, af0=-0.00019169, af1=-0.0, reserved0=65533)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=4, svHealth=0, e=0.00093555, almWNa=85, toa=233472, deltaI=0.00553703, omegaDot=5e-08, sqrtA=1319311.87353516, omega0=157.88870239, omega=-248.90942383, m0=105.66488636, af0=6.39e-05, af1=-0.0, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=5, svHealth=0, e=0.00605726, almWNa=85, toa=233472, deltaI=0.00373268, omegaDot=5e-08, sqrtA=1319350.12353516, omega0=67.07086182, omega=72.90731812, m0=110.10800171, af0=6.39e-05, af1=-0.0, reserved0=0)>",
        ]
        for i, pld in enumerate(self.mga_gps_alm_payloads):
            res = UBXMessage("MGA", "MGA-GPS-ALM", SET, payload=pld)
            self.assertEqual(str(res), EXPECTED_RESULTS[i])

    def testAssistNowEPH(self):
        EXPECTED_RESULTS = [
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=1, reserved0=0, fitInterval=0, uraIndex=1, svHealth=0, tgd=1e-08, iodc=79, toc=214032, reserved1=31, af2=0.0, af1=-0.0, af0=0.20594227, crs=464.0, deltaN=0.0, m0=0.42456355, cuc=-4.663e-05, cus=1.19e-06, e=0.09091991, sqrtA=4564.25253296, toe=659664, cic=1.509e-05, omega0=0.82031896, cis=-4.317e-05, crc=-560.25, i0=0.1572504, omega=-0.09252821, omegaDot=6.343e-05, idot=-0.0, reserved2=78315519)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=2, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-2e-08, iodc=66, toc=214032, reserved1=31, af2=0.0, af1=-0.0, af0=-0.13978303, crs=23.96875, deltaN=-0.0, m0=0.43314805, cuc=-4.233e-05, cus=1.51e-06, e=0.49051704, sqrtA=4191.50502205, toe=659648, cic=1.509e-05, omega0=0.57032087, cis=4.75e-05, crc=791.65625, i0=-0.33495307, omega=0.32150797, omegaDot=-0.00012345, idot=-0.0, reserved2=68616191)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=3, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=0.0, iodc=20, toc=214032, reserved1=31, af2=0.0, af1=-0.0, af0=-0.00292242, crs=431.96875, deltaN=-0.0, m0=0.51302519, cuc=5.21e-05, cus=-2.9e-06, e=0.38961825, sqrtA=5117.37581253, toe=659664, cic=1.509e-05, omega0=0.92185024, cis=-3.51e-06, crc=-134.9375, i0=-0.47550356, omega=-0.85035983, omegaDot=6.915e-05, idot=-0.0, reserved2=4277731327)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=4, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-0.0, iodc=574, toc=214032, reserved1=31, af2=0.0, af1=-0.0, af0=-0.04044581, crs=255.96875, deltaN=-0.0, m0=0.42937376, cuc=-1.374e-05, cus=-2.11e-06, e=0.16678686, sqrtA=7563.1252327, toe=659648, cic=1.509e-05, omega0=-0.60155616, cis=-2.66e-06, crc=-69.5625, i0=-0.03058267, omega=0.99338105, omegaDot=-0.0002379, idot=-0.0, reserved2=4269015039)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=5, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-1e-08, iodc=7, toc=214032, reserved1=31, af2=0.0, af1=-0.0, af0=-0.0068084, crs=-40.03125, deltaN=0.0, m0=0.52358105, cuc=8.68e-06, cus=-2.31e-06, e=0.11366305, sqrtA=1232.50151443, toe=659680, cic=1.509e-05, omega0=0.03122607, cis=-5.236e-05, crc=97.03125, i0=-0.63958299, omega=-0.42068856, omegaDot=6.916e-05, idot=-0.0, reserved2=4281204735)>",
        ]
        for i, pld in enumerate(self.mga_gps_eph_payloads):
            res = UBXMessage("MGA", "MGA-GPS-EPH", SET, payload=pld)
            self.assertEqual(str(res), EXPECTED_RESULTS[i])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
