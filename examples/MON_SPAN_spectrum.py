"""
mon_span_spectrum.py

Simple illustration of how to plot MON-SPAN spectrum data
as a spectrum analysis chart using pyubx2 and matplotlib.

Each MON-SPAN message can contain multiple RF Blocks.

The example mon_span.ubx file contains a single raw
MON-SPAN message.

Created on 19 Nov 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

import matplotlib.pyplot as plt
import numpy as np
from pyubx2 import UBXReader, UBXMessage


def plot_spectrum(msg: UBXMessage):
    """
    Plot frequency spectrum from MON-SPAN message

    :param UBXMessage msg: MON-SPAN message
    """

    # set up subplot for each RF block
    numrf = msg.numRfBlocks
    fig, sbp = plt.subplots(
        1,
        numrf,
        figsize=(numrf * 5, 4),
        squeeze=False,
    )

    # plot each RF block
    for i in range(numrf):

        # get MON-SPAN message attributes for this RF block
        idx = f"_{i + 1:02}"
        spectrum = getattr(msg, "spectrum" + idx)
        span = getattr(msg, "span" + idx)
        res = getattr(msg, "res" + idx)
        center = getattr(msg, "center" + idx)
        pga = getattr(msg, "pga" + idx)

        # set data coordinates
        x_axis = np.arange(center - span / 2, center + span / 2, res)
        x_axis = x_axis / 1e9  # plot as GHz
        y_axis = np.array(spectrum)
        y_axis = y_axis - pga  # adjust by receiver gain

        # create subplot
        sbp[0][i].plot(x_axis, y_axis)
        sbp[0][i].set_title(f"RF Block {i + 1}")
        sbp[0][i].set_xlabel("GHz")
        sbp[0][i].set_ylabel(f"dB - pga (pga = {pga} dB)")
        sbp[0][i].set_ylim(bottom=0)
        sbp[0][i].grid(visible=True, which="major", axis="both")

    # display plot
    fig.suptitle("MON-SPAN Spectrum Analysis")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # read binary UBX data stream containing one or more MON-SPAN messages
    with open("mon_span.ubx", "rb") as stream:

        ubr = UBXReader(stream)
        for (raw_data, parsed_data) in ubr.iterate():
            if parsed_data.identity == "MON-SPAN":
                # print(parsed_data)
                plot_spectrum(parsed_data)
