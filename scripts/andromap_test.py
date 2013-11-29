#!/usr/bin/env python
# encoding: utf-8
"""
Test script for Andromap with an inverted LSB PNG basemap.

2013-11-29 - Created by Jonathan Sick
"""

import os

from andromap import Andromap


def main():
    pngpath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.inverted.png")
    fitspath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.fits")
    m = Andromap(fitspath, figsize=(6.5, 6.5))
    m.fig.show_rgb(pngpath)
    m.save("andromap_test.pdf", dpi=300, transparent=True, adjust_bbox=True,
            format='pdf')


if __name__ == '__main__':
    main()
