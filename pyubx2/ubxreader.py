"""
UBXReader class.

Reads and parses individual UBX messages from any stream which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data (as a UBXMessage object).

If the 'ubxonly' parameter is set to 'True', the reader will raise a UBXStreamerError if
it encounters any non-UBX data. Otherwise, it will ignore the non-UBX data and attempt
to carry on.

Created on 2 Oct 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from pyubx2.ubxmessage import UBXMessage
from pyubx2.ubxhelpers import calc_checksum
import pyubx2.ubxtypes_core as ubt
import pyubx2.exceptions as ube

NMEAMSG = "Looks like NMEA data. Set ubxonly flag to 'False' to ignore."
# parser validation flag values
VALNONE = 0
VALCKSUM = 1


class UBXReader:
    """
    UBXReader class.
    """

    def __init__(self, stream, *args, **kwargs):
        """Constructor.

        :param stream stream: input data stream
        :param bool ubxonly (kwarg): check for non-UBX data (False (ignore - default), True (reject))
        :param int validate (kwarg): validate checksum (VALCKSUM (1)=True (default), VALNONE (0)=False)
        :param int msgmode (kwarg): message mode (0=GET (default), 1=SET, 2=POLL)
        :raises: UBXStreamError (if mode is invalid)

        """

        ubx_only = kwargs.get("ubxonly", False)
        msgmode = kwargs.get("msgmode", 0)
        validate = kwargs.get("validate", VALCKSUM)

        # accept args for backwards compatibility if no kwargs
        if len(kwargs) == 0:
            if len(args) > 0:
                ubx_only = args[0]
            if len(args) > 1:
                msgmode = args[1]

        if msgmode not in (0, 1, 2):
            raise ube.UBXStreamError(
                f"Invalid stream mode {msgmode} - must be 0, 1 or 2"
            )

        self._stream = stream
        self._ubx_only = ubx_only
        self._validate = validate
        self._mode = msgmode

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> (bytes, UBXMessage):
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage)
        :rtype: tuple
        :raises: StopIteration

        """

        (raw_data, parsed_data) = self.read()
        if raw_data is not None:
            return (raw_data, parsed_data)
        raise StopIteration

    def read(self) -> (bytes, UBXMessage):
        """
        Read the binary data from the stream buffer.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage)
        :rtype: tuple
        :raises: UBXStreamError (if ubxonly=True and stream includes non-UBX data)

        """

        reading = True
        raw_data = None
        parsed_data = None

        byte1 = self._stream.read(1)  # read the first byte

        while reading:
            is_ubx = False
            is_nmea = False
            if len(byte1) < 1:  # EOF
                break
            if byte1 == b"\xb5":
                byte2 = self._stream.read(1)
                if len(byte2) < 1:  # EOF
                    break
                if byte2 == b"\x62":
                    is_ubx = True
            if is_ubx:  # it's a UBX message
                byten = self._stream.read(4)
                if len(byten) < 4:  # EOF
                    break
                clsid = byten[0:1]
                msgid = byten[1:2]
                lenb = byten[2:4]
                leni = int.from_bytes(lenb, "little", signed=False)
                byten = self._stream.read(leni + 2)
                if len(byten) < leni + 2:  # EOF
                    break
                plb = byten[0:leni]
                cksum = byten[leni : leni + 2]
                raw_data = ubt.UBX_HDR + clsid + msgid + lenb + plb + cksum
                parsed_data = self.parse(
                    raw_data, validate=self._validate, msgmode=self._mode
                )
                reading = False
            else:  # it's not a UBX message (NMEA or something else)
                prevbyte = byte1
                byte1 = self._stream.read(1)
                if prevbyte == b"\x24" and byte1 in (b"\x47", b"\x50"):  # "$G" or "$P"
                    is_nmea = True  # looks like an NMEA message
                if self._ubx_only:  # raise error and quit
                    nmeawarn = NMEAMSG if is_nmea else ""
                    raise ube.UBXStreamError(
                        f"Unknown data header {prevbyte + byte1}. {nmeawarn}"
                    )

        return (raw_data, parsed_data)

    @staticmethod
    def parse(message: bytes, *args, **kwargs) -> object:
        """
        Parse UBX byte stream to UBXMessage object.

        Includes option to validate incoming payload length and checksum
        (the UBXMessage constructor can calculate and assign its own values anyway).

        :param bytes message: binary message to parse
        :param int validate (kwarg): validate checksum (VALCKSUM (1)=True (default), VALNONE (0)=False)
        :param int msgmode (kwarg): message mode (0=GET (default), 1=SET, 2=POLL)
        :return: UBXMessage object
        :rtype: UBXMessage
        :raises: UBXParseError (if data stream contains invalid data or unknown message type)

        """

        msgmode = kwargs.get("msgmode", ubt.GET)
        validate = kwargs.get("validate", VALCKSUM)

        # accept args for backwards compatibility if no kwargs
        if len(kwargs) == 0:
            if len(args) > 0:
                validate = args[0]
            if len(args) > 1:
                msgmode = args[1]

        if msgmode not in (0, 1, 2):
            raise ube.UBXParseError(
                f"Invalid message mode {msgmode} - must be 0, 1 or 2"
            )

        lenm = len(message)
        hdr = message[0:2]
        clsid = message[2:3]
        msgid = message[3:4]
        lenb = message[4:6]
        if lenb == b"\x00\x00":
            payload = None
            leni = 0
        else:
            payload = message[6 : lenm - 2]
            leni = len(payload)
        ckm = message[lenm - 2 : lenm]
        if payload is not None:
            ckv = calc_checksum(clsid + msgid + lenb + payload)
        else:
            ckv = calc_checksum(clsid + msgid + lenb)
        if validate & VALCKSUM:
            if hdr != ubt.UBX_HDR:
                raise ube.UBXParseError(
                    (f"Invalid message header {hdr}" f" - should be {ubt.UBX_HDR}")
                )
            if leni != UBXMessage.bytes2val(lenb, ubt.U2):
                raise ube.UBXParseError(
                    (
                        f"Invalid payload length {lenb}"
                        f" - should be {UBXMessage.val2bytes(leni, ubt.U2)}"
                    )
                )
            if ckm != ckv:
                raise ube.UBXParseError(
                    (f"Message checksum {ckm}" f" invalid - should be {ckv}")
                )
        try:
            if payload is None:
                return UBXMessage(clsid, msgid, msgmode)
            return UBXMessage(clsid, msgid, msgmode, payload=payload)
        except KeyError as err:
            modestr = ["GET", "SET", "POLL"][msgmode]
            raise ube.UBXParseError(
                (f"Unknown message type clsid {clsid}, msgid {msgid}, mode {modestr}")
            ) from err
