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

    # Case 2: Custom coordinate system - show using axis relationships
    # Use the coordinate system's axis angles to provide meaningful geometric explanations
    if is_custom_coord_sys:
        import math
        axis1_label = format_axis_ref(wrt1)
        axis2_label = format_axis_ref(wrt2)

        # Calculate gamma (angle between vectors)
        raw_diff = abs(theta1_std_deg - theta2_std_deg)
        gamma = raw_diff if raw_diff <= 180 else 360 - raw_diff

        # Get coordinate system info for smart display
        if coordinate_system is not None and hasattr(coordinate_system, 'axis1_angle') and hasattr(coordinate_system, 'axis2_angle'):
            # Base angle between positive axes
            base_axis_angle_deg = abs(math.degrees(coordinate_system.axis2_angle - coordinate_system.axis1_angle))

            # Determine which axis each vector references and if it's negative
            wrt1_stripped = wrt1.lower().lstrip('+-')
            wrt2_stripped = wrt2.lower().lstrip('+-')
            wrt1_is_negative = wrt1.lower().startswith('-')
            wrt2_is_negative = wrt2.lower().startswith('-')

            # Compute the effective angle between the referenced axes
            # When one axis is negative, add 180° to get the effective angle
            # For example, if +a to +b is 40°, then +a to -b is 180° - 40° = 140°
            effective_axis_angle_deg = base_axis_angle_deg
            if wrt1_stripped != wrt2_stripped:
                # Different axes - check if one or both are negative
                if wrt1_is_negative != wrt2_is_negative:
                    # One positive, one negative: angle is 180° - base_angle
                    effective_axis_angle_deg = 180 - base_axis_angle_deg
                # If both same sign (both positive or both negative), use base angle

            # Get absolute values of input angles for cleaner display
            abs_theta1 = abs(theta1_input_deg)
            abs_theta2 = abs(theta2_input_deg)

            # Case 2a: One vector is along its axis (angle=0), other has an offset from a different axis
            # This is the common decomposition case like F_2u along +u and F_2 at -30° from +u
            if abs(theta1_input_deg) < 0.5 and wrt1_stripped != wrt2_stripped:
                # vec1 is along its axis, vec2 has an offset from a different axis
                # The angle is: |effective_angle_between_axes - vec2_offset| or |effective_angle_between_axes + vec2_offset|
                if abs(effective_axis_angle_deg - abs_theta2 - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = ∠({axis1_label},{axis2_label}) - |∠({axis2_label},{vec2_name})|\n"
                        f"= {effective_axis_angle_deg:.0f}° - {abs_theta2:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )
                elif abs(effective_axis_angle_deg + abs_theta2 - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = ∠({axis1_label},{axis2_label}) + |∠({axis2_label},{vec2_name})|\n"
                        f"= {effective_axis_angle_deg:.0f}° + {abs_theta2:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )
                elif abs(abs_theta2 - effective_axis_angle_deg - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = |∠({axis2_label},{vec2_name})| - ∠({axis1_label},{axis2_label})\n"
                        f"= {abs_theta2:.0f}° - {effective_axis_angle_deg:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )

            elif abs(theta2_input_deg) < 0.5 and wrt1_stripped != wrt2_stripped:
                # vec2 is along its axis, vec1 has an offset from a different axis
                if abs(effective_axis_angle_deg - abs_theta1 - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = ∠({axis1_label},{axis2_label}) - |∠({axis1_label},{vec1_name})|\n"
                        f"= {effective_axis_angle_deg:.0f}° - {abs_theta1:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )
                elif abs(effective_axis_angle_deg + abs_theta1 - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = ∠({axis1_label},{axis2_label}) + |∠({axis1_label},{vec1_name})|\n"
                        f"= {effective_axis_angle_deg:.0f}° + {abs_theta1:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )
                elif abs(abs_theta1 - effective_axis_angle_deg - result_deg) < 0.5:
                    return (
                        f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name})| - ∠({axis1_label},{axis2_label})\n"
                        f"= {abs_theta1:.0f}° - {effective_axis_angle_deg:.0f}°\n"
                        f"= {result_deg:.0f}°"
                    )

            # Case 2b: Both vectors have the same angle relative to their respective axes
            # Show directly as 180° - axis_angle to get the interior angle
            if abs(theta1_input_deg - theta2_input_deg) < 0.5 and abs(effective_axis_angle_deg - gamma) < 0.5:
                return (
                    f"∠({vec1_name},{vec2_name}) = 180° - ∠({axis1_label},{axis2_label})\n"
                    f"= 180° - {effective_axis_angle_deg:.0f}°\n"
                    f"= {result_deg:.0f}°"
                )

            # Case 2c: Same axis - simple difference
            if wrt1_stripped == wrt2_stripped:
                return (
                    f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name}) - ∠({axis1_label},{vec2_name})|\n"
                    f"= |{theta1_input_deg:.0f}° - {theta2_input_deg:.0f}°|\n"
                    f"= {result_deg:.0f}°"
                )

        # Fallback: show using angle between vectors in the triangle
        # For force triangles, the interior angle is 180° - gamma only when dealing with parallelogram law
        # For decomposition triangles, the interior angle may be gamma directly
        #
        # Important: The interior angle formula depends on whether raw_diff > 180°
        # If raw_diff <= 180: interior = raw_diff, shown as |θ1 - θ2|
        # If raw_diff > 180: interior = 360 - raw_diff, shown as 360° - |θ1 - θ2|
        if abs(gamma - result_deg) < 0.5:
            # Result matches the interior angle (gamma)
            if raw_diff <= 180:
                return (
                    f"∠({vec1_name},{vec2_name}) = |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                    f"= {result_deg:.0f}°"
                )
            else:
                return (
                    f"∠({vec1_name},{vec2_name}) = 360° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                    f"= 360° - {raw_diff:.0f}°\n"
                    f"= {result_deg:.0f}°"
                )
        else:
            # Result is the supplementary angle (used in parallelogram law)
            if raw_diff <= 180:
                return (
                    f"∠({vec1_name},{vec2_name}) = 180° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                    f"= 180° - {gamma:.0f}°\n"
                    f"= {result_deg:.0f}°"
                )
            else:
                return (
                    f"∠({vec1_name},{vec2_name}) = 180° - (360° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|)\n"
                    f"= 180° - (360° - {raw_diff:.0f}°)\n"
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
    # Use geometric reasoning based on tip-to-tail vector placement

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

    # Check if 90 - angle relationship applies (single angle case)
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

    # Case 3a: Use opposite axis relationship for cleaner geometric explanation
    # When vectors are on opposite sides relative to their reference axes,
    # express using the complementary angle from the opposite axis
    # Example: F_1 at -40° from +y and F_2 at -35° from +x
    #   → F_2 is at 90° - 35° = 55° from -y
    #   → ∠(F_1, F_2) = |∠(y, F_1)| + ∠(-y, F_2) = 40° + 55° = 95°

    # Determine opposite axis labels
    opposite_axis = {"+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}
    opp_axis1 = opposite_axis.get(wrt1.lower(), wrt1)
    opp_axis2 = opposite_axis.get(wrt2.lower(), wrt2)
    opp_axis1_label = format_axis_ref(opp_axis1)
    opp_axis2_label = format_axis_ref(opp_axis2)

    # Calculate angles from opposite axes
    # If vec is at θ from +x, it's at (90° - θ) from +y or -y depending on direction
    # More generally: angle from opposite axis = 90° - |original angle|
    opp_theta1 = 90 - abs_theta1  # angle from opposite axis type
    opp_theta2 = 90 - abs_theta2

    # Check if using opposite axis for vec2 gives a clean formula
    # ∠(axis1, vec1) + ∠(opp_axis1, vec2) = result
    if abs(abs_theta1 + opp_theta2 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name})| + ∠({opp_axis1_label},{vec2_name})\n"
            f"= {abs_theta1:.0f}° + (90° - |∠({axis2_label},{vec2_name})|)\n"
            f"= {abs_theta1:.0f}° + (90° - {abs_theta2:.0f}°)\n"
            f"= {abs_theta1:.0f}° + {opp_theta2:.0f}°\n"
            f"= {result_deg:.0f}°"
        )

    # Check if using opposite axis for vec1 gives a clean formula
    if abs(opp_theta1 + abs_theta2 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = ∠({opp_axis2_label},{vec1_name}) + |∠({axis2_label},{vec2_name})|\n"
            f"= (90° - |∠({axis1_label},{vec1_name})|) + {abs_theta2:.0f}°\n"
            f"= (90° - {abs_theta1:.0f}°) + {abs_theta2:.0f}°\n"
            f"= {opp_theta1:.0f}° + {abs_theta2:.0f}°\n"
            f"= {result_deg:.0f}°"
        )

    # Check if using opposite axes for both gives a clean formula
    if abs(opp_theta1 + opp_theta2 - result_deg) < 0.5:
        return (
            f"∠({vec1_name},{vec2_name}) = ∠({opp_axis2_label},{vec1_name}) + ∠({opp_axis1_label},{vec2_name})\n"
            f"= (90° - {abs_theta1:.0f}°) + (90° - {abs_theta2:.0f}°)\n"
            f"= {opp_theta1:.0f}° + {opp_theta2:.0f}°\n"
            f"= {result_deg:.0f}°"
        )

    # Check subtraction with opposite axis
    if abs(abs(abs_theta1 - opp_theta2) - result_deg) < 0.5:
        if abs_theta1 >= opp_theta2:
            return (
                f"∠({vec1_name},{vec2_name}) = |∠({axis1_label},{vec1_name})| - ∠({opp_axis1_label},{vec2_name})\n"
                f"= {abs_theta1:.0f}° - (90° - {abs_theta2:.0f}°)\n"
                f"= {abs_theta1:.0f}° - {opp_theta2:.0f}°\n"
                f"= {result_deg:.0f}°"
            )
        else:
            return (
                f"∠({vec1_name},{vec2_name}) = ∠({opp_axis1_label},{vec2_name}) - |∠({axis1_label},{vec1_name})|\n"
                f"= (90° - {abs_theta2:.0f}°) - {abs_theta1:.0f}°\n"
                f"= {opp_theta2:.0f}° - {abs_theta1:.0f}°\n"
                f"= {result_deg:.0f}°"
            )

    if abs(abs(opp_theta1 - abs_theta2) - result_deg) < 0.5:
        if opp_theta1 >= abs_theta2:
            return (
                f"∠({vec1_name},{vec2_name}) = ∠({opp_axis2_label},{vec1_name}) - |∠({axis2_label},{vec2_name})|\n"
                f"= (90° - {abs_theta1:.0f}°) - {abs_theta2:.0f}°\n"
                f"= {opp_theta1:.0f}° - {abs_theta2:.0f}°\n"
                f"= {result_deg:.0f}°"
            )
        else:
            return (
                f"∠({vec1_name},{vec2_name}) = |∠({axis2_label},{vec2_name})| - ∠({opp_axis2_label},{vec1_name})\n"
                f"= {abs_theta2:.0f}° - (90° - {abs_theta1:.0f}°)\n"
                f"= {abs_theta2:.0f}° - {opp_theta1:.0f}°\n"
                f"= {result_deg:.0f}°"
            )

    # Fallback: show using standard angles from +x with proper interior angle calculation
    # First compute the interior angle (minimum angle between the two directions)
    raw_diff = abs(theta1_std_deg - theta2_std_deg)
    interior_deg = raw_diff if raw_diff <= 180 else 360 - raw_diff

    # Check if result matches the interior angle
    if abs(interior_deg - result_deg) < 0.5:
        # Result is the interior angle - show the calculation
        if raw_diff <= 180:
            return (
                f"∠({vec1_name},{vec2_name}) = |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                f"= {interior_deg:.0f}°"
            )
        else:
            return (
                f"∠({vec1_name},{vec2_name}) = 360° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                f"= 360° - {raw_diff:.0f}°\n"
                f"= {interior_deg:.0f}°"
            )
    else:
        # Result is the supplementary angle (used in parallelogram law)
        # Show the calculation through the interior angle
        if raw_diff <= 180:
            return (
                f"∠({vec1_name},{vec2_name}) = 180° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|\n"
                f"= 180° - {interior_deg:.0f}°\n"
                f"= {result_deg:.0f}°"
            )
        else:
            return (
                f"∠({vec1_name},{vec2_name}) = 180° - (360° - |{theta1_std_deg:.0f}° - {theta2_std_deg:.0f}°|)\n"
                f"= 180° - (360° - {raw_diff:.0f}°)\n"
                f"= 180° - {interior_deg:.0f}°\n"
                f"= {result_deg:.0f}°"
            )
