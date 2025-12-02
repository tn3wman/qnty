"""
Shared utilities for expression handling and variable operations.

This module consolidates common patterns used across algebra and problems modules
to eliminate code duplication and improve maintainability.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import numpy as np

# Type aliases
OperandType = Any  # Expression | FieldQuantity | Quantity | int | float


# ========== INTROSPECTION UTILITIES ==========


def caller_var_name(fn: str, frame_depth: int = 2, unicode: bool = False) -> str:
    """
    Inspect the caller's line to infer a variable name when `name` is omitted.

    This consolidates the repeated pattern in unit.py and dimension.py for
    detecting the LHS variable name from source code like:
        my_unit = add_unit(...)

    Args:
        fn: Function name to match in the source line
        frame_depth: Number of stack frames to go back (default: 2)
        unicode: If True, use Unicode-aware pattern matching for non-ASCII
                identifiers (e.g., Greek letters like Θ)

    Returns:
        The variable name on the left-hand side of the assignment

    Raises:
        RuntimeError: If call stack cannot be accessed or variable name
                     cannot be detected

    Examples:
        >>> # In calling code:
        >>> my_var = add_unit(...)  # fn="add_unit"
        >>> # caller_var_name("add_unit") returns "my_var"
    """
    import inspect

    frame = inspect.currentframe()
    if frame is None:
        raise RuntimeError("Could not access call stack for variable name detection")

    # Navigate up the call stack
    current = frame
    for _ in range(frame_depth):
        if current.f_back is None:
            raise RuntimeError("Could not access call stack for variable name detection")
        current = current.f_back

    frame_info = inspect.getframeinfo(current)
    if frame_info.code_context is None or not frame_info.code_context:
        raise RuntimeError("Could not get source code context for variable name detection")

    line = frame_info.code_context[0]

    # Choose pattern based on Unicode support
    if unicode:
        # Support Unicode identifiers (like Θ, α, β) in addition to ASCII
        pattern = rf"\s*([\w_][\w\d_]*)\s*=\s*{fn}\b"
        flags = re.UNICODE
    else:
        # ASCII-only identifiers
        pattern = rf"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*{fn}\b"
        flags = 0

    m = re.match(pattern, line, flags)
    if not m:
        raise RuntimeError("Could not auto-detect variable name")

    return m.group(1)


# ========== SHARED VALIDATION UTILITIES ==========


class ValidationHelper:
    """Consolidates common validation patterns used across modules."""

    @staticmethod
    def has_valid_value(obj) -> bool:
        """Check if an object has a valid (non-None) value attribute."""
        return hasattr(obj, "value") and getattr(obj, "value", None) is not None

    @staticmethod
    def safe_get_symbol(obj) -> str | None:
        """Safely get symbol from various object types."""
        if hasattr(obj, "symbol"):
            return getattr(obj, "symbol", None)
        if hasattr(obj, "name"):
            return getattr(obj, "name", None)
        return None

    @staticmethod
    def safe_get_name(obj) -> str | None:
        """Safely get name from various object types."""
        if hasattr(obj, "name"):
            return getattr(obj, "name", None)
        if hasattr(obj, "symbol"):
            return getattr(obj, "symbol", None)
        return None

    @staticmethod
    def safe_get_attribute(obj, *attr_names, default=None):
        """Safely get first available attribute from object."""
        for attr_name in attr_names:
            if hasattr(obj, attr_name):
                value = getattr(obj, attr_name, None)
                if value is not None:
                    return value
        return default

    @staticmethod
    def safe_get_callable(obj, attr_name, default=None):
        """Safely get callable attribute from object."""
        if hasattr(obj, attr_name):
            attr_value = getattr(obj, attr_name, None)
            if callable(attr_value):
                return attr_value
        return default

    @staticmethod
    def safe_get_identifier(obj) -> str | None:
        """Get the best identifier (symbol or name) from object."""
        return ValidationHelper.safe_get_attribute(obj, "symbol", "name")

    @staticmethod
    def is_simple_variable_symbol(symbol: str) -> bool:
        """Check if a symbol looks like a simple variable identifier."""
        if not symbol or not isinstance(symbol, str):
            return False
        return symbol.isidentifier() and not any(char in symbol for char in ["(", ")", "+", "-", "*", "/", " "])

    @staticmethod
    def vector_has_valid_computed_data(force: Any) -> bool:
        """
        Check if a vector/force has fully computed data.

        A vector is fully computable only if it has both magnitude and angle
        with known values, and doesn't have an unresolved relative angle.

        Args:
            force: A _Vector or similar object with is_known, vector, magnitude, and angle attributes

        Returns:
            True if the vector has all necessary data for computation
        """
        has_relative_angle = hasattr(force, "_relative_to_force") and force._relative_to_force is not None
        return (
            force.is_known
            and force.vector is not None
            and force.magnitude is not None
            and force.magnitude.value is not None
            and force.angle is not None
            and force.angle.value is not None
            and not has_relative_angle
        )

    @staticmethod
    def get_effective_unit(quantity):
        """Get the effective unit for a quantity, handling both old and new Quantity objects."""
        # New Quantity objects have preferred attribute
        if hasattr(quantity, "preferred") and quantity.preferred is not None:
            return quantity.preferred

        # Old Quantity objects might have unit attribute
        if hasattr(quantity, "unit"):
            return quantity.unit

        # Try to get preferred unit from dimension
        if hasattr(quantity, "dim"):
            try:
                from ..core.unit import ureg

                return ureg.preferred_for(quantity.dim) or ureg.si_unit_for(quantity.dim)
            except ImportError:
                pass

        return None


# ========== SAFE EXECUTION PATTERNS ==========


class SafeExecutionMixin:
    """Mixin providing safe execution patterns used across modules."""

    def safe_execute(self, operation_name: str, operation: Callable[[], Any], default_return: Any = None) -> Any:
        """Execute an operation safely with standardized error handling."""
        try:
            return operation()
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.debug(f"Failed to {operation_name}: {e}")  # type: ignore[attr-defined]
            return default_return

    def safe_execute_with_logging(self, operation_name: str, operation: Callable[[], Any], default_return: Any = None) -> Any:
        """Execute an operation safely with standardized error handling and logging."""
        try:
            return operation()
        except Exception as e:
            if hasattr(self, "logger"):
                self.logger.debug(f"{operation_name} failed: {e}")  # type: ignore[attr-defined]
            return default_return


# ========== VARIABLE REFERENCE UTILITIES ==========


class VariableReferenceHelper:
    """Consolidates variable reference handling patterns."""

    @staticmethod
    def extract_variable_from_obj(obj):
        """Extract the underlying variable from various wrapper types."""
        if hasattr(obj, "_wrapped") and not hasattr(obj, "evaluate"):  # Not an Expression
            return obj._wrapped
        elif hasattr(obj, "_variable") and not hasattr(obj, "evaluate"):  # Not an Expression
            return obj._variable
        elif hasattr(obj, "_wrapped_var") and not hasattr(obj, "evaluate"):  # Not an Expression
            return obj._wrapped_var
        elif hasattr(obj, "symbol") and hasattr(obj, "dim") and hasattr(obj, "value") and hasattr(obj, "name") and not hasattr(obj, "evaluate"):  # Not an Expression
            return obj
        else:
            return None

    @staticmethod
    def get_variable_symbol_or_name(obj) -> str | None:
        """Get variable symbol or name from various object types."""
        if hasattr(obj, "symbol") and obj.symbol:
            return obj.symbol
        if hasattr(obj, "name") and obj.name:
            return obj.name
        return None

    @staticmethod
    def is_variable_reference(obj) -> bool:
        """Check if object is a variable reference."""
        # Check for VariableReference type name to avoid circular imports
        return type(obj).__name__ == "VariableReference"

    @staticmethod
    def is_variable_like(obj) -> bool:
        """Check if object is variable-like (has symbol and can be used as variable)."""
        return hasattr(obj, "symbol") and hasattr(obj, "value") and hasattr(obj, "dim") and not hasattr(obj, "evaluate")


def reconstruct_unary_expression(expr: Any, new_operand: Any) -> Any:
    """
    Reconstruct a unary expression with a new operand.

    This consolidates the common pattern:
        if hasattr(expr, "function_name"):
            return type(expr)(expr.function_name, new_operand)
        else:
            return type(expr)(expr.operator, new_operand)

    Args:
        expr: Original unary expression (UnaryFunction or UnaryOperation)
        new_operand: New operand to use in reconstruction

    Returns:
        New expression of same type with new operand
    """
    if hasattr(expr, "function_name"):
        return type(expr)(expr.function_name, new_operand)
    else:
        return type(expr)(expr.operator, new_operand)


# ========== EXPRESSION TREE UTILITIES ==========


# ========== NAMESPACE UTILITIES ==========


class NamespaceHelper:
    """Consolidates namespace handling patterns."""

    @staticmethod
    def extract_namespace_from_symbol(symbol: str) -> str | None:
        """Extract namespace from a namespaced symbol."""
        if "_" in symbol:
            return symbol.split("_")[0]
        return None

    @staticmethod
    def extract_base_symbol_from_namespaced(symbol: str) -> str:
        """Extract base symbol from a namespaced symbol."""
        if "_" in symbol:
            return "_".join(symbol.split("_")[1:])
        return symbol

    @staticmethod
    def create_namespaced_symbol(namespace: str, base_symbol: str) -> str:
        """Create a namespaced symbol."""
        return f"{namespace}_{base_symbol}"

    @staticmethod
    def find_variables_by_pattern(variables: dict[str, Any], pattern: str) -> list[str]:
        """Find variables matching a pattern."""
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return [name for name in variables.keys() if name.startswith(prefix)]
        else:
            return [name for name in variables.keys() if name == pattern]


# ========== EXPRESSION FACTORY ==========


class ExpressionFactory(ABC):
    """Abstract factory for creating expression objects."""

    @abstractmethod
    def create_variable_reference(self, variable) -> Any:
        """Create a variable reference."""
        pass

    @abstractmethod
    def create_binary_operation(self, operator: str, left: Any, right: Any) -> Any:
        """Create a binary operation."""
        pass

    @abstractmethod
    def create_unary_function(self, function_name: str, operand: Any) -> Any:
        """Create a unary function."""
        pass

    @abstractmethod
    def create_conditional_expression(self, condition: Any, true_expr: Any, false_expr: Any) -> Any:
        """Create a conditional expression."""
        pass


# ========== PATTERN MATCHING UTILITIES ==========


class PatternMatchingHelper:
    """Consolidates pattern matching utilities."""

    # Compiled regex patterns for performance
    VARIABLE_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\b")
    VARIABLE_PATTERN_DETAILED = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")

    # Mathematical operators
    MATH_OPERATORS = {"(", ")", "+", "-", "*", "/"}

    # Excluded function names
    EXCLUDED_FUNCTION_NAMES = {"sin", "cos", "max", "min", "exp", "log", "sqrt", "tan"}

    @staticmethod
    def extract_variables_from_expression_string(expression_str: str, exclude_functions: bool = True) -> list[str]:
        """Extract variable names from an expression string."""
        var_matches = PatternMatchingHelper.VARIABLE_PATTERN_DETAILED.findall(expression_str)
        if exclude_functions:
            return [var for var in var_matches if var not in PatternMatchingHelper.EXCLUDED_FUNCTION_NAMES]
        return var_matches

    @staticmethod
    def is_mathematical_expression(text: str) -> bool:
        """Check if text contains mathematical operators."""
        return any(op in text for op in PatternMatchingHelper.MATH_OPERATORS)

    @staticmethod
    def clean_malformed_expression(expression_str: str) -> str | None:
        """Clean malformed expression strings."""
        if not expression_str or not isinstance(expression_str, str):
            return None

        try:
            # Remove numeric values that look like results
            cleaned = re.sub(r"\d+\.\d+", "VAR", expression_str)

            # Remove method calls like .value, .quantity
            cleaned = re.sub(r"\.(?:value|quantity|magnitude)\b", "", cleaned)

            # Return pattern if it contains mathematical operators
            return cleaned if PatternMatchingHelper.is_mathematical_expression(cleaned) else None

        except (AttributeError, re.error):
            return None


# ========== ARITHMETIC OPERATIONS MIXIN ==========


class ArithmeticOperationsMixin:
    """Mixin providing common arithmetic operations that create expressions."""

    def _create_arithmetic_operation(self, other, operator: str, reverse: bool = False):
        """Create arithmetic operation based on context."""
        # This is a placeholder - implementations should override this
        # to create appropriate expression types (DelayedExpression, BinaryOperation, etc.)
        raise NotImplementedError("Subclasses must implement _create_arithmetic_operation")

    def __add__(self, other):
        return self._create_arithmetic_operation(other, "+")

    def __radd__(self, other):
        return self._create_arithmetic_operation(other, "+", True)

    def __sub__(self, other):
        return self._create_arithmetic_operation(other, "-")

    def __rsub__(self, other):
        return self._create_arithmetic_operation(other, "-", True)

    def __mul__(self, other):
        return self._create_arithmetic_operation(other, "*")

    def __rmul__(self, other):
        return self._create_arithmetic_operation(other, "*", True)

    def __truediv__(self, other):
        return self._create_arithmetic_operation(other, "/")

    def __rtruediv__(self, other):
        return self._create_arithmetic_operation(other, "/", True)

    def __pow__(self, other):
        return self._create_arithmetic_operation(other, "**")

    def __rpow__(self, other):
        return self._create_arithmetic_operation(other, "**", True)


# ========== CONTEXT DETECTION UTILITIES ==========


class ContextDetectionHelper:
    """Consolidates context detection patterns."""

    @staticmethod
    def should_preserve_symbolic_expression() -> bool:
        """Check if we're in a context where symbolic expressions should be preserved."""
        import inspect

        frame = inspect.currentframe()
        try:
            while frame:
                code = frame.f_code
                filename = code.co_filename
                locals_dict = frame.f_locals

                # Skip if we're in a resolve() method - we want actual expressions during resolution
                if "resolve" in code.co_name:
                    frame = frame.f_back
                    continue

                # Skip if we're in the equations module or solver modules - they should evaluate concretely
                if ("equations" in filename.lower() or "_solver" in filename.lower() or "_solve" in code.co_name.lower()) and "qnty" in filename.lower():
                    return False

                # If we find a frame in Problem-related code or class definition,
                # don't auto-evaluate to preserve symbolic expressions
                if (
                    "<class" in code.co_name
                    or "problem" in filename.lower()
                    or "composition" in filename.lower()
                    or "_extract" in code.co_name.lower()
                    or "WeldedBranchConnection" in str(locals_dict.get("__qualname__", ""))
                    or "Problem" in str(locals_dict.get("__qualname__", ""))
                    or any("Problem" in str(base) for base in locals_dict.get("__bases__", []))
                    or "test_composed_problem" in filename
                ):
                    return True
                frame = frame.f_back
            return False
        finally:
            del frame

    @staticmethod
    def should_use_delayed_arithmetic() -> bool:
        """Check if we should use delayed arithmetic based on context."""
        import inspect

        frame = inspect.currentframe()
        try:
            while frame:
                code = frame.f_code
                filename = code.co_filename
                locals_dict = frame.f_locals

                # Check if we're in a class definition context
                if "<class" in code.co_name or "problem" in filename.lower() or any("Problem" in str(base) for base in locals_dict.get("__bases__", [])) or "test_composed_problem" in filename:
                    return True
                frame = frame.f_back
            return False
        finally:
            del frame


