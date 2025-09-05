"""
Example showing how to refactor BinaryOperation.evaluate() to use the strategy pattern.

This demonstrates the before/after comparison and shows how the strategy pattern
simplifies the complex evaluation logic.
"""

from typing import TYPE_CHECKING

from .strategies import get_operation_manager

if TYPE_CHECKING:
    from .quantities.quantity import Quantity
    from .quantities.unified_variable import UnifiedVariable


class BinaryOperationRefactoredExample:
    """
    Example of how BinaryOperation.evaluate() would be refactored using strategies.
    
    BEFORE: Large method with complex if-elif chains
    AFTER: Delegated to strategy manager with clean separation of concerns
    """
    
    def __init__(self, operator: str, left: "Expression", right: "Expression"):
        self.operator = operator
        self.left = left
        self.right = right
    
    def evaluate_before_refactoring(self, variable_values: dict[str, "UnifiedVariable"]) -> "Quantity":
        """
        BEFORE: Original complex evaluation method (simplified for example).
        
        Problems:
        - Long method with many responsibilities
        - Complex if-elif chains hard to extend
        - Arithmetic and comparison logic mixed together
        - Fast path optimizations scattered throughout
        - Difficult to add new operation types
        """
        left_val = self.left.evaluate(variable_values)
        right_val = self.right.evaluate(variable_values)
        
        # Long if-elif chain for different operations
        if self.operator == "*":
            # Fast path optimizations embedded in main logic
            if right_val.value == 1.0:
                return left_val
            elif left_val.value == 1.0:
                return right_val
            elif right_val.value == 0.0 or left_val.value == 0.0:
                # Complex zero handling logic...
                pass
            return left_val * right_val
        elif self.operator == "+":
            # More embedded fast path logic...
            if right_val.value == 0.0:
                return left_val
            elif left_val.value == 0.0:
                return right_val
            return left_val + right_val
        elif self.operator == "-":
            # Yet more embedded logic...
            if right_val.value == 0.0:
                return left_val
            return left_val - right_val
        # ... many more elif statements for /, **, <, <=, >, >=, ==, !=
        # This gets very long and hard to maintain!
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
    
    def evaluate_after_refactoring(self, variable_values: dict[str, "UnifiedVariable"]) -> "Quantity":
        """
        AFTER: Clean evaluation method using strategy pattern.
        
        Benefits:
        - Single responsibility: just coordinate evaluation
        - Extensible: new strategies can be added easily
        - Clean separation: arithmetic vs comparison logic separated
        - Fast paths encapsulated in appropriate strategies
        - Much shorter and easier to understand
        """
        # Evaluate operands
        left_val = self.left.evaluate(variable_values)
        right_val = self.right.evaluate(variable_values)
        
        # Delegate to appropriate strategy
        operation_manager = get_operation_manager()
        return operation_manager.evaluate_operation(self.operator, left_val, right_val)


class EquationRefactoredExample:
    """
    Example of how Equation.solve_for() would be refactored using strategies.
    
    BEFORE: Complex solving logic with if-elif chains
    AFTER: Delegated to strategy manager for clean extensibility
    """
    
    def solve_for_before_refactoring(self, target_var: str, variable_values: dict) -> "UnifiedVariable":
        """
        BEFORE: Original complex solving method.
        
        Problems:
        - Mixed responsibilities: validation + solving
        - Hard-coded solving approaches
        - Difficult to extend with new solving methods
        - Complex nested conditionals
        """
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' not found in equation")

        # Complex nested conditionals for different equation types
        if hasattr(self.lhs, 'name') and self.lhs.name == target_var:
            # Direct assignment logic embedded here...
            result_qty = self.rhs.evaluate(variable_values)
            var_obj = variable_values.get(target_var)
            if var_obj is not None:
                # Complex unit conversion logic...
                if var_obj.quantity is not None and var_obj.quantity.unit is not None:
                    try:
                        result_qty = result_qty.to(var_obj.quantity.unit)
                    except (ValueError, TypeError, AttributeError):
                        pass
                var_obj.quantity = result_qty
                var_obj.is_known = True
                return var_obj
            raise ValueError(f"Variable '{target_var}' not found")
        else:
            # More complex solving would go here...
            raise NotImplementedError("Only direct assignment supported")
    
    def solve_for_after_refactoring(self, target_var: str, variable_values: dict) -> "UnifiedVariable":
        """
        AFTER: Clean solving method using strategy pattern.
        
        Benefits:
        - Single responsibility: validate inputs and delegate
        - Extensible: new solving strategies can be added
        - Clean separation: different solving approaches isolated
        - Easy to test each strategy independently
        - Much shorter main method
        """
        from .strategies import get_equation_solver
        
        # Delegate to appropriate strategy
        equation_solver = get_equation_solver()
        return equation_solver.solve_equation(self, target_var, variable_values)


def demonstrate_strategy_benefits():
    """
    Demonstrate the benefits of the strategy pattern refactoring:
    
    1. **Extensibility**: New operation types or solving methods can be added
       by implementing new strategies without modifying existing code.
    
    2. **Single Responsibility**: Each strategy class has one clear responsibility.
    
    3. **Open/Closed Principle**: Open for extension (new strategies) but
       closed for modification (existing strategies don't change).
    
    4. **Testability**: Each strategy can be tested independently.
    
    5. **Maintainability**: Related logic is grouped together instead of
       scattered across large methods.
    
    6. **Performance**: Fast path optimizations are encapsulated where
       they belong rather than cluttering main logic.
    
    Example of adding a new operation type:
    
    ```python
    class LogicalOperationStrategy(OperationStrategy):
        def can_handle(self, operator: str) -> bool:
            return operator in {"and", "or", "not"}
        
        def evaluate(self, operator: str, left_val: Quantity, right_val: Quantity) -> Quantity:
            # Implementation for logical operations
            pass
    
    # Register the new strategy
    get_operation_manager().register_strategy(LogicalOperationStrategy())
    ```
    
    No changes needed to existing evaluation code!
    """
    pass


def usage_comparison():
    """
    Compare usage patterns before and after strategy refactoring.
    
    BEFORE: All logic embedded in single method
    - evaluate() method: ~100+ lines
    - solve_for() method: ~50+ lines
    - Hard to extend or modify
    - Complex testing due to many responsibilities
    
    AFTER: Clean delegation with focused strategies
    - evaluate() method: ~10 lines
    - solve_for() method: ~5 lines  
    - Easy to extend with new strategies
    - Simple unit testing for each strategy
    
    The strategy pattern transforms complex methods into simple coordinators
    while making the system much more extensible and maintainable.
    """
    pass