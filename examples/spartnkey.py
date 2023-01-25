"""
spartnkey.py

Example script illustrating how to format current and next
SPARTN keys (e.g. from u-blox PointPerfect service) as a
UBX RXM-SPARTN-KEY message and upload this to a ZED-F9P receiver.

You can find the current and next keys in Thingstream here:

https://thingstream.io/
Location Services \ Location Things \ Thing Details \ Credentials
L-Band + IP Dynamic Keys

Current and Next GPS Calendar Wno and Tow can be obtained from:

https://navigationservices.agi.com/GNSSWeb/

(e.g. for Thursday Jan 25th; Wno = 2246 and Tow = 259200)

Created on 23 Jan 2023

:author: semuadmin
:copyright: SEMU Consulting © 2023
:license: BSD 3-Clause
"""

import sys
from serial import Serial, SerialException
from pyubx2 import UBXMessage, UBXReader, SET, U1, U2, U4, val2bytes

keys = []
keylens = []
wnos = []
tows = []
print("How many SPARTN keys do you want to upload (1 or 2)? (2): ", end="")
val = input() or "2"
numkeys = int(val)
for i in range(numkeys):
    LBL = "second" if i + 1 == 2 else "first"
    print(f"Enter {LBL} key as string (max 255 chars): ", end="")
    val = input()
    lval = len(val)
    if lval > 255:
        print("Key must be less than 255 characters!")
        sys.exit()
    keylens.append(val2bytes(lval, U1))
    keys.append(bytes(val, "utf-8"))
    print(f"Enter {LBL} valid from Week Number (Wno) as integer: ", end="")
    val = input() or "2246"
    wnos.append(val2bytes(int(val), U2))
    print(f"Enter {LBL} valid from Time of Week (Tow) as integer: ", end="")
    val = input() or "259200"
    tows.append(val2bytes(int(val), U4))

version = val2bytes(1, U1)
numKeys = val2bytes(numkeys, U1)
RESERVED0 = b"\x00\x00"
RESERVED1 = b"\x00"

payload = version + numKeys + RESERVED0
for i in range(numkeys):
    payload += RESERVED1 + keylens[i] + wnos[i] + tows[i]
for i in range(numkeys):
    payload += keys[i]

print("Formatting UBX RXM-SPARTN-KEY message...\n")
msg = UBXMessage("RXM", "RXM-SPARTN-KEY", SET, payload=payload)
print(msg)
print("\n")
print(msg.serialize())
msg1 = UBXReader.parse(msg.serialize())
CHECKED = str(msg) == str(msg1)
print(f"\nCheck message formatted correctly: {'PASS' if CHECKED else 'FAIL'}")

if not CHECKED:
    sys.exit()

print("Do you want to send this message to the receiver? (y/n) ", end="")
val = input() or "n"

if val == "y":
    print("Enter receiver port: (dev/ttyACM1) ", end="")
    val = input() or "/dev/ttyACM1"
    port = val
    print("Enter receiver baud rate: (9600) ", end="")
    val = input() or "9600"
    baudrate = int(val)
    print("Enter receiver timeout: (3) ", end="")
    val = input() or "3"
    timeout = int(val)

    print(f"Sending message to {port}@{baudrate}...\n")
    try:
        with Serial(port, baudrate, timeout=timeout) as serial:
            serial.write(msg.serialize())
            print("Message sent")
    except (SerialException) as err:
        print(f"\nError sending message! {err}")

print(
    "\nTo make this message a PyGPSClient user preset, the following",
    "\nstring can be cut-and-pasted into PyGPSClient's ubxpresets file:\n",
)
print(f"Send RXM-SPARTN-KEY, RXM, RXM-SPARTN-KEY, {msg.payload.hex()}, 1")
