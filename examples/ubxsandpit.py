'''
My testing sandpit

Created on 3 Oct 2020

@author: semuadmin
'''

from sys import platform
from serial import Serial, SerialException, SerialTimeoutException

from pyubx2 import UBXMessage, SET, UBX_CONFIG_MESSAGES, UBXMessageError
import pyubx2.exceptions as ube


class UBXSandpit():
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

        for msg, val in UBX_CONFIG_MESSAGES.items():
            try:
                msgCls = msg[0:1]
                msgId = msg[1:2]
                m = UBXMessage(msgCls, msgId)
                print(msg, val, m)
            except UBXMessageError as err:
                print(f'this one didnt work {err}')
                continue

if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == 'win32':
        PORT = 'COM6'
    else:
        PORT = '/dev/tty.usbmodem14101'
    BAUDRATE = 9600
    TIMEOUT = 5
    NMEA = b'\x02\x00'
    UBX = b'\x01\x00'
    BOTH = b'\x03\x00'

    print("Instantiating UBXSandpit class...")
    ubs = UBXSandpit(PORT, BAUDRATE, TIMEOUT)
#     print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
#     ubs.connect()
#     print("Sending configuration message to receiver...")
    ubs.send_configuration(BOTH)  # NMEA, UBX or BOTH
#     print("Disconnecting from serial port...")
#     ubs.disconnect()
#     print("Test Complete")
