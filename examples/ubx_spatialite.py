"""
ubx_spatialite.py

Simple example script illustrating how to write parsed UBX GNSS data to
a sqlite3/spatialite database previously created in QGIS.

gnssdata table in gnss.db has the following fields:
    pk integer
    geom POINT
    source text
    time integer
    fixtype integer
    difftype integer
    dop decimal
    hacc decimal

Created on 27 Jul 2023

:author: semuadmin
:copyright: SEMU Consulting © 2023
:license: BSD 3-Clause
"""

import sqlite3
from os import environ, path

from pyubx2 import ERR_LOG, UBX_PROTOCOL, UBXReader

# input file containing binary UBX data
INFILE = "pygpsdata-ubx.log"
# path to spatialite database created using QGIS
DBPATH = path.join("/home/myuser/Downloads/qgis", "gnss.db")
# path to mod_spatialite.so (or .dll) module in QGIS binaries
SLPATH = "/opt/QGIS_3.44.1/bin"
# INSERT SQL statement
SQLI1 = (
    "INSERT INTO gnssdata (source, time, fixtype, difftype, dop, hacc, geom) "
    "VALUES ('{}', {}, {}, {}, {}, {}, GeomFromText('POINT({} {})', 4326));"
)

# ensure spatialite extension module is in PATH
environ["PATH"] = SLPATH + ";" + environ["PATH"]

# connect to the database
con = sqlite3.connect(DBPATH)
cur = con.cursor()
# load spatialite extension to support spatial (geometry) attributes
con.enable_load_extension(True)
con.load_extension("mod_spatialite")
# con.execute("SELECT InitSpatialMetaData();") # already done by QGIS

# iterate through UBX data log
with open(INFILE, "rb") as stream:
    ubr = UBXReader(stream, protfilter=UBX_PROTOCOL, quitonerror=ERR_LOG)
    for raw, parsed in ubr:
        if parsed.identity == "NAV-PVT":
            sql = SQLI1.format(
                parsed.identity,
                parsed.iTOW,
                parsed.fixType,
                parsed.carrSoln,
                parsed.pDOP,
                parsed.hAcc,
                parsed.lon,
                parsed.lat,
            )
            print(sql)
            cur.execute(sql)

con.commit()
con.close()
