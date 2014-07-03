#!/usr/bin/env python
# encoding: utf-8
"""
Test script for Andromap with an inverted LSB PNG basemap.

2013-11-29 - Created by Jonathan Sick
"""

import os
import logging
import numpy as np

from andromap import Andromap
from andromass.profile.datasets import read_release
from andromap.constants import M31RA0, M31DEC0


def main():
    log = logging.getLogger('andromap')
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # box(0:51:44.130,+41:11:54.49,3600",3600",0) # text={SE1}
    # box(0:50:02.796,+40:16:10.59,3600",3600",0) # text={SE2}
    # box(0:46:18.611,+39:21:42.43,3600",3600",0) # text={SE4}
    # box(0:51:07.630,+39:19:35.84,3600",3600",0) # text={SE3}
    # box(0:41:27.670,+43:08:55.63,3600",3600",0) # text={NW1}
    # box(0:36:23.986,+42:12:54.65,3600",3600",0) # text={NW2}
    # box(0:32:44.822,+41:15:51.34,3600",3600",0) # text={NW3}
    # box(0:31:14.572,+40:18:11.44,3600",3600",0) # text={NW4}
    # box(0:36:17.710,+43:08:30.21,3600",3600",0) # text={NW5}
    # box(0:31:27.235,+42:11:42.97,3600",3600",0) # text={NW6}
    # box(0:31:18.318,+43:06:58.70,3600",3600",0) # text={NW7}
    sky_fields = [
        {'ra': (0, 59., 11.75),  'dec': (40, 41, 38.0), 'n': 'SKY2'},
        {'n': 'SKY1', 'ra': (1, 00., 58.57), 'dec': ('+42', 32, 37.3)},
        {'n': 'SKY8', 'ra': (0, 53., 45.56), 'dec': ('+44', 30, 14.1)},
        {'n': 'SKY7', 'ra': (0, 38., 45.86), 'dec': ('+43', 36, 40.1)},
        {'n': 'SKY6', 'ra': (0, 31., 42.71), 'dec': ('+42', 16, 38.7)},
        {'n': 'SKY5', 'ra': (0, 25., 05.00), 'dec': ('+40', 26, 37.5)},
        {'n': 'SKY4', 'ra': (0, 25., 43.04), 'dec': ('+37', 59, 41.0)},
        {'n': 'SKY3', 'ra': (0, 33., 01.01), 'dec': ('+37', 56, 54.5)}]
    square_fields = [
        {'ra': (0, 51., 44.130), 'dec': (41, 11, 54.49), 'n': 'SE1'},
        {'ra': (0, 50., 02.796), 'dec': (40, 16, 10.59), 'n': 'SE2'},
        {'ra': (0, 46., 18.611), 'dec': (39, 21, 42.43), 'n': 'SE4'},
        {'ra': (0, 51., 07.630), 'dec': (39, 19, 35.84), 'n': 'SE3'},
        {'ra': (0, 41., 27.670), 'dec': (43, 8, 55.63), 'n': 'NW1'},
        {'ra': (0, 36., 23.986), 'dec': (42, 12, 54.65), 'n': 'NW2'},
        {'ra': (0, 32., 44.822), 'dec': (41, 15, 51.34), 'n': 'NW3'},
        {'ra': (0, 31., 14.572), 'dec': (40, 18, 11.44), 'n': 'NW4'},
        {'ra': (0, 36., 17.710), 'dec': (43, 8, 30.21), 'n': 'NW5'},
        {'ra': (0, 31., 27.235), 'dec': (42, 11, 42.97), 'n': 'NW6'},
        {'ra': (0, 31., 18.318), 'dec': (43, 6, 58.70), 'n': 'NW7'}]
    perimeter_fields = [
        {'ra': (0, 41, 47.547), 'dec': (43, 05, 05.51), 'n': 'N1'},
        {'ra': (0, 36, 46.869), 'dec': (42, 9, 03.14), 'n': 'N2'},
        {'ra': (0, 32, 54.665), 'dec': (41, 12, 46.38), 'n': 'N3'},
        {'ra': (0, 52, 25.926), 'dec': (41, 13, 58.31), 'n': 'S1'},
        {'ra': (0, 49, 42.631), 'dec': (40, 22, 23.89), 'n': 'S2'},
        {'ra': (0, 45, 49.648), 'dec': (39, 25, 19.53), 'n': 'S3'},
        {'ra': (0, 30, 25.494), 'dec': (40, 16, 08.21), 'n': 'N4'},
        {'ra': (0, 50, 19.185), 'dec': (43, 56, 57.26), 'n': 'NE1'},
        {'ra': (0, 55, 15.200), 'dec': (43, 55, 12.99), 'n': 'NE2'},
        {'ra': (0, 56, 27.736), 'dec': (43, 03, 57.23), 'n': 'NE3'},
        {'ra': (0, 30, 36.378), 'dec': (38, 24, 08.19), 'n': 'SW1'},
        {'ra': (0, 34, 51.415), 'dec': (38, 26, 03.58), 'n': 'SW2'},
        {'ra': (0, 39, 13.450), 'dec': (38, 27, 22.95), 'n': 'SW3'}]
    for field in sky_fields:
        convert_field_coord(field)
    for field in square_fields:
        convert_field_coord(field)
    for field in perimeter_fields:
        convert_field_coord(field)

    pngpath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.inverted.png")
    fitspath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.fits")
    m = Andromap(fitspath, figsize=(3.5, 3.5))
    m.fig.show_rgb(pngpath)

    radii = np.arange(10., 70., 10.)
    prof = read_release()
    m.plot_xvista_profile_ellipse_grid(prof, radii, zorder=100,
                                       edgecolor='r')

    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sci"})
    # m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
    #                         "RUNID": {"$in": ['07BC20', '07BH47']}})
    # m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
    #                         "RUNID": {"$in": ['09BH52', '09BC29',
    #                                           '11BC12', '12BH04']}})
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"})
    # m.plot_phat(union=True)
    # m.plot_phat_fields(union=False, edgecolor='None', facecolor='r',
    #     zorder=10, alpha=0.2, band="F110W")
    m.plot_hst_halo()
    for field in sky_fields:
        m.plot_box(field['ra'], field['dec'], width=1., height=1.,
                   facecolor='None', edgecolor='orange', lw=1.)
        # m.add_label(field['ra'], field['dec'], field['n'])
    for field in perimeter_fields:
        m.plot_box(field['ra'], field['dec'], width=1., height=1.,
                   facecolor='dodgerblue', alpha=0.7, edgecolor='dodgerblue',
                   lw=1.)

    m.fig.recenter(M31RA0, M31DEC0, radius=4)  # , width=9, height=9)
    m.save("cfht_lsb_14b.pdf", dpi=300, transparent=True, adjust_bbox=True,
           format='pdf')


def convert_field_coord(field):
    field['ra'] = 15. * (float(field['ra'][0]) + field['ra'][1] / 60.
                            + field['ra'][1] / 3600.)
    field['dec'] = float(field['dec'][0]) + field['dec'][1] / 60. \
        + field['dec'][1] / 3600.


if __name__ == '__main__':
    main()
