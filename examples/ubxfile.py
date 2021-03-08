"""
Example implementation of a UBXMessage file reader
using the UBXReader iterator functions

Created on 25 Oct 2020

@author: semuadmin
"""

from pyubx2.ubxreader import UBXReader
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

    def reader(self, validate=False, mode=0):
        """
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        """

        i = 0
        self._ubxreader = UBXReader(self._stream, validate, mode)

        for msg in self._ubxreader:  # invokes iterator method
            try:
                (raw_data, parsed_data) = msg
                #                 if raw_data:
                #                     print(raw_data)
                if parsed_data:
                    print(parsed_data)
                    i += 1
            except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
                print(f"Something went wrong {err}")
                continue

        print(f"\n\n{i} message{'' if i == 1 else 's'} read from {self._filename}.")


if __name__ == "__main__":

    print("Enter fully qualified name of file containing binary UBX data: ", end="")
    filefqn = input().strip('"')
    print("Do you want to validate the data stream (y/n)? (n) ", end="")
    val = input() or "n"
    VALD = val in ("Y", "y", "YES,", "yes", "True")
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    MODED = int(mode)

    print("Instantiating UBXStreamer class...")
    ubf = UBXStreamer(filefqn)
    print(f"Opening file {filefqn}...")
    if ubf.open():
        print("Starting file reader")
        ubf.reader(VALD, MODED)
        print("\n\nClosing file...")
        ubf.close()
        print("Test Complete")
