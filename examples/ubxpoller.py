"""
ubxpoller.py

This example illustrates a simple implementation of a
'pseudo-concurrent' threaded UBXMessage configuration
polling utility.

(NB: Since Python implements a Global Interpreter Lock (GIL),
threads are not truly concurrent.)

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a variety of CFG POLL
messages to the device. The read thread reads and parses
any responses to these polls and outputs them to the terminal.

The response may be an ACK-ACK acknowledgement message followed
by the poll response itself, or an ACK-NAK message signifying
that this particular configuration message type is not supported
by the receiver.

Created on 2 Oct 2020

@author: semuadmin
"""
# pylint: disable=invalid-name

from sys import platform
from io import BufferedReader
from threading import Thread, Lock
from time import sleep
from serial import Serial
from pyubx2 import (
    UBXMessage,
    UBXReader,
    POLL,
    UBX_MSGIDS,
)

# initialise global variables
reading = False


def read_messages(stream, lock, ubxreader):
    """
    Reads, parses and prints out incoming UBX messages
    """
    # pylint: disable=unused-variable, broad-except

    while reading:
        if stream.in_waiting:
            try:
                lock.acquire()
                (raw_data, parsed_data) = ubxreader.read()
                lock.release()
                if parsed_data:
                    print(parsed_data)
            except Exception as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                continue


def start_thread(stream, lock, ubxreader):
    """
    Start read thread
    """

    thr = Thread(target=read_messages, args=(stream, lock, ubxreader), daemon=True)
    thr.start()
    return thr


def send_message(stream, lock, message):
    """
    Send message to device
    """

    lock.acquire()
    stream.write(message.serialize())
    lock.release()


if __name__ == "__main__":

    # set port, baudrate and timeout to suit your device configuration
    if platform == "win32":  # Windows
        port = "COM13"
    elif platform == "darwin":  # MacOS
        port = "/dev/tty.usbmodem14101"
    else:  # Linux
        port = "/dev/ttyACM1"
    baudrate = 9600
    timeout = 0.1

    with Serial(port, baudrate, timeout=timeout) as serial:

        # create UBXReader instance, reading only UBX messages
        ubr = UBXReader(BufferedReader(serial), protfilter=2)

        print("\nStarting read thread...\n")
        reading = True
        serial_lock = Lock()
        read_thread = start_thread(serial, serial_lock, ubr)

        # poll the receiver port configuration using CFG-PRT
        print("\nPolling port configuration CFG-PRT...\n")
        for prt in (0, 1, 2, 3, 4):  # I2C, UART1, UART2, USB, SPI
            msg = UBXMessage("CFG", "CFG-PRT", POLL, portID=prt)
            send_message(serial, serial_lock, msg)
            sleep(1)

        # poll all available CFG configuration messages
        print("\nPolling CFG configuration CFG-*...\n")
        for (msgid, msgname) in UBX_MSGIDS.items():
            if msgid[0] == 0x06:  # CFG-* configuration messages
                msg = UBXMessage("CFG", msgname, POLL)
                send_message(serial, serial_lock, msg)
                sleep(1)

        # poll a selection of current navigation message rates using CFG-MSG
        print("\nPolling navigation message rates CFG-MSG...\n")
        for (msgid, msgname) in UBX_MSGIDS.items():
            if msgid[0] in (0x01, 0xF0, 0xF1):  # NAV, NMEA-Standard, NMEA-Proprietary
                msg = UBXMessage("CFG", "CFG-MSG", POLL, payload=msgid)
                send_message(serial, serial_lock, msg)
                sleep(1)

        print("\nPolling complete. Pausing for any final responses...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        reading = False
        read_thread.join()
        print("\nProcessing Complete")
