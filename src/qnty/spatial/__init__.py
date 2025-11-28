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
from .points import create_point_along, create_point_cartesian, create_point_direction_angles, create_point_from_ratio, create_point_polar, create_point_spherical
from .vector import _Vector, _Vector, _Vector
from .vectors import _VectorWithUnknowns, create_point_at_midpoint, create_vector_along, create_vector_cartesian, create_vector_direction_angles, create_vector_from_points, create_vector_from_ratio, create_vector_in_plane, create_vector_polar, create_vector_resultant, create_vector_resultant_cartesian, create_vector_resultant_polar, create_vector_spherical, create_vector_with_magnitude
from .vector_direction_ratios import VectorDirectionRatios
from .vector_between import VectorBetween
from .plane import Plane, create_plane_rotated_x, create_plane_rotated_y, create_plane_rotated_z

__all__ = [
    "_Point",
    "Point",
    "create_point_along",
    "create_point_at_midpoint",
    "create_point_cartesian",
    "create_point_direction_angles",
    "create_point_from_ratio",
    "create_point_polar",
    "create_point_spherical",
    "_Vector",
    "_VectorWithUnknowns",
    "_Vector",
    "create_vector_along",
    "create_vector_cartesian",
    "create_vector_direction_angles",
    "create_vector_from_points",
    "create_vector_from_ratio",
    "create_vector_in_plane",
    "create_vector_polar",
    "create_vector_resultant",
    "create_vector_resultant_cartesian",
    "create_vector_resultant_polar",
    "create_vector_spherical",
    "create_vector_with_magnitude",
    "VectorDirectionRatios",
    "_Vector",
    "VectorBetween",
    "Plane",
    "create_plane_rotated_x",
    "create_plane_rotated_y",
    "create_plane_rotated_z",
]
