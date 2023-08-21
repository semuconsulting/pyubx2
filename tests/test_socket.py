"""
Socket reader tests for pyubx2 - uses dummy socket class
to achieve 99% test coverage of SocketStream.

Created on 11 May 2022

*** NB: must be saved in UTF-8 format ***

:author: semuadmin
"""

import unittest
from socket import socket
from pyubx2 import UBXReader, UBXMessage, POLL


class DummySocket(socket):
    """
    Dummy socket class which simulates recv() and send() methods
    and TimeoutError.
    """

    def __init__(self, *args, **kwargs):
        self._timeout = False
        if "timeout" in kwargs:
            self._timeout = kwargs["timeout"]
            kwargs.pop("timeout")

        super().__init__(*args, **kwargs)

        pool = (
            b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d"
            + b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51"
            + b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c"
            + b"$GNDTM,W84,,0.0,N,0.0,E,0.0,W84*71\r\n"
            + b"$GNRMC,103607.00,A,5327.03942,N,10214.42462,W,0.046,,060321,,,A,V*0E\r\n"
            + b"$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73\r\n"
            + b"\xD3\x00\x13\x3E\xD7\xD3\x02\x02\x98\x0E\xDE\xEF\x34\xB4\xBD\x62\xAC\x09\x41\x98\x6F\x33\x36\x0B\x98"
            + b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
            + b"\xd3\x00\x12B\x91\x81\xc9\x84\x00\x04B\xb8\x88\x008\x80\t\xd0F\x00(\xf0kf"
        )
        self._stream = pool * round(4096 / len(pool))
        self._buffer = self._stream

    def recv(self, num: int) -> bytes:
        if self._timeout:
            raise TimeoutError
        if len(self._buffer) < num:
            self._buffer = self._buffer + self._stream
        buff = self._buffer[:num]
        self._buffer = self._buffer[num:]
        return buff

    def send(self, data: bytes):
        if self._timeout:
            raise TimeoutError
        return None


class SocketTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    # *******************************************
    # Helper methods
    # *******************************************

    def testSocketStub(self):
        EXPECTED_RESULTS = (
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_NAVSPG_USRDAT_ROTY=1.2339999675750732)>",
            "<UBX(ESF-MEAS, timeTag=514157, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1741, dataType_01=14, dataField_02=16776932, dataType_02=13, dataField_03=16775683, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514157, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514162, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776523, dataType_01=16, dataField_02=576, dataType_02=17, dataField_03=10275, dataType_03=18, dataField_04=514162, dataType_04=0)>",
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, active=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
            "<RTCM(1005, DF002=1005, DF003=2003, DF021=0, DF022=1, DF023=0, DF024=0, DF141=0, DF025=1114104.5999, DF142=0, DF001_1=0, DF026=-4850729.7108000005, DF364=0, DF027=3975521.4643)>",
            "<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.802800001, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>",
            "<RTCM(1065, DF002=1065, DF386=12345, DF391=3, DF388=0, DF413=1, DF414=1, DF415=1, DF387=2, DF384_01=23, DF379_01=2, DF381_01_01=4, DF383_01_01=0.07, DF381_01_02=2, DF383_01_02=0.09, DF384_02=26, DF379_02=1, DF381_02_01=3, DF383_02_01=0.05)>",
            "<UBX(CFG-VALGET, version=0, layer=0, position=0, CFG_NAVSPG_USRDAT_ROTY=1.2339999675750732)>",
            "<UBX(ESF-MEAS, timeTag=514157, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=4, id=0, dataField_01=1741, dataType_01=14, dataField_02=16776932, dataType_02=13, dataField_03=16775683, dataType_03=5, dataField_04=2825, dataType_04=12, dataField_05=514157, dataType_05=0)>",
            "<UBX(ESF-MEAS, timeTag=514162, timeMarkSent=0, timeMarkEdge=0, calibTtagValid=1, numMeas=3, id=0, dataField_01=16776523, dataType_01=16, dataField_02=576, dataType_02=17, dataField_03=10275, dataType_03=18, dataField_04=514162, dataType_04=0)>",
        )
        raw = None
        stream = DummySocket()
        ubr = UBXReader(stream, bufsize=1024, protfilter=7)
        buff = ubr._stream.buffer  # test buffer getter method
        i = 0
        for raw, parsed in ubr:
            if raw is not None:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
                if i >= 12:
                    break
        self.assertEqual(i, 12)

    def testSocketSend(self):
        stream = DummySocket()
        ubr = UBXReader(stream, bufsize=1024, protfilter=7)
        msg = UBXMessage("CFG", "CFG-PRT", POLL)
        res = ubr.datastream.write(msg.serialize())
        self.assertEqual(res, None)

    def testSocketIter(self):  # test for extended stream
        raw = None
        stream = DummySocket()
        ubr = UBXReader(stream)
        i = 0
        for raw, parsed in ubr:
            if raw is None:
                raise EOFError
            i += 1
            if i >= 123:
                break
        self.assertEqual(i, 123)

    def testSocketError(self):  # test for simulated socket timeout
        raw = None
        stream = DummySocket(timeout=True)
        ubr = UBXReader(stream)
        i = 0
        for raw, parsed in ubr:
            i += 1
            if i >= 12:
                break
        self.assertEqual(i, 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
