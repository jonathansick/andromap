#!/usr/bin/env python
# encoding: utf-8
"""
Tools for working with polygons through shapely

2013-12-11 - Created by Jonathan Sick
"""

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union
import numpy as np


def close_vertices(polygon):
    """Make the last vertex the same as the first."""
    polygon.append(polygon[0])
    return polygon


def polygon_union(polygons):
    """Make the union of polygons. Returns a list of all isolated polygon
    unions."""
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
