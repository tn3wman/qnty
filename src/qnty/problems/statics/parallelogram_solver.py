"""
Parallelogram Law Problem - A Problem class for solving vector addition.

This problem uses the triangle method with Law of Cosines and Law of Sines
to solve parallelogram law problems. It dispatches to the equations module
for step-by-step solution generation.

The parallelogram law states that the resultant of two vectors can be found by
forming a parallelogram where:
- The two vectors form adjacent sides
- The diagonal represents the resultant
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from ...core import Q
from ...equations import AngleBetween, AngleSum, LawOfCosines, LawOfSines
from ..problem import Problem

if TYPE_CHECKING:
    from ...spatial.vector import _Vector
    from ...spatial.vectors import _VectorWithUnknowns


class ParallelogramLawProblem(Problem):
    """
    Problem class for solving parallelogram law (vector addition) problems.

    Uses the triangle method with Law of Cosines and Law of Sines to find
    unknown magnitudes and angles. Integrates with the report generator
    for Markdown and PDF output.

    Example:
        >>> from qnty.problems.statics import parallelogram_law as pl
        >>>
        >>> class MyProblem(ParallelogramLawProblem):
        ...     F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        ...     F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        ...     F_R = pl.create_vector_resultant(F_1, F_2)
        >>>
        >>> problem = MyProblem()
        >>> problem.solve()
        >>> problem.generate_report("report.pdf", format="pdf")
    """

    def __init__(self, name: str | None = None, description: str = ""):
        super().__init__(name=name, description=description)
        self.forces: dict[str, _Vector] = {}
        self._output_unit = "N"
        self._equations_used: list[str] = []

        # Track original states for reporting
        self._original_force_states: dict[str, bool] = {}

        # Extract vectors from class attributes
        self._extract_vectors()

    def _extract_vectors(self) -> None:
        """Extract vector objects defined at class level and create mag/angle variables."""
        from ...spatial.vector import _Vector
        from ...spatial.vectors import _VectorWithUnknowns

        vector_clones: dict[int, _Vector] = {}

        # First pass: clone all plain _Vectors (known vectors)
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, _Vector) and not isinstance(attr, _VectorWithUnknowns):
                clone = attr.clone(name=attr_name)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
                self.forces[attr_name] = clone
                self._original_force_states[attr_name] = True

                # Create magnitude and angle variables for report generation
                self._create_vector_variables(attr_name, clone, is_known=True)

        # Second pass: clone _VectorWithUnknowns (which may reference other vectors)
        for attr_name in dir(self.__class__):
            if attr_name.startswith("_"):
                continue
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, _VectorWithUnknowns):
                clone = attr.clone(name=attr_name, vector_clones=vector_clones)
                vector_clones[id(attr)] = clone
                setattr(self, attr_name, clone)
                self.forces[attr_name] = clone
                self._original_force_states[attr_name] = False

                # Create magnitude and angle variables for report generation (unknown)
                self._create_vector_variables(attr_name, clone, is_known=False)

    def _create_vector_variables(self, name: str, vec: _Vector, is_known: bool) -> None:
        """Create magnitude and angle Quantity variables for a vector."""
        from ...core import Q

        # Get magnitude from vector's magnitude property (returns a Quantity)
        if is_known and vec.magnitude is not None:
            mag_qty = vec.magnitude
            mag_qty.name = f"{name}_mag"
        else:
            # Create unknown magnitude quantity
            mag_qty = Q(0, self._output_unit)
            mag_qty.name = f"{name}_mag"
            mag_qty.value = None  # Mark as unknown

        self.variables[f"{name}_mag"] = mag_qty
        self._original_variable_states[f"{name}_mag"] = is_known

        # Get angle from vector's _original_angle attribute
        if is_known:
            original_angle = getattr(vec, "_original_angle", None)
            if original_angle is not None:
                angle_qty = Q(original_angle, 'degree')
                angle_qty.name = f"{name}_angle"
            else:
                angle_qty = Q(0, 'degree')
                angle_qty.name = f"{name}_angle"
                angle_qty.value = None
        else:
            angle_qty = Q(0, 'degree')
            angle_qty.name = f"{name}_angle"
            angle_qty.value = None  # Mark as unknown

        self.variables[f"{name}_angle"] = angle_qty
        self._original_variable_states[f"{name}_angle"] = is_known

    def get_known_variables(self) -> dict[str, Any]:
        """Get known variables for report generation."""
        known = {}
        for name, vec in self.forces.items():
            if self._original_force_states.get(name, True):
                known[name] = vec
        return known

    def get_unknown_variables(self) -> dict[str, Any]:
        """Get unknown variables for report generation."""
        unknown = {}
        for name, vec in self.forces.items():
            if not self._original_force_states.get(name, True):
                unknown[name] = vec
        return unknown

    def solve(self, output_unit: str = "N") -> ParallelogramLawProblem:
        """
        Solve the parallelogram law problem.

        Args:
            output_unit: Unit for output values (default "N")

        Returns:
            Self for method chaining
        """
        self._output_unit = output_unit

        # Find component vectors and resultant
        components = []
        resultant = None

        for name, vec in self.forces.items():
            if getattr(vec, "is_resultant", False):
                resultant = (name, vec)
            else:
                components.append((name, vec))

        if len(components) != 2:
            raise ValueError(f"Expected 2 component vectors, got {len(components)}")

        if resultant is None:
            raise ValueError("No resultant vector found")

        v1_name, v1 = components[0]
        v2_name, v2 = components[1]
        vr_name, vr = resultant

        # Solve using triangle method with vectors directly
        self._solve_forward(v1_name, v1, v2_name, v2, vr_name, vr)

        self.is_solved = True
        return self

    def _extract_vector_info(self, name: str, vector: _Vector) -> dict[str, Any]:
        """Extract magnitude, angle, and reference from a vector."""
        info: dict[str, Any] = {
            "name": name,
            "magnitude": None,
            "angle_deg": None,
            "wrt": "+x",
        }

        # Check for polar info
        polar_mag = getattr(vector, "_polar_magnitude", None)
        if polar_mag is not None:
            info["magnitude"] = polar_mag

        polar_angle_rad = getattr(vector, "_polar_angle_rad", None)
        if polar_angle_rad is not None:
            info["angle_deg"] = math.degrees(polar_angle_rad)

        original_wrt = getattr(vector, "_original_wrt", None)
        if original_wrt is not None:
            info["wrt"] = original_wrt

        original_angle = getattr(vector, "_original_angle", None)
        if original_angle is not None:
            info["angle_deg"] = original_angle

        # Check for magnitude property
        vec_magnitude = getattr(vector, "_magnitude", None)
        if info["magnitude"] is None and vec_magnitude is not None:
            if isinstance(vec_magnitude, Quantity) and vec_magnitude.value is not None:
                # Convert from SI to display unit
                from ...core.unit import ureg
                force_unit = ureg.resolve(self._output_unit)
                if force_unit:
                    info["magnitude"] = vec_magnitude.value / force_unit.si_factor

        # Compute from components if needed
        coords = getattr(vector, "_coords", None)
        if coords is not None and len(coords) >= 2:
            unknowns = getattr(vector, "_unknowns", None) or {}
            if "u" not in unknowns and "v" not in unknowns:
                x_si, y_si = float(coords[0]), float(coords[1])
                if info["magnitude"] is None:
                    mag_si = math.sqrt(x_si**2 + y_si**2)
                    from ...core.unit import ureg
                    force_unit = ureg.resolve(self._output_unit)
                    if force_unit:
                        info["magnitude"] = mag_si / force_unit.si_factor
                if info["angle_deg"] is None:
                    angle_rad = math.atan2(y_si, x_si)
                    info["angle_deg"] = math.degrees(angle_rad)
                    if info["angle_deg"] < 0:
                        info["angle_deg"] += 360

        return info

    def _solve_forward(
        self,
        v1_name: str,
        v1: _Vector,
        v2_name: str,
        v2: _Vector,
        vr_name: str,
        vr: _Vector,
    ) -> None:
        """Solve forward problem: find resultant from two known component vectors."""
        from ...core import u
        from ...core.quantity import Quantity
        from ...core.unit import ureg

        force_unit = ureg.resolve(self._output_unit) or u.newton

        # Get magnitude Quantities from vectors and set names for equation formatting
        mag1_qty = v1.magnitude
        mag2_qty = v2.magnitude

        if mag1_qty is None or mag2_qty is None:
            raise ValueError("Both component vectors must have known magnitude")

        # Set names on magnitude quantities for proper equation formatting
        mag1_qty.name = f"{v1_name}_mag"
        mag2_qty.name = f"{v2_name}_mag"

        # Step 1: Calculate triangle angle between the two vectors
        angle_between_eq = AngleBetween(
            target=f"\\angle(\\vec{{{v1_name}}}, \\vec{{{v2_name}}})",
            vec1=v1,
            vec2=v2,
        )
        triangle_angle_qty, step1 = angle_between_eq.solve()
        self.solving_history.append(step1)

        # Step 2: Law of Cosines to find resultant magnitude
        loc = LawOfCosines(
            target=f"|\\vec{{{vr_name}}}| using Eq 1",
            side_a=mag1_qty,
            side_b=mag2_qty,
            angle=triangle_angle_qty,
        )
        mag_r_qty, step2 = loc.solve()
        self.solving_history.append(step2)
        self._equations_used.append(loc.equation_for_list())

        # Step 3: Law of Sines to find angle from v1 to resultant
        use_obtuse = mag2_qty.value > mag_r_qty.value

        los = LawOfSines(
            target=f"\\angle(\\vec{{{v1_name}}}, \\vec{{{vr_name}}}) using Eq 2",
            opposite_side=mag2_qty,
            known_angle=triangle_angle_qty,
            known_side=mag_r_qty,
            use_obtuse=use_obtuse,
        )
        angle_v1_vr_qty, step3 = los.solve()
        self.solving_history.append(step3)
        self._equations_used.append(los.equation_for_list())

        # Step 4: Calculate resultant angle with respect to reference axis
        # Get v1's original angle as a Quantity using Q()
        v1_angle_deg = getattr(v1, '_original_angle', 0.0)
        v1_angle_qty = Q(v1_angle_deg, 'degree')
        v1_angle_qty.name = f"\\angle(\\vec{{x}}, \\vec{{{v1_name}}})"

        angle_sum = AngleSum(
            target=f"\\angle(\\vec{{x}}, \\vec{{{vr_name}}}) with respect to +x",
            base_angle=v1_angle_qty,
            offset_angle=angle_v1_vr_qty,
            result_ref="+x",
        )
        theta_r_qty, step4 = angle_sum.solve()
        self.solving_history.append(step4)

        # Get values using magnitude() for display units
        mag_r = mag_r_qty.magnitude()
        theta_r = theta_r_qty.magnitude()

        # Update resultant vector with computed values
        from ...algebra.functions import cos, sin
        theta_r_rad_qty = Q(theta_r, 'degree')
        x_r = mag_r * cos(theta_r_rad_qty).magnitude()
        y_r = mag_r * sin(theta_r_rad_qty).magnitude()

        # Store in SI units internally
        vr._coords[0] = x_r * force_unit.si_factor
        vr._coords[1] = y_r * force_unit.si_factor
        vr._coords[2] = 0.0

        # Store magnitude and angle for reporting
        vr._original_angle = theta_r
        vr._original_wrt = "+x"
        vr.is_known = True

        # Clear unknowns
        if hasattr(vr, "_unknowns"):
            vr._unknowns.clear()

        # Update the result variables for report generation
        if f"{vr_name}_mag" in self.variables:
            self.variables[f"{vr_name}_mag"] = mag_r_qty
        if f"{vr_name}_angle" in self.variables:
            self.variables[f"{vr_name}_angle"] = theta_r_qty

    def generate_report(
        self,
        output_path: str,
        format: str = "pdf",
    ) -> None:
        """
        Generate a report (Markdown, LaTeX, or PDF).

        Args:
            output_path: Path for output file
            format: Output format - 'markdown', 'latex', or 'pdf'
        """
        if not self.is_solved:
            raise ValueError("Problem must be solved before generating report")

        from ...extensions.reporting import generate_report as _generate_report
        _generate_report(self, output_path, format=format)


def solve_class(problem_class: type, output_unit: str = "N") -> ParallelogramLawProblem:
    """
    Solve a parallelogram law problem defined as a class.

    Args:
        problem_class: Class with vector attributes
        output_unit: Unit for output values

    Returns:
        Solved ParallelogramLawProblem instance

    Example:
        >>> class MyProblem:
        ...     F_1 = create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        ...     F_2 = create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        ...     F_R = create_vector_resultant(F_1, F_2)
        >>> problem = solve_class(MyProblem)
        >>> problem.generate_report("report.md", format="markdown")
    """
    # Create a dynamic problem class
    class DynamicProblem(ParallelogramLawProblem):
        pass

    # Copy class attributes
    DynamicProblem.name = getattr(problem_class, "name", problem_class.__name__)

    # Copy vector attributes
    from ...spatial.vector import _Vector
    from ...spatial.vectors import _VectorWithUnknowns

    for attr_name in dir(problem_class):
        if attr_name.startswith("_"):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, _Vector | _VectorWithUnknowns):
            setattr(DynamicProblem, attr_name, attr)

    # Create and solve
    problem = DynamicProblem()
    problem.solve(output_unit=output_unit)
    return problem
