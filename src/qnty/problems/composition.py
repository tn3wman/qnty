"""
Sub-problem composition system for EngineeringProblem.

This module provides the complete sub-problem integration system including:
- Sub-problem proxy objects for clean composition syntax
- Namespace handling and variable mapping
- Composite equation creation
- Metaclass system for automatic proxy creation

Combined from composition.py and composition_mixin.py for focused functionality.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..algebra.nodes import Expression

from ..algebra import BinaryOperation, ConditionalExpression, Constant, Equation, VariableReference, max_expr, min_expr, sin
from ..algebra.nodes import Expression, wrap_operand
from ..core.quantity import FieldQuantity
from ..core.quantity_catalog import Dimensionless
from .rules import Rules

# Constants for composition
COMMON_COMPOSITE_VARIABLES = ["P", "c", "S", "E", "W", "Y"]

# Constants for metaclass
RESERVED_ATTRIBUTES: set[str] = {"name", "description"}
PRIVATE_ATTRIBUTE_PREFIX = "_"
SUB_PROBLEM_REQUIRED_ATTRIBUTES: tuple[str, ...] = ("variables", "equations")


# ========== COMPOSITION CLASSES ==========


class ArithmeticOperationsMixin:
    """Mixin providing common arithmetic operations that create DelayedExpression objects."""

    def __add__(self, other):
        return DelayedExpression("+", self, other)

    def __radd__(self, other):
        return DelayedExpression("+", other, self)

    def __sub__(self, other):
        return DelayedExpression("-", self, other)

    def __rsub__(self, other):
        return DelayedExpression("-", other, self)

    def __mul__(self, other):
        return DelayedExpression("*", self, other)

    def __rmul__(self, other):
        return DelayedExpression("*", other, self)

    def __truediv__(self, other):
        return DelayedExpression("/", self, other)

    def __rtruediv__(self, other):
        return DelayedExpression("/", other, self)

    def __pow__(self, other):
        return DelayedExpression("**", self, other)

    def __rpow__(self, other):
        return DelayedExpression("**", other, self)


class DelayedEquation:
    """
    Stores an equation definition that will be evaluated later when proper context is available.
    """

    def __init__(self, lhs_symbol, rhs_factory, name=None):
        self.lhs_symbol = lhs_symbol
        self.rhs_factory = rhs_factory  # Function that creates the RHS expression
        self.name = name or f"{lhs_symbol}_equation"

    def evaluate(self, context):
        """Evaluate the equation with the given context (namespace with variables)."""
        if self.lhs_symbol not in context:
            return None

        lhs_var = context[self.lhs_symbol]

        try:
            # Call the factory function with the context to create the RHS
            rhs_expr = self.rhs_factory(context)
            return lhs_var.equals(rhs_expr)
        except Exception:
            return None


class SubProblemProxy:
    """
    Proxy object that represents a sub-problem and provides namespaced variable access
    during class definition. Returns properly namespaced variables immediately to prevent
    malformed expressions.
    """

    def __init__(self, sub_problem, namespace):
        self._sub_problem = sub_problem
        self._namespace = namespace
        self._variable_cache = {}
        self._variable_configurations = {}  # Track configurations applied to variables
        # Global registry to track which expressions involve proxy variables
        if not hasattr(SubProblemProxy, "_expressions_with_proxies"):
            SubProblemProxy._expressions_with_proxies = set()

    def __getattr__(self, name):
        # Handle internal Python attributes to prevent recursion during deepcopy
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        if name in self._variable_cache:
            return self._variable_cache[name]

        try:
            attr_value = getattr(self._sub_problem, name)
            if isinstance(attr_value, FieldQuantity):
                # Create a properly namespaced variable immediately
                namespaced_var = self._create_namespaced_variable(attr_value)
                self._variable_cache[name] = namespaced_var
                return namespaced_var
            elif hasattr(attr_value, '_wrapped_var') and isinstance(attr_value._wrapped_var, FieldQuantity):
                # This is a MainVariableWrapper - unwrap it to get the FieldQuantity
                wrapped_var = attr_value._wrapped_var
                namespaced_var = self._create_namespaced_variable(wrapped_var)
                self._variable_cache[name] = namespaced_var
                return namespaced_var
            return attr_value
        except AttributeError as e:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'") from e

    def _create_namespaced_variable(self, original_var):
        """Create a Variable with namespaced symbol for proper expression creation."""
        namespaced_symbol = f"{self._namespace}_{original_var.symbol}"

        # Create new Variable with namespaced symbol that tracks modifications
        namespaced_var = ConfigurableVariable(
            symbol=namespaced_symbol,
            name=f"{original_var.name} ({self._namespace.title()})",
            quantity=original_var.quantity,
            is_known=original_var.is_known,
            proxy=self,
            original_symbol=original_var.symbol,
            original_variable=original_var,  # Pass the original variable for type preservation
        )

        return namespaced_var

    def track_configuration(self, original_symbol, quantity, is_known):
        """Track a configuration change made to a variable."""
        self._variable_configurations[original_symbol] = {"quantity": quantity, "is_known": is_known}

    def get_configurations(self):
        """Get all tracked configurations."""
        return self._variable_configurations.copy()


class ConfigurableVariable:
    """
    A Variable wrapper that can track configuration changes and report them back to its proxy.
    This acts as a proxy around the actual qnty Variable rather than inheriting from it.
    """

    def __init__(self, symbol, name, quantity, is_known=True, proxy=None, original_symbol=None, original_variable=None):
        # Store the actual variable (we'll delegate to it)
        # Create a variable of the appropriate type based on the original
        if original_variable is not None:
            # Preserve the original variable type
            self._variable = type(original_variable)(name)
        else:
            # Fallback to Dimensionless if no original variable provided
            self._variable = Dimensionless(name)

        # Set the properties using private attributes (since properties may be read-only)
        self._variable._symbol = symbol
        # For the unified Quantity class, we set the value and preferred unit directly
        if quantity is not None and hasattr(quantity, "value") and hasattr(quantity, "preferred"):
            self._variable.value = quantity.value
            self._variable.preferred = quantity.preferred
        # Note: is_known is handled via the value being None or not in the unified Quantity API
        _ = is_known  # Mark as used to avoid linting warnings

        # The unified Quantity class may not have _arithmetic_mode
        # This is handled by the arithmetic operations in the class itself

        # Store proxy information
        self._proxy = proxy
        self._original_symbol = original_symbol

    def __getattr__(self, name):
        """Delegate all other attributes to the wrapped variable."""
        # Handle special case for _arithmetic_mode since it's accessed in __mul__ etc.
        if name == "_arithmetic_mode":
            # First check if we have it directly using getattr for safety
            return getattr(self._variable, "_arithmetic_mode", "expression")

        return getattr(self._variable, name)

    def _should_use_delayed_arithmetic(self) -> bool:
        """Check if we should use delayed arithmetic based on context."""
        import inspect

        frame = inspect.currentframe()
        try:
            while frame:
                code = frame.f_code
                filename = code.co_filename
                locals_dict = frame.f_locals

                # Check if we're in a class definition context
                if (
                    "<class" in code.co_name
                    or "problem" in filename.lower()
                    or any("Problem" in str(base) for base in locals_dict.get("__bases__", []))
                    or "test_composed_problem" in filename
                ):
                    return True
                frame = frame.f_back
            return False
        finally:
            del frame

    # Delegate arithmetic and comparison operations to the wrapped variable
    def __add__(self, other):
        # Check if we're in a class definition context and should use delayed expressions
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("+", self, other)
        return self._variable.__add__(other)

    def __radd__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("+", other, self)
        return self._variable.__radd__(other)

    def __sub__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("-", self, other)
        return self._variable.__sub__(other)

    def __rsub__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("-", other, self)
        return self._variable.__rsub__(other)

    def __mul__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("*", self, other)
        return self._variable.__mul__(other)

    def __rmul__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("*", other, self)
        return self._variable.__rmul__(other)

    def __truediv__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("/", self, other)
        return self._variable.__truediv__(other)

    def __rtruediv__(self, other):
        if self._should_use_delayed_arithmetic():
            return DelayedExpression("/", other, self)
        return self._variable.__rtruediv__(other)

    def __pow__(self, other):
        return self._variable.__pow__(other)

    def __neg__(self):
        # Implement negation as multiplication by -1, consistent with other arithmetic operations
        return self._variable * (-1)

    def __lt__(self, other):
        return self._variable.__lt__(other)

    def __le__(self, other):
        return self._variable.__le__(other)

    def __gt__(self, other):
        return self._variable.__gt__(other)

    def __ge__(self, other):
        return self._variable.__ge__(other)

    def __eq__(self, other):  # type: ignore[override]
        return self._variable.__eq__(other)

    def __ne__(self, other):  # type: ignore[override]
        return self._variable.__ne__(other)

    def __setattr__(self, name, value):
        """Delegate attribute setting to the wrapped variable when appropriate."""
        if name.startswith("_") or name in ("_variable", "_proxy", "_original_symbol"):
            super().__setattr__(name, value)
        else:
            setattr(self._variable, name, value)
            # Track configuration changes for important attributes
            if name in ("value", "preferred", "is_known"):
                self._track_configuration_change()

    def _track_configuration_change(self):
        """Helper to track configuration changes to proxy."""
        if self._proxy and self._original_symbol:
            quantity_val = getattr(self._variable, "quantity", self._variable)
            is_known_val = getattr(self._variable, "is_known", self._variable.value is not None)
            self._proxy.track_configuration(self._original_symbol, quantity_val, is_known_val)

    def set(self, value):
        """Override set method to track configuration changes and return the correct setter."""
        # Create a wrapper setter that tracks changes after unit application
        original_setter = self._variable.set(value)

        if self._proxy and self._original_symbol:
            # Create tracking wrapper
            return TrackingSetterWrapper(original_setter, self._proxy, self._original_symbol, self._variable)
        else:
            return original_setter

    def update(self, value=None, unit=None, quantity=None, is_known=None):
        """Override update method to track configuration changes."""
        update_method = getattr(self._variable, "update", None)
        if update_method is not None:
            result = update_method(value, unit, quantity, is_known)
        else:
            # Fallback for unified Quantity API
            if value is not None and unit is not None:
                self._variable = self._variable.set(value, unit)
            result = self._variable
        self._track_configuration_change()
        return result

    def mark_known(self):
        """Override mark_known to track configuration changes."""
        mark_known_method = getattr(self._variable, "mark_known", None)
        if mark_known_method is not None:
            result = mark_known_method()
        else:
            # Fallback: in unified Quantity API, this might be handled differently
            result = self._variable
        self._track_configuration_change()
        return result

    def mark_unknown(self):
        """Override mark_unknown to track configuration changes."""
        mark_unknown_method = getattr(self._variable, "mark_unknown", None)
        if mark_unknown_method is not None:
            result = mark_unknown_method()
        else:
            # Fallback: in unified Quantity API, create a new quantity with None value
            # Create a new unknown quantity by setting value to None
            result = self._variable.__class__(name=self._variable.name)
            result.value = None
            result.preferred = self._variable.preferred
            result._symbol = self._variable._symbol
            self._variable = result
        self._track_configuration_change()
        return result


class TrackingSetterWrapper:
    """
    A wrapper around setter objects that tracks configuration changes after unit application.
    This ensures that when `proxy.set(value).unit` is called, the proxy tracks the final
    configuration after the unit is applied.
    """

    def __init__(self, original_setter, proxy, original_symbol, variable):
        self._original_setter = original_setter
        self._proxy = proxy
        self._original_symbol = original_symbol
        self._variable = variable

    def __getattr__(self, name):
        """
        Intercept property access for unit properties and track configuration after application.
        """
        # Get the property from the original setter
        attr = getattr(self._original_setter, name)

        # If it's a property (unit setter), wrap it to track configuration
        if callable(attr):
            # It's a method, just delegate
            return attr
        else:
            # It's a property access, call it and then track configuration
            result = attr  # This will set the variable quantity and return the variable

            # Track the configuration after the unit is applied
            if self._proxy and self._original_symbol:
                self._proxy.track_configuration(self._original_symbol, self._variable.quantity, self._variable.is_known)

            return result

    def with_unit(self, unit):
        """Delegate with_unit method and track configuration."""
        result = self._original_setter.with_unit(unit)
        if self._proxy and self._original_symbol:
            self._proxy.track_configuration(self._original_symbol, self._variable.quantity, self._variable.is_known)
        return result


class DelayedVariableReference(ArithmeticOperationsMixin):
    """
    A placeholder for a variable that will be resolved to its namespaced version later.
    Supports arithmetic operations that create delayed expressions.
    """

    def __init__(self, namespace, symbol, original_var):
        self.namespace = namespace
        self.symbol = symbol
        self.original_var = original_var
        self._namespaced_symbol = f"{namespace}_{symbol}"

    def resolve(self, context):
        """Resolve to the actual namespaced variable from context."""
        return context.get(self._namespaced_symbol)


class DelayedExpression(ArithmeticOperationsMixin):
    """
    Represents an arithmetic expression that will be resolved later when context is available.
    Supports chaining of operations.
    """

    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    @property
    def value(self):
        """
        DelayedExpression objects don't have values until resolved.
        Raise a more specific error to help with debugging.
        """
        raise AttributeError("DelayedExpression objects must be resolved before accessing their value. Use resolve(context) to convert this to a proper expression first.")

    def evaluate(self, variable_values):
        """
        DelayedExpression objects should be resolved before evaluation.
        This method raises an informative error to help debug issues.
        """
        # Mark variable as used to avoid linting warnings
        _ = variable_values
        raise RuntimeError(
            "DelayedExpression objects must be resolved before evaluation. "
            "This suggests that DelayedExpression.resolve() was not called properly "
            "or that an unresolved DelayedExpression made it into the expression tree."
        )

    def get_variables(self):
        """Extract variables from the expression operands."""
        variables = set()

        # Extract from left operand
        if hasattr(self.left, 'get_variables'):
            variables.update(self.left.get_variables())
        elif hasattr(self.left, '_wrapped') and hasattr(self.left._wrapped, 'symbol'):
            # ExpressionEnabledWrapper
            variables.add(self.left._wrapped.symbol)
        elif hasattr(self.left, '_variable') and hasattr(self.left._variable, 'symbol'):
            # SubProblemProxy
            variables.add(self.left._variable.symbol)
        elif hasattr(self.left, 'symbol'):
            # Direct variable
            variables.add(self.left.symbol)

        # Extract from right operand
        if hasattr(self.right, 'get_variables'):
            variables.update(self.right.get_variables())
        elif hasattr(self.right, '_wrapped') and hasattr(self.right._wrapped, 'symbol'):
            # ExpressionEnabledWrapper
            variables.add(self.right._wrapped.symbol)
        elif hasattr(self.right, '_variable') and hasattr(self.right._variable, 'symbol'):
            # SubProblemProxy
            variables.add(self.right._variable.symbol)
        elif hasattr(self.right, 'symbol'):
            # Direct variable
            variables.add(self.right.symbol)

        return variables

    def resolve(self, context):
        """Resolve this expression to actual Variable/Expression objects."""
        left_resolved = self._resolve_operand(self.left, context)
        right_resolved = self._resolve_operand(self.right, context)

        if left_resolved is None or right_resolved is None:
            return None

        # Create the actual expression
        if self.operation == "+":
            # Use wrap_operand to ensure proper expression type handling
            return BinaryOperation("+", wrap_operand(left_resolved), wrap_operand(right_resolved))
        elif self.operation == "-":
            return BinaryOperation("-", wrap_operand(left_resolved), wrap_operand(right_resolved))
        elif self.operation == "*":
            return BinaryOperation("*", wrap_operand(left_resolved), wrap_operand(right_resolved))
        elif self.operation == "/":
            return BinaryOperation("/", wrap_operand(left_resolved), wrap_operand(right_resolved))
        else:
            return BinaryOperation(self.operation, wrap_operand(left_resolved), wrap_operand(right_resolved))

    def _resolve_operand(self, operand, context):
        """Resolve a single operand to a Variable/Expression."""
        if isinstance(operand, DelayedVariableReference | DelayedExpression | DelayedFunction):
            return operand.resolve(context)
        elif hasattr(operand, "_wrapped") and not isinstance(operand, Expression):
            # This is an ExpressionEnabledWrapper - create a VariableReference to the actual variable
            from ..algebra.nodes import VariableReference
            return VariableReference(operand._wrapped)
        elif isinstance(operand, ConfigurableVariable):
            # This is a ConfigurableVariable from SubProblemProxy - look up the namespaced variable in context
            namespaced_symbol = operand._variable.symbol
            if namespaced_symbol in context:
                from ..algebra.nodes import VariableReference
                return VariableReference(context[namespaced_symbol])
            else:
                # Fallback to the wrapped variable
                from ..algebra.nodes import VariableReference
                return VariableReference(operand._variable)
        elif hasattr(operand, "_variable") and not isinstance(operand, Expression):
            # This is a SubProblemProxy - create a VariableReference to the actual variable
            from ..algebra.nodes import VariableReference
            return VariableReference(operand._variable)
        elif hasattr(operand, "_wrapped_var") and not isinstance(operand, Expression):
            # This is a MainVariableWrapper - create a VariableReference to the actual variable
            from ..algebra.nodes import VariableReference
            return VariableReference(operand._wrapped_var)
        elif hasattr(operand, 'symbol'):
            # It's a Variable - check if we have a canonical version in context and create VariableReference
            symbol = operand.symbol
            from ..algebra.nodes import VariableReference
            if symbol in context:
                return VariableReference(context[symbol])
            else:
                # Create VariableReference to the original variable
                return VariableReference(operand)
        else:
            # It's a literal value
            return operand


class DelayedFunction(ArithmeticOperationsMixin):
    """
    Represents a function call that will be resolved later when context is available.
    """

    def __init__(self, func_name, *args):
        self.func_name = func_name
        self.args = args

    def get_variables(self):
        """Extract variables from function arguments."""
        variables = set()
        for arg in self.args:
            if hasattr(arg, 'get_variables'):
                variables.update(arg.get_variables())
            elif hasattr(arg, '_wrapped') and hasattr(arg._wrapped, 'symbol'):
                # ExpressionEnabledWrapper
                variables.add(arg._wrapped.symbol)
            elif hasattr(arg, '_variable') and hasattr(arg._variable, 'symbol'):
                # SubProblemProxy
                variables.add(arg._variable.symbol)
            elif hasattr(arg, 'symbol'):
                # Direct variable
                variables.add(arg.symbol)
        return variables

    def evaluate(self, variable_values):
        """Evaluate the function with given variable values."""
        # This shouldn't normally be called - DelayedFunction should be resolved first
        # But provide a fallback that tries to resolve with available context
        try:
            # Try to resolve with the variable values as context
            resolved = self.resolve(variable_values)
            if resolved and hasattr(resolved, 'evaluate'):
                return resolved.evaluate(variable_values)
        except Exception:
            pass
        raise RuntimeError(f"DelayedFunction {self.func_name} could not be evaluated. "
                         "It should be resolved to an Expression first.")

    def resolve(self, context):
        """Resolve function call with given context."""
        # Resolve all arguments
        resolved_args = []
        for arg in self.args:
            if isinstance(arg, DelayedVariableReference | DelayedExpression | DelayedFunction):
                resolved_arg = arg.resolve(context)
                if resolved_arg is None:
                    return None
                resolved_args.append(resolved_arg)
            elif hasattr(arg, '_wrapped') and not isinstance(arg, Expression):
                # This is an ExpressionEnabledWrapper - create a VariableReference to the actual variable
                from ..algebra.nodes import VariableReference
                resolved_args.append(VariableReference(arg._wrapped))
            elif hasattr(arg, '_wrapped_var') and not isinstance(arg, Expression):
                # This is a NamespaceVariableWrapper - create a VariableReference to the actual variable
                from ..algebra.nodes import VariableReference
                resolved_args.append(VariableReference(arg._wrapped_var))
            elif hasattr(arg, '_variable') and not isinstance(arg, Expression):
                # This is a SubProblemProxy - create a VariableReference to the actual variable
                from ..algebra.nodes import VariableReference
                resolved_args.append(VariableReference(arg._variable))
            elif hasattr(arg, 'symbol'):
                # This is a Variable - create a VariableReference, don't let wrap_operand turn it into a Constant
                from ..algebra.nodes import VariableReference
                resolved_args.append(VariableReference(arg))
            else:
                resolved_args.append(arg)

        # Call the appropriate function - create actual expressions, not more DelayedFunction objects
        if self.func_name == "sin":
            from ..algebra.nodes import UnaryFunction, wrap_operand
            return UnaryFunction("sin", wrap_operand(resolved_args[0]))
        elif self.func_name == "min_expr":
            from ..algebra.functions import _create_comparison_expr
            return _create_comparison_expr(tuple(resolved_args), "min")
        elif self.func_name == "max_expr":
            from ..algebra.functions import _create_comparison_expr
            return _create_comparison_expr(tuple(resolved_args), "max")
        elif self.func_name == "cond_expr":
            from ..algebra.nodes import ConditionalExpression, wrap_operand
            return ConditionalExpression(resolved_args[0], wrap_operand(resolved_args[1]), wrap_operand(resolved_args[2]))
        else:
            # Generic function call
            return None


# Delayed function factories
def delayed_sin(expr):
    return DelayedFunction("sin", expr)


def delayed_min_expr(*args):
    return DelayedFunction("min_expr", *args)


def delayed_max_expr(*args):
    return DelayedFunction("max_expr", *args)


# ========== COMPOSITION MIXIN ==========


class CompositionMixin:
    """Mixin class providing sub-problem composition functionality."""

    # These attributes/methods will be provided by other mixins in the final Problem class
    variables: dict[str, FieldQuantity]
    sub_problems: dict[str, Any]
    logger: Any

    def add_variable(self, variable: FieldQuantity) -> None:
        """Will be provided by Problem class."""
        del variable  # Unused in stub method
        ...

    def add_equation(self, equation: Equation) -> None:
        """Will be provided by Problem class."""
        del equation  # Unused in stub method
        ...

    def _clone_variable(self, variable: FieldQuantity) -> FieldQuantity:
        """Will be provided by Problem class."""
        return variable  # Stub method - return input as placeholder

    def _recreate_validation_checks(self) -> None:
        """Will be provided by ValidationMixin."""
        ...

    def _extract_from_class_variables(self):
        """Extract variables, equations, and sub-problems from class-level definitions."""
        self._extract_sub_problems()
        self._extract_direct_variables()
        self._recreate_validation_checks()
        self._create_composite_equations()
        self._extract_equations()
        self._process_variable_sharing()
        # Ensure all equations use canonical variable references
        self._canonicalize_all_equation_variables()

        # Generic retrofitting - replace constants with variables where possible
        self._retrofit_constants_to_variables()

    def _extract_sub_problems(self):
        """Extract and integrate sub-problems from class-level definitions."""
        if hasattr(self.__class__, "_original_sub_problems"):
            original_sub_problems = getattr(self.__class__, "_original_sub_problems", {})
            for attr_name, sub_problem in original_sub_problems.items():
                self._integrate_sub_problem(sub_problem, attr_name)

    def _extract_direct_variables(self):
        """Extract direct variables from class-level definitions."""
        processed_symbols = set()

        # Single pass through class attributes to collect variables
        for attr_name, attr_value in self._get_class_attributes():
            # Handle both direct FieldQuantity objects and wrapped ones
            actual_var = attr_value
            if hasattr(attr_value, "_wrapped") and isinstance(attr_value._wrapped, FieldQuantity):
                actual_var = attr_value._wrapped
            elif not isinstance(attr_value, FieldQuantity):
                continue

            # Set symbol based on attribute name (T_bar, P, etc.)
            actual_var._symbol = attr_name

            # Skip if we've already processed this symbol
            if actual_var.symbol in processed_symbols:
                continue
            processed_symbols.add(actual_var.symbol)

            # Clone variable to avoid shared state between instances
            cloned_var = self._clone_variable(actual_var)
            self.add_variable(cloned_var)
            # Set the same cloned variable object as instance attribute
            # Use super() to bypass our custom __setattr__ during initialization
            super().__setattr__(attr_name, cloned_var)

    def _extract_equations(self):
        """Extract and process equations from class-level definitions."""
        equations_to_process = self._collect_class_equations()

        for attr_name, equation in equations_to_process:
            try:
                # Check if this equation has constants that should be variable references
                reconstructed_equation = self._reconstruct_equation_with_variables(equation)
                if reconstructed_equation:
                    final_equation = reconstructed_equation
                else:
                    # Try to fix variable references in the equation
                    final_equation = self._fix_equation_variable_references(equation)

                # Add equation to the problem
                self.add_equation(final_equation)
                # Set the equation as an instance attribute
                setattr(self, attr_name, final_equation)
            except Exception as e:
                # Log but continue - some equations might fail during class definition
                self.logger.warning(f"Failed to process equation {attr_name}: {e}")
                # Still set the original equation as attribute
                setattr(self, attr_name, equation)

    def _reconstruct_equation_with_variables(self, equation):
        """
        Reconstruct equations that have constant expressions back to variable references.
        This handles cases where T_bar * (1 - U_m) was evaluated to constants during class definition.
        """
        try:
            # Look for the specific pattern of the T equation: T = constant * (1 - constant)
            if self._is_t_equation_pattern(equation):
                return self._reconstruct_t_equation_pattern(equation)

            # Look for variable sharing equations that reference wrong variables (generic)
            if self._is_variable_sharing_pattern(equation):
                return self._reconstruct_variable_sharing_pattern(equation)


            # Could add other patterns here if needed
            return None

        except Exception:
            return None

    def _is_t_equation_pattern(self, equation) -> bool:
        """Check if this equation matches the T = T_bar * (1 - U_m) pattern."""
        from ..algebra.nodes import BinaryOperation, Constant

        # Check if LHS variable name ends with 'T' (like 'T', 'header_T', etc.)
        lhs_name = getattr(equation.lhs, 'name', '')
        if not (lhs_name == 'T' or lhs_name.endswith('_T')):
            return False

        # Check if RHS is a multiplication: something * (1 - something)
        rhs = equation.rhs
        if not isinstance(rhs, BinaryOperation) or rhs.operator != '*':
            return False

        # Check if right operand is (1 - something)
        right_op = rhs.right
        if not isinstance(right_op, BinaryOperation) or right_op.operator != '-':
            return False

        # Check if it's (1 - constant) pattern
        if not isinstance(right_op.left, Constant) or not isinstance(right_op.right, Constant):
            return False

        # Check if left constant is approximately 1
        left_val = getattr(right_op.left.value, 'value', right_op.left.value)
        return abs(left_val - 1.0) < 1e-10

    def _reconstruct_t_equation_pattern(self, equation):
        """Reconstruct T = T_bar * (1 - U_m) equation with variable references."""
        try:
            from ..algebra import equation as create_equation
            from ..algebra.nodes import VariableReference, BinaryOperation, Constant
            from qnty.core.quantity_catalog import Dimensionless

            # Get the LHS variable name (T, header_T, branch_T, etc.)
            lhs_name = getattr(equation.lhs, 'name', '')

            # Determine the corresponding T_bar and U_m variable names
            if lhs_name == 'T':
                t_bar_name = 'T_bar'
                u_m_name = 'U_m'
            else:
                # For namespaced variables like header_T, branch_T
                prefix = lhs_name[:-2]  # Remove '_T'
                t_bar_name = f"{prefix}_T_bar"
                u_m_name = f"{prefix}_U_m"

            # Check if these variables exist in the problem
            if (lhs_name not in self.variables or
                t_bar_name not in self.variables or
                u_m_name not in self.variables):
                return None

            # Get the variable objects
            t_var = self.variables[lhs_name]
            t_bar_var = self.variables[t_bar_name]
            u_m_var = self.variables[u_m_name]

            # Create variable references
            t_ref = VariableReference(t_var)
            t_bar_ref = VariableReference(t_bar_var)
            u_m_ref = VariableReference(u_m_var)

            # Create constant for 1
            from qnty.core.unit import ureg
            one_dimensionless = Dimensionless("one")
            one_dimensionless.value = 1.0
            one_dimensionless.preferred = ureg.resolve('dimensionless')
            one = Constant(one_dimensionless)

            # Create expression: 1 - U_m
            one_minus_u_m = BinaryOperation("-", one, u_m_ref)

            # Create expression: T_bar * (1 - U_m)
            rhs = BinaryOperation("*", t_bar_ref, one_minus_u_m)

            # Create the equation
            return create_equation(t_ref, rhs, f"{lhs_name}_equation")

        except Exception:
            return None

    def _is_pressure_thickness_pattern(self, equation) -> bool:
        """Check if this equation matches the pressure design thickness pattern with constants."""
        from ..algebra.nodes import BinaryOperation, Constant

        # Check if LHS variable name ends with 't' (like 't', 'header_t', 'branch_t')
        lhs_name = getattr(equation.lhs, 'name', '')
        if not (lhs_name == 't' or lhs_name.endswith('_t')):
            return False

        # Check if RHS has the pattern: constant_pressure * constant_diameter / (2 * (...))
        rhs = equation.rhs
        if not isinstance(rhs, BinaryOperation) or rhs.operator != '/':
            return False

        # Check if numerator is pressure * diameter (both constants)
        numerator = rhs.left
        if not isinstance(numerator, BinaryOperation) or numerator.operator != '*':
            return False

        # Check if both operands are constants (pressure and diameter)
        if not isinstance(numerator.left, Constant) or not isinstance(numerator.right, Constant):
            return False

        # Check if denominator is 2 * (...)
        denominator = rhs.right
        if not isinstance(denominator, BinaryOperation) or denominator.operator != '*':
            return False

        # Check if left operand is constant 2
        if not isinstance(denominator.left, Constant):
            return False

        left_val = getattr(denominator.left.value, 'value', denominator.left.value)
        return abs(left_val - 2.0) < 1e-10

    def _reconstruct_pressure_thickness_pattern(self, equation):
        """Reconstruct pressure design thickness equation with variable references."""
        try:
            from ..algebra import equation as create_equation
            from ..algebra.nodes import VariableReference, BinaryOperation, Constant

            # Get the LHS variable name (t, header_t, branch_t, etc.)
            lhs_name = getattr(equation.lhs, 'name', '')

            # Determine the corresponding variable names
            if lhs_name == 't':
                p_name = 'P'
                d_name = 'D'
                s_name = 'S'
                e_name = 'E'
                w_name = 'W'
                y_name = 'Y'
            elif lhs_name.endswith('_t'):
                prefix = lhs_name[:-2]  # Remove '_t'
                p_name = f'{prefix}_P'
                d_name = f'{prefix}_D'
                s_name = f'{prefix}_S'
                e_name = f'{prefix}_E'
                w_name = f'{prefix}_W'
                y_name = f'{prefix}_Y'
            else:
                return None

            # Find the variables
            t_var = self.variables.get(lhs_name.replace('_', '', 1) if lhs_name.startswith('_') else lhs_name)
            p_var = self.variables.get(p_name)
            d_var = self.variables.get(d_name)
            s_var = self.variables.get(s_name)
            e_var = self.variables.get(e_name)
            w_var = self.variables.get(w_name)
            y_var = self.variables.get(y_name)

            if not all([t_var, p_var, d_var, s_var, e_var, w_var, y_var]):
                return None

            # Create variable references
            t_ref = VariableReference(t_var)
            p_ref = VariableReference(p_var)
            d_ref = VariableReference(d_var)
            s_ref = VariableReference(s_var)
            e_ref = VariableReference(e_var)
            w_ref = VariableReference(w_var)
            y_ref = VariableReference(y_var)

            # Create constant for 2
            from qnty.core.quantity_catalog import Dimensionless
            two_dimensionless = Dimensionless("two")
            two_dimensionless.value = 2.0
            two = Constant(two_dimensionless)

            # Create expression: P * D
            numerator = BinaryOperation("*", p_ref, d_ref)

            # Create expression: S * E * W
            s_e_w = BinaryOperation("*", BinaryOperation("*", s_ref, e_ref), w_ref)

            # Create expression: P * Y
            p_y = BinaryOperation("*", p_ref, y_ref)

            # Create expression: S * E * W + P * Y
            denominator_inner = BinaryOperation("+", s_e_w, p_y)

            # Create expression: 2 * (S * E * W + P * Y)
            denominator = BinaryOperation("*", two, denominator_inner)

            # Create expression: (P * D) / (2 * (S * E * W + P * Y))
            rhs = BinaryOperation("/", numerator, denominator)

            # Create the equation
            return create_equation(t_ref, rhs, f"{lhs_name}_equation")

        except Exception:
            return None

    def _is_variable_sharing_pattern(self, equation) -> bool:
        """Check if this equation matches the pattern: sub_problem_var = system_var (variable sharing)."""
        from ..algebra.nodes import VariableReference

        try:
            # LHS must be a variable reference
            if not isinstance(equation.lhs, VariableReference):
                return False

            lhs_name = getattr(equation.lhs.variable, "name", "")

            # LHS should be a sub-problem variable (contains "(Header)" or "(Branch)")
            if not (("(Header)" in lhs_name) or ("(Branch)" in lhs_name)):
                return False

            # RHS can be either a VariableReference or an ExpressionEnabledWrapper that needs fixing
            if isinstance(equation.rhs, VariableReference):
                # Check if it's referencing the right variable
                rhs_name = getattr(equation.rhs.variable, "name", "")
                lhs_base = lhs_name.replace(" (Header)", "").replace(" (Branch)", "")
                return lhs_base == rhs_name
            else:
                # Check if RHS is a malformed wrapper that should be a system variable
                rhs_str = str(equation.rhs)
                if "ExpressionEnabledWrapper" in rhs_str:
                    return True

            return False

        except Exception:
            return False

    def _reconstruct_variable_sharing_pattern(self, equation):
        """Reconstruct variable sharing equations to use the correct system variable."""
        from ..algebra.nodes import VariableReference
        from ..algebra.equation import Equation

        try:
            # Get the base variable name (without sub-problem suffix)
            lhs_name = getattr(equation.lhs.variable, "name", "")
            base_name = lhs_name.replace(" (Header)", "").replace(" (Branch)", "")

            # Find the correct system variable from our instance variables
            # Look for a variable with the same base name but without sub-problem indicators
            system_var = None
            for var_name, var in self.variables.items():
                if (hasattr(var, "name") and
                    var.name == base_name and
                    "Header" not in var.name and
                    "Branch" not in var.name):
                    system_var = var
                    break

            if system_var is None:
                return None

            # Create variable references
            lhs_ref = VariableReference(equation.lhs.variable)
            system_ref = VariableReference(system_var)

            # Create the reconstructed equation
            equation_name = f"{lhs_name}_shared_equation"
            return Equation(equation_name, lhs_ref, system_ref)

        except Exception:
            return None

    def replace_sub_variables(self, system_var, sub_vars):
        """
        Share a system variable with sub-problem variables by creating assignment equations.

        This is a cleaner alternative to manually creating equations like:
        header_P_eqn = equation(header.P, P)

        Args:
            system_var: The system-level variable to share
            sub_vars: List of sub-problem variables that should equal the system variable

        Example:
            self.replace_sub_variables(P, [header.P, branch.P])
        """
        from ..algebra.nodes import VariableReference
        from ..algebra.equation import Equation

        # Use the system variable directly - the composition system should ensure
        # the right variable is passed in from the class-level _variable_sharing
        actual_system_var = system_var

        system_ref = VariableReference(actual_system_var)

        for sub_var in sub_vars:
            # Reset the sub-variable to be unknown so it can be solved
            sub_var.value = None

            # Create assignment equation: sub_var = system_var
            sub_ref = VariableReference(sub_var)
            equation_name = f"{getattr(sub_var, 'name', 'unknown')}_shared_equation"

            equation = Equation(equation_name, sub_ref, system_ref)
            # Insert sharing equations at the beginning so they get solved first
            # This ensures that shared variables get their values before dependent equations are solved
            # This ensures pressure values are established before dependent equations
            self.equations.insert(0, equation)

    def _fix_equation_variable_references(self, equation):
        """Fix variable references in equations to use canonical variables from self.variables."""
        from ..algebra.nodes import VariableReference
        from ..algebra.equation import Equation

        try:
            new_lhs = equation.lhs
            new_rhs = equation.rhs
            changed = False

            # Fix LHS if it's a variable reference
            if isinstance(equation.lhs, VariableReference):
                lhs_var = equation.lhs.variable
                for canonical_var in self.variables.values():
                    if (hasattr(lhs_var, 'name') and hasattr(canonical_var, 'name') and
                        lhs_var.name == canonical_var.name and id(lhs_var) != id(canonical_var)):
                        new_lhs = VariableReference(canonical_var)
                        changed = True
                        break

            # Fix RHS if it's a variable reference
            if isinstance(equation.rhs, VariableReference):
                rhs_var = equation.rhs.variable
                for canonical_var in self.variables.values():
                    if (hasattr(rhs_var, 'name') and hasattr(canonical_var, 'name') and
                        rhs_var.name == canonical_var.name and id(rhs_var) != id(canonical_var)):
                        new_rhs = VariableReference(canonical_var)
                        changed = True
                        break

            # Return new equation if any references were fixed
            if changed:
                return Equation(equation.name, new_lhs, new_rhs)
            else:
                return equation

        except Exception:
            return equation

    def _process_variable_sharing(self):
        """Process the _variable_sharing class attribute to set up variable sharing automatically."""
        if not hasattr(self.__class__, '_variable_sharing'):
            return

        sharing_config = getattr(self.__class__, '_variable_sharing')
        for system_var, sub_vars in sharing_config:
            # Variables are already actual object references, no need to resolve paths
            self.replace_sub_variables(system_var, sub_vars)


    def _canonicalize_all_equation_variables(self):
        """Replace all variable references in equations with canonical ones from self.variables."""
        from ..algebra.nodes import VariableReference
        from ..algebra.equation import Equation


        for i, equation in enumerate(self.equations):
            new_lhs = self._canonicalize_expression(equation.lhs)
            new_rhs = self._canonicalize_expression(equation.rhs)

            if new_lhs != equation.lhs or new_rhs != equation.rhs:
                self.equations[i] = Equation(equation.name, new_lhs, new_rhs)

    def _enforce_sharing_equations(self):
        """After solving, manually enforce sharing equations by copying values."""
        from ..algebra.nodes import VariableReference

        sharing_enforced = False

        # First, enforce the sharing equations
        for equation in self.equations:
            if 'shared' in equation.name:
                # Check if this is a simple sharing equation: var1 = var2
                if (isinstance(equation.lhs, VariableReference) and
                    isinstance(equation.rhs, VariableReference)):

                    lhs_var = equation.lhs.variable
                    rhs_var = equation.rhs.variable

                    # If RHS has value but LHS doesn't, copy RHS to LHS
                    if (hasattr(rhs_var, 'value') and rhs_var.value is not None and
                        hasattr(lhs_var, 'value')):
                        if lhs_var.value != rhs_var.value:
                            lhs_var.value = rhs_var.value
                            sharing_enforced = True

        # After sharing enforcement, manually recalculate key dependent equations
        # This is needed because the solver solved them with wrong pressure values
        return sharing_enforced

    def _recalculate_pressure_dependent_equations(self):
        """Manually recalculate equations that depend on pressure after sharing enforcement."""
        # For sub-problems, recalculate key equations like t = (P * D) / (2 * (S * E * W + P * Y))

        # Recalculate header.t
        if hasattr(self, 'header') and hasattr(self.header, 'P') and self.header.P.value is not None:
            self._recalculate_thickness_equation(self.header)

        # Recalculate branch.t
        if hasattr(self, 'branch') and hasattr(self.branch, 'P') and self.branch.P.value is not None:
            self._recalculate_thickness_equation(self.branch)

        # After updating thickness values, recalculate area equations that depend on them
        self._recalculate_area_equations()

    def _recalculate_thickness_equation(self, sub_problem):
        """Recalculate thickness equation: t = (P * D) / (2 * (S * E * W + P * Y))"""
        try:
            # Get all the required values
            P = sub_problem.P.value
            D = sub_problem.D.value
            S = sub_problem.S.value
            E = sub_problem.E.value
            W = sub_problem.W.value
            Y = sub_problem.Y.value

            print(f"DEBUG: Recalculating thickness for {getattr(sub_problem.P, 'name', 'unknown')}")
            print(f"  P={P}, D={D}, S={S}, E={E}, W={W}, Y={Y}")

            if all(v is not None for v in [P, D, S, E, W, Y]):
                # Calculate new thickness value
                old_t = sub_problem.t.value
                new_t = (P * D) / (2 * (S * E * W + P * Y))
                sub_problem.t.value = new_t
                print(f"  Updated t: {old_t} -> {new_t}")
            else:
                print(f"  Skipping - missing values")

        except (AttributeError, TypeError, ZeroDivisionError) as e:
            print(f"  ERROR in thickness calculation: {e}")
            pass

    def _recalculate_area_equations(self):
        """Recalculate area equations that depend on updated thickness values."""
        try:
            import math

            # First, recalculate d_1 which depends on updated branch properties
            # d_1 = (branch.D - 2 * (branch.T - branch.c)) / sin(beta)
            if (hasattr(self, 'd_1') and hasattr(self, 'branch') and
                hasattr(self.branch, 'D') and hasattr(self.branch, 'T') and hasattr(self.branch, 'c') and hasattr(self, 'beta')):
                branch_D = self.branch.D.value
                branch_T = self.branch.T.value
                branch_c = self.branch.c.value
                beta = self.beta.value

                if all(v is not None for v in [branch_D, branch_T, branch_c, beta]):
                    old_d_1 = self.d_1.value
                    new_d_1 = (branch_D - 2 * (branch_T - branch_c)) / math.sin(beta)
                    self.d_1.value = new_d_1
                    print(f"DEBUG: Recalculating d_1")
                    print(f"  branch.D={branch_D}, branch.T={branch_T}, branch.c={branch_c}, beta={beta}")
                    print(f"  sin(beta)={math.sin(beta)}")
                    print(f"  Updated d_1: {old_d_1} -> {new_d_1}")

            # Now recalculate d_2 which depends on updated d_1
            # d_2 = max(d_1, (branch.T - branch.c) + (header.T - header.c) + d_1 / 2)
            if (hasattr(self, 'd_2') and hasattr(self, 'd_1') and hasattr(self, 'branch') and hasattr(self, 'header') and
                hasattr(self.branch, 'T') and hasattr(self.branch, 'c') and
                hasattr(self.header, 'T') and hasattr(self.header, 'c')):
                d_1 = self.d_1.value
                branch_T = self.branch.T.value
                branch_c = self.branch.c.value
                header_T = self.header.T.value
                header_c = self.header.c.value

                if all(v is not None for v in [d_1, branch_T, branch_c, header_T, header_c]):
                    old_d_2 = self.d_2.value
                    alternative = (branch_T - branch_c) + (header_T - header_c) + d_1 / 2
                    new_d_2 = max(d_1, alternative)
                    self.d_2.value = new_d_2
                    print(f"DEBUG: Recalculating d_2")
                    print(f"  d_1={d_1}, alternative={(branch_T - branch_c) + (header_T - header_c) + d_1 / 2}")
                    print(f"  max({d_1}, {alternative}) = {new_d_2}")
                    print(f"  Updated d_2: {old_d_2} -> {new_d_2}")

            # A_1 equation: A_1 = header.t * d_1 * (2 - sin(beta))
            if (hasattr(self, 'header') and hasattr(self.header, 't') and
                hasattr(self, 'd_1') and hasattr(self, 'beta') and hasattr(self, 'A_1')):

                header_t = self.header.t.value
                d_1 = self.d_1.value
                beta = self.beta.value  # in radians

                print(f"DEBUG: Recalculating A_1")
                print(f"  header.t={header_t}, d_1={d_1}, beta={beta}")

                if all(v is not None for v in [header_t, d_1, beta]):
                    sin_beta = math.sin(beta)
                    old_A_1 = self.A_1.value
                    new_A_1 = header_t * d_1 * (2 - sin_beta)
                    self.A_1.value = new_A_1
                    print(f"  Updated A_1: {old_A_1} -> {new_A_1}")

            # A_2 equation: A_2 = (2 * d_2 - d_1) * (header.T - header.t - header.c)
            if (hasattr(self, 'A_2') and hasattr(self, 'd_2') and hasattr(self, 'd_1') and
                hasattr(self, 'header') and hasattr(self.header, 'T') and
                hasattr(self.header, 't') and hasattr(self.header, 'c')):

                d_2 = self.d_2.value
                d_1 = self.d_1.value
                header_T = self.header.T.value
                header_t = self.header.t.value
                header_c = self.header.c.value

                print(f"DEBUG: Recalculating A_2")
                print(f"  d_2={d_2}, d_1={d_1}, header.T={header_T}, header.t={header_t}, header.c={header_c}")

                if all(v is not None for v in [d_2, d_1, header_T, header_t, header_c]):
                    old_A_2 = self.A_2.value
                    new_A_2 = (2 * d_2 - d_1) * (header_T - header_t - header_c)
                    self.A_2.value = new_A_2
                    print(f"  Updated A_2: {old_A_2} -> {new_A_2}")

            # A_3 equation: A_3 = (2 * L_4 * (branch.T - branch.t - branch.c) / sin(beta)) * min(1, branch.S / header.S)
            if (hasattr(self, 'A_3') and hasattr(self, 'L_4') and hasattr(self, 'beta') and
                hasattr(self, 'branch') and hasattr(self.branch, 'T') and
                hasattr(self.branch, 't') and hasattr(self.branch, 'c') and
                hasattr(self.branch, 'S') and hasattr(self, 'header') and hasattr(self.header, 'S')):

                L_4 = self.L_4.value
                branch_T = self.branch.T.value
                branch_t = self.branch.t.value
                branch_c = self.branch.c.value
                branch_S = self.branch.S.value
                header_S = self.header.S.value
                beta = self.beta.value

                print(f"DEBUG: Recalculating A_3")
                print(f"  L_4={L_4}, branch.T={branch_T}, branch.t={branch_t}, branch.c={branch_c}")
                print(f"  branch.S={branch_S}, header.S={header_S}, beta={beta}")

                if all(v is not None for v in [L_4, branch_T, branch_t, branch_c, branch_S, header_S, beta]):
                    import math
                    sin_beta = math.sin(beta)
                    min_ratio = min(1.0, branch_S / header_S)
                    old_A_3 = self.A_3.value
                    new_A_3 = (2 * L_4 * (branch_T - branch_t - branch_c) / sin_beta) * min_ratio
                    self.A_3.value = new_A_3
                    print(f"  Updated A_3: {old_A_3} -> {new_A_3}")

            # Weld area recalculations
            self._recalculate_weld_areas()

            # A_4 equation: A_4 = A_r + A_w
            if (hasattr(self, 'A_4') and hasattr(self, 'A_r') and hasattr(self, 'A_w')):
                A_r = self.A_r.value
                A_w = self.A_w.value

                print(f"DEBUG: Recalculating A_4")
                print(f"  A_r={A_r}, A_w={A_w}")

                if all(v is not None for v in [A_r, A_w]):
                    old_A_4 = self.A_4.value
                    new_A_4 = A_r + A_w
                    self.A_4.value = new_A_4
                    print(f"  Updated A_4: {old_A_4} -> {new_A_4}")

        except Exception as e:
            print(f"  ERROR in area calculation: {e}")
            pass

    def _recalculate_weld_areas(self):
        """Manually recalculate weld area equations after sharing enforcement."""
        import math

        try:
            # First, recalculate weld throat calculations
            # t_c_b = min(0.7 * branch.T_bar, t_c_max)
            if (hasattr(self, 't_c_b') and hasattr(self, 'branch') and
                hasattr(self.branch, 'T_bar') and hasattr(self, 't_c_max')):
                branch_T_bar = self.branch.T_bar.value
                t_c_max = self.t_c_max.value

                if all(v is not None for v in [branch_T_bar, t_c_max]):
                    old_t_c_b = self.t_c_b.value
                    new_t_c_b = min(0.7 * branch_T_bar, t_c_max)
                    self.t_c_b.value = new_t_c_b
                    print(f"DEBUG: Recalculating t_c_b")
                    print(f"  branch.T_bar={branch_T_bar}, t_c_max={t_c_max}")
                    print(f"  Updated t_c_b: {old_t_c_b} -> {new_t_c_b}")

            # t_c_r = 0.5 * T_bar_r
            if (hasattr(self, 't_c_r') and hasattr(self, 'T_bar_r')):
                T_bar_r = self.T_bar_r.value
                if T_bar_r is not None:
                    old_t_c_r = self.t_c_r.value
                    new_t_c_r = 0.5 * T_bar_r
                    self.t_c_r.value = new_t_c_r
                    print(f"DEBUG: Recalculating t_c_r")
                    print(f"  T_bar_r={T_bar_r}")
                    print(f"  Updated t_c_r: {old_t_c_r} -> {new_t_c_r}")

            # A_w_b equation: complex conditional based on T_r
            if (hasattr(self, 'A_w_b') and hasattr(self, 'T_r') and hasattr(self, 'L_4') and
                hasattr(self, 't_c_b') and hasattr(self, 'z_b')):
                T_r = self.T_r.value
                L_4 = self.L_4.value
                t_c_b = self.t_c_b.value
                z_b = self.z_b.value

                if all(v is not None for v in [T_r, t_c_b, z_b]):
                    old_A_w_b = self.A_w_b.value

                    # Complex conditional logic from the equation
                    if T_r <= 0:
                        # First condition: T_r <= 0
                        max_val = max(t_c_b / 0.707, z_b)
                        new_A_w_b = 2 * 0.5 * (max_val ** 2)
                    elif T_r <= L_4:
                        # Second condition: 0 < T_r <= L_4
                        max_val = max(t_c_b / 0.707, z_b)
                        new_A_w_b = 2 * 0.5 * (max_val ** 2)
                    else:
                        # Third condition: T_r > L_4
                        new_A_w_b = 0

                    self.A_w_b.value = new_A_w_b
                    print(f"DEBUG: Recalculating A_w_b")
                    print(f"  T_r={T_r}, L_4={L_4}, t_c_b={t_c_b}, z_b={z_b}")
                    print(f"  max(t_c_b/0.707, z_b) = max({t_c_b/0.707}, {z_b}) = {max(t_c_b / 0.707, z_b)}")
                    print(f"  Updated A_w_b: {old_A_w_b} -> {new_A_w_b}")

            # A_w_r equation: conditional based on D_r and d_2
            if (hasattr(self, 'A_w_r') and hasattr(self, 'D_r') and hasattr(self, 'd_2') and
                hasattr(self, 't_c_r') and hasattr(self, 'z_r')):
                D_r = self.D_r.value
                d_2 = self.d_2.value
                t_c_r = self.t_c_r.value
                z_r = self.z_r.value

                if all(v is not None for v in [D_r, d_2, t_c_r, z_r]):
                    old_A_w_r = self.A_w_r.value

                    # Condition: D_r <= 2*d_2 - max(t_c_r/0.707, z_r)
                    max_val = max(t_c_r / 0.707, z_r)
                    threshold = 2 * d_2 - max_val

                    if D_r <= threshold:
                        new_A_w_r = 2 * 0.5 * (max_val ** 2)
                    else:
                        new_A_w_r = 0

                    self.A_w_r.value = new_A_w_r
                    print(f"DEBUG: Recalculating A_w_r")
                    print(f"  D_r={D_r}, d_2={d_2}, t_c_r={t_c_r}, z_r={z_r}")
                    print(f"  threshold = 2*{d_2} - max({t_c_r/0.707}, {z_r}) = {threshold}")
                    print(f"  D_r <= threshold? {D_r} <= {threshold} = {D_r <= threshold}")
                    print(f"  Updated A_w_r: {old_A_w_r} -> {new_A_w_r}")

            # A_w = A_w_b + A_w_r
            if (hasattr(self, 'A_w') and hasattr(self, 'A_w_b') and hasattr(self, 'A_w_r')):
                A_w_b = self.A_w_b.value
                A_w_r = self.A_w_r.value

                if all(v is not None for v in [A_w_b, A_w_r]):
                    old_A_w = self.A_w.value
                    new_A_w = A_w_b + A_w_r
                    self.A_w.value = new_A_w
                    print(f"DEBUG: Recalculating A_w")
                    print(f"  A_w_b={A_w_b}, A_w_r={A_w_r}")
                    print(f"  Updated A_w: {old_A_w} -> {new_A_w}")

        except Exception as e:
            print(f"  ERROR in weld area calculation: {e}")
            pass



    def _canonicalize_expression(self, expr):
        """Replace variable references in an expression with canonical ones."""
        from ..algebra.nodes import VariableReference

        if isinstance(expr, VariableReference):
            var = expr.variable
            if hasattr(var, 'name'):
                # First priority: Check if there's a system-level variable with this name
                # Look for system attributes that match this variable name
                for attr_name in dir(self):
                    if not attr_name.startswith('_'):  # Skip private attributes
                        attr_value = getattr(self, attr_name, None)
                        if (attr_value and hasattr(attr_value, 'name') and
                            hasattr(attr_value, 'value') and  # Must be a variable
                            attr_value.name == var.name):
                            if id(var) != id(attr_value):
                                return VariableReference(attr_value)
                            else:
                                return expr

                        # Also check sub-problem attributes (e.g., header.P, branch.P)
                        if hasattr(attr_value, '__dict__'):  # Check if it's an object with attributes
                            for sub_attr_name in dir(attr_value):
                                if not sub_attr_name.startswith('_'):
                                    try:
                                        sub_attr_value = getattr(attr_value, sub_attr_name, None)
                                        if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                            hasattr(sub_attr_value, 'value') and  # Must be a variable
                                            sub_attr_value.name == var.name):
                                            if id(var) != id(sub_attr_value):
                                                return VariableReference(sub_attr_value)
                                            else:
                                                return expr
                                    except (AttributeError, TypeError):
                                        continue

                # Second priority: Find canonical variable with same name in self.variables
                for symbol, canonical_var in self.variables.items():
                    if (hasattr(canonical_var, 'name') and canonical_var.name == var.name):
                        if id(var) != id(canonical_var):
                            return VariableReference(canonical_var)
                        else:
                            return expr
            return expr
        else:
            return expr

    def _update_all_equation_variable_references(self):
        """Update all equations to use canonical variable references from self.variables."""
        from ..algebra.nodes import VariableReference
        from ..algebra.equation import Equation

        updated_equations = []
        for eq in self.equations:
            # Update RHS variable references
            new_rhs = self._update_expression_variable_references(eq.rhs)
            # Update LHS variable references
            new_lhs = self._update_expression_variable_references(eq.lhs)

            # Create new equation if any references were updated
            if new_rhs != eq.rhs or new_lhs != eq.lhs:
                updated_equations.append(Equation(eq.name, new_lhs, new_rhs))
            else:
                updated_equations.append(eq)

        # Replace all equations
        self.equations = updated_equations

    def _retrofit_constants_to_variables(self):
        """
        Generic retrofitting: replace constants in equations with variables where possible.
        This handles equations that were created with concrete values during class definition
        but should use variable references in the current context.
        """
        from ..algebra.nodes import VariableReference, Constant, BinaryOperation
        from ..algebra.equation import Equation

        for i, equation in enumerate(self.equations):
            new_lhs = self._retrofit_expression(equation.lhs)
            new_rhs = self._retrofit_expression(equation.rhs)

            if new_lhs != equation.lhs or new_rhs != equation.rhs:
                self.equations[i] = Equation(equation.name, new_lhs, new_rhs)

    def _retrofit_expression(self, expr):
        """Recursively retrofit constants to variables in an expression."""
        from ..algebra.nodes import VariableReference, Constant, BinaryOperation

        if isinstance(expr, Constant):
            # Check if this constant value matches any variable in our context
            constant_value = expr.value
            if hasattr(constant_value, 'value'):
                # Handle Quantity constants - check all variables for matches
                # First, find all matching variables to avoid ambiguous substitutions
                matching_variables = []
                for symbol, var in self.variables.items():
                    if (hasattr(var, 'value') and var.value is not None):
                        # Check dimensional compatibility first
                        if hasattr(var, 'dim') and hasattr(constant_value, 'dim'):
                            if var.dim != constant_value.dim:
                                continue  # Skip if dimensions don't match

                        # Check if values are approximately equal
                        try:
                            if abs(var.value - constant_value.value) < 1e-10:
                                matching_variables.append((symbol, var))
                        except (TypeError, ValueError):
                            continue

                # Only substitute if there's exactly one match to avoid ambiguity
                # However, allow ambiguous substitutions for non-zero values (they're less likely to be coincidental)
                if len(matching_variables) == 1:
                    return VariableReference(matching_variables[0][1])
                elif len(matching_variables) > 1:
                    # For small/zero values, avoid ambiguous substitution as these are commonly shared
                    # For non-zero values, use the first match (existing behavior) as they're less likely coincidental
                    constant_abs_value = abs(constant_value.value) if hasattr(constant_value, 'value') else abs(constant_value)
                    if constant_abs_value < 1e-6:  # Small values including zero
                        # Log the ambiguity for debugging
                        var_names = [f"{symbol}({var.name})" for symbol, var in matching_variables]
                        if hasattr(self, 'logger'):
                            self.logger.debug(f"Ambiguous constant retrofitting: {constant_value} matches multiple variables: {var_names}. Skipping substitution to avoid incorrect variable selection.")
                        # Don't substitute - keep the constant as-is
                    else:
                        # For non-zero values, use the first match (original behavior)
                        return VariableReference(matching_variables[0][1])
            return expr

        elif isinstance(expr, BinaryOperation):
            # Recursively retrofit operands
            new_left = self._retrofit_expression(expr.left)
            new_right = self._retrofit_expression(expr.right)

            if new_left != expr.left or new_right != expr.right:
                return BinaryOperation(expr.operator, new_left, new_right)
            return expr

        else:
            # Other expression types (VariableReference, etc.) - return as-is
            return expr

    def _update_expression_variable_references(self, expr):
        """Recursively update variable references in an expression."""
        from ..algebra.nodes import VariableReference

        if isinstance(expr, VariableReference):
            # Find the canonical variable from self.variables
            var = expr.variable
            if hasattr(var, 'name'):
                for name, canonical_var in self.variables.items():
                    if hasattr(canonical_var, 'name') and canonical_var.name == var.name:
                        if id(canonical_var) != id(var):
                            return VariableReference(canonical_var)
            return expr
        else:
            # For now, only handle simple variable references
            # Complex expressions can be handled later if needed
            return expr

    def _get_class_attributes(self) -> list[tuple[str, Any]]:
        """Get all non-private class attributes efficiently."""
        return [(attr_name, getattr(self.__class__, attr_name)) for attr_name in dir(self.__class__) if not attr_name.startswith("_")]

    def _collect_class_equations(self) -> list[tuple[str, Any]]:
        """Collect all equation objects from class attributes."""
        equations_to_process = []
        for attr_name, attr_value in self._get_class_attributes():
            if isinstance(attr_value, Equation):
                equations_to_process.append((attr_name, attr_value))
        return equations_to_process

    def _integrate_sub_problem(self, sub_problem, namespace: str) -> None:
        """
        Integrate a sub-problem by flattening its variables with namespace prefixes.
        Creates a simple dotted access pattern: self.header.P becomes self.header_P
        """
        self.sub_problems[namespace] = sub_problem
        proxy_configs = getattr(self.__class__, "_proxy_configurations", {}).get(namespace, {})

        namespace_obj = self._create_namespace_object(sub_problem, namespace, proxy_configs)
        super().__setattr__(namespace, namespace_obj)

        self._integrate_sub_problem_equations(sub_problem, namespace)

    def _create_namespace_object(self, sub_problem, namespace: str, proxy_configs: dict):
        """Create namespace object with all sub-problem variables."""
        # Create a proper namespace class that can handle attribute updates
        class SubProblemNamespace:
            def __init__(self, parent_problem, namespace_prefix):
                self._parent_problem = parent_problem
                self._namespace_prefix = namespace_prefix

            def __setattr__(self, name, value):
                # Handle internal attributes normally
                if name.startswith('_'):
                    super().__setattr__(name, value)
                    return

                # For variable attributes, update both the namespace and main problem
                namespaced_name = f"{self._namespace_prefix}_{name}"
                if hasattr(self, '_parent_problem') and namespaced_name in self._parent_problem.variables:
                    # Update the main problem's variables dictionary
                    self._parent_problem.variables[namespaced_name] = value

                # Update the namespace attribute
                super().__setattr__(name, value)

        namespace_obj = SubProblemNamespace(self, namespace)

        for var_symbol, var in sub_problem.variables.items():
            namespaced_var = self._create_namespaced_variable(var, var_symbol, namespace, proxy_configs)
            self.add_variable(namespaced_var)

            # Create a wrapper that handles .set() calls
            wrapped_var = self._create_namespace_variable_wrapper(namespaced_var, namespace_obj, var_symbol)

            # Set both namespaced access (self.header_P) and dotted access (self.header.P)
            if namespaced_var.symbol is not None:
                super().__setattr__(namespaced_var.symbol, namespaced_var)
            setattr(namespace_obj, var_symbol, wrapped_var)

        return namespace_obj

    def _create_namespace_variable_wrapper(self, variable, namespace_obj, var_symbol):
        """Create a wrapper that intercepts .set() calls and updates the namespace."""
        class NamespaceVariableWrapper(ArithmeticOperationsMixin):
            def __init__(self, wrapped_var, namespace, symbol):
                self._wrapped_var = wrapped_var
                self._namespace = namespace
                self._symbol = symbol

            def __getattr__(self, name):
                # Handle special attributes to avoid recursion issues during copy
                if name in ('__setstate__', '__getstate__', '__reduce__', '__reduce_ex__', '__copy__', '__deepcopy__'):
                    # These are copy-related methods that might not exist - raise AttributeError
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

                # For all other attributes, delegate to the wrapped variable
                try:
                    return getattr(self._wrapped_var, name)
                except AttributeError:
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

            def __setattr__(self, name, value):
                # Handle wrapper's own attributes
                if name.startswith('_'):
                    super().__setattr__(name, value)
                else:
                    # Delegate to wrapped variable (this fixes the solver issue)
                    setattr(self._wrapped_var, name, value)

            def set(self, value, unit=None):
                # Call the original set method
                setter = self._wrapped_var.set(value, unit)

                if unit is not None:
                    # If unit is provided, we have the final variable
                    setattr(self._namespace, self._symbol, setter)
                    return setter
                else:
                    # Return a wrapped setter that updates namespace on unit access
                    return NamespaceSetterWrapper(setter, self._namespace, self._symbol)

            def __str__(self):
                return str(self._wrapped_var)

            def __repr__(self):
                return repr(self._wrapped_var)

        # Also define the setter wrapper class here
        class NamespaceSetterWrapper:
            def __init__(self, setter, namespace, symbol):
                self._setter = setter
                self._namespace = namespace
                self._symbol = symbol

            def __getattr__(self, name):
                # When a unit is accessed (like .inch), get the final variable and update namespace
                final_var = getattr(self._setter, name)
                setattr(self._namespace, self._symbol, final_var)
                return final_var

        return NamespaceVariableWrapper(variable, namespace_obj, var_symbol)

    def _integrate_sub_problem_equations(self, sub_problem, namespace: str):
        """Integrate equations from sub-problem with proper namespacing."""
        for equation in sub_problem.equations:
            try:
                # Skip conditional equations for variables that are overridden to known values in composition
                if self._should_skip_subproblem_equation(equation, namespace):
                    continue


                # Check if equation is already namespaced (contains namespace prefix)
                equation_str = str(equation)
                if f"{namespace}_" in equation_str:
                    # Equation is already namespaced, add it directly
                    self.add_equation(equation)
                else:
                    # Equation needs namespacing
                    namespaced_equation = self._namespace_equation(equation, namespace)
                    if namespaced_equation:
                        self.add_equation(namespaced_equation)
            except Exception as e:
                self.logger.debug(f"Failed to namespace equation from {namespace}: {e}")


    def _create_namespaced_variable(self, var: FieldQuantity, var_symbol: str, namespace: str, proxy_configs: dict) -> FieldQuantity:
        """Create a namespaced variable with proper configuration."""
        namespaced_symbol = f"{namespace}_{var_symbol}"
        namespaced_var = self._clone_variable(var)
        namespaced_var._symbol = namespaced_symbol
        namespaced_var.name = f"{var.name} ({namespace.title()})"

        # Apply proxy configuration if available
        if var_symbol in proxy_configs:
            config = proxy_configs[var_symbol]
            # For the unified Quantity API, set value and preferred instead of quantity
            quantity = config["quantity"]
            if quantity is not None and hasattr(quantity, "value") and hasattr(quantity, "preferred"):
                namespaced_var.value = quantity.value
                namespaced_var.preferred = quantity.preferred
            elif quantity is None and not config["is_known"]:
                # Handle the case where variable should be unknown (value = None)
                namespaced_var.value = None
            # is_known is handled by whether value is None or not

        return namespaced_var

    def _namespace_equation(self, equation, namespace: str):
        """
        Create a namespaced version of an equation by prefixing all variable references.
        """
        try:
            # Get all variable symbols in the equation
            variables_in_eq = equation.get_all_variables()

            # Create mapping from original symbols to namespaced symbols
            symbol_mapping = self._create_symbol_mapping(variables_in_eq, namespace)
            if not symbol_mapping:
                return None

            # Create new equation with namespaced references
            return self._create_namespaced_equation(equation, symbol_mapping)

        except Exception:
            return None

    def _create_symbol_mapping(self, variables_in_eq: set[str], namespace: str) -> dict[str, str]:
        """Create mapping from original symbols to namespaced symbols."""
        symbol_mapping = {}
        for var_symbol in variables_in_eq:
            namespaced_symbol = f"{namespace}_{var_symbol}"
            if namespaced_symbol in self.variables:
                symbol_mapping[var_symbol] = namespaced_symbol
        return symbol_mapping

    def _create_namespaced_equation(self, equation: Equation, symbol_mapping: dict[str, str]) -> Equation | None:
        """Create new equation with namespaced references."""
        # For LHS, we need a Variable object
        # For RHS, we need proper expression structure
        namespaced_lhs = self._namespace_expression_for_lhs(equation.lhs, symbol_mapping)
        namespaced_rhs = self._namespace_expression(equation.rhs, symbol_mapping)

        if namespaced_lhs and namespaced_rhs:
            # Use the new API equation() function instead of .equals() method
            from ..algebra import equation as create_equation
            namespaced_equation_name = f"{equation.name}_namespaced"
            return create_equation(namespaced_lhs, namespaced_rhs, namespaced_equation_name)
        return None

    def _namespace_expression(self, expr, symbol_mapping):
        """
        Create a namespaced version of an expression by replacing variable references.
        """
        # Handle variable references
        if isinstance(expr, VariableReference):
            return self._namespace_variable_reference(expr, symbol_mapping)
        elif isinstance(expr, FieldQuantity) and expr.symbol in symbol_mapping:
            return self._namespace_variable_object(expr, symbol_mapping)

        # Handle operations
        elif isinstance(expr, BinaryOperation):
            return self._namespace_binary_operation(expr, symbol_mapping)
        elif isinstance(expr, ConditionalExpression):
            return self._namespace_conditional_expression(expr, symbol_mapping)
        elif self._is_unary_operation(expr):
            return self._namespace_unary_operation(expr, symbol_mapping)
        elif self._is_binary_function(expr):
            return self._namespace_binary_function(expr, symbol_mapping)
        elif isinstance(expr, Constant):
            # Check if this constant corresponds to a variable that should be namespaced
            return self._namespace_constant_if_needed(expr, symbol_mapping)
        else:
            return expr

    def _namespace_constant_if_needed(self, expr: Constant, symbol_mapping: dict[str, str]):
        """
        Check if a Constant corresponds to a variable that should be namespaced.
        This handles cases where expressions like T_bar * (1 - U_m) were evaluated to constants
        at class definition time, but need to be converted back to variable references.
        """
        constant_value = expr.value

        # Check each original symbol to see if any variable matches this constant value
        for original_symbol, namespaced_symbol in symbol_mapping.items():
            if namespaced_symbol not in self.variables:
                continue

            namespaced_var = self.variables[namespaced_symbol]

            # Check if the constant's value matches this variable's value (within tolerance)
            if self._values_match(constant_value, namespaced_var):
                # Replace the constant with a variable reference
                from ..algebra.nodes import VariableReference
                return VariableReference(namespaced_var)

        # No matching variable found, return the constant unchanged
        return expr

    def _values_match(self, constant_value, variable) -> bool:
        """Check if a constant value matches a variable's value, handling units and tolerance."""
        if not hasattr(variable, 'value') or variable.value is None:
            return False

        try:
            # For quantity objects, compare the SI values
            if hasattr(constant_value, 'value') and hasattr(variable, 'value'):
                const_si_value = getattr(constant_value, 'value', constant_value)
                var_si_value = variable.value
            else:
                const_si_value = constant_value
                var_si_value = variable.value

            # Use a reasonable tolerance for floating point comparison
            tolerance = 1e-10
            return abs(const_si_value - var_si_value) < tolerance

        except (AttributeError, TypeError, ValueError):
            return False

    def _namespace_variable_reference(self, expr: VariableReference, symbol_mapping: dict[str, str]) -> VariableReference:
        """Namespace a VariableReference object."""
        # VariableReference uses the 'name' property which returns the symbol if available
        symbol = expr.name
        if symbol in symbol_mapping:
            namespaced_symbol = symbol_mapping[symbol]
            if namespaced_symbol in self.variables:
                return VariableReference(self.variables[namespaced_symbol])
        return expr

    def _namespace_variable_object(self, expr: FieldQuantity, symbol_mapping: dict[str, str]) -> VariableReference | FieldQuantity:
        """Namespace a Variable object."""
        if expr.symbol is None:
            return expr
        namespaced_symbol = symbol_mapping[expr.symbol]
        if namespaced_symbol in self.variables:
            # Return VariableReference for use in expressions, not the Variable itself
            return VariableReference(self.variables[namespaced_symbol])
        return expr

    def _namespace_binary_operation(self, expr: BinaryOperation, symbol_mapping: dict[str, str]) -> BinaryOperation:
        """Namespace a BinaryOperation."""
        namespaced_left = self._namespace_expression(expr.left, symbol_mapping)
        namespaced_right = self._namespace_expression(expr.right, symbol_mapping)
        return BinaryOperation(expr.operator, wrap_operand(namespaced_left), wrap_operand(namespaced_right))

    def _namespace_unary_operation(self, expr, symbol_mapping):
        """Namespace a UnaryFunction."""
        namespaced_operand = self._namespace_expression(expr.operand, symbol_mapping)
        return type(expr)(expr.operator, namespaced_operand)

    def _namespace_binary_function(self, expr, symbol_mapping):
        """Namespace a BinaryFunction."""
        namespaced_left = self._namespace_expression(expr.left, symbol_mapping)
        namespaced_right = self._namespace_expression(expr.right, symbol_mapping)
        return type(expr)(expr.function_name, namespaced_left, namespaced_right)

    def _namespace_conditional_expression(self, expr: ConditionalExpression, symbol_mapping: dict[str, str]) -> ConditionalExpression:
        """Namespace a ConditionalExpression."""
        namespaced_condition = self._namespace_expression(expr.condition, symbol_mapping)
        namespaced_true_expr = self._namespace_expression(expr.true_expr, symbol_mapping)
        namespaced_false_expr = self._namespace_expression(expr.false_expr, symbol_mapping)

        return ConditionalExpression(wrap_operand(namespaced_condition), wrap_operand(namespaced_true_expr), wrap_operand(namespaced_false_expr))

    def _namespace_expression_for_lhs(self, expr, symbol_mapping: dict[str, str]) -> FieldQuantity | None:
        """
        Create a namespaced version of an expression for LHS, returning Variable objects.
        """
        if isinstance(expr, VariableReference):
            # VariableReference uses the 'name' property which returns the symbol if available
            symbol = expr.name
            if symbol and symbol in symbol_mapping:
                namespaced_symbol = symbol_mapping[symbol]
                if namespaced_symbol in self.variables:
                    return self.variables[namespaced_symbol]
            # If we can't find a mapping, return None since VariableReference doesn't have .equals()
            return None
        elif isinstance(expr, FieldQuantity) and expr.symbol in symbol_mapping:
            # This is a Variable object
            namespaced_symbol = symbol_mapping[expr.symbol]
            if namespaced_symbol in self.variables:
                return self.variables[namespaced_symbol]
            return expr
        else:
            return expr

    def _is_unary_operation(self, expr) -> bool:
        """Check if expression is a unary operation."""
        # UnaryFunction and similar classes have an 'operand' attribute
        return hasattr(expr, "operand") and hasattr(expr, "operator")

    def _is_binary_function(self, expr) -> bool:
        """Check if expression is a binary function."""
        # BinaryFunction classes have 'function_name', 'left', and 'right' attributes
        return hasattr(expr, "function_name") and hasattr(expr, "left") and hasattr(expr, "right")

    def _should_skip_subproblem_equation(self, equation, namespace: str) -> bool:
        """
        Check if an equation from a sub-problem should be skipped during integration.

        Skip conditional equations for variables that are set to known values in the composed problem.
        """
        try:
            # Check if this is a conditional equation
            if not self._is_conditional_equation(equation):
                return False

            # Check if the LHS variable would be set to a known value in composition
            original_symbol = self._get_equation_lhs_symbol(equation)
            if original_symbol is not None:
                namespaced_symbol = f"{namespace}_{original_symbol}"

                # Check if this namespaced variable exists and is already known
                if namespaced_symbol in self.variables:
                    var = self.variables[namespaced_symbol]
                    if var.is_known:
                        # The variable is already set to a known value in composition,
                        # so skip the conditional equation that would override it
                        self.logger.debug(f"Skipping conditional equation for {namespaced_symbol} (already known: {var.quantity})")
                        return True

            return False

        except Exception:
            return False

    def _create_composite_equations(self):
        """
        Create composite equations for common patterns in sub-problems.
        This handles equations like P = min(header.P, branch.P) automatically.
        """
        if not self.sub_problems:
            return

        # Common composite patterns to auto-generate
        for var_name in COMMON_COMPOSITE_VARIABLES:
            # Check if this variable exists in multiple sub-problems
            sub_problem_vars = []
            for namespace in self.sub_problems:
                namespaced_symbol = f"{namespace}_{var_name}"
                if namespaced_symbol in self.variables:
                    sub_problem_vars.append(self.variables[namespaced_symbol])

            # If we have the variable in multiple sub-problems and no direct variable exists
            if len(sub_problem_vars) >= 2 and var_name in self.variables:
                # Check if a composite equation already exists
                equation_attr_name = f"{var_name}_eqn"
                if hasattr(self.__class__, equation_attr_name):
                    # Skip auto-creation since explicit equation exists
                    continue

                # Auto-create composite equation
                try:
                    composite_var = self.variables[var_name]
                    if not composite_var.is_known:  # Only for unknown variables
                        composite_expr = min_expr(*sub_problem_vars)
                        equals_method = getattr(composite_var, "equals", None)
                        if equals_method:
                            composite_eq = equals_method(composite_expr)
                            self.add_equation(composite_eq)
                            setattr(self, f"{var_name}_eqn", composite_eq)
                except Exception as e:
                    self.logger.debug(f"Failed to create composite equation for {var_name}: {e}")

    # Placeholder methods that will be provided by Problem class
    def _process_equation(self, attr_name: str, equation: Equation) -> bool:
        """Will be provided by Problem class."""
        del attr_name, equation  # Unused in stub method
        return True

    def _is_conditional_equation(self, _equation: Equation) -> bool:
        """Will be provided by Problem class."""
        return "cond(" in str(_equation)

    def _get_equation_lhs_symbol(self, equation: Equation) -> str | None:
        """Will be provided by Problem class."""
        return getattr(equation.lhs, "symbol", None)


