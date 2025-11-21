"""
VectorPolar class for defining vectors using polar/cylindrical coordinates.

Provides a clean interface for specifying vectors by magnitude and angle
in a specific plane, which is common in engineering problems.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .vector import _Vector


class VectorPolar:
    """
    Vector defined by magnitude and angle in a plane.

    This class provides a convenient way to define vectors using polar
    coordinates within a specific plane (xy, xz, or yz).

    Examples:
        >>> from qnty.spatial import VectorPolar
        >>>
        >>> # Vector at 5m, 30 deg from +x axis in xy plane
        >>> v = VectorPolar(magnitude=5, angle=30, plane="xy", wrt="+x", unit="m")
        >>> vec = v.to_cartesian()
        >>> print(vec)  # _Vector(4.33, 2.5, 0 m)
        >>>
        >>> # Vector at 100N, 45 deg from +y axis in xy plane
        >>> v2 = VectorPolar(magnitude=100, angle=45, plane="xy", wrt="+y", unit="N")
    """

    __slots__ = ("_magnitude", "_angle_rad", "_plane", "_wrt", "_unit", "_name", "_vector")

    def __init__(
        self,
        magnitude: float,
        angle: float,
        plane: str = "xy",
        wrt: str = "+x",
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a vector using polar coordinates in a plane.

        Args:
            magnitude: Vector magnitude
            angle: Angle measured from reference axis (CCW positive)
            plane: Plane containing the vector ("xy", "xz", "yz")
            wrt: Reference axis for angle ("+x", "-x", "+y", "-y", "+z", "-z")
            unit: Unit for magnitude
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional vector name

        Raises:
            ValueError: If plane or wrt is invalid

        Examples:
            # Vector in xy plane, 5m magnitude, 30 deg from +x axis
            v = VectorPolar(magnitude=5, angle=30, plane="xy", wrt="+x", unit="m")

            # Vector in xz plane, 100N magnitude, 45 deg from +z axis
            v2 = VectorPolar(magnitude=100, angle=45, plane="xz", wrt="+z", unit="N")
        """
        self._name = name
        self._magnitude = float(magnitude)

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

        # Create internal _Vector
        u, v, w = self._compute_cartesian()
        self._vector = _Vector(u, v, w, unit=self._unit)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Examples:
            >>> v = VectorPolar(magnitude=5, angle=30, plane="xy", wrt="+x", unit="m")
            >>> vec = v.to_cartesian()
        """
        return self._vector

    def _compute_cartesian(self) -> tuple[float, float, float]:
        """
        Compute Cartesian components from polar definition.

        Returns:
            Tuple (u, v, w) in display units
        """
        # Determine the reference angle for the wrt axis
        axis_angles = {
            "xy": {"+x": 0, "+y": 90, "-x": 180, "-y": 270},
            "xz": {"+x": 0, "+z": 90, "-x": 180, "-z": 270},
            "yz": {"+y": 0, "+z": 90, "-y": 180, "-z": 270},
        }

        # Get the base angle for the reference axis
        base_angle_deg = axis_angles[self._plane][self._wrt]

        # Total angle in the plane (CCW from first axis of plane)
        total_angle_rad = math.radians(base_angle_deg) + self._angle_rad

        # Compute components based on plane
        if self._plane == "xy":
            u = self._magnitude * math.cos(total_angle_rad)
            v = self._magnitude * math.sin(total_angle_rad)
            w = 0.0
        elif self._plane == "xz":
            u = self._magnitude * math.cos(total_angle_rad)
            v = 0.0
            w = self._magnitude * math.sin(total_angle_rad)
        else:  # yz
            u = 0.0
            v = self._magnitude * math.cos(total_angle_rad)
            w = self._magnitude * math.sin(total_angle_rad)

        return (u, v, w)

    @property
    def u(self) -> float:
        """First component in display unit."""
        return self._compute_cartesian()[0]

    @property
    def v(self) -> float:
        """Second component in display unit."""
        return self._compute_cartesian()[1]

    @property
    def w(self) -> float:
        """Third component in display unit."""
        return self._compute_cartesian()[2]

    @property
    def magnitude_value(self) -> float:
        """Magnitude in display unit."""
        return self._magnitude

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
        """Plane containing the vector."""
        return self._plane

    @property
    def wrt(self) -> str:
        """Reference axis for angle."""
        return self._wrt

    @property
    def unit(self) -> Unit | None:
        """Unit."""
        return self._unit

    @property
    def name(self) -> str | None:
        """Vector name."""
        return self._name

    def __str__(self) -> str:
        """String representation."""
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        return f"VectorPolar({self._magnitude}{unit_str}, {self.angle_deg}° from {self._wrt} in {self._plane})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
