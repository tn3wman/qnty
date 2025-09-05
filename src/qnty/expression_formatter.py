"""
Expression String Formatting System
===================================

Centralized formatting logic for mathematical expressions with proper
operator precedence handling and readable output generation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from .expressions.nodes import Expression, BinaryOperation, UnaryFunction, ConditionalExpression


class ExpressionFormatter:
    """
    Handles string representation of expressions with proper precedence rules.
    
    Centralizes complex formatting logic that was previously scattered across
    expression classes, making it easier to maintain and extend.
    """
    
    # Operator precedence levels (higher number = higher precedence)
    OPERATOR_PRECEDENCE = {
        # Comparison operators (lowest precedence)
        '<': 0, '<=': 0, '>': 0, '>=': 0, '==': 0, '!=': 0,
        # Arithmetic operators
        '+': 1, '-': 1,      # Addition/subtraction  
        '*': 2, '/': 2,      # Multiplication/division
        '**': 3,             # Exponentiation (highest precedence)
    }
    
    # Right-associative operators (most are left-associative by default)
    RIGHT_ASSOCIATIVE = {'**'}
    
    # Left-associative operators that need special parenthesization
    LEFT_ASSOCIATIVE_SPECIAL = {'-', '/'}
    
    @staticmethod
    def format_binary_operation(
        binary_op: BinaryOperation,
        can_auto_evaluate: bool = False,
        auto_eval_variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format binary operation with proper parenthesization.
        
        Args:
            binary_op: The binary operation to format
            can_auto_evaluate: Whether auto-evaluation should be attempted
            auto_eval_variables: Variables for auto-evaluation
            
        Returns:
            Formatted string representation
        """
        # Try auto-evaluation first if requested
        if can_auto_evaluate and auto_eval_variables:
            try:
                result = binary_op.evaluate(auto_eval_variables)
                return str(result)
            except Exception:
                pass  # Fall back to symbolic representation
        
        # Get string representations of operands
        left_str = str(binary_op.left)
        right_str = str(binary_op.right)
        
        # Apply parenthesization rules
        left_str = ExpressionFormatter._maybe_parenthesize_left(
            binary_op.left, binary_op.operator, left_str
        )
        right_str = ExpressionFormatter._maybe_parenthesize_right(
            binary_op.right, binary_op.operator, right_str
        )
        
        return f"{left_str} {binary_op.operator} {right_str}"
    
    @staticmethod
    def _maybe_parenthesize_left(left_expr: Expression, operator: str, left_str: str) -> str:
        """Add parentheses to left operand if needed for precedence."""
        from .expressions.nodes import BinaryOperation
        
        if not isinstance(left_expr, BinaryOperation):
            return left_str
            
        left_precedence = ExpressionFormatter.OPERATOR_PRECEDENCE.get(left_expr.operator, 0)
        current_precedence = ExpressionFormatter.OPERATOR_PRECEDENCE.get(operator, 0)
        
        # Left side needs parentheses only if its precedence is strictly lower
        if left_precedence < current_precedence:
            return f"({left_str})"
            
        return left_str
    
    @staticmethod
    def _maybe_parenthesize_right(right_expr: Expression, operator: str, right_str: str) -> str:
        """Add parentheses to right operand if needed for precedence and associativity."""
        from .expressions.nodes import BinaryOperation
        
        if not isinstance(right_expr, BinaryOperation):
            return right_str
            
        right_precedence = ExpressionFormatter.OPERATOR_PRECEDENCE.get(right_expr.operator, 0)
        current_precedence = ExpressionFormatter.OPERATOR_PRECEDENCE.get(operator, 0)
        
        # Right side needs parentheses if:
        # 1. Its precedence is strictly lower, OR
        # 2. Same precedence AND current operator is left-associative (-, /)
        needs_parentheses = (
            right_precedence < current_precedence or
            (right_precedence == current_precedence and operator in ExpressionFormatter.LEFT_ASSOCIATIVE_SPECIAL)
        )
        
        if needs_parentheses:
            return f"({right_str})"
            
        return right_str
    
    @staticmethod
    def format_unary_function(func: UnaryFunction) -> str:
        """Format unary function call."""
        return f"{func.function_name}({func.operand})"
    
    @staticmethod
    def format_conditional_expression(cond_expr: ConditionalExpression) -> str:
        """Format conditional expression in if-then-else form."""
        return f"if({cond_expr.condition}, {cond_expr.true_expr}, {cond_expr.false_expr})"
    
    @staticmethod
    def format_variable_reference(var_ref) -> str:
        """Format variable reference (just the name)."""
        return var_ref.name
    
    @staticmethod
    def format_constant(constant) -> str:
        """Format constant value."""
        return str(constant.value.value)
    
    @staticmethod
    def is_operator_right_associative(operator: str) -> bool:
        """Check if operator is right-associative."""
        return operator in ExpressionFormatter.RIGHT_ASSOCIATIVE
    
    @staticmethod
    def get_operator_precedence(operator: str) -> int:
        """Get precedence level for operator."""
        return ExpressionFormatter.OPERATOR_PRECEDENCE.get(operator, 0)
    
    @staticmethod
    def format_expression_with_auto_eval(expr: Expression) -> str:
        """
        Format expression, attempting auto-evaluation if possible.
        
        This is a convenience method that handles the common pattern of
        trying to auto-evaluate before falling back to symbolic representation.
        """
        # Check if auto-evaluation is possible
        from .expressions.nodes import BinaryOperation
        
        if isinstance(expr, BinaryOperation):
            # Try to discover variables from scope for auto-evaluation
            can_eval, variables = expr._can_auto_evaluate()
            return ExpressionFormatter.format_binary_operation(
                expr, can_auto_evaluate=can_eval, auto_eval_variables=variables
            )
        else:
            # For other expression types, just use their standard string representation
            return str(expr)


class ExpressionStyle:
    """
    Style preferences for expression formatting.
    
    Future extension point for customizable formatting styles
    (e.g., mathematical notation vs programming notation).
    """
    
    # Style options
    USE_UNICODE_OPERATORS = False  # Future: use × instead of *, ÷ instead of /
    COMPACT_PARENTHESES = False    # Future: minimize parentheses usage
    SHOW_MULTIPLICATION_EXPLICITLY = True  # Future: show * or use implicit multiplication
    
    @classmethod
    def apply_style_preferences(cls, formatted_expr: str) -> str:
        """Apply style preferences to formatted expression."""
        # Future extension point for style transformations
        return formatted_expr