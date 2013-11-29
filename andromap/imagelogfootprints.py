#!/usr/bin/env python
# encoding: utf-8
"""
Get footprints from the image log

2013-11-28 - Created by Jonathan Sick
"""

from pymongo import MongoClient
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union
import numpy as np


def get_combined_image_footprint(sel):
    """Get image footprints and combine them.
    
    Returns
    -------
    verts : list
        A list of one or more Nx2 Numpy arrays which contain the [x, y]
        positions of the vertices in world coordinates.
    """
    client = MongoClient(host='localhost', port=27017)
    c = client.m31.images
    docs = c.find(sel, fields=['footprint'])
    if docs.count() == 0:
        return None
    polygons = [doc['footprint'] for doc in docs]
    polygons = [close_vertices(p) for p in polygons]
    shapely_polys = [Polygon(p) for p in polygons]
    multipoly = MultiPolygon(shapely_polys)
    u = cascaded_union(multipoly)
    if isinstance(u, MultiPolygon):
        vert_seq = []
        for p in u:
            vert_seq.append(np.array(p.exterior.coords[:]))
        return vert_seq
    else:
        return [np.array(u.exterior.coords[:])]


def close_vertices(polygon):
    """Make the last vertex the same as the first."""
    polygon.append(polygon[0])
    return polygon
