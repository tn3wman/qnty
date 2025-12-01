"""
Triangle/Trigonometric solver for 2D/3D vector equilibrium using geometric methods.

This solver implements the classical geometric/trigonometric approach to force
equilibrium problems, commonly known as the "Force Triangle Method" or
"Parallelogram Law" in engineering mechanics statics.

Uses closed-form solutions (law of cosines, law of sines, Pythagorean theorem)
for fast, exact solutions with step-by-step solution tracking.

This method is preferred for problems with 2-3 forces where geometric
relationships can be visualized as triangles or parallelograms.
"""

from __future__ import annotations

import math
from typing import Any

from ..core.quantity import Quantity
from ..spatial.vector import _Vector
from ..utils.geometry import normalize_angle_positive
from ..utils.shared_utilities import compute_law_of_cosines


def _format_latex_subscript(name: str) -> str:
    """
    Format a force name for LaTeX subscript rendering.

    Converts names like 'F_R' to 'F_{R}' format for proper LaTeX rendering
    in theta subscripts.

    Args:
        name: The force name (e.g., 'F_R', 'F_AB', 'force1')

    Returns:
        Formatted string suitable for LaTeX subscripts
    """
    if "_" in name:
        return name.replace("_", "_{") + "}"
    return name


def _create_law_of_sines_step(
    force_name: str, resultant_name: str, angle_opposite_force_deg: float, angle_opposite_resultant_deg: float, F_R: float, F_computed: float, force_unit: str
) -> dict[str, Any]:
    """
    Create a solution step for Law of Sines computation.

    Args:
        force_name: Name of the force being solved
        resultant_name: Name of the resultant force
        angle_opposite_force_deg: Angle opposite the force (in degrees)
        angle_opposite_resultant_deg: Angle opposite the resultant (in degrees)
        F_R: Resultant magnitude
        F_computed: Computed force magnitude
        force_unit: Unit symbol for forces

    Returns:
        Dictionary containing the solution step
    """
    return {
        "target": f"|{force_name}|",
        "method": "Law of Sines",
        "equation": f"{force_name}/sin(\\alpha_{{opp,{force_name}}}) = {resultant_name}/sin(\\alpha_{{opp,{resultant_name}}})",
        "substitution": f"{force_name}/sin({angle_opposite_force_deg:.1f}°) = {F_R:.2f} {force_unit}/sin({angle_opposite_resultant_deg:.1f}°)",
        "result_value": f"{F_computed:.2f}",
        "result_unit": force_unit,
    }


def sum_force_components(forces: list[_Vector]) -> tuple[float, float, float, Any]:
    """
    Sum the x, y, z components of a list of force vectors.

    Args:
        forces: List of force vectors with x, y, z components

    Returns:
        Tuple of (sum_x, sum_y, sum_z, ref_unit) where ref_unit is the
        preferred unit from the first force that has one
    """
    sum_x = 0.0
    sum_y = 0.0
    sum_z = 0.0
    ref_unit = None

    for force in forces:
        if force.vector is None or force.x is None or force.y is None or force.z is None:
            continue

        if force.x.value is not None:
            sum_x += force.x.value
        if force.y.value is not None:
            sum_y += force.y.value
        if force.z.value is not None:
            sum_z += force.z.value

        if ref_unit is None and force.x.preferred is not None:
            ref_unit = force.x.preferred

    return sum_x, sum_y, sum_z, ref_unit


