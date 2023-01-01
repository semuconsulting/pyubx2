"""
mon_span_spectrum.py

Simple illustration of how to plot MON-SPAN spectrum data
as a spectrum analysis chart using pyubx2 and matplotlib.

Each MON-SPAN message can contain multiple RF Blocks.

The sample mon_span.ubx file contains a multiple MON-SPAN
messages, each of which has two frequency blocks (L1 & L2).

Created on 19 Nov 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

from random import randrange
import matplotlib.pyplot as plt
import numpy as np
from pyubx2 import UBXReader, UBXMessage

RF_SIGS = {
    "L1": 1.57542,
    "L2": 1.22760,
    "L5": 1.17645,
}


def plot_spectrum(msg: UBXMessage):
    """
    Plot frequency spectrum from MON-SPAN message

    :param UBXMessage msg: MON-SPAN message
    """

    # MON-SPAN message can contain multiple RF blocks
    numrf = msg.numRfBlocks

    # plot each RF block
    maxdb = 0
    for i in range(1, numrf + 1):

        # get MON-SPAN message attributes for this RF block
        idx = f"_{i:02}"
        spec = getattr(msg, "spectrum" + idx)
        spn = getattr(msg, "span" + idx)
        res = getattr(msg, "res" + idx)
        ctr = getattr(msg, "center" + idx)
        pga = getattr(msg, "pga" + idx)

        # set data coordinates
        x_axis = np.arange(ctr - spn / 2, ctr + spn / 2, res) / 1e9  # plot as GHz
        y_axis = np.array(spec)  # - pga  # adjust by receiver gain
        maxdb = max(maxdb, np.max(y_axis))

        # create plot
        plt.plot(x_axis, y_axis, label=f"RF {i}")

    for nam, frq in RF_SIGS.items():
        x_axis = np.array([frq, frq])
        y_axis = np.array([0, maxdb])
        # create plot
        plt.plot(x_axis, y_axis, label=f"{nam}", linestyle="dotted")

    # display plot
    plt.title("MON-SPAN Spectrum Analysis")
    plt.legend(fontsize="small")
    plt.xlabel("GHz")
    plt.ylabel("dB")
    plt.ylim(bottom=0)
    plt.grid()
    plt.show()


if __name__ == "__main__":

    # read binary UBX data stream containing one or more MON-SPAN messages
    with open("mon_span.ubx", "rb") as stream:

        ubr = UBXReader(stream)
        for (raw_data, parsed_data) in ubr.iterate():
            if parsed_data.identity == "MON-SPAN":
                # print(parsed_data)
                plot_spectrum(parsed_data)
