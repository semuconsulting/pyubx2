"""
Collection of UBX helper methods which can be used
outside the UBXMessage or UBXReader classes.

Created on 15 Dec 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

import struct
from datetime import datetime, timedelta
from math import cos, pi, sin, trunc

from pynmeagps.nmeatypes_core import NMEA_HDR

import pyubx2.exceptions as ube
import pyubx2.ubxtypes_configdb as ubcdb
import pyubx2.ubxtypes_core as ubt
from pyubx2.ubxtypes_core import (
    ATTTYPE,
    NMEA_PROTOCOL,
    POLL,
    RTCM3_PROTOCOL,
    SET,
    UBX_HDR,
    UBX_PROTOCOL,
)
from pyubx2.ubxtypes_decodes import FIXTYPE, GNSSLIST

EPOCH0 = datetime(1980, 1, 6)  # EPOCH start date
LEAPOFFSET = 18  # leap year offset in seconds, valid as from 1/1/2017
SIW = 604800  # seconds in week = 3600*24*7


def att2idx(att: str) -> object:
    """
    Get integer indices corresponding to grouped attribute.

    e.g. svid_06 -> 6; gnssId_103 -> 103, gsid_03_04 -> (3,4), tow -> 0

    :param str att: grouped attribute name e.g. svid_01
    :return: indices as integer(s), or 0 if not grouped
    :rtype: int or tuple for nested group
    """

    try:
        att = att.split("_")
        ln = len(att)
        if ln == 2:  # one group level
            return int(att[1])
        if ln > 2:  # nested group level(s)
            return tuple(int(att[i]) for i in range(1, ln))
        return 0  # not grouped
    except ValueError:
        return 0


def att2name(att: str) -> str:
    """
    Get name of grouped attribute.

    e.g. svid_06 -> svid; gnssId_103 -> gnssId, tow -> tow

    :param str att: grouped attribute name e.g. svid_01
    :return: name without index e.g. svid
    :rtype: str
    """

    return att.split("_")[0]


def attsiz(att: str) -> int:
    """
    Helper function to return attribute size in bytes.

    :param str: attribute type e.g. 'U002'
    :return: size of attribute in bytes, or -1 if variable length
    :rtype: int

    """

    if att == "CH":  # variable length
        return -1
    return int(att[1:4])


def atttyp(att: str) -> str:
    """
    Helper function to return attribute type as string.

    :param str: attribute type e.g. 'U002'
    :return: type of attribute as string e.g. 'U'
    :rtype: str

    """

    return att[0:1]


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
    elif atttyp(att) in ("E", "I", "L", "U"):  # integer
        val = int.from_bytes(valb, byteorder="little", signed=atttyp(att) == "I")
    elif atttyp(att) == "R":  # floating point
        val = struct.unpack("<f" if attsiz(att) == 4 else "<d", valb)[0]
    elif atttyp(att) == "A":  # array of unsigned integers
        val = []
        for i in range(attsiz(att)):
            val.append(valb[i])
    else:
        raise ube.UBXTypeError(f"Unknown attribute type {att}")
    return val


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


def cel2cart(elevation: float, azimuth: float) -> tuple:
    """
    Convert celestial coordinates (degrees) to Cartesian coordinates.

    :param float elevation: elevation
    :param float azimuth: azimuth
    :return: cartesian x,y coordinates
    :rtype: tuple
    """

    if not (isinstance(elevation, (float, int)) and isinstance(azimuth, (float, int))):
        return (0, 0)
    ele, azi = [c * pi / 180 for c in (elevation, azimuth)]
    x = cos(azi) * cos(ele)
    y = sin(azi) * cos(ele)
    return (x, y)


def cfgkey2name(keyid: int) -> tuple:
    """
    Return key name and data type for given
    configuration database hexadecimal key.

    :param int keyID: config key as integer e.g. 0x20930001
    :return: tuple of (keyname, type)
    :rtype: tuple: (str, str)
    :raises: UBXMessageError

    """

    try:
        val = None
        for key, val in ubcdb.UBX_CONFIG_DATABASE.items():
            (kid, typ) = val
            if keyid == kid:
                return (key, typ)

        # undocumented configuration database key
        # type is derived from keyID
        key = f"CFG_{hex(keyid)}"
        typ = f"X{ubcdb.UBX_CONFIG_STORSIZE[int(hex(keyid)[2:3])]:03d}"
        return (key, typ)

    except KeyError as err:
        raise ube.UBXMessageError(
            f"Invalid configuration database key {hex(keyid)}"
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


def dop2str(dop: float) -> str:
    """
    Convert Dilution of Precision float to descriptive string.

    :param float dop: dilution of precision as float
    :return: dilution of precision as string
    :rtype: str

    """

    if dop == 0:
        dops = "N/A"
    elif dop <= 1:
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


def escapeall(val: bytes) -> str:
    """
    Escape all byte characters e.g. b'\\\\x73' rather than b`s`

    :param bytes val: bytes
    :return: string of escaped bytes
    :rtype: str
    """

    return "b'{}'".format("".join(f"\\x{b:02x}" for b in val))


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


def getinputmode(data: bytes) -> int:
    """
    Return input message mode (SET or POLL).

    :param bytes data: raw UBX input message
    :return: message mode (1 = SET, 2 = POLL)
    :rtype: int
    """

    if (
        len(data) == 8
        or data[2:4] == b"\x06\x8b"  # CFG-VALGET
        or (
            data[2:4]
            in (
                b"\x06\x01",
                b"\x06\x02",
                b"\x06\x03",
                b"\x06\x31",
            )  # CFG-INF, CFG-MSG, CFG-PRT, CFG-TP5
            and len(data) <= 10
        )
    ):
        return POLL
    return SET


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


def gpsfix2str(fix: int) -> str:
    """
    Convert GPS fix integer to descriptive string.

    :param int fix: GPS fix type (0-5)
    :return: GPS fix type as string
    :rtype: str

    """

    try:
        return FIXTYPE[fix]
    except KeyError:
        return str(fix)


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
        bfh = str(bytes.fromhex(rawl))
        hextbl += f" | {bfh:<67} |\n"

    return hextbl


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


def itow2utc(itow: int, leaps: int = LEAPOFFSET) -> datetime.time:
    """
    Convert GPS Time Of Week to UTC time

    :param int itow: GPS Time Of Week in milliseconds
    :param int leaps: leapsecond offset
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = EPOCH0 + timedelta(seconds=(itow / 1000) - leaps)
    return utc.time()


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


