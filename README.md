pyubx2
=======

`pyubx2` is an original python library for the UBX protocol. 

UBX is a proprietary binary protocol implemented on u-blox &copy; GPS/GNSS receiver modules.

The `pyubx2` homepage is located at [http://github.com/semuconsulting/pyubx2](http://github.com/semuconsulting/pyubx2).

This is a personal project and I am in no way affiliated with u-blox.

### Current Status

![Status](https://img.shields.io/pypi/status/pyubx2)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyubx2?include_prereleases)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyubx2)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyubx2)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyubx2.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyubx2)

At time of writing the library is based on the [u-blox generation 8 protocol](https://www.u-blox.com/en/docs/UBX-13003221) but is readily extensible for later generations.

Implements an almost complete range of inbound and outbound UBX Generation 8 protocol messages *with the exception of* a handful of message classes which require non-standard processing (see release notes on GitHub for details). These are in hand.

Constructive feedback and feature requests welcome.

### Compatibility

![Python version](https://img.shields.io/pypi/pyversions/pyubx2.svg?style=flat)

`pyubx2` is compatible with Python 3.6+ and has no third-party library dependencies.

### Installation

[![PyPI version](https://img.shields.io/pypi/v/pyubx2.svg?style=flat)](https://pypi.org/project/pyubx2/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyubx2.svg?style=flat)

The recommended way to install `pyubx2` is with
[pip](http://pypi.python.org/pypi/pip/):

`pip install pyubx2`

## Reading (Streaming)

You can create a `UBXReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual UBX messages can then be read using the `UBXReader.read()` function, which returns both the raw binary
data (as bytes) and the parsed data (as a `UBXMessage` object). The function is thread-safe in so far as the incoming
data stream object is thread-safe.

## Parsing

You can parse individual UBX messages using the `UBXMessage.parse(data, validate=False)` function, which takes a bytes array containing a
binary UBX message and returns a `UBXMessage` object.

If the optional 'validate' parameter is set to `True`, `parse` will validate the supplied UBX message header, payload length and checksum. 
If any of these are not consistent with the message content, it will raise a `UBXParseError`. Otherwise, the function will automatically
generate the appropriate payload length and checksum.

Example:

```python
>>> from pyubx2 import UBXMessage
>>> msg = UBXMessage.parse(b'\xb5b\x05\x01\x02\x00\x06\x01\x0f\x38', True)
>>> msg
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
>>> msg = UBXMessage.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
>>> msg
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

You can create a `UBXMessage` object by calling the constructor with message class, message id, payload and mode parameters.

The 'mode' parameter is an integer flag signifying whether the message payload refers to a: 
* GET message (i.e. *from* the receiver - the default)
* SET message (i.e. *to* the receiver)
* POLL message (i.e. *to* the receiver in anticipation of a response back)

The distinction is necessary because the UBX protocol uses the same message class and id
for all three modes, but with different payloads.

e.g. to generate a outgoing CFG-MSG which polls the 'VTG' NMEA message rate on the current port:

```python
>>> from pyubx2 import UBXMessage, POLL
>>> msg = UBXMessage(b'\x06', b'\x01', b'\xF0\x05', POLL)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```

The constructor also supports plain text representations of the message class and id, e.g.

```python
>>> from pyubx2 import UBXMessage, POLL
>>> msg = UBXMessage('CFG','CFG-MSG', b'\xF1\x03', POLL)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Proprietary, msgID=UBX-03)>
```

### Serializing

The `UBXMessage` class implements a `serialize()` method to convert a `UBXMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` message which sets the NMEA GLL message rate to '1' on the receiver's UART and USB ports (assuming an output serial stream has been created as `serialOut`):

```python
>>> from pyubx2 import UBXMessage, SET
>>> msg = UBXMessage('CFG','CFG-MSG', b'\xF0\x01\x00\x01\x01\x01\x00\x00', SET)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=GLL, rateDDC=0, rateUART1=1, rateUART2=1, rateUSB=1, rateSPI=0, reserved=0)>
>>> output = msg.serialize()
>>> output
b'\xb5b\x06\x01\x08\x00\xf0\x01\x00\x01\x01\x01\x00\x00\x036'
>>> serialOut.write(output)
```

## Examples

The following examples can be found in the `\examples` folder:

1. `ubxstreamer.py` illustrates how to implement a threaded serial reader for UBX messages using pyubx2. 

1. `ubxconfig.py` illustrates how to implement a simple configuration utility which sets output UBX-NAV message  rates on the  receiver's UART and USB ports (on a non-permanent basis). You can see the results using `ubxstreamer.py`.

1. `ubxprotocol.py` illustrates how to set the outbound protocols on the receiver's USB port 
to NMEA, UBX or both (on a non-permanent basis). You can see the results using `ubxstreamer.py`.


## Extensibility

The UBX protocol is principally defined in the modules `ubxtypes_*.py` as a series of dictionaries. Additional message types 
can be readily added to the appropriate dictionary. Message payload definitions must conform to the following rules:
* attribute names must be unique within each message class
* attribute types must be one of the valid types (I1, U1, etc.)
* repeating groups are defined as nested dicts and must be preceded by an attribute which contains the number of
repeats (see NAV-SVINFO by way of example). If this attribute is named 'numCh', the code will identity it automatically; 
if the attribute is given a different name, ubxmessage.py will need to be modified to identify it explicitly. If such
an attribute is *not* present, the code will need to be modified to handle this particular message type as an exception to
the norm e.g. deduce the number of repeats from the payload length.
* repeating attribute names are suffixed with a two-digit index (svid_01, svid_02, etc.)

## Graphical Client

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols (via pynmea2 and pyubx2 
respectively) is under development at: 

[http://github.com/semuconsulting/PyGPSClient](http://github.com/semuconsulting/PyGPSClient)

## Author Information

![License](https://img.shields.io/github/license/semuconsulting/pyubx2.svg)

semuadmin@semuconsulting.com
 