def create_law_of_cosines_step(
    target_force_name: str,
    force1_name: str,
    force2_name: str,
    angle_expression: str,
    force1_magnitude: float,
    force2_magnitude: float,
    included_angle_deg: float,
    computed_magnitude: float,
    force_unit: str,
) -> dict:
    """
    Create a Law of Cosines solution step dictionary.

    The Law of Cosines relates three sides and one angle of a triangle:
    c² = a² + b² - 2ab·cos(C)

    In the force triangle context, this computes the third force magnitude
    when two force magnitudes and the included angle are known.

    Args:
        target_force_name: Name of the force being solved for (the unknown side)
        force1_name: Name of first known force (side a)
        force2_name: Name of second known force (side b)
        angle_expression: LaTeX expression for the included angle between force1 and force2
        force1_magnitude: Magnitude of first force (|a|)
        force2_magnitude: Magnitude of second force (|b|)
        included_angle_deg: Angle between force1 and force2 in degrees (angle C)
        computed_magnitude: The computed result magnitude for the target force
        force_unit: Unit symbol for display (e.g., "N", "lb")

    Returns:
        Dictionary with solution step data including equation, substitution, and result
    """
    return {
        "target": f"|{target_force_name}|",
        "method": "Law of Cosines",
        "equation": f"{target_force_name}^2 = {force1_name}^2 + {force2_name}^2 - 2*{force1_name}*{force2_name}*cos({angle_expression})",
        "substitution": f"{target_force_name}^2 = ({force1_magnitude:.2f} {force_unit})^2 + ({force2_magnitude:.2f} {force_unit})^2 - 2 * ({force1_magnitude:.2f} {force_unit}) * ({force2_magnitude:.2f} {force_unit}) * cos({included_angle_deg:.1f}°)",
        "result_value": f"{computed_magnitude:.2f}",
        "result_unit": force_unit,
    }


