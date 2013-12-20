#!/usr/bin/env python
# encoding: utf-8
"""Maps of the ANDROIDS survey using Aplpy."""

import os
import logging
import json

import aplpy

from .imagelogfootprints import get_combined_image_footprint, \
    get_phat_bricks, get_combined_phat_bricks, get_acs_halo_fields, \
    get_image_footprints
from .polytools import close_vertices, polygon_union


class Andromap(object):
    """This class plots ANDROIDS maps/footprints with an image using Aplpy.
    
    Parameters
    ----------
    fitspath : str
        Path to a FITS image (or a AVM-enabled JPG/PNG image).
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
    def __init__(self, fitspath, fig=None, subplot=(1, 1, 1),
            figsize=(3.5, 3.5), **kw):
        super(Andromap, self).__init__()
        self.fitspath = fitspath
        self._figure = fig
        self._subplot = subplot
        self._log = logging.getLogger('andromap')

        if (self._figure is not None) and (self._subplot_bounds is not None):
            # Put Aplpy axes into an existing axis
            self._f = aplpy.FITSFigure(fitspath, figure=self._figure,
                    subplot=self._subplot, **kw)
        else:
            # Let Aplpy set it all up
            self._f = aplpy.FITSFigure(fitspath, figsize=figsize,
                    subplot=self._subplot, **kw)

        # Set up typography
        self._f.set_system_latex('True')
        self._f.set_tick_labels_format(xformat='hh:mm',yformat='dd')

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

    def plot_combined_fields(self, sel, layer=False, zorder=None, **mpl):
        """Plot unions of image footprints."""
        polygons = get_combined_image_footprint(sel)
        if polygons is None: return
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

    def plot_phat(self, union=True, layer=False, zorder=None, **mpl):
        """Plot the PHAT footprint."""
        if union:
            polygons = get_combined_phat_bricks()
        else:
            polydict = get_phat_bricks()
            polygons = [p for n, p in polydict.iteritems()]
        if polygons is None: return
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
            if polygons is None: return
            self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)
        else:
            footprints = get_image_footprints(sel)
            polys = [v for k, v in footprints.iteritems()]
            self._f.show_polygons(polys, layer=layer, zorder=zorder, **mpl)

    def plot_hst_halo(self, union=True, layer=False, zorder=None, **mpl):
        """Plot the Brown et al HST/ACS halo footprints."""
        polydict = get_acs_halo_fields()
        polygons = [p for n, p in polydict.iteritems()]
        if polygons is None: return
        self._f.show_polygons(polygons, layer=layer, zorder=zorder, **mpl)

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
