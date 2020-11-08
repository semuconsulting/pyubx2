"""
UBXReader class.

Reads and parses individual UBX messages from any stream which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data (as a UBXMessage object).

If the 'validate' parameter is set to 'True', the reader will raise a UBXStreamerError if
it encounters any non-UBX data. Otherwise, it will ignore the non-UBX data and attempt
to carry on.

Created on 2 Oct 2020

@author: semuadmin
"""

from pyubx2.ubxmessage import UBXMessage
from pyubx2.exceptions import UBXStreamError
import pyubx2.ubxtypes_core as ubt

NMEAMSG = "Looks like NMEA data. Set validate to 'False' to ignore."


class UBXReader:
    """
    UBXReader class.
    """

    def __init__(self, stream, validate=False):
        """Constructor.

        :params stream: stream
        :params validate: bool

        """

        self._stream = stream
        self._validate = validate

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> (bytes, UBXMessage):
        """Return next item in iteration."""

        (raw_data, parsed_data) = self.read()
        if raw_data is not None:
            return (raw_data, parsed_data)
        raise StopIteration

    def read(self) -> (bytes, UBXMessage):
        """Read the binary data from the serial buffer.

        :return (bytes:, UBXMessage:)

        """

        stm = self._stream
        reading = True
        raw_data = None
        parsed_data = None

        byte1 = stm.read(2)  # read the first two bytes

        while reading:
            if len(byte1) < 2:  # EOF
                break
            if byte1 == ubt.UBX_HDR:  # it's a UBX message
                byten = stm.read(4)
                if len(byten) < 4:  # EOF
                    break
                clsid = byten[0:1]
                msgid = byten[1:2]
                lenb = byten[2:4]
                leni = int.from_bytes(lenb, "little", signed=False)
                byten = stm.read(leni + 2)
                if len(byten) < leni + 2:  # EOF
                    break
                plb = byten[0:leni]
                cksum = byten[leni : leni + 2]
                raw_data = ubt.UBX_HDR + clsid + msgid + lenb + plb + cksum
                parsed_data = UBXMessage.parse(raw_data)
                reading = False
            else:  # it's not a UBX message
                if self._validate:  # raise error and quit
                    nmeawarn = NMEAMSG if byte1 in (b"$G", b"$P") else ""
                    raise UBXStreamError(f"Unknown data header {byte1}. {nmeawarn}")
                byte1 = stm.read(2)  # read next 2 bytes and carry on

        return (raw_data, parsed_data)
