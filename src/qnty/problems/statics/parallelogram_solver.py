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

from ...algebra.functions import asin, sin
from ...core import Q
from ...equations import AngleSum, LawOfCosines, LawOfSines
from ...equations.angle_finder import get_relative_angle
from ...equations.base import SolutionStepBuilder, format_angle, latex_name
from ...geometry.triangle import Triangle, TriangleCase, from_vectors_dynamic
from ...linalg.vector2 import Vector, VectorUnknown
from ...spatial.angle_reference import AngleDirection

if TYPE_CHECKING:
    from ...core.quantity import Quantity
    from ...linalg.vector2 import VectorDTO


# =============================================================================
# Helper Functions for Vector Sign Correction
# =============================================================================


def _compute_component_signs(
    resultant_mag: float,
    resultant_dir: float,
    comp1_mag: float,
    comp1_dir: float,
    comp2_mag: float,
    comp2_dir: float,
) -> tuple[float, float]:
    """
    Determine the correct signs for component magnitudes in vector addition.

    Given R = A + B where we know |R|, θ_R, |A|, θ_A, |B|, θ_B (all directions
    in absolute degrees), verify that the components add up correctly. If not,
    flip the sign of one or both components.

    This handles cases where the resultant is "outside" the angular span of
    the two component directions, requiring one component to point opposite
    to its reference direction (negative magnitude).

    Args:
        resultant_mag: Magnitude of the resultant vector
        resultant_dir: Absolute direction of the resultant (degrees)
        comp1_mag: Magnitude of first component (always positive from Law of Sines)
        comp1_dir: Absolute direction of first component (degrees)
        comp2_mag: Magnitude of second component (always positive from Law of Sines)
        comp2_dir: Absolute direction of second component (degrees)

    Returns:
        Tuple of (corrected_comp1_mag, corrected_comp2_mag) with appropriate signs
    """
    import math

    def to_radians(deg: float) -> float:
        return math.radians(deg)

    # Compute expected resultant from components with current signs
    def compute_resultant(c1_mag: float, c1_dir: float, c2_mag: float, c2_dir: float) -> tuple[float, float]:
        rx = c1_mag * math.cos(to_radians(c1_dir)) + c2_mag * math.cos(to_radians(c2_dir))
        ry = c1_mag * math.sin(to_radians(c1_dir)) + c2_mag * math.sin(to_radians(c2_dir))
        r_mag = math.sqrt(rx**2 + ry**2)
        r_dir = math.degrees(math.atan2(ry, rx)) % 360
        return r_mag, r_dir

    # Target values
    target_mag = resultant_mag
    target_dir = resultant_dir % 360

    # Try all four sign combinations and find the one that matches
    sign_combos = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    best_combo = (1, 1)
    best_error = float("inf")

    for s1, s2 in sign_combos:
        r_mag, r_dir = compute_resultant(s1 * comp1_mag, comp1_dir, s2 * comp2_mag, comp2_dir)

        # Compute error (magnitude error + direction error)
        mag_error = abs(r_mag - target_mag) / max(target_mag, 1e-10)

        # Direction error (handle wraparound)
        dir_diff = abs(r_dir - target_dir)
        if dir_diff > 180:
            dir_diff = 360 - dir_diff
        dir_error = dir_diff / 180  # Normalize to [0, 1]

        total_error = mag_error + dir_error

        if total_error < best_error:
            best_error = total_error
            best_combo = (s1, s2)

    return (best_combo[0] * comp1_mag, best_combo[1] * comp2_mag)


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

    # Angle direction preference for resultant (CCW or CW)
    result_angle_dir: AngleDirection = AngleDirection.COUNTERCLOCKWISE

    # Vector reference axes (wrt) - maps vector name to its reference axis (e.g., "+y", "-x")
    vector_references: dict[str, str] = field(default_factory=dict)

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
    2. Generate step showing how the included angle was computed (from vector directions)
    3. Law of Cosines to find the unknown side magnitude
    4. Law of Sines to find an interior angle at a vertex adjacent to the unknown side
    5. Use vertex geometry to compute the unknown side's direction
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

    # Step 1: Generate step showing how the included angle was determined
    # This shows the user that the angle comes from the vector directions
    included_angle_step = triangle.get_included_angle_step(included_angle)
    if included_angle_step is not None:
        state.solving_steps.append(included_angle_step)

    # Step 2: Use Law of Cosines to find unknown side magnitude
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

    # Determine if we need obtuse angle using the "largest angle opposite longest side" rule.
    # In Law of Sines, when sin(A) = k has two solutions (acute and obtuse), we choose:
    # - Obtuse if the side opposite to angle A is the LONGEST side of the triangle
    # - Acute otherwise (the more common case)
    #
    # This is because in any triangle, the largest interior angle is always opposite
    # the longest side. So the angle is obtuse only if its opposite side is longest.

    # Find the third known side magnitude (the one that's not opposite_side or unknown_side)
    third_side_mag = None
    for side in [known_side_1, known_side_2]:
        if side is not opposite_side:
            third_side_mag = side.magnitude
            break

    if third_side_mag is None or third_side_mag is ...:
        # Fallback to original heuristic if we can't find third side
        use_obtuse = mag_opposite > mag_unknown
    else:
        # Use obtuse only if the opposite side is the longest in the triangle
        all_mags = [mag_opposite.magnitude(), mag_unknown.magnitude(), third_side_mag.magnitude()]
        use_obtuse = mag_opposite.magnitude() == max(all_mags)

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
                # Determine operation: compare computed_dir with base + offset and base - offset
                # to see which one matches the actual computed direction
                base_dir = adjacent_known_side.direction
                computed_dir_val = computed_dir.to_unit.degree.magnitude()
                base_val = base_dir.to_unit.degree.magnitude()
                offset_val = solved_angle.to_unit.degree.magnitude()

                # Normalize angles to [0, 360) for comparison
                def normalize(x: float) -> float:
                    return x % 360

                add_result = normalize(base_val + offset_val)
                sub_result = normalize(base_val - offset_val)
                computed_norm = normalize(computed_dir_val)

                # Determine which operation was used (with tolerance for floating point)
                add_diff = min(abs(add_result - computed_norm), abs(add_result - computed_norm + 360), abs(add_result - computed_norm - 360))
                sub_diff = min(abs(sub_result - computed_norm), abs(sub_result - computed_norm + 360), abs(sub_result - computed_norm - 360))

                operation = "-" if sub_diff < add_diff else "+"

                # Get the reference axis from the vector_references map
                result_ref = state.vector_references.get(unknown_side.name, "+x")

                # AngleSum handles LaTeX formatting internally and returns normalized angle
                angle_sum = AngleSum(
                    base_angle=adjacent_known_side.direction,
                    offset_angle=solved_angle,
                    result_vector_name=unknown_side.name,
                    base_vector_name=adjacent_known_side.name,
                    offset_vector_1=adjacent_known_side.name,
                    offset_vector_2=unknown_side.name,
                    result_ref=result_ref,
                    operation=operation,
                    angle_dir=state.result_angle_dir,
                )
                normalized_dir, step = angle_sum.solve()
                state.solving_steps.append(step)
                # Update dir_r with the normalized angle (0° to 360°)
                state.dir_r = normalized_dir
            else:
                # Fallback: simple step using SolutionStepBuilder directly
                from ...equations.base import SolutionStepBuilder, latex_name

                # Get the reference axis from the vector_references map
                ref_wrt = state.vector_references.get(unknown_side.name, "+x")
                ref_axis = ref_wrt.lstrip("+-")

                result_name = latex_name(unknown_side.name)
                computed_dir_deg = computed_dir.to_unit.degree
                step = SolutionStepBuilder(
                    target=f"\\angle({ref_axis}, \\vec{{{result_name}}}) with respect to {ref_wrt}",
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


def solve_ssa(state: SolvingState) -> None:
    """
    Solve SSA case: Two sides and non-included angle known.

    This is the ambiguous case - may have 0, 1, or 2 solutions.

    In parallelogram law problems, SSA occurs when:
    - Two component magnitudes are known (e.g., F_A and F_B magnitudes)
    - One component's direction is unknown (e.g., F_A angle)
    - The resultant's direction is known but magnitude is unknown
    - This gives us one interior angle (between the two vectors with known directions)

    For Problem 2-12:
        - F_A: magnitude=8000 N, angle=unknown
        - F_B: magnitude=6000 N, angle=40° wrt -y (known)
        - F_R: magnitude=unknown, angle=0° wrt +x (known)
        - angle_C = 50° (between F_B and F_R directions)

    Strategy:
    1. Use Law of Sines to find the unknown angle (opposite one of the known sides)
       sin(A)/|F_B| = sin(C)/|F_A|  where C is the known angle opposite F_A
    2. Handle the ambiguous case: sin(A) has two solutions (acute and obtuse)
       - Pick the solution that gives a valid triangle (all angles positive, sum = 180°)
       - Use "largest angle opposite longest side" rule to verify
    3. Compute the third angle: angle_B = 180° - angle_A - angle_C
    4. Use Law of Sines to find the unknown side magnitude (F_R)
       |F_R|/sin(B) = |F_A|/sin(C)
    5. Compute the unknown side's direction using vertex geometry
    """
    triangle = state.triangle

    # Find the SSA configuration
    # We have: 2 known sides + 1 known angle (not between the known sides)

    # First, identify the known angle and its opposite side
    known_angle_info = None
    for angle_attr in ["angle_A", "angle_B", "angle_C"]:
        angle = getattr(triangle, angle_attr)
        if angle.is_known and angle.angle is not None:
            known_angle_info = (angle_attr, angle)
            break

    if known_angle_info is None:
        raise ValueError("SSA requires one known angle")

    known_angle_attr, known_angle = known_angle_info
    known_angle_value = known_angle.angle

    # Find the side opposite to the known angle
    opposite_side_map = {"angle_A": "side_a", "angle_B": "side_b", "angle_C": "side_c"}
    opposite_side_attr = opposite_side_map[known_angle_attr]
    opposite_side = getattr(triangle, opposite_side_attr)

    # Find the other known side (not opposite to the known angle)
    other_known_side = None
    other_known_side_attr = None
    for side_attr in ["side_a", "side_b", "side_c"]:
        if side_attr == opposite_side_attr:
            continue
        side = getattr(triangle, side_attr)
        if side.is_known and side.magnitude is not ...:
            other_known_side = side
            other_known_side_attr = side_attr
            break

    if other_known_side is None:
        raise ValueError("SSA requires two known sides")

    # Find the unknown side
    unknown_side = None
    unknown_side_attr = None
    for side_attr in ["side_a", "side_b", "side_c"]:
        side = getattr(triangle, side_attr)
        if not side.is_known or side.magnitude is ...:
            unknown_side = side
            unknown_side_attr = side_attr
            break

    if unknown_side is None:
        raise ValueError("SSA: could not find unknown side")

    # Get magnitudes
    if opposite_side.magnitude is ...:
        raise ValueError("SSA: opposite side magnitude is unknown")

    opp_mag = opposite_side.magnitude  # side opposite to known angle
    other_mag = other_known_side.magnitude  # the other known side

    # Step 1: Use Law of Sines to find the angle opposite to the other known side
    # sin(unknown_angle) / other_mag = sin(known_angle) / opp_mag
    # unknown_angle = asin(other_mag * sin(known_angle) / opp_mag)
    sin_known = sin(known_angle_value)
    sin_unknown = other_mag * sin_known / opp_mag

    # Clamp to valid range for asin
    sin_val = sin_unknown.value
    if sin_val is not None and abs(sin_val) > 1.0:
        if sin_val > 1.0:
            sin_unknown = Q(1.0, "dimensionless")
        else:
            sin_unknown = Q(-1.0, "dimensionless")

    # Get the acute angle solution
    acute_angle = asin(sin_unknown).to_unit.degree
    obtuse_angle = Q(180, "degree") - acute_angle

    # Determine which solution is valid
    # Both solutions must give positive third angle (180 - known - found > 0)
    acute_third = Q(180, "degree") - known_angle_value - acute_angle
    obtuse_third = Q(180, "degree") - known_angle_value - obtuse_angle

    # Pick the solution that gives a valid (positive) third angle
    # If both are valid, use the one consistent with largest-angle-opposite-longest-side
    solved_angle = None

    acute_third_val = acute_third.to_unit.degree.magnitude()
    obtuse_third_val = obtuse_third.to_unit.degree.magnitude()

    if acute_third_val > 0 and obtuse_third_val <= 0:
        solved_angle = acute_angle
        third_angle = acute_third
    elif obtuse_third_val > 0 and acute_third_val <= 0:
        solved_angle = obtuse_angle
        third_angle = obtuse_third
    elif acute_third_val > 0 and obtuse_third_val > 0:
        # Both valid - use geometric verification
        # The largest angle should be opposite the longest side
        # We'll use the acute solution by default (more common case)
        solved_angle = acute_angle
        third_angle = acute_third
    else:
        raise ValueError("SSA: No valid triangle solution found")

    # Find the angle attribute for the solved angle (opposite to other_known_side)
    angle_opposite_map = {"side_a": "angle_A", "side_b": "angle_B", "side_c": "angle_C"}
    assert other_known_side_attr is not None, "other_known_side_attr should not be None at this point"
    solved_angle_attr = angle_opposite_map[other_known_side_attr]
    solved_triangle_angle = getattr(triangle, solved_angle_attr)

    # Find the angle attribute for the third angle (opposite to unknown_side)
    assert unknown_side_attr is not None, "unknown_side_attr should not be None at this point"
    third_angle_attr = angle_opposite_map[unknown_side_attr]
    third_triangle_angle = getattr(triangle, third_angle_attr)

    # Use LawOfSines class for the angle computation
    # Determine use_obtuse based on our earlier analysis
    use_obtuse_for_los = solved_angle == (Q(180, "degree") - asin(sin_unknown).to_unit.degree)

    # The solved angle is opposite to other_known_side.
    # Find the two sides adjacent to the solved angle's vertex (i.e., the sides that form this angle)
    # The angle opposite to other_known_side is at the vertex where the OTHER two sides meet.
    # For angle_A (opposite side_a/F_B): adjacent sides are side_b (F_R) and side_c (F_A)
    # For angle_B (opposite side_b/F_R): adjacent sides are side_a (F_B) and side_c (F_A)
    # For angle_C (opposite side_c/F_A): adjacent sides are side_a (F_B) and side_b (F_R)
    adjacent_sides_map = {
        "side_a": ("side_b", "side_c"),  # angle_A is formed by F_R and F_A
        "side_b": ("side_a", "side_c"),  # angle_B is formed by F_B and F_A
        "side_c": ("side_a", "side_b"),  # angle_C is formed by F_B and F_R
    }
    adj_side_attrs = adjacent_sides_map[other_known_side_attr]
    adj_side_1 = getattr(triangle, adj_side_attrs[0])
    adj_side_2 = getattr(triangle, adj_side_attrs[1])

    los_angle = LawOfSines(
        opposite_side=other_mag,
        known_angle=known_angle_value,
        known_side=opp_mag,
        angle_vector_1=adj_side_1.name or "V1",
        angle_vector_2=adj_side_2.name or "V2",
        equation_number=1,
        use_obtuse=use_obtuse_for_los,
        solve_for="angle",
    )
    # Call solve() to get the step dict (result matches our solved_angle)
    _, step = los_angle.solve()
    state.solving_steps.append(step)
    state.equations_used.append(los_angle.equation_for_list())

    # Update triangle with solved angle
    solved_triangle_angle.angle = solved_angle
    solved_triangle_angle.is_known = True

    # Step 2: Compute the direction of the side with unknown direction
    # This comes right after finding the interior angle, as it's what the user wants to know
    # Find which side has unknown direction but known magnitude
    side_with_unknown_dir = None
    for side_attr in ["side_a", "side_b", "side_c"]:
        side = getattr(triangle, side_attr)
        if side.direction is None and side.is_known:
            side_with_unknown_dir = side
            break

    if side_with_unknown_dir is not None:
        # Use compute_unknown_direction with the angle we just solved
        computed_dir = triangle.compute_unknown_direction(side_with_unknown_dir, solved_triangle_angle)
        if computed_dir is not None:
            side_with_unknown_dir.direction = computed_dir

            # Update state.dir_r
            if triangle._is_side_resultant(side_with_unknown_dir):
                state.dir_r = computed_dir
            else:
                state.dir_r = computed_dir

            # Find the adjacent side with known direction at the same vertex as the solved angle
            # The solved angle is at a vertex where two sides meet - we want the OTHER side
            # (not side_with_unknown_dir) that has a known direction
            adjacent_known_side = None
            angle_vertex = solved_triangle_angle.vertex
            for side_attr in ["side_a", "side_b", "side_c"]:
                side = getattr(triangle, side_attr)
                if side != side_with_unknown_dir and side.direction is not None:
                    # Check if this side is at the same vertex as the solved angle
                    if side.start == angle_vertex or side.end == angle_vertex:
                        adjacent_known_side = side
                        break

            if adjacent_known_side is not None:
                # Get the reference axis from the vector_references map
                result_ref = state.vector_references.get(side_with_unknown_dir.name, "+x")
                ref_axis = result_ref.lstrip("+-")

                # For SSA case, the user typically wants to see:
                # angle(ref_axis, F_A) = 90° - angle(F_R, F_A)
                # This is because F_R is along +x, and +y is 90° from +x
                result_name = latex_name(side_with_unknown_dir.name or "V")
                adj_name = latex_name(adjacent_known_side.name or "V")
                solved_deg = solved_angle.to_unit.degree

                # Compute the final angle relative to the user's reference axis
                # For +y reference: angle from +y = 90° - interior_angle (for acute angles)
                # For +x reference: angle from +x = interior_angle (when base is at 0°)
                base_val = adjacent_known_side.direction.to_unit.degree.magnitude()

                if ref_axis.lower() == "y":
                    # Show calculation as: 90° - interior_angle
                    result_angle = 90.0 - solved_deg.magnitude()
                    step = SolutionStepBuilder(
                        target=f"\\angle({ref_axis}, \\vec{{{result_name}}}) with respect to {result_ref}",
                        method="Geometry",
                        description=f"Compute direction of {side_with_unknown_dir.name} from interior angle",
                        substitution=f"\\angle({ref_axis}, \\vec{{{result_name}}}) &= 90^{{\\circ}} - \\angle(\\vec{{{adj_name}}}, \\vec{{{result_name}}}) \\\\\n&= 90^{{\\circ}} - {format_angle(solved_deg, precision=1)} \\\\\n&= {result_angle:.1f}^{{\\circ}} \\\\",
                    )
                    state.solving_steps.append(step.build())
                else:
                    # Use AngleSum for other reference axes
                    # Determine operation: compare computed_dir with base + offset and base - offset
                    computed_dir_val = computed_dir.to_unit.degree.magnitude()
                    offset_val = solved_deg.magnitude()

                    # Normalize angles to [0, 360) for comparison
                    def normalize(x: float) -> float:
                        return x % 360

                    add_result = normalize(base_val + offset_val)
                    sub_result = normalize(base_val - offset_val)
                    computed_norm = normalize(computed_dir_val)

                    # Determine which operation was used (with tolerance for floating point)
                    add_diff = min(abs(add_result - computed_norm), abs(add_result - computed_norm + 360), abs(add_result - computed_norm - 360))
                    sub_diff = min(abs(sub_result - computed_norm), abs(sub_result - computed_norm + 360), abs(sub_result - computed_norm - 360))

                    operation = "-" if sub_diff < add_diff else "+"

                    # AngleSum handles LaTeX formatting internally and returns normalized angle
                    angle_sum = AngleSum(
                        base_angle=adjacent_known_side.direction,
                        offset_angle=solved_angle,
                        result_vector_name=side_with_unknown_dir.name,
                        base_vector_name=adjacent_known_side.name,
                        offset_vector_1=adjacent_known_side.name,
                        offset_vector_2=side_with_unknown_dir.name,
                        result_ref=result_ref,
                        operation=operation,
                        angle_dir=state.result_angle_dir,
                    )
                    normalized_dir, step = angle_sum.solve()
                    state.solving_steps.append(step)
                    # Update dir_r with the normalized angle
                    state.dir_r = normalized_dir
            else:
                # Fallback: simple step if no adjacent known side found
                result_name = latex_name(side_with_unknown_dir.name or "V")
                computed_dir_deg = computed_dir.to_unit.degree

                ref_wrt = state.vector_references.get(side_with_unknown_dir.name, "+x")
                ref_axis = ref_wrt.lstrip("+-")

                step = SolutionStepBuilder(
                    target=f"\\angle({ref_axis}, \\vec{{{result_name}}}) with respect to {ref_wrt}",
                    method="Geometry",
                    description=f"Compute direction of {side_with_unknown_dir.name} from interior angle",
                    substitution=f"\\theta = {format_angle(computed_dir_deg, precision=1)}",
                )
                state.solving_steps.append(step.build())

    # Step 3: Compute the third angle (interior angle opposite the unknown side)
    third_triangle_angle.angle = third_angle
    third_triangle_angle.is_known = True

    known_angle_deg = known_angle_value.to_unit.degree
    third_deg = third_angle.to_unit.degree
    solved_deg = solved_angle.to_unit.degree

    # Build a more descriptive target for the angle sum step
    angle_sum_target = f"Interior angle opposite {unknown_side.name or 'unknown side'}"

    step = SolutionStepBuilder(
        target=angle_sum_target,
        method="Angle Sum",
        description="Calculate interior angle using triangle angle sum rule",
        substitution=f"180° - {format_angle(known_angle_deg, precision=1)} - {format_angle(solved_deg, precision=1)} = {format_angle(third_deg, precision=1)}",
    )
    state.solving_steps.append(step.build())

    # Step 4: Use Law of Cosines to find the unknown side magnitude
    # This matches the textbook approach: c² = a² + b² - 2ab·cos(C)
    # where C is the angle opposite the unknown side (third_angle)

    loc = LawOfCosines(
        side_a=opp_mag,
        side_b=other_mag,
        angle=third_angle,
        result_vector_name=unknown_side.name,
        equation_number=2,
    )
    unknown_mag, step = loc.solve()
    state.solving_steps.append(step)
    state.equations_used.append(loc.equation_for_list())

    # Preserve unit from known side
    if hasattr(opp_mag, "preferred") and opp_mag.preferred is not None:
        unknown_mag.preferred = opp_mag.preferred

    unknown_mag.name = f"{unknown_side.name}_mag"

    # Update triangle with unknown side magnitude
    unknown_side.magnitude = unknown_mag
    unknown_side.is_known = True


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
    # a/sin(A) = b/sin(B) = c/sin(C)
    # So: unknown_side = known_side * sin(unknown_opposite_angle) / sin(known_opposite_angle)

    # The known angle (third_angle) is formed by the two unknown sides
    # So known_angle_vectors = (unknown_side1.name, unknown_side2.name)
    known_angle_vectors = (unknown_side1.name or "unknown1", unknown_side2.name or "unknown2")

    # Find unknown_side1 magnitude
    # unknown_side1 is opposite to its corresponding angle
    unknown_side1_opposite_attr = opposite_angle_map[unknown_side1_attr]
    unknown_side1_opposite = getattr(triangle, unknown_side1_opposite_attr)

    if unknown_side1_opposite.angle is None:
        raise ValueError(f"Cannot solve for {unknown_side1_attr}: opposite angle is None")

    # Use LawOfSines with solve_for="side"
    # angle_vector_1 and angle_vector_2 specify the angle opposite to the unknown side (unknown_side1)
    # This angle is formed by included_side and unknown_side2
    los1 = LawOfSines(
        opposite_side=known_side_mag,  # Not used for side mode, but kept for API compatibility
        known_angle=opposite_angle,  # Angle opposite to known side
        known_side=known_side_mag,  # The known side
        angle_vector_1=unknown_side2.name or "unknown2",
        angle_vector_2=included_side.name or "known",
        equation_number=1,
        solve_for="side",
        unknown_angle=unknown_side1_opposite.angle,
        result_vector_name=unknown_side1.name,
        known_angle_vectors=known_angle_vectors,
    )

    unknown_side1_mag, step1 = los1.solve()

    # Update the triangle
    unknown_side1.magnitude = unknown_side1_mag
    unknown_side1.is_known = True

    state.solving_steps.append(step1)
    state.equations_used.append(los1.equation_for_list())

    # Step 3: Find unknown_side2 magnitude
    unknown_side2_opposite_attr = opposite_angle_map[unknown_side2_attr]
    unknown_side2_opposite = getattr(triangle, unknown_side2_opposite_attr)

    if unknown_side2_opposite.angle is None:
        raise ValueError(f"Cannot solve for {unknown_side2_attr}: opposite angle is None")

    # angle_vector_1 and angle_vector_2 specify the angle opposite to the unknown side (unknown_side2)
    # This angle is formed by included_side and unknown_side1
    los2 = LawOfSines(
        opposite_side=known_side_mag,
        known_angle=opposite_angle,
        known_side=known_side_mag,
        angle_vector_1=unknown_side1.name or "unknown1",
        angle_vector_2=included_side.name or "known",
        equation_number=2,
        solve_for="side",
        unknown_angle=unknown_side2_opposite.angle,
        result_vector_name=unknown_side2.name,
        known_angle_vectors=known_angle_vectors,
    )

    unknown_side2_mag, step2 = los2.solve()

    state.solving_steps.append(step2)
    state.equations_used.append(los2.equation_for_list())

    # Sign correction for vector components
    # Law of Sines always returns positive magnitudes, but in some geometries
    # a component may need to be negative (pointing opposite to its reference direction)
    # This happens when the resultant is "outside" the angular span of the components

    # Get the absolute directions of all three sides
    # TriangleSide has .direction attribute (absolute direction as Quantity)
    if included_side.direction is None or unknown_side1.direction is None or unknown_side2.direction is None:
        # Can't apply sign correction without directions - just use positive magnitudes
        unknown_side1.magnitude = unknown_side1_mag
        unknown_side1.is_known = True
        unknown_side2.magnitude = unknown_side2_mag
        unknown_side2.is_known = True
        return

    resultant_dir = included_side.direction.to_unit.degree.magnitude()
    resultant_mag_val = known_side_mag.magnitude()

    comp1_dir = unknown_side1.direction.to_unit.degree.magnitude()
    comp1_mag_val = unknown_side1_mag.magnitude()

    comp2_dir = unknown_side2.direction.to_unit.degree.magnitude()
    comp2_mag_val = unknown_side2_mag.magnitude()

    # Compute corrected signs
    corrected_comp1, corrected_comp2 = _compute_component_signs(
        resultant_mag_val, resultant_dir,
        comp1_mag_val, comp1_dir,
        comp2_mag_val, comp2_dir,
    )

    # Apply sign corrections if needed
    if corrected_comp1 < 0:
        # Need to create a new quantity with negative value
        unknown_side1_mag = Q(corrected_comp1, unknown_side1_mag.preferred.symbol if unknown_side1_mag.preferred else "N")
        unknown_side1_mag.name = f"{unknown_side1.name}_mag"

    if corrected_comp2 < 0:
        unknown_side2_mag = Q(corrected_comp2, unknown_side2_mag.preferred.symbol if unknown_side2_mag.preferred else "N")
        unknown_side2_mag.name = f"{unknown_side2.name}_mag"

    # Update the triangle with corrected magnitudes
    unknown_side1.magnitude = unknown_side1_mag
    unknown_side1.is_known = True
    unknown_side2.magnitude = unknown_side2_mag
    unknown_side2.is_known = True

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

                # VectorUnknown is known only if BOTH magnitude AND angle are known
                # (not ellipsis and have a value)
                mag_known = attr.magnitude is not ... and attr.magnitude.value is not None
                angle_known = attr.angle is not ...
                is_known = mag_known and angle_known
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
        """Create variables for VectorUnknown (may have ellipsis values).

        Note: is_known indicates if the whole vector is known, but individual
        components (magnitude, angle) can be known even if the vector is "unknown".
        For example, a vector with unknown magnitude but known angle=0.
        """
        # Magnitude - known if not ellipsis and has a value
        if vec.magnitude is not ...:
            mag_qty = vec.magnitude
            mag_qty.name = f"{name}_mag"
            self.variables[f"{name}_mag"] = mag_qty
            # Magnitude is known if it has a concrete value
            mag_is_known = mag_qty.value is not None
            self._original_variable_states[f"{name}_mag"] = mag_is_known
        else:
            # Ellipsis means unknown
            self._original_variable_states[f"{name}_mag"] = False

        # Angle - known if not ellipsis and has a value
        if vec.angle is not ...:
            angle_qty = vec.angle
            angle_qty.name = f"{name}_angle"
            self.variables[f"{name}_angle"] = angle_qty
            # Angle is known if it has a concrete value
            angle_is_known = angle_qty.value is not None
            self._original_variable_states[f"{name}_angle"] = angle_is_known
        else:
            # Ellipsis means unknown
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

        # Extract angle_dir from the resultant (unknown) vector if set
        result_angle_dir = AngleDirection.COUNTERCLOCKWISE
        for vec in self.vectors.values():
            if hasattr(vec, "_angle_dir"):
                result_angle_dir = vec._angle_dir
                break

        # Build vector_references map (vector name -> reference axis like "+y", "-x")
        vector_references = {name: vec.wrt for name, vec in self.vectors.items()}

        # Create solving state
        state = SolvingState(
            triangle=triangle,
            result_angle_dir=result_angle_dir,
            vector_references=vector_references,
        )
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
