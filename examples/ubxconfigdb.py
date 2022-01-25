"""
ubxconfigdb.py

This example illustrates a simple implementation of a
threaded UBXMessage configuration database utility using
the newer CFG-VALGET, CFG-VALSET and CFG-VALDEL configuration
database message types.

You can use any of the configuration database keys defined in
UBX_CONFIG_DATABASE.

NB: These will only work on Generation 9+ devices (e.g. NEO-M9N,
UBX protocol 23.01 or later).

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a series of CFG-VAL* commands to
the device to set and unset the baud rates on the UART1 and UART2 ports.

The read thread reads and parses any responses and outputs
them to the terminal.

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
    POLL_LAYER_RAM,
    POLL_LAYER_BBR,
    SET_LAYER_BBR,
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

    # example configuration database keys and values
    # you could use any of the available keys in UBX_CONFIG_DATABASE
    # provided they are appropriate for your particular device
    CONFIG_KEY1 = "CFG_MSGOUT_UBX_MON_COMMS_USB"
    CONFIG_VAL1 = 1
    CONFIG_KEY2 = "CFG_MSGOUT_UBX_MON_TXBUF_UART1"
    CONFIG_VAL2 = 1

    with Serial(port, baudrate, timeout=timeout) as serial:

        # create UBXReader instance, reading only UBX messages
        ubr = UBXReader(BufferedReader(serial), protfilter=2)

        print("\nStarting read thread...\n")
        reading = True
        serial_lock = Lock()
        read_thread = start_thread(serial, serial_lock, ubr)

        # STEP 1: poll the existing configuration in volate memory (for comparison)
        print(
            "\nPolling UART configuration in the volatile RAM memory layer via CFG-VALGET..."
        )
        print("(This should result in ACK-ACK and CFG-VALGET responses)")
        position = 0
        layer = POLL_LAYER_RAM  # volatile memory
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_poll(layer, position, keys)
        send_message(serial, serial_lock, msg)
        sleep(1)

        # STEP 2: poll the existing configuration in non-volatile memory (battery-backed RAM or BBR)
        print(
            "\nPolling UART configuration in the BBR memory layer via CFG-VALGET...",
            "\n(This should result in an ACK-NAK response in the ",
            "absence of an existing BBR configuration setting)",
        )
        layer = POLL_LAYER_BBR
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_poll(layer, position, keys)
        send_message(serial, serial_lock, msg)
        sleep(1)

        # STEP 3: set the configuration in the non-volatile memory layer
        print(
            "\nSetting UART configuration in the BBR memory layer via CFG-VALSET...",
            "\n(This should result in an ACK-ACK response)",
        )
        transaction = 0
        layers = SET_LAYER_BBR  # *** NB: SET and DEL messages use different memory layer values to POLL ***
        cfgData = [(CONFIG_KEY1, CONFIG_VAL1), (CONFIG_KEY2, CONFIG_VAL2)]
        msg = UBXMessage.config_set(layers, transaction, cfgData)
        send_message(serial, serial_lock, msg)
        sleep(2)

        # STEP 4: poll the newly-set configuration in the non-volatile memory layer
        print(
            "\nPolling UART configuration in the BBR memory layer via CFG-VALGET...",
            "\n(This should result in ACK-ACK and CFG-VALGET responses, provided the",
            "configuration is valid for your particular device)",
        )
        position = 0
        layer = POLL_LAYER_BBR
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_poll(layer, position, keys)
        send_message(serial, serial_lock, msg)
        sleep(2)

        # STEP 5: unset (delete) the previously-set configuration in the non-volatile memory layer
        print(
            "\nUnsetting UART configuration in the BBR memory layer via CFG-VALDEL...",
            "\n(This should result in an ACK-ACK response)",
        )
        layers = SET_LAYER_BBR
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_del(layers, transaction, keys)
        send_message(serial, serial_lock, msg)
        sleep(2)

        # STEP 6: poll the configuration in the non-volatile memory layer
        # to check that the configuration has been removed
        print(
            "\nPolling UART configuration in the BBR memory",
            "layer via CFG-VALGET...",
            "\n(This should result in an ACK-NAK response as the",
            "BBR configuration setting has now been removed)",
        )
        layer = POLL_LAYER_BBR
        keys = ["CFG_UART1_BAUDRATE", "CFG_UART2_BAUDRATE"]
        msg = UBXMessage.config_poll(layer, position, keys)
        send_message(serial, serial_lock, msg)
        sleep(2)

        print("\nCommands sent. Waiting for any final acknowledgements...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        reading = False
        read_thread.join()
        print("\nProcessing Complete")
