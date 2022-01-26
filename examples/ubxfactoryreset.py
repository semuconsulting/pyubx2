"""
ubxfactoryreset.py

This example illustrates a simple implementation of a
'pseudo-concurrent'threaded UBXMessage factory reset utility.

(NB: Since Python implements a Global Interpreter Lock (GIL),
threads are not truly concurrent.)

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a factory reset command CFG-CFG.

The read thread picks up any acknowledgement and outputs
it to the terminal.

Created on 2 Oct 2020

@author: semuadmin
"""
# pylint: disable=invalid-name

from sys import platform
from io import BufferedReader
from threading import Thread, Lock
from time import sleep
from serial import Serial
from pyubx2 import UBXMessage, UBXReader, SET

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

        # send the factory reset command CFG-CFG
        print("\nSending factory reset command CFG-CFG...\n")
        msg = UBXMessage(
            "CFG",
            "CFG-CFG",
            SET,
            clearMask=b"\x1f\x1f\x00\x00",  # clear everything
            loadMask=b"\x1f\x1f\x00\x00",  # reload everything
            devBBR=1,  # clear from battery-backed RAM
            devFlash=1,  # clear from flash memory
            devEEPROM=1,  # clear from EEPROM memory
        )
        send_message(serial, serial_lock, msg)

        print("\nFactory reset command sent. Waiting for acknowledgement...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        reading = False
        read_thread.join()
        print("\nProcessing Complete")
