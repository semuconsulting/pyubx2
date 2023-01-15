"""
utilities.py

Illustration of the various utility methods available in pyubx2

Created on 14 Jan 2023

@author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from pyubx2 import latlon2dms, latlon2dmm, ecef2llh, llh2ecef, haversine
from pyubx2.ubxtypes_core import GRS80_EARTH_RADIUS, GRS80_FLATTENING

LAT1, LON1 = 53.24, -2.16
LAT2, LON2 = 53.32, -2.08

print(f"\nConvert {LAT1}, {LON1} to degrees, minutes, seconds ...")
lat, lon = latlon2dms(LAT1, LON1)
print(f"D.M.S = {lat}, {lon}")

print(f"\nConvert {LAT2}, {LON2} to degrees, minutes ...")
lat, lon = latlon2dmm(LAT2, LON2)
print(f"D.MM = {lat}, {lon}")

print(
    f"\nFind spherical distance between {LAT1}, {LON1} and {LAT2}, {LON2} using default WGS84 datum..."
)
dist = haversine(LAT1, LON1, LAT2, LON2)
print(f"Distance: {dist/1000} km")

print(
    f"\nFind spherical distance between {LAT1}, {LON1} and {LAT2}, {LON2} using alternate GRS80 datum..."
)
dist = haversine(LAT1, LON1, LAT2, LON2, GRS80_EARTH_RADIUS / 1000)
print(f"Distance: {dist/1000} km")

X, Y, Z = 3822566.3113, -144427.5123, 5086857.1208
print(f"\nConvert ECEF X: {X}, Y: {Y}, Z: {Z} to geodetic using default WGS84 datum...")
lat, lon, height = ecef2llh(X, Y, Z)
print(f"Geodetic lat: {lat}, lon: {lon}, height: {height}")

print(f"\nConvert geodetic {lat}, {lon}, {height} back to ECEF ...")
x, y, z = llh2ecef(lat, lon, height)
print(f"ECEF X: {x}, Y: {y}, Z: {z}")

print(
    f"\nConvert ECEF X: {X}, Y: {Y}, Z: {Z} to geodetic using alternate GRS80 datum ..."
)
lat, lon, height = ecef2llh(X, Y, Z, GRS80_EARTH_RADIUS, GRS80_FLATTENING)
print(f"Geodetic lat: {lat}, lon: {lon}, height: {height}")

print(f"\nConvert geodetic {lat}, {lon}, {height} back to ECEF ...")
x, y, z = llh2ecef(lat, lon, height, GRS80_EARTH_RADIUS, GRS80_FLATTENING)
print(f"ECEF X: {x}, Y: {y}, Z: {z}")
