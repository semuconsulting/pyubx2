"""
Example implementation of a UBXMessage file reader
using the UBXReader iterator functions

Created on 25 Oct 2020

@author: semuadmin
"""

from pyubx2.ubxreader import UBXReader, VALCKSUM
from pyubx2 import GET
import pyubx2.exceptions as ube


class UBXStreamer:
    """
    UBXStreamer class.
    """

    def __init__(self, filename):
        """
        Constructor.
        """

        self._filename = filename
        self._stream = None
        self._ubxreader = None
        self._connected = False
        self._reading = False
        self._count = 0

    def __del__(self):
        """
        Destructor.
        """

        self.close()

    def open(self):
        """
        Open file.
        """

        self._connected = False
        try:
            self._stream = open(self._filename, "rb")
            self._connected = True
        except Exception as err:
            print(f"Error opening file {err}")

        return self._connected

    def close(self):
        """
        Close file.
        """

        if self._connected and self._stream:
            try:
                self._stream.close()
            except Exception as err:
                print(f"Error closing file {err}")
        self._connected = False

        return self._connected

    def reader(self, ubx_only=False, validate=VALCKSUM, msgmode=GET):
        """
        Reads and parses NMEA message data from stream.
        """

        ubr = UBXReader(
            self._stream,
            ubxonly=ubx_only,
            validate=vald,
            msgmode=msgmode,
            parsebitfield=True,
        )
        for (raw_data, parsed_data) in ubr.iterate(quityonerror=False):
            print(parsed_data)
            self._count += 1

        print(
            f"\n\n{self._count} message{'' if self._count == 1 else 's'} read from {self._filename}."
        )


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")
    vald = 0

    print("Enter fully qualified name of file containing binary UBX data: ", end="")
    filefqn = input().strip('"')
    print("Do you want to ignore any non-UBX data (y/n)? (y) ", end="")
    val = input() or "y"
    ubxonly = val in NO
    print("Do you want to validate the message checksums (y/n)? (y) ", end="")
    val = input() or "y"
    if val in YES:
        vald = VALCKSUM
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    moded = int(mode)

    print("Instantiating UBXStreamer class...")
    ubf = UBXStreamer(filefqn)
    print(f"Opening file {filefqn}...")
    if ubf.open():
        print("Starting file reader")
        ubf.reader(vald, moded)
        print("\n\nClosing file...")
        ubf.close()
        print("Test Complete")
