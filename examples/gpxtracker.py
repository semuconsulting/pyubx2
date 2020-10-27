'''
Simple CLI utility which creates a GPX track file
from a binary UBX dump (such as that created by
PyGPSClient's datalogging facility).

Dump must contain UBX NAV-PVT messages.

There are a number of free online GPX viewers
e.g. https://gpx-viewer.com/view

Could have used minidom for XML but didn't seem worth it.

Created on 27 Oct 2020

@author: semuadmin
'''

import os
from datetime import datetime
from time import strftime
from pyubx2.ubxreader import UBXReader
import pyubx2.exceptions as ube

GPX_NS = ' '.join(('xmlns="http://www.topografix.com/GPX/1/1"',
            'creator="pyubx2" version="0.2.6"',
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
            'http://www.topografix.com/GPX/1/1/gpx.xsd"'))

GPX_LINK = '<link href="https://github.com/semuconsulting/pyubx2">' \
            '<text>pyubx2</text></link>'


class UBXTracker():
    '''
    UBXTracker class.
    '''

    def __init__(self, infile, outdir):
        '''
        Constructor.
        '''

        self._filename = infile
        self._outdir = outdir
        self._infile = None
        self._gpxfname = None
        self._gpxfile = None
        self._ubxreader = None
        self._connected = False

    def __del__(self):
        '''
        Destructor.
        '''

        self.close()

    def open(self):
        '''
        Open files.
        '''

        try:
            timestamp = strftime("%Y%m%d%H%M%S")
            self._infile = open(self._filename, 'rb')
            self._gpxfname = os.path.join(self._outdir, f"gpxtrack-{timestamp}.gpx")
            self._gpxfile = open(self._gpxfname, 'a')
            self._connected = True
        except IOError as err:
            print(f"Error opening file {err}")

    def close(self):
        '''
        Close files.
        '''

        if self._connected and self._infile:
            try:
                self._infile.close()
                self._gpxfile.close()
            except IOError as err:
                print(f"Error closing file {err}")
        self._connected = False

    def reader(self, validate=False):
        '''
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        '''

        i = 0
        self._ubxreader = UBXReader(self._infile, validate)

        self._gpx_hdr()

        for (_, msg) in self._ubxreader:  # invokes iterator method
            try:
                if msg.identity == 'NAV-PVT':
                    self._gpx_trkpnt(msg)
                    i += 1
            except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
                print(f"Something went wrong {err}")
                continue

        self._gpx_tlr()

        print(f"\n{i} NAV-PVT message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {self._gpxfname}")

    def _gpx_hdr(self):
        '''
        Create GPX track header tags
        '''

        date = datetime.now().isoformat() + 'Z'
        gpxtrack = '<gpx ' + GPX_NS + '>' + GPX_LINK
        gpxtrack += f'<metadata><time>{date}</time></metadata>'
        gpxtrack += '<trk><name>GPX track from UBX NAV-PVT datalog</name><trkseg>'
        self._gpxfile.write(gpxtrack)

    def _gpx_trkpnt(self, msg):
        '''
        Creates GPX track point from NAV-PVT message content
        '''

        date = datetime(msg.year, msg.month, msg.day, msg.hour, \
                        msg.min, msg.second).isoformat() + 'Z'
        trkpnt = f'<trkpt lat="{msg.lat / 10 ** 7}" lon="{msg.lon / 10 ** 7}">'
        trkpnt += f'<ele>{msg.hMSL / 1000}</ele>'
        trkpnt += f'<fix>{msg.fixType}</fix>'
        trkpnt += f'<sat>{msg.numSV}</sat>'
        trkpnt += f'<pdop>{msg.pDOP}</pdop>'
        trkpnt += f'<speed>{msg.gSpeed / 1000}</speed>'  # unofficial
        trkpnt += f'<time>{date}</time></trkpt>'

        self._gpxfile.write(trkpnt)

    def _gpx_tlr(self):
        '''
        Create GPX track trailer tags
        '''

        gpxtrack = '</trkseg></trk></gpx>'
        self._gpxfile.write(gpxtrack)


if __name__ == "__main__":

    print("UBX datalog to GPX file converter\n")
    infilep = input("Enter input UBX datalog file: ")
    outdirp = input("Enter output directory for GPX file: ")
    tkr = UBXTracker(infilep, outdirp)
    print(f"\nProcessing file {infilep}...")
    tkr.open()
    tkr.reader()
    tkr.close()
    print("\nOperation Complete")
