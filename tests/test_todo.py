'''
Created on 13 Oct 2020

Just provides warning information on any payload definitions not yet implemented

@author: semuadmin
'''
import unittest
import pyubx2


class TodoTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testToDoGET(self):

        i = 0
        print("\nChecking for possible missing GET payload definitions in UBX_PAYLOADS_GET ...\n")
        for _, val in pyubx2.UBX_MSGIDS.items():
            try:
                # print(f"key {key}, val {val}")
                pyubx2.UBX_PAYLOADS_GET[val]
            except KeyError:
                i += 1
                print(f"{i} - {val}")
                continue
        print("\nCheck complete.\n")

    def testToDoSET(self):

        i = 0
        print("\nChecking for possible missing SET payload definitions in UBX_PAYLOADS_SET ...\n")
        for _, val in pyubx2.UBX_MSGIDS.items():
            try:
                # print(f"key {key}, val {val}")
                pyubx2.UBX_PAYLOADS_SET[val]
            except KeyError:
                i += 1
                print(f"{i} - {val}")
                continue
        print("\nCheck complete.\n")
        
    def testToDoPOLL(self):

        i = 0
        print("\nChecking for possible missing POLL payload definitions in UBX_PAYLOADS_POLL ...\n")
        for _, val in pyubx2.UBX_MSGIDS.items():
            try:
                # print(f"key {key}, val {val}")
                pyubx2.UBX_PAYLOADS_POLL[val]
            except KeyError:
                i += 1
                print(f"{i} - {val}")
                continue
        print("\nCheck complete.\n")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