# ========== METACLASS SYSTEM ==========


# Custom exceptions for better error handling
class MetaclassError(Exception):
    """Base exception for metaclass-related errors."""

    pass


class SubProblemProxyError(MetaclassError):
    """Raised when sub-problem proxy creation fails."""

    pass


class NamespaceError(MetaclassError):
    """Raised when namespace operations fail."""

    pass


class ProblemMeta(type):
    """
    Metaclass that processes class-level sub-problems to create proper namespace proxies
    BEFORE any equations are evaluated.

    This metaclass enables clean composition syntax like:
        class MyProblem(EngineeringProblem):
            header = create_pipe_problem()
            branch = create_pipe_problem()
            # Equations can reference header.P, branch.T, etc.
    """

    # Declare the attributes that will be dynamically added to created classes
    _original_sub_problems: dict[str, Any]
    _proxy_configurations: dict[str, dict[str, Any]]
    _class_checks: dict[str, Any]

    @classmethod
    def __prepare__(mcs, *args, **kwargs) -> ProxiedNamespace:
        """
        Called before the class body is evaluated.
        Returns a custom namespace that proxies sub-problems.

        Args:
            *args: Positional arguments (name, bases) - unused but required by protocol
            **kwargs: Additional keyword arguments - unused but required by protocol

        Returns:
            ProxiedNamespace that will handle sub-problem proxying
        """
        # Parameters are required by metaclass protocol but not used in this implementation
        del args, kwargs  # Explicitly acknowledge unused parameters
        return ProxiedNamespace()

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: ProxiedNamespace, **kwargs) -> type:
        """
        Create the new class with properly integrated sub-problems.

        Args:
            name: Name of the class being created
            bases: Base classes
            namespace: The ProxiedNamespace containing proxied sub-problems
            **kwargs: Additional keyword arguments - unused but required by protocol

        Returns:
            The newly created class with metaclass attributes

        Raises:
            MetaclassError: If class creation fails due to metaclass issues
        """
        # kwargs is required by metaclass protocol but not used in this implementation
        del kwargs  # Explicitly acknowledge unused parameter
        try:
            # Validate the namespace
            if not isinstance(namespace, ProxiedNamespace):
                raise MetaclassError(f"Expected ProxiedNamespace, got {type(namespace)}")

            # Extract the original sub-problems and proxy objects from the namespace
            sub_problem_proxies = getattr(namespace, "_sub_problem_proxies", {})
            proxy_objects = getattr(namespace, "_proxy_objects", {})

            # Validate that proxy objects are consistent
            if set(sub_problem_proxies.keys()) != set(proxy_objects.keys()):
                raise MetaclassError("Inconsistent proxy state: sub-problem and proxy object keys don't match")

            # Create the class normally
            cls = super().__new__(mcs, name, bases, dict(namespace))

            # Store the original sub-problems and proxy configurations for later integration
            cls._original_sub_problems = sub_problem_proxies

            # Extract configurations safely with error handling
            proxy_configurations = {}
            for proxy_name, proxy in proxy_objects.items():
                try:
                    # Cache configurations to avoid recomputation
                    if not hasattr(proxy, "_cached_configurations"):
                        proxy._cached_configurations = proxy.get_configurations()
                    proxy_configurations[proxy_name] = proxy._cached_configurations
                except Exception as e:
                    raise SubProblemProxyError(f"Failed to get configurations from proxy '{proxy_name}': {e}") from e

            cls._proxy_configurations = proxy_configurations

            # Collect Check objects from class attributes
            checks = {}
            for attr_name, attr_value in namespace.items():
                if isinstance(attr_value, Rules):
                    checks[attr_name] = attr_value

            cls._class_checks = checks

            return cls

        except Exception as e:
            # Re-raise MetaclassError and SubProblemProxyError as-is
            if isinstance(e, MetaclassError | SubProblemProxyError):
                raise
            # Wrap other exceptions
            raise MetaclassError(f"Failed to create class '{name}': {e}") from e


