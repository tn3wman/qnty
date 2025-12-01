"""
VectorEquilibriumProblem class for solving 2D/3D statics problems algebraically.

Uses closed-form solutions (law of cosines, law of sines, Pythagorean theorem)
instead of numerical solvers for fast, exact solutions with step-by-step reporting.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from ..core.quantity import Quantity
from ..solving.solution_step import SolutionStep
from ..solving.triangle_solver import TriangleSolver
from ..spatial.vector import _Vector
from ..spatial.vector_helpers import vector_helper as _helper
from ..spatial.vectors import _VectorWithUnknowns
from ..utils.geometry import _format_angle_difference_display, compute_angle_between_display, format_axis_ref, interior_angle, normalize_angle_positive
from ..utils.shared_utilities import (
    capture_original_force_states,
    clone_force_vector,
    compute_law_of_cosines,
    convert_angle_to_direction,
    format_law_of_sines_angle_substitution,
    format_law_of_sines_substitution,
)
from .problem import Problem

# =============================================================================
# Helper functions for repeated calculations
# =============================================================================


def _get_unit_info(unit) -> tuple[str, float]:
    """Extract unit symbol and SI factor from a unit object."""
    if unit is None:
        return "", 1.0
    return unit.symbol, unit.si_factor


def _to_display_value(si_value: float, si_factor: float) -> float:
    """Convert SI value to display units."""
    return si_value / si_factor


def _latex_name(name: str) -> str:
    """Format a name for LaTeX (convert F_BA to F_{BA} for proper subscripts)."""
    if "_" in name:
        parts = name.split("_", 1)
        return f"{parts[0]}_{{{parts[1]}}}"
    return name


def _format_law_of_cosines_equation(result_name: str, side1_name: str, side2_name: str) -> str:
    """Format the Law of Cosines equation string for display.

    Args:
        result_name: Name of the result vector (e.g., "F_R")
        side1_name: Name of first side vector
        side2_name: Name of second side vector

    Returns:
        Formatted equation string like "|F_R|² = |F_1|² + |F_2|² - 2·|F_1|·|F_2|·cos(∠(F_1,F_2))"
    """
    return f"|{result_name}|² = |{side1_name}|² + |{side2_name}|² - 2·|{side1_name}|·|{side2_name}|·cos(∠({side1_name},{side2_name}))"


def _all_angles_known(forces: list[_Vector]) -> bool:
    """Check if all forces in the list have known angles.

    Args:
        forces: List of force vectors to check

    Returns:
        True if all forces have non-None angle values
    """
    return all(f.angle is not None and f.angle.value is not None for f in forces)


def _all_magnitudes_known(forces: list[_Vector]) -> bool:
    """Check if all forces in the list have known magnitudes.

    Args:
        forces: List of force vectors to check

    Returns:
        True if all forces have non-None magnitude values
    """
    return all(f.magnitude is not None and f.magnitude.value is not None for f in forces)


# Use the shared utility for Law of Cosines computation
_law_of_cosines = compute_law_of_cosines


def _convert_angle_for_display(angle_deg: float, angle_dir: str | None) -> float:
    """Convert angle based on the angle_dir setting.

    Args:
        angle_deg: Angle in degrees (standard CCW convention, 0-360)
        angle_dir: Direction convention - "ccw" (default), "cw", or "signed"

    Returns:
        Converted angle based on angle_dir:
        - "ccw" (default): 0 to 360, counterclockwise from reference
        - "cw": Negative for clockwise angles (e.g., 358.8° -> -1.2°)
        - "signed": -180 to 180 range
    """
    return convert_angle_to_direction(angle_deg, angle_dir)


def _magnitude_and_angle_from_coords(coords: np.ndarray) -> tuple[float, float]:
    """Compute magnitude and angle from Cartesian coordinates."""
    mag = float(np.sqrt(np.sum(coords**2)))
    angle = float(np.arctan2(coords[1], coords[0]))
    return mag, angle


def _sum_force_components(forces: list[_Vector], skip_resultants: bool = False) -> tuple[float, float, float, Any]:
    """
    Sum x, y, z components of forces.

    Returns:
        Tuple of (sum_x, sum_y, sum_z, reference_unit)
    """
    sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
    ref_unit = None

    for force in forces:
        if skip_resultants and force.is_resultant:
            continue
        if force.x and force.x.value is not None:
            sum_x += force.x.value
        if force.y and force.y.value is not None:
            sum_y += force.y.value
        if force.z and force.z.value is not None:
            sum_z += force.z.value
        if ref_unit is None and force.x and force.x.preferred:
            ref_unit = force.x.preferred

    return sum_x, sum_y, sum_z, ref_unit


def _require_magnitude(force: _Vector, name: str = "Force") -> float:
    """Validate and return magnitude value, raising ValueError if None."""
    if force.magnitude.value is None:
        raise ValueError(f"{name} has no magnitude value")
    return force.magnitude.value


def _require_angle(force: _Vector, name: str = "Force") -> float:
    """Validate and return angle value, raising ValueError if None."""
    if force.angle is None or force.angle.value is None:
        raise ValueError(f"{name} has no angle value")
    return force.angle.value


def _get_force_display_value(force: _Vector) -> tuple[float, str]:
    """Get magnitude in display units and unit symbol."""
    if force.magnitude.value is None:
        return 0.0, ""
    si_value = force.magnitude.value
    if force.magnitude.preferred:
        return si_value / force.magnitude.preferred.si_factor, force.magnitude.preferred.symbol
    return si_value, ""


def _format_force_string(name: str, force: _Vector) -> str | None:
    """Format force as 'name = magnitude unit at angle°'. Returns None if force lacks required values."""
    if force.magnitude.value is None:
        return None
    if force.angle is None or force.angle.value is None:
        return None
    mag_val, mag_unit = _get_force_display_value(force)
    ang_val = math.degrees(force.angle.value)
    return f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°"


def _create_component_step(vec_name: str, component: str, mag_display: float, angle_deg: float, coord_display: float, unit_symbol: str) -> dict[str, Any]:
    """Create a component resolution solution step dictionary."""
    trig_fn = "cos" if component == "x" else "sin"
    return {
        "target": f"{vec_name}_{component}",
        "method": "component_resolution",
        "description": f"Resolve {vec_name} into x and y components",
        "equation": f"{vec_name}_{component} = |{vec_name}| {trig_fn}(θ)",
        "substitution": f"{vec_name}_{component} = {mag_display:.3f} {trig_fn}({angle_deg:.1f}°)",
        "result_value": f"{coord_display:.3f}",
        "result_unit": unit_symbol,
    }


def _create_sum_step(resultant_name: str, component: str, component_names: list[str], terms: str, sum_display: float, unit_symbol: str) -> dict[str, Any]:
    """Create a component sum solution step dictionary."""
    return {
        "target": f"{resultant_name}_{component}",
        "method": "component_sum",
        "description": f"Sum {component}-components",
        "equation": f"Σ{resultant_name}_{component} = {' + '.join([f'{n}_{component}' for n in component_names])}",
        "substitution": f"Σ{resultant_name}_{component} = {terms}",
        "result_value": f"{sum_display:.3f}",
        "result_unit": unit_symbol,
    }


def _get_axis_angle(wrt: str, coord_sys: Any) -> float:
    """
    Get the standard angle (in radians) for an axis reference.

    Args:
        wrt: Axis reference like "+x", "-y", or custom axis label
        coord_sys: Coordinate system object with axis1_label, axis2_label, axis1_angle, axis2_angle

    Returns:
        Angle in radians from +x axis (counterclockwise)

    Raises:
        ValueError: If axis is unknown and no coordinate system is defined
    """
    standard_axis_angles = {"+x": 0, "+y": math.pi / 2, "-x": math.pi, "-y": 3 * math.pi / 2}
    wrt_lower = wrt.lower()

    if wrt_lower in standard_axis_angles:
        return standard_axis_angles[wrt_lower]

    if coord_sys is not None:
        wrt_stripped = wrt.lstrip("+-")
        is_negative = wrt.startswith("-")
        if wrt_stripped == coord_sys.axis1_label:
            base_angle = coord_sys.axis1_angle
        elif wrt_stripped == coord_sys.axis2_label:
            base_angle = coord_sys.axis2_angle
        else:
            raise ValueError(f"Unknown axis '{wrt}'")
        if is_negative:
            base_angle += math.pi
        return base_angle

    raise ValueError(f"Unknown axis '{wrt}' and no coordinate system defined")


# =============================================================================
# ParallelogramLawProblem class
# =============================================================================


class ParallelogramLawProblem(Problem):
    """
    Specialized Problem for 2D/3D vector equilibrium using algebraic methods.

    Automatically applies:
    - Law of cosines: c² = a² + b² - 2ab·cos(C)
    - Law of sines: a/sin(A) = b/sin(B) = c/sin(C)
    - Pythagorean theorem: c² = a² + b² (when angle = 90°)
    - Component summation: ΣFx = 0, ΣFy = 0, ΣFz = 0

    Examples:
        >>> # Define problem with class inheritance
        >>> class CableProblem(VectorEquilibriumProblem):
        ...     F1 = create_vector_polar(magnitude=700, angle=60, unit="N")
        ...     F2 = create_vector_polar(magnitude=450, angle=105, unit="N")
        ...     FR = create_vector_resultant(F1, F2, name="FR")
        ...
        >>> problem = CableProblem()
        >>> solution = problem.solve()

        >>> # Or programmatically
        >>> problem = VectorEquilibriumProblem("Cable Forces")
        >>> problem.add_force(create_vector_polar(magnitude=700, angle=60, unit="N", name="F1"))
        >>> problem.add_force(create_vector_polar(magnitude=450, angle=105, unit="N", name="F2"))
        >>> problem.add_force(create_vector_resultant("F1", "F2", name="FR"))
        >>> solution = problem.solve()
    """

    def __init__(self, name: str | None = None, description: str = ""):
        """
        Initialize VectorEquilibriumProblem.

        Args:
            name: Problem name
            description: Problem description
        """
        super().__init__(name=name, description=description)
        self.forces: dict[str, _Vector] = {}
        self.solution_steps: list[dict[str, Any]] = []
        self._original_variable_states: dict[str, bool] = {}
        self._original_force_states: dict[str, bool] = {}
        self.solver = TriangleSolver()

        # Extract ForceVector class attributes
        self._extract_force_vectors()

        # Compute any vector resultants from _VectorWithUnknowns
        self._compute_vector_resultants()

    # =========================================================================
    # Vector cloning helpers (consolidated)
    # =========================================================================

    def _clone_vector(self, vec: _Vector, default_name: str = "") -> _Vector:
        """Create a copy of a _Vector using the built-in clone method."""
        # Use the name from vec if meaningful, otherwise use default_name
        original_name = getattr(vec, "name", "")
        name = original_name if (original_name and original_name != "Vector") else default_name
        return vec.clone(name=name if name else None)

    def _clone_vector_with_unknowns(self, vec: _VectorWithUnknowns, vector_clones: dict[int, _Vector], default_name: str = "") -> _VectorWithUnknowns:
        """Create a copy of a _VectorWithUnknowns using the built-in clone method."""
        # Use the name from vec if meaningful, otherwise use default_name
        original_name = getattr(vec, "name", "")
        name = original_name if (original_name and original_name != "Vector") else default_name
        return vec.clone(name=name if name else None, vector_clones=vector_clones)

    def _extract_force_vectors(self) -> None:
        """Extract ForceVector and _Vector objects defined at class level."""
        vector_clones: dict[int, _Vector] = {}

        # First pass: clone all plain _Vectors
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if type(attr).__name__ == "_Vector":
                clone = self._clone_vector(attr, default_name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)

        # Second pass: clone _VectorWithUnknowns that are NOT resultants
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if id(attr) in vector_clones:
                continue
            if isinstance(attr, _VectorWithUnknowns) and not getattr(attr, "is_resultant", False):
                clone = self._clone_vector_with_unknowns(attr, vector_clones, default_name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)

        # Third pass: clone _VectorWithUnknowns that ARE resultants
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if id(attr) in vector_clones:
                continue
            if isinstance(attr, _VectorWithUnknowns) and getattr(attr, "is_resultant", False):
                clone = self._clone_vector_with_unknowns(attr, vector_clones, default_name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
            elif isinstance(attr, _Vector):
                force_copy = self._clone_force_vector(attr)
                self.forces[attr_name] = force_copy
                setattr(self, attr_name, force_copy)

        # Fourth pass: resolve force references now that all vectors have names
        # This handles cases where F_AC references F_AB by vector object,
        # but F_AB was cloned later and now has its proper name
        for original_id, cloned_vec in vector_clones.items():
            force_vec_ref = getattr(cloned_vec, "_relative_to_force_vec", None)
            if force_vec_ref is None:
                # Also check the original class-level vector for the reference
                for attr_name in dir(self.__class__):
                    if attr_name.startswith("_"):
                        continue
                    attr = getattr(self.__class__, attr_name)
                    if id(attr) == original_id:
                        force_vec_ref = getattr(attr, "_relative_to_force_vec", None)
                        break

            if force_vec_ref is not None:
                # Find the cloned version of the referenced vector
                cloned_ref = vector_clones.get(id(force_vec_ref))
                if cloned_ref and cloned_ref.name:
                    cloned_vec._relative_to_force = cloned_ref.name
                    # Also update _original_wrt
                    old_wrt = getattr(cloned_vec, "_original_wrt", "")
                    if old_wrt.startswith("+"):
                        cloned_vec._original_wrt = f"+{cloned_ref.name}"
                    elif old_wrt.startswith("-"):
                        cloned_vec._original_wrt = f"-{cloned_ref.name}"

    def _clone_force_vector(self, force: _Vector) -> _Vector:
        """Create a copy of a ForceVector."""
        return clone_force_vector(force, _Vector)

    # =========================================================================
    # Vector resultant computation
    # =========================================================================

    def _compute_vector_resultants(self) -> None:
        """Compute resultant vectors from _VectorWithUnknowns placeholders."""
        solved_any = False
        needs_parametric_solve = False

        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self, attr_name)
            if not isinstance(attr, _VectorWithUnknowns) or not attr.component_vectors:
                continue

            is_constraint = getattr(attr, "_is_constraint", False)

            if is_constraint:
                if self._solve_inverse_resultant(attr, attr_name):
                    solved_any = True
                else:
                    # Parametric constraint: populate forces dict for main solve() method
                    needs_parametric_solve = True
                    self._populate_forces_for_parametric_solve(attr, attr_name)
                continue

            # Forward problem: sum component vectors
            self._compute_forward_resultant(attr, attr_name)
            solved_any = True

        if solved_any:
            self.is_solved = True
            self._populate_solving_history()
        elif needs_parametric_solve:
            # Don't mark as solved - the main solve() method will handle it
            self.is_solved = False

    def _populate_forces_for_parametric_solve(self, resultant: _VectorWithUnknowns, resultant_name: str) -> None:
        """Populate the forces dict for parametric constraint problems.

        When a resultant has parametric constraints (vectors with _relative_to_force),
        we need to add all component vectors to the forces dict so the main solve()
        method can process them.
        """
        # Add component vectors to forces dict
        for vec in resultant.component_vectors:
            vec_name = getattr(vec, "name", None)
            if vec_name and vec_name not in self.forces:
                self.forces[vec_name] = vec

        # Add the resultant itself
        if resultant_name not in self.forces:
            self.forces[resultant_name] = resultant

    def _compute_forward_resultant(self, resultant: _VectorWithUnknowns, resultant_name: str) -> None:
        """Compute forward resultant by summing component vectors."""
        # Add known vectors as variables
        for vec in resultant.component_vectors:
            vec_name = getattr(vec, "name", None)
            if vec_name and vec._unit:
                mag = vec.magnitude
                if mag:
                    mag_var = Quantity(
                        name=f"{vec_name} Magnitude",
                        dim=mag.dim,
                        value=mag.value,
                        preferred=mag.preferred,
                        _symbol=f"|{vec_name}|",
                    )
                    self.variables[f"{vec_name}_mag"] = mag_var
                    self._original_variable_states[f"{vec_name}_mag"] = True

                if hasattr(vec, "_angle") and vec._angle and vec._angle.value is not None:
                    angle_var = Quantity(
                        name=f"{vec_name} Angle",
                        dim=_helper.dim.D,
                        value=vec._angle.value,
                        preferred=vec._angle.preferred,
                        _symbol=f"θ_{vec_name}",
                    )
                    self.variables[f"{vec_name}_angle"] = angle_var
                    self._original_variable_states[f"{vec_name}_angle"] = True

        # Sum components
        sum_coords = np.array([0.0, 0.0, 0.0], dtype=float)
        for vec in resultant.component_vectors:
            sum_coords += vec._coords

        # Update resultant
        resultant._coords = sum_coords
        resultant._unknowns = {}
        resultant.is_known = True

        if hasattr(resultant, "_compute_magnitude_and_angle"):
            resultant._compute_magnitude_and_angle()

        # Compute magnitude and angle
        mag_si = float(np.sqrt(np.sum(sum_coords**2)))
        angle_rad = float(np.arctan2(sum_coords[1], sum_coords[0]))
        if angle_rad < 0:
            angle_rad += 2 * np.pi

        # Store magnitude and angle
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", mag_si, resultant._unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", angle_rad)

        # Add resultant as solved variable
        if resultant._dim is None:
            raise ValueError("Resultant has no dimension")
        self._add_force_variables(resultant_name, mag_si, angle_rad, resultant._dim, resultant._unit, is_known=False)

        # Add solution steps
        num_forces = len(resultant.component_vectors)
        if num_forces == 1:
            # Single force: resultant equals the force, no steps needed
            pass
        elif num_forces == 2:
            self._add_triangle_method_steps(
                resultant.component_vectors[0],
                resultant.component_vectors[1],
                resultant,
                resultant_name,
                mag_si,
                angle_rad,
            )
        else:
            # For 3+ forces, use iterative parallelogram law (like textbook solution)
            self._add_iterative_parallelogram_steps(
                resultant.component_vectors,
                resultant,
                resultant_name,
            )

    def _solve_inverse_resultant(self, resultant: _VectorWithUnknowns, resultant_name: str) -> bool:
        """Solve for unknown component vectors given a known resultant constraint.

        Returns:
            True if the problem was solved, False if it requires parametric solving.
        """
        component_vectors = resultant.component_vectors
        known_vectors: list[_Vector] = []
        unknown_vectors: list[_VectorWithUnknowns] = []

        # Check if any vectors have parametric constraints (relative to another force)
        has_parametric_constraint = any(getattr(vec, "_relative_to_force", None) is not None for vec in component_vectors)
        if has_parametric_constraint:
            # Parametric constraints require the main solve() method which handles
            # the coupled equations properly. Skip inverse solve and let solve() handle it.
            return False

        for vec in component_vectors:
            if isinstance(vec, _VectorWithUnknowns) and vec.has_unknowns:
                unknown_vectors.append(vec)
            else:
                known_vectors.append(vec)

        # Check if resultant itself has unknown magnitude (but known direction)
        resultant_has_unknown_magnitude = "magnitude" in resultant.unknowns

        if resultant_has_unknown_magnitude:
            # Special case: resultant direction is known but magnitude is unknown
            # Get direction from the unit vector stored in coords (we set mag=1 during creation)
            FR_angle = getattr(resultant, "_polar_angle_rad", None)
            if FR_angle is None:
                # Compute from coords (they are unit direction)
                FR_angle = math.atan2(resultant._coords[1], resultant._coords[0])
            unit = resultant._unit
            self._solve_with_unknown_resultant_magnitude(known_vectors, unknown_vectors, resultant, resultant_name, FR_angle, unit)
            return True

        FR_coords = resultant._coords
        FR_mag, FR_angle = _magnitude_and_angle_from_coords(FR_coords)

        unit = resultant._unit

        if len(known_vectors) == 1 and len(unknown_vectors) == 1:
            self._solve_one_known_one_unknown_inverse(known_vectors[0], unknown_vectors[0], resultant, resultant_name, FR_coords, FR_mag, FR_angle, unit)
        elif len(known_vectors) == 0 and len(unknown_vectors) == 2:
            # Check what type of unknowns we have
            both_have_known_angles = all(hasattr(vec, "_polar_angle_rad") and vec._polar_angle_rad is not None for vec in unknown_vectors)
            # Check for mixed unknowns: one with unknown angle, one with unknown magnitude
            has_unknown_angle = [hasattr(vec, "_unknowns") and "angle" in vec._unknowns for vec in unknown_vectors]
            has_unknown_magnitude = [hasattr(vec, "_unknowns") and "magnitude" in vec._unknowns for vec in unknown_vectors]
            is_mixed_unknowns = (
                sum(has_unknown_angle) == 1 and sum(has_unknown_magnitude) == 1 and has_unknown_angle != has_unknown_magnitude  # One each, not both on same vector
            )

            if both_have_known_angles:
                self._solve_two_unknown_magnitudes_inverse(unknown_vectors, resultant, resultant_name, FR_mag, FR_angle, unit)
            elif is_mixed_unknowns:
                # One vector has unknown angle (known magnitude), other has unknown magnitude (known angle)
                # For mixed unknowns with vector-relative resultant, use _polar_magnitude directly
                # since _coords were computed with wrong reference (when wrt is a vector with unknown angle)
                wrt_R = getattr(resultant, "_original_wrt", "+x")
                if wrt_R.startswith("@"):
                    # Vector-relative resultant: use polar values directly
                    FR_mag_polar = getattr(resultant, "_polar_magnitude", None)
                    if FR_mag_polar is not None:
                        FR_mag = FR_mag_polar
                self._solve_mixed_unknowns_inverse(unknown_vectors, resultant, resultant_name, FR_mag, FR_angle, unit)
            else:
                raise NotImplementedError("Inverse resultant solve requires either both unknown magnitudes or one unknown angle + one unknown magnitude")
        else:
            raise NotImplementedError(f"Inverse resultant solve not implemented for {len(known_vectors)} known + {len(unknown_vectors)} unknown vectors")

        return True

    def _solve_one_known_one_unknown_inverse(
        self, known_vec: _Vector, unknown_vec: _VectorWithUnknowns, resultant: _VectorWithUnknowns, resultant_name: str, FR_coords: np.ndarray, FR_mag: float, FR_angle: float, unit
    ) -> None:
        """Solve inverse problem with one known and one unknown vector."""
        F_known_coords = known_vec._coords
        F_known_mag, F_known_angle = _magnitude_and_angle_from_coords(F_known_coords)

        # Vector subtraction: F_unknown = F_R - F_known
        F_unknown_coords = FR_coords - F_known_coords
        F_unknown_mag, F_unknown_angle_raw = _magnitude_and_angle_from_coords(F_unknown_coords)
        F_unknown_angle = normalize_angle_positive(F_unknown_angle_raw)

        # Calculate angles for solution steps
        gamma = interior_angle(FR_angle, F_known_angle)
        alpha = interior_angle(FR_angle, F_unknown_angle)

        # Update unknown vector
        unknown_vec._coords = F_unknown_coords.copy()
        unknown_vec._unknowns = {}
        unknown_vec.is_known = True
        unknown_vec._magnitude = _helper.create_force_quantity(f"{unknown_vec.name}_magnitude", F_unknown_mag, unit)
        unknown_vec._angle = _helper.create_angle_quantity(f"{unknown_vec.name}_angle", F_unknown_angle)
        unknown_vec._original_angle = math.degrees(F_unknown_angle)
        unknown_vec._original_wrt = "+x"

        # Add variables
        vec_name = unknown_vec.name or "F_unknown"
        self._add_force_variables(vec_name, F_unknown_mag, F_unknown_angle, resultant._dim, unit, is_known=False)

        known_name = known_vec.name or "F_known"
        self._add_force_variables(known_name, F_known_mag, F_known_angle, resultant._dim, unit, is_known=True, skip_angle=True)

        self._add_force_variables(resultant_name, FR_mag, FR_angle, resultant._dim, unit, is_known=True)

        # Store on resultant
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", FR_mag, unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", FR_angle)

        # Add solution steps
        self._add_inverse_triangle_method_steps(known_vec, unknown_vec, resultant, resultant_name, F_unknown_mag, F_unknown_angle, F_known_angle, FR_angle, gamma, alpha)

    def _solve_two_unknown_magnitudes_inverse(self, unknown_vectors: list[_VectorWithUnknowns], resultant: _VectorWithUnknowns, resultant_name: str, FR_mag: float, FR_angle: float, unit) -> None:
        """
        Solve inverse problem with two unknown vectors that have known angles but unknown magnitudes.

        Given: FR = F1 + F2 where FR is known, and F1, F2 have known angles but unknown magnitudes.
        Solve: |F1| and |F2| using the Parallelogram Law (Law of Sines):
            |F1| / sin(α) = |F2| / sin(β) = |FR| / sin(γ)
        where α, β, γ are the interior angles of the force triangle.

        The force triangle is formed by:
        - F1 from origin
        - F2 from the tip of F1 to the tip of FR
        - FR from origin to its tip (the diagonal of the parallelogram)

        The interior angles are:
        - γ (at the tip of F1, opposite FR) = 180° - (angle between F1 and F2)
        - α (at the tip of FR, opposite F1) = determined by triangle geometry
        - β (at origin, opposite F2) = determined by triangle geometry
        """
        vec1, vec2 = unknown_vectors

        # Get the known angles (stored as input angles in radians)
        theta1_input = vec1._polar_angle_rad
        theta2_input = vec2._polar_angle_rad

        # Get original angle specs for reporting
        wrt1 = getattr(vec1, "_original_wrt", "+x")
        wrt2 = getattr(vec2, "_original_wrt", "+x")

        # Convert wrt to standard angle from +x
        # Support both standard axes and custom coordinate system axes
        coord_sys = getattr(self, "coordinate_system", None)
        base1 = _get_axis_angle(wrt1, coord_sys)
        base2 = _get_axis_angle(wrt2, coord_sys)

        # Compute standard angles from +x axis
        theta1_std = base1 + theta1_input
        theta2_std = base2 + theta2_input

        # Normalize to [0, 2π)
        theta1_std = normalize_angle_positive(theta1_std)
        theta2_std = normalize_angle_positive(theta2_std)
        FR_angle_norm = normalize_angle_positive(FR_angle)

        # Compute resultant components
        FR_x = FR_mag * math.cos(FR_angle)
        FR_y = FR_mag * math.sin(FR_angle)

        # Use linear algebra approach: solve the 2x2 system
        # M1 * [cos(θ1), sin(θ1)] + M2 * [cos(θ2), sin(θ2)] = [FR_x, FR_y]
        #
        # This handles all cases including negative components
        # (when resultant is outside the "cone" of positive component directions)
        cos1, sin1 = math.cos(theta1_std), math.sin(theta1_std)
        cos2, sin2 = math.cos(theta2_std), math.sin(theta2_std)

        # Build matrix A = [[cos1, cos2], [sin1, sin2]]
        det = cos1 * sin2 - cos2 * sin1
        if abs(det) < 1e-10:
            raise ValueError("Cannot solve: vectors are collinear (determinant ≈ 0)")

        # Solve using Cramer's rule
        M1 = (FR_x * sin2 - FR_y * cos2) / det
        M2 = (cos1 * FR_y - sin1 * FR_x) / det

        # Compute the Cartesian coordinates for each vector
        vec1_coords = np.array([M1 * cos1, M1 * sin1, 0.0])
        vec2_coords = np.array([M2 * cos2, M2 * sin2, 0.0])

        # Update vec1
        vec1._coords = vec1_coords
        vec1._unknowns = {}
        vec1.is_known = True
        vec1._magnitude = _helper.create_force_quantity(f"{vec1.name}_magnitude", abs(M1), unit)
        vec1._angle = _helper.create_angle_quantity(f"{vec1.name}_angle", theta1_std)

        # Update vec2
        vec2._coords = vec2_coords
        vec2._unknowns = {}
        vec2.is_known = True
        vec2._magnitude = _helper.create_force_quantity(f"{vec2.name}_magnitude", abs(M2), unit)
        vec2._angle = _helper.create_angle_quantity(f"{vec2.name}_angle", theta2_std)

        # Add variables
        vec1_name = vec1.name or "F_1"
        vec2_name = vec2.name or "F_2"

        self._add_force_variables(vec1_name, abs(M1), theta1_std, resultant._dim, unit, is_known=False)
        self._add_force_variables(vec2_name, abs(M2), theta2_std, resultant._dim, unit, is_known=False)
        self._add_force_variables(resultant_name, FR_mag, FR_angle_norm, resultant._dim, unit, is_known=True)

        # Store on resultant
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", FR_mag, unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", FR_angle_norm)

        # Compute triangle angles for solution steps (for display purposes)
        # Angle between vec1 and vec2 directions
        angle_between = interior_angle(theta1_std, theta2_std)
        # gamma: angle at vertex opposite to resultant (supplementary to angle between)
        gamma = math.pi - angle_between
        # beta: angle at origin between vec1 and FR
        beta = interior_angle(theta1_std, FR_angle_norm)
        # alpha: remaining angle
        alpha = math.pi - gamma - beta
        if alpha < 0:
            alpha = interior_angle(theta2_std, FR_angle_norm)
            beta = math.pi - gamma - alpha

        # Add solution steps using Law of Sines
        # alpha is opposite F1 (vec1), beta is opposite F2 (vec2)
        # Pass the original input angles for showing the calculation
        theta1_input_deg = math.degrees(theta1_input)
        theta2_input_deg = math.degrees(theta2_input)
        self._add_law_of_sines_solution_steps(vec1, vec2, resultant, resultant_name, M1, M2, alpha, beta, gamma, unit, theta1_input_deg, theta2_input_deg)

    def _solve_mixed_unknowns_inverse(
        self,
        unknown_vectors: list[_VectorWithUnknowns],
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        FR_mag: float,
        FR_angle: float,
        unit,
    ) -> None:
        """
        Solve inverse problem with mixed unknowns: one vector has unknown angle (known magnitude),
        the other has unknown magnitude (known angle).

        Given: FR = F1 + F2 where FR is known
        - F1: known magnitude |F1|, unknown angle θ1
        - F2: unknown magnitude |F2|, known angle θ2

        When FR is specified relative to F1 (wrt=F1), we use the triangle method:
        1. Law of Cosines: |F2|² = |FR|² + |F1|² - 2·|FR|·|F1|·cos(θ_FR_from_F1)
        2. Law of Sines: sin(angle_F2_to_FR)/|F1| = sin(θ_FR_from_F1)/|F2|

        The angle between F1 and F2 (call it γ = 45° + φ in Problem 2-16) can be found
        from the law of sines, and then φ (the unknown angle of F1) can be computed.
        """
        # Identify which vector has unknown angle vs unknown magnitude
        vec_with_unknown_angle = None
        vec_with_unknown_magnitude = None

        for vec in unknown_vectors:
            if "angle" in vec._unknowns:
                vec_with_unknown_angle = vec
            if "magnitude" in vec._unknowns:
                vec_with_unknown_magnitude = vec

        if vec_with_unknown_angle is None or vec_with_unknown_magnitude is None:
            raise ValueError("Expected one vector with unknown angle and one with unknown magnitude")

        # Get known values
        # F1: Vector with unknown angle has known magnitude (convert to SI)
        F1_mag_input = vec_with_unknown_angle._polar_magnitude
        if F1_mag_input is None:
            raise ValueError("Vector with unknown angle must have known magnitude")
        # Convert to SI using Quantity.from_value
        F1_mag = Quantity.from_value(F1_mag_input, unit).value if unit else F1_mag_input

        # F2: Vector with unknown magnitude has known angle
        theta2_input = vec_with_unknown_magnitude._polar_angle_rad
        if theta2_input is None:
            raise ValueError("Vector with unknown magnitude must have known angle")

        # Convert FR_mag to SI as well
        if unit:
            FR_mag_qty = Quantity.from_value(FR_mag, unit)
            if FR_mag_qty.value is not None:
                FR_mag = FR_mag_qty.value

        # Get wrt references
        wrt1 = getattr(vec_with_unknown_angle, "_original_wrt", "+x")
        wrt2 = getattr(vec_with_unknown_magnitude, "_original_wrt", "+x")
        wrt_R = getattr(resultant, "_original_wrt", "+x")

        coord_sys = getattr(self, "coordinate_system", None)

        # Check if resultant is specified relative to F1 (the vector with unknown angle)
        # This is indicated by wrt_R starting with '@' (vector reference)
        is_wrt_vector_ref = wrt_R.startswith("@")

        if is_wrt_vector_ref:
            # Triangle method: FR is specified at angle θ_R relative to F1
            # θ_R is stored in resultant._polar_angle_rad
            theta_R_from_F1 = resultant._polar_angle_rad  # angle of FR from F1

            # Law of Cosines to find |F2|:
            # |F2|² = |FR|² + |F1|² - 2·|FR|·|F1|·cos(θ_R_from_F1)
            F2_mag = _law_of_cosines(FR_mag, F1_mag, theta_R_from_F1)

            # Get base angle for F2 (known angle)
            base2 = _get_axis_angle(wrt2, coord_sys)
            theta2_std = base2 + theta2_input  # F2's absolute angle (standard)

            # Solve for θ1 (F1's standard angle) using vector equation:
            # FR = F1 + F2
            # FR is at angle (θ1 + θ_R_from_F1) with magnitude FR_mag
            #
            # FR_x = FR_mag * cos(θ1 + θ_R_from_F1) = F1_mag * cos(θ1) + F2_mag * cos(θ2)
            # FR_y = FR_mag * sin(θ1 + θ_R_from_F1) = F1_mag * sin(θ1) + F2_mag * sin(θ2)
            #
            # Using angle addition:
            # FR_mag * [cos(θ1)cos(θ_R) - sin(θ1)sin(θ_R)] = F1_mag * cos(θ1) + F2_mag * cos(θ2)
            # FR_mag * [sin(θ1)cos(θ_R) + cos(θ1)sin(θ_R)] = F1_mag * sin(θ1) + F2_mag * sin(θ2)
            #
            # Let c1 = cos(θ1), s1 = sin(θ1), cR = cos(θ_R_from_F1), sR = sin(θ_R_from_F1)
            # c2 = cos(θ2_std), s2 = sin(θ2_std)
            #
            # Eq1: FR_mag * (c1*cR - s1*sR) = F1_mag * c1 + F2_mag * c2
            # Eq2: FR_mag * (s1*cR + c1*sR) = F1_mag * s1 + F2_mag * s2
            #
            # Rearranging:
            # Eq1: c1 * (FR_mag*cR - F1_mag) - s1 * (FR_mag*sR) = F2_mag * c2
            # Eq2: s1 * (FR_mag*cR - F1_mag) + c1 * (FR_mag*sR) = F2_mag * s2
            #
            # Let A = FR_mag*cR - F1_mag, B = FR_mag*sR
            # A*c1 - B*s1 = F2_mag*c2  ... (1)
            # A*s1 + B*c1 = F2_mag*s2  ... (2)
            #
            # From (1): c1 = (F2_mag*c2 + B*s1) / A
            # Sub into (2): A*s1 + B*(F2_mag*c2 + B*s1)/A = F2_mag*s2
            # A²*s1 + B*F2_mag*c2 + B²*s1 = A*F2_mag*s2
            # s1*(A² + B²) = A*F2_mag*s2 - B*F2_mag*c2
            # s1 = F2_mag * (A*s2 - B*c2) / (A² + B²)

            # Use the triangle method (law of sines) to find the angle
            # In the force triangle:
            # - θ_R_from_F1 is the angle at the F1 vertex (between F1 and FR)
            # - β is the angle at the FR vertex (between F1 and F2 sides)
            # - γ is the angle at the F2 vertex (between FR and F1 sides)
            #
            # Law of sines: sin(γ)/|FR| = sin(θ_R_from_F1)/|F2|
            # γ is the interior angle at the F1 tip, which equals the angle between
            # the directions of -F1 and F2. This is related to the frame geometry.

            # Law of sines to find γ (angle at F1 tip in force triangle)
            sin_gamma = FR_mag * math.sin(abs(theta_R_from_F1)) / F2_mag
            sin_gamma = max(-1.0, min(1.0, sin_gamma))

            # Two possible values for γ: asin and π - asin
            gamma1 = math.asin(sin_gamma)
            gamma2 = math.pi - gamma1

            # Get base angle for wrt1 and wrt2
            base1 = _get_axis_angle(wrt1, coord_sys)
            base2 = _get_axis_angle(wrt2, coord_sys)
            theta2_std = base2 + theta2_input  # F2's absolute angle (standard)

            # The angle γ is between (-F1 direction) and (F2 direction)
            # So: theta2_std - (theta1_std + π) = ±γ
            # Therefore: theta1_std = theta2_std - π ∓ γ

            # Try both solutions and pick the one with valid input angle
            candidates = []
            for gamma in [gamma1, gamma2]:
                for sign in [1, -1]:
                    theta1_std_candidate = theta2_std - math.pi - sign * gamma
                    theta1_std_candidate = normalize_angle_positive(theta1_std_candidate)

                    # Compute input angle relative to reference axis
                    theta1_input_candidate = theta1_std_candidate - base1
                    # Normalize to [-π, π]
                    if theta1_input_candidate > math.pi:
                        theta1_input_candidate -= 2 * math.pi
                    if theta1_input_candidate < -math.pi:
                        theta1_input_candidate += 2 * math.pi

                    candidates.append((theta1_std_candidate, theta1_input_candidate, gamma))

            # Select the candidate where input angle is in valid range [0, π/4] for this problem
            # More generally, prefer smaller positive angles from the reference axis
            theta1_std = None
            theta1_input = None
            best_gamma = None

            for theta1_std_c, theta1_input_c, gamma_c in candidates:
                # For problems like 2-16 where constraint is 0 ≤ φ ≤ 45°
                # the input angle should be positive and ≤ 45°
                if 0 <= theta1_input_c <= math.pi / 4:
                    theta1_std = theta1_std_c
                    theta1_input = theta1_input_c
                    best_gamma = gamma_c
                    break

            # If no candidate in [0, 45°], try [0, 90°]
            if theta1_std is None:
                for theta1_std_c, theta1_input_c, gamma_c in candidates:
                    if 0 <= theta1_input_c <= math.pi / 2:
                        theta1_std = theta1_std_c
                        theta1_input = theta1_input_c
                        best_gamma = gamma_c
                        break

            # Fallback: pick smallest positive angle
            if theta1_std is None:
                positive_candidates = [(t, i, g) for t, i, g in candidates if i >= 0]
                if positive_candidates:
                    theta1_std, theta1_input, best_gamma = min(positive_candidates, key=lambda x: x[1])
                else:
                    # Last resort: first candidate
                    theta1_std, theta1_input, best_gamma = candidates[0]

            # For solution step display
            beta = math.pi - abs(theta_R_from_F1) - best_gamma
            gamma = best_gamma

        else:
            # Original Cartesian approach when FR is specified relative to a fixed axis
            # (This won't work well when FR is relative to unknown vector)
            raise NotImplementedError("Mixed unknowns solver currently requires resultant to be specified relative to the vector with unknown angle (wrt=vector)")

        # Verify theta1_input was computed (should always be set if we reached this point)
        assert theta1_input is not None, "theta1_input should have been set in the if/else block above"

        # Normalize the computed angle
        theta1_std = normalize_angle_positive(theta1_std)
        theta2_std = normalize_angle_positive(theta2_std)

        # Compute Cartesian coordinates
        cos1, sin1 = math.cos(theta1_std), math.sin(theta1_std)
        cos2, sin2 = math.cos(theta2_std), math.sin(theta2_std)
        vec1_coords = np.array([F1_mag * cos1, F1_mag * sin1, 0.0])
        vec2_coords = np.array([F2_mag * cos2, F2_mag * sin2, 0.0])

        # Update vec_with_unknown_angle (F1)
        vec_with_unknown_angle._coords = vec1_coords
        # Save original unknowns before clearing for reporting
        vec_with_unknown_angle._original_unknowns = vec_with_unknown_angle._unknowns.copy()
        vec_with_unknown_angle._unknowns = {}
        vec_with_unknown_angle.is_known = True
        vec_with_unknown_angle._magnitude = _helper.create_force_quantity(f"{vec_with_unknown_angle.name}_magnitude", F1_mag, unit)
        vec_with_unknown_angle._angle = _helper.create_angle_quantity(f"{vec_with_unknown_angle.name}_angle", theta1_std)
        vec_with_unknown_angle._polar_angle_rad = theta1_input
        vec_with_unknown_angle._original_angle = math.degrees(theta1_input)

        # Update vec_with_unknown_magnitude (F2)
        vec_with_unknown_magnitude._coords = vec2_coords
        # Save original unknowns before clearing for reporting
        vec_with_unknown_magnitude._original_unknowns = vec_with_unknown_magnitude._unknowns.copy()
        vec_with_unknown_magnitude._unknowns = {}
        vec_with_unknown_magnitude.is_known = True
        vec_with_unknown_magnitude._magnitude = _helper.create_force_quantity(f"{vec_with_unknown_magnitude.name}_magnitude", F2_mag, unit)
        vec_with_unknown_magnitude._angle = _helper.create_angle_quantity(f"{vec_with_unknown_magnitude.name}_angle", theta2_std)
        vec_with_unknown_magnitude._polar_magnitude = F2_mag

        # Update resultant coordinates (now that we know F1's direction)
        FR_angle_std = theta1_std + theta_R_from_F1  # FR is θ_R from F1
        FR_angle_std = normalize_angle_positive(FR_angle_std)
        FR_coords = np.array([FR_mag * math.cos(FR_angle_std), FR_mag * math.sin(FR_angle_std), 0.0])
        resultant._coords = FR_coords

        # Add variables to the problem
        vec1_name = vec_with_unknown_angle.name or "F_1"
        vec2_name = vec_with_unknown_magnitude.name or "F_2"

        self._add_force_variables(vec1_name, F1_mag, theta1_std, resultant._dim, unit, is_known=False)
        self._add_force_variables(vec2_name, F2_mag, theta2_std, resultant._dim, unit, is_known=False)
        self._add_force_variables(resultant_name, FR_mag, FR_angle_std, resultant._dim, unit, is_known=True)

        # Store on resultant
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", FR_mag, unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", FR_angle_std)

        # Add solution steps
        self._add_mixed_unknowns_solution_steps(
            vec_with_unknown_angle,
            vec_with_unknown_magnitude,
            resultant,
            resultant_name,
            F1_mag,
            F2_mag,
            theta1_input,
            theta2_input,
            theta1_std,
            theta2_std,
            FR_mag,
            FR_angle_std,
            wrt1,
            wrt2,
            unit,
            theta_R_from_F1,
            beta,
            gamma,
        )

    def _add_mixed_unknowns_solution_steps(
        self,
        vec1: _VectorWithUnknowns,  # Has unknown angle
        vec2: _VectorWithUnknowns,  # Has unknown magnitude
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        F1_mag: float,
        F2_mag: float,
        theta1_input: float,
        theta2_input: float,
        theta1_std: float,  # noqa: ARG002
        theta2_std: float,  # noqa: ARG002
        FR_mag: float,
        FR_angle: float,  # noqa: ARG002
        wrt1: str,
        wrt2: str,
        unit,
        theta_R_from_F1: float | None = None,
        beta_triangle: float | None = None,  # noqa: ARG002
        gamma_triangle: float | None = None,
    ) -> None:
        """Add solution steps for mixed unknowns case (triangle method).

        This handles Problem 2-16 type problems where:
        - vec1 (F_BA): known magnitude, unknown angle φ from -x
        - vec2 (F_BC): unknown magnitude, known angle from +x
        - resultant (F): known magnitude and angle (θ = 30°) relative to vec1

        Following the textbook solution:
        Step 1: Law of Cosines to find |F_BC|
        Step 2: Law of Sines to find φ (angle of F_BA)
        """
        unit_symbol, si_factor = _get_unit_info(unit)
        if not unit_symbol:
            unit_symbol = "N"

        vec1_name = vec1.name or "F_1"
        vec2_name = vec2.name or "F_2"

        vec1_latex = _latex_name(vec1_name)
        vec2_latex = _latex_name(vec2_name)
        resultant_latex = _latex_name(resultant_name)

        theta1_input_deg = math.degrees(theta1_input)
        theta2_input_deg = math.degrees(theta2_input)
        theta_R_deg = math.degrees(theta_R_from_F1) if theta_R_from_F1 is not None else 0

        # Convert to display units
        F1_display = _to_display_value(F1_mag, si_factor)
        F2_display = _to_display_value(F2_mag, si_factor)
        FR_display = _to_display_value(FR_mag, si_factor)

        # For Problem 2-16: F_BC is at -45° from +x, so the angle between F_BA and F_BC
        # in the force triangle is (45° + φ) where φ is the angle of F_BA from -x
        # The triangle has:
        # - Angle θ = 30° at F_BA vertex (between F and F_BA)
        # - Angle (45° + φ) at F vertex (between F_BA and F_BC)
        # - Angle β at F_BC vertex

        # Step 1: Calculate angle between F_BA and F_R
        # This is the angle θ given in the problem (angle of resultant relative to vec1)
        # Use multi-line format for consistency with other problems (left-aligned flalign*)
        # The newline character triggers the multi-line path in the LaTeX renderer
        step1_sub = f"∠({vec1_latex},{resultant_latex}) = {theta_R_deg:.0f}° (given)\n= {theta_R_deg:.0f}°"

        self._add_solution_step(
            SolutionStep(
                target=f"∠({vec1_latex},{resultant_latex})",
                method="From problem definition",
                description=f"Angle between {vec1_name} and {resultant_name}",
                substitution=step1_sub,
            )
        )

        # Step 2: Law of Cosines to find |F_BC|
        # |F_BC|² = |F|² + |F_BA|² - 2·|F|·|F_BA|·cos(θ)
        step2_sub = f"|{vec2_latex}| = sqrt({FR_display:.0f}² + {F1_display:.0f}² - 2·{FR_display:.0f}·{F1_display:.0f}·cos({theta_R_deg:.0f}°))\n= {F2_display:.0f}\\ \\text{{{unit_symbol}}}"

        self._add_solution_step(
            SolutionStep(
                target=f"|{vec2_latex}| using Eq 1",
                method="Law of Cosines",
                description=f"Calculate |{vec2_name}| using Law of Cosines",
                equation_for_list=f"|{vec2_latex}|² = |{resultant_latex}|² + |{vec1_latex}|² - 2·|{resultant_latex}|·|{vec1_latex}|·cos(∠({vec1_latex},{resultant_latex}))",
                substitution=step2_sub,
            )
        )

        # Step 3: Law of Sines to find ∠(F_BA, F_BC)
        # sin(∠(F_BA,F_BC))/|F_R| = sin(∠(F_BA,F_R))/|F_BC|
        # For Problem 2-16: sin(∠(F_BA,F_BC))/850 = sin(30°)/434
        if gamma_triangle is not None:
            gamma_deg = math.degrees(gamma_triangle)
            # gamma is the angle between F_BA and F_BC in the force triangle
            # For Problem 2-16: this is (45° + φ) where φ is the angle of F_BA from -x

            # The angle between vec1 and vec2 = |θ2_input| + φ
            angle_between_vecs = abs(theta2_input_deg) + theta1_input_deg

            step3_sub = f"∠({vec1_latex},{vec2_latex}) = sin⁻¹({FR_display:.0f}·sin({theta_R_deg:.0f}°)/{F2_display:.0f})\n= {angle_between_vecs:.1f}°"

            self._add_solution_step(
                SolutionStep(
                    target=f"∠({vec1_latex},{vec2_latex}) using Eq 2",
                    method="Law of Sines",
                    description=f"Calculate angle between {vec1_name} and {vec2_name} using Law of Sines",
                    equation_for_list=f"sin(∠({vec1_latex},{vec2_latex}))/|{resultant_latex}| = sin(∠({vec1_latex},{resultant_latex}))/|{vec2_latex}|",
                    substitution=step3_sub,
                )
            )

            # Step 4: Calculate ∠(-x, F_BA) = φ
            # ∠(F_BA, F_BC) = |θ_BC| + φ, so φ = ∠(F_BA, F_BC) - |θ_BC|
            # Format the reference axis for display
            axis_label = wrt1.replace("+", "").replace("-", "")  # Get just 'x' or 'y'
            sign = "-" if wrt1.startswith("-") else "+"

            step4_sub = f"∠({wrt1},{vec1_latex}) = ∠({vec1_latex},{vec2_latex}) - |∠({wrt2},{vec2_latex})|\n= {angle_between_vecs:.1f}° - {abs(theta2_input_deg):.0f}°\n= {theta1_input_deg:.1f}°"

            self._add_solution_step(
                SolutionStep(
                    target=f"∠({wrt1},{vec1_latex})",
                    method="Angle subtraction",
                    description=f"Calculate {vec1_name} angle from {wrt1}",
                    substitution=step4_sub,
                )
            )

    def _solve_with_unknown_resultant_magnitude(
        self,
        known_vectors: list[_Vector],
        unknown_vectors: list[_VectorWithUnknowns],
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        FR_angle: float,
        unit,
    ) -> None:
        """
        Solve when resultant direction is known but magnitude is unknown.

        This handles the case where:
        - F_R direction is known (e.g., along +x axis)
        - F_R magnitude is unknown
        - One component vector has known magnitude but unknown angle
        - Other component vector(s) are fully known

        The constraint is: F_A + F_B = F_R where F_R is along a known direction.

        For Problem 2-12:
        - F_A: 8000 N, unknown angle (wrt +y)
        - F_B: 6000 N at 40° (wrt -y) - fully known
        - F_R: along +x axis (unknown magnitude)

        We use the constraint that F_R_y = 0 (no y-component) to solve for F_A's angle,
        then compute F_R_x from the x-components.
        """
        if len(known_vectors) != 1 or len(unknown_vectors) != 1:
            raise NotImplementedError(f"Unknown resultant magnitude solve requires exactly 1 known + 1 unknown vector, got {len(known_vectors)} known + {len(unknown_vectors)} unknown")

        known_vec = known_vectors[0]
        unknown_vec = unknown_vectors[0]

        # Check what's unknown about the unknown vector
        has_unknown_angle = "angle" in unknown_vec.unknowns
        has_unknown_magnitude = "magnitude" in unknown_vec.unknowns

        # Case 1: Unknown vector has known magnitude, unknown angle (Problem 2-12)
        # Case 2: Unknown vector has unknown magnitude, known angle (Problem 2-14)
        if has_unknown_magnitude and not has_unknown_angle:
            # Case 2: Known angle, unknown magnitude - use Law of Sines
            self._solve_unknown_resultant_with_known_angles(known_vec, unknown_vec, resultant, resultant_name, FR_angle, unit)
            return

        # Case 1: Unknown angle, known magnitude
        if not has_unknown_angle:
            raise NotImplementedError("Unknown resultant magnitude solve requires the unknown vector to have unknown angle or unknown magnitude")
        unknown_magnitude = getattr(unknown_vec, "_polar_magnitude", None)
        if unknown_magnitude is None:
            raise NotImplementedError("Unknown resultant magnitude solve requires the unknown vector to have known magnitude")

        # Get known vector components
        F_known_coords = known_vec._coords
        F_known_mag, F_known_angle = _magnitude_and_angle_from_coords(F_known_coords)

        # Get unknown vector's known magnitude
        F_unknown_mag = unknown_magnitude

        # Get wrt reference for unknown vector to compute base angle
        wrt = getattr(unknown_vec, "_original_wrt", "+x")
        coord_sys = getattr(self, "coordinate_system", None)
        base_angle_rad = _get_axis_angle(wrt, coord_sys)

        # The constraint is that F_R is along the direction FR_angle.
        # F_R = F_unknown + F_known
        # For F_R to be along FR_angle, the perpendicular component must be zero.
        #
        # If FR_angle = 0 (along +x), then F_R_y = 0.
        # F_unknown_y + F_known_y = 0
        # |F_unknown| * sin(base + theta) + F_known_y = 0
        # sin(base + theta) = -F_known_y / |F_unknown|
        #
        # General case: project onto perpendicular direction
        FR_perp_angle = FR_angle + math.pi / 2  # perpendicular to resultant direction

        # Perpendicular component of known vector
        F_known_perp = F_known_coords[0] * math.sin(FR_perp_angle) - F_known_coords[1] * math.cos(FR_perp_angle)
        # Actually let's use the simpler approach: dot product with perpendicular unit vector
        perp_x = -math.sin(FR_angle)
        perp_y = math.cos(FR_angle)
        F_known_perp = F_known_coords[0] * perp_x + F_known_coords[1] * perp_y

        # For unknown vector:
        # F_unknown_perp = |F_unknown| * (cos(base + theta) * perp_x + sin(base + theta) * perp_y)
        # = |F_unknown| * sin(base + theta - FR_angle)  (using angle subtraction)
        # Actually, let's just expand:
        # cos(base + theta) * perp_x + sin(base + theta) * perp_y
        # = cos(base + theta) * (-sin(FR_angle)) + sin(base + theta) * cos(FR_angle)
        # = sin(base + theta - FR_angle)

        # Constraint: F_unknown_perp + F_known_perp = 0
        # |F_unknown| * sin(base + theta - FR_angle) = -F_known_perp
        # sin(base + theta - FR_angle) = -F_known_perp / |F_unknown|

        sin_value = -F_known_perp / F_unknown_mag

        # Clamp to valid range for asin (handle numerical precision)
        if sin_value > 1.0:
            sin_value = 1.0
        elif sin_value < -1.0:
            sin_value = -1.0

        # Solve for (base + theta - FR_angle)
        angle_offset = math.asin(sin_value)

        # There are two solutions: angle_offset and (pi - angle_offset)
        # We need to pick the one that makes sense for the problem geometry
        # For now, try both and pick the one that gives positive resultant magnitude

        solutions = []
        for offset in [angle_offset, math.pi - angle_offset]:
            # theta = offset + FR_angle - base
            theta = offset + FR_angle - base_angle_rad

            # Compute unknown vector components
            total_angle = base_angle_rad + theta
            F_unknown_x = F_unknown_mag * math.cos(total_angle)
            F_unknown_y = F_unknown_mag * math.sin(total_angle)

            # Compute resultant components
            FR_x = F_unknown_x + F_known_coords[0]
            FR_y = F_unknown_y + F_known_coords[1]

            # Resultant magnitude (should be along FR_angle direction)
            FR_computed_mag = FR_x * math.cos(FR_angle) + FR_y * math.sin(FR_angle)

            # Check if the solution is valid (resultant should be in the expected direction)
            if FR_computed_mag > 0:
                solutions.append((theta, total_angle, FR_computed_mag, F_unknown_x, F_unknown_y))

        if not solutions:
            raise ValueError("No valid solution found for unknown resultant magnitude problem")

        # Pick the solution (prefer positive angle if multiple valid solutions)
        solution = solutions[0]
        if len(solutions) > 1:
            # Pick solution with theta closest to 0 or smallest absolute value
            solution = min(solutions, key=lambda s: abs(s[0]))

        theta, total_angle, FR_mag, F_unknown_x, F_unknown_y = solution

        # Update unknown vector
        unknown_vec._coords = np.array([F_unknown_x, F_unknown_y, 0.0])
        unknown_vec._unknowns = {}
        unknown_vec.is_known = True
        unknown_vec._magnitude = _helper.create_force_quantity(f"{unknown_vec.name}_magnitude", F_unknown_mag, unit)
        unknown_vec._angle = _helper.create_angle_quantity(f"{unknown_vec.name}_angle", total_angle)
        unknown_vec._original_angle = math.degrees(theta)  # Store the angle relative to wrt

        # Update resultant
        FR_x = F_unknown_x + F_known_coords[0]
        FR_y = F_unknown_y + F_known_coords[1]
        resultant._coords = np.array([FR_x, FR_y, 0.0])
        resultant._unknowns = {}
        resultant.is_known = True
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", FR_mag, unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", FR_angle)

        # Add variables
        vec_name = unknown_vec.name or "F_unknown"
        known_name = known_vec.name or "F_known"

        # For unknown_vec: magnitude was known, angle was unknown (solved)
        self._add_force_variables(vec_name, F_unknown_mag, total_angle, resultant._dim, unit, is_known=False)
        # Override: magnitude was actually known at input time
        self._original_variable_states[f"{vec_name}_mag"] = True

        # Known vector: both magnitude and angle are known
        self._add_force_variables(known_name, F_known_mag, F_known_angle, resultant._dim, unit, is_known=True)

        # Resultant: angle was known, magnitude was unknown (solved)
        self._add_force_variables(resultant_name, FR_mag, FR_angle, resultant._dim, unit, is_known=False)
        # Override: angle was actually known at input time
        self._original_variable_states[f"{resultant_name}_angle"] = True

        # Add solution steps for this solving approach
        self._add_unknown_resultant_magnitude_steps(known_vec, unknown_vec, resultant, resultant_name, F_unknown_mag, theta, base_angle_rad, FR_mag, FR_angle, unit)

    def _solve_unknown_resultant_with_known_angles(
        self,
        known_vec: _Vector,
        unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        FR_angle: float,
        unit,
    ) -> None:
        """
        Solve for unknown vector magnitude and resultant magnitude when all angles are known.

        This handles the case where:
        - One component vector is fully known (magnitude and angle)
        - One component vector has known angle but unknown magnitude
        - Resultant has known angle but unknown magnitude

        Uses the Law of Sines in the force triangle:
            |F_known| / sin(angle opposite F_known) = |F_unknown| / sin(angle opposite F_unknown)
                                                    = |F_R| / sin(angle opposite F_R)

        For Problem 2-14:
        - F_a: 30 lbf at 0° from +a (known)
        - F_b: unknown magnitude at 0° from -b
        - F: unknown magnitude at 80° from -b
        """
        # Get known vector properties
        F_known_coords = known_vec._coords
        F_known_mag, F_known_angle = _magnitude_and_angle_from_coords(F_known_coords)

        # Get unknown vector's known angle (standard angle from input)
        unknown_angle = unknown_vec._polar_angle_rad
        if unknown_angle is None:
            raise ValueError("Unknown vector must have a known angle")

        # Convert unknown angle to standard if needed (using wrt reference)
        unknown_wrt = getattr(unknown_vec, "_original_wrt", "+x")
        unknown_standard_angle = self._get_standard_angle(unknown_angle, unknown_wrt)

        # Convert resultant's angle to standard form (FR_angle is the input angle)
        resultant_wrt = getattr(resultant, "_original_wrt", "+x")
        FR_standard_angle = self._get_standard_angle(FR_angle, resultant_wrt)

        # Calculate the interior angles of the force triangle
        # The force triangle has vertices at:
        # - Origin (where F_known and F_R start)
        # - Tip of F_known (where F_unknown starts in head-to-tail)
        # - Tip of F_R (end point)
        #
        # Using the Law of Sines:
        # |F_known| / sin(angle_opposite_known) = |F_unknown| / sin(angle_opposite_unknown)
        #                                        = |F_R| / sin(angle_opposite_resultant)

        # angle_opposite_unknown = interior angle between F_known and F_R (at origin)
        angle_opposite_unknown = interior_angle(F_known_angle, FR_standard_angle)

        # angle_opposite_resultant = interior angle between -F_known and F_unknown (at tip of F_known)
        # In head-to-tail, at tip of F_known, we have -F_known meeting F_unknown
        angle_opposite_resultant = interior_angle(F_known_angle + math.pi, unknown_standard_angle)

        # angle_opposite_known = 180 - other two (triangle sum property)
        angle_opposite_known = math.pi - angle_opposite_unknown - angle_opposite_resultant

        # Apply Law of Sines
        # |F_known| / sin(angle_opposite_known) = |F_unknown| / sin(angle_opposite_unknown)
        #                                        = |F_R| / sin(angle_opposite_resultant)
        sin_opposite_known = math.sin(angle_opposite_known)
        sin_opposite_unknown = math.sin(angle_opposite_unknown)
        sin_opposite_resultant = math.sin(angle_opposite_resultant)

        if abs(sin_opposite_known) < 1e-10:
            raise ValueError("Cannot solve: angle opposite to known vector is zero")

        ratio = F_known_mag / sin_opposite_known
        F_unknown_mag = ratio * sin_opposite_unknown
        FR_mag = ratio * sin_opposite_resultant

        # Handle negative magnitudes (can happen if angles are obtuse)
        F_unknown_mag = abs(F_unknown_mag)
        FR_mag = abs(FR_mag)

        # Compute unknown vector coordinates
        F_unknown_x = F_unknown_mag * math.cos(unknown_standard_angle)
        F_unknown_y = F_unknown_mag * math.sin(unknown_standard_angle)

        # Update unknown vector
        unknown_vec._coords = np.array([F_unknown_x, F_unknown_y, 0.0])
        unknown_vec._unknowns = {}
        unknown_vec.is_known = True
        unknown_vec._magnitude = _helper.create_force_quantity(f"{unknown_vec.name}_magnitude", F_unknown_mag, unit)
        unknown_vec._angle = _helper.create_angle_quantity(f"{unknown_vec.name}_angle", unknown_standard_angle)

        # Update resultant
        FR_x = FR_mag * math.cos(FR_standard_angle)
        FR_y = FR_mag * math.sin(FR_standard_angle)
        resultant._coords = np.array([FR_x, FR_y, 0.0])
        resultant._unknowns = {}
        resultant.is_known = True
        resultant._magnitude = _helper.create_force_quantity(f"{resultant_name}_magnitude", FR_mag, unit)
        resultant._angle = _helper.create_angle_quantity(f"{resultant_name}_angle", FR_standard_angle)

        # Add variables
        vec_name = unknown_vec.name or "F_unknown"
        known_name = known_vec.name or "F_known"

        # For unknown_vec: magnitude was unknown, angle was known
        self._add_force_variables(vec_name, F_unknown_mag, unknown_standard_angle, resultant._dim, unit, is_known=False)
        # Override: angle was actually known at input time
        self._original_variable_states[f"{vec_name}_angle"] = True

        # Known vector: both magnitude and angle are known
        self._add_force_variables(known_name, F_known_mag, F_known_angle, resultant._dim, unit, is_known=True)

        # Resultant: both magnitude and angle were unknown (but angle was constrained)
        self._add_force_variables(resultant_name, FR_mag, FR_standard_angle, resultant._dim, unit, is_known=False)
        # Override: angle was actually known at input time
        self._original_variable_states[f"{resultant_name}_angle"] = True

        # Get input angles for display
        unknown_input_deg = math.degrees(unknown_angle)
        resultant_input_deg = math.degrees(getattr(resultant, "_polar_angle_rad", FR_angle))

        # Add solution steps using the Law of Sines approach
        self._add_known_angles_unknown_magnitudes_steps(
            known_vec,
            unknown_vec,
            resultant,
            resultant_name,
            F_known_mag,
            F_unknown_mag,
            FR_mag,
            angle_opposite_known,
            angle_opposite_unknown,
            angle_opposite_resultant,
            unknown_input_deg,
            resultant_input_deg,
            unit,
        )

    def _get_standard_angle(self, input_angle_rad: float, wrt: str) -> float:
        """Convert an input angle (relative to wrt axis) to standard angle (from +x CCW)."""
        coord_sys = getattr(self, "coordinate_system", None)
        base_angle = _get_axis_angle(wrt, coord_sys)
        return normalize_angle_positive(base_angle + input_angle_rad)

    def _compute_angle_display(
        self,
        vec1: _Vector | _VectorWithUnknowns,
        vec2: _Vector | _VectorWithUnknowns,
        interior_angle_deg: float,
        vec1_std_override: float | None = None,
        vec1_input_override: float | None = None,
        vec2_std_override: float | None = None,
        vec2_input_override: float | None = None,
        vec1_name_override: str | None = None,
        vec2_name_override: str | None = None,
    ) -> str:
        """
        Compute angle display string between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector
            interior_angle_deg: The interior angle result in degrees
            vec1_std_override: Override for vec1's standard angle (radians)
            vec1_input_override: Override for vec1's input angle (degrees)
            vec2_std_override: Override for vec2's standard angle (radians)
            vec2_input_override: Override for vec2's input angle (degrees)
            vec1_name_override: Override for vec1's display name
            vec2_name_override: Override for vec2's display name

        Returns:
            Formatted display string showing angle calculation
        """
        # Extract vec1 properties
        vec1_wrt = getattr(vec1, "_original_wrt", "+x")
        if vec1_std_override is not None:
            vec1_std = vec1_std_override
        else:
            vec1_std = self._get_standard_angle(getattr(vec1, "_polar_angle_rad", 0.0), vec1_wrt)
        if vec1_input_override is not None:
            vec1_input = vec1_input_override
        else:
            vec1_input = math.degrees(getattr(vec1, "_polar_angle_rad", 0.0))
            if vec1_input == 0 and hasattr(vec1, "_original_angle"):
                vec1_input = vec1._original_angle
        vec1_name = vec1_name_override or getattr(vec1, "name", "F_1")

        # Extract vec2 properties
        vec2_wrt = getattr(vec2, "_original_wrt", "+x")
        if vec2_std_override is not None:
            vec2_std = vec2_std_override
        else:
            vec2_std = self._get_standard_angle(getattr(vec2, "_polar_angle_rad", 0.0), vec2_wrt)
        if vec2_input_override is not None:
            vec2_input = vec2_input_override
        else:
            vec2_input = getattr(vec2, "_original_angle", None) or np.degrees(getattr(vec2, "_polar_angle_rad", 0.0))
        vec2_name = vec2_name_override or getattr(vec2, "name", "F_2")

        coord_sys = getattr(self, "coordinate_system", None)

        return compute_angle_between_display(
            first_vector_standard_angle_deg=math.degrees(vec1_std),
            second_vector_standard_angle_deg=math.degrees(vec2_std),
            first_vector_input_angle_deg=vec1_input,
            second_vector_input_angle_deg=vec2_input,
            first_vector_reference_axis=vec1_wrt,
            second_vector_reference_axis=vec2_wrt,
            first_vector_name=vec1_name,
            second_vector_name=vec2_name,
            interior_angle_result_deg=interior_angle_deg,
            coordinate_system=coord_sys,
        )

    def _add_known_angles_unknown_magnitudes_steps(
        self,
        known_vec: _Vector,
        unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        F_known_mag: float,
        F_unknown_mag: float,
        FR_mag: float,
        angle_opposite_known: float,
        angle_opposite_unknown: float,
        angle_opposite_resultant: float,
        unknown_input_deg: float,
        resultant_input_deg: float,
        unit,
    ) -> None:
        """Add solution steps for known angles, unknown magnitudes case (Law of Sines)."""
        unit_symbol, si_factor = _get_unit_info(unit)
        if not unit_symbol:
            unit_symbol = "N"

        known_name = known_vec.name or "F_known"
        unknown_name = unknown_vec.name or "F_unknown"

        F_known_display = _to_display_value(F_known_mag, si_factor)
        F_unknown_display = _to_display_value(F_unknown_mag, si_factor)
        FR_display = _to_display_value(FR_mag, si_factor)

        # Step 1: Compute triangle angles
        # Get the input angles in degrees for display
        known_input_deg = math.degrees(getattr(known_vec, "_polar_angle_rad", 0.0))
        if known_input_deg == 0 and hasattr(known_vec, "_original_angle"):
            known_input_deg = known_vec._original_angle

        # Angle between unknown and resultant (opposite to known vector)
        alpha_deg = math.degrees(angle_opposite_known)
        # Angle between known and resultant (opposite to unknown vector)
        beta_deg = math.degrees(angle_opposite_unknown)
        # Angle between known and unknown (opposite to resultant)
        gamma_deg = math.degrees(angle_opposite_resultant)

        # Build angle computation displays for the two triangle angles
        # Both angles are measured from first_vector to the resultant
        angle_configs = [
            # (vector, interior_angle_deg, input_deg_override)
            (unknown_vec, alpha_deg, unknown_input_deg),  # unknown-resultant angle
            (known_vec, beta_deg, known_input_deg),  # known-resultant angle
        ]

        angle_displays = []
        for vec, interior_deg, input_override in angle_configs:
            display = self._compute_angle_display(
                vec,
                resultant,
                interior_deg,
                vec1_input_override=input_override,
                vec2_input_override=resultant_input_deg,
                vec2_name_override=resultant_name,
            )
            angle_displays.append(display)

        # Third angle from triangle sum
        angle_displays.append(f"∠({known_name},{unknown_name}) = 180° - {alpha_deg:.0f}° - {beta_deg:.0f}°\n= {gamma_deg:.0f}°")

        step1_content = "\n".join(angle_displays)

        self.solving_history.append(
            {
                "target_variable": "triangle angles",
                "equation_str": "",  # No equation for angle computation step
                "equation_inline": "",
                "substituted_equation": step1_content,
            }
        )

        # Step 2: Solve for unknown magnitude using Law of Sines
        step2_sub = format_law_of_sines_substitution(unknown_name, F_known_display, beta_deg, alpha_deg, F_unknown_display, unit_symbol)

        self.solving_history.append(
            {
                "target_variable": f"|{unknown_name}| using Eq 1",
                "equation_str": f"|{unknown_name}|/sin(∠({known_name},{resultant_name})) = |{known_name}|/sin(∠({unknown_name},{resultant_name}))",
                "equation_inline": "",
                "substituted_equation": step2_sub,
            }
        )

        # Step 3: Solve for resultant magnitude using Law of Sines
        step3_sub = format_law_of_sines_substitution(resultant_name, F_known_display, gamma_deg, alpha_deg, FR_display, unit_symbol)

        self.solving_history.append(
            {
                "target_variable": f"|{resultant_name}| using Eq 2",
                "equation_str": f"|{resultant_name}|/sin(∠({known_name},{unknown_name})) = |{known_name}|/sin(∠({unknown_name},{resultant_name}))",
                "equation_inline": "",
                "substituted_equation": step3_sub,
            }
        )

    def _add_law_of_sines_solution_steps(
        self,
        vec1: _VectorWithUnknowns,
        vec2: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        M1: float,
        M2: float,
        alpha: float,
        beta: float,
        gamma: float,
        unit,
        theta1_input_deg: float,
        theta2_input_deg: float,
    ) -> None:
        """Add solution steps for two unknown magnitudes using Law of Sines (Parallelogram Law)."""
        unit_symbol, si_factor = _get_unit_info(unit)
        if not unit_symbol:
            unit_symbol = "N"

        vec1_name = vec1.name or "F_1"
        vec2_name = vec2.name or "F_2"

        M1_display = _to_display_value(abs(M1), si_factor)
        M2_display = _to_display_value(abs(M2), si_factor)
        FR_display = _to_display_value(_magnitude_and_angle_from_coords(resultant._coords)[0], si_factor)

        alpha_deg = math.degrees(alpha)
        beta_deg = math.degrees(beta)
        gamma_deg = math.degrees(gamma)

        vec1_latex = _latex_name(vec1_name)
        vec2_latex = _latex_name(vec2_name)
        resultant_latex = _latex_name(resultant_name)

        # Get original angle specs for display
        wrt1 = getattr(vec1, "_original_wrt", "+x")
        wrt2 = getattr(vec2, "_original_wrt", "+x")
        resultant_wrt = getattr(resultant, "_original_wrt", "+x")
        resultant_input_deg = getattr(resultant, "_original_angle", None)
        if resultant_input_deg is None:
            resultant_input_deg = math.degrees(resultant._angle.value) if resultant._angle and resultant._angle.value else 0

        # Get standard angles from +x
        # Use coordinate system axis angles for custom axes (u, v, etc.)
        coord_sys = getattr(self, "coordinate_system", None)
        axis_angles = {"+x": 0, "+y": 90, "-x": 180, "-y": 270, "x": 0, "y": 90}

        def get_axis_base_angle(wrt: str) -> float:
            """Get the base angle for a reference axis, using coordinate system if available."""
            wrt_lower = wrt.lower()
            # Check standard axes first
            if wrt_lower in axis_angles:
                return axis_angles[wrt_lower]
            # For custom axes, use coordinate system
            if coord_sys is not None:
                wrt_stripped = wrt_lower.lstrip("+-")
                is_negative = wrt_lower.startswith("-")
                if wrt_stripped == coord_sys.axis1_label.lower():
                    base = math.degrees(coord_sys.axis1_angle)
                    return (base + 180) % 360 if is_negative else base
                elif wrt_stripped == coord_sys.axis2_label.lower():
                    base = math.degrees(coord_sys.axis2_angle)
                    return (base + 180) % 360 if is_negative else base
            return 0  # Default fallback

        base1 = get_axis_base_angle(wrt1)
        base2 = get_axis_base_angle(wrt2)
        base_r = get_axis_base_angle(resultant_wrt)

        theta1_std_deg = (base1 + theta1_input_deg) % 360
        theta2_std_deg = (base2 + theta2_input_deg) % 360
        resultant_std_deg = (base_r + resultant_input_deg) % 360

        # Step 1: Calculate all triangle angles with proper geometric explanations
        # Generate display strings for each angle calculation
        vector_angle_configs = [
            (theta1_std_deg, theta1_input_deg, wrt1, vec1_latex, beta_deg),
            (theta2_std_deg, theta2_input_deg, wrt2, vec2_latex, alpha_deg),
        ]
        angle_displays = [
            compute_angle_between_display(
                first_vector_standard_angle_deg=std_deg,
                second_vector_standard_angle_deg=resultant_std_deg,
                first_vector_input_angle_deg=input_deg,
                second_vector_input_angle_deg=resultant_input_deg,
                first_vector_reference_axis=ref_axis,
                second_vector_reference_axis=resultant_wrt,
                first_vector_name=vec_name,
                second_vector_name=resultant_latex,
                interior_angle_result_deg=interior_deg,
                coordinate_system=coord_sys,
            )
            for std_deg, input_deg, ref_axis, vec_name, interior_deg in vector_angle_configs
        ]
        angle_vec1_FR_display, angle_vec2_FR_display = angle_displays

        # Build the consolidated Step 1 substitution
        step1_substitution = f"{angle_vec1_FR_display}\n{angle_vec2_FR_display}\n∠({vec1_latex},{vec2_latex}) = 180° - {beta_deg:.0f}° - {alpha_deg:.0f}°\n= {gamma_deg:.0f}°"

        self._add_solution_step(
            SolutionStep(
                target="triangle angles",
                method="Geometry",
                description="Calculate the interior angles of the force triangle",
                substitution=step1_substitution,
            )
        )

        # Step 2: Law of Sines for vec1
        self._add_solution_step(
            SolutionStep(
                target=f"|{vec1_latex}| using Eq 1",
                method="Law of Sines",
                description=f"Solve for |{vec1_name}| using Equation 1",
                equation_for_list=f"|{vec1_latex}|/sin(∠({vec2_latex},{resultant_latex})) = |{resultant_latex}|/sin(∠({vec1_latex},{vec2_latex}))",
                substitution=format_law_of_sines_substitution(vec1_latex, FR_display, alpha_deg, gamma_deg, M1_display, unit_symbol),
            )
        )

        # Step 3: Law of Sines for vec2
        self._add_solution_step(
            SolutionStep(
                target=f"|{vec2_latex}| using Eq 2",
                method="Law of Sines",
                description=f"Solve for |{vec2_name}| using Equation 2",
                equation_for_list=f"|{vec2_latex}|/sin(∠({vec1_latex},{resultant_latex})) = |{resultant_latex}|/sin(∠({vec1_latex},{vec2_latex}))",
                substitution=format_law_of_sines_substitution(vec2_latex, FR_display, beta_deg, gamma_deg, M2_display, unit_symbol),
            )
        )

    def _add_unknown_resultant_magnitude_steps(
        self,
        known_vec: _Vector,
        unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns,  # noqa: ARG002
        resultant_name: str,
        F_unknown_mag: float,
        theta: float,
        base_angle_rad: float,  # noqa: ARG002
        FR_mag: float,
        FR_angle: float,  # noqa: ARG002
        unit,
    ) -> None:
        """Add solution steps for unknown resultant magnitude problem.

        This problem type has:
        - One fully known vector (F_B)
        - One vector with known magnitude but unknown angle (F_A)
        - Resultant with known direction but unknown magnitude (F_R)

        Following textbook Problem 2-12 solution:
        1. Law of Sines to find θ: sin(90° - θ)/|F_B| = sin(50°)/|F_A|
        2. Calculate interior angle φ = 180° - (90° - θ) - 50°
        3. Law of Cosines for F_R: F_R = sqrt(F_A² + F_B² - 2·F_A·F_B·cos(φ))
        """
        unit_symbol, si_factor = _get_unit_info(unit)
        if not unit_symbol:
            unit_symbol = "N"

        # Get vector names
        known_name = known_vec.name or "F_B"
        unknown_name = unknown_vec.name or "F_A"
        unknown_wrt = getattr(unknown_vec, "_original_wrt", "+x")

        # Get angle info
        known_mag, _ = _magnitude_and_angle_from_coords(known_vec._coords)
        known_original_angle = getattr(known_vec, "_original_angle", 0)
        known_wrt = getattr(known_vec, "_original_wrt", "+x")

        # Convert values for display
        F_unknown_display = _to_display_value(F_unknown_mag, si_factor)
        FR_display = _to_display_value(FR_mag, si_factor)
        F_known_display = _to_display_value(known_mag, si_factor)

        # Compute the angles for the force triangle
        theta_deg = math.degrees(theta)  # Angle of F_A from its wrt reference
        base_angle_deg = math.degrees(base_angle_rad)

        # The angle at vertex opposite to F_R in the force triangle
        # For Problem 2-12: F_B is at 40° from -y, which means 50° from +x
        # F_A is at θ from +y (90° - θ from +x)
        # The angle between F_A direction and horizontal (+x) is (90° - θ)

        # Known vector angle from +x (standard angle)
        known_std_angle_deg = math.degrees(math.atan2(known_vec._coords[1], known_vec._coords[0]))
        if known_std_angle_deg < 0:
            known_std_angle_deg += 360

        # The interior angle at the vertex where F_A and F_B meet
        # This is the supplement of the angle between F_A and F_B directions
        # For F_R along +x, the angle from F_B to +x is (90° - known_original_angle) if known_wrt is -y
        if known_wrt == "-y":
            angle_FB_to_horizontal = 90 - known_original_angle  # 90° - 40° = 50° for Problem 2-12
        elif known_wrt == "+y":
            angle_FB_to_horizontal = 90 + known_original_angle
        elif known_wrt == "+x":
            angle_FB_to_horizontal = known_original_angle
        elif known_wrt == "-x":
            angle_FB_to_horizontal = 180 - known_original_angle
        else:
            angle_FB_to_horizontal = known_original_angle

        # The angle ∠(F_R, F_A) in the force triangle - this is (90° - θ) for Problem 2-12
        # because F_R is along +x and F_A is at angle θ from +y
        angle_FR_FA = 90 - abs(theta_deg)  # This is the angle at the F_R vertex of the triangle

        # The angle ∠(F_B, F_R) - angle from F_B to the horizontal (F_R direction)
        # For Problem 2-12: F_B is at 40° from -y, which means 50° from +x
        angle_FB_FR = angle_FB_to_horizontal

        # Step 1: Calculate ∠(F_B, F_R) - the angle between F_B and the resultant direction
        # For F_B at 40° from -y and F_R along +x:
        # ∠(-y, +x) = 90° in standard coordinates
        # ∠(F_B, F_R) = ∠(-y, +x) - ∠(-y, F_B) = 90° - 40° = 50°
        self._add_solution_step(
            SolutionStep(
                target=f"∠({known_name},{resultant_name})",
                method="Angle Calculation",
                description=f"Calculate the angle between {known_name} and {resultant_name}",
                substitution=(f"∠({known_name},{resultant_name}) = ∠({known_wrt},x) - ∠({known_wrt},{known_name})\n= 90° - {known_original_angle:.0f}°\n= {angle_FB_FR:.0f}°"),
            )
        )

        # Step 2: Law of Sines to find ∠(F_R, F_A) and thus θ
        # sin(∠(F_R,F_A))/|F_B| = sin(∠(F_B,F_R))/|F_A|
        self._add_solution_step(
            SolutionStep(
                target=f"∠({resultant_name},{unknown_name}) using Eq 1",
                method="Law of Sines",
                description=f"Use Law of Sines to find ∠({resultant_name},{unknown_name})",
                equation_for_list=f"sin(∠({resultant_name},{unknown_name}))/|{known_name}| = sin(∠({known_name},{resultant_name}))/|{unknown_name}|",
                substitution=(f"∠({resultant_name},{unknown_name}) = sin⁻¹({F_known_display:.0f} · sin({angle_FB_FR:.0f}°)/{F_unknown_display:.0f})\n= {angle_FR_FA:.1f}°"),
            )
        )

        # Step 3: Calculate θ (the angle of F_A from its reference axis)
        self._add_solution_step(
            SolutionStep(
                target=f"∠({unknown_wrt},{unknown_name})",
                method="Angle Calculation",
                description=f"Calculate θ from ∠({resultant_name},{unknown_name})",
                substitution=(f"θ = 90° - ∠({resultant_name},{unknown_name})\n= 90° - {angle_FR_FA:.1f}°\n= {abs(theta_deg):.1f}°"),
            )
        )

        # Step 4: Calculate interior angle ∠(F_A, F_B)
        # φ = 180° - ∠(F_R,F_A) - ∠(F_B,F_R)
        phi_deg = 180 - angle_FR_FA - angle_FB_FR
        self._add_solution_step(
            SolutionStep(
                target=f"∠({unknown_name},{known_name})",
                method="Triangle Geometry",
                description="Calculate the interior angle of the force triangle",
                substitution=(
                    f"∠({unknown_name},{known_name}) = 180° - ∠({resultant_name},{unknown_name}) - ∠({known_name},{resultant_name})\n= 180° - {angle_FR_FA:.1f}° - {angle_FB_FR:.0f}°\n= {phi_deg:.1f}°"
                ),
            )
        )

        # Step 5: Law of Cosines for F_R
        # F_R = sqrt(F_A² + F_B² - 2·F_A·F_B·cos(φ))
        self._add_solution_step(
            SolutionStep(
                target=f"|{resultant_name}| using Eq 2",
                method="Law of Cosines",
                description=f"Calculate |{resultant_name}| using Law of Cosines",
                equation_for_list=_format_law_of_cosines_equation(resultant_name, unknown_name, known_name),
                substitution=(
                    f"|{resultant_name}| = sqrt(({F_unknown_display:.0f})² + ({F_known_display:.0f})² - "
                    f"2({F_unknown_display:.0f})({F_known_display:.0f})cos({phi_deg:.1f}°))\n"
                    f"= {FR_display:.1f}\\ \\text{{{unit_symbol}}}"
                ),
            )
        )

    def _add_force_variables(self, name: str, magnitude: float, angle: float, dim, unit, is_known: bool, skip_angle: bool = False) -> None:
        """Add magnitude and angle variables for a force."""
        mag_var = Quantity(name=f"{name} Magnitude", dim=dim, value=magnitude, preferred=unit, _symbol=f"|{name}|")
        self.variables[f"{name}_mag"] = mag_var
        self._original_variable_states[f"{name}_mag"] = is_known

        if not skip_angle:
            angle_var = Quantity(name=f"{name} Angle", dim=_helper.dim.D, value=angle, preferred=_helper.degree_unit, _symbol=f"θ_{name}")
            self.variables[f"{name}_angle"] = angle_var
            self._original_variable_states[f"{name}_angle"] = is_known

    # =========================================================================
    # Solution step generation methods
    # =========================================================================

    def _add_solution_step(self, step: SolutionStep) -> None:
        """Add a solution step to the list."""
        self.solution_steps.append(step.to_dict())

    def _add_inverse_triangle_method_steps(
        self,
        known_vec: _Vector,
        unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns,
        resultant_name: str,
        F_unknown_mag: float,
        F_unknown_angle: float,
        F_known_angle: float,
        FR_angle: float,
        gamma: float,
        alpha: float,
    ) -> None:
        """Add solution steps for inverse parallelogram law problem."""
        unit_symbol, si_factor = _get_unit_info(resultant._unit)
        if not unit_symbol:
            unit_symbol = "N"

        known_name = known_vec.name or "F_known"
        unknown_name = unknown_vec.name or "F_unknown"

        F_known_mag, _ = _magnitude_and_angle_from_coords(known_vec._coords)
        FR_mag, _ = _magnitude_and_angle_from_coords(resultant._coords)

        F_known_display = _to_display_value(F_known_mag, si_factor)
        FR_display = _to_display_value(FR_mag, si_factor)
        F_unknown_display = _to_display_value(F_unknown_mag, si_factor)

        gamma_deg = math.degrees(gamma)
        alpha_deg = math.degrees(alpha)
        F_unknown_angle_deg = math.degrees(F_unknown_angle)
        # Note: triangle_angle = 180 - gamma_deg (unused, kept as comment for reference)

        # Build substitution for angle calculation
        known_original_angle = getattr(known_vec, "_original_angle", None)
        known_original_wrt = getattr(known_vec, "_original_wrt", "+x")
        resultant_original_angle = getattr(resultant, "_original_angle", None)
        resultant_original_wrt = getattr(resultant, "_original_wrt", "+x")

        known_axis = format_axis_ref(known_original_wrt)
        resultant_axis = format_axis_ref(resultant_original_wrt)

        substitution = self._build_angle_substitution(
            known_name, resultant_name, known_axis, resultant_axis, known_original_angle, resultant_original_angle, known_original_wrt, resultant_original_wrt, gamma_deg, F_known_angle, FR_angle
        )

        self._add_solution_step(
            SolutionStep(
                target=f"∠({known_name},{resultant_name})",
                method="Angle Calculation",
                description=f"Calculate the angle between {known_name} and {resultant_name}",
                substitution=substitution,
            )
        )

        self._add_solution_step(
            SolutionStep(
                target=f"|{unknown_name}| using Eq 1",
                method="Law of Cosines",
                description=f"Calculate {unknown_name} magnitude using Law of Cosines",
                equation_for_list=_format_law_of_cosines_equation(unknown_name, known_name, resultant_name),
                substitution=(
                    f"|{unknown_name}| = sqrt(({F_known_display:.0f})² + ({FR_display:.0f})² - "
                    f"2({F_known_display:.0f})({FR_display:.0f})cos({gamma_deg:.0f}°))\n"
                    f"= {F_unknown_display:.1f}\\ \\text{{{unit_symbol}}}"
                ),
            )
        )

        self._add_solution_step(
            SolutionStep(
                target=f"∠({resultant_name},{unknown_name}) using Eq 2",
                method="Law of Sines",
                description=f"Calculate angle from {resultant_name} to {unknown_name} using Law of Sines",
                equation_for_list=f"sin(∠({resultant_name},{unknown_name}))/|{known_name}| = sin(∠({known_name},{resultant_name}))/|{unknown_name}|",
                substitution=format_law_of_sines_angle_substitution(resultant_name, unknown_name, F_known_display, gamma_deg, F_unknown_display, alpha_deg),
            )
        )

        # Step 4: Final angle calculation - be smart about how we show this
        # Case 1: If resultant is along an axis (angle ≈ 0°), simplify the display
        # Case 2: Otherwise show the full calculation
        FR_angle_deg = math.degrees(FR_angle)

        # Determine the proper angle of resultant wrt its reference axis
        if resultant_original_wrt == "+x":
            FR_angle_from_ref = resultant_original_angle if resultant_original_angle is not None else FR_angle_deg
        elif resultant_original_wrt == "+y":
            FR_angle_from_ref = 90 + (resultant_original_angle if resultant_original_angle is not None else FR_angle_deg - 90)
        elif resultant_original_wrt == "-x":
            FR_angle_from_ref = 180 + (resultant_original_angle if resultant_original_angle is not None else FR_angle_deg - 180)
        elif resultant_original_wrt == "-y":
            FR_angle_from_ref = 270 + (resultant_original_angle if resultant_original_angle is not None else FR_angle_deg - 270)
        else:
            FR_angle_from_ref = FR_angle_deg

        # Check if resultant is along the +x axis (angle from +x ≈ 0°)
        # This is only true if:
        # 1. The reference is +x and the angle from +x is ≈ 0, OR
        # 2. The reference is -x and the angle from -x is ≈ 0 (i.e., along -x, but we focus on +x), OR
        # 3. The standard angle from +x is ≈ 0
        resultant_along_x_axis = (resultant_original_wrt == "+x" and abs(resultant_original_angle or 0) < 0.5) or abs(FR_angle_deg) < 0.5 or abs(FR_angle_deg - 360) < 0.5

        if resultant_along_x_axis:
            # Resultant is along the +x axis - simplify the display
            # ∠(x, F_A) = ∠(F_R, F_A) since F_R is along +x
            substitution = f"∠(x,{unknown_name}) = ∠({resultant_name},{unknown_name})  \\text{{(since }} {resultant_name} \\text{{ is along +x)}}\n= {alpha_deg:.1f}°"
        else:
            # General case: show the angle addition
            substitution = f"∠(x,{unknown_name}) = ∠(x,{resultant_name}) - ∠({resultant_name},{unknown_name})\n= {FR_angle_from_ref:.1f}° - {alpha_deg:.1f}°\n= {F_unknown_angle_deg:.1f}°"

        self._add_solution_step(
            SolutionStep(
                target=f"∠(x,{unknown_name}) with respect to +x",
                method="Angle Addition",
                description=f"Calculate {unknown_name} direction relative to +x axis",
                substitution=substitution,
            )
        )

    def _build_angle_substitution(
        self,
        known_name: str,
        resultant_name: str,
        known_axis: str,
        resultant_axis: str,
        known_original_angle: float | None,
        resultant_original_angle: float | None,
        known_wrt: str,
        resultant_wrt: str,
        gamma_deg: float,
        F_known_angle: float,
        FR_angle: float,
    ) -> str:
        """Build substitution string for angle calculation step."""
        if known_original_angle is not None and resultant_original_angle is not None:
            if known_wrt == "-x" and resultant_wrt == "+y":
                display_known = known_original_angle
                display_resultant = 90 + resultant_original_angle
                return _format_angle_difference_display(known_name, resultant_name, known_axis, "x", display_known, display_resultant, gamma_deg, operator="+", use_absolute=True)
            # Determine operator based on axis combination
            use_addition = (known_wrt == "-x" and resultant_wrt == "+x") or (known_wrt == "+x" and resultant_wrt == "-x")
            op = "+" if use_addition else "-"
            return _format_angle_difference_display(known_name, resultant_name, known_axis, resultant_axis, known_original_angle, resultant_original_angle, gamma_deg, operator=op, use_absolute=True)
        else:
            F_known_angle_deg = math.degrees(F_known_angle)
            FR_angle_deg = math.degrees(FR_angle)
            return _format_angle_difference_display(known_name, resultant_name, "x", "x", F_known_angle_deg, FR_angle_deg, gamma_deg, operator="-", use_absolute=True)

    def _add_triangle_method_steps(self, force1: _Vector, force2: _Vector, resultant: _Vector, resultant_name: str, mag_si: float, angle_rad: float, eq_num_offset: int = 0) -> None:
        """Add solution steps using the parallelogram law (Law of Cosines and Law of Sines).

        Args:
            eq_num_offset: Offset for equation numbers (e.g., 2 means use Eq 3 and Eq 4 instead of Eq 1 and Eq 2)
        """
        F1, theta1 = _magnitude_and_angle_from_coords(force1._coords)
        F2, theta2 = _magnitude_and_angle_from_coords(force2._coords)

        unit_symbol, si_factor = _get_unit_info(resultant._unit)
        if not unit_symbol:
            unit_symbol = "N"

        F1_display = _to_display_value(F1, si_factor)
        F2_display = _to_display_value(F2, si_factor)
        FR_display = _to_display_value(mag_si, si_factor)

        f1_name = getattr(force1, "name", "F_1")
        f2_name = getattr(force2, "name", "F_2")

        gamma = interior_angle(theta2, theta1)
        angle_in_triangle = math.pi - gamma
        angle_in_triangle_deg = np.degrees(angle_in_triangle)

        theta1_display = getattr(force1, "_original_angle", None) or np.degrees(theta1)
        theta2_display = getattr(force2, "_original_angle", None) or np.degrees(theta2)
        wrt1 = getattr(force1, "_original_wrt", "+x")
        wrt2 = getattr(force2, "_original_wrt", "+x")

        axis1 = format_axis_ref(wrt1)
        axis2 = format_axis_ref(wrt2)

        # Step 1: Angle between forces - use smart display generator
        substitution = self._compute_angle_display(
            force1,
            force2,
            angle_in_triangle_deg,
            vec1_std_override=theta1,
            vec2_std_override=theta2,
        )

        self._add_solution_step(
            SolutionStep(
                target=f"∠({f1_name},{f2_name})",
                method="Angle Difference",
                description=f"Calculate the angle between {f1_name} and {f2_name}",
                substitution=substitution,
            )
        )

        # Step 2: Law of Cosines for magnitude
        eq1_num = 1 + eq_num_offset
        self._add_solution_step(
            SolutionStep(
                target=f"|{resultant_name}| using Eq {eq1_num}",
                method="Law of Cosines",
                description="Calculate resultant magnitude using Law of Cosines",
                equation_for_list=f"|{resultant_name}|² = |{f1_name}|² + |{f2_name}|² + 2·|{f1_name}|·|{f2_name}|·cos(∠({f1_name},{f2_name}))",
                substitution=f"|{resultant_name}| = sqrt(({F1_display:.1f})² + ({F2_display:.1f})² + 2({F1_display:.1f})({F2_display:.1f})cos({angle_in_triangle_deg:.0f}°))\n= {FR_display:.1f}\\ \\text{{{unit_symbol}}}",
            )
        )

        # Step 3: Law of Sines for angle
        angle_deg = np.degrees(angle_rad)
        theta1_std = np.degrees(theta1)
        theta2_std = np.degrees(theta2)

        ref_label = "+x"
        if hasattr(resultant, "angle_reference") and resultant.angle_reference is not None:
            if hasattr(resultant.angle_reference, "axis_label"):
                ref_label = resultant.angle_reference.axis_label
        ref_axis = ref_label[1] if ref_label.startswith("+") else ref_label

        # Determine approach based on geometry
        if mag_si > 1e-10:
            sin_angle_A = F2 * np.sin(angle_in_triangle) / mag_si
            sin_angle_A = np.clip(sin_angle_A, -1.0, 1.0)
            interior_A = np.degrees(np.arcsin(sin_angle_A))

            sin_angle_B = F1 * np.sin(angle_in_triangle) / mag_si
            sin_angle_B = np.clip(sin_angle_B, -1.0, 1.0)
            interior_B = np.degrees(np.arcsin(sin_angle_B))

            angle_f1_to_fr = angle_deg - theta1_std
            while angle_f1_to_fr > 180:
                angle_f1_to_fr -= 360
            while angle_f1_to_fr < -180:
                angle_f1_to_fr += 360

            angle_f2_to_fr = angle_deg - theta2_std
            while angle_f2_to_fr > 180:
                angle_f2_to_fr -= 360
            while angle_f2_to_fr < -180:
                angle_f2_to_fr += 360

            use_f1_approach = angle_f2_to_fr >= 0

            if use_f1_approach:
                interior_angle_deg = interior_B
                law_of_sines_force = F1_display
                law_of_sines_name = f1_name
                phi_deg = interior_B if angle_f2_to_fr >= 0 else -interior_B
                theta_ref_deg = theta2_std
                theta_ref_display = theta2_display  # Use original angle for display
                axis_for_step4 = axis2
                force_for_step4 = f2_name
            else:
                interior_angle_deg = 180 - interior_A if abs(angle_f1_to_fr) > 90 else interior_A
                law_of_sines_force = F2_display
                law_of_sines_name = f2_name
                phi_deg = interior_angle_deg if angle_f1_to_fr >= 0 else -interior_angle_deg
                theta_ref_deg = theta1_std
                theta_ref_display = theta1_display  # Use original angle for display
                axis_for_step4 = axis1
                force_for_step4 = f1_name
        else:
            interior_angle_deg = 0.0
            phi_deg = 0.0
            law_of_sines_force = F2_display
            law_of_sines_name = f2_name
            theta_ref_deg = np.degrees(theta1)
            theta_ref_display = theta1_display  # Use original angle for display
            axis_for_step4 = axis1
            force_for_step4 = f1_name
            use_f1_approach = False

        eq2_num = 2 + eq_num_offset
        self._add_solution_step(
            SolutionStep(
                target=f"∠({force_for_step4},{resultant_name}) using Eq {eq2_num}",
                method="Law of Sines",
                description=f"Calculate angle from {force_for_step4} to {resultant_name} using Law of Sines",
                equation_for_list=f"sin(∠({force_for_step4},{resultant_name}))/|{law_of_sines_name}| = sin(∠({f1_name},{f2_name}))/|{resultant_name}|",
                substitution=format_law_of_sines_angle_substitution(force_for_step4, resultant_name, law_of_sines_force, angle_in_triangle_deg, FR_display, interior_angle_deg),
            )
        )

        # Step 4: Final angle calculation
        final_angle = angle_deg
        if final_angle < 0:
            final_angle += 360

        FR_x = mag_si * np.cos(angle_rad)
        FR_y = mag_si * np.sin(angle_rad)
        if FR_x >= 0 and FR_y >= 0:
            resultant_quadrant = 1
        elif FR_x < 0 and FR_y >= 0:
            resultant_quadrant = 2
        elif FR_x < 0 and FR_y < 0:
            resultant_quadrant = 3
        else:
            resultant_quadrant = 4

        original_angle = getattr(force2 if use_f1_approach else force1, "_original_angle", None)

        # Get angle_dir setting from resultant vector, then fall back to problem
        angle_dir = getattr(resultant, "angle_dir", None)
        if angle_dir is None:
            angle_dir = getattr(self, "angle_dir", None)
        display_angle = _convert_angle_for_display(final_angle, angle_dir)

        if resultant_quadrant == 4 and original_angle is not None and original_angle < 0:
            formula_ref_angle = original_angle
            # When angle_dir is "cw" or "signed", show math that naturally leads to negative result
            # Skip the 360° term since we want -30° + 28.8° = -1.2° (not 360° + -30° + 28.8° = 358.8°)
            if angle_dir in ("cw", "signed"):
                substitution = (
                    f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n"
                    f"= {formula_ref_angle:.1f}° + {interior_angle_deg:.1f}°\n"
                    f"= {display_angle:.1f}°"
                )
            else:
                intermediate_sum = 360 + formula_ref_angle + interior_angle_deg
                substitution = (
                    f"∠({ref_axis},{resultant_name}) = 360° + ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n"
                    f"= 360° + {formula_ref_angle:.1f}° + {interior_angle_deg:.1f}°\n"
                    f"= {display_angle:.1f}°"
                )
        else:
            # Calculate intermediate sum using standard angles for correctness check
            intermediate_sum = theta_ref_deg + phi_deg
            # But display using original problem-defined angle
            display_intermediate_sum = theta_ref_display + phi_deg

            # Check if the force's reference axis is different from the output reference axis
            # In that case, we need to include the angle from +x to the force's reference axis
            axis_for_step4_normalized = axis_for_step4.lower().replace(" ", "")
            needs_axis_offset = axis_for_step4_normalized not in ("x", "+x")

            if needs_axis_offset:
                # Calculate angle from +x to the force's reference axis
                axis_angles_from_x = {"+x": 0, "x": 0, "+y": 90, "y": 90, "-x": 180, "-y": -90}
                # Handle with or without + prefix
                axis_key = (
                    axis_for_step4_normalized
                    if axis_for_step4_normalized.startswith("-")
                    else f"+{axis_for_step4_normalized}"
                    if not axis_for_step4_normalized.startswith("+")
                    else axis_for_step4_normalized
                )
                axis_offset = axis_angles_from_x.get(axis_key, 0)

                # Show expanded formula: ∠(x, F_R) = ∠(x, -y) + ∠(-y, F_B) + ∠(F_B, F_R)
                substitution = (
                    f"∠({ref_axis},{resultant_name}) = ∠({ref_axis},{axis_for_step4}) + ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n"
                    f"= {axis_offset:.1f}° + {theta_ref_display:.1f}° + {phi_deg:.1f}°\n"
                    f"= {display_angle:.1f}°"
                )
            else:
                # Build base formula for angle addition
                arithmetic_sum = theta_ref_display + phi_deg
                # Show intermediate step if:
                # 1. The arithmetic sum differs from final angle (normalization happened), OR
                # 2. The display angle differs from the arithmetic sum (angle_dir conversion)
                needs_intermediate_for_normalization = abs(intermediate_sum - final_angle) > 0.1 and abs(intermediate_sum + 360 - final_angle) > 0.1 and abs(intermediate_sum - 360 - final_angle) > 0.1
                needs_intermediate_for_display = abs(arithmetic_sum - display_angle) > 0.5

                if needs_intermediate_for_display and arithmetic_sum > 180:
                    # When sum > 180° and we need a negative result, show the subtraction form
                    # θ_FR = ∠(x, F') + ∠(F', F_R) - 360° = 181.5° + 176.2° - 360° = -2.4°
                    base_formula = f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name}) - 360°\n= {theta_ref_display:.1f}° + {phi_deg:.1f}° - 360°"
                    substitution = f"{base_formula}\n= {display_angle:.1f}°"
                elif needs_intermediate_for_normalization:
                    base_formula = f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n= {theta_ref_display:.1f}° + {phi_deg:.1f}°"
                    substitution = f"{base_formula}\n= {display_intermediate_sum:.1f}°\n= {display_angle:.1f}°"
                else:
                    base_formula = f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n= {theta_ref_display:.1f}° + {phi_deg:.1f}°"
                    substitution = f"{base_formula}\n= {display_angle:.1f}°"

        self._add_solution_step(
            SolutionStep(
                target=f"∠({ref_axis},{resultant_name}) with respect to {ref_label}",
                method="Angle Addition",
                description=f"Calculate {resultant_name} direction relative to {ref_label} axis",
                substitution=substitution,
            )
        )

    def _add_iterative_parallelogram_steps(self, component_vectors: list[_Vector], resultant: _VectorWithUnknowns, resultant_name: str) -> None:
        """
        Add solution steps using iterative parallelogram law for 3+ forces.

        Following textbook approach: F' = F_1 + F_2, then F_R = F' + F_3, etc.
        Each step uses Law of Cosines and Law of Sines with proper solution steps.
        """
        if len(component_vectors) < 3:
            raise ValueError("Iterative parallelogram method requires at least 3 forces")

        unit_symbol, si_factor = _get_unit_info(resultant._unit)
        if not unit_symbol:
            unit_symbol = "N"

        # Start with first two forces
        force1 = component_vectors[0]
        force2 = component_vectors[1]

        # Compute intermediate resultant F' = F_1 + F_2
        intermediate_coords = force1._coords + force2._coords
        intermediate_mag = float(np.sqrt(np.sum(intermediate_coords**2)))
        intermediate_angle = float(np.arctan2(intermediate_coords[1], intermediate_coords[0]))
        if intermediate_angle < 0:
            intermediate_angle += 2 * np.pi

        # Create a temporary vector for the intermediate result (for step generation)
        intermediate = _Vector(
            name="F'",
            magnitude=intermediate_mag,
            angle=np.degrees(intermediate_angle),
            unit=resultant._unit,
            angle_unit="degree",
            is_known=True,
        )
        intermediate._coords = intermediate_coords
        intermediate._original_wrt = "+x"
        intermediate._original_angle = np.degrees(intermediate_angle)

        # Add triangle method steps for F' = F_1 + F_2 (uses Eq 1, Eq 2)
        self._add_triangle_method_steps(force1, force2, intermediate, "F'", intermediate_mag, intermediate_angle, eq_num_offset=0)

        # Chain additional forces: F'' = F' + F_3, F''' = F'' + F_4, etc.
        current_intermediate = intermediate
        remaining_forces = component_vectors[2:]

        for i, force in enumerate(remaining_forces):
            is_last_force = (i == len(remaining_forces) - 1)
            # Each iteration uses 2 more equations (offset increases by 2)
            eq_offset = (i + 1) * 2  # i=0 -> offset=2 (Eq 3, Eq 4), i=1 -> offset=4 (Eq 5, Eq 6), etc.

            # Compute the new intermediate (or final resultant)
            new_coords = current_intermediate._coords + force._coords
            new_mag = float(np.sqrt(np.sum(new_coords**2)))
            new_angle = float(np.arctan2(new_coords[1], new_coords[0]))
            if new_angle < 0:
                new_angle += 2 * np.pi

            if is_last_force:
                # Final step: F_R = F'' + F_n
                # Use the actual resultant name
                self._add_triangle_method_steps(current_intermediate, force, resultant, resultant_name, new_mag, new_angle, eq_num_offset=eq_offset)
            else:
                # Create next intermediate with proper prime notation
                prime_count = i + 2  # F'' for second intermediate, F''' for third, etc.
                prime_str = "'" * prime_count
                next_name = f"F{prime_str}"

                next_intermediate = _Vector(
                    name=next_name,
                    magnitude=new_mag,
                    angle=np.degrees(new_angle),
                    unit=resultant._unit,
                    angle_unit="degree",
                    is_known=True,
                )
                next_intermediate._coords = new_coords
                next_intermediate._original_wrt = "+x"
                next_intermediate._original_angle = np.degrees(new_angle)

                self._add_triangle_method_steps(current_intermediate, force, next_intermediate, next_name, new_mag, new_angle, eq_num_offset=eq_offset)
                current_intermediate = next_intermediate

    def _add_component_method_steps(self, component_vectors: list[_Vector], resultant: _VectorWithUnknowns, resultant_name: str, sum_coords: np.ndarray, mag_si: float, angle_rad: float) -> None:
        """Add solution steps using the component method (for 3+ forces). DEPRECATED - use iterative parallelogram."""
        unit_symbol, si_factor = _get_unit_info(resultant._unit)

        mag_display = _to_display_value(mag_si, si_factor)
        angle_deg = np.degrees(angle_rad)
        display_sum = sum_coords / si_factor if resultant._unit else sum_coords

        component_names = [getattr(v, "name", "Vector") for v in component_vectors]

        # Step 1: Resolve each force into components
        for vec in component_vectors:
            vec_name = getattr(vec, "name", "Vector")
            coords = vec._coords
            display_coords = coords / si_factor if resultant._unit else coords
            vec_mag, vec_angle = _magnitude_and_angle_from_coords(coords)
            if vec_angle < 0:
                vec_angle += 2 * np.pi
            vec_mag_display = _to_display_value(vec_mag, si_factor) if resultant._unit else vec_mag
            vec_angle_deg = np.degrees(vec_angle)

            self.solution_steps.append(_create_component_step(vec_name, "x", vec_mag_display, vec_angle_deg, display_coords[0], unit_symbol))
            self.solution_steps.append(_create_component_step(vec_name, "y", vec_mag_display, vec_angle_deg, display_coords[1], unit_symbol))

        # Steps 2-3: Sum components
        x_terms = " + ".join([f"({(v._coords[0] / si_factor):.3f})" for v in component_vectors])
        self.solution_steps.append(_create_sum_step(resultant_name, "x", component_names, x_terms, display_sum[0], unit_symbol))

        y_terms = " + ".join([f"({(v._coords[1] / si_factor):.3f})" for v in component_vectors])
        self.solution_steps.append(_create_sum_step(resultant_name, "y", component_names, y_terms, display_sum[1], unit_symbol))

        # Steps 4-5: Magnitude and angle
        self.solution_steps.append(
            {
                "target": f"|{resultant_name}|",
                "method": "pythagorean",
                "description": "Calculate resultant magnitude using Pythagorean theorem",
                "equation": f"|{resultant_name}| = √(({resultant_name}_x)² + ({resultant_name}_y)²)",
                "substitution": f"|{resultant_name}| = √(({display_sum[0]:.3f})² + ({display_sum[1]:.3f})²)",
                "result_value": f"{mag_display:.3f}",
                "result_unit": unit_symbol,
            }
        )

        self.solution_steps.append(
            {
                "target": f"θ_{resultant_name}",
                "method": "inverse_trig",
                "description": "Calculate resultant direction using inverse tangent",
                "equation": f"θ = tan⁻¹({resultant_name}_y / {resultant_name}_x)",
                "substitution": f"θ = tan⁻¹({display_sum[1]:.3f} / {display_sum[0]:.3f})",
                "result_value": f"{angle_deg:.3f}",
                "result_unit": "°",
            }
        )

    # =========================================================================
    # Force management
    # =========================================================================

    def add_force(self, force: _Vector, name: str | None = None) -> None:
        """Add a force to the problem."""
        force_name = name or force.name
        self.forces[force_name] = force
        setattr(self, force_name, force)

    def get_known_variables(self) -> dict[str, Quantity]:
        """Get known variables for report generation."""
        return {name: var for name, var in self.variables.items() if self._original_variable_states.get(name, False)}

    def get_unknown_variables(self) -> dict[str, Quantity]:
        """Get unknown variables for report generation."""
        return {name: var for name, var in self.variables.items() if not self._original_variable_states.get(name, False)}

    # =========================================================================
    # Main solve method with dispatch pattern
    # =========================================================================

    def _resolve_relative_angles(self) -> None:
        """Resolve any relative angle constraints before solving."""
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            unresolved = [f for f in self.forces.values() if f.has_relative_angle()]
            if not unresolved:
                return

            resolved_any = False
            for force in unresolved:
                try:
                    force.resolve_relative_angle(self.forces)
                    resolved_any = True
                    self.logger.info(f"Resolved relative angle for {force.name}")
                except ValueError as e:
                    self.logger.debug(f"Cannot resolve {force.name} yet: {e}")

            if not resolved_any:

                def _is_angle_unknown(force: _Vector) -> bool:
                    if force._relative_to_force not in self.forces:
                        return True
                    ref_force = self.forces[force._relative_to_force]
                    if ref_force.angle is None:
                        return True
                    return ref_force.angle.value is None

                all_refs_unknown = all(_is_angle_unknown(force) for force in unresolved if force._relative_to_force)
                if all_refs_unknown:
                    self.logger.info(f"Skipping resolution of {len(unresolved)} parametric angle constraints")
                    return

                unresolved_names = [f.name for f in unresolved]
                raise ValueError(f"Cannot resolve relative angle constraints for: {', '.join(unresolved_names)}")

            iteration += 1

        raise ValueError("Exceeded maximum iterations while resolving relative angle constraints")

    def _classify_forces(self) -> tuple[list[_Vector], list[_Vector], list[_Vector], int]:
        """Classify forces into known, unknown, and resultant categories."""
        known_forces = []
        unknown_forces = []
        resultant_forces = [f for f in self.forces.values() if f.is_resultant]
        total_unknowns = 0

        for force in self.forces.values():
            mag_unknown = force.magnitude.value is None
            angle_unknown = force.angle is None or force.angle.value is None or force.has_relative_angle()
            is_parametric = angle_unknown and force._relative_to_force is not None
            angle_unknown_for_count = angle_unknown and not is_parametric

            if mag_unknown and angle_unknown_for_count:
                unknown_forces.append(force)
                total_unknowns += 2
            elif mag_unknown or angle_unknown_for_count:
                unknown_forces.append(force)
                total_unknowns += 1
            elif is_parametric:
                unknown_forces.append(force)
            else:
                known_forces.append(force)

        return known_forces, unknown_forces, resultant_forces, total_unknowns

    def _select_solver(self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant_forces: list[_Vector], total_unknowns: int) -> tuple[str, Any]:
        """Select the appropriate solver method based on problem configuration."""
        # Check for angle-between problem
        all_mags_known = all(f.magnitude is not None and f.magnitude.value is not None for f in self.forces.values())
        all_angles_unknown = all(f.angle is None or f.angle.value is None for f in self.forces.values())

        if all_mags_known and all_angles_unknown and len(self.forces) <= 3:
            return "angle_between", (list(self.forces.values()), resultant_forces)

        if len(unknown_forces) == 0:
            return "resultant", (known_forces,)

        if len(unknown_forces) == 1 and len(known_forces) >= 1:
            return "single_unknown", (known_forces, unknown_forces[0], resultant_forces)

        if len(unknown_forces) == 2 and len(resultant_forces) == 1:
            has_parametric = any(f._relative_to_force is not None for f in unknown_forces)
            if has_parametric:
                return "parametric", (known_forces, unknown_forces, resultant_forces[0])

            partially_known = [f for f in unknown_forces if (f.magnitude is not None and f.magnitude.value is not None) != (f.angle is not None and f.angle.value is not None)]

            if total_unknowns == 2 and len(partially_known) == 2:
                has_known_mag = any(f.magnitude is not None and f.magnitude.value is not None for f in partially_known)
                has_known_angle = any(f.angle is not None and f.angle.value is not None for f in partially_known)

                if has_known_mag and has_known_angle:
                    return "two_partially_known", (known_forces, partially_known, resultant_forces[0])

                all_angles_known = _all_angles_known(partially_known)
                all_mags_known = _all_magnitudes_known(partially_known)

                if all_angles_known:
                    return "two_unknowns_resultant", (known_forces, unknown_forces, resultant_forces[0])
                if all_mags_known and resultant_forces[0].is_known:
                    return "two_angles_known_mags", (known_forces, partially_known, resultant_forces[0])

            if resultant_forces[0].is_known:
                return "two_unknowns_resultant", (known_forces, unknown_forces, resultant_forces[0])

        if len(unknown_forces) == 3 and len(resultant_forces) == 1:
            has_parametric = any(f._relative_to_force is not None for f in unknown_forces)
            if has_parametric and total_unknowns == 2:
                return "parametric", (known_forces, unknown_forces, resultant_forces[0])

        raise ValueError(f"Problem configuration not supported: {len(known_forces)} known, {len(unknown_forces)} unknown ({total_unknowns} total unknowns)")

    def solve(self, max_iterations: int = 100, tolerance: float = 1e-10) -> dict[str, _Vector]:  # type: ignore[override]
        """Solve the vector equilibrium problem algebraically."""
        self.solution_steps = []

        # Save original states
        if not self._original_force_states:
            capture_original_force_states(self.forces, self._original_force_states, self._original_variable_states)

        self._resolve_relative_angles()

        known_forces, unknown_forces, resultant_forces, total_unknowns = self._classify_forces()
        self.logger.info(f"Solving {self.name}: {len(known_forces)} known, {len(unknown_forces)} unknown ({total_unknowns} total unknowns)")

        # Dispatch to appropriate solver
        solver_name, args = self._select_solver(known_forces, unknown_forces, resultant_forces, total_unknowns)

        dispatch = {
            "angle_between": self._solve_angle_between_forces,
            "resultant": self._solve_resultant,
            "single_unknown": self._solve_single_unknown,
            "parametric": self._solve_with_parametric_angle_constraint,
            "two_partially_known": self._solve_two_partially_known_equilibrium,
            "two_unknowns_resultant": self._solve_two_unknowns_with_resultant,
            "two_angles_known_mags": self._solve_two_angles_with_known_magnitudes,
        }

        dispatch[solver_name](*args)

        self.is_solved = True
        self._populate_variables_from_forces()
        self._populate_solving_history()

        return self.forces

    # =========================================================================
    # Solver methods - delegating to TriangleSolver where possible
    # =========================================================================

    def _solve_resultant(self, known_forces: list[_Vector]) -> None:
        """Compute resultant of known forces."""
        # Find the resultant force in the problem
        resultant = None
        for force in self.forces.values():
            if force.is_resultant:
                resultant = force
                break

        # For 3+ forces, use iterative parallelogram law
        if len(known_forces) >= 3 and resultant is not None:
            self._solve_resultant_iterative_parallelogram(known_forces, resultant)
            return

        # For 2 forces, use the standard triangle solver
        self.solver.solve_resultant(known_forces, self.forces)
        self.solution_steps.extend(self.solver.solution_steps)
        self.solver.solution_steps = []

    def _solve_resultant_iterative_parallelogram(self, known_forces: list[_Vector], resultant: _Vector) -> None:
        """
        Solve for resultant of 3+ forces using iterative parallelogram law.

        This matches textbook approach: F' = F_1 + F_2, then F_R = F' + F_3, etc.
        Each step uses Law of Cosines and Law of Sines with proper solution steps.

        Args:
            known_forces: List of 3 or more known forces to sum
            resultant: The resultant force to solve for
        """
        if len(known_forces) < 3:
            raise ValueError("Iterative parallelogram law requires at least 3 forces")

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        # Get reference unit from first force
        ref_unit = known_forces[0].magnitude.preferred if known_forces[0].magnitude else None

        # Start with first two forces
        intermediate = _Vector(
            name="F'",
            magnitude=0.0,
            angle=0.0,
            unit=ref_unit,
            angle_unit="degree",
            is_known=False,
            is_resultant=True,
        )

        # Solve F' = F_1 + F_2
        self.solver.solve_resultant_from_two_forces(known_forces[0], known_forces[1], intermediate)
        self.solution_steps.extend(self.solver.solution_steps)
        self.solver.solution_steps = []

        # Store intermediate name for reporting
        intermediate._original_wrt = "+x"
        if intermediate._angle and intermediate._angle.value is not None:
            intermediate._original_angle = math.degrees(intermediate._angle.value)

        # Chain additional forces: F'' = F' + F_3, F''' = F'' + F_4, etc.
        # For 3 forces: F' = F_1 + F_2 (done above), then F_R = F' + F_3
        # For 4 forces: F' = F_1 + F_2, F'' = F' + F_3, then F_R = F'' + F_4
        current_intermediate = intermediate
        remaining_forces = known_forces[2:]

        for i, force in enumerate(remaining_forces):
            is_last_force = (i == len(remaining_forces) - 1)

            if is_last_force:
                # Final step: solve for actual resultant
                self.solver.solve_resultant_from_two_forces(current_intermediate, force, resultant)
                self.solution_steps.extend(self.solver.solution_steps)
                self.solver.solution_steps = []
            else:
                # Create next intermediate with proper prime notation
                prime_count = i + 2  # F'' for second intermediate, F''' for third, etc.
                prime_str = "'" * prime_count
                next_intermediate = _Vector(
                    name=f"F{prime_str}",
                    magnitude=0.0,
                    angle=0.0,
                    unit=ref_unit,
                    angle_unit="degree",
                    is_known=False,
                    is_resultant=True,
                )
                self.solver.solve_resultant_from_two_forces(current_intermediate, force, next_intermediate)
                self.solution_steps.extend(self.solver.solution_steps)
                self.solver.solution_steps = []

                next_intermediate._original_wrt = "+x"
                if next_intermediate._angle and next_intermediate._angle.value is not None:
                    next_intermediate._original_angle = math.degrees(next_intermediate._angle.value)

                current_intermediate = next_intermediate

    def _solve_single_unknown(self, known_forces: list[_Vector], unknown_force: _Vector, resultant_forces: list[_Vector]) -> None:
        """Solve for single unknown force."""
        # Handle special cases
        if len(resultant_forces) == 1 and len(known_forces) == 2:
            resultant = resultant_forces[0]
            if any(f is resultant for f in known_forces):
                other_known = [f for f in known_forces if f is not resultant][0]
                self.solver.solve_unknown_from_resultant_and_known(unknown_force, resultant, other_known)
                self.solution_steps.extend(self.solver.solution_steps)
                self.solver.solution_steps = []
                return

        if len(known_forces) == 2 and (len(resultant_forces) == 1 or unknown_force.is_resultant):
            self.solver.solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
            self.solution_steps.extend(self.solver.solution_steps)
            self.solver.solution_steps = []
            return

        if len(known_forces) >= 3 and unknown_force.is_resultant:
            # Use iterative parallelogram law: F' = F_1 + F_2, then F_R = F' + F_3, etc.
            self._solve_resultant_iterative_parallelogram(known_forces, unknown_force)
            return

        # Fallback to component method
        self.solver.solve_by_components(known_forces, unknown_force)
        self.solution_steps.extend(self.solver.solution_steps)
        self.solver.solution_steps = []

    def _solve_two_unknowns_with_resultant(self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector) -> None:
        """Solve for two unknowns given a resultant."""
        if resultant.is_known:
            self.solver.solve_two_unknowns_with_known_resultant(unknown_forces, resultant)
            self.solution_steps.extend(self.solver.solution_steps)
            self.solver.solution_steps = []
        else:
            all_angles_known = _all_angles_known(unknown_forces)
            if not all_angles_known or resultant.angle is None or resultant.angle.value is None:
                raise ValueError("Cannot solve: all angles must be known to solve for magnitudes")
            self._solve_two_magnitudes_with_known_angles(known_forces, unknown_forces, resultant)

    def _solve_two_partially_known_equilibrium(self, known_forces: list[_Vector], partially_known_forces: list[_Vector], resultant: _Vector) -> None:
        """Solve for two partially known forces using equilibrium equations."""
        self.solution_steps.append({"method": "Equilibrium with Partially Known Forces", "description": "Using ΣFx = 0 and ΣFy = 0 with partially known force properties"})

        force_with_known_mag = None
        force_with_known_angle = None

        for force in partially_known_forces:
            mag_known = force.magnitude is not None and force.magnitude.value is not None
            angle_known = force.angle is not None and force.angle.value is not None
            if mag_known and not angle_known:
                force_with_known_mag = force
            elif angle_known and not mag_known:
                force_with_known_angle = force

        if force_with_known_mag is None or force_with_known_angle is None:
            raise ValueError("Expected one force with known magnitude and one with known angle")

        # Sum known force components
        sum_x, sum_y, _, ref_unit = _sum_force_components(known_forces)

        M: float = _require_magnitude(force_with_known_mag, "Force with known magnitude")
        alpha_rad: float = _require_angle(force_with_known_angle, "Force with known angle")

        # Solve quadratic for R
        a, b = 1.0, -2.0 * (math.cos(alpha_rad) * sum_x + math.sin(alpha_rad) * sum_y)
        c = sum_x**2 + sum_y**2 - M**2
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            raise ValueError("No solution exists (discriminant < 0)")

        R1 = (-b + math.sqrt(discriminant)) / (2 * a)
        R2 = (-b - math.sqrt(discriminant)) / (2 * a)

        R = abs(R2) if abs(R2) > abs(R1) else abs(R1) if force_with_known_angle.is_resultant else (R1 if R1 > 0 else R2)

        cos_theta = (R * math.cos(alpha_rad) - sum_x) / M
        sin_theta = (R * math.sin(alpha_rad) - sum_y) / M
        theta_rad = math.atan2(sin_theta, cos_theta)

        # Update forces
        pref_unit = ref_unit or (force_with_known_mag.magnitude.preferred if force_with_known_mag.magnitude else None)
        _helper.set_force_angle(force_with_known_mag, theta_rad)
        _helper.update_force_from_polar(force_with_known_mag, M, theta_rad, pref_unit)

        _helper.set_force_magnitude(force_with_known_angle, R, pref_unit)
        _helper.update_force_from_polar(force_with_known_angle, R, alpha_rad, pref_unit)

    def _solve_two_magnitudes_with_known_angles(self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector) -> None:
        """Solve for two unknown magnitudes given known angles."""
        # Sum known forces
        sum_x, sum_y, _, ref_unit = _sum_force_components(known_forces)

        # Identify component and resultant
        component_force = None
        for f in unknown_forces:
            if f is not resultant:
                component_force = f
                break

        if component_force is None:
            raise ValueError("Cannot identify component force")

        theta_comp: float = _require_angle(component_force, "Component force")
        theta_res: float = _require_angle(resultant, "Resultant")

        # Solve linear system
        from ..utils.shared_utilities import solve_two_unknown_magnitudes

        M_comp, M_res = solve_two_unknown_magnitudes(theta_comp, theta_res, sum_x, sum_y, error_context="component equilibrium")

        # Update forces
        _helper.update_force_from_polar(component_force, M_comp, theta_comp, ref_unit)
        _helper.update_force_from_polar(resultant, M_res, theta_res, ref_unit)

        self.solution_steps.append(
            {
                "method": "Component Equilibrium (Linear System)",
                "description": f"Solving for {component_force.name} and {resultant.name} magnitudes",
            }
        )

    def _solve_two_angles_with_known_magnitudes(self, known_forces: list[_Vector], partially_known_forces: list[_Vector], resultant: _Vector) -> None:
        """Solve for two unknown angles given known magnitudes and known resultant."""
        if len(partially_known_forces) != 2:
            raise ValueError("Expected exactly 2 partially known forces")

        force1, force2 = partially_known_forces

        # Sum known forces (excluding resultant)
        sum_x, sum_y, _, ref_unit = _sum_force_components(known_forces, skip_resultants=True)

        if ref_unit is None:
            ref_unit = (resultant.magnitude.preferred if resultant.magnitude else None) or (force1.magnitude.preferred if force1.magnitude else None)

        # Validate required values
        M1: float = _require_magnitude(force1, "Force1")
        M2: float = _require_magnitude(force2, "Force2")
        M_R: float = _require_magnitude(resultant, "Resultant")
        theta_R: float = _require_angle(resultant, "Resultant")

        A = M_R * math.cos(theta_R) - sum_x
        B = M_R * math.sin(theta_R) - sum_y

        # Solve trigonometric system
        rhs = (A**2 + B**2 + M1**2 - M2**2) / (2 * M1)
        R = math.sqrt(A**2 + B**2)

        if abs(rhs) > R + 1e-9:
            raise ValueError("No solution exists")

        cos_value = max(-1.0, min(1.0, rhs / R))
        phi = math.atan2(B, A)
        alpha = math.acos(cos_value)

        theta1 = normalize_angle_positive(phi + alpha)
        theta2 = math.atan2((B - M1 * math.sin(theta1)) / M2, (A - M1 * math.cos(theta1)) / M2)
        theta2 = normalize_angle_positive(theta2)

        _helper.update_force_from_polar(force1, M1, theta1, ref_unit)
        _helper.update_force_from_polar(force2, M2, theta2, ref_unit)

        self.solution_steps.append(
            {
                "method": "Component Equilibrium (Nonlinear System)",
                "description": f"Solving for {force1.name} and {force2.name} angles",
            }
        )

    def _solve_with_parametric_angle_constraint(self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector) -> None:
        """Solve equilibrium when one force has a relative angle constraint."""
        parametric_force = None
        reference_force = None
        independent_force = None

        for force in unknown_forces:
            if force._relative_to_force is not None:
                parametric_force = force
                reference_force = next((f for f in unknown_forces if f.name == force._relative_to_force), None)
                break

        for force in unknown_forces:
            if force is not parametric_force and force is not reference_force and not force.is_resultant:
                independent_force = force
                break

        if independent_force is None:
            if resultant.magnitude is not None and resultant.magnitude.value is not None and resultant.angle is not None and resultant.angle.value is not None:
                independent_force = resultant

        if parametric_force is None or reference_force is None or independent_force is None:
            raise ValueError("Cannot identify forces for parametric constraint")

        angle_offset = parametric_force._relative_angle or 0.0

        ref_mag_known = reference_force.magnitude is not None and reference_force.magnitude.value is not None
        ref_angle_known = reference_force.angle is not None and reference_force.angle.value is not None
        indep_mag_known = independent_force.magnitude is not None and independent_force.magnitude.value is not None
        indep_angle_known = independent_force.angle is not None and independent_force.angle.value is not None

        if ref_mag_known and not ref_angle_known and indep_angle_known:
            self._solve_parametric_decomposition(reference_force, parametric_force, independent_force, angle_offset, resultant)
        elif not ref_mag_known and not ref_angle_known and indep_mag_known and indep_angle_known:
            self._solve_parametric_composition(reference_force, parametric_force, independent_force, angle_offset, resultant)
        else:
            raise ValueError("Unsupported parametric constraint configuration")

    def _solve_parametric_decomposition(self, reference_force: _Vector, parametric_force: _Vector, independent_force: _Vector, angle_offset: float, resultant: _Vector) -> None:
        """Solve Pattern A: F_ref = F_param + F_indep."""
        M_param_si: float = _require_magnitude(parametric_force, "Parametric force")
        theta_indep: float = _require_angle(independent_force, "Independent force")
        M_ref_si: float = _require_magnitude(reference_force, "Reference force")
        ref_unit = parametric_force.magnitude.preferred if parametric_force.magnitude else None

        angle_between = abs(angle_offset)
        M_indep_si = _law_of_cosines(M_ref_si, M_param_si, angle_between)

        sin_angle_at_indep = (M_param_si * math.sin(angle_between)) / M_indep_si
        angle_at_indep_interior = math.asin(sin_angle_at_indep)
        angle_at_param = math.pi - angle_between - angle_at_indep_interior
        phi = theta_indep - angle_offset - angle_at_param

        _helper.update_force_from_polar(reference_force, M_ref_si, phi, ref_unit)
        _helper.update_force_from_polar(parametric_force, M_param_si, phi + angle_offset, ref_unit)
        parametric_force._relative_to_force = None
        parametric_force._relative_angle = None
        _helper.update_force_from_polar(independent_force, M_indep_si, theta_indep, ref_unit)

        self.solution_steps.append(
            {
                "method": "Parametric Angle Constraint Solver",
                "description": f"Solved for {reference_force.name} angle with {parametric_force.name} at relative angle",
            }
        )

    def _solve_parametric_composition(self, reference_force: _Vector, parametric_force: _Vector, independent_force: _Vector, angle_offset: float, resultant: _Vector) -> None:
        """Solve Pattern B: F_indep = F_ref + F_param."""
        M_param_si: float = _require_magnitude(parametric_force, "Parametric force")
        R_si: float = _require_magnitude(independent_force, "Independent force")
        theta_R: float = _require_angle(independent_force, "Independent force")
        ref_unit = parametric_force.magnitude.preferred if parametric_force.magnitude else None

        R_x = -R_si * math.cos(theta_R)
        R_y = -R_si * math.sin(theta_R)

        cos_delta = math.cos(angle_offset)
        a, b, c = 1.0, 2.0 * M_param_si * cos_delta, M_param_si**2 - R_si**2
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            raise ValueError("No solution exists")

        M_ref_1 = (-b + math.sqrt(discriminant)) / (2 * a)
        M_ref_2 = (-b - math.sqrt(discriminant)) / (2 * a)
        M_ref_si = M_ref_1 if abs(M_ref_1) > abs(M_ref_2) else M_ref_2

        magnitude_is_negative = M_ref_si < 0
        A = M_ref_si + M_param_si * cos_delta
        B = M_param_si * math.sin(angle_offset)

        cos_theta_ref = (A * R_x + B * R_y) / (A**2 + B**2)
        sin_theta_ref = (A * R_y - B * R_x) / (A**2 + B**2)
        theta_ref = math.atan2(sin_theta_ref, cos_theta_ref)

        if magnitude_is_negative:
            theta_ref = theta_ref - math.pi

        _helper.update_force_from_polar(reference_force, M_ref_si, theta_ref, ref_unit)
        _helper.update_force_from_polar(parametric_force, M_param_si, theta_ref + angle_offset, ref_unit)
        parametric_force._relative_to_force = None
        parametric_force._relative_angle = None

        self.solution_steps.append(
            {
                "method": "Parametric Composition Solver",
                "description": f"Solved for {reference_force.name} magnitude and angle",
            }
        )

    def _solve_angle_between_forces(self, all_forces: list[_Vector], resultant_forces: list[_Vector]) -> None:
        """Solve for the angle between two forces given all three magnitudes."""
        self.solution_steps.append({"method": "Law of Cosines (Angle Between Forces)", "description": "Finding angle between forces given all magnitudes"})

        if len(resultant_forces) != 1:
            raise ValueError("Angle-between solver requires exactly one resultant")

        resultant = resultant_forces[0]
        component_forces = [f for f in all_forces if not f.is_resultant]

        if len(component_forces) != 2:
            raise ValueError("Angle-between solver requires exactly two component forces")

        F1, F2 = component_forces

        M1: float = _require_magnitude(F1, "F1")
        M2: float = _require_magnitude(F2, "F2")
        MR: float = _require_magnitude(resultant, "Resultant")

        cos_theta = (MR**2 - M1**2 - M2**2) / (2 * M1 * M2)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        theta_rad = math.acos(cos_theta)
        theta_deg = math.degrees(theta_rad)

        self.solution_steps.append(
            {
                "target": "θ (angle between forces)",
                "method": "Law of Cosines",
                "equation": f"{resultant.name}² = {F1.name}² + {F2.name}² - 2·{F1.name}·{F2.name}·cos(180° - θ)",
                "substitution": f"({MR:.0f})² = ({M1:.0f})² + ({M2:.0f})² - 2·({M1:.0f})·({M2:.0f})·cos(180° - θ)",
                "result_value": f"{theta_deg:.1f}",
                "result_unit": "°",
            }
        )

        # Assign directions
        sin_alpha = M2 * math.sin(theta_rad) / MR
        sin_alpha = np.clip(sin_alpha, -1.0, 1.0)
        alpha = math.asin(sin_alpha)
        beta = theta_rad - alpha

        theta_R = 0.0
        theta1 = alpha
        theta2 = -beta

        ref_unit = F1.magnitude.preferred if F1.magnitude else None

        _helper.update_force_from_polar(F1, M1, theta1, ref_unit)
        _helper.update_force_from_polar(F2, M2, theta2, ref_unit)

        FRx = M1 * math.cos(theta1) + M2 * math.cos(theta2)
        FRy = M1 * math.sin(theta1) + M2 * math.sin(theta2)
        _helper.update_force_coords(resultant, FRx, FRy, 0.0, ref_unit)
        _helper.set_force_angle(resultant, theta_R)
        resultant.is_known = True

    # =========================================================================
    # Post-processing methods
    # =========================================================================

    def _populate_variables_from_forces(self) -> None:
        """Convert ForceVector objects to Quantity variables for report generation."""
        for force_name, force in self.forces.items():
            was_originally_known = not force.is_resultant

            # Use existing helper method for magnitude and angle
            if force.magnitude is not None and force.magnitude.value is not None:
                magnitude = force.magnitude.value
                angle = force.angle.value if force.angle is not None else None
                unit = force.magnitude.preferred
                skip_angle = angle is None
                self._add_force_variables(force_name, magnitude, angle or 0.0, _helper.dim.force, unit, was_originally_known, skip_angle)

            # Add component variables (not covered by _add_force_variables)
            if force.x is not None and force.x.value is not None:
                x_var = Quantity(name=f"{force.name} X-Component", dim=_helper.dim.force, value=force.x.value, preferred=force.x.preferred, _symbol=f"{force_name}_x")
                self.variables[f"{force_name}_x"] = x_var

            if force.y is not None and force.y.value is not None:
                y_var = Quantity(name=f"{force.name} Y-Component", dim=_helper.dim.force, value=force.y.value, preferred=force.y.preferred, _symbol=f"{force_name}_y")
                self.variables[f"{force_name}_y"] = y_var

    def _populate_solving_history(self) -> None:
        """Convert solution_steps to solving_history format for report generation.

        Note: If solving_history already has entries (e.g., from direct appends during
        solving), they are preserved and new entries from solution_steps are appended.
        """
        # Initialize solving_history if it doesn't exist, but preserve existing entries
        if not hasattr(self, "solving_history"):
            self.solving_history = []

        for i, step in enumerate(self.solution_steps):
            equation_for_list = step.get("equation") or step.get("equation_for_list", "")
            equation_inline = step.get("equation", "")
            history_entry = {
                "step": i + 1,
                "target_variable": step.get("target", "Unknown"),
                "method": step.get("method", "algebraic"),
                "description": step.get("description", ""),
                "equation_str": equation_for_list,
                "equation_inline": equation_inline,
                "substituted_equation": step.get("substitution", ""),
                "result_value": step.get("result_value", ""),
                "result_unit": step.get("result_unit", ""),
                "details": step.get("description", ""),
            }
            self.solving_history.append(history_entry)

    def generate_report_content(self) -> dict[str, Any]:
        """Generate report content for vector equilibrium problem."""
        content: dict[str, Any] = {
            "title": self.name,
            "description": self.description,
            "problem_type": "Vector Equilibrium (Statics)",
            "given": [],
            "find": [],
            "solution_steps": self.solution_steps,
            "results": [],
        }

        for name, force in self.forces.items():
            if force.is_known and not force.is_resultant:
                force_str = _format_force_string(name, force)
                if force_str:
                    content["given"].append(force_str)

        for name, force in self.forces.items():
            if not force.is_known or (force.is_resultant and not self.is_solved):
                content["find"].append(f"{name}: {force.description or 'magnitude and direction'}")

        if self.is_solved:
            for name, force in self.forces.items():
                if force.is_resultant or not force.is_known:
                    force_str = _format_force_string(name, force)
                    if force_str:
                        content["results"].append(force_str)

        return content

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"VectorEquilibriumProblem('{self.name}', forces={len(self.forces)}, {status})"
