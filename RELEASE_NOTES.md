# pyubx2 Release Notes

### RELEASE 0.3.3-beta

ENHANCEMENTS:

1. Add CFG-MSGOUT-RTCM configuration database keys - thanks to lyngklip for contribution.

### RELEASE 0.3.2-beta

Mainly validation and error message enhancements. Switch from Travis CI to Github Actions workflow.

ENHANCEMENTS:

1. Validation and error messaging enhanced for 'special case' message types which have multiple payload definitions (CFG-NMEA, RXM-PMP, RXM-RLM, ESF-MEAS). Will now raise `UBXMessageError` if message constructor does not contain the keyword(s) necessary to determine which payload definition to use (e.g. `version`, `type`, `flags` or the entire `payload`).

### RELEASE 0.3.1-beta

ENHANCEMENTS:

1. Further Generation 9 enhancements.
2. Support for following G9 message types added:
	CFG-DGNSS,
	CFG-SPT,
	CFG-TMODE3,
	ESF-MEAS,
	MON-HW3,
	MON-RF,
	MON-SPT,
	NAV-ATT,
	RXM-PMP (2 versions),
	RXM-RLM (2 versions)

3. Repeating group processing enhanced to cater for fixed length and nested groups - some existing payload definitions have been refactored using the new structures (repeating elements will now use suffix `_01`, `_02` etc.)
	MON-MSGPP,
	MON-RXBUF,
	MON-SPAN,
	MON-TXBUF

4. ubxmessage.py refactored per pylint recommendations.
5. Some generic static methods moved from `ubxmessage.py` to new `ubxhelpers.py` module:
`itow2utc()`, `gpsfix2str()`, `dop2str()`, `gnss2str()`, `key_from_val()`

FIXES:

1. Alternate versions of RXM-PMREQ payload now supported.

---

### RELEASE v0.3.0-beta

ENHANCEMENTS:

1. Significant release adding support for UBX Generation 9 configuration interface and message types, and adding several Generation 8 message types omitted from earlier versions.
2. Add support for following message types:
    CFG-VALSET,
    CFG-VALDEL,
    CFG-VALGET,
    ESF-ALG,
    ESF-INS,
    ESF-MEAS,
    ESF-RAW,
    HNR-ATT,
    HNR-INS,
    HNR-PVT,
    NAV-EELL,
    NAV-HPPOSECEF,
    NAV-HPPOSLLH (updated for G9),
    NAV-NMI,
    NAV-RELPOSNED,
    NAV-SLAS,
    NAV-SVIN,
    NAV-TIMEQZSS
3. New G9 configuration database key definition module: `ubxtypes_configdb.py`
4. New UBXMessage static methods in UBXessage for G9 configuration interface:
    `cfgname2key()`,
    `cfgkey2name()`,
    `config_set()`,
    `config_del()`,
    `config_poll()`

5. UBXMessage.py code streamlined and de-duplicated.
6. `/examples/ufxcfgval.py` added to illustrate use of CFG-VAL message types.

FIXES:

1. NAV-ODO payload definition corrected (`reserved0` is now U3)
2. NAV-ORB attribute `numCh` amended to `numSv` as per spec

---

### RELEASE v0.2.9-beta

ENHANCEMENTS:

1. CFG-VALGET, CFG-VALDEL and CFG-VALSET message types added from NEO9 protocol. Test coverage extended accordingly.

---

### RELEASE v0.2.8-beta

FIXES:

1. CFG-PRT payload updated to G8 format (with portID). UBXStreamer example updated accordingly.

---

### RELEASE v0.2.7-beta

FIXES:

1. Fix MGA message generation and add test cases for MGA-GPS-EPH and MGA-GPS-ALM messages created using u-blox AssistNow utility.

---

### RELEASE v0.2.6-beta

FIXES:

1.AID-EPH GET and SET payload definition corrected - thanks to Ts Ahmed for contribution.

---

### RELEASE v0.2.5-beta

ENHANCEMENTS:

1. Project formatted using black
2. Setup flagged to beta
3. No other functional changes

---

### RELEASE v0.2.4-alpha

FIXES:

1. Legacy CFG-NMEA parsing corrected and test coverage enhanced
2. MGA message parsing corrected and test coverage enhanced
3. `repr()` enhanced to reflect principle: `eval(repr(obj)) = obj`
4. UBXMessage objects are now immutable after initialisation

---

### RELEASE v0.2.3-alpha

ENHANCEMENTS:

1. Updated to support Travis and Coveralls CI. No changes in functionality.

---

### RELEASE v0.2.2-alpha

FIXES:

1. MON-VER GET payload definition updated to protocol >=15 version

---

### RELEASE v0.2.1-alpha

ENHANCEMENTS:

1. UBXMessage code substantially streamlined and refactored.
2. Iterator added to UBXReader with option to tolerate or reject mixed (UBX and non-UBX) data streams. `ubxfile.py` example implementation added.
3. Error messaging enhanced.
4. UBX payload definitions now accommodate earlier versions of the CFG-NMEA message for backwards compatibility.

