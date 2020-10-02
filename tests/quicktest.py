# pylint: disable=line-too-long
'''
Quick test routines

Created on 2 Oct 2020

@author: semuadmin
'''

from pyubx2 import UBXMessage

if __name__ == "__main__":

    t = UBXMessage(b'\x06', b'\x01', b'\xf0\x03\x00\x01\x01\x01\x00\x00')
    print(t)
    t = UBXMessage('CFG', 'CFG-MSG', b'\xf1\x04\x00\x01\x01\x01\x00\x00')
    print(t)
    t = UBXMessage('INF', 'INF-NOTICE', 'Now is the time for all good men to come to the aid of the party')
    print(t)
    t = UBXMessage.parse(b'\xb5\x62\x05\x01\x02\x00\x06\x01\x0f\x38', False)
    print(t)
    t = UBXMessage.parse(b'\xb5\x62\x04\x02\x02\x00\x06\x01\x0f\x38', True)  # should produce UBXParseError
