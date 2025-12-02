"""
Angle finder equation class with dynamic solution step generation.

This module provides utilities for computing angles between vectors
and generating solution steps for the report.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SolutionStepBuilder, format_angle

if TYPE_CHECKING:
    from ..core.quantity import Quantity
    from ..linalg.vector2 import Vector


def get_absolute_angle(vec: Vector) -> Quantity:
    """
    Get the absolute angle from the coordinate system's primary axis.

    The absolute angle is computed as:
        absolute_angle = axis_angle(wrt) + vector.angle

    where axis_angle(wrt) is the angle of the reference axis in the coordinate system.

    Args:
        vec: Vector with angle, wrt, and coordinate_system attributes

    Returns:
        Absolute angle as a Quantity
    """
    # Get the angle of the reference axis from the coordinate system
    axis_angle = vec.coordinate_system.get_axis_angle(vec.wrt)

    # Add the vector's angle to get absolute angle
    return axis_angle + vec.angle


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

        # Get the numeric value and take absolute value
        # Create result as absolute difference
        diff_value = angle_diff.magnitude()
        result = Q(abs(diff_value), "degree")
        result.name = self.target

        # Get display values for the solution step
        vec1_name = self.vec1.name or 'V_1'
        vec2_name = self.vec2.name or 'V_2'
        vec1_ref = self.vec1.wrt
        vec2_ref = self.vec2.wrt

        vec1_ref_display = vec1_ref.lstrip('+') if vec1_ref.startswith('+') else vec1_ref
        vec2_ref_display = vec2_ref.lstrip('+') if vec2_ref.startswith('+') else vec2_ref

        # Format angles for display (convert to degrees for readability)
        vec1_angle_display = self.vec1.angle.as_unit.degree.magnitude()
        vec2_angle_display = self.vec2.angle.as_unit.degree.magnitude()
        result_display = result.magnitude()

        substitution = (
            f"\\angle(\\vec{{{vec1_name}}}, \\vec{{{vec2_name}}}) &= "
            f"|\\angle(\\vec{{{vec1_ref_display}}}, \\vec{{{vec1_name}}}) - "
            f"\\angle(\\vec{{{vec2_ref_display}}}, \\vec{{{vec2_name}}})| \\\\\n"
            f"&= |{format_angle(vec1_angle_display)} - {format_angle(vec2_angle_display)}| \\\\\n"
            f"&= {format_angle(result_display)} \\\\"
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
    Calculate a final angle as the sum of two angles.
    Takes angle Quantities as input and returns an angle Quantity.
    """

    def __init__(
        self,
        target: str,
        base_angle: Quantity,
        offset_angle: Quantity,
        result_ref: str = "+x",
        description: str = "",
    ):
        """
        Initialize angle sum calculation.

        Args:
            target: Name of the final angle (e.g., "∠(x,F_R) with respect to +x")
            base_angle: Base angle as a Quantity
            offset_angle: Offset angle as a Quantity
            result_ref: Reference axis for result (e.g., "+x")
            description: Description for the step
        """
        self.target = target
        self.base_angle = base_angle
        self.offset_angle = offset_angle
        self.result_ref = result_ref
        self.description = description or f"Calculate direction relative to {result_ref} axis"

    def solve(self) -> tuple[Quantity, dict]:
        """
        Calculate the sum of two angles.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        # Use Quantity arithmetic for the sum (handles unit conversion automatically)
        result = self.base_angle + self.offset_angle
        result.name = self.target.split(" with")[0]

        # Extract target name without "with respect to" suffix
        target_name = self.target.split(" with")[0]

        # Get display values in degrees for the solution step
        base_deg = self.base_angle.to_unit.degree.magnitude()
        offset_deg = self.offset_angle.to_unit.degree.magnitude()
        result_deg = result.to_unit.degree.magnitude()

        # Format substitution with proper LaTeX notation
        substitution = (
            f"{target_name} &= {self.base_angle.name} + {self.offset_angle.name} \\\\\n"
            f"&= {format_angle(base_deg, precision=1)} + {format_angle(offset_deg, precision=1)} \\\\\n"
            f"&= {format_angle(result_deg, precision=1)} \\\\"
        )

        step = SolutionStepBuilder(
            target=self.target,
            method="Angle Addition",
            description=self.description,
            substitution=substitution,
        )

        return result, step.build()
