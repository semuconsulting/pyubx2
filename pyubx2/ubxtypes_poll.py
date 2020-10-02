# pylint: disable=unused-import
'''
UBX Protocol payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
Response payloads are defined in UBX_PAYLOADS_GET

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

@author: semuadmin
'''

from pyubx2.ubxtypes_core import U1, I1, X1, U2, I2, X2, U4, I4 , X4 , R4 , X6, R8 , C06, C10, C30, C32, CH

UBX_PAYLOADS_POLL = {
'AID-ALM': {
},
'AID-ALM-SV': {
'svid': U1
},
'AID-ALPSRV': {
'idSize': U1,
'type': U1,
'ofs': U2,
'size': U2,
'fileId': U2,
'dataSize': U2,
'id1': U1,
'id2': U1,
'id3': U4
},
'AID-ALP': {
'predTow': U4,
'predDur': U4,
'age': I4,
'predWno': U2,
'almWno': U2,
'reserved1': U4,
'svs': U1,
'reserved2': U1,
'reserved3': U2
},
'AID-AOP': {
},
'AID-AOP-SV': {
'svid': U1
},
'AID-DATA': {
},
'AID-EPH': {
},
'AID-EPH-SV': {
'svid': U1
},
'AID-HUI': {
},
'AID-INI': {
},
'AID-REQ': {
},
'CFG-ANT': {
},
'CFG-DAT': {
},
'CFG-EKF': {
},
'CFG-FXN': {
},
'CFG-INF': {
'protocolID': U1
},
'CFG-MSG': {
'msgClass': U1,
'msgID': U1
},
'CFG-NAV5': {
},
'CFG-NAVX5': {
},
'CFG-NMEA': {
},
'CFG-PM2': {
},
'CFG-PM': {
},
'CFG-PRT': {
},
'CFG-PRT-IO': {
'portID': U1
},
'CFG-RATE': {
},
'CFG-RINV': {
},
'CFG-RXM': {
},
'CFG-SBAS': {
},
'CFG-TMODE2': {
},
'CFG-TMODE': {
},
'CFG-TP5': {
},
'CFG-TP5-TPX': {
'tIdx': U1
},
'CFG-TP': {
},
'CFG-USB': {
},
'RXM-ALM': {
},
'RXM-ALM-SV': {
'svid': U1
},
'RXM-EPH': {
},
'RXM-EPH-SV': {
'svid': U1
},
}
