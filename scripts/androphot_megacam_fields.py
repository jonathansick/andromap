#!/usr/bin/env python
# encoding: utf-8
"""
Test script for Andromap with an inverted LSB PNG basemap.

2013-11-29 - Created by Jonathan Sick
"""

import os
import logging

import numpy as np

from pymongo import MongoClient

from andromap import Andromap
from andromap.constants import M31RA0, M31DEC0

from andromass.profile.datasets import read_release

BLUE = "#377eb8"
RED = '#e41a1c'
GREEN = '#4daf4a'

androids_runids = ['10BC23', '10BC97', '10BD99', '12BC23', '13BC32']


def main():
    log = logging.getLogger('andromap')
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    plot_archive_fields()


def plot_archive_fields():
    client = MongoClient(host='localhost', port=27017)
    c = client.m31.images

    pngpath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.inverted.png")
    fitspath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.fits")
    m = Andromap(fitspath, figsize=(7.5, 7.5))
    m.fig.show_rgb(pngpath)
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"},
                           edgecolor=BLUE, lw=3.)
    m.plot_combined_fields({"INSTRUME": "WIRCam",
                            "TYPE": "sci",
                            "RUNID": {'$in': ['07BC20',
                                              '09BC29',
                                              '11BC12',
                                              '12BH04']}},
                           edgecolor=RED, lw=3.)

    # everyone *but* ANDROIDS observations
    sel = {"INSTRUME": "MegaPrime",
           "RUNID": {"$nin": androids_runids},
           "footprint": {"$exists": 1},
           "FILTER": {"$in": ['u', 'g', 'r', 'i']}}
    fieldnames = c.find(sel).distinct("OBJECT")
    for fieldname in fieldnames:
        s = dict(sel)
        s.update({"OBJECT": fieldname})
        doc = c.find_one(s)
        ra = doc['RA_DEG']
        dec = doc['DEC_DEG']
        # m.plot_combined_fields(s)
        m.add_label(ra, dec, fieldname.replace(r"_", r"\_"),
                    size=7, zorder=1000)

    radii = np.arange(10., 50., 10.)
    prof = read_release()
    m.plot_xvista_profile_ellipse_grid(prof, radii, zorder=100,
                                       edgecolor='0.2', alpha=0.7)

    m.fig.recenter(M31RA0, M31DEC0, radius=5)
    m.save("megacam_archive_fields.png", format='png',
           dpi=300, transparent=True, adjust_bbox=True)


if __name__ == '__main__':
    main()
