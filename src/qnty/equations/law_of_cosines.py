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

from .base import SolutionStepBuilder, format_angle

if TYPE_CHECKING:
    from ..core.quantity import Quantity


class LawOfCosines:
    """
    Law of Cosines equation: c² = a² + b² - 2·a·b·cos(C)

    Standard triangle formula where C is the angle between sides a and b.
    Takes Quantity objects as input and returns a Quantity as output.
    """

    def __init__(
        self,
        target: str,
        side_a: "Quantity",
        side_b: "Quantity",
        angle: "Quantity",
        description: str = "",
    ):
        """
        Initialize Law of Cosines equation.

        Args:
            target: Name of variable being solved for (e.g., "|F_R| using Eq 1")
            side_a: First side as a Quantity with magnitude value
            side_b: Second side as a Quantity with magnitude value
            angle: Angle between sides as a Quantity (in any angle unit)
            description: Description for the step
        """
        self.target = target
        self.side_a = side_a
        self.side_b = side_b
        self.angle = angle
        self.description = description or "Calculate resultant magnitude using Law of Cosines"

    def _clean_name(self, name: str) -> str:
        """Remove existing \\vec{} wrapper if present and return clean name."""
        if name.startswith("\\vec{") and name.endswith("}"):
            return name[5:-1]  # Remove \vec{ and }
        return name

    def equation_for_list(self) -> str:
        """Return the equation string for the 'Equations Used' section with proper LaTeX."""
        result_name = self._clean_name(self.target.split()[0].strip("|"))
        side_a_name = self._clean_name(self.side_a.name.replace("_mag", ""))
        side_b_name = self._clean_name(self.side_b.name.replace("_mag", ""))
        return (
            f"|\\vec{{{result_name}}}|^2 = |\\vec{{{side_a_name}}}|^2 + |\\vec{{{side_b_name}}}|^2 "
            f"- 2 \\cdot |\\vec{{{side_a_name}}}| \\cdot |\\vec{{{side_b_name}}}| \\cdot "
            f"\\cos(\\angle(\\vec{{{side_a_name}}}, \\vec{{{side_b_name}}}))"
        )

    def solve(self) -> tuple["Quantity", dict]:
        """
        Solve for the unknown side using Law of Cosines.

        Returns:
            Tuple of (result_quantity, solution_step_dict)
        """
        from ..algebra.functions import cos, sqrt

        # Law of Cosines using qnty math: c² = a² + b² - 2ab·cos(C)
        c_squared = self.side_a**2 + self.side_b**2 - 2 * self.side_a * self.side_b * cos(self.angle)
        result = sqrt(c_squared)

        # Set name on result
        result_name = self._clean_name(self.target.split()[0].strip("|"))
        result.name = f"{result_name}_mag"

        # Get display values for step formatting
        a = self.side_a.magnitude()
        b = self.side_b.magnitude()
        angle_deg = self.angle.magnitude()
        c = result.magnitude()
        unit_str = self.side_a.preferred.symbol if self.side_a.preferred else "N"

        # Format substitution with proper LaTeX notation
        substitution = (
            f"|\\vec{{{result_name}}}| &= \\sqrt{{({a:.1f})^2 + ({b:.1f})^2 - "
            f"2({a:.1f})({b:.1f})\\cos({format_angle(angle_deg)})}} \\\\\n"
            f"&= {c:.1f}\\ \\text{{{unit_str}}} \\\\"
        )

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Cosines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()
