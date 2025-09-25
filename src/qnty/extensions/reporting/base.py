"""
Base class for report generation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ReportStep:
    """Represents a single step in the solution process."""

    equation_name: str
    equation_str: str
    substituted_equation: str
    calculation_steps: list[str]
    result_value: Any
    result_unit: str


class ReportGenerator(ABC):
    """Abstract base class for report generators."""

    def __init__(self, problem: Any):
        """
        Initialize the report generator.

        Args:
            problem: Solved Problem instance from qnty library
        """
        if not problem.is_solved:
            raise ValueError("Problem must be solved before generating a report")

        self.problem = problem
        self.known_variables = problem.get_known_variables()
        self.unknown_variables = problem.get_unknown_variables()
        self.equations = problem.equations
        self.solving_history = getattr(problem, "solving_history", [])

    @abstractmethod
    def generate(self, output_path: str | Path) -> None:
        """
        Generate the report and save it to the specified path.

        Args:
            output_path: Path where the report should be saved
        """
        pass

    def _get_unit_string(self, var) -> str:
        """Get a readable unit string for a variable."""
        # Try to get output unit first (for display/reporting preference)
        if hasattr(var, "_output_unit") and var._output_unit:
            return var._output_unit.symbol if hasattr(var._output_unit, "symbol") else str(var._output_unit)

        # Try to get preferred unit second
        if hasattr(var, "preferred") and var.preferred:
            return var.preferred.symbol if hasattr(var.preferred, "symbol") else str(var.preferred)

        # If no preferred unit, try to get SI unit for the dimension
        if hasattr(var, "dim"):
            # Try to determine SI unit based on dimension
            if str(var.dim) == "Dim(-1, 1, -2, 0, 0, 0, 0) [3/50]":  # Pressure
                return "Pa"
            elif str(var.dim) == "Dim(1, 0, 0, 0, 0, 0, 0) [2/1]":  # Length
                return "m"
            elif str(var.dim) == "Dim(0, 0, 0, 0, 0, 0, 0) [1/1]":  # Dimensionless
                return ""

        return ""

    def _format_variable_table_data(self) -> tuple[list[dict], list[dict]]:
        """
        Format known and unknown variables for table display.

        Returns:
            Tuple of (known_vars_data, unknown_vars_data) where each is a list of dicts
        """
        known_data = []
        for symbol, var in self.known_variables.items():
            # Show original value in original unit, not SI-converted value
            if hasattr(var, "preferred") and var.preferred:
                # Get the value in the preferred unit
                original_value = var.value / var.preferred.si_factor
                value_str = f"{original_value:.6g}" if original_value is not None else "N/A"
                unit_str = var.preferred.symbol
            elif hasattr(var, "_unit") and var._unit:
                # Get the value in the original unit
                original_value = var.value / var._unit.si_factor
                value_str = f"{original_value:.6g}" if original_value is not None else "N/A"
                unit_str = var._unit.symbol
            else:
                # Fallback to SI value if no unit info available
                value_str = f"{var.value:.6g}" if var.value is not None else "N/A"
                unit_str = self._get_unit_string(var)

            known_data.append({"symbol": symbol, "name": getattr(var, "name", symbol), "value": value_str, "unit": unit_str})

        unknown_data = []
        # List unknown variables WITHOUT their calculated values (those go in the results section)
        for symbol, var in self.problem.variables.items():
            if symbol not in self.known_variables:
                # Get expected unit for the variable type
                unit_str = self._get_unit_string(var)
                unknown_data.append({"symbol": symbol, "name": getattr(var, "name", symbol), "unit": unit_str})

        return known_data, unknown_data

    def _format_equation_list(self) -> list[str]:
        """
        Format equations for display in the order they were solved.

        Returns:
            List of formatted equation strings in solving order
        """
        # If we have solving history, use that order
        if self.solving_history:
            equation_strs = []
            used_equations = set()  # Track equations we've already added

            for step_data in self.solving_history:
                equation_str = step_data.get("equation_str", "")
                if equation_str and equation_str not in used_equations:
                    equation_strs.append(equation_str)
                    used_equations.add(equation_str)

            # Add any remaining equations that weren't used in solving
            for eq in self.equations:
                eq_str = str(eq)
                if eq_str not in used_equations:
                    equation_strs.append(eq_str)

            return equation_strs

        # Fallback to original order if no solving history
        equation_strs = []
        for eq in self.equations:
            equation_strs.append(str(eq))
        return equation_strs

    def _extract_solution_steps(self) -> list[ReportStep]:
        """
        Extract solution steps from solving history.

        Returns:
            List of ReportStep objects representing the solution process
        """
        steps = []

        for step_data in self.solving_history:
            # Extract information from each solving step
            equation_name = step_data.get("equation", "Unknown")
            target_var = step_data.get("target", "Unknown")
            method = step_data.get("method", "Unknown")

            # Build step information
            equation_str = f"{target_var} = ..."
            if "equation_str" in step_data:
                equation_str = step_data["equation_str"]

            # Create substituted equation with values
            substituted = equation_str
            if "substituted" in step_data:
                substituted = step_data["substituted"]

            # Get the result
            result_value = step_data.get("result_value", "N/A")
            result_unit = step_data.get("result_unit", "")

            # Create calculation steps
            calc_steps = []
            if method == "direct":
                calc_steps.append("Direct substitution")
            elif method == "symbolic":
                calc_steps.append("Symbolic solving using SymPy")
            else:
                calc_steps.append(f"Method: {method}")

            if "details" in step_data:
                calc_steps.append(step_data["details"])

            steps.append(
                ReportStep(
                    equation_name=target_var,  # Use target_var instead of equation_name for cleaner step titles
                    equation_str=equation_str,
                    substituted_equation=substituted,
                    calculation_steps=calc_steps,
                    result_value=result_value,
                    result_unit=result_unit,
                )
            )

        return steps

    def _format_final_results(self) -> list[dict]:
        """
        Format final results summary.

        Returns:
            List of dicts containing final results
        """
        results = []
        for symbol, var in self.problem.variables.items():
            if symbol not in self.known_variables:
                # Get value in the correct display unit
                if var.value is not None:
                    # Check if we have an output unit specified
                    if hasattr(var, "_output_unit") and var._output_unit:
                        display_value = var._value_in_unit(var._output_unit) if hasattr(var, "_value_in_unit") else var.value
                        value_str = f"{display_value:.6g}"
                    else:
                        value_str = f"{var.value:.6g}"
                else:
                    value_str = "Unknown"
                unit_str = self._get_unit_string(var)
                results.append({"symbol": symbol, "name": getattr(var, "name", symbol), "value": value_str, "unit": unit_str})
        return results
