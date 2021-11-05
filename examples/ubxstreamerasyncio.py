"""
Example implementation of a threaded UBXMessage streamer using asyncio.
Depends on python modules pySerial-asyncio and pyserial.

Connects to the receiver's serial port and sets up a
threaded asyncio process. With this process running
in the background, it polls the current PRT, USB, NMEA and MSG
configuration.

You should see the poll responses in the input stream,
or an ACK-NAK (Not Acknowledged) message if that
particular CFG-MSG type is not supported by the receiver.

Created on 05 Nov 2021

@author: Hadatko
"""

import threading
import time
import pyubx2
import asyncio
import serial_asyncio

CFGMESSAGES = [
    "CFG-ANT",
    "CFG-BATCH",
    "CFG-CFG",
    "CFG-DAT",
    "CFG-DGNSS",
    "CFG-DOSC",
    "CFG-DYNSEED",
    "CFG-ESFALG",
    "CFG-ESFA",
    "CFG-ESFG",
    "CFG-ESFWT",
    "CFG-ESRC",
    "CFG-FIXSEED",
    "CFG-GEOFENCE",
    "CFG-GNSS",
    "CFG-HNR",
    "CFG-INF",
    "CFG-ITFM",
    "CFG-LOGFILTER",
    "CFG-MSG",
    "CFG-NAV5",
    "CFG-NAVX5",
    "CFG-NMEA",
    "CFG-ODO",
    "CFG-PM2",
    "CFG-PMS",
    "CFG-PRT",
    "CFG-PWR",
    "CFG-RATE",
    "CFG-RINV",
    "CFG-RST",
    "CFG-RXM",
    "CFG-SBAS",
    "CFG-SENIF",
    "CFG-SLAS",
    "CFG-SMGR",
    "CFG-SPT",
    "CFG-TMODE2",
    "CFG-TMODE3",
    "CFG-TP5",
    "CFG-TXSLOT",
    "CFG-USB",
]

class GNSSDataReader(asyncio.Protocol):
    '''
    This class is implementing asyncio.Protocol functionality to read data from
    GNSS device once ready.
    '''

    reading = b''
    HEADERLEN = 6
    TRAILINGMSGLEN = 2
    cb = None
    readerReady = None

    def __init__(self):
        self.readerReady = threading.Event()

    def setCb(self, cb):
        '''
        Assign cb function for parsed data.
        '''

        self.cb = cb

    def connection_made(self, transport):
        '''
        When connection is made set flag to inform app that we are ready to read data.
        '''

        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        self.readerReady.set()

    def data_received(self, data):
        '''
        On data received from transport serialize and parse them.
        '''

        global DEBUG_LOG

        try:
            while True:
                #print(f'Data received from {self.transport.serial.port}: {data.hex()}')

                #concatenate msg
                if len(self.reading) == 0:
                    for byteIdx in range(len(data)):
                        if data[byteIdx] == pyubx2.UBX_HDR[0]:
                            self.reading = data[byteIdx:]
                            break
                else:
                    self.reading += data

                redingLen = len(self.reading) # get new size of self.reading
                if redingLen >= self.HEADERLEN:
                    if self.reading[1] == pyubx2.UBX_HDR[1]:
                        rawMsgSize = int.from_bytes(self.reading[4:6], "little", signed=False)+self.TRAILINGMSGLEN+self.HEADERLEN
                        if redingLen >= rawMsgSize:
                            rawMsg = self.reading[:rawMsgSize]
                            parsedMsg = pyubx2.ubxreader.UBXReader.parse(rawMsg)
                            if self.cb:
                                self.cb(rawMsg, parsedMsg)
                            else:
                                print(parsedMsg)
                            data = self.reading[rawMsgSize:]
                            self.reading = b''
                        else:
                            break
                    else:
                        data = self.reading[1:]
                else:
                    break
        except Exception as e:
            print(f"Something went wrong: {e} \nMSG: {self.reading}")
            self.reading = b''

    def connection_lost(self, exc):
        '''
        When connection is lost, set flag to inform rest of app.
        '''

        self.readerReady.clear()
        print('port closed')
        self.transport.loop.stop()

    def waitForRead(self, time):
        self.readerReady.wait(time)

