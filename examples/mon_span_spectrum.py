"""
mon_span_spectrum.py

Simple illustration of how to plot MON-SPAN spectrum data
as a spectrum analysis chart using pyubx2 and matplotlib.

Each MON-SPAN message can contain multiple RF Blocks.

The sample mon_span.ubx file contains multiple MON-SPAN
messages from M9N and F9P receivers, containing one (L1)
and two (L1, L2) frequency blocks respectively.

Created on 19 Nov 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

import matplotlib.pyplot as plt
import numpy as np
from pyubx2 import UBXMessage, UBXReader

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
    minhz = 999 * 1e9
    maxhz = 0
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
        minhz = min(minhz, np.min(x_axis))
        maxhz = max(maxhz, np.max(x_axis))
        maxdb = max(maxdb, np.max(y_axis))

        # create plot
        plt.plot(x_axis, y_axis, label=f"RF {i}")

    # plot L1, L2, L5 markers if within frequency span
    for nam, frq in RF_SIGS.items():
        if minhz < frq < maxhz:
            x_axis = np.array([frq, frq])
            y_axis = np.array([0, maxdb])
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
        for raw_data, parsed_data in ubr:
            if parsed_data.identity == "MON-SPAN":
                plot_spectrum(parsed_data)
