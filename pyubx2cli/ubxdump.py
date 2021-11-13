"""
Simple command line utility to stream the parsed UBX output of a u-blox GNSS device.

Usage (all args are optional):
ubxdump port="/dev/ttyACM1" baud=9600 timeout=5 ubxonly=0 validate=1 output=0
   parsebitfield=1 filter=*

output: 0 = parsed, 1 = binary, 2 = hexadecimal

If ubxonly=True (1), streaming will terminate on any non-UBX data (e.g. NMEA).

For help, type:
ubxdump -h

Created on 20 Aug 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

import sys
from serial import Serial
from pyubx2 import UBXReader, GET, VALCKSUM

# Output formats
PARSED = 0
BIN = 1
HEX = 2

# Default port settings - amend as required
PORT = "/dev/ttyACM1"
BAUD = 9600
TIMEOUT = 5


def stream_ubx(**kwargs):
    """
    Stream output to terminal.

    :param int port: (kwarg)  baud rate (/dev/ttyACM1)
    :param int baud: (kwarg) baud rate (9600)
    :param int timeout: (kwarg) timeout in seconds (5)
    :param int ubxonly: (kwarg) set to True to generate error on non-UBX data (0)
    :param int validate: (kwarg) validate checksum (1)
    :param int parsebf: (kwarg) parse bitfields (1)
    :param int output: (kwarg) 0=parsed, 1=binary, 2=hexadecimal (0)
    :param int filter: (kwarg) comma-separated list of UBX message identities to display (*)
    :raises: UBXStreamError (if ubxonly flag is 1 and stream contains non-UBX data)

    """

    try:
        port = kwargs.get("port", PORT).strip('"')
        baud = int(kwargs.get("baud", BAUD))
        timeout = int(kwargs.get("timeout", TIMEOUT))
        ubxonly = int(kwargs.get("ubxonly", 0))
        validate = int(kwargs.get("validate", VALCKSUM))
        output = int(kwargs.get("output", PARSED))
        parsebf = int(kwargs.get("parsebitfield", True))
        filt = kwargs.get("filter", "*")
        filtertxt = "" if filt == "*" else f", filtered by {filt}"
        print(
            f"\nStreaming from {port} at {baud} baud in",
            f"{['parsed','binary','hexadecimal'][output]} format{filtertxt}...\n",
        )
        stream = Serial(port, baud, timeout=timeout)
        ubr = UBXReader(
            stream,
            ubxonly=ubxonly,
            validate=validate,
            msgmode=GET,
            parsebitfield=parsebf,
        )
        for (raw, parsed) in ubr:
            if filt == "*" or parsed.identity in filt:
                if output == BIN:
                    print(raw)
                elif output == HEX:
                    print(raw.hex())
                else:
                    print(parsed)
    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


def main():
    """
    CLI Entry point.

    args as per stream_ubx() method
    """

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " ubxdump is a simple command line utility to stream",
                "the parsed UBX output of a u-blox GNSS device.\n\n",
                "Usage (all args are optional): ubxdump",
                f"port={PORT} baud={BAUD} timeout={TIMEOUT}",
                "ubxonly=0 validate=1 output=0 parsebitfield=1 ",
                "filter=*\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_ubx(**dict(arg.split("=") for arg in sys.argv[1:]))


if __name__ == "__main__":

    main()
