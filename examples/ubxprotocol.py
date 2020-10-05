'''
Example implementation of a simple UBX receiver configuration utility

This example sets the protocol(s) which will transmitted on the
receiver's USB port (port 0x03) to NMEA, UBX or both

**NOTE:**

1.  The configuration set here is volatile and will be reset after a receiver
    power cycle or CFG-RST. To make the configuration permanent, you'd need to
    send a CFG-CFG message - **caveat emptor!**.

Created on 3 Oct 2020

@author: semuadmin
'''

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

    def send_configuration(self, protocol):
        '''
        Creates a CFG-PRT configuration message and
        sends them to the receiver.
        '''
    
        try:

            if protocol == NMEAONLY:  # turn on just the NMEA protocol
                config = b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x02\x00\x00\x00\x00\x00'
            elif protocol == UBXONLY:  # turn on just the UBX protocol
                config = b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x01\x00\x00\x00\x00\x00'
            else:  # turn on both NMEA and UBX protocols
                config = b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x03\x00\x00\x00\x00\x00'

            msg = UBXMessage('CFG', 'CFG-PRT', config, SET)
            print(f"Sending {msg}")
            self._send(msg.serialize())

        except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
            print(f"Something went wrong {err}")


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
#     PORT = 'COM6'
    PORT = '/dev/tty.usbmodem14101'
    BAUDRATE = 9600
    TIMEOUT = 5
    NMEAONLY = 0
    UBXONLY = 1
    BOTH = 2

    print("Instantiating UBXConfig class...")
    ubs = UBXSetter(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubs.connect()
    print("Sending configuration messages to receiver...")
    ubs.send_configuration(BOTH)
    print("Disconnecting from serial port...")
    ubs.disconnect()
    print("Test Complete")
