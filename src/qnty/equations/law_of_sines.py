"""
Law of Sines equation class with dynamic solution step generation.

The Law of Sines relates sides and opposite angles of a triangle:
    a/sin(A) = b/sin(B) = c/sin(C)

This can be used to find:
- An unknown angle when two sides and one angle are known
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SolutionStepBuilder, format_angle

if TYPE_CHECKING:
    from ..core.quantity import Quantity


class LawOfSines:
    """
    Law of Sines equation: sin(A)/a = sin(B)/b

    Used to find angles in the force triangle.
    Takes Quantity objects as input and returns a Quantity as output.
    """

    def __init__(
        self,
        target: str,
        opposite_side: "Quantity",
        known_angle: "Quantity",
        known_side: "Quantity",
        use_obtuse: bool = False,
        description: str = "",
    ):
        """
        Initialize Law of Sines equation.

        To find angle A given:
        - sin(A)/a = sin(B)/b
        - A = sin⁻¹(a · sin(B) / b)

        Args:
            target: Name of variable being solved for (e.g., "∠(F_1,F_R) using Eq 2")
            opposite_side: Side opposite to unknown angle as a Quantity
            known_angle: Known angle as a Quantity
            known_side: Side opposite to known angle as a Quantity
            use_obtuse: If True, use the obtuse angle (180° - asin result)
            description: Description for the step
        """
        self.target = target
        self.opposite_side = opposite_side
        self.known_angle = known_angle
        self.known_side = known_side
        self.use_obtuse = use_obtuse
        self.description = description or "Calculate angle using Law of Sines"

    def _clean_name(self, name: str) -> str:
        """Remove existing \\vec{} wrapper if present and return clean name."""
        if name.startswith("\\vec{") and name.endswith("}"):
            return name[5:-1]  # Remove \vec{ and }
        return name

    def equation_for_list(self) -> str:
        """Return the equation string for the 'Equations Used' section with proper LaTeX.

        Law of Sines: sin(A)/a = sin(B)/b
        We use it to find angle A where:
        - a is the opposite_side (e.g., F_2)
        - B is the known_angle (triangle angle)
        - b is the known_side (e.g., F_R)
        """
        opp_name = self._clean_name(self.opposite_side.name.replace("_mag", ""))
        result_name = self._clean_name(self.known_side.name.replace("_mag", ""))
        return (
            f"\\frac{{\\sin(\\theta)}}{{|\\vec{{{opp_name}}}|}} = "
            f"\\frac{{\\sin(\\gamma)}}{{|\\vec{{{result_name}}}|}}"
        )

    def solve(self) -> tuple["Quantity", dict]:
        """
        Solve for the unknown angle using Law of Sines.

        Returns:
            Tuple of (result_angle_quantity, solution_step_dict)
        """
        import math

        from ..algebra.functions import sin
        from ..core import Q

        # Get values for calculation
        a = self.opposite_side.magnitude()  # Side opposite to unknown angle
        b = self.known_side.magnitude()      # Side opposite to known angle
        known_angle_deg = self.known_angle.magnitude()

        # sin(A) = a · sin(B) / b
        # We need to compute this carefully since we need asin at the end
        sin_known = sin(self.known_angle)
        sin_result_value = a * sin_known.magnitude() / b

        # Clamp to valid range for asin
        sin_result_value = max(-1.0, min(1.0, sin_result_value))
        result_deg = math.degrees(math.asin(sin_result_value))

        # Use obtuse angle if requested (180° - acute)
        if self.use_obtuse:
            result_deg = 180.0 - result_deg

        # Create result Quantity using Q()
        result = Q(result_deg, 'degree')

        # Extract angle name (everything before " using" if present)
        angle_name = self.target.split(" using")[0] if " using" in self.target else self.target
        result.name = angle_name

        substitution = (
            f"{angle_name} &= \\sin^{{-1}}({a:.1f} \\cdot "
            f"\\frac{{\\sin({format_angle(known_angle_deg)})}}{{{b:.1f}}}) \\\\\n"
            f"&= {format_angle(result_deg, precision=1)} \\\\"
        )

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Sines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()
