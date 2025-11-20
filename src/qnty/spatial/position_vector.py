"""
PositionVector class for position vectors between points in 3D space.

Position vectors are used to define the direction of forces along lines,
such as cables, rods, and other structural members.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.quantity import Quantity
from ..core.unit import Unit
from .point import _Point


class PositionVector:
    """
    Position vector representing displacement from one point to another.

    Position vectors are fundamental in statics for:
    - Defining forces along lines (cables, rods)
    - Computing unit vectors for force direction
    - Finding coordinate direction angles

    The standard pattern for a force along a line from A to B is:
        r_AB = B - A (position vector)
        u_AB = r_AB / |r_AB| (unit vector)
        F = |F| * u_AB (force vector)

    Examples:
        >>> from qnty.spatial import Point, PositionVector
        >>> from qnty.core.unit_catalog import LengthUnits
        >>>
        >>> # Create points
        >>> A = Point(0, 0, 6, unit=LengthUnits.meter)
        >>> B = Point(2, -3, 0, unit=LengthUnits.meter)
        >>>
        >>> # Create position vector from A to B
        >>> r_AB = PositionVector.from_points(A, B)
        >>> print(r_AB.magnitude)
        7.0 m
        >>>
        >>> # Get direction cosines
        >>> cos_alpha, cos_beta, cos_gamma = r_AB.direction_cosines
    """

    __slots__ = ("_coords", "_dim", "_unit", "_name")

    def __init__(
        self,
        x: float,
        y: float,
        z: float = 0.0,
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a position vector from components.

        Args:
            x: X component in specified unit
            y: Y component in specified unit
            z: Z component in specified unit (default 0.0)
            unit: Length unit for components
            name: Optional name for the position vector (e.g., "r_AB")
        """
        self._name = name or "r"

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            unit = resolved

        if unit is None:
            # Dimensionless
            self._coords = np.array([x, y, z], dtype=float)
            self._dim = None
            self._unit = None
        else:
            # Convert to SI for internal storage
            si_values = unit.si_factor * np.array([x, y, z], dtype=float)
            self._coords = si_values
            self._dim = unit.dim
            self._unit = unit

    @classmethod
    def from_points(cls, from_point: _Point, to_point: _Point, name: str | None = None) -> PositionVector:
        """
        Create position vector from point A to point B.

        This computes r_AB = B - A, the displacement from A to B.

        Args:
            from_point: Starting point A (can be _Point or any class with to_cartesian())
            to_point: Ending point B (can be _Point or any class with to_cartesian())
            name: Optional name (e.g., "r_AB")

        Returns:
            Position vector pointing from A to B

        Raises:
            ValueError: If points have different dimensions

        Examples:
            >>> A = Point(0, 0, 6, unit=LengthUnits.meter)
            >>> B = Point(2, -3, 0, unit=LengthUnits.meter)
            >>> r_AB = PositionVector.from_points(A, B, name="r_AB")
        """
        # Convert frontend classes to _Point if needed
        if hasattr(from_point, 'to_cartesian') and not isinstance(from_point, _Point):
            from_point = from_point.to_cartesian()
        if hasattr(to_point, 'to_cartesian') and not isinstance(to_point, _Point):
            to_point = to_point.to_cartesian()

        # Check dimensions match
        if from_point._dim != to_point._dim:
            raise ValueError(
                f"Points must have same dimension: {from_point._dim} vs {to_point._dim}"
            )

        # Compute displacement (to - from) using internal SI coords
        delta = to_point._coords - from_point._coords

        # Create position vector directly
        result = object.__new__(cls)
        result._coords = delta
        result._dim = from_point._dim
        result._unit = from_point._unit or to_point._unit
        result._name = name or "r"
        return result

    @property
    def name(self) -> str:
        """Position vector name."""
        return self._name

    @property
    def x(self) -> Quantity:
        """X component as Quantity."""
        return self._make_quantity(0, f"{self._name}_x")

    @property
    def y(self) -> Quantity:
        """Y component as Quantity."""
        return self._make_quantity(1, f"{self._name}_y")

    @property
    def z(self) -> Quantity:
        """Z component as Quantity."""
        return self._make_quantity(2, f"{self._name}_z")

    def _make_quantity(self, index: int, name: str) -> Quantity:
        """Create Quantity from component index."""
        if self._dim is None:
            raise ValueError("Cannot create Quantity from dimensionless position vector")

        value = self._coords[index]
        # Apply tolerance for near-zero values
        if abs(value) < 1e-10:
            value = 0.0

        q = object.__new__(Quantity)
        q.name = name
        q.dim = self._dim
        q.value = value
        q.preferred = self._unit
        q._symbol = None
        q._output_unit = None
        return q

    @property
    def magnitude(self) -> Quantity:
        """
        Magnitude (length) of position vector.

        Returns:
            |r| as Quantity with length dimension
        """
        if self._dim is None:
            raise ValueError("Cannot compute magnitude of dimensionless position vector")

        mag_si = float(np.sqrt(np.sum(self._coords**2)))

        q = object.__new__(Quantity)
        q.name = f"|{self._name}|"
        q.dim = self._dim
        q.value = mag_si
        q.preferred = self._unit
        q._symbol = None
        q._output_unit = None
        return q

    def magnitude_in(self, unit: Unit | str) -> float:
        """
        Get magnitude in specified unit.

        Args:
            unit: Target length unit

        Returns:
            Magnitude value in specified unit
        """
        if self._dim is None:
            raise ValueError("Cannot get magnitude of dimensionless position vector")

        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            unit = resolved

        return self.magnitude.magnitude(unit)

    def unit_vector(self) -> tuple[float, float, float]:
        """
        Get unit vector (direction cosines).

        Returns:
            Tuple (cos α, cos β, cos γ) where:
            - cos α = x / |r|
            - cos β = y / |r|
            - cos γ = z / |r|

        Raises:
            ValueError: If position vector is zero
        """
        mag = np.sqrt(np.sum(self._coords**2))
        if mag == 0:
            raise ValueError("Cannot compute unit vector of zero position vector")

        return (
            float(self._coords[0] / mag),
            float(self._coords[1] / mag),
            float(self._coords[2] / mag),
        )

    @property
    def direction_cosines(self) -> tuple[float, float, float]:
        """
        Direction cosines (cos α, cos β, cos γ).

        Same as unit_vector(), provided for consistency with ForceVector.

        Returns:
            Tuple (cos α, cos β, cos γ)
        """
        return self.unit_vector()

    @property
    def alpha(self) -> Quantity:
        """
        Coordinate direction angle from +x axis.

        Returns:
            α = arccos(x / |r|) in radians
        """
        cos_alpha = self.direction_cosines[0]
        alpha_rad = math.acos(max(-1.0, min(1.0, cos_alpha)))

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        return Quantity(
            name=f"{self._name}_alpha",
            dim=dim.D,
            value=alpha_rad,
            preferred=degree_unit,
        )

    @property
    def beta(self) -> Quantity:
        """
        Coordinate direction angle from +y axis.

        Returns:
            β = arccos(y / |r|) in radians
        """
        cos_beta = self.direction_cosines[1]
        beta_rad = math.acos(max(-1.0, min(1.0, cos_beta)))

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        return Quantity(
            name=f"{self._name}_beta",
            dim=dim.D,
            value=beta_rad,
            preferred=degree_unit,
        )

    @property
    def gamma(self) -> Quantity:
        """
        Coordinate direction angle from +z axis.

        Returns:
            γ = arccos(z / |r|) in radians
        """
        cos_gamma = self.direction_cosines[2]
        gamma_rad = math.acos(max(-1.0, min(1.0, cos_gamma)))

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        return Quantity(
            name=f"{self._name}_gamma",
            dim=dim.D,
            value=gamma_rad,
            preferred=degree_unit,
        )

    def to_unit(self, unit: Unit | str) -> PositionVector:
        """
        Convert to different display unit.

        Args:
            unit: Target length unit

        Returns:
            New PositionVector with updated display unit
        """
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown length unit '{unit}'")
            unit = resolved

        result = object.__new__(PositionVector)
        result._coords = self._coords.copy()
        result._dim = self._dim
        result._unit = unit
        result._name = self._name
        return result

    def to_array(self) -> np.ndarray:
        """
        Get components as numpy array in display unit.

        Returns:
            Array [x, y, z] in display units
        """
        if self._unit is None:
            return self._coords.copy()
        return self._coords / self._unit.si_factor

    def __neg__(self) -> PositionVector:
        """
        Negation (reverse direction).

        Returns:
            Position vector pointing in opposite direction
        """
        result = object.__new__(PositionVector)
        result._coords = -self._coords
        result._dim = self._dim
        result._unit = self._unit
        result._name = f"-{self._name}"
        return result

    def __mul__(self, scalar: float | int) -> PositionVector:
        """Scalar multiplication."""
        result = object.__new__(PositionVector)
        result._coords = self._coords * float(scalar)
        result._dim = self._dim
        result._unit = self._unit
        result._name = self._name
        return result

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, PositionVector):
            return NotImplemented

        if self._dim != other._dim:
            return False

        return bool(np.allclose(self._coords, other._coords, rtol=1e-10, atol=1e-10))

    def __str__(self) -> str:
        """String representation."""
        coords = self.to_array()
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        return f"{self._name} = {{{coords[0]:.4g}i + {coords[1]:.4g}j + {coords[2]:.4g}k}}{unit_str}"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
