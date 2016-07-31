#!/usr/bin/env python
# encoding: utf-8
"""Maps of the ANDROIDS survey using Aplpy."""

import os
import logging
import json

import numpy as np
import aplpy

from .imagelogfootprints import get_combined_image_footprint, \
    get_phat_bricks, get_combined_phat_bricks, get_acs_halo_fields, \
    get_image_footprints
from .polytools import close_vertices, polygon_union
from .constants import D_KPC, M31RA0, M31DEC0
from .tanproj import tan_to_eq


class Andromap(object):
    """This class plots ANDROIDS maps/footprints with an image using Aplpy.

    Parameters
    ----------
    dataset : str or HDU
        Path to a FITS image (or a AVM-enabled JPG/PNG image), or an
        astropy.fits HDU.
    fig : Figure
        A matplotlib Figure instance to plot into
    subplot : list
        Either: a length-4 list giving bounds of a sub-axes to plot into,
        given a ``fig``. The bounds are given by ``[xmin, ymin, dx, dy]``.
        A length-3 list gives the matplotlib-style subplot index.
    figsize : tuple
        Size figure, inches, (width, height).
    kw :
        Arguments passed directly to the ``aplpy.FITSFigure`` constructor.
    """
    def __init__(self, dataset, fig=None, subplot=(1, 1, 1),
                 figsize=(3.5, 3.5), **kw):
        super(Andromap, self).__init__()
        self.dataset = dataset
        self._figure = fig
        self._subplot = subplot
        self._log = logging.getLogger('andromap')

        if self._figure is not None:
            # Put Aplpy axes into an existing axis
            self._f = aplpy.FITSFigure(dataset, figure=self._figure,
                                       subplot=self._subplot, **kw)
        else:
            # Let Aplpy set it all up
            self._f = aplpy.FITSFigure(dataset, figsize=figsize,
                                       subplot=self._subplot, **kw)

        # Set up typography
        self._f.set_system_latex('True')
        self._f.set_tick_labels_format(xformat='hh:mm', yformat='dd')

    @property
    def fig(self):
        """The Aplypy FITSFigure instance"""
        return self._f

    def save(self, path, dpi=300, transparent=False, adjust_bbox=True,
             max_dpi=300, format='pdf'):
        """Save the figure."""
        if not path.endswith(format):
            path = path + "." + format
        dirname = os.path.dirname(path)
        if dirname is not "" and not os.path.exists(dirname):
            os.makedirs(dirname)
        if self._figure is not None:
            # Save through matplotlib
            self._figure.canvas.savefig(path, format=format, dpi=300)
        else:
            # Save through Aplpy
            self._f.save(path, dpi=dpi, transparent=transparent,
                         adjust_bbox=adjust_bbox,
                         max_dpi=max_dpi, format=format)

    def add_label(self, ra, dec, txt):
        """Add a text label at the world coordinates."""
        self._f.add_label(ra, dec, txt)

    def plot_box(self, ra, dec, width, height,
                 layer=False, zorder=None, **mpl):
        """Plot a rectangle in world coordinates."""
        self._f.show_rectangles(ra, dec, width, height,
                                layer=layer, zorder=zorder, **mpl)

    def plot_fields(self, sel, layer=False, zorder=None, **mpl):
        """Plot individual image footprints."""
        polydict = get_image_footprints(sel)
        polygons = [p for n, p in polydict.iteritems()]
        if polygons is None:
            return
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

    def plot_combined_fields(self, sel, layer=False, zorder=None, **mpl):
        """Plot unions of image footprints."""
        polygons = get_combined_image_footprint(sel)
        if polygons is None:
            return None
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

    def plot_phat(self, union=True, layer=False, zorder=None, **mpl):
        """Plot the PHAT footprint."""
        if union:
            polygons = get_combined_phat_bricks()
        else:
            polydict = get_phat_bricks()
            polygons = [p for n, p in polydict.iteritems()]
        if polygons is None:
            return None
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

    def plot_phat_fields(self, band="F160W", bricks=None, fields=None,
                         union=True, layer=False, zorder=None, **mpl):
        """Plot the PHAT footprint from individual field footprints rather than
        brick-by-brick.

        Parameters
        ----------
        band : str
            Name of bandpass to search for
        bricks : list
            List of brick numbers (integers) to plot
        fields : list
            List of field number (integers) from bricks to plot.
        """
        sel = {"survey": "PHAT", "FILTER": band}
        if bricks is not None:
            sel['brick'] = {"$in": bricks}
        if fields is not None:
            sel['field'] = {"$in": fields}
        if union:
            polygons = get_combined_image_footprint(sel)
            if polygons is None:
                return None
            self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)
        else:
            footprints = get_image_footprints(sel)
            polys = [v for k, v in footprints.iteritems()]
            self._f.show_polygons(polys, layer=layer, zorder=zorder, **mpl)

    def plot_hst_halo(self, union=True, layer=False, zorder=None,
                      label=None, **mpl):
        """Plot the Brown et al HST/ACS halo footprints."""
        polydict = get_acs_halo_fields()
        polygons = [p for n, p in polydict.iteritems()]
        if polygons is None:
            return
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)
        if label:
            for name, poly in polydict.iteritems():
                x = np.array([v[0] for v in poly]).mean()
                y = np.array([v[1] for v in poly]).mean()
                self._f.add_label(x, y - 0.05, name, size=7,
                                  verticalalignment='top')

    def plot_narrowband_fields(self, names, union=True, layer=False,
                               zorder=None, **mpl):
        """Plot named narrowband fields."""
        if isinstance(names, str) or isinstance(names, unicode):
            names = [names]
        data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "data/narrowband_fields.json")
        self._log.debug("Data path: {path}".format(path=data_path))
        with open(data_path) as f:
            field_data = json.loads(f.read())
        polygons = [field_data[n] for n in names]
        if union:
            polygons = [close_vertices(p) for p in polygons]
            polygons = polygon_union(polygons)
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

    def plot_xvista_profile_ellipse_grid(self, prof, radii,
                                         layer=False, zorder=None, **mpl):
        """Plot ellipses from an XVISTA SB profile at a specified grid of
        radii (given in kiloparsecs).
        """
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
            poly = ellipse_polygon(r_deg, b_deg, pa, M31RA0, M31DEC0,
                                   n_verts=1000)
            polygons.append(poly)

        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)


def ellipse_generator(R, PA, ELL, radii):
    """Generate interpolated ellipses at the given radii (kpc).

    The generate will continue to make ellipses past the profile by maintaining
    PA and ellipticity from the last profile ellipse.
    """
    for r0 in radii:
        if r0 < R.max():
            pa = np.interp(r0, R, PA)
            ell = np.interp(r0, R, ELL)
            yield r0, pa, ell
        else:
            yield r0, pa, ell


def ellipse_polygon(r_deg, b_deg, pa, ra0, dec0, n_verts=1000):
    """Make a polygon with RA,Dec vertices from an ellipse."""
    # Parametric angle
    t = np.linspace(0., 2. * np.pi, num=n_verts, endpoint=False)
    # Transform PA to radians
    p = pa * np.pi / 180.
    # Parametric equation for an ellipse centered at origin
    # note that the x-axis is reverse; increases to left
    X = - (r_deg * np.cos(t) * np.cos(p) - b_deg * np.sin(t) * np.sin(p))
    Y = r_deg * np.cos(t) * np.sin(p) + b_deg * np.sin(t) * np.cos(p)
    ras, decs = tan_to_eq(X, Y, ra0Deg=ra0, dec0Deg=dec0)
    verts = np.vstack([ras, decs]).T
    return verts
