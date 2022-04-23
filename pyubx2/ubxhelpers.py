"""
Collection of UBX helper methods which can be used
outside the UBXMessage or UBXReader classes

Created on 15 Dec 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import struct
from datetime import datetime, timedelta
from pyubx2.ubxtypes_core import GNSSLIST, UBX_HDR, NMEA_HDR
import pyubx2.ubxtypes_core as ubt
import pyubx2.ubxtypes_configdb as ubcdb
import pyubx2.exceptions as ube


def calc_checksum(content: bytes) -> bytes:
    """
    Calculate checksum using 8-bit Fletcher's algorithm.

    :param bytes content: message content, excluding header and checksum bytes
    :return: checksum
    :rtype: bytes

    """

    check_a = 0
    check_b = 0

    for char in content:
        check_a += char
        check_a &= 0xFF
        check_b += check_a
        check_b &= 0xFF

    return bytes((check_a, check_b))


def isvalid_checksum(message: bytes) -> bool:
    """
    Validate message checksum.

    :param bytes message: message including header and checksum bytes
    :return: checksum valid flag
    :rtype: bool

    """

    lenm = len(message)
    ckm = message[lenm - 2 : lenm]
    return ckm == calc_checksum(message[2 : lenm - 2])


def atttyp(att: str) -> str:
    """
    Helper function to return attribute type as string.

    :param str: attribute type e.g. 'U002'
    :return: type of attribute as string e.g. 'U'
    :rtype: str

    """

    return att[0:1]


def attsiz(att: str) -> int:
    """
    Helper function to return attribute size in bytes.

    :param str: attribute type e.g. 'U002'
    :return: size of attribute in bytes
    :rtype: int

    """

    return int(att[1:4])


def itow2utc(itow: int) -> datetime.time:
    """
    Convert GPS Time Of Week to UTC time
    (UTC = GPS - 18 seconds; correct as from 1/1/2017).

    :param int itow: GPS Time Of Week
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = datetime(1980, 1, 6) + timedelta(seconds=(itow / 1000) - 18)
    return utc.time()


def gpsfix2str(fix: int) -> str:
    """
    Convert GPS fix integer to descriptive string.

    :param int fix: GPS fix type (0-5)
    :return: GPS fix type as string
    :rtype: str

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


def dop2str(dop: float) -> str:
    """
    Convert Dilution of Precision float to descriptive string.

    :param float dop: dilution of precision as float
    :return: dilution of precision as string
    :rtype: str

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


def gnss2str(gnss_id: int) -> str:
    """
    Convert GNSS ID to descriptive string
    ('GPS', 'GLONASS', etc.).

    :param int gnss_id: GNSS identifier as integer (0-6)
    :return: GNSS identifier as string
    :rtype: str

    """

    try:
        return GNSSLIST[gnss_id]
    except KeyError:
        return str(gnss_id)


def key_from_val(dictionary: dict, value) -> str:
    """
    Helper method - get dictionary key corresponding to (unique) value.

    :param dict dictionary: dictionary
    :param object value: unique dictionary value
    :return: dictionary key
    :rtype: str
    :raises: KeyError: if no key found for value

    """

    val = None
    for key, val in dictionary.items():
        if val == value:
            return key
    raise KeyError(f"No key found for value {value}")


def get_bits(bitfield: bytes, bitmask: int) -> int:
    """
    Get integer value of specified (masked) bit(s) in a UBX bitfield (attribute type 'X')

    e.g. to get value of bits 6,7 in bitfield b'\\\\x89' (binary 0b10001001)::

        get_bits(b'\\x89', 0b11000000) = get_bits(b'\\x89', 192) = 2

    :param bytes bitfield: bitfield byte(s)
    :param int bitmask: bitmask as integer (= Σ(2**n), where n is the number of the bit)
    :return: value of masked bit(s)
    :rtype: int
    """

    i = 0
    val = int(bitfield.hex(), 16)
    while bitmask & 1 == 0:
        bitmask = bitmask >> 1
        i += 1
    return val >> i & bitmask


def val2bytes(val, att: str) -> bytes:
    """
    Convert value to bytes for given UBX attribute type.

    :param object val: attribute value e.g. 25
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as bytes
    :rtype: bytes
    :raises: UBXTypeError

    """

    if att == ubt.CH:  # single variable-length string (e.g. INF-NOTICE)
        return val.encode("utf-8", "backslashreplace")
    atts = attsiz(att)
    if atttyp(att) in ("C", "X"):  # byte or char
        valb = val
    elif atttyp(att) in ("E", "L", "U"):  # unsigned integer
        valb = val.to_bytes(atts, byteorder="little", signed=False)
    elif atttyp(att) == "A":  # array of unsigned integers
        atts = attsiz(att)
        valb = b""
        for i in range(atts):
            valb += val[i].to_bytes(1, byteorder="little", signed=False)
    elif atttyp(att) == "I":  # signed integer
        valb = val.to_bytes(atts, byteorder="little", signed=True)
    elif att == ubt.R4:  # single precision floating point
        valb = struct.pack("<f", val)
    elif att == ubt.R8:  # double precision floating point
        valb = struct.pack("<d", val)
    else:
        raise ube.UBXTypeError(f"Unknown attribute type {att}")
    return valb


