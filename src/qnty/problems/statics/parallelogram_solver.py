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

from ...equations import AngleSum, LawOfCosines, LawOfSines
from ...equations.angle_finder import get_relative_angle
from ...geometry.triangle import Triangle, TriangleCase, from_vectors_dynamic
from ...linalg.vector2 import Vector, VectorUnknown
from ...spatial.angle_reference import AngleDirection

if TYPE_CHECKING:
    from ...core.quantity import Quantity
    from ...linalg.vector2 import VectorDTO


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

    Uses the vertex-based triangle model to handle all configurations uniformly:
    1. Get the SAS configuration from the triangle (which sides, which angle)
    2. Law of Cosines to find the unknown side magnitude
    3. Law of Sines to find an interior angle at a vertex adjacent to the unknown side
    4. Use vertex geometry to compute the unknown side's direction
    """
    triangle = state.triangle

    # Get the SAS configuration from the triangle
    sas_config = triangle.get_sas_configuration()
    if sas_config is None:
        raise ValueError("Cannot solve SAS: triangle is not in SAS configuration")

    known_side_1 = sas_config["known_side_1"]
    known_side_2 = sas_config["known_side_2"]
    included_angle = sas_config["included_angle"]
    unknown_side = sas_config["unknown_side"]

    if included_angle.angle is None:
        raise ValueError("Cannot solve SAS: included angle is not known")

    angle_included = included_angle.angle

    # Step 1: Use Law of Cosines to find unknown side magnitude
    if not unknown_side.is_known:
        if known_side_1.magnitude is ... or known_side_2.magnitude is ...:
            raise ValueError("SAS requires both known sides to have magnitudes")

        mag_1 = known_side_1.magnitude
        mag_2 = known_side_2.magnitude

        # Set names for reporting
        mag_1.name = f"{known_side_1.name}_mag"
        mag_2.name = f"{known_side_2.name}_mag"

        # LawOfCosines handles LaTeX formatting internally
        loc = LawOfCosines(
            side_a=mag_1,
            side_b=mag_2,
            angle=angle_included,
            result_vector_name=unknown_side.name,
            equation_number=1,
        )
        mag_unknown, step = loc.solve()
        state.solving_steps.append(step)
        state.equations_used.append(loc.equation_for_list())

        # Update the triangle side
        unknown_side.magnitude = mag_unknown
        unknown_side.is_known = True

    # Step 2: Use Law of Sines to find an interior angle
    # We need an angle at a vertex adjacent to the unknown side
    # The unknown_angle_1 is at a vertex where the unknown side meets a known side
    unknown_angle_1 = sas_config["unknown_angle_1"]

    # Find the side opposite to unknown_angle_1 (this is one of the known sides)
    # For Law of Sines: sin(unknown_angle_1) / opposite_side = sin(included_angle) / unknown_side
    opposite_side = None
    for side in [known_side_1, known_side_2]:
        if side.name == unknown_angle_1.opposite_side:
            opposite_side = side
            break

    if opposite_side is None:
        # Try the other unknown angle
        unknown_angle_1 = sas_config["unknown_angle_2"]
        for side in [known_side_1, known_side_2]:
            if side.name == unknown_angle_1.opposite_side:
                opposite_side = side
                break

    if opposite_side is None or opposite_side.magnitude is ...:
        raise ValueError("Cannot find opposite side for Law of Sines")

    mag_opposite = opposite_side.magnitude
    mag_unknown = unknown_side.magnitude

    if mag_unknown is ...:
        raise ValueError("Unknown side magnitude not computed")

    # Determine if we need obtuse angle
    use_obtuse = mag_opposite > mag_unknown

    # Find the adjacent side names for the angle we're solving
    # The angle at a vertex is between the two sides adjacent to that vertex
    adjacent_side_names = []
    for side in [known_side_1, known_side_2, unknown_side]:
        if side.start == unknown_angle_1.vertex or side.end == unknown_angle_1.vertex:
            adjacent_side_names.append(side.name)

    # LawOfSines handles LaTeX formatting internally
    if len(adjacent_side_names) == 2:
        los = LawOfSines(
            opposite_side=mag_opposite,
            known_angle=angle_included,
            known_side=mag_unknown,
            angle_vector_1=adjacent_side_names[0],
            angle_vector_2=adjacent_side_names[1],
            equation_number=2,
            use_obtuse=use_obtuse,
        )
    else:
        # Fallback - shouldn't happen in normal cases
        los = LawOfSines(
            opposite_side=mag_opposite,
            known_angle=angle_included,
            known_side=mag_unknown,
            angle_vector_1=known_side_1.name or "V1",
            angle_vector_2=unknown_side.name or "R",
            equation_number=2,
            use_obtuse=use_obtuse,
        )

    solved_angle, step = los.solve()
    state.solving_steps.append(step)
    state.equations_used.append(los.equation_for_list())

    # Update triangle angle
    unknown_angle_1.angle = solved_angle
    unknown_angle_1.is_known = True

    # Store for direction computation
    state.angle_ar = solved_angle

    # Step 3: Compute direction of the unknown side using vertex geometry
    if state.dir_r is None:
        # Use the triangle's vertex-based direction computation for the correct answer
        computed_dir = triangle.compute_unknown_direction(unknown_side, unknown_angle_1)

        if computed_dir is not None:
            state.dir_r = computed_dir

            # Find the adjacent known side to build the proper step with AngleSum
            # The side at vertex A that's not the unknown side (resultant)
            adjacent_known_side = None
            for side in [known_side_1, known_side_2]:
                if side.direction is not None:
                    # Prefer the side at vertex A (shares start with unknown_side)
                    if side.start == unknown_side.start:
                        adjacent_known_side = side
                        break
                    # Fall back to any adjacent side
                    elif side.end == unknown_side.start or side.start == unknown_side.end or side.end == unknown_side.end:
                        if adjacent_known_side is None:
                            adjacent_known_side = side

            if adjacent_known_side is not None and solved_angle is not None:
                # AngleSum handles LaTeX formatting internally
                angle_sum = AngleSum(
                    base_angle=adjacent_known_side.direction,
                    offset_angle=solved_angle,
                    result_vector_name=unknown_side.name,
                    base_vector_name=adjacent_known_side.name,
                    offset_vector_1=adjacent_known_side.name,
                    offset_vector_2=unknown_side.name,
                    result_ref="+x",
                )
                _, step = angle_sum.solve()
                state.solving_steps.append(step)
            else:
                # Fallback: simple step using SolutionStepBuilder directly
                from ...equations.base import SolutionStepBuilder, latex_name

                result_name = latex_name(unknown_side.name)
                computed_dir_deg = computed_dir.to_unit.degree
                step = SolutionStepBuilder(
                    target=f"\\angle(\\vec{{x}}, \\vec{{{result_name}}}) with respect to +x",
                    method="Vertex Geometry",
                    description="Compute direction using vertex-based geometry",
                    substitution=f"\\theta = {computed_dir_deg}",
                ).build()
                state.solving_steps.append(step)
        else:
            raise ValueError("Cannot compute direction of unknown side")


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


def solve_ssa(_state: SolvingState) -> None:
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


def solve_asa(state: SolvingState) -> None:
    """
    Solve ASA case: Two angles and included side known.

    In parallelogram law problems, this occurs when:
    - Both component vectors have known directions (angles) but unknown magnitudes
    - The resultant has known magnitude and direction

    The "included side" is the side between the two known angles.

    Strategy:
    1. Compute the third interior angle using angle sum (180° - A - B = C)
    2. Use Law of Sines to find each unknown side magnitude
    3. The directions are already known from the input vectors

    For Problem 2-4:
        - F_AB: direction = -45° wrt -y, magnitude unknown
        - F_AC: direction = -30° wrt +x, magnitude unknown
        - F_R:  direction = 0° wrt -y, magnitude = 500 N (the included side)
    """
    from ...core import Q
    from ...equations import LawOfSines
    from ...equations.base import SolutionStepBuilder

    triangle = state.triangle

    # Find the ASA configuration
    # In ASA, we have 2+ angles known and 1+ side known
    # The included side is the one that connects the two known angles

    # ASA configurations: (angle1_attr, angle2_attr, included_side_attr, unknown_side1_attr, unknown_side2_attr)
    asa_configs = [
        ("angle_A", "angle_B", "side_c", "side_a", "side_b"),  # angle_A and angle_B -> side_c between them
        ("angle_A", "angle_C", "side_b", "side_a", "side_c"),  # angle_A and angle_C -> side_b between them
        ("angle_B", "angle_C", "side_a", "side_b", "side_c"),  # angle_B and angle_C -> side_a between them
    ]

    # Find which ASA configuration matches
    config = None
    for cfg in asa_configs:
        angle1_attr, angle2_attr, included_side_attr, _, _ = cfg
        angle1 = getattr(triangle, angle1_attr)
        angle2 = getattr(triangle, angle2_attr)
        included_side = getattr(triangle, included_side_attr)

        if angle1.is_known and angle2.is_known and included_side.is_known:
            config = cfg
            break

    if config is None:
        raise ValueError("Cannot solve ASA: no valid ASA configuration found")

    angle1_attr, angle2_attr, included_side_attr, unknown_side1_attr, unknown_side2_attr = config

    angle1 = getattr(triangle, angle1_attr)
    angle2 = getattr(triangle, angle2_attr)
    included_side = getattr(triangle, included_side_attr)
    unknown_side1 = getattr(triangle, unknown_side1_attr)
    unknown_side2 = getattr(triangle, unknown_side2_attr)

    # The third angle is opposite the included side
    # Map: side_a -> angle_A, side_b -> angle_B, side_c -> angle_C
    opposite_angle_map = {
        "side_a": "angle_A",
        "side_b": "angle_B",
        "side_c": "angle_C",
    }
    third_angle_attr = opposite_angle_map[included_side_attr]
    third_angle = getattr(triangle, third_angle_attr)

    # Step 1: Compute the third angle if not already known
    if not third_angle.is_known:
        if angle1.angle is None or angle2.angle is None:
            raise ValueError("Cannot compute third angle: known angles have None values")

        # Third angle = 180° - angle1 - angle2
        angle_sum = angle1.angle + angle2.angle
        third_angle_value = Q(180, "degree") - angle_sum

        # Update the triangle angle
        third_angle.angle = third_angle_value
        third_angle.is_known = True

        # Add a step for angle sum
        angle1_deg = angle1.angle.to_unit.degree
        angle2_deg = angle2.angle.to_unit.degree
        third_angle_deg = third_angle_value.to_unit.degree
        step = SolutionStepBuilder(
            target=f"Third angle ({third_angle_attr})",
            method="Angle Sum",
            description="Calculate third angle using triangle angle sum rule",
            substitution=f"180° - {angle1_deg} - {angle2_deg} = {third_angle_deg}",
        ).build()
        state.solving_steps.append(step)

    # Get the magnitude of the known side
    if included_side.magnitude is ...:
        raise ValueError("ASA requires the included side to have a known magnitude")
    known_side_mag = included_side.magnitude

    # The angle opposite the known side is the third angle (just computed)
    opposite_angle = third_angle.angle
    if opposite_angle is None:
        raise ValueError("Cannot solve ASA: opposite angle is None")

    # Step 2: Use Law of Sines to find each unknown side
    # sin(A)/a = sin(B)/b = sin(C)/c
    # So: unknown_side = known_side * sin(unknown_opposite_angle) / sin(known_opposite_angle)

    # Find unknown_side1 magnitude
    # unknown_side1 is opposite to its corresponding angle
    unknown_side1_opposite_attr = opposite_angle_map[unknown_side1_attr]
    unknown_side1_opposite = getattr(triangle, unknown_side1_opposite_attr)

    if unknown_side1_opposite.angle is None:
        raise ValueError(f"Cannot solve for {unknown_side1_attr}: opposite angle is None")

    # Law of Sines: unknown_side1 / sin(unknown_side1_opposite) = known_side / sin(opposite_angle)
    # unknown_side1 = known_side * sin(unknown_side1_opposite) / sin(opposite_angle)
    los1 = LawOfSines(
        opposite_side=known_side_mag,  # This is used to compute the ratio
        known_angle=opposite_angle,  # Angle opposite to known side
        known_side=known_side_mag,  # The known side
        angle_vector_1=included_side.name or "known",
        angle_vector_2=unknown_side1.name or "unknown1",
        equation_number=1,
    )

    # Use qnty sin function for Quantity arithmetic
    from ...algebra.functions import sin

    sin_unknown_angle = sin(unknown_side1_opposite.angle)
    sin_known_angle = sin(opposite_angle)

    # Law of Sines: unknown_side / sin(unknown_angle) = known_side / sin(known_angle)
    # unknown_side = known_side * sin(unknown_angle) / sin(known_angle)
    unknown_side1_mag = known_side_mag * sin_unknown_angle / sin_known_angle
    unknown_side1_mag.name = f"{unknown_side1.name}_mag"

    # Update the triangle
    unknown_side1.magnitude = unknown_side1_mag
    unknown_side1.is_known = True

    # Create solution step for first unknown side
    unknown_side1_angle_deg = unknown_side1_opposite.angle.to_unit.degree
    opposite_angle_deg = opposite_angle.to_unit.degree
    step1 = SolutionStepBuilder(
        target=f"|{unknown_side1.name}| using Law of Sines",
        method="Law of Sines",
        description=f"Calculate magnitude of {unknown_side1.name}",
        equation_for_list=f"|{unknown_side1.name}|/sin({unknown_side1_opposite_attr}) = |{included_side.name}|/sin({third_angle_attr})",
        substitution=f"|{unknown_side1.name}| = {known_side_mag} × sin({unknown_side1_angle_deg}) / sin({opposite_angle_deg}) = {unknown_side1_mag}",
    ).build()
    state.solving_steps.append(step1)
    state.equations_used.append(f"|{unknown_side1.name}|/sin({unknown_side1_opposite_attr}) = |{included_side.name}|/sin({third_angle_attr})")

    # Step 3: Find unknown_side2 magnitude
    unknown_side2_opposite_attr = opposite_angle_map[unknown_side2_attr]
    unknown_side2_opposite = getattr(triangle, unknown_side2_opposite_attr)

    if unknown_side2_opposite.angle is None:
        raise ValueError(f"Cannot solve for {unknown_side2_attr}: opposite angle is None")

    sin_unknown_angle2 = sin(unknown_side2_opposite.angle)
    unknown_side2_mag = known_side_mag * sin_unknown_angle2 / sin_known_angle
    unknown_side2_mag.name = f"{unknown_side2.name}_mag"

    # Update the triangle
    unknown_side2.magnitude = unknown_side2_mag
    unknown_side2.is_known = True

    # Create solution step for second unknown side
    unknown_side2_angle_deg = unknown_side2_opposite.angle.to_unit.degree
    step2 = SolutionStepBuilder(
        target=f"|{unknown_side2.name}| using Law of Sines",
        method="Law of Sines",
        description=f"Calculate magnitude of {unknown_side2.name}",
        equation_for_list=f"|{unknown_side2.name}|/sin({unknown_side2_opposite_attr}) = |{included_side.name}|/sin({third_angle_attr})",
        substitution=f"|{unknown_side2.name}| = {known_side_mag} × sin({unknown_side2_angle_deg}) / sin({opposite_angle_deg}) = {unknown_side2_mag}",
    ).build()
    state.solving_steps.append(step2)
    state.equations_used.append(f"|{unknown_side2.name}|/sin({unknown_side2_opposite_attr}) = |{included_side.name}|/sin({third_angle_attr})")

    # For ASA, the directions are already known from the input vectors, so we don't need to compute them
    # However, we need to set state.dir_r appropriately if any of the unknown sides is the resultant
    # In ASA, the resultant is typically the known side, so this may not apply

    # Check if any of the unknown sides is a resultant and set dir_r if needed
    for unknown_side in [unknown_side1, unknown_side2]:
        if triangle._is_side_resultant(unknown_side) and unknown_side.direction is not None:
            state.dir_r = unknown_side.direction


# Strategy dispatch table
SOLVING_STRATEGIES = {
    TriangleCase.SAS: solve_sas,
    TriangleCase.SSS: solve_sss,
    TriangleCase.SSA: solve_ssa,
    TriangleCase.ASA: solve_asa,
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
                if hasattr(attr, "_component_vectors"):
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
                if hasattr(attr, "_component_vectors"):
                    vec_copy._component_vectors = attr._component_vectors  # type: ignore[attr-defined]
                # Copy angle direction if present
                if hasattr(attr, "_angle_dir"):
                    vec_copy._angle_dir = attr._angle_dir  # type: ignore[attr-defined]
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
        return {name: vec for name, vec in self.vectors.items() if self._original_vector_states.get(name, True)}

    def get_unknown_variables(self) -> dict[str, Any]:
        """Get unknown variables for report generation."""
        return {name: vec for name, vec in self.vectors.items() if not self._original_vector_states.get(name, True)}

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
        """Update unknown vectors with values from solved state.

        Handles both SAS (single unknown - resultant) and ASA (multiple unknowns - components) cases.
        """
        triangle = state.triangle

        # Find ALL unknown sides that need to be updated
        # A side is unknown if it's a VectorUnknown in our vectors dict
        unknown_sides = []
        for side in [triangle.side_a, triangle.side_b, triangle.side_c]:
            if side.name and side.name in self.vectors:
                vec = self.vectors[side.name]
                if isinstance(vec, VectorUnknown):
                    unknown_sides.append(side)

        if not unknown_sides:
            return  # Nothing to update

        # Update each unknown side
        for unknown_side in unknown_sides:
            name = unknown_side.name
            if name is None:
                continue

            vec = self.vectors.get(name)
            if vec is None or not isinstance(vec, VectorUnknown):
                continue

            # Get solved magnitude from the triangle side
            solved_mag = unknown_side.magnitude if unknown_side.magnitude is not ... else None

            if solved_mag is None:
                continue

            # Get solved angle
            # For ASA cases: the angle was already known from the input vector - use the original relative angle
            # For SAS cases: the direction was computed during solving and stored in state.dir_r
            if vec.angle is not ...:
                # ASA case: angle was known from input, use it directly (it's relative to wrt)
                solved_angle = vec.angle
            elif state.dir_r is not None:
                # SAS case: direction was computed during solving (absolute angle from +x)
                # Convert to relative angle based on wrt axis and angle_dir
                angle_dir = getattr(vec, "_angle_dir", AngleDirection.COUNTERCLOCKWISE)
                solved_angle = get_relative_angle(
                    absolute_angle=state.dir_r,
                    wrt=vec.wrt,
                    coordinate_system=vec.coordinate_system,
                    angle_dir=angle_dir,
                )
            else:
                continue

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
    ) -> dict[str, VectorDTO]:
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
