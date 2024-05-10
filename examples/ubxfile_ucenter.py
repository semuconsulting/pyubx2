"""
ubxfile_ucenter.py

Usage:

python3 ubxfile_ucenter.py filename="2023-4-17_82912_serial-COM3.ubx"

This example illustrates how to suppress 'msgmode' warnings while
parsing a u-center *.ubx recording containing mixed message modes
(i.e. debug and configuration data):

- GET - NAV messages and CFG-VALGET poll responses from receiver
- POLL - CFG-VALGET polls to receiver
- SET - CFG-VALSET commands to receiver

The supplied "2023-4-17_82912_serial-COM3.ubx" file contains
951 GET messages, 27 SET messages and 70 POLL messages. 

Created on 22 Apr 2023

@author: semuadmin
"""

from sys import argv

from pyubx2 import ERR_IGNORE, GET, POLL, SET, UBXReader


def main(**kwargs):
    """
    Main Routine.
    """

    filename = kwargs.get("filename", "2023-4-17_82912_serial-COM3.ubx")

    for mode in (GET, SET, POLL):
        i = 0
        with open(filename, "rb") as stream:
            ubr = UBXReader(stream, quitonerror=ERR_IGNORE, msgmode=mode)
            for _, parsed in ubr:
                if parsed is not None:
                    i += 1
                    print(parsed)

        print(f'\n{i} {("GET","SET","POLL")[mode]} messages parsed\n\n')


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
