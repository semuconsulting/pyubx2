"""
Simple CLI utility which creates a GPX track file
from a binary UBX/NMEA dump, such as that created by
PyGPSClient or u-Center datalogging facility.

usage: gpxtracker.py [-h] -I INFILE [-O OUTPATH]

Input must be a binary file containing any combination of
UBX (NAV-PVT, NAV-POSLLH or NAV-HPPOSLLH) and NMEA
(GNGGA, GNRMC or GNGLL) messages. If the message doesn't
include an explicit date, the utility will use today's date
in conjunction with the message iTOW.

There are a number of free online GPX viewers
e.g. https://maplorer.com/view_gpx.html

Could have used minidom for XML but didn't seem worth it.

Created on 27 Oct 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

import os
from argparse import ArgumentParser
from datetime import date, datetime
from time import strftime

import pynmeagps.exceptions as nme
from pynmeagps import NMEAMessage

import pyubx2.exceptions as ube
from pyubx2 import VALCKSUM, UBXMessage, UBXReader, itow2utc

XML_HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

GPX_NS = " ".join(
    (
        'xmlns="http://www.topografix.com/GPX/1/1"',
        'creator="pyubx2" version="1.1"',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
        'http://www.topografix.com/GPX/1/1/gpx.xsd"',
    )
)
GITHUB_LINK = "https://github.com/semuconsulting/pyubx2"


class UBXTracker:
    """
    UBXTracker class.
    """

    def __init__(self, infile, outpath="."):
        """
        Constructor.
        """

        self._filename = infile
        self._outpath = outpath
        self._infile = None
        self._trkfname = None
        self._trkfile = None
        self._ubxreader = None

    def run(self):
        """
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        """

        i = 0
        print(f"\nProcessing file {self._filename}...")

        ts = strftime("%Y%m%d%H%M%S")
        trkfname = os.path.join(self._outpath, f"gpxtrack-{ts}.gpx")
        with open(trkfname, "a", encoding="utf-8") as outfile:

            with open(self._filename, "rb") as infile:

                self.write_gpx_hdr(outfile)

                self._ubxreader = UBXReader(infile, validate=VALCKSUM)
                for _, msg in self._ubxreader:
                    try:
                        if isinstance(msg, UBXMessage):
                            if msg.identity == "NAV-PVT":
                                time = (
                                    datetime(
                                        msg.year,
                                        msg.month,
                                        msg.day,
                                        msg.hour,
                                        msg.min,
                                        msg.second,
                                    ).isoformat()
                                    + "Z"
                                )
                                if msg.fixType == 3:
                                    fix = "3d"
                                elif msg.fixType == 2:
                                    fix = "2d"
                                else:
                                    fix = "none"
                                self.write_gpx_trkpnt(
                                    outfile,
                                    msg.lat,
                                    msg.lon,
                                    ele=msg.hMSL / 1000,  # height in meters
                                    time=time,
                                    fix=fix,
                                )
                            elif msg.identity in ("NAV-POSLLH", "NAV-HPPOSLLH"):
                                time = (
                                    date.today().isoformat()
                                    + "T"
                                    + itow2utc(msg.iTOW).isoformat()
                                    + "Z"
                                )
                                self.write_gpx_trkpnt(
                                    outfile,
                                    msg.lat,
                                    msg.lon,
                                    ele=msg.hMSL / 1000,  # height in meters
                                    time=time,
                                )
                        elif isinstance(msg, NMEAMessage):
                            if msg.msgID in ("GGA",):
                                self.write_gpx_trkpnt(
                                    outfile,
                                    msg.lat,
                                    msg.lon,
                                    ele=msg.alt,
                                    time=self.nmeatime2utc(msg.time),
                                )
                            elif msg.msgID in ("RMC", "GLL"):
                                self.write_gpx_trkpnt(
                                    outfile,
                                    msg.lat,
                                    msg.lon,
                                    time=self.nmeatime2utc(msg.time),
                                )
                        i += 1
                    except (
                        nme.NMEAMessageError,
                        nme.NMEATypeError,
                        nme.NMEAParseError,
                        ube.UBXMessageError,
                        ube.UBXTypeError,
                        ube.UBXParseError,
                    ) as err:
                        print(f"Something went wrong {err}")
                        continue

                self.write_gpx_tlr(outfile)

        print(f"\n{i} NAV message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {trkfname}")
        print("\nOperation Complete")

    def nmeatime2utc(self, time: datetime) -> str:
        """
        Convert NMEA time to GPX datetime format.
        """

        return f"{date.today().isoformat()}T{time.isoformat()}Z"

    def write_gpx_hdr(self, outfile):
        """
        Write GPX track header tags
        """

        dat = datetime.now().isoformat() + "Z"
        gpxtrack = (
            XML_HDR + "<gpx " + GPX_NS + ">"
            f"<metadata>"
            f'<link href="{GITHUB_LINK}"><text>pyubx2</text></link><time>{dat}</time>'
            "</metadata>"
            "<trk><name>GPX track from UBX NAV-PVT datalog</name><trkseg>"
        )

        outfile.write(gpxtrack)

    def write_gpx_trkpnt(self, outfile, lat: float, lon: float, **kwargs):
        """
        Write GPX track point from NAV-PVT message content
        """

        trkpnt = f'<trkpt lat="{lat}" lon="{lon}">'

        # these are the permissible elements in the GPX schema for wptType
        # http://www.topografix.com/GPX/1/1/#type_wptType
        for tag in (
            "ele",
            "time",
            "magvar",
            "geoidheight",
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "sym",
            "type",
            "fix",
            "sat",
            "hdop",
            "vdop",
            "pdop",
            "ageofdgpsdata",
            "dgpsid",
            "extensions",
        ):
            if tag in kwargs:
                val = kwargs[tag]
                trkpnt += f"<{tag}>{val}</{tag}>"

        trkpnt += "</trkpt>"

        outfile.write(trkpnt)

    def write_gpx_tlr(self, outfile):
        """
        Write GPX track trailer tags
        """

        gpxtrack = "</trkseg></trk></gpx>"
        outfile.write(gpxtrack)


def main():
    """
    CLI entry point.
    """

    ap = ArgumentParser()
    ap.add_argument("-I", "--infile", required=True, help="Input gnss file", type=str)
    ap.add_argument(
        "-O", "--outpath", required=False, help="Output path", default=".", type=str
    )
    args = ap.parse_args()

    UBXTracker(args.infile, args.outpath).run()


if __name__ == "__main__":

    main()
