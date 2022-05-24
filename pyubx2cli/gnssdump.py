"""
Command line utility, installed with PyPi library pyubx2,
to stream the parsed UBX, NMEA or RTCM3 output of a GNSS device
to the stdout or a designated protocol handler.

Created on 15 Jan 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=line-too-long eval-used

import sys
from socket import socket
from queue import Queue
from io import TextIOWrapper, BufferedWriter
from serial import Serial
from pyubx2 import (
    UBXReader,
    VALCKSUM,
    UBXMessageError,
    UBXParseError,
    UBXStreamError,
    UBXTypeError,
    ParameterError,
    GET,
    UBX_PROTOCOL,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
    ERR_LOG,
    ERR_RAISE,
    hextable,
    protocol,
)
from pynmeagps import (
    NMEAMessageError,
    NMEAParseError,
    NMEAStreamError,
    NMEATypeError,
)
from pyrtcm import (
    RTCMMessageError,
    RTCMParseError,
    RTCMStreamError,
    RTCMTypeError,
)
from pyubx2cli.helpstrings import GNSSDUMP_HELP

MIN_NMEA_PAYLOAD = 3  # minimum viable length of NMEA message payload
FORMAT_PARSED = 1
FORMAT_BINARY = 2
FORMAT_HEX = 4
FORMAT_HEXTABLE = 8
FORMAT_PARSEDSTRING = 16
VERBOSITY_LOW = 0
VERBOSITY_MEDIUM = 1
VERBOSITY_HIGH = 2


class GNSSStreamer:
    """
    GNSS Streamer Class.

    Streams and parses UBX, NMEA or RTCM3 GNSS messages from any data stream (e.g. Serial, Socket or File)
    to stdout (e.g. terminal) or to designated NMEA, UBX or RTCM protocol handler(s). The protocol
    handler can either be a writeable output medium (Serial, File, socket or Queue) or an evaluable
    expression.

    Ensure the output media type is consistent with the format e.g. don't try writing binary data to
    a text file.

    Input stream is defined via keyword arguments. One of either stream, socket, port or filename MUST be
    specified. The remaining arguments are all optional with defaults.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        """
        Constructor.

        Example of usage with external protocol handler:

        gnssdump port=COM3 msgfilter=NAV-PVT ubxhandler="lambda msg: print(f'lat: {msg.lat}, lon: {msg.lon}')"

        :param object stream: (kwarg) stream object (must implement read(n) -> bytes method)
        :param str port: (kwarg) serial port name
        :param str filename: (kwarg) input file FQN
        :param str socket: (kwarg) input socket host:port
        :param int baudrate: (kwarg) serial baud rate (9600)
        :param int timeout: (kwarg) serial timeout in seconds (3)
        :param int validate: (kwarg) 1 = validate checksums, 0 = do not validate (1)
        :param int msgmode: (kwarg) 0 = GET, 1 = SET, 2 = POLL (0)
        :param int parsebitfield: (kwarg) 1 = parse UBX 'X' attributes as bitfields, 0 = leave as bytes (1)
        :param int format: (kwarg) output format 1 = parsed, 2 = raw, 4 = hex, 8 = tabulated hex, 16 = parsed as string (1) (can be OR'd)
        :param int quitonerror: (kwarg) 0 = ignore errors,  1 = log errors and continue, 2 = (re)raise errors (1)
        :param int protfilter: (kwarg) 1 = NMEA, 2 = UBX, 4 = RTCM3 (7 - ALL)
        :param str msgfilter: (kwarg) comma-separated string of message identities e.g. 'NAV-PVT,GNGSA' (None)
        :param int limit: (kwarg) maximum number of messages to read (0 = unlimited)
        :param int verbosity: (kwarg) log message verbosity 0 = low, 1 = medium, 3 = high (1)
        :param object errorhandler: (kwarg) either writeable output medium or evaluable expression (None)
        :param object nmeahandler: (kwarg) either writeable output medium or evaluable expression (None)
        :param object ubxhandler: (kwarg) either writeable output medium or evaluable expression (None)
        :param object rtcmhandler: (kwarg) either writeable output medium or evaluable expression (None)
        :raises: ParameterError
        """
        # pylint: disable=raise-missing-from

        self._reader = None
        self._datastream = kwargs.get("datastream", None)
        self._port = kwargs.get("port", None)
        self._socket = kwargs.get("socket", None)
        self._filename = kwargs.get("filename", None)
        if (
            self._datastream is None
            and self._port is None
            and self._socket is None
            and self._filename is None
        ):
            raise ParameterError(
                "Either stream, port, socket or filename keyword argument must be provided.\nType gnssdump -h for help.",
            )

        try:

            self._baudrate = int(kwargs.get("baudrate", 9600))
            self._timeout = int(kwargs.get("timeout", 3))
            self._validate = int(kwargs.get("validate", VALCKSUM))
            self._msgmode = int(kwargs.get("msgmode", GET))
            self._parsebitfield = int(kwargs.get("parsebitfield", 1))
            self._format = int(kwargs.get("format", FORMAT_PARSED))
            self._quitonerror = int(kwargs.get("quitonerror", ERR_LOG))
            self._protfilter = int(
                kwargs.get("protfilter", NMEA_PROTOCOL | UBX_PROTOCOL | RTCM3_PROTOCOL)
            )
            self._msgfilter = kwargs.get("msgfilter", None)
            self._verbosity = int(kwargs.get("verbosity", VERBOSITY_MEDIUM))
            self._limit = int(kwargs.get("limit", 0))
            self._parsing = False
            self._stream = None
            self._msgcount = 0
            self._errcount = 0

            # protocol handlers can either be writeable output media
            # (Serial, File, socket or Queue) or an evaluable expression
            # acceptable output media types:
            htypes = (Serial, TextIOWrapper, BufferedWriter, Queue, socket)

            erh = kwargs.get("errorhandler", None)
            if isinstance(erh, htypes) or erh is None:
                self._errorhandler = erh
            else:
                self._errorhandler = eval(erh)
            nmh = kwargs.get("nmeahandler", None)
            if isinstance(nmh, htypes) or nmh is None:
                self._nmeahandler = nmh
            else:
                self._nmeahandler = eval(nmh)
            ubh = kwargs.get("ubxhandler", None)
            if isinstance(ubh, htypes) or ubh is None:
                self._ubxhandler = ubh
            else:
                self._ubxhandler = eval(ubh)
            rth = kwargs.get("rtcmhandler", None)
            if isinstance(rth, htypes) or rth is None:
                self._rtcmhandler = rth
            else:
                self._rtcmhandler = eval(rth)

        except ValueError:
            raise ParameterError(f"Invalid parameter(s).\n{GNSSDUMP_HELP}")

    def run(self, **kwargs):
        """
        Read from provided data stream (serial, file or other stream type).
        The data stream must support a read(n) -> bytes method.

        :param int limit: (kwarg) maximum number of messages to read (0 = unlimited)
        """

        self._limit = int(kwargs.get("limit", self._limit))

        # open the specified input stream
        if self._datastream is not None:  # generic stream
            with self._datastream as self._stream:
                self._start_reader()
        elif self._port is not None:  # serial
            with Serial(
                self._port, self._baudrate, timeout=self._timeout
            ) as self._stream:
                self._start_reader()
        elif self._socket is not None:  # socket
            with socket() as self._stream:
                sock = self._socket.split(":")
                if len(sock) != 2:
                    raise ParameterError(
                        "socket keyword must be in the format host:port.\nType gnssdump -h for help."
                    )
                host = sock[0]
                port = int(sock[1])
                self._stream.connect((host, port))
                self._start_reader()
        elif self._filename is not None:  # binary file
            with open(self._filename, "rb") as self._stream:
                self._start_reader()

    def _start_reader(self):
        """Create UBXReader instance."""

        self._reader = UBXReader(
            self._stream,
            quitonerror=self._quitonerror,
            protfilter=self._protfilter,
            validate=self._validate,
            msgmode=self._msgmode,
            parsebitfield=self._parsebitfield,
        )
        self._do_log(f"\nParsing GNSS data stream from: {self._stream}...\n")
        self._do_parse()

    def _do_parse(self):
        """
        Read the data stream and direct to the appropriate
        UBX or NMEA parser.

        :raises: EOFError if stream ends prematurely or message limit reached
        :raises: KeyboardInterrupt if user presses Ctrl-C
        :raises: Exception for any other uncaptured Exception
        """

        try:

            while True:  # loop until EOF, stream timeout or user hits Ctrl-C

                try:
                    (raw_data, parsed_data) = self._reader.read()
                except (
                    UBXMessageError,
                    UBXParseError,
                    UBXStreamError,
                    UBXTypeError,
                    NMEAMessageError,
                    NMEAParseError,
                    NMEAStreamError,
                    NMEATypeError,
                    RTCMMessageError,
                    RTCMParseError,
                    RTCMStreamError,
                    RTCMTypeError,
                ) as err:
                    self._do_error(err)
                    continue

                if raw_data is None:  # EOF or timeout
                    raise EOFError

                # get the message protocol (NMEA or UBX)
                msgprot = protocol(raw_data)
                handler = None
                # establish the appropriate handler and identity for this protocol
                if msgprot == UBX_PROTOCOL:
                    msgidentity = parsed_data.identity
                    handler = self._ubxhandler
                elif msgprot == NMEA_PROTOCOL:
                    msgidentity = parsed_data.talker + parsed_data.msgID
                    handler = self._nmeahandler
                elif msgprot == RTCM3_PROTOCOL:
                    msgidentity = parsed_data.identity
                    handler = self._rtcmhandler
                # does it pass the protocol filter?
                if self._protfilter & msgprot:
                    # does it pass the message identity filter if there is one?
                    if self._msgfilter is not None:
                        if msgidentity not in self._msgfilter:
                            continue
                    # if it passes, send to designated output
                    self._do_output(raw_data, parsed_data, handler)

                if self._limit and self._msgcount >= self._limit:
                    raise EOFError

        except KeyboardInterrupt:  # user hit Ctrl-C
            self._do_log("user")
        except EOFError:  # end of stream
            self._do_log("eof")
        except Exception as err:  # pylint: disable=broad-except
            self._quitonerror = ERR_RAISE  # don't ignore irrecoverable errors
            self._do_error(err)

    def _do_output(self, raw: bytes, parsed: object, handler: object):
        """
        Output message to terminal in specified format(s) OR pass
        to external protocol handler if one is specified.

        :param bytes raw: raw (binary) message
        :param object parsed: parsed message
        :param object handler: Queue, socket or protocol handler (NMEA, UBX or RTCM3)
        """

        self._msgcount += 1

        # stdout (can output multiple formats)
        if handler is None:
            if self._format & FORMAT_PARSED:
                print(parsed)
            if self._format & FORMAT_BINARY:
                print(raw)
            if self._format & FORMAT_HEX:
                print(raw.hex())
            if self._format & FORMAT_HEXTABLE:
                print(hextable(raw))
            if self._format & FORMAT_PARSEDSTRING:
                print(str(parsed))
            return

        # writeable output media (can output one format)
        if self._format == FORMAT_PARSED:
            output = parsed
        elif self._format == FORMAT_PARSEDSTRING:
            output = f"{parsed}\n"
        elif self._format == FORMAT_HEX:
            output = str(raw.hex())
        elif self._format == FORMAT_HEXTABLE:
            output = str(hextable(raw))
        else:
            output = raw
        if isinstance(handler, (Serial, TextIOWrapper, BufferedWriter)):
            handler.write(output)
        elif isinstance(handler, Queue):
            handler.put(output)
        elif isinstance(handler, socket):
            handler.wfile.write(output)
            handler.wfile.flush()
        # treated as evaluable expression
        else:
            handler(output)

    def _do_error(self, err: Exception):
        """
        Handle error according to quitonerror flag;
        either ignore, log, (re)raise or pass to
        external error handler if one is specified.

        :param err Exception: error
        """

        if self._errorhandler is None:
            if self._quitonerror == ERR_RAISE:
                raise err
            if self._quitonerror == ERR_LOG:
                print(err)
        elif isinstance(self._errorhandler, (Serial, BufferedWriter)):
            self._errorhandler.write(err)
        elif isinstance(self._errorhandler, TextIOWrapper):
            self._errorhandler.write(str(err))
        elif isinstance(self._errorhandler, Queue):
            self._errorhandler.put(err)
        elif isinstance(self._errorhandler, socket):
            self._errorhandler.wfile.write(err)
            self._errorhandler.wfile.flush()
        else:
            self._errorhandler(err)
        self._errcount += 1

    def _do_log(self, msg: str, loglevel: int = VERBOSITY_MEDIUM):
        """
        Log output according to verbosity setting.

        :param str msg: log message
        :param int loglevel: min verbosity level for this message
        """

        if msg in ("eof", "user"):
            mss = "" if self._msgcount == 1 else "s"
            ers = "" if self._errcount == 1 else "s"
            pre = (
                "Streaming terminated by user"
                if msg == "user"
                else "End of stream reached"
            )
            msg = f"\n\n{pre}, {self._msgcount:,} message{mss} processed with {self._errcount:,} error{ers}.\n"
        if loglevel <= self._verbosity and self._verbosity > VERBOSITY_LOW:
            print(msg)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream


def main():
    """
    CLI Entry point.

    :param: as per GNSSStreamer constructor.
    :raises: ParameterError if parameters are invalid
    """
    # pylint: disable=raise-missing-from

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(GNSSDUMP_HELP)
            sys.exit()

    try:
        gns = GNSSStreamer(**dict(arg.split("=") for arg in sys.argv[1:]))
        gns.run()
    except ValueError:
        raise ParameterError(f"Invalid parameter(s).\n{GNSSDUMP_HELP}")


if __name__ == "__main__":

    main()
