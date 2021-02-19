"""
Simple command line utility to stream the parsed UBX output of a u-blox GNSS device.

Usage (all args are optional):
ubxdump.py port="COM8" baud=9600 timeout=5 validate=0 raw=0

If validate=True (1), streaming will terminate on any non-UBX data (e.g. NMEA).
"""

import sys
from serial import Serial
from pyubx2 import UBXReader


def stream_ubx(**kwargs):
    """
    Stream output
    """

    try:
        port = kwargs.get("port", "COM8").strip('"')
        baud = int(kwargs.get("baud", 9600))
        timeout = int(kwargs.get("timeout", 5))
        validate = int(kwargs.get("validate", 0))
        rawformat = int(kwargs.get("raw", 0))
        print(f"\nStreaming from {port} at {baud} baud in",
              f"{'raw' if rawformat else 'parsed'} format...\n")
        stream = Serial(port, baud, timeout=timeout)
        ubr = UBXReader(stream, validate)
        for (raw, parsed) in ubr:
            if rawformat:
                print(raw)
            else:
                print(parsed)
    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " ubxdump.py is a simple command line utility to stream",
                "the parsed UBX output of a u-blox GNSS device.\n\n",
                "Usage (all args are optional): ubxdump.py",
                "port=\"COM8\" baud=9600 timeout=5",
                "validate=0 raw=0\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_ubx(**dict(arg.split("=") for arg in sys.argv[1:]))
