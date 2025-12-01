"""
RectangularVectorProblem class for solving 2D/3D force equilibrium using the component method.

Uses the rectangular component method (also known as Cartesian vector method or scalar notation)
for solving force equilibrium problems. This is the standard method taught in engineering mechanics.
"""

from __future__ import annotations

import math
from typing import Any

from ..core.quantity import Quantity
from ..solving.component_solver import ComponentSolver
from ..spatial import _Vector
from ..utils.shared_utilities import (
    VariableStateTrackingMixin,
    add_force_components_xy,
    capture_original_force_states,
    clone_force_vector,
    extract_force_vectors_from_class,
)
from .problem import Problem


class RectangularVectorProblem(VariableStateTrackingMixin, Problem):
    """
    Specialized Problem for 2D/3D vector equilibrium using the rectangular component method.

    This class uses the Cartesian/Component method (also known as scalar notation)
    to solve force equilibrium problems. This is the standard method taught in
    engineering mechanics for problems with multiple forces.

    Method:
    1. Resolve each force into components: Fx, Fy, (Fz)
    2. Sum components algebraically: ΣFx, ΣFy, (ΣFz)
    3. For equilibrium: ΣFx = 0, ΣFy = 0, (ΣFz = 0)
    4. For resultant: FR = √(ΣFx² + ΣFy² + ΣFz²)
    5. Direction: θ = tan⁻¹(ΣFy/ΣFx) or direction cosines

    This method is preferred over geometric/trigonometric methods when:
    - More than 3 forces are present
    - Forces are given in component form
    - 3D problems (z-component)

    Examples:
        >>> # Define problem with class inheritance
        >>> class GussetPlateProblem(RectangularVectorProblem):
        ...     F_1 = ForceVector(magnitude=200, angle=-45, unit="N", wrt="+y", name="F_1")
        ...     F_2 = ForceVector(magnitude=-150, angle=-30, unit="N", wrt="+x", name="F_2")
        ...     F_R = ForceVector.unknown("F_R", is_resultant=True)
        ...
        >>> problem = GussetPlateProblem()
        >>> solution = problem.solve()

        >>> # Or programmatically
        >>> problem = RectangularVectorProblem("Gusset Plate Forces")
        >>> problem.add_force(ForceVector(magnitude=200, angle=-45, unit="N", wrt="+y", name="F_1"))
        >>> problem.add_force(ForceVector(magnitude=-150, angle=-30, unit="N", wrt="+x", name="F_2"))
        >>> problem.add_force(ForceVector.unknown("F_R", is_resultant=True))
        >>> solution = problem.solve()
    """

    def __init__(self, name: str | None = None, description: str = ""):
        """
        Initialize RectangularVectorProblem.

        Args:
            name: Problem name
            description: Problem description
        """
        super().__init__(name=name, description=description)
        self.forces: dict[str, _Vector] = {}
        self.solution_steps: list[dict[str, Any]] = []
        self._original_variable_states: dict[str, bool] = {}  # Track which variables were originally known
        self._original_force_states: dict[str, bool] = {}  # Track original is_known state of each force
        self.solver = ComponentSolver()  # Create component solver instance

        # Extract ForceVector class attributes
        self._extract_force_vectors()

    def _extract_force_vectors(self) -> None:
        """Extract ForceVector objects defined at class level."""
        extract_force_vectors_from_class(self.__class__, self, self.forces, self._clone_force_vector)

    def _clone_force_vector(self, force: _Vector) -> _Vector:
        """Create a copy of a ForceVector."""
        return clone_force_vector(force, _Vector)

    def solve(self, max_iterations: int = 100, tolerance: float = 1e-10) -> dict[str, _Vector]:  # type: ignore[override]
        """
        Solve the vector equilibrium problem using the rectangular component method.

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
            capture_original_force_states(self.forces, self._original_force_states, self._original_variable_states)

        # Convert forces dict to list for solver
        forces_list = list(self.forces.values())

        # Solve using ComponentSolver
        solved_forces_dict = self.solver.solve(forces_list)

        # Update our forces dict with solved values
        self.forces.update(solved_forces_dict)

        # Get solution steps from solver
        self.solution_steps = self.solver.get_solution_steps()

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
        from ..utils.shared_utilities import add_force_magnitude_variable

        for force_name, force in self.forces.items():
            # Determine if this was originally known or unknown
            was_originally_known = self._original_force_states.get(force_name, force.is_known)

            add_force_magnitude_variable(force, force_name, was_originally_known, self.variables, self._original_variable_states)

            if force.angle is not None and force.angle.value is not None:
                # Add angle as a variable
                angle_var = Quantity(
                    name=f"{force.name} Direction",
                    dim=dim.D,
                    value=force.angle.value,
                    preferred=force.angle.preferred,
                    _symbol=f"{force_name}_angle"
                )
                self.variables[f"{force_name}_angle"] = angle_var

                # Store original state
                self._original_variable_states[f"{force_name}_angle"] = was_originally_known

            # Add 2D components (X, Y) using shared utility
            add_force_components_xy(force, force_name, self.variables)

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
                "method": step.get("method", "component"),
                "description": step.get("description", ""),
                "equation_str": step.get("equation", ""),
                "substituted": step.get("substitution", ""),
                "result_value": step.get("result_value", ""),
                "result_unit": step.get("result_unit", ""),
                "details": step.get("description", ""),
            }
            self.solving_history.append(history_entry)

    def generate_report_content(self) -> dict[str, Any]:
        """
        Generate report content for rectangular component method problem.

        Returns:
            Dictionary with report sections
        """
        content = {
            "title": self.name,
            "description": self.description,
            "problem_type": "Vector Equilibrium (Rectangular Component Method)",
            "given": [],
            "find": [],
            "solution_steps": self.solution_steps,
            "results": []
        }

        # List given forces
        for name, force in self.forces.items():
            if self._original_force_states.get(name, False) and not force.is_resultant:
                if force.magnitude is not None and force.angle is not None:
                    if force.magnitude.value is not None and force.angle.value is not None:
                        mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                        ang_val = force.angle.value * 180 / math.pi
                        mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""

                        content["given"].append(f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°")

        # List unknowns
        for name, force in self.forces.items():
            if not self._original_force_states.get(name, False) or (force.is_resultant and not self.is_solved):
                content["find"].append(f"{name}: {force.description or 'magnitude and direction'}")

        # List results
        if self.is_solved:
            for name, force in self.forces.items():
                if force.is_resultant or not self._original_force_states.get(name, False):
                    if force.magnitude and force.angle and force.magnitude.value is not None and force.angle.value is not None:
                        mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                        ang_val = force.angle.value * 180 / math.pi
                        mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""

                        content["results"].append(f"{name} = {mag_val:.1f} {mag_unit} at {ang_val:.1f}°")

        return content

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"RectangularVectorProblem('{self.name}', forces={len(self.forces)}, {status})"
