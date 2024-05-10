"""
ubxconfigdb.py

This example illustrates how to send UBX configuration database 
commands (CFG-VALSET & CFG-VALDEL) to a receiver while simultaneously
reading CFG-VALGET responses and  acknowledgements from the receiver.

python3 ubxconfigdb.py port="/dev/ttyACM0" baudrate=38400 timeout=0.1

You can use any of the configuration database keys defined in
UBX_CONFIG_DATABASE. 

NB: These will only work on Generation 9+ devices running UBX protocol
23.01 or later (e.g. NEO-M9N or ZED-F9P).

It connects to the receiver's serial port and sets up a
UBXReader read thread. With the read thread running
in the background, it sends a series of CFG-VAL* commands to
the device to apply the designated configuration commands.

The read thread reads and parses any responses and outputs
them to the terminal.

Created on 2 Oct 2020

@author: semuadmin
"""

from sys import argv
from threading import Event, Lock, Thread
from time import sleep

from serial import Serial

from pyubx2 import (
    POLL_LAYER_BBR,
    POLL_LAYER_RAM,
    SET_LAYER_BBR,
    UBXMessage,
    UBXReader,
    UBX_PROTOCOL,
)

# example configuration database keys and values
# you could use any of the available keys in UBX_CONFIG_DATABASE
# provided they are appropriate for your particular device
CONFIG_KEY1 = "CFG_MSGOUT_UBX_MON_COMMS_UART1"
CONFIG_VAL1 = 1
CONFIG_KEY2 = "CFG_MSGOUT_UBX_MON_TXBUF_UART1"
CONFIG_VAL2 = 1


def read_messages(stream, lock, stopevent, ubxreader):
    """
    Reads, parses and prints out incoming UBX messages
    """
    # pylint: disable=unused-variable, broad-except

    while not stopevent.is_set():
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
        serial_lock = Lock()
        stopevent = Event()
        stopevent.clear()
        read_thread = start_thread(stream, serial_lock, stopevent, ubr)

        # STEP 1: poll the existing configuration in volate memory (for comparison)
        print(
            "\nPolling UART configuration in the volatile RAM memory layer via CFG-VALGET..."
        )
        print("(This should result in ACK-ACK and CFG-VALGET responses)")
        position = 0
        layer = POLL_LAYER_RAM  # volatile memory
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_poll(layer, position, keys)
        send_message(stream, serial_lock, msg)
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
        send_message(stream, serial_lock, msg)
        sleep(1)

        # STEP 3: set the configuration in the non-volatile memory layer
        # *** NB: SET and DEL messages use different memory layer values to POLL ***
        print(
            "\nSetting UART configuration in the BBR memory layer via CFG-VALSET...",
            "\n(This should result in an ACK-ACK response)",
        )
        transaction = 0
        layers = SET_LAYER_BBR
        cfgdata = [(CONFIG_KEY1, CONFIG_VAL1), (CONFIG_KEY2, CONFIG_VAL2)]
        msg = UBXMessage.config_set(layers, transaction, cfgdata)
        send_message(stream, serial_lock, msg)
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
        send_message(stream, serial_lock, msg)
        sleep(2)

        # STEP 5: unset (delete) the previously-set configuration in the non-volatile memory layer
        print(
            "\nUnsetting UART configuration in the BBR memory layer via CFG-VALDEL...",
            "\n(This should result in an ACK-ACK response)",
        )
        layers = SET_LAYER_BBR
        keys = [CONFIG_KEY1, CONFIG_KEY2]
        msg = UBXMessage.config_del(layers, transaction, keys)
        send_message(stream, serial_lock, msg)
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
        send_message(stream, serial_lock, msg)
        sleep(2)

        print("\nCommands sent. Waiting for any final acknowledgements...\n")
        sleep(1)
        print("\nStopping reader thread...\n")
        stopevent.set()
        read_thread.join()
        print("\nProcessing Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
