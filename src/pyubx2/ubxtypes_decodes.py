"""
UBX Protocol attribute value decode constants.

Created on 26 Aug 2023

Information sourced from public domain u-blox Interface Specifications © 2013-2021, u-blox AG

:author: semuadmin (Steve Smith)
"""

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
"""GNSS code"""

# UBX-CFG-DGNSS
DGNSMODE = {
    2: "RTK float",
    3: "RTK fixed",
    5: "RTK CAR",  # Conservative ambiguity resolution
}
"""Differential correction mode from UBX-CFG-DGNSS"""

# UBX-CFG-GEOFENCE
CONFLVL = {
    0: "no confidence required",
    1: "68%",
    2: "95%",
    3: "99.7%",
    4: "99.99%",
}
"""Confidence level from UBX-CFG-GEOFENCE"""

# UBX-CFG-GNSS
# key is (gnssId, sigCfMask)
SIGCFMASK = {
    (0, 0x01): "GPS L1C/A",
    (0, 0x10): "GPS L2C",
    (0, 0x20): "GPS L5",
    (1, 0x01): "SBAS L1C/A",
    (2, 0x01): "Galileo E1",
    (2, 0x10): "Galileo E5a",
    (2, 0x20): "Galileo E5b",
    (3, 0x01): "BeiDou B1I",
    (3, 0x10): "BeiDou B2I",
    (3, 0x80): "BeiDou B2A",
    (4, 0x01): "IMES L1",
    (5, 0x01): "QZSS L1C/A",
    (5, 0x04): "QZSS L1S",
    (5, 0x10): "QZSS L2C",
    (5, 0x20): "QZSS L5",
    (6, 0x01): "GLONASS L1",
    (6, 0x10): "GLONASS L2",
}
"""
Signal & carrier frequency code from UBX-CFG_GNSS
 - key is (gnssId, sigCfMask)
"""

# UBX-CFG-INF
PROTOCOLID = {
    0: "UBX",
    1: "NMEA",
}
"""Protocol from UBX-CFG-INF"""

# UBX-CFG-NAV5
DYNMODEL = {
    0: "portable",
    2: "stationary",
    3: "pedestrian",
    4: "automotive",
    5: "sea",
    6: "airborne with <1g acceleration",
    7: "airborne with <2g acceleration",
    8: "airborne with <4g acceleration",
    9: "wrist-worn watch",  # (not supported for protocol versions less than 18.00)
    10: "motorbike",  # (supported for protocol versions 19.20, and 35.10)
    11: "robotic lawn mower",  # (supported for protocol versions 33.21)
    12: "electric kick scooter",  # (supported for protocol versions 33.21, and 35.10)
    13: "rail",  # trains and trams
}
"""Dynamic model from UBX-CFG-NAV5"""

# UBX-CFG-NAV5
FIXMODE = {
    1: "2D only",
    2: "3D only",
    3: "auto 2D/3D",
}
"""Fix mode from UBX-CFG-NAV5"""

# UBX-CFG-NMEA
NMEAVERSION = {
    0x4B: "NMEA version 4.11",  # (not available in all products)
    0x41: "NMEA version 4.10",  # (not available in all products)
    0x40: "NMEA version 4.0",  # (not available in all products)
    0x23: "NMEA version 2.3",
    0x21: "NMEA version 2.1",
}
"""NMEA version from UBX-CFG-NMEA"""

# UBX-CFG-NMEA
SVNUMBERING = {
    0: "Strict - Satellites are not output",
    1: "Extended - Use proprietary numbering",  # (see Satellite Numbering)
}
"""Space vehicle numbering from UBX-CFG-NMEA"""

# UBX-CFG-NMEA
MAINTALKERID = {
    0: "Main Talker ID is not overridden",
    1: "Set main Talker ID to 'GP'",
    2: "Set main Talker ID to 'GL'",
    3: "Set main Talker ID to 'GN'",
    4: "Set main Talker ID to 'GA'",  # (not supported for protocol versions less than 15.00)
    5: "Set main Talker ID to 'GB'",  # (not supported for protocol versions less than 15.00)
    6: "Set main Talker ID to 'GQ'",  # (available in NMEA 4.11 and later)
}
"""Main talker ID from UBX-CFG-NMEA"""

# UBX-CFG-NMEA
GSVTALKERID = {
    0: "Use GNSS-specific Talker ID (as defined byNMEA)",
    1: "Use the main Talker ID",
}
"""GSV talker ID from UBX-CFG-NMEA"""

