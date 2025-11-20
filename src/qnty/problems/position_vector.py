"""
PositionVectorProblem class for solving 3D position vector and force-along-line problems.

Uses position vectors to define force directions along lines between points,
then solves for forces and resultants using the component method.
"""

from __future__ import annotations

import math
from typing import Any

from ..core.quantity import Quantity
from ..solving.component_solver import ComponentSolver
from ..spatial.force_vector import ForceVector
from ..spatial.point import _Point
from ..spatial.position_vector import PositionVector
from .problem import Problem


class PositionVectorProblem(Problem):
    """
    Specialized Problem for 3D force systems defined by position vectors.

    This class handles problems where forces act along lines between points,
    using position vectors to determine force directions. Common in statics
    problems involving cables, rods, and other structural members.

    Method:
    1. Define points in 3D space
    2. Create position vectors between points
    3. Use position vectors to define force directions (unit vectors)
    4. Resolve forces into components
    5. Solve for resultant or unknown forces

    Examples:
        >>> class CableForces(PositionVectorProblem):
        ...     A = PointCartesian(x=0, y=4, z=0, unit="ft")
        ...     B = PointCartesian(x=2, z=-6, unit="ft")
        ...     F_AB = {"from": "A", "to": "B", "magnitude": 50, "unit": "lbf"}
        ...     F_R = ForceVector.unknown("F_R", is_resultant=True)
        ...
        >>> problem = CableForces()
        >>> result = problem.solve()
    """

    def __init__(self, name: str | None = None, description: str = ""):
        """
        Initialize PositionVectorProblem.

        Args:
            name: Problem name
            description: Problem description
        """
        super().__init__(name=name, description=description)
        self.points: dict[str, Any] = {}  # Point objects (various frontend types)
        self.position_vectors: dict[str, PositionVector] = {}
        self.forces: dict[str, ForceVector] = {}
        self.force_specs: dict[str, dict] = {}  # Force specifications (from/to/magnitude)
        self.solution_steps: list[dict[str, Any]] = []
        self._original_force_states: dict[str, bool] = {}
        self.solver = ComponentSolver()
        self.solved_points: dict[str, _Point] = {}  # Points solved from force vectors

        # Extract class-level attributes
        self._extract_problem_elements()

    def _extract_problem_elements(self) -> None:
        """Extract points, force specs, and ForceVectors from class attributes."""
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.__class__, attr_name)

            # Check if it's a point (has to_cartesian method or is _Point)
            if hasattr(attr, "to_cartesian") or isinstance(attr, _Point):
                self.points[attr_name] = attr
                setattr(self, attr_name, attr)

            # Check if it's a force specification dict
            elif isinstance(attr, dict) and "from" in attr and "to" in attr:
                self.force_specs[attr_name] = attr

            # Check if it's a ForceVector (e.g., resultant)
            elif isinstance(attr, ForceVector):
                force_copy = self._clone_force_vector(attr)
                self.forces[attr_name] = force_copy
                setattr(self, attr_name, force_copy)

    def _clone_force_vector(self, force: ForceVector) -> ForceVector:
        """Create a copy of a ForceVector."""
        if force.is_known and force.vector is not None:
            cloned = ForceVector(
                vector=force.vector,
                name=force.name,
                description=force.description,
                is_known=True,
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )
            return cloned
        else:
            # Unknown force
            cloned = ForceVector(
                name=force.name,
                magnitude=force.magnitude,
                unit=force.magnitude.preferred if force.magnitude else None,
                description=force.description,
                is_known=force.is_known,
                is_resultant=force.is_resultant,
                coordinate_system=force.coordinate_system,
                angle_reference=force.angle_reference,
            )
            return cloned

    def add_point(self, name: str, point: Any) -> None:
        """Add a point to the problem."""
        self.points[name] = point
        setattr(self, name, point)

    def add_force_along_line(
        self,
        name: str,
        from_point: str,
        to_point: str,
        magnitude: float,
        unit: str,
    ) -> None:
        """
        Add a force acting along a line between two points.

        Args:
            name: Force name
            from_point: Name of starting point
            to_point: Name of ending point
            magnitude: Force magnitude
            unit: Force unit (e.g., "lbf", "N")
        """
        self.force_specs[name] = {
            "from": from_point,
            "to": to_point,
            "magnitude": magnitude,
            "unit": unit,
        }

    def add_resultant(self, name: str = "F_R", unit: str | None = None) -> None:
        """Add an unknown resultant force."""
        resultant = ForceVector.unknown(name=name, unit=unit, is_resultant=True)
        self.forces[name] = resultant

    def _create_position_vectors(self) -> None:
        """Create position vectors from force specifications."""
        for force_name, spec in self.force_specs.items():
            from_name = spec["from"]
            to_name = spec["to"]

            if from_name not in self.points:
                raise ValueError(f"Point '{from_name}' not found for force '{force_name}'")
            if to_name not in self.points:
                raise ValueError(f"Point '{to_name}' not found for force '{force_name}'")

            from_point = self.points[from_name]
            to_point = self.points[to_name]

            # Convert to _Point if needed
            if hasattr(from_point, "to_cartesian"):
                from_point = from_point.to_cartesian()
            if hasattr(to_point, "to_cartesian"):
                to_point = to_point.to_cartesian()

            # Create position vector
            pv_name = f"r_{from_name}{to_name}"
            r = PositionVector.from_points(from_point, to_point, name=pv_name)
            self.position_vectors[pv_name] = r

    def _create_forces_from_specs(self) -> None:
        """Create ForceVector objects from force specifications using position vectors."""
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        for force_name, spec in self.force_specs.items():
            from_name = spec["from"]
            to_name = spec["to"]
            magnitude = spec["magnitude"]
            unit_str = spec["unit"]

            # Get the corresponding position vector
            pv_name = f"r_{from_name}{to_name}"
            r = self.position_vectors[pv_name]

            # Get unit vector (direction cosines)
            cos_alpha, cos_beta, cos_gamma = r.unit_vector()

            # Resolve force unit
            force_unit = ureg.resolve(unit_str, dim=dim.force)

            # Compute force components: F = |F| * u_hat
            # Components are in SI units internally
            mag_si = magnitude * force_unit.si_factor
            fx = mag_si * cos_alpha
            fy = mag_si * cos_beta
            fz = mag_si * cos_gamma

            # Create Quantity objects for components
            x_qty = Quantity(name=f"{force_name}_x", dim=dim.force, value=fx, preferred=force_unit)
            y_qty = Quantity(name=f"{force_name}_y", dim=dim.force, value=fy, preferred=force_unit)
            z_qty = Quantity(name=f"{force_name}_z", dim=dim.force, value=fz, preferred=force_unit)

            # Create ForceVector from components
            F = ForceVector(
                x=x_qty,
                y=y_qty,
                z=z_qty,
                unit=force_unit,
                name=force_name,
                is_known=True,
            )
            self.forces[force_name] = F

    def _solve_unknown_points(self) -> None:
        """Solve for unknown points given force vectors and distances."""
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        import numpy as np

        # Find unknown points and their corresponding known points/forces
        for point_name, point in list(self.points.items()):
            if not (hasattr(point, 'is_unknown') and point.is_unknown):
                continue

            # Get distance from unknown point
            distance = getattr(point, '_distance', None)
            if distance is None:
                continue

            # Find a position vector spec that involves this unknown point
            # Look in force_specs for the force that connects this point
            known_point: _Point | None = None
            known_point_name: str | None = None
            force_name: str | None = None

            for fname, fspec in self.force_specs.items():
                if fspec.get("from") == point_name:
                    known_point_name = fspec.get("to")
                    force_name = fname
                    break
                elif fspec.get("to") == point_name:
                    known_point_name = fspec.get("from")
                    force_name = fname
                    break

            # Also check for direct ForceVector objects (not specs) that might be the direction
            if force_name is None:
                # Look for a force with matching direction in self.forces
                for fname, fvec in self.forces.items():
                    if fvec.is_known and fvec.vector is not None:
                        force_name = fname
                        break

            if force_name is None:
                continue

            # Get known point
            if known_point_name:
                known_point = self.points.get(known_point_name)
            else:
                # Find any known point (assume origin if only one known point)
                for pname, p in self.points.items():
                    if pname != point_name and not (hasattr(p, 'is_unknown') and p.is_unknown):
                        known_point = p
                        known_point_name = pname
                        break

            if known_point is None:
                continue

            # Get the force vector
            force = self.forces.get(force_name)
            if force is None or force.vector is None:
                continue

            # Convert known point to cartesian if needed
            if hasattr(known_point, "to_cartesian"):
                known_point = known_point.to_cartesian()  # type: ignore[union-attr]

            # Get force vector components
            if force.x is None or force.y is None or force.z is None:
                continue
            fx = force.x.value if force.x.value is not None else 0.0
            fy = force.y.value if force.y.value is not None else 0.0
            fz = force.z.value if force.z.value is not None else 0.0

            # Get force unit vector
            force_mag = math.sqrt(fx**2 + fy**2 + fz**2)
            if force_mag == 0:
                continue

            ux = fx / force_mag
            uy = fy / force_mag
            uz = fz / force_mag

            # Distance is in the same unit as the unknown point
            output_unit = point._unit
            dist_si = distance * output_unit.si_factor

            # Calculate unknown point coordinates from force direction
            # Force F acts from A to B along the cable/rod.
            # The position vector r_AB = B - A is in the same direction as F.
            # So: r_AB = |r| * u_F, where |r| = distance and u_F = F/|F|
            # Therefore: B - A = distance * u_F
            # Solving for A: A = B - distance * u_F
            kp_coords = known_point._coords  # type: ignore[union-attr]
            ax = kp_coords[0] - dist_si * ux
            ay = kp_coords[1] - dist_si * uy
            az = kp_coords[2] - dist_si * uz

            # Create solved point
            solved = object.__new__(_Point)
            solved._coords = np.array([ax, ay, az], dtype=float)
            solved._dim = dim.length
            solved._unit = output_unit
            solved._is_unknown = False
            solved._distance = None

            self.solved_points[point_name] = solved
            self.points[point_name] = solved

            # Add solution step
            coords = solved.to_array()
            self.solution_steps.append({
                "target": point_name,
                "method": "position_vector",
                "description": f"Solved for {point_name} using force {force_name} and distance {distance} {output_unit.symbol}",
                "result_value": f"({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f})",
                "result_unit": output_unit.symbol,
            })

    def solve(self, max_iterations: int = 100, tolerance: float = 1e-10) -> dict[str, ForceVector]:  # type: ignore[override]
        """
        Solve the position vector problem.

        Args:
            max_iterations: Not used (for compatibility)
            tolerance: Not used (for compatibility)

        Returns:
            Dictionary mapping force names to solved ForceVector objects
        """
        self.solution_steps = []

        # Step 0: Check for unknown points to solve
        has_unknown_points = any(
            hasattr(p, 'is_unknown') and p.is_unknown
            for p in self.points.values()
        )

        if has_unknown_points:
            # Solve for unknown points first
            self._solve_unknown_points()

        # Step 1: Create position vectors
        self._create_position_vectors()

        # Step 2: Create forces from specifications
        self._create_forces_from_specs()

        # Save original states
        if not self._original_force_states:
            for force_name, force in self.forces.items():
                self._original_force_states[force_name] = force.is_known

        # Step 3: Solve using ComponentSolver
        forces_list = list(self.forces.values())
        solved_forces = self.solver.solve(forces_list)

        # Update forces dict
        self.forces.update(solved_forces)

        # Get solution steps
        self.solution_steps.extend(self.solver.get_solution_steps())

        self.is_solved = True

        # Populate variables for report generation
        self._populate_variables_from_forces()

        return self.forces

    def _populate_variables_from_forces(self) -> None:
        """Convert ForceVector objects to Quantity variables for report generation."""
        from ..core.dimension_catalog import dim

        for force_name, force in self.forces.items():
            if force.magnitude is not None and force.magnitude.value is not None:
                mag_var = Quantity(
                    name=f"{force.name} Magnitude",
                    dim=dim.force,
                    value=force.magnitude.value,
                    preferred=force.magnitude.preferred,
                    _symbol=f"{force_name}_mag",
                )
                self.variables[f"{force_name}_mag"] = mag_var

            if force.x is not None and force.x.value is not None:
                x_var = Quantity(
                    name=f"{force.name} X-Component",
                    dim=dim.force,
                    value=force.x.value,
                    preferred=force.x.preferred,
                    _symbol=f"{force_name}_x",
                )
                self.variables[f"{force_name}_x"] = x_var

            if force.y is not None and force.y.value is not None:
                y_var = Quantity(
                    name=f"{force.name} Y-Component",
                    dim=dim.force,
                    value=force.y.value,
                    preferred=force.y.preferred,
                    _symbol=f"{force_name}_y",
                )
                self.variables[f"{force_name}_y"] = y_var

            if force.z is not None and force.z.value is not None:
                z_var = Quantity(
                    name=f"{force.name} Z-Component",
                    dim=dim.force,
                    value=force.z.value,
                    preferred=force.z.preferred,
                    _symbol=f"{force_name}_z",
                )
                self.variables[f"{force_name}_z"] = z_var

            # Add direction angles
            if hasattr(force, "alpha") and force.alpha is not None and force.alpha.value is not None:
                alpha_var = Quantity(
                    name=f"{force.name} Alpha",
                    dim=dim.D,
                    value=force.alpha.value,
                    preferred=force.alpha.preferred,
                    _symbol=f"{force_name}_alpha",
                )
                self.variables[f"{force_name}_alpha"] = alpha_var

            if hasattr(force, "beta") and force.beta is not None and force.beta.value is not None:
                beta_var = Quantity(
                    name=f"{force.name} Beta",
                    dim=dim.D,
                    value=force.beta.value,
                    preferred=force.beta.preferred,
                    _symbol=f"{force_name}_beta",
                )
                self.variables[f"{force_name}_beta"] = beta_var

            if hasattr(force, "gamma") and force.gamma is not None and force.gamma.value is not None:
                gamma_var = Quantity(
                    name=f"{force.name} Gamma",
                    dim=dim.D,
                    value=force.gamma.value,
                    preferred=force.gamma.preferred,
                    _symbol=f"{force_name}_gamma",
                )
                self.variables[f"{force_name}_gamma"] = gamma_var

    def get_position_vector(self, name: str) -> PositionVector | None:
        """Get a position vector by name."""
        return self.position_vectors.get(name)

    def get_force(self, name: str) -> ForceVector | None:
        """Get a force by name."""
        return self.forces.get(name)

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"PositionVectorProblem('{self.name}', points={len(self.points)}, forces={len(self.forces)}, {status})"
