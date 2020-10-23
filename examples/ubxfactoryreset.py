'''
Example implementation of a simple UBX receiver configuration utility

This example resets the UBX receiver to its factory defaults

Created on 10 Oct 2020

@author: semuadmin
'''

from sys import platform
from serial import Serial, SerialException, SerialTimeoutException

from pyubx2 import UBXMessage, SET
import pyubx2.exceptions as ube


class UBXFactoryReset():
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

    def send_configuration(self):
        '''
        Creates a CFG-CFG configuration message and
        sends it to the receiver.
        '''

        try:
            clearMask = b'\x07\x00\x00\x00'  # little-endian
            saveMask = b'\x00\x00\x00\x00'
            loadMask = b'\x07\x00\x00\x00'
            devicerMask = b'\x01'  # only target the battery-backed RAM
            payload = clearMask + saveMask + loadMask + devicerMask
            msg = UBXMessage('CFG', 'CFG-CFG', SET, payload=payload)
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

    print("Instantiating UBXFactoryReset class...")
    ubs = UBXFactoryReset(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubs.connect()
    print("Sending factory reset message to receiver...")
    ubs.send_configuration()
    print("Disconnecting from serial port...")
    ubs.disconnect()
    print("Test Complete")
