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
from ..spatial import ForceVector, _Vector
from ..spatial.point import _Point
from ..spatial.vectors import create_vector_cartesian, create_vector_from_points
from ..spatial.vector_between import VectorBetween
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
        self.position_vectors: dict[str, _Vector] = {}
        self.position_vector_specs: dict[str, dict] = {}  # Position vector specifications with constraints
        self.position_vectors_with_constraints: dict[str, _Vector] = {}  # Vectors with magnitude constraints
        self.vector_betweens: dict[str, VectorBetween] = {}  # VectorBetween objects
        self.forces: dict[str, ForceVector] = {}
        self.force_specs: dict[str, dict] = {}  # Force specifications (from/to/magnitude)
        self.solution_steps: list[dict[str, Any]] = []
        self._original_force_states: dict[str, bool] = {}
        self.solver = ComponentSolver()
        self.solved_points: dict[str, _Point] = {}  # Points solved from force vectors

        # Extract class-level attributes
        self._extract_problem_elements()

    def reset(self) -> None:
        """
        Reset the problem state so it can be re-solved with modified inputs.

        Call this after changing point coordinates (lock/unlock) before re-solving.

        Examples:
            >>> prob = YourProblem()
            >>> prob.solve()
            >>> # Change what's known/unknown
            >>> prob.B.set_coordinate('z', 6.0)  # Lock z
            >>> prob.B.unlock_coordinate('y')     # Unlock y
            >>> prob.reset()
            >>> prob.solve()  # Re-solve for y
        """
        self.is_solved = False
        self.solution_steps = []
        self.solved_points = {}
        self.position_vectors = {}
        self._original_force_states = {}

        # Re-extract problem elements from instance attributes (not class)
        # This picks up modified points
        self._re_extract_instance_elements()

    def _re_extract_instance_elements(self) -> None:
        """Re-extract elements from instance attributes after modification."""
        # Clear existing collections but keep instance attributes
        self.points = {}
        self.vector_betweens = {}

        # Re-populate from instance attributes (which may have been modified)
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self, attr_name)

            # Check if it's a VectorBetween object or _Vector (solved result)
            if isinstance(attr, VectorBetween):
                self.vector_betweens[attr_name] = attr
            elif isinstance(attr, _Vector):
                # This was a solved VectorBetween - need to recreate it
                # Find original from class
                class_attr = getattr(self.__class__, attr_name, None)
                if isinstance(class_attr, VectorBetween):
                    # Recreate VectorBetween with current instance points
                    from_point_name = None
                    to_point_name = None
                    # Find point names by checking class-level VectorBetween
                    for pname in dir(self.__class__):
                        p = getattr(self.__class__, pname)
                        if p is class_attr.from_point:
                            from_point_name = pname
                        if p is class_attr.to_point:
                            to_point_name = pname

                    if from_point_name and to_point_name:
                        # Get current instance points
                        from_pt = getattr(self, from_point_name)
                        to_pt = getattr(self, to_point_name)
                        # Create new VectorBetween with updated points
                        new_vb = VectorBetween(
                            from_point=from_pt,
                            to_point=to_pt,
                            magnitude=class_attr.constraint_magnitude,
                            unit=class_attr.unit,
                            name=class_attr.name
                        )
                        self.vector_betweens[attr_name] = new_vb
                        setattr(self, attr_name, new_vb)

            # Check if it's a point
            elif hasattr(attr, "to_cartesian") or isinstance(attr, _Point):
                if isinstance(attr, _Point):
                    self.points[attr_name] = attr

    def _extract_problem_elements(self) -> None:
        """Extract points, force specs, and ForceVectors from class attributes."""
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.__class__, attr_name)

            # Check if it's a VectorBetween object (must come before point check since it has to_cartesian)
            if isinstance(attr, VectorBetween):
                self.vector_betweens[attr_name] = attr
                setattr(self, attr_name, attr)

            # Check if it's a _Vector with magnitude constraint (position vector)
            # Must come before point check since _Vector has to_cartesian method
            elif isinstance(attr, _Vector) and hasattr(attr, '_constraint_magnitude') and attr._constraint_magnitude is not None:
                self.position_vectors_with_constraints[attr_name] = attr
                setattr(self, attr_name, attr)

            # Check if it's a ForceVector / plain _Vector (e.g., resultant or direction vector)
            # Must come before point check since _Vector has to_cartesian method
            elif isinstance(attr, _Vector):
                # Check if it's a ForceVector that needs cloning
                if hasattr(attr, 'is_resultant') and attr.is_resultant:
                    force_copy = self._clone_force_vector(attr)
                    self.forces[attr_name] = force_copy
                    setattr(self, attr_name, force_copy)
                else:
                    # It's a direction vector (like F in Problem 2-89)
                    setattr(self, attr_name, attr)

            # Check if it's a point (has to_cartesian method or is _Point)
            elif hasattr(attr, "to_cartesian") or isinstance(attr, _Point):
                self.points[attr_name] = attr
                setattr(self, attr_name, attr)

            # Check if it's a force specification dict (has magnitude in force units)
            elif isinstance(attr, dict) and "from" in attr and "to" in attr and "magnitude" in attr:
                self.force_specs[attr_name] = attr

            # Check if it's a position vector spec (has magnitude but no force unit - just length constraint)
            elif isinstance(attr, dict) and "from" in attr and "to" in attr:
                self.position_vector_specs[attr_name] = attr

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
            r = create_vector_from_points(from_point, to_point, name=pv_name)
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
        """Solve for unknown points given position vector magnitude constraints or force vectors."""
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        import numpy as np

        # First, handle PointCartesian with ellipsis unknowns and magnitude constraints
        self._solve_points_from_magnitude_constraints()

        # Then handle legacy Point.unknown with force direction
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

    def _solve_points_from_magnitude_constraints(self) -> None:
        """Solve for unknown point coordinates using position vector magnitude constraints."""
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        import numpy as np

        # Process VectorBetween objects first
        for vb_name, vb in self.vector_betweens.items():
            if not vb.has_unknowns():
                continue

            magnitude = vb.constraint_magnitude
            if magnitude is None:
                raise ValueError(f"VectorBetween '{vb_name}' has unknowns but no magnitude constraint")

            from_point = vb.from_point
            to_point = vb.to_point
            length_unit = vb.unit

            if length_unit is None:
                raise ValueError(f"VectorBetween '{vb_name}' requires a unit")

            self._solve_single_constraint(
                vb_name, from_point, to_point, magnitude, length_unit, vb
            )

        # Process position vectors with magnitude constraints
        for pv_name, pv in self.position_vectors_with_constraints.items():
            if not pv.has_unknowns():
                continue

            # Magnitude is already in SI units
            magnitude_si = pv.constraint_magnitude
            if magnitude_si is None:
                raise ValueError(f"Position vector '{pv_name}' has unknowns but no magnitude constraint. "
                               "Cannot solve for unknown point coordinates without a magnitude constraint.")

            from_point = pv.from_point
            to_point = pv.to_point
            length_unit = pv._unit

            if length_unit is None:
                raise ValueError(f"Position vector '{pv_name}' requires a unit")

            # Convert magnitude back to user units for _solve_single_constraint
            magnitude = magnitude_si / length_unit.si_factor

            self._solve_single_constraint(
                pv_name, from_point, to_point, magnitude, length_unit, None
            )

        # Then process dict-based position vector specs
        for pv_name, pv_spec in self.position_vector_specs.items():
            from_name = pv_spec["from"]
            to_name = pv_spec["to"]
            magnitude = pv_spec.get("magnitude")
            unit_str = pv_spec.get("unit", "m")

            if magnitude is None:
                continue

            from_point = self.points.get(from_name)
            to_point = self.points.get(to_name)

            if from_point is None or to_point is None:
                continue

            # Resolve length unit
            length_unit = ureg.resolve(unit_str, dim=dim.length)
            if length_unit is None:
                raise ValueError(f"Unknown length unit '{unit_str}'")

            self._solve_single_constraint(
                pv_name, from_point, to_point, magnitude, length_unit, None
            )

    def _solve_single_constraint(
        self,
        name: str,
        from_point: Any,
        to_point: Any,
        magnitude: float,
        length_unit: Any,
        vector_between: VectorBetween | None,
    ) -> None:
        """Solve a single magnitude constraint for unknown coordinates."""
        from ..core.dimension_catalog import dim

        import numpy as np

        # Check which point has unknowns
        from_unknowns = getattr(from_point, 'unknowns', {}) if hasattr(from_point, 'unknowns') else {}
        to_unknowns = getattr(to_point, 'unknowns', {}) if hasattr(to_point, 'unknowns') else {}

        if not from_unknowns and not to_unknowns:
            # No unknowns - just compute the vector if VectorBetween
            if vector_between is not None:
                vector_between._compute_vector()
            return

        # Convert magnitude to SI
        mag_si = magnitude * length_unit.si_factor

        # Get coordinates (convert to _Point if needed)
        from_cart = from_point.to_cartesian() if hasattr(from_point, 'to_cartesian') else from_point
        to_cart = to_point.to_cartesian() if hasattr(to_point, 'to_cartesian') else to_point

        from_coords = from_cart._coords
        to_coords = to_cart._coords

        # Determine which coordinates are unknown
        solved_point: _Point | None = None
        unknown_point_name: str | None = None

        # Handle case where all 3 coordinates are unknown - need direction vector
        if len(from_unknowns) == 3 or len(to_unknowns) == 3:
            # Look for a direction vector (create_vector_cartesian named F or similar)
            # Must be a vector that is NOT the position vector being solved
            direction_vector = None
            for attr_name in dir(self):
                if attr_name.startswith('_'):
                    continue
                if attr_name == name:  # Skip the position vector we're solving
                    continue
                attr = getattr(self, attr_name)
                if isinstance(attr, _Vector) and not attr.has_unknowns():
                    # Check it's not a position vector with constraint (those have _from_point)
                    if not hasattr(attr, '_from_point') or attr._from_point is None:
                        direction_vector = attr
                        break

            if direction_vector is None:
                raise ValueError(
                    f"Cannot solve for 3 unknown coordinates in '{name}' without a direction vector. "
                    f"Please provide a force or direction vector (e.g., F = create_vector_cartesian(u=..., v=..., w=..., unit='N')) "
                    f"to define the direction from the known point to the unknown point."
                )

            # Get unit vector from direction
            dir_coords = direction_vector._coords
            dir_mag = math.sqrt(dir_coords[0]**2 + dir_coords[1]**2 + dir_coords[2]**2)
            if dir_mag == 0:
                raise ValueError("Direction vector has zero magnitude")

            ux = dir_coords[0] / dir_mag
            uy = dir_coords[1] / dir_mag
            uz = dir_coords[2] / dir_mag

            # r_AB = B - A = mag * unit_direction
            # So A = B - mag * unit_direction
            if len(from_unknowns) == 3:
                # Solving for from_point (A)
                ax = to_coords[0] - mag_si * ux
                ay = to_coords[1] - mag_si * uy
                az = to_coords[2] - mag_si * uz
                solved_coords = np.array([ax, ay, az], dtype=float)
                unknown_point = from_point
            else:
                # Solving for to_point (B)
                bx = from_coords[0] + mag_si * ux
                by = from_coords[1] + mag_si * uy
                bz = from_coords[2] + mag_si * uz
                solved_coords = np.array([bx, by, bz], dtype=float)
                unknown_point = to_point

            # Create solved point
            solved_point = object.__new__(_Point)
            solved_point._coords = solved_coords
            solved_point._dim = dim.length
            solved_point._unit = length_unit
            solved_point._is_unknown = False
            solved_point._distance = None

            # Find point name
            for pname, p in self.points.items():
                if p is unknown_point:
                    unknown_point_name = pname
                    break

            if unknown_point_name:
                self.solved_points[unknown_point_name] = solved_point
                self.points[unknown_point_name] = solved_point
                setattr(self, unknown_point_name, solved_point)

            # Add solution step
            display_coords = solved_point.to_array()
            self.solution_steps.append({
                "target": unknown_point_name or "unknown",
                "method": "direction_vector",
                "description": f"Solved all coordinates using direction and |{name}| = {magnitude} {length_unit.symbol}",
                "result_value": f"({display_coords[0]:.2f}, {display_coords[1]:.2f}, {display_coords[2]:.2f})",
                "result_unit": length_unit.symbol,
            })
            return

        elif len(to_unknowns) == 1:
            unknown_coord = list(to_unknowns.keys())[0]

            # Get known differences
            if unknown_coord == "x":
                dy = to_coords[1] - from_coords[1]
                dz = to_coords[2] - from_coords[2]
                dx_sq = mag_si**2 - dy**2 - dz**2
                if dx_sq < 0:
                    raise ValueError(f"Magnitude {magnitude} is too small for the given coordinates")
                dx = math.sqrt(dx_sq)
                solved_x = from_coords[0] + dx if to_coords[0] >= from_coords[0] else from_coords[0] - dx
                solved_coords = np.array([solved_x, to_coords[1], to_coords[2]], dtype=float)
                solved_value = solved_x / length_unit.si_factor

            elif unknown_coord == "y":
                dx = to_coords[0] - from_coords[0]
                dz = to_coords[2] - from_coords[2]
                dy_sq = mag_si**2 - dx**2 - dz**2
                if dy_sq < 0:
                    raise ValueError(f"Magnitude {magnitude} is too small for the given coordinates")
                dy = math.sqrt(dy_sq)
                solved_y = from_coords[1] + dy if to_coords[1] >= from_coords[1] else from_coords[1] - dy
                solved_coords = np.array([to_coords[0], solved_y, to_coords[2]], dtype=float)
                solved_value = solved_y / length_unit.si_factor

            elif unknown_coord == "z":
                dx = to_coords[0] - from_coords[0]
                dy = to_coords[1] - from_coords[1]
                dz_sq = mag_si**2 - dx**2 - dy**2
                if dz_sq < 0:
                    raise ValueError(f"Magnitude {magnitude} is too small for the given coordinates")
                dz = math.sqrt(dz_sq)
                solved_z = from_coords[2] + dz
                solved_coords = np.array([to_coords[0], to_coords[1], solved_z], dtype=float)
                solved_value = solved_z / length_unit.si_factor

            else:
                return

            # Create solved _Point first (internal representation)
            solved_point = object.__new__(_Point)
            solved_point._coords = solved_coords
            solved_point._dim = dim.length
            solved_point._unit = length_unit
            solved_point._is_unknown = False
            solved_point._distance = None

            # Find the point name - need to search through points dict
            for pname, p in self.points.items():
                if p is to_point:
                    unknown_point_name = pname
                    break

            if unknown_point_name:
                self.solved_points[unknown_point_name] = solved_point
                self.points[unknown_point_name] = solved_point
                # Update instance attribute so prob.B returns solved _Point
                setattr(self, unknown_point_name, solved_point)

            # Add solution step
            unit_str = length_unit.symbol if length_unit else ""
            self.solution_steps.append({
                "target": unknown_point_name or "unknown",
                "method": "magnitude_constraint",
                "description": f"Solved {unknown_coord} using |{name}| = {magnitude} {unit_str}",
                "result_value": f"{solved_value:.2f}",
                "result_unit": unit_str,
            })

            # Update VectorBetween's internal vector and replace with create_vector_cartesian
            if vector_between is not None:
                vector_between._compute_vector(from_cart, solved_point)
                # Create create_vector_cartesian wrapper for user-friendly output
                vec = vector_between._vector
                if vec is not None:
                    vec_coords = vec.to_array()
                    solved_vector_cartesian = create_vector_cartesian(
                        u=vec_coords[0],
                        v=vec_coords[1],
                        w=vec_coords[2],
                        unit=length_unit
                    )
                    # Find the VectorBetween name and update instance attribute
                    for vb_name_key, vb_obj in self.vector_betweens.items():
                        if vb_obj is vector_between:
                            setattr(self, vb_name_key, solved_vector_cartesian)
                            break

        elif len(from_unknowns) == 1:
            unknown_coord = list(from_unknowns.keys())[0]

            if unknown_coord == "z":
                dx = to_coords[0] - from_coords[0]
                dy = to_coords[1] - from_coords[1]
                dz_sq = mag_si**2 - dx**2 - dy**2
                if dz_sq < 0:
                    raise ValueError(f"Magnitude {magnitude} is too small for the given coordinates")
                dz = math.sqrt(dz_sq)
                solved_z = to_coords[2] - dz
                solved_coords = np.array([from_coords[0], from_coords[1], solved_z], dtype=float)
                solved_value = solved_z / length_unit.si_factor
            else:
                return

            # Create solved _Point first (internal representation)
            solved_point = object.__new__(_Point)
            solved_point._coords = solved_coords
            solved_point._dim = dim.length
            solved_point._unit = length_unit
            solved_point._is_unknown = False
            solved_point._distance = None

            # Find the point name
            for pname, p in self.points.items():
                if p is from_point:
                    unknown_point_name = pname
                    break

            if unknown_point_name:
                self.solved_points[unknown_point_name] = solved_point
                self.points[unknown_point_name] = solved_point
                # Update instance attribute so prob.A returns solved _Point
                setattr(self, unknown_point_name, solved_point)

            # Add solution step
            unit_str = length_unit.symbol if length_unit else ""
            self.solution_steps.append({
                "target": unknown_point_name or "unknown",
                "method": "magnitude_constraint",
                "description": f"Solved {unknown_coord} using |{name}| = {magnitude} {unit_str}",
                "result_value": f"{solved_value:.2f}",
                "result_unit": unit_str,
            })

            # Update VectorBetween's internal vector and replace with create_vector_cartesian
            if vector_between is not None:
                vector_between._compute_vector(solved_point, to_cart)
                # Create create_vector_cartesian wrapper for user-friendly output
                vec = vector_between._vector
                if vec is not None:
                    vec_coords = vec.to_array()
                    solved_vector_cartesian = create_vector_cartesian(
                        u=vec_coords[0],
                        v=vec_coords[1],
                        w=vec_coords[2],
                        unit=length_unit
                    )
                    # Find the VectorBetween name and update instance attribute
                    for vb_name_key, vb_obj in self.vector_betweens.items():
                        if vb_obj is vector_between:
                            setattr(self, vb_name_key, solved_vector_cartesian)
                            break

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
            (hasattr(p, 'is_unknown') and p.is_unknown) or
            (hasattr(p, 'has_unknowns') and p.has_unknowns)
            for p in self.points.values()
        )

        # Also check VectorBetween objects for unknowns
        has_vector_unknowns = any(
            vb.has_unknowns() for vb in self.vector_betweens.values()
        )

        if has_unknown_points or has_vector_unknowns:
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

    def get_position_vector(self, name: str) -> _Vector | None:
        """Get a position vector by name."""
        return self.position_vectors.get(name)

    def get_force(self, name: str) -> ForceVector | None:
        """Get a force by name."""
        return self.forces.get(name)

    def __str__(self) -> str:
        """String representation."""
        status = "SOLVED" if self.is_solved else "UNSOLVED"
        return f"PositionVectorProblem('{self.name}', points={len(self.points)}, forces={len(self.forces)}, {status})"
