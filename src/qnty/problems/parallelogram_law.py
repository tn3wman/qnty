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
from ..solving.component_solver import ComponentSolver
from ..solving.triangle_solver import TriangleSolver
from ..spatial import ForceVector
from ..spatial.vector import Vector, _Vector
from ..spatial.vectors import _VectorWithUnknowns
from .problem import Problem


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
        ...     F1 = ForceVector(magnitude=700, angle=60, unit="N")
        ...     F2 = ForceVector(magnitude=450, angle=105, unit="N")
        ...     FR = ForceVector.unknown("FR", is_resultant=True)
        ...
        >>> problem = CableProblem()
        >>> solution = problem.solve()

        >>> # Or programmatically
        >>> problem = VectorEquilibriumProblem("Cable Forces")
        >>> problem.add_force(ForceVector(magnitude=700, angle=60, unit="N", name="F1"))
        >>> problem.add_force(ForceVector(magnitude=450, angle=105, unit="N", name="F2"))
        >>> problem.add_force(ForceVector.unknown("FR", is_resultant=True))
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
        self.forces: dict[str, ForceVector] = {}
        self.solution_steps: list[dict[str, Any]] = []
        self._original_variable_states: dict[str, bool] = {}  # Track which variables were originally known
        self._original_force_states: dict[str, bool] = {}  # Track original is_known state of each force
        self.solver = TriangleSolver()  # Create triangle solver instance

        # Extract ForceVector class attributes
        self._extract_force_vectors()

        # Compute any vector resultants from _VectorWithUnknowns
        self._compute_vector_resultants()

    def _extract_force_vectors(self) -> None:
        """Extract ForceVector and _Vector objects defined at class level."""
        # First pass: clone all plain _Vectors so we have fresh copies
        vector_clones: dict[int, _Vector] = {}  # Map from id(original) to clone

        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.__class__, attr_name)
            # First pass: only handle plain _Vector from create_vector_polar (not ForceVector or _VectorWithUnknowns)
            # Check for exact type to avoid catching ForceVector subclass
            if type(attr).__name__ == "_Vector":
                # Clone plain _Vector, using attr_name as default name
                clone = self._clone_vector(attr, default_name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)

        # Second pass: handle _VectorWithUnknowns and ForceVectors not already cloned
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.__class__, attr_name)

            # Skip if already cloned in first pass
            if id(attr) in vector_clones:
                continue

            # Check _VectorWithUnknowns FIRST since it's also a ForceVector and _Vector
            if isinstance(attr, _VectorWithUnknowns):
                # Clone the _VectorWithUnknowns and update component_vectors to use cloned vectors
                clone = self._clone_vector_with_unknowns(attr, vector_clones)
                setattr(self, attr_name, clone)
            elif isinstance(attr, ForceVector):
                # Clone to avoid sharing between instances
                force_copy = self._clone_force_vector(attr)
                self.forces[attr_name] = force_copy
                setattr(self, attr_name, force_copy)

    def _clone_vector(self, vec: _Vector, default_name: str = "") -> _Vector:
        """Create a copy of a _Vector."""
        clone = object.__new__(_Vector)
        clone._coords = vec._coords.copy()
        clone._dim = vec._dim
        clone._unit = vec._unit
        # Use original name if it exists and is meaningful, otherwise use default_name
        original_name = getattr(vec, 'name', "")
        # Replace generic names like "Vector" or empty with the attribute name
        clone.name = original_name if (original_name and original_name != "Vector") else default_name
        clone._description = getattr(vec, '_description', "")
        clone.is_known = getattr(vec, 'is_known', True)
        clone.is_resultant = getattr(vec, 'is_resultant', False)
        clone.coordinate_system = getattr(vec, 'coordinate_system', None)
        clone.angle_reference = getattr(vec, 'angle_reference', None)

        # Copy magnitude and angle if present
        if hasattr(vec, '_magnitude'):
            clone._magnitude = vec._magnitude
        if hasattr(vec, '_angle'):
            clone._angle = vec._angle

        # Copy original angle and wrt for reporting
        if hasattr(vec, '_original_angle'):
            clone._original_angle = vec._original_angle
        if hasattr(vec, '_original_wrt'):
            clone._original_wrt = vec._original_wrt

        return clone

    def _clone_vector_with_unknowns(self, vec: _VectorWithUnknowns, vector_clones: dict[int, _Vector]) -> _VectorWithUnknowns:
        """Create a copy of a _VectorWithUnknowns with updated component_vectors."""
        clone = object.__new__(_VectorWithUnknowns)
        clone._coords = vec._coords.copy()
        clone._dim = vec._dim
        clone._unit = vec._unit
        clone.name = getattr(vec, 'name', "")
        clone._description = getattr(vec, '_description', "")
        clone.is_known = getattr(vec, 'is_known', False)
        clone.is_resultant = getattr(vec, 'is_resultant', True)
        clone.coordinate_system = getattr(vec, 'coordinate_system', None)
        clone.angle_reference = getattr(vec, 'angle_reference', None)
        clone._unknowns = vec._unknowns.copy() if hasattr(vec, '_unknowns') else {}

        # Update component_vectors to use cloned vectors
        if hasattr(vec, '_component_vectors') and vec._component_vectors:
            clone._component_vectors = [
                vector_clones.get(id(cv), cv) for cv in vec._component_vectors
            ]
        else:
            clone._component_vectors = []

        # Copy other attributes
        if hasattr(vec, '_direction_unit_vector'):
            clone._direction_unit_vector = vec._direction_unit_vector
        if hasattr(vec, '_is_constraint'):
            clone._is_constraint = vec._is_constraint
        if hasattr(vec, '_magnitude'):
            clone._magnitude = vec._magnitude
        if hasattr(vec, '_angle'):
            clone._angle = vec._angle

        return clone

    def _compute_vector_resultants(self) -> None:
        """Compute resultant vectors from _VectorWithUnknowns placeholders."""
        from ..core.dimension_catalog import dim

        has_vector_resultants = False

        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self, attr_name)

            # Check if it's a _VectorWithUnknowns with component vectors
            if isinstance(attr, _VectorWithUnknowns) and attr.component_vectors:
                has_vector_resultants = True

                # First, add known vectors as variables
                for vec in attr.component_vectors:
                    vec_name = getattr(vec, 'name', None)
                    if vec_name and vec._unit:
                        # Add magnitude
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

                        # Add angle if present
                        if hasattr(vec, '_angle') and vec._angle and vec._angle.value is not None:
                            angle_var = Quantity(
                                name=f"{vec_name} Angle",
                                dim=dim.D,
                                value=vec._angle.value,
                                preferred=vec._angle.preferred,
                                _symbol=f"θ_{vec_name}",
                            )
                            self.variables[f"{vec_name}_angle"] = angle_var
                            self._original_variable_states[f"{vec_name}_angle"] = True

                # Forward problem: sum component vectors to get resultant
                sum_coords = np.array([0.0, 0.0, 0.0], dtype=float)

                for vec in attr.component_vectors:
                    sum_coords += vec._coords

                # Update the resultant vector coordinates
                attr._coords = sum_coords
                attr._unknowns = {}  # Clear unknowns
                attr.is_known = True

                # Recompute magnitude and angle
                if hasattr(attr, '_compute_magnitude_and_angle'):
                    attr._compute_magnitude_and_angle()

                # Compute magnitude and angle for reporting
                mag_si = float(np.sqrt(np.sum(sum_coords**2)))
                angle_rad = float(np.arctan2(sum_coords[1], sum_coords[0]))
                if angle_rad < 0:
                    angle_rad += 2 * np.pi

                # Store as _magnitude and _angle for consistency
                from ..core.unit import ureg
                degree_unit = ureg.resolve("degree", dim=dim.D)

                attr._magnitude = Quantity(
                    name=f"{attr_name}_magnitude",
                    dim=attr._dim,
                    value=mag_si,
                    preferred=attr._unit,
                )
                attr._angle = Quantity(
                    name=f"{attr_name}_angle",
                    dim=dim.D,
                    value=angle_rad,
                    preferred=degree_unit,
                )

                # Add resultant as unknown variable (solved)
                mag_var = Quantity(
                    name=f"{attr_name} Magnitude",
                    dim=attr._dim,
                    value=mag_si,
                    preferred=attr._unit,
                    _symbol=f"|{attr_name}|",
                )
                self.variables[f"{attr_name}_mag"] = mag_var
                self._original_variable_states[f"{attr_name}_mag"] = False  # Was unknown

                angle_var = Quantity(
                    name=f"{attr_name} Angle",
                    dim=dim.D,
                    value=angle_rad,
                    preferred=degree_unit,
                    _symbol=f"θ_{attr_name}",
                )
                self.variables[f"{attr_name}_angle"] = angle_var
                self._original_variable_states[f"{attr_name}_angle"] = False  # Was unknown

                # Add solution steps in format expected by _populate_solving_history
                component_names = [getattr(v, 'name', 'Vector') for v in attr.component_vectors]
                unit_symbol = attr._unit.symbol if attr._unit else ""
                mag_display = mag_si / attr._unit.si_factor if attr._unit else mag_si
                angle_deg = np.degrees(angle_rad)

                if attr._unit:
                    display_sum = sum_coords / attr._unit.si_factor
                else:
                    display_sum = sum_coords

                # Step 1: Resolve each force into components
                for vec in attr.component_vectors:
                    vec_name = getattr(vec, 'name', 'Vector')
                    coords = vec._coords
                    if attr._unit:
                        display_coords = coords / attr._unit.si_factor
                    else:
                        display_coords = coords

                    # Get magnitude and angle for this vector
                    vec_mag = np.sqrt(np.sum(coords**2))
                    vec_angle = np.arctan2(coords[1], coords[0])
                    if vec_angle < 0:
                        vec_angle += 2 * np.pi
                    vec_mag_display = vec_mag / attr._unit.si_factor if attr._unit else vec_mag
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

                # Step 2: Sum x-components
                x_terms = " + ".join([f"({(v._coords[0]/attr._unit.si_factor if attr._unit else v._coords[0]):.3f})" for v in attr.component_vectors])
                self.solution_steps.append({
                    "target": f"{attr_name}_x",
                    "method": "component_sum",
                    "description": "Sum x-components",
                    "equation": f"Σ{attr_name}_x = {' + '.join([f'{n}_x' for n in component_names])}",
                    "substitution": f"Σ{attr_name}_x = {x_terms}",
                    "result_value": f"{display_sum[0]:.3f}",
                    "result_unit": unit_symbol,
                })

                # Step 3: Sum y-components
                y_terms = " + ".join([f"({(v._coords[1]/attr._unit.si_factor if attr._unit else v._coords[1]):.3f})" for v in attr.component_vectors])
                self.solution_steps.append({
                    "target": f"{attr_name}_y",
                    "method": "component_sum",
                    "description": "Sum y-components",
                    "equation": f"Σ{attr_name}_y = {' + '.join([f'{n}_y' for n in component_names])}",
                    "substitution": f"Σ{attr_name}_y = {y_terms}",
                    "result_value": f"{display_sum[1]:.3f}",
                    "result_unit": unit_symbol,
                })

                # Step 4: Calculate magnitude
                self.solution_steps.append({
                    "target": f"|{attr_name}|",
                    "method": "pythagorean",
                    "description": "Calculate resultant magnitude using Pythagorean theorem",
                    "equation": f"|{attr_name}| = √(({attr_name}_x)² + ({attr_name}_y)²)",
                    "substitution": f"|{attr_name}| = √(({display_sum[0]:.3f})² + ({display_sum[1]:.3f})²)",
                    "result_value": f"{mag_display:.3f}",
                    "result_unit": unit_symbol,
                })

                # Step 5: Calculate angle
                self.solution_steps.append({
                    "target": f"θ_{attr_name}",
                    "method": "inverse_trig",
                    "description": "Calculate resultant direction using inverse tangent",
                    "equation": f"θ = tan⁻¹({attr_name}_y / {attr_name}_x)",
                    "substitution": f"θ = tan⁻¹({display_sum[1]:.3f} / {display_sum[0]:.3f})",
                    "result_value": f"{angle_deg:.3f}",
                    "result_unit": "°",
                })

        # Mark as solved if we computed any resultants
        if has_vector_resultants:
            self.is_solved = True
            self._populate_solving_history()

    def _clone_force_vector(self, force: ForceVector) -> ForceVector:
        """Create a copy of a ForceVector."""
        # Check if force has unresolved relative angle
        has_relative_angle = hasattr(force, '_relative_to_force') and force._relative_to_force is not None

        # A force is fully computable only if it has both magnitude and angle with known values
        # Otherwise the vector coords might be placeholder zeros from _init_magnitude_only
        has_valid_vector = (force.is_known and
                           force.vector is not None and
                           force.magnitude is not None and force.magnitude.value is not None and
                           force.angle is not None and force.angle.value is not None and
                           not has_relative_angle)

        if has_valid_vector:
            # Known force with computed vector - copy with same values
            cloned = ForceVector(
                vector=force.vector,
                name=force.name,
                description=force.description,
                is_known=True,
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )
            # If original had negative magnitude, restore it after cloning
            # (_compute_magnitude_and_angle converts to positive via sqrt)
            if force.magnitude is not None and force.magnitude.value is not None and force.magnitude.value < 0:
                if cloned._magnitude is not None and cloned._magnitude.value is not None:
                    # The cloned magnitude is now in SI units (from vector computation)
                    # Flip the sign to preserve the negative
                    cloned._magnitude.value = -abs(cloned._magnitude.value)
                    # Also flip the angle by 180° since negative magnitude means opposite direction
                    if cloned._angle is not None and cloned._angle.value is not None:
                        import math
                        cloned._angle.value = (cloned._angle.value + math.pi) % (2 * math.pi)
            return cloned
        else:
            # Unknown force - may have known angle or known magnitude
            angle_value = None
            angle_unit = None
            if force.angle is not None and force.angle.value is not None:
                # Angle is stored internally as standard (CCW from +x)
                # Convert back to the angle_reference system for cloning
                angle_value = force.angle_reference.from_standard(force.angle.value, angle_unit="degree")
                angle_unit = "degree"

            # Create cloned force with Quantity objects to avoid double conversion
            # Use the main constructor which accepts Quantity objects
            cloned = ForceVector(
                name=force.name,
                magnitude=force.magnitude,  # Pass Quantity object directly
                angle=angle_value if angle_value is not None else None,  # This is a float in degrees
                unit=force.magnitude.preferred if force.magnitude else None,
                angle_unit=angle_unit if angle_unit else "degree",
                description=force.description,
                is_known=force.is_known,  # Preserve original is_known state
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )

            # Preserve relative angle constraint if present
            if hasattr(force, '_relative_to_force') and force._relative_to_force is not None:
                cloned._relative_to_force = force._relative_to_force
                cloned._relative_angle = force._relative_angle

            return cloned

    def add_force(self, force: ForceVector, name: str | None = None) -> None:
        """
        Add a force to the problem.

        Args:
            force: ForceVector to add
            name: Optional name (uses force.name if not provided)
        """
        force_name = name or force.name
        self.forces[force_name] = force
        setattr(self, force_name, force)

    def get_known_variables(self) -> dict[str, Quantity]:
        """
        Get known variables for report generation.

        Returns:
            Dictionary of variable names to Quantity objects that were originally known
        """
        known_vars = {}
        for var_name, var in self.variables.items():
            if self._original_variable_states.get(var_name, False):
                known_vars[var_name] = var
        return known_vars

    def get_unknown_variables(self) -> dict[str, Quantity]:
        """
        Get unknown variables for report generation.

        Returns:
            Dictionary of variable names to Quantity objects that were originally unknown
        """
        unknown_vars = {}
        for var_name, var in self.variables.items():
            if not self._original_variable_states.get(var_name, False):
                unknown_vars[var_name] = var
        return unknown_vars

    def _resolve_relative_angles(self) -> None:
        """
        Resolve any relative angle constraints before solving.

        Iteratively resolves forces that have relative angle constraints (e.g., "30 degrees from F_R")
        by converting them to absolute angles. Handles chains of dependencies.
        """
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            # Find forces with unresolved relative angles
            unresolved = [f for f in self.forces.values() if f.has_relative_angle()]

            if not unresolved:
                # All resolved!
                return

            # Try to resolve each one
            resolved_any = False
            for force in unresolved:
                try:
                    force.resolve_relative_angle(self.forces)
                    resolved_any = True
                    self.logger.info(f"Resolved relative angle for {force.name}")
                except ValueError as e:
                    # Can't resolve yet - might depend on another force that isn't resolved
                    self.logger.debug(f"Cannot resolve {force.name} yet: {e}")
                    continue

            if not resolved_any:
                # Made no progress - check if it's because references are to unknown forces
                # In that case, these will be handled by the parametric solver
                all_refs_unknown = True
                for force in unresolved:
                    if force._relative_to_force in self.forces:
                        ref_force = self.forces[force._relative_to_force]
                        if ref_force.angle is not None and ref_force.angle.value is not None:
                            # Reference has known angle but we couldn't resolve - that's bad
                            all_refs_unknown = False
                            break

                if all_refs_unknown:
                    # All unresolved constraints reference unknown forces
                    # These will be handled by the parametric solver
                    self.logger.info(f"Skipping resolution of {len(unresolved)} parametric angle constraints (will be solved parametrically)")
                    return

                # Otherwise, we have a problem (circular dependency or missing reference)
                unresolved_names = [f.name for f in unresolved]
                raise ValueError(f"Cannot resolve relative angle constraints for: {', '.join(unresolved_names)}. Check for circular dependencies or missing force references.")

            iteration += 1

        # If we get here, we exceeded max iterations
        raise ValueError("Exceeded maximum iterations while resolving relative angle constraints")

    def solve(self, max_iterations: int = 100, tolerance: float = 1e-10) -> dict[str, ForceVector]:  # type: ignore[override]
        """
        Solve the vector equilibrium problem algebraically.

        Args:
            max_iterations: Not used (for compatibility with parent class)
            tolerance: Not used (for compatibility with parent class)

        Returns:
            Dictionary mapping force names to solved ForceVector objects

        Raises:
            ValueError: If problem is under-constrained or over-constrained
        """
        self.solution_steps = []

        # Save original is_known state for each force (for report generation)
        if not self._original_force_states:  # Only save once
            for force_name, force in self.forces.items():
                # Save whether the force was known
                self._original_force_states[force_name] = force.is_known

                # Also track which individual components were known before solving
                # This handles partially known forces (e.g., known angle, unknown magnitude)
                mag_known = force.magnitude is not None and force.magnitude.value is not None
                angle_known = force.angle is not None and force.angle.value is not None
                self._original_variable_states[f"{force_name}_mag_known"] = mag_known
                self._original_variable_states[f"{force_name}_angle_known"] = angle_known

        # Resolve any relative angle constraints before analyzing
        self._resolve_relative_angles()

        # Analyze problem type - use actual values, not just is_known flag
        # A force is truly known only if it has both magnitude and angle values
        resultant_forces = [f for f in self.forces.values() if f.is_resultant]

        # Count actual unknowns (magnitudes and angles separately) across ALL forces
        total_unknowns = 0
        partially_known_forces = []
        fully_unknown_forces = []
        known_forces = []
        unknown_forces = []

        for force in self.forces.values():
            mag_unknown = force.magnitude is None or force.magnitude.value is None
            # An angle is unknown if it's None OR if it has an unresolved relative constraint
            angle_unknown = (force.angle is None or force.angle.value is None or
                           force.has_relative_angle())

            # Check if this is a parametric angle constraint
            is_parametric = angle_unknown and force._relative_to_force is not None

            # For counting total_unknowns, don't count parametric angles as separate unknowns
            # But still mark the force as unknown for the solver to handle
            angle_unknown_for_count = angle_unknown and not is_parametric

            if mag_unknown and angle_unknown_for_count:
                fully_unknown_forces.append(force)
                unknown_forces.append(force)
                total_unknowns += 2  # Both magnitude and angle unknown
            elif mag_unknown or angle_unknown_for_count:
                partially_known_forces.append(force)
                unknown_forces.append(force)
                total_unknowns += 1  # Either magnitude or angle unknown (non-parametric)
            elif is_parametric:
                # Parametric angle - still needs to be solved but doesn't add to total_unknowns
                partially_known_forces.append(force)
                unknown_forces.append(force)
                # Don't increment total_unknowns - will be determined by reference force
            else:
                # Fully known - has both magnitude and angle
                known_forces.append(force)

        self.logger.info(f"Solving {self.name}: {len(known_forces)} known, {len(unknown_forces)} unknown ({total_unknowns} total unknowns)")

        # Check for special case: all magnitudes known, all angles unknown (angle-between problem)
        all_mags_known = all(
            f.magnitude is not None and f.magnitude.value is not None
            for f in self.forces.values()
        )
        all_angles_unknown = all(
            f.angle is None or f.angle.value is None
            for f in self.forces.values()
        )

        if all_mags_known and all_angles_unknown and len(self.forces) <= 3:
            # This is an angle-between problem (e.g., Problem 2-23)
            # Given: F1, F2, FR magnitudes
            # Find: angle θ between F1 and F2
            self._solve_angle_between_forces(list(self.forces.values()), resultant_forces)
            self.is_solved = True
            self._populate_variables_from_forces()
            self._populate_solving_history()
            return self.forces

        # Determine solution method
        if len(unknown_forces) == 0:
            # All forces known - compute resultant
            self._solve_resultant(known_forces)
        elif len(unknown_forces) == 1 and len(known_forces) >= 1:
            # One unknown - solve using equilibrium
            self._solve_single_unknown(known_forces, unknown_forces[0], resultant_forces)
        elif len(unknown_forces) == 2 and len(resultant_forces) == 1:
            # Two unknowns with resultant
            # First check if any force has a parametric angle constraint (relative to another unknown)
            has_parametric_constraint = any(f._relative_to_force is not None for f in unknown_forces)

            if has_parametric_constraint:
                # Use parametric angle constraint solver
                self._solve_with_parametric_angle_constraint(known_forces, unknown_forces, resultant_forces[0])
            elif total_unknowns == 2 and len(partially_known_forces) == 2:
                # Check if we have one with known mag and one with known angle (complementary unknowns)
                has_known_mag = any(f.magnitude is not None and f.magnitude.value is not None for f in partially_known_forces)
                has_known_angle = any(f.angle is not None and f.angle.value is not None for f in partially_known_forces)

                if has_known_mag and has_known_angle:
                    # One force with known mag/unknown angle, one with known angle/unknown mag
                    self._solve_two_partially_known_equilibrium(known_forces, partially_known_forces, resultant_forces[0])
                else:
                    # Both have same property known (either both angles OR both magnitudes)
                    all_angles_known = all(f.angle is not None and f.angle.value is not None for f in partially_known_forces)
                    all_mags_known = all(f.magnitude is not None and f.magnitude.value is not None for f in partially_known_forces)

                    if all_angles_known:
                        # Both angles known, magnitudes unknown - use Law of Sines
                        self._solve_two_unknowns_with_resultant(known_forces, unknown_forces, resultant_forces[0])
                    elif all_mags_known and resultant_forces[0].is_known:
                        # Both magnitudes known, angles unknown, and resultant fully known
                        # Can solve using component equations (2 equations, 2 unknown angles)
                        self._solve_two_angles_with_known_magnitudes(known_forces, partially_known_forces, resultant_forces[0])
                    else:
                        raise ValueError("Cannot solve: two unknowns require known angles or magnitudes with fully known resultant")
            elif resultant_forces[0].is_known:
                # Resultant fully known - use standard solver
                self._solve_two_unknowns_with_resultant(known_forces, unknown_forces, resultant_forces[0])
            else:
                raise ValueError("Cannot solve: two unknowns require a known resultant")
        elif len(unknown_forces) == 3 and len(resultant_forces) == 1:
            # Three unknowns - check if parametric constraint exists
            has_parametric_constraint = any(f._relative_to_force is not None for f in unknown_forces)
            if has_parametric_constraint and total_unknowns == 2:
                # Parametric constraint with 2 total unknowns
                self._solve_with_parametric_angle_constraint(known_forces, unknown_forces, resultant_forces[0])
            else:
                raise ValueError(f"Cannot solve: {len(unknown_forces)} unknown forces with {total_unknowns} total unknowns")
        else:
            raise ValueError(f"Problem configuration not supported: {len(known_forces)} known, {len(unknown_forces)} unknown ({total_unknowns} total unknowns)")

        self.is_solved = True

        # Convert forces to variables for report generation compatibility
        self._populate_variables_from_forces()

        # Populate solving history for report generation
        self._populate_solving_history()

        return self.forces

    def _populate_variables_from_forces(self) -> None:
        """
        Convert ForceVector objects to Quantity variables for report generation.

        This ensures compatibility with qnty's report generation system.
        """
        from ..core.dimension_catalog import dim

        for force_name, force in self.forces.items():
            # Determine if this was originally known or unknown
            was_originally_known = not force.is_resultant

            if force.magnitude is not None and force.magnitude.value is not None:
                # Add magnitude as a variable
                mag_var = Quantity(name=f"{force.name} Magnitude", dim=dim.force, value=force.magnitude.value, preferred=force.magnitude.preferred, _symbol=f"{force_name}_mag")
                self.variables[f"{force_name}_mag"] = mag_var

                # Store original state for report generator
                if was_originally_known:
                    self._original_variable_states[f"{force_name}_mag"] = True
                else:
                    self._original_variable_states[f"{force_name}_mag"] = False

            if force.angle is not None and force.angle.value is not None:
                # Add angle as a variable
                angle_var = Quantity(name=f"{force.name} Direction", dim=dim.D, value=force.angle.value, preferred=force.angle.preferred, _symbol=f"{force_name}_angle")
                self.variables[f"{force_name}_angle"] = angle_var

                # Store original state
                if was_originally_known:
                    self._original_variable_states[f"{force_name}_angle"] = True
                else:
                    self._original_variable_states[f"{force_name}_angle"] = False

            # Add components if available
            if force.x is not None and force.x.value is not None:
                x_var = Quantity(name=f"{force.name} X-Component", dim=dim.force, value=force.x.value, preferred=force.x.preferred, _symbol=f"{force_name}_x")
                self.variables[f"{force_name}_x"] = x_var

            if force.y is not None and force.y.value is not None:
                y_var = Quantity(name=f"{force.name} Y-Component", dim=dim.force, value=force.y.value, preferred=force.y.preferred, _symbol=f"{force_name}_y")
                self.variables[f"{force_name}_y"] = y_var

    def _populate_solving_history(self) -> None:
        """
        Convert solution_steps to solving_history format for report generation.

        This ensures the step-by-step solution shows up in generated reports.
        """
        self.solving_history = []

        for i, step in enumerate(self.solution_steps):
            # Our new format already has the correct fields
            history_entry = {
                "step": i + 1,
                "target": step.get("target", "Unknown"),
                "method": step.get("method", "algebraic"),
                "description": step.get("description", ""),
                "equation_str": step.get("equation", ""),
                "substituted": step.get("substitution", ""),
                "result_value": step.get("result_value", ""),
                "result_unit": step.get("result_unit", ""),
                "details": step.get("description", ""),
            }
            self.solving_history.append(history_entry)

    def _solve_resultant(self, known_forces: list[ForceVector]) -> None:
        """
        Compute resultant of known forces.

        Uses vector addition (component summation).
        """
        self.solution_steps.append({"method": "Vector Addition (Component Summation)", "description": "Sum all force components to find resultant"})

        # Sum components
        sum_x = 0.0
        sum_y = 0.0
        sum_z = 0.0
        ref_unit = None

        for force in known_forces:
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

        # Create resultant vector
        from ..core.dimension_catalog import dim

        x_qty = Quantity(name="FR_x", dim=dim.force, value=sum_x, preferred=ref_unit)
        y_qty = Quantity(name="FR_y", dim=dim.force, value=sum_y, preferred=ref_unit)
        z_qty = Quantity(name="FR_z", dim=dim.force, value=sum_z, preferred=ref_unit)

        resultant_vector = Vector.from_quantities(x_qty, y_qty, z_qty)

        # Find or create resultant force
        resultant = None
        for force_name, force in self.forces.items():
            if force.is_resultant:
                resultant = force
                break

        if resultant is None:
            resultant = ForceVector(vector=resultant_vector, name="FR", is_resultant=True)
            self.forces["FR"] = resultant
            setattr(self, "FR", resultant)
        else:
            # Update existing resultant
            resultant.copy_coords_from(resultant_vector)
            resultant._compute_magnitude_and_angle()
            resultant.is_known = True

        if ref_unit is not None and resultant.magnitude is not None and resultant.angle is not None:
            mag_value = resultant.magnitude.value / ref_unit.si_factor if resultant.magnitude.value is not None else 0.0
            ang_value = resultant.angle.value * 180 / math.pi if resultant.angle.value is not None else 0.0
            self.solution_steps.append({"result": f"Resultant: {mag_value:.2f} {ref_unit.symbol} at {ang_value:.1f}°"})

    def _solve_single_unknown(self, known_forces: list[ForceVector], unknown_force: ForceVector, resultant_forces: list[ForceVector]) -> None:
        """
        Solve for single unknown force given known forces.

        Uses law of cosines and law of sines.
        """
        # Special case: Known resultant + one known force, solve for unknown force
        # Pattern: F_unknown + F_known = F_resultant (where F_resultant is also in known_forces)
        if len(resultant_forces) == 1 and len(known_forces) == 2:
            # Check if one of the known forces is the resultant
            resultant = resultant_forces[0]
            if any(f is resultant for f in known_forces):
                # Find the other known force (not the resultant)
                other_known = [f for f in known_forces if f is not resultant][0]
                # Solve: F_unknown = F_resultant - F_other_known
                self._solve_unknown_from_resultant_and_known(unknown_force, resultant, other_known)
                return

        if len(known_forces) == 2 and len(resultant_forces) == 1:
            # Two known forces, unknown resultant
            self._solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) == 2 and unknown_force.is_resultant:
            # Two known forces, solve for resultant
            self._solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) >= 3 and unknown_force.is_resultant:
            # Multiple known forces (3+), solve for resultant using vector addition
            # F_R = F_1 + F_2 + F_3 + ...
            sum_x = 0.0
            sum_y = 0.0
            sum_z = 0.0
            ref_unit = None

            for force in known_forces:
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

            # Create resultant vector
            from ..core.dimension_catalog import dim

            x_qty = Quantity(name=f"{unknown_force.name}_x", dim=dim.force, value=sum_x, preferred=ref_unit)
            y_qty = Quantity(name=f"{unknown_force.name}_y", dim=dim.force, value=sum_y, preferred=ref_unit)
            z_qty = Quantity(name=f"{unknown_force.name}_z", dim=dim.force, value=sum_z, preferred=ref_unit)

            unknown_force._coords = Vector.from_quantities(x_qty, y_qty, z_qty)._coords
            unknown_force._compute_magnitude_and_angle()
            unknown_force.is_known = True

            self.solution_steps.append({
                "method": "Vector Addition (Component Summation)",
                "description": f"Computing resultant {unknown_force.name} from {len(known_forces)} known forces"
            })
        elif len(known_forces) >= 2 and not unknown_force.is_resultant:
            # Multiple known forces and unknown resultant - find equilibrium force
            # First compute resultant of known forces
            self._solve_resultant(known_forces)
            # The unknown force must balance this resultant
            resultant = self.forces.get("FR")
            if resultant and resultant.vector:
                # Unknown force is negative of resultant
                unknown_vector = -resultant.vector
                unknown_force.copy_coords_from(unknown_vector)
                unknown_force._compute_magnitude_and_angle()
                unknown_force.is_known = True
        else:
            # Fall back to component summation
            self._solve_by_components(known_forces, unknown_force)

    def _solve_unknown_from_resultant_and_known(self, unknown_force: ForceVector, resultant: ForceVector, known_force: ForceVector) -> None:
        """
        Solve for unknown force given known resultant and one known force.

        Uses Law of Cosines and Law of Sines to solve the triangle formed by:
        F_unknown + F_known = F_resultant

        This is the same method as solving for a resultant from two known forces,
        but we're solving for one of the sides instead of the resultant.
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
        F_unknown_squared = F_R**2 + F_known**2 - 2 * F_R * F_known * math.cos(gamma)
        F_unknown = math.sqrt(F_unknown_squared)

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
        # Use LaTeX theta command for proper rendering with force angles
        # Format subscript to handle underscores properly (e.g., F_R becomes F_{R})
        resultant_subscript = resultant.name.replace("_", "_{") + "}" if "_" in resultant.name else resultant.name
        known_subscript = known_force.name.replace("_", "_{") + "}" if "_" in known_force.name else known_force.name
        # Display as cos(θ_R - θ_known) or cos(θ_known - θ_R) depending on which is larger
        if theta_R > theta_known:
            angle_expr = f"\\theta_{{{resultant_subscript}}} - \\theta_{{{known_subscript}}}"
        else:
            angle_expr = f"\\theta_{{{known_subscript}}} - \\theta_{{{resultant_subscript}}}"

        self.solution_steps.append(
            {
                "target": f"|{unknown_force.name}|",
                "method": "Law of Cosines",
                "equation": f"{unknown_force.name}^2 = {resultant.name}^2 + {known_force.name}^2 - 2*{resultant.name}*{known_force.name}*cos({angle_expr})",
                "substitution": f"{unknown_force.name}^2 = ({F_R:.2f} {force_unit})^2 + ({F_known:.2f} {force_unit})^2 - 2 * ({F_R:.2f} {force_unit}) * ({F_known:.2f} {force_unit}) * cos({gamma_deg:.1f}°)",
                "result_value": f"{F_unknown:.2f}",
                "result_unit": force_unit,
            }
        )

        # Step 2: Solve for unknown direction using Law of Sines
        # sin(alpha) / F_known = sin(gamma) / F_unknown
        sin_alpha = F_known * math.sin(gamma) / F_unknown
        alpha = math.asin(np.clip(sin_alpha, -1.0, 1.0))

        # The angle we report depends on the geometry
        # For the textbook problem, they report θ where sin(90°+θ)/F_known = sin(gamma)/F_unknown
        theta_unknown_deg = math.degrees(theta_unknown)

        # Format the angle expression using theta notation like in Law of Cosines
        # For consistency, use theta notation for all force angles
        unknown_subscript = unknown_force.name.replace("_", "_{") + "}" if "_" in unknown_force.name else unknown_force.name
        unknown_angle = f"\\theta_{{{unknown_subscript}}}"  # Direction angle of unknown force
        # gamma is the same angle as in Law of Cosines
        if theta_R > theta_known:
            gamma_angle = f"\\theta_{{{resultant_subscript}}} - \\theta_{{{known_subscript}}}"
        else:
            gamma_angle = f"\\theta_{{{known_subscript}}} - \\theta_{{{resultant_subscript}}}"

        self.solution_steps.append(
            {
                "target": f"{unknown_angle}",
                "method": "Law of Sines",
                "equation": f"sin({unknown_angle}) / {known_force.name} = sin({gamma_angle}) / {unknown_force.name}",
                "substitution": f"sin({unknown_angle}) / {F_known:.2f} {force_unit} = sin({gamma_deg:.1f}°) / {F_unknown:.2f} {force_unit}",
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
        unknown_vector = Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update unknown force
        unknown_force.copy_coords_from(unknown_vector)
        unknown_force._magnitude = mag_qty
        unknown_force._angle = angle_qty
        unknown_force.is_known = True

    def _solve_resultant_from_two_forces(self, force1: ForceVector, force2: ForceVector, resultant: ForceVector) -> None:
        """
        Solve for resultant of two forces using law of cosines and law of sines.

        This is the classic parallelogram/triangle method.
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
        FR_squared = F1**2 + F2**2 - 2 * F1 * F2 * math.cos(angle_in_triangle)
        FR = math.sqrt(FR_squared)

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
        # Format substitution like reference: value and unit separated, no complex nesting
        gamma_deg = math.degrees(angle_in_triangle)
        # Use LaTeX theta command for proper rendering with force angles
        # Display as cos(θ_F2 - θ_F1) or cos(θ_F1 - θ_F2) depending on which is larger
        if theta2 > theta1:
            angle_expr = f"\\theta_{{{force2.name}}} - \\theta_{{{force1.name}}}"
        else:
            angle_expr = f"\\theta_{{{force1.name}}} - \\theta_{{{force2.name}}}"

        self.solution_steps.append(
            {
                "target": f"|{resultant.name}|",
                "method": "Law of Cosines",
                "equation": f"{resultant.name}^2 = {force1.name}^2 + {force2.name}^2 - 2*{force1.name}*{force2.name}*cos(180° - ({angle_expr}))",
                "substitution": f"{resultant.name}^2 = ({F1:.2f} {force_unit})^2 + ({F2:.2f} {force_unit})^2 - 2 * ({F1:.2f} {force_unit}) * ({F2:.2f} {force_unit}) * cos({gamma_deg:.1f}°)",
                "result_value": f"{FR:.2f}",
                "result_unit": force_unit,
            }
        )

        # Step 2: Solve for resultant direction using Law of Sines
        # Calculate alpha using law of sines for display purposes
        sin_alpha = F1 * math.sin(angle_in_triangle) / FR
        alpha = math.asin(np.clip(sin_alpha, -1.0, 1.0))

        # Format resultant angle using theta notation
        resultant_subscript = resultant.name.replace("_", "_{") + "}" if "_" in resultant.name else resultant.name
        resultant_angle = f"\\theta_{{{resultant_subscript}}}"

        self.solution_steps.append(
            {
                "target": f"{resultant_angle}",
                "method": "Law of Sines",
                "equation": f"sin(alpha) / {force1.name} = sin(gamma) / {resultant.name}",
                "substitution": f"sin(alpha) / {F1:.2f} {force_unit} = sin({math.degrees(angle_in_triangle):.1f}°) / {FR:.2f} {force_unit}",
                "result_value": f"{math.degrees(theta_R):.2f}",
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
        resultant_vector = Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update resultant force
        resultant.copy_coords_from(resultant_vector)
        resultant._magnitude = mag_qty
        resultant._angle = angle_qty
        resultant.is_known = True

    def _solve_two_unknowns_with_resultant(
        self,
        known_forces: list[ForceVector],
        unknown_forces: list[ForceVector],
        resultant: ForceVector,
    ) -> None:
        """
        Solve for two unknowns given a resultant.

        This uses the TriangleSolver to solve decomposition problems where the resultant
        and component angles are known, but component magnitudes are unknown.

        Handles two cases:
        1. Resultant fully known (magnitude and angle) - use Law of Sines
        2. Resultant has known angle but unknown magnitude - solve using component equations
        """
        if resultant.is_known:
            # Case 1: Fully known resultant - use Law of Sines
            self.solver.solve_two_unknowns_with_known_resultant(unknown_forces, resultant)
        else:
            # Case 2: Resultant has known angle but unknown magnitude
            # This happens when one component is known and we're solving for the other component and resultant
            # Example: F_A (known) + F_B (unknown mag) = F_R (unknown mag, known angle)

            # Check if all angles are known
            all_angles_known = all(f.angle is not None and f.angle.value is not None for f in unknown_forces)
            if not all_angles_known or resultant.angle is None or resultant.angle.value is None:
                raise ValueError("Cannot solve: all angles must be known to solve for magnitudes")

            # Use component-based solver
            self._solve_two_magnitudes_with_known_angles(known_forces, unknown_forces, resultant)

    def _solve_two_partially_known_equilibrium(
        self,
        known_forces: list[ForceVector],
        partially_known_forces: list[ForceVector],
        resultant: ForceVector,  # noqa: ARG002
    ) -> None:
        """
        Solve for two partially known forces using equilibrium equations.

        This handles cases like:
        - Force A: known magnitude, unknown angle
        - Force R (resultant): known angle, unknown magnitude
        - Force B: fully known

        Uses ΣFx = 0 and ΣFy = 0 to solve for the two unknowns.
        """
        import math

        self.solution_steps.append({
            "method": "Equilibrium with Partially Known Forces",
            "description": "Using ΣFx = 0 and ΣFy = 0 with partially known force properties"
        })

        # Identify which force has known magnitude and which has known angle
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

        # Sum components of fully known forces (no sign adjustment here)
        sum_x = 0.0
        sum_y = 0.0
        ref_unit = None

        for force in known_forces:
            if force.vector is None or force.x is None or force.y is None:
                continue

            if force.x.value is not None:
                sum_x += force.x.value
            if force.y.value is not None:
                sum_y += force.y.value

            if ref_unit is None and force.x.preferred is not None:
                ref_unit = force.x.preferred

        # Let F_A be the force with known magnitude M and unknown angle θ
        # Let F_R be the force with known angle α and unknown magnitude R
        #
        # For resultant: F_R = F_A + F_B
        # In components: R*cos(α) = M*cos(θ) + sum_x
        #                R*sin(α) = M*sin(θ) + sum_y
        #
        # Rearrange: M*cos(θ) = R*cos(α) - sum_x
        #            M*sin(θ) = R*sin(α) - sum_y
        #
        # Square and add to eliminate θ:
        #   M² = (R*cos(α) - sum_x)² + (R*sin(α) - sum_y)²
        #   M² = R² - 2R(cos(α)*sum_x + sin(α)*sum_y) + sum_x² + sum_y²
        #
        # Quadratic in R: R² - 2R(cos(α)*sum_x + sin(α)*sum_y) + (sum_x² + sum_y² - M²) = 0

        # Type assertions for type checker
        assert force_with_known_mag.magnitude is not None and force_with_known_mag.magnitude.value is not None
        assert force_with_known_angle.angle is not None and force_with_known_angle.angle.value is not None

        M = force_with_known_mag.magnitude.value
        alpha_rad = force_with_known_angle.angle.value  # In radians, standard form

        # Quadratic coefficients: a*R² + b*R + c = 0
        # From equilibrium: R² - 2R(cos(α)*sum_x + sin(α)*sum_y) + (sum_x² + sum_y² - M²) = 0
        a = 1.0
        b = -2.0 * (math.cos(alpha_rad) * sum_x + math.sin(alpha_rad) * sum_y)
        c = sum_x**2 + sum_y**2 - M**2

        # Solve quadratic
        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            raise ValueError("No solution exists (discriminant < 0)")

        R1 = (-b + math.sqrt(discriminant)) / (2*a)
        R2 = (-b - math.sqrt(discriminant)) / (2*a)

        # Use the appropriate root
        # For resultant, we typically want the larger magnitude root
        if force_with_known_angle.is_resultant:
            # Pick the root with larger absolute value (typically the physically meaningful one)
            R = abs(R2) if abs(R2) > abs(R1) else abs(R1)
        else:
            # For non-resultant, pick first positive root
            R = R1 if R1 > 0 else R2
            if R < 0:
                raise ValueError("No positive solution for non-resultant force")

        # Calculate theta from equilibrium: R*cos(α) = M*cos(θ) + sum_x
        # Rearranging: M*cos(θ) = R*cos(α) - sum_x
        cos_theta = (R * math.cos(alpha_rad) - sum_x) / M
        sin_theta = (R * math.sin(alpha_rad) - sum_y) / M

        theta_rad = math.atan2(sin_theta, cos_theta)

        # Update the forces
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        # Update force with known magnitude (set angle)
        degree_unit = ureg.resolve("degree", dim=dim.D)
        force_with_known_mag._angle = Quantity(
            name=f"{force_with_known_mag.name}_angle",
            dim=dim.D,
            value=theta_rad,
            preferred=degree_unit
        )

        # Recreate vector for force with now-known angle
        # theta_rad and M are physical quantities (already in SI units)
        x_val = M * math.cos(theta_rad)
        y_val = M * math.sin(theta_rad)
        z_val = 0.0
        pref_unit = ref_unit or force_with_known_mag.magnitude.preferred
        x_qty = Quantity(name=f"{force_with_known_mag.name}_x", dim=dim.force, value=x_val, preferred=pref_unit)
        y_qty = Quantity(name=f"{force_with_known_mag.name}_y", dim=dim.force, value=y_val, preferred=pref_unit)
        z_qty = Quantity(name=f"{force_with_known_mag.name}_z", dim=dim.force, value=z_val, preferred=pref_unit)
        force_with_known_mag._coords = Vector.from_quantities(x_qty, y_qty, z_qty)._coords
        force_with_known_mag.is_known = True

        # Update force with known angle (set magnitude)
        force_with_known_angle._magnitude = Quantity(
            name=f"{force_with_known_angle.name}_magnitude",
            dim=force_with_known_mag.magnitude.dim,
            value=R,
            preferred=ref_unit or force_with_known_mag.magnitude.preferred
        )

        # Recreate vector for force with now-known magnitude
        # R is always positive, alpha_rad is the direction (already in SI units)
        x_val_r = R * math.cos(alpha_rad)
        y_val_r = R * math.sin(alpha_rad)
        z_val_r = 0.0
        pref_unit = ref_unit or force_with_known_mag.magnitude.preferred
        x_qty_r = Quantity(name=f"{force_with_known_angle.name}_x", dim=dim.force, value=x_val_r, preferred=pref_unit)
        y_qty_r = Quantity(name=f"{force_with_known_angle.name}_y", dim=dim.force, value=y_val_r, preferred=pref_unit)
        z_qty_r = Quantity(name=f"{force_with_known_angle.name}_z", dim=dim.force, value=z_val_r, preferred=pref_unit)
        force_with_known_angle._coords = Vector.from_quantities(x_qty_r, y_qty_r, z_qty_r)._coords
        force_with_known_angle.is_known = True

    def _solve_two_magnitudes_with_known_angles(
        self,
        known_forces: list[ForceVector],
        unknown_forces: list[ForceVector],
        resultant: ForceVector,
    ) -> None:
        """
        Solve for two unknown magnitudes given known angles.

        Handles the case where:
        - One or more forces are fully known
        - Two forces have known angles but unknown magnitudes (one may be the resultant)
        - Equilibrium: sum of known + unknowns = resultant (or sum = 0 if no resultant)

        Uses component-based linear system:
        - ΣF_x = 0: known_x + M1*cos(θ1) + M2*cos(θ2) = 0 (or = resultant_x if resultant is external)
        - ΣF_y = 0: known_y + M1*sin(θ1) + M2*sin(θ2) = 0 (or = resultant_y if resultant is external)

        For the case where the resultant is one of the unknowns:
        - known + M1*cos(θ1) = M_R*cos(θ_R)
        - known + M1*sin(θ1) = M_R*sin(θ_R)
        """
        # Sum all known forces
        sum_x = 0.0
        sum_y = 0.0
        ref_unit = None

        for force in known_forces:
            if force.vector and force.x and force.y:
                if force.x.value is not None:
                    sum_x += force.x.value
                if force.y.value is not None:
                    sum_y += force.y.value
                if ref_unit is None and force.x.preferred:
                    ref_unit = force.x.preferred

        # Identify which unknown is the resultant and which is the component
        # The resultant should be one of the unknown forces
        component_force = None
        resultant_is_unknown = resultant in unknown_forces

        if resultant_is_unknown:
            # Resultant is one of the unknowns - get the other unknown
            # Use 'is not' for object identity, not '!=' (which uses __eq__ and returns True for all unknowns)
            other_unknowns = [f for f in unknown_forces if f is not resultant]
            if len(other_unknowns) != 1:
                raise ValueError(f"Expected exactly 1 non-resultant unknown force, got {len(other_unknowns)}")
            component_force = other_unknowns[0]
        else:
            # Resultant is fully known but passed as parameter - shouldn't happen
            raise ValueError("Cannot solve: expected resultant to be one of the unknowns for this solver method")

        # Get angles - validated earlier so we know they're not None
        if component_force.angle is None or component_force.angle.value is None:
            raise ValueError(f"Component force {component_force.name} must have a known angle")
        if resultant.angle is None or resultant.angle.value is None:
            raise ValueError(f"Resultant {resultant.name} must have a known angle")

        theta_comp: float = component_force.angle.value  # radians
        theta_res: float = resultant.angle.value  # radians

        # Set up linear system:
        # sum_x + M_comp * cos(θ_comp) = M_res * cos(θ_res)
        # sum_y + M_comp * sin(θ_comp) = M_res * sin(θ_res)
        #
        # Rearranging:
        # M_comp * cos(θ_comp) - M_res * cos(θ_res) = -sum_x
        # M_comp * sin(θ_comp) - M_res * sin(θ_res) = -sum_y
        #
        # In matrix form: A * [M_comp, M_res]^T = b
        A = np.array([
            [math.cos(theta_comp), -math.cos(theta_res)],
            [math.sin(theta_comp), -math.sin(theta_res)]
        ])
        b = np.array([-sum_x, -sum_y])

        # Solve for magnitudes
        try:
            magnitudes = np.linalg.solve(A, b)
            M_comp = float(magnitudes[0])
            M_res = float(magnitudes[1])
        except np.linalg.LinAlgError:
            raise ValueError("Cannot solve: system is singular (forces may be collinear)")

        # Check if forces are nearly perpendicular (potential optimization/minimization problem)
        # When perpendicular, there are two solutions - we want the one where resultant has larger magnitude
        angle_diff = abs(theta_res - theta_comp)
        angle_diff_normalized = angle_diff % (2 * math.pi)
        is_near_perpendicular = abs(angle_diff_normalized - math.pi/2) < 0.01 or abs(angle_diff_normalized - 3*math.pi/2) < 0.01

        if is_near_perpendicular and abs(M_res) < abs(M_comp):
            # We got the wrong solution - swap them
            # The correct interpretation is that the component has the smaller magnitude
            M_comp, M_res = M_res, M_comp
            # If either is negative after swap, flip both signs to get the physical solution
            if M_comp < 0 or M_res < 0:
                M_comp = abs(M_comp)
                M_res = abs(M_res)

        # Use the magnitudes as-is (can be negative, which indicates direction opposite to the specified angle)
        # Create magnitude quantities
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        mag_comp_qty = Quantity(
            name=f"{component_force.name}_magnitude",
            dim=dim.force,
            value=M_comp,
            preferred=ref_unit
        )
        mag_res_qty = Quantity(
            name=f"{resultant.name}_magnitude",
            dim=dim.force,
            value=M_res,
            preferred=ref_unit
        )

        # Create angle quantities (use the original angles)
        degree_unit = ureg.resolve("degree", dim=dim.D)
        angle_comp_qty = Quantity(
            name=f"{component_force.name}_angle",
            dim=dim.D,
            value=theta_comp,
            preferred=degree_unit
        )
        angle_res_qty = Quantity(
            name=f"{resultant.name}_angle",
            dim=dim.D,
            value=theta_res,
            preferred=degree_unit
        )

        # Create vectors using the magnitudes and angles as computed (already in SI units)
        # If magnitude is negative, the vector will point in the opposite direction
        comp_x = M_comp * math.cos(theta_comp)
        comp_y = M_comp * math.sin(theta_comp)
        comp_x_qty = Quantity(name=f"{component_force.name}_x", dim=dim.force, value=comp_x, preferred=ref_unit)
        comp_y_qty = Quantity(name=f"{component_force.name}_y", dim=dim.force, value=comp_y, preferred=ref_unit)
        comp_z_qty = Quantity(name=f"{component_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        component_force._coords = Vector.from_quantities(comp_x_qty, comp_y_qty, comp_z_qty)._coords
        component_force._magnitude = mag_comp_qty
        component_force._angle = angle_comp_qty
        component_force.is_known = True

        res_x = M_res * math.cos(theta_res)
        res_y = M_res * math.sin(theta_res)
        res_x_qty = Quantity(name=f"{resultant.name}_x", dim=dim.force, value=res_x, preferred=ref_unit)
        res_y_qty = Quantity(name=f"{resultant.name}_y", dim=dim.force, value=res_y, preferred=ref_unit)
        res_z_qty = Quantity(name=f"{resultant.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        resultant._coords = Vector.from_quantities(res_x_qty, res_y_qty, res_z_qty)._coords
        resultant._magnitude = mag_res_qty
        resultant._angle = angle_res_qty
        resultant.is_known = True

        # Add solution steps
        self.solution_steps.append({
            "method": "Component Equilibrium (Linear System)",
            "description": f"Solving for {component_force.name} and {resultant.name} magnitudes using equilibrium equations",
            "equations": [
                f"ΣFx: {sum_x:.2f} + {component_force.name}*cos({math.degrees(theta_comp):.1f}°) = {resultant.name}*cos({math.degrees(theta_res):.1f}°)",
                f"ΣFy: {sum_y:.2f} + {component_force.name}*sin({math.degrees(theta_comp):.1f}°) = {resultant.name}*sin({math.degrees(theta_res):.1f}°)"
            ],
            "results": [
                f"{component_force.name} = {M_comp:.2f} {ref_unit.symbol if ref_unit else 'SI'}",
                f"{resultant.name} = {M_res:.2f} {ref_unit.symbol if ref_unit else 'SI'}"
            ]
        })

    def _solve_two_angles_with_known_magnitudes(
        self,
        known_forces: list[ForceVector],
        partially_known_forces: list[ForceVector],
        resultant: ForceVector,
    ) -> None:
        """
        Solve for two unknown angles given known magnitudes and a fully known resultant.

        Handles the case where:
        - Two forces have known magnitudes but unknown angles
        - Resultant is fully known (both magnitude and angle)
        - Zero or more additional forces are fully known

        Uses component-based system of nonlinear equations:
        - ΣF_x = F_R_x: M1*cos(θ1) + M2*cos(θ2) + known_x = M_R*cos(θ_R)
        - ΣF_y = F_R_y: M1*sin(θ1) + M2*sin(θ2) + known_y = M_R*sin(θ_R)

        This is solved by converting to a system that can be solved analytically:
        Let A = M_R*cos(θ_R) - known_x and B = M_R*sin(θ_R) - known_y
        Then: M1*cos(θ1) + M2*cos(θ2) = A
              M1*sin(θ1) + M2*sin(θ2) = B

        We solve for θ1 and θ2 using trigonometric methods.
        """
        import math

        # Verify exactly 2 partially known forces
        if len(partially_known_forces) != 2:
            raise ValueError(f"Expected exactly 2 partially known forces, got {len(partially_known_forces)}")

        # Verify resultant is fully known
        if not resultant.is_known or resultant.magnitude is None or resultant.magnitude.value is None:
            raise ValueError("Resultant must be fully known (magnitude and angle)")
        if resultant.angle is None or resultant.angle.value is None:
            raise ValueError("Resultant must have a known angle")

        force1, force2 = partially_known_forces

        # Verify both have known magnitudes but unknown angles
        if force1.magnitude is None or force1.magnitude.value is None:
            raise ValueError(f"Force {force1.name} must have a known magnitude")
        if force2.magnitude is None or force2.magnitude.value is None:
            raise ValueError(f"Force {force2.name} must have a known magnitude")
        if force1.angle is not None and force1.angle.value is not None:
            raise ValueError(f"Force {force1.name} must have an unknown angle")
        if force2.angle is not None and force2.angle.value is not None:
            raise ValueError(f"Force {force2.name} must have an unknown angle")

        # Sum all fully known forces (excluding the resultant)
        sum_x = 0.0
        sum_y = 0.0
        ref_unit = None

        for force in known_forces:
            # Skip the resultant - it's what we're solving FOR, not summing
            if force.is_resultant:
                continue
            if force.vector and force.x and force.y:
                if force.x.value is not None:
                    sum_x += force.x.value
                if force.y.value is not None:
                    sum_y += force.y.value
                if ref_unit is None and force.x.preferred:
                    ref_unit = force.x.preferred

        # Get reference unit from resultant or partially known forces if not found
        if ref_unit is None:
            if resultant.magnitude and resultant.magnitude.preferred:
                ref_unit = resultant.magnitude.preferred
            elif force1.magnitude and force1.magnitude.preferred:
                ref_unit = force1.magnitude.preferred
            elif force2.magnitude and force2.magnitude.preferred:
                ref_unit = force2.magnitude.preferred

        # Get magnitudes and resultant components
        M1 = force1.magnitude.value
        M2 = force2.magnitude.value
        M_R = resultant.magnitude.value
        theta_R = resultant.angle.value  # radians

        # Compute target components (what F1 + F2 must equal)
        A = M_R * math.cos(theta_R) - sum_x  # Target x-component
        B = M_R * math.sin(theta_R) - sum_y  # Target y-component

        self.solution_steps.append({
            "method": "Component Equilibrium (Nonlinear System)",
            "description": f"Solving for {force1.name} and {force2.name} angles using equilibrium equations",
            "equations": [
                f"{force1.name}*cos(θ₁) + {force2.name}*cos(θ₂) = {A:.3f}",
                f"{force1.name}*sin(θ₁) + {force2.name}*sin(θ₂) = {B:.3f}",
            ],
        })

        # System of equations:
        # M1*cos(θ1) + M2*cos(θ2) = A
        # M1*sin(θ1) + M2*sin(θ2) = B
        #
        # Strategy: Use substitution to solve for one angle, then back-substitute
        # From equation 1: cos(θ2) = (A - M1*cos(θ1)) / M2
        # From equation 2: sin(θ2) = (B - M1*sin(θ1)) / M2
        #
        # Using cos²(θ2) + sin²(θ2) = 1:
        # [(A - M1*cos(θ1)) / M2]² + [(B - M1*sin(θ1)) / M2]² = 1
        #
        # Expanding:
        # (A - M1*cos(θ1))² + (B - M1*sin(θ1))² = M2²
        # A² - 2A*M1*cos(θ1) + M1²*cos²(θ1) + B² - 2B*M1*sin(θ1) + M1²*sin²(θ1) = M2²
        # A² + B² + M1²*(cos²(θ1) + sin²(θ1)) - 2M1*(A*cos(θ1) + B*sin(θ1)) = M2²
        # A² + B² + M1² - 2M1*(A*cos(θ1) + B*sin(θ1)) = M2²
        #
        # Rearranging:
        # A*cos(θ1) + B*sin(θ1) = (A² + B² + M1² - M2²) / (2*M1)
        #
        # This is of the form: a*cos(θ) + b*sin(θ) = c
        # Which can be solved using: R*cos(θ - φ) = c, where R = √(a² + b²), φ = atan2(b, a)

        # Compute the right-hand side
        rhs = (A**2 + B**2 + M1**2 - M2**2) / (2 * M1)

        # Solve: A*cos(θ1) + B*sin(θ1) = rhs
        # Rewrite as: R*cos(θ1 - φ) = rhs, where R = √(A² + B²), φ = atan2(B, A)
        R = math.sqrt(A**2 + B**2)

        if abs(rhs) > R + 1e-9:  # Allow small numerical tolerance
            raise ValueError(f"No solution exists: |{rhs:.6f}| > {R:.6f} (forces cannot form a closed triangle)")

        # Clamp to valid range to handle numerical errors
        cos_value = rhs / R
        cos_value = max(-1.0, min(1.0, cos_value))

        phi = math.atan2(B, A)
        alpha = math.acos(cos_value)

        # Two possible solutions: θ1 = φ + α or θ1 = φ - α
        theta1_solution1 = phi + alpha
        theta1_solution2 = phi - alpha

        # For each θ1 solution, compute the corresponding θ2
        def compute_theta2(theta1):
            """Compute θ2 given θ1."""
            cos_theta2 = (A - M1 * math.cos(theta1)) / M2
            sin_theta2 = (B - M1 * math.sin(theta1)) / M2
            return math.atan2(sin_theta2, cos_theta2)

        theta2_solution1 = compute_theta2(theta1_solution1)
        theta2_solution2 = compute_theta2(theta1_solution2)

        # Choose the solution that makes physical sense
        # Typically, we want angles in the range [0, 2π) or [-π, π)
        # For now, use the first solution (can be refined based on problem constraints)
        theta1 = theta1_solution1
        theta2 = theta2_solution1

        # Normalize to [0, 2π) for consistency
        theta1 = theta1 % (2 * math.pi)
        theta2 = theta2 % (2 * math.pi)

        # Create angle quantities
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        angle1_qty = Quantity(
            name=f"{force1.name}_angle",
            dim=dim.D,
            value=theta1,
            preferred=degree_unit
        )
        angle2_qty = Quantity(
            name=f"{force2.name}_angle",
            dim=dim.D,
            value=theta2,
            preferred=degree_unit
        )

        # Create magnitude quantities (already known, but need as Quantity objects)
        mag1_qty = Quantity(
            name=f"{force1.name}_magnitude",
            dim=dim.force,
            value=M1,
            preferred=ref_unit
        )
        mag2_qty = Quantity(
            name=f"{force2.name}_magnitude",
            dim=dim.force,
            value=M2,
            preferred=ref_unit
        )

        # Create vectors
        f1_x = M1 * math.cos(theta1)
        f1_y = M1 * math.sin(theta1)
        f1_x_qty = Quantity(name=f"{force1.name}_x", dim=dim.force, value=f1_x, preferred=ref_unit)
        f1_y_qty = Quantity(name=f"{force1.name}_y", dim=dim.force, value=f1_y, preferred=ref_unit)
        f1_z_qty = Quantity(name=f"{force1.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        force1._coords = Vector.from_quantities(f1_x_qty, f1_y_qty, f1_z_qty)._coords
        force1._magnitude = mag1_qty
        force1._angle = angle1_qty
        force1.is_known = True

        f2_x = M2 * math.cos(theta2)
        f2_y = M2 * math.sin(theta2)
        f2_x_qty = Quantity(name=f"{force2.name}_x", dim=dim.force, value=f2_x, preferred=ref_unit)
        f2_y_qty = Quantity(name=f"{force2.name}_y", dim=dim.force, value=f2_y, preferred=ref_unit)
        f2_z_qty = Quantity(name=f"{force2.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        force2._coords = Vector.from_quantities(f2_x_qty, f2_y_qty, f2_z_qty)._coords
        force2._magnitude = mag2_qty
        force2._angle = angle2_qty
        force2.is_known = True

        # Add solution results
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        self.solution_steps.append({
            "results": [
                f"{force1.name} angle = {theta1_deg:.2f}°",
                f"{force2.name} angle = {theta2_deg:.2f}°"
            ]
        })

    def _solve_with_parametric_angle_constraint(self, known_forces: list[ForceVector], unknown_forces: list[ForceVector], resultant: ForceVector) -> None:
        """
        Solve equilibrium when one force has a relative angle constraint to another unknown force.

        Example: F_BA at angle (φ - 30°), F_BC at angle -45°, F_R at angle φ
        This creates a parametric system where φ is the unknown angle parameter.

        Args:
            known_forces: List of known forces
            unknown_forces: List of unknown forces (includes the one with parametric constraint)
            resultant: The resultant force
        """
        # Identify which force has the parametric constraint
        parametric_force = None
        reference_force = None
        independent_force = None

        for force in unknown_forces:
            if force._relative_to_force is not None:
                parametric_force = force
                # Find the reference force
                ref_name = force._relative_to_force
                reference_force = next((f for f in unknown_forces if f.name == ref_name), None)
                if reference_force is None:
                    raise ValueError(f"Force {force.name} references {ref_name}, but that force is not in the unknown forces list")

        # Find independent force (the third force that's not parametric and not reference)
        # First try to find it in unknown_forces (excluding parametric and reference forces)
        for force in unknown_forces:
            if force is not parametric_force and force is not reference_force and independent_force is None:
                # Only use if it's not the resultant (resultant will be handled separately)
                if not force.is_resultant:
                    independent_force = force
                    break

        # If no independent force found yet, check if resultant can serve as independent force
        # This handles cases like problem 2-19 where the resultant is fully known
        if independent_force is None:
            # First check if the resultant itself can be used
            if resultant.magnitude is not None and resultant.magnitude.value is not None and \
               resultant.angle is not None and resultant.angle.value is not None:
                independent_force = resultant
            else:
                # Fall back to checking unknown_forces list for a resultant with known properties
                for force in unknown_forces:
                    if force.is_resultant and force.magnitude is not None and force.magnitude.value is not None and \
                       force.angle is not None and force.angle.value is not None:
                        independent_force = force
                        break

        if parametric_force is None:
            raise ValueError("No force with parametric angle constraint found")

        if reference_force is None:
            raise ValueError("Reference force not found for parametric constraint")

        if independent_force is None:
            raise ValueError("Independent force not found for parametric constraint")

        self.logger.info(f"Solving parametric constraint: {parametric_force.name} angle relative to {reference_force.name}")

        # Get the relative angle offset
        angle_offset = parametric_force._relative_angle if parametric_force._relative_angle is not None else 0.0

        # Determine which solution pattern we have:
        # Pattern A (decomposition): F_ref (unknown angle) = F_param (parametric) + F_indep (known angle, unknown mag)
        #   - reference_force has known magnitude, unknown angle
        #   - independent_force has known angle, unknown magnitude
        #   - Example: Problem 2-16
        #
        # Pattern B (composition): F_indep (known) = F_ref (unknown) + F_param (parametric)
        #   - reference_force has unknown magnitude and angle
        #   - independent_force is fully known (resultant)
        #   - Example: Problem 2-19

        ref_mag_known = reference_force.magnitude is not None and reference_force.magnitude.value is not None
        ref_angle_known = reference_force.angle is not None and reference_force.angle.value is not None
        indep_mag_known = independent_force.magnitude is not None and independent_force.magnitude.value is not None
        indep_angle_known = independent_force.angle is not None and independent_force.angle.value is not None

        if ref_mag_known and not ref_angle_known and indep_angle_known:
            # Pattern A: Decomposition (F_ref = F_param + F_indep)
            self._solve_parametric_decomposition(
                reference_force, parametric_force, independent_force, angle_offset, resultant
            )
        elif not ref_mag_known and not ref_angle_known and indep_mag_known and indep_angle_known:
            # Pattern B: Composition (F_indep = F_ref + F_param)
            self._solve_parametric_composition(
                reference_force, parametric_force, independent_force, angle_offset, resultant
            )
        else:
            raise ValueError(
                f"Unsupported parametric constraint configuration: "
                f"ref_force={reference_force.name} ref_known=(mag={ref_mag_known}, angle={ref_angle_known}), "
                f"indep_force={independent_force.name} indep_known=(mag={indep_mag_known}, angle={indep_angle_known})"
            )

    def _solve_parametric_decomposition(
        self,
        reference_force: ForceVector,
        parametric_force: ForceVector,
        independent_force: ForceVector,
        angle_offset: float,
        resultant: ForceVector,  # noqa: ARG002
    ) -> None:
        """
        Solve Pattern A: F_ref (unknown angle) = F_param (parametric) + F_indep (known angle, unknown mag).

        Uses Law of Cosines and Law of Sines for force decomposition.
        This is used in problems like 2-16.
        """
        import math

        # Validate inputs
        if reference_force.magnitude is None or reference_force.magnitude.value is None:
            raise ValueError(f"{reference_force.name} must have known magnitude for decomposition solver")
        if parametric_force.magnitude is None or parametric_force.magnitude.value is None:
            raise ValueError(f"{parametric_force.name} must have known magnitude for decomposition solver")
        if independent_force.angle is None or independent_force.angle.value is None:
            raise ValueError(f"{independent_force.name} must have known angle for decomposition solver")

        # Get magnitudes and angles - all in SI units as per qnty conventions
        M_param_si = parametric_force.magnitude.value  # In SI (N)
        theta_indep = independent_force.angle.value  # In SI (radians)
        M_ref_si = reference_force.magnitude.value  # In SI (N)

        # Reference unit for display/output
        ref_unit = parametric_force.magnitude.preferred

        # Solve using Law of Cosines and Law of Sines for force decomposition
        # F_ref decomposes into F_param and F_indep
        # We know: M_ref_si, M_param_si (in SI), and |angle_offset| (angle between F_param and F_ref)
        #
        # Step 1: Use Law of Cosines to find M_indep_si
        # In the force triangle, the interior angle at the F_param vertex is |angle_offset|
        # Law of Cosines: M_indep_si² = M_ref_si² + M_param_si² - 2·M_ref_si·M_param_si·cos(|angle_offset|)

        angle_between = abs(angle_offset)  # Interior angle at F_param vertex
        M_indep_si = math.sqrt(
            M_ref_si**2 + M_param_si**2 - 2 * M_ref_si * M_param_si * math.cos(angle_between)
        )

        # M_indep_si is already in SI units from Law of Cosines

        # Step 2: Use Law of Sines to find the interior angle at F_indep vertex
        # Law of Sines: sin(angle_at_indep) / M_param = sin(angle_between) / M_indep
        # The angle_between (30°) is at the F_ref vertex (origin)
        # We need the angle at the F_indep vertex (where F_BC and -F_R meet)
        sin_angle_at_indep = (M_param_si * math.sin(angle_between)) / M_indep_si
        angle_at_indep_interior = math.asin(sin_angle_at_indep)

        # Now relate the interior angle to the global angles
        # angle_at_indep_interior is the angle at the vertex where F_indep meets -F_ref
        # This is the angle between F_indep direction and the direction back towards origin (-F_ref direction)
        #
        # In terms of global angles:
        # - F_indep points at angle theta_indep
        # - -F_ref points at angle (phi + 180°)
        # - The interior angle is |theta_indep - (phi + 180°)|
        #
        # So: angle_at_indep_interior = |theta_indep - phi - π|
        # Solving for phi: phi = theta_indep - π ± angle_at_indep_interior

        # The sign depends on the geometry. Let's think about it:
        # If angle_offset < 0 (F_param is CW from F_ref), then moving CCW from F_ref by angle_between gets us to F_param
        # The third force F_indep must close the triangle

        # Using the fact that interior angles sum to 180°:
        # angle_between + angle_at_indep_interior + angle_at_param = 180°
        angle_at_param = math.pi - angle_between - angle_at_indep_interior

        # Now, angle_at_param is at the vertex where F_param and F_indep meet
        # In the force triangle F_param + F_indep = F_ref:
        # - F_param points from origin at angle (phi + angle_offset)
        # - F_indep points from tip of F_param at angle theta_indep
        # - F_ref points from origin at angle phi
        #
        # The interior angle at the F_param vertex is between:
        # - Direction back towards origin: (phi + angle_offset + π)
        # - Direction towards F_indep tip: theta_indep
        #
        # So: angle_at_param = theta_indep - (phi + angle_offset + π) (mod 2π)
        # Solving for phi: phi = theta_indep - angle_offset - π - angle_at_param
        #
        # But we need to add π because we want the angle of F_ref, not -F_ref
        phi = theta_indep - angle_offset - angle_at_param


        # Update the forces - all values in SI units, Quantity handles display conversion
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        # Update reference force
        reference_force._angle = Quantity(name=f"{reference_force.name}_angle", dim=dim.D, value=phi, preferred=degree_unit)
        reference_force._magnitude = Quantity(name=f"{reference_force.name}_magnitude", dim=dim.force, value=M_ref_si, preferred=ref_unit)
        # Create vector with SI components
        ref_x = M_ref_si * math.cos(phi)
        ref_y = M_ref_si * math.sin(phi)
        ref_x_qty = Quantity(name=f"{reference_force.name}_x", dim=dim.force, value=ref_x, preferred=ref_unit)
        ref_y_qty = Quantity(name=f"{reference_force.name}_y", dim=dim.force, value=ref_y, preferred=ref_unit)
        ref_z_qty = Quantity(name=f"{reference_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        reference_force._coords = Vector.from_quantities(ref_x_qty, ref_y_qty, ref_z_qty)._coords
        reference_force.is_known = True

        # Update parametric force
        param_angle = phi + angle_offset
        parametric_force._angle = Quantity(name=f"{parametric_force.name}_angle", dim=dim.D, value=param_angle, preferred=degree_unit)
        parametric_force._magnitude = Quantity(name=f"{parametric_force.name}_magnitude", dim=dim.force, value=M_param_si, preferred=ref_unit)
        # Create vector with SI components
        param_x = M_param_si * math.cos(param_angle)
        param_y = M_param_si * math.sin(param_angle)
        param_x_qty = Quantity(name=f"{parametric_force.name}_x", dim=dim.force, value=param_x, preferred=ref_unit)
        param_y_qty = Quantity(name=f"{parametric_force.name}_y", dim=dim.force, value=param_y, preferred=ref_unit)
        param_z_qty = Quantity(name=f"{parametric_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        parametric_force._coords = Vector.from_quantities(param_x_qty, param_y_qty, param_z_qty)._coords
        parametric_force.is_known = True
        parametric_force._relative_to_force = None
        parametric_force._relative_angle = None

        # Update independent force
        independent_force._magnitude = Quantity(name=f"{independent_force.name}_magnitude", dim=dim.force, value=M_indep_si, preferred=ref_unit)
        # Create vector with SI components
        indep_x = M_indep_si * math.cos(theta_indep)
        indep_y = M_indep_si * math.sin(theta_indep)
        indep_x_qty = Quantity(name=f"{independent_force.name}_x", dim=dim.force, value=indep_x, preferred=ref_unit)
        indep_y_qty = Quantity(name=f"{independent_force.name}_y", dim=dim.force, value=indep_y, preferred=ref_unit)
        indep_z_qty = Quantity(name=f"{independent_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        independent_force._coords = Vector.from_quantities(indep_x_qty, indep_y_qty, indep_z_qty)._coords
        independent_force.is_known = True

        self.solution_steps.append({
            "method": "Parametric Angle Constraint Solver",
            "description": f"Solved for {reference_force.name} angle with {parametric_force.name} at relative angle",
            "results": [
                f"{reference_force.name} angle = {math.degrees(phi):.2f}°",
                f"{parametric_force.name} angle = {math.degrees(param_angle):.2f}°",
                f"{independent_force.name} magnitude = {M_indep_si/ref_unit.si_factor if ref_unit else M_indep_si:.2f} {ref_unit.symbol if ref_unit else 'N'}"
            ]
        })

    def _solve_parametric_composition(
        self,
        reference_force: ForceVector,
        parametric_force: ForceVector,
        independent_force: ForceVector,
        angle_offset: float,
        resultant: ForceVector,  # noqa: ARG002
    ) -> None:
        """
        Solve Pattern B: F_indep (known) = F_ref (unknown) + F_param (parametric).

        This handles cases where two forces combine to produce a known resultant,
        and one force has a parametric angle constraint relative to the other.

        Example: Problem 2-19
        - F_R (independent, known) = F_AB (reference, unknown) + F_AC (parametric)
        - F_AC angle = F_AB angle - 40°

        Given:
        - F_indep: magnitude R, angle θ_R (both known)
        - F_param: magnitude M_param, angle = θ_ref + angle_offset (parametric)
        - F_ref: magnitude M_ref, angle θ_ref (both unknown)

        Equilibrium: F_ref + F_param = F_indep

        In components:
        - M_ref * cos(θ_ref) + M_param * cos(θ_ref + angle_offset) = R * cos(θ_R)
        - M_ref * sin(θ_ref) + M_param * sin(θ_ref + angle_offset) = R * sin(θ_R)

        Expanding the parametric force using angle addition formulas:
        - M_ref * cos(θ_ref) + M_param * [cos(θ_ref)cos(angle_offset) - sin(θ_ref)sin(angle_offset)] = R * cos(θ_R)
        - M_ref * sin(θ_ref) + M_param * [sin(θ_ref)cos(angle_offset) + cos(θ_ref)sin(angle_offset)] = R * sin(θ_R)

        Rearranging:
        - [M_ref + M_param*cos(angle_offset)] * cos(θ_ref) - M_param*sin(angle_offset) * sin(θ_ref) = R * cos(θ_R)
        - [M_ref + M_param*cos(angle_offset)] * sin(θ_ref) + M_param*sin(angle_offset) * cos(θ_ref) = R * sin(θ_R)

        Let A = M_ref + M_param*cos(angle_offset) and B = M_param*sin(angle_offset):
        - A * cos(θ_ref) - B * sin(θ_ref) = R * cos(θ_R)
        - A * sin(θ_ref) + B * cos(θ_ref) = R * sin(θ_R)

        We can solve for A and B using the component equations, then solve for M_ref and θ_ref.
        """
        import math

        # Validate inputs
        if parametric_force.magnitude is None or parametric_force.magnitude.value is None:
            raise ValueError(f"{parametric_force.name} must have known magnitude for composition solver")
        if independent_force.magnitude is None or independent_force.magnitude.value is None:
            raise ValueError(f"{independent_force.name} must have known magnitude for composition solver")
        if independent_force.angle is None or independent_force.angle.value is None:
            raise ValueError(f"{independent_force.name} must have known angle for composition solver")

        # Get known values - all in SI units
        M_param_si = parametric_force.magnitude.value
        R_si = independent_force.magnitude.value
        theta_R = independent_force.angle.value  # radians

        # Reference unit for display
        ref_unit = parametric_force.magnitude.preferred

        # Components of independent (resultant) force
        # In equilibrium: F_ref + F_param + F_indep = 0
        # So: F_ref + F_param = -F_indep
        # We need to use -F_indep as the target
        R_x = -R_si * math.cos(theta_R)
        R_y = -R_si * math.sin(theta_R)

        # Equilibrium: F_ref + F_param = F_indep
        # Let θ_ref be the unknown angle of reference force
        # Then θ_param = θ_ref + angle_offset
        #
        # Components:
        # M_ref * cos(θ_ref) + M_param * cos(θ_ref + angle_offset) = R_x
        # M_ref * sin(θ_ref) + M_param * sin(θ_ref + angle_offset) = R_y
        #
        # Expand using angle addition:
        # M_ref * cos(θ_ref) + M_param * [cos(θ_ref)*cos(Δ) - sin(θ_ref)*sin(Δ)] = R_x
        # M_ref * sin(θ_ref) + M_param * [sin(θ_ref)*cos(Δ) + cos(θ_ref)*sin(Δ)] = R_y
        #
        # where Δ = angle_offset
        #
        # Rearrange:
        # [M_ref + M_param*cos(Δ)] * cos(θ_ref) - M_param*sin(Δ) * sin(θ_ref) = R_x
        # [M_ref + M_param*cos(Δ)] * sin(θ_ref) + M_param*sin(Δ) * cos(θ_ref) = R_y
        #
        # This is a system of the form:
        # A * cos(θ_ref) - B * sin(θ_ref) = R_x
        # A * sin(θ_ref) + B * cos(θ_ref) = R_y
        #
        # where A and B involve M_ref (the unknown magnitude)
        # However, we can use a different approach.
        #
        # From the two equations, we can derive:
        # Square both equations and add:
        # [M_ref + M_param*cos(Δ)]² + [M_param*sin(Δ)]² = R_x² + R_y²
        # M_ref² + 2*M_ref*M_param*cos(Δ) + M_param²*cos²(Δ) + M_param²*sin²(Δ) = R²
        # M_ref² + 2*M_ref*M_param*cos(Δ) + M_param² = R²
        #
        # This is a quadratic in M_ref:
        # M_ref² + 2*M_param*cos(Δ)*M_ref + (M_param² - R²) = 0

        cos_delta = math.cos(angle_offset)

        # Quadratic: a*M_ref² + b*M_ref + c = 0
        a = 1.0
        b = 2.0 * M_param_si * cos_delta
        c = M_param_si**2 - R_si**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            raise ValueError("No solution exists for composition problem (discriminant < 0)")

        # Two solutions for M_ref
        M_ref_1 = (-b + math.sqrt(discriminant)) / (2*a)
        M_ref_2 = (-b - math.sqrt(discriminant)) / (2*a)

        # Choose the solution with larger absolute value
        # The magnitude can be negative, representing force direction
        # We'll use the solution with larger absolute value as it's typically the physical one
        if abs(M_ref_1) > abs(M_ref_2):
            M_ref_si = M_ref_1
        else:
            M_ref_si = M_ref_2

        # Track if magnitude is negative for angle adjustment
        magnitude_is_negative = M_ref_si < 0

        # Now solve for θ_ref using the component equations
        # We have: M_ref * cos(θ_ref) + M_param * cos(θ_ref + Δ) = R_x
        #          M_ref * sin(θ_ref) + M_param * sin(θ_ref + Δ) = R_y
        #
        # Rearranging:
        # M_ref * cos(θ_ref) = R_x - M_param * cos(θ_ref + Δ)
        # M_ref * sin(θ_ref) = R_y - M_param * sin(θ_ref + Δ)
        #
        # But θ_ref appears on both sides. Use a different approach:
        # From the expanded form:
        # [M_ref + M_param*cos(Δ)] * cos(θ_ref) - M_param*sin(Δ) * sin(θ_ref) = R_x
        # [M_ref + M_param*cos(Δ)] * sin(θ_ref) + M_param*sin(Δ) * cos(θ_ref) = R_y
        #
        # Let A = M_ref + M_param*cos(Δ) and B = M_param*sin(Δ)
        A = M_ref_si + M_param_si * cos_delta
        B = M_param_si * math.sin(angle_offset)

        # Now we have:
        # A * cos(θ_ref) - B * sin(θ_ref) = R_x
        # A * sin(θ_ref) + B * cos(θ_ref) = R_y
        #
        # This can be rewritten as:
        # sqrt(A²+B²) * cos(θ_ref + φ) = R_x  (where φ = atan2(B, A))
        # sqrt(A²+B²) * sin(θ_ref + φ) = R_y
        #
        # So: θ_ref + φ = atan2(R_y, R_x)
        #     θ_ref = atan2(R_y, R_x) - φ = atan2(R_y, R_x) - atan2(B, A)
        #
        # Or more directly:
        # From A * cos(θ_ref) - B * sin(θ_ref) = R_x
        #      A * sin(θ_ref) + B * cos(θ_ref) = R_y
        #
        # Multiply first by A, second by B:
        # A² * cos(θ_ref) - A*B * sin(θ_ref) = A*R_x
        # A*B * sin(θ_ref) + B² * cos(θ_ref) = B*R_y
        # Adding: (A² + B²) * cos(θ_ref) = A*R_x + B*R_y
        #
        # Multiply first by B, second by A:
        # A*B * cos(θ_ref) - B² * sin(θ_ref) = B*R_x
        # A² * sin(θ_ref) + A*B * cos(θ_ref) = A*R_y
        # Subtracting first from second: (A² + B²) * sin(θ_ref) = A*R_y - B*R_x

        cos_theta_ref = (A * R_x + B * R_y) / (A**2 + B**2)
        sin_theta_ref = (A * R_y - B * R_x) / (A**2 + B**2)
        theta_ref = math.atan2(sin_theta_ref, cos_theta_ref)

        # If magnitude is negative, adjust angle by 180° to represent the force correctly
        # A negative magnitude at angle θ is equivalent to positive magnitude at angle θ+180°
        # So to keep the negative magnitude, we need to subtract 180° from the computed angle
        if magnitude_is_negative:
            theta_ref = theta_ref - math.pi

        # Calculate parametric force angle
        theta_param = theta_ref + angle_offset

        # Update forces
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)

        # Update reference force
        reference_force._magnitude = Quantity(name=f"{reference_force.name}_magnitude", dim=dim.force, value=M_ref_si, preferred=ref_unit)
        reference_force._angle = Quantity(name=f"{reference_force.name}_angle", dim=dim.D, value=theta_ref, preferred=degree_unit)
        ref_x = M_ref_si * math.cos(theta_ref)
        ref_y = M_ref_si * math.sin(theta_ref)
        ref_x_qty = Quantity(name=f"{reference_force.name}_x", dim=dim.force, value=ref_x, preferred=ref_unit)
        ref_y_qty = Quantity(name=f"{reference_force.name}_y", dim=dim.force, value=ref_y, preferred=ref_unit)
        ref_z_qty = Quantity(name=f"{reference_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        reference_force._coords = Vector.from_quantities(ref_x_qty, ref_y_qty, ref_z_qty)._coords
        reference_force.is_known = True

        # Update parametric force
        parametric_force._angle = Quantity(name=f"{parametric_force.name}_angle", dim=dim.D, value=theta_param, preferred=degree_unit)
        param_x = M_param_si * math.cos(theta_param)
        param_y = M_param_si * math.sin(theta_param)
        param_x_qty = Quantity(name=f"{parametric_force.name}_x", dim=dim.force, value=param_x, preferred=ref_unit)
        param_y_qty = Quantity(name=f"{parametric_force.name}_y", dim=dim.force, value=param_y, preferred=ref_unit)
        param_z_qty = Quantity(name=f"{parametric_force.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        parametric_force._coords = Vector.from_quantities(param_x_qty, param_y_qty, param_z_qty)._coords
        parametric_force.is_known = True
        parametric_force._relative_to_force = None
        parametric_force._relative_angle = None

        self.solution_steps.append({
            "method": "Parametric Composition Solver",
            "description": f"Solved for {reference_force.name} magnitude and angle with {parametric_force.name} at relative angle",
            "results": [
                f"{reference_force.name} magnitude = {M_ref_si/ref_unit.si_factor if ref_unit else M_ref_si:.2f} {ref_unit.symbol if ref_unit else 'N'}",
                f"{reference_force.name} angle = {math.degrees(theta_ref):.2f}°",
                f"{parametric_force.name} angle = {math.degrees(theta_param):.2f}°",
            ]
        })

    def _solve_angle_between_forces(self, all_forces: list[ForceVector], resultant_forces: list[ForceVector]) -> None:
        """
        Solve for the angle between two forces given all three magnitudes.

        This handles problems like 2-23 where:
        - F₁, F₂, and F_R magnitudes are all known
        - No angles are specified
        - Goal: Find the angle θ between F₁ and F₂

        Uses the Law of Cosines in the force triangle:
        F_R² = F₁² + F₂² - 2·F₁·F₂·cos(180° - θ)

        Since cos(180° - θ) = -cos(θ), this becomes:
        F_R² = F₁² + F₂² + 2·F₁·F₂·cos(θ)

        Solving for θ:
        cos(θ) = (F_R² - F₁² - F₂²) / (2·F₁·F₂)
        θ = arccos(cos(θ))
        """
        import math
        import numpy as np

        self.solution_steps.append({
            "method": "Law of Cosines (Angle Between Forces)",
            "description": "Finding angle between forces given all magnitudes"
        })

        # Identify resultant and component forces
        if len(resultant_forces) != 1:
            raise ValueError("Angle-between solver requires exactly one resultant force")

        resultant = resultant_forces[0]
        component_forces = [f for f in all_forces if not f.is_resultant]

        if len(component_forces) != 2:
            raise ValueError(f"Angle-between solver requires exactly two component forces, got {len(component_forces)}")

        F1 = component_forces[0]
        F2 = component_forces[1]

        # Get magnitudes - all must be known
        if F1.magnitude is None or F1.magnitude.value is None:
            raise ValueError(f"{F1.name} magnitude must be known")
        if F2.magnitude is None or F2.magnitude.value is None:
            raise ValueError(f"{F2.name} magnitude must be known")
        if resultant.magnitude is None or resultant.magnitude.value is None:
            raise ValueError(f"{resultant.name} magnitude must be known")

        M1 = F1.magnitude.value  # SI units
        M2 = F2.magnitude.value  # SI units
        MR = resultant.magnitude.value  # SI units

        # Apply Law of Cosines to find angle between F1 and F2
        # In the parallelogram law, the resultant forms a triangle with F1 and F2
        # Using the triangle rule: F_R = F1 + F2
        # The angle between F1 and F2 in the parallelogram is θ
        # In the triangle formed by placing F2 at the tip of F1, the interior angle is (180° - θ)
        #
        # Law of Cosines: F_R² = F1² + F2² - 2·F1·F2·cos(180° - θ)
        # Since cos(180° - θ) = -cos(θ):
        # F_R² = F1² + F2² + 2·F1·F2·cos(θ)
        #
        # Solving for cos(θ):
        cos_theta = (MR**2 - M1**2 - M2**2) / (2 * M1 * M2)

        # Clamp to [-1, 1] to handle numerical errors
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        # Calculate angle
        theta_rad = math.acos(cos_theta)
        theta_deg = math.degrees(theta_rad)

        # Get unit symbols
        force_unit = F1.magnitude.preferred.symbol if F1.magnitude.preferred else "N"

        # Add solution step
        self.solution_steps.append({
            "target": "θ (angle between forces)",
            "method": "Law of Cosines",
            "equation": f"{resultant.name}² = {F1.name}² + {F2.name}² - 2·{F1.name}·{F2.name}·cos(180° - θ)",
            "substitution": f"({MR:.0f})² = ({M1:.0f})² + ({M2:.0f})² - 2·({M1:.0f})·({M2:.0f})·cos(180° - θ)",
            "result_value": f"{theta_deg:.1f}",
            "result_unit": "°",
            "details": f"cos(180° - θ) = {-cos_theta:.4f}, therefore θ = {theta_deg:.1f}°"
        })

        # Now assign actual directions to the forces
        # Convention for angle-between problems:
        # - Place F_R (resultant) along the +x axis (most natural reference)
        # - Determine F1 and F2 angles such that they sum to F_R with angle θ between them
        #
        # Using the parallelogram law and law of sines, we can find the angles
        # that F1 and F2 make with the resultant.

        # First, use law of sines to find angle α (angle between F_R and F1)
        # In the force triangle: sin(α)/M2 = sin(180° - θ)/MR
        # Since sin(180° - θ) = sin(θ):
        sin_alpha = M2 * math.sin(theta_rad) / MR
        # Clamp to handle numerical errors
        sin_alpha = np.clip(sin_alpha, -1.0, 1.0)
        alpha = math.asin(sin_alpha)  # Angle between F_R and F1

        # The angle β (between F_R and F2) can be found from the triangle:
        # α + β + (180° - θ) = 180°
        # Therefore: β = θ - α
        beta = theta_rad - alpha  # Angle between F_R and F2

        # Place F_R along +x axis
        theta_R = 0.0  # radians

        # F1 is at angle α from F_R (measured CCW from +x)
        theta1 = alpha

        # F2 is at angle -β from F_R (measured CW from +x, which is negative CCW)
        theta2 = -beta

        # Calculate force components
        F1x = M1 * math.cos(theta1)
        F1y = M1 * math.sin(theta1)
        F2x = M2 * math.cos(theta2)
        F2y = M2 * math.sin(theta2)
        FRx = F1x + F2x
        FRy = F1y + F2y

        # Create force vectors with assigned directions
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        degree_unit = ureg.resolve("degree", dim=dim.D)
        ref_unit = F1.magnitude.preferred

        # Update F1
        F1._angle = Quantity(name=f"{F1.name}_angle", dim=dim.D, value=theta1, preferred=degree_unit)
        x1_qty = Quantity(name=f"{F1.name}_x", dim=dim.force, value=F1x, preferred=ref_unit)
        y1_qty = Quantity(name=f"{F1.name}_y", dim=dim.force, value=F1y, preferred=ref_unit)
        z1_qty = Quantity(name=f"{F1.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        F1._coords = Vector.from_quantities(x1_qty, y1_qty, z1_qty)._coords
        F1.is_known = True

        # Update F2
        F2._angle = Quantity(name=f"{F2.name}_angle", dim=dim.D, value=theta2, preferred=degree_unit)
        x2_qty = Quantity(name=f"{F2.name}_x", dim=dim.force, value=F2x, preferred=ref_unit)
        y2_qty = Quantity(name=f"{F2.name}_y", dim=dim.force, value=F2y, preferred=ref_unit)
        z2_qty = Quantity(name=f"{F2.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        F2._coords = Vector.from_quantities(x2_qty, y2_qty, z2_qty)._coords
        F2.is_known = True

        # Update resultant
        resultant._angle = Quantity(name=f"{resultant.name}_angle", dim=dim.D, value=theta_R, preferred=degree_unit)
        xR_qty = Quantity(name=f"{resultant.name}_x", dim=dim.force, value=FRx, preferred=ref_unit)
        yR_qty = Quantity(name=f"{resultant.name}_y", dim=dim.force, value=FRy, preferred=ref_unit)
        zR_qty = Quantity(name=f"{resultant.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        resultant._coords = Vector.from_quantities(xR_qty, yR_qty, zR_qty)._coords
        resultant.is_known = True

        self.logger.info(f"Solved angle between {F1.name} and {F2.name}: θ = {theta_deg:.1f}°")

    def _solve_by_components(self, known_forces: list[ForceVector], unknown_force: ForceVector) -> None:
        """
        Solve using component summation (ΣFx = 0, ΣFy = 0).

        This assumes equilibrium: unknown force balances known forces.
        """
        self.solution_steps.append({"method": "Component Summation (Equilibrium)", "description": "ΣFx = 0, ΣFy = 0"})

        # Sum known force components
        sum_x = 0.0
        sum_y = 0.0
        sum_z = 0.0
        ref_unit = None

        for force in known_forces:
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

        unknown_vector = Vector.from_quantities(x_qty, y_qty, z_qty)

        # Update unknown force
        unknown_force.copy_coords_from(unknown_vector)
        unknown_force._compute_magnitude_and_angle()
        unknown_force.is_known = True

    def generate_report_content(self) -> dict[str, Any]:
        """
        Generate report content for vector equilibrium problem.

        Returns:
            Dictionary with report sections
        """
        content = {"title": self.name, "description": self.description, "problem_type": "Vector Equilibrium (Statics)", "given": [], "find": [], "solution_steps": self.solution_steps, "results": []}

        # List given forces
        for name, force in self.forces.items():
            if force.is_known and not force.is_resultant and force.magnitude is not None and force.angle is not None:
                if force.magnitude.value is not None and force.angle.value is not None:
                    mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                    ang_val = force.angle.value * 180 / math.pi
                    mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""

                    content["given"].append(f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°")

        # List unknowns
        for name, force in self.forces.items():
            if not force.is_known or (force.is_resultant and not self.is_solved):
                content["find"].append(f"{name}: {force.description or 'magnitude and direction'}")

        # List results
        if self.is_solved:
            for name, force in self.forces.items():
                if force.is_resultant or (not force.is_known):
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
