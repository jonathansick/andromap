#!/usr/bin/env python
# encoding: utf-8
"""
Map of individual megacam fields (labeled).

2017-01-25 - Created by Jonathan Sick
"""

import os
import logging

from andromap import Andromap
import numpy as np
from pymongo import MongoClient

from andromass.profile.datasets import read_release
from andromap.constants import M31RA0, M31DEC0

BLUE = "#377eb8"
RED = '#e41a1c'
GREEN = '#4daf4a'
ORANGE = 'Orange'


MEGACAM_FIELD_NAMES = [u'M31_SB_11',
                       u'M31_SB_12',
                       u'M31_SB_21',
                       u'M31_SB_22',
                       u'M31_SB_23',
                       u'M31_SB_31',
                       u'M31_SB_32',
                       u'M31_SB_33',
                       u'M31_SB_41',
                       u'M31_SB_42',
                       u'M31_SB_43',
                       u'M31_SB_51',
                       u'M31_SB_52',
                       u'M31_SB_53']

MEGACAM_SKY_NAMES = [u'LSB_SKY_1',
                     u'LSB_SKY_2',
                     u'LSB_SKY_3',
                     u'LSB_SKY_4',
                     u'LSB_SKY_5',
                     u'LSB_SKY_6',
                     u'LSB_SKY_7',
                     u'LSB_SKY_8']


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

    client = MongoClient(host='localhost', port=27017)
    c = client.m31.images

    # WIRCam mosaic footprint.
    m.plot_combined_fields({"INSTRUME": "WIRCam",
                            "TYPE": "sci",
                            "RUNID": {'$in': ['07BC20', '09BC29']}},
                           edgecolor=RED, lw=1, alpha=0.8)

    wircam_sky_sel = {"INSTRUME": "WIRCam", "TYPE": "sky",
                      "RUNID": {"$in": ['07BC20', '07BH47', '09BC29']}}
    for field in c.find(wircam_sky_sel).distinct('OBJECT'):
        m.plot_combined_fields(
            {"INSTRUME": "WIRCam", "TYPE": "sky", "OBJECT": field},
            edgecolor=ORANGE, lw=1, alpha=0.8)

    for field in MEGACAM_FIELD_NAMES:
        m.plot_combined_fields(
            {"INSTRUME": "MegaPrime", 'OBJECT': field},
            edgecolor=BLUE, lw=2.)
        coord = m.compute_mean_coordinate({"OBJECT": field})
        m.add_label(coord.ra.value, coord.dec.value,
                    field.split('_')[-1],
                    size=14, weight='heavy',
                    ha='center', va='center',
                    color=BLUE)

    for field in MEGACAM_SKY_NAMES:
        m.plot_combined_fields(
            {"INSTRUME": "MegaPrime", 'OBJECT': field},
            edgecolor=BLUE, lw=1)
        coord = m.compute_mean_coordinate({"OBJECT": field})
        m.add_label(coord.ra.value, coord.dec.value,
                    field.split('_')[-1],
                    size=14, weight='heavy',
                    ha='center', va='center',
                    color=BLUE)

    m.plot_phat(union=True, edgecolor=GREEN, facecolor='None',
                lw=1, alpha=0.8)

    radii = np.arange(10., 50., 10.)
    prof = read_release()
    m.plot_xvista_profile_ellipse_grid(prof, radii, zorder=100,
                                       edgecolor='0.2', alpha=0.7)

    m.fig.recenter(M31RA0, M31DEC0, radius=4)  # , width=9, height=9)
    m.save("megacam_lsb_fields.pdf", format='pdf',
           dpi=300, transparent=True, adjust_bbox=True)


if __name__ == '__main__':
    main()
