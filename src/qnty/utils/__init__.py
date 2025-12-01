"""Shared utilities and helper functions."""

from .geometry import (
    AXIS_NEG_X,
    AXIS_NEG_Y,
    AXIS_POS_X,
    AXIS_POS_Y,
    AXIS_X,
    AXIS_Y,
    DEFAULT_ANGLE_UNIT,
    DEFAULT_FORCE_UNIT_SYMBOL,
    angle_from_components,
    components_from_polar,
    format_axis_ref,
    get_axis_info,
    interior_angle,
    magnitude_from_components,
    normalize_angle_positive,
    normalize_angle_symmetric,
    parse_axis_reference,
)
from .protocols import ExpressionProtocol, TypeRegistry, VariableProtocol, is_expression, is_variable, register_expression_type, register_variable_type
from .scope_discovery import ScopeDiscoveryService, discover_variables_from_scope
from .shared_utilities import SharedConstants, delegate_getattr, is_excluded_dunder, is_private_or_excluded_dunder, raise_if_excluded_dunder

__all__ = [
    # Geometry utilities
    "AXIS_NEG_X",
    "AXIS_NEG_Y",
    "AXIS_POS_X",
    "AXIS_POS_Y",
    "AXIS_X",
    "AXIS_Y",
    "DEFAULT_ANGLE_UNIT",
    "DEFAULT_FORCE_UNIT_SYMBOL",
    "angle_from_components",
    "components_from_polar",
    "format_axis_ref",
    "get_axis_info",
    "interior_angle",
    "magnitude_from_components",
    "normalize_angle_positive",
    "normalize_angle_symmetric",
    "parse_axis_reference",
    # Scope discovery
    "ScopeDiscoveryService",
    "discover_variables_from_scope",
    # Type protocols
    "TypeRegistry",
    "ExpressionProtocol",
    "VariableProtocol",
    "register_expression_type",
    "register_variable_type",
    "is_expression",
    "is_variable",
    # Shared utilities
    "SharedConstants",
    "delegate_getattr",
    "is_excluded_dunder",
    "is_private_or_excluded_dunder",
    "raise_if_excluded_dunder",
]
