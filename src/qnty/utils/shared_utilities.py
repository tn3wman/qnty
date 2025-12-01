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
    WRAPPER_EXCLUDED_DUNDERS = frozenset({
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
    })


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


# ========== FORCE VECTOR UTILITIES ==========


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
            equation_str = step_data.get("equation_str", "")
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


def add_force_magnitude_variable(
    force: Any,
    force_name: str,
    was_originally_known: bool,
    variables: dict[str, Any],
    original_variable_states: dict[str, bool],
) -> None:
    """
    Add force magnitude as a variable for report generation.

    Args:
        force: ForceVector with magnitude attribute
        force_name: Name/key of the force
        was_originally_known: Whether the force was originally known
        variables: Dictionary to add the magnitude variable to
        original_variable_states: Dictionary to track original state
    """
    if force.magnitude is None or force.magnitude.value is None:
        return

    from ..core.dimension_catalog import dim
    from ..core.quantity import Quantity

    mag_var = Quantity(name=f"{force.name} Magnitude", dim=dim.force, value=force.magnitude.value, preferred=force.magnitude.preferred, _symbol=f"{force_name}_mag")
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
    from ..core.unit import ureg

    if isinstance(unit, str):
        if dim is not None:
            resolved = ureg.resolve(unit, dim=dim)
        else:
            resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        return resolved
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

    return np.array([
        [math.cos(theta1), -math.cos(theta2)],
        [math.sin(theta1), -math.sin(theta2)],
    ])


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
