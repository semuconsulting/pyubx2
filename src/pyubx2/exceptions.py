"""
UBX Custom Exception Types.

Created on 27 Sep 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""


class ParameterError(Exception):
    """Parameter Error Class."""


class GNSSStreamError(Exception):
    """Generic Stream Error Class."""


class UBXParseError(Exception):
    """
    UBX Parsing error.
    """


class UBXStreamError(Exception):
    """
    UBX Streaming error.
    """


class UBXMessageError(Exception):
    """
    UBX Undefined message class/id.
    Essentially a prompt to add missing payload types to UBX_PAYLOADS.
    """


class UBXTypeError(Exception):
    """
    UBX Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to UBX_PAYLOADS.
    """
