pyubx2
=======

[Current Status](#currentstatus) |
[Installation](#installation) |
[Message Categories](#msgcat) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Configuration Interface](#configinterface) |
[Utilities](#utilities) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Troubleshooting](#troubleshoot) |
[Command Line Utility](#cli) |
[Graphical Client](#gui) |
[Author & License](#author)

`pyubx2` is an original Python 3 parser for the UBX &copy; protocol. UBX is a proprietary binary protocol implemented on u-blox &trade; GNSS receiver modules. `pyubx2` can also parse NMEA 0183 &copy; and RTCM3 &copy; protocols via the underlying [`pynmeagps`](https://github.com/semuconsulting/pynmeagps) and [`pyrtcm`](https://github.com/semuconsulting/pyrtcm) packages from the same author - hence it covers all the protocols that u-blox GNSS receivers are capable of outputting.

The `pyubx2` homepage is located at [https://github.com/semuconsulting/pyubx2](https://github.com/semuconsulting/pyubx2).

This is an independent project and we have no affiliation whatsoever with u-blox.

## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pyubx2)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyubx2)
![Build](https://img.shields.io/github/actions/workflow/status/semuconsulting/pyubx2/main.yml?branch=master)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyubx2)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyubx2)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyubx2)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyubx2.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyubx2)

The library implements a comprehensive set of inbound (SET/POLL) and outbound (GET) messages for all current u-blox GPS/GNSS devices, but is readily [extensible](#extensibility). Refer to `UBX_MSGIDS` in [ubxtypes_core.py](https://github.com/semuconsulting/pyubx2/blob/master/src/pyubx2/ubxtypes_core.py) for the complete dictionary of messages currently supported. UBX protocol information sourced from public domain u-blox Interface Specifications © 2013-2025, u-blox AG.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyubx2/](https://www.semuconsulting.com/pyubx2/).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyubx2/blob/master/CONTRIBUTING.md). Feel free to discuss any proposed changes beforehand in the [Discussion Channel](https://github.com/semuconsulting/pyubx2/discussions/categories/ideas).

[Bug reports](https://github.com/semuconsulting/pyubx2/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyubx2/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pyubx2 Discussions](https://github.com/semuconsulting/pyubx2/discussions) channels.

---
## <a name="installation">Installation</a>

![Python version](https://img.shields.io/pypi/pyversions/pyubx2.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyubx2.svg?style=flat)](https://pypi.org/project/pyubx2/)
[![PyPI downloads](https://github.com/semuconsulting/pygpsclient/blob/master/images/clickpy_icon.svg?raw=true)](https://clickpy.clickhouse.com/dashboard/pyubx2)

`pyubx2` is compatible with Python 3.9 - 3.13. In the following, `python3` & `pip` refer to the Python 3 executables. You may need to substitute `python` for `python3`, depending on your particular environment (*on Windows it's generally `python`*).

The recommended way to install the latest version of `pyubx2` is with [pip](http://pypi.python.org/pypi/pip/):

```shell
python3 -m pip install --upgrade pyubx2
```

If required, `pyubx2` can also be installed into a virtual environment, e.g.:

```shell
python3 -m venv env
source env/bin/activate # (or env\Scripts\activate on Windows)
python3 -m pip install --upgrade pyubx2
```

For [Conda](https://docs.conda.io/en/latest/) users, `pyubx2` is also available from [conda forge](https://github.com/conda-forge/pyubx2-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyubx2/badges/version.svg)](https://anaconda.org/conda-forge/pyubx2)
[![Anaconda-Server Badge](https://img.shields.io/conda/dn/conda-forge/pyubx2)](https://anaconda.org/conda-forge/pyubx2)

```shell
conda install -c conda-forge pyubx2
```

---
## <a name="msgcat">UBX Message Categories - GET, SET, POLL</a>

`pyubx2` divides UBX messages into three categories, signified by the `mode` or `msgmode` parameter.

| mode        | description                              | defined in         |
|-------------|------------------------------------------|--------------------|
| GET (0x00)  | output *from* the receiver (the default) | `ubxtypes_get.py`  |
| SET (0x01)  | command input *to* the receiver          | `ubxtypes_set.py`  |
| POLL (0x02) | query input *to* the receiver            | `ubxtypes_poll.py` |

If you're simply streaming and/or parsing the *output* of a UBX receiver, the mode is implicitly GET. If you want to create
or parse an *input* (command or query) message, you must set the mode parameter to SET or POLL. If the parser mode is set to
0x03 (SETPOLL), `pyubx2` will automatically determine the applicable input mode (SET or POLL) based on the message payload.

---
## <a name="reading">Reading (Streaming)</a>

```
class pyubx2.ubxreader.UBXReader(stream, *args, **kwargs)
```

You can create a `UBXReader` object by calling the constructor with an active stream object. 
The stream object can be any viable data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper). `pyubx2` implements an internal `SocketWrapper` class to allow sockets to be read in the same way as other streams (see example below).

Individual input UBX, NMEA or RTCM3 messages can then be read using the `UBXReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `UBXMessage`, `NMEAMessage` or `RTCMMessage` object, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `UBXReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:

* `protfilter`: `NMEA_PROTOCOL` (1), `UBX_PROTOCOL` (2), `RTCM3_PROTOCOL` (4). Can be OR'd; default is `NMEA_PROTOCOL | UBX_PROTOCOL | RTCM3_PROTOCOL` (7)
* `quitonerror`: `ERR_IGNORE` (0) = ignore errors, `ERR_LOG` (1) = log errors and continue (default), `ERR_RAISE` (2) = (re)raise errors and terminate
* `validate`: `VALCKSUM` (0x01) = validate checksum (default), `VALNONE` (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields ('X' type properties) as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2), `SETPOLL` (3) = automatically determine SET or POLL input mode

Example -  Serial input. This example will output both UBX and NMEA messages but not RTCM3:
```python
from serial import Serial
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL
with Serial('/dev/ttyACM0', 38400, timeout=3) as stream:
  ubr = UBXReader(stream, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL)
  raw_data, parsed_data = ubr.read()
  if parsed_data is not None:
    print(parsed_data)
```

Example - File input (using iterator). This will only output UBX data:
```python
from pyubx2 import UBXReader, UBX_PROTOCOL
with open('ubxdata.bin', 'rb') as stream:
  ubr = UBXReader(stream, protfilter=UBX_PROTOCOL)
  for raw_data, parsed_data in ubr:
    print(parsed_data)
```

Example - Socket input (using iterator). This will output UBX, NMEA and RTCM3 data:
```python
import socket
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL, RTCM3_PROTOCOL
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
  stream.connect(("localhost", 50007))
  ubr = UBXReader(stream, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL | RTCM3_PROTOCOL)
  for raw_data, parsed_data in ubr:
    print(parsed_data)
```

---
## <a name="parsing">Parsing</a>

You can parse individual UBX messages using the static `UBXReader.parse(data)` function, which takes a bytes array containing a binary UBX message and returns a `UBXMessage` object.

**NB:** Once instantiated, a `UBXMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2), `SETPOLL` (3) = automatically determine SET or POLL input mode

Example - output (GET) message:
```python
from pyubx2 import UBXReader
msg = UBXReader.parse(b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38')
print(msg)
msg = UBXReader.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
print(msg)
```
```
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
<UBX(NAV-VELNED, iTOW=16:01:48, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=1.28387, sAcc=65, cAcc=80.5272)>
```

Example - input (SET) message:
```python
from pyubx2 import UBXReader, SET
msg = UBXReader.parse(b"\xb5b\x13\x40\x14\x00\x01\x00\x01\x02\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x93\xc8", msgmode=SET)
print(msg)
```
```
<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>
```

The `UBXMessage` object exposes different public attributes depending on its message type or 'identity',
e.g. the `NAV-POSLLH` message has the following attributes:

```python
print(msg)
print(msg.identity)
print(msg.lat, msg.lon)
print(msg.hMSL/10**3)
```
```
<UBX(NAV-POSLLH, iTOW=16:01:54, lon=-2.1601284, lat=52.6206345, height=86327, hMSL=37844, hAcc=38885, vAcc=16557)>
'NAV-POSLLH'
(52.6206345, -2.1601284)
37.844
```

The `payload` attribute always contains the raw payload as bytes. Attributes within repeating groups are parsed with a two-digit suffix (svid_01, svid_02, etc.).

**Tip:** To iterate through a repeating group of attributes (*e.g. svid*), the following construct can be used:

```python
vals = [] # list of svid values from repeating group
for i in range(msg.numSV): # numSV = size of repeating group
    svid = getattr(msg, f"svid_{i+1:02d}")
    vals.append(svid)
print(vals)
```

If the input message class / id is unrecognised (i.e. not publicly documented by u-blox), `pyubx2` will parse the message to a nominal payload definition and append the term 'NOMINAL' to the message identity.

---
## <a name="generating">Generating</a>

(see [below](#configinterface) for special methods relating to the UBX configuration interface)

```
class pyubx2.ubxmessage.UBXMessage(ubxClass, ubxID, mode: int, **kwargs)
```

You can create a `UBXMessage` object by calling the constructor with the following parameters:
1. message class (must be a valid class from `pyubx2.UBX_CLASSES`)
2. message id (must be a valid id from `pyubx2.UBX_MSGIDS`)
3. mode (0=GET, 1=SET, 2=POLL)
4. (optional) a series of keyword parameters representing the message payload
5. (optional) `parsebitfield` keyword - 1 = define bitfields as individual bits (default), 0 = define bitfields as byte sequences

The 'message class' and 'message id' parameters may be passed as lookup strings, integers or bytes.

The message payload can be defined via keyword arguments in one of three ways:
1. A single keyword argument of `payload` containing the full payload as a sequence of bytes (any other keyword arguments will be ignored). **NB** the `payload` keyword argument *must* be used for message types which have a 'variable by size' repeating group.
2. One or more keyword arguments corresponding to individual message attributes. Any attributes not explicitly provided as keyword arguments will be set to a nominal value according to their type.
3. If no keyword arguments are passed, the payload is assumed to be null.

Example - to generate a CFG-MSG command (*msgClass 0x06, msgID 0x01*) which sets the NAV-STATUS (*msgClass 0x01, msgID 0x03*) outbound message rate to 1 on the UART1 port, any of the following constructor formats will work:

A. Pass entire payload as bytes:
```python
from pyubx2 import UBXMessage, SET
msg1 = UBXMessage(b'\x06', b'\x01', SET, payload=b'\x01\x03\x00\x01\x00\x00\x00\x00')
print(msg1)
```
```
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```
B. Pass individual attributes as keyword arguments:
```python
from pyubx2 import UBXMessage, SET
msg2 = UBXMessage(0x06, 0x01, SET, msgClass=0x01, msgID=0x03, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0)
print(msg2)
```
```
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```
C. Pass selected attribute as keyword argument; the rest will be set to nominal values (in this case 0):
```python
from pyubx2 import UBXMessage, SET
msg3 = UBXMessage('CFG','CFG-MSG', SET, msgClass=0x01, msgID=0x03, rateUART1=1)
print(msg3)
```
```
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```

---
## <a name="serializing">Serializing</a>

The `UBXMessage` class implements a `serialize()` method to convert a `UBXMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` command which sets the NMEA GLL (*msgClass 0xf0, msgID 0x01*) message rate to 1 on the receiver's UART1 and USB ports:

```python
from serial import Serial
from pyubx2 import UBXMessage, SET
serialOut = Serial('COM7', 38400, timeout=5)
msg = UBXMessage('CFG','CFG-MSG', SET, msgClass=0xf0, msgID=0x01, rateUART1=1, rateUSB=1)
print(msg)
output = msg.serialize()
print(output)
serialOut.write(output)
```
```
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=1, rateSPI=0, reserved=0)>
b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x00\x01\x00\x00\x022'
```

---
## <a name="configinterface">Configuration Interface</a>

**CFG-VALSET, CFG-VALDEL and CFG-VALGET message types**

Generation 9 of the UBX protocol (*23.01 or greater, e.g. NEO-M9N, ZED-F9P*) introduced the concept of a device configuration interface with configurable parameters being set or unset (del) in the designated memory layer(s) via the CFG-VALSET and CFG-VALDEL message types, or queried via the CFG-VALGET message type. *Legacy CFG configuration message types continue to be supported but are now deprecated on Generation 9+ devices*.

Optionally, batches of CFG-VALSET and CFG-VALDEL messages can be applied transactionally, with the combined configuration only being committed at the end of the transaction.

Individual configuration parameters are designated by keys, which may be in string (keyname) or hexadecimal integer (keyID) format. Keynames and their corresponding hexadecimal keyIDs and data types are defined in [ubxtypes_configdb.py](https://github.com/semuconsulting/pyubx2/blob/master/src/pyubx2/ubxtypes_configdb.py) as `UBX_CONFIG_DATABASE`. Two helper methods are available to convert keyname to keyID and vice versa - `cfgname2key()` and `cfgkey2name()`.

Dedicated static methods are provided to create these message types - `UBXMessage.config_set()`, `UBXMessage.config_del()` and `UBXMessage.config_poll()`. The following examples assume an output serial stream has been created as `serialOut`.

**UBXMessage.config_set() (CFG-VALSET)**

Sets up to 64 parameters in the designated memory layer(s).

Parameters:

1. layers - `SET_LAYER_RAM` (1) = Volatile RAM, `SET_LAYER_BBR` (2) = Battery-Backed RAM (BBR), `SET_LAYER_FLASH` (4) = External Flash (may be OR'd)
1. transaction - `TXN_NONE` (0) = None, `TXN_START` (1) = Start, `TXN_ONGOING` (2) = Ongoing, `TXN_COMMIT` (3) = Commit
1. cfgData - an array of up to 64 (key, value) tuples. Keys can be in either 
keyID (int) or keyname (str) format

```python
from pyubx2 import UBXMessage, SET_LAYER_RAM, TXN_NONE
layers = SET_LAYER_RAM
transaction = TXN_NONE
cfgData = [("CFG_UART1_BAUDRATE", 9600), (0x40520001, 115200)]
msg = UBXMessage.config_set(layers, transaction, cfgData)
print(msg)
serialOut.write(msg.serialize())
```
```
<UBX(CFG-VALSET, version=0, ram=1, bbr=0, flash=0, action=0, reserved0=0, cfgData_01=1, cfgData_02=0 ...)>
```

**UBXMessage.config_del() (CFG-VALDEL)**

Unsets (deletes) up to 64 parameter settings in the designated non-volatile memory layer(s).

Parameters:

1. layers - `SET_LAYER_BBR` (2) = Battery-Backed RAM (BBR), `SET_LAYER_FLASH` (4) = External Flash (may be OR'd)
1. transaction - `TXN_NONE` (0) = None, `TXN_START` (1) = Start, `TXN_ONGOING` (2) = Ongoing, `TXN_COMMIT` (3) = Commit
1. keys - an array of up to 64 keys in either keyID (int) or keyname (str) format

```python
from pyubx2 import UBXMessage, SET_LAYER_FLASH, TXN_NONE
layers = SET_LAYER_FLASH
transaction = TXN_NONE
keys = ["CFG_UART1_BAUDRATE", 0x40520001]
msg = UBXMessage.config_del(layers, transaction, keys)
print(msg)
serialOut.write(msg.serialize())
```
```
<UBX(CFG-VALDEL, version=0, bbr=0, flash=1, action=0, reserved0=0, keys_01=1079115777, keys_02=1079181313)>
```

**UBXMessage.config_poll() (CFG-VALGET)**

Polls up to 64 parameters from the designated memory layer.

Parameters:

1. layer - `POLL_LAYER_RAM` (0) = Volatile RAM, `POLL_LAYER_BBR` (1) = Battery-Backed RAM (BBR), `POLL_LAYER_FLASH` (2) = External Flash, `POLL_LAYER_DEFAULT` (7) = Default (readonly)
1. position - unsigned integer representing number of items to be skipped before returning result
(used when number of matches for an individual query exceeds 64)
1. keys - an array of up to 64 keys in either keyID (int) or keyname (str) format. keyIDs can use
wildcards - see example below and UBX device interface specification for details.

```python
from pyubx2 import UBXMessage,  POLL_LAYER_BBR
layer = POLL_LAYER_BBR
position = 0
keys = ["CFG_UART1_BAUDRATE", 0x40520001]
msg = UBXMessage.config_poll(layer, position, keys)
print(msg)
serialOut.write(msg.serialize())
```
```
<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=1079115777, keys_02=1079181313)>
```

Wild card queries can be performed by setting bits 0..15 of the keyID to `0xffff` e.g. to retrieve all CFG_MSGOUT parameters (keyID `0x2091*`) :

```python
from pyubx2 import UBXMessage, POLL_LAYER_BBR
layer = POLL_LAYER_BBR
position = 0 # retrieve first 64 results
keys = [0x2091ffff]
msg1of3 = UBXMessage.config_poll(layer, position, keys)
print(msg1of3)
serialOut.write(msg1of3.serialize())
position = 64 # retrieve next 64 results
msg2of3 = UBXMessage.config_poll(layer, position, keys)
print(msg2of3)
serialOut.write(msg2of3.serialize())
position = 128 # retrieve next 64 results
msg3of3 = UBXMessage.config_poll(layer, position, keys)
print(msg3of3)
serialOut.write(msg3of3.serialize())
```
```
<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=546439167)>
<UBX(CFG-VALGET, version=0, layer=1, position=64, keys_01=546439167)>
<UBX(CFG-VALGET, version=0, layer=1, position=128, keys_01=546439167)>
```

---
## <a name="utilities">Utility Methods</a>
 
 `pyubx2` provides the following utility methods (via the `pynmeagps` library):

 - `latlon2dms` - converts decimal lat/lon to degrees, minutes, decimal seconds format e.g. "53°20′45.6″N", "2°32′46.68″W"
 - `latlon2dmm` - converts decimal lat/lon to degrees, decimal minutes format e.g. "53°20.76′N", "2°32.778′W"
 - `ecef2llh` - converts ECEF (X, Y, Z) coordinates to geodetic (lat, lon, ellipsoidal height) coordinates
 - `llh2ecef` - converts geodetic (lat, lon, ellipsoidal height) coordinates to ECEF (X, Y, Z) coordinates
 - `haversine` - finds spherical distance in km between two sets of (lat, lon) coordinates
 - `bearing` - finds bearing in degrees between two sets of (lat, lon) coordinates
 - `cel2cart` - converts celestial coordinates (elevation, azimuth) to cartesian coordinations (X,Y)

See [Sphinx documentation](https://www.semuconsulting.com/pyubx2/pyubx2.html#module-pyubx2.ubxhelpers) for details.

---
## <a name="examples">Examples</a>

The following command line examples can be found in the `\examples` folder:

1. `ubxoptions.py` illustrates the various options available for parsing and constructing UBX messages.
1. `ubxpoller.py` illustrates how to read, write and display UBX messages 'concurrently' using threads and queues. This represents a useful generic pattern for many end user applications.
1. `ubxsetrates.py` illustrates how to use legacy configuration messages (CFG-MSG) to set navigation message rates.
1. `ubxconfigdb.py` illustrates how to invoke the Generation 9 configuration database interface via CFG-VALSET, CF-VALDEL and CFG-VALGET messages.
1. `ubxfactoryreset.py` illustrates how to send a factory reset (CFG-CFG) command.
1. `ubxfile.py` illustrates how to implement a binary file reader for UBX messages using `UBXReader` iterator functionality. 
1. `ubxsocket.py` illustrates how to implement a TCP Socket reader for UBX messages using `UBXReader` iterator functionality. Can be used in conjunction with the `tcpserver_threaded.py` socket server test harness.
1. `gpxtracker.py` illustrates a simple tool to convert a binary UBX data dump to a `*.gpx` track file.
1. `ubxserver.py` in the \examples\webserver folder illustrates a simple HTTP web server wrapper around `pyubx2.UBXreader`; it presents data from selected UBX messages as a web page http://localhost:8080 or a RESTful API http://localhost:8080/gps.
1. `mon_span_spectrum.py` illustrates how to use `pyubx2` and `matplotlib` to plot a spectrum analysis graph from a UBX MON-SPAN message.
1. `utilities.py` illustrates how to use various `pyubx2` utility methods.
1. `benchmark.py` provides a simple performance benchmarking tool for the `pyubx2` parser.

---
## <a name="extensibility">Extensibility</a>

The UBX protocol is principally defined in the modules `ubxtypes_*.py` as a series of dictionaries. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid types (I1, U2, X4, etc.)
3. if the attribute is scaled, attribute type is list of [attribute type as string (I1, U2, etc.), scaling factor as float] e.g. {"lat": [I4, 1e-7]}
4. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numCh'
     c. an 'X' attribute type ('X1', 'X2', 'X4', etc) representing a group of individual bit flags
     d. 'None' for a 'variable by size' repeating group. Only one such group is permitted per payload and it must be at the end.
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix (svid_01, svid_02, etc.). Nested repeating groups are supported. See CFG-VALGET, MON-SPAN, NAV-PVT, NAV-SAT and RXM-RLM by way of examples.

In most cases, a UBX message's content (payload) is uniquely defined by its class, id and mode; accommodating the message simply requires the addition of an appropriate dictionary entry to the relevant `ubxtypes_*.py` module(s). However, there are a handful of message types which have multiple possible payload variants for the same class, id and mode. These exceptional message types are handled in `ubxvariants.py`, to which any additional variants should be added.

---
## <a name="troubleshoot">Troubleshooting</a>

#### 1. `Unknown Protocol` errors.
These are usually due to corruption of the serial data stream, either because the serial port configuration is incorrect (baud rate, parity, etc.) or because another process is attempting to use the same data stream. 
- Check that your UBX receiver UART1 or UART2 ports are configured for the desired baud rate - remember the factory default is 38400 (*not* 9600).
- Check that no other process is attempting to use the same serial port, including daemon processes like gpsd.
#### 2. `Serial Permission` errors. 
These are usually caused by inadequate user privileges or contention with another process. 
- On Linux platforms, check that the user is a member of the `tty` and/or `dialout` groups.
- Check that no other process is attempting to use the same serial port, including daemon processes like gpsd.
#### 3. `UnicodeDecode` errors.
- If reading UBX data from a log file, check that the file.open() procedure is using the `rb` (read binary) setting e.g.
`stream = open('ubxdatalog.log', 'rb')`.
#### 4. Spurious `CFG-VALGET`, `DBG`, `TRK`, `TUN` and `SEC` data in *.ubx files recorded in u-center.
By default, u-center 21.09 records a series of configuration messages (CFG-VALGET) containing undocumented configuration database keys. In addition, clicking the 'debug' option results in a large number of undocumented DBG, TRK, TUN and SEC message classes. As of version v1.2.15, `pyubx2` is capable of parsing these undocumented message classes (to a nominal payload definition), but they are really only of relevance to u-blox technical support. If you are *not* intending to send the recordings to u-blox;
- When recording GNSS output data in u-center, select 'No' when prompted to 'Add Receiver Configuration' to the recording, and avoid the 'debug' option.

---
## <a name="cli">Command Line Utility</a>

A command line utility `gnssdump` is available via the `pygnssutils` package. This is capable of reading and parsing NMEA, UBX and RTCM3 data from a variety of input sources (e.g. serial, socket and file) and outputting to a variety of media in a variety of formats. See https://github.com/semuconsulting/pygnssutils for further details.

To install `pygnssutils`:
```
python3 -m pip install --upgrade pygnssutils
```

For help with the `gnssdump` utility, type:
```
gnssdump -h
```

---
## <a name="gui">Graphical Client</a>

A python/tkinter graphical GPS client which supports NMEA, UBX and RTCM3 protocols (via pynmeagps, pyubx2 and pyrtcm respectively) is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyubx2.svg)

`pyubx2` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the utility useful, please consider sponsoring the project with the price of a coffee...

[![Sponsor](https://github.com/semuconsulting/pyubx2/blob/master/images/sponsor.png?raw=true)](https://buymeacoffee.com/semuconsulting)

[![Freedom for Ukraine](https://github.com/semuadmin/sandpit/blob/main/src/sandpit/resources/ukraine200.jpg?raw=true)](https://u24.gov.ua/)
