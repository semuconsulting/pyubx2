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
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=1, svHealth=0, e=0.010138034821, almWNa=85, toa=233472, deltaI=0.012788772583, omegaDot=6.5385e-08, sqrtA=1319334.9985351562, omega0=-14.773193359375, omega=67.305267214775, m0=97.398040771484, af0=5.2452087e-05, af1=3.067e-09, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=2, svHealth=0, e=0.020101547241, almWNa=85, toa=233472, deltaI=0.006050109863, omegaDot=4.6759e-08, sqrtA=1319299.7485351562, omega0=-21.289825439453, omega=-128.974609494209, m0=99.577209353447, af0=4.5776367e-05, af1=-2.085e-09, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=3, svHealth=0, e=0.003257274628, almWNa=85, toa=233472, deltaI=0.007884979248, omegaDot=4.7687e-08, sqrtA=1319333.9985351562, omega0=69.872589111328, omega=73.311737060547, m0=136.060424804688, af0=-0.000191688538, af1=-4.7e-11, reserved0=65533)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=4, svHealth=0, e=0.000935554504, almWNa=85, toa=233472, deltaI=0.005537033081, omegaDot=5.1416e-08, sqrtA=1319311.8735351562, omega0=157.888702392578, omega=-248.909423828125, m0=105.6648863554, af0=6.3896179e-05, af1=-6.04e-10, reserved0=65535)>",
            "<UBX(MGA-GPS-ALM, type=2, version=0, svId=5, svHealth=0, e=0.006057262421, almWNa=85, toa=233472, deltaI=0.003732681274, omegaDot=4.9546e-08, sqrtA=1319350.1235351562, omega0=67.070861816406, omega=72.907318115234, m0=110.108001708984, af0=6.3896179e-05, af1=-1.02e-10, reserved0=0)>",
        ]
        for i, pld in enumerate(self.mga_gps_alm_payloads):
            res = UBXMessage("MGA", "MGA-GPS-ALM", SET, payload=pld)
            # print(res)
            self.assertEqual(str(res), EXPECTED_RESULTS[i])

    def testAssistNowEPH(self):
        EXPECTED_RESULTS = [
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=1, reserved0=0, fitInterval=0, uraIndex=1, svHealth=0, tgd=5.122e-09, iodc=79, toc=214032, reserved1=31, af2=0.0, af1=-1.077e-09, af0=0.205942272674, crs=464.0, deltaN=2.3e-09, m0=0.424563548062, cuc=-4.6627596e-05, cus=1.192093e-06, e=0.090919908602, sqrtA=4564.252532958984, toe=659664, cic=1.5087426e-05, omega0=0.820318961516, cis=-4.3172389e-05, crc=-560.25, i0=0.157250403892, omega=-0.092528210487, omegaDot=6.3428708e-05, idot=-2.498e-09, reserved2=78315519)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=2, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-1.7695e-08, iodc=66, toc=214032, reserved1=31, af2=0.0, af1=-1.193e-09, af0=-0.139783025254, crs=23.96875, deltaN=-2.212e-09, m0=0.433148048818, cuc=-4.2332336e-05, cus=1.508743e-06, e=0.490517039318, sqrtA=4191.50502204895, toe=659648, cic=1.5087426e-05, omega0=0.570320870262, cis=4.7497451e-05, crc=791.65625, i0=-0.334953069687, omega=0.321507974528, omegaDot=-0.000123454516, idot=-2.484e-09, reserved2=68616191)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=3, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=1.863e-09, iodc=20, toc=214032, reserved1=31, af2=0.0, af1=-2.561e-09, af0=-0.002922416199, crs=431.96875, deltaN=-3.697e-09, m0=0.513025187887, cuc=5.2100047e-05, cus=-2.902001e-06, e=0.389618253917, sqrtA=5117.375812530518, toe=659664, cic=1.5087426e-05, omega0=0.921850237064, cis=-3.514811e-06, crc=-134.9375, i0=-0.475503564347, omega=-0.850359832402, omegaDot=6.9150773e-05, idot=-2.593e-09, reserved2=4277731327)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=4, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-4.191e-09, iodc=574, toc=214032, reserved1=31, af2=0.0, af1=-9.02e-10, af0=-0.040445805062, crs=255.96875, deltaN=-1.63e-09, m0=0.429373763036, cuc=-1.3738871e-05, cus=-2.108514e-06, e=0.166786856367, sqrtA=7563.125232696533, toe=659648, cic=1.5087426e-05, omega0=-0.60155615909, cis=-2.657995e-06, crc=-69.5625, i0=-0.030582666863, omega=0.993381048553, omegaDot=-0.000237895133, idot=-2.507e-09, reserved2=4269015039)>",
            "<UBX(MGA-GPS-EPH, type=1, version=0, svId=5, reserved0=0, fitInterval=0, uraIndex=0, svHealth=0, tgd=-1.1176e-08, iodc=7, toc=214032, reserved1=31, af2=0.0, af1=-2.33e-10, af0=-0.00680840062, crs=-40.03125, deltaN=3.317e-09, m0=0.52358105313, cuc=8.679926e-06, cus=-2.30968e-06, e=0.113663049648, sqrtA=1232.501514434814, toe=659680, cic=1.5087426e-05, omega0=0.031226071529, cis=-5.2364543e-05, crc=97.03125, i0=-0.6395829916, omega=-0.420688559767, omegaDot=6.9157898e-05, idot=-2.684e-09, reserved2=4281204735)>",
        ]
        for i, pld in enumerate(self.mga_gps_eph_payloads):
            res = UBXMessage("MGA", "MGA-GPS-EPH", SET, payload=pld)
            # print(res)
            self.assertEqual(str(res), EXPECTED_RESULTS[i])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
