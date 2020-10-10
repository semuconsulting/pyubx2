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
X6 = 'X06'  # Bitfield 6
R8 = 'R08'  # Float (IEEE 754) Double Precision 8
C06 = 'C06'  # ASCII / ISO 8859.1 Encoding 6
C10 = 'C10'  # ASCII / ISO 8859.1 Encoding 10
C30 = 'C30'  # ASCII / ISO 8859.1 Encoding 30
C32 = 'C32'  # ASCII / ISO 8859.1 Encoding 32
CH = 'CH'  # ASCII / ISO 8859.1 Encoding Variable Length
VALID_TYPES = (U1, I1, X1, U2, I2, X2, U3, U4, I4 , X4 , R4 , R8 , X6, C06, C10, C30, C32, CH)

'''
THESE ARE THE UBX PROTOCOL MESSAGE CLASSES
'''
UBX_CLASSES = {
b'\x05':'ACK',  # Ack/Nack Messages: as replies to CFG Input Messages
b'\x0B':'AID',  # AssistNow Aiding Messages: Ephemeris, Almanac, other A-GPS data input
b'\x06':'CFG',  # Configuration Input Messages: Set Dynamic Model, Set DOP Mask, Set Baud Rate, etc.
b'\x10':'ESF',  # External Sensor Fusion Messages: External sensor measurements and status information
b'\x04':'INF',  # Information Messages: Printf-Style Messages, with IDs such as Error, Warning, Notice
b'\x0A':'MON',  # Monitoring Messages: Communication Status, CPU Load, Stack Usage, Task Status
b'\x01':'NAV',  # Navigation Results: Position, Speed, Time, Acc, Heading, DOP, SVs used
b'\x02':'RXM',  # Receiver Manager Messages: Satellite Status, RTC Status
b'\x0D':'TIM',  # Timing Messages: Timepulse Output, Timemark Results
b'\x66':'BAD'}  # Non-existent class for error testing

