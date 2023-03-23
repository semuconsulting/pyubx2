"""
socket_stream class.

A skeleton socket wrapper which provides basic stream-like
read(bytes) and readline() methods.

NB: this will read from a socket indefinitely. It is the
responsibility of the calling application to monitor
data returned and implement appropriate socket error,
timeout or inactivity procedures.

Created on 4 Apr 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from socket import socket


class SocketStream:
    """
    socket stream class.
    """

    def __init__(self, sock: socket, **kwargs):
        """
        Constructor.

        :param sock socket: socket object
        :param int bufsize: (kwarg) internal buffer size (4096)
        """

        self._socket = sock
        self._bufsize = kwargs.get("bufsize", 4096)
        self._buffer = bytearray()
        self._recv()  # populate initial buffer

    def _recv(self) -> bool:
        """
        Read bytes from socket into internal buffer.

        :return: return code (0 = failure, 1 = success)
        :rtype: bool
        """

        try:
            data = self._socket.recv(self._bufsize)
            self._buffer += data
        except (OSError, TimeoutError):
            return False
        return True

    @property
    def buffer(self) -> bytearray:
        """
        Getter for buffer.

        :return: buffer
        :rtype: bytearray
        """

        return self._buffer

    def read(self, num: int) -> bytes:
        """
        Read specified number of bytes from buffer.
        NB: always check length of return data.

        :param int num: number of bytes to read
        :return: bytes read (which may be less than num)
        :rtype: bytes
        """

        # if at end of internal buffer, top it up from socket
        while len(self._buffer) < num:
            if not self._recv():
                return b""
        data = self._buffer[:num]
        self._buffer = self._buffer[num:]
        return bytes(data)

    def readline(self) -> bytes:
        """
        Read bytes from buffer until LF reached.
        NB: always check that return data terminator is LF.

        :return: bytes
        :rtype: bytes
        """

        line = b""
        while True:
            data = self.read(1)
            if len(data) == 1:
                line += data
                if line[-1:] == b"\n":  # LF
                    break
            else:
                break

        return line
