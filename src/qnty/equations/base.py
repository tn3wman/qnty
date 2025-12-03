"""
Base classes for the equations module.

This module provides the foundation for reusable equation classes that
generate solution steps dynamically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class SolutionStepBuilder:
    """
    Builder for creating solution steps with consistent formatting.

    This class generates step dictionaries that are compatible with the
    existing report generation system.
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

    def build(self) -> dict[str, Any]:
        """
        Convert to dictionary format for the report system.

        Only includes non-empty fields to keep dictionaries clean.
        Uses field names compatible with ReportBuilder._extract_solution_steps().

        Returns:
            Dictionary with non-empty step fields
        """
        result = {}
        if self.target:
            result["target"] = self.target
            result["target_variable"] = self.target  # For report_ir.py compatibility
        if self.method:
            result["method"] = self.method
        if self.description:
            result["description"] = self.description
        if self.equation is not None:
            result["equation"] = self.equation
            result["equation_str"] = self.equation  # For report compatibility
        if self.equation_for_list is not None:
            result["equation_for_list"] = self.equation_for_list
        if self.substitution is not None:
            result["substitution"] = self.substitution
            result["substituted_equation"] = self.substitution  # For report compatibility
        if self.result_value is not None:
            result["result_value"] = self.result_value
        if self.result_unit:
            result["result_unit"] = self.result_unit
        if self.details:
            result["details"] = self.details
        return result


def latex_name(name: str) -> str:
    """Format a name for LaTeX (convert F_BA to F_{BA} for proper subscripts).

    Only adds braces for multi-character subscripts. Single-character subscripts
    like F_1 or F_R are left unchanged for cleaner output.
    """
    if "_" in name:
        parts = name.split("_", 1)
        subscript = parts[1]
        # Only add braces for multi-character subscripts
        if len(subscript) > 1:
            return f"{parts[0]}_{{{subscript}}}"
    return name


def format_angle(angle: float | "Quantity", precision: int = 0) -> str:
    """Format an angle for display with LaTeX degree notation.

    Args:
        angle: Angle value - either a float (assumed degrees) or a Quantity
        precision: Number of decimal places

    Returns:
        LaTeX-formatted angle string
    """
    # Handle Quantity objects - convert to degrees and extract value
    if hasattr(angle, "to_unit") and hasattr(angle, "magnitude"):
        angle_qty = angle.to_unit.degree
        angle_deg = angle_qty.magnitude() if angle_qty.value is not None else 0.0
    else:
        angle_deg = float(angle)

    if precision == 0:
        return f"{angle_deg:.0f}^{{\\circ}}"
    return f"{angle_deg:.{precision}f}^{{\\circ}}"


def format_magnitude(value: float, unit: str = "", precision: int = 1) -> str:
    """Format a magnitude value with optional unit."""
    if unit:
        return f"{value:.{precision}f}\\ \\text{{{unit}}}"
    return f"{value:.{precision}f}"


class EquationBase(ABC):
    """
    Abstract base class for equations that generate solution steps.

    Subclasses must implement:
    - solve(): Perform the computation and return (result, steps)
    - equation_string(): Return the equation for the "Equations Used" section
    """

    def __init__(
        self,
        target: str,
        unit: str = "N",
        angle_unit: str = "degree",
    ):
        """
        Initialize the equation.

        Args:
            target: Name of the variable being solved for
            unit: Unit for force/magnitude values
            angle_unit: Unit for angle values
        """
        self.target = target
        self.unit = unit
        self.angle_unit = angle_unit
        self._steps: list[dict[str, Any]] = []

    @abstractmethod
    def solve(self) -> tuple[float, list[dict[str, Any]]]:
        """
        Solve the equation and generate solution steps.

        Returns:
            Tuple of (result_value, list_of_step_dicts)
        """
        ...

    @abstractmethod
    def equation_string(self) -> str:
        """
        Return the equation string for the "Equations Used" section.

        Returns:
            Formatted equation string
        """
        ...

    def _add_step(self, step: SolutionStepBuilder) -> None:
        """Add a solution step to the internal list."""
        self._steps.append(step.build())

    def _clear_steps(self) -> None:
        """Clear accumulated solution steps."""
        self._steps = []

    def get_steps(self) -> list[dict[str, Any]]:
        """Return the accumulated solution steps."""
        return self._steps.copy()
