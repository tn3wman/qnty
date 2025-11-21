"""
VectorCartesian class for defining vectors using Cartesian components.

Provides a clean interface for specifying vectors with explicit u, v, w
components with default values of zero for unspecified components.
"""

from __future__ import annotations

from ..core.unit import Unit
from .vector import _Vector


class VectorCartesian:
    """
    Vector defined by u, v, w Cartesian components.

    This class provides a convenient way to define vectors with explicit
    components, where unspecified components default to zero.

    Examples:
        >>> from qnty.spatial import VectorCartesian
        >>>
        >>> # Vector with all components
        >>> v = VectorCartesian(u=3, v=4, w=0, unit="m")
        >>>
        >>> # Vector with default w=0
        >>> v2 = VectorCartesian(u=5, v=10, unit="ft")
        >>>
        >>> # Vector along w-axis
        >>> v3 = VectorCartesian(w=300, unit="mm")
    """

    __slots__ = ("_vector", "_name")

    def __init__(
        self,
        u: float = 0.0,
        v: float = 0.0,
        w: float = 0.0,
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a vector using Cartesian components.

        Args:
            u: First component (default 0.0)
            v: Second component (default 0.0)
            w: Third component (default 0.0)
            unit: Unit for components
            name: Optional vector name

        Examples:
            # Full 3D vector
            v = VectorCartesian(u=3, v=4, w=0, unit="m")

            # 2D vector (w=0)
            v2 = VectorCartesian(u=5, v=10, unit="ft")

            # Vector along axis
            v3 = VectorCartesian(w=300, unit="mm")
        """
        self._name = name

        # Resolve unit
        if isinstance(unit, str):
            from ..core.unit import ureg

            resolved = ureg.resolve(unit)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # Create internal _Vector
        self._vector = _Vector(float(u), float(v), float(w), unit=unit)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Examples:
            >>> v = VectorCartesian(u=3, v=4, w=0, unit="m")
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
    def unit(self) -> Unit | None:
        """Unit."""
        return self._vector._unit

    @property
    def name(self) -> str | None:
        """Vector name."""
        return self._name

    @property
    def magnitude(self):
        """Vector magnitude."""
        return self._vector.magnitude

    @property
    def alpha(self):
        """Coordinate direction angle from +x axis (degrees)."""
        result = self._vector.alpha
        if result is None:
            raise ValueError("Cannot compute alpha for zero-magnitude vector")
        return result

    @property
    def beta(self):
        """Coordinate direction angle from +y axis (degrees)."""
        result = self._vector.beta
        if result is None:
            raise ValueError("Cannot compute beta for zero-magnitude vector")
        return result

    @property
    def gamma(self):
        """Coordinate direction angle from +z axis (degrees)."""
        result = self._vector.gamma
        if result is None:
            raise ValueError("Cannot compute gamma for zero-magnitude vector")
        return result

    def to_unit(self, unit: Unit | str) -> VectorCartesian:
        """
        Convert to different display unit.

        Args:
            unit: Target unit for display (e.g., "ft", "in", "mm")

        Returns:
            New VectorCartesian with components in target unit

        Examples:
            >>> v = VectorCartesian(u=1, v=2, w=3, unit="m")
            >>> v_ft = v.to_unit("ft")
            >>> print(v_ft)
            VectorCartesian(3.28084, 6.56168, 9.84252 ft)
        """
        # Convert internal _Vector to new unit
        converted_vector = self._vector.to_unit(unit)

        # Get components in new unit
        coords = converted_vector.to_array()

        # Create new VectorCartesian with converted values
        result = VectorCartesian(
            u=coords[0],
            v=coords[1],
            w=coords[2],
            unit=converted_vector._unit,
            name=self._name
        )
        return result

    def __str__(self) -> str:
        """String representation."""
        coords = self._vector.to_array()
        unit_str = f" {self._vector._unit.symbol}" if self._vector._unit else ""
        return f"VectorCartesian({coords[0]:.6g}, {coords[1]:.6g}, {coords[2]:.6g}){unit_str}"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
