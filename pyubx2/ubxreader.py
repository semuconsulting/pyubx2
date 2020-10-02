'''
UBXReader class. 

Reads and parses individual UBX messages from any stream which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data (as a UBXMessage object).

Created on 2 Oct 2020

@author: semuadmin
'''

from pyubx2.ubxmessage import UBXMessage
import pyubx2.ubxtypes_core as ubt


class UBXReader():
    '''
    UBXReader class.
    '''

    def __init__(self, stream):
        '''
        Constructor.
        '''

        self._stream = stream

    def read(self) -> (bytes, UBXMessage):

        '''
        Read the binary data from the serial buffer.
        '''

        stm = self._stream
        reading = True
        raw_data = None
        parsed_data = None
        byte1 = stm.read(1)  # read the first byte

        while reading:
            if byte1 == ubt.UBX_HDR[0:1]:  # could be a UBX message
                byte2 = stm.read(1)
                if byte2 == ubt.UBX_HDR[1:2]:  # definitely a UBX message
                    byten = stm.read(4)
                    clsid = byten[0:1]
                    msgid = byten[1:2]
                    lenb = byten[2:4]
                    leni = int.from_bytes(lenb, 'little', signed=False)
                    byten = stm.read(leni + 2)
                    plb = byten[0:leni]
                    cksum = byten[leni:leni + 2]
                    raw_data = ubt.UBX_HDR + clsid + msgid + lenb + plb + cksum
                    parsed_data = UBXMessage.parse(raw_data)
                else:
                    reading = False
            else:
                reading = False

        return (raw_data, parsed_data)
