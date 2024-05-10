"""
ubxsocket.py

A simple example implementation of a GNSS socket reader
using the pyubx2.UBXReader iterator functions.
Parses UBX, NMEA and RTCM3 messages.

Usage:

python3 ubxsocket.py ipaddress=127.0.0.1 ipport=50012

Designed to be used in conjunction with the
tcpserver_thread.py test harness, but can be
used with any accessible open TCP socket.

Created on 05 May 2022

@author: semuadmin
"""

import socket
from datetime import datetime
from sys import argv

from pyubx2.ubxreader import (
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
    UBX_PROTOCOL,
    VALCKSUM,
    UBXReader,
)


def main(**kwargs):
    """
    Reads and parses UBX, NMEA and RTCM3 message data from stream.
    """

    ipaddress = kwargs.get("ipaddress", "localhost")
    ipport = kwargs.get("ipport", 50012)

    print(f"Opening socket {ipaddress}:{ipport}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
        stream.connect((ipaddress, ipport))

        count = 0
        start = datetime.now()

        ubr = UBXReader(
            stream,
            protfilter=UBX_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL,
            validate=VALCKSUM,
        )
        try:
            for _, parsed_data in ubr:
                print(parsed_data)
                count += 1
        except KeyboardInterrupt:
            dur = datetime.now() - start
            secs = dur.seconds + dur.microseconds / 1e6
            print("Session terminated by user")
            print(
                f"{count:,d} messages read in {secs:.2f} seconds:",
                f"{count/secs:.2f} msgs per second",
            )


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
