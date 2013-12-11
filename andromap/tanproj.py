#!/usr/bin/env python
# encoding: utf-8
"""
Tangent-plane projection transformations around M31.

2013-12-11 - Created by Jonathan Sick
"""

import numpy as np


M31RA0 = 10.6846833
M31DEC0 = 41.2690361


def eq_to_tan(ra, dec, ra0=M31RA0, dec0=M31DEC0):
    """Converts RA,Dec coordinates to xi, eta tangential coordiantes.
    See Olkin:1996 eq 3 for example, or Smart 1977.

    :return: tuple of xi, eta in degrees.
    """
    r = ra * np.pi / 180.
    d = dec * np.pi / 180.
    r0 = ra0 * np.pi / 180.
    d0 = dec0 * np.pi / 180.

    xi = np.cos(d) * np.sin(r - r0) \
        / (np.sin(d0) * np.sin(d)
        + np.cos(d0) * np.cos(d) * np.cos(r-r0))

    eta = (np.cos(d0) * np.sin(d)
            - np.sin(d0) * np.cos(d) * np.cos(r - r0)) \
    / (np.sin(d0) * np.sin(d) + np.cos(d0) * np.cos(d) * np.cos(r - r0))

    xi = xi * 180. / np.pi
    eta = eta * 180. / np.pi
    return xi, eta

def tan_to_eq(xiDeg, etaDeg, ra0Deg=M31RA0, dec0Deg=M31DEC0):
    """Convert tangential coordinates to equatorial (RA, Dec) in degrees."""
    xi = xiDeg * np.pi / 180.
    eta = etaDeg * np.pi / 180.
    ra0 = ra0Deg * np.pi / 180.
    dec0 = dec0Deg * np.pi / 180.

    ra = np.arctan(xi / (np.cos(dec0) - eta * np.sin(dec0))) + ra0
    dec = np.arctan((np.sin(dec0) + eta * np.cos(dec0))
            / (np.cos(dec0) - eta * np.sin(dec0))) * np.cos(ra - ra0)

    ra = ra * 180. / np.pi
    dec = dec * 180. / np.pi
    return ra, dec
