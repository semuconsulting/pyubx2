'''
UBX Custom Exception Types

Created on 27 Sep 2020

@author: semuadmin
'''


class UBXParseError(ValueError):
    '''
    UBX Parsing error.
    '''


class UBXMessageError(KeyError):
    '''
    UBX Undefined message class/id.
    Essentially a prompt to add missing payload types to UBX_PAYLOADS.
    '''


class UBXTypeError(KeyError):
    '''
    UBX Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to UBX_PAYLOADS.
    '''

