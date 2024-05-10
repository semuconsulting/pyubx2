"""
ubxsetrates.py

This example illustrates how to send UBX commands to a receiver
(in this case a series of CFG-MSG commands) while simultaneously
reading acknowledgements from the receiver.

Usage:

python3 ubxsetrates.py port="/dev/ttyACM0" baudrate=38400 timout=0.1 rate=4

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

from io import BufferedReader
from sys import argv
from threading import Lock, Thread
from time import sleep

from serial import Serial

from pyubx2 import SET, UBX_MSGIDS, UBXMessage, UBXReader

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


def main(**kwargs):
    """
    Main routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 0.1))
    rate = int(kwargs.get("rate", 4))

    with Serial(port, baudrate, timeout=timeout) as serial:
        # create UBXReader instance, reading only UBX messages
        ubr = UBXReader(BufferedReader(serial), protfilter=2)

        print("\nStarting read thread...\n")
        serial_lock = Lock()
        read_thread = start_thread(serial, serial_lock, ubr)

        # set the UART1 and USB message rate for each UBX-NAV message
        # via a CFG-MSG command
        print("\nSending CFG-MSG message rate configuration messages...\n")
        for msgid, msgname in UBX_MSGIDS.items():
            if msgid[0] == 0x01:  # NAV
                msg = UBXMessage(
                    "CFG",
                    "CFG-MSG",
                    SET,
                    msgClass=msgid[0],
                    msgID=msgid[1],
                    rateUART1=rate,
                    rateUSB=rate,
                )
                print(f"Setting message rate for {msgname} message type to {rate}...\n")
                send_message(serial, serial_lock, msg)
                sleep(1)

        print("\nCommands sent. Waiting for any final acknowledgements...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        read_thread.join()
        print("\nProcessing Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
