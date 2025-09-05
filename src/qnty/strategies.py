"""
Strategy Pattern for Equation Processing and Expression Evaluation.

This module provides different strategies for processing equations and evaluating
expressions, replacing complex if-elif chains with extensible strategy objects.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .quantities.quantity import Quantity
from .quantities.quantity import TypeSafeVariable
from .constants import DIVISION_BY_ZERO_THRESHOLD
from .generated.units import DimensionlessUnits

if TYPE_CHECKING:
    from .equations.equation import Equation


class OperationStrategy(ABC):
    """Abstract base class for operation evaluation strategies."""
    
    @abstractmethod
    def can_handle(self, operator: str) -> bool:
        """Check if this strategy can handle the given operator."""
        pass
    
    @abstractmethod
    def evaluate(self, operator: str, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate the operation using this strategy."""
        pass


class ArithmeticOperationStrategy(OperationStrategy):
    """Strategy for arithmetic operations (+, -, *, /, **)."""
    
    def can_handle(self, operator: str) -> bool:
        """Check if this is an arithmetic operator."""
        return operator in {"+", "-", "*", "/", "**"}
    
    def evaluate(self, operator: str, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate arithmetic operations with fast paths for common cases."""
        if operator == "*":
            return self._evaluate_multiplication(left_val, right_val)
        elif operator == "+":
            return self._evaluate_addition(left_val, right_val)
        elif operator == "-":
            return self._evaluate_subtraction(left_val, right_val)
        elif operator == "/":
            return self._evaluate_division(left_val, right_val)
        elif operator == "**":
            return self._evaluate_power(left_val, right_val)
        else:
            raise ValueError(f"Unknown arithmetic operator: {operator}")
    
    def _evaluate_multiplication(self, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate multiplication with fast paths."""
        # Fast path for multiplication by 1
        if right_val.value == 1.0:
            return left_val
        elif left_val.value == 1.0:
            return right_val
        # Fast path for multiplication by 0
        elif right_val.value == 0.0 or left_val.value == 0.0:
            return Quantity(0.0, left_val.unit if right_val.value == 0.0 else right_val.unit)
        return left_val * right_val
    
    def _evaluate_addition(self, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate addition with fast paths."""
        # Fast path for addition with 0
        if right_val.value == 0.0:
            return left_val
        elif left_val.value == 0.0:
            return right_val
        return left_val + right_val
    
    def _evaluate_subtraction(self, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate subtraction with fast paths."""
        # Fast path for subtraction with 0
        if right_val.value == 0.0:
            return left_val
        return left_val - right_val
    
    def _evaluate_division(self, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate division with zero checking."""
        # Check for division by zero
        if abs(right_val.value) < DIVISION_BY_ZERO_THRESHOLD:
            raise ValueError(f"Division by zero: {left_val} / {right_val}")
        # Fast path for division by 1
        if right_val.value == 1.0:
            return left_val
        return left_val / right_val
    
    def _evaluate_power(self, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate power operations with fast paths."""
        # For power, right side should be dimensionless
        if isinstance(right_val.value, int | float):
            # Fast paths for common exponents
            if right_val.value == 1.0:
                return left_val
            elif right_val.value == 0.0:
                return Quantity(1.0, DimensionlessUnits.dimensionless)
            elif right_val.value == 2.0:
                return left_val * left_val  # Use multiplication for squaring

            if right_val.value < 0 and left_val.value < 0:
                raise ValueError(f"Negative base with negative exponent: {left_val.value}^{right_val.value}")
            result_value = left_val.value**right_val.value
            # For power operations, we need to handle units carefully
            # This is a simplified implementation
            return Quantity(result_value, left_val.unit)
        else:
            raise ValueError("Exponent must be dimensionless number")


class ComparisonOperationStrategy(OperationStrategy):
    """Strategy for comparison operations (<, <=, >, >=, ==, !=)."""
    
    def can_handle(self, operator: str) -> bool:
        """Check if this is a comparison operator."""
        return operator in {"<", "<=", ">", ">=", "==", "!="}
    
    def evaluate(self, operator: str, left_val: Quantity, right_val: Quantity) -> Quantity:
        """Evaluate comparison operations."""
        try:
            # Convert to same units for comparison if needed
            if left_val._dimension_sig != right_val._dimension_sig:
                raise ValueError(f"Cannot compare incompatible dimensions: {left_val} {operator} {right_val}")
            
            # Convert right to left's unit for comparison
            right_converted = right_val.to(left_val.unit)
            
            # Perform comparison
            left_value = left_val.value
            right_value = right_converted.value
            
            if operator == "<":
                result = left_value < right_value
            elif operator == "<=":
                result = left_value <= right_value
            elif operator == ">":
                result = left_value > right_value
            elif operator == ">=":
                result = left_value >= right_value
            elif operator == "==":
                result = abs(left_value - right_value) < 1e-10
            elif operator == "!=":
                result = abs(left_value - right_value) >= 1e-10
            else:
                raise ValueError(f"Unknown comparison operator: {operator}")
            
            # Return dimensionless quantity (1.0 for True, 0.0 for False)
            return Quantity(1.0 if result else 0.0, DimensionlessUnits.dimensionless)
            
        except Exception as e:
            raise ValueError(f"Error in comparison {left_val} {operator} {right_val}: {e}") from e


class OperationStrategyManager:
    """
    Manager class that coordinates different operation strategies.
    
    This replaces the large if-elif chains in the original BinaryOperation.evaluate()
    method with a clean strategy pattern.
    """
    
    def __init__(self):
        """Initialize with default strategies."""
        self._strategies: list[OperationStrategy] = [
            ArithmeticOperationStrategy(),
            ComparisonOperationStrategy(),
        ]
    
    def register_strategy(self, strategy: OperationStrategy) -> None:
        """Register a new operation strategy."""
        self._strategies.append(strategy)
    
    def evaluate_operation(self, operator: str, left_val: Quantity, right_val: Quantity) -> Quantity:
        """
        Evaluate an operation using the appropriate strategy.
        
        Args:
            operator: The operator string
            left_val: Left operand value
            right_val: Right operand value
            
        Returns:
            Result of the operation
            
        Raises:
            ValueError: If no strategy can handle the operator
        """
        for strategy in self._strategies:
            if strategy.can_handle(operator):
                return strategy.evaluate(operator, left_val, right_val)
        
        raise ValueError(f"No strategy available for operator: {operator}")


class EquationSolvingStrategy(ABC):
    """Abstract base class for equation solving strategies."""
    
    @abstractmethod
    def can_solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> bool:
        """Check if this strategy can solve the equation for the target variable."""
        pass
    
    @abstractmethod
    def solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> TypeSafeVariable:
        """Solve the equation for the target variable using this strategy."""
        pass


class DirectAssignmentSolvingStrategy(EquationSolvingStrategy):
    """Strategy for solving direct assignment equations (var = expression)."""
    
    def can_solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> bool:
        """Check if this is a direct assignment equation."""
        from .expressions import VariableReference
        
        # Direct assignment case: lhs is the target variable
        return (isinstance(equation.lhs, VariableReference) and 
                equation.lhs.name == target_var)
    
    def solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> TypeSafeVariable:
        """Solve direct assignment equation."""
        # Direct assignment: target_var = rhs
        result_qty = equation.rhs.evaluate(variable_values)

        # Update existing variable object to preserve references
        var_obj = variable_values.get(target_var)
        if var_obj is not None:
            # Convert result to the target variable's original unit if it had one
            if var_obj.quantity is not None and var_obj.quantity.unit is not None:
                try:
                    result_qty = result_qty.to(var_obj.quantity.unit)
                except (ValueError, TypeError, AttributeError):
                    # Log specific conversion issues but continue with calculated unit
                    pass

            var_obj.quantity = result_qty
            var_obj.is_known = True
            return var_obj

        # Create new variable if not found - this shouldn't happen in normal usage
        raise ValueError(f"Variable '{target_var}' not found in variable_values")


class AlgebraicSolvingStrategy(EquationSolvingStrategy):
    """Strategy for solving equations that require algebraic manipulation."""
    
    def can_solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> bool:
        """Check if equation can be solved algebraically."""
        # For now, we only support direct assignment
        # Future: add support for simple algebraic manipulation
        return False
    
    def solve(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> TypeSafeVariable:
        """Solve equation using algebraic manipulation."""
        raise NotImplementedError("Algebraic solving not yet implemented")


class EquationSolvingManager:
    """
    Manager class that coordinates different equation solving strategies.
    
    This replaces the complex solving logic in the original Equation.solve_for()
    method with extensible strategies.
    """
    
    def __init__(self):
        """Initialize with default solving strategies."""
        self._strategies: list[EquationSolvingStrategy] = [
            DirectAssignmentSolvingStrategy(),
            AlgebraicSolvingStrategy(),  # For future extension
        ]
    
    def register_strategy(self, strategy: EquationSolvingStrategy) -> None:
        """Register a new equation solving strategy."""
        self._strategies.append(strategy)
    
    def solve_equation(self, equation: "Equation", target_var: str, variable_values: dict[str, TypeSafeVariable]) -> TypeSafeVariable:
        """
        Solve an equation using the appropriate strategy.
        
        Args:
            equation: The equation to solve
            target_var: Variable to solve for
            variable_values: Dictionary of variable values
            
        Returns:
            The solved variable
            
        Raises:
            ValueError: If no strategy can solve the equation
        """
        if target_var not in equation.variables:
            raise ValueError(f"Variable '{target_var}' not found in equation")
        
        for strategy in self._strategies:
            if strategy.can_solve(equation, target_var, variable_values):
                return strategy.solve(equation, target_var, variable_values)
        
        raise NotImplementedError(f"Cannot solve for {target_var} in equation {equation}. "
                                f"Only direct assignment equations (var = expression) are supported.")


# Global instances for easy access
_operation_manager = OperationStrategyManager()
_equation_solver = EquationSolvingManager()


def get_operation_manager() -> OperationStrategyManager:
    """Get the global operation strategy manager."""
    return _operation_manager


def get_equation_solver() -> EquationSolvingManager:
    """Get the global equation solving manager."""
    return _equation_solver