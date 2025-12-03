"""
Parallelogram Law Problem Solver - Clean implementation with pattern-based dispatch.

This module provides a solver for vector addition problems using the parallelogram
law (triangle method). It uses the Triangle class from geometry.triangle to model
the problem and classify it by known/unknown quantities, then dispatches to the
appropriate solving strategy.

Key Design Principles:
1. No inheritance from Problem base class - keeps it simple and focused
2. Triangle class models the 3 sides and 3 angles of the vector triangle
3. Pattern matching on knowns determines which equations to call
4. Standard triangle solving cases: SAS, SSS, ASA, AAS, SSA

Triangle Quantities:
- 3 sides (magnitudes): |F₁|, |F₂|, |F_R|
- 3 interior angles: angle_A, angle_B, angle_C

Plus direction information for each vector (needed to compute interior angles
and final resultant direction).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ...core import Q
from ...equations import AngleBetween, AngleSum, LawOfCosines, LawOfSines
from ...geometry.triangle import Triangle, TriangleCase, from_vectors_dynamic
from ...linalg.vector2 import Vector, VectorUnknown

if TYPE_CHECKING:
    from ...core.quantity import Quantity


# =============================================================================
# Solving State (wraps Triangle with additional solving info)
# =============================================================================


@dataclass
class SolvingState:
    """
    Wraps a Triangle with additional state needed for solving.

    The Triangle handles the geometry (sides, angles, classification).
    This class adds:
    - References to original vectors for updating after solving
    - Solution tracking (steps, equations used)
    - Solved values for angles not stored in Triangle
    """
    triangle: Triangle

    # Additional solved angles (Triangle only stores angle_C initially)
    angle_ar: Quantity | None = None  # Angle from vec_a to resultant (angle_A in triangle)
    angle_br: Quantity | None = None  # Angle from vec_b to resultant (angle_B in triangle)

    # Solved resultant direction
    dir_r: Quantity | None = None

    # Solution tracking
    solving_steps: list[dict[str, Any]] = field(default_factory=list)
    equations_used: list[str] = field(default_factory=list)


# =============================================================================
# Solving Strategies
# =============================================================================


def solve_sas(state: SolvingState) -> None:
    """
    Solve SAS case: Two sides and included angle known.

    Strategy:
    1. angle_C (included angle) is already computed by Triangle
    2. Law of Cosines to find unknown side (resultant magnitude)
    3. Law of Sines to find one unknown angle
    4. Angle sum to find the resultant direction
    """
    triangle = state.triangle

    # Get the included angle (angle_C, opposite the resultant)
    if not triangle.angle_C.is_known or triangle.angle_C.angle is None:
        raise ValueError("Cannot solve SAS: included angle (angle_C) is not known")

    angle_ab = triangle.angle_C.angle  # The angle between vec_1 and vec_2

    # Step 1: Use Law of Cosines to find unknown side (resultant)
    if not triangle.side_c.is_known:
        # Get the known sides
        if triangle.side_a.magnitude is ... or triangle.side_b.magnitude is ...:
            raise ValueError("SAS requires sides a and b to be known")

        mag_a = triangle.side_a.magnitude
        mag_b = triangle.side_b.magnitude

        # Set names for reporting
        mag_a.name = f"{triangle.side_a.name}_mag"
        mag_b.name = f"{triangle.side_b.name}_mag"

        loc = LawOfCosines(
            target=f"|\\vec{{{triangle.side_c.name}}}| using Eq 1",
            side_a=mag_a,
            side_b=mag_b,
            angle=angle_ab,
        )
        mag_r, step = loc.solve()
        state.solving_steps.append(step)
        state.equations_used.append(loc.equation_for_list())

        # Update the triangle side
        triangle.side_c.magnitude = mag_r
        triangle.side_c.is_known = True

    # Step 2: Use Law of Sines to find an interior angle
    # Which angle we need depends on the geometric configuration
    v1_is_resultant = getattr(triangle.vec_1, "_is_resultant", False)
    v2_is_resultant = getattr(triangle.vec_2, "_is_resultant", False)

    if not v1_is_resultant and not v2_is_resultant:
        # Case 1: side_c is the resultant (Problem 2-1 type)
        # We need angle_B (opposite side_b), which is at the vertex shared by vec_1 and side_c
        # This is the angle from vec_1 to the resultant
        if state.angle_br is None:
            mag_b = triangle.side_b.magnitude  # Side opposite angle_B
            mag_r = triangle.side_c.magnitude  # The resultant we just computed

            if mag_b is ... or mag_r is ...:
                raise ValueError("Cannot compute angle_B: sides not known")

            # Determine if we need obtuse angle
            use_obtuse = mag_b > mag_r

            los = LawOfSines(
                target=f"\\angle(\\vec{{{triangle.vec_1.name}}}, \\vec{{{triangle.side_c.name}}}) using Eq 2",
                opposite_side=mag_b,  # side_b is opposite angle_B
                known_angle=angle_ab,  # angle_C
                known_side=mag_r,  # side_c
                use_obtuse=use_obtuse,
            )
            state.angle_br, step = los.solve()
            state.solving_steps.append(step)
            state.equations_used.append(los.equation_for_list())

            # Update triangle angle_B
            triangle.angle_B.angle = state.angle_br
            triangle.angle_B.is_known = True
    else:
        # Case 2: side_c is a component (Problem 2-2 type)
        # We need angle_A (opposite side_a), which is at the vertex shared by resultant and side_c
        # This is the angle from the resultant to the unknown component
        if state.angle_ar is None:
            mag_a = triangle.side_a.magnitude  # Side opposite angle_A
            mag_r = triangle.side_c.magnitude  # The unknown side we just computed

            if mag_a is ... or mag_r is ...:
                raise ValueError("Cannot compute angle_A: sides not known")

            # Determine if we need obtuse angle
            use_obtuse = mag_a > mag_r

            los = LawOfSines(
                target=f"\\angle(\\vec{{{triangle.side_c.name}}}, resultant) using Eq 2",
                opposite_side=mag_a,  # side_a is opposite angle_A
                known_angle=angle_ab,  # angle_C
                known_side=mag_r,  # side_c
                use_obtuse=use_obtuse,
            )
            state.angle_ar, step = los.solve()
            state.solving_steps.append(step)
            state.equations_used.append(los.equation_for_list())

            # Update triangle angle_A
            triangle.angle_A.angle = state.angle_ar
            triangle.angle_A.is_known = True

    # Step 3: Compute direction of the unknown side (side_c)
    if state.dir_r is None:
        from ...equations.angle_finder import get_absolute_angle

        if not v1_is_resultant and not v2_is_resultant:
            # Case 1: side_c is the resultant
            # dir(resultant) = dir(vec_1) + angle_B
            dir_ref = get_absolute_angle(triangle.vec_1)
            dir_ref.name = f"\\angle(\\vec{{x}}, \\vec{{{triangle.vec_1.name}}})"

            angle_sum = AngleSum(
                target=f"\\angle(\\vec{{x}}, \\vec{{{triangle.side_c.name}}}) with respect to +x",
                base_angle=dir_ref,
                offset_angle=state.angle_br,
                result_ref="+x",
            )
            state.dir_r, step = angle_sum.solve()
            state.solving_steps.append(step)
        else:
            # Case 2: side_c is a component
            # Find the resultant vector
            if v2_is_resultant:
                resultant_vec = triangle.vec_2
            else:
                resultant_vec = triangle.vec_1

            dir_resultant = get_absolute_angle(resultant_vec)
            dir_resultant.name = f"\\angle(\\vec{{x}}, \\vec{{{resultant_vec.name}}})"

            # dir(component) = dir(resultant) - angle_A
            neg_angle_ar = Q(0, "degree") - state.angle_ar
            neg_angle_ar.name = f"-\\angle_A"

            angle_sum = AngleSum(
                target=f"\\angle(\\vec{{x}}, \\vec{{{triangle.side_c.name}}}) with respect to +x",
                base_angle=dir_resultant,
                offset_angle=neg_angle_ar,
                result_ref="+x",
            )
            state.dir_r, step = angle_sum.solve()
            state.solving_steps.append(step)


def solve_sss(state: SolvingState) -> None:
    """
    Solve SSS case: All three sides known, find angles.

    Strategy:
    1. Law of Cosines to find largest angle (opposite longest side)
    2. Law of Sines for second angle
    3. Third angle = 180° - first - second
    """
    triangle = state.triangle

    if triangle.side_a.magnitude is ... or triangle.side_b.magnitude is ... or triangle.side_c.magnitude is ...:
        raise ValueError("SSS requires all three magnitudes to be known")

    # TODO: Implement Law of Cosines for finding angles
    raise NotImplementedError("SSS case not yet implemented")


def solve_ssa(state: SolvingState) -> None:
    """
    Solve SSA case: Two sides and non-included angle known.

    This is the ambiguous case - may have 0, 1, or 2 solutions.

    Strategy:
    1. Law of Sines to find angle opposite known side
    2. Check for ambiguity (may need to consider both acute and obtuse solutions)
    3. Third angle = 180° - known angles
    4. Law of Sines for unknown side
    """
    raise NotImplementedError("SSA case not yet implemented")


# Strategy dispatch table
SOLVING_STRATEGIES = {
    TriangleCase.SAS: solve_sas,
    TriangleCase.SSS: solve_sss,
    TriangleCase.SSA: solve_ssa,
}


# =============================================================================
# Main Problem Class
# =============================================================================


class ParallelogramLawProblem:
    """
    Solver for parallelogram law (vector addition) problems.

    This is a standalone solver that:
    1. Extracts vectors from class-level attributes
    2. Builds a Triangle from the vectors using geometry.triangle
    3. Classifies the problem (SAS, SSS, etc.) using Triangle.classify()
    4. Dispatches to the appropriate solving strategy
    5. Collects step-by-step solutions for reporting

    Example:
        >>> from qnty.linalg.vectors2 import create_vectors_polar, create_vector_resultant
        >>>
        >>> class MyProblem:
        ...     F_1 = create_vectors_polar(450, "N", 60, wrt="+x", name="F_1")
        ...     F_2 = create_vectors_polar(700, "N", 15, wrt="-x", name="F_2")
        ...     F_R = create_vector_resultant(F_1, F_2)
        >>>
        >>> problem = solve_class(MyProblem)
        >>> problem.generate_report("report.pdf", format="pdf")
    """

    name: str = "Parallelogram Law Problem"

    def __init__(self, name: str | None = None, description: str = ""):
        self.name = name or getattr(self.__class__, "name", self.__class__.__name__)
        self.description = description

        # Storage for vectors (both Vector and VectorUnknown)
        self.vectors: dict[str, Vector | VectorUnknown] = {}
        self._output_unit = "N"
        self._original_vector_states: dict[str, bool] = {}

        # For compatibility with report generator
        self.variables: dict[str, Quantity] = {}
        self._original_variable_states: dict[str, bool] = {}

        # Solving state
        self.is_solved = False
        self.solving_history: list[dict[str, Any]] = []
        self._equations_used: list[str] = []
        self._triangle: Triangle | None = None
        self._solving_state: SolvingState | None = None

        # Extract vectors from class attributes
        self._extract_vectors()

    def _extract_vectors(self) -> None:
        """Extract vector objects defined at class level and create variables for reporting."""
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)

            if isinstance(attr, Vector):
                # Create a copy of the vector for this instance
                vec_copy = Vector(
                    magnitude=attr.magnitude,
                    angle=attr.angle,
                    wrt=attr.wrt,
                    coordinate_system=attr.coordinate_system,
                    name=attr.name or attr_name,
                    _is_resultant=attr._is_resultant,
                )
                # Copy component vectors if present
                if hasattr(attr, '_component_vectors'):
                    vec_copy._component_vectors = attr._component_vectors  # type: ignore[attr-defined]
                setattr(self, attr_name, vec_copy)
                self.vectors[attr_name] = vec_copy

                # Determine if this is a known vector (has non-zero magnitude)
                is_known = attr.magnitude.value is not None and attr.magnitude.value != 0
                self._original_vector_states[attr_name] = is_known
                self._create_vector_variables(attr_name, vec_copy, is_known=is_known)

            elif isinstance(attr, VectorUnknown):
                # Create a copy of the VectorUnknown for this instance
                vec_copy = VectorUnknown(
                    magnitude=attr.magnitude,
                    angle=attr.angle,
                    wrt=attr.wrt,
                    coordinate_system=attr.coordinate_system,
                    name=attr.name or attr_name,
                    _is_resultant=attr._is_resultant,
                )
                # Copy component vectors if present
                if hasattr(attr, '_component_vectors'):
                    vec_copy._component_vectors = attr._component_vectors  # type: ignore[attr-defined]
                setattr(self, attr_name, vec_copy)
                self.vectors[attr_name] = vec_copy

                # VectorUnknown with ellipsis magnitude is unknown
                is_known = attr.magnitude is not ... and attr.magnitude.value is not None
                self._original_vector_states[attr_name] = is_known
                self._create_vector_unknown_variables(attr_name, vec_copy, is_known=is_known)

    def _create_vector_variables(self, name: str, vec: Vector, is_known: bool) -> None:
        """Create magnitude and angle Quantity variables for reporting compatibility."""
        # Magnitude - vec.magnitude is already a Quantity
        mag_qty = vec.magnitude
        mag_qty.name = f"{name}_mag"
        self.variables[f"{name}_mag"] = mag_qty
        self._original_variable_states[f"{name}_mag"] = is_known

        # Angle - vec.angle is already a Quantity
        angle_qty = vec.angle
        angle_qty.name = f"{name}_angle"
        self.variables[f"{name}_angle"] = angle_qty
        self._original_variable_states[f"{name}_angle"] = is_known

    def _create_vector_unknown_variables(self, name: str, vec: VectorUnknown, is_known: bool) -> None:
        """Create variables for VectorUnknown (may have ellipsis values)."""
        # Magnitude
        if vec.magnitude is not ...:
            mag_qty = vec.magnitude
            mag_qty.name = f"{name}_mag"
            self.variables[f"{name}_mag"] = mag_qty
            self._original_variable_states[f"{name}_mag"] = is_known
        else:
            # Create placeholder - will be filled after solving
            self._original_variable_states[f"{name}_mag"] = False

        # Angle
        if vec.angle is not ...:
            angle_qty = vec.angle
            angle_qty.name = f"{name}_angle"
            self.variables[f"{name}_angle"] = angle_qty
            self._original_variable_states[f"{name}_angle"] = is_known
        else:
            # Create placeholder - will be filled after solving
            self._original_variable_states[f"{name}_angle"] = False

    def get_known_variables(self) -> dict[str, Any]:
        """Get known variables for report generation."""
        return {name: vec for name, vec in self.vectors.items()
                if self._original_vector_states.get(name, True)}

    def get_unknown_variables(self) -> dict[str, Any]:
        """Get unknown variables for report generation."""
        return {name: vec for name, vec in self.vectors.items()
                if not self._original_vector_states.get(name, True)}

    def _build_triangle(self) -> Triangle:
        """
        Build Triangle from the extracted vectors using dependency analysis.

        Uses from_vectors_dynamic to automatically determine which vectors
        should form the computable interior angle based on which vectors
        have known directions.
        """
        # Use the new dependency-based triangle builder
        # It will analyze which vectors have known angles and assign them
        # appropriately so that the interior angle can be computed
        return from_vectors_dynamic(self.vectors)

    def solve(self, output_unit: str = "N") -> ParallelogramLawProblem:
        """
        Solve the parallelogram law problem.

        Uses pattern matching to classify the problem and dispatch to
        the appropriate solving strategy.

        Args:
            output_unit: Unit for output values (default "N")

        Returns:
            Self for method chaining
        """
        self._output_unit = output_unit

        # Build triangle
        triangle = self._build_triangle()
        self._triangle = triangle

        # Classify the problem using Triangle's classify method
        case = triangle.classify()

        # Create solving state
        state = SolvingState(triangle=triangle)
        self._solving_state = state

        # Dispatch to solving strategy
        strategy = SOLVING_STRATEGIES.get(case)
        if strategy is None:
            raise ValueError(f"No solving strategy for case: {case}")

        strategy(state)

        # Copy results back to instance
        self.solving_history = state.solving_steps
        self._equations_used = state.equations_used

        # Update resultant vector with solved values
        self._update_resultant_from_state(state)

        self.is_solved = True
        return self

    def _update_resultant_from_state(self, state: SolvingState) -> None:
        """Update the resultant vector with values from solved state."""
        triangle = state.triangle

        # Find the resultant in our vectors and replace VectorUnknown with solved Vector
        for name, vec in list(self.vectors.items()):
            if isinstance(vec, VectorUnknown):
                # Get solved values
                solved_mag = triangle.side_c.magnitude if triangle.side_c.magnitude is not ... else None
                solved_angle = state.dir_r

                if solved_mag is not None and solved_angle is not None:
                    # Create a proper Vector with solved values
                    solved_vector = Vector(
                        magnitude=solved_mag,
                        angle=solved_angle,
                        wrt=vec.wrt,
                        coordinate_system=vec.coordinate_system,
                        name=vec.name,
                    )
                    # Replace the VectorUnknown with the solved Vector
                    self.vectors[name] = solved_vector
                    setattr(self, name, solved_vector)

                    # Update variables for reporting
                    solved_mag.name = f"{name}_mag"
                    self.variables[f"{name}_mag"] = solved_mag
                    solved_angle.name = f"{name}_angle"
                    self.variables[f"{name}_angle"] = solved_angle

    def generate_report(self, output_path: str, format: str = "markdown") -> None:
        """
        Generate a report (Markdown, LaTeX, or PDF).

        Args:
            output_path: Path for output file
            format: Output format - 'markdown', 'latex', or 'pdf'
        """
        if not self.is_solved:
            raise ValueError("Problem must be solved before generating report")

        from .parallelogram_report import generate_report as _generate_report
        _generate_report(self, output_path, format=format)

    def to_dto(
        self,
        magnitude_unit: str = "N",
        angle_unit: str = "degree",
    ) -> dict[str, "VectorDTO"]:
        """
        Convert solved problem vectors to JSON-serializable VectorDTOs.

        Returns all vectors (both known and solved) converted to the
        requested units. This allows frontend applications to display
        results in user-preferred units.

        Args:
            magnitude_unit: Unit for force/magnitude values (e.g., "N", "lbf", "kN")
            angle_unit: Unit for angle values (e.g., "degree", "radian")

        Returns:
            Dictionary mapping vector names to their VectorDTO

        Raises:
            ValueError: If problem hasn't been solved yet

        Example:
            >>> problem = solve_class(MyProblem)
            >>> vectors = problem.to_dto(magnitude_unit="lbf", angle_unit="degree")
            >>> print(vectors["F_R"].magnitude)  # In lbf
            >>> print(vectors["F_1"].angle)  # In degrees
        """
        if not self.is_solved:
            raise ValueError("Problem must be solved before converting to DTO")

        from ...linalg.vector2 import VectorDTO

        # Convert all vectors to DTOs
        vector_dtos: dict[str, VectorDTO] = {}
        for name, vec in self.vectors.items():
            vector_dtos[name] = vec.to_dto(magnitude_unit, angle_unit)

        return vector_dtos


def solve_class(problem_class: type, output_unit: str = "N") -> ParallelogramLawProblem:
    """
    Solve a parallelogram law problem defined as a class.

    Args:
        problem_class: Class with vector attributes
        output_unit: Unit for output values

    Returns:
        Solved ParallelogramLawProblem instance
    """
    # Create dynamic problem class
    class DynamicProblem(ParallelogramLawProblem):
        pass

    DynamicProblem.name = getattr(problem_class, "name", problem_class.__name__)

    # Copy vector attributes (both Vector and VectorUnknown)
    for attr_name in dir(problem_class):
        if attr_name.startswith("_"):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, Vector | VectorUnknown):
            setattr(DynamicProblem, attr_name, attr)

    # Create and solve
    problem = DynamicProblem()
    problem.solve(output_unit=output_unit)
    return problem
