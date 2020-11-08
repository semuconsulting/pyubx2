# pylint: disable=unused-import
"""
UBX Protocol Polling payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
Response payloads are defined in UBX_PAYLOADS_GET

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

@author: semuadmin
"""
# pylint: disable=unused-import, too-many-lines, line-too-long

from pyubx2.ubxtypes_core import U1

UBX_PAYLOADS_POLL = {
    # AID messages are deprecated in favour of MGA messages in >=Gen8
    "AID-ALM": {},
    "AID-ALM-SV": {"svid": U1},
    "AID-AOP": {},
    "AID-AOP-SV": {"svid": U1},
    "AID-DATA": {},
    "AID-EPH": {},
    "AID-EPH-SV": {"svid": U1},
    "AID-HUI": {},
    "AID-INI": {},
    # *************************************************
    "CFG-ANT": {},
    "CFG-DAT": {},
    "CFG-DOSC": {},
    "CFG-DYNSEED": {},
    "CFG-ESRC": {},
    "CFG-FIXSEED": {},
    "CFG-GEOFENCE": {},
    "CFG-GNSS": {},
    "CFG-INF": {"protocolID": U1},
    "CFG-ITFM": {},
    "CFG-LOGFILTER": {},
    "CFG-MSG": {"msgClass": U1, "msgID": U1},
    "CFG-NAV5": {},
    "CFG-NAVX5": {},
    "CFG-NMEA": {},
    "CFG-ODO": {},
    "CFG-PM2": {},
    # 'CFG-PM': {
    # },
    "CFG-PMS": {},
    "CFG-PRT": {},
    "CFG-PRT-IO": {"portID": U1},
    "CFG-PWR": {},
    "CFG-RATE": {},
    "CFG-RINV": {},
    "CFG-RXM": {},
    "CFG-SBAS": {},
    "CFG-TMODE2": {},
    # 'CFG-TMODE': {
    # },
    "CFG-TP5": {},
    "CFG-TP5-TPX": {"tIdx": U1},
    # 'CFG-TP': {
    # },
    "CFG-TXSLOT": {},
    "CFG-USB": {},
    # *************************************************
    "ESF-STATUS": {},
    # *************************************************
    "LOG-INFO": {},
    # *************************************************
    "MGA-DBD": {},
    # *************************************************
    "MON-GNSS": {},
    "MON-HW2": {},
    "MON-HW": {},
    "MON-IO": {},
    "MON-MGSPP": {},
    "MON-PATCH": {},
    "MON-RXBUF": {},
    "MON-SMGR": {},
    "MON-TXBUF": {},
    "MON-VER": {},
    # *************************************************
    "RXM-IMES": {},
    "RXM-RAWX": {},
    "RXM-SVSI": {},
    # *************************************************
    "TIM-FCHG": {},
    "TIM-SVIN": {},
    "TIM-TM2": {},
    "TIM-TP": {},
    "TIM-VCOCAL": {},
    "TIM-VRFY": {},
    # *************************************************
    "UPD-SOS": {},
}
