"""
ubxvariants.py

Various routines to get payload dictionaries for message
types which exist in multiple variants for the same
message class, id and mode.

Created on 20 May 2024

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from pyubx2.exceptions import UBXMessageError
from pyubx2.ubxhelpers import val2bytes
from pyubx2.ubxtypes_core import GET, POLL, SET, U1, UBX_MSGIDS
from pyubx2.ubxtypes_get import UBX_PAYLOADS_GET
from pyubx2.ubxtypes_poll import UBX_PAYLOADS_POLL
from pyubx2.ubxtypes_set import UBX_PAYLOADS_SET


def get_cfgtp5_dict(**kwargs) -> dict:
    """
    Select appropriate CFG-TP5 POLL payload definition by checking
    presence of tpIdx or payload argument.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict

    """

    lp = 0
    if "payload" in kwargs:
        lp = len(kwargs["payload"])
    elif "tpIdx" in kwargs:
        lp = 1
    print(f"DEBUG TP5 dict {kwargs} len payload {lp}")
    if lp == 1:
        return UBX_PAYLOADS_POLL["CFG-TP5-TPX"]
    return UBX_PAYLOADS_POLL["CFG-TP5"]  # pragma: no cover


def get_mga_dict(msg: bytes, mode: int, **kwargs) -> dict:
    """
    Select appropriate MGA payload definition by checking
    value of 'type' attribute (1st byte of payload).

    :param str mode: mode (0=GET, 1=SET, 2=POLL)
    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "type" in kwargs:
        typ = val2bytes(kwargs["type"], U1)
    elif "payload" in kwargs:
        typ = kwargs["payload"][0:1]
    else:
        raise UBXMessageError(
            "MGA message definitions must include type or payload keyword"
        )
    identity = UBX_MSGIDS[msg + typ]
    if mode == SET:
        return UBX_PAYLOADS_SET[identity]
    return UBX_PAYLOADS_GET[identity]


def get_rxmpmreq_dict(**kwargs) -> dict:
    """
    Select appropriate RXM-PMREQ payload definition by checking
    the 'version' keyword or payload length.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    lpd = 0
    if "version" in kwargs:  # assume longer version
        lpd = 16
    elif "payload" in kwargs:
        lpd = len(kwargs["payload"])
    else:
        raise UBXMessageError(
            "RXM-PMREQ message definitions must include version or payload keyword"
        )
    if lpd == 16:
        return UBX_PAYLOADS_SET["RXM-PMREQ"]  # long
    return UBX_PAYLOADS_SET["RXM-PMREQ-S"]  # short


def get_rxmpmp_dict(**kwargs) -> dict:
    """
    Select appropriate RXM-PMP payload definition by checking
    value of 'version' attribute (1st byte of payload).

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "version" in kwargs:
        ver = val2bytes(kwargs["version"], U1)
    elif "payload" in kwargs:
        ver = kwargs["payload"][0:1]
    else:
        raise UBXMessageError(
            "RXM-PMP message definitions must include version or payload keyword"
        )
    if ver == b"\x00":
        return UBX_PAYLOADS_SET["RXM-PMP-V0"]
    return UBX_PAYLOADS_SET["RXM-PMP-V1"]


def get_rxmrlm_dict(**kwargs) -> dict:
    """
    Select appropriate RXM-RLM payload definition by checking
    value of 'type' attribute (2nd byte of payload).

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "type" in kwargs:
        typ = val2bytes(kwargs["type"], U1)
    elif "payload" in kwargs:
        typ = kwargs["payload"][1:2]
    else:
        raise UBXMessageError(
            "RXM-RLM message definitions must include type or payload keyword"
        )
    if typ == b"\x01":
        return UBX_PAYLOADS_GET["RXM-RLM-S"]  # short
    return UBX_PAYLOADS_GET["RXM-RLM-L"]  # long


def get_cfgnmea_dict(**kwargs) -> dict:
    """
    Select appropriate payload definition version for older
    generations of CFG-NMEA message by checking payload length.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "payload" in kwargs:
        lpd = len(kwargs["payload"])
    else:
        raise UBXMessageError(
            "CFG-NMEA message definitions must include payload keyword"
        )
    if lpd == 4:
        return UBX_PAYLOADS_GET["CFG-NMEAvX"]
    if lpd == 12:
        return UBX_PAYLOADS_GET["CFG-NMEAv0"]
    return UBX_PAYLOADS_GET["CFG-NMEA"]


