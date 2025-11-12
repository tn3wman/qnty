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
from .coordinate_system import CoordinateSystem
from .angle_reference import AngleReference, AngleDirection

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
        vector: Vector | None = None,
        name: str | None = None,
        description: str = "",
        is_known: bool = True,
        is_resultant: bool = False,
        coordinate_system: CoordinateSystem | None = None,
        angle_reference: AngleReference | None = None,
        wrt: str | None = None,
    ):
        """
        Create a ForceVector.

        Args:
            magnitude: Force magnitude (if None, will be calculated from components or marked unknown)
            angle: Angle value in the angle_reference system (default: CCW from +x-axis)
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
                # Use from_value to properly convert to SI units
                mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{self.name}_magnitude")
                mag_qty.preferred = unit  # Preserve preferred unit for display
            else:
                mag_qty = magnitude

            # Convert angle to Quantity if needed
            if isinstance(angle, (int, float)):
                from ..core.dimension_catalog import dim

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

                angle_qty = Quantity(name=f"{self.name}_angle", dim=dim.D, value=angle_standard, preferred=angle_unit)
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
                from ..core.dimension_catalog import dim as dim_cat
                x_qty = Quantity(name=f"{self.name}_x", dim=dim_cat.force, value=x_val, preferred=mag_qty.preferred)
                y_qty = Quantity(name=f"{self.name}_y", dim=dim_cat.force, value=y_val, preferred=mag_qty.preferred)
                z_qty = Quantity(name=f"{self.name}_z", dim=dim_cat.force, value=z_val, preferred=mag_qty.preferred)
                self._vector = Vector.from_quantities(x_qty, y_qty, z_qty)
            else:
                # Unknown force or has relative angle constraint
                self._vector = None
            return

        # Case 2b: Angle known but magnitude unknown (for decomposition problems)
        if magnitude is None and angle is not None:
            # Convert angle to Quantity
            if isinstance(angle, (int, float)):
                from ..core.dimension_catalog import dim as dim_catalog

                # Convert angle from angle_reference system to standard (CCW from +x)
                angle_in_ref_system = float(angle) * angle_unit.si_factor  # Convert to radians
                angle_standard = self.angle_reference.to_standard(angle_in_ref_system, angle_unit="radian")

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
            if isinstance(magnitude, (int, float)):
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
        elif isinstance(value, (int, float)):
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

    @staticmethod
    def parse_wrt(wrt: str, coordinate_system: CoordinateSystem | None = None, forces: dict[str, "ForceVector"] | None = None) -> AngleReference:
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
    def unknown(cls, name: str, is_resultant: bool = False, magnitude: float | None = None, angle: float | None = None, coordinate_system: CoordinateSystem | None = None, angle_reference: AngleReference | None = None, wrt: str | None = None, **kwargs) -> ForceVector:
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

    def resolve_relative_angle(self, forces: dict[str, "ForceVector"]) -> None:
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
            from .vector import Vector

            # Create vector from magnitude and angle
            mag_si = self._magnitude.value
            angle_rad = self._angle.value
            x_val = mag_si * math.cos(angle_rad)
            y_val = mag_si * math.sin(angle_rad)
            z_val = 0.0

            x_qty = Quantity(name=f"{self.name}_x", dim=dim.force, value=x_val, preferred=self._magnitude.preferred)
            y_qty = Quantity(name=f"{self.name}_y", dim=dim.force, value=y_val, preferred=self._magnitude.preferred)
            z_qty = Quantity(name=f"{self.name}_z", dim=dim.force, value=z_val, preferred=self._magnitude.preferred)

            self._vector = Vector.from_quantities(x_qty, y_qty, z_qty)
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
