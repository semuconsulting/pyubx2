# pylint: disable=unused-import
'''
UBX Protocol payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _SET_ MESSAGES _TO_ THE RECEIVER

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

@author: semuadmin
'''

from pyubx2.ubxtypes_core import U1, I1, X1, U2, I2, X2, U3, U4, I4, U5, X4, R4, U6, X6, R8, C06, C10, C30, C32, CH

UBX_PAYLOADS_SET = {
'AID-ALM': {
'svid': U4,
'week': U4,
'optBlock': {  # TODO repeating group but optional and no index so how to handle?
'dwrd': U4
}},
'AID-ALPSRV': {
'idSize': U1,
'type': U1,
'ofs': U2,
'size': U2,
'fileId': U2,
'dataSize': U2,
'id1': U1,
'id2': U1,
'id3': U1
},
# 'AID-ALP' : {  # TODO - need to review datasheet
# },
# 'AID-AOP' : {  # TODO - need to review datasheet
# },
# 'AID-EPH' : {  # TODO - need to review datasheet
# },
'AID-HUI': {
'health': X4,
'utcA0': R8,
'utcA1': R8,
'utcTOW': I4,
'utcWNT': I2,
'utcLS': I2,
'utcWNF': I2,
'utcDNs': I2,
'utcLSF': I2,
'utcSpare': I2,
'klobA0': R4,
'klobA1': R4,
'klobA2': R4,
'klobA3': R4,
'klobB0': R4,
'klobB1': R4,
'klobB2': R4,
'klobB3': R4,
'flags': X4
},
# ********************************************************************
'CFG-ANT': {
'flags': X2,
'pins': X2
},
'CFG-CFG': {
'clearMask': X4,
'saveMask' : X4,
'loadMask': X4,
'deviceMask': X1
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
'CFG-DOSC': {
'version': U1,
'numOsc': U1,
'reserved1': U2,
'group': {  # repeating group * numOsc
'oscId': U1,
'reserved2': U1,
'flags': X2,
'freq': U4,
'phaseOffset': I4,
'withTemp': U4,
'withAge': U4,
'timeToTemp': U2,
'reserved3': U1[2],
'gainVco': I4,
'gainUncertainty': U1,
'reserved4': U3
}},
'CFG-DYNSEED': {
'version': U1,
'reserved1': U3,
'seedHi': U4,
'seedLo': U4
},
'CFG-ESRC': {
'version': U1,
'numSources': U1,
'reserved1': U2,
'group': {  # repeating group * numSources
'extInt': U1,
'flags': X2,
'freq': U4,
'reserved2': U4,
'withTemp': U4,
'withAge': U4,
'timeToTemp': U2,
'maxDevLifeTim': U2,
'offset': I4,
'offsetUncertainty': U4,
'jitter': U4
}},
'CFG-FIXSEED': {
'version': U1,
'length': U1,
'reserved1': U2,
'seedHi': U4,
'seedLo': U4,
'group': {  # repeating group * length
'classId': U1,
'msgId': U1
}},
'CFG-GEOFENCE': {
'version': U1,
'numFences': U1,
'confLvl': U1,
'reserved1': U1[1],
'pioEnabled': U1,
'pinPolarity': U1,
'pin': U1,
'reserved2': U1[1],
'group': {  # repeating group * numFences
'lat': I4,
'lon': I4,
'radius': U4
}},
'CFG-GNSS': {
'msgVer': U1,
'numTrkChHw': U1,
'numTrkChUse': U1,
'numConfigBlocks': U1,
'group': {  # repeating group * numConfigBlocks
'gnssId': U1,
'resTrkCh': U1,
'maxTrkCh': U1,
'reserved1': U1,
'flags': X4
}},
'CFG-INF': {
'protocolID': U1,
'reserved1': U3,
'infMsgMaskDDC': X1,
'infMsgMaskUART1': X1,
'infMsgMaskUART2': X1,
'infMsgMaskUSB': X1,
'infMsgMaskSPI': X1,
'reserved2': X1
},
'CFG-ITFM': {
'config': X4,
'config2': X4
},
'CFG-LOGFILTER': {
'version': U1,
'flags': X1,
'minInterval': U2,
'timeThreshold': U2,
'speedThreshold': U2,
'positionThreshold': U4
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
'CFG-NAV5': {
'mask': X2,
'dynModel': U1,
'fixMode': U1,
'fixedAlt': I4,
'fixedAltVar': U4,
'minElev': I1,
'drLimit': U1,
'pDop': U2,
'tDop': U2,
'pAcc': U2,
'tAcc': U2,
'staticHoldThresh': U1,
'dgpsTimeOut': U1,
'reserved2': U4,
'reserved3': U4,
'reserved4': U4
},
'CFG-NAVX5': {
'mask1': X2,
'reserved0': U4,
'reserved1': U1,
'reserved2': U1,
'minSVs': U1,
'maxSVs': U1,
'minCNO': U1,
'reserved5': U1,
'iniFix3D': U1,
'reserved6': U1,
'reserved7': U1,
'reserved8': U1,
'wknRollover': U2,
'reserved9': U1,
'reserved10': U1,
'reserved11': U1,
'usePPP': U1,
'useAOP': U1,
'reserved12': U1,
'reserved13': U1,
'aopOrbMaxErr': U2,
'reserved3': U4,
'reserved4': U4
},
'CFG-NMEA': {
'filter': X1,
'version': U1,
'numSV': U1,
'flags': X1
},
'CFG-ODO': {
'version': U1,
'reserved1': U3,
'flags': U1,
'odoCfg': X1,
'reserved2': U6,
'cogMaxSpeed': U1,
'cogMaxPosAcc': U1,
'reserved3': U2,
'velLpGain': U1,
'cogLpGain': U1,
'reserved4': U2
},
# 'CFG-EKF': {
# 'disableEkf': U1,
# 'actionFlags': X1,
# 'configFlags': U1,
# 'inverseFlags': X1,
# 'reserved2': U4,
# 'nomPPDist': U2,
# 'nomZero': U2,
# 'nomSens': U1,
# 'rmsTemp': U1,
# 'tempUpdate': U2
# },
# 'CFG-ESFGWT': {
# 'flags':X2,
# 'id': U2,
# 'wtFactor': U4,
# 'reserved1': U4,
# 'wtQuantError': U4,
# 'timeTagFactor': U4,
# 'wtCountMax': U4,
# 'timeTagMax': U4,
# 'wtLatency': U2,
# 'reserved2': U2,
# 'wtFrequency': U1,
# 'reserved3': U1,
# 'speedDeadBand': U2,
# 'reserved4': U4,
# 'reserved5': U4
# },
'CFG-PM2': {
'version': U1,
'reserved1': U1,
'reserved2': U1,
'reserved3': U1,
'flags': X4,
'updatePeriod': U4,
'searchPeriod': U4,
'gridOffset': U4,
'onTime': U2,
'minAcqTime': U2,
'reserved4': U2,
'reserved5': U2,
'reserved6': U4,
'reserved7': U4,
'reserved8': U1,
'reserved9': U1,
'reserved10': U2,
'reserved11': U4
},
# 'CFG-PM':{
# 'version': U1,
# 'reserved1': U1,
# 'reserved2': U1,
# 'reserved3': U1,
# 'flags': X4,
# 'updatePeriod': U4,
# 'searchPeriod': U4,
# 'gridOffset': U4,
# 'onTime': U2,
# 'minAcqTime': U2
# },
'CFG-PMS': {
'version': U1,
'powerSetupValue': U1,
'period': U2,
'onTime': U2,
'reserved1': U2
},
'CFG-PRT': {
'portID': U1,
'reserved0': U1,
'txReady': X2,
'mode': X4,
'baudRate': U4,
'inProtoMask': X2,
'outProtoMask': X2,
'reserved4': U2,
'reserved5': U2
},
'CFG-PWR': {
'version': U1,
'reserved1': U3,
'state': U4
},
'CFG-RATE': {
'measRate': U2,
'navRate': U2,
'timeRef': U2
},
'CFG-RINV': {
'flags': X1,
'group': {  # repeating group
'data': U1
}},
'CFG-RST': {
'navBbrMask': X2,
'resetMode': U1,
'reserved1': U1
},
'CFG-RXM': {
'reserved1': U1,
'lpMode': U1
},
'CFG-SBAS': {
'mode': X1,
'usage': X1,
'maxSBAS': U1,
'scanmode2': X1,
'scanmode1': X4
},
'CFG-SMGR': {
'minGNSSFix' : U1,
'maxFreqChange': U2,
'maxPhaseCorrRate': U2,
'reserved1': U2,
'freqTolerance' : U2,
'timeTolerance': U2,
'messageCfg': X2,
'maxSlewRate': U2,
'flags': X4
},
'CFG-TMODE2': {
'timeMode': U1,
'reserved1': U1,
'flags': X2,
'ecefXOrLat': I4,
'ecefYOrLon': I4,
'ecefZOrAlt': I4,
'fixedPosAcc': U4,
'svinMinDur': U4,
'svinAccLimit': U4
},
# 'CFG-TMODE': {
# 'timeMode': U4,
# 'fixedPosX': I4,
# 'fixedPosY': I4,
# 'fixedPosZ': I4,
# 'fixedPosVar': U4,
# 'svinMinDur': U4,
# 'svinAccLimit': U4
# },
'CFG-TP5': {
'tpIdx': U1,
'reserved0': U1,
'reserved1': U2,
'antCableDelay': I2,
'rfGroupDelay': I2,
'freqPeriod': U4,
'freqPeriodLock': U4,
'pulseLenRatio': U4,
'pulseLenRatioLock': U4,
'userConfigDelay': I4,
'flags': X4
},
# 'CFG-TP': {
# 'internal': U4,
# 'length': U4,
# 'status': I1,
# 'timeRef': U1,
# 'flags': U1,
# 'reserved1': U1,
# 'antCableDelay': I2,
# 'rfGroupDelay': I2,
# 'userDelay': I4
# },
'CFG-TXSLOT': {
'version': U1,
'enable': X1,
'refTp': U1,
'reserved1': U1,
'end1': U4,
'end2': U4,
'end3': U4
},
'CFG-USB': {
'vendorID': U2,
'productID': U2,
'reserved1': U2,
'reserved2': U2,
'powerConsumpt': U2,
'flags': X2,
'vendorString': C32,
'productString': C32,
'serialNumber': C32
},
# ********************************************************************
# 'ESF-MEAS': {
# 'timeTag': U4,
# 'flags': X2,
# 'id': U2,
# 'datagroup': {
# 'data': X4
# },
# 'calibgroup': {
# 'calibtTag': U4
# }},
'LOG-ERASE': {
},
'LOG-RETRIEVE': {
'startNumber': U4,
'entryCount': U4,
'version': U1,
'reserved': U3
},
'LOG-STRING': {
'group': {  # repeating group
'bytes': U1
}},
'NAV-RESETODO': {
},
'RXM-PMREQ': {
'duration': U4,
'flags': X4
},
'TIM-HOC': {
'version': U1,
'oscId': U1,
'flags': U1,
'reserved1': U1,
'value': I4
}
}
