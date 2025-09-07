"""
Expression Type Definitions
===========================

Type definitions and protocols to avoid circular imports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any


class ExpressionProtocol(Protocol):
    """Protocol for expression objects."""

    def evaluate(self, variables: dict[str, Any]) -> Any:
        """Evaluate the expression with given variables."""
        ...


class BinaryOperationProtocol(Protocol):
    """Protocol for binary operation objects."""

    left: ExpressionProtocol
    right: ExpressionProtocol
    operator: str

    def evaluate(self, variables: dict[str, Any]) -> Any:
        """Evaluate the binary operation."""
        ...

    def _can_auto_evaluate(self) -> tuple[bool, dict[str, Any] | None]:
        """Check if auto-evaluation is possible."""
        ...


class UnaryFunctionProtocol(Protocol):
    """Protocol for unary function objects."""

    function_name: str
    operand: ExpressionProtocol


class ConditionalExpressionProtocol(Protocol):
    """Protocol for conditional expression objects."""

    condition: ExpressionProtocol
    true_expr: ExpressionProtocol
    false_expr: ExpressionProtocol
