"""
Simple example implementation of a UBXMessage and/or 
NMEAMessage binary logfile reader using the UBXReader iterator 
functions

Created on 25 Oct 2020

@author: semuadmin
"""

from pyubx2.ubxreader import UBXReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def read(stream, errorhandler, protfilter, validate, msgmode):
    """
    Reads and parses UBX message data from stream.
    """

    msgcount = 0

    ubr = UBXReader(
        stream,
        protfilter=protfilter,
        validate=validate,
        msgmode=msgmode,
        parsebitfield=True,
    )
    for (_, parsed_data) in ubr.iterate(quitonerror=False, errorhandler=errorhandler):
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")

    print("Enter fully qualified name of file containing binary UBX data: ", end="")
    filename = input().strip('"')
    print(
        "Which protocols do you want to handle? (1 = NMEA, 2 = UBX, 3 = BOTH) (3) ",
        end="",
    )
    val = input() or "3"
    iprotfilter = int(val)
    print("Do you want to validate the message checksums (y/n)? (y) ", end="")
    val = input() or "y"
    ivalidate = val in YES
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    imsgmode = int(mode)

    print(f"Opening file {filename}...")
    with open(filename, "rb") as fstream:
        read(fstream, errhandler, iprotfilter, ivalidate, imsgmode)
    print("Test Complete")
