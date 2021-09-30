"""
ubxoptions.py

Series of worked examples illustrating the various options available for parsing and constructing UBX messages.
The example used here is a CFG-GNSS (GNSS Configuration) message.

The examples may be run without connecting a receiver.
 
The CFG-GNSS message contains configuration settings for one or more GNSS constellations and augmentation systems 
handled by the receiver (in this particular example the IMES setting is omitted):
"""
GPS = 0
SBAS = 1
Galileo = 2
BeiDou = 3
IMES = 4
QZSS = 5
GLONASS = 6
"""
For each constellation, a bitfield property 'flags' (X4) contains two bit flags 'enable' (U1) and 'sigCfMask' (U8).

The CFG-GNSS message serves as both a command input (SET) message, and an output (GET) message in response to a CFG-GNSS POLL.

Created on 29 Sep 2021
@author: semuadmin
"""

from serial import Serial
from pyubx2 import UBXReader, UBXMessage, GET, SET, POLL, VALCKSUM

# This is the raw CFG-GNSS UBX message, as output by a u-blox M9N receiver.
CFG_GNSS = b"\xb5b\x06>4\x00\x00**\x06\x00\x08\x10\x00\x01\x00\x01\x00\x01\x03\x03\x00\x01\x00\x01\x00\x02\x08\x0c\x00\x01\x00\x01\x00\x03\x02\x05\x00\x01\x00\x01\x00\x05\x03\x04\x00\x01\x00\x05\x00\x06\x08\x0c\x00\x01\x00\x01\x00G\xde"
print("\nHere is the raw CFG-GNSS message, as output by a u-blox M9N receiver:\n")
print(CFG_GNSS)

# To poll this message, we could create and send a CFG-GNSS POLL message to a connected receiver:
# serialOut = Serial("/dev/tty.usbmodem14101", 9600, timeout=5)
# msg0 = UBXMessage("CFG", "CFG-GNSS", POLL)
# serialOut.write(msg0.serialize())

# This is the CFG-GNSS message parsed with all the optional keyword arguments set to their defaults
# (the arguments could in this case be omitted).
# Each bitfield is rendered as its individual bit flags 'enable_01=1, sigCfMask_01=1' etc.
print("\nHere is the CFG-GNSS message parsed with default options:\n")
msg1 = UBXReader.parse(CFG_GNSS, validate=VALCKSUM, msgmode=GET, parsebitfield=True)
print(msg1)

# This is the CFG-GNSS message parsed with 'parsebitfield' set to False and other options left at the defaults
# Each bitfield is rendered as a sequence of bytes 'flags_01=b'\x01\x00\x01\x00' etc.
print(
    "\nHere is the CFG-GNSS message parsed with the parsebitfield option set to False:\n"
)
msg2 = UBXReader.parse(CFG_GNSS, parsebitfield=False)
print(msg2)

# Note that the raw payloads are identical; only the parsed format differs:
print(
    "\nThe raw payloads of these messages are identical, only the parsed format differs:\n"
)
print(msg1.payload)
print(msg2.payload)

# Now construct a new CFG-GNSS input (SET) message from the payload of the previously parsed GET message:
print(
    "\nHere is a new CFG-GNSS input (SET) message constructed from the raw payload of the parsed (GET) message:\n"
)
msg3 = UBXMessage("CFG", "CFG-GNSS", SET, payload=msg1.payload)
print(msg3)

# Now construct an identical message by setting all the individual property keywords.
# Note that properties which are part of a repeating group must be suffixed with the appropriate index '_01', '_02', etc.
# Note that we don't bother setting any reserved fields - they default to zeros, as will any other properties we omit to define
# explicitly.
print(
    "\nHere is a new CFG-GNSS input (SET) message constructed by setting all the individual property keywords:\n"
)
msg4 = UBXMessage(
    "CFG",
    "CFG-GNSS",
    SET,
    msgVer=0,
    numTrkChHw=42,
    numTrkChUse=42,
    numConfigBlocks=6,
    gnssId_01=GPS,
    resTrkCh_01=8,
    maxTrkCh_01=16,
    enable_01=1,
    sigCfMask_01=1,
    gnssId_02=SBAS,
    resTrkCh_02=3,
    maxTrkCh_02=3,
    enable_02=1,
    sigCfMask_02=1,
    gnssId_03=Galileo,
    resTrkCh_03=8,
    maxTrkCh_03=12,
    enable_03=1,
    sigCfMask_03=1,
    gnssId_04=BeiDou,
    resTrkCh_04=2,
    maxTrkCh_04=5,
    enable_04=1,
    sigCfMask_04=1,
    gnssId_05=QZSS,
    resTrkCh_05=3,
    maxTrkCh_05=4,
    enable_05=1,
    sigCfMask_05=5,
    gnssId_06=GLONASS,
    resTrkCh_06=8,
    maxTrkCh_06=12,
    enable_06=1,
    sigCfMask_06=1,
)
print(msg4)

# Verify that the two UBXMessage objects are the same:
print(
    f"\nVerify that the string representations of the messages are the same: {str(msg3) == str(msg4)}"
)
print(
    f"\nVerify that the message payloads are the same: {msg3.payload == msg4.payload}"
)

# Now construct a new CFG-GNSS input (SET) message with only one GNSS block (numConfigBlocks=1), and
# with the 'parsebitfield' option set to False. In this case, rather than setting the two bit flags
# 'enable' and 'sigCfMask' individually, we set the entire 'flags' bitfield as a 4-byte sequence,
# remembering to include the unused reserved bits.
print(
    "\nHere is a new CFG-GNSS input (SET) message with only one GNSS block (numConfigBlocks=1) and parsebitfield=False:\n"
)
msg5 = UBXMessage(
    "CFG",
    "CFG-GNSS",
    SET,
    msgVer=0,
    numTrkChHw=42,
    numTrkChUse=42,
    numConfigBlocks=1,
    gnssId_01=GPS,
    resTrkCh_01=8,
    maxTrkCh_01=16,
    flags_01=b"\x01\x00\x01\x00",
    parsebitfield=False,
)
print(msg5)
print("\nHere are some individual properties from this message:\n")
print(
    f"numConfigBlocks={msg5.numConfigBlocks}, gnssId={msg5.gnssId_01}, maxTrkCh={msg5.maxTrkCh_01}, flags={msg5.flags_01}"
)

# If we now serialize and parse this message with parsebitfield=True (the default), the individual bit flags
# are once again rendered.
print("\nHere is the previous CFG-GNSS message parsed with parsebitfield=True:\n")
msg6 = UBXReader.parse(msg5.serialize(), msgmode=SET, parsebitfield=True)
print(msg6)
print("\nHere are the individual bit flags from this message:\n")
print(f"enable={msg6.enable_01}, sigCfMask={msg6.sigCfMask_01}")
