"""
Arithmetic Mixins for Eliminating Code Duplication.

This module provides mixin classes that eliminate the repeated arithmetic
method implementations across different classes in the qnty library.
"""

from abc import ABC, abstractmethod
from typing import Any


class ArithmeticDelegationMixin:
    """
    Mixin for classes that need to delegate arithmetic operations to another object.
    
    This eliminates duplication in proxy/wrapper classes that delegate all
    arithmetic operations to an underlying object.
    
    Usage:
        class MyProxy(ArithmeticDelegationMixin):
            def __init__(self, target):
                self._target = target
            
            def _get_arithmetic_delegate(self):
                return self._target
    """
    
    @abstractmethod
    def _get_arithmetic_delegate(self) -> Any:
        """Get the object to delegate arithmetic operations to."""
        pass
    
    def __add__(self, other: Any) -> Any:
        """Delegate addition to the target object."""
        return self._get_arithmetic_delegate().__add__(other)

    def __radd__(self, other: Any) -> Any:
        """Delegate reverse addition to the target object."""
        return self._get_arithmetic_delegate().__radd__(other)

    def __sub__(self, other: Any) -> Any:
        """Delegate subtraction to the target object."""
        return self._get_arithmetic_delegate().__sub__(other)

    def __rsub__(self, other: Any) -> Any:
        """Delegate reverse subtraction to the target object."""
        return self._get_arithmetic_delegate().__rsub__(other)

    def __mul__(self, other: Any) -> Any:
        """Delegate multiplication to the target object."""
        return self._get_arithmetic_delegate().__mul__(other)

    def __rmul__(self, other: Any) -> Any:
        """Delegate reverse multiplication to the target object."""
        return self._get_arithmetic_delegate().__rmul__(other)

    def __truediv__(self, other: Any) -> Any:
        """Delegate division to the target object."""
        return self._get_arithmetic_delegate().__truediv__(other)

    def __rtruediv__(self, other: Any) -> Any:
        """Delegate reverse division to the target object."""
        return self._get_arithmetic_delegate().__rtruediv__(other)

    def __pow__(self, other: Any) -> Any:
        """Delegate power operation to the target object."""
        return self._get_arithmetic_delegate().__pow__(other)

    def __neg__(self) -> Any:
        """Delegate negation to the target object."""
        # Default implementation as multiplication by -1, can be overridden
        return self._get_arithmetic_delegate() * (-1)


class ComparisonDelegationMixin:
    """
    Mixin for classes that need to delegate comparison operations to another object.
    
    This eliminates duplication in proxy/wrapper classes that delegate all
    comparison operations to an underlying object.
    """
    
    @abstractmethod
    def _get_comparison_delegate(self) -> Any:
        """Get the object to delegate comparison operations to."""
        pass
    
    def __lt__(self, other: Any) -> Any:
        """Delegate less than comparison to the target object."""
        return self._get_comparison_delegate().__lt__(other)

    def __le__(self, other: Any) -> Any:
        """Delegate less than or equal comparison to the target object."""
        return self._get_comparison_delegate().__le__(other)

    def __gt__(self, other: Any) -> Any:
        """Delegate greater than comparison to the target object."""
        return self._get_comparison_delegate().__gt__(other)

    def __ge__(self, other: Any) -> Any:
        """Delegate greater than or equal comparison to the target object."""
        return self._get_comparison_delegate().__ge__(other)

    def __eq__(self, other: Any) -> Any:
        """Delegate equality comparison to the target object."""
        return self._get_comparison_delegate().__eq__(other)

    def __ne__(self, other: Any) -> Any:
        """Delegate not equal comparison to the target object."""
        return self._get_comparison_delegate().__ne__(other)


class DelayedArithmeticMixin:
    """
    Mixin for classes that need to create delayed/lazy arithmetic expressions.
    
    This eliminates duplication in classes that build expression trees instead
    of immediately evaluating arithmetic operations.
    
    Usage:
        class DelayedProxy(DelayedArithmeticMixin):
            def _create_delayed_expression(self, operator, left, right):
                return DelayedExpression(operator, left, right)
    """
    
    @abstractmethod
    def _create_delayed_expression(self, operator: str, left: Any, right: Any) -> Any:
        """Create a delayed expression for the given operator and operands."""
        pass
    
    def __add__(self, other: Any) -> Any:
        """Create delayed addition expression."""
        return self._create_delayed_expression("+", self, other)

    def __radd__(self, other: Any) -> Any:
        """Create delayed reverse addition expression."""
        return self._create_delayed_expression("+", other, self)

    def __sub__(self, other: Any) -> Any:
        """Create delayed subtraction expression."""
        return self._create_delayed_expression("-", self, other)

    def __rsub__(self, other: Any) -> Any:
        """Create delayed reverse subtraction expression."""
        return self._create_delayed_expression("-", other, self)

    def __mul__(self, other: Any) -> Any:
        """Create delayed multiplication expression."""
        return self._create_delayed_expression("*", self, other)

    def __rmul__(self, other: Any) -> Any:
        """Create delayed reverse multiplication expression."""
        return self._create_delayed_expression("*", other, self)

    def __truediv__(self, other: Any) -> Any:
        """Create delayed division expression."""
        return self._create_delayed_expression("/", self, other)

    def __rtruediv__(self, other: Any) -> Any:
        """Create delayed reverse division expression."""
        return self._create_delayed_expression("/", other, self)


