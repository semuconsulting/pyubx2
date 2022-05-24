"""
gnssserver.py

This is a simple but fully-functional example of a TCP Socket
Server or NTRIP Server which reads the binary data stream from
a connected GNSS receiver and broadcasts the data to any
TCP socket or NTRIP client running on a local or remote
machine (assuming firewalls allow the hostip:port).

Press CTRL-C to stop the server.

The clients must be capable of parsing binary GNSS data.
Suitable clients include (but are not limited to):
1) pyubx2's gnssdump cli utility invoked thus:
   >>> gnssdump socket=hostip:50010
2) The PyGPSClient GUI application, invoked thus:
   >>> pygpsclient

To run in NTRIP Server mode, the receiver should be an
RTK-capable receiver (e.g. u-blox ZED-F9P) running in
"Base Station" mode (either SURVEY_IN or FIXED). The clients
must be NTRIP clients (e.g. PyGPSClient's NTRIP Client
facility). FYI it'll happily run in NTRIP mode with any data
stream but the data would be useless to an NTRIP client
if it's not proper RTCM3 RTK correction data.

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

from queue import Queue
from threading import Thread
from pyubx2cli.gnssdump import GNSSStreamer, FORMAT_BINARY

# If you have PyGPSClient installed, you can import the SocketServer classes from this...
# from pygpsclient.socket_server import SocketServer, ClientHandler

# Otherwise you can use the local copy in /examples/socket_server.py...
from socket_server import SocketServer, ClientHandler


class GNSSStatus:
    """
    GNSS Status class.
    Container for the latest readings from the GNSS receiver.

    THIS IS JUST A STUB FOR THIS EXAMPLE; IN THE ACTUAL PYGPSCLIENT
    IMPLEMENTATION IT STORES THE LATEST LIVE GNSS READINGS
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

    def __init__(
        self, ntripmode: int, hostip: str, inport: str, outport: int, maxclients: int
    ):
        """
        Constructor.
        """

        self._ntripmode = ntripmode  # 0 = TCP Socket server mode, 1 = NTRIP server mode
        self._hostip = hostip
        self._inport = inport
        self._outport = outport
        self._msgqueue = Queue()
        self._maxclients = maxclients
        self._socket_server = None
        self._clients = 0

        self.gnss_status = GNSSStatus()  # stub for compatibility with SocketServer

    def run(self):
        """
        Run server.
        """

        print("Starting server (type CTRL-C to stop)...")
        self.start_input_thread()
        self.start_output_thread()

    def stop(self):
        """
        Shutdown server.
        """

        print("\nStopping server...")
        if self._socket_server is not None:
            self._socket_server.shutdown()

    def start_input_thread(self):
        """
        Start input (read) thread.
        """

        print("Starting input reader thread...")
        thread = Thread(
            target=self._input_thread,
            args=(
                self._inport,
                self._msgqueue,
            ),
            daemon=True,
        )
        thread.start()

    def start_output_thread(self):
        """
        Start output (socket) thread.
        """

        print("Starting socket server thread...")
        thread = Thread(
            target=self._output_thread,
            args=(
                self,
                self._ntripmode,
                self._hostip,
                self._outport,
                self._maxclients,
                self._msgqueue,
            ),
            daemon=True,
        )
        thread.start()

    def _input_thread(self, serialport: str, msgqueue: Queue):
        """
        THREADED

        Input (read) thread.
        """

        # NB: any of the permissible gnssdump kwargs could be used here
        # to configure the data that is actually placed on the message
        # queue. e.g. you could set protfilter=1 to only output NMEA data.
        kwargs = {
            "port": serialport,
            "ubxhandler": msgqueue,
            "nmeahandler": msgqueue,
            "rtcmhandler": msgqueue,
            "format": FORMAT_BINARY,
        }
        gns = GNSSStreamer(**kwargs)
        gns.run()

    def _output_thread(
        self,
        app: object,
        ntripmode: int,
        host: str,
        port: int,
        maxclients: int,
        msgqueue: Queue,
    ):
        """
        THREADED

        Output (socket) thread.
        """

        try:
            with SocketServer(
                app, ntripmode, maxclients, msgqueue, (host, port), ClientHandler
            ) as self._socket_server:
                self._socket_server.serve_forever()
        except OSError as err:
            print(f"Error starting socket server {err}")

    def update_clients(self, clients: int):
        """
        Prints status message showing number of connected clients.
        The SocketServer class invokes this method (if it exists)
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

    ntripmode = 0  # 0 = TCP Socket Server mode, 1 = NTRIP Server mode
    hostip = "0.0.0.0"  # binds to all host IP addresses
    inport = "/dev/tty.usbmodem141301"  # amend as required
    outport = 50010  # amend as required
    maxclients = 5  # arbitrary limit; could be significantly higher

    try:

        server = GNSSServer(ntripmode, hostip, inport, outport, maxclients)
        server.run()

        while True:  # run until user presses CTRL-C
            # While the server is running, you can connect from up to
            # (maxclients) TCP clients running on local or remote machines
            # (assuming the selected port is not blocked by firewalls).
            #
            # Suitable TCP clients include (but are not limited to)
            # pyubx2's gnssdump cli utility or the PyGPSCLient GUI
            # socket client.
            pass

    except KeyboardInterrupt:
        server.stop()
        print("Terminated by user")


if __name__ == "__main__":

    main()
