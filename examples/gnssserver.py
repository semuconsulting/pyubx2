"""
gnssserver.py

This is a simple but fully-functional example of a TCP Socket
Server or NTRIP Server which reads the binary data stream from
a connected GNSS receiver and broadcasts the data to any
TCP socket or NTRIP client running on a local or remote
machine (assuming firewalls allow the hostip:outport).

Settings can be entered as optional command line arguments, e.g.
> python3 gnssserver.py hostip=192.168.0.20 inport="/dev/tty.usbmodem14101" outport=6000
Any arguments not provided will be defaulted;
default hostip = 0.0.0.0 (i.e. binds to all available host IP address)
default inport = "/dev/ttyACM1",
default outport = 50010.

Press CTRL-C to stop the server.

In the default configuration ('format=FORMAT_BINARY'), the clients
must be capable of parsing binary GNSS data.
Suitable clients include (but are not limited to):
1) pyubx2's gnssdump cli utility invoked thus:
   > gnssdump socket=hostip:outport
2) The PyGPSClient GUI application, invoked thus:
   > pygpsclient

To run in NTRIP Server mode, set 'ntripmode=1'. For this mode
to function properly, the receiver must be an RTK-capable receiver
(e.g. u-blox ZED-F9P) running in "Base Station" mode (either
SURVEY_IN or FIXED). The clients must be NTRIP clients (e.g.
PyGPSClient's NTRIP Client facility).
NTRIP server login credentials are set via environment
variables PYGPSCLIENT_USER and PYGPSCLIENT_PASSWORD.


The example essentially runs two (pseudo-)concurrent threads:
- an input thread based on the pyubx2cli.gnssdump.GNSSStreamer
  class from the pyubx2cli gnssdump utility, using a message
  Queue as an external protocol handler.
- an output thread based on the pygpsclient.socket_server
  SocketServer and ClientHandler classes,
  originally designed for the PyGPSClient GUI application.
  (a local copy of the classes is in /examples/socket_server.py
  for those that don't have PYGPSClient installed)

Created on 24 May 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""
# pylint: disable=too-many-arguments

import sys
from queue import Queue
from threading import Thread
from pyubx2cli import GNSSStreamer, FORMAT_BINARY

# If you have PyGPSClient installed, you can import the SocketServer classes from this...
# from pygpsclient.socket_server import SocketServer, ClientHandler

# Otherwise you can use the local copy in /examples/socket_server.py...
from socket_server import SocketServer, ClientHandler


class GNSSStatus:
    """
    GNSS Status class.
    Container for the latest readings from the GNSS receiver.

    THIS IS JUST A STUB FOR THIS EXAMPLE; In a full-blown
    NTRIP server, the lat/lon can be used to populate the mountpoint
    coordinates in the sourcetable. You can set arbitrary fixed
    values rather than 0.0 here if you prefer.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self):
        """
        Constructor.
        """

        self.lat = 0.0  # latitude as decimal
        self.lon = 0.0  # longitude as decimal


class GNSSServer:
    """
    GNSS Server Class.
    """

    def __init__(self, **kwargs):
        """
        Constructor.
        """

        try:

            self._kwargs = kwargs
            # overrideable command line arguments..
            # 0 = TCP Socket Server mode, 1 = NTRIP Server mode
            self._kwargs["ntripmode"] = int(kwargs.get("ntripmode", 0))
            # 0.0.0.0 binds to all host IP addresses
            self._kwargs["hostip"] = kwargs.get("hostip", "0.0.0.0")
            # amend default as required
            self._kwargs["port"] = kwargs.get("inport", "/dev/ttyACM1")
            self._kwargs["outport"] = int(kwargs.get("outport", 50010))
            # 5 is an arbitrary limit; could be significantly higher
            self._kwargs["maxclients"] = int(kwargs.get("maxclients", 5))

            # required fixed arguments...
            self._kwargs["format"] = FORMAT_BINARY
            msgqueue = Queue()
            self._kwargs["ubxhandler"] = msgqueue
            self._kwargs["nmeahandler"] = msgqueue
            self._kwargs["rtcmhandler"] = msgqueue
            self._socket_server = None
            self._clients = 0
            self._validargs = True

            self.gnss_status = GNSSStatus()  # stub for compatibility with SocketServer

        except ValueError as err:
            print(f"Invalid input arguments {kwargs}\n{err}")
            self._validargs = False

    def run(self) -> int:
        """
        Run server.
        """

        if self._validargs:
            print("Starting server (type CTRL-C to stop)...")
            self.start_input_thread(**self._kwargs)
            self.start_output_thread(**self._kwargs)
            return 1
        return 0

    def stop(self):
        """
        Shutdown server.
        """

        print("\nStopping server...")
        if self._socket_server is not None:
            self._socket_server.shutdown()

    def start_input_thread(self, **kwargs):
        """
        Start input (read) thread.
        """

        print(f"Starting input thread, reading from {kwargs['port']}...")
        thread = Thread(
            target=self._input_thread,
            args=(kwargs,),
            daemon=True,
        )
        thread.start()

    def start_output_thread(self, **kwargs):
        """
        Start output (socket) thread.
        """

        print(
            f"Starting output thread, broadcasting on {kwargs['hostip']}:{kwargs['outport']}..."
        )
        thread = Thread(
            target=self._output_thread,
            args=(
                self,
                kwargs,
            ),
            daemon=True,
        )
        thread.start()

    def _input_thread(self, kwargs):
        """
        THREADED

        Input (Serial reader) thread.
        """

        # FYI: any of the permissible gnssdump kwargs could be passed here
        # from command line arguments to configure the data that is
        # actually broadcast to the clients, e.g. you could set
        # 'protfilter=4' to only output RTCM data, or 'msgfilter=NAV-PVT'
        # to only output UBX NAV-PVT messages.
        # type gnssdump -h for help.

        gns = GNSSStreamer(**kwargs)
        gns.run()

    def _output_thread(self, app: object, kwargs):
        """
        THREADED

        Output (socket server) thread.
        """

        try:
            with SocketServer(
                app,
                kwargs["ntripmode"],
                kwargs["maxclients"],
                kwargs["ubxhandler"],
                (kwargs["hostip"], kwargs["outport"]),
                ClientHandler,
            ) as self._socket_server:
                self._socket_server.serve_forever()
        except OSError as err:
            print(f"Error starting socket server {err}")

    def update_clients(self, clients: int):
        """
        Prints status message showing number of connected clients.
        The SocketServer object invokes this method (if implemented)
        whenever a client connects or disconnects.

        :param int clients: no of connected clients
        """

        if clients > self._clients:
            print("Client has connected. ", end="")
        else:
            print("Client has disconnected. ", end="")
        print(f"Total clients: {clients}")
        self._clients = clients


def main():
    """
    CLI Entry point.
    """

    try:

        server = GNSSServer(**dict(arg.split("=") for arg in sys.argv[1:]))
        goodtogo = server.run()

        while goodtogo:  # run until user presses CTRL-C
            pass

    except KeyboardInterrupt:
        server.stop()
        print("Terminated by user")


if __name__ == "__main__":

    main()