class ArithmeticMixin(ArithmeticDelegationMixin, ComparisonDelegationMixin):
    """
    Combined mixin that provides both arithmetic and comparison delegation.
    
    This is a convenience class for objects that need to delegate both
    arithmetic and comparison operations to the same target.
    """
    
    def _get_comparison_delegate(self) -> Any:
        """Default to using the same delegate for comparison operations."""
        return self._get_arithmetic_delegate()


class FastPathArithmeticMixin:
    """
    Mixin that provides optimized arithmetic operations with fast paths.
    
    This eliminates duplication of common optimization patterns like:
    - Multiplication/division by 1
    - Addition/subtraction with 0
    - Multiplication by 0
    """
    
    def _optimized_add(self, left: Any, right: Any) -> Any:
        """Optimized addition with fast paths."""
        # Fast path for addition with 0
        if hasattr(right, 'value') and right.value == 0.0:
            return left
        elif hasattr(left, 'value') and left.value == 0.0:
            return right
        # Fallback to normal addition
        return self._perform_add(left, right)
    
    def _optimized_mul(self, left: Any, right: Any) -> Any:
        """Optimized multiplication with fast paths."""
        # Fast path for multiplication by 1
        if hasattr(right, 'value') and right.value == 1.0:
            return left
        elif hasattr(left, 'value') and left.value == 1.0:
            return right
        # Fast path for multiplication by 0
        elif hasattr(right, 'value') and right.value == 0.0:
            return self._create_zero_result(left)
        elif hasattr(left, 'value') and left.value == 0.0:
            return self._create_zero_result(right)
        # Fallback to normal multiplication
        return self._perform_mul(left, right)
    
    def _optimized_div(self, left: Any, right: Any) -> Any:
        """Optimized division with fast paths and zero checking."""
        # Check for division by zero
        if hasattr(right, 'value') and abs(right.value) < 1e-15:
            raise ValueError(f"Division by zero: {left} / {right}")
        # Fast path for division by 1
        if hasattr(right, 'value') and right.value == 1.0:
            return left
        # Fallback to normal division
        return self._perform_div(left, right)
    
    def _optimized_sub(self, left: Any, right: Any) -> Any:
        """Optimized subtraction with fast paths."""
        # Fast path for subtraction with 0
        if hasattr(right, 'value') and right.value == 0.0:
            return left
        # Fallback to normal subtraction
        return self._perform_sub(left, right)
    
    # Abstract methods that subclasses must implement for actual operations
    @abstractmethod
    def _perform_add(self, left: Any, right: Any) -> Any:
        """Perform the actual addition operation."""
        pass
    
    @abstractmethod
    def _perform_mul(self, left: Any, right: Any) -> Any:
        """Perform the actual multiplication operation.""" 
        pass
    
    @abstractmethod
    def _perform_div(self, left: Any, right: Any) -> Any:
        """Perform the actual division operation."""
        pass
    
    @abstractmethod
    def _perform_sub(self, left: Any, right: Any) -> Any:
        """Perform the actual subtraction operation."""
        pass
    
    @abstractmethod
    def _create_zero_result(self, template: Any) -> Any:
        """Create a zero result with appropriate type/unit based on template."""
        pass


def create_arithmetic_delegation_methods(delegate_attribute: str) -> dict[str, Any]:
    """
    Factory function to create arithmetic delegation methods.
    
    This is useful for dynamically adding arithmetic delegation to classes
    without inheritance, or when you need to specify a different attribute name.
    
    Args:
        delegate_attribute: Name of the attribute to delegate operations to
        
    Returns:
        Dictionary of method name -> method implementation
        
    Example:
        methods = create_arithmetic_delegation_methods('_wrapped_var')
        for name, method in methods.items():
            setattr(MyClass, name, method)
    """
    def make_delegation_method(op_name: str):
        def delegation_method(self, other=None):
            delegate = getattr(self, delegate_attribute)
            if other is None:
                # Unary operation
                return getattr(delegate, op_name)()
            else:
                # Binary operation  
                return getattr(delegate, op_name)(other)
        return delegation_method
    
    def make_reverse_delegation_method(op_name: str):
        def reverse_delegation_method(self, other):
            delegate = getattr(self, delegate_attribute)
            return getattr(delegate, op_name)(other)
        return reverse_delegation_method
    
    operations = {
        "__add__": make_delegation_method("__add__"),
        "__radd__": make_reverse_delegation_method("__radd__"),
        "__sub__": make_delegation_method("__sub__"), 
        "__rsub__": make_reverse_delegation_method("__rsub__"),
        "__mul__": make_delegation_method("__mul__"),
        "__rmul__": make_reverse_delegation_method("__rmul__"),
        "__truediv__": make_delegation_method("__truediv__"),
        "__rtruediv__": make_reverse_delegation_method("__rtruediv__"),
        "__pow__": make_delegation_method("__pow__"),
        "__neg__": make_delegation_method("__neg__"),
    }
    
    return operations