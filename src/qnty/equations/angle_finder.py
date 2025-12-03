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
    from ..linalg.vector2 import Vector, VectorUnknown


def get_absolute_angle(vec: Vector | VectorUnknown) -> Quantity:
    """
    Get the absolute angle from the coordinate system's primary axis.

    The absolute angle is computed as:
        absolute_angle = axis_angle(wrt) + vector.angle

    where axis_angle(wrt) is the angle of the reference axis in the coordinate system.

    Args:
        vec: Vector with angle, wrt, and coordinate_system attributes

    Returns:
        Absolute angle as a Quantity

    Raises:
        ValueError: If the vector's angle is unknown (ellipsis)
    """
    # Check that the angle is known (not ellipsis)
    angle = vec.angle
    if angle is ...:
        raise ValueError("Cannot compute absolute angle for vector with unknown angle")

    # Get the angle of the reference axis from the coordinate system
    axis_angle = vec.coordinate_system.get_axis_angle(vec.wrt)

    # Add the vector's angle to get absolute angle
    return axis_angle + angle


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
        vec1_name = self.vec1.name or "V_1"
        vec2_name = self.vec2.name or "V_2"
        vec1_ref = self.vec1.wrt
        vec2_ref = self.vec2.wrt

        vec1_ref_display = vec1_ref.lstrip("+") if vec1_ref.startswith("+") else vec1_ref
        vec2_ref_display = vec2_ref.lstrip("+") if vec2_ref.startswith("+") else vec2_ref

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
    ):
        """
        Initialize angle sum calculation.

        Args:
            base_angle: Base angle as a Quantity (e.g., angle from x-axis to F_1)
            offset_angle: Offset angle as a Quantity (e.g., angle from F_1 to F_R)
            result_vector_name: Name of the result vector (e.g., "F_R")
            base_vector_name: Name of the base vector (e.g., "F_1")
            offset_vector_1: First vector of the offset angle (e.g., "F_1")
            offset_vector_2: Second vector of the offset angle (e.g., "F_R")
            result_ref: Reference axis for result (e.g., "+x")
            description: Description for the step
        """
        self.base_angle = base_angle
        self.offset_angle = offset_angle
        self.result_vector_name = result_vector_name
        self.base_vector_name = base_vector_name
        self.offset_vector_1 = offset_vector_1
        self.offset_vector_2 = offset_vector_2
        self.result_ref = result_ref
        self.description = description or f"Compute direction relative to {result_ref} axis"

        # Generate LaTeX names
        from .base import latex_name

        result_name = latex_name(result_vector_name)
        base_name = latex_name(base_vector_name)
        off_v1 = latex_name(offset_vector_1)
        off_v2 = latex_name(offset_vector_2)

        # Generate the angle names with LaTeX formatting
        self.target_name = f"\\angle(\\vec{{x}}, \\vec{{{result_name}}})"
        self.base_angle_name = f"\\angle(\\vec{{x}}, \\vec{{{base_name}}})"
        self.offset_angle_name = f"\\angle(\\vec{{{off_v1}}}, \\vec{{{off_v2}}})"
        self.target = f"{self.target_name} with respect to {result_ref}"

    def solve(self) -> tuple[Quantity, dict]:
        """
        Calculate the sum of two angles.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        # Use Quantity arithmetic for the sum (handles unit conversion automatically)
        result = self.base_angle + self.offset_angle
        result.name = self.target_name

        # Get display values in degrees for the solution step
        base_deg = self.base_angle.to_unit.degree.magnitude()
        offset_deg = self.offset_angle.to_unit.degree.magnitude()
        result_deg = result.to_unit.degree.magnitude()

        # Format substitution with proper LaTeX notation
        substitution = (
            f"{self.target_name} &= {self.base_angle_name} + {self.offset_angle_name} \\\\\n"
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
