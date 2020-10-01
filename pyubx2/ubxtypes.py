# pylint: disable=fixme, line-too-long
'''
UBX Protocol globals and constants, including payload definitions

Based on u-blox 6 receiver datasheet:
https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf

Created on 27 Sep 2020

@author: semuadmin
'''

UBX_HDR = b'\xB5\x62'
NMEA_HDR = b'\x24'  # '$'

'''
THESE ARE THE UBX PROTOCOL PAYLOAD ATTRIBUTE TYPES
'''
U1 = 'U01'  # Unsigned Char
I1 = 'I01'  # Signed Char 1 2's complement
X1 = 'X01'  # Bitfield 1
U2 = 'U02'  # Unsigned Short
I2 = 'I02'  # Signed Short
X2 = 'X02'  # Bitfield 2
U4 = 'U04'  # Unsigned Long 4
I4 = 'I04'  # Signed Long 4 2's complement
X4 = 'X04'  # Bitfield 4
R4 = 'R04'  # Float (IEEE 754) Single Precision 4
R8 = 'R08'  # Float (IEEE 754) Double Precision 8
C06 = 'C06'  # ASCII / ISO 8859.1 Encoding 6
C10 = 'C10'  # ASCII / ISO 8859.1 Encoding 10
C30 = 'C30'  # ASCII / ISO 8859.1 Encoding 30
C32 = 'C32'  # ASCII / ISO 8859.1 Encoding 32
CH = 'CH'  # ASCII / ISO 8859.1 Encoding Variable Length
VALID_TYPES = (U1, I1, X1, U2, I2, X2, U4, I4 , X4 , R4 , R8 , C06, C10, C30, C32, CH)

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
THESE ARE THE UBX PROTOCOL MESSAGE IDENTITIES
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
b'\x0B':'MON-HW2',
b'\x09':'MON-HW',
b'\x02':'MON-IO',
b'\x06':'MON-MSGPP',
b'\x07':'MON-RXBUF',
b'\x21':'MON-RXR',
b'\x08':'MON-TXBUF',
b'\x04':'MON-VER'},
#  NAV
b'\x01':{
b'\x60':'NAV-AOPSTATUS',
b'\x22':'NAV-CLOCK',
b'\x31':'NAV-DGPS',
b'\x04':'NAV-DOP',
b'\x40':'NAV-EKFSTATUS',
b'\x01':'NAV-POSECEF',
b'\x02':'NAV-POSLLH',
b'\x32':'NAV-SBAS',
b'\x06':'NAV-SOL',
b'\x03':'NAV-STATUS',
b'\x30':'NAV-SVINFO',
b'\x20':'NAV-TIMEGPS',
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
# TODO add UBX message types
UBX_CONFIG_MESSAGES = {
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

'''
THESE ARE THE PAYLOAD DEFINITIONS FOR _INPUT_ MESSAGES _FROM_ THE RECEIVER
(i.e. Navigation Status, Get or Info messages)

NB: Attribute names must be unique within each message class/id
'''
# TODO add the rest as and when I can be bothered
UBX_PAYLOADS_INPUT = {
'ACK-ACK': {
'clsID': U1,
'msgID': U1
},
'ACK-NAK': {
'clsID': U1,
'msgID': U1
},
'CFG-DAT':{
'datumNum': U2,
'datumName': C06,
'majA': R8,
'flat': R8,
'dX': R4,
'dY': R4,
'dZ': R4,
'rotX': R4,
'rotY': R4,
'rotZ': R4,
'scale': R4
},
'CFG-INF': {
'ProtocolID': U1,
'reserved0': U1,
'reserved1': U2,
'infMsgMaskDDC': X1,
'infMsgMaskUART1': X1,
'infMsgMaskUART2': X1,
'infMsgMaskUSB': X1,
'infMsgMaskSPI': X1,
'reserved3': X1
},
'CFG-MSG': {
'msgClass': U1,
'msgID': U1,
'rateDDC': U1,
'rateUART1': U1,
'rateUART2': U1,
'rateUSB': U1,
'rateSPI': U1,
'reserved': U1
},
'CFG-PRT': {
'PortID': U1,
'reserved0': U1,
'txReady': X2,
'mode': X4,
'baudRate': U4,
'inProtoMask': X2,
'outProtoMask': X2,
'reserved4': U2,
'reserved5': U2
},
'INF-DEBUG': {
'message': CH
},
'INF-ERROR': {
'message': CH
},
'INF-NOTICE': {
'message': CH
},
'INF-TEST': {
'message': CH
},
'INF-WARNING': {
'message': CH
},
'NAV-AOPSTATUS': {
'iTOW': U4,
'config': U1,
'status': U1,
'reserved0': U1,
'reserved1': U1,
'avail': U4,
'reserved2': U4,
'reserved3': U4
},
'NAV-CLOCK': {
'iTOW': U4,
'clkB': I4,
'clkD': I4,
'tAcc': U4,
'fAcc': U4
},
'NAV-DGPS': {
'iTOW': U4,
'age': I4,
'baseId': I2,
'baseHealth': I2,
'numCh': U1,
'status': U1,
'reserved1': U2,
'channels' : {  # repeating group
'svid' : U1,
'flags': U1,
'ageC' : U2,
'prc': R4,
'prrc': R4
}
},
'NAV-DOP': {
'iTOW': U4,
'gDOP': U2,
'pDOP': U2,
'tDOP': U2,
'vDOP': U2,
'hDOP': U2,
'nDOP': U2,
'eDOP': U2
},
'NAV-EKFSTATUS': {
'pulses': I4,
'period': I4,
'gyroMean': U4,
'temperature': I2,
'direction': I1
},
'NAV-POSECEF': {
'iTOW': U4,
'ecefX': I4,
'ecefY': I4,
'ecefZ': I4,
'pAcc': U4
},
'NAV-POSLLH': {
'iTOW': U4,
'lon': I4,
'lat': I4,
'height': I4,
'hMSL': I4,
'HAcc': U4,
'vAcc': U4
},
'NAV-SBAS': {
'iTOW': U4,
'geo' : U1,
'mode:' : U1,
'sys': I1,
'service': X1,
'numCh': U1,
'reserved01': U1,
'reserved02': U1,
'reserved03': U1,
'channels': {  # repeating group
'svid': U1,
'flags': U1,
'udre': U1,
'svSys': U1,
'svService': U1,
'reserved1': U1,
'prc': I2,
'reserved2': U2,
'ic': I2
}
},
'NAV-SOL': {
'iTOW': U4,
'fTOW': I4,
'week': I2,
'gpsFix': U1,
'flags': X1,
'ecefX': I4,
'ecefY': I4,
'ecefZ': I4,
'pAcc': U4,
'ecefVX': I4,
'ecefVY': I4,
'ecefVZ': I4,
'sAcc': U4,
'pDOP': U2,
'reserved1': U1,
'numSV': U1,
'reserved2': U4
},
'NAV-STATUS': {
'iTOW': U4,
'gpsFix': U1,
'flags': X1,
'fixStat': X1,
'flags2': X1,
'ttff': U4,
'msss': U4
},
'NAV-SVINFO': {
'iTOW': U4,
'numCh': U1,
'globalFlags': X1,
'reserved2': U2,
'channels': {  # repeating group
'chn': U1,
'svid': U1,
'flags': X1,
'quality': X1,
'cno': U1,
'elev': I1,
'azim': I2,
'prRes': I4}
},
'NAV-TIMEGPS': {
'iTOW': U4,
'fTOW': I4,
'week': I2,
'leapS': I1,
'valid': X1,
'tAcc': U4
},
'NAV-TIMEUTC': {
'iTOW': U4,
'tAcc': U1,
'nano': I4,
'year': U2,
'month': U1,
'day': U1,
'hour': U1,
'min': U1,
'sec': U1,
'validflags': X1
},
'NAV-VELECEF': {
'iTOW': U4,
'ecefVX': I4,
'ecefVY': I4,
'ecefVZ': I4,
'sAcc': U4
},
'NAV-VELNED': {
'iTOW': U4,
'velN': I4,
'velE': I4,
'velD': I4,
'speed': U4,
'gSpeed': U4,
'heading': I4,
'sAcc': U4,
'cAcc': U4
}
}

'''
THESE ARE THE PAYLOAD DEFINITIONS FOR _OUTPUT_ MESSAGES _TO_ THE RECEIVER
(i.e. Poll or Set messages)

NB: Attribute names must be unique within each message class/id
'''
# TODO add the rest as and when I can be bothered
UBX_PAYLOADS_OUTPUT = {
'CFG-MSG': {
'msgClass': U1,
'msgID': U1
}
}
