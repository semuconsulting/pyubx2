"""
UBX Protocol core globals and constants

Created on 27 Sep 2020

Information sourced from public domain u-blox Interface Specifications © 2013-2021, u-blox AG

:author: semuadmin
"""

UBX_HDR = b"\xb5\x62"
GET = 0
SET = 1
POLL = 2
VALNONE = 0
VALCKSUM = 1
NMEA_PROTOCOL = 1
UBX_PROTOCOL = 2
RTCM3_PROTOCOL = 4
ERR_RAISE = 2
ERR_LOG = 1
ERR_IGNORE = 0

GNSSLIST = {
    0: "GPS",
    1: "SBAS",
    2: "Galileo",
    3: "BeiDou",
    4: "IMES",
    5: "QZSS",
    6: "GLONASS",
    7: "NAVIC",
}

# scaling factor constants
SCAL9 = 1e-9  # 0.000000001
SCAL8 = 1e-8  # 0.00000001
SCAL7 = 1e-7  # 0.0000001
SCAL6 = 1e-6  # 0.000001
SCAL5 = 1e-5  # 0.00001
SCAL4 = 1e-4  # 0.0001
SCAL3 = 1e-3  # 0.001
SCAL2 = 1e-2  # 0.01
SCAL1 = 1e-1  # 0.1
SCALROUND = 12  # number of dp to round scaled attributes to

# **************************************************
# THESE ARE THE UBX PROTOCOL PAYLOAD ATTRIBUTE TYPES
# **************************************************
A250 = "A250"  # Array of 250 bytes, parsed as U1[250]
A256 = "A256"  # Array of 256 bytes, parsed as U1[256]
C2 = "C002"  # ASCII / ISO 8859.1 Encoding 2 bytes
C6 = "C006"  # ASCII / ISO 8859.1 Encoding 6 bytes
C10 = "C010"  # ASCII / ISO 8859.1 Encoding 10 bytes
C30 = "C030"  # ASCII / ISO 8859.1 Encoding 30 bytes
C32 = "C032"  # ASCII / ISO 8859.1 Encoding 32 bytes
CH = "CH"  # ASCII / ISO 8859.1 Encoding Variable Length
E1 = "E001"  # Unsigned Int Enumeration 1 byte
E2 = "E002"  # Unsigned Int Enumeration 2 bytes
E4 = "E004"  # Unsigned Int Enumeration 4 bytes
I1 = "I001"  # Signed Int 2's complement 1 byte
I2 = "I002"  # Signed Int 2's complement 2 bytes
I4 = "I004"  # Signed Int 2's complement 4 bytes
I8 = "I008"  # Signed Int 2's complement 8 bytes
L = "L001"  # Boolean stored as U01
U1 = "U001"  # Unsigned Int 1 byte
U2 = "U002"  # Unsigned Int 2 bytes
U3 = "U003"  # Unsigned Int 3 bytes
U4 = "U004"  # Unsigned Int 4 bytes
U5 = "U005"  # Unsigned Int 5 bytes
U6 = "U006"  # Unsigned Int 6 bytes
U7 = "U007"  # Unsigned Int 7 bytes
U8 = "U008"  # Unsigned Int 8 bytes
U9 = "U009"  # Unsigned Int 9 bytes
U10 = "U010"  # Unsigned Int 10 bytes
U11 = "U011"  # Unsigned Int 11 bytes
U12 = "U012"  # Unsigned Int 12 bytes
U16 = "U016"  # Unsigned Int 16 bytes
U20 = "U020"  # Unsigned Int 20 bytes
U22 = "U022"  # Unsigned Int 22 bytes
U23 = "U023"  # Unsigned Int 23 bytes
U24 = "U024"  # Unsigned Int 24 bytes
U32 = "U032"  # Unsigned Int 32 bytes
U40 = "U040"  # Unsigned Int 40 bytes
U64 = "U064"  # Unsigned Int 64 bytes
X1 = "X001"  # Bitfield 1 byte
X2 = "X002"  # Bitfield 2 bytes
X4 = "X004"  # Bitfield 4 bytes
X6 = "X006"  # Bitfield 6 bytes
X8 = "X008"  # Bitfield 8 bytes
X24 = "X024"  # Bitfield 24 bytes
R4 = "R004"  # Float (IEEE 754) Single Precision 4 bytes
R8 = "R008"  # Float (IEEE 754) Double Precision 8 bytes

