#!/usr/bin/env python
# encoding: utf-8
"""
Get footprints from the image log

2013-11-28 - Created by Jonathan Sick
"""

import logging

from pymongo import MongoClient
import numpy as np

from .polytools import close_vertices, polygon_union


def get_image_footprints(sel):
    """Get image footprints.
    
    Returns
    -------
    footprints : dict
        Dictionary of names mapping to footprints (as numpy vertex arrays).
    """
    log = logging.getLogger('andromap')
    client = MongoClient(host='localhost', port=27017)
    c = client.m31.images
    docs = c.find(sel, projection=['footprint'])
    log.debug("Looking for footprints from %s" % str(sel))
    log.debug("Found %i footprints" % docs.count())
    if docs.count() == 0:
        return None
    footprints = {d['_id']: np.array(close_vertices(d['footprint']))
        for d in docs}
    return footprints


def get_combined_image_footprint(sel):
    """Get image footprints and combine them.
    
    Returns
    -------
    verts : list
        A list of one or more Nx2 Numpy arrays which contain the [x, y]
        positions of the vertices in world coordinates.
    """
    footprints = get_image_footprints(sel)
    polygons = [footprint for k, footprint in footprints.iteritems()]
    return polygon_union(polygons)


def get_phat_bricks(bricks=None):
    """Get polygons for PHAT bricks.
    
    Returns
    -------
    fields : dict
        Dictionary of {field number : polygon vertices}.
    bricks : list
        List of PHAT brick numbers (1 -- 23).
    """
    log = logging.getLogger('andromap')
    sel = {"kind": "ph2", "instrument": "PHAT"}
    if bricks is not None:
        fieldsel = {str(n): {"$exists": 1} for n in bricks}
        sel.update(fieldsel)
    client = MongoClient(host='localhost', port=27017)
    c = client.m31.footprints
    docs = c.find(sel)
    log.debug("Looking for footprints from %s" % str(sel))
    log.debug("Found %i footprints" % docs.count())
    polygons = {}
    for d in docs:
        polygons[d['field']] = np.array(close_vertices(d['radec_poly']))
    return polygons


def get_combined_phat_bricks(bricks=None):
    """Get polygons for the union of PHAT bricks.

    Returns
    -------
    verts : list
        A list of one or more Nx2 Numpy arrays which contain the [x, y]
        positions of the vertices in world coordinates.
    """
    polys = get_phat_bricks(bricks=bricks)
    polylist = [p for name, p in polys.iteritems()]
    return polygon_union(polylist)


def get_acs_halo_fields():
    """Get polygons for the Brown et al HST halo fields.

    Returns
    -------
    fields : dict
        Dictionary of {field number : polygon vertices}.
    """
    log = logging.getLogger('andromap')
    sel = {"survey": "brown"}
    client = MongoClient(host='localhost', port=27017)
    c = client.m31.images
    docs = c.find(sel)
    log.debug("Looking for footprints from %s" % str(sel))
    log.debug("Found %i footprints" % docs.count())
    polygons = {}
    for d in docs:
        polygons[d['field']] = np.array(close_vertices(d['footprint']))
    return polygons
