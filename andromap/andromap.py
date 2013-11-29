#!/usr/bin/env python
# encoding: utf-8
"""Maps of the ANDROIDS survey using Aplpy."""

import os

import aplpy

from .imagelogfootprints import get_combined_image_footprint, \
    get_phat_bricks, get_combined_phat_bricks

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
