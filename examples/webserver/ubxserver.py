"""
ubxserver.py

This example illustrates a simple HTTP wrapper around pyubx2.UBXReader.

It displays selected GPS data from NAV-PVT, NAV-POSLLH, NAV-DOP and NAV-SAT
messages on a dynamically updated web page using the native Python 3 http.server
library and a RESTful API implemented by the pyubx2 streaming and parsing service.

NB: Must be executed from the root folder i.e. /examples/webserver/:

> python3 ubxserver.py

Press CTRL-C to terminate.

The web page can be accessed at http://localhost:8080. The parsed
data can also be accessed directly via the REST API http://localhost:8080/gps.

Created on 17 May 2021

:author: semuadmin
:license: (c) SEMU Consulting 2021 - BSD 3-Clause License
"""
# pylint: disable=invalid-name

from sys import platform
from io import BufferedReader
from threading import Thread, Event
from time import sleep
import json
from serial import Serial, SerialException, SerialTimeoutException
from pyubx2 import UBXMessage, UBXReader, GET, UBX_PROTOCOL
import pyubx2.exceptions as ube
from gpshttpserver import GPSHTTPServer, GPSHTTPHandler


class UBXServer:
    """
    UBXServer class.
    """

    def __init__(self, port, baudrate, timeout, validate=1):
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
        self._validate = validate
        self._stopevent = Event()
        self.gpsdata = {
            "date": "1900-01-01",
            "time": "00.00.00",
            "latitude": 0.0,
            "longitude": 0.0,
            "elevation": 0.0,
            "speed": 0.0,
            "track": 0.0,
            "siv": 0,
            "pdop": 99,
            "hdop": 99,
            "vdop": 99,
            "fix": 0,
        }

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

        self._connected = False
        try:
            print(f"Connecting to serial port {self._port} at {self._baudrate} baud...")
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )
            self._ubxreader = UBXReader(
                BufferedReader(self._serial_object),
                protfilter=UBX_PROTOCOL,
                validate=self._validate,
                msgmode=GET,
            )
            self._connected = True
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

        return self._connected

    def disconnect(self):
        """
        Close serial connection.
        """

        if self._connected and self._serial_object:
            print("Disconnecting from serial port...")
            try:
                self._serial_object.close()
            except (SerialException, SerialTimeoutException) as err:
                print(f"Error disconnecting from serial port {err}")
        self._connected = False

        return self._connected

    def start_read_thread(self):
        """
        Start the serial reader thread.
        """

        if self._connected:
            print("\nStarting serial read thread...")
            self._reading = True
            self._serial_thread = Thread(
                target=self._read_thread, args=(self._stopevent,)
            )
            self._serial_thread.start()

    def stop_read_thread(self):
        """
        Stop the serial reader thread.
        """

        if self._serial_thread is not None:
            self._stopevent.set()
            self._serial_thread.join()
            print("\nSerial read thread stopped")

    def _read_thread(self, stopevent):
        """
        THREADED PROCESS
        Reads and parses UBX message data from stream
        """
        # pylint: disable=unused-variable

        while not stopevent.is_set():
            if self._serial_object.in_waiting:
                try:
                    (raw_data, parsed_data) = self._ubxreader.read()
                    if isinstance(parsed_data, UBXMessage):
                        self.set_data(parsed_data)
                except (
                    ube.UBXStreamError,
                    ube.UBXMessageError,
                    ube.UBXTypeError,
                    ube.UBXParseError,
                ) as err:
                    print(f"Something went wrong {err}")
                    continue

    def set_data(self, parsed_data):
        """
        Set GPS data dictionary from UBX sentences.
        """

        try:
            if parsed_data.identity == "NAV-PVT":
                self.gpsdata[
                    "date"
                ] = f"{parsed_data.day:02}/{parsed_data.month:02}/{parsed_data.year}"
                self.gpsdata[
                    "time"
                ] = f"{parsed_data.hour:02}:{parsed_data.min:02}:{parsed_data.second:02}"
                self.gpsdata["latitude"] = parsed_data.lat
                self.gpsdata["longitude"] = parsed_data.lon
                self.gpsdata["elevation"] = parsed_data.height / 1000
                self.gpsdata["speed"] = parsed_data.gSpeed
                self.gpsdata["track"] = parsed_data.headVeh
                self.gpsdata["fix"] = parsed_data.fixType
                self.gpsdata["pDOP"] = parsed_data.pDOP
            if parsed_data.identity == "NAV-POSLLH":
                self.gpsdata["latitude"] = parsed_data.lat
                self.gpsdata["longitude"] = parsed_data.lon
                self.gpsdata["elevation"] = parsed_data.height / 1000
            if parsed_data.identity == "NAV-DOP":
                self.gpsdata["pdop"] = parsed_data.pDOP
                self.gpsdata["hdop"] = parsed_data.hDOP
                self.gpsdata["vdop"] = parsed_data.vDOP
            if parsed_data.identity == "NAV-SAT":
                self.gpsdata["siv"] = parsed_data.numSvs
        except ube.UBXMessageError as err:
            print(err)
            self._stopevent.set()

    def get_data(self):
        """
        Return GPS data in JSON format.

        This is used by the REST API /gps implemented in the
        GPSHTTPServer class.
        """

        return json.dumps(self.gpsdata)


if __name__ == "__main__":

    ADDRESS = "localhost"
    TCPPORT = 8080

    # set port, baudrate and timeout to suit your device configuration
    if platform == "win32":  # Windows
        prt = "COM13"
    elif platform == "darwin":  # MacOS
        prt = "/dev/cu.usbmodem14101"
    else:  # Linux
        prt = "/dev/ttyACM1"
    baud = 9600
    tmout = 0.1

    ubs = UBXServer(prt, baud, tmout)
    httpd = GPSHTTPServer((ADDRESS, TCPPORT), GPSHTTPHandler, ubs)

    if ubs.connect():
        ubs.start_read_thread()
        print(
            "\nStarting HTTP Server on http://"
            + ADDRESS
            + ":"
            + str(TCPPORT)
            + " ...\nPress Ctrl-C to terminate.\n"
        )
        httpd_thread = Thread(target=httpd.serve_forever, daemon=True)
        httpd_thread.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n\nTerminated by user\n\n")

        ubs.stop_read_thread()
        httpd.shutdown()
        print("\nHTTP Server stopped.")
        sleep(2)  # wait for shutdown
        ubs.disconnect()
        print("\nProcessing Complete")
