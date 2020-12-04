pyubx2
=======

`pyubx2` is an original python library for the UBX protocol. 

UBX is a proprietary binary protocol implemented on u-blox &copy; GPS/GNSS receiver modules.

The `pyubx2` homepage is located at [http://github.com/semuconsulting/pyubx2](http://github.com/semuconsulting/pyubx2).

This is an independent project and we have no affiliation whatsoever with u-blox &copy;.

### Current Status

![Status](https://img.shields.io/pypi/status/pyubx2)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyubx2?include_prereleases)
![Build](https://img.shields.io/travis/semuconsulting/pyubx2)
[![Coverage Status](https://coveralls.io/repos/github/semuconsulting/pyubx2/badge.svg?branch=master)](https://coveralls.io/github/semuconsulting/pyubx2?branch=master)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyubx2)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyubx2)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyubx2.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyubx2)

At time of writing the library implements a comprehensive set of inbound and outbound messages as defined in 
the [u-blox generation 9 protocol](https://www.u-blox.com/en/docs/UBX-19035940), but is readily 
[extensible](#extensibility) for later generations.

Contributions and feedback welcome - see CONTRIBUTING.MD

## <a name="installation">Installation</a>

`pyubx2` is compatible with Python 3.6+ and has no third-party library dependencies.

![Python version](https://img.shields.io/pypi/pyversions/pyubx2.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyubx2.svg?style=flat)](https://pypi.org/project/pyubx2/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyubx2.svg?style=flat)

The recommended way to install the latest version of `pyubx2` is with
[pip](http://pypi.python.org/pypi/pip/):

`python -m pip install --upgrade pyubx2`

## Reading (Streaming)

You can create a `UBXReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual input UBX messages can then be read using the `UBXReader.read()` function, which returns both the raw binary
data (as bytes) and the parsed data (as a `UBXMessage` object). The function is thread-safe in so far as the incoming
data stream object is thread-safe. `UBXReader` also implements an iterator.

The `UBXReader` constructor includes an optional `validate` flag which governs behaviour if the stream includes non-UBX data.
If set to 'False' (the default), it will ignore such data and continue with the next valid UBX message. If set to 'True', it
will raise a `UBXStreamError`.

Examples:

* Serial input - this example will ignore any non-UBX data.

```python
>>> from serial import Serial
>>> from pyubx2 import UBXReader
>>> stream = Serial('COM6', 9600, timeout=3)
>>> ubr = UBXReader(stream)
>>> (raw_data, parsed_data) = ubr.read()
```

* File input (using iterator) - this example will produce a `UBXStreamError` if non-UBX data is encountered.

```python
>>> import os
>>> from pyubx2 import UBXReader
>>> file = os.path.join(os.path.dirname(__file__), 'ubxdata.bin')
>>> stream = open(file, 'rb')
>>> ubr = UBXReader(stream, True)
>>> for (raw_data, parsed_data) in ubr: print(parsed_data)
...
```

## Parsing

You can parse individual UBX messages using the `UBXMessage.parse(data, validate=False)` function, which takes a bytes array containing a binary UBX message and returns a `UBXMessage` object.

If the optional 'validate' parameter is set to `True`, `parse` will validate the supplied UBX message header, payload length and checksum. 
If any of these are not consistent with the message content, it will raise a `UBXParseError`. Otherwise, the function will automatically
generate the appropriate payload length and checksum.

Example:

```python
>>> from pyubx2 import UBXMessage
>>> msg = UBXMessage.parse(b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38', True)
>>> print(msg)
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
>>> msg = UBXMessage.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
>>> print(msg)
<UBX(NAV-VELNED, iTOW=403327000, velN=-1, velE=-21, velD=-4, speed=22, gSpeed=21, heading=128387, sAcc=67, cAcc=8056455)>
```

The `UBXMessage` object exposes different public properties depending on its message type or 'identity',
e.g. the `NAV-POSLLH` message has the following properties:

```python
>>> msg
<UBX(NAV-POSLLH, iTOW=403667000, lon=-21601284, lat=526206345, height=86327, hMSL=37844, hAcc=38885, vAcc=16557)>
>>>msg.identity
'NAV-POSLLH'
>>>msg.lat/10**7, msg.lon/10**7
(52.6206345, -2.1601284)
>>>msg.hMSL/10**3
37.844
```

## Generating

(see [below](#configinterface) for special methods relating to the UBX configuration interface)

You can create a `UBXMessage` object by calling the constructor with the following parameters:
1. ubxClass
2. ubxID
3. mode (0=GET, 1=SET, 2=POLL)
4. (optional) a series of keyword parameters representing the message payload

**NB:** Once instantiated, a `UBXMessage` object is immutable.

The 'ubxClass' and 'ubxID' parameters may be passed as lookup strings, integers or bytes.

The 'mode' parameter signifies whether the message payload refers to a: 
* GET message (i.e. output *from* the receiver)
* SET message (i.e. input *to* the receiver)
* POLL message (i.e. input *to* the receiver in anticipation of a response back)

The message payload can be defined via keyword parameters in one of three ways:
1. A single keyword parameter of `payload` containing the full payload as a sequence of bytes (any other keyword parameters will be ignored). **NB**: messages containing variable length payloads *must* be defined using a `payload` keyword.
2. One or more keyword parameters corresponding to individual message attributes. Any attributes not explicitly provided as keyword
parameters will be set to a nominal value according to their type.
3. If no keyword parameters are passed, the payload is assumed to be null.

e.g. to generate a CFG-MSG which polls the 'VTG' NMEA message rate on the current port, 
any of the following constructor formats will work:

```python
>>> from pyubx2 import UBXMessage, POLL
>>> msg1 = UBXMessage(b'\x06', b'\x01', POLL, payload=b'\xf0\x05')
>>> print(msg1)
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```

```python
>>> from pyubx2 import UBXMessage, POLL
>>> msg2 = UBXMessage(6, 1, POLL, msgClass=240, msgID=5)
>>> print(msg2)
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```

```python
>>> from pyubx2 import UBXMessage, POLL
>>> msg3 = UBXMessage('CFG','CFG-MSG', POLL, msgClass=240, msgID=5)
>>> print(msg3)
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```


### <a name="configinterface">Configuration Interface</a>

**CFG-VALSET, CFG-VALDEL and CFG-VALGET message types**

Generation 9 of the UBX protocol introduced the concept of a device configuration interface with configurable parameters being set or unset (del) in the designated memory layer(s) via the CFG-VALSET and CFG-VALDEL message types, or queried via the CFG-VALGET message type. *Legacy CFG message types continue to be supported but are now deprecated*.

Individual configuration parameters are designated by keys, which may be in string (keyname) or integer (keyID) format. Keynames and their corresponding hexadecimal keyIDs and data types are defined in `ubxtypes_configdb.py` as `UBX_CONFIG_DATABASE`. Two static helper methods are available to convert keyname to keyID and vice versa - `UBXMessage.cfgname2key()` and `UBXMessage.cfgkey2name()`.

Optionally, batches of CFG-VALSET and CFG-VALDEL messages can be applied transactionally, with the combined configuration only being committed at the end of the transaction.

Dedicated static methods are provided to create these message types - `UBXMessage.config_set()`, `UBXMessage.config_del()` and `UBXMessage.config_poll()`. 

**UBXMessage.config_set() (CFG-VALSET)**

Sets up to 64 parameters in the designated memory layer(s).

Parameters:

1. layers - 1 = Volatile RAM, 2 = Battery-Backed RAM (BBR), 4 = External Flash
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
<UBX(CFG-VALSET, version=0, layers=b'\x01', transaction=0, reserved0=0, cfgData_01=1, cfgData_02=0 ...)>
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
<UBX(CFG-VALDEL, version=0, layers=b'\x04', transaction=b'\x00', reserved0=0, keys_01=1079115777, keys_02=1079181313)>
```

**UBXMessage.config_poll() (CFG-VALGET)**

Polls up to 64 parameters from the designated memory layer.

Parameters:

1. layer - 0 = Volatile RAM, 1 = Battery-Backed RAM (BBR), 2 = External Flash, 7 = Default (readonly)
1. position - unsigned integer representing number of items to be skipped before returning result
(used when number of matches for an individual query exceeds 64)
1. keys - an array of up to 64 keys in either keyID (int) or keyname (str) format. keyIDs can be
wildcards - see UBX device interface specification for details.

```python
>>> from pyubx2 import UBXMessage
>>> layer = 1
>>> position = 0
>>> keys = ["CFG_UART1_BAUDRATE", 0x40530001]
>>> msg = UBXMessage.config_poll(layer, position, keys)
>>> print(msg)
<UBX(CFG-VALGET, version=0, layers=b'\x01', position=b'\x00\x00', keys_01=1079115777, keys_02=1079181313)>
```

Wild card query to retrieve all CFG_MSGOUT (keyID 0x2091*) parameters (set bits 0..15 of the keyID to 0xffff):

```python
>>> from pyubx2 import UBXMessage
>>> layer = 1
>>> position = 0 # retrieve first 64 results
>>> keys = [0x2091ffff]
>>> msg1 = UBXMessage.config_poll(layer, position, keys)
>>> print(msg1)
<UBX(CFG-VALGET, version=0, layers=b'\x01', position=b'\x00\x00', keys_01=546439167)>
>>> position = 64 # retrieve next 64 results
>>> msg2 = UBXMessage.config_poll(layer, position, keys)
>>> print(msg2)
<UBX(CFG-VALGET, version=0, layers=b'\x01', position=b'@\x00', keys_01=546439167)>
...
```

### Serializing

The `UBXMessage` class implements a `serialize()` method to convert a `UBXMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` message which sets the NMEA GLL message rate to '1' on the receiver's UART1 and USB ports (assuming an output serial stream has been created as `serialOut`):

```python
>>> from pyubx2 import UBXMessage, SET
>>> msg = UBXMessage('CFG','CFG-MSG', SET, msgClass=240, msgID=1, rateUART1=1, rateUSB=1)
>>> print(msg)
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=1, rateSPI=0, reserved=0)>
>>> output = msg.serialize()
>>> output
b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x00\x01\x00\x00\x036'
>>> serialOut.write(output)
```

## Examples

The following examples can be found in the `\examples` folder:

1. `ubxstreamer.py` illustrates how to implement a threaded serial reader for UBX messages using pyubx2.UBXReader. 

1. `ubxfile.py` illustrates how to implement a binary file reader for UBX messages using 
the pyubx2.UBXReader iterator function. 

1. `ubxconfig.py` illustrates how to implement a simple configuration utility which sets output UBX-NAV message  rates on the  receiver's UART and USB ports (on a non-permanent basis). You can see the results using `ubxstreamer.py`.

1. `ubxprotocol.py` illustrates how to set the outbound protocols on the receiver's USB port 
to NMEA, UBX or both (on a non-permanent basis). You can see the results using `ubxstreamer.py`.

1. `ubxtracker.py` illustrates a simple CLI tool to convert a binary UBX data dump 
(e.g. as produced by the [PyGPSClient](http://github.com/semuconsulting/PyGPSClient)'s data logging facility) to a `*.gpx` track file using pyubx2.UBXReader.



## <a name="extensibility">Extensibility</a>

The UBX protocol is principally defined in the modules `ubxtypes_*.py` as a series of dictionaries. Additional message types 
can be readily added to the appropriate dictionary. Message payload definitions must conform to the following rules:
* attribute names must be unique within each message class
* attribute types must be one of the valid types (I1, U2, X4, etc.)
* repeating groups must be defined as a tuple ('numr', {dict}), where 'numr' is the name of
the preceding attribute containing the number of repeats (or 'None' if there isn't one), 
and {dict} is the nested dictionary of repeating items. See NAV-SVINFO by way of example.
* repeating attribute names are parsed with a two-digit suffix (svid_01, svid_02, etc.)

## Graphical Client

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols (via pynmea2 and pyubx2 
respectively) is under development at: 

[http://github.com/semuconsulting/PyGPSClient](http://github.com/semuconsulting/PyGPSClient)

## Author Information

![License](https://img.shields.io/github/license/semuconsulting/pyubx2.svg)

semuadmin@semuconsulting.com
 