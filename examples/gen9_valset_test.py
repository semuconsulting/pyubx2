#!/usr/bin/env python3
"""
Demo example to test CFG-VALSET ublox message - generation 9

@author: mgesteiro
"""
import sys
import time
from serial import Serial, SerialException, SerialTimeoutException
from pyubx2 import (
    UBXMessage,
    GET,
    SET,
    VALSET_RAM,
    UBXMessageError,
    UBXTypeError,
    UBXParseError,
)


def message_valsetuart1baudrate_set(baudrate):
    """
    Function to generate a CFG-VALSET CFG-UART1-BAUDRATE set UBX message
    """
    # https://www.u-blox.com/en/docs/UBX-18010854#page=86&zoom=auto,-74,499
    # CFG-UART1-BAUDRATE Key = 0x40520001
    return UBXMessage(
        "CFG",
        "CFG-VALSET",
        SET,
        payload=b"\x00"
        + VALSET_RAM  # version
        + int(0).to_bytes(2, byteorder="little", signed=False)  # layers
        + 0x40520001 .to_bytes(4, byteorder="little", signed=False)  # reserved0
        + baudrate.to_bytes(4, byteorder="little", signed=False),  # key  # value
    )


def message_valsetuart1baudrate_response():
    """
    Function to generate a ACK-ACK-ACK UBX message
    """
    # https://www.u-blox.com/en/docs/UBX-18010854#page=52&zoom=auto,-74,379
    return UBXMessage("ACK", "ACK-ACK", GET, clsID=0x06, msgID=0x8A)


if __name__ == "__main__":

    PORTNAME = "/dev/tty.usbserial-A50285BI"
    BAUDRATE = 230400

    try:

        print("\nBuilding CFG-UART1-BAUDRATE VALSET message:")
        msg = message_valsetuart1baudrate_set(BAUDRATE)

        print(f"  GENERATED: {msg.serialize().hex()}")
        print(
            "  EXPECTED:  b562068a0c00000100000100524000840300b7ef"
            + " (Note: valid for 230400 baudrate)"
        )
        print(f"  {msg}\n")

        print(f"This demo will now set your module's UART1 to {BAUDRATE} (only in RAM)")
        try:
            input("press <ENTER> to continue, CTRL-C to abort!\n")
        except KeyboardInterrupt:
            print("\nExecution aborted.\n")
            sys.exit(0)

        sport = Serial(PORTNAME, BAUDRATE, timeout=2)
        time.sleep(0.250)  # stabilize

        print(
            f"Sending set message to {PORTNAME} at {BAUDRATE} "
            + "(edit the code to change these values)\n"
        )
        sport.flushInput()
        sport.write(msg.serialize())

        print("Receiving response ...")
        raw = sport.read(512)

        START = raw.find(b"\xB5\x62")
        data = raw[START : START + 10]  # expected ACK
        msg = message_valsetuart1baudrate_response()

        print(f"  RECEIVED: {data.hex()}")
        print(f"  EXPECTED: {msg.serialize().hex()}")
        print(f"  {UBXMessage.parse(data)}\n")

    except (
        UBXMessageError,
        UBXTypeError,
        UBXParseError,
        SerialException,
        SerialTimeoutException,
    ) as err:
        print(f"Something broke 💥🤷‍♂️: {err}\n")
