"""
Rectangular Method Problem Solver - Resolve vectors into x and y components.

This module provides a solver for vector resolution problems using the rectangular
(Cartesian) method. Given vectors in polar form (magnitude and angle), it computes
their x and y components using:
    Fx = |F| * cos(theta)
    Fy = |F| * sin(theta)

Optionally, it can compute the resultant vector from the components:
    F_Rx = sum(Fx_i)
    F_Ry = sum(Fy_i)
    |F_R| = sqrt(F_Rx^2 + F_Ry^2)
    theta_R = atan2(F_Ry, F_Rx)

Key Design Principles:
1. Uses the Vector class's built-in .x and .y properties for component resolution
2. All trigonometry uses qnty's algebra functions for dimensional correctness
3. Reports show the step-by-step resolution process with proper notation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ...algebra.functions import atan2, cos, sin, sqrt
from ...core import Q
from ...core.quantity import Quantity
from ...equations.angle_finder import get_absolute_angle, get_relative_angle
from ...equations.angle_reference import AngleDirection
from ...equations.base import SolutionStepBuilder, latex_name
from ...linalg.vector2 import Vector, VectorUnknown
from .report_utils import format_component_terms

if TYPE_CHECKING:
    pass


@dataclass
class ComponentResult:
    """Result of resolving a single vector into x and y components."""

    vector_name: str
    magnitude: Quantity
    angle: Quantity
    angle_wrt: str
    abs_angle_deg: float  # Absolute angle from +x axis in degrees
    x_component: Quantity
    y_component: Quantity


@dataclass
class ResultantResult:
    """Result of computing the resultant from component sums."""

    x_sum: Quantity
    y_sum: Quantity
    magnitude: Quantity
    angle: Quantity  # Angle in radians from atan2


@dataclass
class RectangularMethodResult:
    """Complete result of rectangular method solving."""

    components: list[ComponentResult]
    resultant: ResultantResult | None = None
    solving_history: list[dict[str, Any]] = field(default_factory=list)


def _get_trig_functions_for_angle(angle_wrt: str) -> tuple[str, str, str, str]:
    """
    Get the trig function names and i/j sign labels for component resolution.

    For an angle measured from an axis, the trig functions used depend on
    which axis is the reference:
    - wrt +x or -x: x-component uses cos, y-component uses sin
    - wrt +y or -y: x-component uses sin, y-component uses cos

    Args:
        angle_wrt: The reference axis (e.g., "+x", "-x", "+y", "-y")

    Returns:
        Tuple of (x_func, y_func, i_sign, j_sign) where:
        - x_func: "cos" or "sin" for x-component
        - y_func: "sin" or "cos" for y-component
        - i_sign: "+i" or "-i" for i unit vector
        - j_sign: "+j" or "-j" for j unit vector
    """
    wrt_clean = angle_wrt.lower().strip()

    # Default to x-axis reference
    if "y" in wrt_clean:
        # Angle measured from y-axis: x uses sin, y uses cos
        x_func, y_func = "sin", "cos"
    else:
        # Angle measured from x-axis (default): x uses cos, y uses sin
        x_func, y_func = "cos", "sin"

    # Determine signs based on axis direction
    # For +x or +y, standard signs
    # For -x or -y, signs depend on what the angle represents
    i_sign = "+\\mathbf{i}"
    j_sign = "+\\mathbf{j}"

    return x_func, y_func, i_sign, j_sign


def _format_component_i_j(x_val: float, y_val: float, unit: str, precision: int = 1) -> str:
    """
    Format vector components in i-j notation: {xi + yj} unit

    Args:
        x_val: x-component value
        y_val: y-component value
        unit: Unit string
        precision: Decimal precision

    Returns:
        LaTeX formatted string like "{200\\mathbf{i} + 346\\mathbf{j}} \\text{ N}"
    """
    # Format x component
    x_str = f"{x_val:.{precision}f}\\mathbf{{i}}"

    # Format y component with appropriate sign
    if y_val >= 0:
        y_str = f"+ {y_val:.{precision}f}\\mathbf{{j}}"
    else:
        y_str = f"- {abs(y_val):.{precision}f}\\mathbf{{j}}"

    return f"\\{{{x_str} {y_str}\\}} \\text{{ {unit}}}"


class RectangularMethodProblem:
    """
    Problem class for rectangular method vector resolution.

    Resolves input vectors (in polar form) into their x and y components.
    Optionally computes the resultant if requested.

    Attributes:
        name: Problem name
        vectors: List of input vectors to resolve
        compute_resultant: Whether to compute the resultant vector
        result: The solution result after solving
        solving_history: List of solution steps for report generation
        is_solved: True if the problem has been solved
    """

    name: str = "Rectangular Method Problem"

    def __init__(self):
        self.vectors: list[Vector | VectorUnknown] = []
        self.resultant_vector: Vector | VectorUnknown | None = None  # Known resultant for solving unknowns
        self.compute_resultant: bool = False
        self._result: RectangularMethodResult | None = None
        self.solving_history: list[dict[str, Any]] = []
        self.is_solved: bool = False

    @property
    def result(self) -> RectangularMethodResult | None:
        return self._result

    def _build_component_resolution_step(
        self,
        vec_name: str,
        magnitude: Quantity,
        angle: Quantity,
        angle_wrt: str,
        abs_angle_deg: float,
        x_comp: Quantity,
        y_comp: Quantity,
        unit: str,
        equation_number: int,
    ) -> dict[str, Any]:
        """
        Build a solution step for vector component resolution.

        Creates a step showing the trig decomposition like:
        F_1 = {|F_1| sin θ (±i) + |F_1| cos θ (±j)} = {xi + yj} N

        Args:
            vec_name: Name of the vector
            magnitude: Magnitude as Quantity
            angle: Angle as Quantity
            angle_wrt: Reference axis string
            abs_angle_deg: Absolute angle from +x in degrees
            x_comp: X component as Quantity
            y_comp: Y component as Quantity
            unit: Unit string
            equation_number: Equation number for reference

        Returns:
            Solution step dictionary
        """
        vec_latex = latex_name(vec_name)
        mag_val = magnitude.magnitude()
        x_val = x_comp.magnitude()
        y_val = y_comp.magnitude()

        # Get trig functions based on reference axis
        x_func, y_func, i_sign, j_sign = _get_trig_functions_for_angle(angle_wrt)

        # Determine actual signs based on component values
        # The actual sign comes from evaluating the full trig expression
        if x_val >= 0:
            i_sign_actual = "+\\mathbf{i}"
        else:
            i_sign_actual = "-\\mathbf{i}"

        if y_val >= 0:
            j_sign_actual = "+\\mathbf{j}"
        else:
            j_sign_actual = "-\\mathbf{j}"

        # Build the substitution showing the trig decomposition
        # Format: F = {|F| · func(θ)(±i) + |F| · func(θ)(±j)} = {xi + yj} N
        # Use absolute values for magnitude and angle - signs are captured in i/j directions
        angle_deg_val = angle.to_unit.degree.magnitude()
        angle_deg_abs = abs(angle_deg_val)
        angle_latex_abs = f"{angle_deg_abs:.0f}^{{\\circ}}"
        mag_val_abs = abs(mag_val)

        # Build expression: |F| · sin θ (±i) + |F| · cos θ (±j)
        x_expr = f"{mag_val_abs:.0f} \\cdot \\{x_func}({angle_latex_abs})({i_sign_actual})"
        y_expr = f"{mag_val_abs:.0f} \\cdot \\{y_func}({angle_latex_abs})({j_sign_actual})"

        # The computed components
        components_result = _format_component_i_j(x_val, y_val, unit, precision=1)

        substitution = f"\\vec{{{vec_latex}}} &= \\{{{x_expr} + {y_expr}\\}} \\text{{ {unit}}} \\\\\n&= {components_result}"

        # Target string
        target = f"\\vec{{{vec_latex}}}"

        step = SolutionStepBuilder(
            target=target,
            method="Rectangular Component Resolution",
            description=f"Resolve {vec_name} into x and y components",
            equation_for_list="",  # No equation for list - component resolution is shown in steps
            substitution=substitution,
        )

        return step.build()

    def _build_resultant_sum_step(
        self,
        components: list[ComponentResult],
        x_sum: Quantity,
        y_sum: Quantity,
        unit: str,
        equation_number: int,
    ) -> dict[str, Any]:
        """
        Build a solution step for summing components to get the resultant.

        Shows: F_R = F_1 + F_2 = {(x1+x2)i + (y1+y2)j} = {xi + yj} N

        Args:
            components: List of ComponentResult for all vectors
            x_sum: Sum of x components
            y_sum: Sum of y components
            unit: Unit string
            equation_number: Equation number

        Returns:
            Solution step dictionary
        """
        # Build the sum expression
        vec_names = [latex_name(c.vector_name) for c in components]
        sum_expr = " + ".join([f"\\vec{{{n}}}" for n in vec_names])

        # Build individual component expressions
        x_vals = [c.x_component.magnitude() for c in components]
        y_vals = [c.y_component.magnitude() for c in components]

        # Format x-component sum: (200+177)i
        x_terms = format_component_terms(x_vals, precision=1)
        x_sum_expr = f"({''.join(x_terms)})\\mathbf{{i}}"

        # Format y-component sum: (346-177)j
        y_terms = format_component_terms(y_vals, precision=1)
        y_sum_expr = f"({''.join(y_terms)})\\mathbf{{j}}"

        # Final result
        x_sum_val = x_sum.magnitude()
        y_sum_val = y_sum.magnitude()
        result_expr = _format_component_i_j(x_sum_val, y_sum_val, unit, precision=1)

        substitution = f"\\vec{{F_R}} &= {sum_expr} \\\\\n&= \\{{{x_sum_expr} + {y_sum_expr}\\}} \\text{{ {unit}}} \\\\\n&= {result_expr}"

        step = SolutionStepBuilder(
            target="\\vec{F_R}",
            method="Component Addition",
            description="Sum all vector components",
            equation_for_list="",  # No equation for list - summation is shown in steps
            substitution=substitution,
        )

        return step.build()

    def _build_magnitude_step(
        self,
        x_sum: Quantity,
        y_sum: Quantity,
        magnitude: Quantity,
        unit: str,
        equation_number: int,
    ) -> dict[str, Any]:
        """
        Build a solution step for computing resultant magnitude using Pythagorean theorem.

        Shows: |F_R| = sqrt(F_Rx^2 + F_Ry^2) = sqrt(377^2 + 169^2) = 415 N

        Args:
            x_sum: Sum of x components
            y_sum: Sum of y components
            magnitude: Computed magnitude
            unit: Unit string
            equation_number: Equation number

        Returns:
            Solution step dictionary
        """
        x_val = x_sum.magnitude()
        y_val = y_sum.magnitude()
        mag_val = magnitude.magnitude()

        substitution = f"|\\vec{{F_R}}| &= \\sqrt{{(F_R)_x^2 + (F_R)_y^2}} \\\\\n&= \\sqrt{{({x_val:.1f})^2 + ({y_val:.1f})^2}} \\text{{ {unit}}} \\\\\n&= {mag_val:.1f} \\text{{ {unit}}}"

        step = SolutionStepBuilder(
            target="|\\vec{F_R}|",
            method="Pythagorean Theorem",
            description="Calculate resultant magnitude",
            equation_for_list="|\\vec{F_R}| = \\sqrt{(F_R)_x^2 + (F_R)_y^2}",
            substitution=substitution,
        )

        return step.build()

    def _build_direction_step(
        self,
        x_sum: Quantity,
        y_sum: Quantity,
        angle: Quantity,
        unit: str,
        equation_number: int,
    ) -> dict[str, Any]:
        """
        Build a solution step for computing resultant direction using atan2.

        Shows: θ = arctan(F_Ry/F_Rx) = arctan(169/377) = 24.2°

        Args:
            x_sum: Sum of x components
            y_sum: Sum of y components
            angle: Computed angle (in radians from atan2)
            unit: Unit string
            equation_number: Equation number

        Returns:
            Solution step dictionary
        """
        x_val = x_sum.magnitude()
        y_val = y_sum.magnitude()

        # Convert angle to degrees for display using Quantity
        angle_deg = angle.to_unit.degree.magnitude()

        substitution = (
            f"\\angle(x, F_R) &= \\arctan\\left(\\frac{{(F_R)_y}}{{(F_R)_x}}\\right) \\\\\n&= \\arctan\\left(\\frac{{{y_val:.1f}}}{{{x_val:.1f}}}\\right) \\\\\n&= {angle_deg:.2f}^{{\\circ}}"
        )

        step = SolutionStepBuilder(
            target="\\angle(x, F_R)",
            method="Inverse Tangent",
            description="Calculate resultant direction",
            equation_for_list="",  # No equation for list - arctan is shown in steps
            substitution=substitution,
        )

        return step.build()

    def _build_unknown_vector_step(
        self,
        vec_name: str,
        known_components: list[tuple[str, Quantity, Quantity]],
        resultant_x: Quantity,
        resultant_y: Quantity,
        unknown_x: Quantity,
        unknown_y: Quantity,
        unknown_mag: Quantity,
        unknown_angle_deg: float,
        unit: str,
        equation_number: int,
    ) -> dict[str, Any]:
        """
        Build a solution step for solving an unknown vector from equilibrium.

        Shows the equilibrium equations and solution for the unknown vector.

        Args:
            vec_name: Name of the unknown vector
            known_components: List of (name, x_comp, y_comp) for known vectors
            resultant_x: X component of known resultant
            resultant_y: Y component of known resultant
            unknown_x: Solved x component of unknown
            unknown_y: Solved y component of unknown
            unknown_mag: Solved magnitude of unknown
            unknown_angle_deg: Solved angle in degrees from +x
            unit: Unit string
            equation_number: Equation number

        Returns:
            Solution step dictionary
        """
        vec_latex = latex_name(vec_name)

        # Build the equilibrium equation showing sum of knowns
        known_x_terms = " + ".join(f"({latex_name(name)})_x" for name, _, _ in known_components)
        known_y_terms = " + ".join(f"({latex_name(name)})_y" for name, _, _ in known_components)

        # Get numeric values
        r_x_val = resultant_x.magnitude()
        r_y_val = resultant_y.magnitude()
        unknown_x_val = unknown_x.magnitude()
        unknown_y_val = unknown_y.magnitude()
        unknown_mag_val = unknown_mag.magnitude()

        # Build substitution showing the solution
        substitution = (
            f"({vec_latex})_x &= (F_R)_x - ({known_x_terms}) \\\\\n"
            f"&= {r_x_val:.1f} - ({' + '.join(f'{c[1].magnitude():.1f}' for c in known_components)}) \\\\\n"
            f"&= {unknown_x_val:.1f} \\text{{ {unit}}} \\\\\n"
            f"({vec_latex})_y &= (F_R)_y - ({known_y_terms}) \\\\\n"
            f"&= {r_y_val:.1f} - ({' + '.join(f'{c[2].magnitude():.1f}' for c in known_components)}) \\\\\n"
            f"&= {unknown_y_val:.1f} \\text{{ {unit}}} \\\\\n"
            f"|\\vec{{{vec_latex}}}| &= \\sqrt{{({vec_latex})_x^2 + ({vec_latex})_y^2}} \\\\\n"
            f"&= \\sqrt{{({unknown_x_val:.1f})^2 + ({unknown_y_val:.1f})^2}} \\\\\n"
            f"&= {unknown_mag_val:.1f} \\text{{ {unit}}} \\\\\n"
            f"\\angle(x, {vec_latex}) &= \\arctan\\left(\\frac{{({vec_latex})_y}}{{({vec_latex})_x}}\\right) \\\\\n"
            f"&= \\arctan\\left(\\frac{{{unknown_y_val:.1f}}}{{{unknown_x_val:.1f}}}\\right) \\\\\n"
            f"&= {unknown_angle_deg:.2f}^{{\\circ}}"
        )

        step = SolutionStepBuilder(
            target=f"\\vec{{{vec_latex}}}",
            method="Equilibrium Equations",
            description=f"Solve for unknown vector {vec_name}",
            equation_for_list="",
            substitution=substitution,
        )

        return step.build()

    def _is_vector_fully_known(self, vec: Vector | VectorUnknown) -> bool:
        """Check if a vector has both magnitude and angle known."""
        return vec.magnitude is not ... and vec.angle is not ...

    def _resolve_known_vector(
        self,
        vec: Vector | VectorUnknown,
        context: dict,
        output_unit: str,
    ) -> ComponentResult:
        """Resolve a fully known vector into x and y components."""
        magnitude = vec.magnitude
        angle = vec.angle

        # Get the reference axis
        wrt = vec.wrt if isinstance(vec.wrt, str) else f"{vec.wrt.name}"

        # Compute absolute angle from +x axis
        abs_angle = get_absolute_angle(vec, context=context)
        abs_angle_deg = abs_angle.to_unit.degree.magnitude()

        # Compute components using qnty algebra
        x_comp = magnitude * cos(abs_angle)
        y_comp = magnitude * sin(abs_angle)

        # Ensure we have Quantity objects
        if not isinstance(x_comp, Quantity):
            x_comp = x_comp.evaluate({}) if hasattr(x_comp, "evaluate") else Q(float(x_comp), output_unit)
        if not isinstance(y_comp, Quantity):
            y_comp = y_comp.evaluate({}) if hasattr(y_comp, "evaluate") else Q(float(y_comp), output_unit)

        return ComponentResult(
            vector_name=vec.name or "F",
            magnitude=magnitude,
            angle=angle,
            angle_wrt=wrt,
            abs_angle_deg=abs_angle_deg,
            x_component=x_comp,
            y_component=y_comp,
        )

    def solve(self, output_unit: str = "N") -> RectangularMethodResult:
        """
        Solve the rectangular method problem.

        Resolves all vectors into x and y components using:
            Fx = |F| * cos(theta)
            Fy = |F| * sin(theta)

        If compute_resultant is True, also computes:
            F_Rx = sum(Fx_i)
            F_Ry = sum(Fy_i)
            |F_R| = sqrt(F_Rx^2 + F_Ry^2)
            theta_R = atan2(F_Ry, F_Rx)

        For problems with unknown vectors and a known resultant, solves for
        the unknown using equilibrium equations:
            F_unknown_x = F_R_x - sum(F_known_x)
            F_unknown_y = F_R_y - sum(F_known_y)

        Args:
            output_unit: Unit for output values (default: "N")

        Returns:
            RectangularMethodResult with all component values
        """
        components: list[ComponentResult] = []
        self.solving_history = []
        equation_number = 1

        # Build context dictionary for resolving force-relative references (e.g., wrt=F_2)
        context = {}
        for vec in self.vectors:
            if vec.name:
                context[vec.name] = vec
        # Add resultant to context if it exists
        if self.resultant_vector is not None and self.resultant_vector.name:
            context[self.resultant_vector.name] = self.resultant_vector

        # Separate known and unknown vectors
        known_vectors = []
        unknown_vectors = []
        for vec in self.vectors:
            if self._is_vector_fully_known(vec):
                known_vectors.append(vec)
            else:
                unknown_vectors.append(vec)

        # Check if we have a known resultant (constraint for solving unknowns)
        resultant_is_known = self.resultant_vector is not None and self._is_vector_fully_known(self.resultant_vector)

        # Phase 1: Resolve all known vectors
        for vec in known_vectors:
            comp_result = self._resolve_known_vector(vec, context, output_unit)
            components.append(comp_result)

            # Get unit from magnitude
            unit = vec.magnitude.preferred.symbol if vec.magnitude.preferred else output_unit

            # Build solution step for this vector
            step = self._build_component_resolution_step(
                vec_name=vec.name or "F",
                magnitude=vec.magnitude,
                angle=vec.angle,
                angle_wrt=comp_result.angle_wrt,
                abs_angle_deg=comp_result.abs_angle_deg,
                x_comp=comp_result.x_component,
                y_comp=comp_result.y_component,
                unit=unit,
                equation_number=equation_number,
            )
            self.solving_history.append(step)
            equation_number += 1

        # Phase 2: If we have a known resultant, resolve it too
        resultant_components = None
        if resultant_is_known:
            resultant_components = self._resolve_known_vector(self.resultant_vector, context, output_unit)
            # Add step for resultant resolution
            unit = self.resultant_vector.magnitude.preferred.symbol if self.resultant_vector.magnitude.preferred else output_unit
            step = self._build_component_resolution_step(
                vec_name=self.resultant_vector.name or "F_R",
                magnitude=self.resultant_vector.magnitude,
                angle=self.resultant_vector.angle,
                angle_wrt=resultant_components.angle_wrt,
                abs_angle_deg=resultant_components.abs_angle_deg,
                x_comp=resultant_components.x_component,
                y_comp=resultant_components.y_component,
                unit=unit,
                equation_number=equation_number,
            )
            self.solving_history.append(step)
            equation_number += 1

        # Phase 3: Solve for unknown vectors using equilibrium
        if unknown_vectors and resultant_is_known:
            # Sum of known vector components
            known_x_sum = sum(c.x_component.magnitude() for c in components)
            known_y_sum = sum(c.y_component.magnitude() for c in components)

            # Resultant components
            r_x = resultant_components.x_component.magnitude()
            r_y = resultant_components.y_component.magnitude()

            # For now, handle the case of a single unknown vector
            if len(unknown_vectors) == 1:
                unknown_vec = unknown_vectors[0]
                unit = output_unit

                # Solve: F_unknown = F_R - sum(F_known)
                unknown_x = r_x - known_x_sum
                unknown_y = r_y - known_y_sum

                unknown_x_qty = Q(unknown_x, unit)
                unknown_y_qty = Q(unknown_y, unit)

                # Compute magnitude and angle
                unknown_mag = sqrt(unknown_x_qty * unknown_x_qty + unknown_y_qty * unknown_y_qty)
                unknown_angle = atan2(unknown_y_qty, unknown_x_qty)

                # Ensure we have Quantity objects
                if not isinstance(unknown_mag, Quantity):
                    unknown_mag = unknown_mag.evaluate({}) if hasattr(unknown_mag, "evaluate") else Q(float(unknown_mag), unit)
                if not isinstance(unknown_angle, Quantity):
                    unknown_angle = unknown_angle.evaluate({}) if hasattr(unknown_angle, "evaluate") else Q(float(unknown_angle), "radian")

                # Get the reference axis for the unknown vector
                wrt = unknown_vec.wrt if isinstance(unknown_vec.wrt, str) else "+x"
                abs_angle_deg = unknown_angle.to_unit.degree.magnitude()

                # Check if wrt is a relative reference to another vector (like "F_R")
                # If so, convert the absolute angle to a relative angle from that vector
                relative_angle = unknown_angle
                if isinstance(wrt, str) and wrt in context:
                    # wrt is a string name referencing another vector - compute relative angle
                    # Use CLOCKWISE direction to express angles > 180° as negative
                    ref_vec = context[wrt]
                    relative_angle = get_relative_angle(
                        unknown_angle,
                        wrt=ref_vec,
                        coordinate_system=unknown_vec.coordinate_system,
                        angle_dir=AngleDirection.CLOCKWISE,
                    )

                # Create component result for unknown vector
                unknown_comp = ComponentResult(
                    vector_name=unknown_vec.name or "F",
                    magnitude=unknown_mag,
                    angle=relative_angle,
                    angle_wrt=wrt,
                    abs_angle_deg=abs_angle_deg,
                    x_component=unknown_x_qty,
                    y_component=unknown_y_qty,
                )
                components.append(unknown_comp)

                # Build solution step for solving the unknown
                step = self._build_unknown_vector_step(
                    vec_name=unknown_vec.name or "F",
                    known_components=[(c.vector_name, c.x_component, c.y_component) for c in components[:-1]],
                    resultant_x=resultant_components.x_component,
                    resultant_y=resultant_components.y_component,
                    unknown_x=unknown_x_qty,
                    unknown_y=unknown_y_qty,
                    unknown_mag=unknown_mag,
                    unknown_angle_deg=abs_angle_deg,
                    unit=unit,
                    equation_number=equation_number,
                )
                self.solving_history.append(step)
                equation_number += 1
            else:
                raise ValueError(f"Cannot solve for {len(unknown_vectors)} unknown vectors. Currently only single unknown vector is supported.")

        # Compute resultant if requested
        resultant = None
        if self.compute_resultant and components:
            # Sum x and y components
            x_sum = sum(c.x_component.value for c in components)
            y_sum = sum(c.y_component.value for c in components)

            # Get unit from first component
            unit = components[0].x_component.preferred.symbol if components[0].x_component.preferred else output_unit

            x_sum_qty = Q(x_sum, unit)
            y_sum_qty = Q(y_sum, unit)

            # Build step for component sum
            sum_step = self._build_resultant_sum_step(
                components=components,
                x_sum=x_sum_qty,
                y_sum=y_sum_qty,
                unit=unit,
                equation_number=equation_number,
            )
            self.solving_history.append(sum_step)
            equation_number += 1

            # Compute resultant magnitude and angle
            r_mag = sqrt(x_sum_qty * x_sum_qty + y_sum_qty * y_sum_qty)
            r_angle = atan2(y_sum_qty, x_sum_qty)

            # Ensure we have Quantity objects
            if not isinstance(r_mag, Quantity):
                r_mag = r_mag.evaluate({}) if hasattr(r_mag, "evaluate") else Q(float(r_mag), unit)
            if not isinstance(r_angle, Quantity):
                r_angle = r_angle.evaluate({}) if hasattr(r_angle, "evaluate") else Q(float(r_angle), "radian")

            # Build step for magnitude calculation
            mag_step = self._build_magnitude_step(
                x_sum=x_sum_qty,
                y_sum=y_sum_qty,
                magnitude=r_mag,
                unit=unit,
                equation_number=equation_number,
            )
            self.solving_history.append(mag_step)
            equation_number += 1

            # Build step for direction calculation
            dir_step = self._build_direction_step(
                x_sum=x_sum_qty,
                y_sum=y_sum_qty,
                angle=r_angle,
                unit=unit,
                equation_number=equation_number,
            )
            self.solving_history.append(dir_step)

            resultant = ResultantResult(
                x_sum=x_sum_qty,
                y_sum=y_sum_qty,
                magnitude=r_mag,
                angle=r_angle,
            )

        self._result = RectangularMethodResult(
            components=components,
            resultant=resultant,
            solving_history=self.solving_history.copy(),
        )

        self.is_solved = True
        return self._result

    def generate_report(self, output_path: str, format: str = "markdown") -> None:
        """
        Generate a report for this rectangular method problem.

        Args:
            output_path: Path for output file
            format: 'markdown', 'latex', or 'pdf'
        """
        from .cartesian_report import generate_report as gen_report

        gen_report(self, output_path, format=format)


def solve_class(problem_class: type, output_unit: str = "N", compute_resultant: bool | None = None) -> RectangularMethodProblem:
    """
    Solve a rectangular method problem defined as a class.

    Args:
        problem_class: Class with vector attributes
        output_unit: Unit for output values
        compute_resultant: Whether to compute the resultant. If None (default),
            auto-detects based on whether F_R is defined in the problem class.

    Returns:
        Solved RectangularMethodProblem instance
    """
    problem = RectangularMethodProblem()
    problem.name = getattr(problem_class, "name", problem_class.__name__)

    # Collect all Vector and VectorUnknown attributes
    has_resultant = False
    resultant_vec = None
    input_vectors = []
    for attr_name in dir(problem_class):
        if attr_name.startswith("_"):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, Vector | VectorUnknown):
            # Set the name if not already set
            if attr.name is None:
                attr.name = attr_name
            # Check if this is a resultant vector (named F_R)
            if attr_name == "F_R" or (attr.name and attr.name == "F_R"):
                has_resultant = True
                resultant_vec = attr
            else:
                input_vectors.append(attr)

    problem.vectors = input_vectors
    problem.resultant_vector = resultant_vec

    # Auto-detect compute_resultant if not specified
    if compute_resultant is None:
        problem.compute_resultant = has_resultant
    else:
        problem.compute_resultant = compute_resultant

    problem.solve(output_unit=output_unit)
    return problem