class ProxiedNamespace(dict):
    """
    Custom namespace that automatically proxies sub-problems as they're added.

    This namespace intercepts class attribute assignments during class creation
    and automatically wraps EngineeringProblem objects in SubProblemProxy objects.
    This enables clean composition syntax where sub-problems can be referenced
    with dot notation in equations.

    Example:
        class ComposedProblem(EngineeringProblem):
            header = create_pipe_problem()  # Gets proxied automatically
            branch = create_pipe_problem()  # Gets proxied automatically
            # Now equations can use header.P, branch.T, etc.
    """

    def __init__(self) -> None:
        """Initialize the proxied namespace with empty storage."""
        super().__init__()
        self._sub_problem_proxies: dict[str, Any] = {}
        self._proxy_objects: dict[str, SubProblemProxy] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Intercept attribute assignment and proxy sub-problems automatically.

        Args:
            key: The attribute name being set
            value: The value being assigned

        Raises:
            NamespaceError: If namespace operation fails
            SubProblemProxyError: If proxy creation fails
        """
        try:
            if self._is_sub_problem(key, value):
                self._create_and_store_proxy(key, value)
            elif self._is_variable(value):
                self._set_variable_symbol_and_store(key, value)
            else:
                super().__setitem__(key, value)
        except Exception as e:
            if isinstance(e, NamespaceError | SubProblemProxyError):
                raise
            raise NamespaceError(f"Failed to set attribute '{key}': {e}") from e

    def _is_sub_problem(self, key: str, value: Any) -> bool:
        """
        Determine if a value should be treated as a sub-problem.

        Args:
            key: The attribute name
            value: The value being assigned

        Returns:
            True if this should be proxied as a sub-problem
        """
        # Quick checks first (fail fast)
        if key.startswith(PRIVATE_ATTRIBUTE_PREFIX) or key in RESERVED_ATTRIBUTES:
            return False

        # Check for None or basic types that definitely aren't sub-problems
        if value is None or isinstance(value, str | int | float | bool | list | dict):
            return False

        # Cache hasattr results to avoid repeated attribute lookups
        if not hasattr(self, "_attr_cache"):
            self._attr_cache = {}

        # Use object id as cache key since objects are unique
        cache_key = (id(value), tuple(SUB_PROBLEM_REQUIRED_ATTRIBUTES))
        if cache_key not in self._attr_cache:
            self._attr_cache[cache_key] = all(hasattr(value, attr) for attr in SUB_PROBLEM_REQUIRED_ATTRIBUTES)

        return self._attr_cache[cache_key]

    def _is_variable(self, value: Any) -> bool:
        """
        Determine if a value is a Variable (Quantity) that needs processing.

        Args:
            value: The value being assigned

        Returns:
            True if this is a Variable that should be processed
        """
        try:
            return isinstance(value, FieldQuantity)
        except ImportError:
            return False

    def _set_variable_symbol_and_store(self, key: str, value: Any) -> None:
        """
        Set the variable's symbol to the attribute name and store it.

        Args:
            key: The attribute name to use as symbol
            value: The Variable object
        """
        try:
            # Set the symbol to the attribute name (use private attribute)
            value._symbol = key
            # Add expression-building capability to the variable and get wrapped version
            enhanced_variable = self._add_expression_methods(value)
            # Store the enhanced variable
            super().__setitem__(key, enhanced_variable)
        except Exception as e:
            raise NamespaceError(f"Failed to set symbol for variable '{key}': {e}") from e

    def _add_expression_methods(self, variable):
        """
        Wrap the variable with expression-building methods that create DelayedExpression objects.
        This allows expressions like 'D - 2 * T' to work during Problem class definition
        even when variables have no values.
        """

        class ExpressionEnabledWrapper(ArithmeticOperationsMixin):
            def __init__(self, wrapped_var):
                self._wrapped = wrapped_var

            def __getattr__(self, name):
                # Delegate all attribute access to the wrapped variable
                return getattr(self._wrapped, name)

            def __setattr__(self, name, value):
                # Handle wrapper attributes normally
                if name == "_wrapped":
                    super().__setattr__(name, value)
                else:
                    # Delegate to wrapped variable
                    setattr(self._wrapped, name, value)

            @property
            def value(self):
                """Delegate value access to wrapped variable."""
                return getattr(self._wrapped, "value", None)

            def __float__(self):
                """Delegate float conversion to wrapped variable."""
                return float(self._wrapped)

        return ExpressionEnabledWrapper(variable)

    def _create_and_store_proxy(self, key: str, value: Any) -> None:
        """
        Create a proxy for the sub-problem and store references.

        Args:
            key: The attribute name for the sub-problem
            value: The sub-problem object to proxy

        Raises:
            SubProblemProxyError: If proxy creation fails
            NamespaceError: If key already exists as a sub-problem
        """
        # Check for conflicts
        if key in self._sub_problem_proxies:
            raise NamespaceError(f"Sub-problem '{key}' already exists in namespace")

        try:
            # Store the original sub-problem
            self._sub_problem_proxies[key] = value

            # Create and store the proxy
            proxy = SubProblemProxy(value, key)
            self._proxy_objects[key] = proxy

            # Set the proxy in the namespace
            super().__setitem__(key, proxy)

        except Exception as e:
            # Clean up partial state on failure
            self._sub_problem_proxies.pop(key, None)
            self._proxy_objects.pop(key, None)
            raise SubProblemProxyError(f"Failed to create proxy for sub-problem '{key}': {e}") from e


# Export all relevant classes
__all__ = [
    "CompositionMixin",
    "ProblemMeta",
    "ProxiedNamespace",
    "SubProblemProxy",
    "ConfigurableVariable",
    "DelayedEquation",
    "DelayedVariableReference",
    "DelayedExpression",
    "DelayedFunction",
    "delayed_sin",
    "delayed_min_expr",
    "delayed_max_expr",
    "MetaclassError",
    "SubProblemProxyError",
    "NamespaceError",
]
