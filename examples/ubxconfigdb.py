"""
ubxconfigdb.py

This example illustrates how to send UBX configuration database
commands (CFG-VALSET & CFG-VALDEL) to a receiver while simultaneously
reading CFG-VALGET responses and  acknowledgements from the receiver.

python3 ubxconfigdb.py port="/dev/ttyACM0" baudrate=38400 timeout=0.1

You can use any of the configuration database keys defined in
UBX_CONFIG_DATABASE.

NB: IF YOU'RE MODIFYING PARAMETERS RELATING TO THE DEVICE'S SERIAL
PORT CONFIGURATION (E.G. "CFG_UART1_BAUDRATE"), YOU WILL NEED
TO DISCONNECT THE DEVICE AND RECONNECT USING THE UPDATED SERIAL
CONFIGURATION BEFORE MAKING ANY FURTHER CONFIGURATION CHANGES.

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

from queue import Queue
from sys import argv
from threading import Event, Thread
from time import sleep

from serial import Serial

from pyubx2 import (
    POLL_LAYER_BBR,
    POLL_LAYER_RAM,
    SET_LAYER_BBR,
    UBX_PROTOCOL,
    UBXMessage,
    UBXReader,
)

# example configuration database keys and values
# you could use any of the available keys in UBX_CONFIG_DATABASE
# provided they are appropriate for your particular device
# BUT note proviso above re. changing serial port configuration

CONFIG_KEY1 = "CFG_MSGOUT_UBX_MON_COMMS_UART1"
CONFIG_VAL1 = 1
CONFIG_KEY2 = "CFG_MSGOUT_UBX_MON_TXBUF_UART1"
CONFIG_VAL2 = 1


def io_data(
    ubr: UBXReader,
    readqueue: Queue,
    sendqueue: Queue,
    stop: Event,
):
    """
    THREADED
    Read and parse inbound UBX data and place
    raw and parsed data on queue.

    Send any queued outbound messages to receiver.
    """
    # pylint: disable=broad-exception-caught

    while not stop.is_set():
        try:
            (raw_data, parsed_data) = ubr.read()
            if parsed_data:
                readqueue.put((raw_data, parsed_data))

            # refine this if outbound message rates exceed inbound
            while not sendqueue.empty():
                data = sendqueue.get(False)
                if data is not None:
                    ubr.datastream.write(data.serialize())
                sendqueue.task_done()

        except Exception as err:
            print(f"\n\nSomething went wrong - {err}\n\n")
            continue


def process_data(queue: Queue, stop: Event):
    """
    THREADED
    Get UBX data from queue and display.
    """

    while not stop.is_set():
        if queue.empty() is False:
            (_, parsed) = queue.get()
            print(parsed)
            queue.task_done()


def main(**kwargs):
    """
    Main Routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 0.1))
    read_queue = Queue()
    send_queue = Queue()
    stop_event = Event()

    with Serial(port, baudrate, timeout=timeout) as stream:
        # create UBXReader instance, reading only UBX messages
        ubxreader = UBXReader(stream, protfilter=UBX_PROTOCOL)

        stop_event.clear()
        io_thread = Thread(
            target=io_data,
            args=(
                ubxreader,
                read_queue,
                send_queue,
                stop_event,
            ),
            daemon=True,
        )
        process_thread = Thread(
            target=process_data,
            args=(
                read_queue,
                stop_event,
            ),
            daemon=True,
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        # proceed until user presses Ctrl-C
        while not stop_event.is_set():
            try:

                # STEP 1: poll the existing configuration in volate memory (for comparison)
                print(
                    "\nPolling UART configuration in the volatile RAM memory layer via CFG-VALGET..."
                )
                print("(This should result in ACK-ACK and CFG-VALGET responses)")
                position = 0
                layer = POLL_LAYER_RAM  # volatile memory
                keys = [CONFIG_KEY1, CONFIG_KEY2]
                msg = UBXMessage.config_poll(layer, position, keys)
                send_queue.put(msg)
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
                send_queue.put(msg)
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
                send_queue.put(msg)
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
                send_queue.put(msg)
                sleep(2)

                # STEP 5: unset (delete) the previously-set configuration in the non-volatile memory layer
                print(
                    "\nUnsetting UART configuration in the BBR memory layer via CFG-VALDEL...",
                    "\n(This should result in an ACK-ACK response)",
                )
                layers = SET_LAYER_BBR
                keys = [CONFIG_KEY1, CONFIG_KEY2]
                msg = UBXMessage.config_del(layers, transaction, keys)
                send_queue.put(msg)
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
                send_queue.put(msg)
                sleep(2)
                print("\nCommands sent. Waiting for any final acknowledgements...\n")
                sleep(2)
                stop_event.set()
                print("\nStop signal set. Waiting for threads to complete...")

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