class TriangleSolver:
    """
    Solver for vector equilibrium problems using the Force Triangle Method.

    Also known as the Geometric Method or Trigonometric Method in engineering
    mechanics statics. This solver uses force triangles/parallelograms with
    trigonometric relationships to solve for unknown forces.

    Applies:
    - Law of cosines: c² = a² + b² - 2ab·cos(C)
    - Law of sines: a/sin(A) = b/sin(B) = c/sin(C)
    - Pythagorean theorem: c² = a² + b² (when angle = 90°)
    - Parallelogram law for force composition
    - Component summation: ΣFx = 0, ΣFy = 0, ΣFz = 0

    Best suited for problems with 2-3 forces where geometric visualization
    is straightforward. For problems with many forces, use ComponentSolver instead.
    """

    def __init__(self):
        """Initialize the triangle solver."""
        self.solution_steps: list[dict[str, Any]] = []

    def _append_law_of_cosines_step(
        self,
        target_force: _Vector,
        force1: _Vector,
        force2: _Vector,
        angle_expression: str,
        force1_magnitude: float,
        force2_magnitude: float,
        included_angle_deg: float,
        computed_magnitude: float,
        force_unit: str,
    ) -> None:
        """
        Append a Law of Cosines solution step to the solution steps list.

        Args:
            target_force: The force being solved for (unknown)
            force1: First known force
            force2: Second known force
            angle_expression: LaTeX expression for the included angle
            force1_magnitude: Magnitude of first force
            force2_magnitude: Magnitude of second force
            included_angle_deg: Included angle in degrees
            computed_magnitude: Computed result magnitude
            force_unit: Unit symbol for display
        """
        self.solution_steps.append(
            create_law_of_cosines_step(
                target_force_name=target_force.name,
                force1_name=force1.name,
                force2_name=force2.name,
                angle_expression=angle_expression,
                force1_magnitude=force1_magnitude,
                force2_magnitude=force2_magnitude,
                included_angle_deg=included_angle_deg,
                computed_magnitude=computed_magnitude,
                force_unit=force_unit,
            )
        )

    def solve_resultant(self, known_forces: list[_Vector], forces_dict: dict[str, _Vector]) -> _Vector:
        """
        Compute resultant of known forces using vector addition (component summation).

        Args:
            known_forces: List of known forces to sum
            forces_dict: Dictionary of all forces (to find/create resultant)

        Returns:
            The resultant force vector
        """
        self.solution_steps.append({"method": "Vector Addition (Component Summation)", "description": "Sum all force components to find resultant"})

        # Sum components
        sum_x, sum_y, sum_z, ref_unit = sum_force_components(known_forces)

        # Create resultant vector
        from ..core.dimension_catalog import dim

        x_qty = Quantity(name="FR_x", dim=dim.force, value=sum_x, preferred=ref_unit)
        y_qty = Quantity(name="FR_y", dim=dim.force, value=sum_y, preferred=ref_unit)
        z_qty = Quantity(name="FR_z", dim=dim.force, value=sum_z, preferred=ref_unit)

        resultant_vector = _Vector.from_quantities(x_qty, y_qty, z_qty)

        # Find or create resultant force
        resultant = None
        for _force_name, force in forces_dict.items():
            if force.is_resultant:
                resultant = force
                break

        if resultant is None:
            resultant = _Vector(vector=resultant_vector, name="FR", is_resultant=True)
            forces_dict["FR"] = resultant
        else:
            # Update existing resultant
            resultant.copy_coords_from(resultant_vector)
            resultant._compute_magnitude_and_angle()
            resultant.is_known = True

        if ref_unit is not None and resultant.magnitude is not None and resultant.angle is not None:
            mag_value = resultant.magnitude.value / ref_unit.si_factor if resultant.magnitude.value is not None else 0.0
            ang_value = resultant.angle.value * 180 / math.pi if resultant.angle.value is not None else 0.0
            self.solution_steps.append({"result": f"Resultant: {mag_value:.2f} {ref_unit.symbol} at {ang_value:.1f}°"})

        return resultant

    def solve_single_unknown(self, known_forces: list[_Vector], unknown_force: _Vector, resultant_forces: list[_Vector], forces_dict: dict[str, _Vector]) -> None:
        """
        Solve for single unknown force given known forces.

        Args:
            known_forces: List of known forces
            unknown_force: The unknown force to solve for
            resultant_forces: List of forces marked as resultants
            forces_dict: Dictionary of all forces
        """
        # Special case: Known resultant + one known force, solve for unknown force
        # Pattern: F_unknown + F_known = F_resultant (where F_resultant is also in known_forces)
        if len(resultant_forces) == 1 and len(known_forces) == 2:
            # Check if one of the known forces is the resultant
            resultant = resultant_forces[0]
            if resultant in known_forces:
                # Find the other known force (not the resultant)
                other_known = [f for f in known_forces if f != resultant][0]
                # Solve: F_unknown = F_resultant - F_other_known
                self.solve_unknown_from_resultant_and_known(unknown_force, resultant, other_known)
                return

        if len(known_forces) == 2 and len(resultant_forces) == 1:
            # Two known forces, unknown resultant
            self.solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) == 2 and unknown_force.is_resultant:
            # Two known forces, solve for resultant
            self.solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) >= 2 and not unknown_force.is_resultant:
            # Multiple known forces and unknown resultant - find equilibrium force
            # First compute resultant of known forces
            resultant = self.solve_resultant(known_forces, forces_dict)
            # The unknown force must balance this resultant
            if resultant and resultant.vector:
                # Unknown force is negative of resultant
                unknown_vector = -resultant.vector
                unknown_force.copy_coords_from(unknown_vector)
                unknown_force._compute_magnitude_and_angle()
                unknown_force.is_known = True
        else:
            # Fall back to component summation
            self.solve_by_components(known_forces, unknown_force)

    def solve_unknown_from_resultant_and_known(self, unknown_force: _Vector, resultant: _Vector, known_force: _Vector) -> None:
        """
        Solve for unknown force given known resultant and one known force.

        Uses Law of Cosines and Law of Sines to solve the triangle formed by:
        F_unknown + F_known = F_resultant

        Args:
            unknown_force: The unknown force to solve for
            resultant: The known resultant force
            known_force: The known force
        """
        # Get magnitudes and angles
        if resultant.magnitude is None or resultant.magnitude.value is None:
            raise ValueError(f"Resultant {resultant.name} has no magnitude")
        if known_force.magnitude is None or known_force.magnitude.value is None:
            raise ValueError(f"Force {known_force.name} has no magnitude")
        if resultant.angle is None or resultant.angle.value is None:
            raise ValueError(f"Resultant {resultant.name} has no angle")
        if known_force.angle is None or known_force.angle.value is None:
            raise ValueError(f"Force {known_force.name} has no angle")

        F_R = resultant.magnitude.value
        F_known = known_force.magnitude.value
        theta_R = resultant.angle.value  # radians
        theta_known = known_force.angle.value  # radians

        # Compute the angle between the resultant and known force in the triangle
        # This is the interior angle at the junction point
        gamma = abs(theta_R - theta_known)
        # Ensure gamma is the angle in the triangle (between 0 and π)
        if gamma > math.pi:
            gamma = 2 * math.pi - gamma

        # Apply law of cosines: F_unknown² = F_R² + F_known² - 2·F_R·F_known·cos(γ)
        # This gives us the magnitude of the unknown force
        F_unknown = compute_law_of_cosines(F_R, F_known, gamma)

        # Now find the angle of the unknown force using vector addition
        # F_unknown = F_R - F_known (vector subtraction)
        F_Rx = F_R * math.cos(theta_R)
        F_Ry = F_R * math.sin(theta_R)
        F_knownx = F_known * math.cos(theta_known)
        F_knowny = F_known * math.sin(theta_known)
        F_unknownx = F_Rx - F_knownx
        F_unknowny = F_Ry - F_knowny
        theta_unknown = math.atan2(F_unknowny, F_unknownx)

        # Get unit symbols
        force_unit = resultant.magnitude.preferred.symbol if resultant.magnitude.preferred else "N"

        # Step 1: Solve for unknown magnitude using Law of Cosines
        gamma_deg = math.degrees(gamma)
        # Use LaTeX theta command for proper rendering
        resultant_subscript = _format_latex_subscript(resultant.name)
        known_subscript = _format_latex_subscript(known_force.name)
        angle_diff = f"\\theta_{{{resultant_subscript}}} - \\theta_{{{known_subscript}}}"
        self._append_law_of_cosines_step(unknown_force, resultant, known_force, angle_diff, F_R, F_known, gamma_deg, F_unknown, force_unit)

        # Step 2: Solve for unknown direction using Law of Sines
        # Law of Sines: sin(α)/a = sin(β)/b
        # In our triangle: F_unknown + F_known = F_resultant
        # We need to find the angle θ of F_unknown
        # Using: sin(θ_R + θ)/F_known = sin(γ)/F_unknown
        theta_unknown_deg = math.degrees(theta_unknown)
        theta_R_deg = math.degrees(theta_R)

        # Format: sin(90° + θ)/F_known = sin(γ)/F_unknown
        # This matches the textbook format from Problem 2-2
        unknown_subscript = _format_latex_subscript(unknown_force.name)
        resultant_subscript = _format_latex_subscript(resultant.name)
        known_subscript = _format_latex_subscript(known_force.name)
        angle_var = f"\\theta_{{{unknown_subscript}}}"
        theta_R_var = f"\\theta_{{{resultant_subscript}}}"
        theta_known_var = f"\\theta_{{{known_subscript}}}"
        angle_sum = f"({theta_R_var} + {angle_var})"
        # Use the same angle difference as in Law of Cosines for consistency
        gamma_angle = f"({theta_R_var} - {theta_known_var})"
        self.solution_steps.append(
            {
                "target": f"{angle_var}",
                "method": "Law of Sines",
                "equation": f"sin({angle_sum})/{known_force.name} = sin({gamma_angle})/{unknown_force.name}",
                "substitution": f"sin(({theta_R_deg:.1f}° + {angle_var}))/{F_known:.2f} = sin(({gamma_deg:.1f}°))/{F_unknown:.2f}",
                "result_value": f"{theta_unknown_deg:.2f}",
                "result_unit": "°",
            }
        )

        # Create unknown force vector
        ref_unit = resultant.magnitude.preferred
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        mag_qty = Quantity(name=f"{unknown_force.name}_magnitude", dim=dim.force, value=F_unknown, preferred=ref_unit)
        degree_unit = ureg.resolve("degree", dim=dim.D)
        angle_qty = Quantity(name=f"{unknown_force.name}_angle", dim=dim.D, value=theta_unknown, preferred=degree_unit)

        # Use the computed components (already in SI units)
        x_qty = Quantity(name=f"{unknown_force.name}_x", dim=dim.force, value=F_unknownx, preferred=ref_unit)
        y_qty = Quantity(name=f"{unknown_force.name}_y", dim=dim.force, value=F_unknowny, preferred=ref_unit)
        z_qty = Quantity(name=f"{unknown_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        unknown_vector = _Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update unknown force
        unknown_force.copy_coords_from(unknown_vector)
        unknown_force._magnitude = mag_qty
        unknown_force._angle = angle_qty
        unknown_force.is_known = True

    def solve_resultant_from_two_forces(self, force1: _Vector, force2: _Vector, resultant: _Vector) -> None:
        """
        Solve for resultant of two forces using law of cosines and law of sines.

        This is the classic parallelogram/triangle method.

        Args:
            force1: First known force
            force2: Second known force
            resultant: The resultant force to solve for
        """
        # Get magnitudes and angles
        if force1.magnitude is None or force1.magnitude.value is None:
            raise ValueError(f"Force {force1.name} has no magnitude")
        if force2.magnitude is None or force2.magnitude.value is None:
            raise ValueError(f"Force {force2.name} has no magnitude")
        if force1.angle is None or force1.angle.value is None:
            raise ValueError(f"Force {force1.name} has no angle")
        if force2.angle is None or force2.angle.value is None:
            raise ValueError(f"Force {force2.name} has no angle")

        F1 = force1.magnitude.value
        F2 = force2.magnitude.value
        theta1 = force1.angle.value  # radians
        theta2 = force2.angle.value  # radians

        # Compute the angle between the two forces
        # Always use the positive angle between 0 and 2π
        gamma = abs(theta2 - theta1)
        # Ensure gamma is the smaller angle (between 0 and π)
        if gamma > math.pi:
            gamma = 2 * math.pi - gamma

        # Apply law of cosines: FR² = F1² + F2² - 2·F1·F2·cos(180° - γ)
        # Note: The angle in the triangle is (180° - γ) due to parallelogram law
        angle_in_triangle = math.pi - gamma
        FR = compute_law_of_cosines(F1, F2, angle_in_triangle)

        # Compute resultant using vector addition (this gives the correct angle)
        F1x = F1 * math.cos(theta1)
        F1y = F1 * math.sin(theta1)
        F2x = F2 * math.cos(theta2)
        F2y = F2 * math.sin(theta2)
        FRx = F1x + F2x
        FRy = F1y + F2y
        theta_R = math.atan2(FRy, FRx)

        # Get unit symbols
        force_unit = force1.magnitude.preferred.symbol if force1.magnitude.preferred else "N"

        # Step 1: Solve for resultant magnitude using Law of Cosines
        gamma_deg = math.degrees(angle_in_triangle)
        # Use LaTeX theta command for proper rendering
        force2_subscript = _format_latex_subscript(force2.name)
        force1_subscript = _format_latex_subscript(force1.name)
        angle_diff = f"180° - (\\theta_{{{force2_subscript}}} - \\theta_{{{force1_subscript}}})"
        self._append_law_of_cosines_step(resultant, force1, force2, angle_diff, F1, F2, gamma_deg, FR, force_unit)

        # Step 2: Solve for resultant direction using Law of Sines
        theta_R_deg = math.degrees(theta_R)
        resultant_subscript = _format_latex_subscript(resultant.name)
        angle_var = f"\\theta_{{{resultant_subscript}}}"
        angle_diff_sin = f"(180° - {angle_var})"

        # Using Law of Sines: sin(α)/a = sin(β)/b
        # This matches textbook format for engineering reports
        self.solution_steps.append(
            {
                "target": f"{angle_var}",
                "method": "Law of Sines",
                "equation": f"sin({angle_var})/{force1.name} = sin({angle_diff_sin})/{force2.name}",
                "substitution": f"sin(({angle_var}))/{F1:.2f} = sin(({angle_diff_sin}))/{F2:.2f}",
                "result_value": f"{theta_R_deg:.2f}",
                "result_unit": "°",
            }
        )

        # Create resultant vector using the correct angle from atan2
        ref_unit = force1.magnitude.preferred
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        mag_qty = Quantity(name="FR_magnitude", dim=dim.force, value=FR, preferred=ref_unit)
        degree_unit = ureg.resolve("degree", dim=dim.D)
        angle_qty = Quantity(name="FR_angle", dim=dim.D, value=theta_R, preferred=degree_unit)

        # Use the computed components (already in SI units)
        x_qty = Quantity(name="FR_x", dim=dim.force, value=FRx, preferred=ref_unit)
        y_qty = Quantity(name="FR_y", dim=dim.force, value=FRy, preferred=ref_unit)
        z_qty = Quantity(name="FR_z", dim=dim.force, value=0.0, preferred=ref_unit)
        resultant_vector = _Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update resultant force
        resultant.copy_coords_from(resultant_vector)
        resultant._magnitude = mag_qty
        resultant._angle = angle_qty
        resultant.is_known = True

    def solve_two_unknowns_with_known_resultant(self, unknown_forces: list[_Vector], resultant: _Vector) -> None:
        """
        Solve for two unknown force magnitudes given known resultant and known angles.

        This handles force decomposition problems where:
        - Resultant magnitude and direction are known
        - Two component force directions are known
        - Two component force magnitudes are unknown

        Uses Law of Sines twice to solve the force triangle.

        Args:
            unknown_forces: List of exactly 2 unknown forces (with known angles, unknown magnitudes)
            resultant: The known resultant force
        """
        if len(unknown_forces) != 2:
            raise ValueError(f"Expected exactly 2 unknown forces, got {len(unknown_forces)}")

        # Verify resultant has magnitude and angle
        if resultant.magnitude is None or resultant.magnitude.value is None:
            raise ValueError(f"Resultant {resultant.name} must have a known magnitude")
        if resultant.angle is None or resultant.angle.value is None:
            raise ValueError(f"Resultant {resultant.name} must have a known angle")

        force1 = unknown_forces[0]
        force2 = unknown_forces[1]

        # Verify both unknowns have angles but not magnitudes
        if force1.angle is None or force1.angle.value is None:
            raise ValueError(f"Force {force1.name} must have a known angle")
        if force2.angle is None or force2.angle.value is None:
            raise ValueError(f"Force {force2.name} must have a known angle")

        # Use absolute value of resultant magnitude for decomposition
        # (negative magnitude means force points opposite to specified angle)
        # magnitude.value is now stored in SI units
        F_R = abs(resultant.magnitude.value)  # Already in SI units
        theta_R = resultant.angle.value  # radians
        theta_1 = force1.angle.value  # radians
        theta_2 = force2.angle.value  # radians

        # Compute interior angles of the force triangle using the parallelogram law
        # The triangle is formed by: force1 + force2 = resultant
        #
        # Interior angles are computed from the directions (measured CCW from +x axis):
        # - Angle opposite force1 = angle from force2 to resultant (CCW)
        # - Angle opposite force2 = angle from force1 to resultant (CCW)
        # - Angle opposite resultant = angle between force1 and force2
        #
        # We always compute angles in the CCW direction to maintain consistency with the
        # standard convention that angles are measured counterclockwise from positive x-axis.

        # Normalize all angles to [0, 2π) using shared utility
        theta_R = normalize_angle_positive(theta_R)
        theta_1 = normalize_angle_positive(theta_1)
        theta_2 = normalize_angle_positive(theta_2)

        # Angle opposite to resultant (angle from force1 to force2, measured CCW)
        angle_opposite_R = theta_2 - theta_1
        if angle_opposite_R < 0:
            angle_opposite_R += 2 * math.pi
        # Take the smaller angle (interior angle of triangle)
        if angle_opposite_R > math.pi:
            angle_opposite_R = 2 * math.pi - angle_opposite_R

        # Angle opposite to force2 (angle from force1 to resultant, measured CCW)
        angle_opposite_2 = theta_R - theta_1
        if angle_opposite_2 < 0:
            angle_opposite_2 += 2 * math.pi
        # Take the smaller angle
        if angle_opposite_2 > math.pi:
            angle_opposite_2 = 2 * math.pi - angle_opposite_2

        # Angle opposite to force1 (angle from force2 to resultant, measured CCW)
        angle_opposite_1 = theta_R - theta_2
        if angle_opposite_1 < 0:
            angle_opposite_1 += 2 * math.pi
        # Take the smaller angle
        if angle_opposite_1 > math.pi:
            angle_opposite_1 = 2 * math.pi - angle_opposite_1

        # Get unit symbols
        force_unit = resultant.magnitude.preferred.symbol if resultant.magnitude.preferred else "N"

        # Apply Law of Sines: a/sin(A) = b/sin(B) = c/sin(C)
        # Force1 / sin(angle_opposite_1) = Resultant / sin(angle_opposite_R)
        F1 = (F_R * math.sin(angle_opposite_1)) / math.sin(angle_opposite_R)

        # Force2 / sin(angle_opposite_2) = Resultant / sin(angle_opposite_R)
        F2 = (F_R * math.sin(angle_opposite_2)) / math.sin(angle_opposite_R)

        # Convert angles to degrees for display
        angle_opposite_1_deg = math.degrees(angle_opposite_1)
        angle_opposite_2_deg = math.degrees(angle_opposite_2)
        angle_opposite_R_deg = math.degrees(angle_opposite_R)

        # Step 1: Solve for Force 1 magnitude using Law of Sines
        self.solution_steps.append(_create_law_of_sines_step(force1.name, resultant.name, angle_opposite_1_deg, angle_opposite_R_deg, F_R, F1, force_unit))

        # Step 2: Solve for Force 2 magnitude using Law of Sines
        self.solution_steps.append(_create_law_of_sines_step(force2.name, resultant.name, angle_opposite_2_deg, angle_opposite_R_deg, F_R, F2, force_unit))

        # Create force vectors with computed magnitudes
        ref_unit = resultant.magnitude.preferred
        from ..core.dimension_catalog import dim

        # Store SI values directly (F1 and F2 are already in SI units from calculations)
        # Quantity class handles conversion to preferred units for display

        # Update force 1
        mag1_qty = Quantity(name=f"{force1.name}_magnitude", dim=dim.force, value=F1, preferred=ref_unit)
        force1._magnitude = mag1_qty
        F1x = F1 * math.cos(theta_1)
        F1y = F1 * math.sin(theta_1)
        # Create vector from SI components
        f1_x_qty = Quantity(name=f"{force1.name}_x", dim=dim.force, value=F1x, preferred=ref_unit)
        f1_y_qty = Quantity(name=f"{force1.name}_y", dim=dim.force, value=F1y, preferred=ref_unit)
        f1_z_qty = Quantity(name=f"{force1.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        force1._coords = _Vector.from_quantities(f1_x_qty, f1_y_qty, f1_z_qty)._coords
        force1.is_known = True

        # Update force 2
        mag2_qty = Quantity(name=f"{force2.name}_magnitude", dim=dim.force, value=F2, preferred=ref_unit)
        force2._magnitude = mag2_qty
        F2x = F2 * math.cos(theta_2)
        F2y = F2 * math.sin(theta_2)
        # Create vector from SI components
        f2_x_qty = Quantity(name=f"{force2.name}_x", dim=dim.force, value=F2x, preferred=ref_unit)
        f2_y_qty = Quantity(name=f"{force2.name}_y", dim=dim.force, value=F2y, preferred=ref_unit)
        f2_z_qty = Quantity(name=f"{force2.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        force2._coords = _Vector.from_quantities(f2_x_qty, f2_y_qty, f2_z_qty)._coords
        force2.is_known = True

    def solve_by_components(self, known_forces: list[_Vector], unknown_force: _Vector) -> None:
        """
        Solve using component summation (ΣFx = 0, ΣFy = 0).

        This assumes equilibrium: unknown force balances known forces.

        Args:
            known_forces: List of known forces
            unknown_force: The unknown force to solve for
        """
        self.solution_steps.append({"method": "Component Summation (Equilibrium)", "description": "ΣFx = 0, ΣFy = 0"})

        # Sum known force components
        sum_x, sum_y, sum_z, ref_unit = sum_force_components(known_forces)

        # Unknown force must balance the sum
        unknown_x = -sum_x
        unknown_y = -sum_y
        unknown_z = -sum_z

        self.solution_steps.append({"calculation": f"ΣFx = {sum_x:.2f} → Unknown Fx = {unknown_x:.2f}", "calculation2": f"ΣFy = {sum_y:.2f} → Unknown Fy = {unknown_y:.2f}"})

        # Create unknown vector
        from ..core.dimension_catalog import dim

        x_qty = Quantity(name=f"{unknown_force.name}_x", dim=dim.force, value=unknown_x, preferred=ref_unit)
        y_qty = Quantity(name=f"{unknown_force.name}_y", dim=dim.force, value=unknown_y, preferred=ref_unit)
        z_qty = Quantity(name=f"{unknown_force.name}_z", dim=dim.force, value=unknown_z, preferred=ref_unit)

        unknown_vector = _Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update unknown force
        unknown_force.copy_coords_from(unknown_vector)
        unknown_force._compute_magnitude_and_angle()
        unknown_force.is_known = True