def bytes2val(valb: bytes, att: str) -> object:
    """
    Convert bytes to value for given UBX attribute type.

    :param bytes valb: attribute value in byte format e.g. b'\\\\x19\\\\x00\\\\x00\\\\x00'
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: object
    :raises: UBXTypeError

    """

    if att == ubt.CH:  # single variable-length string (e.g. INF-NOTICE)
        val = valb.decode("utf-8", "backslashreplace")
    elif atttyp(att) in ("X", "C"):
        val = valb
    elif atttyp(att) in ("E", "L", "U"):  # unsigned integer
        val = int.from_bytes(valb, "little", signed=False)
    elif atttyp(att) == "A":  # array of unsigned integers
        atts = attsiz(att)
        val = []
        for i in range(atts):
            val.append(valb[i])
    elif atttyp(att) == "I":  # signed integer
        val = int.from_bytes(valb, "little", signed=True)
    elif att == ubt.R4:  # single precision floating point
        val = struct.unpack("<f", valb)[0]
    elif att == ubt.R8:  # double precision floating point
        val = struct.unpack("<d", valb)[0]
    else:
        raise ube.UBXTypeError(f"Unknown attribute type {att}")
    return val


def nomval(att: str) -> object:
    """
    Get nominal value for given UBX attribute type.

    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: object
    :raises: UBXTypeError

    """

    if att == "CH":
        val = ""
    elif atttyp(att) in ("X", "C"):
        val = b"\x00" * attsiz(att)
    elif atttyp(att) == "R":
        val = 0.0
    elif atttyp(att) in ("E", "I", "L", "U"):
        val = 0
    elif atttyp(att) == "A":  # array of unsigned integers
        val = [0] * attsiz(att)
    else:
        raise ube.UBXTypeError(f"Unknown attribute type {att}")
    return val


def msgclass2bytes(msgClass: int, msgID: int) -> bytes:
    """
    Convert message class/id integers to bytes.

    :param int msgClass: message class as integer e.g. 6
    :param int msgID: message ID as integer e.g. 1
    :return: message class as bytes e.g. b'/x06/x01'
    :rtype: bytes

    """

    msgClass = val2bytes(msgClass, ubt.U1)
    msgID = val2bytes(msgID, ubt.U1)
    return (msgClass, msgID)


def msgstr2bytes(msgClass: str, msgID: str) -> bytes:
    """
    Convert plain text UBX message class to bytes.

    :param str msgClass: message class as str e.g. 'CFG'
    :param str msgID: message ID as str e.g. 'CFG-MSG'
    :return: message class as bytes e.g. b'/x06/x01'
    :rtype: bytes
    :raises: UBXMessageError

    """

    try:
        clsid = key_from_val(ubt.UBX_CLASSES, msgClass)
        msgid = key_from_val(ubt.UBX_MSGIDS, msgID)[1:2]
        return (clsid, msgid)
    except KeyError as err:
        raise ube.UBXMessageError(
            f"Undefined message, class {msgClass}, id {msgID}"
        ) from err


def cfgname2key(name: str) -> tuple:
    """
    Return hexadecimal key and data type for given
    configuration database key name.

    :param str name: config key as string e.g. "CFG_NMEA_PROTVER"
    :return: tuple of (key, type)
    :rtype: tuple: (int, str)
    :raises: UBXMessageError

    """
    try:
        return ubcdb.UBX_CONFIG_DATABASE[name]
    except KeyError as err:
        raise ube.UBXMessageError(
            f"Undefined configuration database key {name}"
        ) from err


def cfgkey2name(keyID: int) -> tuple:
    """
    Return key name and data type for given
    configuration database hexadecimal key.

    :param int keyID: config key as integer e.g. 0x20930001
    :return: tuple of (keyname, type)
    :rtype: tuple: (str, str)
    :raises: UBXMessageError

    """

    val = None
    for key, val in ubcdb.UBX_CONFIG_DATABASE.items():
        (kid, typ) = val
        if keyID == kid:
            return (key, typ)
    raise ube.UBXMessageError(f"Undefined configuration database key {hex(keyID)}")


def protocol(raw: bytes) -> int:
    """
    Gets protocol of raw message.

    :param bytes raw: raw (binary) message
    :return: protocol type (1 = NMEA, 2 = UBX, 4 = RTCM3, 0 = unknown)
    :rtype: int
    """

    p = raw[0:2]
    if p == UBX_HDR:
        return 2
    if p in NMEA_HDR:
        return 1
    if p[0] == 0xD3 and (p[1] & ~0x03) == 0:
        return 4
    return 0


def hextable(raw: bytes, cols: int = 8) -> str:
    """
    Formats raw (binary) message in tabular hexadecimal format e.g.

    000: 2447 4e47 5341 2c41 2c33 2c33 342c 3233 | b'$GNGSA,A,3,34,23' |

    :param bytes raw: raw (binary) data
    :param int cols: number of columns in hex table (8)
    :return: table of hex data
    :rtype: str
    """

    hextbl = ""
    colw = cols * 4
    rawh = raw.hex()
    for i in range(0, len(rawh), colw):
        rawl = rawh[i : i + colw].ljust(colw, " ")
        hextbl += f"{int(i/2):03}: "
        for col in range(0, colw, 4):
            hextbl += f"{rawl[col : col + 4]} "
        hextbl += f" | {bytes.fromhex(rawl)} |\n"

    return hextbl
