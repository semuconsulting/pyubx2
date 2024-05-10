"""
ubxfile.py

Usage:

python3 ubxfile.pyh filename=pygpsdata.log

This example illustrates a simple example implementation of a 
UBXMessage and/or NMEAMessage binary logfile reader using the
UBXReader iterator functions and an external error handler.

Created on 25 Oct 2020

@author: semuadmin
"""

from sys import argv

from pyubx2.ubxreader import (
    ERR_LOG,
    GET,
    UBX_PROTOCOL,
    VALCKSUM,
    UBXReader,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
)


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def main(**kwargs):
    """
    Main Routine.
    """

    filename = kwargs.get("filename", "pygpsdata.log")

    print(f"Opening file {filename}...")
    with open(filename, "rb") as stream:

        count = 0

        ubr = UBXReader(
            stream,
            protfilter=UBX_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL,
            quitonerror=ERR_LOG,
            validate=VALCKSUM,
            msgmode=GET,
            parsebitfield=True,
            errorhandler=errhandler,
        )
        for _, parsed_data in ubr:
            print(parsed_data)
            count += 1

    print(f"\n{count} messages read.\n")
    print("Test Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
