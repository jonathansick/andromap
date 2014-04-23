#!/usr/bin/env python
# encoding: utf-8
"""
Plot of M31/HST footprints.
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
    m.plot_hst_halo(label=True)

    m.save("hst_footprint.pdf", format='pdf',
            dpi=300, transparent=True, adjust_bbox=True)


if __name__ == '__main__':
    main()
