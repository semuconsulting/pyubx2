"""
ubxsetrates.py

This example illustrates a simple implementation of a
threaded UBXMessage message rate configuration utility.

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a series of CFG-MSG commands to
the device to set the message rate of each UBX-NAV message type to
the designated rate value on the UART1 and USB ports.

NB: the rate value means 'per navigation solution' e.g. a rate of
4 means 'every 4th navigation solution', which at a standard solution
interval of 1000ms corresponds to every 4 seconds.

The read thread reads and parses any responses and outputs
them to the terminal. You should also start seeing any incoming
UBX-NAV messages arriving at the designated rate.

The response may be an ACK-ACK acknowledgement message, or an
ACK-NAK message signifying that this particular navigation message
type is not supported by the receiver.

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
    UBX_MSGIDS,
    SET,
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
    RATE = 4  # set to 0 to disable NAV messages on USB and UART1 ports

    with Serial(port, baudrate, timeout=timeout) as serial:

        # create UBXReader instance, reading only UBX messages
        ubr = UBXReader(BufferedReader(serial), protfilter=2)

        print("\nStarting read thread...\n")
        reading = True
        serial_lock = Lock()
        read_thread = start_thread(serial, serial_lock, ubr)

        # set the UART1 and USB message rate for each UBX-NAV message
        # via a CFG-MSG command
        print("\nSending CFG-MSG message rate configuration messages...\n")
        for (msgid, msgname) in UBX_MSGIDS.items():
            if msgid[0] == 0x01:  # NAV
                msg = UBXMessage(
                    "CFG",
                    "CFG-MSG",
                    SET,
                    msgClass=msgid[0],
                    msgID=msgid[1],
                    rateUART1=RATE,
                    rateUSB=RATE,
                )
                print(
                    f"\nSetting message rate for {msgname} message type to {RATE}...\n"
                )
                send_message(serial, serial_lock, msg)
                sleep(1)

        print("\nCommands sent. Waiting for any final acknowledgements...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        reading = False
        read_thread.join()
        print("\nProcessing Complete")
