'''
Simple CLI utility which creates a GPX or KML track file
from a binary UBX dump (such as that created by
PyGPSClient's datalogging facility).

Dump must contain UBX NAV-PVT messages.

There are a number of free online GPX/KML viewers
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
            'creator="pyubx2" version="0.2.6"',
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
            'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
            'http://www.topografix.com/GPX/1/1/gpx.xsd"'))
KML_NS = 'xmlns="http://www.opengis.net/kml/2.2"'
GITHUB_LINK = 'https://github.com/semuconsulting/pyubx2'

GPX = 'G'
KML = 'K'


class UBXTracker():
    '''
    UBXTracker class.
    '''

    def __init__(self, infile, outdir, form='g'):
        '''
        Constructor.
        '''

        self._filename = infile
        self._outdir = outdir
        self._infile = None
        self._format = form.upper() if form in ('g', 'k', 'G', 'K') else 'G'
        self._trkfname = None
        self._trkfile = None
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
            ext = 'gpx' if self._format == GPX else 'kml'
            timestamp = strftime("%Y%m%d%H%M%S")
            self._infile = open(self._filename, 'rb')
            self._trkfname = os.path.join(self._outdir, f"{ext}track-{timestamp}.{ext}")
            self._trkfile = open(self._trkfname, 'a')
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
                self._trkfile.close()
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

        if self._format == GPX:
            self._gpx_hdr()
        else:
            self._kml_hdr()

        for (_, msg) in self._ubxreader:  # invokes iterator method
            try:
                if msg.identity == 'NAV-PVT':
                    if self._format == GPX:
                        self._gpx_trkpnt(msg)
                    else:
                        self._kml_trkpnt(msg)
                    i += 1
            except (ube.UBXMessageError, ube.UBXTypeError, ube.UBXParseError) as err:
                print(f"Something went wrong {err}")
                continue

        if self._format == GPX:
            self._gpx_tlr()
        else:
            self._kml_tlr()

        print(f"\n{i} NAV-PVT message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {self._trkfname}")

    def _gpx_hdr(self):
        '''
        Create GPX track header tags
        '''

        date = datetime.now().isoformat() + 'Z'
        gpxtrack = (XML_HDR + '<gpx ' + GPX_NS + '>'
        f'<link href="{GITHUB_LINK}"><text>pyubx2</text></link>'
        f'<metadata><time>{date}</time></metadata>'
        '<trk><name>GPX track from UBX NAV-PVT datalog</name><trkseg>')

        self._trkfile.write(gpxtrack)

    def _gpx_trkpnt(self, msg):
        '''
        Creates GPX track point from NAV-PVT message content
        '''

        date = datetime(msg.year, msg.month, msg.day, msg.hour, \
                        msg.min, msg.second).isoformat() + 'Z'
        trkpnt = (f'<trkpt lat="{msg.lat / 10 ** 7}" lon="{msg.lon / 10 ** 7}">'
        f'<ele>{msg.hMSL / 1000}</ele>'
        f'<fix>{msg.fixType}</fix>'
        f'<sat>{msg.numSV}</sat>'
        f'<pdop>{msg.pDOP}</pdop>'
        f'<speed>{msg.gSpeed / 1000}</speed>'  # unofficial
        f'<time>{date}</time></trkpt>')

        self._trkfile.write(trkpnt)

    def _gpx_tlr(self):
        '''
        Create GPX track trailer tags
        '''

        gpxtrack = '</trkseg></trk></gpx>'
        self._trkfile.write(gpxtrack)

    def _kml_hdr(self):
        '''
        Create KML track header tags
        '''

        kmltrack = (XML_HDR + '<kml ' + KML_NS + '>'
        f'<Document><name><![CDATA[{self._trkfname}]]></name>'
        '<visibility>1</visibility><open>1</open>'
        f'<Snippet><![CDATA[created using <a {GITHUB_LINK}">pyubx2</a>]]></Snippet>'
        '<Folder id="Tracks"><name>KML track from UBX NAV-PVT datalog</name>'
        '<Style id="mystyle"><LineStyle>'
        '<color>e00000ff</color><width>4</width></LineStyle></Style>'
        '<visibility>1</visibility><open>0</open>'
        '<Placemark><name><![CDATA[GPX track from UBX NAV-PVT datalog]]></name>'
        '<styleUrl>#mystyle</styleUrl>'
        '<LineString><tessellate>1</tessellate>'
        '<altitudeMode>clampToGround</altitudeMode><coordinates>')

        self._trkfile.write(kmltrack)

    def _kml_trkpnt(self, msg):
        '''
        Creates KML track point from NAV-PVT message content
        '''

        kmlpnt = f'{msg.lon / 10 ** 7},{msg.lat / 10 ** 7},{msg.hMSL / 1000} '

        self._trkfile.write(kmlpnt)

    def _kml_tlr(self):
        '''
        Create KML track trailer tags
        '''

        kmltrack = '</coordinates></LineString></Placemark></Folder></Document></kml>'
        self._trkfile.write(kmltrack)


if __name__ == "__main__":

    print("UBX datalog to GPX/KML file converter\n")
    infilep = input("Enter input UBX datalog file: ")
    outdirp = input("Enter output directory: ")
    trkform = input("Select g for GPX or k for KML (g): ") or 'g'
    tkr = UBXTracker(infilep, outdirp, trkform)
    print(f"\nProcessing file {infilep}...")
    tkr.open()
    tkr.reader()
    tkr.close()
    print("\nOperation Complete")
