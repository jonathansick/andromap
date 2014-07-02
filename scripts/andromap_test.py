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
    fields = [
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
    for field in fields:
        field['ra'] = 15. * (float(field['ra'][0]) + field['ra'][1] / 60.
                             + field['ra'][1] / 3600.)
        field['dec'] = float(field['dec'][0]) + field['dec'][1] / 60. \
            + field['dec'][1] / 3600.

    pngpath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.inverted.png")
    fitspath = os.path.expanduser("~/andromap/Elixir_B3_r.resamp.fits")
    m = Andromap(fitspath, figsize=(3.5, 3.5))
    m.fig.show_rgb(pngpath)
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sci"})
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
                            "RUNID": {"$in": ['07BC20', '07BH47']}})
    m.plot_combined_fields({"INSTRUME": "WIRCam", "TYPE": "sky",
                            "RUNID": {"$in": ['09BH52', '09BC29',
                                              '11BC12', '12BH04']}})
    m.plot_combined_fields({"INSTRUME": "MegaPrime", "lsb_mosaic.kind": "sci"})
    # m.plot_phat(union=True)
    # m.plot_phat_fields(union=False, edgecolor='None', facecolor='r',
    #     zorder=10, alpha=0.2, band="F110W")
    m.plot_hst_halo()
    for field in fields:
        m.plot_box(field['ra'], field['dec'], width=1., height=1.,
                   facecolor='None', edgecolor='orange', lw=2.)
    m.save("cfht_lsb_14b.pdf", dpi=300, transparent=True, adjust_bbox=True,
           format='pdf')


if __name__ == '__main__':
    main()