# UBX-CFG-ODO
ODOPROFILE = {0: "running", 1: "cycling", 2: "swimming", 3: "car", 4: "custom"}
"""Odometer profile from UBX-CFG-ODO"""

# UBX-CFG-PRT
CHARLEN = {
    0x00: "5bit",  # (not supported)
    0x01: "6bit",  # (not supported)
    0x10: "7bit",  # (supported only with parity)
    0x11: "8bit",
}
"""Serial port character length from UBX-CFG-PRT"""

PARITY = {
    "000": "Even parity",
    "001": "Odd parity",
    "10X": "No parity",
    "X1X": "Reserved",
}
"""Serial port parity from UBX-CFG-PRT"""

NSTOPBITS = {
    0x00: "1 Stop bit",
    0x01: "1.5 Stop bit",
    0x10: "2 Stop bit",
    0x11: "0.5 Stop bit",
}
"""Serial port stop bits from IBX-CFG-PRT"""

POL = {
    0: "High-active",
    1: "Low-active",
}
"""Serial port polarity from UBX-CFG-PRT"""

SPIMODE = {
    0x00: "SPI Mode 0: CPOL = 0, CPHA = 0",
    0x01: "SPI Mode 1: CPOL = 0, CPHA = 1",
    0x10: "SPI Mode 2: CPOL = 1, CPHA = 0",
    0x11: "SPI Mode 3: CPOL = 1, CPHA = 1",
}
"""SPI mode from UBX-CFG-PRT"""

# UBX-CFG-PWR
STATE = {
    0x52554E20: "GNSS running",
    0x53544F50: "GNSS stopped",
    0x42434B50: "Software backup",  # USB interface will be disabled, other wakeup source is needed.
}
"""Power state from UBX-CFG-PWR"""

# UBX-CFG-RATE
TIMEREF = {
    0: "UTC time",
    1: "GPS time",
    2: "GLONASS time",  # (not supported for protocol versions less than 18.00)
    3: "BeiDou time",  # (not supported for protocol versions less than 18.00)
    4: "Galileo time",  # (not supported for protocol versions less than 18.00)
    5: "NavIC time",  # (not supported for protocol versions less than 29.00)
}
"""Time reference from UBX-CFG-RATE"""

# UBX-CFG-RST
NAVBBRMASK = {
    0x0000: "Hot start",
    0x0001: "Warm start",
    0xFFFF: "Cold start",
}
"""Navigation battery-backed RAM mask from UBX-CFG-RST"""

RESETMODE = {
    0x00: "Hardware reset (watchdog) immediately",
    0x01: "Controlled software reset",
    0x02: "Controlled software reset (GNSS only)",
    0x04: "Hardware reset (watchdog) after shutdown",
    0x08: "Controlled GNSS stop",
    0x09: "Controlled GNSS start",
}
"""Reset mode from UBX-CFG-RST"""

# UBX-CFG-TMODE3
MODE = {
    0: "Disabled",
    1: "Survey In",
    2: "Fixed Mode",  # (true ARP position information required)
}
"""Timing mode from UBX-CFG-TMODE3"""

# UBX-CFG-TP5
GRIDUTCGNSS = {
    0: "UTC",
    1: "GPS",
    2: "GLONASS",
    3: "BeiDou",
    4: "Galileo",  # (not supported for protocol versions less than 18.00)
}
"""Timing Grid UTC GNSS source from UBX-CFG-TP5"""

# UBX-MON-COMMS
PROTIDS = {
    0: "UBX",
    1: "NMEA",
    2: "RTCM2",
    5: "RTCM3",
    6: "SPARTN",
    0xFF: "No protocol reported",
}
"""Protocol IDs from UBX-MON-COMMS"""

# UBX-MON-HW, UBX-MON-RF
ASTATUS = {
    0: "INIT",
    1: "DONTKNOW",
    2: "OK",
    3: "SHORT",
    4: "OPEN",
}
"""Antenna status from UBX-MON-HW, UBX-MON-RF"""

APOWER = {
    0: "OFF",
    1: "ON",
    2: "DONTKNOW",
}
"""Antenna power from UBX-MON-HW, UBX-MON-RF"""

JAMMINGSTATE = {
    0: "unknown or feature disabled",
    1: "ok - no significant jamming",
    2: "warning - interference visible but fix OK",
    3: "critical - interference visible and no fix",
}
"""Jamming state from UBX-MON-HW, UBX-MON-RF"""

