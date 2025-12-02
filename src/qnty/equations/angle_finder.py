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
    from ..spatial.vector import _Vector


class AngleBetween:
    """
    Calculate the angle between two vectors given their directions.
    Takes vectors as input and returns an angle Quantity.
    """

    def __init__(
        self,
        target: str,
        vec1: "_Vector",
        vec2: "_Vector",
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

    def solve(self) -> tuple["Quantity", dict]:
        """
        Calculate the triangle angle between two vectors for parallelogram law.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        from ..core import Q

        # Get original angles and references from vectors
        vec1_angle_deg = getattr(self.vec1, '_original_angle', 0.0)
        vec2_angle_deg = getattr(self.vec2, '_original_angle', 0.0)
        vec1_ref = getattr(self.vec1, '_original_wrt', '+x')
        vec2_ref = getattr(self.vec2, '_original_wrt', '+x')
        vec1_name = getattr(self.vec1, 'name', 'V_1')
        vec2_name = getattr(self.vec2, 'name', 'V_2')

        # Compute triangle angle as absolute difference
        result_deg = abs(vec1_angle_deg - vec2_angle_deg)

        # Create result Quantity using Q() - handles unit conversion automatically
        result = Q(result_deg, 'degree')
        result.name = self.target

        # Format substitution with proper LaTeX notation
        substitution = (
            f"\\angle(\\vec{{{vec1_name}}}, \\vec{{{vec2_name}}}) &= "
            f"|\\angle(\\vec{{{vec1_ref}}}, \\vec{{{vec1_name}}}) - "
            f"\\angle(\\vec{{{vec2_ref}}}, \\vec{{{vec2_name}}})| \\\\\n"
            f"&= |{format_angle(vec1_angle_deg)} - {format_angle(vec2_angle_deg)}| \\\\\n"
            f"&= {format_angle(result_deg)} \\\\"
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
        base_angle: "Quantity",
        offset_angle: "Quantity",
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

    def solve(self) -> tuple["Quantity", dict]:
        """
        Calculate the sum of two angles.

        Returns:
            Tuple of (angle_quantity, solution_step_dict)
        """
        from ..core import Q

        # Get angle values in degrees using magnitude()
        base_deg = self.base_angle.magnitude()
        offset_deg = self.offset_angle.magnitude()
        result_deg = base_deg + offset_deg

        # Create result Quantity using Q()
        result = Q(result_deg, 'degree')
        result.name = self.target.split(" with")[0]

        # Extract target name without "with respect to" suffix
        target_name = self.target.split(" with")[0]

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
