"""
Law of Sines equation class with dynamic solution step generation.

The Law of Sines relates sides and opposite angles of a triangle:
    a/sin(A) = b/sin(B) = c/sin(C)

This can be used to find:
- An unknown angle when two sides and one angle are known (solve_for="angle")
- An unknown side when two angles and one side are known (solve_for="side")
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .base import SolutionStepBuilder, format_angle, latex_name

if TYPE_CHECKING:
    from ..core.quantity import Quantity


class LawOfSines:
    """
    Law of Sines equation: sin(A)/a = sin(B)/b

    Used to find angles or sides in the force triangle.
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
        solve_for: Literal["angle", "side"] = "angle",
        unknown_angle: Quantity | None = None,
        result_vector_name: str | None = None,
        known_angle_vectors: tuple[str, str] | None = None,
    ):
        """
        Initialize Law of Sines equation.

        For finding an angle (solve_for="angle"):
        - sin(A)/a = sin(B)/b
        - A = sin⁻¹(a · sin(B) / b)

        For finding a side (solve_for="side"):
        - a/sin(A) = b/sin(B)
        - a = b · sin(A) / sin(B)

        Args:
            opposite_side: Side opposite to unknown angle (for angle mode) or known side (for side mode)
            known_angle: Known angle as a Quantity (angle opposite to known_side)
            known_side: Side opposite to known angle as a Quantity
            angle_vector_1: First vector forming the angle (e.g., "F_1")
            angle_vector_2: Second vector forming the angle (e.g., "F_R")
            equation_number: Equation number for reference (default 2)
            use_obtuse: If True, use the obtuse angle (180° - asin result) - only for angle mode
            description: Description for the step
            solve_for: "angle" to find an angle, "side" to find a side
            unknown_angle: The angle opposite to the unknown side (required for side mode)
            result_vector_name: Name of the result vector (for side mode)
            known_angle_vectors: Tuple of (vector1, vector2) that form the known angle (for side mode)
        """
        self.opposite_side = opposite_side
        self.known_angle = known_angle
        self.known_side = known_side
        self.angle_vector_1 = angle_vector_1
        self.angle_vector_2 = angle_vector_2
        self.equation_number = equation_number
        self.use_obtuse = use_obtuse
        self.solve_for = solve_for
        self.unknown_angle = unknown_angle
        self.result_vector_name = result_vector_name or angle_vector_1
        self.known_angle_vectors = known_angle_vectors

        if solve_for == "angle":
            self.description = description or "Calculate angle using Law of Sines"
            # Generate the angle name with LaTeX formatting
            v1 = latex_name(angle_vector_1)
            v2 = latex_name(angle_vector_2)
            self.angle_name = f"\\angle(\\vec{{{v1}}}, \\vec{{{v2}}})"
            self.target = f"{self.angle_name} using Eq {equation_number}"
        else:
            self.description = description or f"Calculate magnitude of {result_vector_name}"
            self.target = f"|\\vec{{{latex_name(self.result_vector_name)}}}| using Eq {equation_number}"

    def _get_vector_name(self, qty: Quantity) -> str:
        """Extract clean vector name from a Quantity, removing _mag suffix."""
        name = qty.name if qty.name else "V"
        # Remove _mag suffix if present
        if name.endswith("_mag"):
            name = name[:-4]
        return latex_name(name)

    def equation_for_list(self) -> str:
        """Return the equation string for the 'Equations Used' section with proper LaTeX."""
        if self.solve_for == "side":
            return self._equation_for_list_side()
        return self._equation_for_list_angle()

    def _equation_for_list_angle(self) -> str:
        """Equation for finding an angle."""
        opp_name = self._get_vector_name(self.opposite_side)
        result_name = self._get_vector_name(self.known_side)

        # Use the generated angle_name for the angle being solved
        # For the known angle, use a proper LaTeX representation
        known_angle_name = getattr(self.known_angle, "name", None)
        if known_angle_name and not known_angle_name.replace(".", "").replace("-", "").isdigit():
            known_angle_repr = known_angle_name
        else:
            known_angle_repr = f"\\angle(\\vec{{{opp_name}}}, \\vec{{{result_name}}})"

        return f"\\frac{{\\sin({self.angle_name})}}{{|\\vec{{{opp_name}}}|}} = \\frac{{\\sin({known_angle_repr})}}{{|\\vec{{{result_name}}}|}}"

    def _equation_for_list_side(self) -> str:
        """Equation for finding a side."""
        result_name = latex_name(self.result_vector_name)
        known_side_name = self._get_vector_name(self.known_side)

        # Build unknown angle name using angle_vector_1 and angle_vector_2
        # These specify the two vectors that form the angle opposite to the unknown side
        v1 = latex_name(self.angle_vector_1)
        v2 = latex_name(self.angle_vector_2)
        unknown_angle_name = f"\\angle(\\vec{{{v1}}}, \\vec{{{v2}}})"

        # Build known angle name using known_angle_vectors if provided
        if self.known_angle_vectors:
            kv1 = latex_name(self.known_angle_vectors[0])
            kv2 = latex_name(self.known_angle_vectors[1])
            known_angle_name = f"\\angle(\\vec{{{kv1}}}, \\vec{{{kv2}}})"
        else:
            # Fallback: use opposite vectors to known side
            known_angle_name = f"\\angle(\\vec{{{known_side_name}}})"

        return f"\\frac{{|\\vec{{{result_name}}}|}}{{\\sin({unknown_angle_name})}} = \\frac{{|\\vec{{{known_side_name}}}|}}{{\\sin({known_angle_name})}}"

    def solve(self) -> tuple[Quantity, dict]:
        """Solve using Law of Sines."""
        if self.solve_for == "side":
            return self._solve_for_side()
        return self._solve_for_angle()

    def _solve_for_angle(self) -> tuple[Quantity, dict]:
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

        # Get display values for substitution using LaTeX formatting for proper spacing
        a_latex = self.opposite_side.to_latex(precision=1) if hasattr(self.opposite_side, 'to_latex') else str(self.opposite_side)
        b_latex = self.known_side.to_latex(precision=1) if hasattr(self.known_side, 'to_latex') else str(self.known_side)
        known_angle_deg = self.known_angle.to_unit.degree

        substitution = f"{self.angle_name} &= \\sin^{{-1}}({a_latex} \\cdot \\frac{{\\sin({format_angle(known_angle_deg, precision=1)})}}{{{b_latex}}}) \\\\\n&= {format_angle(result, precision=1)} \\\\"

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Sines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()

    def _solve_for_side(self) -> tuple[Quantity, dict]:
        """
        Solve for an unknown side using Law of Sines.

        Uses: a = b · sin(A) / sin(B)
        Where:
        - a is the unknown side (result)
        - b is the known side (self.known_side)
        - A is the angle opposite to the unknown side (self.unknown_angle)
        - B is the angle opposite to the known side (self.known_angle)

        Returns:
            Tuple of (result_side_quantity, solution_step_dict)
        """
        from ..algebra.functions import sin

        if self.unknown_angle is None:
            raise ValueError("unknown_angle is required for solve_for='side'")

        from ..core.quantity import Quantity

        # a = b · sin(A) / sin(B)
        sin_unknown = sin(self.unknown_angle)
        sin_known = sin(self.known_angle)

        result = self.known_side * sin_unknown / sin_known

        # Ensure result is a Quantity (should always be true for concrete inputs)
        if not isinstance(result, Quantity):
            raise TypeError(f"Expected Quantity result from Law of Sines, got {type(result).__name__}")

        result.name = f"{self.result_vector_name}_mag"

        # Preserve the unit from the known side for display
        if hasattr(self.known_side, "preferred") and self.known_side.preferred is not None:
            result.preferred = self.known_side.preferred

        # Get display values for substitution using LaTeX formatting
        result_name = latex_name(self.result_vector_name)
        known_side_latex = self.known_side.to_latex(precision=1)
        unknown_angle_deg = self.unknown_angle.to_unit.degree
        known_angle_deg = self.known_angle.to_unit.degree
        result_latex = result.to_latex(precision=1)

        substitution = (
            f"|\\vec{{{result_name}}}| &= {known_side_latex} \\cdot "
            f"\\frac{{\\sin({format_angle(unknown_angle_deg, precision=1)})}}{{\\sin({format_angle(known_angle_deg, precision=1)})}} \\\\\n"
            f"&= {result_latex} \\\\"
        )

        step = SolutionStepBuilder(
            target=self.target,
            method="Law of Sines",
            description=self.description,
            equation_for_list=self.equation_for_list(),
            substitution=substitution,
        )

        return result, step.build()
