"""
Collection of UBX helper methods which can be used
outside the UBXMessage or UBXReader classes

Created on 15 Dec 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from datetime import datetime, timedelta
from pyubx2.ubxtypes_core import GNSSLIST


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
    Convert GPS Time Of Week to UTC time.

    :param int itow: GPS Time Of Week
    :return: UTC time hh.mm.ss
    :rtype: datetime.time

    """

    utc = datetime(1980, 1, 6) + timedelta(seconds=(itow / 1000) - (35 - 19))
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
