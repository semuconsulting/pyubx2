"""
UBXReader class.

Reads and parses individual UBX, NMEA or RTCM3 messages from any stream
which supports a read(n) -> bytes method.

Returns both the raw binary data (as bytes) and the parsed data
(as a UBXMessage, NMEAMessage or RTCMMessage object).

'protfilter' governs which protocols (NMEA, UBX or RTCM3) are processed
'quitonerror' governs how errors are handled
'msgmode' indicates the type of UBX datastream (input GET, output SET, query POLL)

Created on 2 Oct 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from socket import socket

import pynmeagps.exceptions as nme
import pyrtcm.exceptions as rte
from pynmeagps import NMEA_HDR, NMEAReader
from pyrtcm import RTCMReader

from pyubx2.exceptions import (
    UBXMessageError,
    UBXParseError,
    UBXStreamError,
    UBXTypeError,
)
from pyubx2.socket_stream import SocketStream
from pyubx2.ubxhelpers import bytes2val, calc_checksum, val2bytes
from pyubx2.ubxmessage import UBXMessage
from pyubx2.ubxtypes_core import (
    ERR_LOG,
    ERR_RAISE,
    GET,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
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
        msgmode: int = GET,
        validate: int = VALCKSUM,
        protfilter: int = NMEA_PROTOCOL | UBX_PROTOCOL,
        quitonerror: int = ERR_LOG,
        parsebitfield: bool = True,
        scaling: bool = True,
        labelmsm: bool = True,
        bufsize: int = 4096,
        parsing: bool = True,
        errorhandler: object = None,
    ):
        """Constructor.

        :param datastream stream: input data stream
        :param int msgmode: 0=GET, 1=SET, 2=POLL (0)
        :param int validate: 0 = ignore invalid checksum, 1 = validate checksum (1)
        :param int protfilter: protocol filter 1 = NMEA, 2 = UBX, 4 = RTCM3 (3)
        :param int quitonerror: 0 = ignore errors,  1 = log continue, 2 = (re)raise (1)
        :param bool parsebitfield: 1 = parse bitfields, 0 = leave as bytes (1)
        :param bool scaling: 1 = apply scale factors, 0 = do not apply (1)
        :param bool labelmsm: whether to label RTCM3 MSM NSAT and NCELL attributes (1)
        :param int bufsize: socket recv buffer size (1024)
        :param bool parsing: True = parse data, False = don't parse data (output raw only) (True)
        :param int errorhandler: error handling object or function (None)
        :raises: UBXStreamError (if mode is invalid)
        """
        # pylint: disable=too-many-arguments

        if isinstance(datastream, socket):
            self._stream = SocketStream(datastream, bufsize=bufsize)
        else:
            self._stream = datastream
        self._protfilter = protfilter
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._validate = validate
        self._parsebf = parsebitfield
        self._scaling = scaling
        self._labelmsm = labelmsm
        self._msgmode = msgmode
        self._parsing = parsing

        if self._msgmode not in (0, 1, 2):
            raise UBXStreamError(
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
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(self) -> tuple:
        """
        Read a single NMEA, UBX or RTCM3 message from the stream buffer
        and return both raw and parsed data.

        'protfilter' determines which protocols are parsed.
        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage, NMEAMessage or RTCMMessage)
        :rtype: tuple
        :raises: UBXStreamError (if unrecognised protocol in data stream)
        """

        flag = True

        try:
            while flag:  # loop until end of valid message or EOF
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
                    (raw_data, parsed_data) = self._parse_ubx(bytehdr)
                    # if protocol filter passes UBX, return message,
                    # otherwise discard and continue
                    if self._protfilter & UBX_PROTOCOL:
                        flag = False
                    else:
                        continue
                # if it's an NMEA message ('$G' or '$P')
                elif bytehdr in NMEA_HDR:
                    (raw_data, parsed_data) = self._parse_nmea(bytehdr)
                    # if protocol filter passes NMEA, return message,
                    # otherwise discard and continue
                    if self._protfilter & NMEA_PROTOCOL:
                        flag = False
                    else:
                        continue
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                elif byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    (raw_data, parsed_data) = self._parse_rtcm3(bytehdr)
                    # if protocol filter passes RTCM, return message,
                    # otherwise discard and continue
                    if self._protfilter & RTCM3_PROTOCOL:
                        flag = False
                    else:
                        continue
                # unrecognised protocol header
                else:
                    if self._quitonerror == ERR_RAISE:
                        raise UBXParseError(f"Unknown protocol {bytehdr}.")
                    if self._quitonerror == ERR_LOG:
                        return (bytehdr, f"<UNKNOWN PROTOCOL(header={bytehdr})>")
                    continue

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
                self._do_error(str(err))
            parsed_data = str(err)

        return (raw_data, parsed_data)

    def _parse_ubx(self, hdr: bytes) -> tuple:
        """
        Parse remainder of UBX message.

        :param bytes hdr: UBX header (b'\xb5\x62')
        :return: tuple of (raw_data as bytes, parsed_data as UBXMessage or None)
        :rtype: tuple
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
                quitonerror=self._quitonerror,
                msgmode=self._msgmode,
                parsebitfield=self._parsebf,
                scaling=self._scaling,
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

    def _parse_rtcm3(self, hdr: bytes) -> tuple:
        """
        Parse any RTCM3 data in the stream (using pyrtcm library).

        :param bytes hdr: first 2 bytes of RTCM3 header
        :param bool validate: (kwarg) validate crc Y/N
        :return: tuple of (raw_data as bytes, parsed_stub as RTCMMessage)
        :rtype: tuple
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
                scaling=self._scaling,
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
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) < size:  # EOF
            raise EOFError()
        return data

    def _read_line(self) -> bytes:
        """
        Read bytes until LF (0x0a) terminator.

        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if data[-1:] != b"\x0a":
            raise EOFError()
        return data

    def _do_error(self, err: str):
        """
        Handle error.

        :param str err: error message
        :raises: UBXParseError if quitonerror = 2
        """

        if self._quitonerror == ERR_RAISE:
            raise UBXParseError(err)
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            if self._errorhandler is None:
                print(err)
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
        msgmode: int = GET,
        validate: int = VALCKSUM,
        quitonerror: int = ERR_LOG,
        parsebitfield: bool = True,
        scaling: bool = True,
    ) -> object:
        """
        Parse UBX byte stream to UBXMessage object.

        Includes option to validate incoming payload length and checksum
        (the UBXMessage constructor can calculate and assign its own values anyway).

        :param bytes message: binary message to parse
        :param int quitonerror: 0 = ignore errors,  1 = log continue, 2 = (re)raise (1)
        :param int validate: validate cksum (VALCKSUM (1)=True (default), VALNONE (0)=False)
        :param int msgmode: message mode (0=GET (default), 1=SET, 2=POLL)
        :param bool parsebitfield: 1 = parse bitfields, 0 = leave as bytes (1)
        :param bool scaling: 1 = apply scale factors, 0 = do not apply (1)
        :return: UBXMessage object
        :rtype: UBXMessage
        :raises: UBXParseError (if data stream contains invalid data or unknown message type)
        """
        # pylint: disable=too-many-arguments

        if msgmode not in (0, 1, 2):
            raise UBXParseError(f"Invalid message mode {msgmode} - must be 0, 1 or 2")

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
        try:
            if payload is None:
                return UBXMessage(clsid, msgid, msgmode)
            return UBXMessage(
                clsid,
                msgid,
                msgmode,
                payload=payload,
                parsebitfield=parsebitfield,
                scaling=scaling,
            )
        except KeyError as err:
            modestr = ["GET", "SET", "POLL"][msgmode]
            errmsg = (
                f"Unknown message type clsid {clsid}, msgid {msgid}, mode {modestr}\n"
                + "Check 'msgmode' keyword argument is appropriate for data stream"
            )
            if quitonerror == ERR_RAISE:
                raise UBXParseError(errmsg) from err
            if quitonerror == ERR_LOG:
                print(errmsg)
            return None
