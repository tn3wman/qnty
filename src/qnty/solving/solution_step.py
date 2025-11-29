"""
SolutionStep dataclass for consistent step generation across solvers.

This module provides a structured representation for solution steps
that can be used by all solvers for consistent reporting and tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SolutionStep:
    """
    Represents a single step in the solution process.

    This dataclass provides a consistent structure for recording solution
    steps across different solvers (TriangleSolver, ComponentSolver,
    ParallelogramLawProblem, etc.).

    Attributes:
        target: The variable or quantity being solved for (e.g., "|F_R|", "theta")
        method: The solving method used (e.g., "Law of Cosines", "Component Summation")
        description: Human-readable description of what this step does
        equation: The equation being applied (for inline display)
        equation_for_list: The equation formatted for "Equations Used" section
        substitution: The equation with values substituted
        result_value: The computed result value as a string
        result_unit: The unit of the result (e.g., "N", "degrees")
        details: Additional details or notes about the step

    Examples:
        >>> step = SolutionStep(
        ...     target="|F_R|",
        ...     method="Law of Cosines",
        ...     description="Calculate resultant magnitude",
        ...     equation="F_R^2 = F_1^2 + F_2^2 - 2*F_1*F_2*cos(theta)",
        ...     substitution="F_R^2 = (100)^2 + (150)^2 - 2*(100)*(150)*cos(45)",
        ...     result_value="180.3",
        ...     result_unit="N"
        ... )
        >>> step_dict = step.to_dict()
    """

    target: str = ""
    method: str = ""
    description: str = ""
    equation: str | None = None
    equation_for_list: str | None = None
    substitution: str | None = None
    result_value: str | None = None
    result_unit: str = ""
    details: str = ""

    # Additional fields for specific solver types
    calculation: str | None = field(default=None, repr=False)
    calculation2: str | None = field(default=None, repr=False)
    result: str | None = field(default=None, repr=False)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary format for backward compatibility.

        Only includes non-empty fields to keep dictionaries clean.

        Returns:
            Dictionary with non-empty step fields
        """
        result = {}
        if self.target:
            result["target"] = self.target
        if self.method:
            result["method"] = self.method
        if self.description:
            result["description"] = self.description
        if self.equation is not None:
            result["equation"] = self.equation
        if self.equation_for_list is not None:
            result["equation_for_list"] = self.equation_for_list
        if self.substitution is not None:
            result["substitution"] = self.substitution
        if self.result_value is not None:
            result["result_value"] = self.result_value
        if self.result_unit:
            result["result_unit"] = self.result_unit
        if self.details:
            result["details"] = self.details
        if self.calculation is not None:
            result["calculation"] = self.calculation
        if self.calculation2 is not None:
            result["calculation2"] = self.calculation2
        if self.result is not None:
            result["result"] = self.result
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SolutionStep:
        """
        Create a SolutionStep from a dictionary.

        Args:
            data: Dictionary with step data

        Returns:
            SolutionStep instance
        """
        return cls(
            target=data.get("target", ""),
            method=data.get("method", ""),
            description=data.get("description", ""),
            equation=data.get("equation"),
            equation_for_list=data.get("equation_for_list"),
            substitution=data.get("substitution"),
            result_value=data.get("result_value"),
            result_unit=data.get("result_unit", ""),
            details=data.get("details", ""),
            calculation=data.get("calculation"),
            calculation2=data.get("calculation2"),
            result=data.get("result"),
        )


def create_law_of_cosines_step(
    target: str,
    side_a: str,
    side_b: str,
    side_c: str,
    angle_name: str,
    a_val: float,
    b_val: float,
    angle_val_deg: float,
    result_val: float,
    unit: str,
    description: str = "",
) -> SolutionStep:
    """
    Create a solution step for Law of Cosines calculation.

    Args:
        target: The side being solved for
        side_a, side_b, side_c: Names of the three sides
        angle_name: Name of the angle opposite to side_c
        a_val, b_val: Values of sides a and b
        angle_val_deg: Angle value in degrees
        result_val: Computed result value
        unit: Force unit symbol
        description: Optional description

    Returns:
        SolutionStep configured for Law of Cosines
    """
    return SolutionStep(
        target=target,
        method="Law of Cosines",
        description=description or f"Calculate {target} using Law of Cosines",
        equation_for_list=f"|{side_c}|^2 = |{side_a}|^2 + |{side_b}|^2 - 2*|{side_a}|*|{side_b}|*cos({angle_name})",
        substitution=(
            f"|{side_c}| = sqrt(({a_val:.1f})^2 + ({b_val:.1f})^2 - "
            f"2({a_val:.1f})({b_val:.1f})cos({angle_val_deg:.0f} deg))\n"
            f"= {result_val:.1f} {unit}"
        ),
    )


def create_law_of_sines_step(
    target: str,
    side_a: str,
    side_b: str,
    angle_a: str,
    angle_b: str,
    a_val: float,
    angle_a_deg: float,
    result_val_deg: float,
    description: str = "",
) -> SolutionStep:
    """
    Create a solution step for Law of Sines calculation.

    Args:
        target: The angle or side being solved for
        side_a, side_b: Names of the sides
        angle_a, angle_b: Names of the angles
        a_val: Value of known side
        angle_a_deg: Value of known angle in degrees
        result_val_deg: Computed result in degrees
        description: Optional description

    Returns:
        SolutionStep configured for Law of Sines
    """
    return SolutionStep(
        target=target,
        method="Law of Sines",
        description=description or f"Calculate {target} using Law of Sines",
        equation_for_list=f"sin({angle_a})/|{side_a}| = sin({angle_b})/|{side_b}|",
        substitution=(
            f"{target} = sin^-1({a_val:.1f}*sin({angle_a_deg:.0f} deg)/{result_val_deg:.1f})\n"
            f"= {result_val_deg:.1f} deg"
        ),
    )


def create_component_resolution_step(
    force_name: str,
    component: str,
    magnitude: float,
    angle_deg: float,
    result: float,
    unit: str,
) -> SolutionStep:
    """
    Create a solution step for component resolution.

    Args:
        force_name: Name of the force being resolved
        component: Component being calculated ('x' or 'y')
        magnitude: Force magnitude
        angle_deg: Force angle in degrees
        result: Computed component value
        unit: Force unit symbol

    Returns:
        SolutionStep configured for component resolution
    """
    trig_func = "cos" if component.lower() == "x" else "sin"
    return SolutionStep(
        target=f"{force_name}_{component}",
        method="component_resolution",
        description=f"Resolve {force_name} into {component} component",
        equation=f"{force_name}_{component} = |{force_name}| {trig_func}(theta)",
        substitution=f"{force_name}_{component} = {magnitude:.3f} {trig_func}({angle_deg:.1f} deg)",
        result_value=f"{result:.3f}",
        result_unit=unit,
    )
