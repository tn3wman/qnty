"""
PointDirectionAngles class for defining points using coordinate direction angles.

Provides a clean interface for specifying points by distance from origin and
coordinate direction angles (alpha, beta, gamma) measured from +x, +y, +z axes.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from ..utils.shared_utilities import resolve_length_unit_from_string
from .point import _Point
from .vector_helpers import compute_direction_cosines


class PointDirectionAngles:
    """
    Point defined by distance and coordinate direction angles.

    This class provides a convenient way to define points using:
    - dist: Distance from origin
    - alpha: Angle from +x axis (0 to 180 degrees)
    - beta: Angle from +y axis (0 to 180 degrees)
    - gamma: Angle from +z axis (0 to 180 degrees)

    The direction cosines are: cos(alpha), cos(beta), cos(gamma)
    And the coordinates are: x = dist * cos(alpha), y = dist * cos(beta), z = dist * cos(gamma)

    Note: The angles must satisfy: cos^2(alpha) + cos^2(beta) + cos^2(gamma) = 1

    Examples:
        >>> from qnty.spatial import PointDirectionAngles
        >>>
        >>> # Point at 10m with direction angles
        >>> A = PointDirectionAngles(dist=10, alpha=60, beta=45, gamma=120, unit="m")
        >>> point = A.to_cartesian()
    """

    __slots__ = ("_dist", "_alpha_rad", "_beta_rad", "_gamma_rad", "_unit", "_name", "_point")

    def __init__(
        self,
        dist: float,
        alpha: float,
        beta: float,
        gamma: float,
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a point using coordinate direction angles.

        Args:
            dist: Distance from origin
            alpha: Angle from +x axis (0 to 180)
            beta: Angle from +y axis (0 to 180)
            gamma: Angle from +z axis (0 to 180)
            unit: Length unit for distance
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional point name

        Raises:
            ValueError: If angles don't satisfy the constraint cos^2(a) + cos^2(b) + cos^2(g) = 1

        Examples:
            # Point with direction angles
            A = PointDirectionAngles(dist=10, alpha=60, beta=45, gamma=120, unit="m")
        """
        self._dist = float(dist)
        self._name = name

        # Convert angles to radians
        if angle_unit.lower() in ("degree", "degrees", "deg"):
            self._alpha_rad = math.radians(float(alpha))
            self._beta_rad = math.radians(float(beta))
            self._gamma_rad = math.radians(float(gamma))
        elif angle_unit.lower() in ("radian", "radians", "rad"):
            self._alpha_rad = float(alpha)
            self._beta_rad = float(beta)
            self._gamma_rad = float(gamma)
        else:
            raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

        # Validate: cos^2(alpha) + cos^2(beta) + cos^2(gamma) = 1
        cos_alpha = math.cos(self._alpha_rad)
        cos_beta = math.cos(self._beta_rad)
        cos_gamma = math.cos(self._gamma_rad)
        sum_squares = cos_alpha**2 + cos_beta**2 + cos_gamma**2

        if abs(sum_squares - 1.0) > 0.01:  # Allow some tolerance
            raise ValueError(
                f"Invalid direction angles: cos^2(alpha) + cos^2(beta) + cos^2(gamma) = {sum_squares:.4f}, must equal 1. "
                f"Got alpha={math.degrees(self._alpha_rad):.1f}, beta={math.degrees(self._beta_rad):.1f}, gamma={math.degrees(self._gamma_rad):.1f}"
            )

        # Resolve unit
        self._unit = resolve_length_unit_from_string(unit)

        # Create internal _Point
        x, y, z = self._compute_cartesian()
        self._point = _Point(x, y, z, unit=self._unit)

    def to_cartesian(self) -> _Point:
        """
        Convert to Cartesian _Point.

        Returns:
            _Point object with x, y, z coordinates

        Examples:
            >>> A = PointDirectionAngles(dist=10, alpha=60, beta=45, gamma=120, unit="m")
            >>> point = A.to_cartesian()
        """
        return self._point

    def _compute_cartesian(self) -> tuple[float, float, float]:
        """
        Compute Cartesian coordinates from direction angles.

        Returns:
            Tuple (x, y, z) in display units
        """
        # x = dist * cos(alpha)
        # y = dist * cos(beta)
        # z = dist * cos(gamma)
        x = self._dist * math.cos(self._alpha_rad)
        y = self._dist * math.cos(self._beta_rad)
        z = self._dist * math.cos(self._gamma_rad)

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
    def alpha_rad(self) -> float:
        """Alpha angle in radians."""
        return self._alpha_rad

    @property
    def beta_rad(self) -> float:
        """Beta angle in radians."""
        return self._beta_rad

    @property
    def gamma_rad(self) -> float:
        """Gamma angle in radians."""
        return self._gamma_rad

    @property
    def alpha_deg(self) -> float:
        """Alpha angle in degrees."""
        return math.degrees(self._alpha_rad)

    @property
    def beta_deg(self) -> float:
        """Beta angle in degrees."""
        return math.degrees(self._beta_rad)

    @property
    def gamma_deg(self) -> float:
        """Gamma angle in degrees."""
        return math.degrees(self._gamma_rad)

    @property
    def direction_cosines(self) -> tuple[float, float, float]:
        """Direction cosines (cos(alpha), cos(beta), cos(gamma))."""
        return compute_direction_cosines(self._alpha_rad, self._beta_rad, self._gamma_rad)

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
        return (
            f"PointDirectionAngles({self._dist}{unit_str}, "
            f"alpha={self.alpha_deg:.1f}deg, beta={self.beta_deg:.1f}deg, gamma={self.gamma_deg:.1f}deg)"
        )

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
