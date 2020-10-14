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

    def testTodo(self):

        i = 0
        print("\nChecking for missing GET payload definitions in UBX_PAYLOADS_GET ...\n")
        for _, val in pyubx2.UBX_MSGIDS.items():
            if val[0:3] != 'CFG':
                try:
                    # print(f"key {key}, val {val}")
                    pyubx2.UBX_PAYLOADS_GET[val]
                except KeyError:
                    i += 1
                    print(f"{i} Check if {val} needs to be added to UBX_PAYLOADS_GET")
                    continue
        print("\nCheck complete.\n")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
