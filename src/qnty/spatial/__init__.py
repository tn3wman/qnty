"""
Spatial Module
==============

Provides Point and Vector classes for 3D spatial calculations with units.

Examples:
    >>> from qnty.spatial import Point, Vector
    >>> from qnty.core.unit_catalog import LengthUnits
    >>>
    >>> # Create points with units
    >>> p1 = Point(10.0, 20.0, 30.0, unit=LengthUnits.meter)
    >>> p2 = Point(5.0, 10.0, 0.0, unit=LengthUnits.meter)
    >>>
    >>> # Compute displacement
    >>> displacement = p2 - p1
    >>>
    >>> # Compute distance
    >>> distance = p1.distance_to(p2)
    >>> print(distance)
    26.9258 m
    >>>
    >>> # Create vectors
    >>> v1 = Vector(1.0, 0.0, 0.0, unit=LengthUnits.meter)
    >>> v2 = Vector(0.0, 1.0, 0.0, unit=LengthUnits.meter)
    >>>
    >>> # Vector operations
    >>> v3 = v1.cross(v2)  # Cross product
    >>> dot = v1.dot(v2)   # Dot product
"""

from .point import _Point, Point
from .points import create_point_cartesian, create_point_from_ratio, create_point_polar, create_point_spherical
from .point_direction_angles import PointDirectionAngles
from .vector import _Vector, Vector, ForceVector
from .vectors import create_vector_cartesian, create_vector_from_points, create_vector_from_ratio, create_vector_polar, create_vector_spherical
from .vector_direction_angles import VectorDirectionAngles
from .vector_direction_ratios import VectorDirectionRatios
from .vector_between import VectorBetween

__all__ = [
    "_Point",
    "Point",
    "create_point_cartesian",
    "create_point_from_ratio",
    "create_point_polar",
    "create_point_spherical",
    "PointDirectionAngles",
    "_Vector",
    "Vector",
    "create_vector_cartesian",
    "create_vector_from_points",
    "create_vector_from_ratio",
    "create_vector_polar",
    "create_vector_spherical",
    "VectorDirectionAngles",
    "VectorDirectionRatios",
    "ForceVector",
    "VectorBetween",
]
