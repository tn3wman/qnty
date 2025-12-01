"""
VectorBetween class for defining vectors between two points.

Provides a way to create a _Vector from two points, optionally with a
magnitude constraint when one or more point coordinates are unknown.
"""

from __future__ import annotations

from typing import Any

from ..core.unit import Unit
from ..utils.shared_utilities import resolve_length_unit_from_string
from .point import _Point
from .vector import _Vector


class VectorBetween:
    """
    Vector defined by two points, optionally with a magnitude constraint.

    This class creates a _Vector from the displacement between two points.
    If the points are fully known, the vector is computed immediately.
    If points have unknown coordinates, a magnitude constraint can be used
    to solve for the unknowns first.

    Examples:
        >>> from qnty.spatial import PointCartesian, VectorBetween
        >>>
        >>> # Fully known points - vector computed immediately
        >>> A = PointCartesian(x=0, y=0, z=0, unit="m")
        >>> B = PointCartesian(x=3, y=4, z=0, unit="m")
        >>> r_AB = VectorBetween(from_point=A, to_point=B)
        >>>
        >>> # Point with unknown - magnitude constraint used to solve
        >>> A = PointCartesian(x=4, y=2, z=0, unit="m")
        >>> B = PointCartesian(x=0, y=0, z=..., unit="m")  # z unknown
        >>> r_AB = VectorBetween(from_point=A, to_point=B, magnitude=8, unit="m")
    """

    __slots__ = ("_from_point", "_to_point", "_magnitude", "_unit", "_name", "_vector")

    def __init__(
        self,
        from_point: Any,
        to_point: Any,
        magnitude: float | None = None,
        unit: Unit | str | None = None,
        name: str | None = None,
    ):
        """
        Create a vector between two points.

        Args:
            from_point: Starting point (e.g., PointCartesian)
            to_point: Ending point (e.g., PointCartesian)
            magnitude: Optional magnitude constraint (required if points have unknowns)
            unit: Length unit for the magnitude/components
            name: Optional name for the vector

        Examples:
            # Vector from A to B
            r_AB = VectorBetween(from_point=A, to_point=B, unit="m")

            # With magnitude constraint for unknown coordinates
            r_AB = VectorBetween(from_point=A, to_point=B, magnitude=8, unit="m")
        """
        self._from_point = from_point
        self._to_point = to_point
        self._magnitude = magnitude
        self._name = name
        self._vector: _Vector | None = None

        # Resolve unit
        self._unit = resolve_length_unit_from_string(unit) if unit is not None else None

        # If both points are fully known, compute the vector immediately
        if not self.has_unknowns():
            self._compute_vector()

    def _compute_vector(self, from_point: _Point | None = None, to_point: _Point | None = None) -> None:
        """Compute the internal _Vector from the two points."""
        # Get points
        fp = from_point if from_point is not None else self._from_point
        tp = to_point if to_point is not None else self._to_point

        # Convert to _Point if needed
        if hasattr(fp, 'to_cartesian'):
            fp = fp.to_cartesian()
        if hasattr(tp, 'to_cartesian'):
            tp = tp.to_cartesian()

        # Compute displacement
        from_coords = fp._coords
        to_coords = tp._coords

        dx = to_coords[0] - from_coords[0]
        dy = to_coords[1] - from_coords[1]
        dz = to_coords[2] - from_coords[2]

        # Determine unit - use provided unit or get from points
        unit = self._unit
        if unit is None and fp._unit is not None:
            unit = fp._unit

        # Create _Vector (need to convert back from SI to display unit)
        if unit is not None:
            # coords are in SI, convert to display unit
            dx_disp = dx / unit.si_factor
            dy_disp = dy / unit.si_factor
            dz_disp = dz / unit.si_factor
            self._vector = _Vector(dx_disp, dy_disp, dz_disp, unit=unit)
        else:
            self._vector = _Vector(dx, dy, dz)

    def has_unknowns(self) -> bool:
        """Check if either point has unknown coordinates."""
        from_unknowns = getattr(self._from_point, 'unknowns', {}) if hasattr(self._from_point, 'unknowns') else {}
        to_unknowns = getattr(self._to_point, 'unknowns', {}) if hasattr(self._to_point, 'unknowns') else {}
        return bool(from_unknowns) or bool(to_unknowns)

    def to_cartesian(self) -> _Vector:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with u, v, w components

        Raises:
            ValueError: If vector hasn't been computed yet (unknowns not resolved)
        """
        if self._vector is None:
            raise ValueError("Vector not computed yet - unknowns must be resolved first")
        return self._vector

    @property
    def from_point(self) -> Any:
        """Starting point."""
        return self._from_point

    @property
    def to_point(self) -> Any:
        """Ending point."""
        return self._to_point

    @property
    def constraint_magnitude(self) -> float | None:
        """Magnitude constraint (if specified)."""
        return self._magnitude

    @property
    def unit(self) -> Unit | None:
        """Length unit."""
        return self._unit

    @property
    def name(self) -> str | None:
        """Vector name."""
        return self._name

    # Delegate to internal _Vector
    @property
    def u(self) -> float | None:
        """First component (available after solving)."""
        return self._vector.to_array()[0] if self._vector else None

    @property
    def v(self) -> float | None:
        """Second component (available after solving)."""
        return self._vector.to_array()[1] if self._vector else None

    @property
    def w(self) -> float | None:
        """Third component (available after solving)."""
        return self._vector.to_array()[2] if self._vector else None

    @property
    def magnitude(self):
        """Vector magnitude (computed from components if available, else constraint)."""
        if self._vector:
            return self._vector.magnitude
        return self._magnitude

    def __str__(self) -> str:
        """String representation."""
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        if self._vector:
            coords = self._vector.to_array()
            return f"VectorBetween({coords[0]:.6g}, {coords[1]:.6g}, {coords[2]:.6g}{unit_str})"
        else:
            mag_str = f"|r| = {self._magnitude}" if self._magnitude else "unsolved"
            return f"VectorBetween({mag_str}{unit_str})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