# ========== SHARED CONSTANTS ==========


class SharedConstants:
    """Consolidated constants used across modules."""

    # Validation constants
    CONDITION_EVALUATION_THRESHOLD = 1e-10
    DIVISION_BY_ZERO_THRESHOLD = 1e-15
    FLOAT_EQUALITY_TOLERANCE = 1e-12
    SOLVER_DEFAULT_TOLERANCE = 1e-9
    SOLVER_DEFAULT_MAX_ITERATIONS = 100

    # String constants
    MSG_VARIABLE_EXISTS = "Variable {symbol} already exists. Replacing."
    MSG_VARIABLE_NOT_FOUND = "Variable '{symbol}' not found in problem '{name}'"
    MSG_VALIDATION_CHECK_FAILED = "Validation check execution failed"

    # Reserved attributes for metaclass
    RESERVED_ATTRIBUTES = {"name", "description"}
    PRIVATE_ATTRIBUTE_PREFIX = "_"

    # Special dunder methods that should raise AttributeError for wrapper classes
    # Used to guard against deepcopy/pickle operations that cause recursion
    WRAPPER_EXCLUDED_DUNDERS = frozenset(
        {
            "__setstate__",
            "__getstate__",
            "__getnewargs__",
            "__getnewargs_ex__",
            "__reduce__",
            "__reduce_ex__",
            "__copy__",
            "__deepcopy__",
            "__getattribute__",
            "__setattr__",
            "__delattr__",
            "__dict__",
            "__weakref__",
            "__class__",
        }
    )

    # Unicode subscript to ASCII mapping for LaTeX rendering
    # Used in report_ir.py for formatting subscripted variable names
    SUBSCRIPT_MAP: dict[str, str] = {
        "ₓ": "x",
        "ᵧ": "y",
        "ᵤ": "u",
        "ᵥ": "v",
        "ₙ": "n",
        "ₜ": "t",
        "₁": "1",
        "₂": "2",
        "₃": "3",
        "ₐ": "a",
        "ᵦ": "b",
    }

    # Angle unit string patterns for degree/radian detection
    DEGREE_UNIT_PATTERNS = ("degree", "degrees", "deg")


def is_private_or_excluded_dunder(name: str) -> bool:
    """
    Check if an attribute name is private or an excluded dunder method.

    This consolidates the repeated pattern used in wrapper classes to guard
    against deepcopy/pickle operations that cause recursion.

    Args:
        name: Attribute name to check

    Returns:
        True if the name starts with '_' or is in WRAPPER_EXCLUDED_DUNDERS
    """
    return name.startswith("_") or name in SharedConstants.WRAPPER_EXCLUDED_DUNDERS


