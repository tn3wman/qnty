"""
PointSpherical class for defining points using spherical coordinates.

Provides a clean interface for specifying points with distance from origin,
transverse angle (theta) in the xy-plane, and azimuth angle (phi) from z-axis.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .point import _Point


class PointSpherical:
    """
    Point defined by spherical coordinates (distance, theta, phi).

    This class provides a convenient way to define points using:
    - dist: Distance from origin
    - theta: Transverse angle in xy-plane (CCW from +x by default)
    - phi: Azimuth angle from +z axis (CW from +z by default)

    Examples:
        >>> from qnty.spatial import PointSpherical
        >>>
        >>> # Point at 10m, theta=30° from +x in xy-plane, phi=60° from +z
        >>> A = PointSpherical(dist=10, theta=30, phi=60, unit="m")
        >>> point = A.to_cartesian()
        >>>
        >>> # With custom reference axes
        >>> B = PointSpherical(dist=5, theta=45, phi=30, theta_wrt="+y", phi_wrt="-z", unit="ft")
    """

    __slots__ = ("_dist", "_theta_rad", "_phi_rad", "_unit", "_name", "_point")

    def __init__(
        self,
        dist: float,
        theta: float = 0.0,
        phi: float = 0.0,
        theta_wrt: str = "+x",
        phi_wrt: str = "+z",
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a point using spherical coordinates.

        Args:
            dist: Distance from origin
            theta: Transverse angle in xy-plane (CCW from theta_wrt axis)
            phi: Azimuth angle (CW from phi_wrt axis, toward xy-plane)
            theta_wrt: Reference axis for theta ("+x", "-x", "+y", "-y")
            phi_wrt: Reference for phi ("+z", "-z", "xy")
                - "+z": angle measured from +z axis toward xy-plane
                - "-z": angle measured from -z axis toward xy-plane
                - "xy": angle measured from xy-plane (+phi toward +z, -phi toward -z)
            unit: Length unit for distance
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional point name

        Raises:
            ValueError: If theta_wrt or phi_wrt is invalid

        Notes:
            The coordinate system follows physics convention:
            - theta: angle in xy-plane, measured CCW from reference axis
            - phi: angle from z-axis toward xy-plane

            Standard formulas:
            - x = dist * sin(phi) * cos(theta)
            - y = dist * sin(phi) * sin(theta)
            - z = dist * cos(phi)

        Examples:
            # Point with theta=30° from +x, phi=60° from +z
            A = PointSpherical(dist=10, theta=30, phi=60, unit="m")

            # Point with theta measured from +y axis
            B = PointSpherical(dist=5, theta=45, theta_wrt="+y", phi=30, unit="ft")

            # Point with phi measured from xy-plane (elevation angle)
            C = PointSpherical(dist=10, theta=30, phi=70, theta_wrt="+y", phi_wrt="xy", unit="ft")
        """
        self._dist = float(dist)
        self._name = name

        # Validate theta_wrt
        valid_theta_axes = {"+x", "-x", "+y", "-y"}
        theta_wrt_lower = theta_wrt.lower()
        if theta_wrt_lower not in valid_theta_axes:
            raise ValueError(f"Invalid theta_wrt '{theta_wrt}'. Must be one of: {valid_theta_axes}")

        # Validate phi_wrt
        valid_phi_axes = {"+z", "-z", "xy"}
        phi_wrt_lower = phi_wrt.lower()
        if phi_wrt_lower not in valid_phi_axes:
            raise ValueError(f"Invalid phi_wrt '{phi_wrt}'. Must be one of: {valid_phi_axes}")

        # Convert angles to radians
        if angle_unit.lower() in ("degree", "degrees", "deg"):
            theta_input_rad = math.radians(float(theta))
            phi_input_rad = math.radians(float(phi))
        elif angle_unit.lower() in ("radian", "radians", "rad"):
            theta_input_rad = float(theta)
            phi_input_rad = float(phi)
        else:
            raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

        # Convert theta to standard form (CCW from +x)
        theta_base_angles = {
            "+x": 0,
            "+y": 90,
            "-x": 180,
            "-y": 270,
        }
        theta_base_rad = math.radians(theta_base_angles[theta_wrt_lower])
        self._theta_rad = theta_base_rad + theta_input_rad

        # Convert phi to standard form (from +z)
        # If phi_wrt is -z, then the angle is measured from -z toward xy-plane
        # In standard form, this means phi_standard = 180° - phi_input
        # If phi_wrt is xy, angle is from xy-plane: +phi goes toward +z, -phi goes toward -z
        # In standard form, phi_standard = 90° - phi_input
        if phi_wrt_lower == "+z":
            self._phi_rad = phi_input_rad
        elif phi_wrt_lower == "-z":
            self._phi_rad = math.pi - phi_input_rad
        else:  # xy
            self._phi_rad = math.pi / 2 - phi_input_rad

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
            >>> A = PointSpherical(dist=10, theta=30, phi=60, unit="m")
            >>> point = A.to_cartesian()
        """
        return self._point

    def _compute_cartesian(self) -> tuple[float, float, float]:
        """
        Compute Cartesian coordinates from spherical definition.

        Returns:
            Tuple (x, y, z) in display units
        """
        # Standard spherical to Cartesian conversion:
        # x = r * sin(phi) * cos(theta)
        # y = r * sin(phi) * sin(theta)
        # z = r * cos(phi)
        x = self._dist * math.sin(self._phi_rad) * math.cos(self._theta_rad)
        y = self._dist * math.sin(self._phi_rad) * math.sin(self._theta_rad)
        z = self._dist * math.cos(self._phi_rad)

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
    def theta_rad(self) -> float:
        """Theta angle in radians (standard form, CCW from +x)."""
        return self._theta_rad

    @property
    def phi_rad(self) -> float:
        """Phi angle in radians (standard form, from +z)."""
        return self._phi_rad

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
        theta_deg = math.degrees(self._theta_rad)
        phi_deg = math.degrees(self._phi_rad)
        return f"PointSpherical({self._dist}{unit_str}, theta={theta_deg:.1f}deg, phi={phi_deg:.1f}deg)"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
