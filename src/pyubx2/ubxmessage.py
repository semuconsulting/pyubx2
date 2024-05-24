"""
ubxmessage.py

Main UBX Message Protocol Class.

Created on 26 Sep 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

# pylint: disable=invalid-name

import struct

from pyubx2.exceptions import UBXMessageError, UBXTypeError
from pyubx2.ubxhelpers import (
    attsiz,
    bytes2val,
    calc_checksum,
    cfgkey2name,
    cfgname2key,
    escapeall,
    gnss2str,
    itow2utc,
    msgclass2bytes,
    msgstr2bytes,
    nomval,
    val2bytes,
)
from pyubx2.ubxtypes_core import (
    CH,
    GET,
    POLL,
    SCALROUND,
    SET,
    U1,
    U2,
    U4,
    UBX_CLASSES,
    UBX_HDR,
    UBX_MSGIDS,
    X1,
    X2,
    X4,
    X6,
    X8,
    X24,
)
from pyubx2.ubxtypes_get import UBX_PAYLOADS_GET
from pyubx2.ubxtypes_poll import UBX_PAYLOADS_POLL
from pyubx2.ubxtypes_set import UBX_PAYLOADS_SET
from pyubx2.ubxvariants import VARIANTS


class UBXMessage:
    """UBX Message Class."""

    def __init__(
        self,
        ubxClass,
        ubxID,
        msgmode: int,
        parsebitfield: bool = True,
        **kwargs,
    ):
        """Constructor.

        If no keyword parms are passed, the payload is taken to be empty.

        If 'payload' is passed as a keyword parm, this is taken to contain the complete
        payload as a sequence of bytes; any other keyword parms are ignored.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param object msgClass: message class as str, int or byte
        :param object msgID: message ID as str, int or byte
        :param int msgmode: message mode (0=GET, 1=SET, 2=POLL)
        :param bool parsebitfield: parse bitfields ('X' type attributes) Y/N
        :param kwargs: optional payload keyword arguments
        :raises: UBXMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self._mode = msgmode
        self._payload = b""
        self._length = b""
        self._checksum = b""
        self._parsebf = parsebitfield  # parsing bitfields Y/N?

        if msgmode not in (GET, SET, POLL):
            raise UBXMessageError(f"Invalid msgmode {msgmode} - must be 0, 1 or 2")

        # accommodate different formats of msgClass and msgID
        if isinstance(ubxClass, str) and isinstance(
            ubxID, str
        ):  # string e.g. 'CFG', 'CFG-PRT'
            (self._ubxClass, self._ubxID) = msgstr2bytes(ubxClass, ubxID)
        elif isinstance(ubxClass, int) and isinstance(ubxID, int):  # int e.g. 6, 1
            (self._ubxClass, self._ubxID) = msgclass2bytes(ubxClass, ubxID)
        else:  # bytes e.g. b'\x06', b'\x01'
            self._ubxClass = ubxClass
            self._ubxID = ubxID

        self._do_attributes(**kwargs)

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate UBXMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param kwargs: optional payload key/value pairs
        :raises: UBXTypeError

        """

        offset = 0  # payload offset in bytes
        index = []  # array of (nested) group indices

        try:
            if len(kwargs) == 0:  # if no kwargs, assume null payload
                self._payload = None
            else:
                self._payload = kwargs.get("payload", b"")
                pdict = self._get_dict(**kwargs)  # get appropriate payload dict
                for anam in pdict:  # process each attribute in dict
                    (offset, index) = self._set_attribute(
                        anam, pdict, offset, index, **kwargs
                    )
            self._do_len_checksum()

        except (
            AttributeError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise UBXTypeError(
                (
                    f"Incorrect type for attribute '{anam}' "
                    f"in {['GET', 'SET', 'POLL'][self._mode]} message "
                    f"class {self.identity}"
                )
            ) from err
        except (OverflowError,) as err:
            raise UBXTypeError(
                (
                    f"Overflow error for attribute '{anam}' "
                    f"in {['GET', 'SET', 'POLL'][self._mode]} message "
                    f"class {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, anam: str, pdict: dict, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param str anam: attribute name
        :param dict pdict: dict representing payload definition
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        adef = pdict[anam]  # get attribute definition
        if isinstance(
            adef, tuple
        ):  # repeating group of attributes or subdefined bitfield
            numr, _ = adef
            if numr in (X1, X2, X4, X6, X8, X24):  # bitfield
                if self._parsebf:  # if we're parsing bitfields
                    (offset, index) = self._set_attribute_bitfield(
                        adef, offset, index, **kwargs
                    )
                else:  # treat bitfield as a single byte array
                    offset = self._set_attribute_single(
                        anam, numr, offset, index, **kwargs
                    )
            else:  # repeating group of attributes
                (offset, index) = self._set_attribute_group(
                    adef, offset, index, **kwargs
                )
        else:  # single attribute
            offset = self._set_attribute_single(anam, adef, offset, index, **kwargs)

        return (offset, index)

    def _set_attribute_group(
        self, adef: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple adef: attribute definition - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        index.append(0)  # add a (nested) group index
        anam, gdict = adef  # attribute signifying group size, group dictionary
        # if CFG-VALGET or CFG-VALSET message, use dedicated method to
        # parse as configuration key value pairs
        if self._ubxClass == b"\x06" and (
            (self._ubxID == b"\x8b" and self._mode == GET)
            or (self._ubxID == b"\x8a" and self._mode == SET)
        ):
            self._set_attribute_cfgval(offset, **kwargs)
        else:
            # derive or retrieve number of items in group
            if isinstance(anam, int):  # fixed number of repeats
                gsiz = anam
            elif anam == "None":  # number of repeats 'variable by size'
                gsiz = self._calc_num_repeats(gdict, self._payload, offset, 0)
            else:  # number of repeats is defined in named attribute
                gsiz = getattr(self, anam)
                # special handling for ESF-MEAS message types
                if (
                    self._ubxClass == b"\x10"
                    and self._ubxID == b"\x02"
                    and self._mode == SET
                ):
                    if getattr(self, "calibTtagValid", 0):
                        gsiz += 1
            # recursively process each group attribute,
            # incrementing the payload offset and index as we go
            for i in range(gsiz):
                index[-1] = i + 1
                for key1 in gdict:
                    (offset, index) = self._set_attribute(
                        key1, gdict, offset, index, **kwargs
                    )

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_single(
        self, anam: str, adef: object, offset: int, index: list, **kwargs
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str anam: attribute keyword
        EITHER
        :param str adef: attribute definition string e.g. 'U002'
        OR
        :param list adef: if scaled, list of [attribute type string, scaling factor float]
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: offset
        :rtype: int

        """
        # pylint: disable=no-member

        # if attribute is scaled
        ares = 1
        if isinstance(adef, list):
            ares = adef[1]  # attribute resolution (i.e. scaling factor)
            adef = adef[0]  # attribute definition

        # if attribute is part of a (nested) repeating group, suffix name with index
        anami = anam
        for i in index:  # one index for each nested level
            if i > 0:
                anami += f"_{i:02d}"

        # determine attribute size (bytes)
        if adef == CH:  # variable length string
            asiz = len(self._payload)
        else:
            asiz = attsiz(adef)

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            valb = self._payload[offset : offset + asiz]
            if ares == 1:
                val = bytes2val(valb, adef)
            else:
                val = round(bytes2val(valb, adef) * ares, SCALROUND)
        else:
            # if individual keyword has been provided,
            # set to provided value, else set to
            # nominal value
            val = kwargs.get(anami, nomval(adef))
            if ares == 1:
                valb = val2bytes(val, adef)
            else:
                valb = val2bytes(int(val / ares), adef)
            self._payload += valb

        if anami[0:3] == "_HP":  # high precision component of earlier attribute
            # add standard and high precision values in a single attribute
            setattr(self, anami[3:], round(getattr(self, anami[3:]) + val, SCALROUND))
        else:
            setattr(self, anami, val)

        return offset + asiz

    def _set_attribute_bitfield(
        self, atyp: str, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Parse bitfield attribute (type 'X').

        :param str atyp: attribute type e.g. 'X002'
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """
        # pylint: disable=no-member

        btyp, bdict = atyp  # type of bitfield, bitfield dictionary
        bsiz = attsiz(btyp)  # size of bitfield in bytes
        bfoffset = 0

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            bitfield = int.from_bytes(self._payload[offset : offset + bsiz], "little")
        else:
            bitfield = 0

        # process each flag in bitfield
        for key, keyt in bdict.items():
            (bitfield, bfoffset) = self._set_attribute_bits(
                bitfield, bfoffset, key, keyt, index, **kwargs
            )

        # update payload
        if "payload" not in kwargs:
            self._payload += bitfield.to_bytes(bsiz, "little")

        return (offset + bsiz, index)

    def _set_attribute_bits(
        self,
        bitfield: int,
        bfoffset: int,
        key: str,
        keyt: str,
        index: list,
        **kwargs,
    ) -> tuple:
        """
        Set individual bit flag from bitfield.

        :param int bitfield: bitfield
        :param int bfoffset: bitfield offset in bits
        :param str key: attribute key name
        :param str keyt: key type e.g. 'U001'
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (bitfield, bfoffset)
        :rtype: tuple

        """
        # pylint: disable=no-member

        # if attribute is part of a (nested) repeating group, suffix name with index
        keyr = key
        for i in index:  # one index for each nested level
            if i > 0:
                keyr += f"_{i:02d}"

        atts = attsiz(keyt)  # determine flag size in bits

        if "payload" in kwargs:
            val = (bitfield >> bfoffset) & ((1 << atts) - 1)
        else:
            val = kwargs.get(keyr, 0)
            bitfield = bitfield | (val << bfoffset)

        if key[0:8] != "reserved":  # don't bother to set reserved bits
            setattr(self, keyr, val)
        return (bitfield, bfoffset + atts)

    def _set_attribute_cfgval(self, offset: int, **kwargs):
        """
        Parse CFG-VALGET / CFG-VALSET payload to set of configuration
        key value pairs.

        :param int offset: payload offset
        :param **kwargs:  optional payload key/value pairs
        :raises: UBXMessageError

        """

        KEYLEN = 4
        if "payload" in kwargs:
            self._payload = kwargs["payload"]
        else:
            raise UBXMessageError(
                "CFG-VALGET message definitions must include payload keyword"
            )
        cfglen = len(self._payload[offset:])

        i = 0
        while offset < cfglen:
            if i == KEYLEN:
                key = int.from_bytes(
                    self._payload[offset : offset + KEYLEN], "little", signed=False
                )
                (keyname, att) = cfgkey2name(key)
                atts = attsiz(att)
                valb = self._payload[offset + KEYLEN : offset + KEYLEN + atts]
                val = bytes2val(valb, att)
                setattr(self, keyname, val)
                i = 0
                offset += KEYLEN + atts

            else:
                i += 1

    def _do_len_checksum(self):
        """
        Calculate and format payload length and checksum as bytes."""

        payload = b"" if self._payload is None else self._payload
        self._length = val2bytes(len(payload), U2)
        self._checksum = calc_checksum(
            self._ubxClass + self._ubxID + self._length + payload
        )

    def _get_dict(self, **kwargs) -> dict:
        """
        Get payload dictionary corresponding to message mode (GET/SET/POLL)
        Certain message types need special handling as alternate payload
        variants exist for the same ubxClass/ubxID/mode.

        :param kwargs: optional payload key/value pairs
        :return: dictionary representing payload definition
        :rtype: dict

        """

        try:
            msg = self._ubxClass + self._ubxID
            variant = VARIANTS[self._mode].get(msg, False)
            if variant and msg[0] == 0x13:  # MGA
                pdict = variant(msg, self._mode, **kwargs)
            elif variant:
                pdict = variant(**kwargs)
            elif self._mode == POLL:
                pdict = UBX_PAYLOADS_POLL[self.identity]
            elif self._mode == SET:
                pdict = UBX_PAYLOADS_SET[self.identity]
            else:
                # Unknown GET message, parsed to nominal definition
                if self.identity[-7:] == "NOMINAL":
                    pdict = {}
                else:
                    pdict = UBX_PAYLOADS_GET[self.identity]
            return pdict
        except KeyError as err:
            mode = ["GET", "SET", "POLL"][self._mode]
            raise UBXMessageError(
                f"Unknown message type {escapeall(self._ubxClass + self._ubxID)}, mode {mode}. "
                "Check 'msgmode' setting is appropriate for data stream"
            ) from err

    def _calc_num_repeats(
        self, attd: dict, payload: bytes, offset: int, offsetend: int = 0
    ) -> int:
        """
        Deduce number of items in 'variable by size' repeating group by
        dividing length of remaining payload by length of group.

        This is predicated on there being only one such repeating group
        per message payload, which is true for all currently supported types.

        :param dict attd: grouped attribute dictionary
        :param bytes payload : raw payload
        :param int offset: number of bytes in payload before repeating group
        :param int offsetend: number of bytes in payload after repeating group
        :return: number of repeats
        :rtype: int

        """

        lenpayload = len(payload) - offset - offsetend
        lengroup = 0
        for _, val in attd.items():
            if isinstance(val, tuple):
                val, _ = val
            lengroup += attsiz(val)
        return int(lenpayload / lengroup)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str

        """

        clsid = None
        msgid = None

        umsg_name = self.identity
        if self.payload is None:
            return f"<UBX({umsg_name})>"
        if self.identity[-7:] == "NOMINAL":
            return f"<UBX({umsg_name}, payload={escapeall(self._payload)})>"

        stg = f"<UBX({umsg_name}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                # escape all byte chars
                if (
                    isinstance(val, bytes)
                    and att not in ("datumName",)
                    and self.identity != "MON-VER"
                ):
                    val = escapeall(val)
                if att[0:6] == "gnssId":  # attribute is a GNSS ID
                    val = gnss2str(val)  # get string representation e.g. 'GPS'
                if att == "iTOW":  # attribute is a GPS Time of Week
                    val = itow2utc(val)  # show time in UTC format
                # if it's an ACK, we show what it's acknowledging in plain text
                # if it's a CFG-MSG, we show what message class/id it refers to in plain text
                if self._ubxClass == b"\x05" or (
                    self._ubxClass == b"\x06" and self._ubxID == b"\x01"
                ):
                    if att in ["clsID", "msgClass"]:
                        clsid = val2bytes(val, U1)
                        val = UBX_CLASSES.get(clsid, clsid)
                    if att == "msgID" and clsid:
                        msgid = val2bytes(val, U1)
                        val = UBX_MSGIDS.get(clsid + msgid, clsid + msgid)
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str

        """

        if self._payload is None:
            return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode})"
        return f"UBXMessage({self._ubxClass}, {self._ubxID}, {self._mode}, payload={self._payload})"

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name: attribute name
        :param object value: attribute value
        :raises: UBXMessageError

        """

        if self._immutable:
            raise UBXMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return: serialized output
        :rtype: bytes

        """

        return (
            UBX_HDR
            + self._ubxClass
            + self._ubxID
            + self._length
            + (b"" if self._payload is None else self._payload)
            + self._checksum
        )

    @property
    def identity(self) -> str:
        """
        Returns message identity in plain text form.

        If the message is unrecognised, the message is parsed
        to a nominal payload definition UBX-NOMINAL and
        the term 'NOMINAL' is appended to the identity.

        :return: message identity e.g. 'CFG-MSG'
        :rtype: str

        """

        try:
            # all MGA messages except MGA-DBD need to be identified by the
            # 'type' attribute - the first byte of the payload
            if self._ubxClass == b"\x13" and self._ubxID != b"\x80":
                umsg_name = UBX_MSGIDS[
                    self._ubxClass + self._ubxID + self._payload[0:1]
                ]
            else:
                umsg_name = UBX_MSGIDS[self._ubxClass + self._ubxID]
        except KeyError:
            # unrecognised u-blox message, parsed to UBX-NOMINAL definition
            if self._ubxClass in UBX_CLASSES:  # known class
                cls = UBX_CLASSES[self._ubxClass]
            else:  # unknown class
                cls = "UNKNOWN"
            umsg_name = (
                f"{cls}-{int.from_bytes(self._ubxClass, 'little'):02x}"
                + f"{int.from_bytes(self._ubxID, 'little'):02x}-NOMINAL"
            )
        return umsg_name

    @property
    def msg_cls(self) -> bytes:
        """
        Class id getter.

        :return: message class as bytes
        :rtype: bytes

        """
        return self._ubxClass

    @property
    def msg_id(self) -> bytes:
        """
        Message id getter.

        :return: message id as bytes
        :rtype: bytes

        """

        return self._ubxID

    @property
    def length(self) -> int:
        """
        Payload length getter.

        :return: payload length as integer
        :rtype: int

        """

        return bytes2val(self._length, U2)

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return: raw payload as bytes
        :rtype: bytes

        """

        return self._payload

    @property
    def msgmode(self) -> int:
        """
        Message mode getter.

        :return: msgmode as integer
        :rtype: int

        """

        return self._mode

    @staticmethod
    def config_set(layers: int, transaction: int, cfgData: list) -> object:
        """
        Construct CFG-VALSET message from an array of
        configuration database (key, value) tuples. Keys
        can be in int (keyID) or str (keyname) format.

        :param int layers: memory layer(s) SET_LAYER_RAM (1) = RAM,
            SET_LAYER_BBR (2) = Battery Backed RAM, SETLAYER_FLASH (4) = Flash
        :param int transaction: TXN_NONE (0) = no txn, TXN _START (1) = start txn,
            TXN_ONGOING (2) = continue txn, TXT_COMMIT (3) = apply txn
        :param list cfgData: list of up to 64 tuples (key, value)
        :return: UBXMessage CFG-VALSET
        :rtype: UBXMessage
        :raises: UBXMessageError

        """

        num = len(cfgData)
        if num > 64:
            raise UBXMessageError(
                f"Number of configuration tuples {num} exceeds maximum of 64"
            )

        version = val2bytes(0 if transaction == 0 else 1, U1)
        layers = val2bytes(layers, U1)
        transaction = val2bytes(transaction, U1)
        payload = version + layers + transaction + b"\x00"
        lis = b""

        for cfgItem in cfgData:
            att = ""
            (key, val) = cfgItem
            if isinstance(key, str):  # if key is a string (keyname)
                (key, att) = cfgname2key(key)  # lookup keyID & attribute type
            else:
                (_, att) = cfgkey2name(key)  # lookup attribute type
            keyb = val2bytes(key, U4)
            valb = val2bytes(val, att)
            lis = lis + keyb + valb

        return UBXMessage("CFG", "CFG-VALSET", SET, payload=payload + lis)

    @staticmethod
    def config_del(layers: int, transaction: int, keys: list) -> object:
        """
        Construct CFG-VALDEL message from an array of
        configuration database keys. Keys can be in int (keyID)
        or str (keyname) format.

        :param int layers: non-volatile memory layer(s) SET_LAYER_BBR (2) = Battery Backed RAM,
            SET_LAYER_FLASH (4) = Flash
        :param int transaction: TXN_NONE (0) = no txn, TXN _START (1) = start txn,
            TXN_ONGOING (2) = continue txn, TXT_COMMIT (3) = apply txn
        :param list keys: array of up to 64 keys as int (keyID) or string (keyname)
        :return: UBXMessage CFG-VALDEL
        :rtype: UBXMessage
        :raises: UBXMessageError

        """

        num = len(keys)
        if num > 64:
            raise UBXMessageError(
                f"Number of configuration keys {num} exceeds maximum of 64"
            )

        version = val2bytes(0 if transaction == 0 else 1, U1)
        layers = val2bytes(layers, U1)
        transaction = val2bytes(transaction, U1)
        payload = version + layers + transaction + b"\x00"
        lis = b""

        for key in keys:
            if isinstance(key, str):  # if keyname as a string
                (key, _) = cfgname2key(key)  # lookup keyID
            keyb = val2bytes(key, U4)
            lis = lis + keyb

        return UBXMessage("CFG", "CFG-VALDEL", SET, payload=payload + lis)

    @staticmethod
    def config_poll(layer: int, position: int, keys: list) -> object:
        """
        Construct CFG-VALGET message from an array of
        configuration database keys, which can be in int (keyID)
        or str (keyname) format.

        :param int layer: memory layer POLL_LAYER_RAM (0) = RAM,
            POLL_LAYER_BBR (1) = Battery-backed RAM, POLL_LAYER_FLASH (2) = Flash,
            POLL_LAYER_DEFAULT (7) = Default
        :param int position: number of keys to skip before returning result
        :param list keys: array of up to 64 keys as int (keyID) or str (keyname)
        :return: UBXMessage CFG-VALGET
        :rtype: UBXMessage
        :raises: UBXMessageError

        """

        num = len(keys)
        if num > 64:
            raise UBXMessageError(
                f"Number of configuration keys {num} exceeds maximum of 64"
            )

        version = val2bytes(0, U1)
        layer = val2bytes(layer, U1)
        position = val2bytes(position, U2)
        payload = version + layer + position
        lis = b""

        for key in keys:
            if isinstance(key, str):  # if keyname as a string
                (key, _) = cfgname2key(key)  # lookup keyID
            keyb = val2bytes(key, U4)
            lis = lis + keyb

        return UBXMessage("CFG", "CFG-VALGET", POLL, payload=payload + lis)
