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
[Examples](#examples) |
[Extensibility](#extensibility) |
[Command Line Utility](#cli) |
[Troubleshooting](#troubleshoot) |
[Graphical Client](#gui) |
[Author & License](#author)

`pyubx2` is an original Python 3 parser for the UBX &copy; protocol. UBX is a proprietary binary protocol implemented on u-blox &trade; GNSS/GPS receiver modules.

The `pyubx2` homepage is located at [https://github.com/semuconsulting/pyubx2](https://github.com/semuconsulting/pyubx2).

This is an independent project and we have no affiliation whatsoever with u-blox.

**FYI** There are companion libraries which handle standard NMEA 0183 &copy; and RTCM3 &copy; GNSS/GPS messages.

- [pynmeagps](http://github.com/semuconsulting/pynmeagps)
- [pyrtcm](http://github.com/semuconsulting/pyrtcm)


## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pyubx2)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyubx2)
![Build](https://img.shields.io/github/workflow/status/semuconsulting/pyubx2/pyubx2)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyubx2)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyubx2)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyubx2)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyubx2.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyubx2)

At time of writing the library implements a comprehensive set of inbound (SET/POLL) and outbound (GET) messages for
u-blox GPS/GNSS devices from generation 6 through generation 10 [(NEO-M6*, NEO-M7*, NEO-M8*, NEO-M9*, NEO-D9*, RCB-F9*, ZED-F9*, MAX-M10S, etc.)](https://www.u-blox.com/en/positioning-chips-and-modules), but is readily [extensible](#extensibility). Refer to `UBX_MSGIDS` in [ubxtypes_core.py](https://github.com/semuconsulting/pyubx2/blob/master/pyubx2/ubxtypes_core.py) for the complete dictionary of messages currently supported. UBX protocol information sourced from u-blox Interface Specifications © 2013-2021, u-blox AG.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyubx2](https://www.semuconsulting.com/pyubx2).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyubx2/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyubx2/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyubx2/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided.

### New in v1.2.9

1. Ability to read from socket as well as serial or file datastream.

---
## <a name="installation">Installation</a>

`pyubx2` is compatible with Python >=3.7 and has no third-party library dependencies.

In the following, `python` & `pip` refer to the Python 3 executables. You may need to type 
`python3` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pyubx2.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyubx2.svg?style=flat)](https://pypi.org/project/pyubx2/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyubx2.svg?style=flat)

The recommended way to install the latest version of `pyubx2` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python -m pip install --upgrade pyubx2
```

If required, `pyubx2` can also be installed into a virtual environment, e.g.:

```shell
python -m pip install --user --upgrade virtualenv
python -m virtualenv env
source env/bin/activate (or env\Scripts\activate on Windows)
(env) python -m pip install --upgrade pyubx2
...
deactivate
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
or parse an *input* (command or query) message, you must set the mode parameter to SET or POLL.

---
## <a name="reading">Reading (Streaming)</a>

```
class pyubx2.ubxreader.UBXReader(stream, *args, **kwargs)
```

You can create a `UBXReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper). `pyubx2` implements an internal `SocketStream` class to allow sockets to be read in the same way as other streams (see example below).

Individual input UBX, NMEA or RTCM3 messages can then be read using the `UBXReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `UBXMessage`, `NMEAMessage` or `RTCMMessage` object, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `UBXReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:

* `protfilter`: 1 = NMEA, 2 = UBX, 4 = RTCM3 (can be OR'd. default is 3 - NMEA & UBX)
* `quitonerror`: 0 = ignore errors, 1 = log errors and continue (default), 2 = (re)raise errors and terminate
* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields ('X' type properties) as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: 0 = GET (default), 1 = SET, 2 = POLL

Example -  Serial input. This example will output both UBX and NMEA messages:
```python
>>> from serial import Serial
>>> from pyubx2 import UBXReader
>>> stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
>>> ubr = UBXReader(stream)
>>> (raw_data, parsed_data) = ubr.read()
>>> print(parsed_data)
```

Example - File input (using iterator). This will only output UBX data:
```python
>>> from pyubx2 import UBXReader
>>> stream = open('ubxdata.bin', 'rb')
>>> ubr = UBXReader(stream, protfilter=2)
>>> for (raw_data, parsed_data) in ubr: print(parsed_data)
...
```

Example - Socket input (using enhanced iterator). This will output UBX, NMEA and RTCM3 data:
```python
>>> import socket
>>> from pyubx2 import UBXReader
>>> stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
>>> stream.connect(("localhost", 50007))
>>> ubr = UBXReader(stream, protfilter=7)
>>> for (raw_data, parsed_data) in ubr.iterate(): print(parsed_data)
...
```

---
## <a name="parsing">Parsing</a>

You can parse individual UBX messages using the static `UBXReader.parse(data)` function, which takes a bytes array containing a binary UBX message and returns a `UBXMessage` object.

**NB:** Once instantiated, a `UBXMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: 0 = GET (default), 1 = SET, 2 = POLL

Example - output (GET) message:
```python
>>> from pyubx2 import UBXReader
>>> msg = UBXReader.parse(b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38')
>>> print(msg)
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
>>> msg = UBXReader.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
>>> print(msg)
<UBX(NAV-VELNED, iTOW=16:01:48, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=1.28387, sAcc=65, cAcc=80.5272)>
```

Example - input (SET) message:
```python
>>> from pyubx2 import UBXReader, SET
>>> msg = UBXReader.parse(b"\xb5b\x13\x40\x14\x00\x01\x00\x01\x02\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04\x93\xc8", msgmode=SET)
>>> print(msg)
<UBX(MGA-INI-POS-LLH, type=1, version=0, reserved0=513, lat=6.7305985, lon=6.7305985, alt=67305985, posAcc=67305985)>
```

The `UBXMessage` object exposes different public attributes depending on its message type or 'identity',
e.g. the `NAV-POSLLH` message has the following attributes:

```python
>>> print(msg)
<UBX(NAV-POSLLH, iTOW=16:01:54, lon=-2.1601284, lat=52.6206345, height=86327, hMSL=37844, hAcc=38885, vAcc=16557)>
>>> msg.identity
'NAV-POSLLH'
>>> msg.lat, msg.lon
(52.6206345, -2.1601284)
>>> msg.hMSL/10**3
37.844
```

Attributes within repeating groups are parsed with a two-digit suffix (svid_01, svid_02, etc.). The `payload` attribute always contains the raw payload as bytes.

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
>>> from pyubx2 import UBXMessage, SET
>>> msg1 = UBXMessage(b'\x06', b'\x01', SET, payload=b'\x01\x03\x00\x01\x00\x00\x00\x00')
>>> print(msg1)
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```
B. Pass individual attributes as keyword arguments:
```python
>>> from pyubx2 import UBXMessage, SET
>>> msg2 = UBXMessage(0x06, 0x01, SET, msgClass=0x01, msgID=0x03, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0)
>>> print(msg2)
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```
C. Pass selected attribute as keyword argument; the rest will be set to nominal values (in this case 0):
```python
>>> from pyubx2 import UBXMessage, SET
>>> msg3 = UBXMessage('CFG','CFG-MSG', SET, msgClass=0x01, msgID=0x03, rateUART1=1)
>>> print(msg3)
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-STATUS, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
```

---
## <a name="serializing">Serializing</a>

The `UBXMessage` class implements a `serialize()` method to convert a `UBXMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` command which sets the NMEA GLL (*msgClass 0xf0, msgID 0x01*) message rate to 1 on the receiver's UART1 and USB ports:

```python
>>> from serial import Serial
>>> serialOut = Serial('COM7', 38400, timeout=5)
>>> from pyubx2 import UBXMessage, SET
>>> msg = UBXMessage('CFG','CFG-MSG', SET, msgClass=0xf0, msgID=0x01, rateUART1=1, rateUSB=1)
>>> print(msg)
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=1, rateSPI=0, reserved=0)>
>>> output = msg.serialize()
>>> output
b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x00\x01\x00\x00\x022'
>>> serialOut.write(output)
```

---
## <a name="configinterface">Configuration Interface</a>

**CFG-VALSET, CFG-VALDEL and CFG-VALGET message types**

Generation 9 of the UBX protocol (*23.01 or greater, e.g. NEO-M9N, ZED-F9P*) introduced the concept of a device configuration interface with configurable parameters being set or unset (del) in the designated memory layer(s) via the CFG-VALSET and CFG-VALDEL message types, or queried via the CFG-VALGET message type. *Legacy CFG configuration message types continue to be supported but are now deprecated on Generation 9+ devices*.

Optionally, batches of CFG-VALSET and CFG-VALDEL messages can be applied transactionally, with the combined configuration only being committed at the end of the transaction.

Individual configuration parameters are designated by keys, which may be in string (keyname) or hexadecimal integer (keyID) format. Keynames and their corresponding hexadecimal keyIDs and data types are defined in [ubxtypes_configdb.py](https://github.com/semuconsulting/pyubx2/blob/master/pyubx2/ubxtypes_configdb.py) as `UBX_CONFIG_DATABASE`. Two helper methods are available to convert keyname to keyID and vice versa - `cfgname2key()` and `cfgkey2name()`.

Dedicated static methods are provided to create these message types - `UBXMessage.config_set()`, `UBXMessage.config_del()` and `UBXMessage.config_poll()`. The following examples assume an output serial stream has been created as `serialOut`.

**UBXMessage.config_set() (CFG-VALSET)**

Sets up to 64 parameters in the designated memory layer(s).

Parameters:

1. layers - 1 = Volatile RAM, 2 = Battery-Backed RAM (BBR), 4 = External Flash (may be OR'd)
1. transaction - 0 = None, 1 = Start, 2 = Ongoing, 3 = Commit
1. cfgData - an array of up to 64 (key, value) tuples. Keys can be in either 
keyID (int) or keyname (str) format

```python
>>> from pyubx2 import UBXMessage
>>> layers = 1
>>> transaction = 0
>>> cfgData = [("CFG_UART1_BAUDRATE", 9600), (0x40530001, 115200)]
>>> msg = UBXMessage.config_set(layers, transaction, cfgData)
>>> print(msg)
<UBX(CFG-VALSET, version=0, ram=1, bbr=0, flash=0, action=0, reserved0=0, cfgData_01=1, cfgData_02=0 ...)>
>>> serialOut.write(msg.serialize())
```

**UBXMessage.config_del() (CFG-VALDEL)**

Unsets (deletes) up to 64 parameter settings in the designated non-volatile memory layer(s).

Parameters:

1. layers - 2 = Battery-Backed RAM (BBR), 4 = External Flash
1. transaction - 0 = None, 1 = Start, 2 = Ongoing, 3 = Commit
1. keys - an array of up to 64 keys in either keyID (int) or keyname (str) format

```python
>>> from pyubx2 import UBXMessage
>>> layers = 4
>>> transaction = 0
>>> keys = ["CFG_UART1_BAUDRATE", 0x40530001]
>>> msg = UBXMessage.config_del(layers, transaction, keys)
>>> print(msg)
<UBX(CFG-VALDEL, version=0, bbr=0, flash=1, action=0, reserved0=0, keys_01=1079115777, keys_02=1079181313)>
>>> serialOut.write(msg.serialize())
```

**UBXMessage.config_poll() (CFG-VALGET)**

Polls up to 64 parameters from the designated memory layer.

Parameters:

1. layer - 0 = Volatile RAM, 1 = Battery-Backed RAM (BBR), 2 = External Flash, 7 = Default (readonly)
1. position - unsigned integer representing number of items to be skipped before returning result
(used when number of matches for an individual query exceeds 64)
1. keys - an array of up to 64 keys in either keyID (int) or keyname (str) format. keyIDs can use
wildcards - see example below and UBX device interface specification for details.

```python
>>> from pyubx2 import UBXMessage
>>> layer = 1
>>> position = 0
>>> keys = ["CFG_UART1_BAUDRATE", 0x40530001]
>>> msg = UBXMessage.config_poll(layer, position, keys)
>>> print(msg)
<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=1079115777, keys_02=1079181313)>
>>> serialOut.write(msg.serialize())
```

Wild card queries can be performed by setting bits 0..15 of the keyID to `0xffff` e.g. to retrieve all CFG_MSGOUT parameters (keyID `0x2091*`) :

```python
>>> from pyubx2 import UBXMessage
>>> layer = 1
>>> position = 0 # retrieve first 64 results
>>> keys = [0x2091ffff]
>>> msg1of3 = UBXMessage.config_poll(layer, position, keys)
>>> print(msg1of3)
<UBX(CFG-VALGET, version=0, layer=1, position=0, keys_01=546439167)>
>>> serialOut.write(msg1of3.serialize())
>>> position = 64 # retrieve next 64 results
>>> msg2of3 = UBXMessage.config_poll(layer, position, keys)
>>> print(msg2of3)
<UBX(CFG-VALGET, version=0, layer=1, position=64, keys_01=546439167)>
>>> serialOut.write(msg2of3.serialize())
>>> position = 128 # retrieve next 64 results
>>> msg3of3 = UBXMessage.config_poll(layer, position, keys)
>>> print(msg3of3)
<UBX(CFG-VALGET, version=0, layer=1, position=128, keys_01=546439167)>
>>> serialOut.write(msg3of3.serialize())
```

---
## <a name="examples">Examples</a>

The following command line examples can be found in the `\examples` folder:

1. `ubxoptions.py` illustrates the various options available for parsing and constructing UBX messages.
1. `ubxpoller.py` illustrates how to implement a simple threaded configuration polling utility for UBX messages. 
1. `ubxsetrates.py` illustrates how to use legacy configuration messages (CFG-MSG) to set navigation message rates.
1. `ubxconfigdb.py` illustrates how to invoke the Generation 9 configuration database interface via CFG-VALSET, CF-VALDEL and CFG-VALGET messages.
1. `ubxfactoryreset.py` illustrates how to send a factory reset (CFG-CFG) command.
1. `ubxfile.py` illustrates how to implement a binary file reader for UBX messages using `UBXReader` iterator functionality. 
1. `ubxsocket.py` illustrates how to implement a TCP Socket reader for UBX messages using `UBXReader` iterator functionality. Can be used in conjunction with the `tcpserver_threaded.py` socket server test harness.
1. `gpxtracker.py` illustrates a simple tool to convert a binary UBX data dump to a `*.gpx` track file.
1. `ubxserver.py` in the \examples\webserver folder illustrates a simple HTTP web server wrapper around `pyubx2.UBXreader`; it presents data from selected UBX messages as a web page http://localhost:8080 or a RESTful API http://localhost:8080/gps.
1. `benchmark.py` provides a simple performance benchmarking tool for the `pyubx2` parser.
1. `gnssserver.py` implements a simple but fully-functional command-line TCP Socket Server or NTRIP server, broadcasting GNSS data from the receiver to any connected TCP socket client.

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

In most cases, a UBX message's content (payload) is uniquely defined by its class, id and mode; accommodating the message simply requires the addition of an appropriate dictionary entry to the relevant `ubxtypes_*.py` module(s).

However, there are a handful of message types which have multiple possible payload definitions for the same class, id and mode. These exceptional message types require dedicated routines in `ubxmessage.py` which examine elements of the payload itself in order to determine the appropriate dictionary definition. This currently applies to the following message types: CFG-NMEA, NAV-RELPOSNED, RXM-PMP, RXM-PMREQ, RXM-RLM, TIM-VCOCAL.

---
## <a name="cli">Command Line Utility</a>

If `pyubx2` is installed using pip, a command line utility `gnssdump` is automatically installed into the Python 3 scripts (bin) directory. This utility is capable of streaming and parsing NMEA, UBX and RTCM3 data from any data stream (including Serial and File) to the terminal or to designated NMEA, UBX or RTCM3 protocol handlers. A protocol handler could be a 
writeable output media (e.g. File or socket) or an evaluable Python expression.

The utility can output data in a variety of formats; parsed (1), raw binary (2), hexadecimal string (4), tabulated hexadecimal (8) or any combination thereof.

Any one of the following data stream specifiers must be provided:
- `stream`: any instance of a stream class which implements a read(n) -> bytes method
- `filename`: name of binary input file e.g. `logfile.bin`
- `port`: serial port e.g. `COM3` or `/dev/ttyACM1`
- `socket`: socket e.g. `192.168.0.72:50007` (port must be specified)

For help and full list of optional arguments, type:

```shell
> gnssdump -h
```

Assuming the Python 3 scripts (bin) directory is in your PATH, the CLI utility may be invoked from the shell thus:

Serial input example (with simple external UBX protocol handler):

```shell
> gnssdump port=/dev/ttyACM1 baud=9600 timeout=5 quitonerror=1 protfilter=2 msgfilter=NAV-PVT ubxhandler="lambda msg: print(f'lat: {msg.lat}, lon: {msg.lon}')"

Parsing GNSS data stream from serial: Serial<id=0x10fe8f100, open=True>(port='/dev/ttyACM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False)...

lat: 51.352179, lon: -2.130762
lat: 51.352155, lon: -2.130751
```

File input example (in tabulated hexadecimal format):

```shell
> gnssdump filename=pygpsdata.log quitonerror=2 format=8 protfilter=1 msgfilter=GPGGA,GPGSA

Parsing GNSS data stream from file: <_io.BufferedReader name='pygpsdata.log'>...

000: 2447 5047 4741 2c30 3830 3234 372e 3030  | b'$GPGGA,080247.00' |
016: 2c35 3332 372e 3034 3330 302c 4e2c 3030  | b',5327.04300,N,00' |
032: 3231 342e 3431 3338 352c 572c 312c 3037  | b'214.41385,W,1,07' |
048: 2c31 2e36 332c 3336 2e37 2c4d 2c34 382e  | b',1.63,36.7,M,48.' |
064: 352c 4d2c 2c2a 3737 0d0a                 | b'5,M,,*77\r\n' |

000: 2447 5047 5341 2c41 2c33 2c30 322c 3133  | b'$GPGSA,A,3,02,13' |
016: 2c32 302c 3037 2c30 352c 3330 2c30 392c  | b',20,07,05,30,09,' |
032: 2c2c 2c2c 2c32 2e34 342c 312e 3633 2c31  | b',,,,,2.44,1.63,1' |
048: 2e38 322a 3035 0d0a                      | b'.82*05\r\n' |
```

The `gnssdump` utility implements a new `GNSSStreamer` class which may be used directly within Python application code via:

```python
>>> from pyubx2cli import GNSSStreamer
```

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
#### 4. Reading from NMEA log file returns no results.
- If reading from a binary log file containing NMEA messages, ensure that the message terminator is `CRLF` (`\r\n` or `x0d0a`) rather than just `LF` (`\n` or `0x0a`). Some standard text editors may replace a `CRLF` with `LF` - use a dedicated hex editor instead.


---
## <a name="gui">Graphical Client</a>

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols (via pynmeagps and pyubx2 
respectively) is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyubx2.svg)

`pyubx2` is maintained entirely by volunteers. If you find it useful, a small donation would be greatly appreciated!

[![Donations](https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=4TG5HGBNAM7YJ)
