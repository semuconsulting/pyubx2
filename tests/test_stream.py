'''
Created on 3 Oct 2020

Stream method tests for pyubx2.UBXReader

@author: semuadmin
'''

import sys
import unittest

import pyubx2
from serial import Serial

if sys.platform == "win32":
    PORT = 'COM6'
else:
    PORT = '/dev/tty.usbmodem14101'

class StreamTest(unittest.TestCase):

    def setUp(self):
        pass
#         self.port = PORT
#         self.baudrate = 9600
#         self.timeout = 5
#         self.serial_object = Serial(self.port, self.baudrate, timeout=self.timeout)
#         self.serial_object.open()

    def tearDown(self):
        pass
#         self.serial_object.close()
#         self.serial_object = None

    def testStream(self):
        pass  # TODO


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
