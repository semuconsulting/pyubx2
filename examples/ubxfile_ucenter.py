"""
ubxfile_ucenter.py

This example illustrates how to suppress 'msgmode' warnings while
parsing a u-center *.ubx recording containing mixed message modes
(i.e. debug and configuration data):

- GET - NAV messages and CFG-VALGET poll responses from receiver
- POLL - CFG-VALGET polls to receiver
- SET - CFG-VALSET commands to receiver

The supplied "2023-4-17_82912_serial-COM3.ubx" file contains
951 GET messages, 27 SET messages and 70 POLL messages. 

Created on 23 Apr 2023

@author: semuadmin
"""

from pyubx2 import UBXReader, ERR_IGNORE, GET, SET, POLL


for mode in (GET, SET, POLL):
    i = 0
    with open("2023-4-17_82912_serial-COM3.ubx", "rb") as infile:
        ubr = UBXReader(infile, quitonerror=ERR_IGNORE, msgmode=mode)
        for raw, parsed in ubr:
            if parsed is not None:
                i += 1
                print(parsed)

    print(f'\n{i} {("GET","SET","POLL")[mode]} messages parsed\n\n')
