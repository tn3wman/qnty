"""
PointDirectionRatios class for defining points using direction ratios.

Provides a clean interface for specifying points by distance from origin and
direction ratios (like 3-4-5, 5-12-13 triangles) common in engineering problems.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .point import _Point


class PointDirectionRatios:
    """
    Point defined by distance and direction ratios.

    This class provides a convenient way to define points using direction
    ratios, which are common in statics problems where directions are given
    as integer ratios (like 3-4-5, 5-12-13, 8-15-17 right triangles).

    The ratios define the relative proportions in each direction. The point
    is placed at the specified distance along that direction.

    Examples:
        >>> from qnty.spatial import PointDirectionRatios
        >>>
        >>> # Point at 2.5ft in direction with ratios (-5, 0, 12)
        >>> # The 5 corresponds to the 2.5ft in -x, 12 to +z
        >>> A = PointDirectionRatios(
        ...     dist=2.5, ratio_component="x",
        ...     x=-5, y=0, z=12, unit="ft"
        ... )
        >>> point = A.to_cartesian()
        >>> # Result: (-2.5, 0, 6) ft
        >>>
        >>> # Using hypotenuse as the distance reference
        >>> B = PointDirectionRatios(
        ...     dist=13, ratio_component="hyp",
        ...     x=5, y=0, z=12, unit="m"
        ... )
        >>> # Result: (5, 0, 12) m
    """

    __slots__ = ("_dist", "_ratios", "_ratio_component", "_unit", "_name", "_point")

    def __init__(
        self,
        dist: float,
        x: float,
        y: float,
        z: float = 0.0,
        ratio_component: str = "hyp",
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a point using direction ratios.

        Args:
            dist: Distance value corresponding to the ratio_component
            x: X direction ratio (positive or negative)
            y: Y direction ratio (positive or negative)
            z: Z direction ratio (positive or negative)
            ratio_component: Which component dist corresponds to:
                - "hyp": dist is the total distance (hypotenuse/magnitude)
                - "x": dist corresponds to the x ratio
                - "y": dist corresponds to the y ratio
                - "z": dist corresponds to the z ratio
            unit: Length unit for distance
            name: Optional point name

        Raises:
            ValueError: If ratio_component is invalid or ratios are all zero

        Examples:
            # Point where 2.5ft corresponds to x-ratio of -5, with z-ratio of 12
            A = PointDirectionRatios(
                dist=2.5, ratio_component="x",
                x=-5, y=0, z=12, unit="ft"
            )
            # Coordinates: (-2.5, 0, 6) ft

            # Point at total distance 13m with ratios 5-12
            B = PointDirectionRatios(
                dist=13, ratio_component="hyp",
                x=5, y=0, z=12, unit="m"
            )
            # Coordinates: (5, 0, 12) m
        """
        self._dist = float(dist)
        self._ratios = (float(x), float(y), float(z))
        self._name = name

        # Validate ratio_component
        valid_components = {"hyp", "x", "y", "z"}
        ratio_component_lower = ratio_component.lower()
        if ratio_component_lower not in valid_components:
            raise ValueError(f"Invalid ratio_component '{ratio_component}'. Must be one of: {valid_components}")
        self._ratio_component = ratio_component_lower

        # Validate ratios aren't all zero
        if x == 0 and y == 0 and z == 0:
            raise ValueError("Direction ratios cannot all be zero")

        # Resolve unit
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            self._unit = resolved
        else:
            self._unit = unit

        # Create internal _Point
        coords = self._compute_cartesian()
        self._point = _Point(coords[0], coords[1], coords[2], unit=self._unit)

    def to_cartesian(self) -> _Point:
        """
        Convert to Cartesian _Point.

        Returns:
            _Point object with x, y, z coordinates

        Examples:
            >>> A = PointDirectionRatios(dist=2.5, ratio_component="x", x=-5, z=12, y=0, unit="ft")
            >>> point = A.to_cartesian()
        """
        return self._point

    def _compute_cartesian(self) -> tuple[float, float, float]:
        """
        Compute Cartesian coordinates from direction ratios.

        Returns:
            Tuple (x, y, z) in display units
        """
        rx, ry, rz = self._ratios

        # Compute the magnitude of the ratio vector
        ratio_magnitude = math.sqrt(rx**2 + ry**2 + rz**2)

        # Determine the scale factor based on which component dist corresponds to
        if self._ratio_component == "hyp":
            # dist is the total distance
            scale = self._dist / ratio_magnitude
        elif self._ratio_component == "x":
            # dist corresponds to x ratio (absolute value)
            if rx == 0:
                raise ValueError("Cannot use ratio_component='x' when x ratio is 0")
            scale = self._dist / abs(rx)
        elif self._ratio_component == "y":
            # dist corresponds to y ratio (absolute value)
            if ry == 0:
                raise ValueError("Cannot use ratio_component='y' when y ratio is 0")
            scale = self._dist / abs(ry)
        else:  # z
            # dist corresponds to z ratio (absolute value)
            if rz == 0:
                raise ValueError("Cannot use ratio_component='z' when z ratio is 0")
            scale = self._dist / abs(rz)

        # Scale the ratios to get coordinates
        x = rx * scale
        y = ry * scale
        z = rz * scale

        return (x, y, z)

    @property
    def x(self) -> float:
        """X coordinate in display unit."""
        return self._compute_cartesian()[0]

    @property
    def y(self) -> float:
        """Y coordinate in display unit."""
        return self._compute_cartesian()[1]

    @property
    def z(self) -> float:
        """Z coordinate in display unit."""
        return self._compute_cartesian()[2]

    @property
    def dist(self) -> float:
        """Distance value in display unit."""
        return self._dist

    @property
    def ratios(self) -> tuple[float, float, float]:
        """Direction ratios (x, y, z)."""
        return self._ratios

    @property
    def unit(self) -> Unit | None:
        """Length unit."""
        return self._unit

    @property
    def name(self) -> str | None:
        """Point name."""
        return self._name

    def __str__(self) -> str:
        """String representation."""
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        rx, ry, rz = self._ratios
        return f"PointDirectionRatios({self._dist}{unit_str}, ratios=({rx}, {ry}, {rz}), {self._ratio_component})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
