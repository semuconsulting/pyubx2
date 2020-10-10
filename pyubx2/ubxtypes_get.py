# pylint: disable=unused-import
'''
UBX Protocol payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _GET_ MESSAGES _FROM_ THE RECEIVER
(i.e. Periodic Navigation Data, Poll Responses, Info messages)

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

@author: semuadmin
'''

from pyubx2.ubxtypes_core import U1, I1, X1, U2, I2, X2, U3, U4, I4 , X4 , R4 , X6, R8 , C06, C10, C30, C32, CH

UBX_PAYLOADS_GET = {
'ACK-ACK': {
'clsID': U1,
'msgID': U1
},
'ACK-NAK': {
'clsID': U1,
'msgID': U1
},
'AID-ALM': {
'svid': U4,
'week': U4,
'optBlock': {
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
'id3': U1,
'group': {  # repeating group
'data': U2
}},
# 'AID-ALP' : { # TODO need to review datasheet
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
'AID-INI': {
'ecefXOrLat': I4,
'ecefYOrLon': I4,
'ecefZOrAlt': I4,
'posAcc': U4,
'tmCfg': X2,
'wn': U2,
'tow': U4,
'towNs': I4,
'tAccMs': U4,
'tAccNs': U4,
'clkDOrFreq': I4,
'clkDAccOrFreq': U4,
'flags': X4
},
'CFG-ANT': {
'flags': X2,
'pins': X2
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
'CFG-EKF': {
'disableEkf': U1,
'actionFlags': X1,
'configFlags': U1,
'inverseFlags': X1,
'reserved2': U4,
'nomPPDist': U2,
'nomZero': U2,
'nomSens': U1,
'rmsTemp': U1,
'tempUpdate': U2
},
'CFG-ESFGWT': {
'flags':X2,
'id': U2,
'wtFactor': U4,
'reserved1': U4,
'wtQuantError': U4,
'timeTagFactor': U4,
'wtCountMax': U4,
'timeTagMax': U4,
'wtLatency': U2,
'reserved2': U2,
'wtFrequency': U1,
'reserved3': U1,
'speedDeadBand': U2,
'reserved4': U4,
'reserved5': U4
},
'CFG-INF': {
'protocolID': U1,
'reserved0': U1,
'reserved1': U2,
'infMsgMask': X6
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
'CFG-PM':{
'version': U1,
'reserved1': U1,
'reserved2': U1,
'reserved3': U1,
'flags': X4,
'updatePeriod': U4,
'searchPeriod': U4,
'gridOffset': U4,
'onTime': U2,
'minAcqTime': U2
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
'CFG-RATE': {
'measRate': U2,
'navRate': U2,
'timeRef': U2
},
'CFG-RINV': {
'flags': X1,
'group': {
'data': U1
}},
'CFG-RXM': {
'reserved1': U1,
'lpMode': U1
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
'CFG-TMODE': {
'timeMode': U4,
'fixedPosX': I4,
'fixedPosY': I4,
'fixedPosZ': I4,
'fixedPosVar': U4,
'svinMinDur': U4,
'svinAccLimit': U4
},
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
'CFG-TP': {
'internal': U4,
'length': U4,
'status': I1,
'timeRef': U1,
'flags': U1,
'reserved1': U1,
'antCableDelay': I2,
'rfGroupDelay': I2,
'userDelay': I4
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
'ESF-MEAS': {
'timeTag': U4,
'flags': X2,
'id': U2,
'datagroup': {
'data': X4
},
'calibgroup': {  # TODO repeating group but optional and no index so how to handle?
'calibtTag': U4
}},
'ESF-STATUS': {
'iTOW': U4,
'version': U1,
'reserved1': U1,
'reserved2': U2,
'reserved3': U4,
'status': U1,
'reserved4': U1,
'reserved5': U1,
'numCh': U1,
'group': {  # repeating block
'sensStatus1': X1,
'sensStatus2': X2,
'freq': U1,
'faults': X1,
}},
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
'MON-GNSS': {
'version': U1,
'supported': X1,
'default': X1,
'enabled': X1,
'simultaneous': U1,
'reserved11': U1,
'reserved12': U1,
'reserved13': U1,
},
'MON-HW2': {
'ofsI': I1,
'magI': U1,
'ofsQ': I1,
'magQ': U1,
'cfgSource': U1,
'reserved01': U1,
'reserved02': U1,
'reserved03': U1,
'lowLevCfg': X4,
'reserved11': U4,
'reserved12': U4,
'postStatus': X4,
'reserved2': U4
},
'MON-HW': {
'pinSel': X4,
'pinBank': X4,
'pinDir': X4,
'pinVal': X4,
'noisePerMS': U2,
'agcCnt': U2,
'aStatus': U1,
'aPower': U1,
'flags': X1,
'reserved1': U1,
'usedMask': X4,
'VP01': X1,
'VP02': X1,
'VP03': X1,
'VP04': X1,
'VP05': X1,
'VP06': X1,
'VP07': X1,
'VP08': X1,
'VP09': X1,
'VP10': X1,
'VP11': X1,
'VP12': X1,
'VP13': X1,
'VP14': X1,
'VP15': X1,
'VP16': X1,
'VP17': X1,
'VP18': X1,
'VP19': X1,
'VP20': X1,
'VP21': X1,
'VP22': X1,
'VP23': X1,
'VP24': X1,
'VP25': X1,
'jamInd': U1,
'reserved3': U2,
'pinIrq': X4,
'pullH': X4,
'pullL': X4
},
'MON-IO': {
'rxBytes': U4,
'txBytes': U4,
'parityErrs': U2,
'framingErrs': U2,
'overrunErrs': U2,
'breakCond': U2,
'rxBusy': U1,
'txBusy': U1,
'reserved1': U2
},
'MON-MSGPP': {
'msg10': U2,
'msg11': U2,
'msg12': U2,
'msg13': U2,
'msg14': U2,
'msg15': U2,
'msg16': U2,
'msg17': U2,
'msg20': U2,
'msg21': U2,
'msg22': U2,
'msg23': U2,
'msg24': U2,
'msg25': U2,
'msg26': U2,
'msg27': U2,
'msg30': U2,
'msg31': U2,
'msg32': U2,
'msg33': U2,
'msg34': U2,
'msg35': U2,
'msg36': U2,
'msg37': U2,
'msg40': U2,
'msg41': U2,
'msg42': U2,
'msg43': U2,
'msg44': U2,
'msg45': U2,
'msg46': U2,
'msg47': U2,
'msg50': U2,
'msg51': U2,
'msg52': U2,
'msg53': U2,
'msg54': U2,
'msg55': U2,
'msg56': U2,
'msg57': U2,
'msg60': U2,
'msg61': U2,
'msg62': U2,
'msg63': U2,
'msg64': U2,
'msg65': U2,
'msg66': U2,
'msg67': U2,
'skipped1': U4,
'skipped2': U4,
'skipped3': U4,
'skipped4': U4,
'skipped5': U4,
'skipped6': U4
},
'MON-PATCH': {
'version': U2,
'nEntries': U2,
'group': { # repeating group
'patchInfo': X4,
'comparatorNumber': U4,
'patchAddress': U4,
'patchData': U4,
}},
'MON-RXBUF': {
'pending0': U2,
'pending1': U2,
'pending2': U2,
'pending3': U2,
'pending4': U2,
'pending5': U2,
'usage0': U1,
'usage1': U1,
'usage2': U1,
'usage3': U1,
'usage4': U1,
'usage5': U1,
'peakUsage0': U1,
'peakUsage1': U1,
'peakUsage2': U1,
'peakUsage3': U1,
'peakUsage4': U1,
'peakUsage5': U1
},
'MON-RXR': {
'flags': U1
},
'MON-SMGR': {
'version': U1,
'reserved11': U1,
'reserved12': U1,
'reserved13': U1,
'iTOW': U4,
'intOsc': X2,
'extOsc': X2,
'discSrc': U1,
'gnss': X1,
'extInt0': X1,
'extInt1': X1
},
'MON-TXBUF': {
'pending0': U2,
'pending1': U2,
'pending2': U2,
'pending3': U2,
'pending4': U2,
'pending5': U2,
'usage0': U1,
'usage1': U1,
'usage2': U1,
'usage3': U1,
'usage4': U1,
'usage5': U1,
'peakUsage0': U1,
'peakUsage1': U1,
'peakUsage2': U1,
'peakUsage3': U1,
'peakUsage4': U1,
'peakUsage5': U1,
'tUsage': U1,
'tPeakUsage': U1,
'errors': X1,
'reserved1': U1
},
'MON-VER': {
'swVersion': C30,
'hwVersion': C30,
'romVersion': C30,
'group': {
'extension': C30
}},
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
}},
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
'NAV-EOE': {
'iTOW': U4
},
'NAV-GEOFENCE': {
'iTOW': U4,
'version' : U1,
'status' : U1,
'numFences': U1,
'combState': U1,
'group': { # repeating group
'state': U1,
'reserved1': U1
}},
'NAV-ODO' : {
'version' : U1,
'reserved11': U1,
'reserved12': U1,
'reserved13': U1,
'iTOW': U4,
'distance' : U4,
'totalDistance' : U4,
'distanceStd' : U4
},
'NAV-ORB' : {
'iTOW': U4,
'version' : U1,
'numCh' : U1,
'reserved11': U1,
'reserved12': U1,
'group' : {
'gnssId': U1,
'svId': U1,
'svFlag': X1,
'eph': X1,
'alm': X1,
'otherOrb': X1
}},
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
'hAcc': U4,
'vAcc': U4
},
'NAV-PVT': {
'iTOW': U4,
'year': U2,
'month': U1,
'day': U1,
'hour': U1,
'min': U1,
'second': U1,
'valid': X1,
'tAcc': U4,
'nano': I4,
'fixType': U1,
'flags': X1,
'flags2': X1,
'numSV': U1,
'lon': I4,
'lat': I4,
'height': I4,
'hMSL': I4,
'hAcc': U4,
'vAcc': U4,
'velN': I4,
'velE': I4,
'velD': I4,
'gSpeed': I4,
'headMot': I4,
'sAcc': U4,
'headAcc': U4,
'pDOP': U2,
'reserved11': U1,
'reserved12': U1,
'reserved13': U1,
'reserved14': U1,
'reserved15': U1,
'reserved16': U1,
'headVeh': I4,
'magDec': I2,
'magAcc': U2
},
'NAV-SAT': {
'iTOW': U4,
'version' : U1,
'numCh' : U1,
'reserved11': I1,
'reserved12': I1,
'group': {
'gnssId': U1,
'svId': U1,
'cno': U1,
'elev': I1,
'azim': I2,
'prRes': I2,
'flags': X4
}},
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
}},
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
'prRes': I4
}},
'NAV-TIMEBDS': {
'iTOW': U4,
'SOW': U4,
'fSOW': I4,
'week': I2,
'leapS': I1,
'valid': X1,
'tAcc': U4
},
'NAV-TIMEGAL': {
'iTOW': U4,
'galTow': U4,
'fGalTow': I4,
'galWno': I2,
'leapS': I1,
'valid': X1,
'tAcc': U4
},
'NAV-TIMEGLO': {
'iTOW': U4,
'TOD': U4,
'fTOD': I4,
'Nt': U2,
'N4': U1,
'valid': X1,
'tAcc': U4
},
'NAV-TIMEGPS': {
'iTOW': U4,
'fTOW': I4,
'week': I2,
'leapS': I1,
'valid': X1,
'tAcc': U4
},
'NAV-TIMELS': {
'iTOW': U4,
'version': U1,
'reserved11': U1,
'reserved12': U1,
'reserved13': U1,
'srcOfCurrLs': U1,
'currLs': I1,
'srcOfLsChange': U1,
'lsChange': I1,
'timeToLsEvent': I4,
'dateOfLsGpsWn': U2,
'dateOfLsGpsDn': U2,
'reserved21': U1,
'reserved22': U1,
'reserved23': U1,
'valid': X1
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
},
'RXM-ALM': {
'svid': U4,
'week': U4,
'group': {
'dwrd': U4
}},
'RXM-EPH': {
'svid': U4,
'how': U4,
'group': {  # TODO multiple repeating groups so how to handle?
'sf1d': U4
},
'group2': {  # TODO multiple repeating groups so how to handle?
'sf2d': U4
},
'group3': {  # TODO multiple repeating groups so how to handle?
'sf3d': U4
}},
'RXM-RAW': {
'iTOW': I4,
'week': I2,
'numCh': U1,
'reserved1': U1,
'group': {
'cpMes': R8,
'prMes': R8,
'doMes': R4,
'sv': U1,
'mesQI': U4,
'cno': I1,
'lli': U1
}},
'RXM-SFRB': {
'chn': U1,
'svid': U1,
'dwrd00': X4,
'dwrd01': X4,
'dwrd02': X4,
'dwrd03': X4,
'dwrd04': X4,
'dwrd05': X4,
'dwrd06': X4,
'dwrd07': X4,
'dwrd08': X4,
'dwrd09': X4
},
'RXM-SVSI': {
'iTOW': I4,
'week': I2,
'numVis': U1,
'numCh': U1,
'group': {
'svid': U1,
'svFlag': X1,
'azim': I2,
'elev': I1,
'age': X1
}},
'TIM-SVIN': {
'dur': U4,
'meanX': I4,
'meanY': I4,
'meanZ': I4,
'meanV': U4,
'obs': U4,
'valid': U1,
'active': U1,
'reserved1': U2
},
'TIM-TM2': {
'ch': U1,
'flags': X1,
'count': U2,
'wnR': U2,
'wnF': U2,
'towMsR': U4,
'towSubMsR': U4,
'towMsF': U4,
'towSubMsF': U4,
'accEst': U4
},
'TIM-TP': {
'towMS': U4,
'towSubMS': U4,
'qErr': I4,
'week': U2,
'flags': X1,
'reserved1': U1
},
'TIM-VRFY': {
'itow': I4,
'frac': I4,
'deltaMs': I4,
'deltaNs': I4,
'wno': U2,
'flags': X1,
'reserved1': U1
}
}
