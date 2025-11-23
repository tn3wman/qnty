"""
VectorDirectionRatios class for defining vectors using direction ratios.

Provides a clean interface for specifying vectors by magnitude and
direction ratios (a, b, c) which are proportional to the components.
"""

from __future__ import annotations

import math

from ..core.unit import Unit
from .vector import _Vector


class VectorDirectionRatios:
    """
    Vector defined by magnitude and direction ratios.

    This class provides a convenient way to define 3D vectors using
    direction ratios (a, b, c). The direction ratios define the direction
    of the vector, and are normalized to create a unit vector, then
    scaled by magnitude.

    The unit vector is: û = (a, b, c) / √(a² + b² + c²)
    The final vector is: v = magnitude * û

    This is useful when you know the vector passes through certain points
    or has a direction defined by proportional values.

    Examples:
        >>> from qnty.spatial import VectorDirectionRatios
        >>>
        >>> # Vector with magnitude 100N in direction (2, -3, 6)
        >>> v = VectorDirectionRatios(magnitude=100, a=2, b=-3, c=6, unit="N")
        >>> vec = v.to_cartesian()
        >>> # Components: (28.57, -42.86, 85.71) N
    """

    __slots__ = ("_magnitude", "_a", "_b", "_c", "_unit", "_name", "_vector")

    def __init__(
        self,
        magnitude: float,
        a: float,
        b: float,
        c: float = 0.0,
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a vector using direction ratios.

        Args:
            magnitude: Vector magnitude
            a: First direction ratio (proportional to u component)
            b: Second direction ratio (proportional to v component)
            c: Third direction ratio (proportional to w component, default 0)
            unit: Unit for magnitude
            name: Optional vector name

        Raises:
            ValueError: If all direction ratios are zero

        Examples:
            # Vector with magnitude 100N in direction (2, -3, 6)
            v = VectorDirectionRatios(magnitude=100, a=2, b=-3, c=6, unit="N")

            # 2D vector in direction (3, 4)
            v2 = VectorDirectionRatios(magnitude=50, a=3, b=4, unit="m")
        """
        self._name = name
        self._magnitude = float(magnitude)
        self._a = float(a)
        self._b = float(b)
        self._c = float(c)

        # Calculate magnitude of direction vector
        dir_magnitude = math.sqrt(a**2 + b**2 + c**2)
        if dir_magnitude == 0:
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

        # Compute Cartesian components
        # v = magnitude * (a, b, c) / ||(a, b, c)||
        scale = self._magnitude / dir_magnitude
        u = self._a * scale
        v = self._b * scale
        w = self._c * scale

        # Create internal _Vector
        self._vector = _Vector(u, v, w, unit=self._unit)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Examples:
            >>> v = VectorDirectionRatios(magnitude=100, a=2, b=-3, c=6, unit="N")
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
    def direction_ratios(self) -> tuple[float, float, float]:
        """Direction ratios (a, b, c)."""
        return (self._a, self._b, self._c)

    @property
    def direction_cosines(self) -> tuple[float, float, float]:
        """Direction cosines (cos α, cos β, cos γ)."""
        dir_magnitude = math.sqrt(self._a**2 + self._b**2 + self._c**2)
        return (
            self._a / dir_magnitude,
            self._b / dir_magnitude,
            self._c / dir_magnitude,
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
        return f"VectorDirectionRatios({self._magnitude}{unit_str}, [{self._a}, {self._b}, {self._c}])"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
