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

At time of writing the library implements a complete set of inbound and outbound messages as defined in 
the [u-blox generation 8 protocol](https://www.u-blox.com/en/docs/UBX-13003221), but is readily 
[extensible](#extensibility) for later generations.

Constructive feedback and feature requests welcome.

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

Examples:

* Serial input

```python
>>> from serial import Serial
>>> from pyubx2 import UBXReader
>>> stream = Serial('COM6', 9600, timeout=3)
>>> ubr = UBXReader(stream)
>>> (raw_data, parsed_data) = ubr.read()
```

* File input (using iterator)

```python
>>> import os
>>> from pyubx2 import UBXReader
>>> file = os.path.join(os.path.dirname(__file__), 'ubxdata.bin')
>>> stream = open(file, 'rb')
>>> ubr = UBXReader(stream)
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
1. A single keyword parameter of `payload` containing the full payload as a sequence of bytes (any other keyword parameters will be ignored).
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
 