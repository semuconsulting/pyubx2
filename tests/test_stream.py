'''
Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

Stream method tests for pyubx2.UBXReader

@author: semuadmin
'''

import os
import unittest

import pyubx2


class StreamTest(unittest.TestCase):

    def setUp(self):
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, 'ubxlog.bin')
        self.stream = open(filepath, 'rb')

    def tearDown(self):
        self.stream.close()

    def testStream(self):
        ubxreader = pyubx2.UBXReader(self.stream)
        (raw, parsed) = ubxreader.read()
        self.assertEqual(raw, b'\xb5b\x01\x064\x00(\xf5M\x17\xa8B\xfb\xffN\x08\x03\xdd\x10\xe9\xab\x16\xfc\xf6\x1c\xffj\xeff\x1e\xba\x08\x00\x00"\x00\x00\x00\x1f\x00\x00\x00\xe3\xff\xff\xfft\x00\x00\x00\xf5\x00\x03\x05\x84\xd3\x01\x00&k')
        self.assertEqual(str(parsed), "<UBX(NAV-SOL, iTOW=12:36:09, fTOW=-310616, week=2126, gpsFix=3, flags=b'\\xdd', ecefX=380365072, ecefY=-14878980, ecefZ=510062442, pAcc=2234, ecefVX=34, ecefVY=31, ecefVZ=-29, sAcc=116, pDOP=245, reserved1=3, numSV=5, reserved2=119684)>")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
