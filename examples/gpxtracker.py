'''
Simple CLI utility which creates a GPX track file
from a binary UBX dump (such as that created by
PyGPSClient's datalogging facility) using pyubx2.UBXReader().

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

XML_HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

GPX_NS = ' '.join(('xmlns="http://www.topografix.com/GPX/1/1"',
            'creator="pyubx2" version="1.1"',
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
            'http://www.topografix.com/GPX/1/1/gpx.xsd"'))
GITHUB_LINK = 'https://github.com/semuconsulting/pyubx2'


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
        self._trkfname = None
        self._trkfile = None
        self._ubxreader = None
        self._connected = False

    def open(self):
        '''
        Open datalog file.
        '''

        self._infile = open(self._filename, 'rb')
        self._connected = True

    def close(self):
        '''
        Close datalog file.
        '''

        if self._connected and self._infile:
            self._infile.close()

    def reader(self, validate=False):
        '''
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        '''

        i = 0
        self._ubxreader = UBXReader(self._infile, validate)

        self.write_gpx_hdr()

        for (_, msg) in self._ubxreader:  # invokes iterator method
            try:
                if msg.identity == 'NAV-PVT':
                    time = datetime(msg.year, msg.month, msg.day, msg.hour,
                                    msg.min, msg.second).isoformat() + 'Z'
                    if msg.fixType == 3:
                        fix = '3d'
                    elif msg.fixType == 2:
                        fix = '2d'
                    else:
                        fix = 'none'
                    self.write_gpx_trkpnt(msg.lat / 10 ** 7, msg.lon / 10 ** 7,
                                     ele=msg.hMSL / 1000, time=time, fix=fix)
                i += 1
            except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
                print(f"Something went wrong {err}")
                continue

        self.write_gpx_tlr()

        print(f"\n{i} NAV-PVT message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {self._trkfname}")

    def write_gpx_hdr(self):
        '''
        Open gpx file and write GPX track header tags
        '''

        timestamp = strftime("%Y%m%d%H%M%S")
        self._trkfname = os.path.join(self._outdir, f"gpxtrack-{timestamp}.gpx")
        self._trkfile = open(self._trkfname, 'a')

        date = datetime.now().isoformat() + 'Z'
        gpxtrack = (XML_HDR + '<gpx ' + GPX_NS + '>'
        f'<metadata>'
        f'<link href="{GITHUB_LINK}"><text>pyubx2</text></link><time>{date}</time>'
        '</metadata>'
        '<trk><name>GPX track from UBX NAV-PVT datalog</name><trkseg>')

        self._trkfile.write(gpxtrack)

    def write_gpx_trkpnt(self, lat: float, lon: float, **kwargs):
        '''
        Write GPX track point from NAV-PVT message content
        '''

        trkpnt = f'<trkpt lat="{lat}" lon="{lon}">'

        # these are the main permissible elements in the GPX schema for wptType
        # http://www.topografix.com/GPX/1/1/#type_wptType
        for tag in ('ele', 'time', 'magvar', 'geoidheight', 'name', 'cmt', 'desc', 'src',
                    'link', 'sym', 'type', 'fix', 'sat', 'hdop', 'vdop', 'pdop'):
            if tag in kwargs:
                val = kwargs[tag]
                trkpnt += f'<{tag}>{val}</{tag}>'

        trkpnt += '</trkpt>'

        self._trkfile.write(trkpnt)

    def write_gpx_tlr(self):
        '''
        Write GPX track trailer tags and close file
        '''

        gpxtrack = '</trkseg></trk></gpx>'
        self._trkfile.write(gpxtrack)
        self._trkfile.close()


if __name__ == "__main__":

    print("UBX datalog to GPX file converter\n")
    infilep = input("Enter input UBX datalog file: ").strip('\"')
    outdirp = input("Enter output directory: ").strip('\"')
    tkr = UBXTracker(infilep, outdirp)
    print(f"\nProcessing file {infilep}...")
    tkr.open()
    tkr.reader()
    tkr.close()
    print("\nOperation Complete")
