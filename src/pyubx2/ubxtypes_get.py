"""
UBX Protocol Output payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _GET_ MESSAGES _FROM_ THE RECEIVER
(e.g. Periodic Navigation Data; Poll Responses; Info messages)

Created on 27 Sep 2020

Information sourced from u-blox Interface Specifications © 2013-2021, u-blox AG

:author: semuadmin
"""
# pylint: disable=too-many-lines, line-too-long

from pyubx2.ubxtypes_core import (
    A250,
    A256,
    C2,
    C6,
    C10,
    C30,
    C32,
    CH,
    I1,
    I2,
    I4,
    R4,
    R8,
    SCAL1,
    SCAL2,
    SCAL3,
    SCAL4,
    SCAL5,
    SCAL6,
    SCAL7,
    SCAL9,
    U1,
    U2,
    U3,
    U4,
    U5,
    U6,
    U7,
    U8,
    U9,
    U10,
    U12,
    U16,
    U20,
    U22,
    U23,
    U24,
    U32,
    U64,
    X1,
    X2,
    X4,
    X24,
)

UBX_PAYLOADS_GET = {
    "ACK-ACK": {"clsID": U1, "msgID": U1},
    "ACK-NAK": {"clsID": U1, "msgID": U1},
    # ********************************************************************
    # AssistNow Aiding Messages: i.e. Ephemeris, Almanac, other A-GPS data input.
    # Messages in the AID class are used to send GPS aiding data to the receiver
    # AID messages are deprecated in favour of MGA messages in >=Gen8
    "AID-ALM": {"svid": U4, "week": U4, "optBlock": ("None", {"dwrd": U4})},
    "AID-AOP": {"gnssId": U1, "svId": U1, "reserved1": U2, "data": U64},
    "AID-EPH": {
        "svid": U4,
        "how": U4,
        "optBlock": (
            "None",
            {
                "sf1d1": U4,
                "sf1d2": U4,
                "sf1d3": U4,
                "sf1d4": U4,
                "sf1d5": U4,
                "sf1d6": U4,
                "sf1d7": U4,
                "sf1d8": U4,
                "sf2d1": U4,
                "sf2d2": U4,
                "sf2d3": U4,
                "sf2d4": U4,
                "sf2d5": U4,
                "sf2d6": U4,
                "sf2d7": U4,
                "sf2d8": U4,
                "sf3d1": U4,
                "sf3d2": U4,
                "sf3d3": U4,
                "sf3d4": U4,
                "sf3d5": U4,
                "sf3d6": U4,
                "sf3d7": U4,
                "sf3d8": U4,
            },
        ),
    },
    "AID-HUI": {
        "health": X4,
        "utcA0": R8,
        "utcA1": R8,
        "utcTOW": I4,
        "utcWNT": I2,
        "utcLS": I2,
        "utcWNF": I2,
        "utcDNs": I2,
        "utcLSF": I2,
        "utcSpare": I2,
        "klobA0": R4,
        "klobA1": R4,
        "klobA2": R4,
        "klobA3": R4,
        "klobB0": R4,
        "klobB1": R4,
        "klobB2": R4,
        "klobB3": R4,
        "flags": X4,
    },
    "AID-INI": {
        "ecefXOrLat": I4,
        "ecefYOrLon": I4,
        "ecefZOrAlt": I4,
        "posAcc": U4,
        "tmCfg": X2,
        "wn": U2,
        "tow": U4,
        "towNs": I4,
        "tAccMs": U4,
        "tAccNs": U4,
        "clkDOrFreq": I4,
        "clkDAccOrFreqAcc": U4,
        "flags": X4,
    },
    "AID-ALP-ACK": {
        "acknak": U1,
    },
    "AID-ALP": {
        "predTow": U4,
        "predDur": U4,
        "age": I4,
        "predWno": U2,
        "almWno": U2,
        "reserved1": U4,
        "svs": U1,
        "reserved2": U1,
        "reserved3": U1,
        "reserved4": U1,
    },
    "ALP-ALPSRV": {
        "idSize": U1,
        "type": U1,
        "ofs": U2,
        "size": U2,
        "fileId": U2,
        "dataSize": U2,
        "id1": U1,
        "id2": U1,
        "id3": U1,
    },
    # ********************************************************************
    # Configuration Input Messages: i.e. Set Dynamic Model, Set DOP Mask, Set Baud Rate, etc..
    # Messages in the CFG class are used to configure the receiver and read out current configuration values. Any
    # messages in the CFG class sent to the receiver are either acknowledged (with message UBX-ACK-ACK) if
    # processed successfully or rejected (with message UBX-ACK-NAK) if processing unsuccessfully.
    "CFG-ANT": {
        "flags": (
            X2,
            {
                "svcs": U1,
                "scd": U1,
                "ocd": U1,
                "pdwnOnSCD": U1,
                "recovery": U1,
            },
        ),
        "pins": (
            X2,
            {
                "pinSwitch": U5,
                "pinSCD": U5,
                "pinOCD": U5,
                "reconfig": U1,
            },
        ),
    },
    "CFG-BATCH": {
        "version": U1,
        "flags": (
            X1,
            {
                "enable": U1,
                "reserved1": U1,
                "extraPvt": U1,
                "extraOdo": U1,
                "reserved2": U1,
                "pioEnable": U1,
                "pioActiveLow": U1,
            },
        ),
        "bufSize": U2,
        "notifThrs": U2,
        "pioId": U1,
        "reserved0": U1,
    },
    "CFG-CFG": {
        "clearMask": X4,
        "saveMask": X4,
        "loadMask": X4,
        "deviceMask": (
            X1,
            {
                "devBBR": U1,
                "devFlash": U1,
                "devEEPROM": U1,
                "reserved1": U1,
                "devSpiFlash": U1,
            },
        ),
    },
    "CFG-DAT": {
        "datumNum": U2,
        "datumName": C6,
        "majA": R8,
        "flat": R8,
        "dX": R4,
        "dY": R4,
        "dZ": R4,
        "rotX": R4,
        "rotY": R4,
        "rotZ": R4,
        "scale": R4,
    },
    "CFG-DGNSS": {
        "dgnssMode": U1,
        "reserved0": U3,
    },
    "CFG-DOSC": {
        "version": U1,
        "numOsc": U1,
        "reserved1": U2,
        "group": (
            "numOsc",
            {  # repeating group * numOsc
                "oscId": U1,
                "reserved2": U1,
                "flags": (
                    X2,
                    {
                        "isCalibrated": U1,
                        "controlIf": U4,
                    },
                ),
                "freq": [U4, 0.25],
                "phaseOffset": I4,
                "withTemp": [U4, 2**-8],
                "withAge": [U4, 2**-8],
                "timeToTemp": U2,
                "reserved3": U2,
                "gainVco": [I4, 2**-16],
                "gainUncertainty": [U1, 2**-8],
                "reserved4": U3,
            },
        ),
    },
    "CFG-DYNSEED": {"version": U1, "reserved1": U3, "seedHi": U4, "seedLo": U4},
    "CFG-EKF": {
        "disableEkf": U1,
        "actionFLags": (
            X1,
            {
                "reserved0": U1,
                "clTab": U1,
                "clCalib": U1,
                "reserved1": U1,
                "nomTacho": U1,
                "nomGyro": U1,
                "setTemp": U1,
                "dir": U1,
            },
        ),
        "configFlags": (
            X1,
            {
                "pulsesPerM": U1,
                "userSerWt": U1,
            },
        ),
        "inverseFlags": (
            X1,
            {
                "invDir": U1,
                "invGyro": U1,
            },
        ),
        "reserved2": U4,
        "nomPPDist": U2,
        "nomZero": U2,
        "nomSens": U1,
        "rmsTemp": [U1, SCAL1],
        "tempUpdate": U2,
    },
    "CFG-ESFALG": {
        "bitfield": (
            X4,
            {
                "version": U8,
                "doAutoMntAlg": U1,
            },
        ),
        "yaw": [U4, SCAL2],
        "pitch": [I2, SCAL2],
        "roll": [I2, SCAL2],
    },
    "CFG-ESFA": {
        "version": U1,
        "reserved1": U9,
        "accelRmsThdl": [U1, 2**-6],
        "frequency": U1,
        "latency": U2,
        "accuracy": [U2, SCAL4],
        "reserved2": U4,
    },
    "CFG-ESFG": {
        "version": U1,
        "reserved1": U7,
        "tcTableSaveRate": U2,
        "gyroRmsThdl": [U1, 2**-8],
        "frequency": U1,
        "latency": U2,
        "accuracy": [U2, SCAL3],
        "reserved2": U4,
    },
    "CFG-ESFGWT": {
        "flags": (
            X2,
            {
                "reserved0": U12,
                "setVehicle": U1,
                "setTime": U1,
                "setWt": U1,
            },
        ),
        "id": U2,
        "wtFactor": [U4, SCAL6],
        "reserved1": U4,
        "wtQuantError": [U4, SCAL6],
        "timeTagFactor": [U4, SCAL6],
        "wtCountMax": U4,
        "timeTagMax": U4,
        "wtLatency": U2,
        "reserved2": U2,
        "wtFrequency": U1,
        "reserved3": U1,
        "speedDeadBand": U2,
        "reserved4": U4,
        "reserved5": U4,
    },
    "CFG-ESFWT": {
        "version": U1,
        "flags1": (
            X1,
            {
                "combineTicks": U1,
                "reserved3": U3,
                "useWtSpeed": U1,
                "dirPinPol": U1,
                "useWtPin": U1,
            },
        ),
        "flags2": (
            X1,
            {
                "autoWtCountMaxOff": U1,
                "autoDirPinPolOff": U1,
                "autoSoftwareWtOff": U1,
                "autoUseWtSpeedOff": U1,
            },
        ),
        "reserved1": U1,
        "wtFactor": [U4, SCAL6],
        "wtQuantError": [U4, SCAL6],
        "wtCountMax": U4,
        "wtLatency": U2,
        "wtFrequency": U1,
        "flags3": (
            X1,
            {
                "reserved3": U4,
                "cntBothEdges": U1,
            },
        ),
        "speedDeadBand": U2,
        "reserved2": U10,
    },
    "CFG-ESRC": {
        "version": U1,
        "numSources": U1,
        "reserved1": U2,
        "group": (
            "numSources",
            {  # repeating group * numSources
                "extInt": U1,
                "sourceType": U1,
                "flags": (
                    X2,
                    {
                        "polarity": U1,
                        "gnssUtc": U1,
                    },
                ),
                "freq": [U4, 0.25],
                "reserved2": U4,
                "withTemp": [U4, 2**-8],
                "withAge": [U4, 2**-8],
                "timeToTemp": U2,
                "maxDevLifeTim": U2,
                "offset": I4,
                "offsetUncertainty": U4,
                "jitter": U4,
            },
        ),
    },
    "CFG-FIXSEED": {
        "version": U1,
        "length": U1,
        "reserved1": U2,
        "seedHi": U4,
        "seedLo": U4,
        "group": ("length", {"classId": U1, "msgId": U1}),  # repeating group * length
    },
    "CFG-FXN": {
        "flags": (
            X4,
            {
                "reserved0": U1,
                "sleep": U1,
                "reserved2": U1,
                "absAlign": U1,
                "onOff": U1,
            },
        ),
        "tReacq": U4,
        "tAcq": U4,
        "tReacqOff": U4,
        "tAcqOff": U4,
        "tOn": U4,
        "tOff": U4,
        "reserved1": U4,
        "baseTow": U4,
    },
    "CFG-GEOFENCE": {
        "version": U1,
        "numFences": U1,
        "confLvl": U1,
        "reserved0": U1,
        "pioEnabled": U1,
        "pinPolarity": U1,
        "pin": U1,
        "reserved1": U1,
        "group": (
            "numFences",
            {
                "lat": [I4, SCAL7],
                "lon": [I4, SCAL7],
                "radius": [U4, SCAL2],
            },  # repeating group * numFences
        ),
    },
    "CFG-GNSS": {
        "msgVer": U1,
        "numTrkChHw": U1,
        "numTrkChUse": U1,
        "numConfigBlocks": U1,
        "group": (
            "numConfigBlocks",
            {  # repeating group * numConfigBlocks
                "gnssId": U1,
                "resTrkCh": U1,
                "maxTrkCh": U1,
                "reserved0": U1,
                "flags": (
                    X4,
                    {
                        "enable": U1,
                        "reserved1": U7,
                        "reserved2": U8,
                        "sigCfMask": U8,
                        "reserved3": U8,
                    },
                ),
            },
        ),
    },
    "CFG-HNR": {
        "highNavRate": U1,
        "reserved1": U3,
    },
    "CFG-INF": {
        "protocolID": U1,
        "reserved0": U3,
        "infMaskGroup": (
            6,
            {
                "infMsgMask": (
                    X1,
                    {
                        "enableError": U1,
                        "enableWarning": U1,
                        "enableNotice": U1,
                        "enableTest": U1,
                        "enableDebug": U1,
                    },
                ),
            },
        ),
    },
    "CFG-ITFM": {
        "config": (
            X4,
            {
                "bbThreshold": U4,
                "cwThreshold": U5,
                "algorithmBits": U22,
                "enable": U1,
            },
        ),
        "config2": (
            X4,
            {
                "generalBits": U12,
                "antSetting": U2,
                "enable2": U1,
            },
        ),
    },
    "CFG-LOGFILTER": {
        "version": U1,
        "flags": (
            X1,
            {
                "recordEnabled": U1,
                "psmOncePerWakupEnabled": U1,
                "applyAllFilterSettings": U1,
            },
        ),
        "minInterval": U2,
        "timeThreshold": U2,
        "speedThreshold": U2,
        "positionThreshold": U4,
    },
    "CFG-MSG": {
        "msgClass": U1,
        "msgID": U1,
        "rateDDC": U1,
        "rateUART1": U1,
        "rateUART2": U1,
        "rateUSB": U1,
        "rateSPI": U1,
        "reserved": U1,
    },
    "CFG-NAV5": {
        "mask": (
            X2,
            {
                "dyn": U1,
                "minEl": U1,
                "posFixMode": U1,
                "drLim": U1,
                "posMask": U1,
                "timeMask": U1,
                "staticHoldMask": U1,
                "dgpsMask": U1,
                "cnoThreshold": U1,
                "reserved0": U1,
                "utc": U1,
            },
        ),
        "dynModel": U1,
        "fixMode": U1,
        "fixedAlt": [I4, SCAL2],
        "fixedAltVar": [U4, SCAL4],
        "minElev": I1,
        "drLimit": U1,
        "pDop": [U2, SCAL1],
        "tDop": [U2, SCAL1],
        "pAcc": U2,
        "tAcc": U2,
        "staticHoldThresh": U1,
        "dgnssTimeOut": U1,
        "cnoThreshNumSVs": U1,
        "cnoThresh": U1,
        "reserved0": U2,
        "staticHoldMaxDist": U2,
        "utcStandard": U1,
        "reserved1": U5,
    },
    "CFG-NAVX5": {
        "version": U2,
        "mask1": (
            X2,
            {
                "reserved9": U2,
                "minMax": U1,
                "minCno": U1,
                "reserved10": U2,
                "initial3dfix": U1,
                "reserved11": U2,
                "wknRoll": U1,
                "ackAid": U1,
                "reserved12": U2,
                "ppp": U1,
                "aop": U1,
            },
        ),
        "mask2": (
            X4,
            {
                "reserved13": U6,
                "adr": U1,
                "sigAttenComp": U1,
            },
        ),
        "reserved0": U2,
        "minSVs": U1,
        "maxSVs": U1,
        "minCNO": U1,
        "reserved1": U1,
        "iniFix3D": U1,
        "reserved2": U2,
        "ackAiding": U1,
        "wknRollover": U2,
        "sigAttenCompMode": U1,
        "reserved3": U1,
        "reserved4": U2,
        "reserved5": U2,
        "usePPP": U1,
        "aopCfg": U1,
        "reserved6": U2,
        "aopOrbMaxErr": U2,
        "reserved7": U4,
        "reserved8": U3,
        "useAdr": U1,
    },
    "CFG-NMEAvX": {  # deprecated length 4
        "filter": (
            X1,
            {
                "posFilt": U1,
                "mskPosFilt": U1,
                "timeFilt": U1,
                "dateFilt": U1,
                "gpsOnlyFilter": U1,
                "trackFilt": U1,
            },
        ),
        "nmeaVersion": U1,
        "numSV": U1,
        "flags": (
            X1,
            {
                "compat": U1,
                "consider": U1,
                "limit82": U1,
                "highPrec": U1,
            },
        ),
    },
    "CFG-NMEAv0": {  # v0 deprecated length 12
        "filter": (
            X1,
            {
                "posFilt": U1,
                "mskPosFilt": U1,
                "timeFilt": U1,
                "dateFilt": U1,
                "gpsOnlyFilter": U1,
                "trackFilt": U1,
            },
        ),
        "nmeaVersion": U1,
        "numSV": U1,
        "flags": (
            X1,
            {
                "compat": U1,
                "consider": U1,
                "limit82": U1,
                "highPrec": U1,
            },
        ),
        "gnssToFilter": (
            X4,
            {
                "gps": U1,
                "sbas": U1,
                "galileo": U1,
                "reserved2": U1,
                "qzss": U1,
                "glonass": U1,
                "bBeidou": U1,
            },
        ),
        "svNumbering": U1,
        "mainTalkerId": U1,
        "gsvTalkerId": U1,
        "version": U1,
    },
    "CFG-NMEA": {  # preferred version length 20
        "filter": (
            X1,
            {
                "posFilt": U1,
                "mskPosFilt": U1,
                "timeFilt": U1,
                "dateFilt": U1,
                "gpsOnlyFilter": U1,
                "trackFilt": U1,
            },
        ),
        "nmeaVersion": U1,
        "numSV": U1,
        "flags": (
            X1,
            {
                "compat": U1,
                "consider": U1,
                "limit82": U1,
                "highPrec": U1,
            },
        ),
        "gnssToFilter": (
            X4,
            {
                "gps": U1,
                "sbas": U1,
                "galileo": U1,
                "reserved2": U1,
                "qzss": U1,
                "glonass": U1,
                "beidou": U1,
            },
        ),
        "svNumbering": U1,
        "mainTalkerId": U1,
        "gsvTalkerId": U1,
        "version": U1,
        "bdsTalkerId": C2,
        "reserved1": U6,
    },
    "CFG-ODO": {
        "version": U1,
        "reserved0": U3,
        "flags": (
            X1,
            {
                "useODO": U1,
                "useCOG": U1,
                "outLPVel": U1,
                "outLPCog": U1,
            },
        ),
        "odoCfg": (
            X1,
            {
                "profile": U3,
            },
        ),
        "reserved1": U6,
        "cogMaxSpeed": [U1, SCAL1],
        "cogMaxPosAcc": U1,
        "reserved2": U2,
        "velLpGain": U1,
        "cogLpGain": U1,
        "reserved3": U2,
    },
    "CFG-PM": {
        "version": U1,
        "reserved1": U1,
        "reserved2": U1,
        "reserved3": U1,
        "flags": (
            X4,
            {
                "reserved4": U2,
                "interval": U2,
                "exintSelect": U1,
                "extintWake": U1,
                "extintBackup": U1,
                "reserved5": U1,
                "limitPeakCurr": U2,
                "waitTimeFix": U1,
                "updateRTC": U1,
                "updateEPH": U1,
            },
        ),
        "updatePeriod": U4,
        "searchPeriod": U4,
        "gridOffset": U4,
        "onTime": U2,
        "minAcqTime": U2,
    },
    "CFG-PM2": {
        "version": U1,
        "reserved0": U1,
        "maxStartupStateDur": U1,
        "reserved1": U1,
        "flags": (
            X4,
            {
                "reserved3": U1,
                "optTarget": U3,
                "extintSel": U1,
                "extintWake": U1,
                "extintBackup": U1,
                "extintInactive": U1,
                "limitPeakCurr": U2,
                "waitTimeFix": U1,
                "updateRTC": U1,
                "updateEPH": U1,
                "reserved4": U3,
                "doNotEnterOff": U1,
                "operationMode": U2,
            },
        ),
        "updatePeriod": U4,
        "searchPeriod": U4,
        "gridOffset": U4,
        "onTime": U2,
        "minAcqTime": U2,
        "reserved2": U20,
        "extintInactivityMs": U4,
    },
    "CFG-PMS": {
        "version": U1,
        "powerSetupValue": U1,
        "period": U2,
        "onTime": U2,
        "reserved0": U2,
    },
    "CFG-PRT": {
        "portID": U1,
        "reserved0": U1,
        "txReady": (
            X2,
            {
                "enable": U1,
                "pol": U1,
                "pin": U5,
                "thres": U9,
            },
        ),
        "UARTmode": (
            X4,
            {
                "reserved2": U6,
                "charLen": U2,
                "reserved3": U1,
                "parity": U3,
                "nStopBits": U2,
            },
        ),
        "baudRate": U4,
        "inProtoMask": (
            X2,
            {
                "inUBX": U1,
                "inNMEA": U1,
                "inRTCM": U1,
                "reserved4": U2,
                "inRTCM3": U1,
            },
        ),
        "outProtoMask": (
            X2,
            {
                "outUBX": U1,
                "outNMEA": U1,
                "reserved5": U3,
                "outRTCM3": U1,
            },
        ),
        "flags": (
            X2,
            {
                "reserved6": U1,
                "extendedTxTimeout": U1,
            },
        ),
        "reserved1": U2,
    },
    "CFG-PWR": {"version": U1, "reserved1": U3, "state": U4},
    "CFG-RATE": {"measRate": U2, "navRate": U2, "timeRef": U2},
    "CFG-RINV": {
        "flags": (
            X1,
            {
                "dump": U1,
                "binary": U1,
            },
        ),
        "group": ("None", {"data": U1}),
    },  # repeating group
    "CFG-RXM": {"reserved0": U1, "lpMode": U1},
    "CFG-SBAS": {
        "mode": (
            X1,
            {
                "enabled": U1,
                "test": U1,
            },
        ),
        "usage": (
            X1,
            {
                "range": U1,
                "diffCorr": U1,
                "integrity": U1,
            },
        ),
        "maxSBAS": U1,
        "scanmode2": (
            X1,
            {
                "PRN152": U1,
                "PRN153": U1,
                "PRN154": U1,
                "PRN155": U1,
                "PRN156": U1,
                "PRN157": U1,
                "PRN158": U1,
            },
        ),
        "scanmode1": (
            X4,
            {
                "PRN120": U1,
                "PRN121": U1,
                "PRN122": U1,
                "PRN123": U1,
                "PRN124": U1,
                "PRN125": U1,
                "PRN126": U1,
                "PRN127": U1,
                "PRN128": U1,
                "PRN129": U1,
                "PRN130": U1,
                "PRN131": U1,
                "PRN132": U1,
                "PRN133": U1,
                "PRN134": U1,
                "PRN135": U1,
                "PRN136": U1,
                "PRN137": U1,
                "PRN138": U1,
                "PRN139": U1,
                "PRN140": U1,
                "PRN141": U1,
                "PRN142": U1,
                "PRN143": U1,
                "PRN144": U1,
                "PRN145": U1,
                "PRN146": U1,
                "PRN147": U1,
                "PRN148": U1,
                "PRN149": U1,
                "PRN150": U1,
                "PRN151": U1,
            },
        ),
    },
    "CFG-SENIF": {
        "type": U1,
        "version": U1,
        "flags": (
            X2,
            {
                "senConn": U1,
            },
        ),
        "pioConf": X2,
    },
    "CFG-SLAS": {
        "mode": (
            X1,
            {
                "enabled": U1,
                "test": U1,
                "raim": U1,
            },
        ),
        "reserved1": U3,
    },
    "CFG-SMGR": {
        "version": U1,
        "minGNSSFix": U1,
        "maxFreqChange": U2,
        "maxPhaseCorrRate": U2,
        "reserved1": U2,
        "freqTolerance": U2,
        "timeTolerance": U2,
        "messageCfg": (
            X2,
            {
                "measInternal": U1,
                "measGNSS": U1,
                "measEXTINT0": U1,
                "measEXTINT1": U1,
            },
        ),
        "maxSlewRate": U2,
        "flags": (
            X4,
            {
                "disableInternal": U1,
                "disableExternal": U1,
                "preferenceMode": U1,
                "enableGNSS": U1,
                "enableEXTINT0": U1,
                "enableEXTINT1": U1,
                "enableHostMeasInt": U1,
                "enableHostMeasExt": U1,
                "reserved1": U2,
                "useAnyFix": U1,
                "disableMaxSlewRate": U1,
                "issueFreqWarning": U1,
                "issueTimeWarning": U1,
                "TPCoherent": U2,
                "disableOffset": U1,
            },
        ),
    },
    "CFG-SPT": {
        "version": U1,
        "reserved0": U1,
        "sensorId": U2,
        "reserved1": U8,
    },
    "CFG-TMODE": {
        "timeMode": U4,
        "fixedPosX": I4,
        "fixedPosY": I4,
        "fixedPosZ": I4,
        "fixedPosVar": U4,
        "svinMinDur": U4,
        "svinVarLimit": U4,
    },
    "CFG-TMODE2": {
        "timeMode": U1,
        "reserved1": U1,
        "flags": (
            X2,
            {
                "lla": U1,
                "altInv": U1,
            },
        ),
        "ecefXOrLat": I4,
        "ecefYOrLon": I4,
        "ecefZOrAlt": I4,
        "fixedPosAcc": U4,
        "svinMinDur": U4,
        "svinAccLimit": U4,
    },
    "CFG-TMODE3": {
        "version": U1,
        "reserved0": U1,
        "flags": (
            X2,
            {
                "rcvrMode": U8,
                "lla": U1,
            },
        ),
        "ecefXOrLat": I4,
        "ecefYOrLon": I4,
        "ecefZOrAlt": I4,
        "ecefXOrLatHP": I1,
        "ecefYOrLonHP": I1,
        "ecefZOrAltHP": I1,
        "reserved1": U1,
        "fixedPosAcc": U4,
        "svinMinDur": U4,
        "svinAccLimit": U4,
        "reserved2": U8,
    },
    "CFG-TP": {
        "interval": U4,
        "length": U4,
        "status": I1,
        "timeRef": U1,
        "flags": (
            X1,
            {
                "syncMode": U1,
            },
        ),
        "reserved0": U1,
        "antennaCableDelay": I2,
        "rfGroupDelay": I2,
        "userDelay": I4,
    },
    "CFG-TP5": {
        "tpIdx": U1,
        "version": U1,
        "reserved0": U2,
        "antCableDelay": I2,
        "rfGroupDelay": I2,
        "freqPeriod": U4,
        "freqPeriodLock": U4,
        "pulseLenRatio": U4,
        "pulseLenRatioLock": U4,
        "userConfigDelay": I4,
        "flags": (
            X4,
            {
                "active": U1,
                "lockGnssFreq": U1,
                "lockedOtherSet": U1,
                "isFreq": U1,
                "isLength": U1,
                "alignToTow": U1,
                "polarity": U1,
                "gridUtcGnss": U4,
                "syncMode": U3,
            },
        ),
    },
    "CFG-TXSLOT": {
        "version": U1,
        "enable": (
            X1,
            {
                "enableDDC": U1,
                "enableUART1": U1,
                "enableUART2": U1,
                "enableUSB": U1,
                "enableSPI": U1,
            },
        ),
        "refTp": U1,
        "reserved1": U1,
        "end_01": U4,
        "end_02": U4,
        "end_03": U4,
    },
    "CFG-USB": {
        "vendorID": U2,
        "productID": U2,
        "reserved0": U2,
        "reserved1": U2,
        "powerConsumption": U2,
        "flags": (
            X2,
            {
                "reEnum": U1,
                "powerMode": U1,
            },
        ),
        "vendorString": C32,
        "productString": C32,
        "serialNumber": C32,
    },
    "CFG-VALGET": {
        "version": U1,
        "layer": U1,
        "position": U2,
        "group": ("None", {"cfgData": U1}),  # repeating group
    },
    # ********************************************************************
    # External Sensor Fusion Messages: i.e. External Sensor Measurements and Status Information.
    # Messages in the ESF class are used to output external sensor fusion information from the receiver.
    "ESF-ALG": {
        "iTOW": U4,
        "version": U1,
        "flags": (
            X1,
            {
                "autoMntAlgOn": U1,
                "status": U3,
            },
        ),
        "error": (
            X1,
            {
                "tiltAlgError": U1,
                "yawAlgError": U1,
                "angleError": U1,
            },
        ),
        "reserved1": U1,
        "yaw": [U4, SCAL2],
        "pitch": [I2, SCAL2],
        "roll": [I2, SCAL2],
    },
    "ESF-CAL": {
        "sTtag": U4,
        "version": U1,
        "reserved0": U3,
        "reserved1": U4,
        "group": (  # variable by size repeating group
            "None",
            {
                "data": (
                    X4,
                    {
                        "dataField": X24,  # U24 in spec but should be X24
                        "dataType": U6,
                    },
                ),
            },
        ),
    },
    "ESF-INS": {
        "bitfield0": (
            X4,
            {
                "version": U8,
                "xAngRateValid": U1,
                "AngRateValid": U1,
                "zAngRateValid": U1,
                "xAccelValid": U1,
                "yAccelValid": U1,
                "zAccelValid": U1,
            },
        ),
        "reserved1": U4,
        "iTOW": U4,
        "xAngRate": [I4, SCAL3],
        "yAngRate": [I4, SCAL3],
        "zAngRate": [I4, SCAL3],
        "xAccel": [I4, SCAL2],
        "yAccel": [I4, SCAL2],
        "zAccel": [I4, SCAL2],
    },
    # if calibTtagValid = 1; last dataField = calibTtag, numMeas = num of dataFields excluding calibTtag
    "ESF-MEAS": {
        "timeTag": U4,
        "flags": (
            X2,
            {
                "timeMarkSent": U2,
                "timeMarkEdge": U1,
                "calibTtagValid": U1,
                "reserved0": U7,
                "numMeas": U5,
            },
        ),
        "id": U2,
        "group": (
            "None",
            {  # repeating group * numMeas
                "data": (
                    X4,
                    {
                        "dataField": X24,
                        "dataType": U6,
                    },
                ),
            },
        ),
    },
    "ESF-RAW": {
        "reserved1": U4,
        "group": (
            "None",
            {  # repeating group
                "data": X4,
                "sTag": X4,
            },
        ),
    },
    "ESF-STATUS": {
        "iTOW": U4,
        "version": U1,
        "reserved0": U7,
        "fusionMode": U1,
        "reserved1": U2,
        "numSens": U1,
        "group": (
            "numSens",
            {  # repeating group * numSens
                "sensStatus1": (
                    X1,
                    {
                        "type": U6,
                        "used": U1,
                        "ready": U1,
                    },
                ),
                "sensStatus2": (
                    X1,
                    {
                        "calibStatus": U2,
                        "timeStatus": U2,
                    },
                ),
                "freq": U1,
                "faults": (
                    X1,
                    {
                        "badMeas": U1,
                        "badTTag": U1,
                        "missingMeas": U1,
                        "noisyMeas": U1,
                    },
                ),
            },
        ),
    },
    # ********************************************************************
    # High Rate Navigation Results Messages: i.e. High rate time, position, speed, heading.
    # Messages in the HNR class are used to output high rate navigation data for position, altitude,
    # velocity and their accuracies.
    "HNR-ATT": {
        "iTOW": U4,
        "version": U1,
        "reserved1": U3,
        "roll": [I4, SCAL5],
        "pitch": [I4, SCAL5],
        "heading": [I4, SCAL5],
        "accRoll": [U4, SCAL5],
        "accPitch": [U4, SCAL5],
        "accHeading": [U4, SCAL5],
    },
    "HNR-INS": {
        "bitfield0": (
            X4,
            {
                "version": U8,
                "xAngRateValid": U1,
                "yAngRateValid": U1,
                "zAngRateValid": U1,
                "xAccelValid": U1,
                "yAccelValid": U1,
                "zAccelValid": U1,
            },
        ),
        "reserved1": U4,
        "iTOW": U4,
        "xAngRate": [I4, SCAL3],
        "yAngRate": [I4, SCAL3],
        "zAngRate": [I4, SCAL3],
        "xAccel": [I4, SCAL2],
        "yAccel": [I4, SCAL2],
        "zAccel": [I4, SCAL2],
    },
    "HNR-PVT": {
        "iTOW": U4,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "min": U1,
        "second": U1,
        "valid": (
            X1,
            {
                "validDate": U1,
                "validTime": U1,
                "fullyResolved": U1,
            },
        ),
        "nano": I4,
        "gpsFix": U1,
        "flags": (
            X1,
            {
                "GPSfixOK": U1,
                "DiffSoln": U1,
                "WKNSET": U1,
                "TOWSET": U1,
                "headVehValid": U1,
            },
        ),
        "reserved1": U2,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "height": I4,
        "hMSL": I4,
        "gSpeed": I4,
        "speed": I4,
        "headMot": [I4, SCAL5],
        "headVeh": [I4, SCAL5],
        "hAcc": U4,
        "vAcc": U4,
        "sAcc": U4,
        "headAcc": [U4, SCAL5],
        "reserved2": U4,
    },
    # ********************************************************************
    # Information Messages: i.e. Printf-Style Messages, with IDs such as Error, Warning, Notice.
    # Messages in the INF class are used to output strings in a printf style from the firmware or application code. All
    # INF messages have an associated type to indicate the kind of message.
    "INF-DEBUG": {"message": CH},
    "INF-ERROR": {"message": CH},
    "INF-NOTICE": {"message": CH},
    "INF-TEST": {"message": CH},
    "INF-WARNING": {"message": CH},
    # ********************************************************************
    # Logging Messages: i.e. Log creation, deletion, info and retrieval.
    # Messages in the LOG class are used to configure and report status information of the logging feature.
    "LOG-BATCH": {
        "version": U1,
        "contentValid": (
            X1,
            {
                "extraPvt": U1,
                "extraOdo": U1,
            },
        ),
        "msgCnt": U2,
        "iTOW": U4,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "min": U1,
        "sec": U1,
        "valid": (
            X1,
            {
                "validDate": U1,
                "validTime": U1,
            },
        ),
        "tAcc": U4,
        "fracSec": I4,
        "fixType": U1,
        "flags": (
            X1,
            {
                "gnssFixOK": U1,
                "diffSoln": U1,
                "psmState": U3,
            },
        ),
        "flags2": X1,  # no definition for these bitflags
        "numSV": U1,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "height": I4,
        "hMSL": I4,
        "hAcc": U4,
        "vAcc": U4,
        "velN": I4,
        "velE": I4,
        "velD": I4,
        "gSpeed": I4,
        "headMot": [I4, SCAL5],
        "sAcc": U4,
        "headAcc": [U4, SCAL5],
        "pDOP": [U2, SCAL2],
        "reserved0": U2,
        "distance": U4,
        "totalDistance": U4,
        "distanceStd": U4,
        "reserved1": U4,
    },
    "LOG-FINDTIME": {"version": U1, "type": U1, "reserved0": U2, "entryNumber": U4},
    "LOG-INFO": {
        "version": U1,
        "reserved0": U3,
        "filestoreCapacity": U4,
        "reserved1": U8,
        "currentMaxLogSize": U4,
        "currentLogSize": U4,
        "entryCount": U4,
        "oldestYear": U2,
        "oldestMonth": U1,
        "oldestDay": U1,
        "oldestHour": U1,
        "oldestMinute": U1,
        "oldestSecond": U1,
        "reserved2": U1,
        "newestYear": U2,
        "newestMonth": U1,
        "newestDay": U1,
        "newestHour": U1,
        "newestMinute": U1,
        "newestSecond": U1,
        "reserved3": U1,
        "status": (
            X1,
            {
                "reserved5": U3,
                "recording": U1,
                "inactive": U1,
                "circular": U1,
            },
        ),
        "reserved4": U3,
    },
    "LOG-RETRIEVEPOS": {
        "entryIndex": U4,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "hMSL": I4,
        "hAcc": U4,
        "gSpeed": U4,
        "heading": [U4, SCAL5],
        "version": U1,
        "fixType": U1,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "minute": U1,
        "second": U1,
        "reserved0": U1,
        "numSV": U1,
        "reserved1": U1,
    },
    "LOG-RETRIEVEPOSEXTRA": {
        "entryIndex": U4,
        "version": U1,
        "reserved0": U1,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "minute": U1,
        "second": U1,
        "reserved1": U3,
        "distance": U4,
        "reserved2": U12,
    },
    "LOG-RETRIEVESTRING": {
        "entryIndex": U4,
        "version": U1,
        "reserved0": U1,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "minute": U1,
        "second": U1,
        "reserved1": U1,
        "byteCount": U2,
        "group": ("byteCount", {"bytes": U1}),  # repeating group * byteCount
    },
    # ********************************************************************
    # Multiple GNSS Assistance Messages: i.e. Assistance data for various GNSS.
    # Messages in the MGA class are used for GNSS aiding information from and to the receiver.
    "MGA-ACK-DATA0": {
        "type": U1,
        "version": U1,
        "infoCode": U1,
        "msgId": U1,
        "msgPayloadStart": U4,
    },
    "MGA-NAK-DATA0": {
        "type": U1,
        "version": U1,
        "infoCode": U1,
        "msgId": U1,
        "msgPayloadStart": U4,
    },
    "MGA-DBD": {"reserved1": U12, "group": ("None", {"data": U1})},  # repeating group
    "MGA-FLASH-ACK": {
        "type": U1,
        "version": U1,
        "ack": U1,
        "reserved1": U1,
        "sequence": U2,
    },
    # ********************************************************************
    # Monitoring Messages: i.e. Communication Status, CPU Load, Stack Usage, Task Status.
    # Messages in the MON class are used to report the receiver status, such as CPU load, stack usage, I/O subsystem
    # statistics etc.
    "MON-COMMS": {
        "version": U1,
        "nPorts": U1,
        "txErrors": (
            X1,
            {
                "mem": U1,
                "alloc": U1,
            },
        ),
        "reserved0": U1,
        "protgroup": (
            4,
            {  # repeating group * 4
                "protIds": U1,
            },
        ),
        "portsgroup": (
            "nPorts",
            {  # repeating group * nPorts
                "portId": U2,
                "txPending": U2,
                "txBytes": U4,
                "txUsage": U1,
                "txPeakUsage": U1,
                "rxPending": U2,
                "rxBytes": U4,
                "rxUsage": U1,
                "rxPeakUsage": U1,
                "overrunErrs": U2,
                "msggroup": (
                    4,
                    {
                        "msgs": U2,
                    },
                ),
                "reserved1": U8,
                "skipped": U4,
            },
        ),
    },
    "MON-GNSS": {
        "version": U1,
        "supported": (
            X1,
            {
                "GPSSup": U1,
                "GlonassSup": U1,
                "BeidouSup": U1,
                "GalileoSup": U1,
            },
        ),
        "defaultGnss": (
            X1,
            {
                "GPSDef": U1,
                "GlonassDef": U1,
                "BeidouDef": U1,
                "GalileoDef": U1,
            },
        ),
        "enabled": (
            X1,
            {
                "GPSEna": U1,
                "GlonassEna": U1,
                "BeidouEna": U1,
                "GalileoEna": U1,
            },
        ),
        "simultaneous": U1,
        "reserved0": U3,
    },
    "MON-HW": {
        "pinSel": X4,
        "pinBank": X4,
        "pinDir": X4,
        "pinVal": X4,
        "noisePerMS": U2,
        "agcCnt": U2,
        "aStatus": U1,
        "aPower": U1,
        "flags": (
            X1,
            {
                "rtcCalib": U1,
                "safeBoot": U1,
                "jammingState": U2,
                "xtalAbsent": U1,
            },
        ),
        "reserved0": U1,
        "usedMask": X4,
        "groupVP": (
            17,
            {
                "VP": X1,
            },
        ),  # repeating group * 17
        "jamInd": U1,
        "reserved1": U2,
        "pinIrq": X4,
        "pullH": X4,
        "pullL": X4,
    },
    "MON-HW2": {
        "ofsI": I1,
        "magI": U1,
        "ofsQ": I1,
        "magQ": U1,
        "cfgSource": U1,
        "reserved0": U3,
        "lowLevCfg": U4,
        "reserved1": U8,
        "postStatus": U4,
        "reserved2": U4,
    },
    "MON-HW3": {
        "version": U1,
        "nPins": U1,
        "flags": (
            X1,
            {
                "rtcCalib": U1,
                "safeBoot": U1,
                "xtalAbsent": U1,
            },
        ),
        "hwVersion": C10,
        "reserved0": U9,
        "pingroup": (  # repeating group * nPins
            "nPins",
            {
                "pinId": U2,
                "pinMask": (
                    X2,
                    {
                        "periphPIO": U1,
                        "pinBank": U3,
                        "direction": U1,
                        "pinValue": U1,
                        "vpManager": U1,
                        "pioIrq": U1,
                        "pioPullHigh": U1,
                        "pioPullLow": U1,
                    },
                ),
                "VP": U1,
                "reserved1": U1,
            },
        ),
    },
    "MON-IO": {
        "rxBytes": U4,
        "txBytes": U4,
        "parityErrs": U2,
        "framingErrs": U2,
        "overrunErrs": U2,
        "breakCond": U2,
        "rxBusy": U1,
        "txBusy": U1,
        "reserved1": U2,
    },
    "MON-MSGPP": {
        "groupmsg1": (
            8,
            {
                "msg1": U2,
            },
        ),  # repeating group * 8
        "groupmsg2": (
            8,
            {
                "msg2": U2,
            },
        ),  # repeating group * 8
        "groupmsg3": (
            8,
            {
                "msg3": U2,
            },
        ),  # repeating group * 8
        "groupmsg4": (
            8,
            {
                "msg4": U2,
            },
        ),  # repeating group * 8
        "groupmsg5": (
            8,
            {
                "msg5": U2,
            },
        ),  # repeating group * 8
        "groupmsg6": (
            8,
            {
                "msg6": U2,
            },
        ),  # repeating group * 8
        "groupskipped": (
            6,
            {
                "skipped": U4,
            },
        ),  # repeating group * 6
    },
    "MON-PATCH": {
        "version": U2,
        "nEntries": U2,
        "group": (  # repeating group * nEntries
            "nEntries",
            {
                "patchInfo": (
                    X4,
                    {
                        "activated": U1,
                        "location": U2,
                    },
                ),
                "comparatorNumber": U4,
                "patchAddress": U4,
                "patchData": U4,
            },
        ),
    },
    "MON-RF": {
        "version": U1,
        "nBlocks": U1,
        "reserved0": U2,
        "group": (  # repeating group * nBlocks
            "nBlocks",
            {
                "blockId": U1,
                "flags": (
                    X1,
                    {
                        "jammingState": U1,
                    },
                ),
                "antStatus": U1,
                "antPower": U1,
                "postStatus": U4,
                "reserved1": U4,
                "noisePerMS": U2,
                "agcCnt": U2,
                "jamInd": U1,
                "ofsI": I1,
                "magI": U1,
                "ofsQ": I1,
                "magQ": U1,
                "reserved2": U3,
            },
        ),
    },
    "MON-RXBUF": {
        "groupPending": (
            6,
            {
                "pending": U2,
            },
        ),  # repeating group * 6
        "groupUsage": (
            6,
            {
                "usage": U1,
            },
        ),  # repeating group * 6
        "groupPeakUsage": (
            6,
            {
                "peakUsage": U1,
            },
        ),  # repeating group * 6
    },
    "MON-RXR": {
        "flags": (
            X1,
            {
                "awake": U1,
            },
        ),
    },
    "MON-SMGR": {
        "version": U1,
        "reserved1": U3,
        "iTOW": U4,
        "intOsc": (
            X2,
            {
                "intOscState": U4,
                "intOscCalib": U1,
                "intOscDisc": U1,
            },
        ),
        "extOsc": (
            X2,
            {
                "extOscState": U4,
                "extOscCalib": U1,
                "extOscDisc": U1,
            },
        ),
        "discSrc": U1,
        "gnss": (
            X1,
            {
                "gnssAvail": U1,
            },
        ),
        "extInt0": (
            X1,
            {
                "extInt0Avail": U1,
                "extInt0Type": U1,
                "extInt0FeedBack": U1,
            },
        ),
        "extInt1": (
            X1,
            {
                "extInt1Avail": U1,
                "extInt1Type": U1,
                "extInt1FeedBack": U1,
            },
        ),
    },
    "MON-SPAN": {
        "version": U1,
        "numRfBlocks": U1,
        "reserved0": U2,
        "group": (  # repeating group * numRfBlocks
            "numRfBlocks",
            {
                "spectrum": A256,  # parsed as array of 256 integers
                "span": U4,
                "res": U4,
                "center": U4,
                "pga": U1,
                "reserved1": U3,
            },
        ),
    },
    "MON-SPT": {
        "version": U1,
        "numSensor": U1,
        "numRes": U1,
        "reserved0": U1,
        "groupSensor": (  # repeating group * numSensor
            "numSensor",
            {
                "sensorId": U1,
                "drvVer": X1,
                "testState": U1,
                "drvFileName": U1,
            },
        ),
        "groupRes": (  # repeating group * numRes
            "numRes",
            {
                "sensorIdRes": U2,
                "sensorType": U2,
                "resType": U2,
                "reserved1": U2,
                "value": I4,
            },
        ),
    },
    "MON-SYS": {
        "msgVer": U1,
        "bootType": U1,
        "cpuLoad": U1,
        "cpuLoadMax": U1,
        "memUsage": U1,
        "memUsageMax": U1,
        "ioUsage": U1,
        "ioUsageMax": U1,
        "runTime": U4,
        "noticeCount": U2,
        "warnCount": U2,
        "errorCount": U2,
        "tempValue": I1,
        "reserved0": U5,
    },
    "MON-TXBUF": {
        "groupPending": (  # repeating group * 6
            6,
            {
                "pending": U2,
            },
        ),
        "groupUsage": (  # repeating group * 6
            6,
            {
                "usage": U1,
            },
        ),
        "groupPeakUsage": (  # repeating group * 6
            6,
            {
                "peakUsage": U1,
            },
        ),
        "tUsage": U1,
        "tPeakUsage": U1,
        "errors": (
            X1,
            {
                "limit": U6,
                "lem": U1,
                "alloc": U1,
            },
        ),
        "reserved0": U1,
    },
    "MON-VER": {
        "swVersion": C30,
        "hwVersion": C10,
        "group": ("None", {"extension": C30}),  # repeating group
    },
    # ********************************************************************
    # Navigation Results Messages: i.e. Position, Speed, Time, Acceleration, Heading, DOP, SVs used.
    # Messages in the NAV class are used to output navigation data such as position, altitude and velocity in a
    # number of formats. Additionally, status flags and accuracy figures are output. The messages are generated with
    # the configured navigation/measurement rate.
    "NAV-AOPSTATUS-L": {  # long 20 version for M6
        "iTOW": U4,
        "config": U1,
        "status": U1,
        "reserved0": U1,
        "reserved1": U1,
        "avail": U4,
        "reserved2": U4,
        "reserved3": U4,
    },
    "NAV-AOPSTATUS": {  # short 16 version for M8
        "iTOW": U4,
        "aopCfg": U1,
        "status": U1,
        "reserved1": U10,
    },
    "NAV-ATT": {
        "iTOW": U4,
        "version": U1,
        "reserved0": U3,
        "roll": [I4, SCAL5],
        "pitch": [I4, SCAL5],
        "heading": [I4, SCAL5],
        "accRoll": [U4, SCAL5],
        "accPitch": [U4, SCAL5],
        "accHeading": [U4, SCAL5],
    },
    "NAV-CLOCK": {"iTOW": U4, "clkB": I4, "clkD": I4, "tAcc": U4, "fAcc": U4},
    "NAV-COV": {
        "iTOW": U4,
        "version": U1,
        "posCovValid": U1,
        "velCovValid": U1,
        "reserved0": U9,
        "posCovNN": R4,
        "posCovNE": R4,
        "posCovND": R4,
        "posCovEE": R4,
        "posCovED": R4,
        "posCovDD": R4,
        "velCovNN": R4,
        "velCovNE": R4,
        "velCovND": R4,
        "velCovEE": R4,
        "velCovED": R4,
        "velCovDD": R4,
    },
    "NAV-DGPS": {
        "iTOW": U4,
        "age": I4,
        "baseId": I2,
        "baseHealth": I2,
        "numCh": U1,
        "status": U1,
        "reserved1": U2,
        "channels": (  # repeating group * numCh
            "numCh",
            {
                "svid": U1,
                "flags": (
                    X1,
                    {
                        "channel": U4,
                        "dgpsUsed": U1,
                    },
                ),
                "ageC": U2,
                "prc": R4,
                "prrc": R4,
            },
        ),
    },
    "NAV-DOP": {
        "iTOW": U4,
        "gDOP": [U2, SCAL2],
        "pDOP": [U2, SCAL2],
        "tDOP": [U2, SCAL2],
        "vDOP": [U2, SCAL2],
        "hDOP": [U2, SCAL2],
        "nDOP": [U2, SCAL2],
        "eDOP": [U2, SCAL2],
    },
    "NAV-EELL": {
        "iTOW": U4,
        "version": U1,
        "reserved0": U1,
        "errEllipseOrient": [U2, SCAL2],
        "errEllipseMajor": U4,
        "errEllipseMinor": U4,
    },
    "NAV-EKFSTATUS": {
        "pulses": I4,
        "period": I4,
        "gyroMean": [U4, SCAL2],
        "temperature": [I2, 2**-8],
        "direction": I1,
        "calibStatus": (
            X1,
            {
                "calibTacho": U2,
                "calibGyro": U2,
                "calibGyroB": U2,
            },
        ),
        "pulseScale": [I4, SCAL5],
        "gyroBias": [I4, SCAL5],
        "gyroScale": [I4, SCAL5],
        "accPulseScale": [I4, SCAL4],
        "accGyroBias": [I4, SCAL4],
        "accGyroScale": [I4, SCAL4],
        "measUsed": (
            X1,
            {
                "pulse": U1,
                "dir": U1,
                "gyro": U1,
                "temp": U1,
                "pos": U1,
                "vel": U1,
                "errGyro": U1,
                "errPulse": U1,
            },
        ),
        "reserved2": U1,
    },
    "NAV-EOE": {"iTOW": U4},
    "NAV-GEOFENCE": {
        "iTOW": U4,
        "version": U1,
        "status": U1,
        "numFences": U1,
        "combState": U1,
        "group": (  # repeating group * numFences
            "numFences",
            {"state": U1, "reserved1": U1},
        ),
    },
    # NB: special handling for NAV-HPPOS* message types;
    # private standard and high precision attributes are
    # combined into a single public attribute in
    # accordance with interface specification
    "NAV-HPPOSECEF": {
        "version": U1,
        "reserved0": U3,
        "iTOW": U4,
        "_ecefX": I4,  # cm
        "_ecefY": I4,  # cm
        "_ecefZ": I4,  # cm
        "_ecefXHp": [I1, SCAL1],  # mm
        "_ecefYHp": [I1, SCAL1],  # mm
        "_ecefZHp": [I1, SCAL1],  # mm
        "flags": (
            X1,
            {
                "invalidEcef": U1,
            },
        ),
        "pAcc": [U4, SCAL1],
    },
    "NAV-HPPOSLLH": {
        "version": U1,
        "reserved0": U2,
        "flags": (
            X1,
            {
                "invalidLlh": U1,
            },
        ),
        "iTOW": U4,
        "_lon": [I4, SCAL7],
        "_lat": [I4, SCAL7],
        "_height": I4,  # mm
        "_hMSL": I4,  # mm
        "_lonHp": [I1, SCAL9],
        "_latHp": [I1, SCAL9],
        "_heightHp": [I1, SCAL1],  # mm
        "_hMSLHp": [I1, SCAL1],  # mm
        "hAcc": [U4, SCAL1],
        "vAcc": [U4, SCAL1],
    },
    "NAV-NMI": {
        "iTOW": U4,
        "version": U1,
        "reserved1": U4,
        "gpsNmiFlags": (
            X1,
            {
                "wnoCheckedGPS": U1,
                "wnoInvalidGPS": U1,
                "UTCORefCheckedGPS": U1,
                "UTCORefInvalidGPS": U1,
            },
        ),
        "gpsLsFlags": (
            X1,
            {
                "lsValGPS": U1,
                "dnRangeGPS": U1,
                "totRangeGPS": U1,
                "lsEventGPS": U1,
                "recNowGPS": U1,
            },
        ),
        "galNmiFlags": (
            X1,
            {
                "wnoCheckedGAL": U1,
                "wnoInvalidGAL": U1,
            },
        ),
        "galLsFlags": (
            X1,
            {
                "lsValGAL": U1,
                "dnRangeGAL": U1,
                "totRangeGAL": U1,
                "lsEventGAL": U1,
                "recNowGAL": U1,
            },
        ),
        "bdsNmiFlags": (
            X1,
            {
                "wnoCheckedBDS": U1,
                "wnoInvalidBDS": U1,
            },
        ),
        "bdsLsFlags": (
            X1,
            {
                "lsValBDS": U1,
                "dnRangeBDS": U1,
                "totRangeBDS": U1,
                "lsEventBDS": U1,
                "recNowBDS": U1,
            },
        ),
        "gloNmiFlags": (
            X1,
            {
                "wnoCheckedGLO": U1,
                "wnoInvalidGLO": U1,
            },
        ),
    },
    "NAV-ODO": {
        "version": U1,
        "reserved0": U3,
        "iTOW": U4,
        "distance": U4,
        "totalDistance": U4,
        "distanceStd": U4,
    },
    "NAV-ORB": {
        "iTOW": U4,
        "version": U1,
        "numSv": U1,
        "reserved0": U2,
        "group": (  # repeating group * numSv
            "numSv",
            {
                "gnssId": U1,
                "svId": U1,
                "svFlag": (
                    X1,
                    {
                        "health": U2,
                        "visibility": U2,
                    },
                ),
                "eph": (
                    X1,
                    {
                        "ephUsability": U5,
                        "ephSource": U3,
                    },
                ),
                "alm": (
                    X1,
                    {
                        "almUsability": U5,
                        "almSource": U3,
                    },
                ),
                "otherOrb": (
                    X1,
                    {
                        "anoAopUsability": U5,
                        "type": U3,
                    },
                ),
            },
        ),
    },
    "NAV-PL": {
        "version": U1,
        "tmirCoeff": U1,
        "tmirExp": I1,
        "plPosValid": U1,
        "plPosFrame": U1,
        "plVelValid": U1,
        "plVelFrame": U1,
        "plTimeValid": U1,
        "reserved": U4,
        "iTOW": U4,
        "plPos1": U4,
        "plPos2": U4,
        "plPos3": U4,
        "plVel1": U4,
        "plVel2": U4,
        "plVel3": U4,
        "plPosHorizOrient": U2,
        "plVelHorizOrient": U2,
        "plTime": U4,
        "reserved2": U4,
    },
    "NAV-POSECEF": {"iTOW": U4, "ecefX": I4, "ecefY": I4, "ecefZ": I4, "pAcc": U4},
    "NAV-POSLLH": {
        "iTOW": U4,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "height": I4,
        "hMSL": I4,
        "hAcc": U4,
        "vAcc": U4,
    },
    "NAV-PVAT": {
        "iTOW": U4,
        "version": U1,
        "valid": (
            X1,
            {
                "validDate": U1,
                "validTime": U1,
                "fullyResolved": U1,
                "validMag": U1,
            },
        ),
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "min": U1,
        "sec": U1,
        "reserved0": U1,
        "reserved1": U2,
        "tAcc": U4,
        "nano": I4,
        "fixType": U1,
        "flags": (
            X1,
            {
                "gnssFixOK": U1,
                "diffSoln": U1,
                "reserved4": U1,
                "vehRollValid": U1,
                "vehPitchValid": U1,
                "vehHeadingValid": U1,
                "carrSoln": U2,
            },
        ),
        "flags2": (
            X1,
            {
                "reserved5": U5,
                "confirmedAvai": U1,
                "confirmedDate": U1,
                "confirmedTime": U1,
            },
        ),
        "numSV": U1,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "height": I4,
        "hMSL": I4,
        "hAcc": U4,
        "vAcc": U4,
        "velN": I4,
        "velE": I4,
        "velD": I4,
        "gSpeed": I4,
        "sAcc": U4,
        "vehRoll": [I4, SCAL5],
        "vehPitch": [I4, SCAL5],
        "vehHeading": [I4, SCAL5],
        "motHeading": [I4, SCAL5],
        "accRoll": [U2, SCAL2],
        "accPitch": [U2, SCAL2],
        "accHeading": [U2, SCAL2],
        "magDec": [I2, SCAL2],
        "magAcc": [U2, SCAL2],
        "errEllipseOrient": [U2, SCAL2],
        "errEllipseMajor": U4,
        "errEllipseMinor": U4,
        "reserved2": U4,
        "reserved3": U4,
    },
    "NAV-PVT": {
        "iTOW": U4,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "min": U1,
        "second": U1,
        "valid": (
            X1,
            {
                "validDate": U1,
                "validTime": U1,
                "fullyResolved": U1,
                "validMag": U1,
            },
        ),
        "tAcc": U4,
        "nano": I4,
        "fixType": U1,
        "flags": (
            X1,
            {
                "gnssFixOk": U1,
                "difSoln": U1,
                "psmState": U3,
                "headVehValid": U1,
                "carrSoln": U2,
            },
        ),
        "flags2": (
            X1,
            {
                "reserved": U5,
                "confirmedAvai": U1,
                "confirmedDate": U1,
                "confirmedTime": U1,
            },
        ),
        "numSV": U1,
        "lon": [I4, SCAL7],
        "lat": [I4, SCAL7],
        "height": I4,
        "hMSL": I4,
        "hAcc": U4,
        "vAcc": U4,
        "velN": I4,
        "velE": I4,
        "velD": I4,
        "gSpeed": I4,
        "headMot": [I4, SCAL5],
        "sAcc": U4,
        "headAcc": [U4, SCAL5],
        "pDOP": [U2, SCAL2],
        "flags3": (
            X2,
            {
                "invalidLlh": U1,
                "lastCorrectionAge": U4,
            },
        ),
        "reserved0": U4,  # NB this is incorrectly stated as U5 in older documentation
        "headVeh": [I4, SCAL5],
        "magDec": [I2, SCAL2],
        "magAcc": [U2, SCAL2],
    },
    "NAV-RELPOSNED-V0": {
        "version": U1,  # 0x00
        "reserved1": U1,
        "refStationID": U2,
        "iTOW": U4,
        "relPosN": I4,
        "relPosE": I4,
        "relPosD": I4,
        "relPosHPN": [I1, SCAL1],
        "relPosHPE": [I1, SCAL1],
        "relPosHPD": [I1, SCAL1],
        "reserved2": U1,
        "accN": [U4, SCAL1],
        "accE": [U4, SCAL1],
        "accD": [U4, SCAL1],
        "flags": (
            X4,
            {
                "gnssFixOK": U1,
                "diffSoln": U1,
                "relPosValid": U1,
                "carrSoln": U2,
                "isMoving": U1,
                "refPosMiss": U1,
                "refObsMiss": U1,
                "relPosHeadingValid": U1,
                "relPosNormalized": U1,
            },
        ),
    },
    "NAV-RELPOSNED": {
        "version": U1,  # 0x01
        "reserved0": U1,
        "refStationID": U2,
        "iTOW": U4,
        "relPosN": I4,
        "relPosE": I4,
        "relPosD": I4,
        "relPosLength": I4,
        "relPosHeading": [I4, SCAL5],
        "reserved1": U4,
        "relPosHPN": [I1, SCAL1],
        "relPosHPE": [I1, SCAL1],
        "relPosHPD": [I1, SCAL1],
        "relPosHPLength": [I1, SCAL1],
        "accN": [U4, SCAL1],
        "accE": [U4, SCAL1],
        "accD": [U4, SCAL1],
        "accLength": [U4, SCAL1],
        "accHeading": [U4, SCAL5],
        "reserved2": U4,
        "flags": (
            X4,
            {
                "gnssFixOK": U1,
                "diffSoln": U1,
                "relPosValid": U1,
                "carrSoln": U2,
                "isMoving": U1,
                "refPosMiss": U1,
                "refObsMiss": U1,
                "relPosHeadingValid": U1,
                "relPosNormalized": U1,
            },
        ),
    },
    "NAV-SAT": {
        "iTOW": U4,
        "version": U1,
        "numSvs": U1,
        "reserved0": U2,
        "group": (  # repeating group * numSvs
            "numSvs",
            {
                "gnssId": U1,
                "svId": U1,
                "cno": U1,
                "elev": I1,
                "azim": I2,
                "prRes": [I2, SCAL1],
                "flags": (
                    X4,
                    {
                        "qualityInd": U3,
                        "svUsed": U1,
                        "health": U2,
                        "diffCorr": U1,
                        "smoothed": U1,
                        "orbitSource": U3,
                        "ephAvail": U1,
                        "almAvail": U1,
                        "anoAvail": U1,
                        "aopAvail": U1,
                        "reserved13": U1,
                        "sbasCorrUsed": U1,
                        "rtcmCorrUsed": U1,
                        "slasCorrUsed": U1,
                        "spartnCorrUsed": U1,
                        "prCorrUsed": U1,
                        "crCorrUsed": U1,
                        "doCorrUsed": U1,
                    },
                ),
            },
        ),
    },
    "NAV-SBAS": {
        "iTOW": U4,
        "geo": U1,
        "mode": U1,
        "sys": I1,
        "service": (
            X1,
            {
                "Ranging": U1,
                "Corrections": U1,
                "Integrity": U1,
                "Testmode": U1,
                "Bad": U1,
            },
        ),
        "cnt": U1,
        "statusFlags": (
            X1,
            {
                "integrityUsed": U2,
            },
        ),
        "reserved1": U2,
        "channels": (  # repeating group * cnt
            "cnt",
            {
                "svid": U1,
                "flags": U1,
                "udre": U1,
                "svSys": U1,
                "svService": U1,
                "reserved2": U1,
                "prc": I2,
                "reserved3": U2,
                "ic": I2,
            },
        ),
    },
    "NAV-SIG": {
        "iTOW": U4,
        "version": U1,
        "numSigs": U1,
        "reserved0": U2,
        "group": (
            "numSigs",
            {  # repeating group * numSigs
                "gnssId": U1,
                "svId": U1,
                "sigId": U1,
                "freqId": U1,
                "prRes": [I2, SCAL1],
                "cno": U1,
                "qualityInd": U1,
                "corrSource": U1,
                "ionoModel": U1,
                "sigFlags": (
                    X2,
                    {
                        "health": U2,
                        "prSmoothed": U1,
                        "prUsed": U1,
                        "crUsed": U1,
                        "doUsed": U1,
                        "prCorrUsed": U1,
                        "crCorrUsed": U1,
                        "doCorrUsed": U1,
                    },
                ),
                "reserved1": U4,
            },
        ),
    },
    "NAV-SLAS": {
        "iTOW": U4,
        "version": U1,
        "reserved0": U3,
        "gmsLon": [I4, SCAL3],
        "gmsLat": [I4, SCAL3],
        "gmsCode": U1,
        "qzssSvId": U1,
        "serviceFlags": (
            X1,
            {
                "gmsAvailable": U1,
                "qzssSvAvailable": U1,
                "testMode": U1,
            },
        ),
        "cnt": U1,
        "group": (  # repeating group * cnt
            "cnt",
            {
                "gnssID": U1,
                "svId": U1,
                "reserved1": U1,
                "reserved2": U3,
                "prc": I2,
            },
        ),
    },
    "NAV-SOL": {
        "iTOW": U4,
        "fTOW": I4,
        "week": I2,
        "gpsFix": U1,
        "flags": (
            X1,
            {
                "gpsfixOK": U1,
                "diffSoln": U1,
                "wknSet": U1,
                "towSet": U1,
            },
        ),
        "ecefX": I4,
        "ecefY": I4,
        "ecefZ": I4,
        "pAcc": U4,
        "ecefVX": I4,
        "ecefVY": I4,
        "ecefVZ": I4,
        "sAcc": U4,
        "pDOP": [U2, SCAL2],
        "reserved1": U1,
        "numSV": U1,
        "reserved2": U4,
    },
    "NAV-STATUS": {
        "iTOW": U4,
        "gpsFix": U1,
        "flags": (
            X1,
            {
                "gpsFixOk": U1,
                "diffSoln": U1,
                "wknSet": U1,
                "towSet": U1,
            },
        ),
        "fixStat": (
            X1,
            {
                "diffCorr": U1,
                "carrSolnValid": U1,
                "reserved0": U4,
                "mapMatching": U2,
            },
        ),
        "flags2": (
            X1,
            {
                "psmState": U2,
                "reserved1": U1,
                "spoofDetState": U2,
                "reserved2": U1,
                "carrSoln": U2,
            },
        ),
        "ttff": U4,
        "msss": U4,
    },
    "NAV-SVIN": {
        "version": U1,
        "reserved1": U3,
        "iTOW": U4,
        "dur": U4,
        "meanX": I4,
        "meanY": I4,
        "meanZ": I4,
        "meanXHP": I1,
        "meanYHP": I1,
        "meanZHP": I1,
        "reserved2": U1,
        "meanAcc": U4,
        "obs": U4,
        "valid": U1,
        "active": U1,
        "reserved3": U2,
    },
    "NAV-SVINFO": {  # deprecated - use NAV-SAT
        "iTOW": U4,
        "numCh": U1,
        "globalFlags": (
            X1,
            {
                "chipGen": U3,
            },
        ),
        "reserved1": U2,
        "channels": (
            "numCh",
            {  # repeating group * numCh
                "chn": U1,
                "svid": U1,
                "flags": (
                    X1,
                    {
                        "svUsed": U1,
                        "diffCorr": U1,
                        "orbitAvail": U1,
                        "orbitEph": U1,
                        "unhealthy": U1,
                        "orbitAlm": U1,
                        "orbitAop": U1,
                        "smoothed": U1,
                    },
                ),
                "quality": (
                    X1,
                    {
                        "qualityInd": U4,
                    },
                ),
                "cno": U1,
                "elev": I1,
                "azim": I2,
                "prRes": I4,
            },
        ),
    },
    "NAV-TIMEBDS": {
        "iTOW": U4,
        "SOW": U4,
        "fSOW": I4,
        "week": I2,
        "leapS": I1,
        "valid": (
            X1,
            {
                "sowValid": U1,
                "weekValid": U1,
                "leapSValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMEGAL": {
        "iTOW": U4,
        "galTow": U4,
        "fGalTow": I4,
        "galWno": I2,
        "leapS": I1,
        "valid": (
            X1,
            {
                "galTowValid": U1,
                "galWnoValid": U1,
                "leapSValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMEGLO": {
        "iTOW": U4,
        "TOD": U4,
        "fTOD": I4,
        "Nt": U2,
        "N4": U1,
        "valid": (
            X1,
            {
                "todValid": U1,
                "dateValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMEGPS": {
        "iTOW": U4,
        "fTOW": I4,
        "week": I2,
        "leapS": I1,
        "valid": (
            X1,
            {
                "towValid": U1,
                "weekValid": U1,
                "leapSValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMELS": {
        "iTOW": U4,
        "version": U1,
        "reserved0": U3,
        "srcOfCurrLs": U1,
        "currLs": I1,
        "srcOfLsChange": U1,
        "lsChange": I1,
        "timeToLsEvent": I4,
        "dateOfLsGpsWn": U2,
        "dateOfLsGpsDn": U2,
        "reserved1": U3,
        "valid": (
            X1,
            {
                "validCurrLs": U1,
                "validTimeToLsEvent": U1,
            },
        ),
    },
    "NAV-TIMENAVIC": {
        "iTOW": U4,
        "NavICTow": U4,
        "fNavICTow": I4,
        "NavICWno": I2,
        "leapS": I1,
        "valid": (
            X1,
            {
                "NavICTowValid": U1,
                "NavICWnoValid": U1,
                "leapSValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMEQZSS": {
        "iTOW": U4,
        "qzssTow": U4,
        "fQzssTow": I4,
        "qzssWno": I2,
        "leapS": I1,
        "valid": (
            X1,
            {
                "qzssTowValid": U1,
                "qzssWnoValid": U1,
                "leapSValid": U1,
            },
        ),
        "tAcc": U4,
    },
    "NAV-TIMEUTC": {
        "iTOW": U4,
        "tAcc": U4,
        "nano": I4,
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "min": U1,
        "sec": U1,
        "validflags": (
            X1,
            {
                "validTOW": U1,
                "validWKN": U1,
                "validUTC": U1,
                "reserved0": U1,
                "utcStandard": U4,
            },
        ),
    },
    "NAV-VELECEF": {"iTOW": U4, "ecefVX": I4, "ecefVY": I4, "ecefVZ": I4, "sAcc": U4},
    "NAV-VELNED": {
        "iTOW": U4,
        "velN": I4,
        "velE": I4,
        "velD": I4,
        "speed": U4,
        "gSpeed": U4,
        "heading": [I4, SCAL5],
        "sAcc": U4,
        "cAcc": [U4, SCAL5],
    },
    # ********************************************************************
    #
    # NAV2 payloads are identical to NAV and are cross-referenced in
    # UBX_PAYLOADS_GET_NAV2 below.
    #
    # ********************************************************************
    # Receiver Manager Messages: i.e. Satellite Status, RTC Status.
    # Messages in the RXM class are used to output status and result data from the Receiver Manager. The output
    # rate is not bound to the navigation/measurement rate and messages can also be generated on events.
    "RXM-ALM": {
        "svid": U4,
        "week": U4,
        "group": (
            8,
            {
                "dwrd": U4,
            },
        ),
    },
    "RXM-COR": {
        "version": U1,
        "ebno": [U1, 0.125],
        "reserved0": U2,
        "statusInfo": (
            X4,
            {
                "protocol": U5,
                "errStatus": U2,
                "msgUsed": U2,
                "correctionId": U16,
                "msgTypeValid": U1,
                "msgSubTypeValid": U1,
                "msgInputHandle": U1,
                "msgEncrypted": U2,
                "msgDecrypted": U2,
            },
        ),
        "msgType": U2,
        "msgSubType": U2,
    },
    "RXM-EPH": {
        "svid": U4,
        "how": U4,
        "group": (
            8,
            {
                "sf1d": U4,
                "sf2d": U4,
                "sf3d": U4,
            },
        ),
    },
    "RXM-IMES": {
        "numTx": U1,
        "version": U1,
        "reserved1": U2,
        "group": (
            "numTx",
            {  # repeating group * numTx
                "reserved2": U1,
                "txId": U1,
                "reserved3": U3,
                "cno": U1,
                "reserved4": U2,
                "doppler": [I4, 2**-12],
                "position1_1": (
                    X4,
                    {
                        "pos1Floor": U8,
                        "pos1Lat": U23,  # signed, scaled 180 / 2^23
                    },
                ),
                "position1_2": (
                    X4,
                    {
                        "pos1Lon": U24,  # signed, scaled 360 / 2^24
                        "pos1Valid": U1,
                    },
                ),
                "position2_1": (
                    X4,
                    {
                        "pos2Floor": U8,
                        "pos2Alt": U12,
                        "pos2Acc": U2,
                        "pos2Valid": U1,
                    },
                ),
                "lat": [I4, 180 * 2**-24],
                "lon": [I4, 360 * 2**-32],
                "shortIdFrame": (
                    X4,
                    {
                        "shortId": U12,
                        "shortValid": U1,
                        "shortBoundary": U1,
                    },
                ),
                "mediumIdLSB": U4,
                "mediumId_2": (
                    X4,
                    {
                        "mediumIdMSB": U1,
                        "mediumValid": U1,
                        "mediumBoundary": U1,
                    },
                ),
            },
        ),
    },
    "RXM-MEAS20": {
        "group": (
            "None",
            {
                "payload": U1,
            },
        )
    },
    "RXM-MEAS50": {
        "group": (
            "None",
            {
                "payload": U1,
            },
        )
    },
    "RXM-MEASC12": {
        "group": (
            "None",
            {
                "payload": U1,
            },
        )
    },
    "RXM-MEASD12": {
        "group": (
            "None",
            {
                "payload": U1,
            },
        )
    },
    "RXM-MEASX": {
        "version": U1,
        "reserved0": U3,
        "gpsTOW": U4,
        "gloTOW": U4,
        "bdsTOW": U4,
        "reserved1": U4,
        "qzssTOW": U4,
        "gpsTOWacc": [U2, 0.0625],
        "gloTOWacc": [U2, 0.0625],
        "bdsTOWacc": [U2, 0.0625],
        "reserved2": U2,
        "qzssTOWacc": [U2, 0.0625],
        "numSv": U1,
        "flags": (
            X1,
            {
                "towSet": U2,
            },
        ),
        "reserved3": U8,
        "group": (
            "numSv",
            {  # repeating group * numSv
                "gnssId": U1,
                "svId": U1,
                "cNo": U1,
                "mpathIndic": U1,
                "dopplerMS": [I4, 0.04],
                "dopplerHz": [I4, 0.2],
                "wholeChips": U2,
                "fracChips": U2,
                "codePhase": [U4, 2**-21],
                "intCodePhase": U1,
                "pseuRangeRMSErr": U1,
                "reserved4": U2,
            },
        ),
    },
    "RXM-PMP-V0": {
        "version": U1,  # 0x00
        "reserved0": U3,
        "timeTag": U4,
        "uniqueWord1": U4,
        "uniqueWord2": U4,
        "serviceIdentifier": U2,
        "spare": U1,
        "uniqueWordBitErrors": U1,
        "groupUserData": (
            504,
            {
                "userData": U1,
            },
        ),  # repeating group * 504
        "fecBits": U2,
        "ebno": [U1, 0.125],
        "reserved1": U1,
    },
    "RXM-PMP-V1": {
        "version": U1,  # 0x01
        "reserved0": U1,
        "numBytesUserData": U2,
        "timeTag": U4,
        "uniqueWord1": U4,
        "uniqueWord2": U4,
        "serviceIdentifier": U2,
        "spare": U1,
        "uniqueWordBitErrors": U1,
        "fecBits": U2,
        "ebno": [U1, 0.125],
        "reserved1": U1,
        "groupUserData": (
            "numBytesUserData",
            {  # repeating group * numBytesUserData
                "userData": U1,
            },
        ),
    },
    "RXM-QZSSL6": {
        "version": U1,
        "svId": U1,
        "cno": [U2, 2**-8],
        "timeTag": U4,
        "groupDelay": U1,
        "bitErrCorr": U1,
        "chInfo": (
            X2,
            {
                "reserved1": U8,
                "chn": U2,
                "msgName": U1,
                "reserved2": U1,
                "errStatus": U2,
                "chName": U2,
            },
        ),
        "reserved0": U2,
        "msgBytes": A250,  # parsed as U1[250]
    },
    "RXM-RAW": {
        "iTOW": I4,
        "week": I2,
        "numSV": U1,
        "reserved1": U1,
        "group": (
            "numSV",
            {  # repeating group * numSV
                "cpMes": R8,
                "prMes": R8,
                "doMes": R4,
                "sv": U1,
                "mesQI": I1,
                "cno": I1,
                "lli": U1,
            },
        ),
    },
    "RXM-RAWX": {
        "rcvTow": R8,
        "week": U2,
        "leapS": I1,
        "numMeas": U1,
        "recStat": (
            X1,
            {
                "leapSec": U1,
                "clkReset": U1,
            },
        ),
        "reserved1": U3,
        "group": (
            "numMeas",
            {  # repeating group * numMeas
                "prMes": R8,
                "cpMes": R8,
                "doMes": R4,
                "gnssId": U1,
                "svId": U1,
                "sigId": U1,
                "freqId": U1,
                "locktime": U2,
                "cno": U1,
                "prStdev": (
                    X1,  # scaling = 0.01*2^-n
                    {
                        "prStd": U4,
                    },
                ),
                "cpStdev": (
                    X1,  # scaling = 0.004
                    {
                        "cpStd": U4,
                    },
                ),
                "doStdev": (
                    X1,  # scaling = 0.002*2^n
                    {
                        "doStd": U4,
                    },
                ),
                "trkStat": (
                    X1,
                    {
                        "prValid": U1,
                        "cpValid": U1,
                        "halfCyc": U1,
                        "subHalfCyc": U1,
                    },
                ),
                "reserved3": U1,
            },
        ),
    },
    "RXM-RLM-S": {
        "version": U1,  # 0x00
        "type": U1,  # 0x01
        "svId": U1,
        "reserved0": U1,
        "beacon": U8,
        "message": U1,
        "params": U2,
        "reserved1": U1,
    },
    "RXM-RLM-L": {
        "version": U1,  # 0x00
        "type": U1,  # 0x02
        "svId": U1,
        "reserved0": U1,
        "beacon": U8,
        "message": U1,
        "params": U12,
        "reserved1": U3,
    },
    "RXM-RTCM": {
        "version": U1,  # 0x02
        "flags": (
            X1,
            {
                "crcFailed": U1,
                "msgUsed": U2,
            },
        ),
        "subType": U2,
        "refStation": U2,
        "msgType": U2,
    },
    "RXM-SFRB": {
        "chn": U1,
        "svid": U1,
        "group": (
            10,
            {
                "dwrd": X4,
            },
        ),
    },
    "RXM-SFRBX": {
        "gnssId": U1,
        "svId": U1,
        "sigId": U1,
        "freqId": U1,
        "numWords": U1,
        "chn": U1,
        "version": U1,
        "reserved0": U1,
        "navdata": ("numWords", {"dwrd": U4}),  # repeating group * numWords
    },
    "RXM-SPARTN": {
        "version": U1,
        "flags": (
            X1,
            {
                "reserved1": U1,
                "msgUsed": U2,
            },
        ),
        "subType": U2,
        "reserved0": U2,
        "msgType": U2,
    },
    "RXM-SPARTN-KEY": {
        "version": U1,
        "numKeys": U1,
        "reserved0": U2,
        "group1": (  # repeating group * numKeys
            "numKeys",
            {
                "encryptAlgorithm": U1,  # according to UBX-22008160-R02
                "keyLengthBytes": U1,
                "validFromWno": U2,
                "validFromTow": U4,
            },
        ),
        "group2": (  # repeating group * (numKeys * keyLengthBytes)
            "None",
            {
                "key": U1,
            },
        ),
    },
    "RXM-SVSI": {
        "iTOW": U4,
        "week": I2,
        "numVis": U1,
        "numSV": U1,
        "group": (  # repeating group * numSv
            "numSV",
            {
                "svid": U1,
                "svFlag": (
                    X1,
                    {
                        "ura": U4,
                        "healthy": U1,
                        "ephVal": U1,
                        "almVal": U1,
                        "notAvail": U1,
                    },
                ),
                "azim": I2,
                "elev": I1,
                "age": (
                    X1,
                    {
                        "almAge": U4,
                        "ephAge": U4,
                    },
                ),
            },
        ),
    },
    "RXM-TM": {
        "version": U1,
        "numMeas": U1,
        "reserved0": U2,
        "reserved1": U4,
        "group": (
            "numMeas",
            {
                "edgeInfo": (
                    X4,
                    {
                        "channel": U4,
                        "edgeType": U1,
                    },
                ),
                "count": U2,
                "wno": U2,
                "towMs": U4,
                "towSubMsR": U4,
                "reserved2": U4,
                "reserved3": U4,
            },
        ),
    },
    # ********************************************************************
    # Security Feature Messages
    # Messages in the SEC class are used for security features of the receiver.
    "SEC-SIG": {
        "version": U1,  # 0x01
        "reserved0": U3,
        "jamFlags": (
            X1,
            {
                "jamDetEnabled": U1,
                "jammingState": U2,
            },
        ),
        "reserved1": U3,
        "spfFlags": (
            X1,
            {
                "spfDetEnabled": U1,
                "spoofingState": U3,
            },
        ),
        "reserved2": U3,
    },
    "SEC-SIGLOG": {
        "version": U1,  # 0x00
        "numEvents": U1,
        "reserved0": U6,
        "group": (
            "numEvents",
            {
                "timeElapsed": U4,
                "detectionType": U1,
                "eventType": U1,
            },
        ),
        "reserved1": U2,
    },
    "SEC-SIGN": {
        "version": U1,
        "reserved1": U3,
        "classID": U1,
        "messageID": U1,
        "checksum": U2,
        "hash": U32,
    },
    "SEC-UNIQID": {"version": U1, "reserved0": U3, "uniqueId": U5},  # 0x01
    "SEC-UNIQID-V2": {"version": U1, "reserved0": U3, "uniqueId": U6},  # 0x02 for M10
    # ********************************************************************
    # Timing Messages: i.e. Time Pulse Output, Time Mark Results.
    # Messages in the TIM class are used to output timing information from the receiver, like Time Pulse and Time
    # Mark measurements.
    "TIM-DOSC": {"version": U1, "reserved1": U3, "value": U4},
    "TIM-FCHG": {
        "version": U1,
        "reserved1": U3,
        "iTOW": U4,
        "intDeltaFreq": [I4, 2**-8],
        "intDeltaFreqU": [U4, 2**-8],
        "intRaw": U4,
        "extDeltaFreq": [I4, 2**-8],
        "extDeltaFreqU": [U4, 2**-8],
        "extRaw": U4,
    },
    "TIM-SMEAS": {
        "version": U1,  # 0x00
        "numMeas": U1,
        "reserved1": U2,
        "iTOW": U4,
        "reserved2": U4,
        "group": (  # repeating group * numMeas
            "numMeas",
            {
                "sourceId": U1,
                "flags": (
                    X1,
                    {
                        "freqValid": U1,
                        "phaseValid": U1,
                    },
                ),
                "phaseOffsetFrac": [I1, 2**-8],
                "phaseUncFrac": [U1, 2**-8],
                "phaseOffset": I4,
                "phaseUnc": U4,
                "reserved3": U4,
                "freqOffset": [I4, 2**-8],
                "freqUnc": [U4, 2**-8],
            },
        ),
    },
    "TIM-SVIN": {
        "dur": U4,
        "meanX": I4,
        "meanY": I4,
        "meanZ": I4,
        "meanV": U4,
        "obs": U4,
        "valid": U1,
        "active": U1,
        "reserved1": U2,
    },
    "TIM-TM2": {
        "ch": U1,
        "flags": (
            X1,
            {
                "mode": U1,
                "run": U1,
                "newFallingEdge": U1,
                "timeBase": U2,
                "utc": U1,
                "time": U1,
                "newRisingEdge": U1,
            },
        ),
        "count": U2,
        "wnR": U2,
        "wnF": U2,
        "towMsR": U4,
        "towSubMsR": U4,
        "towMsF": U4,
        "towSubMsF": U4,
        "accEst": U4,
    },
    "TIM-TOS": {
        "version": U1,  # 0x00
        "gnssId": U1,
        "reserved11": U2,
        "flags": (
            X4,
            {
                "leapNow": U1,
                "leapSoon": U1,
                "leapPositive": U1,
                "timeInLimit": U1,
                "intOscInLimit": U1,
                "extOscInLimit": U1,
                "gnssTimeValid": U1,
                "UTCTimeValid": U1,
                "DiscSrc": U3,
                "raim": U1,
                "cohPulse": U1,
                "lockedPulse": U1,
            },
        ),
        "year": U2,
        "month": U1,
        "day": U1,
        "hour": U1,
        "minute": U1,
        "second": U1,
        "utcStandard": U1,
        "utcOffset": I4,
        "utcUncertainty": U4,
        "week": U4,
        "TOW": U4,
        "gnssOffset": I4,
        "gnssUncertainty": U4,
        "intOscOffset": [I4, 2**-8],
        "intOscUncertainty": [U4, 2**-8],
        "extOscOffset": [I4, 2**-8],
        "extOscUncertainty": [U4, 2**-8],
    },
    "TIM-TP": {
        "towMS": U4,
        "towSubMS": [U4, 2**-32],
        "qErr": I4,
        "week": U2,
        "flags": (
            X1,
            {
                "timeBase": U1,
                "utc": U1,
                "raim": U2,
                "qErrInvalid": U1,
            },
        ),
        "refinfo": (
            X1,
            {
                "timeRefGnss": U4,
                "utcStandard": U4,
            },
        ),
    },
    "TIM-VCOCAL": {
        "type": U1,
        "version": U1,
        "oscId": U1,
        "reserved1": U3,
        "gainUncertainty": [U2, 2**-16],
        "gainVco": [I4, 2**-16],
    },
    "TIM-VRFY": {
        "itow": I4,
        "frac": I4,
        "deltaMs": I4,
        "deltaNs": I4,
        "wno": U2,
        "flags": (
            X1,
            {
                "src": U3,
            },
        ),
        "reserved1": U1,
    },
    # ********************************************************************
    # Firmware Update Messages: i.e. Memory/Flash erase/write, Reboot, Flash identification, etc..
    # Messages in the UPD class are used to update the firmware and identify any attached flash device.
    "UPD-SOS": {  # System restored from backup
        "cmd": U1,
        "reserved0": U3,
        "response": U1,
        "reserved1": U3,
    },
    # ********************************************************************
    # UBX nominal payload definition, used as fallback where no documented
    # payload definition is available.
    "UBX-NOMINAL": {
        "group": (
            "None",
            {
                "data": X1,
            },
        )
    },
    # ********************************************************************
    # Dummy message for error testing
    "FOO-BAR": {"spam": "Z2", "eggs": "Y1"},
}

# ********************************************************************
# Navigation 2 Messages: i.e. Position, Speed, Time, Acceleration, Heading, DOP, SVs used.
# The messages in the UBX-NAV2 class are used to output navigation results and data, such as
# position, altitude and velocity in a number of formats, and status flags and accuracy estimate
# figures, or satellite and signal information. The messages are generated with the configured
# navigation rate.
_UBX_PAYLOADS_GET_NAV2 = {
    "NAV2-CLOCK": UBX_PAYLOADS_GET["NAV-CLOCK"],
    "NAV2-COV": UBX_PAYLOADS_GET["NAV-COV"],
    "NAV2-DOP": UBX_PAYLOADS_GET["NAV-DOP"],
    "NAV2-EELL": UBX_PAYLOADS_GET["NAV-EELL"],
    "NAV2-EOE": UBX_PAYLOADS_GET["NAV-EOE"],
    "NAV2-ODO": UBX_PAYLOADS_GET["NAV-ODO"],
    "NAV2-POSECEF": UBX_PAYLOADS_GET["NAV-POSECEF"],
    "NAV2-POSLLH": UBX_PAYLOADS_GET["NAV-POSLLH"],
    "NAV2-PVAT": UBX_PAYLOADS_GET["NAV-PVAT"],
    "NAV2-PVT": UBX_PAYLOADS_GET["NAV-PVT"],
    "NAV2-SAT": UBX_PAYLOADS_GET["NAV-SAT"],
    "NAV2-SBAS": UBX_PAYLOADS_GET["NAV-SBAS"],
    "NAV2-SIG": UBX_PAYLOADS_GET["NAV-SIG"],
    "NAV2-SLAS": UBX_PAYLOADS_GET["NAV-SLAS"],
    "NAV2-STATUS": UBX_PAYLOADS_GET["NAV-STATUS"],
    "NAV2-SVIN": UBX_PAYLOADS_GET["NAV-SVIN"],
    "NAV2-TIMEBDS": UBX_PAYLOADS_GET["NAV-TIMEBDS"],
    "NAV2-TIMEGAL": UBX_PAYLOADS_GET["NAV-TIMEGAL"],
    "NAV2-TIMEGLO": UBX_PAYLOADS_GET["NAV-TIMEGLO"],
    "NAV2-TIMEGPS": UBX_PAYLOADS_GET["NAV-TIMEGPS"],
    "NAV2-TIMELS": UBX_PAYLOADS_GET["NAV-TIMELS"],
    "NAV2-TIMENAVIC": UBX_PAYLOADS_GET["NAV-TIMENAVIC"],
    "NAV2-TIMEQZSS": UBX_PAYLOADS_GET["NAV-TIMEQZSS"],
    "NAV2-TIMEUTC": UBX_PAYLOADS_GET["NAV-TIMEUTC"],
    "NAV2-VELECEF": UBX_PAYLOADS_GET["NAV-VELECEF"],
    "NAV2-VELNED": UBX_PAYLOADS_GET["NAV-VELNED"],
}

# Update main dictionary with NAV2 definitions
UBX_PAYLOADS_GET.update(_UBX_PAYLOADS_GET_NAV2)
