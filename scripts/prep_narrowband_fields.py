#!/usr/bin/env python
# encoding: utf-8
"""
Create a JSON file indicating where narrowband (CFH12K-sized) fields are
located. Once these field are in the footprint DB this will no longer
be needed.

2013-12-11 - Created by Jonathan Sick
"""

import json
import os
import numpy as np
from andromap.tanproj import eq_to_tan, tan_to_eq


def main():
    androids_fields = androids_nb_fields()
    cfh12k_fields = cntio_12k_fields()
    androids_fields.update(cfh12k_fields)
    path = "narrowband_fields.json"
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as f:
        f.write(json.dumps(androids_fields))


def androids_nb_fields():
    """dict of locations of ANDROIDS narrowband fields."""
    fields = {}

    w = 42. / 60.  # width of NB FOV in deg
    h = 28. / 60.  # height of NB FOV in deg
    dh = 4. / 60.  # overlap in deg, heightwise

    r1Xi0, r1Eta0 = 0., 0.
    xi0 = 0.05
    xi_eta = [[0.25, xi0],
            [0.65, xi0 + h - dh],
            [0.65 - w + dh, xi0 + h - dh],
            [0.65, xi0 + 2. * (h - dh)],
            [0.9, xi0 + 3. * (h - dh)]]
    names = ["AGB_%i" % n for n in range(1, len(xi_eta) + 1)]
    norig = len(names)
    for name, (x, e) in zip(names, xi_eta):
        fields[name] = make_nb_field_box(x, e)

    xi_eta = [[1.4, 0.35],
            [0.7, 1.7],
            [0.25 - w + dh, 0.05],
            [0.1, 0.05 - h + dh],
            [0.1 - w + dh, 0.05 - h + dh],
            [-0.3, 0.05 - 2. * h + 2. * dh],  # 11
            [-0.3 - w + dh, 0.05 - 2. * h + 2. * dh],  # 12
            [-0.3, 0.05 - 3. * h + 3. * dh],  # 13
            [-0.3 - w + dh, 0.05 - 3. * h + 3. * dh],   # 14
            [-0.05, 0.85],  # 15
            [0.2, 1.25],  # 16
            [-0.5, 0.4],  # 17 NGC 205
            [0.4, -0.55],  # 18 minor axis
            [0.8, -0.1],  # 19 minor axis
            [1.3, 0.8],  # 20 minor axis
            ]
    names = ["AGB_%i" % n for n in range(norig + 1, norig + len(xi_eta) + 1)]
    for name, (x, e) in zip(names, xi_eta):
        fields[name] = make_nb_field_box(x, e)
    return fields

def cntio_12k_fields():
    """Dict of locations of CN-TiO data from Battinelli, Demers CFHT12K."""
    names = ["NGC205", "SW1", "SW2"]
    alpha = 15. * np.array([.672777778, .638138889, .617313889])
    delta = np.array([41.6853, 40.067497222, 39.680555556])
    xi, eta = eq_to_tan(alpha, delta)
    fields = {}
    for name, x, e in zip(names, xi, eta):
        fields[name] = make_nb_field_box(x, e)
    return fields


def make_nb_field_box(xi, eta):
    """Produce a box with vertices in RA, Dec given xi, eta coords."""
    hw = 42. / 60. / 2.  # half-width of NB FOV in deg
    hh = 28. / 60. / 2.  # half-height of NB FOV in deg
    verts = [tan_to_eq(xi - hw, eta - hh),
            tan_to_eq(xi + hw, eta - hh),
            tan_to_eq(xi + hw, eta + hh),
            tan_to_eq(xi - hw, eta + hh)]
    return verts


if __name__ == '__main__':
    main()
