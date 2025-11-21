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
from .point_cartesian import PointCartesian
from .point_direction_angles import PointDirectionAngles
from .point_direction_ratios import PointDirectionRatios
from .point_polar import PointPolar
from .point_spherical import PointSpherical
from .vector import _Vector, Vector
from .vector_cartesian import VectorCartesian
from .vector_direction_angles import VectorDirectionAngles
from .vector_direction_ratios import VectorDirectionRatios
from .vector_polar import VectorPolar
from .vector_spherical import VectorSpherical
from .force_vector import ForceVector
from .position_vector import PositionVector
from .vector_between import VectorBetween

__all__ = [
    "_Point",
    "Point",
    "PointCartesian",
    "PointDirectionAngles",
    "PointDirectionRatios",
    "PointPolar",
    "PointSpherical",
    "_Vector",
    "Vector",
    "VectorCartesian",
    "VectorDirectionAngles",
    "VectorDirectionRatios",
    "VectorPolar",
    "VectorSpherical",
    "ForceVector",
    "PositionVector",
    "VectorBetween",
]