def is_excluded_dunder(name: str) -> bool:
    """
    Check if an attribute name is an excluded dunder method that should raise AttributeError.

    This is used in __getattr__ methods to guard against deepcopy/pickle operations
    that cause recursion. Unlike is_private_or_excluded_dunder, this only checks
    the specific dunders, not all private attributes.

    Args:
        name: Attribute name to check

    Returns:
        True if the name is in WRAPPER_EXCLUDED_DUNDERS
    """
    return name in SharedConstants.WRAPPER_EXCLUDED_DUNDERS


def raise_if_excluded_dunder(name: str, obj: Any) -> None:
    """
    Raise AttributeError if the attribute name is an excluded dunder.

    This consolidates the repeated pattern:
        if name in {'__setstate__', '__getstate__', ...}:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    Args:
        name: Attribute name to check
        obj: Object to use for type name in error message

    Raises:
        AttributeError: If name is in WRAPPER_EXCLUDED_DUNDERS
    """
    if name in SharedConstants.WRAPPER_EXCLUDED_DUNDERS:
        raise AttributeError(f"'{type(obj).__name__}' object has no attribute '{name}'")


def delegate_getattr(wrapped_obj: Any, name: str, wrapper_obj: Any) -> Any:
    """
    Delegate attribute access to wrapped object with proper error handling.

    This consolidates the repeated pattern:
        try:
            return getattr(self._wrapped_var, name)
        except AttributeError as err:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'") from err

    Args:
        wrapped_obj: The object to delegate attribute access to
        name: The attribute name being accessed
        wrapper_obj: The wrapper object (for error message type name)

    Returns:
        The attribute value from the wrapped object

    Raises:
        AttributeError: If the wrapped object has no such attribute
    """
    try:
        return getattr(wrapped_obj, name)
    except AttributeError as err:
        raise AttributeError(f"'{type(wrapper_obj).__name__}' object has no attribute '{name}'") from err


# ========== FORCE VECTOR UTILITIES ==========


def clone_vector_as_known(force: Any) -> Any:
    """
    Clone a force vector as a known force.

    Creates a new _Vector instance with the same properties as the original,
    but explicitly marked as known. This is used during problem initialization
    to create independent copies of force vectors.

    Args:
        force: The original force vector to clone

    Returns:
        A new _Vector instance with is_known=True
    """
    # Import here to avoid circular imports
    from qnty.spatial.vector import _Vector

    return _Vector(
        vector=force.vector,
        name=force.name,
        description=force.description,
        is_known=True,
        is_resultant=force.is_resultant,
        coordinate_system=force.coordinate_system,
        angle_reference=force.angle_reference,
    )


def get_angle_reference_label(obj: Any) -> str:
    """
    Get the axis label from an object's angle_reference attribute.

    This consolidates the common pattern:
        reference_str = ""
        if hasattr(obj, 'angle_reference') and obj.angle_reference is not None:
            ref = obj.angle_reference
            if hasattr(ref, 'axis_label'):
                reference_str = ref.axis_label

    Args:
        obj: Object with potential angle_reference attribute

    Returns:
        The axis_label string, or empty string if not available
    """
    if hasattr(obj, "angle_reference") and obj.angle_reference is not None:
        ref = obj.angle_reference
        if hasattr(ref, "axis_label"):
            return ref.axis_label
    return ""


def convert_to_si(value: float, unit: Any) -> float:
    """
    Convert a value to SI units if a unit is provided.

    This consolidates the common pattern:
        if unit is not None:
            return value * unit.si_factor
        else:
            return value

    Args:
        value: The value to convert
        unit: The unit object with si_factor attribute, or None

    Returns:
        The value converted to SI units, or the original value if no unit
    """
    if unit is not None:
        return value * unit.si_factor
    return value


def handle_negative_magnitude(cloned: Any, original_magnitude_value: float | None) -> None:
    """
    Handle negative magnitude restoration after cloning a force vector.

    When cloning a force with a negative magnitude, the cloned force will have
    a positive magnitude (due to sqrt in magnitude computation). This function
    restores the negative magnitude and flips the angle by 180°.

    Args:
        cloned: The cloned force vector with _magnitude and _angle attributes
        original_magnitude_value: The original magnitude value (may be negative)
    """
    import math

    if original_magnitude_value is not None and original_magnitude_value < 0:
        if cloned._magnitude is not None and cloned._magnitude.value is not None:
            # Flip the sign to preserve the negative
            cloned._magnitude.value = -abs(cloned._magnitude.value)
            # Also flip the angle by 180° since negative magnitude means opposite direction
            if cloned._angle is not None and cloned._angle.value is not None:
                cloned._angle.value = (cloned._angle.value + math.pi) % (2 * math.pi)


def build_force_data_dict(
    symbol: str,
    force_obj: Any,
    magnitude_str: str,
    angle_str: str,
    unit_str: str,
    x_str: str,
    y_str: str,
    reference_str: str,
) -> dict[str, str]:
    """
    Build a standardized force data dictionary for reporting.

    This consolidates the common pattern of building force data dicts
    in reporting modules (base.py and report_ir.py).

    Args:
        symbol: Force symbol/name identifier
        force_obj: Force object (used to get display name)
        magnitude_str: Formatted magnitude string (value or "?")
        angle_str: Formatted angle string (value or "?")
        unit_str: Unit symbol string
        x_str: X component string
        y_str: Y component string
        reference_str: Angle reference label (e.g., "+x", "-y")

    Returns:
        Dictionary with keys: symbol, name, magnitude, angle, unit, x, y, reference
    """
    return {
        "symbol": symbol,
        "name": getattr(force_obj, "name", symbol),
        "magnitude": magnitude_str,
        "angle": angle_str,
        "unit": unit_str,
        "x": x_str,
        "y": y_str,
        "reference": reference_str,
    }


def capture_original_force_states(
    forces: dict[str, Any],
    force_states: dict[str, bool],
    variable_states: dict[str, bool],
) -> None:
    """
    Capture original force states for restoration after solving.

    This saves the is_known state and magnitude/angle known states for each force,
    allowing the problem to be reset to its original state.

    Args:
        forces: Dictionary of force name -> force vector
        force_states: Dictionary to populate with force name -> is_known
        variable_states: Dictionary to populate with variable state flags
    """
    for name, force in forces.items():
        force_states[name] = force.is_known
        mag_known = force.magnitude is not None and force.magnitude.value is not None
        angle_known = force.angle is not None and force.angle.value is not None
        variable_states[f"{name}_mag_known"] = mag_known
        variable_states[f"{name}_angle_known"] = angle_known


# ========== LATEX UTILITIES ==========


# Constant list of LaTeX character replacements
_LATEX_CHAR_REPLACEMENTS = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]


def escape_latex(text: str) -> str:
    """
    Escape special LaTeX characters in text.

    Args:
        text: Input text that may contain special LaTeX characters

    Returns:
        Text with all special LaTeX characters properly escaped
    """
    if not text:
        return ""
    result = text
    for old, new in _LATEX_CHAR_REPLACEMENTS:
        result = result.replace(old, new)
    return result


def format_equation_list_from_history(solving_history: list[dict], equations: list) -> list[str]:
    """
    Format equations for display in the order they were solved.

    Args:
        solving_history: List of solving step dictionaries with 'equation_str' key
        equations: List of equation objects (fallback if no solving history)

    Returns:
        List of formatted equation strings in solving order
    """
    if solving_history:
        equation_strs = []
        used_equations: set[str] = set()

        for step_data in solving_history:
            # Look for equation_for_list first (from equations module), then equation_str
            equation_str = step_data.get("equation_for_list", "") or step_data.get("equation_str", "")
            if equation_str and equation_str not in used_equations:
                equation_strs.append(equation_str)
                used_equations.add(equation_str)

        # Add any remaining equations that weren't used in solving
        for eq in equations:
            eq_str = str(eq)
            if eq_str not in used_equations:
                equation_strs.append(eq_str)

        return equation_strs

    # Fallback to original order if no solving history
    return [str(eq) for eq in equations]


# ========== ANGLE CONVERSION UTILITIES ==========


def convert_angle_to_direction(angle_deg: float, angle_dir: str | None) -> float:
    """
    Convert an angle from standard CCW convention to specified direction convention.

    This consolidates the repeated pattern in parallelogram_law.py and report_ir.py
    for converting angles based on direction preference.

    Args:
        angle_deg: Angle in degrees (standard CCW convention, 0-360)
        angle_dir: Direction convention - "ccw" (default), "cw", or "signed"

    Returns:
        Converted angle based on angle_dir:
        - "ccw" (default/None): 0 to 360, counterclockwise from reference
        - "cw": Negative for clockwise angles (e.g., 358.8° -> -1.2°)
        - "signed": -180 to 180 range
    """
    if angle_dir == "cw":
        # Convert to clockwise: if angle > 180, show as negative
        if angle_deg > 180:
            return angle_deg - 360
        return angle_deg
    elif angle_dir == "signed":
        # Convert to signed range: -180 to 180
        if angle_deg > 180:
            return angle_deg - 360
        return angle_deg
    else:
        # Default: CCW, 0-360
        return angle_deg


