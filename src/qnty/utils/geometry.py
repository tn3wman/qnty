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


# =============================================================================
# Triangle Angle Display Helpers
# =============================================================================


def compute_angle_between_display(
    theta1_std_deg: float,
    theta2_std_deg: float,
    theta1_input_deg: float,
    theta2_input_deg: float,
    wrt1: str,
    wrt2: str,
    vec1_name: str,
    vec2_name: str,
    result_deg: float,
    coordinate_system=None,
) -> str:
    """
    Generate a human-readable display string showing how an interior angle
    between two vectors was calculated from their given angle specifications.

    This function intelligently determines the simplest geometric explanation
    for the angle calculation based on the reference axes used.

    Args:
        theta1_std_deg: First vector's angle in degrees from +x (standard form)
        theta2_std_deg: Second vector's angle in degrees from +x (standard form)
        theta1_input_deg: First vector's angle as originally specified
        theta2_input_deg: Second vector's angle as originally specified
        wrt1: Reference axis for first vector (e.g., '+x', '-y')
        wrt2: Reference axis for second vector
        vec1_name: Display name for first vector (LaTeX formatted)
        vec2_name: Display name for second vector (LaTeX formatted)
        result_deg: The resulting interior angle in degrees
        coordinate_system: Optional coordinate system object with axis angles

    Returns:
        A formatted string showing the calculation steps
    """
    # Normalize standard angles to [0, 360)
    theta1_std_deg = theta1_std_deg % 360
    theta2_std_deg = theta2_std_deg % 360

    # Compute the raw difference and interior angle
    diff = abs(theta2_std_deg - theta1_std_deg)
    if diff > 180:
        diff = 360 - diff

    # Define standard axes for detecting custom coordinate systems
    standard_axes = {"+x", "-x", "+y", "-y", "x", "y"}
    is_custom_coord_sys = wrt1.lower() not in standard_axes or wrt2.lower() not in standard_axes

    # Case 1: Both vectors use the same reference axis
    if wrt1 == wrt2:
        # Simple difference of angles from the same reference
        axis_label = format_axis_ref(wrt1)
        return (
            f"∠({vec1_name},{vec2_name}) = |∠({axis_label},{vec1_name}) - ∠({axis_label},{vec2_name})|\n"
            f"= |{theta1_input_deg:.0f}° - {theta2_input_deg:.0f}°|\n"
            f"= {result_deg:.0f}°"
        )

    # Case 2: Custom coordinate system - show using standard angles from +x
    # The result_deg is the interior angle of the force triangle, which is 180° - gamma
    # where gamma is the angle between the vectors
    if is_custom_coord_sys:
        import math
        axis1_label = format_axis_ref(wrt1)
        axis2_label = format_axis_ref(wrt2)

        # Calculate gamma (angle between vectors)
        raw_diff = abs(theta1_std_deg - theta2_std_deg)
        gamma = raw_diff if raw_diff <= 180 else 360 - raw_diff

        # If we have coordinate system info, check for special case where both vectors
        # have the same angle relative to their respective axes
        if coordinate_system is not None and hasattr(coordinate_system, 'axis1_angle') and hasattr(coordinate_system, 'axis2_angle'):
            axis_angle_deg = abs(math.degrees(coordinate_system.axis2_angle - coordinate_system.axis1_angle))

            # Special case: both input angles are equal, so angle between vectors = angle between axes
            # Show directly as 180° - axis_angle to get the interior angle
            if abs(theta1_input_deg - theta2_input_deg) < 0.5 and abs(axis_angle_deg - gamma) < 0.5:
                return (
                    f"∠({vec1_name},{vec2_name}) = 180° - ∠({axis1_label},{axis2_label})\n"
                    f"= 180° - {axis_angle_deg:.0f}°\n"
                    f"= {result_deg:.0f}°"
                )

        # General case: show using standard angles from +x
        return (
            f"∠({vec1_name},{vec2_name}) = 180° - |{theta1_std_deg:.0f}° - ({theta2_std_deg:.0f}°)|\n"
            f"= 180° - {gamma:.0f}°\n"
            f"= {result_deg:.0f}°"
        )

    # Case 3: Both vectors reference standard axes - need to find the relationship
    axis1_type, _ = get_axis_info(wrt1)
    axis2_type, _ = get_axis_info(wrt2)

    axis1_label = format_axis_ref(wrt1)
    axis2_label = format_axis_ref(wrt2)

    # If axes are of the same type (both x or both y), show as difference
    if axis1_type == axis2_type:
        return (
            f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name}) - ∠({axis2_label},{vec2_name})|\n"
            f"= |{theta1_input_deg:.0f}° - {theta2_input_deg:.0f}°|\n"
            f"= {result_deg:.0f}°"
        )

    # Axes are orthogonal (one is x-type, one is y-type)
    # Determine the geometric relationship between the angles

    # Get the axis angles in standard form
    axis_angles = {"+x": 0, "+y": 90, "-x": 180, "-y": 270}
    axis1_std = axis_angles.get(wrt1.lower(), 0)
    axis2_std = axis_angles.get(wrt2.lower(), 0)

    # Calculate the angle between the two reference axes
    axis_diff = abs(axis2_std - axis1_std)
    if axis_diff > 180:
        axis_diff = 360 - axis_diff

    # Determine how to express the calculation most naturally
    # Use absolute values of input angles for clarity
    abs_theta1 = abs(theta1_input_deg)
    abs_theta2 = abs(theta2_input_deg)

    # Check if adding the absolute angles gives the result (common case)
    if abs(abs_theta1 + abs_theta2 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name})| + |∠({axis2_label},{vec2_name})|\n"
            f"= |{theta1_input_deg:.0f}°| + |{theta2_input_deg:.0f}°|\n"
            f"= {abs_theta1:.0f}° + {abs_theta2:.0f}°\n"
            f"= {result_deg:.0f}°"
        )

    # Check if subtracting gives the result
    if abs(abs(abs_theta1 - abs_theta2) - result_deg) < 0.5:
        if abs_theta1 >= abs_theta2:
            return (
                f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name})| - |∠({axis2_label},{vec2_name})|\n"
                f"= |{theta1_input_deg:.0f}°| - |{theta2_input_deg:.0f}°|\n"
                f"= {abs_theta1:.0f}° - {abs_theta2:.0f}°\n"
                f"= {result_deg:.0f}°"
            )
        else:
            return (
                f"∠({vec1_name},{vec2_name}) = |∠({axis2_label},{vec2_name})| - |∠({axis1_label},{vec1_name})|\n"
                f"= |{theta2_input_deg:.0f}°| - |{theta1_input_deg:.0f}°|\n"
                f"= {abs_theta2:.0f}° - {abs_theta1:.0f}°\n"
                f"= {result_deg:.0f}°"
            )

    # Check if 90 - angle relationship applies
    if abs(90 - abs_theta1 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = 90° - |∠({axis1_label},{vec1_name})|\n"
            f"= 90° - |{theta1_input_deg:.0f}°|\n"
            f"= {result_deg:.0f}°"
        )

    if abs(90 - abs_theta2 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = 90° - |∠({axis2_label},{vec2_name})|\n"
            f"= 90° - |{theta2_input_deg:.0f}°|\n"
            f"= {result_deg:.0f}°"
        )

    # Fallback: show using standard angles from +x
    return (
        f"∠({vec1_name},{vec2_name}) = |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
        f"= {result_deg:.0f}°"
    )
