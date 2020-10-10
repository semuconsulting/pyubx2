# pylint: disable=unused-import
'''
UBX Protocol payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _SET_ MESSAGES _TO_ THE RECEIVER

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

@author: semuadmin
'''
from pyubx2.ubxtypes_core import  U1, I1, X1, U2, I2, X2, U4, I4 , X4 , R4 , X6, R8 , C06, C10, C30, C32, CH

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
'CFG-ANT': {
'flags': X2,
'pins': X2
},
'CFG-CFG': {
'clearMask': X4,
'saveMask': X4,
'loadMask': X4,
'devicerMask': X1
},
'CFG-DAT': {
'datumNum': U2
},
'CFG-DAT-USER': {
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
'CFG-ITFM': {
'config': X4,
'config2': X4
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
'CFG-MSG-CUR': {
'msgClass': U1,
'msgID': U1,
'rate': U1
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
'CFG-NVS': {
'clearMask': X4,
'saveMask': X4,
'loadMask': X4,
'deviceMask': X1
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
'group': {  # TODO repeating group but no index so how to handle?
'data': U1
}},
'CFG-RST': {
'navBrMask': X2,
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
'datagroup': {  # TODO repeating group but no index so how to handle?
'data': X4
},
'calibgroup': {  # TODO repeating group but optional and no index so how to handle?
'calibtTag': U4
}},
}