# ***********************************************
# THESE ARE THE UBX PROTOCOL CORE MESSAGE CLASSES
# ***********************************************
# pylint: disable=line-too-long
UBX_CLASSES = {
    b"\x01": "NAV",  # Navigation Results: Position, Speed, Time, Acc, Heading, DOP, SVs used
    b"\x02": "RXM",  # Receiver Manager Messages: Satellite Status, RTC Status
    b"\x03": "TRK",  # u-blox Tracking Messages (not documented)
    b"\x04": "INF",  # Information Messages: Printf-Style Messages, with IDs such as Error, Warning, Notice
    b"\x05": "ACK",  # Ack/Nack Messages: as replies to CFG Input Messages
    b"\x06": "CFG",  # Configuration Input Messages: Set Dynamic Model, Set DOP Mask, Set Baud Rate, etc.
    b"\x08": "TUN",  # u-blox Debug Messages (not documented)
    b"\x09": "UPD",  # Firmware Update Messages: Memory/Flash erase/write, Reboot, Flash identification, etc.
    b"\x0a": "MON",  # Monitoring Messages: Communication Status, CPU Load, Stack Usage, Task Status
    b"\x0b": "AID",  # AssistNow Aiding Messages: Ephemeris, Almanac, other A-GPS data input
    b"\x0c": "DBG",  # u-blox Debug Messages (not documented)
    b"\x0d": "TIM",  # Timing Messages: Timepulse Output, Timemark Results
    b"\x10": "ESF",  # External Sensor Fusion Messages: External sensor measurements and status information
    b"\x13": "MGA",  # Multiple GNSS Assistance Messages: Assistance data for various GNSS
    b"\x21": "LOG",  # Logging Messages: Log creation, deletion, info and retrieval
    b"\x27": "SEC",  # Security Feature Messages
    b"\x28": "HNR",  # High Rate Navigation Messages
    b"\x29": "NAV2",  # Navigation 2 Results: Position, Speed, Time, Acc, Heading, DOP, SVs used
    b"\xf0": "NMEA-Standard",  # Standard NMEA Messages: Used for message rate configuration via CFG-MSG
    b"\xf1": "NMEA-Proprietary",  # Proprietary NMEA Messages: Used for message rate configuration via CFG-MSG
    b"\xf4": "RTCM2",  # RTCM2 Messages: Used for message rate configuration via CFG-MSG
    b"\xf5": "RTCM3",  # RTCM3 Messages: Used for message rate configuration via CFG-MSG
    b"\xf6": "SPARTN",  # SPARTN Messages: Used for message rate configuration via CFG-MSG
    b"\xf7": "NMEA-NAV2",  # NMEA-NAV2 Messages: Used for message rate configuration via CFG-MSG
    b"\x66": "FOO",  # Dummy message class for testing
}

