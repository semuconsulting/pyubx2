"""
Example implementation of a simple UBX receiver configuration utility

This example sets the message rate for all UBX-NAV message types
- these are the ones that provide principal navigation data -
to '0' (off) or '1' (on, i.e. one message per navigation solution) on
the receiver's UART and USB ports.

**NOTE:**

1.  Some UBX-NAV message combinations are unsupported or mutually
    exclusive (e.g. NAV-POSLLH & NAV-POSECEF on some NEO-6 receivers),
    so you won't necessarily receive each and every type on the input stream.

2.  The configuration set here is volatile and will be reset after a receiver
    power cycle or CFG-RST. To make the configuration permanent, you'd need to
    send a CFG-CFG message - **caveat emptor**.

3.  In a production implementation, it may be prudent to check for an
    explicit acknowledgement (ACK-ACK message) to each configuration message.

Created on 3 Oct 2020

@author: semuadmin
"""

from sys import platform
from time import sleep
from serial import Serial, SerialException, SerialTimeoutException

from pyubx2 import UBXMessage, SET, UBX_CONFIG_MESSAGES
import pyubx2.exceptions as ube


class UBXSetter:
    """
    UBXSetter class.
    """

    def __init__(self, port, baudrate, timeout=5):
        """
        Constructor.
        """

        self._serial_object = None
        self._connected = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def connect(self):
        """
        Open serial connection.
        """

        try:
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )
            self._connected = True
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

    def disconnect(self):
        """
        Close serial connection.
        """

        if self._connected and self._serial_object:
            try:
                self._serial_object.close()
            except (SerialException, SerialTimeoutException) as err:
                print(f"Error disconnecting from serial port {err}")
        self._connected = False

    def _send(self, data):
        """
        Send data to serial connection.
        """

        self._serial_object.write(data)

    def send_configuration(self, config):
        """
        Creates a series of CFG-MSG configuration messages and
        sends them to the receiver.
        """

        try:

            msgs = []

            # compile all the UBX-NAV config message types
            for key, val in UBX_CONFIG_MESSAGES.items():
                if val[0:3] == "NAV":
                    msgs.append(key)

            # send each UBX-NAV config message in turn
            for msgtype in msgs:
                payload = msgtype + config
                msg = UBXMessage("CFG", "CFG-MSG", SET, payload=payload)
                print(f"Sending {msg}")
                self._send(msg.serialize())
                sleep(1)

        except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
            print(f"Something went wrong {err}")


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == "win32":
        PORT = "COM7"
    else:
        PORT = "/dev/tty.usbmodem14101"
    BAUDRATE = 9600
    TIMEOUT = 5

    # each of 6 config bytes corresponds to a receiver port
    # the UART and USB ports are bytes 2, 3 and 4
    ON = b"\x01\x01\x01\x01\x01\x00"
    OFF = b"\x00\x00\x00\x00\x00\x00"

    print("Instantiating UBXSetter class...")
    ubs = UBXSetter(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubs.connect()
    print("Sending configuration messages to receiver...")
    ubs.send_configuration(ON)
    print("Disconnecting from serial port...")
    ubs.disconnect()
    print("Test Complete")