'''
THESE ARE THE UBX PROTOCOL CORE MESSAGE IDENTITIES
Payloads for each of these identities are defined in the ubxtypes_* modules
'''
UBX_MSGIDS = {
# ACK
b'\x05':{
b'\x01':'ACK-ACK',
b'\x00':'ACK-NAK'},
# AID
b'\x0B':{
b'\x30':'AID-ALM',
b'\x32':'AID-ALPSRV',
b'\x50':'AID-ALP',
b'\x33':'AID-AOP',
b'\x10':'AID-DATA',
b'\x31':'AID-EPH',
b'\x02':'AID-HUI',
b'\x01':'AID-INI',
b'\x00':'AID-REQ'},
# CFG
b'\x06':{
b'\x13':'CFG-ANT',
b'\x09':'CFG-CFG',
b'\x06':'CFG-DAT',
b'\x12':'CFG-EKF',
b'\x29':'CFG-ESFGWT',
b'\x0E':'CFG-FXN',
b'\x02':'CFG-INF',
b'\x39':'CFG-ITFM',
b'\x01':'CFG-MSG',
b'\x24':'CFG-NAV5',
b'\x23':'CFG-NAVX5',
b'\x17':'CFG-NMEA',
b'\x22':'CFG-NVS',
b'\x3B':'CFG-PM2',
b'\x32':'CFG-PM',
b'\x00':'CFG-PRT',
b'\x08':'CFG-RATE',
b'\x34':'CFG-RINV',
b'\x04':'CFG-RST',
b'\x11':'CFG-RXM',
b'\x16':'CFG-SBAS',
b'\x3D':'CFG-TMODE2',
b'\x1D':'CFG-TMODE',
b'\x31':'CFG-TP5',
b'\x07':'CFG-TP',
b'\x1B':'CFG-USB'},
# ESF
b'\x10':{
b'\x02':'ESF-MEAS',
b'\x10':'ESF-STATUS'},
# INF
b'\x04':{
b'\x04':'INF-DEBUG',
b'\x00':'INF-ERROR',
b'\x02':'INF-NOTICE',
b'\x03':'INF-TEST',
b'\x01':'INF-WARNING'},
# MON
b'\x0A':{
b'\x28':'MON-GNSS', 
b'\x0B':'MON-HW2',
b'\x09':'MON-HW',
b'\x02':'MON-IO',
b'\x06':'MON-MSGPP',
b'\x27':'MON-PATCH',
b'\x07':'MON-RXBUF',
b'\x21':'MON-RXR',
b'\x2E':'MON-SMGR',
b'\x08':'MON-TXBUF',
b'\x04':'MON-VER'},
#  NAV
b'\x01':{
b'\x60':'NAV-AOPSTATUS',
b'\x05':'NAV-ATT',  # TODO
b'\x22':'NAV-CLOCK',
b'\x31':'NAV-DGPS',
b'\x04':'NAV-DOP',
b'\x40':'NAV-EKFSTATUS',
b'\x61':'NAV-EOE',
b'\x39':'NAV-GEOFENCE',
b'\x13':'NAV-HPPOSECEF',  # TODO
b'\x14':'NAV-HPPOSLLH',  # TODO
b'\x28':'NAV-NMI',  # TODO
b'\x09':'NAV-ODO',
b'\x34':'NAV-ORB',
b'\x01':'NAV-POSECEF',
b'\x02':'NAV-POSLLH',
b'\x07':'NAV-PVT',
b'\x3C':'NAV-RELPOSNED',  # TODO
b'\x35':'NAV-SAT',
b'\x32':'NAV-SBAS',
b'\x43':'NAV-SIG',  # TODO
b'\x42':'NAV-SLAS',  # TODO
b'\x06':'NAV-SOL',
b'\x03':'NAV-STATUS',
b'\x30':'NAV-SVINFO',
b'\x3B':'NAV-SVIN',  # TODO
b'\x24':'NAV-TIMEBDS',
b'\x25':'NAV-TIMEGAL',
b'\x23':'NAV-TIMEGLO',
b'\x20':'NAV-TIMEGPS',
b'\x26':'NAV-TIMELS',
b'\x27':'NAV-TIMEQZSS',  # TODO
b'\x21':'NAV-TIMEUTC',
b'\x11':'NAV-VELECEF',
b'\x12':'NAV-VELNED'},
# RXM
b'\x02':{
b'\x30':'RXM-ALM',
b'\x31':'RXM-EPH',
b'\x41':'RXM-PMREQ',
b'\x10':'RXM-RAW',
b'\x11':'RXM-SFRB',
b'\x20':'RXM-SVSI'},
# TIM
b'\x0D':{
b'\x04':'TIM-SVIN',
b'\x03':'TIM-TM2',
b'\x01':'TIM-TP',
b'\x06':'TIM-VRFY'},
# TESTING
b'\x66':{
b'\x66':'BAD-BAD'}  # for error testing
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
b'\xF1\x00': 'UBX-00',  # Lat/Long Position Data
b'\xF1\x03': 'UBX-03',  # Satellite Status
b'\xF1\x04': 'UBX-04',  # Time of Day and Clock Information
b'\xF1\x05': 'UBX-05',  # Lat/Long Position Data
b'\xF1\x06': 'UBX-06',  # Lat/Long Position Data
b'\xF1\x40': 'UBX-40',  # Set NMEA message output rate
b'\xF1\x41': 'UBX-41',  # Set Protocols and Baudrate
b'\xF0\x0A': 'DTM',  # Datum Reference
b'\xF0\x09': 'GBS',  # GNSS Satellite Fault Detection
b'\xF0\x00': 'GGA',  # Global positioning system fix data
b'\xF0\x01': 'GLL',  # Latitude and longitude, with time of position fix and status
b'\xF0\x40': 'GPQ',  # Poll message
b'\xF0\x06': 'GRS',  # GNSS Range Residuals
b'\xF0\x02': 'GSA',  # GNSS DOP and Active Satellites
b'\xF0\x07': 'GST',  # GNSS Pseudo Range Error Statistics
b'\xF0\x03': 'GSV',  # GNSS Satellites in View
b'\xF0\x04': 'RMC',  # Recommended Minimum data
b'\xF0\x0E': 'THS',  # TRUE Heading and Status
b'\xF0\x41': 'TXT',  # Text Transmission
b'\xF0\x05': 'VTG',  # Course over ground and Groundspeed
b'\xF0\x08': 'ZDA',  # Time and Date
}