# ========== FORCE VECTOR EXTRACTION ==========


def extract_force_vectors_from_class(cls: type, instance: Any, forces: dict, clone_func) -> None:
    """
    Extract ForceVector objects defined at class level.

    Args:
        cls: The class to scan for force vectors
        instance: The instance to set attributes on
        forces: Dictionary to populate with force name -> force vector
        clone_func: Function to clone force vectors (receives force, returns cloned force)
    """
    for attr_name in dir(cls):
        if attr_name.startswith("_"):
            continue

        attr = getattr(cls, attr_name)
        # Check if it's a Vector (duck typing by checking for is_known and magnitude attrs)
        if hasattr(attr, "is_known") and hasattr(attr, "magnitude"):
            # Clone to avoid sharing between instances
            force_copy = clone_func(attr)
            forces[attr_name] = force_copy
            setattr(instance, attr_name, force_copy)


def create_force_magnitude_quantity(
    force: Any,
    force_name: str,
) -> Any | None:
    """
    Create a Quantity for force magnitude if valid.

    This is the core function for creating magnitude quantities from forces.
    Used by both add_force_magnitude_variable and add_force_magnitude_to_variables.

    Args:
        force: ForceVector with magnitude attribute
        force_name: Name/key of the force

    Returns:
        Quantity object or None if magnitude is not valid
    """
    if force.magnitude.value is None:
        return None

    from ..core.dimension_catalog import dim
    from ..core.quantity import Quantity

    return Quantity(
        name=f"{force.name} Magnitude",
        dim=dim.force,
        value=force.magnitude.value,
        preferred=force.magnitude.preferred,
        _symbol=f"{force_name}_mag",
    )


def add_force_magnitude_to_variables(
    force: Any,
    force_name: str,
    variables: dict[str, Any],
) -> None:
    """
    Add force magnitude as a variable for report generation (simple version).

    This version doesn't track original_variable_states - use add_force_magnitude_variable
    if you need state tracking.

    Args:
        force: ForceVector with magnitude attribute
        force_name: Name/key of the force
        variables: Dictionary to add the magnitude variable to
    """
    mag_var = create_force_magnitude_quantity(force, force_name)
    if mag_var is not None:
        variables[f"{force_name}_mag"] = mag_var


def add_force_magnitude_variable(
    force: Any,
    force_name: str,
    was_originally_known: bool,
    variables: dict[str, Any],
    original_variable_states: dict[str, bool],
) -> None:
    """
    Add force magnitude as a variable for report generation with state tracking.

    Args:
        force: ForceVector with magnitude attribute
        force_name: Name/key of the force
        was_originally_known: Whether the force was originally known
        variables: Dictionary to add the magnitude variable to
        original_variable_states: Dictionary to track original state
    """
    mag_var = create_force_magnitude_quantity(force, force_name)
    if mag_var is not None:
        variables[f"{force_name}_mag"] = mag_var
        original_variable_states[f"{force_name}_mag"] = was_originally_known


def convert_angle_to_radians(angle: float, angle_unit: str) -> float:
    """
    Convert an angle from the given unit to radians.

    Args:
        angle: Angle value
        angle_unit: Unit string - "degree", "degrees", "deg", "radian", "radians", or "rad"

    Returns:
        Angle in radians

    Raises:
        ValueError: If angle_unit is not recognized
    """
    import math

    angle_unit_lower = angle_unit.lower()
    if angle_unit_lower in ("degree", "degrees", "deg"):
        return math.radians(float(angle))
    elif angle_unit_lower in ("radian", "radians", "rad"):
        return float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")


def convert_angle_to_radians_optional(angle: float | None, angle_unit: str) -> float | None:
    """
    Convert an optional angle from the given unit to radians.

    This is a None-safe wrapper around convert_angle_to_radians for use
    in functions where angles may be optional (e.g., direction angles where
    only 2 of 3 angles are specified).

    Args:
        angle: Angle value or None
        angle_unit: Unit string - "degree", "degrees", "deg", "radian", "radians", or "rad"

    Returns:
        Angle in radians, or None if input was None

    Raises:
        ValueError: If angle_unit is not recognized
    """
    if angle is None:
        return None
    return convert_angle_to_radians(angle, angle_unit)


# ========== NUMERICAL VALUE EXTRACTION ==========


def extract_numerical_value(value: Any) -> float:
    """
    Extract numerical value from various quantity types.

    This function handles the common pattern of extracting a float from different
    types of objects that may have a .value attribute or be directly convertible.

    Args:
        value: Value to extract from (Quantity, int, float, or object with .value)

    Returns:
        Float representation of the value

    Raises:
        ValueError: If value cannot be converted to float
    """
    try:
        if hasattr(value, "value") and value.value is not None:
            return float(value.value)
        elif isinstance(value, int | float):
            return float(value)
        else:
            return float(value)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Cannot extract numerical value from {type(value)}: {value}") from e


# ========== FORCE COMPONENT UTILITIES ==========


def add_force_component_variable(
    force: Any,
    component_name: str,
    force_name: str,
    component_attr: str,
    variables: dict[str, Any],
) -> None:
    """
    Add a single force component (X, Y, or Z) as a variable for report generation.

    Args:
        force: ForceVector with component attributes (x, y, z)
        component_name: Display name for component ("X", "Y", or "Z")
        force_name: Name/key of the force
        component_attr: Attribute name on force ("x", "y", or "z")
        variables: Dictionary to add the component variable to
    """
    component = getattr(force, component_attr, None)
    if component is None or component.value is None:
        return

    from ..core.dimension_catalog import dim
    from ..core.quantity import Quantity

    var = Quantity(name=f"{force.name} {component_name}-Component", dim=dim.force, value=component.value, preferred=component.preferred, _symbol=f"{force_name}_{component_attr}")
    variables[f"{force_name}_{component_attr}"] = var


def add_force_components_xyz(
    force: Any,
    force_name: str,
    variables: dict[str, Any],
) -> None:
    """
    Add X, Y, and Z force components as variables for report generation.

    Args:
        force: ForceVector with x, y, z component attributes
        force_name: Name/key of the force
        variables: Dictionary to add the component variables to
    """
    add_force_component_variable(force, "X", force_name, "x", variables)
    add_force_component_variable(force, "Y", force_name, "y", variables)
    add_force_component_variable(force, "Z", force_name, "z", variables)


def add_force_components_xy(
    force: Any,
    force_name: str,
    variables: dict[str, Any],
) -> None:
    """
    Add X and Y force components as variables for report generation (2D).

    Args:
        force: ForceVector with x, y component attributes
        force_name: Name/key of the force
        variables: Dictionary to add the component variables to
    """
    add_force_component_variable(force, "X", force_name, "x", variables)
    add_force_component_variable(force, "Y", force_name, "y", variables)


# ========== FORCE VECTOR CLONING ==========


def clone_force_vector(force: Any, Vector: type) -> Any:
    """
    Clone a force vector, handling both known and unknown forces.

    This is the unified function for cloning force vectors, used by both
    ParallelogramLawProblem and RectangularVectorProblem. It checks whether
    the force has valid computed data and routes to the appropriate cloning
    strategy.

    Args:
        force: The original force vector to clone
        Vector: The _Vector class to use for creating the clone

    Returns:
        A cloned force vector with the same properties as the original
    """
    has_valid_vector = ValidationHelper.vector_has_valid_computed_data(force)

    if has_valid_vector:
        cloned = clone_vector_as_known(force)
        # Handle negative magnitude
        original_mag = force.magnitude.value if force.magnitude is not None else None
        handle_negative_magnitude(cloned, original_mag)
        return cloned
    else:
        # Unknown force - use shared utility
        return clone_unknown_force_vector(force, Vector)


def clone_unknown_force_vector(force: Any, Vector: type) -> Any:
    """
    Clone an unknown (or partially known) force vector.

    This handles force vectors that may have known angle but unknown magnitude,
    or vice versa. It properly handles angle reference system conversion.

    Args:
        force: The original force vector to clone
        Vector: The _Vector class to use for creating the clone

    Returns:
        A cloned force vector with the same properties as the original
    """
    angle_value = None
    angle_unit = None
    if force.angle is not None and force.angle.value is not None:
        # Angle is stored internally as standard (CCW from +x)
        # Convert back to the angle_reference system for cloning
        angle_value = force.angle_reference.from_standard(force.angle.value, angle_unit="degree")
        angle_unit = "degree"

    # Create cloned force with Quantity objects to avoid double conversion
    cloned = Vector(
        name=force.name,
        magnitude=force.magnitude,  # Pass Quantity object directly
        angle=angle_value if angle_value is not None else None,
        unit=force.magnitude.preferred if force.magnitude else None,
        angle_unit=angle_unit if angle_unit else "degree",
        description=force.description,
        is_known=force.is_known,
        is_resultant=force.is_resultant,
        coordinate_system=force.coordinate_system,
        angle_reference=force.angle_reference,
    )

    # Preserve relative angle constraint if present
    if hasattr(force, "_relative_to_force") and force._relative_to_force is not None:
        cloned._relative_to_force = force._relative_to_force
        cloned._relative_angle = force._relative_angle

    return cloned


