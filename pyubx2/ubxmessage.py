"""
UBX Message Protocol Class

Created on 26 Sep 2020

@author: semuadmin
"""
# pylint: disable=invalid-name

import struct
import pyubx2.exceptions as ube
import pyubx2.ubxtypes_core as ubt
import pyubx2.ubxtypes_get as ubg
import pyubx2.ubxtypes_set as ubs
import pyubx2.ubxtypes_poll as ubp
import pyubx2.ubxtypes_configdb as ubcdb
from pyubx2.ubxhelpers import atttyp, attsiz, itow2utc, gnss2str, key_from_val


class UBXMessage:
    """UBX Message Class."""

    def __init__(self, ubxClass, ubxID, mode: int, **kwargs):
        """Constructor.

        If no keyword parms are passed, the payload is taken to be empty.

        If 'payload' is passed as a keyword parm, this is taken to contain the complete
        payload as a sequence of bytes; any other keyword parms are ignored.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param object msgClass: str, int or byte:
        :param object msgID: str, int or byte:
        :param int mode: SET, GET or POLL
        :param kwargs: payload key value pairs
        :raise UBXMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self._mode = mode
        self._payload = b""
        self._length = b""
        self._checksum = b""

        if mode not in (0, 1, 2):
            raise ube.UBXMessageError(f"Invalid mode {mode} - must be 0, 1 or 2")

        # accommodate different formats of msgClass and msgID
        if isinstance(ubxClass, str) and isinstance(
            ubxID, str
        ):  # string e.g. 'CFG', 'CFG-PRT'
            (self._ubxClass, self._ubxID) = UBXMessage.msgstr2bytes(ubxClass, ubxID)
        elif isinstance(ubxClass, int) and isinstance(ubxID, int):  # int e.g. 6, 1
            (self._ubxClass, self._ubxID) = UBXMessage.msgclass2bytes(ubxClass, ubxID)
        else:  # bytes e.g. b'\x06', b'\x01'
            self._ubxClass = ubxClass
            self._ubxID = ubxID

        self._do_attributes(**kwargs)
        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate UBXMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param **kwargs: payload key value pairs
        :raise UBXTypeError
        """

        offset = 0  # payload offset in bytes
        index = []  # array of (nested) group indices

        try:

            if len(kwargs) == 0:  # if no kwargs, assume null payload
                self._payload = None
            else:
                self._payload = kwargs.get("payload", b"")
                pdict = self._get_dict(**kwargs)  # get appropriate payload dict
                for key in pdict.keys():  # process each attribute in dict
                    (offset, index) = self._set_attribute(
                        offset, pdict, key, index, **kwargs
                    )
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
                    f"in {['GET', 'SET', 'POLL'][self._mode]} message "
                    f"class {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, offset: int, pdict: dict, key: str, index: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param int offset: payload offset
        :param dict pdict: dict representing payload definition
        :param str key: attribute keyword
        :param list index: repeating group index array
        :param **kwargs: payload key value pairs
        :return (offset, index[])
        :rtype tuple
        """

        att = pdict[key]  # get attribute type
        if isinstance(att, tuple):  # repeating group of attributes
            (offset, index) = self._set_attribute_group(att, offset, index, **kwargs)
        else:  # single attribute
            offset = self._set_attribute_single(att, offset, key, index, **kwargs)

        return (offset, index)

    def _set_attribute_group(
        self, att: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple att: tuple of (num repeats, attribute dict)
        :param int offset: payload offset
        :param list index: repeating group index array
        :param **kwargs: payload key value pairs
        :return (offset, index[])
        :rtype tuple
        """

        index.append(0)  # add a (nested) group index
        numr, attd = att  # number of repeats, attribute dictionary
        # if CFG-VALGET message, use dedicated method to
        # parse as configuration key value pairs
        if (
            self._ubxClass == b"\x06"
            and self._ubxID == b"\x8b"
            and self._mode == ubt.GET
        ):
            self._set_cfgval_attributes(offset, **kwargs)
        else:
            # derive or retrieve number of items in group
            if isinstance(numr, int):  # fixed number of repeats
                rng = numr
            elif numr == "None":  # number of repeats 'variable by size'
                rng = self._calc_num_repeats(attd, self._payload, offset, 0)
            elif numr == "ESF-MEAS-CT":  # special handling for ESF-MEAS
                rng = self._calc_num_repeats(attd, self._payload, offset, 4)
            else:  # number of repeats is defined in named attribute
                rng = getattr(self, numr)
            # recursively process each group attribute,
            # incrementing the payload offset and index as we go
            for i in range(rng):
                index[-1] = i + 1
                for key1 in attd.keys():
                    (offset, index) = self._set_attribute(
                        offset, attd, key1, index, **kwargs
                    )

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_single(
        self, att: str, offset: int, key: str, index: list, **kwargs
    ) -> int:
        """
        Set individual attribute value.

        :param str att: attribute type e.g. 'U002'
        :param int offset: payload offset
        :param str key: attribute keyword
        :param list index: repeating group index array
        :param **kwargs: payload key value pairs
        :return offset
        :rtype int
        """
        # pylint: disable=no-member

        # if attribute is part of a (nested) repeating group, suffix name with index
        keyr = key
        for i in index:  # one index for each nested level
            if i > 0:
                keyr = keyr + "_{0:0=2d}".format(i)

        # determine attribute size (bytes)
        if att == ubt.CH:  # variable length string
            atts = len(self._payload)
        else:
            atts = attsiz(att)

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            valb = self._payload[offset : offset + atts]
            val = self.bytes2val(valb, att)
        else:
            # if individual attribute keyword has been provided
            if keyr in kwargs:
                val = kwargs[keyr]
            # else set attribute to nominal value (0)
            else:
                if atttyp(att) in ("X", "C"):  # byte or char
                    val = b"\x00" * atts
                else:
                    val = 0
            valb = self.val2bytes(val, att)
            self._payload += valb

        setattr(self, keyr, val)
        offset += atts

        return offset

    def _set_cfgval_attributes(self, offset: int, **kwargs):
        """
        Parse CFG-VALGET payload to set of configuration
        key value pairs.

        :param int offset: payload offset
        :param **kwargs:  payload key value pairs
        :raise UBXMessageError
        """

        KEYLEN = 4
        if "payload" in kwargs:
            self._payload = kwargs["payload"]
        else:
            raise ube.UBXMessageError(
                "CFG-VALGET message definitions must include payload keyword"
            )
        cfglen = len(self._payload[offset:])

        i = 0
        while offset < cfglen:
            if i == KEYLEN:
                key = int.from_bytes(
                    self._payload[offset : offset + KEYLEN], "little", signed=False
                )
                (keyname, att) = self.cfgkey2name(key)
                atts = attsiz(att)
                valb = self._payload[offset + KEYLEN : offset + KEYLEN + atts]
                val = self.bytes2val(valb, att)
                setattr(self, keyname, val)
                i = 0
                offset += KEYLEN + atts

            else:
                i += 1

    def _do_len_checksum(self):
        """
        Calculate and format payload length and checksum as bytes."""

        if self._payload is None:
            self._length = self.val2bytes(0, ubt.U2)
            self._checksum = self.calc_checksum(
                self._ubxClass + self._ubxID + self._length
            )
        else:
            self._length = self.val2bytes(len(self._payload), ubt.U2)
            self._checksum = self.calc_checksum(
                self._ubxClass + self._ubxID + self._length + self._payload
            )

    def _get_dict(self, **kwargs) -> dict:
        """
        Get payload dictionary corresponding to message mode (GET/SET/POLL)
        Certain message types need special handling as alternate payload
        definitions exist for the same ubxClass/ubxID.

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        """

        if self._mode == ubt.POLL:
            pdict = ubp.UBX_PAYLOADS_POLL[self.identity]
        elif self._mode == ubt.SET:
            if self._ubxClass == b"\x13" and self._ubxID != b"\x80":  # MGA SET
                pdict = self._get_mga_version(ubt.SET, **kwargs)
            elif self._ubxClass == b"\x02" and self._ubxID == b"\x41":  # RXM-PMREQ SET
                pdict = self._get_rxmpmreq_version(**kwargs)
            else:
                pdict = ubs.UBX_PAYLOADS_SET[self.identity]
        else:  # GET message
            if self._ubxClass == b"\x13" and self._ubxID != b"\x80":  # MGA GET
                pdict = self._get_mga_version(ubt.GET, **kwargs)
            elif self._ubxClass == b"\x02" and self._ubxID == b"\x72":  # RXM-PMP
                pdict = self._get_rxmpmp_version(**kwargs)
            elif self._ubxClass == b"\x02" and self._ubxID == b"\x59":  # RXM-RLM
                pdict = self._get_rxmrlm_version(**kwargs)
            elif self._ubxClass == b"\x06" and self._ubxID == b"\x17":  # CFG-NMEA
                pdict = self._get_cfgnmea_version(**kwargs)
            elif self._ubxClass == b"\x10" and self._ubxID == b"\x02":  # ESF-MEAS
                pdict = self._get_esfmeas_version(**kwargs)
            else:
                pdict = ubg.UBX_PAYLOADS_GET[self.identity]
        return pdict

    def _get_mga_version(self, mode: int, **kwargs) -> dict:
        """
        Select appropriate MGA payload definition by checking
        value of 'type' attribute (1st byte of payload).

        :param str mode: 0=GET, 1=SET, 2=POLL
        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """

        if "type" in kwargs:
            typ = self.val2bytes(kwargs["type"], ubt.U1)
        elif "payload" in kwargs:
            typ = kwargs["payload"][0:1]
        else:
            raise ube.UBXMessageError(
                "MGA message definitions must include type or payload keyword"
            )
        identity = ubt.UBX_MSGIDS[self._ubxClass + self._ubxID + typ]
        if mode == ubt.SET:
            pdict = ubs.UBX_PAYLOADS_SET[identity]
        else:
            pdict = ubg.UBX_PAYLOADS_GET[identity]
        return pdict

    def _get_rxmpmreq_version(self, **kwargs) -> dict:
        """
        Select appropriate RXM-PMREQ payload definition by checking
        the 'version' keyword or payload length.

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """
        # pylint: disable=no-self-use

        lpd = 0
        if "version" in kwargs:  # assume longer version
            lpd = 16
        elif "payload" in kwargs:
            lpd = len(kwargs["payload"])
        else:
            raise ube.UBXMessageError(
                "RXM-PMREQ message definitions must include version or payload keyword"
            )
        if lpd == 16:
            pdict = ubs.UBX_PAYLOADS_SET["RXM-PMREQ"]  # long
        else:
            pdict = ubs.UBX_PAYLOADS_SET["RXM-PMREQ-S"]  # short
        return pdict

    def _get_rxmpmp_version(self, **kwargs) -> dict:
        """
        Select appropriate RXM-PMP payload definition by checking
        value of 'version' attribute (1st byte of payload).

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """
        # pylint: disable=no-self-use

        if "version" in kwargs:
            ver = self.val2bytes(kwargs["version"], ubt.U1)
        elif "payload" in kwargs:
            ver = kwargs["payload"][0:1]
        else:
            raise ube.UBXMessageError(
                "RXM-PMP message definitions must include version or payload keyword"
            )
        if ver == b"\x00":
            pdict = ubg.UBX_PAYLOADS_GET["RXM-PMP-V0"]
        else:
            pdict = ubg.UBX_PAYLOADS_GET["RXM-PMP-V1"]
        return pdict

    def _get_rxmrlm_version(self, **kwargs) -> dict:
        """
        Select appropriate RXM-PMP payload definition by checking
        value of 'type' attribute (2nd byte of payload).

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """
        # pylint: disable=no-self-use

        if "type" in kwargs:
            typ = self.val2bytes(kwargs["type"], ubt.U1)
        elif "payload" in kwargs:
            typ = kwargs["payload"][1:2]
        else:
            raise ube.UBXMessageError(
                "RXM-RLM message definitions must include type or payload keyword"
            )
        if typ == b"\x01":
            pdict = ubg.UBX_PAYLOADS_GET["RXM-RLM-S"]  # short
        else:
            pdict = ubg.UBX_PAYLOADS_GET["RXM-RLM-L"]  # long
        return pdict

    def _get_cfgnmea_version(self, **kwargs) -> dict:
        """
        Select appropriate payload definition version for older
        generations of CFG-NMEA message by checking payload length.

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """
        # pylint: disable=no-self-use

        if "payload" in kwargs:
            lpd = len(kwargs["payload"])
        else:
            raise ube.UBXMessageError(
                "CFG-NMEA message definitions must include payload keyword"
            )
        if lpd == 4:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEAvX"]
        elif lpd == 12:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEAv0"]
        else:
            pdict = ubg.UBX_PAYLOADS_GET["CFG-NMEA"]
        return pdict

    def _get_esfmeas_version(self, **kwargs) -> dict:
        """
        Select appropriate payload definition version for
        ESF-MEAS message by checking bit 3 (calibTtagValid)
        in the'flags' attribute.

        :param **kwargs: payload key value pairs
        :return dictionary representing payload definition
        :rtype dict
        :raise UBXMessageError
        """
        # pylint: disable=no-self-use

        if "flags" in kwargs:
            flags = kwargs["flags"]
        elif "payload" in kwargs:
            flags = kwargs["payload"][4:6]
        else:
            raise ube.UBXMessageError(
                "ESF-MEAS message definitions must include flags or payload keyword"
            )
        flags = int(flags.hex(), 16)  # int
        calibTtagValid = flags >> 3 & 1  # test bit 3
        if calibTtagValid:
            pdict = ubg.UBX_PAYLOADS_GET["ESF-MEAS-CT"]
        else:
            pdict = ubg.UBX_PAYLOADS_GET["ESF-MEAS"]
        return pdict

    def _calc_num_repeats(
        self, att: str, payload: bytes, offset: int, offsetend: int = 0
    ) -> int:
        """
        Deduce number of items in 'variable by size' repeating group by
        dividing length of remaining payload by length of group.

        This is predicated on there being only one such repeating group
        per message payload, which is true for all currently supported types.

        :param str att: attribute type e.g. 'U004'
        :param bytes payload : raw payload
        :param int offset: number of bytes in payload before repeating group
        :param int offsetend: number of bytes in payload after repeating group
        :return number of repeats
        :rtype int

        """
        # pylint: disable=no-self-use

        lenpayload = len(payload) - offset - offsetend
        lengroup = 0
        for _, val in att.items():
            lengroup += attsiz(val)
        return int(lenpayload / lengroup)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return human readable representation
        :rtype str
        """

        clsid = None

        umsg_name = self.identity
        if self.payload is None:
            return f"<UBX({umsg_name})>"

        stg = f"<UBX({umsg_name}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                if att[0:6] == "gnssId":  # attribute is a GNSS ID
                    val = gnss2str(val)  # get string representation e.g. 'GPS'
                if att == "iTOW":  # attribute is a GPS Time of Week
                    val = itow2utc(val)  # show time in UTC format
                # if it's an ACK-ACK or ACK-NAK, we show what it's acknowledging in plain text
                if self._ubxClass == b"\x05":  # ACK
                    if att == "clsID":
                        clsid = self.val2bytes(val, ubt.U1)
                        val = ubt.UBX_CLASSES[clsid]
                    if att == "msgID" and clsid:
                        msgid = self.val2bytes(val, ubt.U1)
                        val = ubt.UBX_MSGIDS[clsid + msgid]
                # if it's a CFG-MSG, we show what message class/id it refers to in plain text
                if self._ubxClass == b"\x06" and self._ubxID == b"\x01":  # CFG-MSG
                    if att == "msgClass":
                        clsid = self.val2bytes(val, ubt.U1)
                        val = ubt.UBX_CLASSES[clsid]
                    if att == "msgID" and clsid:
                        msgid = self.val2bytes(val, ubt.U1)
                        val = ubt.UBX_MSGIDS[clsid + msgid]
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return machine readable representation
        :rtype str
        """

        if self._payload is None:
            return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode})"
        return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode}, payload={self._payload})"

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name
        :param object value
        :raise UBXMessageError
        """

        if self._immutable:
            raise ube.UBXMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return serialized output
        :rtype bytes
        """

        output = ubt.UBX_HDR + self._ubxClass + self._ubxID + self._length
        output += (
            self._checksum if self._payload is None else self._payload + self._checksum
        )
        return output

    @property
    def identity(self) -> str:
        """
        Returns identity in plain text form e.g. 'CFG-MSG'.

        :return message identity
        :rtype str
        :raise UBXMessageError
        """

        try:
            # all MGA messages except MGA-DBD need to be identified by the
            # 'type' attribute - the first byte of the payload
            if self._ubxClass == b"\x13" and self._ubxID != b"\x80":
                umsg_name = ubt.UBX_MSGIDS[
                    self._ubxClass + self._ubxID + self._payload[0:1]
                ]
            else:
                umsg_name = ubt.UBX_MSGIDS[self._ubxClass + self._ubxID]
        except KeyError as err:
            raise ube.UBXMessageError(
                f"Unknown UBX message type class {self._ubxClass} id {self._ubxID}"
            ) from err
        return umsg_name

    @property
    def msg_cls(self) -> bytes:
        """
        Class id getter.

        :return message class as bytes
        :rtype bytes
        """
        return self._ubxClass

    @property
    def msg_id(self) -> bytes:
        """
        Message id getter.

        :return message id as bytes
        :rtype bytes
        """

        return self._ubxID

    @property
    def length(self) -> int:
        """
        Payload length getter.

        :return payload length as integer
        :rtype int
        """

        return UBXMessage.bytes2val(self._length, ubt.U2)

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return raw payload as bytes
        :rtype bytes
        """

        return self._payload

    @staticmethod
    def parse(message: bytes, validate: bool = False, mode: int = 0) -> object:
        """
        Parse UBX byte stream to UBXMessage object.

        Includes option to validate incoming payload length and checksum
        (UXBMessage will calculate and assign it's own values anyway).

        :param bytes message
        :param bool validate: Default value = False
        :param int mode: message mode (0=GET, 1=SET, 2=POLL)
        :return UBXMessage object
        :rtype UBXMessage
        :raise UBXParseError
        """

        if mode not in (0, 1, 2):
            raise ube.UBXParseError(f"Invalid message mode {mode} - must be 0, 1 or 2")

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
            if leni != UBXMessage.bytes2val(lenb, ubt.U2):
                raise ube.UBXParseError(
                    (
                        f"Invalid payload length {lenb}"
                        f" - should be {UBXMessage.val2bytes(leni, ubt.U2)}"
                    )
                )
            if ckm != ckv:
                raise ube.UBXParseError(
                    (f"Message checksum {ckm}" f" invalid - should be {ckv}")
                )
        try:
            if payload is None:
                return UBXMessage(clsid, msgid, mode)
            return UBXMessage(clsid, msgid, mode, payload=payload)
        except KeyError as err:
            modestr = ["GET", "SET", "POLL"][mode]
            raise ube.UBXParseError(
                (f"Unknown message type clsid {clsid}, msgid {msgid}, mode {modestr}")
            ) from err

    @staticmethod
    def msgclass2bytes(msgClass: int, msgID: int) -> bytes:
        """
        Convert message class/id integers to bytes
        e.g. 6, 1 to b'/x06/x01'.

        :param int msgClass
        :param int msgID
        :return message class as bytes
        :rtype bytes
        """

        msgClass = UBXMessage.val2bytes(msgClass, ubt.U1)
        msgID = UBXMessage.val2bytes(msgID, ubt.U1)
        return (msgClass, msgID)

    @staticmethod
    def msgstr2bytes(msgClass: str, msgID: str) -> bytes:
        """
        Convert plain text UBX message class to bytes
        e.g. 'CFG-MSG' to b'/x06/x01'.

        :param str msgClass
        :param str msgID
        :return message class as bytes
        :rtype bytes
        :raise UBXMessageError
        """

        try:
            clsid = key_from_val(ubt.UBX_CLASSES, msgClass)
            msgid = key_from_val(ubt.UBX_MSGIDS, msgID)[1:2]
            return (clsid, msgid)
        except KeyError as err:
            raise ube.UBXMessageError(
                f"Undefined message, class {msgClass}, id {msgID}"
            ) from err

    @staticmethod
    def val2bytes(val, att: str) -> bytes:
        """
        Return bytes from value for given UBX attribute type.

        :param object val: value
        :param str att: attribute type
        :return value as bytes
        :rtype bytes
        :raise UBXTypeError
        """

        if att == ubt.CH:  # single variable-length string (e.g. INF-NOTICE)
            return val.encode("utf-8", "backslashreplace")
        atts = attsiz(att)
        if atttyp(att) in ("C", "X"):  # byte or char
            valb = val
        elif atttyp(att) in ("E", "L", "U"):  # unsigned integer
            valb = val.to_bytes(atts, byteorder="little", signed=False)
        elif atttyp(att) == "I":  # signed integer
            valb = val.to_bytes(atts, byteorder="little", signed=True)
        elif att == ubt.R4:  # single precision floating point
            valb = struct.pack("<f", val)
        elif att == ubt.R8:  # double precision floating point
            valb = struct.pack("<d", val)
        else:
            raise ube.UBXTypeError(f"Unknown attribute type {att}")
        return valb

    @staticmethod
    def bytes2val(valb: bytes, att: str) -> object:
        """
        Return value from bytes for given UBX attribute type.

        :param bytes valb: value in byte format
        :param str att: attribute type
        :return value
        :rtype object
        :raise UBXTypeError
        """

        if att == ubt.CH:  # single variable-length string (e.g. INF-NOTICE)
            val = valb.decode("utf-8", "backslashreplace")
        elif atttyp(att) in ("X", "C"):
            val = valb
        elif atttyp(att) in ("E", "L", "U"):  # unsigned integer
            val = int.from_bytes(valb, "little", signed=False)
        elif atttyp(att) == "I":  # signed integer
            val = int.from_bytes(valb, "little", signed=True)
        elif att == ubt.R4:  # single precision floating point
            val = struct.unpack("<f", valb)[0]
        elif att == ubt.R8:  # double precision floating point
            val = struct.unpack("<d", valb)[0]
        else:
            raise ube.UBXTypeError(f"Unknown attribute type {att}")
        return val

    @staticmethod
    def calc_checksum(content: bytes) -> bytes:
        """
        Calculate checksum using 8-bit Fletcher's algorithm.

        :param bytes content: message content, excluding header and checksum bytes
        :return checksum
        :rtype bytes
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
        """
        Validate input message's checksum.

        :param bytes message: message including header and checksum
        :return checksum valid flag
        :rtype bool
        """

        lenm = len(message)
        ckm = message[lenm - 2 : lenm]
        return ckm == UBXMessage.calc_checksum(message[2 : lenm - 2])

    @staticmethod
    def cfgname2key(name: str) -> tuple:
        """
        Return hexadecimal key and data type for given
        configuration database key name.

        :param str name: config database key name as string
        :return tuple of (key: int, type: str)
        :rtype tuple: (int, str)
        :raise UBXMessageError
        """
        try:
            return ubcdb.UBX_CONFIG_DATABASE[name]
        except KeyError as err:
            raise ube.UBXMessageError(
                f"Undefined configuration database key {name}"
            ) from err

    @staticmethod
    def cfgkey2name(keyID: int) -> tuple:
        """
        Return key name and data type for given
        configuration database hexadecimal key.

        :param int keyID: config key as integer
        :return tuple of (keyname: str, type: str)
        :rtype tuple: (str, str)
        :raise UBXMessageError
        """

        val = None
        for key, val in ubcdb.UBX_CONFIG_DATABASE.items():
            (kid, typ) = val
            if keyID == kid:
                return (key, typ)
        raise ube.UBXMessageError(f"Undefined configuration database key {hex(keyID)}")

    @staticmethod
    def config_set(layers: int, transaction: int, cfgData: list) -> object:
        """
        Construct CFG-VALSET message from an array of
        configuration database (key, value) tuples. Keys
        can be in int (keyID) or str (keyname) format.

        :param int layers: memory layer(s) (1=RAM, 2=BBR, 4=Flash)
        :param int transaction: 0=no txn, 1=start txn, 2=continue txn, 3=apply txn
        :param list cfgData: list of up to 64 tuples (key, value)
        :return UBXMessage CFG-VALSET
        :rtype UBXMessage
        :raise UBXMessageError
        """

        num = len(cfgData)
        if num > 64:
            raise ube.UBXMessageError(
                f"Number of configuration tuples {num} exceeds maximum of 64"
            )

        version = UBXMessage.val2bytes(0 if transaction == 0 else 1, ubt.U1)
        layers = UBXMessage.val2bytes(layers, ubt.U1)
        transaction = UBXMessage.val2bytes(transaction, ubt.U1)
        payload = version + layers + transaction + b"\x00"
        lis = b""

        for cfgItem in cfgData:
            att = ""
            (key, val) = cfgItem
            if isinstance(key, str):  # if key is a string (keyname)
                (key, att) = UBXMessage.cfgname2key(
                    key
                )  # lookup keyID & attribute type
            else:
                (_, att) = UBXMessage.cfgkey2name(key)  # lookup attribute type
            keyb = UBXMessage.val2bytes(key, ubt.U4)
            valb = UBXMessage.val2bytes(val, att)
            lis = lis + keyb + valb

        return UBXMessage("CFG", "CFG-VALSET", ubt.SET, payload=payload + lis)

    @staticmethod
    def config_del(layers: int, transaction: int, keys: list) -> object:
        """
        Construct CFG-VALDEL message from an array of
        configuration database keys, which can be in int (keyID)
        or str (keyname) format.

        :param int layers: memory layer(s) 2=BBR, 4=Flash
        :param int transaction: 0=no txn, 1=start txn, 2=continue txn, 3=apply txn
        :param list keys: array of up to 64 keys as int (keyID) or string (keyname)
        :return UBXMessage CFG-VALDEL
        :rtype UBXMessage
        :raise UBXMessageError
        """

        num = len(keys)
        if num > 64:
            raise ube.UBXMessageError(
                f"Number of configuration keys {num} exceeds maximum of 64"
            )

        version = UBXMessage.val2bytes(0 if transaction == 0 else 1, ubt.U1)
        layers = UBXMessage.val2bytes(layers, ubt.U1)
        transaction = UBXMessage.val2bytes(transaction, ubt.U1)
        payload = version + layers + transaction + b"\x00"
        lis = b""

        for key in keys:
            if isinstance(key, str):  # if keyname as a string
                (key, _) = UBXMessage.cfgname2key(key)  # lookup keyID
            keyb = UBXMessage.val2bytes(key, ubt.U4)
            lis = lis + keyb

        return UBXMessage("CFG", "CFG-VALDEL", ubt.SET, payload=payload + lis)

    @staticmethod
    def config_poll(layer: int, position: int, keys: list) -> object:
        """
        Construct CFG-VALGET message from an array of
        configuration database keys, which can be in int (keyID)
        or str (keyname) format.

        :param int layer: memory layer 0=RAM, 1=BBR, 2=Flash, 7 = Default
        :param int position: number of keys to skip before returning result
        :param list keys: array of up to 64 keys as int (keyID) or str (keyname)
        :return UBXMessage CFG-VALGET
        :rtype UBXMessage
        :raise UBXMessageError
        """

        num = len(keys)
        if num > 64:
            raise ube.UBXMessageError(
                f"Number of configuration keys {num} exceeds maximum of 64"
            )

        version = UBXMessage.val2bytes(0, ubt.U1)
        layer = UBXMessage.val2bytes(layer, ubt.U1)
        position = UBXMessage.val2bytes(position, ubt.U2)
        payload = version + layer + position
        lis = b""

        for key in keys:
            if isinstance(key, str):  # if keyname as a string
                (key, _) = UBXMessage.cfgname2key(key)  # lookup keyID
            keyb = UBXMessage.val2bytes(key, ubt.U4)
            lis = lis + keyb

        return UBXMessage("CFG", "CFG-VALGET", ubt.POLL, payload=payload + lis)
