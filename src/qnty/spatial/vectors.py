"""
Factory functions for creating Vector objects.

Provides convenient factory functions for creating _Vector objects
with various component specifications.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.unit import Unit
from .vector import _Vector

if TYPE_CHECKING:
    from .point import _Point


def create_vector_cartesian(
    u: float = 0.0,
    v: float = 0.0,
    w: float = 0.0,
    unit: Unit | str | None = None,
    name: str | None = None,
) -> _Vector:
    """
    Create a vector using Cartesian components.

    This factory function provides a convenient way to create _Vector objects
    with explicit u, v, w components. Unspecified components default to zero.

    Args:
        u: First component (default 0.0)
        v: Second component (default 0.0)
        w: Third component (default 0.0)
        unit: Unit for components
        name: Optional vector name

    Returns:
        _Vector object with the specified components

    Examples:
        >>> from qnty.spatial import create_vector_cartesian
        >>>
        >>> # Vector with all components
        >>> v = create_vector_cartesian(u=3, v=4, w=0, unit="m")
        >>>
        >>> # Vector with default w=0
        >>> v2 = create_vector_cartesian(u=5, v=10, unit="ft")
        >>>
        >>> # Vector along w-axis
        >>> v3 = create_vector_cartesian(w=300, unit="mm")
    """
    # Resolve unit if string
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        unit = resolved

    return _Vector(float(u), float(v), float(w), unit=unit, name=name)


def create_vector_from_ratio(
    magnitude: float,
    u: float,
    v: float,
    w: float = 0.0,
    unit: Unit | str | None = None,
    name: str | None = None,
) -> _Vector:
    """
    Create a vector using magnitude and direction ratios.

    This factory function provides a convenient way to define vectors using direction
    ratios, which are common in statics problems where directions are given
    as integer ratios (like 3-4-5, 5-12-13, 8-15-17 right triangles).

    The ratios define the relative proportions in each direction. The vector
    has the specified magnitude along that direction.

    Args:
        magnitude: Vector magnitude
        u: First component ratio (positive or negative)
        v: Second component ratio (positive or negative)
        w: Third component ratio (positive or negative)
        unit: Unit for vector components
        name: Optional vector name

    Returns:
        _Vector object with computed components

    Raises:
        ValueError: If ratios are all zero

    Examples:
        >>> from qnty.spatial import create_vector_from_ratio
        >>>
        >>> # Vector with magnitude 130N in direction 5-12-0
        >>> F = create_vector_from_ratio(
        ...     magnitude=130, u=5, v=12, w=0, unit="N"
        ... )
        >>> # Components: (50, 120, 0) N
        >>>
        >>> # Vector with magnitude 26m in 3D direction
        >>> v = create_vector_from_ratio(
        ...     magnitude=26, u=3, v=4, w=12, unit="m"
        ... )
    """
    import math

    # Validate ratios aren't all zero
    if u == 0 and v == 0 and w == 0:
        raise ValueError("Direction ratios cannot all be zero")

    # Resolve unit
    resolved_unit: Unit | None = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute vector components
    ru, rv, rw = float(u), float(v), float(w)
    mag_val = float(magnitude)

    # Compute the magnitude of the ratio vector
    ratio_magnitude = math.sqrt(ru**2 + rv**2 + rw**2)

    # Scale factor to get unit direction, then multiply by magnitude
    scale = mag_val / ratio_magnitude

    # Scale the ratios to get components
    u_comp = ru * scale
    v_comp = rv * scale
    w_comp = rw * scale

    return _Vector(u_comp, v_comp, w_comp, unit=resolved_unit, name=name)


def create_vector_polar(
    magnitude: float,
    angle: float,
    plane: str = "xy",
    wrt: str = "+x",
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
) -> _Vector:
    """
    Create a vector using polar coordinates in a plane.

    This factory function provides a convenient way to define vectors using polar
    coordinates within a specific plane (xy, xz, or yz).

    Args:
        magnitude: Vector magnitude
        angle: Angle measured from reference axis (CCW positive)
        plane: Plane containing the vector ("xy", "xz", "yz")
        wrt: Reference axis for angle ("+x", "-x", "+y", "-y", "+z", "-z")
        unit: Unit for magnitude
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional vector name

    Returns:
        _Vector object with computed components

    Raises:
        ValueError: If plane or wrt is invalid

    Examples:
        >>> from qnty.spatial import create_vector_polar
        >>>
        >>> # Vector at 5m, 30° from +x axis in xy plane
        >>> v = create_vector_polar(magnitude=5, angle=30, plane="xy", wrt="+x", unit="m")
        >>>
        >>> # Vector at 100N, 45° from +y axis in xy plane
        >>> v2 = create_vector_polar(magnitude=100, angle=45, plane="xy", wrt="+y", unit="N")
    """
    import math

    # Validate plane
    valid_planes = {"xy", "xz", "yz"}
    plane_lower = plane.lower()
    if plane_lower not in valid_planes:
        raise ValueError(f"Invalid plane '{plane}'. Must be one of: {valid_planes}")

    # Validate wrt axis
    valid_axes = {"+x", "-x", "+y", "-y", "+z", "-z"}
    wrt_lower = wrt.lower()
    if wrt_lower not in valid_axes:
        raise ValueError(f"Invalid wrt axis '{wrt}'. Must be one of: {valid_axes}")

    # Validate wrt axis is in the specified plane
    axis_char = wrt_lower[1]  # 'x', 'y', or 'z'
    if axis_char not in plane_lower:
        raise ValueError(
            f"Reference axis '{wrt}' must be in plane '{plane}'. "
            f"Valid axes for {plane} plane: {[f'+{c}' for c in plane] + [f'-{c}' for c in plane]}"
        )

    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Resolve unit
    resolved_unit: Unit | None = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian components
    mag_val = float(magnitude)

    # Axis angles for each plane
    axis_angles = {
        "xy": {"+x": 0, "+y": 90, "-x": 180, "-y": 270},
        "xz": {"+x": 0, "+z": 90, "-x": 180, "-z": 270},
        "yz": {"+y": 0, "+z": 90, "-y": 180, "-z": 270},
    }

    # Get the base angle for the reference axis
    base_angle_deg = axis_angles[plane_lower][wrt_lower]

    # Total angle in the plane (CCW from first axis of plane)
    total_angle_rad = math.radians(base_angle_deg) + angle_rad

    # Compute components based on plane
    if plane_lower == "xy":
        u = mag_val * math.cos(total_angle_rad)
        v = mag_val * math.sin(total_angle_rad)
        w = 0.0
    elif plane_lower == "xz":
        u = mag_val * math.cos(total_angle_rad)
        v = 0.0
        w = mag_val * math.sin(total_angle_rad)
    else:  # yz
        u = 0.0
        v = mag_val * math.cos(total_angle_rad)
        w = mag_val * math.sin(total_angle_rad)

    return _Vector(u, v, w, unit=resolved_unit, name=name)


def create_vector_spherical(
    magnitude: float,
    theta: float = 0.0,
    phi: float = 0.0,
    theta_wrt: str = "+x",
    phi_wrt: str = "+z",
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
) -> _Vector:
    """
    Create a vector using spherical coordinates.

    This factory function provides a convenient way to define 3D vectors using:
    - magnitude: length of the vector
    - theta: transverse angle in xy-plane (CCW from theta_wrt axis)
    - phi: azimuth angle from z-axis (CW from phi_wrt toward xy-plane)

    Args:
        magnitude: Vector magnitude
        theta: Transverse angle in xy-plane (CCW from theta_wrt axis)
        phi: Azimuth angle (CW from phi_wrt axis, toward xy-plane)
        theta_wrt: Reference axis for theta ("+x", "-x", "+y", "-y")
        phi_wrt: Reference for phi ("+z", "-z", "xy")
            - "+z": angle measured from +z axis toward xy-plane
            - "-z": angle measured from -z axis toward xy-plane
            - "xy": angle measured from xy-plane (+phi toward +z, -phi toward -z)
        unit: Unit for magnitude
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional vector name

    Returns:
        _Vector object with computed components

    Raises:
        ValueError: If theta_wrt or phi_wrt is invalid

    Examples:
        >>> from qnty.spatial import create_vector_spherical
        >>>
        >>> # Vector with magnitude 10m, theta=30° from +x, phi=60° from +z
        >>> v = create_vector_spherical(magnitude=10, theta=30, phi=60, unit="m")
        >>>
        >>> # With custom reference axes
        >>> v2 = create_vector_spherical(magnitude=5, theta=45, phi=30, theta_wrt="+y", phi_wrt="-z", unit="ft")
    """
    import math

    # Validate theta_wrt
    valid_theta_axes = {"+x", "-x", "+y", "-y"}
    theta_wrt_lower = theta_wrt.lower()
    if theta_wrt_lower not in valid_theta_axes:
        raise ValueError(f"Invalid theta_wrt '{theta_wrt}'. Must be one of: {valid_theta_axes}")

    # Validate phi_wrt
    valid_phi_axes = {"+z", "-z", "xy"}
    phi_wrt_lower = phi_wrt.lower()
    if phi_wrt_lower not in valid_phi_axes:
        raise ValueError(f"Invalid phi_wrt '{phi_wrt}'. Must be one of: {valid_phi_axes}")

    # Convert angles to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        theta_input_rad = math.radians(float(theta))
        phi_input_rad = math.radians(float(phi))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        theta_input_rad = float(theta)
        phi_input_rad = float(phi)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Convert theta to standard form (CCW from +x)
    theta_base_angles = {
        "+x": 0,
        "+y": 90,
        "-x": 180,
        "-y": 270,
    }
    theta_base_rad = math.radians(theta_base_angles[theta_wrt_lower])
    theta_rad = theta_base_rad + theta_input_rad

    # Convert phi to standard form (from +z)
    if phi_wrt_lower == "+z":
        phi_rad = phi_input_rad
    elif phi_wrt_lower == "-z":
        phi_rad = math.pi - phi_input_rad
    else:  # xy
        phi_rad = math.pi / 2 - phi_input_rad

    # Resolve unit
    resolved_unit: Unit | None = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian components
    mag_val = float(magnitude)
    u = mag_val * math.sin(phi_rad) * math.cos(theta_rad)
    v = mag_val * math.sin(phi_rad) * math.sin(theta_rad)
    w = mag_val * math.cos(phi_rad)

    return _Vector(u, v, w, unit=resolved_unit, name=name)


def create_vector_from_points(
    from_point: "_Point",
    to_point: "_Point",
    name: str | None = None,
    magnitude: float | None = None,
    unit: Unit | str | None = None,
) -> _Vector:
    """
    Create a vector from point A to point B.

    This factory function creates a position vector r_AB = B - A representing
    the displacement from from_point to to_point.

    If magnitude is provided, it acts as a constraint for solving unknown
    point coordinates. The direction is given by the force/direction vector.

    Args:
        from_point: Starting point A
        to_point: Ending point B
        name: Optional vector name (default "r")
        magnitude: Optional magnitude constraint for solving unknowns
        unit: Unit for magnitude constraint

    Returns:
        _Vector object representing the position vector

    Raises:
        ValueError: If points have different dimensions

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_vector_from_points
        >>>
        >>> # Simple position vector
        >>> A = create_point_cartesian(x=0, y=4, z=0, unit="ft")
        >>> B = create_point_cartesian(x=2, y=0, z=-6, unit="ft")
        >>> r_AB = create_vector_from_points(A, B, name="r_AB")
        >>>
        >>> # With magnitude constraint (for solving unknowns)
        >>> A = create_point_cartesian(x=..., y=..., z=..., unit="m")
        >>> B = create_point_cartesian(x=0, y=0, z=0, unit="m")
        >>> r_AB = create_vector_from_points(A, B, magnitude=9, unit="m", name="r_AB")
    """
    from .point import _Point

    # Convert to _Point if needed
    if isinstance(from_point, _Point):
        from_pt = from_point
    else:
        from_pt = from_point.to_cartesian()
    if isinstance(to_point, _Point):
        to_pt = to_point
    else:
        to_pt = to_point.to_cartesian()

    if from_pt._dim != to_pt._dim:
        raise ValueError(f"Points must have same dimension: {from_pt._dim} vs {to_pt._dim}")

    delta = to_pt._coords - from_pt._coords

    result = object.__new__(_Vector)
    result._coords = delta
    result._dim = from_pt._dim
    result._unit = from_pt._unit or to_pt._unit
    result.name = name or "r"
    result.is_known = True
    result.is_resultant = False
    result._description = ""
    result.coordinate_system = None
    result.angle_reference = None
    result._magnitude = None
    result._angle = None
    result._relative_to_force = None
    result._relative_angle = None
    result._from_point = from_point
    result._to_point = to_point

    if magnitude is not None:
        resolved_unit = unit
        if isinstance(unit, str):
            from ..core.dimension_catalog import dim
            from ..core.unit import ureg
            resolved = ureg.resolve(unit, dim=dim.length)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            resolved_unit = resolved
        result._constraint_magnitude = magnitude * resolved_unit.si_factor if resolved_unit else magnitude
    else:
        result._constraint_magnitude = None

    return result