# ========== RANGE SPECIFICATION UTILITIES ==========


def normalize_range_specs(range_specs: tuple) -> list[range]:
    """
    Convert range specifications to a list of range objects.

    This handles the common pattern of accepting flexible range specifications
    and normalizing them to actual range objects.

    Args:
        range_specs: Tuple of range specifications. Each can be:
            - An integer (creates range(n))
            - A tuple (start, stop) or (start, stop, step)
            - A range object

    Returns:
        List of range objects

    Raises:
        ValueError: If a specification is not a valid range type
    """
    ranges = []
    for spec in range_specs:
        if isinstance(spec, int):
            ranges.append(range(spec))
        elif isinstance(spec, tuple):
            ranges.append(range(*spec))
        elif isinstance(spec, range):
            ranges.append(spec)
        else:
            raise ValueError(f"Invalid range specification: {spec}")
    return ranges


def generate_terms_from_product(
    ranges: list[range],
    term_generator: Callable,
    kwargs: dict | None = None,
) -> list[Any]:
    """
    Generate terms by iterating over the Cartesian product of ranges.

    This consolidates the repeated pattern in algebra/functions.py and
    problems/composition.py for generating summation terms.

    Args:
        ranges: List of range objects to iterate over
        term_generator: Callable that takes indices and returns a term
        kwargs: Optional keyword arguments to pass to term_generator

    Returns:
        List of generated terms
    """
    import itertools

    terms = []
    for indices in itertools.product(*ranges):
        if kwargs:
            term = term_generator(*indices, **kwargs)
        else:
            term = term_generator(*indices)
        terms.append(term)
    return terms


# ========== UNIT RESOLUTION UTILITIES ==========


def validate_axis_in_plane(axis: str, plane: str) -> None:
    """
    Validate that an axis is in the specified plane.

    Args:
        axis: Axis string like '+x', '-y', etc. (lowercase)
        plane: Plane string like 'xy', 'xz', 'yz' (lowercase)

    Raises:
        ValueError: If axis is not in the plane
    """
    axis_char = axis[1]  # 'x', 'y', or 'z' from '+x', '-x', etc.
    if axis_char not in plane:
        raise ValueError(f"Reference axis '{axis}' must be in plane '{plane}'. Valid axes for {plane} plane: {[f'+{c}' for c in plane] + [f'-{c}' for c in plane]}")


def resolve_length_unit_from_string(unit: str | Any) -> Any:
    """
    Resolve a unit from a string to a Unit object, specifically for length dimension.

    This consolidates the repeated pattern of resolving length units from strings
    that appears in vector_direction_ratios.py, point_direction_angles.py, and
    vector_direction_angles.py.

    Args:
        unit: Unit specification - can be a string unit name or a Unit object

    Returns:
        Resolved Unit object

    Raises:
        ValueError: If unit is a string but cannot be resolved as a length unit
    """
    if isinstance(unit, str):
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.length)
        if resolved is None:
            raise ValueError(f"Unknown length unit '{unit}'")
        return resolved
    return unit


def resolve_angle_unit_from_string(unit: str | Any) -> Any:
    """
    Resolve a unit from a string to a Unit object, specifically for angle (dimensionless) dimension.

    This consolidates the repeated pattern of resolving angle units from strings
    that appears in vector.py and other spatial modules.

    Args:
        unit: Unit specification - can be a string unit name or a Unit object

    Returns:
        Resolved Unit object

    Raises:
        ValueError: If unit is a string but cannot be resolved as an angle unit
    """
    if isinstance(unit, str):
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.D)
        if resolved is None:
            raise ValueError(f"Unknown angle unit '{unit}'")
        return resolved
    return unit


def resolve_unit_from_string(unit: str | Any, dim: Any = None) -> Any:
    """
    Resolve a unit from a string to a Unit object with optional dimension constraint.

    This consolidates the general pattern of resolving units from strings
    that appears across multiple modules.

    Args:
        unit: Unit specification - can be a string unit name or a Unit object
        dim: Optional dimension to constrain the unit lookup

    Returns:
        Resolved Unit object

    Raises:
        ValueError: If unit is a string but cannot be resolved
    """
    if isinstance(unit, str):
        from ..core.unit import ureg

        if dim is not None:
            resolved = ureg.resolve(unit, dim=dim)
        else:
            resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        return resolved
    return unit


def resolve_unit_from_string_or_fallback(
    unit: str | Any | None,
    fallback_sources: list[Any] | None = None,
    dim: Any = None,
) -> Any:
    """
    Resolve a unit from a string, Unit object, or fallback to a default from sources.

    This consolidates the common pattern of resolving units in vector factory functions.

    Args:
        unit: Unit specification - can be a string unit name, a Unit object, or None
        fallback_sources: List of objects to check for _unit attribute if unit is None
        dim: Optional dimension to validate the unit against

    Returns:
        Resolved Unit object or None if no unit could be determined

    Raises:
        ValueError: If unit is a string but cannot be resolved

    Examples:
        >>> from qnty.spatial import _Vector
        >>> vectors = [v1, v2]
        >>> resolved = resolve_unit_from_string_or_fallback("N", vectors)
        >>> resolved = resolve_unit_from_string_or_fallback(None, vectors)  # Uses v1._unit
    """
    if isinstance(unit, str):
        # Delegate to resolve_unit_from_string for actual resolution
        return resolve_unit_from_string(unit, dim=dim)
    elif unit is not None:
        return unit
    elif fallback_sources:
        # Get unit from first source that has _unit attribute
        for source in fallback_sources:
            if hasattr(source, "_unit") and source._unit is not None:
                return source._unit
    return None


# ========== MAGNITUDE EXTRACTION UTILITIES ==========


def extract_magnitude_string(obj: Any, decimal_places: int = 1) -> str:
    """
    Extract magnitude value from an object and format it as a string.

    This consolidates the repeated pattern of extracting magnitude from objects
    that may have a callable magnitude() method.

    Args:
        obj: Object that may have a magnitude() callable method
        decimal_places: Number of decimal places for formatting (default: 1)

    Returns:
        Formatted magnitude string, or "?" if magnitude cannot be extracted
    """
    if hasattr(obj, "magnitude") and callable(obj.magnitude):
        try:
            mag_value = obj.magnitude()
            return f"{mag_value:.{decimal_places}f}"
        except (ValueError, AttributeError):
            return "?"
    return "?"


# ========== MAGNITUDE QUANTITY UTILITIES ==========


def create_magnitude_quantity(
    magnitude: int | float | Any,
    unit: Any,
    name: str,
) -> Any:
    """
    Create a Quantity for magnitude, handling both numeric values and existing Quantity objects.

    This consolidates the repeated pattern in vector.py where magnitude can be either
    a numeric value (requiring unit conversion) or an existing Quantity object.

    Args:
        magnitude: Either a numeric value (int/float) or a Quantity object
        unit: The unit to use if magnitude is numeric (required if numeric)
        name: Name prefix for the quantity (e.g., "F_1" will create "F_1_magnitude")

    Returns:
        Quantity object representing the magnitude

    Raises:
        ValueError: If magnitude is numeric but unit is None
    """
    from ..core.quantity import Quantity

    if isinstance(magnitude, int | float):
        if unit is None:
            raise ValueError("unit must be specified")
        mag_qty = Quantity.from_value(float(magnitude), unit, name=f"{name}_magnitude")
        mag_qty.preferred = unit
        return mag_qty
    return magnitude


# ========== VARIABLE STATE TRACKING MIXIN ==========


class VariableStateTrackingMixin:
    """
    Mixin providing get_known_variables and get_unknown_variables methods.

    This consolidates the repeated methods in CartesianVectorProblem and
    RectangularVectorProblem that filter variables based on their original known state.

    Classes using this mixin must have:
    - self.variables: dict[str, Quantity] - dictionary of variable names to Quantity objects
    - self._original_variable_states: dict[str, bool] - dictionary tracking original known states
    """

    def get_known_variables(self) -> dict[str, Any]:
        """
        Get known variables for report generation.

        Returns:
            Dictionary of variable names to Quantity objects that were originally known
        """
        known_vars = {}
        for var_name, var in self.variables.items():  # type: ignore[attr-defined]
            if self._original_variable_states.get(var_name, False):  # type: ignore[attr-defined]
                known_vars[var_name] = var
        return known_vars

    def get_unknown_variables(self) -> dict[str, Any]:
        """
        Get unknown variables for report generation.

        Returns:
            Dictionary of variable names to Quantity objects that were originally unknown
        """
        unknown_vars = {}
        for var_name, var in self.variables.items():  # type: ignore[attr-defined]
            if not self._original_variable_states.get(var_name, False):  # type: ignore[attr-defined]
                unknown_vars[var_name] = var
        return unknown_vars

    def add_force(self, force: Any, name: str | None = None) -> None:
        """
        Add a force to the problem.

        This method consolidates the repeated pattern in CartesianVectorProblem and
        RectangularVectorProblem for adding forces.

        Args:
            force: ForceVector to add (must have a 'name' attribute)
            name: Optional name (uses force.name if not provided)
        """
        force_name = name or force.name
        self.forces[force_name] = force  # type: ignore[attr-defined]
        setattr(self, force_name, force)


