# pyubx2 Release Notes

### RELEASE 1.0.16

ENHANCEMENTS:

1. Message filter option added to ubxdump command line utility. See README for usage.

2. MON-SPAN spectrum attribute now parsed as a single array of integers `spectrumRf`rather than as 256 separate integers `spectrum_01_01`, `spectrum_01_02`etc. for ease of processing and charting.

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
