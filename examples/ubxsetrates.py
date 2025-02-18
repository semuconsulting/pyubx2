"""
ubxsetrates.py

This example illustrates how to send UBX commands to a receiver
(in this case a series of CFG-MSG commands) while simultaneously
reading acknowledgements from the receiver.

Usage:

python3 ubxsetrates.py port="/dev/ttyACM0" baudrate=38400 timout=0.1 rate=4

It implements two threads which run concurrently:
1) an I/O thread which continuously reads UBX data from the
receiver and sends any queued outbound command or poll messages.
2) a process thread which processes parsed UBX data - in this example
it simply prints the parsed data to the terminal.
UBX data is passed between threads using queues.

NB: the rate value means 'per navigation solution' e.g. a rate of
4 means 'every 4th navigation solution', which at a standard solution
interval of 1000ms corresponds to every 4 seconds.

The process thread reads and parses any responses and outputs
them to the terminal. You should also start seeing any incoming
UBX-NAV messages arriving at the designated rate.

The response may be an ACK-ACK acknowledgement message, or an
ACK-NAK message signifying that this particular navigation message
type is not supported by the receiver.

Created on 07 Aug 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

from queue import Queue
from sys import argv
from threading import Event, Thread
from time import sleep

from serial import Serial

from pyubx2 import SET, UBX_MSGIDS, UBX_PROTOCOL, UBXMessage, UBXReader


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
    Main routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 0.1))
    rate = int(kwargs.get("rate", 4))
    read_queue = Queue()
    send_queue = Queue()
    stop_event = Event()

    with Serial(port, baudrate, timeout=timeout) as stream:
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

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # DO STUFF IN THE BACKGROUND...

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
                        print(
                            f"Setting message rate for {msgname} message type to {rate}...\n"
                        )
                        send_queue.put(msg)
                        sleep(1)

                print("\nCommands sent. Waiting for any final acknowledgements...\n")
                sleep(1)

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