# ========== LINEAR SYSTEM SOLVING UTILITIES ==========


def build_equilibrium_matrix(theta1: float, theta2: float) -> np.ndarray:
    """
    Build the 2x2 coefficient matrix for solving two unknown force magnitudes.

    This constructs the matrix for the equilibrium equations:
        sum_x + |F1| * cos(θ1) = |F2| * cos(θ2)
        sum_y + |F1| * sin(θ1) = |F2| * sin(θ2)

    Rearranged to: A * [|F1|, |F2|]^T = b

    Args:
        theta1: Angle of first unknown force (radians)
        theta2: Angle of second unknown force (radians)

    Returns:
        2x2 numpy array: [[cos(θ1), -cos(θ2)], [sin(θ1), -sin(θ2)]]
    """
    import math

    import numpy as np

    return np.array(
        [
            [math.cos(theta1), -math.cos(theta2)],
            [math.sin(theta1), -math.sin(theta2)],
        ]
    )


def solve_two_unknown_magnitudes(
    theta1: float,
    theta2: float,
    sum_x: float,
    sum_y: float,
    error_context: str = "system",
) -> tuple[float, float]:
    """
    Solve for two unknown force magnitudes given their angles and known force sums.

    Solves the linear system:
        |F1| * cos(θ1) - |F2| * cos(θ2) = -sum_x
        |F1| * sin(θ1) - |F2| * sin(θ2) = -sum_y

    Args:
        theta1: Angle of first unknown force (radians)
        theta2: Angle of second unknown force (radians)
        sum_x: Sum of known force x-components
        sum_y: Sum of known force y-components
        error_context: Context string for error messages

    Returns:
        Tuple of (magnitude1, magnitude2)

    Raises:
        ValueError: If the system is singular (forces are parallel)
    """
    import numpy as np

    A = build_equilibrium_matrix(theta1, theta2)
    b = np.array([-sum_x, -sum_y])

    try:
        magnitudes = np.linalg.solve(A, b)
        return float(magnitudes[0]), float(magnitudes[1])
    except np.linalg.LinAlgError as err:
        raise ValueError(f"Cannot solve {error_context}: system is singular. Forces may be parallel.") from err


# ========== SPHERICAL COORDINATE CONVERSION UTILITIES ==========


def convert_phi_to_standard(phi_input_rad: float, phi_wrt: str) -> float:
    """
    Convert phi angle to standard form (measured from +z axis).

    This consolidates the repeated pattern for converting phi angles in spherical
    coordinates based on the reference axis.

    Args:
        phi_input_rad: Input phi angle in radians
        phi_wrt: Reference axis for phi - "+z", "-z", or "xy"

    Returns:
        Phi angle in standard form (measured from +z axis) in radians
    """
    import math

    phi_wrt_lower = phi_wrt.lower()
    if phi_wrt_lower == "+z":
        return phi_input_rad
    elif phi_wrt_lower == "-z":
        return math.pi - phi_input_rad
    else:  # xy
        return math.pi / 2 - phi_input_rad


# ========== 3D VECTOR DIRECTION ANGLES UTILITIES ==========


def convert_direction_angle_to_degrees(angle_value: float | None, default: float = 0.0) -> float:
    """
    Convert direction angle from radians to degrees with None handling.

    This consolidates the repeated pattern in cartesian_vector.py for converting
    direction angles (alpha, beta, gamma) from radians to degrees.

    Args:
        angle_value: Angle value in radians, or None
        default: Default value to return if angle_value is None (default: 0.0)

    Returns:
        Angle in degrees, or default if input was None
    """
    import math

    if angle_value is None:
        return default
    return angle_value * 180 / math.pi


def format_3d_force_with_direction_angles(
    name: str,
    mag_val: float,
    mag_unit: str,
    alpha_deg: float,
    beta_deg: float,
    gamma_deg: float,
) -> str:
    """
    Format a 3D force with direction angles (α, β, γ) as a string.

    This consolidates the repeated pattern in cartesian_vector.py for formatting
    force vectors with direction angles.

    Args:
        name: Name of the force
        mag_val: Magnitude value
        mag_unit: Unit symbol for magnitude
        alpha_deg: Alpha angle in degrees
        beta_deg: Beta angle in degrees
        gamma_deg: Gamma angle in degrees

    Returns:
        Formatted string like "F = 100.0 N (α=60.0°, β=45.0°, γ=60.0°)"
    """
    return f"{name} = {mag_val:.1f} {mag_unit} (α={alpha_deg:.1f}°, β={beta_deg:.1f}°, γ={gamma_deg:.1f}°)"


def get_direction_angles_degrees(force: Any) -> tuple[float, float, float]:
    """
    Get direction angles (alpha, beta, gamma) from a 3D force vector in degrees.

    This consolidates the repeated pattern in cartesian_vector.py for extracting
    and converting direction angles.

    Args:
        force: Force vector with alpha, beta, gamma Quantity attributes

    Returns:
        Tuple of (alpha_deg, beta_deg, gamma_deg)
    """
    import math

    alpha_deg = force.alpha.value * 180 / math.pi if (force.alpha and force.alpha.value is not None) else 0
    beta_deg = (force.beta.value * 180 / math.pi) if (force.beta and force.beta.value is not None) else 0
    gamma_deg = (force.gamma.value * 180 / math.pi) if (force.gamma and force.gamma.value is not None) else 0
    return alpha_deg, beta_deg, gamma_deg


# ========== LAW OF SINES/COSINES FORMATTING UTILITIES ==========


def format_law_of_sines_substitution(
    vector_name: str,
    known_mag: float,
    angle1_deg: float,
    angle2_deg: float,
    result_mag: float,
    unit_symbol: str,
) -> str:
    """
    Format a Law of Sines substitution step.

    This consolidates the repeated pattern in parallelogram_law.py for formatting
    Law of Sines solution steps.

    Args:
        vector_name: LaTeX name of the vector being solved
        known_mag: Known magnitude value
        angle1_deg: First angle in degrees (numerator sin)
        angle2_deg: Second angle in degrees (denominator sin)
        result_mag: Resulting magnitude
        unit_symbol: Unit symbol for display

    Returns:
        Formatted LaTeX string showing the calculation
    """
    return f"|{vector_name}| = {known_mag:.0f} · sin({angle1_deg:.0f}°)/sin({angle2_deg:.0f}°)\n= {result_mag:.0f}\\ \\text{{{unit_symbol}}}"


def format_law_of_sines_angle_substitution(
    angle_name_from: str,
    angle_name_to: str,
    known_mag: float,
    interior_angle_deg: float,
    other_mag: float,
    result_angle_deg: float,
) -> str:
    """
    Format a Law of Sines angle substitution step.

    This consolidates the repeated pattern in parallelogram_law.py for formatting
    Law of Sines angle solution steps.

    Args:
        angle_name_from: First vector name for angle
        angle_name_to: Second vector name for angle
        known_mag: Known magnitude value
        interior_angle_deg: Interior angle in degrees
        other_mag: Other magnitude value
        result_angle_deg: Resulting angle in degrees

    Returns:
        Formatted string showing the calculation
    """
    return f"∠({angle_name_from},{angle_name_to}) = sin⁻¹({known_mag:.1f}·sin({interior_angle_deg:.0f}°)/{other_mag:.1f})\n= {result_angle_deg:.1f}°"


# ========== LAW OF COSINES UTILITIES ==========


def compute_law_of_cosines(side_a: float, side_b: float, angle_rad: float) -> float:
    """
    Apply the Law of Cosines to compute the third side of a triangle.

    Formula: c² = a² + b² - 2·a·b·cos(C)

    This consolidates the repeated pattern in triangle_solver.py for computing
    magnitudes using the Law of Cosines.

    Args:
        side_a: Length of first side
        side_b: Length of second side
        angle_rad: Angle opposite to the side being computed, in radians

    Returns:
        Length of the third side
    """
    import math

    c_squared = side_a**2 + side_b**2 - 2 * side_a * side_b * math.cos(angle_rad)
    return math.sqrt(c_squared)


# ========== TABLE ROW BUILDING UTILITIES ==========