def get_aopstatus_dict(**kwargs) -> dict:
    """
    Select appropriate payload definition version for older
    generations of NAV-AOPSTATUS message by checking payload length.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "payload" in kwargs:
        lpd = len(kwargs["payload"])
    else:
        raise UBXMessageError(
            "NAV-AOPSTATUS message definitions must include payload keyword"
        )
    if lpd == 20:
        return UBX_PAYLOADS_GET["NAV-AOPSTATUS-L"]
    return UBX_PAYLOADS_GET["NAV-AOPSTATUS"]


def get_relposned_dict(**kwargs) -> dict:
    """
    Select appropriate NAV-RELPOSNED payload definition by checking
    value of 'version' attribute (1st byte of payload).

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    if "version" in kwargs:
        ver = val2bytes(kwargs["version"], U1)
    elif "payload" in kwargs:
        ver = kwargs["payload"][0:1]
    else:
        raise UBXMessageError(
            "NAV-RELPOSNED message definitions must include version or payload keyword"
        )
    if ver == b"\x00":
        return UBX_PAYLOADS_GET["NAV-RELPOSNED-V0"]
    return UBX_PAYLOADS_GET["NAV-RELPOSNED"]


def get_timvcocal_dict(**kwargs) -> dict:
    """
    Select appropriate TIM-VCOCAL SET payload definition by checking
    the payload length.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict
    :raises: UBXMessageError

    """

    lpd = 1
    typ = 0
    if "type" in kwargs:
        typ = kwargs["type"]
    elif "payload" in kwargs:
        lpd = len(kwargs["payload"])
    else:
        raise UBXMessageError(
            "TIM-VCOCAL SET message definitions must include type or payload keyword"
        )
    if lpd == 1 and typ == 0:
        return UBX_PAYLOADS_SET["TIM-VCOCAL-V0"]  # stop cal
    return UBX_PAYLOADS_SET["TIM-VCOCAL"]  # cal


def get_cfgdat_dict(**kwargs) -> dict:
    """
    Select appropriate CFG-DAT SET payload definition by checking
    presence of datumNum keyword or payload length of 2 bytes.

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict

    """

    lpd = 0
    if "payload" in kwargs:
        lpd = len(kwargs["payload"])
    if lpd == 2 or "datumNum" in kwargs:
        return UBX_PAYLOADS_SET["CFG-DAT-NUM"]  # datum num set
    return UBX_PAYLOADS_SET["CFG-DAT"]  # manual datum set


def get_secsig_dict(**kwargs) -> dict:
    """
    Select appropriate SEC-SIG GET payload definition by checking
    value of 'version' attribute (1st byte of payload).

    :param kwargs: optional payload key/value pairs
    :return: dictionary representing payload definition
    :rtype: dict

    """

    if "version" in kwargs:
        ver = val2bytes(kwargs["version"], U1)
    elif "payload" in kwargs:
        ver = kwargs["payload"][0:1]
    else:
        raise UBXMessageError(
            "SEC-SIG message definitions must include version or payload keyword"
        )
    if ver == b"\x01":
        return UBX_PAYLOADS_GET["SEC-SIG-V1"]
    return UBX_PAYLOADS_GET["SEC-SIG-V2"]


VARIANTS = {
    POLL: {b"\x06\x31": get_cfgtp5_dict},  # CFG-TP5
    SET: {
        b"\x13\x00": get_mga_dict,  # MGA GPS
        b"\x13\x02": get_mga_dict,  # MGA GAL
        b"\x13\x03": get_mga_dict,  # MGA BDS
        b"\x13\x05": get_mga_dict,  # MGA QZSS
        b"\x13\x06": get_mga_dict,  # MGA GLO
        b"\x13\x21": get_mga_dict,  # MGA FLASH
        b"\x13\x40": get_mga_dict,  # MGA INI
        b"\x02\x72": get_rxmpmp_dict,  # RXM-PMP
        b"\x02\x41": get_rxmpmreq_dict,  # RXM-PMREQ
        b"\x0d\x15": get_timvcocal_dict,  # TIM-VCOCAL
        b"\x06\x06": get_cfgdat_dict,  # CFG-DAT
    },
    GET: {
        b"\x13\x21": get_mga_dict,  # MGA FLASH
        b"\x13\x60": get_mga_dict,  # MGA ACK NAK
        b"\x02\x72": get_rxmpmp_dict,  # RXM-PMP
        b"\x02\x59": get_rxmrlm_dict,  # RXM-RLM
        b"\x06\x17": get_cfgnmea_dict,  # CFG-NMEA
        b"\x01\x60": get_aopstatus_dict,  # NAV-AOPSTATUS
        b"\x01\x3C": get_relposned_dict,  # NAV-RELPOSNED
        b"\x27\x09": get_secsig_dict,  # SEC-SIG
    },
}
