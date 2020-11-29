#!/usr/bin/env python3
"""
Demo example to test CFG-VALGET ublox message - generation 9

@author: mgesteiro
"""
import time
from serial import Serial, SerialException, SerialTimeoutException
from pyubx2 import (
    UBXMessage,
    GET,
    POLL,
    VALGET_RAM,
    UBXMessageError,
    UBXTypeError,
    UBXParseError,
)


def message_valgetuart1baudrate_poll():
    """
    Function to generate a CFG-VALGET CFG-UART1-BAUDRATE poll UBX message
    """
    # https://www.u-blox.com/en/docs/UBX-18010854#page=84&zoom=auto,-70,114
    # CFG-UART1-BAUDRATE Key = 0x40520001
    return UBXMessage(
        "CFG",
        "CFG-VALGET",
        POLL,
        payload=b"\x00"
        + VALGET_RAM  # version
        + int(0).to_bytes(2, byteorder="little", signed=False)  # layers
        + 0x40520001 .to_bytes(4, byteorder="little", signed=False),  # position  # key
    )


def message_valgetuart1baudrate_response(baudrate):
    """
    Function to generate a CFG-VALGET CFG-UART1-BAUDRATE get UBX message
    """
    # https://www.u-blox.com/en/docs/UBX-18010854#page=85&zoom=auto,-70,169
    # CFG-UART1-BAUDRATE Key = 0x40520001
    return UBXMessage(
        "CFG",
        "CFG-VALGET",
        GET,
        payload=b"\x01"
        + VALGET_RAM  # version
        + int(0).to_bytes(2, byteorder="little", signed=False)  # layers
        + 0x40520001 .to_bytes(4, byteorder="little", signed=False)  # position
        + baudrate.to_bytes(4, byteorder="little", signed=False),  # key  # value
    )


if __name__ == "__main__":

    PORTNAME = "/dev/tty.usbserial-A50285BI"
    BAUDRATE = 230400

    try:

        print("\nBuilding CFG-UART1-BAUDRATE VALGET poll message:")
        msg = message_valgetuart1baudrate_poll()

        print(f"  GENERATED: {msg.serialize().hex()}")
        print("  EXPECTED:  b562068b080000000000010052402c79")
        print(f"  {msg}\n")

        sport = Serial(PORTNAME, BAUDRATE, timeout=2)
        time.sleep(0.250)  # stabilize

        print(f"Sending poll message to {PORTNAME} at {BAUDRATE}\n")
        sport.flushInput()
        sport.write(msg.serialize())

        print("Receiving response ...")
        raw = sport.read(512)

        START = raw.find(b"\xB5\x62")
        data = raw[START : START + 20]
        msg = message_valgetuart1baudrate_response(BAUDRATE)

        print(f"  RECEIVED: {data.hex()}")
        print(f"  EXPECTED: {msg.serialize().hex()}")
        print(f"  {msg}\n")

    except (
        UBXMessageError,
        UBXTypeError,
        UBXParseError,
        SerialException,
        SerialTimeoutException,
    ) as err:
        print(f"Something broke 💥🤷‍♂️: {err}\n")