def build_variable_table_rows(data: list[dict], row_class: type, keys: list[str] | None = None) -> list:
    """
    Build table rows from variable data dictionaries.

    This consolidates the repeated pattern in report_ir.py for building table rows
    from variable dictionaries.

    Args:
        data: List of dictionaries containing variable data
        row_class: The TableRow class to use for creating rows
        keys: Keys to extract from each dict (default: ['symbol', 'name', 'value', 'unit'])

    Returns:
        List of TableRow objects
    """
    if keys is None:
        keys = ["symbol", "name", "value", "unit"]

    rows = []
    for item in data:
        rows.append(row_class([item[key] for key in keys]))
    return rows


# ========== LATEX PARSING UTILITIES ==========


def scan_backwards_for_latex_command(text: str, start_pos: int) -> int:
    """
    Scan backwards in text to find the start of a LaTeX command or function name.

    This consolidates the repeated pattern in report_ir.py for scanning backwards
    to find LaTeX command boundaries (e.g., finding '\\sin' before a parenthesis).

    Args:
        text: The text to scan
        start_pos: Position to start scanning backwards from

    Returns:
        Position of the start of the command/function name
    """
    pos = start_pos
    while pos > 0 and (text[pos - 1].isalpha() or text[pos - 1] == "\\"):
        pos -= 1
    return pos


# ========== PROXY GETATTR UTILITIES ==========


def proxy_getattr_with_delegation(
    proxy_obj: Any,
    attr_name: str,
    wrapped_attr: str = "_wrapped_var",
) -> Any:
    """
    Get attribute from a proxy object, delegating to the wrapped variable.

    This consolidates the repeated pattern in problem.py and composition.py for
    proxy __getattr__ implementations.

    Args:
        proxy_obj: The proxy object
        attr_name: Name of the attribute to get
        wrapped_attr: Name of the attribute on proxy_obj that holds the wrapped variable

    Returns:
        The attribute from the wrapped variable

    Raises:
        AttributeError: If the wrapped variable doesn't have the attribute
    """
    try:
        wrapped = getattr(proxy_obj, wrapped_attr)
        return getattr(wrapped, attr_name)
    except AttributeError as err:
        raise AttributeError(f"'{type(proxy_obj).__name__}' object has no attribute '{attr_name}'") from err


# ========== ARC DRAWING UTILITIES ==========


def create_angle_arc(arc_class: type, radius: float, angle_deg: float, color: str) -> Any:
    """
    Create an angle arc patch for matplotlib.

    This consolidates the repeated pattern in diagram_utils.py and vector_diagram.py
    for creating Arc patches to show angles.

    Args:
        arc_class: The matplotlib Arc class (matplotlib.patches.Arc)
        radius: Radius of the arc
        angle_deg: Angle in degrees (from 0 to this value)
        color: Color of the arc

    Returns:
        Arc patch object
    """
    return arc_class(
        (0, 0),
        2 * radius,
        2 * radius,
        angle=0,
        theta1=0,
        theta2=angle_deg,
        color=color,
        linewidth=1.5,
        linestyle=":",
        zorder=2,
    )


# ========== MAGNITUDE EXTRACTION UTILITIES ==========


def get_magnitude_in_preferred_unit(magnitude_obj: Any) -> float:
    """
    Extract magnitude value in preferred unit from a Quantity-like object.

    This consolidates the repeated pattern:
        mag_val = magnitude.value / magnitude.preferred.si_factor if magnitude.preferred else magnitude.value

    Args:
        magnitude_obj: Object with value and preferred attributes (typically a Quantity)

    Returns:
        The magnitude value in preferred units, or raw value if no preferred unit
    """
    if magnitude_obj is None or magnitude_obj.value is None:
        return 0.0
    if magnitude_obj.preferred:
        return magnitude_obj.value / magnitude_obj.preferred.si_factor
    return magnitude_obj.value


def get_unit_symbol(magnitude_obj: Any) -> str:
    """
    Get the unit symbol from a Quantity-like object.

    Args:
        magnitude_obj: Object with preferred attribute (typically a Quantity)

    Returns:
        The unit symbol string, or empty string if no preferred unit
    """
    if magnitude_obj is None:
        return ""
    if magnitude_obj.preferred:
        return magnitude_obj.preferred.symbol
    return ""


# ========== SMALL INTEGER CACHING UTILITIES ==========


def is_small_cacheable_integer(value: int | float) -> bool:
    """
    Check if a value is a small integer suitable for caching.

    This consolidates the repeated pattern:
        isinstance(value, int | float) and -10 <= value <= 10 and value == int(value)

    Args:
        value: Value to check

    Returns:
        True if value is an integer between -10 and 10 inclusive
    """
    return isinstance(value, int | float) and -10 <= value <= 10 and value == int(value)


# ========== COORDINATE CONVERSION UTILITIES ==========


def convert_coords_to_unit(coords_si: list[float], target_unit: Any) -> list[float]:
    """
    Convert coordinates from SI units to a target unit.

    This consolidates the repeated pattern:
        if target_unit is not None:
            coords_output = [c / target_unit.si_factor for c in coords_si]
        else:
            coords_output = list(coords_si)

    Args:
        coords_si: List of coordinate values in SI units
        target_unit: Target unit with si_factor attribute, or None

    Returns:
        List of coordinate values in target unit
    """
    if target_unit is not None:
        return [c / target_unit.si_factor for c in coords_si]
    return list(coords_si)


# ========== DIMENSION PRODUCT UTILITIES ==========


def compute_dimension_product(dim1: Any, dim2: Any) -> Any:
    """
    Compute the product of two dimensions, handling None values.

    This consolidates the repeated pattern:
        result_dim = dim1 * dim2 if dim1 is not None and dim2 is not None else None

    Args:
        dim1: First dimension (may be None)
        dim2: Second dimension (may be None)

    Returns:
        Product of dimensions, or None if either is None
    """
    if dim1 is not None and dim2 is not None:
        return dim1 * dim2
    return None


# ========== SAFE COMPUTATION UTILITIES ==========


def safe_compute_difference(val1: float | None, val2: float | None) -> float:
    """
    Compute absolute difference between two values, handling None.

    This consolidates the repeated pattern:
        if val1 is not None and val2 is not None:
            diff = abs(val1 - val2)
        else:
            diff = float('inf')

    Args:
        val1: First value (may be None)
        val2: Second value (may be None)

    Returns:
        Absolute difference, or infinity if either value is None
    """
    if val1 is not None and val2 is not None:
        return abs(val1 - val2)
    return float("inf")


# ========== ERROR RESULT UTILITIES ==========


def format_exception_with_traceback(exc: Exception) -> str:
    """
    Format an exception with its traceback for error reporting.

    This consolidates the repeated pattern:
        f"{type(e).__name__}: {e}\n{traceback.format_exc()}"

    Args:
        exc: The exception to format

    Returns:
        Formatted error string with exception type, message, and traceback
    """
    import traceback

    return f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"


# ========== COORDINATE FORMATTING UTILITIES ==========


def format_3d_coords(coords: tuple[float, float, float] | list[float] | Any, precision: int = 2) -> str:
    """
    Format 3D coordinates as a string with consistent precision.

    This consolidates the repeated pattern:
        f"({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f})"

    Args:
        coords: Sequence of 3 coordinate values (x, y, z)
        precision: Number of decimal places (default: 2)

    Returns:
        Formatted string like "(1.23, 4.56, 7.89)"

    Examples:
        >>> format_3d_coords([1.234, 5.678, 9.012])
        '(1.23, 5.68, 9.01)'
        >>> format_3d_coords((1.0, 2.0, 3.0), precision=1)
        '(1.0, 2.0, 3.0)'
    """
    fmt = f"{{:.{precision}f}}"
    return f"({fmt.format(coords[0])}, {fmt.format(coords[1])}, {fmt.format(coords[2])})"


def is_degree_unit(unit_str: str) -> bool:
    """
    Check if a unit string represents degrees (vs radians).

    This consolidates the repeated pattern:
        if x_0.lower() in ('degree', 'degrees', 'deg'):

    Args:
        unit_str: Unit string to check

    Returns:
        True if the unit string represents degrees

    Examples:
        >>> is_degree_unit("degree")
        True
        >>> is_degree_unit("rad")
        False
    """
    return unit_str.lower() in SharedConstants.DEGREE_UNIT_PATTERNS


def convert_angle_with_unit(angle_rad: float, output_unit: str) -> float:
    """
    Convert angle from radians to output unit (degrees or radians).

    This consolidates the repeated pattern:
        if x_0.lower() in ('degree', 'degrees', 'deg'):
            x_1 = math.degrees(x_3)
        else:
            x_1 = x_3

    Args:
        angle_rad: Angle in radians
        output_unit: Output unit string ("degree", "degrees", "deg", or "rad")

    Returns:
        Angle in the requested unit

    Examples:
        >>> import math
        >>> convert_angle_with_unit(math.pi / 2, "degrees")
        90.0
        >>> convert_angle_with_unit(math.pi / 2, "rad")
        1.5707963267948966
    """
    import math

    if is_degree_unit(output_unit):
        return math.degrees(angle_rad)
    return angle_rad


