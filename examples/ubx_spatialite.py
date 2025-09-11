"""
ubx_spatialite.py

Simple example script illustrating how to create a
sqlite3 database with the spatialite extension enabled
and load geometry (lat/lon/height) data from a binary
UBX NAV-PVT data log into it using pyubx2.

*************************************************************
NB: Although sqlite3 is a native Python 3 module,
the version of sqlite3 which comes as standard on most
Unix-like platforms (Linux & MacOS) does NOT support
the loading of extensions (e.g. mod_spatialite). It
may be necessary to install or compile a special version
of Python with the --enable-loadable-sqlite-extensions option
set.
*************************************************************

gpsdata example table has the following fields:
    pk integer
    geom POINTZ
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

# path to input file containing binary UBX NAV-PVT data
INFILE = "pygpsdata_NAVPVT.log"

# path to spatialite database
DB = "gnss.sqlite"
DBPATH = path.join("/home/myuser/Downloads/maps", DB)
TABLE = "gpsdata"

# path to mod_spatialite module in QGIS binaries, if required
# SLPATH = "C:/Program Files/QGIS 3.44.1/bin"
# environ["PATH"] = SLPATH + ";" + environ["PATH"]

SQLBEGIN = "BEGIN TRANSACTION;"
SQLCOMMIT = "COMMIT;"

# CREATE SQL statement with 3D POINT
SQLC1 = (
    "BEGIN TRANSACTION;"
    "DROP TABLE IF EXISTS {table};"
    "CREATE TABLE {table} (id INTEGER PRIMARY KEY, source TEXT, time INTEGER, fixtype INTEGER, difftype INTEGER, dop DECIMAL, hacc DECIMAL);"
    "SELECT AddGeometryColumn('gpsdata', 'geom', 4326, 'POINT', 'XYZ');"
    "SELECT CreateSpatialIndex('gpsdata', 'geom');"
    "COMMIT;"
)

# INSERT SQL statement with 3D POINT (lon, lat, height)
SQLI3D = (
    "INSERT INTO {table} (source, time, fixtype, difftype, dop, hacc, geom) "
    "VALUES ('{source}', {time}, {fixtype}, {difftype}, {dop}, {hacc}, GeomFromText('POINTZ({lon} {lat} {height})', 4326));"
)


def create_database(con, cur):
    """
    Create spatial database.
    """

    # load spatialite extension to support spatial (geometry) attributes
    print("Enabling extension loading")
    try:
        con.enable_load_extension(True)
    except AttributeError as err:
        raise AttributeError(
            "Your Python installation does not support sqlite3 extensions"
        ) from err
    print("Loading mod_spatialite extension")
    con.load_extension("mod_spatialite")
    print("Initialising spatial metadata (may take a few seconds)")
    con.execute("SELECT InitSpatialMetaData();")
    # create database table
    print(f"Creating {TABLE} table")
    cur.executescript(SQLC1.format(table=TABLE))


def load_data(con, cur):
    """
    Load data into database.
    """

    # iterate through UBX data log
    print(f"Loading data into {TABLE} from UBX data log")
    i = 0
    cur.execute(SQLBEGIN)
    with open(INFILE, "rb") as stream:
        ubr = UBXReader(stream, protfilter=UBX_PROTOCOL, quitonerror=ERR_LOG)
        for raw, parsed in ubr:
            if parsed.identity == "NAV-PVT":
                sql = SQLI3D.format(
                    table=TABLE,
                    source=parsed.identity,
                    time=parsed.iTOW,
                    fixtype=parsed.fixType,
                    difftype=parsed.carrSoln,
                    dop=parsed.pDOP,
                    hacc=parsed.hAcc,
                    lon=parsed.lon,
                    lat=parsed.lat,
                    height=parsed.hMSL / 1000,  # meters
                )
                cur.execute(sql)
                i += 1
    cur.execute(SQLCOMMIT)
    print(f"{i} records loaded into {TABLE}")


if __name__ == "__main__":

    # create & connect to the database
    print(f"Connecting to database {DBPATH}")
    with sqlite3.connect(DBPATH) as con:
        cur = con.cursor()
        create_database(con, cur)
        load_data(con, cur)
    print("Complete")
