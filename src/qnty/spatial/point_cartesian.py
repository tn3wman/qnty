"""
PointCartesian class for defining points using Cartesian coordinates.

Provides a clean interface for specifying points with explicit x, y, z
coordinates with default values of zero for unspecified components.
"""

from __future__ import annotations

from ..core.unit import Unit
from .point import _Point


class PointCartesian:
    """
    Point defined by x, y, z Cartesian coordinates.

    This class provides a convenient way to define points with explicit
    coordinates, where unspecified coordinates default to zero.

    Examples:
        >>> from qnty.spatial import PointCartesian
        >>>
        >>> # Point with all coordinates
        >>> A = PointCartesian(x=2, y=-3, z=6, unit="m")
        >>>
        >>> # Point with default z=0
        >>> B = PointCartesian(x=5, y=10, unit="ft")
        >>>
        >>> # Point on z-axis
        >>> C = PointCartesian(z=300, unit="mm")
    """

    __slots__ = ("_point", "_name")

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a point using Cartesian coordinates.

        Args:
            x: X coordinate (default 0.0)
            y: Y coordinate (default 0.0)
            z: Z coordinate (default 0.0)
            unit: Length unit for coordinates
            name: Optional point name

        Examples:
            # Full 3D point
            A = PointCartesian(x=2, y=-3, z=6, unit="m")

            # 2D point (z=0)
            B = PointCartesian(x=5, y=10, unit="ft")

            # Point on axis
            C = PointCartesian(z=300, unit="mm")
        """
        self._name = name

        # Resolve unit
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            unit = resolved

        # Create internal _Point
        self._point = _Point(float(x), float(y), float(z), unit=unit)

    def to_cartesian(self) -> _Point:
        """
        Convert to Cartesian _Point.

        Returns:
            _Point object with x, y, z coordinates

        Examples:
            >>> A = PointCartesian(x=2, y=-3, z=6, unit="m")
            >>> point = A.to_cartesian()
        """
        return self._point

    @property
    def x(self) -> float:
        """X coordinate in display unit."""
        return self._point.to_array()[0]

    @property
    def y(self) -> float:
        """Y coordinate in display unit."""
        return self._point.to_array()[1]

    @property
    def z(self) -> float:
        """Z coordinate in display unit."""
        return self._point.to_array()[2]

    @property
    def unit(self) -> Unit | None:
        """Length unit."""
        return self._point._unit

    @property
    def name(self) -> str | None:
        """Point name."""
        return self._name

    def __str__(self) -> str:
        """String representation."""
        coords = self._point.to_array()
        unit_str = f" {self._point._unit.symbol}" if self._point._unit else ""
        return f"PointCartesian({coords[0]:.6g}, {coords[1]:.6g}, {coords[2]:.6g}{unit_str})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
