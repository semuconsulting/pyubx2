"""
ubxpoller.py

This example illustrates how to read, write and display UBX messages
"concurrently" using threads and queues. This represents a useful
generic pattern for many end user applications.

It implements two threads which run concurrently:
1) an I/O thread which continuously reads UBX data from the
receiver and sends any queued outbound command or poll messages.
2) a process thread which processes parsed UBX data - in this example
it simply prints the parsed data to the terminal.
UBX data is passed between threads using queues.

Press CTRL-C to terminate.

FYI: Since Python implements a Global Interpreter Lock (GIL),
threads are not strictly concurrent, though this is of minor
practical consequence here. True concurrency could be
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

from queue import Queue
from sys import platform
from threading import Event, Lock, Thread
from time import sleep
from serial import Serial
from pyubx2 import POLL, UBX_PROTOCOL, UBXMessage, UBXReader, UBX_PAYLOADS_POLL


def io_data(
    stream: object,
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
        if stream.in_waiting:
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
                print(f"\n\nSomething went wrong {err}\n\n")
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


if __name__ == "__main__":
    # set port, baudrate and timeout to suit your device configuration
    if platform == "win32":  # Windows
        port = "COM13"
    elif platform == "darwin":  # MacOS
        port = "/dev/tty.usbmodem101"
    else:  # Linux
        port = "/dev/ttyACM1"
    baudrate = 38400
    timeout = 0.1

    DELAY = 1

    with Serial(port, baudrate, timeout=timeout) as serial_stream:
        ubxreader = UBXReader(serial_stream, protfilter=UBX_PROTOCOL)

        serial_lock = Lock()
        read_queue = Queue()
        send_queue = Queue()
        stop_event = Event()

        io_thread = Thread(
            target=io_data,
            args=(
                serial_stream,
                ubxreader,
                read_queue,
                send_queue,
                stop_event,
            ),
        )
        process_thread = Thread(
            target=process_data,
            args=(
                read_queue,
                stop_event,
            ),
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # DO STUFF IN THE BACKGROUND...
                # poll all available NAV messages (receiver will only respond
                # to those NAV message types it supports; responses won't
                # necessarily arrive in sequence)
                count = 0
                for nam in UBX_PAYLOADS_POLL:
                    if nam[0:4] == "NAV-":
                        print(f"Polling {nam} message type...")
                        msg = UBXMessage("NAV", nam, POLL)
                        send_queue.put(msg)
                        count += 1
                        sleep(DELAY)
                stop_event.set()
                print(f"{count} NAV message types polled.")

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")
