"""
mon_span_spectrum.py

Simple illustration of how to plot MON-SPAN spectrum data
as a spectrum analysis chart using pyubx2 and matplotlib.

The mon_span.ubx file contains a single raw MON-SPAN message.

Created on 19 Nov 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

import matplotlib.pyplot as plt
import numpy as np
from pyubx2 import UBXReader, UBXMessage


def plot_spectrum(msg: UBXMessage, style: str = "default"):
    """
    Plot frequency spectrum from MON-SPAN message

    :param UBXMessage msg: MON-SPAN message
    :param str style: plot style ("default")
    """

    # get MON-SPAN message attributes for first rfBlock
    # (use _02, _03, etc. for subsequent rfBlocks)
    spectrum = msg.spectrum_01
    span = msg.span_01
    res = msg.res_01
    center = msg.center_01
    pga = msg.pga_01

    # data coordinates
    x_axis = np.arange(center - span / 2, center + span / 2, res)
    x_axis = x_axis / 1e9  # plot as GHz
    y_axis = np.array(spectrum)
    y_axis = y_axis - pga  # adjust by receiver gain

    # create plot
    plt.style.use(style)
    plt.plot(x_axis, y_axis)

    # add title
    plt.title("MON-SPAN Spectrum Analysis")

    # add axes labels and grid
    plt.xlabel("GHz")
    plt.ylabel(f"dB - pga (pga = {pga} dB)")
    plt.ylim(bottom=0)
    plt.grid(visible=True, which="major", axis="both")

    # display plot
    plt.show()


if __name__ == "__main__":

    # read binary UBX data stream containing one or more MON-SPAN messages
    with open("mon_span.ubx", "rb") as stream:

        ubr = UBXReader(stream)
        for (raw_data, parsed_data) in ubr.iterate():
            if parsed_data.identity == "MON-SPAN":
                # print(parsed_data)
                plot_spectrum(parsed_data)