def msgclass2bytes(msgclass: int, msgid: int) -> bytes:
    """
    Convert message class/id integers to bytes.

    :param int msgClass: message class as integer e.g. 6
    :param int msgID: message ID as integer e.g. 1
    :return: message class as bytes e.g. b'/x06/x01'
    :rtype: bytes

    """

    return (val2bytes(msgclass, ubt.U1), val2bytes(msgid, ubt.U1))


def msgstr2bytes(msgclass: str, msgid: str) -> bytes:
    """
    Convert plain text UBX message class to bytes.

    :param str msgClass: message class as str e.g. 'CFG'
    :param str msgID: message ID as str e.g. 'CFG-MSG'
    :return: message class as bytes e.g. b'/x06/x01'
    :rtype: bytes
    :raises: UBXMessageError

    """

    try:
        return (
            key_from_val(ubt.UBX_CLASSES, msgclass),
            key_from_val(ubt.UBX_MSGIDS, msgid)[1:2],
        )
    except KeyError as err:
        raise ube.UBXMessageError(
            f"Undefined message, class {msgclass}, id {msgid}"
        ) from err


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


def process_monver(msg: object) -> dict:
    """
    Process parsed MON-VER sentence into dictionary of
    hardware, firmware and software version identifiers.

    :param UBXMessage msg: UBX MON-VER config message
    :return: dict of version information
    :rtype: dict
    """

    exts = []
    fw_version = "N/A"
    rom_version = "N/A"
    gnss_supported = ""
    model = ""
    sw_version = getattr(msg, "swVersion", b"N/A")
    sw_version = sw_version.replace(b"\x00", b"").decode()
    sw_version = sw_version.replace("ROM CORE", "ROM")
    sw_version = sw_version.replace("EXT CORE", "Flash")
    hw_version = getattr(msg, "hwVersion", b"N/A")
    hw_version = hw_version.replace(b"\x00", b"").decode()

    for i in range(9):
        ext = getattr(msg, f"extension_{i+1:02d}", b"")
        ext = ext.replace(b"\x00", b"").decode()
        exts.append(ext)
        if "FWVER=" in exts[i]:
            fw_version = exts[i].replace("FWVER=", "")
        if "PROTVER=" in exts[i]:
            rom_version = exts[i].replace("PROTVER=", "")
        if "PROTVER " in exts[i]:
            rom_version = exts[i].replace("PROTVER ", "")
        if "MOD=" in exts[i]:
            model = exts[i].replace("MOD=", "")
            hw_version = f"{model} {hw_version}"
        for gnss in (
            "GPS",
            "GLO",
            "GAL",
            "BDS",
            "SBAS",
            "IMES",
            "QZSS",
            "NAVIC",
        ):
            if gnss in exts[i]:
                gnss_supported = gnss_supported + gnss + " "

    verdata = {}
    verdata["swversion"] = sw_version
    verdata["hwversion"] = hw_version
    verdata["fwversion"] = fw_version
    verdata["romversion"] = rom_version
    verdata["gnss"] = gnss_supported

    return verdata


