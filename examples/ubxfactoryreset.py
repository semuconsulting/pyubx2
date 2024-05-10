"""
ubxfactoryreset.py

This example illustrates how to send a UBX command to a receiver
(in this case a CFG-CFG factory reset command) while
simultaneously reading acknowledgements from the receiver.

Usage:

python3 ubxfactoryreset.py port="/dev/ttyACM0" baudrate=38400 timeout=0.1

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a factory reset command CFG-CFG.

The read thread picks up any acknowledgement and outputs
it to the terminal.

NB: THIS RESETS THE CURRENT CONFIGURATIONS IN ALL MEMORY
LAYERS (BBR, Flash and EEPROM) - USE WITH CAUTION!!

Created on 2 Oct 2020

@author: semuadmin
"""

# pylint: disable=invalid-name

from sys import argv
from threading import Event, Lock, Thread
from time import sleep

from serial import Serial

from pyubx2 import SET, UBX_PROTOCOL, UBXMessage, UBXReader


def read_messages(stream, lock, stopevent, ubxreader):
    """
    Reads, parses and prints out incoming UBX messages
    """
    # pylint: disable=unused-variable, broad-except

    while not stopevent.is_set:
        if stream.in_waiting:
            try:
                lock.acquire()
                _, parsed_data = ubxreader.read()
                lock.release()
                if parsed_data:
                    print(parsed_data)
            except Exception as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                continue


def start_thread(stream, lock, stopevent, ubxreader):
    """
    Start read thread
    """

    thr = Thread(
        target=read_messages, args=(stream, lock, stopevent, ubxreader), daemon=True
    )
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
    Main Routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 0.1))

    with Serial(port, baudrate, timeout=timeout) as stream:

        # create UBXReader instance, reading only UBX messages
        ubr = UBXReader(stream, protfilter=UBX_PROTOCOL)

        print("\nStarting read thread...\n")
        stopevent = Event()
        stopevent.clear()
        serial_lock = Lock()
        read_thread = start_thread(stream, serial_lock, stopevent, ubr)

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
        send_message(stream, serial_lock, msg)

        print("\nFactory reset command sent. Waiting for acknowledgement...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        stopevent.set()
        read_thread.join()
        print("\nProcessing Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
