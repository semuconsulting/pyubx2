"""
ubxsock.py

This example illustrates a simple example implementation of a 
UBXMessage and/or NMEAMessage socket reader using the
UBXReader iterator functions and an external error handler.

Created on 05 May 2022

@author: semuadmin
"""

import socket
from pyubx2.ubxreader import UBXReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def read(stream):
    """
    Reads and parses UBX message data from stream.
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
