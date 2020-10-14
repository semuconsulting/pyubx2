# pylint: disable=fixme, line-too-long
'''
UBX Protocol core globals and constants

Based on u-blox 6 receiver datasheet:
https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf

Created on 27 Sep 2020

@author: semuadmin
'''

UBX_HDR = b'\xB5\x62'
INPUT = 0
OUTPUT = 1
GET = 0
SET = 1
POLL = 2

'''
THESE ARE THE UBX PROTOCOL PAYLOAD ATTRIBUTE TYPES
'''
U1 = 'U01'  # Unsigned Char
I1 = 'I01'  # Signed Char 1 2's complement
X1 = 'X01'  # Bitfield 1
U2 = 'U02'  # Unsigned Short
I2 = 'I02'  # Signed Short
X2 = 'X02'  # Bitfield 2
U3 = 'U03'  # Unsigned Long 3
U4 = 'U04'  # Unsigned Long 4
I4 = 'I04'  # Signed Long 4 2's complement
X4 = 'X04'  # Bitfield 4
R4 = 'R04'  # Float (IEEE 754) Single Precision 4
U4 = 'U04'  # Unsigned Long 4
U5 = 'U05'  # Unsigned Long 5
U6 = 'U06'  # Unsigned Long 6
X6 = 'X06'  # Bitfield 6
R8 = 'R08'  # Float (IEEE 754) Double Precision 8
U8 = 'U08'  # Unsigned Long 8
U12 = 'U12'  # Unsigned Long 12
U40 = 'U40'  # Unsigned Long 40
U64 = 'U64'  # Unsigned Long 64
C06 = 'C06'  # ASCII / ISO 8859.1 Encoding 6
C10 = 'C10'  # ASCII / ISO 8859.1 Encoding 10
C30 = 'C30'  # ASCII / ISO 8859.1 Encoding 30
C32 = 'C32'  # ASCII / ISO 8859.1 Encoding 32
CH = 'CH'  # ASCII / ISO 8859.1 Encoding Variable Length
VALID_TYPES = (U1, I1, X1, U2, I2, X2, U3, U4, I4, X4, R4, U5, R8, U6, X6, U12, U40, U64, C06, C10, C30, C32, CH)

'''
THESE ARE THE UBX PROTOCOL MESSAGE CLASSES
'''
UBX_CLASSES = {
b'\x01':'NAV',  # Navigation Results: Position, Speed, Time, Acc, Heading, DOP, SVs used
b'\x02':'RXM',  # Receiver Manager Messages: Satellite Status, RTC Status
b'\x04':'INF',  # Information Messages: Printf-Style Messages, with IDs such as Error, Warning, Notice
b'\x05':'ACK',  # Ack/Nack Messages: as replies to CFG Input Messages
b'\x06':'CFG',  # Configuration Input Messages: Set Dynamic Model, Set DOP Mask, Set Baud Rate, etc.
b'\x09':'UPD',  # Firmware Update Messages: Memory/Flash erase/write, Reboot, Flash identification, etc.
b'\x0A':'MON',  # Monitoring Messages: Communication Status, CPU Load, Stack Usage, Task Status
b'\x0B':'AID',  # AssistNow Aiding Messages: Ephemeris, Almanac, other A-GPS data input
b'\x0D':'TIM',  # Timing Messages: Timepulse Output, Timemark Results
b'\x10':'ESF',  # External Sensor Fusion Messages: External sensor measurements and status information
b'\x13':'MGA',  # Multiple GNSS Assistance Messages: Assistance data for various GNSS
b'\x21':'LOG',  # Logging Messages: Log creation, deletion, info and retrieval
b'\x27':'SEC'  # Security Feature Messages
}

