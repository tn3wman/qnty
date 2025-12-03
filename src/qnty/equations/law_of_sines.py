"""
Law of Sines equation class with dynamic solution step generation.

The Law of Sines relates sides and opposite angles of a triangle:
    a/sin(A) = b/sin(B) = c/sin(C)

This can be used to find:
- An unknown angle when two sides and one angle are known
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SolutionStepBuilder, format_angle, latex_name

if TYPE_CHECKING:
    from ..core.quantity import Quantity


class LawOfSines:
    """
    Law of Sines equation: sin(A)/a = sin(B)/b

    Used to find angles in the force triangle.
    Takes Quantity objects as input and returns a Quantity as output.

    The class handles LaTeX formatting internally - callers should pass
    vector names and the class will generate proper LaTeX notation.
    """

    def __init__(
        self,
        opposite_side: Quantity,
        known_angle: Quantity,
        known_side: Quantity,
        angle_vector_1: str,
        angle_vector_2: str,
        equation_number: int = 2,
        use_obtuse: bool = False,
        description: str = "",
    ):
        """
        Initialize Law of Sines equation.

        To find angle A given:
        - sin(A)/a = sin(B)/b
        - A = sin⁻¹(a · sin(B) / b)

        Args:
            opposite_side: Side opposite to unknown angle as a Quantity
            known_angle: Known angle as a Quantity
            known_side: Side opposite to known angle as a Quantity
            angle_vector_1: First vector forming the angle (e.g., "F_1")
            angle_vector_2: Second vector forming the angle (e.g., "F_R")
            equation_number: Equation number for reference (default 2)
            use_obtuse: If True, use the obtuse angle (180° - asin result)
            description: Description for the step
        """
        self.opposite_side = opposite_side
        self.known_angle = known_angle
        self.known_side = known_side
        self.angle_vector_1 = angle_vector_1
        self.angle_vector_2 = angle_vector_2
        self.equation_number = equation_number
        self.use_obtuse = use_obtuse
        self.description = description or "Calculate angle using Law of Sines"

        # Generate the angle name with LaTeX formatting
        v1 = latex_name(angle_vector_1)
        v2 = latex_name(angle_vector_2)
        self.angle_name = f"\\angle(\\vec{{{v1}}}, \\vec{{{v2}}})"
        self.target = f"{self.angle_name} using Eq {equation_number}"

    def _get_vector_name(self, qty: Quantity) -> str:
        """Extract clean vector name from a Quantity, removing _mag suffix."""
        name = qty.name if qty.name else "V"
        # Remove _mag suffix if present
        if name.endswith("_mag"):
            name = name[:-4]
        return latex_name(name)

    def equation_for_list(self) -> str:
        """Return the equation string for the 'Equations Used' section with proper LaTeX.

        Law of Sines: sin(A)/a = sin(B)/b
        We use it to find angle A where:
        - a is the opposite_side (e.g., F_2)
        - B is the known_angle (triangle angle)
        - b is the known_side (e.g., F_R)
        """
        opp_name = self._get_vector_name(self.opposite_side)
        result_name = self._get_vector_name(self.known_side)

        # Use the generated angle_name for the angle being solved
        # Extract the known angle representation - this is the interior angle
        known_angle_repr = getattr(self.known_angle, "name", "\\angle")

        return f"\\frac{{\\sin({self.angle_name})}}{{|\\vec{{{opp_name}}}|}} = \\frac{{\\sin({known_angle_repr})}}{{|\\vec{{{result_name}}}|}}"

    def solve(self) -> tuple[Quantity, dict]:
        """
        Solve for the unknown angle using Law of Sines.

        Returns:
            Tuple of (result_angle_quantity, solution_step_dict)
        """
        from ..algebra.functions import asin, sin
        from ..core import Q
        from ..core.quantity import Quantity
        from ..geometry.triangle import _get_angle_constants

        _, half_rotation, _ = _get_angle_constants()

        # sin(A) = a · sin(B) / b
        # A = asin(a · sin(B) / b)
        sin_known = sin(self.known_angle)

        # Ensure sin_known is a Quantity (should always be true for concrete angle inputs)
        if not isinstance(sin_known, Quantity):
            raise TypeError(f"Expected Quantity result from sin(), got {type(sin_known).__name__}")

        # Compute sin(A) using Quantity arithmetic: a * sin(B) / b
        sin_result = self.opposite_side * sin_known / self.known_side

        # Clamp to valid range for asin [-1, 1]
        # We need to check the value and clamp if needed
        sin_value = sin_result.value
        if sin_value is not None:
            if sin_value > 1.0:
                sin_result = Q(1.0, "dimensionless")
            elif sin_value < -1.0:
                sin_result = Q(-1.0, "dimensionless")

        # Use asin to get the angle
        result = asin(sin_result)

        # Use obtuse angle if requested (180° - acute)
        if self.use_obtuse:
            result = half_rotation - result

        # Convert to degrees for display
        result = result.to_unit.degree

        # Use the generated angle_name for the result
        result.name = self.angle_name

        # Get display values for substitution
        a_display = self.opposite_side.to_unit.newton if hasattr(self.opposite_side, 'to_unit') else self.opposite_side
        b_display = self.known_side.to_unit.newton if hasattr(self.known_side, 'to_unit') else self.known_side
        known_angle_deg = self.known_angle.to_unit.degree

        substitution = f"{self.angle_name} &= \\sin^{{-1}}({a_display} \\cdot \\frac{{\\sin({format_angle(known_angle_deg)})}}{{{b_display}}}) \\\\\n&= {format_angle(result)} \\\\"

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Sines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()
