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
from ..solving.trig_solver import TrigSolver
from ..spatial.force_vector import ForceVector
from ..spatial.vector import Vector
from .problem import Problem


class VectorEquilibriumProblem(Problem):
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
        self.solver = TrigSolver()  # Create trig solver instance

        # Extract ForceVector class attributes
        self._extract_force_vectors()

    def _extract_force_vectors(self) -> None:
        """Extract ForceVector objects defined at class level."""
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, ForceVector):
                # Clone to avoid sharing between instances
                force_copy = self._clone_force_vector(attr)
                self.forces[attr_name] = force_copy
                setattr(self, attr_name, force_copy)

    def _clone_force_vector(self, force: ForceVector) -> ForceVector:
        """Create a copy of a ForceVector."""
        if force.is_known and force.vector is not None:
            # Known force - copy with same values
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
                is_known=False,  # Cloning an unknown force
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

        # Analyze problem type
        known_forces = [f for f in self.forces.values() if f.is_known]
        unknown_forces = [f for f in self.forces.values() if not f.is_known]
        resultant_forces = [f for f in self.forces.values() if f.is_resultant]

        # Count actual unknowns (magnitudes and angles separately)
        total_unknowns = 0
        partially_known_forces = []
        fully_unknown_forces = []

        for force in unknown_forces:
            mag_unknown = force.magnitude is None or force.magnitude.value is None
            angle_unknown = force.angle is None or force.angle.value is None

            # If angle is unknown due to parametric constraint, don't count it as unknown
            # It will be determined by solving for the reference force's angle
            if angle_unknown and force._relative_to_force is not None:
                angle_unknown = False  # Parametric, not truly unknown

            if mag_unknown and angle_unknown:
                fully_unknown_forces.append(force)
                total_unknowns += 2  # Both magnitude and angle unknown
            elif mag_unknown or angle_unknown:
                partially_known_forces.append(force)
                total_unknowns += 1  # Either magnitude or angle unknown
            # else: both known (or parametric), no unknowns to count

        self.logger.info(f"Solving {self.name}: {len(known_forces)} known, {len(unknown_forces)} unknown ({total_unknowns} total unknowns)")

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
                    # Both have known angles but unknown magnitudes
                    # Check if both angles are known
                    all_angles_known = all(f.angle is not None and f.angle.value is not None for f in partially_known_forces)
                    if all_angles_known:
                        # Can solve using component equations (works whether resultant is fully known or not)
                        self._solve_two_unknowns_with_resultant(known_forces, unknown_forces, resultant_forces[0])
                    else:
                        raise ValueError("Cannot solve: two unknowns require known angles or complementary partial knowledge")
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
            resultant._vector = resultant_vector
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
            if resultant in known_forces:
                # Find the other known force (not the resultant)
                other_known = [f for f in known_forces if f != resultant][0]
                # Solve: F_unknown = F_resultant - F_other_known
                self._solve_unknown_from_resultant_and_known(unknown_force, resultant, other_known)
                return

        if len(known_forces) == 2 and len(resultant_forces) == 1:
            # Two known forces, unknown resultant
            self._solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) == 2 and unknown_force.is_resultant:
            # Two known forces, solve for resultant
            self._solve_resultant_from_two_forces(known_forces[0], known_forces[1], unknown_force)
        elif len(known_forces) >= 2 and not unknown_force.is_resultant:
            # Multiple known forces and unknown resultant - find equilibrium force
            # First compute resultant of known forces
            self._solve_resultant(known_forces)
            # The unknown force must balance this resultant
            resultant = self.forces.get("FR")
            if resultant and resultant.vector:
                # Unknown force is negative of resultant
                unknown_vector = -resultant.vector
                unknown_force._vector = unknown_vector
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
        unknown_force._vector = unknown_vector
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
        resultant._vector = resultant_vector
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

        This uses the TrigSolver to solve decomposition problems where the resultant
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
        force_with_known_mag._vector = Vector.from_quantities(x_qty, y_qty, z_qty)
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
        force_with_known_angle._vector = Vector.from_quantities(x_qty_r, y_qty_r, z_qty_r)
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
        component_force._vector = Vector.from_quantities(comp_x_qty, comp_y_qty, comp_z_qty)
        component_force._magnitude = mag_comp_qty
        component_force._angle = angle_comp_qty
        component_force.is_known = True

        res_x = M_res * math.cos(theta_res)
        res_y = M_res * math.sin(theta_res)
        res_x_qty = Quantity(name=f"{resultant.name}_x", dim=dim.force, value=res_x, preferred=ref_unit)
        res_y_qty = Quantity(name=f"{resultant.name}_y", dim=dim.force, value=res_y, preferred=ref_unit)
        res_z_qty = Quantity(name=f"{resultant.name}_z", dim=dim.force, value=0.0, preferred=ref_unit)
        resultant._vector = Vector.from_quantities(res_x_qty, res_y_qty, res_z_qty)
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
        import math

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
            elif force is not resultant and independent_force is None:
                independent_force = force

        if parametric_force is None:
            raise ValueError("No force with parametric angle constraint found")

        if reference_force is None:
            raise ValueError("Reference force not found for parametric constraint")

        if independent_force is None:
            raise ValueError("Independent force not found for parametric constraint")

        # Validate that we have the right information
        if parametric_force.magnitude is None or parametric_force.magnitude.value is None:
            raise ValueError(f"{parametric_force.name} must have known magnitude for parametric solver")
        if independent_force.angle is None or independent_force.angle.value is None:
            raise ValueError(f"{independent_force.name} must have known angle for parametric solver")
        if reference_force.magnitude is None or reference_force.magnitude.value is None:
            raise ValueError(f"{reference_force.name} must have known magnitude for parametric solver")

        self.logger.info(f"Solving parametric constraint: {parametric_force.name} angle relative to {reference_force.name}")

        # Get the relative angle offset
        angle_offset = parametric_force._relative_angle if parametric_force._relative_angle is not None else 0.0

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
        reference_force._vector = Vector.from_quantities(ref_x_qty, ref_y_qty, ref_z_qty)
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
        parametric_force._vector = Vector.from_quantities(param_x_qty, param_y_qty, param_z_qty)
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
        independent_force._vector = Vector.from_quantities(indep_x_qty, indep_y_qty, indep_z_qty)
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
        unknown_force._vector = unknown_vector
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
