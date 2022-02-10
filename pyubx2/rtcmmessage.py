"""
Stub RTCM3 Message Protocol Class.

NB: pyubx2 does not currently decode RTCM3 data; we
simply read the complete RTCM3 message and package
the raw payload as a stub RTCMMessage object.

RTCM3 transport layer bit format:
+-------+--------+--------+--------+----------------+--------+
| 0xd3  | 000000 | length |  type  |    content     |  crc   |
+-------+--------+--------+--------+----------------+--------+
|<- 8 ->|<- 6 -->|<- 10 ->|<- 12 ->|<-- variable -->|<- 24 ->|
                          |<----- length x 8 ------>|

Created on 10 Feb 2022

:author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""


class RTCMMessage:
    """RTCM Stub Message Class."""

    def __init__(self, payload: bytes):
        """Constructor.

        :param bytes payload: message payload
        """

        self.payload = payload
        self.identity = str(payload[0] << 4 | payload[1] >> 4)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str
        """

        return f"<RTCM({self.identity})>"
