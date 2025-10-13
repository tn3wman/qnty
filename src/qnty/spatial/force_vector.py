"""
ForceVector class for 2D/3D force vectors in statics problems.

Provides multiple construction methods:
- From magnitude and angle (polar)
- From x/y components (cartesian)
- From coordinates and points

Integrates with qnty's unit system and Vector class.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np

from ..core.dimension import Dimension
from ..core.quantity import Quantity
from ..core.unit import Unit
from .vector import Vector

if TYPE_CHECKING:
    from ..core.unit_catalog import ForceUnits, AnglePlaneUnits


class ForceVector:
    """
    2D/3D force vector for statics problems.

    Supports multiple construction patterns:
    - Magnitude + angle: ForceVector(magnitude=500, angle=60, unit="N", angle_unit="degree")
    - Components: ForceVector(x=300, y=400, unit="N")
    - From Vector: ForceVector(vector=my_vector)

    Examples:
        >>> # Polar form (magnitude + angle)
        >>> F1 = ForceVector(magnitude=700, angle=60, unit="N", name="Cable Force")
        >>> print(F1.magnitude)
        700 N

        >>> # Component form
        >>> F2 = ForceVector(x=300, y=400, unit="N", name="Applied Force")
        >>> print(F2.magnitude)
        500 N

        >>> # Unknown force (to be solved)
        >>> FR = ForceVector(magnitude=None, angle=None, name="Resultant", is_known=False)
    """

    __slots__ = ("_vector", "_magnitude", "_angle", "name", "is_known", "is_resultant", "_description")

    def __init__(
        self,
        magnitude: float | Quantity | None = None,
        angle: float | Quantity | None = None,
        x: float | Quantity | None = None,
        y: float | Quantity | None = None,
        z: float | Quantity | None = None,
        unit: Unit | str | None = None,
        angle_unit: Unit | str = "degree",
        vector: Vector | None = None,
        name: str | None = None,
        description: str = "",
        is_known: bool = True,
        is_resultant: bool = False,
    ):
        """
        Create a ForceVector.

        Args:
            magnitude: Force magnitude (if None, will be calculated from components or marked unknown)
            angle: Angle from positive x-axis (counterclockwise)
            x: X-component of force
            y: Y-component of force
            z: Z-component of force (default 0 for 2D problems)
            unit: Force unit (e.g., "N", "lb", "kN")
            angle_unit: Angle unit (default "degree", can be "radian")
            vector: Pre-constructed Vector object
            name: Descriptive name for the force
            description: Longer description
            is_known: Whether this force is known (False for unknowns to solve for)
            is_resultant: Whether this is a resultant force (for equilibrium problems)
        """
        self.name = name or "Force"
        self.is_known = is_known
        self.is_resultant = is_resultant
        self._description = description
        self._magnitude: Quantity | None = None
        self._angle: Quantity | None = None

        # Resolve unit
        if isinstance(unit, str):
            from ..core.unit import ureg
            from ..core.dimension_catalog import dim
            resolved = ureg.resolve(unit, dim=dim.force)
            if resolved is None:
                raise ValueError(f"Unknown force unit '{unit}'")
            unit = resolved

        # Resolve angle unit
        if isinstance(angle_unit, str):
            from ..core.unit import ureg
            from ..core.dimension_catalog import dim
            resolved = ureg.resolve(angle_unit, dim=dim.D)
            if resolved is None:
                raise ValueError(f"Unknown angle unit '{angle_unit}'")
            angle_unit = resolved

        # Case 1: Construct from existing Vector
        if vector is not None:
            self._vector = vector
            self._compute_magnitude_and_angle()
            return

        # Case 2: Construct from magnitude and angle (polar)
        if magnitude is not None and angle is not None:
            # Convert magnitude to Quantity if needed
            if isinstance(magnitude, (int, float)):
                if unit is None:
                    raise ValueError("unit must be specified when magnitude is a scalar")
                mag_qty = Quantity(name=f"{self.name}_magnitude", dim=unit.dim, value=float(magnitude), preferred=unit)
            else:
                mag_qty = magnitude

            # Convert angle to Quantity if needed
            if isinstance(angle, (int, float)):
                from ..core.dimension_catalog import dim
                angle_qty = Quantity(name=f"{self.name}_angle", dim=dim.D, value=float(angle) * angle_unit.si_factor, preferred=angle_unit)
            else:
                angle_qty = angle

            # Store magnitude and angle
            self._magnitude = mag_qty
            self._angle = angle_qty

            # Convert to vector components
            if mag_qty.value is not None and angle_qty.value is not None:
                angle_rad = angle_qty.value  # Already in SI (radians)
                x_val = mag_qty.value * math.cos(angle_rad)
                y_val = mag_qty.value * math.sin(angle_rad)
                z_val = 0.0

                self._vector = Vector(x_val, y_val, z_val, unit=mag_qty.preferred)
            else:
                # Unknown force
                self._vector = None
            return

        # Case 3: Construct from components (cartesian)
        if x is not None or y is not None:
            if unit is None:
                raise ValueError("unit must be specified for component construction")

            # Convert to Quantity objects
            x_qty = self._to_quantity(x, unit, "x") if x is not None else Quantity(name="x", dim=unit.dim, value=0.0, preferred=unit)
            y_qty = self._to_quantity(y, unit, "y") if y is not None else Quantity(name="y", dim=unit.dim, value=0.0, preferred=unit)
            z_qty = self._to_quantity(z, unit, "z") if z is not None else Quantity(name="z", dim=unit.dim, value=0.0, preferred=unit)

            # Create vector from quantities
            if x_qty.value is not None and y_qty.value is not None and z_qty.value is not None:
                self._vector = Vector.from_quantities(x_qty, y_qty, z_qty)
                self._compute_magnitude_and_angle()
            else:
                self._vector = None
            return

        # Case 4: Unknown force (no data provided)
        if not is_known:
            self._vector = None
            self._magnitude = None
            self._angle = None
            return

        raise ValueError("Must provide either (magnitude, angle), (x, y, z components), or vector")

    def _to_quantity(self, value: float | Quantity | None, unit: Unit, component_name: str) -> Quantity:
        """Convert value to Quantity."""
        if isinstance(value, Quantity):
            return value
        elif isinstance(value, (int, float)):
            return Quantity(name=component_name, dim=unit.dim, value=float(value), preferred=unit)
        else:
            return Quantity(name=component_name, dim=unit.dim, value=None, preferred=unit)

    def _compute_magnitude_and_angle(self) -> None:
        """Compute magnitude and angle from vector components."""
        if self._vector is None:
            return

        self._magnitude = self._vector.magnitude

        # Compute angle
        coords = self._vector.to_array()
        angle_rad = math.atan2(coords[1], coords[0])

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg
        degree_unit = ureg.resolve("degree", dim=dim.D)

        self._angle = Quantity(
            name=f"{self.name}_angle",
            dim=dim.D,
            value=angle_rad,
            preferred=degree_unit
        )

    @classmethod
    def from_magnitude_angle(
        cls,
        magnitude: float | Quantity,
        angle: float | Quantity,
        unit: Unit | str | None = None,
        angle_unit: Unit | str = "degree",
        name: str | None = None,
        **kwargs
    ) -> ForceVector:
        """
        Create ForceVector from magnitude and angle (polar form).

        Args:
            magnitude: Force magnitude
            angle: Angle from positive x-axis (counterclockwise)
            unit: Force unit
            angle_unit: Angle unit (default "degree")
            name: Force name
            **kwargs: Additional arguments

        Returns:
            ForceVector instance
        """
        return cls(magnitude=magnitude, angle=angle, unit=unit, angle_unit=angle_unit, name=name, **kwargs)

    @classmethod
    def from_components(
        cls,
        x: float | Quantity,
        y: float | Quantity,
        z: float | Quantity | None = None,
        unit: Unit | str | None = None,
        name: str | None = None,
        **kwargs
    ) -> ForceVector:
        """
        Create ForceVector from x, y, z components (cartesian form).

        Args:
            x: X-component
            y: Y-component
            z: Z-component (default 0)
            unit: Force unit
            name: Force name
            **kwargs: Additional arguments

        Returns:
            ForceVector instance
        """
        return cls(x=x, y=y, z=z, unit=unit, name=name, **kwargs)

    @classmethod
    def unknown(cls, name: str, is_resultant: bool = False, **kwargs) -> ForceVector:
        """
        Create an unknown ForceVector to be solved for.

        Args:
            name: Force name
            is_resultant: Whether this is a resultant force
            **kwargs: Additional arguments

        Returns:
            ForceVector instance marked as unknown
        """
        return cls(magnitude=None, angle=None, name=name, is_known=False, is_resultant=is_resultant, **kwargs)

    # Properties
    @property
    def magnitude(self) -> Quantity | None:
        """Force magnitude."""
        return self._magnitude

    @property
    def angle(self) -> Quantity | None:
        """Angle from positive x-axis (counterclockwise)."""
        return self._angle

    @property
    def vector(self) -> Vector | None:
        """Underlying Vector object."""
        return self._vector

    @property
    def x(self) -> Quantity | None:
        """X-component."""
        return self._vector.u if self._vector else None

    @property
    def y(self) -> Quantity | None:
        """Y-component."""
        return self._vector.v if self._vector else None

    @property
    def z(self) -> Quantity | None:
        """Z-component."""
        return self._vector.w if self._vector else None

    @property
    def description(self) -> str:
        """Force description."""
        return self._description

    def __str__(self) -> str:
        """String representation."""
        if not self.is_known:
            return f"ForceVector({self.name}, unknown)"

        if self._magnitude and self._angle:
            mag_val = self._magnitude.value / self._magnitude.preferred.si_factor if self._magnitude.preferred else self._magnitude.value
            ang_val = self._angle.value / self._angle.preferred.si_factor if self._angle.preferred else self._angle.value
            mag_unit = self._magnitude.preferred.symbol if self._magnitude.preferred else ""
            ang_unit = self._angle.preferred.symbol if self._angle.preferred else ""
            return f"ForceVector({self.name}, {mag_val:.3f} {mag_unit} at {ang_val:.1f}{ang_unit})"

        return f"ForceVector({self.name})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """
        Compare two ForceVectors for equality.

        Two ForceVectors are considered equal if they have the same:
        - Magnitude (within tolerance)
        - Angle (within tolerance)
        - Units

        Note: Name and description are not compared.
        """
        if not isinstance(other, ForceVector):
            return NotImplemented

        # Both unknown
        if not self.is_known and not other.is_known:
            return True

        # One known, one unknown
        if self.is_known != other.is_known:
            return False

        # Both known - compare values
        if self._magnitude is None or other._magnitude is None:
            return False
        if self._angle is None or other._angle is None:
            return False

        # Compare magnitudes (in SI units to handle different preferred units)
        if self._magnitude.value is None or other._magnitude.value is None:
            return False
        mag_diff = abs(self._magnitude.value - other._magnitude.value)
        mag_tolerance = max(abs(self._magnitude.value), abs(other._magnitude.value)) * 1e-6

        # Compare angles (in radians - SI units)
        if self._angle.value is None or other._angle.value is None:
            return False
        # Normalize angles to [0, 2π]
        import math
        angle1 = self._angle.value % (2 * math.pi)
        angle2 = other._angle.value % (2 * math.pi)
        angle_diff = abs(angle1 - angle2)
        # Handle wrap-around (e.g., 359° vs 1°)
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        angle_tolerance = 3e-4  # ~0.017 degrees, accounts for rounding in degree specifications

        return mag_diff <= mag_tolerance and angle_diff <= angle_tolerance
