"""
UBXReader class.

Reads and parses individual UBX, NMEA or RTCM3 messages from any viable
data stream which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data
(as a UBXMessage, NMEAMessage or RTCMMessage object).

- 'protfilter' governs which protocols (NMEA, UBX or RTCM3) are processed
- 'quitonerror' governs how errors are handled
- 'msgmode' indicates the type of UBX datastream (output GET, input SET, query POLL).
  If msgmode is set to SETPOLL, input/query mode will be automatically detected by parser.

Created on 2 Oct 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

from logging import getLogger
from socket import socket
from types import FunctionType, NoneType
from typing import Literal

import pynmeagps.exceptions as nme
import pyrtcm.exceptions as rte
from pynmeagps import (
    DEFAULT_BUFSIZE,
    ENCODE_NONE,
    NMEA_HDR,
    NMEAMessage,
    NMEAReader,
    SocketWrapper,
)
from pyrtcm import RTCMMessage, RTCMReader

from pyubx2.exceptions import (
    UBXMessageError,
    UBXParseError,
    UBXStreamError,
    UBXTypeError,
)
from pyubx2.ubxhelpers import bytes2val, calc_checksum, getinputmode, val2bytes
from pyubx2.ubxmessage import UBXMessage
from pyubx2.ubxtypes_core import (
    ERR_LOG,
    ERR_RAISE,
    GET,
    NMEA_PROTOCOL,
    POLL,
    RTCM3_PROTOCOL,
    SET,
    SETPOLL,
    U2,
    UBX_HDR,
    UBX_PROTOCOL,
    VALCKSUM,
)


class UBXReader:
    """
    UBXReader class.
    """

    def __init__(
        self,
        datastream,
        msgmode: Literal[0, 1, 2] = GET,
        validate: int = VALCKSUM,
        protfilter: int = NMEA_PROTOCOL | UBX_PROTOCOL | RTCM3_PROTOCOL,
        quitonerror: Literal[0, 1, 2] = ERR_LOG,
        parsebitfield: Literal[0, 1, 2] = 1,
        labelmsm: Literal[1, 2] = 1,
        bufsize: int = DEFAULT_BUFSIZE,
        parsing: bool = True,
        errorhandler: FunctionType | NoneType = None,
        encoding: int = ENCODE_NONE,
    ):
        """Constructor.

        :param datastream stream: input data stream
        :param Literal[0,1,2] msgmode: 0=GET, 1=SET, 2=POLL, 3=SETPOLL (0)
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :param int protfilter: NMEA_PROTOCOL (1), UBX_PROTOCOL (2), RTCM3_PROTOCOL (4),
            Can be OR'd (7)
        :param Literal[0,1,2] quitonerror: ERR_IGNORE (0) = ignore errors,  
            ERR_LOG (1) = log continue, ERR_RAISE (2) = (re)raise (1)
        :param Literal[0,1,2] parsebitfield: 0 = parse bitfield as bytes, 1 = parse as \
            individual bits, 2 = parse as bytes and bits (1)
        :param Literal[1,2] labelmsm: RTCM3 MSM label type 1 = RINEX, 2 = BAND (1)
        :param int bufsize: socket recv buffer size (4096)
        :param bool parsing: True = parse data, False = don't parse data (output raw only) (True)
        :param FunctionType | NoneType errorhandler: error handling object or function (None)
        :param int encoding: encoding for socket stream \
            (0 = none, 1 = chunk, 2 = gzip, 4 = compress, 8 = deflate (can be OR'd)) (0)
        :raises: UBXStreamError (if mode is invalid)
        """
        # pylint: disable=too-many-arguments

        if isinstance(datastream, socket):
            self._stream = SocketWrapper(datastream, encoding=encoding, bufsize=bufsize)
        else:
            self._stream = datastream
        self._protfilter = protfilter
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._validate = validate
        self._parsebf = parsebitfield
        self._labelmsm = labelmsm
        self._msgmode = msgmode
        self._parsing = parsing
        self._logger = getLogger(__name__)

        if self._msgmode not in (GET, SET, POLL, SETPOLL):
            raise UBXStreamError(
                f"Invalid stream mode {self._msgmode} - must be 0, 1, 2 or 3"
            )

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(
        self,
    ) -> tuple[bytes | NoneType, UBXMessage | NMEAMessage | RTCMMessage | NoneType]:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage,
            NMEAMessage or RTCMMessage)
        :rtype: tuple[bytes | NoneType, UBXMessage | NMEAMessage | RTCMMessage | NoneType]
        :raises: StopIteration

        """

        raw_data, parsed_data = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(
        self,
    ) -> tuple[bytes | NoneType, UBXMessage | NMEAMessage | RTCMMessage | NoneType]:
        """
        Read a single NMEA, UBX or RTCM3 message from the stream buffer
        and return both raw and parsed data.

        'protfilter' determines which protocols are parsed.
        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage,
            NMEAMessage or RTCMMessage)
        :rtype: tuple[bytes | NoneType, UBXMessage | NMEAMessage | RTCMMessage | NoneType]
        :raises: Exception (if invalid or unrecognised protocol in data stream)
        """

        raw_data = None
        parsed_data = None
        parsing = True
        while parsing:  # loop until end of valid message or EOF
            try:

                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                # if not UBX, NMEA or RTCM3, discard and continue
                if byte1 not in (b"\xb5", b"\x24", b"\xd3"):
                    continue
                byte2 = self._read_bytes(1)
                bytehdr = byte1 + byte2
                # if it's a UBX message (b'\xb5\x62')
                if bytehdr == UBX_HDR:
                    raw_data, parsed_data = self._parse_ubx(bytehdr)
                    # if protocol filter passes UBX, return message,
                    # otherwise discard and continue
                    if self._protfilter & UBX_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's an NMEA message (b'\x24\x..)
                elif bytehdr in NMEA_HDR:
                    raw_data, parsed_data = self._parse_nmea(bytehdr)
                    # if protocol filter passes NMEA, return message,
                    # otherwise discard and continue
                    if self._protfilter & NMEA_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                elif byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    raw_data, parsed_data = self._parse_rtcm3(bytehdr)
                    # if protocol filter passes RTCM, return message,
                    # otherwise discard and continue
                    if self._protfilter & RTCM3_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # unrecognised protocol header
                else:
                    raise UBXParseError(f"Unknown protocol header {bytehdr}.")

            except EOFError:
                return (None, None)
            except (
                UBXMessageError,
                UBXTypeError,
                UBXParseError,
                UBXStreamError,
                nme.NMEAMessageError,
                nme.NMEATypeError,
                nme.NMEAParseError,
                nme.NMEAStreamError,
                rte.RTCMMessageError,
                rte.RTCMParseError,
                rte.RTCMStreamError,
                rte.RTCMTypeError,
            ) as err:
                if self._quitonerror:
                    self._do_error(err)
                continue

        return (raw_data, parsed_data)

    def _parse_ubx(self, hdr: bytes) -> tuple[bytes | NoneType, UBXMessage | NoneType]:
        """
        Parse remainder of UBX message.

        :param bytes hdr: UBX header (b'\\xb5\\x62')
        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or None)
        :rtype: tuple[bytes | NoneType, UBXMessage | NoneType]
        """

        # read the rest of the UBX message from the buffer
        byten = self._read_bytes(4)
        clsid = byten[0:1]
        msgid = byten[1:2]
        lenb = byten[2:4]
        leni = int.from_bytes(lenb, "little", signed=False)
        byten = self._read_bytes(leni + 2)
        plb = byten[0:leni]
        cksum = byten[leni : leni + 2]
        raw_data = hdr + clsid + msgid + lenb + plb + cksum
        # only parse if we need to (filter passes UBX)
        if (self._protfilter & UBX_PROTOCOL) and self._parsing:
            parsed_data = self.parse(
                raw_data,
                validate=self._validate,
                msgmode=self._msgmode,
                parsebitfield=self._parsebf,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_nmea(
        self, hdr: bytes
    ) -> tuple[bytes | NoneType, NMEAMessage | NoneType]:
        """
        Parse remainder of NMEA message (using pynmeagps library).

        :param bytes hdr: NMEA header (b'\\x24\\x..')
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage or None)
        :rtype: tuple[bytes | NoneType, NMEAMessage | NoneType]
        """

        # read the rest of the NMEA message from the buffer
        byten = self._read_line()  # NMEA protocol is CRLF-terminated
        raw_data = hdr + byten
        # only parse if we need to (filter passes NMEA)
        if (self._protfilter & NMEA_PROTOCOL) and self._parsing:
            # invoke pynmeagps parser
            parsed_data = NMEAReader.parse(
                raw_data,
                validate=self._validate,
                msgmode=self._msgmode,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_rtcm3(
        self, hdr: bytes
    ) -> tuple[bytes | NoneType, RTCMMessage | NoneType]:
        """
        Parse any RTCM3 data in the stream (using pyrtcm library).

        :param bytes hdr: first 2 bytes of RTCM3 header
        :return: tuple of (raw_data as bytes, parsed_stub as RTCMMessage)
        :rtype: tuple[bytes | NoneType, RTCMMessage | NoneType]
        """

        hdr3 = self._read_bytes(1)
        size = hdr3[0] | (hdr[1] << 8)
        payload = self._read_bytes(size)
        crc = self._read_bytes(3)
        raw_data = hdr + hdr3 + payload + crc
        # only parse if we need to (filter passes RTCM)
        if (self._protfilter & RTCM3_PROTOCOL) and self._parsing:
            # invoke pyrtcm parser
            parsed_data = RTCMReader.parse(
                raw_data,
                validate=self._validate,
                labelmsm=self._labelmsm,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: UBXStreamError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) == 0:  # EOF
            raise EOFError()
        if 0 < len(data) < size:  # truncated stream
            raise UBXStreamError(
                "Serial stream terminated unexpectedly. "
                f"{size} bytes requested, {len(data)} bytes returned."
            )
        return data

    def _read_line(self) -> bytes:
        """
        Read bytes until LF (0x0a) terminator.

        :return: bytes
        :rtype: bytes
        :raises: UBXStreamError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if len(data) == 0:
            raise EOFError()  # pragma: no cover
        if data[-1:] != b"\x0a":  # truncated stream
            raise UBXStreamError(
                "Serial stream terminated unexpectedly. "
                f"Line requested, {len(data)} bytes returned."
            )
        return data

    def _do_error(self, err: Exception):
        """
        Handle error.

        :param Exception err: error
        :raises: Exception if quitonerror = ERR_RAISE (2)
        """

        if self._quitonerror == ERR_RAISE:
            raise err from err
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            # else just log
            if self._errorhandler is None:
                self._logger.error(err)
            else:
                self._errorhandler(err)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(
        message: bytes,
        msgmode: Literal[0, 1, 2] = GET,
        validate: int = VALCKSUM,
        parsebitfield: Literal[0, 1, 2] = 1,
    ) -> UBXMessage:
        """
        Parse UBX byte stream to UBXMessage object.

        :param bytes message: binary message to parse
        :param Literal[0,1,2] msgmode: GET (0), SET (1), POLL (2) (0)
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :param Literal[0,1,2] parsebitfield: 0 = parse bitfield as bytes, 1 = parse as \
            individual bits, 2 = parse as bytes and bits (1)
        :return: UBXMessage object
        :rtype: UBXMessage
        :raises: Exception (if data stream contains invalid data or unknown message type)
        """
        # pylint: disable=too-many-arguments

        if msgmode not in (GET, SET, POLL, SETPOLL):
            raise UBXParseError(
                f"Invalid message mode {msgmode} - must be 0, 1, 2 or 3"
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
            if hdr != UBX_HDR:
                raise UBXParseError(
                    (f"Invalid message header {hdr}" f" - should be {UBX_HDR}")
                )
            if leni != bytes2val(lenb, U2):
                raise UBXParseError(
                    (
                        f"Invalid payload length {lenb}"
                        f" - should be {val2bytes(leni, U2)}"
                    )
                )
            if ckm != ckv:
                raise UBXParseError(
                    (f"Message checksum {ckm}" f" invalid - should be {ckv}")
                )
        # if input message (SET or POLL), determine mode automatically
        if msgmode == SETPOLL:
            msgmode = getinputmode(message)  # returns SET or POLL
        if payload is None:
            return UBXMessage(clsid, msgid, msgmode)
        return UBXMessage(
            clsid,
            msgid,
            msgmode,
            payload=payload,
            parsebitfield=parsebitfield,
        )
