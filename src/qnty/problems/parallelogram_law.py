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
from ..utils.geometry import format_axis_ref, get_axis_info, interior_angle, normalize_angle_positive
from .problem import Problem

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
        original_name = getattr(vec, 'name', "")
        name = original_name if (original_name and original_name != "Vector") else default_name
        return vec.clone(name=name if name else None)

    def _clone_vector_with_unknowns(self, vec: _VectorWithUnknowns, vector_clones: dict[int, _Vector], default_name: str = "") -> _VectorWithUnknowns:
        """Create a copy of a _VectorWithUnknowns using the built-in clone method."""
        # Use the name from vec if meaningful, otherwise use default_name
        original_name = getattr(vec, 'name', "")
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
            if isinstance(attr, _VectorWithUnknowns) and not getattr(attr, 'is_resultant', False):
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
            if isinstance(attr, _VectorWithUnknowns) and getattr(attr, 'is_resultant', False):
                clone = self._clone_vector_with_unknowns(attr, vector_clones, default_name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
            elif isinstance(attr, _Vector):
                force_copy = self._clone_force_vector(attr)
                self.forces[attr_name] = force_copy
                setattr(self, attr_name, force_copy)

    def _clone_force_vector(self, force: _Vector) -> _Vector:
        """Create a copy of a ForceVector."""
        has_relative_angle = hasattr(force, '_relative_to_force') and force._relative_to_force is not None
        has_valid_vector = (force.is_known and
                           force.vector is not None and
                           force.magnitude is not None and force.magnitude.value is not None and
                           force.angle is not None and force.angle.value is not None and
                           not has_relative_angle)

        if has_valid_vector:
            cloned = _Vector(
                vector=force.vector,
                name=force.name,
                description=force.description,
                is_known=True,
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )
            # Handle negative magnitude
            if force.magnitude is not None and force.magnitude.value is not None and force.magnitude.value < 0:
                if cloned._magnitude is not None and cloned._magnitude.value is not None:
                    cloned._magnitude.value = -abs(cloned._magnitude.value)
                    if cloned._angle is not None and cloned._angle.value is not None:
                        cloned._angle.value = (cloned._angle.value + math.pi) % (2 * math.pi)
            return cloned
        else:
            angle_value = None
            angle_unit = None
            if force.angle is not None and force.angle.value is not None:
                angle_value = force.angle_reference.from_standard(force.angle.value, angle_unit="degree")
                angle_unit = "degree"

            cloned = _Vector(
                name=force.name,
                magnitude=force.magnitude,
                angle=angle_value if angle_value is not None else None,
                unit=force.magnitude.preferred if force.magnitude else None,
                angle_unit=angle_unit if angle_unit else "degree",
                description=force.description,
                is_known=force.is_known,
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )

            if hasattr(force, '_relative_to_force') and force._relative_to_force is not None:
                cloned._relative_to_force = force._relative_to_force
                cloned._relative_angle = force._relative_angle

            return cloned

    # =========================================================================
    # Vector resultant computation
    # =========================================================================

    def _compute_vector_resultants(self) -> None:
        """Compute resultant vectors from _VectorWithUnknowns placeholders."""
        has_vector_resultants = False

        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self, attr_name)
            if not isinstance(attr, _VectorWithUnknowns) or not attr.component_vectors:
                continue

            has_vector_resultants = True
            is_constraint = getattr(attr, '_is_constraint', False)

            if is_constraint:
                self._solve_inverse_resultant(attr, attr_name)
                continue

            # Forward problem: sum component vectors
            self._compute_forward_resultant(attr, attr_name)

        if has_vector_resultants:
            self.is_solved = True
            self._populate_solving_history()

    def _compute_forward_resultant(self, resultant: _VectorWithUnknowns, resultant_name: str) -> None:
        """Compute forward resultant by summing component vectors."""
        # Add known vectors as variables
        for vec in resultant.component_vectors:
            vec_name = getattr(vec, 'name', None)
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

                if hasattr(vec, '_angle') and vec._angle and vec._angle.value is not None:
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

        if hasattr(resultant, '_compute_magnitude_and_angle'):
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
        mag_var = Quantity(
            name=f"{resultant_name} Magnitude",
            dim=resultant._dim,
            value=mag_si,
            preferred=resultant._unit,
            _symbol=f"|{resultant_name}|",
        )
        self.variables[f"{resultant_name}_mag"] = mag_var
        self._original_variable_states[f"{resultant_name}_mag"] = False

        angle_var = Quantity(
            name=f"{resultant_name} Angle",
            dim=_helper.dim.D,
            value=angle_rad,
            preferred=_helper.degree_unit,
            _symbol=f"θ_{resultant_name}",
        )
        self.variables[f"{resultant_name}_angle"] = angle_var
        self._original_variable_states[f"{resultant_name}_angle"] = False

        # Add solution steps
        if len(resultant.component_vectors) == 2:
            self._add_triangle_method_steps(
                resultant.component_vectors[0],
                resultant.component_vectors[1],
                resultant,
                resultant_name,
                mag_si,
                angle_rad,
            )
        else:
            self._add_component_method_steps(
                resultant.component_vectors,
                resultant,
                resultant_name,
                sum_coords,
                mag_si,
                angle_rad,
            )

    def _solve_inverse_resultant(self, resultant: _VectorWithUnknowns, resultant_name: str) -> None:
        """Solve for unknown component vectors given a known resultant constraint."""
        component_vectors = resultant.component_vectors
        known_vectors: list[_Vector] = []
        unknown_vectors: list[_VectorWithUnknowns] = []

        for vec in component_vectors:
            if isinstance(vec, _VectorWithUnknowns) and vec.has_unknowns:
                unknown_vectors.append(vec)
            else:
                known_vectors.append(vec)

        FR_coords = resultant._coords
        FR_mag = float(np.sqrt(np.sum(FR_coords**2)))
        FR_angle = float(np.arctan2(FR_coords[1], FR_coords[0]))

        unit = resultant._unit

        if len(known_vectors) == 1 and len(unknown_vectors) == 1:
            self._solve_one_known_one_unknown_inverse(
                known_vectors[0], unknown_vectors[0], resultant, resultant_name,
                FR_coords, FR_mag, FR_angle, unit
            )
        else:
            raise NotImplementedError(
                f"Inverse resultant solve not implemented for {len(known_vectors)} known + "
                f"{len(unknown_vectors)} unknown vectors"
            )

    def _solve_one_known_one_unknown_inverse(
        self, known_vec: _Vector, unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns, resultant_name: str,
        FR_coords: np.ndarray, FR_mag: float, FR_angle: float, unit
    ) -> None:
        """Solve inverse problem with one known and one unknown vector."""
        F_known_coords = known_vec._coords
        F_known_mag = float(np.sqrt(np.sum(F_known_coords**2)))
        F_known_angle = float(np.arctan2(F_known_coords[1], F_known_coords[0]))

        # Vector subtraction: F_unknown = F_R - F_known
        F_unknown_coords = FR_coords - F_known_coords
        F_unknown_mag = float(np.sqrt(np.sum(F_unknown_coords**2)))
        F_unknown_angle = normalize_angle_positive(float(np.arctan2(F_unknown_coords[1], F_unknown_coords[0])))

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
        self._add_inverse_triangle_method_steps(
            known_vec, unknown_vec, resultant, resultant_name,
            F_unknown_mag, F_unknown_angle, F_known_angle, FR_angle, gamma, alpha
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
        self, known_vec: _Vector, unknown_vec: _VectorWithUnknowns,
        resultant: _VectorWithUnknowns, resultant_name: str,
        F_unknown_mag: float, F_unknown_angle: float,
        F_known_angle: float, FR_angle: float, gamma: float, alpha: float
    ) -> None:
        """Add solution steps for inverse parallelogram law problem."""
        unit = resultant._unit
        unit_symbol = unit.symbol if unit else "N"
        si_factor = unit.si_factor if unit else 1.0

        known_name = known_vec.name or "F_known"
        unknown_name = unknown_vec.name or "F_unknown"

        F_known_mag = float(np.sqrt(np.sum(known_vec._coords**2)))
        FR_mag = float(np.sqrt(np.sum(resultant._coords**2)))

        F_known_display = F_known_mag / si_factor
        FR_display = FR_mag / si_factor
        F_unknown_display = F_unknown_mag / si_factor

        gamma_deg = math.degrees(gamma)
        alpha_deg = math.degrees(alpha)
        F_unknown_angle_deg = math.degrees(F_unknown_angle)
        # Note: triangle_angle = 180 - gamma_deg (unused, kept as comment for reference)

        # Build substitution for angle calculation
        known_original_angle = getattr(known_vec, '_original_angle', None)
        known_original_wrt = getattr(known_vec, '_original_wrt', '+x')
        resultant_original_angle = getattr(resultant, '_original_angle', None)
        resultant_original_wrt = getattr(resultant, '_original_wrt', '+x')

        known_axis = format_axis_ref(known_original_wrt)
        resultant_axis = format_axis_ref(resultant_original_wrt)

        substitution = self._build_angle_substitution(
            known_name, resultant_name, known_axis, resultant_axis,
            known_original_angle, resultant_original_angle, known_original_wrt, resultant_original_wrt,
            gamma_deg, F_known_angle, FR_angle
        )

        self._add_solution_step(SolutionStep(
            target=f"∠({known_name},{resultant_name})",
            method="Angle Calculation",
            description=f"Calculate the angle between {known_name} and {resultant_name}",
            substitution=substitution,
        ))

        self._add_solution_step(SolutionStep(
            target=f"|{unknown_name}| using Eq 1",
            method="Law of Cosines",
            description=f"Calculate {unknown_name} magnitude using Law of Cosines",
            equation_for_list=f"|{unknown_name}|² = |{known_name}|² + |{resultant_name}|² - 2·|{known_name}|·|{resultant_name}|·cos(∠({known_name},{resultant_name}))",
            substitution=(
                f"|{unknown_name}| = sqrt(({F_known_display:.0f})² + ({FR_display:.0f})² - "
                f"2({F_known_display:.0f})({FR_display:.0f})cos({gamma_deg:.0f}°))\n"
                f"= {F_unknown_display:.1f} {unit_symbol}"
            ),
        ))

        self._add_solution_step(SolutionStep(
            target=f"∠({resultant_name},{unknown_name}) using Eq 2",
            method="Law of Sines",
            description=f"Calculate angle from {resultant_name} to {unknown_name} using Law of Sines",
            equation_for_list=f"sin(∠({resultant_name},{unknown_name}))/|{known_name}| = sin(∠({known_name},{resultant_name}))/|{unknown_name}|",
            substitution=(
                f"∠({resultant_name},{unknown_name}) = sin⁻¹({F_known_display:.1f}·sin({gamma_deg:.0f}°)/{F_unknown_display:.1f})\n"
                f"= {alpha_deg:.1f}°"
            ),
        ))

        FR_angle_for_display = 90 + resultant_original_angle if resultant_original_angle is not None else math.degrees(FR_angle)
        self._add_solution_step(SolutionStep(
            target=f"∠(x,{unknown_name}) with respect to +x",
            method="Angle Addition",
            description=f"Calculate {unknown_name} direction relative to +x axis",
            substitution=(
                f"∠(x,{unknown_name}) = ∠(x,{resultant_name}) - ∠({resultant_name},{unknown_name})\n"
                f"= {FR_angle_for_display:.1f}° - {alpha_deg:.1f}°\n"
                f"= {F_unknown_angle_deg:.1f}°"
            ),
        ))

    def _build_angle_substitution(
        self, known_name: str, resultant_name: str,
        known_axis: str, resultant_axis: str,
        known_original_angle: float | None, resultant_original_angle: float | None,
        known_wrt: str, resultant_wrt: str, gamma_deg: float,
        F_known_angle: float, FR_angle: float
    ) -> str:
        """Build substitution string for angle calculation step."""
        if known_original_angle is not None and resultant_original_angle is not None:
            if known_wrt == '-x' and resultant_wrt == '+y':
                display_known = known_original_angle
                display_resultant = 90 + resultant_original_angle
                return (
                    f"∠({known_name},{resultant_name}) = |∠({known_axis},{known_name}) + ∠(x,{resultant_name})|\n"
                    f"= |{display_known:.0f}° + {display_resultant:.0f}°|\n"
                    f"= {gamma_deg:.0f}°"
                )
            elif known_wrt == '-x' and resultant_wrt == '+x':
                return (
                    f"∠({known_name},{resultant_name}) = |∠({known_axis},{known_name}) + ∠({resultant_axis},{resultant_name})|\n"
                    f"= |{known_original_angle:.0f}° + {resultant_original_angle:.0f}°|\n"
                    f"= {gamma_deg:.0f}°"
                )
            elif known_wrt == '+x' and resultant_wrt == '-x':
                return (
                    f"∠({known_name},{resultant_name}) = |∠({known_axis},{known_name}) + ∠({resultant_axis},{resultant_name})|\n"
                    f"= |{known_original_angle:.0f}° + {resultant_original_angle:.0f}°|\n"
                    f"= {gamma_deg:.0f}°"
                )
            else:
                return (
                    f"∠({known_name},{resultant_name}) = |∠({known_axis},{known_name}) - ∠({resultant_axis},{resultant_name})|\n"
                    f"= |{known_original_angle:.0f}° - {resultant_original_angle:.0f}°|\n"
                    f"= {gamma_deg:.0f}°"
                )
        else:
            F_known_angle_deg = math.degrees(F_known_angle)
            FR_angle_deg = math.degrees(FR_angle)
            return (
                f"∠({known_name},{resultant_name}) = |∠(x,{known_name}) - ∠(x,{resultant_name})|\n"
                f"= |{F_known_angle_deg:.0f}° - {FR_angle_deg:.0f}°|\n"
                f"= {gamma_deg:.0f}°"
            )

    def _add_triangle_method_steps(
        self, force1: _Vector, force2: _Vector, resultant: _VectorWithUnknowns,
        resultant_name: str, mag_si: float, angle_rad: float
    ) -> None:
        """Add solution steps using the parallelogram law (Law of Cosines and Law of Sines)."""
        F1 = np.sqrt(np.sum(force1._coords**2))
        F2 = np.sqrt(np.sum(force2._coords**2))
        theta1 = np.arctan2(force1._coords[1], force1._coords[0])
        theta2 = np.arctan2(force2._coords[1], force2._coords[0])

        unit = resultant._unit
        unit_symbol = unit.symbol if unit else "N"
        si_factor = unit.si_factor if unit else 1.0

        F1_display = F1 / si_factor
        F2_display = F2 / si_factor
        FR_display = mag_si / si_factor

        f1_name = getattr(force1, 'name', 'F_1')
        f2_name = getattr(force2, 'name', 'F_2')

        gamma = interior_angle(theta2, theta1)
        angle_in_triangle = math.pi - gamma
        angle_in_triangle_deg = np.degrees(angle_in_triangle)

        theta1_display = getattr(force1, '_original_angle', None) or np.degrees(theta1)
        theta2_display = getattr(force2, '_original_angle', None) or np.degrees(theta2)
        wrt1 = getattr(force1, '_original_wrt', '+x')
        wrt2 = getattr(force2, '_original_wrt', '+x')

        axis1 = format_axis_ref(wrt1)
        axis2 = format_axis_ref(wrt2)

        # Step 1: Angle between forces
        substitution = self._build_force_angle_substitution(
            f1_name, f2_name, axis1, axis2, wrt1, wrt2,
            theta1_display, theta2_display, angle_in_triangle_deg
        )

        self._add_solution_step(SolutionStep(
            target=f"∠({f1_name},{f2_name})",
            method="Angle Difference",
            description=f"Calculate the angle between {f1_name} and {f2_name}",
            substitution=substitution,
        ))

        # Step 2: Law of Cosines for magnitude
        self._add_solution_step(SolutionStep(
            target=f"|{resultant_name}| using Eq 1",
            method="Law of Cosines",
            description="Calculate resultant magnitude using Law of Cosines",
            equation_for_list=f"|{resultant_name}|² = |{f1_name}|² + |{f2_name}|² + 2·|{f1_name}|·|{f2_name}|·cos(∠({f1_name},{f2_name}))",
            substitution=f"|{resultant_name}| = sqrt(({F1_display:.1f})² + ({F2_display:.1f})² + 2({F1_display:.1f})({F2_display:.1f})cos({angle_in_triangle_deg:.0f}°))\n= {FR_display:.1f} {unit_symbol}",
        ))

        # Step 3: Law of Sines for angle
        angle_deg = np.degrees(angle_rad)
        theta1_std = np.degrees(theta1)
        theta2_std = np.degrees(theta2)

        ref_label = "+x"
        if hasattr(resultant, 'angle_reference') and resultant.angle_reference is not None:
            if hasattr(resultant.angle_reference, 'axis_label'):
                ref_label = resultant.angle_reference.axis_label
        ref_axis = ref_label[1] if ref_label.startswith('+') else ref_label

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
                axis_for_step4 = axis2
                force_for_step4 = f2_name
            else:
                interior_angle_deg = 180 - interior_A if abs(angle_f1_to_fr) > 90 else interior_A
                law_of_sines_force = F2_display
                law_of_sines_name = f2_name
                phi_deg = interior_angle_deg if angle_f1_to_fr >= 0 else -interior_angle_deg
                theta_ref_deg = theta1_std
                axis_for_step4 = axis1
                force_for_step4 = f1_name
        else:
            interior_angle_deg = 0.0
            phi_deg = 0.0
            law_of_sines_force = F2_display
            law_of_sines_name = f2_name
            theta_ref_deg = np.degrees(theta1)
            axis_for_step4 = axis1
            force_for_step4 = f1_name
            use_f1_approach = False

        self._add_solution_step(SolutionStep(
            target=f"∠({force_for_step4},{resultant_name}) using Eq 2",
            method="Law of Sines",
            description=f"Calculate angle from {force_for_step4} to {resultant_name} using Law of Sines",
            equation_for_list=f"sin(∠({force_for_step4},{resultant_name}))/|{law_of_sines_name}| = sin(∠({f1_name},{f2_name}))/|{resultant_name}|",
            substitution=f"∠({force_for_step4},{resultant_name}) = sin⁻¹({law_of_sines_force:.1f}·sin({angle_in_triangle_deg:.0f}°)/{FR_display:.1f})\n= {interior_angle_deg:.1f}°",
        ))

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

        original_angle = getattr(force2 if use_f1_approach else force1, '_original_angle', None)

        if resultant_quadrant == 4 and original_angle is not None and original_angle < 0:
            formula_ref_angle = original_angle
            intermediate_sum = 360 + formula_ref_angle + interior_angle_deg
            substitution = (
                f"∠({ref_axis},{resultant_name}) = 360° + ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n"
                f"= 360° + {formula_ref_angle:.1f}° + {interior_angle_deg:.1f}°\n"
                f"= {final_angle:.1f}°"
            )
        else:
            intermediate_sum = theta_ref_deg + phi_deg
            if abs(intermediate_sum - final_angle) > 0.1 and abs(intermediate_sum + 360 - final_angle) > 0.1 and abs(intermediate_sum - 360 - final_angle) > 0.1:
                substitution = f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n= {theta_ref_deg:.1f}° + {phi_deg:.1f}°\n= {intermediate_sum:.1f}°\n= {final_angle:.1f}°"
            else:
                substitution = f"∠({ref_axis},{resultant_name}) = ∠({axis_for_step4},{force_for_step4}) + ∠({force_for_step4},{resultant_name})\n= {theta_ref_deg:.1f}° + {phi_deg:.1f}°\n= {final_angle:.1f}°"

        self._add_solution_step(SolutionStep(
            target=f"∠({ref_axis},{resultant_name}) with respect to {ref_label}",
            method="Angle Addition",
            description=f"Calculate {resultant_name} direction relative to {ref_label} axis",
            substitution=substitution,
        ))

    def _build_force_angle_substitution(
        self, f1_name: str, f2_name: str, axis1: str, axis2: str,
        wrt1: str, wrt2: str, theta1_display: float, theta2_display: float,
        angle_in_triangle_deg: float
    ) -> str:
        """Build substitution string for angle between forces."""
        axis1_type, _ = get_axis_info(wrt1)
        axis2_type, _ = get_axis_info(wrt2)

        if wrt1 == wrt2:
            return (
                f"∠({f1_name},{f2_name}) = |∠({axis1},{f1_name}) - ∠({axis1},{f2_name})|\n"
                f"= |{theta1_display:.0f}° - {theta2_display:.0f}°|\n"
                f"= {angle_in_triangle_deg:.0f}°"
            )
        elif axis1_type == axis2_type:
            return (
                f"∠({f1_name},{f2_name}) = |∠({axis1},{f1_name}) - ∠({axis2},{f2_name})|\n"
                f"= |{theta1_display:.0f}° - {theta2_display:.0f}°|\n"
                f"= {angle_in_triangle_deg:.0f}°"
            )
        else:
            abs_theta1 = abs(theta1_display)
            abs_theta2 = abs(theta2_display)
            return (
                f"∠({f1_name},{f2_name}) = |∠({axis1},{f1_name})| + |∠({axis2},{f2_name})|\n"
                f"= |{theta1_display:.0f}°| + |{theta2_display:.0f}°|\n"
                f"= {abs_theta1:.0f}° + {abs_theta2:.0f}°\n"
                f"= {angle_in_triangle_deg:.0f}°"
            )

    def _add_component_method_steps(
        self, component_vectors: list[_Vector], resultant: _VectorWithUnknowns,
        resultant_name: str, sum_coords: np.ndarray, mag_si: float, angle_rad: float
    ) -> None:
        """Add solution steps using the component method (for 3+ forces)."""
        unit = resultant._unit
        unit_symbol = unit.symbol if unit else ""
        si_factor = unit.si_factor if unit else 1.0

        mag_display = mag_si / si_factor
        angle_deg = np.degrees(angle_rad)
        display_sum = sum_coords / si_factor if unit else sum_coords

        component_names = [getattr(v, 'name', 'Vector') for v in component_vectors]

        # Step 1: Resolve each force into components
        for vec in component_vectors:
            vec_name = getattr(vec, 'name', 'Vector')
            coords = vec._coords
            display_coords = coords / si_factor if unit else coords
            vec_mag = np.sqrt(np.sum(coords**2))
            vec_angle = np.arctan2(coords[1], coords[0])
            if vec_angle < 0:
                vec_angle += 2 * np.pi
            vec_mag_display = vec_mag / si_factor if unit else vec_mag
            vec_angle_deg = np.degrees(vec_angle)

            self.solution_steps.append({
                "target": f"{vec_name}_x",
                "method": "component_resolution",
                "description": f"Resolve {vec_name} into x and y components",
                "equation": f"{vec_name}_x = |{vec_name}| cos(θ)",
                "substitution": f"{vec_name}_x = {vec_mag_display:.3f} cos({vec_angle_deg:.1f}°)",
                "result_value": f"{display_coords[0]:.3f}",
                "result_unit": unit_symbol,
            })
            self.solution_steps.append({
                "target": f"{vec_name}_y",
                "method": "component_resolution",
                "description": f"Resolve {vec_name} into x and y components",
                "equation": f"{vec_name}_y = |{vec_name}| sin(θ)",
                "substitution": f"{vec_name}_y = {vec_mag_display:.3f} sin({vec_angle_deg:.1f}°)",
                "result_value": f"{display_coords[1]:.3f}",
                "result_unit": unit_symbol,
            })

        # Steps 2-3: Sum components
        x_terms = " + ".join([f"({(v._coords[0]/si_factor):.3f})" for v in component_vectors])
        self.solution_steps.append({
            "target": f"{resultant_name}_x",
            "method": "component_sum",
            "description": "Sum x-components",
            "equation": f"Σ{resultant_name}_x = {' + '.join([f'{n}_x' for n in component_names])}",
            "substitution": f"Σ{resultant_name}_x = {x_terms}",
            "result_value": f"{display_sum[0]:.3f}",
            "result_unit": unit_symbol,
        })

        y_terms = " + ".join([f"({(v._coords[1]/si_factor):.3f})" for v in component_vectors])
        self.solution_steps.append({
            "target": f"{resultant_name}_y",
            "method": "component_sum",
            "description": "Sum y-components",
            "equation": f"Σ{resultant_name}_y = {' + '.join([f'{n}_y' for n in component_names])}",
            "substitution": f"Σ{resultant_name}_y = {y_terms}",
            "result_value": f"{display_sum[1]:.3f}",
            "result_unit": unit_symbol,
        })

        # Steps 4-5: Magnitude and angle
        self.solution_steps.append({
            "target": f"|{resultant_name}|",
            "method": "pythagorean",
            "description": "Calculate resultant magnitude using Pythagorean theorem",
            "equation": f"|{resultant_name}| = √(({resultant_name}_x)² + ({resultant_name}_y)²)",
            "substitution": f"|{resultant_name}| = √(({display_sum[0]:.3f})² + ({display_sum[1]:.3f})²)",
            "result_value": f"{mag_display:.3f}",
            "result_unit": unit_symbol,
        })

        self.solution_steps.append({
            "target": f"θ_{resultant_name}",
            "method": "inverse_trig",
            "description": "Calculate resultant direction using inverse tangent",
            "equation": f"θ = tan⁻¹({resultant_name}_y / {resultant_name}_x)",
            "substitution": f"θ = tan⁻¹({display_sum[1]:.3f} / {display_sum[0]:.3f})",
            "result_value": f"{angle_deg:.3f}",
            "result_unit": "°",
        })

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
        return {name: var for name, var in self.variables.items()
                if self._original_variable_states.get(name, False)}

    def get_unknown_variables(self) -> dict[str, Quantity]:
        """Get unknown variables for report generation."""
        return {name: var for name, var in self.variables.items()
                if not self._original_variable_states.get(name, False)}

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
                all_refs_unknown = all(
                    force._relative_to_force not in self.forces or
                    (self.forces[force._relative_to_force].angle is None or
                     self.forces[force._relative_to_force].angle.value is None)
                    for force in unresolved
                    if force._relative_to_force
                )
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
            mag_unknown = force.magnitude is None or force.magnitude.value is None
            angle_unknown = (force.angle is None or force.angle.value is None or force.has_relative_angle())
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

    def _select_solver(
        self, known_forces: list[_Vector], unknown_forces: list[_Vector],
        resultant_forces: list[_Vector], total_unknowns: int
    ) -> tuple[str, Any]:
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

            partially_known = [f for f in unknown_forces
                              if (f.magnitude is not None and f.magnitude.value is not None) !=
                                 (f.angle is not None and f.angle.value is not None)]

            if total_unknowns == 2 and len(partially_known) == 2:
                has_known_mag = any(f.magnitude is not None and f.magnitude.value is not None for f in partially_known)
                has_known_angle = any(f.angle is not None and f.angle.value is not None for f in partially_known)

                if has_known_mag and has_known_angle:
                    return "two_partially_known", (known_forces, partially_known, resultant_forces[0])

                all_angles_known = all(f.angle is not None and f.angle.value is not None for f in partially_known)
                all_mags_known = all(f.magnitude is not None and f.magnitude.value is not None for f in partially_known)

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
            for force_name, force in self.forces.items():
                self._original_force_states[force_name] = force.is_known
                mag_known = force.magnitude is not None and force.magnitude.value is not None
                angle_known = force.angle is not None and force.angle.value is not None
                self._original_variable_states[f"{force_name}_mag_known"] = mag_known
                self._original_variable_states[f"{force_name}_angle_known"] = angle_known

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
        self.solver.solve_resultant(known_forces, self.forces)
        self.solution_steps.extend(self.solver.solution_steps)
        self.solver.solution_steps = []

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
            # Sum all known forces for resultant
            sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
            ref_unit = None
            for force in known_forces:
                if force.x and force.x.value is not None:
                    sum_x += force.x.value
                if force.y and force.y.value is not None:
                    sum_y += force.y.value
                if force.z and force.z.value is not None:
                    sum_z += force.z.value
                if ref_unit is None and force.x and force.x.preferred:
                    ref_unit = force.x.preferred

            _helper.update_force_coords(unknown_force, sum_x, sum_y, sum_z, ref_unit)
            unknown_force._compute_magnitude_and_angle()
            unknown_force.is_known = True

            self.solution_steps.append({
                "method": "Vector Addition (Component Summation)",
                "description": f"Computing resultant {unknown_force.name} from {len(known_forces)} known forces"
            })
            return

        # Fallback to component method
        self.solver.solve_by_components(known_forces, unknown_force)
        self.solution_steps.extend(self.solver.solution_steps)
        self.solver.solution_steps = []

    def _solve_two_unknowns_with_resultant(
        self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector
    ) -> None:
        """Solve for two unknowns given a resultant."""
        if resultant.is_known:
            self.solver.solve_two_unknowns_with_known_resultant(unknown_forces, resultant)
            self.solution_steps.extend(self.solver.solution_steps)
            self.solver.solution_steps = []
        else:
            all_angles_known = all(f.angle is not None and f.angle.value is not None for f in unknown_forces)
            if not all_angles_known or resultant.angle is None or resultant.angle.value is None:
                raise ValueError("Cannot solve: all angles must be known to solve for magnitudes")
            self._solve_two_magnitudes_with_known_angles(known_forces, unknown_forces, resultant)

    def _solve_two_partially_known_equilibrium(
        self, known_forces: list[_Vector], partially_known_forces: list[_Vector], resultant: _Vector
    ) -> None:
        """Solve for two partially known forces using equilibrium equations."""
        self.solution_steps.append({
            "method": "Equilibrium with Partially Known Forces",
            "description": "Using ΣFx = 0 and ΣFy = 0 with partially known force properties"
        })

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
        sum_x, sum_y = 0.0, 0.0
        ref_unit = None
        for force in known_forces:
            if force.x and force.x.value is not None:
                sum_x += force.x.value
            if force.y and force.y.value is not None:
                sum_y += force.y.value
            if ref_unit is None and force.x and force.x.preferred:
                ref_unit = force.x.preferred

        M = force_with_known_mag.magnitude.value
        alpha_rad = force_with_known_angle.angle.value

        # Solve quadratic for R
        a, b = 1.0, -2.0 * (math.cos(alpha_rad) * sum_x + math.sin(alpha_rad) * sum_y)
        c = sum_x**2 + sum_y**2 - M**2
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            raise ValueError("No solution exists (discriminant < 0)")

        R1 = (-b + math.sqrt(discriminant)) / (2*a)
        R2 = (-b - math.sqrt(discriminant)) / (2*a)

        R = abs(R2) if abs(R2) > abs(R1) else abs(R1) if force_with_known_angle.is_resultant else (R1 if R1 > 0 else R2)

        cos_theta = (R * math.cos(alpha_rad) - sum_x) / M
        sin_theta = (R * math.sin(alpha_rad) - sum_y) / M
        theta_rad = math.atan2(sin_theta, cos_theta)

        # Update forces
        pref_unit = ref_unit or force_with_known_mag.magnitude.preferred
        _helper.set_force_angle(force_with_known_mag, theta_rad)
        _helper.update_force_from_polar(force_with_known_mag, M, theta_rad, pref_unit)

        _helper.set_force_magnitude(force_with_known_angle, R, pref_unit)
        _helper.update_force_from_polar(force_with_known_angle, R, alpha_rad, pref_unit)

    def _solve_two_magnitudes_with_known_angles(
        self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector
    ) -> None:
        """Solve for two unknown magnitudes given known angles."""
        # Sum known forces
        sum_x, sum_y = 0.0, 0.0
        ref_unit = None
        for force in known_forces:
            if force.vector and force.x and force.y:
                if force.x.value is not None:
                    sum_x += force.x.value
                if force.y.value is not None:
                    sum_y += force.y.value
                if ref_unit is None and force.x.preferred:
                    ref_unit = force.x.preferred

        # Identify component and resultant
        component_force = None
        for f in unknown_forces:
            if f is not resultant:
                component_force = f
                break

        if component_force is None:
            raise ValueError("Cannot identify component force")

        theta_comp = component_force.angle.value
        theta_res = resultant.angle.value

        # Solve linear system
        A = np.array([
            [math.cos(theta_comp), -math.cos(theta_res)],
            [math.sin(theta_comp), -math.sin(theta_res)]
        ])
        b = np.array([-sum_x, -sum_y])

        try:
            magnitudes = np.linalg.solve(A, b)
            M_comp, M_res = float(magnitudes[0]), float(magnitudes[1])
        except np.linalg.LinAlgError as err:
            raise ValueError("Cannot solve: system is singular") from err

        # Update forces
        _helper.update_force_from_polar(component_force, M_comp, theta_comp, ref_unit)
        _helper.update_force_from_polar(resultant, M_res, theta_res, ref_unit)

        self.solution_steps.append({
            "method": "Component Equilibrium (Linear System)",
            "description": f"Solving for {component_force.name} and {resultant.name} magnitudes",
        })

    def _solve_two_angles_with_known_magnitudes(
        self, known_forces: list[_Vector], partially_known_forces: list[_Vector], resultant: _Vector
    ) -> None:
        """Solve for two unknown angles given known magnitudes and known resultant."""
        if len(partially_known_forces) != 2:
            raise ValueError("Expected exactly 2 partially known forces")

        force1, force2 = partially_known_forces

        # Sum known forces (excluding resultant)
        sum_x, sum_y = 0.0, 0.0
        ref_unit = None
        for force in known_forces:
            if force.is_resultant:
                continue
            if force.vector and force.x and force.y:
                if force.x.value is not None:
                    sum_x += force.x.value
                if force.y.value is not None:
                    sum_y += force.y.value
                if ref_unit is None and force.x.preferred:
                    ref_unit = force.x.preferred

        if ref_unit is None:
            ref_unit = resultant.magnitude.preferred or force1.magnitude.preferred

        M1, M2 = force1.magnitude.value, force2.magnitude.value
        M_R, theta_R = resultant.magnitude.value, resultant.angle.value

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

        self.solution_steps.append({
            "method": "Component Equilibrium (Nonlinear System)",
            "description": f"Solving for {force1.name} and {force2.name} angles",
        })

    def _solve_with_parametric_angle_constraint(
        self, known_forces: list[_Vector], unknown_forces: list[_Vector], resultant: _Vector
    ) -> None:
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
            if resultant.magnitude is not None and resultant.magnitude.value is not None and \
               resultant.angle is not None and resultant.angle.value is not None:
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

    def _solve_parametric_decomposition(
        self, reference_force: _Vector, parametric_force: _Vector,
        independent_force: _Vector, angle_offset: float, resultant: _Vector
    ) -> None:
        """Solve Pattern A: F_ref = F_param + F_indep."""
        M_param_si = parametric_force.magnitude.value
        theta_indep = independent_force.angle.value
        M_ref_si = reference_force.magnitude.value
        ref_unit = parametric_force.magnitude.preferred

        angle_between = abs(angle_offset)
        M_indep_si = math.sqrt(M_ref_si**2 + M_param_si**2 - 2 * M_ref_si * M_param_si * math.cos(angle_between))

        sin_angle_at_indep = (M_param_si * math.sin(angle_between)) / M_indep_si
        angle_at_indep_interior = math.asin(sin_angle_at_indep)
        angle_at_param = math.pi - angle_between - angle_at_indep_interior
        phi = theta_indep - angle_offset - angle_at_param

        _helper.update_force_from_polar(reference_force, M_ref_si, phi, ref_unit)
        _helper.update_force_from_polar(parametric_force, M_param_si, phi + angle_offset, ref_unit)
        parametric_force._relative_to_force = None
        parametric_force._relative_angle = None
        _helper.update_force_from_polar(independent_force, M_indep_si, theta_indep, ref_unit)

        self.solution_steps.append({
            "method": "Parametric Angle Constraint Solver",
            "description": f"Solved for {reference_force.name} angle with {parametric_force.name} at relative angle",
        })

    def _solve_parametric_composition(
        self, reference_force: _Vector, parametric_force: _Vector,
        independent_force: _Vector, angle_offset: float, resultant: _Vector
    ) -> None:
        """Solve Pattern B: F_indep = F_ref + F_param."""
        M_param_si = parametric_force.magnitude.value
        R_si = independent_force.magnitude.value
        theta_R = independent_force.angle.value
        ref_unit = parametric_force.magnitude.preferred

        R_x = -R_si * math.cos(theta_R)
        R_y = -R_si * math.sin(theta_R)

        cos_delta = math.cos(angle_offset)
        a, b, c = 1.0, 2.0 * M_param_si * cos_delta, M_param_si**2 - R_si**2
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            raise ValueError("No solution exists")

        M_ref_1 = (-b + math.sqrt(discriminant)) / (2*a)
        M_ref_2 = (-b - math.sqrt(discriminant)) / (2*a)
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

        self.solution_steps.append({
            "method": "Parametric Composition Solver",
            "description": f"Solved for {reference_force.name} magnitude and angle",
        })

    def _solve_angle_between_forces(self, all_forces: list[_Vector], resultant_forces: list[_Vector]) -> None:
        """Solve for the angle between two forces given all three magnitudes."""
        self.solution_steps.append({
            "method": "Law of Cosines (Angle Between Forces)",
            "description": "Finding angle between forces given all magnitudes"
        })

        if len(resultant_forces) != 1:
            raise ValueError("Angle-between solver requires exactly one resultant")

        resultant = resultant_forces[0]
        component_forces = [f for f in all_forces if not f.is_resultant]

        if len(component_forces) != 2:
            raise ValueError("Angle-between solver requires exactly two component forces")

        F1, F2 = component_forces
        M1, M2 = F1.magnitude.value, F2.magnitude.value
        MR = resultant.magnitude.value

        cos_theta = (MR**2 - M1**2 - M2**2) / (2 * M1 * M2)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        theta_rad = math.acos(cos_theta)
        theta_deg = math.degrees(theta_rad)

        self.solution_steps.append({
            "target": "θ (angle between forces)",
            "method": "Law of Cosines",
            "equation": f"{resultant.name}² = {F1.name}² + {F2.name}² - 2·{F1.name}·{F2.name}·cos(180° - θ)",
            "substitution": f"({MR:.0f})² = ({M1:.0f})² + ({M2:.0f})² - 2·({M1:.0f})·({M2:.0f})·cos(180° - θ)",
            "result_value": f"{theta_deg:.1f}",
            "result_unit": "°",
        })

        # Assign directions
        sin_alpha = M2 * math.sin(theta_rad) / MR
        sin_alpha = np.clip(sin_alpha, -1.0, 1.0)
        alpha = math.asin(sin_alpha)
        beta = theta_rad - alpha

        theta_R = 0.0
        theta1 = alpha
        theta2 = -beta

        ref_unit = F1.magnitude.preferred

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
                self._add_force_variables(
                    force_name, magnitude, angle or 0.0, _helper.dim.force, unit, was_originally_known, skip_angle
                )

            # Add component variables (not covered by _add_force_variables)
            if force.x is not None and force.x.value is not None:
                x_var = Quantity(
                    name=f"{force.name} X-Component",
                    dim=_helper.dim.force,
                    value=force.x.value,
                    preferred=force.x.preferred,
                    _symbol=f"{force_name}_x"
                )
                self.variables[f"{force_name}_x"] = x_var

            if force.y is not None and force.y.value is not None:
                y_var = Quantity(
                    name=f"{force.name} Y-Component",
                    dim=_helper.dim.force,
                    value=force.y.value,
                    preferred=force.y.preferred,
                    _symbol=f"{force_name}_y"
                )
                self.variables[f"{force_name}_y"] = y_var

    def _populate_solving_history(self) -> None:
        """Convert solution_steps to solving_history format for report generation."""
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
        content = {
            "title": self.name,
            "description": self.description,
            "problem_type": "Vector Equilibrium (Statics)",
            "given": [],
            "find": [],
            "solution_steps": self.solution_steps,
            "results": []
        }

        for name, force in self.forces.items():
            if force.is_known and not force.is_resultant and force.magnitude and force.angle:
                if force.magnitude.value is not None and force.angle.value is not None:
                    mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                    ang_val = force.angle.value * 180 / math.pi
                    mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""
                    content["given"].append(f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°")

        for name, force in self.forces.items():
            if not force.is_known or (force.is_resultant and not self.is_solved):
                content["find"].append(f"{name}: {force.description or 'magnitude and direction'}")

        if self.is_solved:
            for name, force in self.forces.items():
                if force.is_resultant or not force.is_known:
                    if force.magnitude and force.angle and force.magnitude.value is not None and force.angle.value is not None:
                        mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                        ang_val = force.angle.value * 180 / math.pi
                        mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""
                        content["results"].append(f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°")

        return content

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"VectorEquilibriumProblem('{self.name}', forces={len(self.forces)}, {status})"
