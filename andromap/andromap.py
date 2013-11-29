#!/usr/bin/env python
# encoding: utf-8
"""Maps of the ANDROIDS survey using Aplpy."""

import os

import aplpy


class Andromap(object):
    """This class plots ANDROIDS maps/footprints with an image using Aplpy.
    
    Parameters
    ----------
    fitspath : str
        Path to a FITS image (or a AVM-enabled JPG/PNG image).
    fig : Figure
        A matplotlib Figure instance to plot into
    bounds : list
        Bounds of a sub-axes to plot into, given a ``fig``. The bounds are
        given by ``[xmin, ymin, dx, dy]``.
    figsize : tuple
        Size figure, inches, (width, height).
    kw :
        Arguments passed directly to the ``aplpy.FITSFigure`` constructor.
    """
    def __init__(self, fitspath, fig=None, bounds=None, figsize=(3.5, 3.5),
            **kw):
        super(Andromap, self).__init__()
        self.fitspath = fitspath
        self._figure = fig
        self._subplot_bounds = bounds

        if (self._figure is not None) and (self._subplot_bounds is not None):
            # Put Aplpy axes into an existing axis
            self._f = aplpy.FITSFigure(fitspath, figure=self._figure,
                    subplot=self._subplot_bounds, **kw)
        else:
            # Let Aplpy set it all up
            self._f = aplpy.FITSFigure(fitspath, figsize=figsize,
                    subplot=bounds, **kw)
        self._f.set_system_latex('False')
    
    def save(self, path, dpi=300, transparent=False, adjust_bbox=False,
            max_dpi=300, format='pdf'):
        """Save the figure."""
        if not path.endswith(format):
            path = path + "." + format
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if self._figure is not None:
            # Save through matplotlib
            self._figure.canvas.savefig(path, format=format, dpi=300)
        else:
            # Save through Aplpy
            self._f.save(path, dpi=dpi, transparent=transparent,
                    adjust_bbox=adjust_bbox,
                    max_dpi=max_dpi, format=format)