class UBXStreamer:
    """
    UBXStreamer class.
    """

    received_data_loop = None
    def __init__(self, port, baudrate):
        """
        Constructor.
        """

        self._serial_object = None
        self._serial_thread = None
        self._serial_data_loop = None
        self._serial_data_protocol = None
        self._port = port
        self._baudrate = baudrate
        self.received_data_lock = threading.Lock()

    def __del__(self):
        """
        Destructor.
        """

        self.stop_read_thread()

    def start_read_thread(self):
        """
        Start the serial reader thread.
        """

        self._serial_thread = threading.Thread(target=self._read_thread, daemon=True)
        self._serial_thread.start()
        if self._serial_data_protocol.waitForRead(5) == False:
            print("Thread is not ready for reading data.")
            exit()

    def stop_read_thread(self):
        """
        Stop the serial reader thread.
        """

        if self._serial_thread is not None:
            self._serial_data_loop.stop()

    def send(self, data):
        """
        Send data to serial connection.
        """

        self._serial_object.write(data)

    def _receiveDataCb(self, rawData, parsedData):
        '''
        receive data cb
        '''

        with self.received_data_lock:
            print(f"Parsed data{parsedData}") # can be replaced with pushing to list and reading in other thread.

    def _read_thread(self):
        """
        THREADED PROCESS
        Reads and parses UBX message data from stream
        """

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = serial_asyncio.create_serial_connection(loop, GNSSDataReader, self._port, baudrate=self._baudrate)
        transport, protocol = loop.run_until_complete(coro)
        self._serial_data_protocol = protocol
        self._serial_object = transport
        self._serial_data_loop = loop
        self._serial_data_protocol.setCb(self._receiveDataCb)
        loop.run_forever()
        print("read exit")
        loop.close()


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")
    PAUSE = 1

    print("Enter port: ", end="")
    val = input().strip('"')
    prt = val
    print("Enter baud rate (9600): ", end="")
    val = input().strip('"') or "9600"
    baud = int(val)
    print("Enter timeout (0.1): ", end="")
    val = input().strip('"') or "0.1"
    timout = float(val)
    print("Do you want to ignore any non-UBX data (y/n)? (y) ", end="")
    val = input() or "y"
    ubxonly = val in NO

    print("Instantiating UBXStreamer class...")
    ubp = UBXStreamer(prt, baud)
    print(f"Connecting to serial port {prt} at {baud} baud...")
    if ubp.connect():
        print("Starting reader thread...")
        ubp.start_read_thread()

        print("\nPolling receiver configuration...\n")
        # poll the receiver configuration
        print("\nPolling port configuration CFG-PRT...\n")
        for prt in (0, 1, 2, 3, 4):  # I2C, UART1, UART2, USB, SPI
            msg = pyubx2.UBXMessage("CFG", "CFG-PRT", pyubx2.POLL, portID=prt)
            ubp.send(msg.serialize())
            time.sleep(PAUSE)
        # poll all available CFG configuration messages
        print("\nPolling CFG configuration CFG-*...\n")
        for msgtype in CFGMESSAGES:  # ("CFG-USB", "CFG-NMEA", "CFG-NAV5"):
            msg = pyubx2.UBXMessage("CFG", msgtype, pyubx2.POLL)
            ubp.send(msg.serialize())
            time.sleep(PAUSE)

        # poll a selection of current navigation message rates using CFG-MSG
        print("\nPolling navigation message rates CFG-MSG...\n")
        for msgid in pyubx2.UBX_MSGIDS.keys():
            if msgid[0] in (1, 240, 241):  # NAV, NMEA-Standard, NMEA-Proprietary
                msg = pyubx2.UBXMessage("CFG", "CFG-MSG", pyubx2.POLL, payload=msgid)
                ubp.send(msg.serialize())
                time.sleep(1)
        print("\n\nPolling complete, waiting for final responses...\n\n")

        time.sleep(PAUSE)

        print("\n\nStopping reader thread...")
        ubp.stop_read_thread()
        print("Disconnecting from serial port...")
        ubp.disconnect()
        print("Test Complete")