# UBX-MON-SYS
BOOTTYPE = {
    0: "Unknown",
    1: "Cold Start",
    2: "Watchdog",
    3: "Hardware reset",
    4: "Hardware backup",
    5: "Software backup",
    6: "Software reset",
    7: "VIO fail",
    8: "VDD_X fail",
    9: "VDD_RF fail",
    10: "V_CORE_HIGH fail",
}
"""Boot type from UBX-MON-SYS"""

# UBX-NAV-GEOFENCE
GEOFENCE_STATUS = {
    0: "Geofencing not available or not reliable",
    1: "Geofencing active",
}
"""Geofence status from UBX-NAV-GEOFENCE"""

COMBSTATE = {
    0: "unknown",
    1: "inside",
    2: "outside",
}
"""Comb state from UBX-NAV-GEOFENCE"""

# UBX-NAV-ORB
HEALTH = {
    0: "unknown",
    1: "healthy",
    2: "not healthy",
}
"""Space vehicle health from UBX-NAV-ORB"""

VISIBILITY = {
    0: "unknown",
    1: "below horizon",
    2: "above horizon",
    3: "above elevation mask",
}
"""Space vehicle visibility from UBX-NAV-ORB"""

# UBX-NAV-PL
PLPOSFRAME = PLVELFRAME = {
    0: "Invalid (not possible to calculate frameconversion)",
    1: "North-East-Down",
    2: "Longitudinal-Lateral-Vertical",
    3: "HorizSemiMajorAxis-HorizSemiMinorAxis-Vertical",
}
"""Position protection level from UBX-NAV-PL"""

# UBX-NAV-PVT
GPSFIX = FIXTYPE = {
    0: "NO FIX",
    1: "DR",
    2: "2D",
    3: "3D",
    4: "GPS + DR",
    5: "TIME ONLY",
}
"""Fix type from UBX-NAV-PVT"""

PSMSTATE = {
    0: "PSM is not active",
    1: "Enabled",
    2: "Acquisition",
    3: "Tracking",
    4: "Power Optimized Tracking",
    5: "Inactive",
}
"""Power save mode state from UBX-NAV-PVT"""

CARRSOLN = {
    0: "NO RTK",
    1: "RTK FLOAT",
    2: "RTK FIXED",
}
"""Carrier phase range solution from UBX-NAV-PVT"""

LASTCORRECTIONAGE = {
    0: 0,
    1: 1,
    2: 2,
    3: 5,
    4: 10,
    5: 15,
    6: 20,
    7: 30,
    8: 45,
    9: 60,
    10: 90,
    11: 120,
}
"""Last DGPS correction age from UBX-NAV-PVT"""

# UBX-NAV-SAT
QUALITYIND = {
    0: "no signal",
    1: "searching signal",
    2: "signal acquired",
    3: "signal detected but unusable",
    4: "code locked and time synchronized",
    5: "code and carrier locked and time synchronized",
    6: "code and carrier locked and time synchronized",
    7: "code and carrier locked and time synchronized",
}
"""Signal quality indicator from UBX-NAV-SAT"""

ORBITSOURCE = {
    0: "no orbit information is available for this SV",
    1: "ephemeris is used",
    2: "almanac is used",
    3: "AssistNow Offline orbit is used",
    4: "AssistNow Autonomous orbit is used",
    5: "other orbit information is used",
    6: "other orbit information is used",
    7: "other orbit information is used",
}
"""Orbit source from UBX-NAV-SAT"""

# UBX-NAV-SBAS
SBASMODE = {
    0: "Disabled",
    1: "Enabled integrity",
    3: "Enabled test mode",
}
"""SBAS (satellite-based augmentation system) mode from UBX-NAV-SBAS"""

SBASSYS = {
    -1: "Unknown",
    0: "WAAS",
    1: "EGNOS",
    2: "MSAS",
    3: "GAGAN",
    16: "GPS",
}
"""SBAS system from UBX-NAV-SBAS"""

SBASINTEGRITYUSED = {
    0: "Unknown",
    1: "Integrity information is not available or SBAS integrity is not enabled",
    2: "Receiver uses only GPS satellites for which integrity information is available",
}
"""SBAS integrity used indicator from UBX-NAV-SBAS"""

# UBX-NAV-SIG
CORRSOURCE = {
    0: "NONE",
    1: "SBAS",
    2: "BeiDou",
    3: "RTCM2",
    4: "RTCM3 OSR",
    5: "RTCM3 SSR",
    6: "QZSS SLAS",
    7: "SPARTN",
    8: "CLAS",  # not used in HPG 2.00
    9: "CLAS",
    10: "LPP OSR",
    11: "LPP SSR",
    12: "GAL HAS",
}
"""DGPS correction source from UBX-NAV-SIG"""

