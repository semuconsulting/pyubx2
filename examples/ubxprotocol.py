'''
Example implementation of a simple UBX receiver configuration utility

This example sets the protocol(s) which will transmitted on the
receiver's USB port to NMEA, UBX or both

**NOTE:**

1.  The configuration set here is volatile and will be reset after a receiver
    power cycle or CFG-RST. To make the configuration permanent, you'd need to
    send a CFG-CFG message - **caveat emptor**.

Created on 3 Oct 2020

@author: semuadmin
'''

from sys import platform
from serial import Serial, SerialException, SerialTimeoutException

from pyubx2 import UBXMessage, SET
import pyubx2.exceptions as ube


class UBXSetter():
    '''
    UBXSetter class.
    '''

    def __init__(self, port, baudrate, timeout=5):
        '''
        Constructor.
        '''

        self._serial_object = None
        self._connected = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def connect(self):
        '''
        Open serial connection.
        '''

        try:
            self._serial_object = Serial(self._port,
                                         self._baudrate,
                                         timeout=self._timeout)
            self._connected = True
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

    def disconnect(self):
        '''
        Close serial connection.
        '''

        if self._connected and self._serial_object:
            try:
                self._serial_object.close()
            except (SerialException, SerialTimeoutException) as err:
                print(f"Error disconnecting from serial port {err}")
        self._connected = False

    def _send(self, data):
        '''
        Send data to serial connection.
        '''

        self._serial_object.write(data)

    def send_configuration(self, outProtoMask):
        '''
        Creates a CFG-PRT configuration message and
        sends it to the receiver.
        '''

        portID = b'\x03'  # USB port
        reserved0 = b'\x00'
        txReady = b'\x00\x00'
        mode = b'\x00\x00\x00\x00'  # not used for USB port
        baudRate = b'\x00\x00\x00\x00'  # not used for USB port
        inProtoMask = b'\x07\x00'  # NMEA + UBX + RTCM3
        reserved4 = b'\x00\x00'
        reserved5 = b'\x00\x00'
        payload = portID + reserved0 + txReady + mode + baudRate + inProtoMask \
                  +outProtoMask + reserved4 + reserved5

        try:
            msg = UBXMessage('CFG', 'CFG-PRT', SET, payload=payload)
            print(f"Sending {msg}")
            self._send(msg.serialize())
        except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
            print(f"Something went wrong {err}")


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == 'win32':
        PORT = 'COM7'
    else:
        PORT = '/dev/tty.usbmodem14101'
    BAUDRATE = 9600
    TIMEOUT = 5
    NMEA = b'\x02\x00'
    UBX = b'\x01\x00'
    BOTH = b'\x03\x00'

    print("Instantiating UBXConfig class...")
    ubs = UBXSetter(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubs.connect()
    print("Sending configuration message to receiver...")
    ubs.send_configuration(BOTH)  # NMEA, UBX or BOTH
    print("Disconnecting from serial port...")
    ubs.disconnect()
    print("Test Complete")
