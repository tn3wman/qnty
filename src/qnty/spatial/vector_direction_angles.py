"""
VectorDirectionAngles class for defining vectors using coordinate direction angles.

Provides a clean interface for specifying vectors by magnitude and
direction angles (alpha, beta, gamma) from the coordinate axes.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from ..utils.shared_utilities import convert_angle_to_radians_optional, resolve_length_unit_from_string
from .vector import _Vector
from .vector_helpers import compute_missing_direction_angle, validate_direction_cosines


class VectorDirectionAngles:
    """
    Vector defined by magnitude and coordinate direction angles.

    This class provides a convenient way to define 3D vectors using
    coordinate direction angles:
    - alpha: angle from +x axis
    - beta: angle from +y axis
    - gamma: angle from +z axis

    These angles must satisfy: cos²α + cos²β + cos²γ = 1

    The conversion formulas are:
    - u = magnitude * cos(alpha)
    - v = magnitude * cos(beta)
    - w = magnitude * cos(gamma)

    Examples:
        >>> from qnty.spatial import VectorDirectionAngles
        >>>
        >>> # Vector with magnitude 100N, alpha=60 deg, beta=45 deg, gamma=120 deg
        >>> v = VectorDirectionAngles(magnitude=100, alpha=60, beta=45, gamma=120, unit="N")
        >>> vec = v.to_cartesian()
    """

    __slots__ = ("_magnitude", "_alpha_rad", "_beta_rad", "_gamma_rad", "_unit", "_name", "_vector")

    def __init__(
        self,
        magnitude: float,
        alpha: float | None = None,
        beta: float | None = None,
        gamma: float | None = None,
        unit: Unit | str | None = None,
        angle_unit: str = "degree",
        name: str | None = None,
    ):
        """
        Create a vector using coordinate direction angles.

        Args:
            magnitude: Vector magnitude
            alpha: Angle from +x axis (optional if other two provided)
            beta: Angle from +y axis (optional if other two provided)
            gamma: Angle from +z axis (optional if other two provided)
            unit: Unit for magnitude
            angle_unit: Angle unit ("degree" or "radian")
            name: Optional vector name

        Note:
            At least 2 of the 3 angles must be provided. The third will be
            calculated from the constraint cos²α + cos²β + cos²γ = 1.

        Examples:
            # Vector with all angles specified
            v = VectorDirectionAngles(magnitude=100, alpha=60, beta=45, gamma=120, unit="N")

            # Vector with two angles (third calculated)
            v2 = VectorDirectionAngles(magnitude=100, alpha=60, beta=45, unit="N")
        """
        self._name = name
        self._magnitude = float(magnitude)

        # Convert angles to radians using shared utility
        alpha_rad = convert_angle_to_radians_optional(alpha, angle_unit)
        beta_rad = convert_angle_to_radians_optional(beta, angle_unit)
        gamma_rad = convert_angle_to_radians_optional(gamma, angle_unit)

        # Calculate missing angle from constraint cos²α + cos²β + cos²γ = 1
        alpha_rad, beta_rad, gamma_rad = compute_missing_direction_angle(alpha_rad, beta_rad, gamma_rad)

        # Validate the constraint
        validate_direction_cosines(alpha_rad, beta_rad, gamma_rad)

        self._alpha_rad = alpha_rad
        self._beta_rad = beta_rad
        self._gamma_rad = gamma_rad

        # Resolve unit
        self._unit = resolve_length_unit_from_string(unit)

        # Compute Cartesian components using direction cosines
        u = self._magnitude * math.cos(self._alpha_rad)
        v = self._magnitude * math.cos(self._beta_rad)
        w = self._magnitude * math.cos(self._gamma_rad)

        # Create internal _Vector
        self._vector = _Vector(u, v, w, unit=self._unit)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Examples:
            >>> v = VectorDirectionAngles(magnitude=100, alpha=60, beta=45, gamma=120, unit="N")
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
    def alpha_deg(self) -> float:
        """Alpha angle in degrees."""
        return math.degrees(self._alpha_rad)

    @property
    def alpha_rad(self) -> float:
        """Alpha angle in radians."""
        return self._alpha_rad

    @property
    def beta_deg(self) -> float:
        """Beta angle in degrees."""
        return math.degrees(self._beta_rad)

    @property
    def beta_rad(self) -> float:
        """Beta angle in radians."""
        return self._beta_rad

    @property
    def gamma_deg(self) -> float:
        """Gamma angle in degrees."""
        return math.degrees(self._gamma_rad)

    @property
    def gamma_rad(self) -> float:
        """Gamma angle in radians."""
        return self._gamma_rad

    @property
    def direction_cosines(self) -> tuple[float, float, float]:
        """Direction cosines (cos α, cos β, cos γ)."""
        return (
            math.cos(self._alpha_rad),
            math.cos(self._beta_rad),
            math.cos(self._gamma_rad),
        )

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
        return f"VectorDirectionAngles({self._magnitude}{unit_str}, α={self.alpha_deg}°, β={self.beta_deg}°, γ={self.gamma_deg}°)"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