IONOMODEL = {
    0: "none",
    1: "Klobuchar GPS",
    2: "SBAS",
    3: "Klobuchar BeiDou",
    4: "Dual Frequency",  # not used in HPG 2.00
    8: "Dual frequency",
}
"""Ionospheric model type from UBX-NAV-SIG"""

# key is (gnssId, sigId)
SIGID = {
    (0, 0): "GPS L1C/A",
    (0, 3): "GPS L2 CL",
    (0, 4): "GPS L2 CM",
    (0, 6): "GPS L5 I",
    (0, 7): "GPS L5 Q",
    (1, 0): "SBAS L1C/A",
    (2, 0): "Galileo E1 C",
    (2, 1): "Galileo E1 B",
    (2, 3): "Galileo E5 al",
    (2, 4): "Galileo E5 aQ",
    (2, 5): "Galileo E5 bI",
    (2, 6): "Galileo E5 bQ",
    (3, 0): "BeiDou B1I D1",
    (3, 1): "BeiDou B1I D2",
    (3, 2): "BeiDou B2I D1",
    (3, 3): "BeiDou B2I D2",
    (3, 5): "BeiDou B1C",
    (3, 7): "BeiDou B2a",
    (5, 0): "QZSS L1C/A",
    (5, 1): "QZSS L1S",
    (5, 4): "QZSS L2 CM",
    (5, 5): "QZSS L2 CL",
    (5, 8): "QZSS L5 I",
    (5, 9): "QZSS L5 Q",
    (6, 0): "GLONASS L1 OF",
    (6, 2): "GLONASS L2 OF",
    (7, 0): "NavIC L5 A",
}
"""
GNSS, Signal ID from UBX-NAV-SIG
 - key is (gnssId, sigId)
"""

# UBX-NAV-STATUS
SPOOFDETSTATE = {
    0: "unknown or deactivated",
    1: "no spoofing indicated",
    2: "spoofing indicated",
    3: "multiple spoofing indications",
}
"""Spoof detection state from UBX-NAV-STATUS"""

PSMSTATUS = {
    0: "aquisition",
    1: "tracking",
    2: "power optimised tracking",
    3: "inactive",
}
"""Power save mode state from UBX-NAV-STATUS"""

# UBX-NAV-TIME*
UTCSTANDARD = {
    0: "Information not available",
    1: "Communications Research Labratory (CRL), Tokyo, Japan",
    2: "National Institute of Standards and Technology (NIST)",
    3: "U.S. Naval Observatory (USNO)",
    4: "International Bureau of Weights and Measures (BIPM)",
    5: "European laboratories",
    6: "Former Soviet Union (SU)",
    7: "National Time Service Center (NTSC), China",
    8: "National Physics Laboratory India (NPLI)",
    15: "Unknown",
}
"""UTC time standard from UBX-NAV-TIME*"""

SOURCEOFCURLS = {
    0: "Default",
    1: "Derived from time difference between GPS and GLONASS time",
    2: "GPS",
    3: "SBAS",
    4: "BeiDou",
    5: "Galileo",
    6: "Aided data",
    7: "Configured",
    8: "NavIC",
    255: "Unknown",
}
"""Information source for the current number of leap seconds, from UBX-NAV-TIMELS"""

SRCOFLSCHANGE = {
    0: "No source",
    2: "GPS",
    3: "SBAS",
    4: "BeiDou",
    5: "Galileo",
    6: "GLONASS",
    7: "NavIC",
}
"""Information source for the future leap second event, from UBX-NAV-TIMELS"""

ESFALG_AUTOMNTALGON = {
    0: ("AUTOOFF", "automatic alignment is not running"),
    1: ("AUTOON", "automatic alignment is running"),
}
"""autoMntAlgOn from ESF-ALG"""

ESFALG_STATUS = {
    0: ("FIXEDUSED", "user-defined/fixed angles are used"),
    1: ("ALIGNINGRP", "IMU-mount roll/pitch angles alignment is ongoing"),
    2: ("ALIGNINGRPW", "IMU-mount roll/pitch/yaw angles alignment is ongoing"),
    3: ("COARSEUSED", "coarse IMU-mount alignment are used"),
    4: ("FINEUSED", "fine IMU-mount alignment are used"),
}
"""status from ESF-ALG"""
