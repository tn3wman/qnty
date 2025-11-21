"""
VectorSpherical class for defining vectors using spherical coordinates.

Provides a clean interface for specifying vectors by magnitude,
theta (azimuth), and phi (transverse) angles.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .vector import _Vector


class VectorSpherical:
    """
    Vector defined by magnitude and spherical angles (theta, phi).

    This class provides a convenient way to define 3D vectors using spherical
    coordinates:
    - magnitude: length of the vector
    - theta: azimuth angle in the x-y plane (from +x axis)
    - phi: transverse angle from +z axis

    The conversion formulas are:
    - u = magnitude * sin(phi) * cos(theta)
    - v = magnitude * sin(phi) * sin(theta)
    - w = magnitude * cos(phi)

    Examples:
        >>> from qnty.spatial import VectorSpherical
        >>>
        >>> # Vector with magnitude 10m, theta=30 deg, phi=60 deg
        >>> v = VectorSpherical(magnitude=10, theta=30, phi=60, unit="m")
        >>> vec = v.to_cartesian()
    """

    __slots__ = ("_magnitude", "_theta_rad", "_phi_rad", "_unit", "_name", "_vector")

    def __init__(
        self,
        magnitude: float,
        theta: float,
        phi: float,
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a vector using spherical coordinates.

        Args:
            magnitude: Vector magnitude
            theta: Azimuth angle in x-y plane from +x axis
            phi: Transverse angle from +z axis
            unit: Unit for magnitude
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional vector name

        Examples:
            # Vector with magnitude 10m, theta=30 deg, phi=60 deg
            v = VectorSpherical(magnitude=10, theta=30, phi=60, unit="m")
        """
        self._name = name
        self._magnitude = float(magnitude)

        # Convert angles to radians
        if angle_unit.lower() in ("degree", "degrees", "deg"):
            self._theta_rad = math.radians(float(theta))
            self._phi_rad = math.radians(float(phi))
        elif angle_unit.lower() in ("radian", "radians", "rad"):
            self._theta_rad = float(theta)
            self._phi_rad = float(phi)
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

        # Compute Cartesian components
        u = self._magnitude * math.sin(self._phi_rad) * math.cos(self._theta_rad)
        v = self._magnitude * math.sin(self._phi_rad) * math.sin(self._theta_rad)
        w = self._magnitude * math.cos(self._phi_rad)

        # Create internal _Vector
        self._vector = _Vector(u, v, w, unit=self._unit)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Examples:
            >>> v = VectorSpherical(magnitude=10, theta=30, phi=60, unit="m")
            >>> vec = v.to_cartesian()
        """
        return self._vector

    @property
    def u(self) -> float:
        """First component in display unit."""
        return self._vector.to_array()[0]

    @property
    def v(self) -> float:
        """Second component in display unit."""
        return self._vector.to_array()[1]

    @property
    def w(self) -> float:
        """Third component in display unit."""
        return self._vector.to_array()[2]

    @property
    def magnitude_value(self) -> float:
        """Magnitude in display unit."""
        return self._magnitude

    @property
    def theta_deg(self) -> float:
        """Azimuth angle in degrees."""
        return math.degrees(self._theta_rad)

    @property
    def theta_rad(self) -> float:
        """Azimuth angle in radians."""
        return self._theta_rad

    @property
    def phi_deg(self) -> float:
        """Transverse angle in degrees."""
        return math.degrees(self._phi_rad)

    @property
    def phi_rad(self) -> float:
        """Transverse angle in radians."""
        return self._phi_rad

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
        return f"VectorSpherical({self._magnitude}{unit_str}, θ={self.theta_deg}°, φ={self.phi_deg}°)"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
