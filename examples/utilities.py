"""
utilities.py

Illustration of the various utility methods available in pyubx2

Created on 14 Jan 2023

@author: semuadmin
:copyright: SEMU Consulting © 2022
:license: BSD 3-Clause
"""

from datums import DATUMS  # assumes this is in same folder

from pyubx2 import (
    bearing,
    ecef2llh,
    haversine,
    latlon2dmm,
    latlon2dms,
    llh2ecef,
    llh2iso6709,
)

LAT1, LON1, ALT1 = 53.24, -2.16, 42.45
LAT2, LON2 = 53.32, -2.08

print(f"\nConvert {LAT1}, {LON1} to degrees, minutes, seconds ...")
lat, lon = latlon2dms(LAT1, LON1)
print(f"D.M.S = {lat}, {lon}")

print(f"\nConvert {LAT2}, {LON2} to degrees, minutes ...")
lat, lon = latlon2dmm(LAT2, LON2)
print(f"D.MM = {lat}, {lon}")

print(f"\nConvert {LAT1}, {LON1}, {ALT1}m to ISO6709 format ...")
iso6709 = llh2iso6709(LAT1, LON1, ALT1)
print(f"ISO6709 = {iso6709}")

print(
    f"\nFind spherical distance between {LAT1}, {LON1} and",
    f" {LAT2}, {LON2} using default WGS84 datum...",
)
dist = haversine(LAT1, LON1, LAT2, LON2)
print(f"Distance: {dist/1000} km")

print(
    f"\nFind bearing between {LAT1}, {LON1} and",
    f" {LAT2}, {LON2} using default WGS84 datum...",
)
brng = bearing(LAT1, LON1, LAT2, LON2)
print(f"Distance: {brng} degrees")

X, Y, Z = 3822566.3113, -144427.5123, 5086857.1208
print(f"\nConvert ECEF X: {X}, Y: {Y}, Z: {Z} to geodetic using default WGS84 datum...")
lat, lon, height = ecef2llh(X, Y, Z)
print(f"Geodetic lat: {lat}, lon: {lon}, height: {height}")

print(f"\nConvert geodetic {lat}, {lon}, {height} back to ECEF ...")
x, y, z = llh2ecef(lat, lon, height)
print(f"ECEF X: {x}, Y: {y}, Z: {z}")

# Refer to DATUMS.py in the /examples folder for list of common
# international datums with semi-major axis, flattening and
# delta_x,y,z reference values

DATUM = "North_America_83"
datum_dict = DATUMS[DATUM]
ellipsoid, a, f, delta_x, delta_y, delta_z = datum_dict.values()

print(
    f"\nFind spherical distance between {LAT1}, {LON1} and",
    f"{LAT2}, {LON2} using alternate {DATUM} ({ellipsoid}) datum...",
)
dist = haversine(LAT1, LON1, LAT2, LON2, a / 1000)
print(f"Distance: {dist/1000} km")

print(
    f"\nConvert ECEF X: {X}, Y: {Y}, Z: {Z} to",
    f"geodetic using alternate {DATUM} ({ellipsoid}) datum ...",
)
lat, lon, height = ecef2llh(X - delta_x, Y - delta_z, Z - delta_z, a, f)
print(f"Geodetic lat: {lat}, lon: {lon}, height: {height}")

print(f"\nConvert geodetic {lat}, {lon}, {height} back to ECEF ...")
x, y, z = llh2ecef(lat, lon, height, a, f)
print(f"ECEF X: {x + delta_x}, Y: {y + delta_y}, Z: {z + delta_z}")