def protocol(raw: bytes) -> int:
    """
    Gets protocol of raw message.

    :param bytes raw: raw (binary) message
    :return: protocol type (1 = NMEA, 2 = UBX, 4 = RTCM3, 0 = unknown)
    :rtype: int
    """

    p = raw[0:2]
    if p == UBX_HDR:
        return UBX_PROTOCOL
    if p in NMEA_HDR:
        return NMEA_PROTOCOL
    if p[0] == 0xD3 and (p[1] & ~0x03) == 0:
        return RTCM3_PROTOCOL
    return 0


def utc2itow(utc: datetime, leaps: int = LEAPOFFSET) -> tuple:
    """
    Convert UTC datetime to GPS Week Number, Time Of Week

    :param datetime utc: datetime
    :param int leaps: leapsecond offset
    :return: GPS Week Number, Time of Week in milliseconds
    :rtype: tuple

    """

    wno = int((utc - EPOCH0).total_seconds() / SIW)
    sow = EPOCH0 + timedelta(seconds=wno * SIW)
    itow = int(((utc - sow).total_seconds() + leaps) * 1000)
    return wno, itow


def val2bytes(val, att: str) -> bytes:
    """
    Convert value to bytes for given UBX attribute type.

    :param object val: attribute value e.g. 25
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as bytes
    :rtype: bytes
    :raises: UBXTypeError

    """

    try:
        if not isinstance(val, ATTTYPE[atttyp(att)]):
            raise TypeError(
                f"Attribute type {att} value {val} must be {ATTTYPE[atttyp(att)]}, not {type(val)}"
            )
    except KeyError as err:
        raise ube.UBXTypeError(f"Unknown attribute type {att}") from err

    if atttyp(att) == "X":  # byte
        valb = val
    elif atttyp(att) == "C":  # char
        valb = val.encode("utf-8", "backslashreplace") if isinstance(val, str) else val
    elif atttyp(att) in ("E", "I", "L", "U"):  # integer
        valb = val.to_bytes(attsiz(att), byteorder="little", signed=atttyp(att) == "I")
    elif atttyp(att) == "R":  # floating point
        valb = struct.pack("<f" if attsiz(att) == 4 else "<d", float(val))
    elif atttyp(att) == "A":  # array of unsigned integers
        valb = b""
        for i in range(attsiz(att)):
            valb += val[i].to_bytes(1, byteorder="little", signed=False)
    return valb


def val2signmag(val: int, att: str) -> int:
    """
    Convert signed integer to sign magnitude binary representation.

    High-order bit represents sign (0 +ve, 1 -ve).

    :param int val: value
    :param str att: attribute type e.g. "U024"
    :return: sign magnitude representation of value
    :rtype: int
    """

    return (abs(val) & pow(2, attsiz(att)) - 1) | ((1 if val < 0 else 0) << attsiz(att))


def val2sphp(val: float, scale: float = 1e-7) -> tuple:
    """
    Convert a float value into separate standard and high precisions components,
    multiplied by a scaling factor to render them as integers, as required by some
    CFG and NAV messages.

    e.g. 48.123456789 becomes (481234567, 89)

    :param float val: value as float
    :param float scale: scaling factor e.g. 1e-7
    :return: tuple of (standard precision, high precision)
    :rtype: tuple
    """

    val = val / scale
    val_sp = trunc(val)
    val_hp = round((val - val_sp) * 100)
    return val_sp, val_hp


def val2twoscomp(val: int, att: str) -> int:
    """
    Convert signed integer to two's complement binary representation.

    :param int val: value
    :param str att: attribute type e.g. "U024"
    :return: two's complement representation of value
    :rtype: int
    """

    return val & pow(2, attsiz(att)) - 1
