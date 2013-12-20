#!/usr/bin/env python
# encoding: utf-8
"""
Test script for Andromap with an inverted LSB PNG basemap.

2013-11-29 - Created by Jonathan Sick
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
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sci"})
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
        "RUNID": {"$in": ['07BC20', '07BH47']}})
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
        "RUNID": {"$in": ['09BH52', '09BC29', '11BC12', '12BH04']}})
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"})
    # m.plot_phat(union=True)
    m.plot_phat_fields(union=False, edgecolor='None', facecolor='r',
        zorder=10, alpha=0.2, band="F110W")
    m.plot_hst_halo()
    m.save("andromap_test.pdf", dpi=300, transparent=True, adjust_bbox=True,
            format='pdf')


if __name__ == '__main__':
    main()
