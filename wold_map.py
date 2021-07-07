"""Exports a dict `states` that maps state codes to lists of polygons.

Author: Oliver Steele <oliver.steele@olin.edu>
License: MIT

Requirements:

    pip install BeautifulSoup
    pip install svg.path
"""

import itertools
from bs4 import BeautifulSoup
from collections import OrderedDict
from svg.path import parse_path
from lxml import etree as ET

__all__ = ['countries', 'countries_by_code', 'countries_by_name']

SEGMENT_CTL_PT_PROPS = ['start', 'control', 'control1', 'control2', 'end']
"""An ordered list of names of `svg.path` properties that hold control points."""


def get_segment_control_points(segment):
    """Given an `svg.path` segment, return its list of control points.
    Each control point is a pair of floats `(x, y)`.

    This does the minimum to support the paths in the map files.
    In particular, it simply returns the endpoints of arc segments.

    Examples:
    >>> get_segment_control_points(parse_path('M 10 20 L 30 40')[0])
    [(10.0, 20.0), (30.0, 40.0)]
    >>> get_segment_control_points(parse_path('m 10 20 l 30 40')[0])
    [(10.0, 20.0), (40.0, 60.0)]
    """

    cpts = (getattr(segment, prop) for prop in SEGMENT_CTL_PT_PROPS if hasattr(segment, prop))
    return [(pt.real, pt.imag) for pt in cpts]


def path_to_points(path):
    """Given an `svg.path` Path, return a list of its control points.
    Each control point is a pair of floats `(x, y)`.

    Examples:
    >>> path_to_points(parse_path('M 10 20 30 40'))
    [(10.0, 20.0), (30.0, 40.0)]
    >>> path_to_points(parse_path('M 10 20 30 40 100 200'))
    [(10.0, 20.0), (30.0, 40.0), (100.0, 200.0)]
    """

    pts = (pt
           for segment in path
           for pt in get_segment_control_points(segment))
    # remove duplicates
    return [pti.__next__() for _, pti in itertools.groupby(pts)]


def svg_path_to_polygons(path_data):
    """Return a list of polygons that collectively approximate the SVG path whose string is `path_data`.
    This handles just enough cases to parse the map files.

    Examples:
    >>> svg_path_to_polygons('m 10 20 30 40')
    [[(10.0, 20.0), (40.0, 60.0)]]
    >>> svg_path_to_polygons('m 10 20 30 40 z')
    [[(10.0, 20.0), (40.0, 60.0), (10.0, 20.0)]]
    >>> svg_path_to_polygons('m 10 20 30 40 z m 100 200 10 20')
    [[(10.0, 20.0), (40.0, 60.0), (10.0, 20.0)], [(110.0, 220.0), (120.0, 240.0)]]
    """

    # `svg.path` treats the Move command as though it were Line.
    # Split the path data, in order to collect one Path per contour.
    path_strings = [s for s in path_data.split('m') if s]
    path_prefix = 'm'

    polygons = []
    for path_string in path_strings:
        if path_string[0] not in 'M':
            path_string = path_prefix + path_string
        path = parse_path(path_string)
        polygons.append(path_to_points(path))
        end_pt = path[-1].end
        path_prefix = 'M %f,%f m' % (end_pt.real, end_pt.imag)

    return polygons


def _load_countries(svg_filename = 'theworld.svg'):
    """Initialize the `countries` module variable."""

    countries = {}

    with open(svg_filename, 'r') as svg:
        soup = BeautifulSoup(svg.read(),'lxml')

    for p in soup.findAll('path'):
        country_name = p.get('id', None)
        path_data = p.get('d', None)
        if country_name and path_data:
            countries[country_name] = svg_path_to_polygons(path_data)

    return OrderedDict(sorted(countries.items()))

countries= _load_countries()
"""A `dict` of state abbreviations (e.g. `"MA"`) to lists of polygons. Each polygon is a list of points.
Each point is a tuple of floats `(x, y)`."""
