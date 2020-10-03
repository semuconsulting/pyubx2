'''
Example implementation of a threaded UBXMessage streamer

Created on 2 Oct 2020

@author: semuadmin
'''

from io import BufferedReader
from threading import Thread
from time import sleep

from serial import Serial, SerialException, SerialTimeoutException
from pyubx2.ubxreader import UBXReader
import pyubx2.exceptions as ube


class UBXStreamer():
    '''
    UBXStreamer class.
    '''

    def __init__(self, port, baudrate, timeout=5):
        '''
        Constructor.
        '''

        self._serial_object = None
        self._serial_thread = None
        self._ubxreader = None
        self._connected = False
        self._reading = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def __del__(self):
        '''
        Destructor.
        '''

        self.stop_read_thread()
        self.disconnect()

    def connect(self):
        '''
        Open serial connection.
        '''

        try:
            self._serial_object = Serial(self._port,
                                         self._baudrate,
                                         timeout=self._timeout)
            self._ubxreader = UBXReader(BufferedReader(self._serial_object))
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

    def start_read_thread(self):
        '''
        Start the serial reader thread.
        '''

        if self._connected:
            self._reading = True
            self._serial_thread = Thread(target=self._read_thread, daemon=False)
            self._serial_thread.start()

    def stop_read_thread(self):
        '''
        Stop the serial reader thread.
        '''

        if self._serial_thread is not None:
            self._reading = False
            self._serial_thread.join()

    def _read_thread(self):
        '''
        THREADED PROCESS
        Reads and parses UBX message data from stream
        '''

        while self._reading and self._serial_object:
            if self._serial_object.in_waiting:
                try:
                    (raw_data, parsed_data) = self._ubxreader.read()
                    if raw_data:
                        print(raw_data)
                    if parsed_data:
                        print(parsed_data)
                except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
                    print(f"Something went wrong {err}")
                    continue


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
#     PORT = 'COM6'
    PORT = '/dev/tty.usbmodem14101'
    BAUDRATE = 9600
    TIMEOUT = 1
    RUNTIME = 60

    print("Instantiating UBXStreamer class...")
    ubp = UBXStreamer(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubp.connect()
    print(f"Starting reader thread, which will run for {RUNTIME} seconds...\n\n")
    ubp.start_read_thread()
    sleep(RUNTIME)  # do other stuff; reader thread will continue in background
    print("\n\nStopping reader thread...")
    ubp.stop_read_thread()
    print("Disconnecting from serial port...")
    ubp.disconnect()
    print("Test Complete")
