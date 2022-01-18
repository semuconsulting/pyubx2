"""
UBXReader class.

Reads and parses individual UBX or NMEA messages from any stream
which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data
(as a UBXMessage or NMEAMessage object).

'protfilter' governs which protocols (NMEA and/or UBX) are processed
'quitonerror' governs how errors are handled

Created on 2 Oct 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from pynmeagps import NMEAReader
import pynmeagps.exceptions as nme
from pyubx2 import UBXMessage
from pyubx2.ubxhelpers import calc_checksum, val2bytes, bytes2val
import pyubx2.ubxtypes_core as ubt
import pyubx2.exceptions as ube


class UBXReader:
    """
    UBXReader class.
    """

    def __init__(self, datastream, **kwargs):
        """Constructor.

        :param datastream stream: input data stream
        :param int quitonerror: (kwarg) 0 = ignore errors,  1 = log errors and continue, 2 = (re)raise errors (1)
        :param int protfilter: (kwarg) protocol filter 1 = NMEA, 2 = UBX, 3 = BOTH (3)
        :param int validate: (kwarg) 0 = ignore invalid checksum, 1 = validate checksum (1)
        :param int msgmode: (kwarg) 0=GET, 1=SET, 2=POLL (0)
        :param bool parsebitfield: (kwarg) 1 = parse bitfields, 0 = leave as bytes (1)
        :raises: UBXStreamError (if mode is invalid)

        """

        self._stream = datastream
        self._protfilter = int(
            kwargs.get("protfilter", ubt.NMEA_PROTOCOL | ubt.UBX_PROTOCOL)
        )
        self._quitonerror = int(kwargs.get("quitonerror", ubt.ERR_LOG))
        # self._ubxonly = kwargs.get("ubxonly", False) # flag superceded by protfilter
        self._validate = int(kwargs.get("validate", ubt.VALCKSUM))
        self._parsebf = int(kwargs.get("parsebitfield", True))
        self._msgmode = int(kwargs.get("msgmode", 0))

        if self._msgmode not in (0, 1, 2):
            raise ube.UBXStreamError(
                f"Invalid stream mode {self._msgmode} - must be 0, 1 or 2"
            )

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
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

    def read(self) -> tuple:
        """
        Read a single NMEA or UBX message from the stream buffer
        and return both raw and parsed data.

        'protfilter' determines which protocols are parsed.
        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or NMEAMessage)
        :rtype: tuple
        :raises: UBXStreamError (if unrecognised protocol in data stream)
        """

        parsing = True

        try:
            while parsing:  # loop until end of valid message or EOF
                raw_data = None
                parsed_data = None
                byte1 = self._stream.read(1)  # read the first byte
                if len(byte1) < 1:
                    raise EOFError()
                # if not UBX or NMEA, discard and continue
                if byte1 not in (b"\xb5", b"\x24"):
                    continue
                byte2 = self._stream.read(1)
                if len(byte2) < 1:
                    raise EOFError()
                # if it's a UBX message (b'\xb5\x62')
                if byte1 + byte2 == ubt.UBX_HDR:
                    (raw_data, parsed_data) = self._parse_ubx(byte1 + byte2)
                    # if protocol filter passes UBX, return message,
                    # otherwise discard and continue
                    if self._protfilter & ubt.UBX_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's an NMEA message ('$G' or '$P')
                elif byte1 + byte2 in ubt.NMEA_HDR:
                    (raw_data, parsed_data) = self._parse_nmea(byte1 + byte2)
                    # if protocol filter passes NMEA, return message,
                    # otherwise discard and continue
                    if self._protfilter & ubt.NMEA_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # unrecognised protocol header
                else:
                    if self._quitonerror != ubt.ERR_IGNORE:
                        raise ube.UBXStreamError(f"Unknown protocol {byte1 + byte2}.")
                    return (None, None)

        except EOFError:
            return (None, None)

        return (raw_data, parsed_data)

    def _parse_ubx(self, hdr: bytes) -> tuple:
        """
        Parse remainder of UBX message.

        :param bytes hdr: UBX header (b'\xb5\x62')
        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or None)
        :rtype: tuple
        """

        # read the rest of the UBX message from the buffer
        byten = self._stream.read(4)
        if len(byten) < 4:  # EOF
            raise EOFError()
        clsid = byten[0:1]
        msgid = byten[1:2]
        lenb = byten[2:4]
        leni = int.from_bytes(lenb, "little", signed=False)
        byten = self._stream.read(leni + 2)
        if len(byten) < leni + 2:  # EOF
            raise EOFError()
        plb = byten[0:leni]
        cksum = byten[leni : leni + 2]
        raw_data = hdr + clsid + msgid + lenb + plb + cksum
        # only parse if we need to (filter passes UBX)
        if self._protfilter & ubt.UBX_PROTOCOL:
            parsed_data = self.parse(
                raw_data,
                validate=self._validate,
                msgmode=self._msgmode,
                parsebitfield=self._parsebf,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_nmea(self, hdr: bytes) -> tuple:
        """
        Parse remainder of NMEA message (using pynmeagps library).

        :param bytes hdr: NMEA header ($G or $P)
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage or None)
        :rtype: tuple
        """

        # read the rest of the NMEA message from the buffer
        byten = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if byten[-2:] != b"\x0d\x0a":
            raise EOFError()
        raw_data = hdr + byten
        # only parse if we need to (filter passes NMEA)
        if self._protfilter & ubt.NMEA_PROTOCOL:
            # invoke pynmeagps parser
            parsed_data = NMEAReader.parse(
                raw_data,
                validate=self._validate,
                msgmode=self._msgmode,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def iterate(self, **kwargs) -> tuple:
        """
        Invoke the iterator within an exception handling framework.

        :param int quitonerror: (kwarg) 0 = ignore errors,  1 = log errors and continue, 2 = (re)raise errors (0)
        :param object errorhandler: (kwarg) Optional error handler (None)
        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or NMEAMessage)
        :rtype: tuple
        :raises: UBX/NMEA...Error (if quitonerror is set and stream is invalid)

        """

        quitonerror = kwargs.get("quitonerror", ubt.ERR_IGNORE)
        errorhandler = kwargs.get("errorhandler", None)

        while True:
            try:
                yield next(self)  # invoke the iterator
            except StopIteration:
                break
            except (
                ube.UBXMessageError,
                ube.UBXTypeError,
                ube.UBXParseError,
                ube.UBXStreamError,
                nme.NMEAMessageError,
                nme.NMEATypeError,
                nme.NMEAParseError,
                nme.NMEAStreamError,
            ) as err:
                # raise, log or ignore any error depending
                # on the quitonerror setting
                if quitonerror == ubt.ERR_RAISE:
                    raise err
                elif quitonerror == ubt.ERR_LOG:
                    # pass to error handler if there is one
                    if errorhandler is None:
                        print(err)
                    else:
                        errorhandler(err)
                # continue

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(message: bytes, **kwargs) -> object:
        """
        Parse UBX byte stream to UBXMessage object.

        Includes option to validate incoming payload length and checksum
        (the UBXMessage constructor can calculate and assign its own values anyway).

        :param bytes message: binary message to parse
        :param int validate: (kwarg) validate cksum (VALCKSUM (1)=True (default), VALNONE (0)=False)
        :param int msgmode: (kwarg) message mode (0=GET (default), 1=SET, 2=POLL)
        :param bool parsebitfield: (kwarg) parse bitfields True (default)/False
        :return: UBXMessage object
        :rtype: UBXMessage
        :raises: UBXParseError (if data stream contains invalid data or unknown message type)

        """

        msgmode = kwargs.get("msgmode", ubt.GET)
        validate = kwargs.get("validate", ubt.VALCKSUM)
        parsebf = kwargs.get("parsebitfield", True)

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
        if validate & ubt.VALCKSUM:
            if hdr != ubt.UBX_HDR:
                raise ube.UBXParseError(
                    (f"Invalid message header {hdr}" f" - should be {ubt.UBX_HDR}")
                )
            if leni != bytes2val(lenb, ubt.U2):
                raise ube.UBXParseError(
                    (
                        f"Invalid payload length {lenb}"
                        f" - should be {val2bytes(leni, ubt.U2)}"
                    )
                )
            if ckm != ckv:
                raise ube.UBXParseError(
                    (f"Message checksum {ckm}" f" invalid - should be {ckv}")
                )
        try:
            if payload is None:
                return UBXMessage(clsid, msgid, msgmode)
            return UBXMessage(
                clsid,
                msgid,
                msgmode,
                payload=payload,
                parsebitfield=parsebf,
            )
        except KeyError as err:
            modestr = ["GET", "SET", "POLL"][msgmode]
            raise ube.UBXParseError(
                (f"Unknown message type clsid {clsid}, msgid {msgid}, mode {modestr}")
            ) from err
