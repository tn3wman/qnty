"""
Angle finder equation class with dynamic solution step generation.

This module provides utilities for computing angles between vectors
and generating solution steps for the report.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SolutionStepBuilder, format_angle
from ..spatial.angle_reference import AngleDirection

if TYPE_CHECKING:
    from ..coordinates import CoordinateSystem
    from ..core.quantity import Quantity
    from ..linalg.vector2 import Vector, VectorUnknown


def angle_from_ratio(
    u: float,
    v: float,
    axis1_label: str = "x",
    axis2_label: str = "y",
) -> tuple[Quantity, str]:
    """
    Compute angle and reference axis from direction ratios.

    Given direction ratios (u, v), determine the angle measured from the
    dominant axis. This is used for right-triangle style vector definitions
    like 3-4-5 or 5-12-13 triangles.

    The reference axis is chosen as the dominant direction (larger absolute value),
    and the angle is measured from that axis toward the other component.

    Args:
        u: First component ratio (typically x-direction)
        v: Second component ratio (typically y-direction)
        axis1_label: Label for the first axis (default "x")
        axis2_label: Label for the second axis (default "y")

    Returns:
        Tuple of (angle_quantity, wrt_string) where:
        - angle_quantity: The angle as a Quantity in degrees
        - wrt_string: The reference axis string (e.g., "+x", "-y")

    Raises:
        ValueError: If both ratios are zero

    Examples:
        >>> angle_from_ratio(5, 12)  # 5-12-13 triangle
        (Quantity(67.38°), '+x')  # ~67.38° from +x axis
        >>> angle_from_ratio(-3, 4)  # Pointing in -x, +y quadrant
        (Quantity(53.13°), '-x')  # ~53.13° from -x axis toward +y
    """
    import math

    from ..core.quantity import Q

    if u == 0 and v == 0:
        raise ValueError("Direction ratios cannot both be zero")

    ru, rv = float(u), float(v)
    abs_u, abs_v = abs(ru), abs(rv)

    if abs_u >= abs_v:
        # Dominant direction is along u (first axis)
        wrt = f"+{axis1_label}" if ru >= 0 else f"-{axis1_label}"
        if ru >= 0:
            # Reference is +axis1, positive angle goes toward +axis2
            angle_rad = math.atan2(rv, abs_u)
        else:
            # Reference is -axis1, positive angle goes toward -axis2
            angle_rad = -math.atan2(rv, abs_u)
    else:
        # Dominant direction is along v (second axis)
        wrt = f"+{axis2_label}" if rv >= 0 else f"-{axis2_label}"
        if rv >= 0:
            # Reference is +axis2, positive angle goes toward -axis1 (CCW)
            angle_rad = -math.atan2(ru, abs_v)
        else:
            # Reference is -axis2, positive angle goes toward +axis1
            angle_rad = math.atan2(ru, abs_v)

    return Q(math.degrees(angle_rad), "degree"), wrt


def angles_are_equivalent(angle1: Quantity, angle2: Quantity, rtol: float = 0.01) -> bool:
    """
    Check if two angles are equivalent within tolerance.

    Two angles are equivalent if they differ by a multiple of 360° (2π radians).
    For example, 352.9° and -7.1° are equivalent (352.9 - 360 = -7.1).

    Args:
        angle1: First angle as a Quantity
        angle2: Second angle as a Quantity
        rtol: Relative tolerance (default 1%)

    Returns:
        True if the angles are equivalent within tolerance
    """
    from ..geometry.triangle import _get_angle_constants

    _, _, full_rotation = _get_angle_constants()

    # Direct comparison
    if angle1.is_close(angle2, rtol=rtol):
        return True

    # Check if (angle1 + 360°) is close to angle2
    if (angle1 + full_rotation).is_close(angle2, rtol=rtol):
        return True

    # Check if (angle2 + 360°) is close to angle1
    if (angle2 + full_rotation).is_close(angle1, rtol=rtol):
        return True

    return False


def get_absolute_angle(vec: Vector | VectorUnknown) -> Quantity:
    """
    Get the absolute angle from the coordinate system's primary axis.

    The absolute angle is computed as:
        absolute_angle = reference_angle + vector.angle

    where reference_angle is either:
        - axis_angle(wrt) if wrt is an axis string (e.g., "+x", "-y")
        - get_absolute_angle(wrt) if wrt is another Vector (recursive)

    Args:
        vec: Vector with angle, wrt, and coordinate_system attributes

    Returns:
        Absolute angle as a Quantity

    Raises:
        ValueError: If the vector's angle is unknown (ellipsis)
    """
    from ..linalg.vector2 import Vector as VectorClass

    # Check that the angle is known (not ellipsis)
    angle = vec.angle
    if angle is ...:
        raise ValueError("Cannot compute absolute angle for vector with unknown angle")

    # Get the reference angle based on wrt type
    if isinstance(vec.wrt, VectorClass):
        # wrt is a Vector reference - recursively get its absolute angle
        reference_angle = get_absolute_angle(vec.wrt)
    else:
        # wrt is an axis string - get the angle of that axis from the coordinate system
        reference_angle = vec.coordinate_system.get_axis_angle(vec.wrt)

    # Add the vector's angle to the reference to get absolute angle
    return reference_angle + angle


def get_relative_angle(
    absolute_angle: Quantity,
    wrt: str | "Vector",
    coordinate_system: CoordinateSystem,
    angle_dir: AngleDirection = AngleDirection.COUNTERCLOCKWISE,
) -> Quantity:
    """
    Convert an absolute angle to a relative angle from a reference.

    This is the inverse of get_absolute_angle. Given an absolute angle
    (measured CCW from the coordinate system's primary axis), compute
    the relative angle from the specified reference.

    Sign convention:
        - Counterclockwise (CCW) angles are positive
        - Clockwise (CW) angles are negative

    When angle_dir=CW, the measurement is taken going clockwise from the
    reference axis, but expressed with the standard sign convention
    (CW = negative).

    The result is normalized to the range [0°, 360°).

    Args:
        absolute_angle: The absolute angle as a Quantity
        wrt: The reference - either an axis string (e.g., "+x", "-y")
            or a Vector (for angles measured relative to another vector)
        coordinate_system: The coordinate system defining axis angles
        angle_dir: Direction for measuring the angle (CCW or CW).
            Default: COUNTERCLOCKWISE

    Returns:
        Relative angle as a Quantity

    Example:
        >>> # Vector at 352.9° absolute, relative to +x axis (0°)
        >>> # Result: 352.9° - 0° = 352.9° (already in [0°, 360°))
    """
    from ..geometry.triangle import _get_angle_constants
    from ..linalg.vector2 import Vector as VectorClass

    zero, half_rotation, full_rotation = _get_angle_constants()

    # Get the reference angle based on wrt type
    if isinstance(wrt, VectorClass):
        # wrt is a Vector reference - get its absolute angle
        reference_angle = get_absolute_angle(wrt)
    else:
        # wrt is an axis string - get the angle of that axis from the coordinate system
        reference_angle = coordinate_system.get_axis_angle(wrt)

    # Compute CCW angle from reference to vector
    relative_angle = absolute_angle - reference_angle

    # Normalize to range [0, 360) degrees first
    while relative_angle >= full_rotation:
        relative_angle = relative_angle - full_rotation
    while relative_angle < zero:
        relative_angle = relative_angle + full_rotation

    # Apply angle_dir preference:
    # - CCW: keep in [0, 360) range (positive angles go counter-clockwise)
    # - CW: convert to (-360, 0] range for angles > 180° (express as negative
    #       clockwise angle), or keep small positive angles as-is if closer to 0
    if angle_dir == AngleDirection.CLOCKWISE:
        # For clockwise preference, express angles > 180° as negative
        # This makes 358.8° become -1.2° (1.2° clockwise from reference)
        if relative_angle > half_rotation:
            relative_angle = relative_angle - full_rotation

    return relative_angle


class AngleBetween:
    """
    Calculate the angle between two vectors given their directions.
    Takes vectors as input and returns an angle Quantity.
    """

    def __init__(
        self,
        target: str,
        vec1: Vector,
        vec2: Vector,
        description: str = "",
    ):
        """
        Initialize angle calculation.

        Args:
            target: Name of the angle being calculated (e.g., "∠(F_1,F_2)")
            vec1: First vector
            vec2: Second vector
            description: Description for the step
        """
        self.target = target
        self.vec1 = vec1
        self.vec2 = vec2
        self.description = description or "Calculate the angle between vectors"

    def solve(self) -> tuple[Quantity, dict]:
        """
        Calculate the triangle angle between two vectors for parallelogram law.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        from ..core import Q

        # Get absolute angles using coordinate system
        vec1_abs_angle = get_absolute_angle(self.vec1)
        vec2_abs_angle = get_absolute_angle(self.vec2)

        # Compute angle between as difference (using Quantity arithmetic)
        angle_diff = vec1_abs_angle - vec2_abs_angle

        # Take absolute value using Quantity comparison
        from ..geometry.triangle import _get_angle_constants

        zero, _, _ = _get_angle_constants()
        if angle_diff < zero:
            angle_diff = zero - angle_diff

        result = angle_diff.to_unit.degree
        result.name = self.target

        # Get display values for the solution step
        vec1_name = self.vec1.name or "V_1"
        vec2_name = self.vec2.name or "V_2"
        vec1_ref = self.vec1.wrt
        vec2_ref = self.vec2.wrt

        # Handle wrt being either a string or a Vector
        from ..linalg.vector2 import Vector as VectorClass

        if isinstance(vec1_ref, VectorClass):
            vec1_ref_display = vec1_ref.name or "ref"
        else:
            vec1_ref_display = vec1_ref.lstrip("+") if vec1_ref.startswith("+") else vec1_ref

        if isinstance(vec2_ref, VectorClass):
            vec2_ref_display = vec2_ref.name or "ref"
        else:
            vec2_ref_display = vec2_ref.lstrip("+") if vec2_ref.startswith("+") else vec2_ref

        # Format angles for display (convert to degrees for readability)
        vec1_angle_display = self.vec1.angle.to_unit.degree
        vec2_angle_display = self.vec2.angle.to_unit.degree

        substitution = (
            f"\\angle(\\vec{{{vec1_name}}}, \\vec{{{vec2_name}}}) &= "
            f"|\\angle(\\vec{{{vec1_ref_display}}}, \\vec{{{vec1_name}}}) - "
            f"\\angle(\\vec{{{vec2_ref_display}}}, \\vec{{{vec2_name}}})| \\\\\n"
            f"&= |{format_angle(vec1_angle_display, precision=1)} - {format_angle(vec2_angle_display, precision=1)}| \\\\\n"
            f"&= {format_angle(result, precision=1)} \\\\"
        )

        step = SolutionStepBuilder(
            target=self.target,
            method="Angle Difference",
            description=self.description,
            substitution=substitution,
        )

        return result, step.build()


class AngleSum:
    """
    Calculate a final angle as the sum or difference of two angles.
    Takes angle Quantities as input and returns an angle Quantity.

    The class handles LaTeX formatting internally - callers should pass
    vector names and the class will generate proper LaTeX notation.
    """

    def __init__(
        self,
        base_angle: Quantity,
        offset_angle: Quantity,
        result_vector_name: str,
        base_vector_name: str,
        offset_vector_1: str,
        offset_vector_2: str,
        result_ref: str = "+x",
        description: str = "",
        operation: str = "+",
        angle_dir: AngleDirection = AngleDirection.COUNTERCLOCKWISE,
    ):
        """
        Initialize angle sum/difference calculation.

        Args:
            base_angle: Base angle as a Quantity (e.g., angle from x-axis to F_R)
            offset_angle: Offset angle as a Quantity (e.g., angle from F_R to F_1)
            result_vector_name: Name of the result vector (e.g., "F_1")
            base_vector_name: Name of the base vector (e.g., "F_R")
            offset_vector_1: First vector of the offset angle (e.g., "F_R")
            offset_vector_2: Second vector of the offset angle (e.g., "F_1")
            result_ref: Reference axis for result (e.g., "+x")
            description: Description for the step
            operation: "+" for addition, "-" for subtraction
            angle_dir: Direction for measuring the result angle (CCW or CW).
                When CW, angles > 180° are expressed as negative.
        """
        self.base_angle = base_angle
        self.offset_angle = offset_angle
        self.result_vector_name = result_vector_name
        self.base_vector_name = base_vector_name
        self.offset_vector_1 = offset_vector_1
        self.offset_vector_2 = offset_vector_2
        self.result_ref = result_ref
        self.operation = operation
        self.angle_dir = angle_dir

        # Handle result_ref being either a string or a Vector
        from ..linalg.vector2 import Vector as VectorClass

        if isinstance(result_ref, VectorClass):
            # result_ref is a Vector - use its name for display
            ref_display = result_ref.name or "ref"
            ref_axis = ref_display
        else:
            # result_ref is a string axis like "+x" or "-y"
            ref_display = result_ref
            ref_axis = result_ref.lstrip("+-")

        self.description = description or f"Compute direction relative to {ref_display} axis"

        # Generate LaTeX names
        from .base import angle_notation, latex_name

        result_name = latex_name(result_vector_name)
        base_name = latex_name(base_vector_name)

        # Generate the angle names with LaTeX formatting
        # Use the actual reference axis, not hardcoded "x"
        self.target_name = f"\\angle(\\vec{{{ref_axis}}}, \\vec{{{result_name}}})"
        self.base_angle_name = f"\\angle(\\vec{{{ref_axis}}}, \\vec{{{base_name}}})"
        # Use angle_notation for consistent alphanumeric sorting
        self.offset_angle_name = angle_notation(offset_vector_1, offset_vector_2)
        self.target = f"{self.target_name} with respect to {ref_display}"

    def solve(self) -> tuple[Quantity, dict]:
        """
        Calculate the sum or difference of two angles.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        from ..core import Q

        # Use Quantity arithmetic (handles unit conversion automatically)
        if self.operation == "-":
            result = self.base_angle - self.offset_angle
            op_symbol = "-"
            method = "Angle Subtraction"
        else:
            result = self.base_angle + self.offset_angle
            op_symbol = "+"
            method = "Angle Addition"

        result.name = self.target_name

        # Get display values in degrees for the solution step
        base_deg = self.base_angle.to_unit.degree
        offset_deg = self.offset_angle.to_unit.degree
        intermediate_deg = result.to_unit.degree

        # Get intermediate result value
        intermediate_val = intermediate_deg.magnitude()

        # Build substitution based on angle_dir preference
        base_val = base_deg.magnitude()
        offset_val = offset_deg.magnitude()

        # For clockwise direction preference with small negative results,
        # keep the negative value directly without normalizing through [0, 360)
        if self.angle_dir == AngleDirection.CLOCKWISE and -180 < intermediate_val < 0:
            # Direct negative result - simplest case for CW angles
            # e.g., 45° - 46.2° = -1.2° (no need for 360° + 45° - 46.2° = 358.8° - 360° = -1.2°)
            final_val = intermediate_val
            result_final = Q(final_val, "degree")
            result_final.name = self.target_name
            substitution = (
                f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                f"&= {format_angle(base_deg, precision=1)} {op_symbol} {format_angle(offset_deg, precision=1)} \\\\\n"
                f"&= {format_angle(result_final, precision=1)} \\\\"
            )
        else:
            # Standard normalization logic for other cases
            normalized_val = intermediate_val % 360
            if normalized_val < 0:
                normalized_val += 360

            # Check if normalization to [0, 360) is needed
            needs_normalization = abs(intermediate_val - normalized_val) > 0.01

            # Apply angle_dir preference for final result
            # For clockwise, express angles > 180° as negative
            final_val = normalized_val
            needs_cw_conversion = False
            if self.angle_dir == AngleDirection.CLOCKWISE and normalized_val > 180:
                final_val = normalized_val - 360
                needs_cw_conversion = True

            result_final = Q(final_val, "degree")
            result_final.name = self.target_name

            if needs_normalization and intermediate_val < 0:
                # Negative result that needs normalization: show 360° + base - offset
                if needs_cw_conversion:
                    # Also show conversion to CW (negative) angle
                    substitution = (
                        f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                        f"&= 360^{{\\circ}} + {base_val:.1f}^{{\\circ}} {op_symbol} {offset_val:.1f}^{{\\circ}} \\\\\n"
                        f"&= {normalized_val:.1f}^{{\\circ}} \\\\\n"
                        f"&= {normalized_val:.1f}^{{\\circ}} - 360^{{\\circ}} \\\\\n"
                        f"&= {format_angle(result_final, precision=1)} \\\\"
                    )
                else:
                    substitution = (
                        f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                        f"&= 360^{{\\circ}} + {base_val:.1f}^{{\\circ}} {op_symbol} {offset_val:.1f}^{{\\circ}} \\\\\n"
                        f"&= {format_angle(result_final, precision=1)} \\\\"
                    )
            elif needs_normalization:
                # Angle >= 360°: show base + offset - 360°
                if needs_cw_conversion:
                    substitution = (
                        f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                        f"&= {base_val:.1f}^{{\\circ}} {op_symbol} {offset_val:.1f}^{{\\circ}} - 360^{{\\circ}} \\\\\n"
                        f"&= {normalized_val:.1f}^{{\\circ}} \\\\\n"
                        f"&= {normalized_val:.1f}^{{\\circ}} - 360^{{\\circ}} \\\\\n"
                        f"&= {format_angle(result_final, precision=1)} \\\\"
                    )
                else:
                    substitution = (
                        f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                        f"&= {base_val:.1f}^{{\\circ}} {op_symbol} {offset_val:.1f}^{{\\circ}} - 360^{{\\circ}} \\\\\n"
                        f"&= {format_angle(result_final, precision=1)} \\\\"
                    )
            elif needs_cw_conversion:
                # No normalization needed but need CW conversion
                substitution = (
                    f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                    f"&= {format_angle(base_deg, precision=1)} {op_symbol} {format_angle(offset_deg, precision=1)} \\\\\n"
                    f"&= {normalized_val:.1f}^{{\\circ}} \\\\\n"
                    f"&= {normalized_val:.1f}^{{\\circ}} - 360^{{\\circ}} \\\\\n"
                    f"&= {format_angle(result_final, precision=1)} \\\\"
                )
            else:
                substitution = (
                    f"{self.target_name} &= {self.base_angle_name} {op_symbol} {self.offset_angle_name} \\\\\n"
                    f"&= {format_angle(base_deg, precision=1)} {op_symbol} {format_angle(offset_deg, precision=1)} \\\\\n"
                    f"&= {format_angle(result_final, precision=1)} \\\\"
                )

        step = SolutionStepBuilder(
            target=self.target,
            method=method,
            description=self.description,
            substitution=substitution,
        )

        return result_final, step.build()
