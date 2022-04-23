# pyubx2 Release Notes

### RELEASE CANDIDATE 1.2.7

ENHANCEMENTS:

1. `pyubx2` now capable of fully parsing RTCM3 messages via the `pyrtcm` library.

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
