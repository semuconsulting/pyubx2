# pyubx2 Release Notes

### RELEASE 1.2.40

ENHANCEMENTS:

1. Internal field naming clarified and docstrings updated - no functional changes.

### RELEASE 1.2.39

FIXES:

1. Fix incorrect UBX MGA-GPS-EPH payload definition Fixes [#141](https://github.com/semuconsulting/pyubx2/issues/141)

### RELEASE 1.2.38

CHANGES:

1. Add val2sphp helper method to convert high precision (9dp) coordinate to separate standard and high precision components, as required by some CFG and NAV messages.
1. Add utc2itow helper method to convert utc datetime to GPS week number and time of week.
1. Add getinputmode helper to determinate mode of input UBX message (SET or POLL). Add new UBXReader msgmode of SETPOLL (0x03), which will automatically determine input mode.

### RELEASE 1.2.37

CHANGES:

1. Streamline parsing of NAV messages with high precision attributes (NAV-HPPOSSEC, NAV-HPPOSLLH, NAV-RELPOSNED). High precision attributes will now be prefixed "_HP" in the payload definitions, and their scaled values will be automatically added to the corresponding standard precision attribute. The high precision attribute will be omitted from the parsed message (so, for example, the parsed NAV-RELPOSNED message will no longer include both relPosN and relPosHPN values - relPosN will include the scaled relPosHPN value).
1. Add new configuration database items for F10 SPG 6.0 and F9 L1L5 1.41 firmware:

    "CFG_HW_ANT_ON_SHORT_US": (0x30a3003c, U2),

### RELEASE 1.2.36

CHANGES:

1. Update min pynmeagps and pyrtcm versions.
1. Update pyrtcm streaming test cases.
1. Minor black formatting.
1. Add planar helper method from pynmeagps.

### RELEASE 1.2.35

FIXES:

1. Fix typo in UBX-ESF-INS payload definition Fixes [#133](https://github.com/semuconsulting/pyubx2/issues/133)

### RELEASE 1.2.34

ENHANCEMENTS:

1. Cater for NMEA streams with LF (b"\x0a") rather than CRLF (b"\x0d\x0a") message terminators.
2. Simplify string representation of NOMINAL (undocumented) payload definitions to "<UBX(IDENTITY-NOMINAL, payload="b\x99...")>".

### RELEASE 1.2.33

ENHANCEMENTS: 

1. Add legacy `TpNotLocked` bit flag to TIM-TP definition

### RELEASE 1.2.32

ENHANCEMENTS: 

1. Cater for legacy "BD" (Beidou) NMEA Talker ID.

### RELEASE 1.2.31

ENHANCEMENTS:

1. ESF payload definitions updated for firmware HPS 1.30.

FIXES:

1. Fix thrashing in SocketStream if connection closed.

### RELEASE 1.2.30

ENHANCEMENTS:

1. Added `ubxtypes_decodes.py` containing a series of reference lookup dictionaries for various UBX attributes.

FIXES:

1. Fix MON-RF payload definition [#122](https://github.com/semuconsulting/pyubx2/issues/122). Thanks to @dcrowe for contribution.

### RELEASE 1.2.29

ENHANCEMENTS:

1. Add 'NAVIC' to list of gnssId enumerations - cosmetic only, no functional change.

### RELEASE 1.2.28

ENHANCEMENTS:

1. Add write capability to socket_stream wrapper, allowing clients to write to UBXReader socket stream (`UBXReader.datastream`) as well as read from it.
1. Update constructor arguments and docstrings to clarify API (no functional changes).
1. Min pynmeagps and pyrtcm version dependency updated to 1.0.27 and 1.0.11 respectively.

FIXES:

1. Remove redundant quitonerror keyword argument from RTCMReader._parse_rtcm3()

### RELEASE 1.2.27

CHANGES:

1. Python 3.7 removed from workflows (now end of life)

### RELEASE 1.2.26

ENHANCEMENTS:

1. Add 'parsing' keyword argument option - True = as-is behaviour; False = no parsing (simply output individual binary messages) - thanks to @gabrielecoppi for contribution.
1. sigID added to RXM-SFRBX message definition - thanks to @agagniere for contribution.
1. 9 additional configuration database keys added for NEO-F10T.

### RELEASE 1.2.25

ENHANCEMENTS:

1. CFG-VALSET parsing enhanced to match CFG-VALGET as key value pairs rather than a simple array of bytes:

Before:
```
<UBX(CFG-VALSET, version=0, ram=1, bbr=1, flash=0, action=0, reserved0=0, cfgData_01=1, cfgData_02=0, cfgData_03=82, cfgData_04=64, cfgData_05=128, ...>
```
After:
```
<UBX(CFG-VALSET, version=0, ram=1, bbr=1, flash=0, action=0, reserved0=0, CFG_UART1_BAUDRATE=9600)>
```

### RELEASE 1.2.24

ENHANCEMENTS:

1. 'quitonerror' kwarg added to `UBXReader.parse()`. This is useful e.g. when parsing *.ubx recordings from u-center containing a mixture of GET, SET and POLL message modes (i.e. diagnostic and configuration data in addition to navigation messages). Setting quitonerror to ERR_IGNORE (0) allows you to scan the file for a particular msgmode (e.g. GET) while ignoring other modes.
1. example `ubxfile_ucenter.py` added to illustrate use of quitonerror and msgmode kwargs when iterating *.ubx files.

CHANGES:

1. Bandit code security vulnerability task added to VSCode and GHA workflows

### RELEASE 1.2.23

CHANGES:

1. Minimum dependency version updated for pynmeagps and pyrtcm
1. Minor updates to VSCode task and GitHub actions workflows for pyproject.toml build framework
1. No other functional changes

### RELEASE 1.2.22

CHANGES:

1. `__str__` method enhanced to escape all byte values for clarity e.g. will now return b'\x61\x62\x63' rather than b'abc'
2. `UBXReader.iterate()` method deprecated - use the standard iterator instead e.g. `ubr = UBXReader(**wkargs): for (raw,parse) in ubr: ...`, passing any `quitonerror` or `errorhandler` kwargs to the UBXReader constructor.

### RELEASE 1.2.21

ENHANCEMENTS:

1. Add support for RXM-SPARTN-KEY GET/SET messages.

### RELEASE 1.2.20

FIXES:

1. Add sigId attribute to RXM-RAWX message definition (Fixes #97)

CHANGES:

1. Internal updates for compatibility with pynmeagps>=1.0.18. No functional changes.

### RELEASE 1.2.19

ENHANCEMENTS:

1. New utility methods added:

- `latlon2dms()` - converts decimal lat/lon to degrees, minutes, decimal seconds format e.g. "53°20′45.6″N", "2°32′46.68″W"
- `latlon2dmm()` - converts decimal lat/lon to degrees, decimal minutes format e.g. "53°20.76′N", "2°32.778′W"
- `ecef2llh()` - converts ECEF (X, Y, Z) coordinates to geodetic (lat, lon, height) coordinates
- `llh2ecef()` - converts geodetic (lat, lon, helght) coordinates to ECEF (X, Y, Z) coordinates
- `haversine()` - finds spherical distance in km between two sets of (lat, lon) coordinates


### RELEASE 1.2.18

CHANGES:

1. Min pyrtcm version updated to v1.0.0.
2. Min pynmeagps version updated to v1.0.17.
3. shields.io build status badge URL updated.

No other functional changes.

### RELEASE 1.2.17

ENHANCEMENTS:

1. Handling of legacy CFG-TP5 POLL message enhanced to support alternate payload formats (one with tpIdx parameter, the other without). To specify tpIdx value, use `payload` keyword e.g. `msg = UBXMessage('CFG', 'CFG-TP5', POLL, payload=b'\x01')`.

### RELEASE 1.2.16

ENHANCEMENTS:

1. Further enhancements in support of u-center .ubx log files which include receiver configuration poll response data - including CFG-VALGET poll responses for undocumented Generation 9 configuration database keys. This hopefully resolves the earlier `UBXMessageError: Undefined configuration database key` and `KeyError` errors when attempting to parse u-center .ubx log files.

### RELEASE 1.2.15

ENHANCEMENTS:

1. Add support for u-blox debug and tracking messages (UBX message classes x03, x08 & x0c, in addition to a handful of messages in the MON x0a and SEC x27 classes). These are the message types that are enabled by invoking debug mode in u-center. **NB:** the payload definitions for these classes are not publicly documented - pyubx2 simply parses them to a nominal byte array.

CHANGES:

1. The `gnssdump` CLI utility has now been moved to the `pygnssutils` library and enhanced with additional features.
2. Test cases amended to reflect additional precision output by `pynmeagps` NMEA parser v1.0.15.

### RELEASE 1.2.14

ENHANCEMENTS:

1. Added message definitions for NAV2-SLAS, NAV2-SVIN and NAV2-TIMEQZSS.
2. Modify handling of ESF-MEAS SET messages to use appropriate data group dimension based on values of `calibTtagValid` and `numMeas` bitfields. If `calibTtagValid` is True, `numMeas` is automatically incremented by 1 to cater for the additional appended calibration dataField (`dataType` = 0). See test cases `testESFMEASSET0` and `testESFMEASSET1` in [`/tests/set_specialcases.py`](https://github.com/semuconsulting/pyubx2/blob/master/tests/test_specialcases.py) for illustrations of how this works.

FIXES:

1. Minor amendment to correctly parse X24 bitfields as bytes (applies to ESF-CAL and ESF-MEAS messages).


### RELEASE 1.2.13

ENHANCEMENTS:

1. Message definitions added: `ESF-CAL`, `RXM-MEAS20`, `RXM-MEAS50`, `RXM-MEASC12`, `RXM-MEASD12`.
2. 43 new configuration database keys added, covering outstanding keys from LEA-F9T, MAX-M10S, NEO-D9C, NEO-D9S, NEO-M10S, NEO-M9L, NEO-M9N, NEO-M9V, ZED-F9-LAP, ZED-F9, ZED-F9H, ZED-F9K, ZED-F9P and ZED-F9R. To the best of my knowledge this encompasses all available 9th and 10th generation u-blox GNSS devices as at June 2022.

### RELEASE 1.2.12

ENHANCEMENTS:

1. `NAV-TIMENAVIC` and `NAV2-TIMENAVIC` message definitions and corresponding configuration database keyes (from ZED-F9T) added - thanks to @alinsavix for contribution.

CHANGES:

1. Internal de-duplication of code in `ubxtypes_get.py` between NAV and NAV2 message definitions.
2. Add setup classifier for Python 3.11.

### RELEASE 1.2.11

ENHANCEMENTS:

1. `GNSSStreamer` class at heart of `gnssdump` CLI utility enhanced to allow a variety
of writeable output medium to be used as an external protocol handler for NMEA, UBX
and/or RTCM protocols. Acceptable output media types include Serial, File (text or
binary), socket or Queue. Essentially this means that `gnssdump` can write its output
data to any of these media rather than to sys.stdout (terminal).
2. New example `gnssserver.py` added to `/examples` folder. This utilises the enhanced
`GNSSStreamer` class to implement a simple but fully-functional command-line TCP Socket
Server or NTRIP Server.

### RELEASE 1.2.10

ENHANCEMENTS:

1. Add socket reading capability to `gnssdump` CLI utility.
2. Enhance test coverage of socket reader functionality.

### RELEASE 1.2.9

ENHANCEMENTS:

1. Add capability to read from TCP/UDP socket as well as serial stream. Utilises a SocketStream
utility class to allow sockets to be read using standard stream-like read(bytes) and readline() 
methods.

FIXES:

1. Fix typo in NAV2-SAT message definition (`reserved0` is now U2 rather than I1).

### RELEASE 1.2.8

ENHANCEMENTS:

1. Add support for NAV-PL message type (new to HPG 1.30). Thanks to @ArrEssJay for contribution.

### RELEASE 1.2.7

ENHANCEMENTS:

1. `pyubx2` now capable of fully parsing RTCM3 messages via the `pyrtcm` library (`pyrtcm>=0.2.5`).

CHANGES:

1. Remove support for Python 3.6, now end of life (should still work fine on 3.6 but no longer actively tested on this version)

### RELEASE 1.2.6

ENHANCEMENTS:

1. Parsing of NAV-HPPOSECEF and NAV-HPPOSLLH messages enhanced to render standard and high precision elements as single high precision attributes, in accordance with the interface specification e.g.
```lat = (lat + latHp * 0.01) * 1e-7```
2. Applies to the following attributes: ```lat``` + ```latHp```, ```lon``` + ```lonHp```, ```height``` + ```heightHp```, ```hMSL``` + ```hMSLHp```, ```ecefX``` + ```ecefXHp```, ```ecefY``` + ```ecefYHp```, ```ecefZ``` + ```ecefZHp```.
3. NB: Dimensions in interface specification have been retained i.e. NAV-HPPOSLLH returns height in mm, NAV-HPPOSECEF returns height in cm.
4. Rounding precision for scaled attributes increased to 12 dp from 8 dp.

### RELEASE 1.2.5

FIXES:

1. Fix issue where presence of RTCM3 data in input stream could cause iterator to fail - thanks to @flytrex-vadim for contributions.

ENHANCEMENTS:

1. `UBXReader` can now accommodate any RTCM3 data in the input stream, alongside UBX and/or NMEA data. It can read the RTCM3 message, verify the CRC (if the `validate` flag is set to VALCKSUM), and return a 'stub' `RTCMMessage` object containing the raw (undecoded) payload e.g. `<RTCM3(1005)>`. **NOTE THAT** `pyubx2` does not decode the RTCM3 payload (*other than the message type*) and there are no current plans to add such functionality.

### RELEASE 1.2.4

ENHANCEMENTS:

1. By popular request, **`UBXReader` now optionally streams NMEA data (via the companion `pynmeagps` library)** in addition to UBX. The `UBXReader.read()` method has been internally refactored to allow for configurable protocol filtering and error handling.
1. New CLI utility `gnssdump` added. This leverages the new `UBXReader.read()` functionality to parse both NMEA and UBX data from any data stream (including Serial and File) to the terminal or to designated NMEA and/or UBX protocol handlers. The utility implements a new `GNSSStreamer` class which may also be invoked within application code (see examples).  `gnssdump` renders the older `ubxdump` and `nmeadump` CLI utilities obsolete and these will be removed in future versions. `gnssdump` requires the `pyserial` library in addition to `pyubx2` and `pynmeagps` (these will be installed automatically via pip).
4. A new helper method `hextable()` has been added to `ubxhelpers.py` which formats raw (binary) data into tabular hexadecimal format, similar to that used in most hex editors.


### RELEASE 1.2.3

ENHANCEMENTS:

1. Following UBX message payload definitions added: AID-DATA, AID-ALP, AID-ALPSRV, AID-REQ, MON-SYS, NAV-PVAT, NAV2-EELL, NAV2-PVAT, RXM-ALM, RXM-COR, RXM-EPH, RXM-POSREQ, RXM-QZSSL6, RXM-SFRB, RXM-SPARTN, RXM-SPARTN-KEY, RXM-TM.
2. Several missing configdb keys added - many thanks to cturvey (clive1) for contributions.

### RELEASE 1.2.2

FIXES:

1. ESF-STATUS payload definition corrected.

### RELEASE 1.2.1

FIXES:

1. UTC offset corrected in `iTOW2UTC` helper method.

### RELEASE 1.2.0

ENHANCEMENTS:

1. SIGNIFICANT CHANGE - Scaling factors have now been added to payload definitions, obviating the need to apply manual scaling factors to pyubx2 inputs or outputs. To define a scaled attribute, define the attribute type as a list of [attribute type as string (I1, U2, etc.), scaling factor as float e.g. 1e-7].

**NB:** If you're using the [PyGPSClient](https://github.com/semuconsulting/PyGPSClient) application, this will need to be updated to v1.1.2 or later to accommodate the new scaling factors in pyubx2 v1.2.0

e.g.

BEFORE (no scaling):

```
    "NAV-PVT": {
        ... ,
        "lon": I4,
        "lat": I4,
        ... ,
```

<UBX(NAV-PVT, ... , lon=-21602964, lat=532566912, ...)>

AFTER (scale factor of 1e-7):

```
    "NAV-PVT": {
        ... ,
        "lon": [I4, 0.0000001],
        "lat": [I4, 0.0000001],
        ... ,
```

<UBX(NAV-PVT, ... , lon=-2.1602964, lat=53.2566912, ...)>

FIXES:

1. Various payload fixes and updates (mainly typos): MON-MSGPP, CFG-DAT, CFG-EKF, CFG-NAVX5, CFG-NMEA, CFG-PMS, CFG-PRT, CFG-RST, CFG-TP5, CFG-USB
2. Add support for older message versions: NAV-AOPSTATUS  

### RELEASE 1.1.7

ENHANCEMENTS:

1. Add NAV2 payload definitions.
2. De-duplicate GET and SET CFG message payload definitions, and other minor streamlining.

FIXES:

1. Correct various payload definitions: CFG-ESFALG, NAV-RELPOSNED v0, RXM-PMREQ, RXM-SVSI, SEC-SIGN, TIM-SET.

### RELEASE 1.1.6

ENHANCEMENTS:

FIXES:

1. Add omitted configuration database items to ubxtypes_configdb.py for ZED-F9* and M10-S devices.

### RELEASE 1.1.5

ENHANCEMENTS:

1. Legacy (pre-v1) args removed from UBXReader.parse() - only accepts kwargs now.
2. Minor code and test case rationalisation.

FIXES:

1. Fix bitfield definitions in CFG-PM2 - thanks to contributors.

### RELEASE 1.1.4

ENHANCEMENTS:
1. Performance benchmarking utility `benchmark.py` added to examples.
2. Python 3.10 support added to `setup.py` and GitHub Actions workflow.
3. Minor code clarifications & pylint advisories.

FIXES:
1. Minor fixes to bitfield definitions in CFG-CFG, CFG-PVT and NAV-SOL - thanks to all contributors.

### RELEASE 1.1.3

ENHANCEMENTS:

1. Extend POLL message types to include NAV - thanks for Nerolf05 for contribution.
2. Add bitfield definitions for TIM (timing) GET messages.

FIXES:

1. Fix payload for LOG-FINDTIME SET message (incorrect u-blox documentation) - thanks to qcabrol for contribution.

### RELEASE 1.1.2

ENHANCEMENTS:

1. Add bitfield definitions for ESF External Sensor Fusion, HNR High Rate Navigation and LOG messages.

FIXES:

1. Fix ESF-MEAS parsing with calibTtagValid flag setting (if calibTtagValid = 1, the final dataField contains the calibTtag).
2. Fix NAV-SAT 'flags' bitfield parsing.

### RELEASE 1.1.1

ENHANCEMENTS:

1. Added new optional boolean keyword argument `parsebitfield` to `UBXReader` and `UBXMessage` constructors and `UBXReader.parse()` static method. If True (the default), `pyubx2` parses bitfields (type 'X' attributes) as individual bit flags. If False, bitfields are left as byte sequences (i.e. same behaviour as `pyubx2` <=1.0.16)

### RELEASE 1.1.0

ENHANCEMENTS:

1. New functionality added in `ubxmessage.py` to parse individual bit flags in bitfield ('X' type) attributes, where defined. For example, the NAV-PVT attribute `valid` (X1) is now parsed as four individual bit flags: `validDate` (U1), `validTime` (U1), `fullyResolved` (U1) and `validMag` (U1).

2. CFG, NAV & MON payload definitions updated in `ubxtypes_get.py` and `ubxtypes_set.py` to model bitfield ('X' type) attributes as groups of individual bit flags. Payload definitions for other message categories (MGA, RXM, etc.) will be updated in a subsequent release (contributions welcome).

3. UBX messages can also be created using individual bit flag keywords.

4. **NB:** If you're using the associated graphical client PyGPSClient, this will need to be upgraded to v1.1.0 to accommodate the pyubx2 changes.

### RELEASE 1.0.16

ENHANCEMENTS:

1. Message filter option added to ubxdump command line utility. See README for usage.

2. New payload attribute type "A" added for byte arrays (e.g. MON-SPAN spectrum attribute).

3. For ease of processing and charting, MON-SPAN spectrum attribute now parsed as a single array of integers per Rf block e.g. `spectrum_01[]` rather than as 256 separate integers per Rf block e.g. `spectrum_01_01`, `spectrum_01_02`, etc. 

### RELEASE 1.0.15

ENHANCEMENTS:

1. The ubxdump.py example has been moved into the pyubx2cli module and configured as a setup entry point. It is now available as a simple command line utility. See README for usage.

### RELEASE 1.0.14

ENHANCEMENTS:

1. Additional configuration parameters added for NEO-D9S, ZED-F9K, ZED-F9P & ZED-F9R Receivers:
   CFG_NAVHPG, CFG_PMP, CFG_RTCM, CFG_SFCORE, CFG_SFIMU, CFG_SFODO

### RELEASE 1.0.13

FIXES:

1. CFG-DAT SET payload definition corrected.

### RELEASE 1.0.12

FIXES:

1. Fix CFG-NAVX5 payload definition - thanks to Nerolf05 for contribution.

### RELEASE 1.0.11

FIXES:

1. Fix NAV-RELPOSNED payload definition - thanks to nikitamankovskii for contribution.

### RELEASE 1.0.10

FIXES:

1. Fix typo error in NAV-SBAS payload - thanks to Nerofl05 for contribution.

ENHANCEMENTS:

1. Add msgmode getter method to `ubxmessage.py` -  - thanks to Nerofl05 for contribution.

### RELEASE 1.0.9

ENHANCEMENTS:

1. Add CFG_BDS_USE_PRN_1_TO_5 to list of configuration keyIDs in ubxtypes_configdb.py - thanks to Nerolf05 for contribution.

FIXES:

1. Fix incorrect CFG-TMODE configuration keyIDs in ubxtypes_configdb.py.

### RELEASE 1.0.8

ENHANCEMENTS:

1. Add following GET/SET message types: CFG-ESFALG, CFG-ESFA, CFG-ESFG, CFG-ESFWT, CFG-HNR, CFG-SENIF, CFG-SLAS

FIXES:

1. Fix incorrect HNR-PVT payload definition

### RELEASE 1.0.7

ENHANCEMENTS:

1. Addition CFG-SIGNAL L2 keys added to `ubxtypes_configdb.py` - thanks to horace1024 for contribution.

### RELEASE 1.0.6

ENHANCEMENTS:

1. UBXReader updated to accept **kwargs: 'ubxonly' and 'msgmode'. Will continue to accept *args for backwards compatibility, but these are now deprecated and may be removed in future versions.
2. Minor enhancements to nominal value assignments - floats will now get nominal value of 0.0.

### RELEASE 1.0.5

ENHANCEMENTS:

1. Added additional helper method `get_bits()` to find value of specified (masked) bit(s) in a UBX bitfield ('X') attribute. See docstring for usage.
2. Docstrings updated.

### RELEASE 1.0.4

Some refactoring of static and helper methods. Improved Sphinx-compliant docstrings.

ENHANCEMENTS:

1. Static parse() method moved from UBXMessage to UBXReader. **NB:** If you were invoking parse() indirectly via the `UBXReader.read()` method, the change is transparent. If you were invoking `UBXMessage.parse()` directly, this will need to be changed to `UBXReader.parse()`. **NB:** If you're using PyGPSClient, this will need to be updated to v0.2.27-beta.
2. Static `calc_checksum()` and `isvalid_checksum()` methods moved from UBXMessage to ubxhelpers.py as stand-alone methods. 
3. Minor enhancements to mixed data stream validation and exception reporting.
4. Docstrings updated for better sphinx-apidoc compliance.

### RELEASE 1.0.3

FIXES:

1. Fixed bug in UBXReader.read() which cause looping with certain mixed protocol streams.

### RELEASE 1.0.2

Code streamlining.

1. De-duplicate CFG-MSG definitions in ubxtypes_core.py. Definitions UBX_CONFIG_CATEGORIES & UBX_CONFIG_MESSAGES
are now incorporated into UBX_CLASSES & UBX_MSGIDS. NB: PyGPSClient GUI will require update to v0.2.23.

### RELEASE 1.0.1

1. Update development status to Production/Stable.

### RELEASE 1.0.0

Marked to major version 1.0.0.
