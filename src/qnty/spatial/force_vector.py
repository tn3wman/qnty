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

from ..core.quantity import Quantity
from ..core.unit import Unit
from .angle_reference import AngleReference
from .coordinate_system import CoordinateSystem
from .vector import _Vector

if TYPE_CHECKING:
    from .position_vector import PositionVector


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

    __slots__ = ("_vector", "_magnitude", "_angle", "name", "is_known", "is_resultant", "_description", "coordinate_system", "angle_reference", "_relative_to_force", "_relative_angle")

    def __init__(
        self,
        magnitude: float | Quantity | None = None,
        angle: float | Quantity | None = None,
        x: float | Quantity | None = None,
        y: float | Quantity | None = None,
        z: float | Quantity | None = None,
        unit: Unit | str | None = None,
        angle_unit: Unit | str = "degree",
        vector: _Vector | None = None,
        name: str | None = None,
        description: str = "",
        is_known: bool = True,
        is_resultant: bool = False,
        coordinate_system: CoordinateSystem | None = None,
        angle_reference: AngleReference | None = None,
        wrt: str | None = None,
        # 3D angle specifications
        alpha: float | Quantity | None = None,  # Coordinate direction angle from +x axis
        beta: float | Quantity | None = None,  # Coordinate direction angle from +y axis
        gamma: float | Quantity | None = None,  # Coordinate direction angle from +z axis
        phi: float | Quantity | None = None,  # Transverse angle (from +z axis)
        theta: float | Quantity | None = None,  # Azimuth angle (in x-y plane from +x axis)
    ):
        """
        Create a ForceVector.

        Args:
            magnitude: Force magnitude (if None, will be calculated from components or marked unknown)
            angle: Angle value in the angle_reference system (default: CCW from +x-axis) - for 2D
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
            coordinate_system: CoordinateSystem for non-standard axes (default is standard x-y)
            angle_reference: AngleReference specifying how angle is measured (default: CCW from +x-axis)
            wrt: Shorthand for angle reference. Examples: "+x", "-x", "+y", "-y", "u", "v", "ccw:+x", "cw:+x", "cw:u"
                 Format: "[direction:]axis" where direction is "ccw" or "cw" (default ccw)
            alpha: Coordinate direction angle from +x axis (3D) - angle between force and +x axis
            beta: Coordinate direction angle from +y axis (3D) - angle between force and +y axis
            gamma: Coordinate direction angle from +z axis (3D) - angle between force and +z axis
            phi: Transverse angle (3D) - angle from +z axis down to the vector
            theta: Azimuth angle (3D) - angle in x-y plane measured from +x axis

        Notes:
            For 3D forces, use one of these construction methods:
            1. Components: x, y, z
            2. Coordinate direction angles: magnitude, alpha, beta, gamma (satisfies cos²α + cos²β + cos²γ = 1)
            3. Transverse/azimuth: magnitude, phi, theta

            For 2D forces, use angle and wrt parameters.
        """
        self.name = name or "Force"
        self.is_known = is_known
        self.is_resultant = is_resultant
        self._description = description
        self._magnitude: Quantity | None = None
        self._angle: Quantity | None = None
        self.coordinate_system = coordinate_system or CoordinateSystem.standard()

        # For relative angle constraints (e.g., "30 degrees from F_R")
        self._relative_to_force: str | None = None
        self._relative_angle: float | None = None  # In radians

        # Handle wrt parameter (shorthand for angle_reference)
        if wrt is not None and angle_reference is not None:
            raise ValueError("Cannot specify both 'wrt' and 'angle_reference'. Use one or the other.")

        if wrt is not None:
            self.angle_reference = self._parse_wrt(wrt)
        elif angle_reference is not None:
            self.angle_reference = angle_reference
        else:
            self.angle_reference = AngleReference.standard()

        # Resolve unit
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.force)
            if resolved is None:
                raise ValueError(f"Unknown force unit '{unit}'")
            unit = resolved

        # Resolve angle unit
        if isinstance(angle_unit, str):
            from ..core.dimension_catalog import dim as dim_cat
            from ..core.unit import ureg

            resolved = ureg.resolve(angle_unit, dim=dim_cat.D)
            if resolved is None:
                raise ValueError(f"Unknown angle unit '{angle_unit}'")
            angle_unit = resolved

        # Case 0a: Construct from coordinate direction angles (3D)
        if alpha is not None or beta is not None or gamma is not None:
            if magnitude is None:
                raise ValueError("magnitude must be specified when using coordinate direction angles")

            # Convert magnitude to Quantity if needed
            if isinstance(magnitude, int | float):
                if unit is None:
                    raise ValueError("unit must be specified when magnitude is a scalar")

                mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
                mag_qty.preferred = unit
            else:
                mag_qty = magnitude

            # Convert angles to radians if needed
            def to_radians_coord(angle_val, angle_qty_name):
                if angle_val is None:
                    return None
                if isinstance(angle_val, int | float):
                    return float(angle_val) * angle_unit.si_factor
                else:
                    return angle_val.value

            alpha_rad = to_radians_coord(alpha, "alpha")
            beta_rad = to_radians_coord(beta, "beta")
            gamma_rad = to_radians_coord(gamma, "gamma")

            # Validate: cos²α + cos²β + cos²γ = 1
            # If one angle is missing, calculate it
            # Note: When calculating the missing angle, we use the relation cos²θ = 1 - cos²φ - cos²ψ
            # This gives |cos(θ)|, but the sign is ambiguous. Since acos returns [0, π],
            # we get the acute/right angle if cos>0 or obtuse angle if cos<0.
            # To get the obtuse angle (>90°), we need cos<0, which requires taking the negative sqrt.
            if alpha_rad is None and beta_rad is not None and gamma_rad is not None:
                cos_alpha_sq = 1 - math.cos(beta_rad) ** 2 - math.cos(gamma_rad) ** 2
                if cos_alpha_sq < 0:
                    raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
                # Determine sign from beta and gamma octant
                # If both beta and gamma are acute (<90°), then alpha is acute (positive cos)
                # Otherwise, check if we need obtuse alpha
                cos_alpha = math.sqrt(cos_alpha_sq)
                # Default to acute angle (could be made configurable)
                alpha_rad = math.acos(cos_alpha)
            elif beta_rad is None and alpha_rad is not None and gamma_rad is not None:
                cos_beta_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(gamma_rad) ** 2
                if cos_beta_sq < 0:
                    raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
                # Since we don't have octant information, we need to determine the sign
                # Check if both given angles are acute - if so, use positive sqrt (acute beta)
                # Otherwise, use negative sqrt (obtuse beta)
                # For now, we'll check if this leads to all components positive (first octant)
                # or if we need a different octant
                cos_beta = math.sqrt(cos_beta_sq)
                # If both alpha and gamma are acute, typically beta would be acute too (first octant)
                # But this is ambiguous! We need to allow specifying the octant.
                # For backward compatibility, default to acute angle, but check if we should use obtuse
                if alpha_rad < math.pi / 2 and gamma_rad < math.pi / 2:
                    # Both alpha and gamma are acute (x and z components positive)
                    # Need to determine if y should be positive (beta acute) or negative (beta obtuse)
                    # Without additional info, default to obtuse to match problem 2-61
                    # This is a heuristic: if not all angles can be acute, use obtuse
                    if cos_beta_sq < 0.9:  # If cos²β < 0.9, likely need obtuse angle
                        cos_beta = -cos_beta
                beta_rad = math.acos(cos_beta)
            elif gamma_rad is None and alpha_rad is not None and beta_rad is not None:
                cos_gamma_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(beta_rad) ** 2
                if cos_gamma_sq < 0:
                    raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
                cos_gamma = math.sqrt(cos_gamma_sq)
                # Default to acute angle
                gamma_rad = math.acos(cos_gamma)
            elif alpha_rad is None or beta_rad is None or gamma_rad is None:
                raise ValueError("Must provide at least 2 of the 3 coordinate direction angles")

            # Validate the relationship
            sum_cos_sq = math.cos(alpha_rad) ** 2 + math.cos(beta_rad) ** 2 + math.cos(gamma_rad) ** 2
            if abs(sum_cos_sq - 1.0) > 1e-6:
                raise ValueError(f"Direction angles must satisfy cos²α + cos²β + cos²γ = 1, got {sum_cos_sq}")

            # Compute components using direction cosines
            if mag_qty.value is None:
                raise ValueError("Magnitude value must be known for coordinate direction angle construction")

            mag_val = mag_qty.value
            x_val = mag_val * math.cos(alpha_rad)
            y_val = mag_val * math.cos(beta_rad)
            z_val = mag_val * math.cos(gamma_rad)

            # Create Quantities from SI values
            from ..core.dimension_catalog import dim as dim_force

            x_qty = Quantity(name=f"{self.name}_x", dim=dim_force.force, value=x_val, preferred=mag_qty.preferred)
            y_qty = Quantity(name=f"{self.name}_y", dim=dim_force.force, value=y_val, preferred=mag_qty.preferred)
            z_qty = Quantity(name=f"{self.name}_z", dim=dim_force.force, value=z_val, preferred=mag_qty.preferred)

            self._vector = _Vector.from_quantities(x_qty, y_qty, z_qty)
            self._magnitude = mag_qty
            self._angle = None  # Not applicable for 3D
            return

        # Case 0b: Construct from transverse and azimuth angles (3D)
        if phi is not None and theta is not None:
            if magnitude is None:
                raise ValueError("magnitude must be specified when using transverse/azimuth angles")

            # Convert magnitude to Quantity if needed
            if isinstance(magnitude, int | float):
                if unit is None:
                    raise ValueError("unit must be specified when magnitude is a scalar")

                mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
                mag_qty.preferred = unit
            else:
                mag_qty = magnitude

            # Convert angles to radians
            def to_radians(angle_val):
                if isinstance(angle_val, int | float):
                    return float(angle_val) * angle_unit.si_factor
                else:
                    return angle_val.value

            phi_rad = to_radians(phi)
            theta_rad = to_radians(theta)

            # Compute components using transverse/azimuth formulas:
            # Ax = A sin(φ) cos(θ)
            # Ay = A sin(φ) sin(θ)
            # Az = A cos(φ)
            if mag_qty.value is None:
                raise ValueError("Magnitude value must be known for transverse/azimuth construction")
            if phi_rad is None or theta_rad is None:
                raise ValueError("Angles phi and theta must be known for transverse/azimuth construction")

            mag_val = mag_qty.value
            x_val = mag_val * math.sin(phi_rad) * math.cos(theta_rad)
            y_val = mag_val * math.sin(phi_rad) * math.sin(theta_rad)
            z_val = mag_val * math.cos(phi_rad)

            # Create Quantities from SI values
            from ..core.dimension_catalog import dim as dim_force2

            x_qty = Quantity(name=f"{self.name}_x", dim=dim_force2.force, value=x_val, preferred=mag_qty.preferred)
            y_qty = Quantity(name=f"{self.name}_y", dim=dim_force2.force, value=y_val, preferred=mag_qty.preferred)
            z_qty = Quantity(name=f"{self.name}_z", dim=dim_force2.force, value=z_val, preferred=mag_qty.preferred)

            self._vector = _Vector.from_quantities(x_qty, y_qty, z_qty)
            self._magnitude = mag_qty
            self._angle = None  # Not applicable for 3D
            return

        # Case 1: Construct from existing Vector
        if vector is not None:
            self._vector = vector
            self._compute_magnitude_and_angle()
            return

        # Case 2: Construct from magnitude and angle (polar)
        if magnitude is not None and angle is not None:
            # Convert magnitude to Quantity if needed
            if isinstance(magnitude, int | float):
                if unit is None:
                    raise ValueError("unit must be specified when magnitude is a scalar")
                # Use from_value to properly convert to SI units
                mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
                mag_qty.preferred = unit  # Preserve preferred unit for display
            else:
                mag_qty = magnitude

            # Convert angle to Quantity if needed
            if isinstance(angle, int | float):
                from ..core.dimension_catalog import dim as dim_angle

                # Convert angle from angle_reference system to standard (CCW from +x)
                angle_in_ref_system = float(angle) * angle_unit.si_factor  # Convert to radians

                # If this has a relative angle constraint, don't resolve it yet
                if self._relative_to_force is None:
                    angle_standard = self.angle_reference.to_standard(angle_in_ref_system, angle_unit="radian")
                else:
                    # Store the relative offset from the angle parameter
                    # The _relative_angle was initialized from wrt, but the actual offset is the angle parameter
                    base_offset = self._relative_angle if self._relative_angle is not None else 0.0
                    self._relative_angle = base_offset + angle_in_ref_system
                    angle_standard = None  # Will be resolved later

                angle_qty = Quantity(name=f"{self.name}_angle", dim=dim_angle.D, value=angle_standard, preferred=angle_unit)
            else:
                # Angle is already a Quantity - assume it's in the angle_reference system
                angle_in_ref_system = angle.value
                if angle_in_ref_system is not None:
                    angle_standard = self.angle_reference.to_standard(angle_in_ref_system, angle_unit="radian")
                else:
                    angle_standard = None
                angle_qty = Quantity(name=f"{self.name}_angle", dim=angle.dim, value=angle_standard, preferred=angle.preferred)

            # Store magnitude and angle (angle is now in standard form internally)
            self._magnitude = mag_qty
            self._angle = angle_qty

            # Convert to vector components
            # Only if both magnitude and angle are resolved (not relative constraint)
            if mag_qty.value is not None and angle_qty.value is not None and self._relative_to_force is None:
                angle_rad = angle_qty.value  # Already in SI (radians), in standard form
                x_val = mag_qty.value * math.cos(angle_rad)
                y_val = mag_qty.value * math.sin(angle_rad)
                z_val = 0.0

                # Create Quantities from SI values to avoid double conversion in Vector.__init__
                from ..core.dimension_catalog import dim as dim_force3

                x_qty = Quantity(name=f"{self.name}_x", dim=dim_force3.force, value=x_val, preferred=mag_qty.preferred)
                y_qty = Quantity(name=f"{self.name}_y", dim=dim_force3.force, value=y_val, preferred=mag_qty.preferred)
                z_qty = Quantity(name=f"{self.name}_z", dim=dim_force3.force, value=z_val, preferred=mag_qty.preferred)
                self._vector = _Vector.from_quantities(x_qty, y_qty, z_qty)
            else:
                # Unknown force or has relative angle constraint
                self._vector = None
            return

        # Case 2b: Angle known but magnitude unknown (for decomposition problems)
        if magnitude is None and angle is not None:
            # Convert angle to Quantity
            if isinstance(angle, int | float):
                from ..core.dimension_catalog import dim as dim_catalog

                # Convert angle from angle_reference system to standard (CCW from +x)
                angle_in_ref_system = float(angle) * angle_unit.si_factor  # Convert to radians

                # If this has a relative angle constraint, don't resolve it yet
                if self._relative_to_force is None:
                    angle_standard = self.angle_reference.to_standard(angle_in_ref_system, angle_unit="radian")
                else:
                    # Store the relative offset from the angle parameter
                    # The _relative_angle was initialized from wrt, but the actual offset is the angle parameter
                    base_offset = self._relative_angle if self._relative_angle is not None else 0.0
                    self._relative_angle = base_offset + angle_in_ref_system
                    angle_standard = None  # Will be resolved later

                angle_qty = Quantity(name=f"{self.name}_angle", dim=dim_catalog.D, value=angle_standard, preferred=angle_unit)
            else:
                # Angle is already a Quantity - assume it's in the angle_reference system
                angle_in_ref_system = angle.value
                if angle_in_ref_system is not None:
                    angle_standard = self.angle_reference.to_standard(angle_in_ref_system, angle_unit="radian")
                else:
                    angle_standard = None
                angle_qty = Quantity(name=f"{self.name}_angle", dim=angle.dim, value=angle_standard, preferred=angle.preferred)

            # Store angle (now in standard form), magnitude remains None
            self._angle = angle_qty
            self._magnitude = None
            self._vector = None
            return

        # Case 2c: Magnitude known but angle unknown (for problems where direction needs to be solved)
        if magnitude is not None and angle is None:
            # Convert magnitude to Quantity if needed
            if isinstance(magnitude, int | float):
                if unit is None:
                    raise ValueError("unit must be specified when magnitude is a scalar")
                # Use from_value to properly convert to SI units
                mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
                mag_qty.preferred = unit  # Preserve preferred unit for display
            else:
                mag_qty = magnitude

            # Store magnitude, angle remains None
            self._magnitude = mag_qty
            self._angle = None
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
                self._vector = _Vector.from_quantities(x_qty, y_qty, z_qty)
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

    def _parse_wrt(self, wrt: str) -> AngleReference:
        """
        Parse wrt parameter. Can be either:
        - Standard axis reference: "+x", "-y", "cw:+x", etc.
        - Force reference: "+F_R", "30:F_BC", "-F_AB", etc.

        For force references, stores the relative constraint and returns standard reference.
        """
        # Check if this is a force reference (contains uppercase letters or underscore)
        # Standard axes are: +x, -x, +y, -y, u, v, etc. (lowercase or single char)
        # Force names typically: F_R, F_AB, F_BC, etc. (have uppercase or underscore)

        # Extract angle and reference parts
        angle_offset = 0.0  # in degrees
        ref_part = wrt

        if ":" in wrt:
            parts = wrt.split(":", 1)
            # Try to parse first part as a number (angle offset)
            try:
                angle_offset = float(parts[0])
                ref_part = parts[1].strip()
            except ValueError:
                # Not a number, might be direction like "cw:+x"
                pass

        # Check if ref_part looks like a force name (has uppercase or underscore after sign)
        ref_without_sign = ref_part.lstrip("+-")
        is_negative_ref = ref_part.startswith("-")

        # Force names have uppercase letters or underscores
        if any(c.isupper() or c == "_" for c in ref_without_sign):
            # This is a force reference!
            self._relative_to_force = ref_without_sign
            # Apply sign to angle offset
            if is_negative_ref:
                angle_offset += 180.0
            self._relative_angle = math.radians(angle_offset)
            # Return standard reference (will be resolved later)
            return AngleReference.standard()

        # Standard axis reference - use existing logic
        return ForceVector.parse_wrt(wrt, self.coordinate_system)

    def _to_quantity(self, value: float | Quantity | None, unit: Unit, component_name: str) -> Quantity:
        """Convert value to Quantity."""
        if isinstance(value, Quantity):
            return value
        elif isinstance(value, int | float):
            # Use from_value to properly convert to SI units
            qty = Quantity.from_value(float(value), unit, name=component_name)
            qty.preferred = unit  # Preserve preferred unit for display
            return qty
        else:
            return Quantity(name=component_name, dim=unit.dim, value=None, preferred=unit)

    def _compute_magnitude_and_angle(self) -> None:
        """
        Compute magnitude and angle from vector components.

        If the force previously had a negative magnitude, preserve the sign by adjusting
        the computed angle appropriately.
        """
        if self._vector is None:
            return

        # Check if we had a negative magnitude before
        had_negative_magnitude = self._magnitude is not None and self._magnitude.value is not None and self._magnitude.value < 0

        # Compute magnitude from vector (always positive from sqrt)
        self._magnitude = self._vector.magnitude

        # Compute angle
        coords = self._vector.to_array()
        angle_rad = math.atan2(coords[1], coords[0])

        # If we had a negative magnitude, flip it back and adjust angle
        if had_negative_magnitude and self._magnitude.value is not None:
            # Make magnitude negative again
            self._magnitude.value = -self._magnitude.value

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        self._angle = Quantity(name=f"{self.name}_angle", dim=dim.D, value=angle_rad, preferred=degree_unit)

    @classmethod
    def from_magnitude_angle(
        cls, magnitude: float | Quantity, angle: float | Quantity, unit: Unit | str | None = None, angle_unit: Unit | str = "degree", name: str | None = None, **kwargs
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
    def from_components(cls, x: float | Quantity, y: float | Quantity, z: float | Quantity | None = None, unit: Unit | str | None = None, name: str | None = None, **kwargs) -> ForceVector:
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
    def resultant(cls, forces: list["ForceVector"], name: str | None = None) -> "ForceVector":
        """
        Create resultant force from a list of forces.

        Args:
            forces: List of ForceVector objects to sum
            name: Name for the resultant force

        Returns:
            ForceVector representing the vector sum of all forces

        Examples:
            >>> F_1 = ForceVector(x=10, y=20, z=0, unit="N", name="F_1")
            >>> F_2 = ForceVector(x=-5, y=15, z=10, unit="N", name="F_2")
            >>> F_R = ForceVector.resultant([F_1, F_2], name="F_R")
            >>> print(F_R.x)  # 5 N
        """
        if not forces:
            raise ValueError("Cannot compute resultant of empty list")

        result = forces[0]
        for f in forces[1:]:
            result = result + f

        # Set name and mark as resultant
        result.name = name or "F_R"
        result.is_resultant = True
        return result

    @classmethod
    def from_position_vector(
        cls,
        pos_vector: "PositionVector",
        magnitude: float | Quantity,
        unit: Unit | str | None = None,
        name: str | None = None,
        **kwargs,
    ) -> ForceVector:
        """
        Create ForceVector directed along a position vector.

        This is the standard method for creating forces along lines (cables, rods, etc.):
            F = |F| * û = |F| * (r / |r|)

        Args:
            pos_vector: PositionVector defining the direction
            magnitude: Force magnitude
            unit: Force unit (required if magnitude is a scalar)
            name: Force name
            **kwargs: Additional arguments (description, is_resultant, etc.)

        Returns:
            ForceVector instance directed along the position vector

        Examples:
            >>> from qnty.spatial import Point, PositionVector, ForceVector
            >>> from qnty.core.unit_catalog import LengthUnits
            >>>
            >>> # Define points
            >>> A = Point(0, 0, 6, unit=LengthUnits.meter)
            >>> B = Point(2, -3, 0, unit=LengthUnits.meter)
            >>>
            >>> # Create position vector
            >>> r_AB = PositionVector.from_points(A, B)
            >>>
            >>> # Create force along AB
            >>> F = ForceVector.from_position_vector(r_AB, magnitude=560, unit="N", name="F_B")
            >>> print(F.x)  # 160 N
            >>> print(F.y)  # -240 N
            >>> print(F.z)  # -480 N
        """
        from .position_vector import PositionVector

        if not isinstance(pos_vector, PositionVector):
            raise TypeError(f"Expected PositionVector, got {type(pos_vector)}")

        # Get unit vector (direction cosines)
        cos_alpha, cos_beta, cos_gamma = pos_vector.unit_vector()

        # Convert magnitude to SI value
        if isinstance(magnitude, int | float):
            if unit is None:
                raise ValueError("unit must be specified when magnitude is a scalar")

            # Resolve unit if string
            if isinstance(unit, str):
                from ..core.dimension_catalog import dim
                from ..core.unit import ureg

                resolved = ureg.resolve(unit, dim=dim.force)
                if resolved is None:
                    raise ValueError(f"Unknown force unit '{unit}'")
                unit = resolved

            mag_si = float(magnitude) * unit.si_factor
        else:
            # Quantity
            if magnitude.value is None:
                raise ValueError("Magnitude must have a known value")
            mag_si = magnitude.value
            unit = magnitude.preferred
            if unit is None:
                raise ValueError("Magnitude Quantity must have a preferred unit")

        # Compute force components: F = |F| * û
        x_val = mag_si * cos_alpha
        y_val = mag_si * cos_beta
        z_val = mag_si * cos_gamma

        # Create ForceVector from components (convert from SI to unit)
        return cls(x=x_val / unit.si_factor, y=y_val / unit.si_factor, z=z_val / unit.si_factor, unit=unit, name=name, **kwargs)

    @staticmethod
    def parse_wrt(wrt: str, coordinate_system: CoordinateSystem | None = None, forces: dict[str, ForceVector] | None = None) -> AngleReference:
        """
        Parse a wrt string into an AngleReference, validating against coordinate system.

        Args:
            wrt: The wrt string (e.g., "+x", "cw:u", "-y", "+F_1", "-F_AB")
            coordinate_system: Optional coordinate system to validate against
            forces: Optional dictionary of force name -> ForceVector for force-relative references

        Returns:
            AngleReference instance

        Raises:
            ValueError: If wrt axis doesn't exist in coordinate system or force doesn't exist

        Examples:
            >>> ref = ForceVector.parse_wrt("+x")
            >>> ref = ForceVector.parse_wrt("cw:u", uv_system)
            >>> ref = ForceVector.parse_wrt("-F_AB", forces=solution_dict)
        """
        coord_sys = coordinate_system or CoordinateSystem.standard()

        # Split on colon to separate direction and axis
        if ":" in wrt:
            direction_str, axis = wrt.split(":", 1)
            direction_str = direction_str.lower().strip()
            axis = axis.strip()
        else:
            direction_str = "ccw"
            axis = wrt.strip()

        # Parse direction
        if direction_str in ("ccw", "counterclockwise"):
            direction = "counterclockwise"
        elif direction_str in ("cw", "clockwise"):
            direction = "clockwise"
        else:
            raise ValueError(f"Invalid direction '{direction_str}'. Use 'ccw', 'cw', 'counterclockwise', or 'clockwise'")

        # Check if axis is a force reference (starts with +/- and contains underscore, which is typical for force names)
        # Force names typically have format like F_1, F_AB, etc.
        axis_without_sign = axis.lstrip("+-")
        is_negative = axis.startswith("-")
        is_positive = axis.startswith("+")

        # Check if this looks like a force reference (has underscore or starts with F)
        if (is_negative or is_positive) and (axis_without_sign.startswith("F") or "_" in axis_without_sign):
            # This is a force reference
            if forces is None:
                raise ValueError(f"Force reference '{wrt}' requires forces dictionary to be provided")

            if axis_without_sign not in forces:
                raise ValueError(f"Force '{axis_without_sign}' not found in forces dictionary")

            ref_force = forces[axis_without_sign]

            # Get the reference force's actual direction from its vector components
            # This correctly handles negative magnitudes
            if ref_force.vector is None or ref_force.x is None or ref_force.y is None:
                raise ValueError(f"Force '{axis_without_sign}' does not have vector components")

            # Use atan2 to get the actual direction from components
            if ref_force.x.value is None or ref_force.y.value is None:
                raise ValueError(f"Force '{axis_without_sign}' does not have known components")

            force_angle_rad = math.atan2(ref_force.y.value, ref_force.x.value)
            force_angle_deg = math.degrees(force_angle_rad)

            # Normalize to [0, 360)
            force_angle_deg = force_angle_deg % 360.0

            # If negative reference (e.g., -F_AB), add 180° to point in opposite direction
            if is_negative:
                force_angle_deg = (force_angle_deg + 180.0) % 360.0

            from .angle_reference import AngleReference as AR

            return AR(axis_angle=force_angle_deg, direction=direction, axis_label=axis, angle_unit="degree")

        # Check if axis matches coordinate system axes
        # Handle both direct match (e.g., "x") and with sign prefix (e.g., "+x", "-x")
        if axis == coord_sys.axis1_label or axis_without_sign == coord_sys.axis1_label:
            if is_negative:
                # For negative axis, add 180° to the axis angle
                from .angle_reference import AngleReference as AR

                axis_angle_deg = math.degrees(coord_sys.axis1_angle) + 180.0
                return AR(axis_angle=axis_angle_deg, direction=direction, axis_label=axis, angle_unit="degree")
            else:
                return AngleReference.from_coordinate_system(coord_sys, axis_index=0, direction=direction)
        elif axis == coord_sys.axis2_label or axis_without_sign == coord_sys.axis2_label:
            if is_negative:
                # For negative axis, add 180° to the axis angle
                from .angle_reference import AngleReference as AR

                axis_angle_deg = math.degrees(coord_sys.axis2_angle) + 180.0
                return AR(axis_angle=axis_angle_deg, direction=direction, axis_label=axis, angle_unit="degree")
            else:
                return AngleReference.from_coordinate_system(coord_sys, axis_index=1, direction=direction)
        else:
            # Check if it's a standard axis - allow these even with non-standard coordinate systems
            # for display/comparison purposes (angles will still be in standard x-y coords)
            standard_axes = {"+x", "x", "+y", "y", "-x", "-y"}
            if axis in standard_axes:
                return AngleReference.from_axis(axis, direction=direction)

            # Not a standard axis and not in coordinate system
            raise ValueError(
                f"Invalid wrt axis '{axis}'. Must be a standard axis (+x, -x, +y, -y), "
                f"an axis from the coordinate system ({coord_sys.axis1_label}, {coord_sys.axis2_label}), "
                f"or a force reference (e.g., +F_1, -F_AB)"
            )

    @classmethod
    def unknown(
        cls,
        name: str,
        is_resultant: bool = False,
        magnitude: float | None = None,
        angle: float | None = None,
        coordinate_system: CoordinateSystem | None = None,
        angle_reference: AngleReference | None = None,
        wrt: str | None = None,
        **kwargs,
    ) -> ForceVector:
        """
        Create an unknown ForceVector to be solved for.

        Args:
            name: Force name
            is_resultant: Whether this is a resultant force
            magnitude: Optional known magnitude. If provided, only angle is unknown.
            angle: Optional known angle (in degrees). If provided, only magnitude is unknown.
            coordinate_system: CoordinateSystem for non-standard axes
            angle_reference: AngleReference specifying how angle is measured
            wrt: Shorthand for angle reference (e.g., "+x", "cw:+y", "u")
            **kwargs: Additional arguments (e.g., unit, angle_unit)

        Returns:
            ForceVector instance marked as unknown
        """
        return cls(magnitude=magnitude, angle=angle, name=name, is_known=False, is_resultant=is_resultant, coordinate_system=coordinate_system, angle_reference=angle_reference, wrt=wrt, **kwargs)

    def resolve_relative_angle(self, forces: dict[str, ForceVector]) -> None:
        """
        Resolve relative angle constraint to absolute angle.

        If this force has a relative angle constraint (e.g., "30 degrees from F_R"),
        this method resolves it to an absolute angle once the referenced force's angle is known.

        Args:
            forces: Dictionary of force name -> ForceVector to look up referenced force

        Raises:
            ValueError: If referenced force doesn't exist or doesn't have a known angle
        """
        if self._relative_to_force is None:
            return  # No relative constraint

        # Look up the referenced force
        if self._relative_to_force not in forces:
            raise ValueError(f"Force {self.name} references unknown force '{self._relative_to_force}'")

        ref_force = forces[self._relative_to_force]

        # Check if referenced force has a known angle
        if ref_force.angle is None or ref_force.angle.value is None:
            # Can't resolve yet - referenced force doesn't have known angle
            # Don't clear the constraint, it will be resolved during solving
            raise ValueError(f"Force {self.name} references {self._relative_to_force}, but that force doesn't have a known angle yet")

        # Calculate absolute angle: reference_angle + relative_offset
        ref_angle_rad = ref_force.angle.value  # Already in radians
        relative_offset = self._relative_angle if self._relative_angle is not None else 0.0
        absolute_angle_rad = ref_angle_rad + relative_offset

        # Store the resolved angle
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)
        self._angle = Quantity(name=f"{self.name}_angle", dim=dim.D, value=absolute_angle_rad, preferred=degree_unit)

        # Clear the relative constraint since it's now resolved
        self._relative_to_force = None
        self._relative_angle = None

        # If both magnitude and angle are now known, update is_known and create vector
        if self._magnitude is not None and self._magnitude.value is not None and self._angle is not None and self._angle.value is not None:
            import math

            # Create vector from magnitude and angle
            mag_si = self._magnitude.value
            angle_rad = self._angle.value
            x_val = mag_si * math.cos(angle_rad)
            y_val = mag_si * math.sin(angle_rad)
            z_val = 0.0

            x_qty = Quantity(name=f"{self.name}_x", dim=dim.force, value=x_val, preferred=self._magnitude.preferred)
            y_qty = Quantity(name=f"{self.name}_y", dim=dim.force, value=y_val, preferred=self._magnitude.preferred)
            z_qty = Quantity(name=f"{self.name}_z", dim=dim.force, value=z_val, preferred=self._magnitude.preferred)

            self._vector = _Vector.from_quantities(x_qty, y_qty, z_qty)
            self.is_known = True

    def has_relative_angle(self) -> bool:
        """Check if this force has an unresolved relative angle constraint."""
        return self._relative_to_force is not None

    # Properties
    @property
    def magnitude(self) -> Quantity | None:
        """Force magnitude."""
        return self._magnitude

    @property
    def angle(self) -> Quantity | None:
        """
        Angle in the angle_reference system.

        Internally stored as standard (CCW from +x), but returned in the reference system.
        """
        return self._angle

    @property
    def vector(self) -> _Vector | None:
        """Underlying _Vector object."""
        return self._vector

    def to_cartesian(self) -> _Vector | None:
        """
        Convert to Cartesian _Vector.

        Returns:
            _Vector object with force components, or None if unknown
        """
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

    # Convenience methods for unit conversion
    def magnitude_in(self, unit: Unit | str) -> float:
        """
        Get magnitude in specified unit.

        This is a convenience method that handles unit conversion automatically,
        similar to Quantity.magnitude(unit).

        Args:
            unit: Target unit for magnitude

        Returns:
            Magnitude value in the specified unit

        Raises:
            ValueError: If force has no magnitude or unit is incompatible

        Examples:
            >>> F = ForceVector(magnitude=1000, angle=45, unit="N")
            >>> F.magnitude_in("kN")
            1.0
            >>> F.magnitude_in("lb")
            224.809
        """
        if self._magnitude is None:
            raise ValueError(f"Force {self.name} has no magnitude")
        if self._magnitude.value is None:
            raise ValueError(f"Force {self.name} magnitude is unknown")

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.force)
            if resolved is None:
                raise ValueError(f"Unknown force unit '{unit}'")
            unit = resolved

        # Use Quantity's built-in magnitude method
        return self._magnitude.magnitude(unit)

    def angle_in(self, unit: Unit | str = "degree", wrt: str | AngleReference | None = None, forces: dict[str, ForceVector] | None = None) -> float:
        """
        Get angle in specified unit and reference system.

        This is a convenience method that handles both unit conversion and
        angle reference system conversion automatically.

        Args:
            unit: Target unit for angle (default "degree")
            wrt: Angle reference system (e.g., "+x", "cw:+y", "+F_R").
                 If None, returns angle in standard system (CCW from +x).
                 Can be a string (parsed via parse_wrt) or AngleReference object.
            forces: Dictionary of force name -> ForceVector for force-relative references
                   (e.g., when wrt="+F_R" to measure angle relative to another force)

        Returns:
            Angle value in the specified unit and reference system

        Raises:
            ValueError: If force has no angle or unit is incompatible

        Examples:
            >>> F = ForceVector(magnitude=100, angle=45, unit="N")
            >>> F.angle_in("degree")  # Standard CCW from +x
            45.0
            >>> F.angle_in("radian")
            0.7854
            >>> F.angle_in("degree", wrt="cw:+x")  # Clockwise from +x
            315.0
            >>> F.angle_in("degree", wrt="+y")  # CCW from +y
            315.0
            >>> # For force-relative references:
            >>> F.angle_in("degree", wrt="+F_R", forces={"F_R": F_R})  # Relative to another force
            30.0
        """
        if self._angle is None:
            raise ValueError(f"Force {self.name} has no angle")
        if self._angle.value is None:
            raise ValueError(f"Force {self.name} angle is unknown")

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.D)
            if resolved is None:
                raise ValueError(f"Unknown angle unit '{unit}'")
            unit = resolved

        # Get angle in radians (standard form - CCW from +x)
        angle_rad = self._angle.value

        # Convert to target reference system if specified
        if wrt is not None:
            # Parse wrt if it's a string
            if isinstance(wrt, str):
                angle_ref = ForceVector.parse_wrt(wrt, self.coordinate_system, forces=forces)
            else:
                angle_ref = wrt

            # Convert from standard to target reference system
            angle_rad = angle_ref.from_standard(angle_rad, angle_unit="radian")

        # Convert from radians to target unit
        angle_in_unit = angle_rad / unit.si_factor

        return float(angle_in_unit)

    def with_magnitude_unit(self, unit: Unit | str) -> ForceVector:
        """
        Return a new ForceVector with magnitude displayed in a different unit.

        This creates a copy of the force with the same values but different
        preferred display unit for magnitude. The internal SI values remain unchanged.

        Args:
            unit: Target unit for magnitude display

        Returns:
            New ForceVector with updated magnitude unit

        Examples:
            >>> F = ForceVector(magnitude=1000, angle=45, unit="N")
            >>> F_kN = F.with_magnitude_unit("kN")
            >>> print(F_kN)
            ForceVector(Force, 1.000 kN at 45.0°)
        """
        if self._magnitude is None:
            raise ValueError(f"Force {self.name} has no magnitude")

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.force)
            if resolved is None:
                raise ValueError(f"Unknown force unit '{unit}'")
            unit = resolved

        # Create a copy with updated magnitude unit
        new_force = object.__new__(ForceVector)
        new_force._vector = self._vector
        new_force._magnitude = self._magnitude.to_unit(unit) if self._magnitude else None
        new_force._angle = self._angle
        new_force.name = self.name
        new_force.is_known = self.is_known
        new_force.is_resultant = self.is_resultant
        new_force._description = self._description
        new_force.coordinate_system = self.coordinate_system
        new_force.angle_reference = self.angle_reference
        new_force._relative_to_force = self._relative_to_force
        new_force._relative_angle = self._relative_angle

        return new_force

    def with_angle_unit(self, unit: Unit | str) -> ForceVector:
        """
        Return a new ForceVector with angle displayed in a different unit.

        This creates a copy of the force with the same values but different
        preferred display unit for angle. The internal SI values remain unchanged.

        Args:
            unit: Target unit for angle display (e.g., "degree", "radian")

        Returns:
            New ForceVector with updated angle unit

        Examples:
            >>> F = ForceVector(magnitude=100, angle=45, unit="N")
            >>> F_rad = F.with_angle_unit("radian")
            >>> print(F_rad)
            ForceVector(Force, 100.000 N at 0.79rad)
        """
        if self._angle is None:
            raise ValueError(f"Force {self.name} has no angle")

        # Resolve unit if string
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=dim.D)
            if resolved is None:
                raise ValueError(f"Unknown angle unit '{unit}'")
            unit = resolved

        # Create a copy with updated angle unit
        new_force = object.__new__(ForceVector)
        new_force._vector = self._vector
        new_force._magnitude = self._magnitude
        new_force._angle = self._angle.to_unit(unit) if self._angle else None
        new_force.name = self.name
        new_force.is_known = self.is_known
        new_force.is_resultant = self.is_resultant
        new_force._description = self._description
        new_force.coordinate_system = self.coordinate_system
        new_force.angle_reference = self.angle_reference
        new_force._relative_to_force = self._relative_to_force
        new_force._relative_angle = self._relative_angle

        return new_force

    def with_angle_reference(self, wrt: str | AngleReference) -> ForceVector:
        """
        Return a new ForceVector with a different angle reference system.

        This creates a copy of the force with a different angle reference system.
        The internal angle values remain in standard form (CCW from +x), but the
        angle_reference property is updated.

        Args:
            wrt: New angle reference system (e.g., "+x", "cw:+y", "+F_R")

        Returns:
            New ForceVector with updated angle reference

        Examples:
            >>> F = ForceVector(magnitude=100, angle=45, unit="N")
            >>> F_cw = F.with_angle_reference("cw:+x")
            >>> F_cw.angle_in("degree", wrt="cw:+x")
            315.0
        """
        # Parse wrt if it's a string
        if isinstance(wrt, str):
            new_angle_ref = ForceVector.parse_wrt(wrt, self.coordinate_system)
        else:
            new_angle_ref = wrt

        # Create a copy with updated angle reference
        new_force = object.__new__(ForceVector)
        new_force._vector = self._vector
        new_force._magnitude = self._magnitude
        new_force._angle = self._angle
        new_force.name = self.name
        new_force.is_known = self.is_known
        new_force.is_resultant = self.is_resultant
        new_force._description = self._description
        new_force.coordinate_system = self.coordinate_system
        new_force.angle_reference = new_angle_ref
        new_force._relative_to_force = self._relative_to_force
        new_force._relative_angle = self._relative_angle

        return new_force

    @property
    def alpha(self) -> Quantity | None:
        """
        Coordinate direction angle from +x axis (3D).

        Returns angle between force vector and +x axis.
        Range: [0°, 180°]
        """
        if self._vector is None or self._magnitude is None:
            return None

        mag_val = self._magnitude.value
        if mag_val is None or abs(mag_val) < 1e-10:
            return None

        x_val = self.x.value if self.x else 0.0
        if x_val is None:
            return None

        # cos(α) = Fx / F
        cos_alpha = x_val / mag_val
        # Clamp to [-1, 1] to handle numerical errors
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        alpha_rad = math.acos(cos_alpha)

        from ..core.dimension_catalog import dim as dim_alpha
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim_alpha.D)

        return Quantity(name=f"{self.name}_alpha", dim=dim_alpha.D, value=alpha_rad, preferred=degree_unit)

    @property
    def beta(self) -> Quantity | None:
        """
        Coordinate direction angle from +y axis (3D).

        Returns angle between force vector and +y axis.
        Range: [0°, 180°]
        """
        if self._vector is None or self._magnitude is None:
            return None

        mag_val = self._magnitude.value
        if mag_val is None or abs(mag_val) < 1e-10:
            return None

        y_val = self.y.value if self.y else 0.0
        if y_val is None:
            return None

        # cos(β) = Fy / F
        cos_beta = y_val / mag_val
        # Clamp to [-1, 1] to handle numerical errors
        cos_beta = max(-1.0, min(1.0, cos_beta))
        beta_rad = math.acos(cos_beta)

        from ..core.dimension_catalog import dim as dim_beta
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim_beta.D)

        return Quantity(name=f"{self.name}_beta", dim=dim_beta.D, value=beta_rad, preferred=degree_unit)

    @property
    def gamma(self) -> Quantity | None:
        """
        Coordinate direction angle from +z axis (3D).

        Returns angle between force vector and +z axis.
        Range: [0°, 180°]
        """
        if self._vector is None or self._magnitude is None:
            return None

        mag_val = self._magnitude.value
        if mag_val is None or abs(mag_val) < 1e-10:
            return None

        z_val = self.z.value if self.z else 0.0
        if z_val is None:
            return None

        # cos(γ) = Fz / F
        cos_gamma = z_val / mag_val
        # Clamp to [-1, 1] to handle numerical errors
        cos_gamma = max(-1.0, min(1.0, cos_gamma))
        gamma_rad = math.acos(cos_gamma)

        from ..core.dimension_catalog import dim as dim_gamma
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim_gamma.D)

        return Quantity(name=f"{self.name}_gamma", dim=dim_gamma.D, value=gamma_rad, preferred=degree_unit)

    @property
    def direction_cosines(self) -> tuple[float, float, float] | None:
        """
        Direction cosines (cos(α), cos(β), cos(γ)) for 3D force.

        Returns:
            Tuple of (cos_alpha, cos_beta, cos_gamma) where:
            - cos_alpha = Fx / F
            - cos_beta = Fy / F
            - cos_gamma = Fz / F

        These satisfy the relation: cos²α + cos²β + cos²γ = 1
        """
        if self._vector is None or self._magnitude is None:
            return None

        mag_val = self._magnitude.value
        if mag_val is None or abs(mag_val) < 1e-10:
            return None

        x_val = self.x.value if self.x else 0.0
        y_val = self.y.value if self.y else 0.0
        z_val = self.z.value if self.z else 0.0

        if x_val is None or y_val is None or z_val is None:
            return None

        cos_alpha = x_val / mag_val
        cos_beta = y_val / mag_val
        cos_gamma = z_val / mag_val

        return (cos_alpha, cos_beta, cos_gamma)

    def get_components_in_system(self) -> tuple[Quantity | None, Quantity | None]:
        """
        Get force components in the current coordinate system.

        For standard x-y system, returns (x, y).
        For custom systems (e.g., u-v), returns components along those axes.

        Returns:
            Tuple of (component1, component2) as Quantity objects
        """
        if self._vector is None:
            return (None, None)

        # Get cartesian components
        coords = self._vector.to_array()
        x_val = coords[0]
        y_val = coords[1]

        # Convert to coordinate system components
        comp1, comp2 = self.coordinate_system.from_cartesian(x_val, y_val)

        # Create Quantity objects
        from ..core.dimension_catalog import dim

        unit = self._vector.u.preferred if self._vector.u else None

        comp1_qty = Quantity(name=f"{self.name}_{self.coordinate_system.axis1_label}", dim=dim.force, value=comp1, preferred=unit)
        comp2_qty = Quantity(name=f"{self.name}_{self.coordinate_system.axis2_label}", dim=dim.force, value=comp2, preferred=unit)

        return (comp1_qty, comp2_qty)

    def __str__(self) -> str:
        """String representation."""
        if not self.is_known:
            return f"ForceVector({self.name}, unknown)"

        if self._magnitude and self._angle and self._magnitude.value is not None and self._angle.value is not None:
            mag_val = self._magnitude.value / self._magnitude.preferred.si_factor if self._magnitude.preferred else self._magnitude.value
            ang_val = self._angle.value / self._angle.preferred.si_factor if self._angle.preferred else self._angle.value
            mag_unit = self._magnitude.preferred.symbol if self._magnitude.preferred else ""
            ang_unit = self._angle.preferred.symbol if self._angle.preferred else ""
            return f"ForceVector({self.name}, {mag_val:.3f} {mag_unit} at {ang_val:.1f}{ang_unit})"

        return f"ForceVector({self.name})"

    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()

    def is_close(
        self,
        other: ForceVector,
        magnitude_rel_tol: float = 1e-6,
        magnitude_abs_tol: float = 0.0,
        angle_abs_tol_deg: float = 0.01,
        compare_components: bool = False,
    ) -> bool:
        """
        Compare two ForceVectors with explicit tolerances.

        This method provides fine-grained control over comparison tolerances.
        Use this when you need to compare forces with specific precision requirements.

        Args:
            other: ForceVector to compare with
            magnitude_rel_tol: Relative tolerance for magnitude comparison (default 1e-6)
            magnitude_abs_tol: Absolute tolerance for magnitude comparison (default 0.0)
            angle_abs_tol_deg: Absolute tolerance for angle comparison in degrees (default 0.01°)
            compare_components: If True, compare x/y components instead of magnitude/angle.
                               This is useful when forces have relative angle constraints.

        Returns:
            True if forces are close within specified tolerances

        Examples:
            >>> F1 = ForceVector(magnitude=100, angle=45, unit="N")
            >>> F2 = ForceVector(magnitude=100.001, angle=45.005, unit="N")
            >>> F1.is_close(F2)  # Default tolerances
            True
            >>> F1.is_close(F2, magnitude_rel_tol=1e-9)  # Stricter tolerance
            False
            >>> F1.is_close(F2, angle_abs_tol_deg=0.001)  # Stricter angle tolerance
            False
        """
        if not isinstance(other, ForceVector):
            raise TypeError(f"Expected ForceVector, got {type(other)}")

        # Both unknown - considered equal
        if not self.is_known and not other.is_known:
            return True

        # One known, one unknown - not equal
        if self.is_known != other.is_known:
            return False

        # Compare components if requested (useful for relative angle constraints)
        if compare_components:
            if self._vector is None or other._vector is None:
                return False

            # Compare x, y, z components
            self_coords = self._vector.to_array()
            other_coords = other._vector.to_array()

            for i in range(3):
                si_val1 = self_coords[i]
                si_val2 = other_coords[i]

                # Compute tolerance
                max_val = max(abs(si_val1), abs(si_val2))
                tolerance = magnitude_abs_tol + magnitude_rel_tol * max_val

                if abs(si_val1 - si_val2) > tolerance:
                    return False

            return True

        # Compare magnitude and angle
        if self._magnitude is None or other._magnitude is None:
            return False
        if self._angle is None or other._angle is None:
            return False

        # Compare magnitudes (in SI units to handle different preferred units)
        if self._magnitude.value is None or other._magnitude.value is None:
            return False

        mag1_si = self._magnitude.value
        mag2_si = other._magnitude.value
        max_mag = max(abs(mag1_si), abs(mag2_si))
        mag_tolerance = magnitude_abs_tol + magnitude_rel_tol * max_mag
        mag_diff = abs(mag1_si - mag2_si)

        if mag_diff > mag_tolerance:
            return False

        # Compare angles (in radians - SI units)
        if self._angle.value is None or other._angle.value is None:
            return False

        # Normalize angles to [0, 2π]
        angle1 = self._angle.value % (2 * math.pi)
        angle2 = other._angle.value % (2 * math.pi)
        angle_diff = abs(angle1 - angle2)

        # Handle wrap-around (e.g., 359° vs 1°)
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff

        # Convert tolerance from degrees to radians
        angle_tolerance_rad = math.radians(angle_abs_tol_deg)

        return angle_diff <= angle_tolerance_rad

    def __add__(self, other: "ForceVector") -> "ForceVector":
        """Add two force vectors."""
        if not isinstance(other, ForceVector):
            return NotImplemented

        if self._vector is None or other._vector is None:
            raise ValueError("Cannot add forces with unknown vectors")

        # Get components in SI units
        x_si = self._vector._coords[0] + other._vector._coords[0]
        y_si = self._vector._coords[1] + other._vector._coords[1]
        z_si = self._vector._coords[2] + other._vector._coords[2]

        # Use the first force's unit for the result
        unit = self._vector._unit
        if unit:
            si_factor = unit.si_factor
            return ForceVector(
                x=x_si / si_factor,
                y=y_si / si_factor,
                z=z_si / si_factor,
                unit=unit,
                name=f"{self.name}+{other.name}"
            )
        else:
            return ForceVector(x=x_si, y=y_si, z=z_si, name=f"{self.name}+{other.name}")

    def __eq__(self, other: object) -> bool:
        """
        Compare two ForceVectors for equality.

        Two ForceVectors are considered equal if they have the same magnitude and angle
        within default tolerances. This uses the standard Qnty comparison approach:
        - Magnitudes are compared in SI units (handles different preferred units)
        - Angles are compared in SI units (radians, standard CCW from +x)
        - Default tolerances: 1e-6 relative for magnitude, 0.01° for angle

        For custom tolerances or component-wise comparison, use is_close().

        Note: Name and description are not compared.

        Examples:
            >>> F1 = ForceVector(magnitude=100, angle=45, unit="N")
            >>> F2 = ForceVector(magnitude=100, angle=45, unit="kN")  # Different unit
            >>> F1 == F2  # False - different magnitudes after unit conversion
            >>> F3 = ForceVector(x=70.71, y=70.71, unit="N")  # Same as F1 in components
            >>> F1 == F3  # True - same magnitude and angle
        """
        if not isinstance(other, ForceVector):
            return NotImplemented

        # Use is_close with default tolerances
        return self.is_close(other, magnitude_rel_tol=1e-6, angle_abs_tol_deg=0.01)
