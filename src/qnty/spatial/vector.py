"""
Vector class for 3D directions/displacements with units.

Represents a direction or displacement in 3D space where all components
share the same unit. Supports standard vector operations like addition,
scaling, dot product, cross product, and normalization.

Also serves as the unified class for ForceVector and PositionVector functionality.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, runtime_checkable

import numpy as np
from numpy.typing import NDArray

from ..core.quantity import Quantity
from ..core.unit import Unit
from ..utils.shared_utilities import create_magnitude_quantity, resolve_angle_unit_from_string, resolve_unit_from_string

if TYPE_CHECKING:
    from .angle_reference import AngleReference
    from .coordinate_system import CoordinateSystem
    from .point import _Point

D = TypeVar("D")


@runtime_checkable
class PointLike(Protocol):
    """Protocol for any point-like object that can be converted to Cartesian coordinates."""

    def to_cartesian(self) -> "_Point": ...


class _Vector(Generic[D]):
    """
    Backend 3D vector with uniform units across all components.

    This is the internal representation used by all frontend Vector classes.
    All components (u, v, w) share the same unit for consistency
    and performance. Internally stores values in SI units.

    Users should use the frontend classes instead:
    - VectorCartesian: Define by u, v, w components
    - VectorPolar: Define by magnitude and angle in a plane
    - VectorSpherical: Define by magnitude, theta, phi angles
    - VectorDirectionAngles: Define by magnitude and direction angles
    - VectorDirectionRatios: Define by magnitude and direction ratios

    Examples:
        >>> from qnty.core.unit_catalog import LengthUnits
        >>> v1 = _Vector(3.0, 4.0, 0.0, unit=LengthUnits.meter)
        >>> magnitude = v1.magnitude
        >>> print(magnitude)
        5 m
        >>> v2 = v1.normalized()
        >>> print(v2.magnitude)
        1 m
    """

    __slots__ = (
        "_coords", "_dim", "_unit",
        # ForceVector attributes
        "_magnitude", "_angle", "name", "is_known", "is_resultant", "_description",
        "coordinate_system", "angle_reference", "_relative_to_force", "_relative_angle",
        # PositionVector attributes
        "_from_point", "_to_point", "_constraint_magnitude",
        # Original polar coordinates for reporting
        "_original_angle", "_original_wrt",
        # Deferred coordinate system attributes (for custom axes like +u, +v)
        "_deferred_magnitude", "_deferred_angle_rad", "_needs_coordinate_system"
    )

    def __init__(
        self,
        u: float | None = None,
        v: float | None = None,
        w: float = 0.0,
        unit: Unit[D] | str | None = None,
        # ForceVector parameters
        magnitude: float | Quantity | None = None,
        angle: float | Quantity | None = None,
        x: float | Quantity | None = None,
        y: float | Quantity | None = None,
        z: float | Quantity | None = None,
        angle_unit: Unit | str = "degree",
        vector: "_Vector | None" = None,
        name: str | None = None,
        description: str = "",
        is_known: bool = True,
        is_resultant: bool = False,
        coordinate_system: "CoordinateSystem | None" = None,
        angle_reference: "AngleReference | None" = None,
        wrt: str | None = None,
        # 3D angle specifications
        alpha: float | Quantity | None = None,
        beta: float | Quantity | None = None,
        gamma: float | Quantity | None = None,
        phi: float | Quantity | None = None,
        theta: float | Quantity | None = None,
    ):
        """
        Create a 3D vector with units.

        Supports multiple construction patterns:
        - Basic: _Vector(u, v, w, unit) - component form
        - Polar: _Vector(magnitude=500, angle=60, unit="N") - for force vectors
        - Cartesian: _Vector(x=300, y=400, unit="N") - cartesian components
        - Direction angles: _Vector(magnitude=100, alpha=60, beta=45, gamma=60, unit="N")

        Args:
            u: First component value in the specified unit
            v: Second component value in the specified unit
            w: Third component value in the specified unit (default: 0.0)
            unit: Unit for all components
            magnitude: Force magnitude (polar form)
            angle: Angle value (polar form, 2D)
            x: X-component (cartesian form)
            y: Y-component (cartesian form)
            z: Z-component (cartesian form)
            angle_unit: Angle unit (default "degree")
            name: Descriptive name for the vector
            description: Longer description
            is_known: Whether this vector is known (False for unknowns to solve)
            is_resultant: Whether this is a resultant (for equilibrium problems)
            coordinate_system: CoordinateSystem for non-standard axes
            angle_reference: AngleReference specifying how angle is measured
            wrt: Shorthand for angle reference (e.g., "+x", "cw:+y")
            alpha: Coordinate direction angle from +x axis (3D)
            beta: Coordinate direction angle from +y axis (3D)
            gamma: Coordinate direction angle from +z axis (3D)
            phi: Transverse angle (3D)
            theta: Azimuth angle (3D)
        """
        # Initialize ForceVector/PositionVector attributes
        self.name = name or "Vector"
        self.is_known = is_known
        self.is_resultant = is_resultant
        self._description = description
        self._magnitude: Quantity | None = None
        self._angle: Quantity | None = None
        self._relative_to_force: str | None = None
        self._relative_angle: float | None = None
        self._from_point = None
        self._to_point = None
        self._constraint_magnitude = None

        # Import coordinate system lazily
        if coordinate_system is None:
            from .coordinate_system import CoordinateSystem
            self.coordinate_system = CoordinateSystem.standard()
        else:
            self.coordinate_system = coordinate_system

        # Handle wrt parameter
        if wrt is not None and angle_reference is not None:
            raise ValueError("Cannot specify both 'wrt' and 'angle_reference'")

        if wrt is not None:
            self.angle_reference = self._parse_wrt(wrt)
            # If wrt refers to a force and angle was provided, use it as relative offset
            if self._relative_to_force is not None and angle is not None:
                # Convert angle to radians and store as relative angle
                if isinstance(angle, int | float):
                    # Resolve angle unit for conversion
                    angle_unit = resolve_angle_unit_from_string(angle_unit)
                    self._relative_angle = float(angle) * angle_unit.si_factor
                else:
                    # Angle is a Quantity
                    self._relative_angle = angle.value if angle.value is not None else 0.0
                # Clear angle so it doesn't go through Mode 4
                angle = None
        elif angle_reference is not None:
            self.angle_reference = angle_reference
        else:
            from .angle_reference import AngleReference
            self.angle_reference = AngleReference.standard()

        # Resolve unit if string
        unit = resolve_unit_from_string(unit) if unit is not None else None

        # Resolve angle unit
        angle_unit = resolve_angle_unit_from_string(angle_unit)

        # Determine construction mode
        # Mode 0: From existing vector
        if vector is not None:
            self._coords = vector._coords.copy()
            self._dim = vector._dim
            self._unit = vector._unit
            self._compute_magnitude_and_angle()
            return

        # Mode 1: Basic u, v, w construction
        if u is not None and v is not None:
            from .vector_helpers import init_coords_from_unit
            self._coords, self._dim, self._unit = init_coords_from_unit(u, v, w, unit)
            return

        # Mode 2: Coordinate direction angles (3D)
        if alpha is not None or beta is not None or gamma is not None:
            self._init_from_direction_angles(magnitude, alpha, beta, gamma, unit, angle_unit)
            return

        # Mode 3: Transverse/azimuth angles (3D)
        if phi is not None and theta is not None:
            self._init_from_transverse_azimuth(magnitude, phi, theta, unit, angle_unit)
            return

        # Mode 4: Magnitude and angle (polar, 2D)
        if magnitude is not None and angle is not None:
            self._init_from_polar(magnitude, angle, unit, angle_unit)
            return

        # Mode 4b: Angle known but magnitude unknown
        if magnitude is None and angle is not None:
            self._init_angle_only(angle, unit, angle_unit)
            return

        # Mode 4c: Magnitude known but angle unknown
        if magnitude is not None and angle is None:
            self._init_magnitude_only(magnitude, unit)
            return

        # Mode 5: Cartesian components (x, y, z)
        if x is not None or y is not None:
            self._init_from_cartesian(x, y, z, unit)
            return

        # Mode 6: Unknown vector
        if not is_known:
            self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
            self._dim = unit.dim if unit else None
            self._unit = unit
            self._magnitude = None
            self._angle = None
            return

        # Default: zero vector
        self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
        self._dim = unit.dim if unit else None
        self._unit = unit

    @classmethod
    def from_quantities(cls, u: Quantity[D], v: Quantity[D], w: Quantity[D] | None = None) -> _Vector[D]:
        """
        Create vector from Quantity objects (must have same dimension).

        Args:
            u: First component as Quantity
            v: Second component as Quantity
            w: Third component as Quantity (default: 0 in same unit as u)

        Returns:
            _Vector with components from the quantities

        Raises:
            ValueError: If quantities have different dimensions
        """
        if w is None:
            # Create zero w-component with same unit as u
            if u.preferred is None:
                raise ValueError("Cannot create vector from quantity without preferred unit")
            w = Quantity(name="w", dim=u.dim, value=0.0, preferred=u.preferred)

        # Validate dimensions match
        if not (u.dim == v.dim == w.dim):
            raise ValueError(f"All components must have the same dimension: u={u.dim}, v={v.dim}, w={w.dim}")

        # Validate all have values
        if u.value is None or v.value is None or w.value is None:
            raise ValueError("Cannot create vector from unknown quantities")

        # Create vector directly from SI values
        result = object.__new__(cls)
        result._coords = np.array([u.value, v.value, w.value], dtype=float)
        result._dim = u.dim
        result._unit = u.preferred or v.preferred or w.preferred
        cls._init_result_slots(result)
        return result

    # Helper methods for different construction modes
    def _parse_wrt(self, wrt: str) -> "AngleReference":
        """Parse wrt parameter into AngleReference."""
        from .angle_reference import AngleReference

        # Check for force reference (contains uppercase or underscore)
        angle_offset = 0.0
        ref_part = wrt

        if ":" in wrt:
            parts = wrt.split(":", 1)
            try:
                angle_offset = float(parts[0])
                ref_part = parts[1].strip()
            except ValueError:
                pass

        ref_without_sign = ref_part.lstrip("+-")
        is_negative_ref = ref_part.startswith("-")

        if any(c.isupper() or c == "_" for c in ref_without_sign):
            self._relative_to_force = ref_without_sign
            if is_negative_ref:
                angle_offset += 180.0
            self._relative_angle = math.radians(angle_offset)
            return AngleReference.standard()

        return _Vector.parse_wrt_static(wrt, self.coordinate_system)

    def _compute_standard_angle_or_relative(self, angle_in_ref: float) -> float | None:
        """
        Compute the standard angle, or update relative angle if this is a relative force.

        Args:
            angle_in_ref: The angle in the reference frame (radians)

        Returns:
            The standard angle (radians) if not relative, None if relative
        """
        if self._relative_to_force is None:
            return self.angle_reference.to_standard(angle_in_ref, angle_unit="radian")
        else:
            base_offset = self._relative_angle if self._relative_angle else 0.0
            self._relative_angle = base_offset + angle_in_ref
            return None

    @staticmethod
    def parse_wrt(wrt: str, coordinate_system: "CoordinateSystem | None" = None) -> "AngleReference":
        """Parse wrt string into AngleReference."""
        return _Vector.parse_wrt_static(wrt, coordinate_system)

    @staticmethod
    def parse_wrt_static(wrt: str, coordinate_system: "CoordinateSystem | None" = None) -> "AngleReference":
        """Parse wrt string into AngleReference."""
        from .angle_reference import AngleReference
        from .coordinate_system import CoordinateSystem

        coord_sys = coordinate_system or CoordinateSystem.standard()

        if ":" in wrt:
            direction_str, axis = wrt.split(":", 1)
            direction_str = direction_str.lower().strip()
            axis = axis.strip()
        else:
            direction_str = "ccw"
            axis = wrt.strip()

        if direction_str in ("ccw", "counterclockwise"):
            direction = "counterclockwise"
        elif direction_str in ("cw", "clockwise"):
            direction = "clockwise"
        else:
            raise ValueError(f"Invalid direction '{direction_str}'")

        axis_without_sign = axis.lstrip("+-")
        is_negative = axis.startswith("-")

        if axis == coord_sys.axis1_label or axis_without_sign == coord_sys.axis1_label:
            if is_negative:
                axis_angle_deg = math.degrees(coord_sys.axis1_angle) + 180.0
                return AngleReference(axis_angle=axis_angle_deg, direction=direction, axis_label=axis, angle_unit="degree")
            else:
                return AngleReference.from_coordinate_system(coord_sys, axis_index=0, direction=direction)
        elif axis == coord_sys.axis2_label or axis_without_sign == coord_sys.axis2_label:
            if is_negative:
                axis_angle_deg = math.degrees(coord_sys.axis2_angle) + 180.0
                return AngleReference(axis_angle=axis_angle_deg, direction=direction, axis_label=axis, angle_unit="degree")
            else:
                return AngleReference.from_coordinate_system(coord_sys, axis_index=1, direction=direction)
        else:
            standard_axes = {"+x", "x", "+y", "y", "-x", "-y"}
            if axis in standard_axes:
                return AngleReference.from_axis(axis, direction=direction)
            raise ValueError(f"Invalid wrt axis '{axis}'")

    def _init_from_direction_angles(self, magnitude, alpha, beta, gamma, unit, angle_unit):
        """Initialize from coordinate direction angles."""
        if magnitude is None:
            raise ValueError("magnitude must be specified with direction angles")

        if isinstance(magnitude, int | float):
            if unit is None:
                raise ValueError("unit must be specified when magnitude is a scalar")
            mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
            mag_qty.preferred = unit
        else:
            mag_qty = magnitude

        def to_radians(angle_val):
            if angle_val is None:
                return None
            if isinstance(angle_val, int | float):
                return float(angle_val) * angle_unit.si_factor
            return angle_val.value

        alpha_rad = to_radians(alpha)
        beta_rad = to_radians(beta)
        gamma_rad = to_radians(gamma)

        # Calculate missing angle
        if alpha_rad is None and beta_rad is not None and gamma_rad is not None:
            cos_alpha_sq = 1 - math.cos(beta_rad)**2 - math.cos(gamma_rad)**2
            if cos_alpha_sq < 0:
                raise ValueError("Invalid angle combination")
            alpha_rad = math.acos(math.sqrt(cos_alpha_sq))
        elif beta_rad is None and alpha_rad is not None and gamma_rad is not None:
            cos_beta_sq = 1 - math.cos(alpha_rad)**2 - math.cos(gamma_rad)**2
            if cos_beta_sq < 0:
                raise ValueError("Invalid angle combination")
            cos_beta = math.sqrt(cos_beta_sq)
            if alpha_rad < math.pi/2 and gamma_rad < math.pi/2 and cos_beta_sq < 0.9:
                cos_beta = -cos_beta
            beta_rad = math.acos(cos_beta)
        elif gamma_rad is None and alpha_rad is not None and beta_rad is not None:
            cos_gamma_sq = 1 - math.cos(alpha_rad)**2 - math.cos(beta_rad)**2
            if cos_gamma_sq < 0:
                raise ValueError("Invalid angle combination")
            gamma_rad = math.acos(math.sqrt(cos_gamma_sq))
        elif alpha_rad is None or beta_rad is None or gamma_rad is None:
            raise ValueError("Must provide at least 2 of 3 direction angles")

        if mag_qty.value is None:
            raise ValueError("Magnitude must be known")

        mag_val = mag_qty.value
        x_val = mag_val * math.cos(alpha_rad)
        y_val = mag_val * math.cos(beta_rad)
        z_val = mag_val * math.cos(gamma_rad)

        self._coords = np.array([x_val, y_val, z_val], dtype=float)
        self._dim = unit.dim if unit else None
        self._unit = unit
        self._magnitude = mag_qty

    def _init_from_transverse_azimuth(self, magnitude, phi, theta, unit, angle_unit):
        """Initialize from transverse/azimuth angles."""
        if magnitude is None:
            raise ValueError("magnitude must be specified")

        mag_qty = create_magnitude_quantity(magnitude, unit, self.name)

        def to_radians(angle_val):
            if isinstance(angle_val, int | float):
                return float(angle_val) * angle_unit.si_factor
            return angle_val.value

        phi_rad = to_radians(phi)
        theta_rad = to_radians(theta)

        if mag_qty.value is None:
            raise ValueError("Magnitude must be known")

        mag_val = mag_qty.value
        x_val = mag_val * math.sin(phi_rad) * math.cos(theta_rad)
        y_val = mag_val * math.sin(phi_rad) * math.sin(theta_rad)
        z_val = mag_val * math.cos(phi_rad)

        self._coords = np.array([x_val, y_val, z_val], dtype=float)
        self._dim = unit.dim if unit else None
        self._unit = unit
        self._magnitude = mag_qty

    def _init_from_polar(self, magnitude, angle, unit, angle_unit):
        """Initialize from magnitude and angle (2D polar)."""
        mag_qty = create_magnitude_quantity(magnitude, unit, self.name)

        if isinstance(angle, int | float):
            from ..core.dimension_catalog import dim

            angle_in_ref = float(angle) * angle_unit.si_factor
            angle_standard = self._compute_standard_angle_or_relative(angle_in_ref)
            angle_qty = Quantity(name=f"{self.name}_angle", dim=dim.D, value=angle_standard, preferred=angle_unit)
        else:
            angle_in_ref = angle.value
            if angle_in_ref is not None:
                angle_standard = self.angle_reference.to_standard(angle_in_ref, angle_unit="radian")
            else:
                angle_standard = None
            angle_qty = Quantity(name=f"{self.name}_angle", dim=angle.dim, value=angle_standard, preferred=angle.preferred)

        self._magnitude = mag_qty
        self._angle = angle_qty

        if mag_qty.value is not None and angle_qty.value is not None and self._relative_to_force is None:
            angle_rad = angle_qty.value
            x_val = mag_qty.value * math.cos(angle_rad)
            y_val = mag_qty.value * math.sin(angle_rad)
            self._coords = np.array([x_val, y_val, 0.0], dtype=float)
            self._dim = unit.dim if unit else None
            self._unit = unit
        else:
            self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
            self._dim = unit.dim if unit else None
            self._unit = unit

    def _init_angle_only(self, angle, unit, angle_unit):
        """Initialize with known angle but unknown magnitude."""
        from ..core.dimension_catalog import dim

        if isinstance(angle, int | float):
            angle_in_ref = float(angle) * angle_unit.si_factor
            angle_standard = self._compute_standard_angle_or_relative(angle_in_ref)
            angle_qty = Quantity(name=f"{self.name}_angle", dim=dim.D, value=angle_standard, preferred=angle_unit)
        else:
            angle_in_ref = angle.value
            if angle_in_ref is not None:
                angle_standard = self.angle_reference.to_standard(angle_in_ref, angle_unit="radian")
            else:
                angle_standard = None
            angle_qty = Quantity(name=f"{self.name}_angle", dim=angle.dim, value=angle_standard, preferred=angle.preferred)

        self._angle = angle_qty
        self._magnitude = None
        self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
        self._dim = unit.dim if unit else None
        self._unit = unit

    def _init_magnitude_only(self, magnitude, unit):
        """Initialize with known magnitude but unknown angle."""
        mag_qty = create_magnitude_quantity(magnitude, unit, self.name)

        self._magnitude = mag_qty
        self._angle = None
        self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
        self._dim = unit.dim if unit else None
        self._unit = unit

    def _init_from_cartesian(self, x, y, z, unit):
        """Initialize from cartesian components."""
        if unit is None:
            raise ValueError("unit must be specified")

        def to_qty(val, name):
            if val is None:
                return Quantity(name=name, dim=unit.dim, value=0.0, preferred=unit)
            if isinstance(val, Quantity):
                return val
            qty = Quantity.from_value(float(val), unit, name=name)
            qty.preferred = unit
            return qty

        x_qty = to_qty(x, "x")
        y_qty = to_qty(y, "y")
        z_qty = to_qty(z, "z")

        if x_qty.value is not None and y_qty.value is not None and z_qty.value is not None:
            self._coords = np.array([x_qty.value, y_qty.value, z_qty.value], dtype=float)
            self._dim = unit.dim
            self._unit = unit
            self._compute_magnitude_and_angle()
        else:
            self._coords = np.array([0.0, 0.0, 0.0], dtype=float)
            self._dim = unit.dim
            self._unit = unit

    def _compute_magnitude_and_angle(self) -> None:
        """
        Compute magnitude and angle from vector components.

        If the force previously had a negative magnitude, preserve the sign by adjusting
        the computed angle appropriately.
        """
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        if self._coords is None:
            return

        # Check if we had a negative magnitude before
        had_negative_magnitude = self._magnitude is not None and self._magnitude.value is not None and self._magnitude.value < 0

        # Compute magnitude from vector (always positive from sqrt)
        mag_si = float(np.sqrt(np.sum(self._coords**2)))
        self._magnitude = self._create_quantity(f"{self.name}_magnitude", self._dim, mag_si, self._unit)

        # Compute angle
        angle_rad = math.atan2(self._coords[1], self._coords[0])

        # If we had a negative magnitude, flip it back
        if had_negative_magnitude and self._magnitude is not None and self._magnitude.value is not None:
            self._magnitude.value = -self._magnitude.value

        degree_unit = ureg.resolve("degree", dim=dim.D)
        self._angle = self._create_quantity(f"{self.name}_angle", dim.D, angle_rad, degree_unit)

    # Properties for component access
    @property
    def u(self) -> Quantity[D]:
        """First component as Quantity."""
        return self._make_quantity(0, "u")

    @property
    def v(self) -> Quantity[D]:
        """Second component as Quantity."""
        return self._make_quantity(1, "v")

    @property
    def w(self) -> Quantity[D]:
        """Third component as Quantity."""
        return self._make_quantity(2, "w")

    @staticmethod
    def _create_quantity(name: str, dim, value: float, preferred=None) -> Quantity:
        """Create Quantity bypassing dataclass overhead."""
        q = object.__new__(Quantity)
        q.name = name
        q.dim = dim
        q.value = value
        q.preferred = preferred
        q._symbol = None
        q._output_unit = None
        return q

    def _make_quantity(self, index: int, name: str) -> Quantity[D]:
        """Create Quantity from component index."""
        if self._dim is None:
            raise ValueError("Cannot create Quantity from dimensionless vector components")

        # Get component value and apply tolerance for near-zero values
        # This prevents floating-point precision errors like 3.06e-14 appearing as non-zero
        value = self._coords[index]
        if abs(value) < 1e-10:  # Tolerance: ~10 orders of magnitude below typical engineering values
            value = 0.0

        return self._create_quantity(name, self._dim, value, self._unit)

    @property
    def magnitude(self) -> Quantity[D] | None:
        """
        Vector magnitude/length.

        Returns:
            Magnitude as Quantity with same dimension as components, or None for unknown vectors
        """
        # For ForceVector compatibility - return stored magnitude if it exists
        if hasattr(self, '_magnitude') and self._magnitude is not None:
            return self._magnitude

        # For unknown vectors without magnitude
        if hasattr(self, 'is_known') and not self.is_known:
            return None

        if self._dim is None:
            raise ValueError("Cannot compute magnitude of dimensionless vector")

        mag_si = float(np.sqrt(np.sum(self._coords**2)))
        return self._create_quantity("magnitude", self._dim, mag_si, self._unit)

    @property
    def angle(self) -> Quantity | None:
        """Angle in the angle_reference system (for 2D polar vectors)."""
        return self._angle if hasattr(self, '_angle') else None

    def _direction_angle(self, component_index: int, name: str) -> Quantity | None:
        """Compute coordinate direction angle for a given axis."""
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        mag_si = float(np.sqrt(np.sum(self._coords**2)))
        if mag_si == 0:
            return None
        cos_angle = self._coords[component_index] / mag_si
        angle_rad = math.acos(max(-1.0, min(1.0, cos_angle)))
        degree_unit = ureg.resolve("degree", dim=dim.D)
        return self._create_quantity(name, dim.D, angle_rad, degree_unit)

    @property
    def alpha(self) -> Quantity | None:
        """Coordinate direction angle from +x axis."""
        return self._direction_angle(0, "alpha")

    @property
    def beta(self) -> Quantity | None:
        """Coordinate direction angle from +y axis."""
        return self._direction_angle(1, "beta")

    @property
    def gamma(self) -> Quantity | None:
        """Coordinate direction angle from +z axis."""
        return self._direction_angle(2, "gamma")

    def magnitude_in(self, unit: Unit[D] | str) -> float:
        """
        Get vector magnitude in specified unit.

        This is a convenience method that handles unit conversion automatically,
        similar to Quantity.magnitude(unit).

        Args:
            unit: Target unit for magnitude

        Returns:
            Magnitude value in the specified unit

        Raises:
            ValueError: If vector is dimensionless or unit is incompatible

        Examples:
            >>> from qnty.core.unit_catalog import LengthUnits
            >>> v = Vector(1000, 0, 0, unit=LengthUnits.meter)
            >>> v.magnitude_in("km")
            1.0
            >>> v.magnitude_in(LengthUnits.foot)
            3280.84
        """
        # Determine dimension from vector or stored magnitude
        vector_dim = self._dim
        if vector_dim is None and hasattr(self, '_magnitude') and self._magnitude is not None:
            vector_dim = self._magnitude.dim

        if vector_dim is None:
            raise ValueError("Cannot get magnitude in unit for dimensionless vector")

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=vector_dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # Use the Quantity's magnitude method
        mag_qty = self.magnitude
        if mag_qty is None:
            raise ValueError("Cannot get magnitude of unknown vector")
        return mag_qty.magnitude(unit)

    def normalized(self) -> _Vector[D]:
        """
        Return unit vector in same direction.

        Returns:
            Normalized vector with magnitude 1

        Raises:
            ValueError: If vector is zero (cannot normalize)
        """
        mag = np.sqrt(np.sum(self._coords**2))
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")

        # Create normalized vector
        result = object.__new__(_Vector)
        result._coords = self._coords / mag
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    def unit_vector(self) -> NDArray[np.float64]:
        """
        Return the unit vector (versor) as a numpy array.

        Returns:
            Numpy array [u, v, w] with magnitude 1 (dimensionless)

        Raises:
            ValueError: If vector is zero (cannot compute unit vector)

        Examples:
            >>> from qnty.spatial import create_vector_cartesian
            >>> v = create_vector_cartesian(u=3, v=4, w=0, unit="m")
            >>> u = v.unit_vector()  # [0.6, 0.8, 0.0]
        """
        mag = np.sqrt(np.sum(self._coords**2))
        if mag == 0:
            raise ValueError("Cannot compute unit vector for zero vector")
        return self._coords / mag

    def dot(self, other: "_Vector | NDArray[np.float64] | tuple[float, float, float]") -> "Quantity":
        """
        Compute dot product with another vector.

        Returns the scalar dot product as a Quantity. If the other argument is a
        unit vector (numpy array or tuple), the result has the same dimension as self.

        Args:
            other: Another vector or unit vector (numpy array or tuple)

        Returns:
            Dot product as Quantity

        Examples:
            >>> from qnty.spatial import create_vector_cartesian
            >>> F = create_vector_cartesian(u=3, v=4, w=0, unit="N")
            >>> r = create_vector_cartesian(u=1, v=0, w=0, unit="m")
            >>> # Dot product with unit vector
            >>> F_parallel = F.dot(r.unit_vector())  # 3.0 N
            >>> # Dot product with vector (gives N·m)
            >>> work = F.dot(r)  # 3.0 N·m
        """
        if isinstance(other, (np.ndarray, tuple)):
            # Dot with unit vector (dimensionless array or tuple)
            other_arr = np.array(other) if isinstance(other, tuple) else other
            dot_product = float(np.dot(self._coords, other_arr))
            return self._create_quantity("dot_product", self._dim, dot_product, self._unit)
        elif isinstance(other, _Vector):
            # Dot with another vector
            dot_product = float(np.dot(self._coords, other._coords))
            # Result dimension is product of vector dimensions
            result_dim = self._dim * other._dim if self._dim is not None and other._dim is not None else None
            return self._create_quantity("dot_product", result_dim, dot_product, None)
        else:
            raise TypeError(f"Cannot compute dot product with {type(other)}")

    def cross(self, other: "_Vector | NDArray[np.float64] | tuple[float, float, float]") -> "_Vector":
        """
        Compute cross product with another vector.

        Returns a new vector perpendicular to both input vectors.
        The magnitude of the cross product equals |A||B|sin(θ).

        Args:
            other: Another vector or unit vector (numpy array or tuple)

        Returns:
            New _Vector representing the cross product

        Examples:
            >>> from qnty.spatial import create_vector_cartesian
            >>> F = create_vector_cartesian(u=3, v=4, w=0, unit="N")
            >>> r = create_vector_cartesian(u=1, v=0, w=0, unit="m")
            >>> # Cross product with unit vector
            >>> F_perp = F.cross(r.unit_vector())
            >>> # Magnitude gives perpendicular component
            >>> F_perp_mag = F_perp.magnitude
        """
        if isinstance(other, (np.ndarray, tuple)):
            # Cross with unit vector (dimensionless array or tuple)
            other_arr = np.array(other) if isinstance(other, tuple) else other
            cross_coords = np.cross(self._coords, other_arr)
            # Create result with same dimension as self (cross with dimensionless)
            result = object.__new__(_Vector)
            result._coords = cross_coords
            result._dim = self._dim
            result._unit = self._unit
            self._init_result_slots(result)
            return result
        elif isinstance(other, _Vector):
            # Cross with another vector
            cross_coords = np.cross(self._coords, other._coords)
            # Result dimension is product of vector dimensions
            result_dim = self._dim * other._dim if self._dim is not None and other._dim is not None else None
            result = object.__new__(_Vector)
            result._coords = cross_coords
            result._dim = result_dim
            result._unit = None  # Cross product may have different units
            self._init_result_slots(result)
            return result
        else:
            raise TypeError(f"Cannot compute cross product with {type(other)}")

    def angle_between(self, other: "_Vector") -> "Quantity":
        """
        Compute the angle between this vector and another vector.

        Uses the dot product formula: cos(θ) = (A · B) / (|A| |B|)

        Args:
            other: Another vector

        Returns:
            Angle as Quantity in degrees

        Examples:
            >>> from qnty.spatial import create_vector_cartesian
            >>> r_AB = create_vector_cartesian(u=-2, v=6, w=-3, unit="m")
            >>> r_AC = create_vector_cartesian(u=-4, v=6, w=1, unit="m")
            >>> theta = r_AB.angle_between(r_AC)  # 36.4 deg
        """
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        if not isinstance(other, _Vector):
            raise TypeError(f"Expected _Vector, got {type(other)}")

        # Get magnitudes
        mag_self = np.sqrt(np.sum(self._coords**2))
        mag_other = np.sqrt(np.sum(other._coords**2))

        if mag_self == 0 or mag_other == 0:
            raise ValueError("Cannot compute angle with zero-length vector")

        # Compute dot product and cos(theta)
        dot_product = float(np.dot(self._coords, other._coords))
        cos_theta = dot_product / (mag_self * mag_other)

        # Clamp to [-1, 1] to handle floating point errors
        cos_theta = max(-1.0, min(1.0, cos_theta))

        # Compute angle in radians (SI)
        angle_rad = float(np.arccos(cos_theta))

        # Return as Quantity with degree unit
        deg_unit = ureg.resolve("deg", dim=dim.D)
        return self._create_quantity("angle", dim.D, angle_rad, deg_unit)

    def is_close(
        self,
        other: "_Vector",
        rtol: float = 0.01,
        magnitude_rel_tol: float | None = None,
        magnitude_abs_tol: float | None = None,
        angle_abs_tol_deg: float | None = None,
        compare_components: bool = False,
    ) -> bool:
        """
        Check if this vector is close to another within tolerance.

        Supports two modes:
        - Simple: is_close(other, rtol) - compare components
        - ForceVector: is_close(other, magnitude_rel_tol=..., angle_abs_tol_deg=...)

        Args:
            other: Vector to compare against
            rtol: Relative tolerance for simple mode (default 1%)
            magnitude_rel_tol: Relative tolerance for magnitude (ForceVector mode)
            magnitude_abs_tol: Absolute tolerance for magnitude
            angle_abs_tol_deg: Absolute tolerance for angle in degrees
            compare_components: If True, compare components instead of magnitude/angle

        Returns:
            True if vectors are close
        """
        if not isinstance(other, _Vector):
            return False

        # ForceVector mode - compare magnitude and angle
        # Triggered if any ForceVector-specific tolerance is provided
        use_force_mode = magnitude_rel_tol is not None or angle_abs_tol_deg is not None or magnitude_abs_tol is not None or compare_components
        if use_force_mode:
            # Apply defaults for ForceVector mode
            if magnitude_rel_tol is None:
                magnitude_rel_tol = 1e-6
            if magnitude_abs_tol is None:
                magnitude_abs_tol = 0.0
            if angle_abs_tol_deg is None:
                angle_abs_tol_deg = 0.01
            if not self.is_known and not other.is_known:
                return True

            if self.is_known != other.is_known:
                return False

            if compare_components:
                if self._coords is None or other._coords is None:
                    return False

                for i in range(3):
                    si_val1 = self._coords[i]
                    si_val2 = other._coords[i]
                    max_val = max(abs(si_val1), abs(si_val2))
                    tolerance = magnitude_abs_tol + magnitude_rel_tol * max_val
                    if abs(si_val1 - si_val2) > tolerance:
                        return False
                return True

            if self._magnitude is None or other._magnitude is None:
                return False
            if self._angle is None or other._angle is None:
                return False
            if self._magnitude.value is None or other._magnitude.value is None:
                return False

            mag1_si = self._magnitude.value
            mag2_si = other._magnitude.value
            max_mag = max(abs(mag1_si), abs(mag2_si))
            mag_tolerance = magnitude_abs_tol + magnitude_rel_tol * max_mag

            if abs(mag1_si - mag2_si) > mag_tolerance:
                return False

            if self._angle.value is None or other._angle.value is None:
                return False

            angle1 = self._angle.value % (2 * math.pi)
            angle2 = other._angle.value % (2 * math.pi)
            angle_diff = abs(angle1 - angle2)

            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff

            angle_tolerance_rad = math.radians(angle_abs_tol_deg)
            return angle_diff <= angle_tolerance_rad

        # Simple mode - compare components
        for i in range(3):
            a = self._coords[i]
            b = other._coords[i]
            if b == 0:
                if abs(a) > rtol:
                    return False
            elif abs(a - b) / abs(b) > rtol:
                return False
        return True

    def with_magnitude(self, magnitude: Quantity[D] | float) -> _Vector[D]:
        """
        Return vector in same direction with specified magnitude.

        Args:
            magnitude: Target magnitude (Quantity or float in SI units)

        Returns:
            Scaled vector with specified magnitude

        Raises:
            ValueError: If vector is zero (no direction to scale)
        """
        current_mag = np.sqrt(np.sum(self._coords**2))
        if current_mag == 0:
            raise ValueError("Cannot scale zero vector")

        if isinstance(magnitude, Quantity):
            if magnitude.dim != self._dim:
                raise ValueError(f"Magnitude dimension {magnitude.dim} doesn't match vector dimension {self._dim}")
            if magnitude.value is None:
                raise ValueError("Cannot use unknown quantity as magnitude")
            target_mag = magnitude.value
        else:
            target_mag = float(magnitude)

        scale = target_mag / current_mag

        # Create scaled vector
        result = object.__new__(_Vector)
        result._coords = self._coords * scale
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    @staticmethod
    def _init_result_slots(result: "_Vector") -> None:
        """Initialize all slots for a newly created result vector."""
        result._magnitude = None
        result._angle = None
        result.name = "Vector"
        result.is_known = True
        result.is_resultant = False
        result._description = ""
        result.coordinate_system = None
        result.angle_reference = None
        result._relative_to_force = None
        result._relative_angle = None
        result._from_point = None
        result._to_point = None
        result._constraint_magnitude = None

    def copy_coords_from(self, other: "_Vector") -> None:
        """Copy coordinates, dimension, and unit from another vector."""
        self._coords = other._coords.copy()
        self._dim = other._dim
        self._unit = other._unit

    def get_components_in_system(self) -> tuple["Quantity | None", "Quantity | None"]:
        """
        Get force components in the current coordinate system.

        For standard x-y system, returns (x, y).
        For custom systems (e.g., u-v), returns components along those axes.

        Returns:
            Tuple of (component1, component2) as Quantity objects
        """
        if self._coords is None:
            return (None, None)

        # Get cartesian components
        x_val = self._coords[0]
        y_val = self._coords[1]

        # Convert to coordinate system components
        comp1, comp2 = self.coordinate_system.from_cartesian(x_val, y_val)

        # Create Quantity objects
        from ..core.dimension_catalog import dim
        from ..core.quantity import Quantity

        unit = self._unit

        comp1_qty = Quantity(name=f"{self.name}_{self.coordinate_system.axis1_label}", dim=dim.force, value=comp1, preferred=unit)
        comp2_qty = Quantity(name=f"{self.name}_{self.coordinate_system.axis2_label}", dim=dim.force, value=comp2, preferred=unit)

        return (comp1_qty, comp2_qty)

    def __sub__(self, other: _Vector[D]) -> _Vector[D]:
        """
        Vector subtraction.

        Args:
            other: Vector to subtract

        Returns:
            Difference of vectors

        Raises:
            ValueError: If vectors have different dimensions
        """
        if not isinstance(other, _Vector):
            return NotImplemented

        if self._dim != other._dim:
            raise ValueError(f"Cannot subtract vectors with different dimensions: {self._dim} vs {other._dim}")

        # Vectorized subtraction (SI values)
        result = object.__new__(_Vector)
        result._coords = self._coords - other._coords
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    def __mul__(self, scalar: float | int) -> _Vector[D]:
        """
        Scalar multiplication.

        Args:
            scalar: Scaling factor

        Returns:
            Scaled vector
        """
        result = object.__new__(_Vector)
        result._coords = self._coords * float(scalar)
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    __rmul__ = __mul__

    def __truediv__(self, scalar: float | int) -> _Vector[D]:
        """
        Scalar division.

        Args:
            scalar: Divisor

        Returns:
            Scaled vector

        Raises:
            ZeroDivisionError: If scalar is zero
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero")

        result = object.__new__(_Vector)
        result._coords = self._coords / float(scalar)
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    def __neg__(self) -> _Vector[D]:
        """
        Negation (opposite direction).

        Returns:
            Vector pointing in opposite direction
        """
        result = object.__new__(_Vector)
        result._coords = -self._coords
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    def is_parallel_to(self, other: _Vector[D], tolerance: float = 1e-10) -> bool:
        """
        Test whether vector is parallel to another.

        Args:
            other: Vector to compare with
            tolerance: Tolerance for parallelism test

        Returns:
            True if vectors are parallel (cross product near zero)
        """
        if not isinstance(other, _Vector):
            raise TypeError(f"Expected _Vector, got {type(other)}")

        cross_coords = np.cross(self._coords, other._coords)
        cross_magnitude = np.sqrt(np.sum(cross_coords**2))

        return bool(cross_magnitude < tolerance)

    def is_perpendicular_to(self, other: _Vector[D], tolerance: float = 1e-10) -> bool:
        """
        Test whether vector is perpendicular to another.

        Args:
            other: Vector to compare with
            tolerance: Tolerance for perpendicularity test

        Returns:
            True if vectors are perpendicular (dot product near zero)
        """
        if not isinstance(other, _Vector):
            raise TypeError(f"Expected _Vector, got {type(other)}")

        dot_product = np.sum(self._coords * other._coords)

        return bool(abs(dot_product) < tolerance)

    def angle_to(self, other: _Vector[D]) -> Quantity:
        """
        Compute angle between this vector and another.

        Args:
            other: Vector to compute angle to

        Returns:
            Angle as dimensionless Quantity (in radians)

        Raises:
            ValueError: If either vector is zero
        """
        if not isinstance(other, _Vector):
            raise TypeError(f"Expected _Vector, got {type(other)}")

        mag_self = np.sqrt(np.sum(self._coords**2))
        mag_other = np.sqrt(np.sum(other._coords**2))

        if mag_self == 0 or mag_other == 0:
            raise ValueError("Cannot compute angle with zero vector")

        # Compute angle using dot product
        cos_angle = np.sum(self._coords * other._coords) / (mag_self * mag_other)

        # Clamp to [-1, 1] to handle numerical errors
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle_rad = float(np.arccos(cos_angle))

        # Return as dimensionless Quantity
        from ..core.dimension_catalog import dim
        return self._create_quantity("angle", dim.angle_plane, angle_rad, None)

    def projection_onto(self, other: _Vector[D]) -> _Vector[D]:
        """
        Compute projection of this vector onto another.

        Args:
            other: Vector to project onto

        Returns:
            Projection vector (parallel to other)

        Raises:
            ValueError: If other vector is zero
        """
        if not isinstance(other, _Vector):
            raise TypeError(f"Expected _Vector, got {type(other)}")

        mag_other_sq = np.sum(other._coords**2)
        if mag_other_sq == 0:
            raise ValueError("Cannot project onto zero vector")

        # Projection formula: proj = (v · u / |u|²) * u
        dot_product = np.sum(self._coords * other._coords)
        scale = dot_product / mag_other_sq

        result = object.__new__(_Vector)
        result._coords = scale * other._coords
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        return result

    def to_unit(self, unit: Unit[D] | str) -> _Vector[D]:
        """
        Convert to different display unit (SI values unchanged).

        Args:
            unit: Target unit for display

        Returns:
            New Vector with updated display unit
        """
        unit = resolve_unit_from_string(unit, dim=self._dim)

        # Create new _Vector with same SI values, different display unit
        result = object.__new__(_Vector)
        result._coords = self._coords.copy()  # Copy to avoid aliasing
        result._dim = self._dim
        result._unit = unit
        self._init_result_slots(result)
        return result

    def to_array(self) -> NDArray[np.float64]:
        """
        Get components as numpy array (in current display unit).

        Returns:
            Array of [u, v, w] components in display units
        """
        if self._unit is None:
            return self._coords.copy()
        return (self._coords - self._unit.si_offset) / self._unit.si_factor

    def __str__(self) -> str:
        """String representation of the vector."""
        coords = self.to_array()
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        return f"_Vector({coords[0]:.6g}, {coords[1]:.6g}, {coords[2]:.6g}{unit_str})"

    def __repr__(self) -> str:
        """Representation of the vector."""
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """
        Check equality between vectors (same components and dimension).

        Returns:
            True if vectors are equal within tolerance
        """
        if not isinstance(other, _Vector):
            return NotImplemented

        if self._dim != other._dim:
            return False

        # Use small tolerance for floating point comparison
        return bool(np.allclose(self._coords, other._coords, rtol=1e-10, atol=1e-10))

    def __hash__(self) -> int:
        """Hash based on name for use in sets/dicts."""
        return hash(self.name) if hasattr(self, 'name') else id(self)

    # ForceVector factory methods and properties
    @classmethod
    def resultant(cls, vectors: list["_Vector"], name: str | None = None) -> "_Vector":
        """Create resultant from a list of vectors."""
        if not vectors:
            raise ValueError("Cannot compute resultant of empty list")

        result = vectors[0]
        for v in vectors[1:]:
            result = result + v

        result.name = name or "R"
        result.is_resultant = True
        return result

    @classmethod
    def unknown(cls, name: str, is_resultant: bool = False, magnitude: float | None = None,
                angle: float | None = None, coordinate_system: "CoordinateSystem | None" = None,
                angle_reference: "AngleReference | None" = None, wrt: str | None = None, **kwargs) -> "_Vector":
        """Create an unknown vector to be solved for."""
        return cls(magnitude=magnitude, angle=angle, name=name, is_known=False, is_resultant=is_resultant,
                  coordinate_system=coordinate_system, angle_reference=angle_reference, wrt=wrt, **kwargs)

    @classmethod
    def from_position_vector(cls, pos_vector: "_Vector", magnitude: float | Quantity,
                            unit: Unit | str | None = None, name: str | None = None, **kwargs) -> "_Vector":
        """Create vector directed along a position vector."""
        # Get unit vector (direction cosines)
        mag = np.sqrt(np.sum(pos_vector._coords**2))
        if mag == 0:
            raise ValueError("Cannot create vector from zero position vector")

        cos_alpha = pos_vector._coords[0] / mag
        cos_beta = pos_vector._coords[1] / mag
        cos_gamma = pos_vector._coords[2] / mag

        # Convert magnitude to SI
        if isinstance(magnitude, int | float):
            if unit is None:
                raise ValueError("unit must be specified")
            if isinstance(unit, str):
                from ..core.unit import ureg
                resolved = ureg.resolve(unit)
                if resolved is None:
                    raise ValueError(f"Unknown unit '{unit}'")
                unit = resolved
            mag_si = float(magnitude) * unit.si_factor
        else:
            if magnitude.value is None:
                raise ValueError("Magnitude must have a known value")
            mag_si = magnitude.value
            unit = magnitude.preferred

        # Compute components
        x_val = mag_si * cos_alpha
        y_val = mag_si * cos_beta
        z_val = mag_si * cos_gamma

        return cls(x=x_val / unit.si_factor, y=y_val / unit.si_factor, z=z_val / unit.si_factor,
                  unit=unit, name=name, **kwargs)

    @classmethod
    def from_points(cls, from_point: "PointLike | _Point", to_point: "PointLike | _Point",
                   name: str | None = None, magnitude: float | None = None, unit: Unit | str | None = None) -> "_Vector":
        """Create position vector from point A to point B."""
        from .point import _Point

        # Convert to _Point if needed
        if isinstance(from_point, _Point):
            from_pt = from_point
        else:
            from_pt = from_point.to_cartesian()
        if isinstance(to_point, _Point):
            to_pt = to_point
        else:
            to_pt = to_point.to_cartesian()

        if from_pt._dim != to_pt._dim:
            raise ValueError(f"Points must have same dimension: {from_pt._dim} vs {to_pt._dim}")

        delta = to_pt._coords - from_pt._coords

        result = object.__new__(cls)
        result._coords = delta
        result._dim = from_pt._dim
        result._unit = from_pt._unit or to_pt._unit
        result.name = name or "r"
        result.is_known = True
        result.is_resultant = False
        result._description = ""
        result.coordinate_system = None
        result.angle_reference = None
        result._magnitude = None
        result._angle = None
        result._relative_to_force = None
        result._relative_angle = None
        result._from_point = from_point
        result._to_point = to_point

        if magnitude is not None:
            if isinstance(unit, str):
                from ..core.dimension_catalog import dim
                from ..core.unit import ureg
                resolved = ureg.resolve(unit, dim=dim.length)
                if resolved is None:
                    raise ValueError(f"Unknown unit '{unit}'")
                unit = resolved
            result._constraint_magnitude = magnitude * unit.si_factor if unit else magnitude
        else:
            result._constraint_magnitude = None

        return result

    # ForceVector properties
    @property
    def x(self) -> Quantity | None:
        """X-component."""
        if not hasattr(self, '_coords') or self._coords is None or self._dim is None:
            return None
        return self._make_quantity(0, "x")

    @property
    def y(self) -> Quantity | None:
        """Y-component."""
        if not hasattr(self, '_coords') or self._coords is None or self._dim is None:
            return None
        return self._make_quantity(1, "y")

    @property
    def z(self) -> Quantity | None:
        """Z-component."""
        if not hasattr(self, '_coords') or self._coords is None or self._dim is None:
            return None
        return self._make_quantity(2, "z")

    @property
    def vector(self) -> "_Vector | None":
        """Return self for compatibility with ForceVector API."""
        return self if hasattr(self, '_coords') else None

    @property
    def description(self) -> str:
        """Vector description."""
        return self._description if hasattr(self, '_description') else ""

    @property
    def constraint_magnitude(self) -> float | None:
        """Magnitude constraint in SI units, if any."""
        return self._constraint_magnitude if hasattr(self, '_constraint_magnitude') else None

    @property
    def from_point(self):
        """Starting point reference."""
        return self._from_point if hasattr(self, '_from_point') else None

    @property
    def to_point(self):
        """Ending point reference."""
        return self._to_point if hasattr(self, '_to_point') else None

    def has_unknowns(self) -> bool:
        """Check if either point has unknown coordinates."""
        from_unknowns = getattr(self._from_point, 'unknowns', {}) if hasattr(self, '_from_point') and self._from_point else {}
        to_unknowns = getattr(self._to_point, 'unknowns', {}) if hasattr(self, '_to_point') and self._to_point else {}
        return bool(from_unknowns) or bool(to_unknowns)

    def to_cartesian(self) -> "_Vector":
        """Convert to Cartesian _Vector."""
        result = object.__new__(_Vector)
        result._coords = self._coords.copy()
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        result.name = self.name if hasattr(self, 'name') else "Vector"
        return result

    def angle_in(self, unit: Unit | str = "degree", wrt: str | None = None, forces: dict[str, "_Vector"] | None = None) -> float:
        """Get angle in specified unit and reference system."""
        if not hasattr(self, '_angle') or self._angle is None:
            raise ValueError(f"Vector {self.name} has no angle")
        if self._angle.value is None:
            raise ValueError(f"Vector {self.name} angle is unknown")

        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg
            resolved = ureg.resolve(unit, dim=dim.D)
            if resolved is None:
                raise ValueError(f"Unknown angle unit '{unit}'")
            unit = resolved

        angle_rad = self._angle.value

        if wrt is not None:
            # Check if wrt references another force
            if forces is not None and any(c.isupper() or c == "_" for c in wrt.lstrip("+-:")):
                # Extract force reference
                ref_part = wrt.split(":")[-1].lstrip("+-")
                if ref_part in forces:
                    ref_force = forces[ref_part]
                    if hasattr(ref_force, '_angle') and ref_force._angle is not None and ref_force._angle.value is not None:
                        ref_angle = ref_force._angle.value
                        relative_angle = angle_rad - ref_angle
                        return float(relative_angle / unit.si_factor)

            angle_ref = _Vector.parse_wrt_static(wrt, self.coordinate_system if hasattr(self, 'coordinate_system') else None)
            angle_rad = angle_ref.from_standard(angle_rad, angle_unit="radian")

        return float(angle_rad / unit.si_factor)

    def resolve_relative_angle(self, vectors: dict[str, "_Vector"]) -> None:
        """Resolve relative angle constraint to absolute angle."""
        if not hasattr(self, '_relative_to_force') or self._relative_to_force is None:
            return

        if self._relative_to_force not in vectors:
            raise ValueError(f"Vector {self.name} references unknown vector '{self._relative_to_force}'")

        ref_vec = vectors[self._relative_to_force]

        if not hasattr(ref_vec, '_angle') or ref_vec._angle is None or ref_vec._angle.value is None:
            raise ValueError("Referenced vector doesn't have known angle")

        ref_angle_rad = ref_vec._angle.value
        relative_offset = self._relative_angle if self._relative_angle else 0.0
        absolute_angle_rad = ref_angle_rad + relative_offset

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)
        self._angle = Quantity(name=f"{self.name}_angle", dim=dim.D, value=absolute_angle_rad, preferred=degree_unit)

        self._relative_to_force = None
        self._relative_angle = None

        if self._magnitude is not None and self._magnitude.value is not None:
            mag_si = self._magnitude.value
            x_val = mag_si * math.cos(absolute_angle_rad)
            y_val = mag_si * math.sin(absolute_angle_rad)
            self._coords = np.array([x_val, y_val, 0.0], dtype=float)
            self.is_known = True

    def has_relative_angle(self) -> bool:
        """Check if vector has unresolved relative angle constraint."""
        return hasattr(self, '_relative_to_force') and self._relative_to_force is not None

    def clone(self, name: str | None = None) -> "_Vector":
        """
        Create a deep copy of this vector.

        This method creates an independent copy of the vector with all
        attributes preserved. Useful when you need to modify a vector
        without affecting the original.

        Args:
            name: Optional new name for the cloned vector. If not provided,
                  uses the original vector's name.

        Returns:
            A new _Vector instance with copied attributes.

        Examples:
            >>> v = _Vector(magnitude=100, angle=45, unit="N", name="F1")
            >>> v_copy = v.clone()
            >>> v_copy.name
            'F1'
            >>> v_copy = v.clone(name="F1_copy")
            >>> v_copy.name
            'F1_copy'
        """
        result = object.__new__(_Vector)
        result._coords = self._coords.copy()
        result._dim = self._dim
        result._unit = self._unit

        # Use provided name or original name (not default "Vector")
        original_name = getattr(self, 'name', "")
        result.name = name if name is not None else (original_name if original_name and original_name != "Vector" else "")

        result._description = getattr(self, '_description', "")
        result.is_known = getattr(self, 'is_known', True)
        result.is_resultant = getattr(self, 'is_resultant', False)
        result.coordinate_system = getattr(self, 'coordinate_system', None)
        result.angle_reference = getattr(self, 'angle_reference', None)

        # Copy magnitude and angle
        result._magnitude = self._magnitude
        result._angle = self._angle

        # Copy relative angle info
        result._relative_to_force = getattr(self, '_relative_to_force', None)
        result._relative_angle = getattr(self, '_relative_angle', None)

        # Copy original angle and wrt for reporting
        if hasattr(self, '_original_angle'):
            result._original_angle = self._original_angle
        if hasattr(self, '_original_wrt'):
            result._original_wrt = self._original_wrt

        # Copy position vector attributes
        result._from_point = getattr(self, '_from_point', None)
        result._to_point = getattr(self, '_to_point', None)
        result._constraint_magnitude = getattr(self, '_constraint_magnitude', None)

        return result

    def __add__(self, other: "_Vector[D]") -> "_Vector[D]":
        """Vector addition."""
        if not isinstance(other, _Vector):
            return NotImplemented

        if self._dim != other._dim:
            raise ValueError(f"Cannot add vectors with different dimensions: {self._dim} vs {other._dim}")

        result = object.__new__(_Vector)
        result._coords = self._coords + other._coords
        result._dim = self._dim
        result._unit = self._unit
        self._init_result_slots(result)
        self_name = getattr(self, 'name', "Vector")
        other_name = getattr(other, 'name', "Vector")
        result.name = f"{self_name}+{other_name}"
        return result
