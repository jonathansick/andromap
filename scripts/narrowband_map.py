#!/usr/bin/env python
# encoding: utf-8
"""
Plot of narrowband footprints.

2013-12-11 - Created by Jonathan Sick
"""

import os
import logging

from andromap import Andromap


def main():
    log = logging.getLogger('andromap')
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    pngpath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.inverted.png")
    fitspath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.fits")
    m = Andromap(fitspath, figsize=(3.5, 3.5))
    m.fig.show_rgb(pngpath)
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sci"},
        edgecolor='r')
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
        "RUNID": {"$in": ['07BC20', '07BH47']}}, edgecolor='r')
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"},
        edgecolor='b')
    m.plot_phat(union=True)
    # Plot archival fields
    m.plot_narrowband_fields(['SW1', 'SW2', 'NGC205'],
            facecolor='g', alpha=0.7)
    # Plot observed fields
    observed = ["AGB_%i" % i for i in range(1, 17)]
    m.plot_narrowband_fields(observed,
            facecolor='orange', alpha=0.6)

    # Plot un-observed fields
    unobserved = ["AGB_%i" % i for i in range(17, 21)]
    m.plot_narrowband_fields(unobserved,
            edgecolor='purple', linestyle='solid')

    m.save("narrowband_footprint.pdf", format='pdf',
            dpi=300, transparent=True, adjust_bbox=True)


if __name__ == '__main__':
    main()
