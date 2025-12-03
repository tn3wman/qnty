"""
Law of Cosines equation class with dynamic solution step generation.

The Law of Cosines relates three sides and one angle of a triangle:
    c² = a² + b² - 2·a·b·cos(C)

This can be used to find:
- An unknown side when two sides and the included angle are known
- An unknown angle when all three sides are known
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SolutionStepBuilder, format_angle, latex_name

if TYPE_CHECKING:
    from ..core.quantity import Quantity


class LawOfCosines:
    """
    Law of Cosines equation: c² = a² + b² - 2·a·b·cos(C)

    Standard triangle formula where C is the angle between sides a and b.
    Takes Quantity objects as input and returns a Quantity as output.

    The class handles LaTeX formatting internally - callers should pass
    the vector name (e.g., "F_R") and the class will generate proper
    LaTeX notation like |\\vec{F_R}|.
    """

    def __init__(
        self,
        side_a: Quantity,
        side_b: Quantity,
        angle: Quantity,
        result_vector_name: str,
        equation_number: int = 1,
        description: str = "",
    ):
        """
        Initialize Law of Cosines equation.

        Args:
            side_a: First side as a Quantity with magnitude value
            side_b: Second side as a Quantity with magnitude value
            angle: Angle between sides as a Quantity (in any angle unit)
            result_vector_name: Name of the unknown vector (e.g., "F_R")
            equation_number: Equation number for reference (default 1)
            description: Description for the step
        """
        self.side_a = side_a
        self.side_b = side_b
        self.angle = angle
        self.result_vector_name = result_vector_name
        self.equation_number = equation_number
        self.description = description or "Calculate resultant magnitude using Law of Cosines"

        # Generate the target string with LaTeX formatting
        self.target = f"|\\vec{{{latex_name(result_vector_name)}}}| using Eq {equation_number}"

    def _get_vector_name(self, qty: Quantity) -> str:
        """Extract clean vector name from a Quantity, removing _mag suffix."""
        name = qty.name if qty.name else "V"
        # Remove _mag suffix if present
        if name.endswith("_mag"):
            name = name[:-4]
        return latex_name(name)

    def equation_for_list(self) -> str:
        """Return the equation string for the 'Equations Used' section with proper LaTeX."""
        result_name = latex_name(self.result_vector_name)
        side_a_name = self._get_vector_name(self.side_a)
        side_b_name = self._get_vector_name(self.side_b)
        return (
            f"|\\vec{{{result_name}}}|^2 = |\\vec{{{side_a_name}}}|^2 + |\\vec{{{side_b_name}}}|^2 "
            f"- 2 \\cdot |\\vec{{{side_a_name}}}| \\cdot |\\vec{{{side_b_name}}}| \\cdot "
            f"\\cos(\\angle(\\vec{{{side_a_name}}}, \\vec{{{side_b_name}}}))"
        )

    def solve(self) -> tuple[Quantity, dict]:
        """
        Solve for the unknown side using Law of Cosines.

        Returns:
            Tuple of (result_quantity, solution_step_dict)
        """
        from ..algebra.functions import cos, sqrt
        from ..core.quantity import Quantity

        # Law of Cosines using qnty math: c² = a² + b² - 2ab·cos(C)
        c_squared = self.side_a**2 + self.side_b**2 - 2 * self.side_a * self.side_b * cos(self.angle)
        result = sqrt(c_squared)

        # Ensure result is a Quantity (should always be true for concrete inputs)
        if not isinstance(result, Quantity):
            raise TypeError(f"Expected Quantity result from Law of Cosines, got {type(result).__name__}")

        # Set name on result using the provided vector name
        result_name = latex_name(self.result_vector_name)
        result.name = f"{self.result_vector_name}_mag"

        # Get display values for step formatting
        a = self.side_a.magnitude()
        b = self.side_b.magnitude()
        angle_deg = self.angle.to_unit.degree.magnitude()
        c = result.magnitude()
        unit_str = self.side_a.preferred.symbol if self.side_a.preferred else "N"

        # Format substitution with proper LaTeX notation
        substitution = f"|\\vec{{{result_name}}}| &= \\sqrt{{({a:.1f})^2 + ({b:.1f})^2 - 2({a:.1f})({b:.1f})\\cos({format_angle(angle_deg)})}} \\\\\n&= {c:.1f}\\ \\text{{{unit_str}}} \\\\"

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Cosines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()
