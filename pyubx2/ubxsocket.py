"""
UBXSocket class.

Inherited from the standard socket class. Implements additional read()
methods to facilitate reading from socket in the same way as reading
from serial stream.

Created on 4 Apr 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from socket import socket


class UBXSocket:
    """
    UBX Socket class.
    """

    def __init__(self, socket: socket, *args, **kwargs):
        """
        Constructor.
        """

        self._socket = socket
        self._buffer = bytearray()
        self._bufidx = 0
        self.recv()

    def recv(self, bufsiz: int = 4096) -> bytes:
        """
        Read from socket.
        """

        data = self._socket.recv(bufsiz)
        self._buffer += data

    @property
    def buffer(self) -> bytearray:
        """
        Getter for buffer.
        """

        return self._buffer

    @buffer.setter
    def buffer(self, buffer: bytearray):
        """
        Setter for buffer.
        """

        self._buffer = buffer

    def read(self, num: int) -> bytes:
        """
        Read specified number of bytes from buffer.
        :param int num: number of bytes to read
        :return: bytes read
        :rtype: bytes
        :raises: EOFError
        """

        if len(self._buffer) < num:
            # data = self._buffer
            self.recv()
            # return bytes(data)
        data = self._buffer[:num]
        self._buffer = self._buffer[num:]
        return bytes(data)

    def readline(self) -> bytes:
        """
        Read bytes from buffer until CRLF reached.
        :return: bytes read
        :rtype: bytes
        :raises: EOFError
        """

        print("DEBUG doing UBXSocket readline")
        i = 0
        line = b""
        while True:
            print(f"DEBUG doing UBXSocket readline {i}")
            data = self.read(2 + i)
            line += data
            # if len(data) < (2 + 1) or line[-2:] == b"\x0d\x0a":
            if line[-2:] == b"\x0d\x0a":
                return line
            i += 1
