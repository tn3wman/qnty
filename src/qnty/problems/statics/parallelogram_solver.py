"""
Parallelogram Law Problem Solver - Clean implementation with pattern-based dispatch.

This module provides a solver for vector addition problems using the parallelogram
law (triangle method). It uses a TriangleState model to classify the problem by
known/unknown quantities and dispatches to the appropriate solving strategy.

Key Design Principles:
1. No inheritance from Problem base class - keeps it simple and focused
2. TriangleState models the 6 quantities of the vector triangle
3. Pattern matching on knowns determines which equations to call
4. Standard triangle solving cases: SAS, SSS, ASA, AAS, SSA

Triangle Quantities:
- 3 sides (magnitudes): |F₁|, |F₂|, |F_R|
- 3 interior angles: ∠(F₁,F₂), ∠(F₁,F_R), ∠(F₂,F_R)

Plus direction information for each vector (needed to compute interior angles
and final resultant direction).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

from ...core import Q
from ...equations import AngleBetween, AngleSum, LawOfCosines, LawOfSines

if TYPE_CHECKING:
    from ...core.quantity import Quantity
    from ...spatial.vector import _Vector


# =============================================================================
# Triangle State Model
# =============================================================================


class TriangleCase(Enum):
    """Classification of triangle solving cases based on known quantities."""
    SAS = auto()  # Two sides + included angle → Law of Cosines
    SSS = auto()  # Three sides → Law of Cosines for angles
    ASA = auto()  # Two angles + included side → Angle sum + Law of Sines
    AAS = auto()  # Two angles + non-included side → Angle sum + Law of Sines
    SSA = auto()  # Two sides + non-included angle → Law of Sines (ambiguous)
    UNKNOWN = auto()  # Cannot determine case


@dataclass
class TriangleState:
    """
    Models the state of a vector triangle for parallelogram law solving.

    The triangle has 6 quantities that can be known or unknown:
    - 3 magnitudes: mag_a, mag_b, mag_r (sides of the triangle)
    - 3 interior angles: angle_ab, angle_ar, angle_br

    Additionally, we track vector directions (needed to compute interior angles
    from geometry and to determine the final resultant direction).
    """
    # Vector references
    vec_a: _Vector
    vec_b: _Vector
    vec_r: _Vector

    # Magnitudes (as Quantity or None if unknown)
    mag_a: Quantity | None = None
    mag_b: Quantity | None = None
    mag_r: Quantity | None = None

    # Interior angles of triangle (as Quantity or None if unknown)
    angle_ab: Quantity | None = None  # Angle at vertex opposite to resultant
    angle_ar: Quantity | None = None  # Angle at vertex opposite to vec_b
    angle_br: Quantity | None = None  # Angle at vertex opposite to vec_a

    # Direction info (for computing interior angles and final direction)
    dir_a: float | None = None  # Direction of vec_a in degrees from +x
    dir_b: float | None = None  # Direction of vec_b in degrees from +x
    dir_r: float | None = None  # Direction of resultant in degrees from +x

    # Solution tracking
    solving_steps: list[dict[str, Any]] = field(default_factory=list)
    equations_used: list[str] = field(default_factory=list)

    @property
    def known_sides(self) -> int:
        """Count of known side magnitudes."""
        return sum(1 for m in [self.mag_a, self.mag_b, self.mag_r] if m is not None)

    @property
    def known_angles(self) -> int:
        """Count of known interior angles."""
        return sum(1 for a in [self.angle_ab, self.angle_ar, self.angle_br] if a is not None)

    @property
    def known_directions(self) -> int:
        """Count of known vector directions."""
        return sum(1 for d in [self.dir_a, self.dir_b, self.dir_r] if d is not None)

    def classify(self) -> TriangleCase:
        """
        Classify the triangle case based on known quantities.

        Returns the appropriate TriangleCase for dispatch to solving strategy.
        """
        sides = self.known_sides
        angles = self.known_angles

        # Note: If we have 2 directions, we can compute the included angle (angle_ab)
        # So effectively we can derive angle_ab from dir_a and dir_b
        can_compute_angle_ab = (self.dir_a is not None and self.dir_b is not None)

        if sides == 2 and (angles >= 1 or can_compute_angle_ab):
            # Check if the known angle is the included angle
            if self.angle_ab is not None or can_compute_angle_ab:
                return TriangleCase.SAS
            else:
                return TriangleCase.SSA

        if sides == 3:
            return TriangleCase.SSS

        if angles >= 2 and sides >= 1:
            # Determine if we have ASA or AAS based on which quantities are known
            return TriangleCase.ASA  # Simplified - actual logic would check positions

        return TriangleCase.UNKNOWN


# =============================================================================
# Solving Strategies
# =============================================================================


def solve_sas(state: TriangleState) -> None:
    """
    Solve SAS case: Two sides and included angle known.

    Strategy:
    1. If angle_ab not known, compute from directions (AngleBetween)
    2. Law of Cosines to find unknown side
    3. Law of Sines to find one unknown angle
    4. Angle sum to find the other angle (or compute from third interior angle)
    """
    # Step 1: Compute angle_ab if not already known
    if state.angle_ab is None and state.dir_a is not None and state.dir_b is not None:
        angle_eq = AngleBetween(
            target=f"\\angle(\\vec{{{state.vec_a.name}}}, \\vec{{{state.vec_b.name}}})",
            vec1=state.vec_a,
            vec2=state.vec_b,
        )
        state.angle_ab, step = angle_eq.solve()
        state.solving_steps.append(step)

    if state.angle_ab is None:
        raise ValueError("Cannot solve SAS: included angle (angle_ab) is not known and cannot be computed")

    # Step 2: Use Law of Cosines to find unknown side
    if state.mag_r is None and state.mag_a is not None and state.mag_b is not None:
        # Finding resultant magnitude: c² = a² + b² - 2ab·cos(C)
        state.mag_a.name = f"{state.vec_a.name}_mag"
        state.mag_b.name = f"{state.vec_b.name}_mag"

        loc = LawOfCosines(
            target=f"|\\vec{{{state.vec_r.name}}}| using Eq 1",
            side_a=state.mag_a,
            side_b=state.mag_b,
            angle=state.angle_ab,
        )
        state.mag_r, step = loc.solve()
        state.solving_steps.append(step)
        state.equations_used.append(loc.equation_for_list())

    # Step 3: Use Law of Sines to find angle_ar (angle from vec_a to resultant)
    if state.angle_ar is None and state.mag_b is not None and state.mag_r is not None:
        # Determine if we need obtuse angle
        use_obtuse = state.mag_b.value > state.mag_r.value

        los = LawOfSines(
            target=f"\\angle(\\vec{{{state.vec_a.name}}}, \\vec{{{state.vec_r.name}}}) using Eq 2",
            opposite_side=state.mag_b,
            known_angle=state.angle_ab,
            known_side=state.mag_r,
            use_obtuse=use_obtuse,
        )
        state.angle_ar, step = los.solve()
        state.solving_steps.append(step)
        state.equations_used.append(los.equation_for_list())

    # Step 4: Compute resultant direction from vec_a direction + angle_ar
    if state.dir_r is None and state.dir_a is not None and state.angle_ar is not None:
        dir_a_qty = Q(state.dir_a, 'degree')
        dir_a_qty.name = f"\\angle(\\vec{{x}}, \\vec{{{state.vec_a.name}}})"

        angle_sum = AngleSum(
            target=f"\\angle(\\vec{{x}}, \\vec{{{state.vec_r.name}}}) with respect to +x",
            base_angle=dir_a_qty,
            offset_angle=state.angle_ar,
            result_ref="+x",
        )
        dir_r_qty, step = angle_sum.solve()
        state.dir_r = dir_r_qty.magnitude()
        state.solving_steps.append(step)


def solve_sss(state: TriangleState) -> None:
    """
    Solve SSS case: All three sides known, find angles.

    Strategy:
    1. Law of Cosines to find largest angle (opposite longest side)
    2. Law of Sines for second angle
    3. Third angle = 180° - first - second
    """
    if state.mag_a is None or state.mag_b is None or state.mag_r is None:
        raise ValueError("SSS requires all three magnitudes to be known")

    # Find the largest side to get the largest angle first
    # This avoids ambiguity in Law of Sines
    mags = [
        (state.mag_a.value, 'a', state.angle_br),  # angle opposite to a
        (state.mag_b.value, 'b', state.angle_ar),  # angle opposite to b
        (state.mag_r.value, 'r', state.angle_ab),  # angle opposite to r
    ]
    mags.sort(key=lambda x: x[0], reverse=True)

    # Use Law of Cosines for largest angle
    # cos(C) = (a² + b² - c²) / (2ab)
    # This requires a modified form - for now, use the standard form
    # TODO: Implement Law of Cosines for finding angles

    raise NotImplementedError("SSS case not yet implemented")


def solve_ssa(state: TriangleState) -> None:
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
    2. Builds a TriangleState from the vectors
    3. Classifies the problem (SAS, SSS, etc.)
    4. Dispatches to the appropriate solving strategy
    5. Collects step-by-step solutions for reporting

    Example:
        >>> from qnty.problems.statics import parallelogram_law as pl
        >>>
        >>> class MyProblem(ParallelogramLawProblem):
        ...     F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        ...     F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        ...     F_R = pl.create_vector_resultant(F_1, F_2)
        >>>
        >>> problem = MyProblem()
        >>> problem.solve()
        >>> problem.generate_report("report.pdf", format="pdf")
    """

    name: str = "Parallelogram Law Problem"

    def __init__(self, name: str | None = None, description: str = ""):
        self.name = name or getattr(self.__class__, "name", self.__class__.__name__)
        self.description = description

        # Storage
        self.forces: dict[str, _Vector] = {}
        self._output_unit = "N"
        self._original_force_states: dict[str, bool] = {}

        # For compatibility with report generator
        self.variables: dict[str, Quantity] = {}
        self._original_variable_states: dict[str, bool] = {}

        # Solving state
        self.is_solved = False
        self.solving_history: list[dict[str, Any]] = []
        self._equations_used: list[str] = []
        self._triangle_state: TriangleState | None = None

        # Extract vectors from class attributes
        self._extract_vectors()

    def _extract_vectors(self) -> None:
        """Extract vector objects defined at class level and create variables for reporting."""
        from ...spatial.vector import _Vector
        from ...spatial.vectors import _VectorWithUnknowns

        vector_clones: dict[int, _Vector] = {}

        # First pass: clone all plain _Vectors (known vectors)
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, _Vector) and not isinstance(attr, _VectorWithUnknowns):
                clone = attr.clone(name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
                self.forces[attr_name] = clone
                self._original_force_states[attr_name] = True
                self._create_vector_variables(attr_name, clone, is_known=True)

        # Second pass: clone _VectorWithUnknowns (may reference other vectors)
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, _VectorWithUnknowns):
                clone = attr.clone(name=attr_name, vector_clones=vector_clones)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
                self.forces[attr_name] = clone
                self._original_force_states[attr_name] = False
                self._create_vector_variables(attr_name, clone, is_known=False)

    def _create_vector_variables(self, name: str, vec: _Vector, is_known: bool) -> None:
        """Create magnitude and angle Quantity variables for reporting compatibility."""
        # Magnitude
        if is_known and vec.magnitude is not None:
            mag_qty = vec.magnitude
            mag_qty.name = f"{name}_mag"
        else:
            mag_qty = Q(0, self._output_unit)
            mag_qty.name = f"{name}_mag"
            mag_qty.value = None

        self.variables[f"{name}_mag"] = mag_qty
        self._original_variable_states[f"{name}_mag"] = is_known

        # Angle
        if is_known:
            original_angle = getattr(vec, "_original_angle", None)
            if original_angle is not None:
                angle_qty = Q(original_angle, 'degree')
                angle_qty.name = f"{name}_angle"
            else:
                angle_qty = Q(0, 'degree')
                angle_qty.name = f"{name}_angle"
                angle_qty.value = None
        else:
            angle_qty = Q(0, 'degree')
            angle_qty.name = f"{name}_angle"
            angle_qty.value = None

        self.variables[f"{name}_angle"] = angle_qty
        self._original_variable_states[f"{name}_angle"] = is_known

    def get_known_variables(self) -> dict[str, Any]:
        """Get known variables for report generation."""
        return {name: vec for name, vec in self.forces.items()
                if self._original_force_states.get(name, True)}

    def get_unknown_variables(self) -> dict[str, Any]:
        """Get unknown variables for report generation."""
        return {name: vec for name, vec in self.forces.items()
                if not self._original_force_states.get(name, True)}

    def _build_triangle_state(self) -> TriangleState:
        """Build TriangleState from the extracted vectors."""
        components = []
        resultant = None

        for vec in self.forces.values():
            if getattr(vec, "is_resultant", False):
                resultant = vec
            else:
                components.append(vec)

        if len(components) != 2:
            raise ValueError(f"Expected 2 component vectors, got {len(components)}")
        if resultant is None:
            raise ValueError("No resultant vector found")

        vec_a, vec_b = components

        # Build state from vectors
        state = TriangleState(
            vec_a=vec_a,
            vec_b=vec_b,
            vec_r=resultant,
        )

        # Populate magnitudes
        if vec_a.magnitude is not None and vec_a.is_known:
            state.mag_a = vec_a.magnitude
        if vec_b.magnitude is not None and vec_b.is_known:
            state.mag_b = vec_b.magnitude
        if resultant.magnitude is not None and resultant.is_known:
            state.mag_r = resultant.magnitude

        # Populate directions
        state.dir_a = getattr(vec_a, '_original_angle', None)
        state.dir_b = getattr(vec_b, '_original_angle', None)
        state.dir_r = getattr(resultant, '_original_angle', None)

        return state

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

        # Build triangle state
        state = self._build_triangle_state()
        self._triangle_state = state

        # Classify the problem
        case = state.classify()

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

    def _update_resultant_from_state(self, state: TriangleState) -> None:
        """Update the resultant vector with values from solved state."""
        from ...algebra.functions import cos, sin
        from ...core.unit import ureg

        vr = state.vec_r
        force_unit = ureg.resolve(self._output_unit)

        if state.mag_r is not None and state.dir_r is not None:
            mag_r = state.mag_r.magnitude()
            theta_r = state.dir_r

            # Compute components
            theta_r_qty = Q(theta_r, 'degree')
            x_r = mag_r * cos(theta_r_qty).magnitude()
            y_r = mag_r * sin(theta_r_qty).magnitude()

            # Store in SI units
            vr._coords[0] = x_r * force_unit.si_factor
            vr._coords[1] = y_r * force_unit.si_factor
            vr._coords[2] = 0.0

            # Store for reporting
            vr._original_angle = theta_r
            vr._original_wrt = "+x"
            vr.is_known = True

            if hasattr(vr, "_unknowns"):
                vr._unknowns.clear()

            # Update variables for report
            vr_name = vr.name
            if f"{vr_name}_mag" in self.variables:
                self.variables[f"{vr_name}_mag"] = state.mag_r
            if f"{vr_name}_angle" in self.variables:
                dir_r_qty = Q(theta_r, 'degree')
                dir_r_qty.name = f"{vr_name}_angle"
                self.variables[f"{vr_name}_angle"] = dir_r_qty

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


def solve_class(problem_class: type, output_unit: str = "N") -> ParallelogramLawProblem:
    """
    Solve a parallelogram law problem defined as a class.

    Args:
        problem_class: Class with vector attributes
        output_unit: Unit for output values

    Returns:
        Solved ParallelogramLawProblem instance
    """
    from ...spatial.vector import _Vector
    from ...spatial.vectors import _VectorWithUnknowns

    # Create dynamic problem class
    class DynamicProblem(ParallelogramLawProblem):
        pass

    DynamicProblem.name = getattr(problem_class, "name", problem_class.__name__)

    # Copy vector attributes
    for attr_name in dir(problem_class):
        if attr_name.startswith("_"):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, _Vector | _VectorWithUnknowns):
            setattr(DynamicProblem, attr_name, attr)

    # Create and solve
    problem = DynamicProblem()
    problem.solve(output_unit=output_unit)
    return problem
