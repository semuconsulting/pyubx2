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

    def __init__(self, stream, validate: bool = False, mode: int = 0):
        """Constructor.

        :param stream stream: input data stream
        :param bool validate: validate (y/n)
        :param int mode: message mode (0=GET, 1=SET, 2=POLL)
        :raise UBXStreamError
        """

        if mode not in (0, 1, 2):
            raise UBXStreamError(f"Invalid stream mode {mode} - must be 0, 1 or 2")

        self._stream = stream
        self._validate = validate
        self._mode = mode

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> (bytes, UBXMessage):
        """
        Return next item in iteration.

        :return tuple of (raw_data as bytes, parsed_data as UBXMessage)
        :rtype tuple
        :raise StopIteration
        """

        (raw_data, parsed_data) = self.read()
        if raw_data is not None:
            return (raw_data, parsed_data)
        raise StopIteration

    def read(self) -> (bytes, UBXMessage):
        """
        Read the binary data from the serial buffer.

        :return tuple of (raw_data as bytes, parsed_data as UBXMessage)
        :rtype tuple
        :raise UBXStreamError
        """

        stm = self._stream
        reading = True
        raw_data = None
        parsed_data = None

        byte1 = stm.read(1)  # read the first byte

        while reading:
            is_ubx = False
            if len(byte1) < 1:  # EOF
                break
            if byte1 == b"\xb5":
                byte2 = stm.read(1)
                if len(byte2) < 1:  # EOF
                    break
                if byte2 == b"\x62":
                    is_ubx = True
            if is_ubx:  # it's a UBX message
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
                parsed_data = UBXMessage.parse(raw_data, False, self._mode)
                reading = False
            else:  # it's not a UBX message (NMEA or something else)
                if self._validate:  # raise error and quit
                    nmeawarn = NMEAMSG if byte1 == b"\x24" else ""  # "$"
                    raise UBXStreamError(f"Unknown data header {byte1}. {nmeawarn}")
                byte1 = stm.read(1)  # read next byte and carry on

        return (raw_data, parsed_data)