'''
THESE ARE THE UBX PROTOCOL CORE MESSAGE IDENTITIES
Payloads for each of these identities are defined in the ubxtypes_* modules
'''
UBX_MSGIDS = {
b'\x05\x01': 'ACK-ACK',
b'\x05\x00': 'ACK-NAK',
# ***************************************************************
# AID messages are deprecated since Gen 8 in favour of MGA
# ***************************************************************
b'\x0B\x30': 'AID-ALM',
b'\x0B\x33': 'AID-AOP',
b'\x0B\x31': 'AID-EPH',
b'\x0B\x02': 'AID-HUI',
b'\x0B\x01': 'AID-INI',
b'\x06\x13': 'CFG-ANT',
b'\x06\x09': 'CFG-CFG',
b'\x06\x06': 'CFG-DAT',
b'\x06\x61': 'CFG-DOSC',
b'\x06\x85': 'CFG-DYNSEED',
b'\x06\x60': 'CFG-ESRC',
b'\x06\x84': 'CFG-FIXSEED',
b'\x06\x69': 'CFG-GEOFENCE',
b'\x06\x3E': 'CFG-GNSS',
b'\x06\x02': 'CFG-INF',
b'\x06\x39': 'CFG-ITFM',
b'\x06\x47': 'CFG-LOGFILTER',
b'\x06\x01': 'CFG-MSG',
b'\x06\x24': 'CFG-NAV5',
b'\x06\x23': 'CFG-NAVX5',
b'\x06\x17': 'CFG-NMEA',
b'\x06\x1E': 'CFG-ODO',
b'\x06\x3B': 'CFG-PM2',
b'\x06\x86': 'CFG-PMS',
b'\x06\x00': 'CFG-PRT',
b'\x06\x57': 'CFG-PWR',
b'\x06\x08': 'CFG-RATE',
b'\x06\x34': 'CFG-RINV',
b'\x06\x04': 'CFG-RST',
b'\x06\x11': 'CFG-RXM',
b'\x06\x16': 'CFG-SBAS',
b'\x06\x62': 'CFG-SMGR',
b'\x06\x3D': 'CFG-TMODE2',
b'\x06\x31': 'CFG-TP5',
b'\x06\x53': 'CFG-TXSLOT',
b'\x06\x1B': 'CFG-USB',
b'\x10\x10': 'ESF-STATUS',
b'\x04\x04': 'INF-DEBUG',
b'\x04\x00': 'INF-ERROR',
b'\x04\x02': 'INF-NOTICE',
b'\x04\x03': 'INF-TEST',
b'\x04\x01': 'INF-WARNING',
b'\x21\x07': 'LOG-CREATE',
b'\x21\x03': 'LOG-ERASE',
b'\x21\x0E': 'LOG-FINDTIME',
b'\x21\x08': 'LOG-INFO',
b'\x21\x0f': 'LOG-RETRIEVEPOSEXTRA',
b'\x21\x0b': 'LOG-RETRIEVEPOS',
b'\x21\x0d': 'LOG-RETRIEVESTRING',
b'\x21\x09': 'LOG-RETRIEVE',
b'\x21\x04': 'LOG-STRING',
# ***************************************************************
# MGA messages need special handling as MSGIDs are not unique
# Message identity is determined by 'type' attribute in payload
# ***************************************************************
b'\x13\x60\x01': 'MGA-ACK-DATA0',
b'\x13\x60\x00': 'MGA-NAK-DATA0',
b'\x13\x20\x00': 'MGA-ANO',
b'\x13\x03\x01': 'MGA-BDS-EPH',
b'\x13\x03\x02': 'MGA-BDS-ALM',
b'\x13\x03\x04': 'MGA-BDS-HEALTH',
b'\x13\x03\x05': 'MGA-BDS-UTC',
b'\x13\x03\x06': 'MGA-BDS-IONO',
b'\x13\x80': 'MGA-DBD',
b'\x13\x21\x01': 'MGA-FLASH-DATA',
b'\x13\x21\x02': 'MGA-FLASH-STOP',
b'\x13\x21\x03': 'MGA-FLASH-ACK',
b'\x13\x02\x01': 'MGA-GAL-EPH',
b'\x13\x02\x02': 'MGA-GAL-ALM',
b'\x13\x02\x03': 'MGA-GAL-TIMEOFFSET',
b'\x13\x02\x05': 'MGA-GAL-UTC',
b'\x13\x06\x01': 'MGA-GLO-EPH',
b'\x13\x06\x02': 'MGA-GLO-ALM',
b'\x13\x06\x03': 'MGA-GLO-TIMEOFFSET',
b'\x13\x00\x01': 'MGA-GPS-EPH',
b'\x13\x00\x02': 'MGA-GPS-ALM',
b'\x13\x00\x04': 'MGA-GPS-HEALTH',
b'\x13\x00\x05': 'MGA-GPS-UTC',
b'\x13\x00\x06': 'MGA-GPS-IONO',
b'\x13\x40\x00': 'MGA-INI-POS_XYZ',
b'\x13\x40\x01': 'MGA-INI-POS_LLH',
b'\x13\x40\x10': 'MGA-INI-TIME_UTC',
b'\x13\x40\x11': 'MGA-INI-TIME_GNSS',
b'\x13\x40\x20': 'MGA-INI-CLKD',
b'\x13\x40\x21': 'MGA-INI-FREQ',
b'\x13\x40\x30': 'MGA-INI-EOP',
b'\x13\x05\x01': 'MGA-QZSS-EPH',
b'\x13\x05\x02': 'MGA-QZSS-ALM',
b'\x13\x05\x04': 'MGA-QZSS-HEALTH',
b'\x0A\x28': 'MON-GNSS',
b'\x0A\x0B': 'MON-HW2',
b'\x0A\x09': 'MON-HW',
b'\x0A\x02': 'MON-IO',
b'\x0A\x06': 'MON-MSGPP',
b'\x0A\x27': 'MON-PATCH',
b'\x0A\x07': 'MON-RXBUF',
b'\x0A\x21': 'MON-RXR',
b'\x0A\x2E': 'MON-SMGR',
b'\x0A\x08': 'MON-TXBUF',
b'\x0A\x04': 'MON-VER',
b'\x01\x60': 'NAV-AOPSTATUS',
b'\x01\x22': 'NAV-CLOCK',
b'\x01\x31': 'NAV-DGPS',
b'\x01\x04': 'NAV-DOP',
b'\x01\x61': 'NAV-EOE',
b'\x01\x39': 'NAV-GEOFENCE',
b'\x01\x09': 'NAV-ODO',
b'\x01\x34': 'NAV-ORB',
b'\x01\x01': 'NAV-POSECEF',
b'\x01\x02': 'NAV-POSLLH',
b'\x01\x07': 'NAV-PVT',
b'\x01\x10': 'NAV-RESETODO',
b'\x01\x35': 'NAV-SAT',
b'\x01\x32': 'NAV-SBAS',
b'\x01\x06': 'NAV-SOL',
b'\x01\x03': 'NAV-STATUS',
b'\x01\x30': 'NAV-SVINFO',
b'\x01\x24': 'NAV-TIMEBDS',
b'\x01\x25': 'NAV-TIMEGAL',
b'\x01\x23': 'NAV-TIMEGLO',
b'\x01\x20': 'NAV-TIMEGPS',
b'\x01\x26': 'NAV-TIMELS',
b'\x01\x21': 'NAV-TIMEUTC',
b'\x01\x11': 'NAV-VELECEF',
b'\x01\x12': 'NAV-VELNED',
b'\x02\x61': 'RXM-IMES',
b'\x02\x14': 'RXM-MEASX',
b'\x02\x41': 'RXM-PMREQ',
b'\x02\x15': 'RXM-RAWX',
b'\x02\x59': 'RXM-RLM',
b'\x02\x13': 'RXM-SFRBX',
b'\x02\x20': 'RXM-SVSI',
b'\x27\x01': 'SEC-SIGN',
b'\x27\x03': 'SEC-UNIQID',
b'\x0D\x11': 'TIM-DOSC',
b'\x0D\x16': 'TIM-FCHG',
b'\x0D\x17': 'TIM-HOC',
b'\x0D\x13': 'TIM-SMEAS',
b'\x0D\x04': 'TIM-SVIN',
b'\x0D\x03': 'TIM-TM2',
b'\x0D\x12': 'TIM-TOS',
b'\x0D\x01': 'TIM-TP',
b'\x0D\x15': 'TIM-VCOCAL',
b'\x0D\x06': 'TIM-VRFY',
b'\x09\x14': 'UPD-SOS',
}