# ***************************************************************************
# THESE ARE THE UBX PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the ubxtypes_* modules
# ***************************************************************************
UBX_MSGIDS = {
    b"\x05\x01": "ACK-ACK",
    b"\x05\x00": "ACK-NAK",
    # *********************************************************************
    # AssistNow Aiding messages
    # Since Gen 8, these are deprecated in favour of MGA
    # *********************************************************************
    b"\x0b\x30": "AID-ALM",
    b"\x0b\x50": "AID-ALP",
    b"\x0b\x32": "AID-ALPSRV",
    b"\x0b\x33": "AID-AOP",
    b"\x0b\x10": "AID-DATA",
    b"\x0b\x31": "AID-EPH",
    b"\x0b\x02": "AID-HUI",
    b"\x0b\x01": "AID-INI",
    b"\x0b\x00": "AID-REQ",
    # *********************************************************************
    # Configuration messages
    # Since Gen 9, many of these are deprecated in favour of CFG-VALSET/DEL
    # *********************************************************************
    b"\x06\x13": "CFG-ANT",
    b"\x06\x93": "CFG-BATCH",
    b"\x06\x09": "CFG-CFG",
    b"\x06\x06": "CFG-DAT",  # two versions
    b"\x06\x70": "CFG-DGNSS",
    b"\x06\x61": "CFG-DOSC",
    b"\x06\x85": "CFG-DYNSEED",
    b"\x06\x12": "CFG-EKF",
    b"\x06\x56": "CFG-ESFALG",
    b"\x06\x4c": "CFG-ESFA",
    b"\x06\x4d": "CFG-ESFG",
    b"\x06\x82": "CFG-ESFWT",
    b"\x06\x29": "CFG-ESFGWT",
    b"\x06\x60": "CFG-ESRC",
    b"\x06\x84": "CFG-FIXSEED",
    b"\x06\x0e": "CFG-FXN",  # deprecated, use CFG-PM2
    b"\x06\x69": "CFG-GEOFENCE",
    b"\x06\x3e": "CFG-GNSS",
    b"\x06\x5c": "CFG-HNR",
    b"\x06\x02": "CFG-INF",
    b"\x06\x39": "CFG-ITFM",
    b"\x06\x47": "CFG-LOGFILTER",
    b"\x06\x01": "CFG-MSG",
    b"\x06\x24": "CFG-NAV5",
    b"\x06\x23": "CFG-NAVX5",
    b"\x06\x17": "CFG-NMEA",  # NB: 3 versions of this
    b"\x06\x22": "CFG-NVS",
    b"\x06\x1e": "CFG-ODO",
    b"\x06\x32": "CFG-PM",  # obsolete M5/6
    b"\x06\x3b": "CFG-PM2",
    b"\x06\x86": "CFG-PMS",
    b"\x06\x00": "CFG-PRT",
    b"\x06\x57": "CFG-PWR",
    b"\x06\x08": "CFG-RATE",
    b"\x06\x34": "CFG-RINV",
    b"\x06\x04": "CFG-RST",
    b"\x06\x11": "CFG-RXM",
    b"\x06\x16": "CFG-SBAS",
    b"\x06\x88": "CFG-SENIF",
    b"\x06\x8D": "CFG-SLAS",
    b"\x06\x62": "CFG-SMGR",
    b"\x06\x64": "CFG-SPT",
    b"\x06\x1d": "CFG-TMODE",  # obsolete M5/6
    b"\x06\x3d": "CFG-TMODE2",
    b"\x06\x71": "CFG-TMODE3",
    b"\x06\x07": "CFG-TP",  # obsolete M5/6
    b"\x06\x31": "CFG-TP5",
    b"\x06\x53": "CFG-TXSLOT",
    b"\x06\x1b": "CFG-USB",
    b"\x06\x8c": "CFG-VALDEL",
    b"\x06\x8b": "CFG-VALGET",
    b"\x06\x8a": "CFG-VALSET",
    # ***************************************************************
    # External Sensor Fusion messages
    # ***************************************************************
    b"\x10\x14": "ESF-ALG",
    b"\x10\x04": "ESF-CAL",
    b"\x10\x15": "ESF-INS",
    b"\x10\x02": "ESF-MEAS",
    b"\x10\x03": "ESF-RAW",
    b"\x10\x13": "ESF-RESETALG",  # referenced but not defined in specs
    b"\x10\x10": "ESF-STATUS",
    # ***************************************************************
    # High Rate Navigation messages
    # ***************************************************************
    b"\x28\x01": "HNR-ATT",
    b"\x28\x02": "HNR-INS",
    b"\x28\x00": "HNR-PVT",
    # ***************************************************************
    # Information messages
    # ***************************************************************
    b"\x04\x04": "INF-DEBUG",
    b"\x04\x00": "INF-ERROR",
    b"\x04\x02": "INF-NOTICE",
    b"\x04\x03": "INF-TEST",
    b"\x04\x01": "INF-WARNING",
    # ***************************************************************
    # Logging messages
    # ***************************************************************
    b"\x21\x11": "LOG-BATCH",
    b"\x21\x07": "LOG-CREATE",
    b"\x21\x03": "LOG-ERASE",
    b"\x21\x0e": "LOG-FINDTIME",
    b"\x21\x08": "LOG-INFO",
    b"\x21\x09": "LOG-RETRIEVE",
    b"\x21\x10": "LOG-RETRIEVEBATCH",
    b"\x21\x0b": "LOG-RETRIEVEPOS",
    b"\x21\x0f": "LOG-RETRIEVEPOSEXTRA",
    b"\x21\x0d": "LOG-RETRIEVESTRING",
    b"\x21\x04": "LOG-STRING",
    # ***************************************************************
    # Multiple GNSS Assistance messages
    # These need special handling as MSGIDs alone are not unique;
    # message identity is determined by 'type' attribute in payload
    # ***************************************************************
    b"\x13\x60\x01": "MGA-ACK-DATA0",
    b"\x13\x60\x00": "MGA-NAK-DATA0",
    b"\x13\x20\x00": "MGA-ANO",
    b"\x13\x03\x01": "MGA-BDS-EPH",
    b"\x13\x03\x02": "MGA-BDS-ALM",
    b"\x13\x03\x04": "MGA-BDS-HEALTH",
    b"\x13\x03\x05": "MGA-BDS-UTC",
    b"\x13\x03\x06": "MGA-BDS-IONO",
    b"\x13\x80": "MGA-DBD",
    b"\x13\x21\x01": "MGA-FLASH-DATA",
    b"\x13\x21\x02": "MGA-FLASH-STOP",
    b"\x13\x21\x03": "MGA-FLASH-ACK",
    b"\x13\x02\x01": "MGA-GAL-EPH",
    b"\x13\x02\x02": "MGA-GAL-ALM",
    b"\x13\x02\x03": "MGA-GAL-TIMEOFFSET",
    b"\x13\x02\x05": "MGA-GAL-UTC",
    b"\x13\x06\x01": "MGA-GLO-EPH",
    b"\x13\x06\x02": "MGA-GLO-ALM",
    b"\x13\x06\x03": "MGA-GLO-TIMEOFFSET",
    b"\x13\x00\x01": "MGA-GPS-EPH",
    b"\x13\x00\x02": "MGA-GPS-ALM",
    b"\x13\x00\x04": "MGA-GPS-HEALTH",
    b"\x13\x00\x05": "MGA-GPS-UTC",
    b"\x13\x00\x06": "MGA-GPS-IONO",
    b"\x13\x40\x00": "MGA-INI-POS-XYZ",
    b"\x13\x40\x01": "MGA-INI-POS-LLH",
    b"\x13\x40\x10": "MGA-INI-TIME-UTC",
    b"\x13\x40\x11": "MGA-INI-TIME-GNSS",
    b"\x13\x40\x20": "MGA-INI-CLKD",
    b"\x13\x40\x21": "MGA-INI-FREQ",
    b"\x13\x40\x30": "MGA-INI-EOP",
    b"\x13\x05\x01": "MGA-QZSS-EPH",
    b"\x13\x05\x02": "MGA-QZSS-ALM",
    b"\x13\x05\x04": "MGA-QZSS-HEALTH",
    # ***************************************************************
    # Hardware Monitoring messages
    # ***************************************************************
    b"\x0a\x36": "MON-COMMS",
    b"\x0a\x28": "MON-GNSS",
    b"\x0a\x09": "MON-HW",
    b"\x0a\x0b": "MON-HW2",
    b"\x0a\x37": "MON-HW3",
    b"\x0a\x02": "MON-IO",  # deprecated, use MON-COMMS
    b"\x0a\x06": "MON-MSGPP",  # deprecated, use MON-COMMS
    b"\x0a\x27": "MON-PATCH",
    b"\x0a\x38": "MON-RF",
    b"\x0a\x07": "MON-RXBUF",  # deprecated, use MON-COMMS
    b"\x0a\x21": "MON-RXR",
    b"\x0a\x2e": "MON-SMGR",
    b"\x0a\x31": "MON-SPAN",
    b"\x0a\x2f": "MON-SPT",
    b"\x0a\x39": "MON-SYS",
    b"\x0a\x08": "MON-TXBUF",
    b"\x0a\x04": "MON-VER",
    # ***************************************************************
    # Navigation messages
    # ***************************************************************
    b"\x01\x60": "NAV-AOPSTATUS",
    b"\x01\x05": "NAV-ATT",
    b"\x01\x22": "NAV-CLOCK",
    b"\x01\x36": "NAV-COV",
    b"\x01\x31": "NAV-DGPS",
    b"\x01\x04": "NAV-DOP",
    b"\x01\x3d": "NAV-EELL",
    b"\x01\x40": "NAV-EKFSTATUS",  # deprecated, use ESF-STATUS and ESF-MEAS
    b"\x01\x61": "NAV-EOE",
    b"\x01\x39": "NAV-GEOFENCE",
    b"\x01\x13": "NAV-HPPOSECEF",
    b"\x01\x14": "NAV-HPPOSLLH",
    b"\x01\x28": "NAV-NMI",
    b"\x01\x09": "NAV-ODO",
    b"\x01\x34": "NAV-ORB",
    b"\x01\x62": "NAV-PL",
    b"\x01\x01": "NAV-POSECEF",
    b"\x01\x02": "NAV-POSLLH",
    b"\x01\x17": "NAV-PVAT",
    b"\x01\x07": "NAV-PVT",
    b"\x01\x3c": "NAV-RELPOSNED",  # two versions
    b"\x01\x10": "NAV-RESETODO",
    b"\x01\x35": "NAV-SAT",
    b"\x01\x32": "NAV-SBAS",
    b"\x01\x43": "NAV-SIG",
    b"\x01\x42": "NAV-SLAS",
    b"\x01\x06": "NAV-SOL",
    b"\x01\x03": "NAV-STATUS",
    b"\x01\x30": "NAV-SVINFO",  # deprecated, use NAV-SAT
    b"\x01\x3b": "NAV-SVIN",
    b"\x01\x24": "NAV-TIMEBDS",
    b"\x01\x25": "NAV-TIMEGAL",
    b"\x01\x23": "NAV-TIMEGLO",
    b"\x01\x20": "NAV-TIMEGPS",
    b"\x01\x26": "NAV-TIMELS",
    b"\x01\x63": "NAV-TIMENAVIC",
    b"\x01\x27": "NAV-TIMEQZSS",
    b"\x01\x21": "NAV-TIMEUTC",
    b"\x01\x11": "NAV-VELECEF",
    b"\x01\x12": "NAV-VELNED",
    # ***************************************************************
    # Navigation 2 messages
    # ***************************************************************
    b"\x29\x22": "NAV2-CLOCK",
    b"\x29\x36": "NAV2-COV",
    b"\x29\x04": "NAV2-DOP",
    b"\x29\x3d": "NAV2-EELL",
    b"\x29\x61": "NAV2-EOE",
    b"\x29\x09": "NAV2-ODO",
    b"\x29\x01": "NAV2-POSECEF",
    b"\x29\x02": "NAV2-POSLLH",
    b"\x29\x17": "NAV2-PVAT",
    b"\x29\x07": "NAV2-PVT",
    b"\x29\x35": "NAV2-SAT",
    b"\x29\x32": "NAV2-SBAS",
    b"\x29\x43": "NAV2-SIG",
    b"\x29\x42": "NAV2-SLAS",
    b"\x29\x03": "NAV2-STATUS",
    b"\x29\x3b": "NAV2-SVIN",
    b"\x29\x24": "NAV2-TIMEBDS",
    b"\x29\x25": "NAV2-TIMEGAL",
    b"\x29\x23": "NAV2-TIMEGLO",
    b"\x29\x20": "NAV2-TIMEGPS",
    b"\x29\x26": "NAV2-TIMELS",
    b"\x29\x63": "NAV2-TIMENAVIC",
    b"\x29\x27": "NAV2-TIMEQZSS",
    b"\x29\x21": "NAV2-TIMEUTC",
    b"\x29\x11": "NAV2-VELECEF",
    b"\x29\x12": "NAV2-VELNED",
    # ***************************************************************
    # Receiver Management messages
    # ***************************************************************
    b"\x02\x30": "RXM-ALM",  # obsolete, use AID-ALM or MGA-*-ALM
    b"\x02\x34": "RXM-COR",
    b"\x02\x31": "RXM-EPH",  # obsolete, use AID-EPH or MGA-*-EPH
    b"\x02\x61": "RXM-IMES",
    b"\x02\x84": "RXM-MEAS20",
    b"\x02\x86": "RXM-MEAS50",
    b"\x02\x82": "RXM-MEASC12",
    b"\x02\x80": "RXM-MEASD12",
    b"\x02\x14": "RXM-MEASX",
    b"\x02\x72": "RXM-PMP",  # 2 versions
    b"\x02\x41": "RXM-PMREQ",  # 2 versions
    b"\x02\x40": "RXM-POSREQ",
    b"\x02\x73": "RXM-QZSSL6",
    b"\x02\x10": "RXM-RAW",
    b"\x02\x15": "RXM-RAWX",
    b"\x02\x59": "RXM-RLM",  # 2 versions
    b"\x02\x32": "RXM-RTCM",
    b"\x02\x11": "RXM-SFRB",
    b"\x02\x13": "RXM-SFRBX",
    b"\x02\x33": "RXM-SPARTN",
    b"\x02\x36": "RXM-SPARTN-KEY",
    b"\x02\x20": "RXM-SVSI",
    b"\x02\x74": "RXM-TM",
    # ***************************************************************
    # Security messages
    # ***************************************************************
    b"\x27\x09": "SEC-SIG",
    b"\x27\x10": "SEC-SIGLOG",
    b"\x27\x01": "SEC-SIGN",
    b"\x27\x03": "SEC-UNIQID",
    # ***************************************************************
    # Timing messages
    # ***************************************************************
    b"\x0d\x11": "TIM-DOSC",
    b"\x0d\x16": "TIM-FCHG",
    b"\x0d\x17": "TIM-HOC",
    b"\x0d\x13": "TIM-SMEAS",
    b"\x0d\x04": "TIM-SVIN",
    b"\x0d\x03": "TIM-TM2",
    b"\x0d\x12": "TIM-TOS",
    b"\x0d\x01": "TIM-TP",
    b"\x0d\x15": "TIM-VCOCAL",  # 2 versions of SET
    b"\x0d\x06": "TIM-VRFY",
    # ***************************************************************
    # Firmware update messages
    # ***************************************************************
    b"\x09\x14": "UPD-SOS",
    # ***************************************************************
    # NMEA Standard message types
    # Used to poll message rates via CFG-MSG; not parsed by pyubx2
    # ***************************************************************
    b"\xf0\x0a": "DTM",  # Datum Reference
    b"\xf0\x45": "GAQ",  # Poll Standard Message - Talker ID GA (Galileo)
    b"\xf0\x44": "GBQ",  # Poll Standard Message - Talker ID GB (BeiDou)
    b"\xf0\x09": "GBS",  # GNSS Satellite Fault Detection
    b"\xf0\x00": "GGA",  # Global positioning system fix data
    b"\xf0\x01": "GLL",  # Latitude and longitude, with time of position fix and status
    b"\xf0\x43": "GLQ",  # Poll Standard Message - Talker ID GL (GLONASS)
    b"\xf0\x42": "GNQ",  # Poll Standard Message - Talker ID GN (Any GNSS)
    b"\xf0\x0d": "GNS",  # GNSS Fix Data
    b"\xf0\x40": "GPQ",  # Poll Standard Message - Talker ID GP (GPS, SBAS)
    b"\xf0\x47": "GQQ",  # Poll Standard Message - Talker ID GQ (QZSS)
    b"\xf0\x06": "GRS",  # GNSS Range Residuals
    b"\xf0\x02": "GSA",  # GNSS DOP and Active Satellites
    b"\xf0\x07": "GST",  # GNSS Pseudo Range Error Statistics
    b"\xf0\x03": "GSV",  # GNSS Satellites in View
    b"\xf0\x0b": "RLM",  # Return Link Message
    b"\xf0\x04": "RMC",  # Recommended Minimum data
    b"\xf0\x0e": "THS",  # TRUE Heading and Status
    b"\xf0\x41": "TXT",  # Text Transmission
    b"\xf0\x0f": "VLW",  # Dual Ground Water Distance
    b"\xf0\x05": "VTG",  # Course over ground and Groundspeed
    b"\xf0\x08": "ZDA",  # Time and Date
    # ***************************************************************
    # NMEA Proprietary message types
    # Used to poll message rates via CFG-MSG; not parsed by pyubx2
    # ***************************************************************
    b"\xf1\x00": "UBX-00",  # aka PUBX-POSITION Lat/Long Position Data
    b"\xf1\x01": "UBX-01",  # unknown - not publicly documented?
    b"\xf1\x03": "UBX-03",  # aka PUBX-SVSTATUS Satellite Status
    b"\xf1\x04": "UBX-04",  # aka PUBX-TIME Time of Day and Clock Information
    b"\xf1\x05": "UBX-05",  # Lat/Long Position Data
    b"\xf1\x06": "UBX-06",  # Lat/Long Position Data
    b"\xf1\x40": "UBX-40",  # Set NMEA message output rate
    b"\xf1\x41": "UBX-41",  # aka PUBX-CONFIG Set Protocols and Baudrate
    # ***************************************************************
    # RTCM3 Message types
    # Used to poll message rates via CFG-MSG; not parsed by pyubx2
    # ***************************************************************
    b"\xf5\x01": "RTCM3-1001",  # L1-only GPS RTK observables (Input)
    b"\xf5\x02": "RTCM3-1002",  # Extended L1-only GPS RTK observables (Input)
    b"\xf5\x03": "RTCM3-1003",  # L1/L2 GPS RTK observables (Input)
    b"\xf5\x04": "RTCM3-1004",  # Extended L1/L2 GPS RTK observables (Input)
    b"\xf5\x05": "RTCM3-1005",  # Stationary RTK reference station ARP (Input/output)
    b"\xf5\x06": "RTCM3-1006",  # Stationary RTK reference station ARP with antenna height (Input)
    b"\xf5\x07": "RTCM3-1007",  # Antenna descriptor (Input)
    b"\xf5\x09": "RTCM3-1009",  # L1-only GLONASS RTK observables (Input)
    b"\xf5\x0a": "RTCM3-1010",  # Extended L1-Only GLONASS RTK observables (Input)
    b"\xf5\xa1": "RTCM3-1011",  # L1&L2 GLONASS RTK observables (Input)
    b"\xf5\xa2": "RTCM3-1012",  # Extended L1&L2 GLONASS RTK observables (Input)
    b"\xf5\x21": "RTCM3-1033",  # Receiver and antenna descriptors (Input)
    b"\xf5\x4a": "RTCM3-1074",  # GPS MSM4 (Input/output)
    b"\xf5\x4b": "RTCM3-1075",  # GPS MSM5 (Input)
    b"\xf5\x4d": "RTCM3-1077",  # GPS MSM7 (Input/output)
    b"\xf5\x54": "RTCM3-1084",  # GLONASS MSM4 (Input/output)
    b"\xf5\x55": "RTCM3-1085",  # GLONASS MSM5 (Input)
    b"\xf5\x57": "RTCM3-1087",  # GLONASS MSM7 (Input/output)
    b"\xf5\x5e": "RTCM3-1094",  # Galileo MSM4 (Input/output)
    b"\xf5\x5f": "RTCM3-1095",  # Galileo MSM5 (Input)
    b"\xf5\x61": "RTCM3-1097",  # Galileo MSM7 (Input/output)
    b"\xf5\x7c": "RTCM3-1124",  # BeiDou MSM4 (Input/output)
    b"\xf5\x7d": "RTCM3-1125",  # BeiDou MSM5 (Input)
    b"\xf5\x7f": "RTCM3-1127",  # BeiDou MSM7 (Input/output)
    b"\xf5\xe6": "RTCM3-1230",  # GLONASS L1 and L2 code-phase biases (Input/output)
    b"\xf5\xfe": "RTCM3-4072",  # Reference station PVT (u-blox proprietary) (Input/output)
    b"\xf5\xfd": "RTCM3-4072",  # Additional reference station information
    # ***************************************************************
    # SPARTN Message types
    # Used to poll message rates via CFG-MSG; not parsed by pyubx2
    # ***************************************************************
    b"\xf6\x01": "SPARTN-0-0",  # GPS orbit, clock, bias (OCB) (Input)
    b"\xf6\x02": "SPARTN-0-1",  # GLONASS orbit, clock, bias (OCB) (Input)
    b"\xf6\x03": "SPARTN-0-2",  # Galileo orbit, clock, bias (OCB) (Input)
    b"\xf6\x0a": "SPARTN-1-0",  # GPS high-precision atmosphere correction (HPAC) (Input)
    b"\xf6\x0b": "SPARTN-1-1",  # GLONASS high-precision atmosphere correction (HPAC) (Input)
    b"\xf6\x0c": "SPARTN-1-2",  # Galileo high-precision atmosphere correction (HPAC) (Input)
    b"\xf6\x13": "SPARTN-2-0",  # Geographic area definition (GAD) (Input)
    # ***************************************************************
    # NMEA-NAV2 Message types
    # Used to poll message rates via CFG-MSG; not parsed by pyubx2
    # ***************************************************************
    b"\xf7\x00": "NMEA-NAV2-00",  #
    b"\xf7\x01": "NMEA-NAV2-01",  #
    b"\xf7\x02": "NMEA-NAV2-02",  #
    b"\xf7\x03": "NMEA-NAV2-03",  #
    b"\xf7\x04": "NMEA-NAV2-04",  #
    b"\xf7\x05": "NMEA-NAV2-05",  #
    b"\xf7\x08": "NMEA-NAV2-08",  #
    b"\xf7\x0d": "NMEA-NAV2-0d",  #
    # ***************************************************************
    # Dummy message for testing only
    # ***************************************************************
    b"\x66\x66": "FOO-BAR",
}
