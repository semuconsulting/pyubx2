pyubx2
=======

`pyubx2` is a python library for the UBX protocol. 

UBX is a proprietary binary protocol implemented on u-blox &copy; GPS/GNSS receiver modules. At time of writing the library is based
on the [u-blox generation 6 protocol](https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf) but
is readily extensible for later generations.

The structure and functionality of `pyubx2` broadly mirrors that of [Knio's pynmea2](https://github.com/Knio/pynmea2) library for NMEA protocols, but the code is entirely original.

The `pyubx2` homepage is located at [http://github.com/semuconsulting/pyubx2](http://github.com/semuconsulting/pyubx2).

This is a personal project and I am in no way affiliated with u-blox.

**Build Status:** Under Development

### Compatibility

`pyubx2` is compatible with Python 3.6+ and has no external library dependencies.


### Installation

The recommended way to install `pyubx2` is with
[pip](http://pypi.python.org/pypi/pip/):

`pip install pyubx2`

Parsing
-------

You can parse individual UBX messages using the `UBXMessage.parse(data, validate=False)` function, which takes a bytes array containing a
binary UBX message and returns a `UBXMessage` object.

If the optional 'validate' parameter is set to `True`, `parse` will validate the supplied UBX message header, payload length and checksum. 
If any of these are not consistent with the message content, it will raise a `UBXParseError`. Otherwise, the function will automatically
generate the appropriate payload length and checksum.

Examples:

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage.parse(b'\xb5b\x05\x00\x02\x00\x06\x01\x0e3', True)
>>> msg
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)>
>>> msg = pyubx2.UBXMessage.parse(b'\xb5b\x01\x12$\x000D\n\x18\xfd\xff\xff\xff\xf1\xff\xff\xff\xfc\xff\xff\xff\x10\x00\x00\x00\x0f\x00\x00\x00\x83\xf5\x01\x00A\x00\x00\x00\xf0\xdfz\x00\xd0\xa6')
>>> msg
<UBX(NAV-VELNED, iTOW=403327000, velN=-1, velE=-21, velD=-4, speed=22, gSpeed=21, heading=128387, sAcc=67, cAcc=8056455)>
```

The `UBXMessage` object exposes different public properties depending on its message type or 'identity',
e.g. the `NAV-POSLLH` message has the following properties:

```python
>>> msg
<UBX(NAV-POSLLH, iTOW=403667000, lon=-21601284, lat=526206345, height=86327, hMSL=37844, HAcc=38885, vAcc=16557)>
>>>msg.identity
'NAV-POSLLH'
>>>msg.lat, msg.lon
526206345, -21601284
```

Generating
----------

You can create a `UBXMessage` object by calling the constructor with message class, message id, payload and inout parameters.

The 'inout' parameter is a boolean signifying whether the message payload is for an output message (*to* the receiver) or an input
message (*from* the receiver) - the distinction is necessary because the UBX protocol uses the same message class and id
for both input and output messages, though with different payloads.

e.g. to generate a outgoing CFG-MSG which polls the 'VTG' NMEA message rate on the current port:

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage(b'\x06', b'\x01', b'\xF0\x05', True)
>>> msg
<UBX(CFG-MSG, msgClass=NMEA-Standard, msgID=VTG)>
```

The constructor also supports plain text representations of the message class and id, e.g.

```python
>>> import pyubx2
>>> msg = pyubx2.UBXMessage('CFG','CFG-MSG', b'x\F0x\05x')
```

## Graphical Client

A free, open-source python/tkinter graphical GPS client which supports both NMEA and UBX protocols (via pynmea2 and pyubx2 
respectively) is under development at: 

[http://github.com/semuconsulting/PyGPSClient](http://github.com/semuconsulting/PyGPSClient)

## Author Information

semuadmin@semuconsulting.com
 