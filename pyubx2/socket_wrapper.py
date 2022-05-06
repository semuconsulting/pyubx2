"""
socket_wrapper class.

Wraps a socket object and provides stream-like read(bytes) and 
readline() methods.

Created on 4 Apr 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from socket import socket


class socket_wrapper:
    """
    socket wrapper class.
    """

    def __init__(self, socket: socket, *args, **kwargs):
        """
        Constructor.

        :param socket socket: socket object
        """

        self._socket = socket
        self._buffer = bytearray()
        self.recv()  # populate initial buffer

    def recv(self, bufsiz: int = 4096) -> bool:
        """
        Read bytes from socket into internal buffer.

        :param int bufsize: buffer size (defaults to 4096)
        :return: return code (0 = failure, 1 = success)
        :rtype: bool
        """

        try:
            data = self._socket.recv(bufsiz)
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

    @buffer.setter
    def buffer(self, buffer: bytearray):
        """
        Setter for buffer.

        :param bytearray buffer: buffer
        """

        self._buffer = buffer

    def read(self, num: int) -> bytes:
        """
        Read specified number of bytes from buffer.
        NB: always check length of return data.

        :param int num: number of bytes to read
        :return: bytes read (which may be less than num)
        :rtype: bytes
        """

        if len(self._buffer) < num:
            if not self.recv():
                return b""
        data = self._buffer[:num]
        self._buffer = self._buffer[num:]
        return bytes(data)

    def readline(self) -> bytes:
        """
        Read bytes from buffer until CRLF reached.
        NB: always check that return data terminator is CRLF.

        :return: bytes
        :rtype: bytes
        :raises: EOFError
        """

        line = b""
        while True:
            data = self.read(1)
            if len(data) == 1:
                line += data
                if line[-2:] == b"\x0d\x0a":  # CRLF
                    break
            else:
                break

        return line
