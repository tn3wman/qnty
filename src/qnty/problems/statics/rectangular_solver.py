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
3. Reports show the step-by-step resolution process
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ...algebra.functions import atan2, cos, sin, sqrt
from ...core import Q
from ...core.quantity import Quantity
from ...equations.angle_finder import get_absolute_angle
from ...linalg.vector2 import Vector, VectorUnknown
from ...linalg.vectors2 import create_vectors_cartesian

if TYPE_CHECKING:
    pass


@dataclass
class ComponentResult:
    """Result of resolving a single vector into x and y components."""

    vector_name: str
    magnitude: Quantity
    angle: Quantity
    angle_wrt: str
    x_component: Quantity
    y_component: Quantity


@dataclass
class ResultantResult:
    """Result of computing the resultant from component sums."""

    x_sum: Quantity
    y_sum: Quantity
    magnitude: Quantity
    angle: Quantity


@dataclass
class RectangularMethodResult:
    """Complete result of rectangular method solving."""

    components: list[ComponentResult]
    resultant: ResultantResult | None = None
    solution_steps: list[dict[str, Any]] = field(default_factory=list)


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
    """

    name: str = "Rectangular Method Problem"

    def __init__(self):
        self.vectors: list[Vector | VectorUnknown] = []
        self.compute_resultant: bool = False
        self._result: RectangularMethodResult | None = None

    @property
    def result(self) -> RectangularMethodResult | None:
        return self._result

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

        Args:
            output_unit: Unit for output values (default: "N")

        Returns:
            RectangularMethodResult with all component values
        """
        components: list[ComponentResult] = []
        solution_steps: list[dict[str, Any]] = []

        # Resolve each vector into components
        for vec in self.vectors:
            if isinstance(vec, VectorUnknown):
                if vec.magnitude is ... or vec.angle is ...:
                    raise ValueError(f"Cannot resolve vector {vec.name} with unknown magnitude or angle")
                magnitude = vec.magnitude
                angle = vec.angle
            else:
                magnitude = vec.magnitude
                angle = vec.angle

            # Get the reference axis
            wrt = vec.wrt if isinstance(vec.wrt, str) else f"{vec.wrt.name}"

            # Compute absolute angle from +x axis
            abs_angle = get_absolute_angle(vec)

            # Compute components using qnty algebra
            x_comp = magnitude * cos(abs_angle)
            y_comp = magnitude * sin(abs_angle)

            # Ensure we have Quantity objects
            if not isinstance(x_comp, Quantity):
                x_comp = x_comp.evaluate({}) if hasattr(x_comp, 'evaluate') else Q(float(x_comp), output_unit)
            if not isinstance(y_comp, Quantity):
                y_comp = y_comp.evaluate({}) if hasattr(y_comp, 'evaluate') else Q(float(y_comp), output_unit)

            comp_result = ComponentResult(
                vector_name=vec.name or "F",
                magnitude=magnitude,
                angle=angle,
                angle_wrt=wrt,
                x_component=x_comp,
                y_component=y_comp,
            )
            components.append(comp_result)

            # Add solution step
            solution_steps.append({
                "type": "component_resolution",
                "vector_name": vec.name or "F",
                "magnitude": magnitude,
                "angle": angle,
                "angle_wrt": wrt,
                "abs_angle_deg": abs_angle.to_unit("degree").magnitude() if hasattr(abs_angle, "to_unit") else abs_angle,
                "x_component": x_comp,
                "y_component": y_comp,
            })

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

            # Compute resultant magnitude and angle
            r_mag = sqrt(x_sum_qty * x_sum_qty + y_sum_qty * y_sum_qty)
            r_angle = atan2(y_sum_qty, x_sum_qty)

            # Ensure we have Quantity objects
            if not isinstance(r_mag, Quantity):
                r_mag = r_mag.evaluate({}) if hasattr(r_mag, 'evaluate') else Q(float(r_mag), unit)
            if not isinstance(r_angle, Quantity):
                r_angle = r_angle.evaluate({}) if hasattr(r_angle, 'evaluate') else Q(float(r_angle), "radian")

            resultant = ResultantResult(
                x_sum=x_sum_qty,
                y_sum=y_sum_qty,
                magnitude=r_mag,
                angle=r_angle,
            )

            solution_steps.append({
                "type": "resultant_computation",
                "x_sum": x_sum_qty,
                "y_sum": y_sum_qty,
                "magnitude": r_mag,
                "angle": r_angle,
            })

        self._result = RectangularMethodResult(
            components=components,
            resultant=resultant,
            solution_steps=solution_steps,
        )

        return self._result


def solve_class(problem_class: type, output_unit: str = "N", compute_resultant: bool = False) -> RectangularMethodProblem:
    """
    Solve a rectangular method problem defined as a class.

    Args:
        problem_class: Class with vector attributes
        output_unit: Unit for output values
        compute_resultant: Whether to compute the resultant

    Returns:
        Solved RectangularMethodProblem instance
    """
    problem = RectangularMethodProblem()
    problem.name = getattr(problem_class, "name", problem_class.__name__)
    problem.compute_resultant = compute_resultant

    # Collect all Vector and VectorUnknown attributes
    for attr_name in dir(problem_class):
        if attr_name.startswith("_"):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, Vector | VectorUnknown):
            # Set the name if not already set
            if attr.name is None:
                attr.name = attr_name
            problem.vectors.append(attr)

    problem.solve(output_unit=output_unit)
    return problem
