"""Shared utilities and helper functions."""

from .scope_discovery import ScopeDiscoveryService, discover_variables_from_scope
from .protocols import TypeRegistry, ExpressionProtocol, VariableProtocol, register_expression_type, register_variable_type, is_expression, is_variable

__all__ = [
    "ScopeDiscoveryService",
    "discover_variables_from_scope",
    "TypeRegistry",
    "ExpressionProtocol",
    "VariableProtocol",
    "register_expression_type",
    "register_variable_type",
    "is_expression",
    "is_variable",
]
