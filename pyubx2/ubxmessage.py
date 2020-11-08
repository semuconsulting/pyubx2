"""
UBX Message Protocol Class

Created on 26 Sep 2020

@author: semuadmin
"""
# pylint: disable=invalid-name

import struct
from datetime import datetime, timedelta

import pyubx2.exceptions as ube
import pyubx2.ubxtypes_core as ubt
import pyubx2.ubxtypes_get as ubg
import pyubx2.ubxtypes_set as ubs
import pyubx2.ubxtypes_poll as ubp


class UBXMessage:
    """UBX Message Class."""

    def __init__(self, ubxClass, ubxID, mode: int, **kwargs):
        """Constructor.

        If no keyword parms are passed, the payload is taken to be empty.

        If 'payload' is passed as a keyword parm, this is taken to contain the complete
        payload as a sequence of bytes; any other keyword parms are ignored.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param msgClass: str, int or byte:
        :param msgID: str, int or byte:
        :param mode: int:
        :param kwargs:

        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self._header = ubt.UBX_HDR
        self._mode = mode
        self._index = 0
        self._payload = b""
        self._length = b""
        self._checksum = b""

        # accommodate different formats of msgClass and msgID
        if isinstance(ubxClass, str) and isinstance(
            ubxID, str
        ):  # string e.g. 'CFG', 'CFG-PRT'
            # print(f"parms are strings {ubxClass} {ubxID}")
            (self._ubxClass, self._ubxID) = UBXMessage.msgstr2bytes(ubxClass, ubxID)
        elif isinstance(ubxClass, int) and isinstance(ubxID, int):  # int e.g. 6, 1
            # print(f"parms are integers {ubxClass} {ubxID}")
            (self._ubxClass, self._ubxID) = UBXMessage.msgclass2bytes(ubxClass, ubxID)
        else:  # bytes e.g. b'\x06', b'\x01'
            # print(f"parms are bytes {ubxClass} {ubxID}")
            self._ubxClass = ubxClass
            self._ubxID = ubxID

        self._do_attributes(**kwargs)

        # once initialised, object is immutable
        self._immutable = True

    def _do_attributes(self, **kwargs):
        """Populate UBXMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param **kwargs:

        """

        offset = 0

        try:

            if len(kwargs) == 0:  # if no kwargs, assume null payload
                self._payload = None
            else:
                pdict = self._get_dict(**kwargs)  # get appropriate payload dict
                for key in pdict.keys():  # set each attribute in dict
                    (offset, att) = self._set_attribute(offset, pdict, key, **kwargs)
            self._do_len_checksum()

        except (
            AttributeError,
            OverflowError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise ube.UBXTypeError(
                (
                    f"Incorrect type for attribute '{key}' "
                    f"in {self.mode2str(self._mode)} message "
                    f"class {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, offset: int, pdict: dict, key: str, **kwargs
    ) -> (int, str):
        """Recursive routine to populate individual payload attributes

        :param offset: int:
        :param pdict: dict:
        :param key: str:
        :param **kwargs:

        """
        # pylint: disable=no-member

        #  if repeating group, suffix keyword with index
        if self._index > 0:
            keyr = key + "_{0:0=2d}".format(self._index)
        else:
            keyr = key

        att = pdict[key]  # get attribute type
        if isinstance(att, tuple):  # attribute is a tuple i.e. a nested repeating group
            numr, attd = att
            if numr == "None":
                rng = self._calc_num_repeats(attd, self._payload, offset)
            else:
                rng = getattr(self, numr)
            for i in range(rng):
                self._index = i + 1
                for key1 in attd.keys():
                    (offset, _) = self._set_attribute(offset, attd, key1, **kwargs)

        else:

            if att == ubt.CH:  # INF message payload
                atts = len(self._payload)
            else:
                atts = int(att[1:3])

            # if the entire payload has been provided,
            # use the appropriate section of the payload
            if "payload" in kwargs:
                self._payload = kwargs["payload"]
                val = self._payload[offset : offset + atts]
                if (
                    att == ubt.CH
                ):  # attribute is a single variable-length string (e.g. INF-NOTICE)
                    val = self._payload.decode("utf-8", "backslashreplace")
                elif att[0:1] in ("X", "C"):
                    pass
                elif att[0:1] == "U":  # unsigned integer
                    val = int.from_bytes(val, "little", signed=False)
                elif att[0:1] == "I":  # signed integer
                    val = int.from_bytes(val, "little", signed=True)
                elif att == ubt.R4:  # single precision floating point
                    val = self.bytes_to_float(val)
                elif att == ubt.R8:  # double precision floating point
                    val = self.bytes_to_double(val)
                else:
                    raise ube.UBXTypeError(
                        f"Unknown attribute type {att} for key {key}"
                    )

            # else if individual attribute has been provided
            elif keyr in kwargs:
                val = kwargs[keyr]
                if att[0:1] in ("X", "C"):  # byte or char
                    valb = val
                elif att[0:1] == "U":  # unsigned integer
                    valb = val.to_bytes(atts, byteorder="little", signed=False)
                elif att[0:1] == "I":  # signed integer
                    valb = val.to_bytes(atts, byteorder="little", signed=True)
                elif att == ubt.R4:  # single precision floating point
                    valb = self.float_to_bytes(val)
                elif att == ubt.R8:  # double precision floating point
                    valb = self.double_to_bytes(val)
                else:
                    raise ube.UBXTypeError(
                        f"Unknown attribute type {att} for key {key}"
                    )
                self._payload += valb

            # else set individual attribute to nominal value
            else:
                if att[0:1] in ("X", "C"):  # byte or char
                    valb = b"\x00" * atts
                    val = valb
                elif att[0:1] == "U":  # unsigned integer
                    val = 0
                    valb = val.to_bytes(atts, byteorder="little", signed=False)
                elif att[0:1] == "I":  # signed integer
                    val = 0
                    valb = val.to_bytes(atts, byteorder="little", signed=True)
                elif att == ubt.R4:  # single precision floating point
                    val = 0.0
                    valb = self.float_to_bytes(val)
                elif att == ubt.R8:  # double precision floating point
                    val = 0.0
                    valb = self.double_to_bytes(val)
                else:
                    raise ube.UBXTypeError(
                        f"Unknown attribute type {att} for key {key}"
                    )
                self._payload += valb

        if not isinstance(att, tuple):
            if self._index > 0:  # add 2-digit suffix to repeating attribute names
                key = key + "_{0:0=2d}".format(self._index)
            setattr(self, key, val)
            offset += atts

        return (offset, att)

    def _do_len_checksum(self):
        """Calculate and format payload length and checksum as bytes"""

        if self._payload is None:
            self._length = self.len2bytes(0)
            self._checksum = self.calc_checksum(
                self._ubxClass + self._ubxID + self._length
            )
        else:
            self._length = self.len2bytes(len(self._payload))
            self._checksum = self.calc_checksum(
                self._ubxClass + self._ubxID + self._length + self._payload
            )

    def _get_dict(self, **kwargs) -> dict:
        """Get payload dictionary corresponding to message mode

        :return dict:

        """

        if self._mode == ubt.POLL:
            pdict = ubp.UBX_PAYLOADS_POLL[self.identity]
        elif self._mode == ubt.SET:
            pdict = ubs.UBX_PAYLOADS_SET[self.identity]
        else:
            if self._ubxClass == b"\x13" and self._ubxID != b"\x80":  # MGA message
                pdict = self._get_mga_version(**kwargs)
            elif self.identity == "CFG-NMEA":
                pdict = self._get_cfgnmea_version(**kwargs)
            else:
                pdict = ubg.UBX_PAYLOADS_GET[self.identity]
        return pdict

    def _get_mga_version(self, **kwargs) -> dict:
        """
        Select appropriate MGA payload definition

         :return dict:

        """

        typ = kwargs["payload"][0:1]
        identity = ubt.UBX_MSGIDS[self._ubxClass + self._ubxID + typ]
        pdict = ubg.UBX_PAYLOADS_GET[identity]
        return pdict

    def _get_cfgnmea_version(self, **kwargs) -> dict:
        """
        Selects appropriate payload definition version for older
        generations of CFG-NMEA message

        :return dict:

        """

        lpd = len(kwargs["payload"])
        if lpd == 4:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEAvX"]
        elif lpd == 12:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEAv0"]
        else:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEA"]
        return pdict

    def _calc_num_repeats(self, att, payload: bytes, offset: int) -> int:
        """Deduce number of items in repeating group by dividing length of
        remaining payload by length of group.

        NB: this assumes the repeating group is always at the end of the
        payload, which is true for all currently supported message types
        but may change in the future.

        :param att:
        :param payload : bytes:
        :param offset: int:

        """
        # pylint: disable=no-self-use

        lenpayload = len(payload) - offset
        lengroup = 0
        for _, val in att.items():
            lengroup += int(val[1:3])
        return int(lenpayload / lengroup)

    def __str__(self) -> str:
        """Human readable representation.

        :return: str:

        """

        clsid = None

        umsg_name = self.identity
        if self.payload is None:
            return f"<UBX({umsg_name})>"

        stg = f"<UBX({umsg_name}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                # if the attributes include a UBX class & id,
                # show the ASCII lookup form rather than the binary
                if att[0:6] == "gnssId":  # attribute is a GNSS ID
                    val = self.gnss2str(val)  # get string representation e.g. 'GPS'
                if att == "nmeaVersion":  # attribute is NMEA version
                    val = self.nmeaver2str(val)
                if att == "iTOW":
                    val = self.itow2utc(val)
                # if it's an ACK-ACK or ACK-NAK, we show what it's acknowledging in plain text
                if self._ubxClass == b"\x05":  # ACK
                    if att == "clsID":
                        clsid = val.to_bytes(1, byteorder="little", signed=False)
                        val = ubt.UBX_CLASSES[clsid]
                    if att == "msgID" and clsid:
                        msgid = val.to_bytes(1, byteorder="little", signed=False)
                        val = ubt.UBX_MSGIDS[clsid + msgid]
                # if it's a CFG-MSG, we show what message class/id it refers to in plain text
                if self._ubxClass == b"\x06" and self._ubxID == b"\x01":  # CFG-MSG
                    if att == "msgClass":
                        clsid = val.to_bytes(1, byteorder="little", signed=False)
                        val = ubt.UBX_CONFIG_CATEGORIES[clsid]
                    if att == "msgID" and clsid:
                        msgid = val.to_bytes(1, byteorder="little", signed=False)
                        val = ubt.UBX_CONFIG_MESSAGES[clsid + msgid]
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """Machine readable representation.

        eval(repr(obj)) = obj

        :return str:

        """

        if self._payload is None:
            return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode})"
        return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode}, payload={self._payload})"

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation
        """

        if self._immutable:
            raise ube.UBXMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """Serialize message

        :return bytes:

        """

        if self._payload is None:
            return (
                ubt.UBX_HDR
                + self._ubxClass
                + self._ubxID
                + self._length
                + self._checksum
            )
        return (
            ubt.UBX_HDR
            + self._ubxClass
            + self._ubxID
            + self._length
            + self._payload
            + self._checksum
        )

    @property
    def identity(self) -> str:
        """Message identity getter.
        Returns identity in plain text form e.g. 'CFG-MSG'.

        :return identity: str:

        """

        # all MGA messages except MGA-DBD need to be identified by the
        # 'type' attribute - the first byte of the payload
        if self._ubxClass == b"\x13" and self._ubxID != b"\x80":
            umsg_name = ubt.UBX_MSGIDS[
                self._ubxClass + self._ubxID + self._payload[0:1]
            ]
        else:
            umsg_name = ubt.UBX_MSGIDS[self._ubxClass + self._ubxID]

        return umsg_name

    @property
    def header(self) -> bytes:
        """Header getter"""
        return self._header

    @property
    def msg_cls(self) -> bytes:
        """Class id getter"""
        return self._ubxClass

    @property
    def msg_id(self) -> bytes:
        """Message id getter"""
        return self._ubxID

    @property
    def length(self) -> bytes:
        """Payload length getter (as 2 little-endian bytes)"""
        return self._length

    @property
    def payload(self) -> bytes:
        """Payload getter - returns the raw payload bytes"""
        return self._payload

    @staticmethod
    def parse(message: bytes, validate: bool = False) -> object:
        """Parse UBX byte stream to UBXMessage object.

        Includes option to validate incoming payload length and checksum
        (UXBMessage will calculate and assign it's own values anyway).

        :param message: bytes:
        :param validate: bool:  (Default value = False)

        """

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
            ckv = UBXMessage.calc_checksum(clsid + msgid + lenb + payload)
        else:
            ckv = UBXMessage.calc_checksum(clsid + msgid + lenb)
        if validate:
            if hdr != ubt.UBX_HDR:
                raise ube.UBXParseError(
                    (f"Invalid message header {hdr}" f" - should be {ubt.UBX_HDR}")
                )
            if leni != UBXMessage.bytes2len(lenb):
                raise ube.UBXParseError(
                    (
                        f"Invalid payload length {lenb}"
                        f" - should be {UBXMessage.len2bytes(leni)}"
                    )
                )
            if ckm != ckv:
                raise ube.UBXParseError(
                    (f"Message checksum {ckm}" f" invalid - should be {ckv}")
                )
        if payload is None:
            return UBXMessage(clsid, msgid, ubt.GET)
        return UBXMessage(clsid, msgid, ubt.GET, payload=payload)

    @staticmethod
    def msgclass2bytes(msgClass: int, msgID: int) -> bytes:
        """Convert message class/id integers to bytes
        e.g. 6, 1 to b'/x06/x01'.

        :param msgClass: int:
        :param msgID: int:

        """

        msgClass = msgClass.to_bytes(1, byteorder="little", signed=False)
        msgID = msgID.to_bytes(1, byteorder="little", signed=False)
        return (msgClass, msgID)

    @staticmethod
    def msgstr2bytes(msgClass: str, msgID: str) -> bytes:
        """Convert plain text UBX message class to bytes
        e.g. 'CFG-MSG' to b'/x06/x01'.

        :param msgClass: str:
        :param msgID: str:

        """

        try:
            clsid = UBXMessage.key_from_val(ubt.UBX_CLASSES, msgClass)
            msgid = UBXMessage.key_from_val(ubt.UBX_MSGIDS, msgID)[1:]
            return (clsid, msgid)
        except ube.UBXMessageError as err:
            raise ube.UBXMessageError(
                f"Undefined message, class {msgClass}, id {msgID}"
            ) from err

    @staticmethod
    def bytes_to_float(b: bytes) -> float:
        """Convert 4 little-endian bytes (R4) to single precision decimal (IEEE754)

        :param b: bytes:
        :return float:

        """

        return struct.unpack("<f", b)[0]

    @staticmethod
    def bytes_to_double(b: bytes) -> float:
        """Convert 8 little-endian bytes (R8) to double precision decimal (IEEE754)

        :param b: bytes:
        :return float:

        """

        return struct.unpack("<d", b)[0]

    @staticmethod
    def float_to_bytes(f: float) -> bytes:
        """Convert single precision decimal to 4 little-endian bytes (R4) (IEEE754)

        :param f: float:
        :return float:

        """

        return struct.pack("<f", f)

    @staticmethod
    def double_to_bytes(f: float) -> bytes:
        """Convert double precision decimal to 8 little-endian bytes (R8) (IEEE754)

        :param f: float:
        :return bytes:

        """

        return struct.pack("<d", f)

    @staticmethod
    def bytes2len(length: bytes) -> int:
        """Convert payload length as bytes to integer.

        :param length: bytes:
        :return int:

        """

        return int.from_bytes(length, "little", signed=False)

    @staticmethod
    def len2bytes(length: int) -> bytes:
        """Convert payload length as integer to two little-endian bytes.

        :param length: int:
        :return bytes:

        """

        return length.to_bytes(2, byteorder="little", signed=False)

    @staticmethod
    def calc_checksum(content: bytes) -> bytes:
        """

        :param content: bytes:
        :return checksum: bytes:

        """

        check_a = 0
        check_b = 0

        for char in content:
            check_a += char
            check_a &= 0xFF
            check_b += check_a
            check_b &= 0xFF

        return bytes((check_a, check_b))

    @staticmethod
    def isvalid_checksum(message: bytes) -> bool:
        """Validate input message's checksum
        ('message' includes header and checksum)

        :param message: bytes:
        :return bool:

        """

        lenm = len(message)
        ckm = message[lenm - 2 : lenm]
        return ckm == UBXMessage.calc_checksum(message[2 : lenm - 2])

    @staticmethod
    def itow2utc(iTOW: int) -> datetime.time:
        """Convert UBX iTOW to UTC time

        :param iTOW: int:
        :return datetime.time:

        """

        utc = datetime(1980, 1, 6) + timedelta(seconds=(iTOW / 1000) - (35 - 19))
        return utc.time()

    @staticmethod
    def gpsfix2str(fix: int) -> str:
        """Converts GPS fix integer to string

        :param fix: int:
        :return str:

        """

        if fix == 5:
            fixs = "TIME ONLY"
        elif fix == 4:
            fixs = "GPS + DR"
        elif fix == 3:
            fixs = "3D"
        elif fix == 2:
            fixs = "2D"
        elif fix == 1:
            fixs = "DR"
        else:
            fixs = "NO FIX"
        return fixs

    @staticmethod
    def dop2str(dop: float) -> str:
        """Converts DOP float to descriptive string

        :param dop: float:
        :return str:

        """

        if dop == 1:
            dops = "Ideal"
        elif dop <= 2:
            dops = "Excellent"
        elif dop <= 5:
            dops = "Good"
        elif dop <= 10:
            dops = "Moderate"
        elif dop <= 20:
            dops = "Fair"
        else:
            dops = "Poor"
        return dops

    @staticmethod
    def gnss2str(gnssId: int) -> str:
        """Converts GNSS ID to descriptive string

        :param gnssId: int:
        :return str:

        """

        try:
            return ubt.GNSSLIST[gnssId]
        except KeyError:
            return str(gnssId)

    @staticmethod
    def nmeaver2str(nmeaVersion: int) -> str:
        """Converts NMEA version integer to readable string

        :param nmeaVersion: int:
        :return str:

        """

        h = hex(nmeaVersion)
        return h[2:3] + "." + h[3:]

    @staticmethod
    def mode2str(mode: int) -> str:
        """Convert mode to string"""

        return ["GET", "SET", "POLL"][mode]

    @staticmethod
    def key_from_val(dictionary: dict, value) -> str:
        """Helper method - get dictionary key corresponding to (unique) value.

        :param dictionary: dict:
        :param value:
        :return str:

        """

        val = None
        for key, val in dictionary.items():
            if val == value:
                return key
        raise ube.UBXMessageError(f"Undefined message type {value}")