'''
THESE ARE THE CONFIG MESSAGE CATEGORIES (CFG-MSG)
'''
UBX_CONFIG_CATEGORIES = {
b'\x01' : 'UBX-NAV',
b'\x02' : 'UBX-RXM',
b'\x05' : 'UBX-ACK',
b'\x09' : 'UBX-ESF',
b'\x0A' : 'UBX-MON',
b'\x0B' : 'UBX-AID',
b'\x0D' : 'UBX-TIM',
b'\x10' : 'UBX-ESF',
b'\x13' : 'UBX-MGA',
b'\x21' : 'UBX-LOG',
b'\x27' : 'UBX-SEC',
b'\x28' : 'UBX-HNR',
b'\xF0' : 'NMEA-Standard',
b'\xF1' : 'NMEA-Proprietary',
b'\xF5' : 'RTCM'
}

'''
THESE ARE THE CONFIG MESSAGE TYPES (CFG-MSG)
NB: Available messages will depend on the receiver
'''
# TODO add additional UBX message types for AID, RXM, ESF
UBX_CONFIG_MESSAGES = {
# b'\x0A\x36': 'MON-COMMS',
b'\x01\x60': 'NAV-AOPSTATUS',
b'\x01\x05': 'NAV-ATT',
b'\x01\x22': 'NAV-CLOCK',
b'\x01\x31': 'NAV-DGPS',
b'\x01\x04': 'NAV-DOP',
b'\x01\x40': 'NAV-EKFSTATUS',
b'\x01\x61': 'NAV-EOE',
b'\x01\x39': 'NAV-GEOFENCE',
b'\x01\x13': 'NAV-HPPOSECEF',
b'\x01\x14': 'NAV-HPPOSLLH',
b'\x01\x28': 'NAV-NMI',
b'\x01\x09': 'NAV-ODO',
b'\x01\x34': 'NAV-ORB',
b'\x01\x01': 'NAV-POSECEF',
b'\x01\x02': 'NAV-POSLLH',
b'\x01\x07': 'NAV-PVT',
b'\x01\x3C': 'NAV-RELPOSNED',
b'\x01\x35': 'NAV-SAT',
b'\x01\x32': 'NAV-SBAS',
b'\x01\x43': 'NAV-SIG',
b'\x01\x42': 'NAV-SLAS',
b'\x01\x06': 'NAV-SOL',
b'\x01\x03': 'NAV-STATUS',
b'\x01\x30': 'NAV-SVINFO',
b'\x01\x3B': 'NAV-SVIN',
b'\x01\x24': 'NAV-TIMEBDS',
b'\x01\x25': 'NAV-TIMEGAL',
b'\x01\x23': 'NAV-TIMEGLO',
b'\x01\x20': 'NAV-TIMEGPS',
b'\x01\x26': 'NAV-TIMELS',
b'\x01\x27': 'NAV-TIMEQZSS',
b'\x01\x21': 'NAV-TIMEUTC',
b'\x01\x11': 'NAV-VELECEF',
b'\x01\x12': 'NAV-VELNED',
b'\x02\x61': 'RXM-IMES',
b'\x02\x14': 'RXM-MEASX',
b'\x02\x41': 'RXM-PMREQ',
b'\x02\x15': 'RXM-RAWX',
b'\x02\x59': 'RXM-RLM',
b'\x02\x13': 'RXM-SFRBX',
b'\x02\x20': 'RXM-SVSI',
b'\x0A\x28': 'MON-GNSS',
b'\x0A\x09': 'MON-HW',
b'\x0A\x0B': 'MON-HW2',
# b'\x0A\x37': 'MON-HW3',
b'\x0A\x02': 'MON-IO',
b'\x0A\x06': 'MON-MSGPP',
b'\x0A\x27': 'MON-PATCH',
# b'\x0A\x38': 'MON-RF',
b'\x0A\x07': 'MON-RXBUF',
b'\x0A\x21': 'MON-RXR',
b'\x0A\x2E': 'MON-SMGR',
# b'\x0A\x31': 'MON-SPAN',
b'\x0A\x08': 'MON-TXBUF',
b'\x0A\x04': 'MON-VER',
b'\x21\x07': 'LOG-CREATE',
b'\x21\x03': 'LOG-ERASE',
b'\x21\x0E': 'LOG-FINDTIME',
b'\x21\x08': 'LOG-INFO',
b'\x21\x0f': 'LOG-RETRIEVEPOSEXTRA',
b'\x21\x0b': 'LOG-RETRIEVEPOS',
b'\x21\x0d': 'LOG-RETRIEVESTRING',
b'\x21\x09': 'LOG-RETRIEVE',
b'\x21\x04': 'LOG-STRING',
b'\xF0\x0A': 'DTM',  # Datum Reference
b'\xF0\x44': 'GBQ',  # Poll Standard Message - Talker ID GB (BeiDou)
b'\xF0\x09': 'GBS',  # GNSS Satellite Fault Detection
b'\xF0\x00': 'GGA',  # Global positioning system fix data
b'\xF0\x01': 'GLL',  # Latitude and longitude, with time of position fix and status
b'\xF0\x43': 'GLQ',  # Poll Standard Message - Talker ID GL (GLONASS)
b'\xF0\x42': 'GNQ',  # Poll Standard Message - Talker ID GN (Any GNSS)
b'\xF0\x0D': 'GNS',  # GNSS Fix Data
b'\xF0\x40': 'GPQ',  # Poll Standard Message - Talker ID GP (GPS, SBAS, QZSS)
b'\xF0\x06': 'GRS',  # GNSS Range Residuals
b'\xF0\x02': 'GSA',  # GNSS DOP and Active Satellites
b'\xF0\x07': 'GST',  # GNSS Pseudo Range Error Statistics
b'\xF0\x03': 'GSV',  # GNSS Satellites in View
b'\xF0\x04': 'RMC',  # Recommended Minimum data
b'\xF0\x0E': 'THS',  # TRUE Heading and Status
b'\xF0\x41': 'TXT',  # Text Transmission
b'\xF0\x0F': 'VLW',  # Dual Ground Water Distance
b'\xF0\x05': 'VTG',  # Course over ground and Groundspeed
b'\xF0\x08': 'ZDA',  # Time and Date
b'\xF1\x00': 'UBX-00',  # Lat/Long Position Data
b'\xF1\x03': 'UBX-03',  # Satellite Status
b'\xF1\x04': 'UBX-04',  # Time of Day and Clock Information
b'\xF1\x05': 'UBX-05',  # Lat/Long Position Data
b'\xF1\x06': 'UBX-06',  # Lat/Long Position Data
b'\xF1\x40': 'UBX-40',  # Set NMEA message output rate
b'\xF1\x41': 'UBX-41'  # Set Protocols and Baudrate
}
