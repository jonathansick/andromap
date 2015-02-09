#!/usr/bin/env python
# encoding: utf-8
"""
Footprint plot for Oxford.
"""

import os
import logging

from andromap import Andromap
import numpy as np

from andromass.profile.datasets import read_release
from andromap.constants import M31RA0, M31DEC0

BLUE = "#377eb8"
RED = '#e41a1c'
GREEN = '#4daf4a'


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
                           edgecolor=RED, lw=1.5)
    # m.plot_combined_fields({"INSTRUME": "WIRCam",
    #                         "TYPE": "sci",
    #                         "RUNID": {'$in': ['07BC20', '09BC29']}},
    #                        edgecolor=RED, lw=3.)
    # m.plot_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
    #                "RUNID": {"$in": ['07BC20', '07BH47']}},
    #               edgecolor=RED, lw=0.8)
    # m.plot_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
    #                "RUNID": {"$in": ['09BC29']}},
    #               edgecolor=RED, lw=0.8)
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"},
                           edgecolor=BLUE, lw=3.)
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sky"},
                           edgecolor=BLUE, lw=0.8)
    m.plot_phat(union=True, edgecolor=GREEN, facecolor='None',
                lw=2.)

    radii = np.arange(10., 50., 10.)
    prof = read_release()
    m.plot_xvista_profile_ellipse_grid(prof, radii, zorder=100,
                                       edgecolor='0.2', alpha=0.7)

    m.save("simple_map_zoomin.pdf", format='pdf',
           dpi=300, transparent=True, adjust_bbox=True)

    m.fig.recenter(M31RA0, M31DEC0, radius=4)  # , width=9, height=9)
    m.save("simple_map.pdf", format='pdf',
           dpi=300, transparent=True, adjust_bbox=True)


if __name__ == '__main__':
    main()
