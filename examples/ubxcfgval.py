"""
Example implementation of UBX Gen 9 Configuration Interface
using CFG-VALSET, CFG-VALDEL and CFG-VALGET messages.

Connects to the receiver's serial port and sets up a
threaded UBXReader process. With the reader process running
in the background, it sends CFG-VALSET and CFG-VALDEL
configuration messages to set the UART1/2 baud rates in 
the BBR memory layer, and uses CFG-VALGET to poll the before and 
after results.

NB: This example will only work on Generation 9 or later devices
(e.g. NEO-9M). You'll get a series of ACK-NAK responses on earlier
devices. It also assumes you're connected via USB rather than UART1/2.

Created on 5 Dec 2020

@author: semuadmin
"""

from sys import platform
from io import BufferedReader
from threading import Thread
from time import sleep

from pyubx2 import UBXMessage, UBXReader, VALCKSUM
from serial import Serial, SerialException, SerialTimeoutException

import pyubx2.exceptions as ube


class UBXStreamer:
    """
    UBXStreamer class.
    """

    def __init__(self, port, baudrate, timeout=5):
        """
        Constructor.
        """

        self._serial_object = None
        self._serial_thread = None
        self._ubxreader = None
        self._connected = False
        self._reading = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def __del__(self):
        """
        Destructor.
        """

        self.stop_read_thread()
        self.disconnect()

    def connect(self):
        """
        Open serial connection.
        """

        try:
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )
            self._ubxreader = UBXReader(BufferedReader(self._serial_object), validate=VALCKSUM)
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

    def start_read_thread(self):
        """
        Start the serial reader thread.
        """

        if self._connected:
            self._reading = True
            self._serial_thread = Thread(target=self._read_thread, daemon=True)
            self._serial_thread.start()

    def stop_read_thread(self):
        """
        Stop the serial reader thread.
        """

        if self._serial_thread is not None:
            self._reading = False

    def send(self, data):
        """
        Send data to serial connection.
        """

        self._serial_object.write(data)

    def flush(self):
        """
        Flush input buffer
        """

        self._serial_object.reset_input_buffer()

    def waiting(self):
        """
        Check if any messages remaining in the input buffer
        """

        return self._serial_object.in_waiting

    def _read_thread(self):
        """
        THREADED PROCESS
        Reads and parses UBX message data from stream
        """

        while self._reading and self._serial_object:
            if self._serial_object.in_waiting:
                try:
                    (_, parsed_data) = self._ubxreader.read()
                    if parsed_data:
                        print(parsed_data)
                except (
                    ube.UBXStreamError,
                    ube.UBXMessageError,
                    ube.UBXTypeError,
                    ube.UBXParseError,
                ) as err:
                    print(f"Something went wrong {err}")
                    continue

    def poll_uart(self, layer=0):
        """
        Poll the current BBR UART1/2 configuration
        """

        position = 0
        keys = ["CFG_UART1_BAUDRATE", "CFG_UART2_BAUDRATE"]
        msg = UBXMessage.config_poll(layer, position, keys)
        ubp.send(msg.serialize())

    def set_uart(self, layers=1):
        """
        Set the current BBR UART1/2 configuration
        """

        transaction = 0
        cfgData = [("CFG_UART1_BAUDRATE", 115200), ("CFG_UART2_BAUDRATE", 57600)]
        msg = UBXMessage.config_set(layers, transaction, cfgData)
        ubp.send(msg.serialize())

    def unset_uart(self, layers=1):
        """
        Unset (del) the current BBR UART1/2 configuration
        """

        transaction = 0
        keys = ["CFG_UART1_BAUDRATE", "CFG_UART2_BAUDRATE"]
        msg = UBXMessage.config_del(layers, transaction, keys)
        ubp.send(msg.serialize())


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == "win32":
        PORT = "COM6"
    else:
        PORT = "/dev/tty.usbmodem14101"
    BAUDRATE = 38400
    TIMEOUT = 1
    NMEA = 0
    UBX = 1
    BOTH = 2

    print("Instantiating UBXStreamer class...")
    ubp = UBXStreamer(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubp.connect()
    print("Starting reader thread...")
    ubp.start_read_thread()

    print("\nPolling UART configuration in the volatile RAM memory layer via CFG-VALGET...")
    print("(This should result in ACK-ACK and CFG-VALGET responses)")
    ubp.poll_uart(0)
    sleep(2)
    print("\nPolling UART configuration in the BBR memory layer via CFG-VALGET...")
    print("(This should result in an ACK-NAK response in the absence of an existing BBR configuration setting)")
    ubp.poll_uart(1)
    sleep(2)
    print("\nSetting UART configuration in the BBR memory layer via CFG-VALSET...")
    print("(This should result in an ACK-ACK response)")
    ubp.set_uart(2)
    sleep(2)
    print("\nPolling UART configuration in the BBR memory layer via CFG-VALGET...")
    print("(This should result in ACK-ACK and CFG-VALGET responses)")
    ubp.poll_uart(1)
    sleep(2)
    print("\nUnsetting UART configuration in the BBR memory layer via CFG-VALDEL...")
    print("(This should result in an ACK-ACK response)")
    ubp.unset_uart(2)
    sleep(2)
    print("\nPolling UART configuration in the BBR memory layer via CFG-VALGET...")
    print("(This should result in an ACK-NAK response as the BBR configuration setting has now been removed)")
    ubp.poll_uart(1)
    sleep(2)
    print("\nPolling UART configuration in the volatile RAM memory layer via CFG-VALGET...")
    print("(This should result in ACK-ACK and CFG-VALGET responses)")
    ubp.poll_uart(0)
    sleep(5)

    print("\n\nStopping reader thread...\n\n")
    ubp.stop_read_thread()
    print("Disconnecting from serial port...")
    ubp.disconnect()
    print("Test Complete")
