'''
Created on 21 Oct 2020

Property tests for pyubx2.UBXMessage

@author: semuadmin
'''
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import unittest

from pyubx2 import UBXMessage, POLL


class FillTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testFill_CFGMSG(self):  # test header in bytes property
        EXPECTED_RESULT = "b'\\xb5b'"
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.header), EXPECTED_RESULT)

    def testFill_CFGMSG2(self):  # test msg_cls in bytes property
        EXPECTED_RESULT = "b'\\x06'"
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.msg_cls), EXPECTED_RESULT)

    def testFill_CFGMSG3(self):  # test msg_id in bytes property
        EXPECTED_RESULT = "b'\\x01'"
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.msg_id), EXPECTED_RESULT)

    def testFill_CFGMSG4(self):  # test msg length in bytes property
        EXPECTED_RESULT = "b'\\x02\\x00'"
        res = UBXMessage('CFG', 'CFG-MSG', POLL, msgClass=240, msgID=5)
        self.assertEqual(str(res.length), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
