"""
ubxpoller2.py

This example illustrates a permutation of 'pseudo-concurrent'
threaded read and write UBX message processing using
queues to pass messages between threads.

NB: Since Python implements a Global Interpreter Lock (GIL),
threads are not truly concurrent. True concurrency could be
achieved using multiprocessing (i.e. separate interpreter
processes rather than threads) but this is non-trivial in
this context as serial streams cannot be shared between
processes. A discrete hardware I/O process must be implemented
e.g. using RPC server techniques.

Created on 07 Aug 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

from sys import platform
from threading import Thread, Event, Lock
from multiprocessing import Queue
from time import sleep
from serial import Serial
from pyubx2 import UBXReader, UBXMessage, POLL, UBX_PROTOCOL


def read_data(
    stream: object,
    ubr: UBXReader,
    queue: Queue,
    lock: Lock,
    stop: Event,
):
    """
    Read and parse incoming UBX data and place
    raw and parsed data on queue
    """
    # pylint: disable=unused-variable, broad-except

    while not stop.is_set():

        if stream.in_waiting:
            try:
                lock.acquire()
                (raw_data, parsed_data) = ubr.read()
                lock.release()
                if parsed_data:
                    queue.put((raw_data, parsed_data))
            except Exception as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                continue


def write_data(stream: object, queue: Queue, lock: Lock, stop: Event):
    """
    Read queue and send UBX message to device
    """

    while not stop.is_set():

        if queue.empty() is False:
            lock.acquire()
            message = queue.get()
            lock.release()
            stream.write(message.serialize())


def display_data(queue: Queue, stop: Event):
    """
    Get UBX data from queue and display.
    """
    # pylint: disable=unused-variable,

    while not stop.is_set():

        if queue.empty() is False:
            (raw, parsed) = queue.get()
            print(parsed)


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

    with Serial(port, baudrate, timeout=timeout) as serial_stream:

        ubxreader = UBXReader(serial_stream, protfilter=UBX_PROTOCOL)

        serial_lock = Lock()
        read_queue = Queue()
        send_queue = Queue()
        stop_event = Event()

        read_thread = Thread(
            target=read_data,
            args=(
                serial_stream,
                ubxreader,
                read_queue,
                serial_lock,
                stop_event,
            ),
        )
        write_thread = Thread(
            target=write_data,
            args=(
                serial_stream,
                send_queue,
                serial_lock,
                stop_event,
            ),
        )
        display_thread = Thread(
            target=display_data,
            args=(
                read_queue,
                stop_event,
            ),
        )

        print("\nStarting handler processes. Press Ctrl-C to terminate...")
        read_thread.start()
        write_thread.start()
        display_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # poll the receiver port configuration using CFG-PRT
                print("\nPolling port configuration CFG-PRT...\n")
                for prt in (0, 1, 2, 3, 4):  # I2C, UART1, UART2, USB, SPI
                    msg = UBXMessage("CFG", "CFG-PRT", POLL, portID=prt)
                    send_queue.put(msg)
                    sleep(1)
                sleep(5)

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        read_thread.join()
        write_thread.join()
        display_thread.join()
        print("\nProcessing complete")
