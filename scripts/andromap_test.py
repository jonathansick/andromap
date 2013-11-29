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
    m = Andromap(fitspath, figsize=(6.5, 6.5))
    m.fig.show_rgb(pngpath)
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sci"})
    m.save("andromap_test.pdf", dpi=300, transparent=True, adjust_bbox=True,
            format='pdf')


if __name__ == '__main__':
    main()