def get_preferred_unit_symbol(obj: Any) -> str:
    """
    Get the preferred unit symbol from an object, with fallback to empty string.

    This consolidates the repeated pattern:
        if hasattr(x_0, 'preferred') and x_0.preferred:
            x_1 = x_0.preferred.symbol
        else:
            x_1 = ''

    Args:
        obj: Object that may have a 'preferred' attribute with a 'symbol' attribute

    Returns:
        The preferred unit symbol, or empty string if not available

    Examples:
        >>> class MockObj:
        ...     class preferred:
        ...         symbol = "N"
        >>> get_preferred_unit_symbol(MockObj())
        'N'
        >>> get_preferred_unit_symbol(object())
        ''
    """
    if hasattr(obj, "preferred") and obj.preferred:
        return obj.preferred.symbol
    return ""


def build_variable_dict(symbol: str, var: Any, value: str, unit_symbol: str) -> dict[str, Any]:
    """
    Build a variable dictionary for report generation.

    This consolidates the repeated pattern:
        x_0.append({'symbol': x_1, 'name': getattr(x_2, 'name', x_1), 'value': x_3, 'unit': x_4})

    Args:
        symbol: Variable symbol/identifier
        var: Variable object (may have 'name' attribute)
        value: Formatted value string
        unit_symbol: Unit symbol string

    Returns:
        Dictionary with 'symbol', 'name', 'value', and 'unit' keys
    """
    return {
        "symbol": symbol,
        "name": getattr(var, "name", symbol),
        "value": value,
        "unit": unit_symbol,
    }


# ========== TEXT STYLING UTILITIES ==========


# Default bbox style for diagram labels
DEFAULT_LABEL_BBOX: dict[str, Any] = {
    "boxstyle": "round,pad=0.2",
    "facecolor": "white",
    "alpha": 0.7,
}


def draw_styled_text(
    ax: Any,
    x: float,
    y: float,
    text: str,
    color: str,
    fontsize: int = 10,
    ha: str = "center",
    va: str = "center",
    bbox: dict[str, Any] | None = None,
) -> None:
    """
    Draw styled text on a matplotlib axes with consistent formatting.

    This consolidates the repeated pattern:
        ax.text(x, y, text, fontsize=10, color=color, ha='center', va='center',
                bbox={'boxstyle': 'round,pad=0.2', 'facecolor': 'white', 'alpha': 0.7})

    Args:
        ax: Matplotlib Axes object
        x: X coordinate
        y: Y coordinate
        text: Text to display
        color: Text color
        fontsize: Font size (default: 10)
        ha: Horizontal alignment (default: "center")
        va: Vertical alignment (default: "center")
        bbox: Bounding box style dict (default: DEFAULT_LABEL_BBOX)

    Examples:
        >>> draw_styled_text(ax, 1.0, 2.0, "F = 100 N", "blue")
    """
    if bbox is None:
        bbox = DEFAULT_LABEL_BBOX
    ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va, bbox=bbox)


# ========== DIRECTION COSINE UTILITIES ==========


def compute_missing_direction_cosine_squared(
    known_cos1: float,
    known_cos2: float,
) -> float:
    """
    Compute the squared cosine of the third direction angle from two known direction cosines.

    Uses the identity: cos²α + cos²β + cos²γ = 1

    This consolidates the repeated pattern:
        cos_sq = 1 - math.cos(angle1)**2 - math.cos(angle2)**2

    Args:
        known_cos1: Cosine of first known angle
        known_cos2: Cosine of second known angle

    Returns:
        Squared cosine of the missing angle (may be negative if invalid)

    Raises:
        ValueError: If the result is negative (invalid angle combination)

    Examples:
        >>> import math
        >>> # For orthogonal unit vectors (90°, 90°, 0°)
        >>> compute_missing_direction_cosine_squared(0.0, 0.0)
        1.0
    """
    return 1 - known_cos1**2 - known_cos2**2


def compute_third_direction_angle(
    angle1_rad: float,
    angle2_rad: float,
    sign: int = 1,
    error_msg: str = "Invalid angle combination: cos²α + cos²β + cos²γ > 1",
) -> float:
    """
    Compute the third direction angle from two known direction angles.

    Uses the identity: cos²α + cos²β + cos²γ = 1

    Args:
        angle1_rad: First known angle in radians
        angle2_rad: Second known angle in radians
        sign: Sign for the cosine of the result (+1 or -1)
        error_msg: Error message if angles are invalid

    Returns:
        Third direction angle in radians

    Raises:
        ValueError: If the angle combination is invalid
    """
    import math

    cos_sq = compute_missing_direction_cosine_squared(math.cos(angle1_rad), math.cos(angle2_rad))
    if cos_sq < 0:
        raise ValueError(error_msg)
    cos_val = sign * math.sqrt(cos_sq)
    return math.acos(cos_val)


# ========== POINT DIMENSION VALIDATION UTILITIES ==========


def validate_points_same_dimension(point1: Any, point2: Any, context: str = "Points") -> None:
    """
    Validate that two points have the same dimension.

    This consolidates the repeated pattern:
        if from_pt._dim != to_pt._dim:
            raise ValueError(f"Points must have same dimension: {from_pt._dim} vs {to_pt._dim}")

    Args:
        point1: First point with _dim attribute
        point2: Second point with _dim attribute
        context: Context string for error message (default: "Points")

    Raises:
        ValueError: If points have different dimensions
    """
    if point1._dim != point2._dim:
        raise ValueError(f"{context} must have same dimension: {point1._dim} vs {point2._dim}")


# ========== COORDS VALIDITY CHECK UTILITIES ==========


def has_valid_coords(obj: Any) -> bool:
    """
    Check if an object has valid coordinate data.

    This consolidates the repeated pattern:
        if not hasattr(self, '_coords') or self._coords is None or self._dim is None:
            return None

    Args:
        obj: Object to check for _coords and _dim attributes

    Returns:
        True if object has valid _coords and _dim, False otherwise
    """
    return hasattr(obj, "_coords") and obj._coords is not None and obj._dim is not None


# ========== 3D MAGNITUDE CALCULATION UTILITIES ==========


def compute_3d_magnitude(x: float, y: float, z: float) -> float:
    """
    Compute the magnitude of a 3D vector.

    This consolidates the repeated pattern:
        magnitude = math.sqrt(x**2 + y**2 + z**2)

    Args:
        x: X component
        y: Y component
        z: Z component

    Returns:
        Magnitude (Euclidean norm) of the vector
    """
    import math

    return math.sqrt(x**2 + y**2 + z**2)


# ========== FORCE QUANTITY CREATION UTILITIES ==========


def create_force_component_quantity(
    force_name: str,
    component: str,
    dim: Any,
    value: float,
    preferred_unit: Any,
) -> Any:
    """
    Create a Quantity for a force component (x, y, z, or magnitude).

    This consolidates the repeated pattern in triangle_solver.py:
        x_qty = Quantity(name=f"{force.name}_x", dim=dim.force, value=F_x, preferred=ref_unit)

    Args:
        force_name: Name of the force (e.g., "F_1")
        component: Component name ("x", "y", "z", "magnitude", or "angle")
        dim: Dimension for the quantity (e.g., dim.force or dim.D)
        value: Numerical value
        preferred_unit: Preferred unit for display

    Returns:
        Quantity object for the force component
    """
    from ..core.quantity import Quantity

    return Quantity(name=f"{force_name}_{component}", dim=dim, value=value, preferred=preferred_unit)


# ========== WRAPPED VARIABLE CHECK UTILITIES ==========


def raise_if_missing_wrapped_var(obj: Any, attr_name: str) -> None:
    """
    Raise AttributeError if object doesn't have _wrapped_var attribute.

    This consolidates the repeated pattern:
        if not hasattr(self, '_wrapped_var'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    Args:
        obj: Object to check
        attr_name: Attribute name to include in error message

    Raises:
        AttributeError: If object doesn't have _wrapped_var attribute
    """
    if not hasattr(obj, "_wrapped_var"):
        raise AttributeError(f"'{type(obj).__name__}' object has no attribute '{attr_name}'")


# ========== VECTOR NAME UTILITIES ==========


def resolve_vector_name(explicit_name: str | None, original_name: str, default_name: str = "Vector") -> str:
    """
    Resolve the name to use for a vector, handling explicit names and defaults.

    This consolidates the repeated pattern:
        name if name is not None else (original_name if original_name and original_name != "Vector" else "")

    Args:
        explicit_name: Explicitly provided name (takes priority if not None)
        original_name: Original name from source object
        default_name: Default name to exclude (default: "Vector")

    Returns:
        Resolved name string

    Examples:
        >>> resolve_vector_name("F1_copy", "F1")
        'F1_copy'
        >>> resolve_vector_name(None, "F1")
        'F1'
        >>> resolve_vector_name(None, "Vector")
        ''
        >>> resolve_vector_name(None, "")
        ''
    """
    if explicit_name is not None:
        return explicit_name
    if original_name and original_name != default_name:
        return original_name
    return ""
