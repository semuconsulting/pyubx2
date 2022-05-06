"""
ubxsocket.py

A very simple example implementation of a 
GNSS socket reader using the UBXReader iterator
functions. Parses UBX, NMEA and RTCM3 messages.

Designed to be used in conjunction with the 
tcpserver_thread.py test harness, but can be
used with any accessible open TCP socket.

Created on 05 May 2022

@author: semuadmin
"""

import socket
from pyubx2.ubxreader import UBXReader


def read(stream: socket.socket):
    """
    Reads and parses UBX, NMEA and RTCM3 message data from stream.
    """

    msgcount = 0

    ubr = UBXReader(
        stream,
        protfilter=7,
    )
    for (_, parsed_data) in ubr.iterate():
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":

    SERVER = "localhost"
    PORT = 50007

    print(f"Opening socket {SERVER}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        read(sock)
    print("Test Complete")
