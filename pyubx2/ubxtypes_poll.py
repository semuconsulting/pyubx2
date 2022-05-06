"""
UBX Protocol Polling payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
(e.g. query configuration; request monitoring, receiver management, logging or sensor fusion status)
Response payloads are defined in UBX_PAYLOADS_GET

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

Information sourced from u-blox Interface Specifications © 2013-2021, u-blox AG

:author: semuadmin
"""

from pyubx2.ubxtypes_core import U1, U2, U4

UBX_PAYLOADS_POLL = {
    # AID messages are deprecated in favour of MGA messages in >=Gen8
    "AID-ALM": {
        "group": (
            "None",
            {
                "svid": U1,
            },
        ),
    },
    "AID-AOP": {
        "group": (
            "None",
            {
                "svid": U1,
            },
        ),
    },
    "AID-EPH": {
        "group": (
            "None",
            {
                "svid": U1,
            },
        ),
    },
    "AID-DATA": {},
    "AID-HUI": {},
    "AID-INI": {},
    "AID-REQ": {},
    # *************************************************
    "CFG-ANT": {},
    "CFG-BATCH": {},
    "CFG-DAT": {},
    "CFG-DGNSS": {},
    "CFG-DOSC": {},
    "CFG-DYNSEED": {},
    "CFG-EKF": {},
    "CFG-ESFA": {},
    "CFG-ESFALG": {},
    "CFG-ESFG": {},
    "CFG-ESFGWT": {},
    "CFG-ESFWT": {},
    "CFG-ESRC": {},
    "CFG-FIXSEED": {},
    "CFG-FXN": {},
    "CFG-GEOFENCE": {},
    "CFG-GNSS": {},
    "CFG-INF": {"protocolID": U1},
    "CFG-ITFM": {},
    "CFG-LOGFILTER": {},
    "CFG-MSG": {"msgClass": U1, "msgID": U1},
    "CFG-NAV5": {},
    "CFG-NAVX5": {},
    "CFG-NMEA": {},
    "CFG-NVS": {},
    "CFG-ODO": {},
    "CFG-PM2": {},
    # 'CFG-PM': {
    # },
    "CFG-PMS": {},
    "CFG-PRT": {"portID": U1},
    "CFG-PWR": {},
    "CFG-RATE": {},
    "CFG-RINV": {},
    "CFG-RXM": {},
    "CFG-SBAS": {},
    "CFG-SENIF": {},
    "CFG-SLAS": {},
    "CFG-SMGR": {},
    "CFG-SPT": {},
    "CFG-TMODE2": {},
    "CFG-TMODE3": {},
    # 'CFG-TMODE': {
    # },
    "CFG-TP5": {},
    "CFG-TP5-TPX": {"tIdx": U1},
    # 'CFG-TP': {
    # },
    "CFG-TXSLOT": {},
    "CFG-USB": {},
    "CFG-VALGET": {
        "version": U1,
        "layer": U1,
        "position": U2,
        "group": ("None", {"keys": U4}),  # repeating group
    },
    # *************************************************
    "ESF-ALG": {},
    "ESF-INS": {},
    "ESF-STATUS": {},
    # *************************************************
    "LOG-BATCH": {},
    "LOG-INFO": {},
    # *************************************************
    "MGA-DBD": {},
    # *************************************************
    "MON-COMMS": {},
    "MON-GNSS": {},
    "MON-HW": {},
    "MON-HW2": {},
    "MON-HW3": {},
    "MON-IO": {},
    "MON-MSGPP": {},
    "MON-PATCH": {},
    "MON-RF": {},
    "MON-RXBUF": {},
    "MON-SMGR": {},
    "MON-SPAN": {},
    "MON-TXBUF": {},
    "MON-VER": {},
    # *************************************************
    "NAV-AOPSTATUS": {},
    "NAV-ATT": {},
    "NAV-CLOCK": {},
    "NAV-COV": {},
    "NAV-DGPS": {},
    "NAV-DOP": {},
    "NAV-EELL": {},
    "NAV-EKFSTATUS": {},
    "NAV-EOE": {},
    "NAV-GEOFENCE": {},
    "NAV-HPPOSECEF": {},
    "NAV-HPPOSLLH": {},
    "NAV-NMI": {},
    "NAV-ODO": {},
    "NAV-ORB": {},
    "NAV-PL": {},
    "NAV-POSECEF": {},
    "NAV-POSLLH": {},
    "NAV-PVT": {},
    "NAV-RELPOSNED": {},
    "NAV-RESETODO": {},
    "NAV-SAT": {},
    "NAV-SBAS": {},
    "NAV-SIG": {},
    "NAV-SLAS": {},
    "NAV-SOL": {},
    "NAV-STATUS": {},
    "NAV-SVINFO": {},
    "NAV-SVIN": {},
    "NAV-TIMEBDS": {},
    "NAV-TIMEGAL": {},
    "NAV-TIMEGLO": {},
    "NAV-TIMEGPS": {},
    "NAV-TIMELS": {},
    "NAV-TIMEQZSS": {},
    "NAV-TIMEUTC": {},
    "NAV-VELECEF": {},
    "NAV-VELNED": {},
    # *************************************************
    "NAV2-CLOCK": {},
    "NAV2-COV": {},
    "NAV2-DOP": {},
    "NAV2-EOE": {},
    "NAV2-ODO": {},
    "NAV2-POSECEF": {},
    "NAV2-POSLLH": {},
    "NAV2-PVT": {},
    "NAV2-SAT": {},
    "NAV2-SBAS": {},
    "NAV2-SIG": {},
    "NAV2-STATUS": {},
    "NAV2-TIMEBDS": {},
    "NAV2-TIMEGAL": {},
    "NAV2-TIMEGLO": {},
    "NAV2-TIMEGPS": {},
    "NAV2-TIMELS": {},
    "NAV2-TIMEUTC": {},
    "NAV2-VELECEF": {},
    "NAV2-VELNED": {},
    # *************************************************
    "RXM-ALM": {},
    "RXM-COR": {},
    "RXM-EPH": {},
    "RXM-IMES": {},
    "RXM-MEASX": {},
    "RXM-POSREQ": {},
    "RXM-RAW": {},
    "RXM-RAWX": {},
    "RXM-RLM": {},
    "RXM-RTCM": {},
    "RXM-SFRB": {},
    "RXM-SFRBX": {},
    "RXM-SPARTN": {},
    "RXM-SPARTN-KEY": {},
    "RXM-SVSI": {},
    "RXM-TM": {},
    # *************************************************
    "SEC-SIG": {},
    "SEC-SIGLOG": {},
    "SEC-SIGN": {},
    "SEC-UNIQID": {},
    # *************************************************
    "TIM-DOSC": {},
    "TIM-FCHG": {},
    "TIM-SMEAS": {},
    "TIM-SVIN": {},
    "TIM-TM2": {},
    "TIM-TOS": {},
    "TIM-TP": {},
    "TIM-VCOCAL": {},
    "TIM-VRFY": {},
    # *************************************************
    "UPD-SOS": {},
}
