"""
Command line utility, installed with PyPi library pyubx2,
to stream the parsed UBX and/or NMEA output of a GNSS device
to the terminal or a designated protocol handler.

Created on 15 Jan 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=line-too-long

import sys
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
VERBOSITY_LOW = 0
VERBOSITY_MEDIUM = 1
VERBOSITY_HIGH = 2


class GNSSStreamer:
    """
    GNSS Streamer Class.

    Streams and parses UBX and NMEA GNSS messages from any data stream (e.g. Serial or File) to the terminal
    or to designated NMEA and/or UBX protocol handler(s).

    Input stream is defined via keyword arguments. One of either stream, port or filename MUST be specified.
    The remaining arguments are all optional with defaults.
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
        :param int baudrate: (kwarg) serial baud rate (9600)
        :param int timeout: (kwarg) serial timeout in seconds (3)
        :param int validate: (kwarg) 1 = validate checksums, 0 = do not validate (1)
        :param int msgmode: (kwarg) 0 = GET, 1 = SET, 2 = POLL (0)
        :param int parsebitfield: (kwarg) 1 = parse UBX 'X' attributes as bitfields, 0 = leave as bytes (1)
        :param int format: (kwarg) output format 1 = parsed, 2 = raw, 4 = hex, 8 = tabulated hex (1) (can be OR'd)
        :param int quitonerror: (kwarg) 0 = ignore errors,  1 = log errors and continue, 2 = (re)raise errors (1)
        :param int protfilter: (kwarg) 1 = NMEA, 2 = UBX, 4 = RTCM3 (7 - ALL)
        :param str msgfilter: (kwarg) comma-separated string of message identities e.g. 'NAV-PVT,GNGSA' (None)
        :param int limit: (kwarg) maximum number of messages to read (0 = unlimited)
        :param int verbosity: (kwarg) log message verbosity 0 = low, 1 = medium, 3 = high (1)
        :param object errorhandler: (kwarg) evaluable expression defining external error handler (None)
        :param object nmeahandler: (kwarg) evaluable expression defining external NMEA message handler (None)
        :param object ubxhandler: (kwarg) evaluable expression defining external UBX message handler (None)
        :param object rtcmhandler: (kwarg) evaluable expression defining external RTCM3 message handler (None)
        :raises: ParameterError
        """
        # pylint: disable=raise-missing-from

        self._reader = None
        self._datastream = kwargs.get("datastream", None)
        self._port = kwargs.get("port", None)
        self._filename = kwargs.get("filename", None)
        if self._datastream is None and self._port is None and self._filename is None:
            raise ParameterError(
                f"Either stream, port or filename keyword argument must be provided.\n{GNSSDUMP_HELP}"
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

            # evaluate protocol handler expressions
            # CAUTION assumes expressions are benign
            erh = kwargs.get("errorhandler", None)
            self._errorhandler = None if erh is None else eval(erh)
            nmh = kwargs.get("nmeahandler", None)
            self._nmeahandler = None if nmh is None else eval(nmh)
            ubh = kwargs.get("ubxhandler", None)
            self._ubxhandler = None if ubh is None else eval(ubh)
            rth = kwargs.get("rtcmhandler", None)
            self._rtcmhandler = None if rth is None else eval(rth)

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
        if self._datastream is not None:
            with self._datastream as self._stream:
                self._start_reader()
        elif self._port is not None:
            with Serial(
                self._port, self._baudrate, timeout=self._timeout
            ) as self._stream:
                self._start_reader()
        elif self._filename is not None:
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
        :param object handler: protocol handler (NMEA or UBX)
        """

        if handler is None:
            if self._format & FORMAT_PARSED:
                print(str(parsed))
            if self._format & FORMAT_BINARY:
                print(raw)
            if self._format & FORMAT_HEX:
                print(raw.hex())
            if self._format & FORMAT_HEXTABLE:
                print(hextable(raw))
        else:
            handler(parsed)
        self._msgcount += 1

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
