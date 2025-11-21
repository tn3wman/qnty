"""
PointCartesian class for defining points using Cartesian coordinates.

Provides a clean interface for specifying points with explicit x, y, z
coordinates with default values of zero for unspecified components.
"""

from __future__ import annotations

from types import EllipsisType

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

    __slots__ = ("_point", "_name", "_unknowns")

    def __init__(
        self,
        x: float | EllipsisType = 0.0,
        y: float | EllipsisType = 0.0,
        z: float | EllipsisType = 0.0,
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

            # Point with unknown z coordinate
            D = PointCartesian(x=4, y=2, z=..., unit="m")
        """
        self._name = name

        # Track which coordinates are unknown (ellipsis)
        self._unknowns: dict[str, str] = {}

        # Handle ellipsis for unknown coordinates
        x_val = 0.0
        y_val = 0.0
        z_val = 0.0

        if x is ...:
            self._unknowns["x"] = "x"
        else:
            x_val = float(x)

        if y is ...:
            self._unknowns["y"] = "y"
        else:
            y_val = float(y)

        if z is ...:
            self._unknowns["z"] = "z"
        else:
            z_val = float(z)

        # Resolve unit
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            unit = resolved

        # Create internal _Point (unknowns stored as 0.0 temporarily)
        self._point = _Point(x_val, y_val, z_val, unit=unit)

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

    @property
    def unknowns(self) -> dict[str, str]:
        """Dictionary of unknown coordinates."""
        return self._unknowns

    @property
    def has_unknowns(self) -> bool:
        """Check if point has any unknown coordinates."""
        return len(self._unknowns) > 0

    def set_coordinate(self, coord: str, value: float) -> None:
        """
        Set a coordinate value (lock it as known).

        Args:
            coord: Coordinate name ('x', 'y', or 'z')
            value: Value in current unit

        Examples:
            >>> B = PointCartesian(x=0, y=0, z=..., unit="m")
            >>> B.set_coordinate('z', 6.0)  # Lock z to 6m
        """
        if coord not in ('x', 'y', 'z'):
            raise ValueError(f"Invalid coordinate '{coord}', must be 'x', 'y', or 'z'")

        # Remove from unknowns if present
        if coord in self._unknowns:
            del self._unknowns[coord]

        # Update internal point coordinates
        coords = list(self._point._coords)
        idx = {'x': 0, 'y': 1, 'z': 2}[coord]

        # Convert value to SI
        if self._point._unit is not None:
            coords[idx] = value * self._point._unit.si_factor
        else:
            coords[idx] = value

        import numpy as np
        self._point._coords = np.array(coords, dtype=float)

    def unlock_coordinate(self, coord: str) -> None:
        """
        Unlock a coordinate (make it unknown to solve for).

        Args:
            coord: Coordinate name ('x', 'y', or 'z')

        Examples:
            >>> B = PointCartesian(x=0, y=0, z=6, unit="m")
            >>> B.unlock_coordinate('y')  # Make y unknown
        """
        if coord not in ('x', 'y', 'z'):
            raise ValueError(f"Invalid coordinate '{coord}', must be 'x', 'y', or 'z'")

        # Add to unknowns
        self._unknowns[coord] = coord

        # Set coordinate to 0 in internal point (placeholder)
        coords = list(self._point._coords)
        idx = {'x': 0, 'y': 1, 'z': 2}[coord]
        coords[idx] = 0.0

        import numpy as np
        self._point._coords = np.array(coords, dtype=float)

    def to_unit(self, unit: Unit | str) -> PointCartesian:
        """
        Convert to different display unit.

        Args:
            unit: Target unit for display (e.g., "ft", "in", "mm")

        Returns:
            New PointCartesian with coordinates in target unit

        Examples:
            >>> A = PointCartesian(x=1, y=2, z=3, unit="m")
            >>> A_ft = A.to_unit("ft")
            >>> print(A_ft)
            PointCartesian(3.28084, 6.56168, 9.84252 ft)
        """
        # Convert internal _Point to new unit
        converted_point = self._point.to_unit(unit)

        # Get coordinates in new unit
        coords = converted_point.to_array()

        # Create new PointCartesian with converted values
        result = PointCartesian(
            x=coords[0],
            y=coords[1],
            z=coords[2],
            unit=converted_point._unit,
            name=self._name
        )
        return result

    def __str__(self) -> str:
        """String representation."""
        coords = self._point.to_array()
        unit_str = f" {self._point._unit.symbol}" if self._point._unit else ""

        # Format coordinates, showing '...' for unknowns
        x_str = "..." if "x" in self._unknowns else f"{coords[0]:.6g}"
        y_str = "..." if "y" in self._unknowns else f"{coords[1]:.6g}"
        z_str = "..." if "z" in self._unknowns else f"{coords[2]:.6g}"

        return f"PointCartesian({x_str}, {y_str}, {z_str}){unit_str}"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
