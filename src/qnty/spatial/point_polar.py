"""
PointPolar class for defining points using polar/cylindrical coordinates.

Provides a clean interface for specifying points by distance and angle
in a specific plane, which is common in engineering problems.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .point import _Point


class PointPolar:
    """
    Point defined by distance from origin and angle in a plane.

    This class provides a convenient way to define points using polar
    coordinates within a specific plane (xy, xz, or yz).

    Examples:
        >>> from qnty.spatial import PointPolar
        >>>
        >>> # Point at 150mm, 30° from -z axis in xz plane
        >>> A = PointPolar(dist=150, angle=30, plane="xz", wrt="-z", unit="mm")
        >>> point = A.to_cartesian()
        >>> print(point)  # Point(-129.9, 0, -75 mm)
        >>>
        >>> # Point at 5ft, 30° from +x axis in xy plane
        >>> B = PointPolar(dist=5, angle=30, plane="xy", wrt="+x", unit="ft")
        >>> point = B.to_cartesian()
        >>> print(point)  # Point(4.33, 2.5, 0 ft)
    """

    __slots__ = ("_dist", "_angle_rad", "_plane", "_wrt", "_unit", "_name", "_point")

    def __init__(
        self,
        dist: float,
        angle: float,
        plane: str = "xy",
        wrt: str = "+x",
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a point using polar coordinates in a plane.

        Args:
            dist: Distance from origin
            angle: Angle measured from reference axis (CCW positive)
            plane: Plane containing the point ("xy", "xz", "yz")
            wrt: Reference axis for angle ("+x", "-x", "+y", "-y", "+z", "-z")
            unit: Length unit for distance
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional point name

        Raises:
            ValueError: If plane or wrt is invalid

        Examples:
            # Point in xz plane, 150mm from origin, 30° from -z axis
            A = PointPolar(dist=150, angle=30, plane="xz", wrt="-z", unit="mm")

            # Point in xy plane, 5ft from origin, 30° from +x axis
            B = PointPolar(dist=5, angle=30, plane="xy", wrt="+x", unit="ft")
        """
        self._name = name
        self._dist = float(dist)

        # Validate plane
        valid_planes = {"xy", "xz", "yz"}
        if plane.lower() not in valid_planes:
            raise ValueError(f"Invalid plane '{plane}'. Must be one of: {valid_planes}")
        self._plane = plane.lower()

        # Validate wrt axis
        valid_axes = {"+x", "-x", "+y", "-y", "+z", "-z"}
        wrt_lower = wrt.lower()
        if wrt_lower not in valid_axes:
            raise ValueError(f"Invalid wrt axis '{wrt}'. Must be one of: {valid_axes}")
        self._wrt = wrt_lower

        # Validate wrt axis is in the specified plane
        axis_char = wrt_lower[1]  # 'x', 'y', or 'z'
        if axis_char not in self._plane:
            raise ValueError(
                f"Reference axis '{wrt}' must be in plane '{plane}'. "
                f"Valid axes for {plane} plane: {[f'+{c}' for c in plane] + [f'-{c}' for c in plane]}"
            )

        # Convert angle to radians
        if angle_unit.lower() in ("degree", "degrees", "deg"):
            self._angle_rad = math.radians(float(angle))
        elif angle_unit.lower() in ("radian", "radians", "rad"):
            self._angle_rad = float(angle)
        else:
            raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

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
        x, y, z = self._compute_cartesian()
        self._point = _Point(x, y, z, unit=self._unit)

    def to_cartesian(self) -> _Point:
        """
        Convert to Cartesian Point.

        Returns:
            Point object with x, y, z coordinates

        Examples:
            >>> A = PointPolar(dist=150, angle=30, plane="xz", wrt="-z", unit="mm")
            >>> point = A.to_cartesian()
        """
        return self._point

    def _compute_cartesian(self) -> tuple[float, float, float]:
        """
        Compute Cartesian coordinates from polar definition.

        Returns:
            Tuple (x, y, z) in display units
        """
        # Determine the reference angle for the wrt axis
        # We need to map from angle measured from wrt axis to standard coordinates

        # For each plane, define the angle that corresponds to each axis
        # Angles are measured CCW when looking at the plane from the positive
        # direction of the axis perpendicular to the plane

        axis_angles = {
            "xy": {"+x": 0, "+y": 90, "-x": 180, "-y": 270},
            "xz": {"+x": 0, "+z": 90, "-x": 180, "-z": 270},
            "yz": {"+y": 0, "+z": 90, "-y": 180, "-z": 270},
        }

        # Get the base angle for the reference axis
        base_angle_deg = axis_angles[self._plane][self._wrt]

        # Total angle in the plane (CCW from first axis of plane)
        total_angle_rad = math.radians(base_angle_deg) + self._angle_rad

        # Compute coordinates based on plane
        if self._plane == "xy":
            x = self._dist * math.cos(total_angle_rad)
            y = self._dist * math.sin(total_angle_rad)
            z = 0.0
        elif self._plane == "xz":
            x = self._dist * math.cos(total_angle_rad)
            y = 0.0
            z = self._dist * math.sin(total_angle_rad)
        else:  # yz
            x = 0.0
            y = self._dist * math.cos(total_angle_rad)
            z = self._dist * math.sin(total_angle_rad)

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
        """Distance from origin in display unit."""
        return self._dist

    @property
    def angle_deg(self) -> float:
        """Angle in degrees."""
        return math.degrees(self._angle_rad)

    @property
    def angle_rad(self) -> float:
        """Angle in radians."""
        return self._angle_rad

    @property
    def plane(self) -> str:
        """Plane containing the point."""
        return self._plane

    @property
    def wrt(self) -> str:
        """Reference axis for angle."""
        return self._wrt

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
        return f"PointPolar({self._dist}{unit_str}, {self.angle_deg}° from {self._wrt} in {self._plane})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
