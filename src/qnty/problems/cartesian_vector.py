"""
CartesianVectorProblem class for solving 3D force equilibrium using the Cartesian method.

Uses the 3D Cartesian vector method (scalar notation) for solving force equilibrium
problems in three dimensions. This extends the 2D rectangular component method to 3D space.
"""

from __future__ import annotations

import math
from typing import Any

from ..core.quantity import Quantity
from ..solving.component_solver import ComponentSolver
from ..spatial import _Vector
from ..utils.shared_utilities import (
    VariableStateTrackingMixin,
    add_force_components_xyz,
    capture_original_force_states,
    clone_unknown_force_vector,
    extract_force_vectors_from_class,
    handle_negative_magnitude,
)
from .problem import Problem


class CartesianVectorProblem(VariableStateTrackingMixin, Problem):
    """
    Specialized Problem for 3D vector equilibrium using the Cartesian vector method.

    This class uses the 3D Cartesian/Component method (scalar notation) to solve
    force equilibrium problems. This is the standard method for 3D statics problems.

    Method:
    1. Resolve each force into components: Fx, Fy, Fz
    2. Sum components algebraically: ΣFx, ΣFy, ΣFz
    3. For equilibrium: ΣFx = 0, ΣFy = 0, ΣFz = 0
    4. For resultant: FR = √(ΣFx² + ΣFy² + ΣFz²)
    5. Direction: Coordinate direction angles α, β, γ or direction cosines

    This method is essential for:
    - 3D force systems
    - Problems with coordinate direction angles
    - Direction cosines and unit vectors
    - Spatial force resolution

    Examples:
        >>> # Define problem with class inheritance
        >>> class SpatialForceProblem(CartesianVectorProblem):
        ...     F_1 = ForceVector(magnitude=80, alpha=60, beta=45, unit="lbf", name="F_1")
        ...     F_2 = ForceVector(x=0, y=0, z=-130, unit="lbf", name="F_2")
        ...     F_R = ForceVector.unknown("F_R", is_resultant=True)
        ...
        >>> problem = SpatialForceProblem()
        >>> solution = problem.solve()

        >>> # Or programmatically
        >>> problem = CartesianVectorProblem("Spatial Force System")
        >>> problem.add_force(ForceVector(magnitude=80, alpha=60, beta=45, unit="lbf", name="F_1"))
        >>> problem.add_force(ForceVector(x=0, y=0, z=-130, unit="lbf", name="F_2"))
        >>> problem.add_force(ForceVector.unknown("F_R", is_resultant=True))
        >>> solution = problem.solve()
    """

    def __init__(self, name: str | None = None, description: str = ""):
        """
        Initialize CartesianVectorProblem.

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
        if force.is_known and force.vector is not None:
            # Known force - copy with same values
            cloned = _Vector(
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
            original_mag = force.magnitude.value if force.magnitude is not None else None
            handle_negative_magnitude(cloned, original_mag)
            return cloned
        else:
            # Unknown force - use shared utility
            return clone_unknown_force_vector(force, _Vector)

    def solve(self, max_iterations: int = 100, tolerance: float = 1e-10) -> dict[str, _Vector]:  # type: ignore[override]
        """
        Solve the vector equilibrium problem using the 3D Cartesian vector method.

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

            # Add 3D components (X, Y, Z) using shared utility
            add_force_components_xyz(force, force_name, self.variables)

            # Add direction angles if available
            if hasattr(force, 'alpha') and force.alpha is not None and force.alpha.value is not None:
                alpha_var = Quantity(
                    name=f"{force.name} Alpha (α)",
                    dim=dim.D,
                    value=force.alpha.value,
                    preferred=force.alpha.preferred,
                    _symbol=f"{force_name}_alpha"
                )
                self.variables[f"{force_name}_alpha"] = alpha_var

            if hasattr(force, 'beta') and force.beta is not None and force.beta.value is not None:
                beta_var = Quantity(
                    name=f"{force.name} Beta (β)",
                    dim=dim.D,
                    value=force.beta.value,
                    preferred=force.beta.preferred,
                    _symbol=f"{force_name}_beta"
                )
                self.variables[f"{force_name}_beta"] = beta_var

            if hasattr(force, 'gamma') and force.gamma is not None and force.gamma.value is not None:
                gamma_var = Quantity(
                    name=f"{force.name} Gamma (γ)",
                    dim=dim.D,
                    value=force.gamma.value,
                    preferred=force.gamma.preferred,
                    _symbol=f"{force_name}_gamma"
                )
                self.variables[f"{force_name}_gamma"] = gamma_var

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
                "method": step.get("method", "cartesian_3d"),
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
        Generate report content for 3D Cartesian vector method problem.

        Returns:
            Dictionary with report sections
        """
        content = {
            "title": self.name,
            "description": self.description,
            "problem_type": "Vector Equilibrium (3D Cartesian Method)",
            "given": [],
            "find": [],
            "solution_steps": self.solution_steps,
            "results": []
        }

        # List given forces
        for name, force in self.forces.items():
            if self._original_force_states.get(name, False) and not force.is_resultant:
                if force.magnitude is not None:
                    if force.magnitude.value is not None:
                        mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                        mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""

                        # For 3D forces, include direction angles if available
                        if hasattr(force, 'alpha') and force.alpha and force.alpha.value is not None:
                            alpha_deg = force.alpha.value * 180 / math.pi
                            beta_deg = (force.beta.value * 180 / math.pi) if (force.beta and force.beta.value is not None) else 0
                            gamma_deg = (force.gamma.value * 180 / math.pi) if (force.gamma and force.gamma.value is not None) else 0
                            given_list: list[str] = content["given"]  # type: ignore[assignment]
                            given_list.append(f"{name} = {mag_val:.1f} {mag_unit} (α={alpha_deg:.1f}°, β={beta_deg:.1f}°, γ={gamma_deg:.1f}°)")
                        else:
                            given_list_simple: list[str] = content["given"]  # type: ignore[assignment]
                            given_list_simple.append(f"{name} = {mag_val:.1f} {mag_unit}")

        # List unknowns
        find_list: list[str] = content["find"]  # type: ignore[assignment]
        for name, force in self.forces.items():
            if not self._original_force_states.get(name, False) or (force.is_resultant and not self.is_solved):
                find_list.append(f"{name}: {force.description or 'magnitude and direction'}")

        # List results
        if self.is_solved:
            results_list: list[str] = content["results"]  # type: ignore[assignment]
            for name, force in self.forces.items():
                if force.is_resultant or not self._original_force_states.get(name, False):
                    if force.magnitude and force.magnitude.value is not None:
                        mag_val = force.magnitude.value / force.magnitude.preferred.si_factor if force.magnitude.preferred else force.magnitude.value
                        mag_unit = force.magnitude.preferred.symbol if force.magnitude.preferred else ""

                        # Include direction angles for 3D forces
                        if hasattr(force, 'alpha') and force.alpha and force.alpha.value is not None:
                            alpha_deg = force.alpha.value * 180 / math.pi
                            beta_deg = (force.beta.value * 180 / math.pi) if (force.beta and force.beta.value is not None) else 0
                            gamma_deg = (force.gamma.value * 180 / math.pi) if (force.gamma and force.gamma.value is not None) else 0
                            results_list.append(f"{name} = {mag_val:.1f} {mag_unit} (α={alpha_deg:.1f}°, β={beta_deg:.1f}°, γ={gamma_deg:.1f}°)")
                        else:
                            results_list.append(f"{name} = {mag_val:.1f} {mag_unit}")

        return content

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"CartesianVectorProblem('{self.name}', forces={len(self.forces)}, {status})"
