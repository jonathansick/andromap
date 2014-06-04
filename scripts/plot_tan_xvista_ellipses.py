#!/usr/bin/env python
# encoding: utf-8
"""
Plot the XVISTA ellipses in xi-eta (tangential) projection.
"""

import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.gridspec as gridspec

from andromap.andromap import ellipse_generator
from andromap.constants import D_KPC, M31RA0, M31DEC0
from andromass.profile.datasets import read_release


def main():
    fig = Figure(figsize=(3.5, 3.5))
    canvas = FigureCanvas(fig)
    gs = gridspec.GridSpec(
        1, 1, left=0.15, right=0.95, bottom=0.15, top=0.95,
        wspace=None, hspace=None, width_ratios=None, height_ratios=None)
    ax = fig.add_subplot(gs[0])

    radii = np.arange(10., 50., 10.)
    prof = read_release()
    R = D_KPC * np.tan(prof['R'] / 3600. * np.pi / 180.)
    # print R
    PA = prof['PA']
    ELL = prof['ELL']
    # print prof['ELL']
    print prof['KPC', 'ELL'][::50]

    polygons = []
    for r_kpc, pa, ell in ellipse_generator(R, PA, ELL, radii):
        r_deg = np.arctan(r_kpc / D_KPC) * 180. / np.pi
        b_deg = (1. - ell) * r_deg  # semi-minor axis
        print r_kpc, r_deg, b_deg, ell, pa
        # XVISTA pa is from +x axis (which points rightwards), out
        # PA must be CCW from north
        pa = 90. - pa  # THIS WORKS
        poly = tan_ellipse_polygon(r_deg, b_deg, pa, M31RA0, M31DEC0,
                                   n_verts=1000)
        polygons.append(poly)

    coll = mpl.collections.PolyCollection(polygons,
                                          edgecolors='r',
                                          facecolors='None')
    ax.add_collection(coll)

    ax.set_xlim(3, -3)
    ax.set_ylim(-3, 3)

    gs.tight_layout(fig, pad=1.08, h_pad=None, w_pad=None, rect=None)
    canvas.print_figure("tan_ellipse.pdf", format="pdf")


def tan_ellipse_polygon(r_deg, b_deg, pa, ra0, dec0, n_verts=1000):
    """Make a polygon with xi-eta vertices from an ellipse."""
    # Parametric angle
    t = np.linspace(0., 2. * np.pi, num=n_verts, endpoint=False)
    # Transform PA to radians
    p = pa * np.pi / 180.
    # Parametric equation for an ellipse centered at origin
    # note that the x-axis is reverse; increases to left
    X = - (r_deg * np.cos(t) * np.cos(p) - b_deg * np.sin(t) * np.sin(p))
    Y = r_deg * np.cos(t) * np.sin(p) + b_deg * np.sin(t) * np.cos(p)
    verts = np.vstack([X, Y]).T
    return verts


if __name__ == '__main__':
    main()
