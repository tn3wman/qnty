"""
Shared geometry utilities for angle and vector operations.

This module provides common geometric functions used across the codebase,
particularly for angle normalization and interior angle calculations in
vector equilibrium problems.
"""

from __future__ import annotations

import math

# =============================================================================
# Axis Reference Constants
# =============================================================================

AXIS_POS_X = "+x"
AXIS_NEG_X = "-x"
AXIS_POS_Y = "+y"
AXIS_NEG_Y = "-y"
AXIS_X = "x"
AXIS_Y = "y"

# Default units
DEFAULT_FORCE_UNIT_SYMBOL = "N"
DEFAULT_ANGLE_UNIT = "degree"


# =============================================================================
# Angle Normalization Functions
# =============================================================================


def normalize_angle_positive(angle: float) -> float:
    """
    Normalize angle to [0, 2*pi) range.

    Args:
        angle: Angle in radians

    Returns:
        Angle normalized to [0, 2*pi) range

    Examples:
        >>> normalize_angle_positive(-math.pi/2)  # -90 degrees
        4.71238898038469  # 270 degrees
        >>> normalize_angle_positive(3 * math.pi)  # 540 degrees
        3.141592653589793  # 180 degrees
    """
    return angle % (2 * math.pi)


def normalize_angle_symmetric(angle: float) -> float:
    """
    Normalize angle to [-pi, pi) range.

    Args:
        angle: Angle in radians

    Returns:
        Angle normalized to [-pi, pi) range

    Examples:
        >>> normalize_angle_symmetric(3 * math.pi / 2)  # 270 degrees
        -1.5707963267948966  # -90 degrees
    """
    angle = angle % (2 * math.pi)
    if angle >= math.pi:
        angle -= 2 * math.pi
    return angle


def interior_angle(angle1: float, angle2: float) -> float:
    """
    Compute interior angle between two directions.

    The interior angle is always in the range [0, pi], representing
    the smallest angle between two directions.

    Args:
        angle1: First angle in radians
        angle2: Second angle in radians

    Returns:
        Interior angle in radians, always in [0, pi]

    Examples:
        >>> interior_angle(0, math.pi/2)  # 0 and 90 degrees
        1.5707963267948966  # 90 degrees
        >>> interior_angle(0, 3*math.pi/2)  # 0 and 270 degrees
        1.5707963267948966  # 90 degrees (interior angle)
    """
    gamma = abs(angle2 - angle1)
    if gamma > math.pi:
        gamma = 2 * math.pi - gamma
    return gamma


# =============================================================================
# Axis Reference Utilities
# =============================================================================


def format_axis_ref(wrt: str) -> str:
    """
    Format axis reference for angle notation.

    Removes leading '+' sign for positive axis references.

    Args:
        wrt: Axis reference string (e.g., '+x', '-x', 'x')

    Returns:
        Formatted axis reference (e.g., 'x', '-x')

    Examples:
        >>> format_axis_ref('+x')
        'x'
        >>> format_axis_ref('-x')
        '-x'
        >>> format_axis_ref('x')
        'x'
    """
    if wrt.startswith('+'):
        return wrt[1:]
    return wrt


def get_axis_info(wrt: str) -> tuple[str, int]:
    """
    Get axis type and sign for a reference axis.

    Args:
        wrt: Axis reference string (e.g., '+x', '-x', 'y')

    Returns:
        Tuple of (axis_type, sign) where axis_type is 'x' or 'y'
        and sign is 1 for positive, -1 for negative

    Examples:
        >>> get_axis_info('+x')
        ('x', 1)
        >>> get_axis_info('-y')
        ('y', -1)
    """
    axis_map = {
        AXIS_POS_X: (AXIS_X, 1),
        AXIS_X: (AXIS_X, 1),
        AXIS_NEG_X: (AXIS_X, -1),
        AXIS_POS_Y: (AXIS_Y, 1),
        AXIS_Y: (AXIS_Y, 1),
        AXIS_NEG_Y: (AXIS_Y, -1),
    }
    return axis_map.get(wrt, (AXIS_X, 1))


def parse_axis_reference(wrt: str) -> tuple[str, bool]:
    """
    Parse axis reference into axis name and positivity.

    Args:
        wrt: Axis reference string

    Returns:
        Tuple of (axis_name, is_positive)

    Examples:
        >>> parse_axis_reference('+x')
        ('x', True)
        >>> parse_axis_reference('-y')
        ('y', False)
    """
    axis_type, sign = get_axis_info(wrt)
    return axis_type, sign > 0


# =============================================================================
# Angle Calculation Helpers
# =============================================================================


def angle_from_components(x: float, y: float) -> float:
    """
    Calculate angle from x and y components using atan2.

    Args:
        x: X component
        y: Y component

    Returns:
        Angle in radians in range [0, 2*pi)
    """
    angle = math.atan2(y, x)
    return normalize_angle_positive(angle)


def magnitude_from_components(x: float, y: float, z: float = 0.0) -> float:
    """
    Calculate magnitude from components.

    Args:
        x: X component
        y: Y component
        z: Z component (default 0)

    Returns:
        Magnitude (always non-negative)
    """
    return math.sqrt(x * x + y * y + z * z)


def components_from_polar(magnitude: float, angle: float) -> tuple[float, float]:
    """
    Convert polar coordinates to Cartesian components.

    Args:
        magnitude: Magnitude (can be negative for opposite direction)
        angle: Angle in radians from positive x-axis

    Returns:
        Tuple of (x, y) components
    """
    return magnitude * math.cos(angle), magnitude * math.sin(angle)
