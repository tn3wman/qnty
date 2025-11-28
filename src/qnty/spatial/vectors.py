"""
Factory functions for creating Vector objects.

Provides convenient factory functions for creating _Vector objects
with various component specifications.
"""

from __future__ import annotations

from types import EllipsisType
from typing import TYPE_CHECKING, Any

import numpy as np

from ..core.unit import Unit
from .vector import _Vector

if TYPE_CHECKING:
    from .point import _Point


class _VectorWithUnknowns(_Vector):
    """
    _Vector subclass that tracks unknown components.

    Supports ellipsis (...) for marking components as unknown,
    and provides methods to lock/unlock components for solving.
    Also stores component vectors for resultant computation.
    """

    __slots__ = ("_unknowns", "_component_vectors", "_direction_unit_vector", "_is_constraint", "_alpha_rad", "_beta_rad", "_gamma_rad", "_original_plane", "_angle_unit", "_polar_magnitude", "_polar_angle_rad")

    def __init__(
        self,
        u: float,
        v: float,
        w: float,
        unit: Unit | None,
        unknowns: dict[str, str],
        component_vectors: list[_Vector] | None = None,
        name: str | None = None,
    ):
        super().__init__(u, v, w, unit=unit, name=name)
        self._unknowns = unknowns
        self._component_vectors = component_vectors or []
        self._direction_unit_vector = None
        self._is_constraint = False
        # Mark as unknown if there are any unknowns
        if unknowns:
            self.is_known = False

    @property
    def unknowns(self) -> dict[str, str]:
        """Dictionary of unknown components."""
        return self._unknowns

    @property
    def has_unknowns(self) -> bool:
        """Check if vector has any unknown components."""
        return len(self._unknowns) > 0

    @property
    def component_vectors(self) -> list[_Vector]:
        """List of vectors to sum for resultant computation."""
        return self._component_vectors

    @property
    def direction_unit_vector(self) -> np.ndarray | None:
        """Unit vector for direction (when magnitude is unknown)."""
        return self._direction_unit_vector

    @direction_unit_vector.setter
    def direction_unit_vector(self, value: np.ndarray | None) -> None:
        """Set the direction unit vector."""
        self._direction_unit_vector = value

    @property
    def is_constraint(self) -> bool:
        """True if this is a known resultant constraint for inverse solving."""
        return self._is_constraint

    def set_component(self, comp: str, value: float) -> None:
        """
        Set a component value (lock it as known).

        Args:
            comp: Component name ('u', 'v', or 'w')
            value: Value in current unit
        """
        if comp not in ('u', 'v', 'w'):
            raise ValueError(f"Invalid component '{comp}', must be 'u', 'v', or 'w'")

        # Remove from unknowns if present
        if comp in self._unknowns:
            del self._unknowns[comp]

        # Update internal coordinates
        idx = {'u': 0, 'v': 1, 'w': 2}[comp]

        # Convert value to SI
        if self._unit is not None:
            self._coords[idx] = value * self._unit.si_factor
        else:
            self._coords[idx] = value

        # Check if all unknowns are resolved
        if not self._unknowns:
            self.is_known = True

    def unlock_component(self, comp: str) -> None:
        """
        Unlock a component (make it unknown to solve for).

        Args:
            comp: Component name ('u', 'v', or 'w')
        """
        if comp not in ('u', 'v', 'w'):
            raise ValueError(f"Invalid component '{comp}', must be 'u', 'v', or 'w'")

        # Add to unknowns
        self._unknowns[comp] = comp

        # Set component to 0 (placeholder)
        idx = {'u': 0, 'v': 1, 'w': 2}[comp]
        self._coords[idx] = 0.0
        self.is_known = False

    def __str__(self) -> str:
        """String representation."""
        coords = self.to_array()
        unit_str = f" {self._unit.symbol}" if self._unit else ""

        # Format components, showing '...' for unknowns
        u_str = "..." if "u" in self._unknowns else f"{coords[0]:.6g}"
        v_str = "..." if "v" in self._unknowns else f"{coords[1]:.6g}"
        w_str = "..." if "w" in self._unknowns else f"{coords[2]:.6g}"

        name_str = f"'{self.name}' " if self.name else ""
        return f"_Vector({name_str}{u_str}, {v_str}, {w_str}{unit_str})"


def create_vector_cartesian(
    u: float = 0.0,
    v: float = 0.0,
    w: float = 0.0,
    unit: Unit | str | None = None,
    from_point: "Any | None" = None,
    name: str | None = None,
) -> _Vector:
    """
    Create a vector using Cartesian components, optionally at a specific point.

    This factory function provides a convenient way to create _Vector objects
    with explicit u, v, w components. Unspecified components default to zero.

    Args:
        u: First component (default 0.0)
        v: Second component (default 0.0)
        w: Third component (default 0.0)
        unit: Unit for components
        from_point: Optional point where vector originates/acts (for moment calculations)
        name: Optional vector name

    Returns:
        _Vector object with the specified components

    Examples:
        >>> from qnty.spatial import create_vector_cartesian, create_point_cartesian
        >>>
        >>> # Vector with all components (at origin by default)
        >>> v = create_vector_cartesian(u=3, v=4, w=0, unit="m")
        >>>
        >>> # Vector with default w=0
        >>> v2 = create_vector_cartesian(u=5, v=10, unit="ft")
        >>>
        >>> # Vector along w-axis
        >>> v3 = create_vector_cartesian(w=300, unit="mm")
        >>>
        >>> # Force vector acting at a specific point
        >>> A = create_point_cartesian(x=3, y=0, z=0, unit="m")
        >>> F = create_vector_cartesian(u=60, v=12, w=-40, unit="N", from_point=A)
    """
    # Resolve unit if string
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        unit = resolved

    vec = _Vector(float(u), float(v), float(w), unit=unit, name=name)

    # If a point of application is specified, store it
    if from_point is not None:
        vec._from_point = from_point

    return vec


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
    magnitude: "float | EllipsisType",
    unit: Unit | str,
    angle: "float | EllipsisType",
    angle_unit: str = "degree",
    wrt: str = "+x",
    plane: str = "xy",
    name: str | None = None,
) -> "_Vector | _VectorWithUnknowns":
    """
    Create a vector using polar coordinates in a plane.

    This factory function provides a convenient way to define vectors using polar
    coordinates within a specific plane (xy, xz, or yz).

    Args:
        magnitude: Vector magnitude, or ... for unknown
        unit: Unit for magnitude
        angle: Angle measured from reference axis (CCW positive), or ... for unknown
        angle_unit: Angle unit ("degree" or "radian")
        wrt: Reference axis for angle ("+x", "-x", "+y", "-y", "+z", "-z")
        plane: Plane containing the vector ("xy", "xz", "yz")
        name: Optional vector name

    Returns:
        _Vector object with computed components, or _VectorWithUnknowns if magnitude
        or angle is unknown (ellipsis)

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
        >>>
        >>> # Unknown vector (for solving)
        >>> v3 = create_vector_polar(magnitude=..., angle=..., unit="N", name="F_1")
    """
    import math

    # Check for unknown values (ellipsis)
    has_unknown_magnitude = magnitude is ...
    has_unknown_angle = angle is ...
    has_unknowns = has_unknown_magnitude or has_unknown_angle

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

    # Handle unknown values - return _VectorWithUnknowns
    if has_unknowns:
        unknowns: dict[str, str] = {}
        if has_unknown_magnitude:
            unknowns["magnitude"] = "magnitude"
        if has_unknown_angle:
            unknowns["angle"] = "angle"

        result = _VectorWithUnknowns(
            u=0.0,
            v=0.0,
            w=0.0,
            unit=resolved_unit,
            unknowns=unknowns,
            name=name,
        )
        result.is_known = False

        # Store known values for partial solving (use polar-specific attributes)
        if not has_unknown_magnitude:
            result._polar_magnitude = float(magnitude)  # type: ignore[arg-type]
        else:
            result._polar_magnitude = None
        if not has_unknown_angle:
            # Convert and store angle
            if angle_unit.lower() in ("degree", "degrees", "deg"):
                result._polar_angle_rad = math.radians(float(angle))  # type: ignore[arg-type]
            else:
                result._polar_angle_rad = float(angle)  # type: ignore[arg-type]
        else:
            result._polar_angle_rad = None

        # Store wrt and plane for later computation
        result._original_wrt = wrt
        result._original_plane = plane
        result._angle_unit = angle_unit

        return result

    # Both magnitude and angle are known - compute Cartesian components
    # At this point we know neither is ellipsis, so cast to float
    angle_value = float(angle)  # type: ignore[arg-type]
    magnitude_value = float(magnitude)  # type: ignore[arg-type]

    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(angle_value)
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = angle_value
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Compute Cartesian components
    mag_val = magnitude_value

    # Axis angles for each plane (following right-hand rule)
    # xy plane: thumb +z, fingers curl +x → +y (CCW from above)
    # xz plane: thumb +y, fingers curl -x → +z → +x → -z
    # yz plane: thumb +x, fingers curl +y → +z
    axis_angles = {
        "xy": {"+x": 0, "+y": 90, "-x": 180, "-y": 270},
        "xz": {"+x": 0, "+z": 90, "-x": 180, "-z": 270},
        "yz": {"+y": 0, "+z": 90, "-y": 180, "-z": 270},
    }

    # Get the base angle for the reference axis
    base_angle_deg = axis_angles[plane_lower][wrt_lower]

    # Total angle in the plane
    # For xz plane, negate angle to follow right-hand rule (thumb +y, -x → +z)
    if plane_lower == "xz":
        total_angle_rad = math.radians(base_angle_deg) - angle_rad
    else:
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

    vec = _Vector(u, v, w, unit=resolved_unit, name=name)
    # Store original angle and reference for reporting
    vec._original_angle = angle_value
    vec._original_wrt = wrt
    return vec


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
) -> _Vector:
    """
    Create a vector from point A to point B.

    This factory function creates a position vector r_AB = B - A representing
    the displacement from from_point to to_point.

    Args:
        from_point: Starting point A
        to_point: Ending point B
        name: Optional vector name (default "r")

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

    return result


def create_vector_with_magnitude(
    from_point: "_Point",
    to_point: "_Point",
    magnitude: float,
    unit: Unit | str | None = None,
    name: str | None = None,
) -> _Vector:
    """
    Create a vector between two points with a known magnitude constraint.

    Use this when points have unknown coordinates but the distance between
    them is known. The magnitude acts as a constraint for solving the unknowns.

    For simple displacement between known points, use create_vector_from_points instead.

    Args:
        from_point: Starting point A
        to_point: Ending point B
        magnitude: Known magnitude/distance between points
        unit: Unit for the magnitude
        name: Optional vector name (default "r")

    Returns:
        _Vector with magnitude constraint stored for solving

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_vector_with_magnitude
        >>>
        >>> # Point A is unknown, B is at origin, distance is 9m
        >>> A = create_point_cartesian(x=..., y=..., z=..., unit="m")
        >>> B = create_point_cartesian(x=0, y=0, z=0, unit="m")
        >>> r_AB = create_vector_with_magnitude(A, B, magnitude=9, unit="m", name="r_AB")
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

    # Store magnitude constraint
    if isinstance(unit, str):
        from ..core.unit import ureg
        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        result._constraint_magnitude = magnitude * resolved.si_factor
    elif unit is not None:
        result._constraint_magnitude = magnitude * unit.si_factor
    else:
        result._constraint_magnitude = magnitude

    return result


def create_vector_along(
    vector: _Vector,
    magnitude: "float | EllipsisType | Any",
    unit: Unit | str | None = None,
    name: str | None = None,
) -> _Vector | _VectorWithUnknowns:
    """
    Create a vector with specified magnitude along the direction of another vector.

    This is useful for creating force vectors along position vectors or
    direction vectors. The resulting vector has the same direction as the
    input vector but with the specified magnitude.

    Args:
        vector: Direction vector (will be normalized)
        magnitude: Magnitude for the new vector, or ... for unknown magnitude,
                   or a Quantity object (unit will be inferred from the Quantity)
        unit: Unit for the magnitude (e.g., "N" for force). If magnitude is a Quantity,
              this parameter is ignored and the Quantity's unit is used.
        name: Optional name for the new vector

    Returns:
        _Vector with specified magnitude along the direction of input vector,
        or _VectorWithUnknowns if magnitude is unknown

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_vector_from_points, create_vector_along
        >>>
        >>> # Create position vector from A to B
        >>> A = create_point_cartesian(x=0, y=4, z=0, unit="ft")
        >>> B = create_point_cartesian(x=2, y=0, z=-6, unit="ft")
        >>> r_AB = create_vector_from_points(A, B, name="r_AB")
        >>>
        >>> # Create force vector along r_AB with magnitude 300 N
        >>> F_AB = create_vector_along(r_AB, magnitude=300, unit="N", name="F_AB")
        >>>
        >>> # Create force with unknown magnitude (for solving)
        >>> F_unknown = create_vector_along(r_AB, magnitude=..., unit="N", name="F")
        >>>
        >>> # Create force with Quantity magnitude (from dot product result)
        >>> F_proj = F.dot(r_AB.unit_vector())  # Returns Quantity
        >>> F_along = create_vector_along(r_AB, magnitude=F_proj, name="F_along")
    """
    import math

    from ..core.quantity import Quantity

    # Handle Quantity magnitude - extract value and unit
    mag_value: float | EllipsisType
    if isinstance(magnitude, Quantity):
        if magnitude.value is None:
            raise ValueError("Quantity magnitude has no value")
        # Get the preferred unit from the Quantity
        qty_unit = magnitude.preferred
        if qty_unit is None:
            from ..core.unit import ureg
            qty_unit = ureg.preferred_for(magnitude.dim) or ureg.si_unit_for(magnitude.dim)
        # Get the value in that unit
        mag_value = magnitude.magnitude(qty_unit)
        # Use the Quantity's unit, ignore the unit parameter
        resolved_unit = qty_unit
    else:
        mag_value = magnitude
        # Resolve unit if string
        resolved_unit = None
        if isinstance(unit, str):
            from ..core.unit import ureg

            resolved = ureg.resolve(unit)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            resolved_unit = resolved
        elif unit is not None:
            resolved_unit = unit
        else:
            resolved_unit = vector._unit

    # Get direction vector components (in SI)
    coords = vector._coords

    # Calculate magnitude of direction vector
    dir_magnitude = math.sqrt(sum(c**2 for c in coords))

    if dir_magnitude == 0:
        raise ValueError("Cannot create vector along zero-length direction vector")

    # Calculate unit vector components (dimensionless)
    unit_vec = coords / dir_magnitude

    # Handle unknown magnitude
    if mag_value is ...:
        # Create a _VectorWithUnknowns with known direction but unknown magnitude
        # Store the unit vector for later scaling when magnitude is solved
        result = _VectorWithUnknowns(
            u=0.0,
            v=0.0,
            w=0.0,
            unit=resolved_unit,
            unknowns={"magnitude": "magnitude"},
            name=name or vector.name,
        )
        # Store the unit vector for solving
        result._direction_unit_vector = unit_vec
        result.is_known = False
        return result

    # Scale by desired magnitude
    # The user provides magnitude in the target unit (e.g., 350 lbf)
    # We need to return components in that same unit
    # Since _Vector constructor converts input to SI, we pass values in target unit
    new_coords = unit_vec * mag_value

    # Create the result vector
    # Pass values in target unit - constructor will convert to SI internally
    result = _Vector(
        float(new_coords[0]),
        float(new_coords[1]),
        float(new_coords[2]),
        unit=resolved_unit,
        name=name or vector.name,
    )

    return result


def create_point_at_midpoint(
    from_point: "Any",
    to_point: "Any",
    name: str | None = None,
) -> "_Point":
    """
    Create a point at the midpoint between two points.

    Args:
        from_point: Starting point
        to_point: Ending point
        name: Optional name for the midpoint

    Returns:
        _Point at the midpoint

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_point_at_midpoint
        >>>
        >>> A = create_point_cartesian(x=0, y=0, z=0, unit="m")
        >>> B = create_point_cartesian(x=4, y=6, z=2, unit="m")
        >>> M = create_point_at_midpoint(A, B, name="M")
        >>> # M = (2, 3, 1) m
    """
    from .point import _Point

    # Convert to _Point if needed
    if hasattr(from_point, 'to_cartesian'):
        from_pt = from_point.to_cartesian()
    else:
        from_pt = from_point
    if hasattr(to_point, 'to_cartesian'):
        to_pt = to_point.to_cartesian()
    else:
        to_pt = to_point

    # Compute midpoint coordinates (in SI)
    mid_coords = (from_pt._coords + to_pt._coords) / 2.0

    # Get unit from first point
    unit = from_pt._unit or to_pt._unit

    # Create midpoint
    result = object.__new__(_Point)
    result._coords = mid_coords
    result._dim = from_pt._dim
    result._unit = unit

    # Note: name parameter available for future use with named points
    _ = name

    return result


def create_vector_resultant(
    *vectors: _Vector,
    name: str = "F_R",
    unit: Unit | str | None = None,
) -> _VectorWithUnknowns:
    """
    Create a resultant vector placeholder from component vectors.

    This function creates a _VectorWithUnknowns with all components unknown
    (like create_vector_cartesian(u=..., v=..., w=...)). The component vectors
    are stored so the solver can compute the actual values by summing them.

    Args:
        *vectors: Variable number of vectors to sum
        name: Name for the resultant vector (default "F_R")
        unit: Preferred unit for the result

    Returns:
        _VectorWithUnknowns with all components unknown and component vectors stored

    Examples:
        >>> from qnty.spatial import ForceVector, create_vector_resultant
        >>>
        >>> # Define vectors and resultant
        >>> F_1 = ForceVector(magnitude=200, angle=30, unit="N", name="F_1")
        >>> F_2 = ForceVector(magnitude=150, angle=120, unit="N", name="F_2")
        >>> F_R = create_vector_resultant(F_1, F_2, name="F_R")
        >>>
        >>> # In a problem class
        >>> class MyProblem(RectangularVectorProblem):
        ...     F_1 = ForceVector(magnitude=200, angle=30, unit="N", name="F_1")
        ...     F_2 = ForceVector(magnitude=150, angle=120, unit="N", name="F_2")
        ...     F_R = create_vector_resultant(F_1, F_2, name="F_R")
    """
    # Resolve unit if string
    resolved_unit = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    elif unit is not None:
        resolved_unit = unit
    elif vectors:
        # Get unit from first vector
        resolved_unit = vectors[0]._unit

    # All components are unknown - they will be computed from component vectors
    unknowns = {"u": "u", "v": "v", "w": "w"}

    # Create the resultant vector with all unknowns
    result = _VectorWithUnknowns(
        u=0.0,
        v=0.0,
        w=0.0,
        unit=resolved_unit,
        unknowns=unknowns,
        component_vectors=list(vectors),
        name=name,
    )
    result.is_resultant = True

    return result


def create_vector_resultant_cartesian(
    *vectors: _Vector,
    u: float = 0.0,
    v: float = 0.0,
    w: float = 0.0,
    unit: Unit | str | None = None,
    name: str = "F_R",
) -> _VectorWithUnknowns:
    """
    Create a known resultant constraint for inverse solving.

    This function defines a known resultant vector (u, v, w) that equals the sum
    of component vectors with unknown magnitudes. The solver will use this
    constraint to solve for the unknown magnitudes.

    This is the inverse of create_vector_resultant:
    - create_vector_resultant: unknown resultant = sum of known vectors
    - create_vector_resultant_cartesian: known resultant = sum of unknown vectors

    Args:
        *vectors: Component vectors with unknown magnitudes (from create_vector_along with ...)
        u: x-component of the known resultant
        v: y-component of the known resultant
        w: z-component of the known resultant
        unit: Unit for the resultant
        name: Name for the resultant (default "F_R")

    Returns:
        _VectorWithUnknowns with known values and component vectors stored for constraint solving

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_vector_from_points
        >>> from qnty.spatial import create_vector_along, create_vector_resultant_cartesian
        >>>
        >>> # Define points and position vectors
        >>> O = create_point_cartesian(x=0, y=0, z=6, unit="ft")
        >>> A = create_point_cartesian(x=3, y=-2, z=0, unit="ft")
        >>> r_OA = create_vector_from_points(O, A)
        >>>
        >>> # Create force with unknown magnitude
        >>> F_A = create_vector_along(r_OA, magnitude=..., unit="lbf", name="F_A")
        >>>
        >>> # Define known resultant as constraint (solve for F_A, F_B, F_C magnitudes)
        >>> F_R = create_vector_resultant_cartesian(
        ...     F_A, F_B, F_C,
        ...     u=0, v=0, w=-130,
        ...     unit="lbf",
        ...     name="F_R"
        ... )
    """
    # Resolve unit if string
    resolved_unit = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    elif unit is not None:
        resolved_unit = unit
    elif vectors:
        # Get unit from first vector
        resolved_unit = vectors[0]._unit

    # Create with the known resultant values (no unknowns in the resultant itself)
    # But store the component vectors for the solver to set up equilibrium equations
    result = _VectorWithUnknowns(
        u=u,
        v=v,
        w=w,
        unit=resolved_unit,
        unknowns={},  # Resultant values are known
        component_vectors=list(vectors),
        name=name,
    )
    result.is_resultant = True
    result.is_known = True  # The resultant itself is known
    result._is_constraint = True  # Mark this as a constraint for inverse solving

    return result


def create_vector_resultant_polar(
    *vectors: _Vector,
    magnitude: float,
    angle: float,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    wrt: str = "+x",
    name: str = "F_R",
) -> _VectorWithUnknowns:
    """
    Create a known resultant constraint using polar coordinates for inverse solving.

    This function defines a known resultant vector (magnitude, angle) that equals the sum
    of component vectors with unknown magnitudes. The solver will use this
    constraint to solve for the unknown magnitudes.

    This is the polar equivalent of create_vector_resultant_cartesian:
    - create_vector_resultant: unknown resultant = sum of known vectors
    - create_vector_resultant_cartesian: known resultant (u, v, w) = sum of unknown vectors
    - create_vector_resultant_polar: known resultant (magnitude, angle) = sum of unknown vectors

    Args:
        *vectors: Component vectors with unknown magnitudes (from create_vector_along with ...)
        magnitude: Magnitude of the known resultant
        angle: Angle of the known resultant (measured CCW from reference axis)
        unit: Unit for the resultant magnitude
        angle_unit: Angle unit ("degree" or "radian")
        wrt: Reference axis for angle measurement ("+x", "-x", "+y", "-y")
        name: Name for the resultant (default "F_R")

    Returns:
        _VectorWithUnknowns with known values and component vectors stored for constraint solving

    Examples:
        >>> from qnty.spatial import create_point_cartesian, create_vector_from_points
        >>> from qnty.spatial import create_vector_along, create_vector_resultant_polar
        >>>
        >>> # Define points and position vectors
        >>> O = create_point_cartesian(x=0, y=0, z=0, unit="ft")
        >>> A = create_point_cartesian(x=3, y=4, z=0, unit="ft")
        >>> r_OA = create_vector_from_points(O, A)
        >>>
        >>> # Create force with unknown magnitude
        >>> F_A = create_vector_along(r_OA, magnitude=..., unit="lbf", name="F_A")
        >>>
        >>> # Define known resultant as constraint using polar form
        >>> F_R = create_vector_resultant_polar(
        ...     F_A, F_B,
        ...     magnitude=500, angle=45,
        ...     unit="lbf",
        ...     name="F_R"
        ... )
    """
    import math

    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Handle wrt (reference axis) - convert to standard angle from +x
    wrt_lower = wrt.lower()
    axis_angles = {
        "+x": 0,
        "+y": 90,
        "-x": 180,
        "-y": 270,
    }
    if wrt_lower not in axis_angles:
        raise ValueError(f"Invalid wrt axis '{wrt}'. Must be one of: {set(axis_angles.keys())}")

    base_angle_rad = math.radians(axis_angles[wrt_lower])
    total_angle_rad = base_angle_rad + angle_rad

    # Compute Cartesian components from polar
    mag_val = float(magnitude)
    u = mag_val * math.cos(total_angle_rad)
    v = mag_val * math.sin(total_angle_rad)
    w = 0.0

    # Resolve unit if string
    resolved_unit = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    elif unit is not None:
        resolved_unit = unit
    elif vectors:
        # Get unit from first vector
        resolved_unit = vectors[0]._unit

    # Create with the known resultant values (no unknowns in the resultant itself)
    # But store the component vectors for the solver to set up equilibrium equations
    result = _VectorWithUnknowns(
        u=u,
        v=v,
        w=w,
        unit=resolved_unit,
        unknowns={},  # Resultant values are known
        component_vectors=list(vectors),
        name=name,
    )
    result.is_resultant = True
    result.is_known = True  # The resultant itself is known
    result._is_constraint = True  # Mark this as a constraint for inverse solving

    # Store original angle and reference for reporting
    result._original_angle = float(angle)
    result._original_wrt = wrt

    return result


def create_vector_in_plane(
    plane: "Any",
    magnitude: float,
    angle: float,
    from_axis: str = "+y",
    toward_axis: str | None = None,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
) -> _Vector:
    """
    Create a vector lying in a plane at a specified angle.

    The vector is defined by an angle measured from a reference axis
    (projected onto the plane) toward another axis.

    Args:
        plane: Plane object the vector lies in
        magnitude: Vector magnitude
        angle: Angle from reference axis (positive toward toward_axis)
        from_axis: Reference axis to measure angle from ("+x", "+y", "+z", etc.)
        toward_axis: Axis to rotate toward (auto-determined if None)
        unit: Unit for magnitude
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional vector name

    Returns:
        _Vector object lying in the plane

    Examples:
        >>> from qnty.spatial import create_plane_rotated_y, create_vector_in_plane
        >>>
        >>> # Plane rotated -30° around y-axis (normal 30° from +z toward +x)
        >>> plane = create_plane_rotated_y(angle=-30)
        >>>
        >>> # Force 30° from +y axis within the plane
        >>> F = create_vector_in_plane(
        ...     plane, magnitude=450, angle=30, from_axis="+y", unit="N", name="F"
        ... )
    """
    import math

    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Get axis vectors
    axis_vectors = {
        "+x": np.array([1.0, 0.0, 0.0]),
        "-x": np.array([-1.0, 0.0, 0.0]),
        "+y": np.array([0.0, 1.0, 0.0]),
        "-y": np.array([0.0, -1.0, 0.0]),
        "+z": np.array([0.0, 0.0, 1.0]),
        "-z": np.array([0.0, 0.0, -1.0]),
    }

    from_lower = from_axis.lower()
    if from_lower not in axis_vectors:
        raise ValueError(f"Invalid from_axis '{from_axis}'. Must be one of: {set(axis_vectors.keys())}")

    from_vec = axis_vectors[from_lower]
    normal = plane.normal

    # Project the reference axis onto the plane
    # v_proj = v - (v · n) * n
    from_proj = from_vec - np.dot(from_vec, normal) * normal
    from_proj_mag = np.linalg.norm(from_proj)

    if from_proj_mag < 1e-9:
        raise ValueError(f"Axis '{from_axis}' is perpendicular to the plane")

    # Normalize
    u1 = from_proj / from_proj_mag

    # Determine the second basis vector in the plane
    # It should be perpendicular to both the normal and u1
    # Use right-hand rule: u2 = n × u1
    u2 = np.cross(normal, u1)

    # If toward_axis is specified, check if u2 points toward it
    if toward_axis is not None:
        toward_lower = toward_axis.lower()
        if toward_lower not in axis_vectors:
            raise ValueError(f"Invalid toward_axis '{toward_axis}'. Must be one of: {set(axis_vectors.keys())}")
        toward_vec = axis_vectors[toward_lower]
        # If u2 points away from toward_axis, flip it
        if np.dot(u2, toward_vec) < 0:
            u2 = -u2

    # Create vector: magnitude * (cos(angle) * u1 + sin(angle) * u2)
    direction = math.cos(angle_rad) * u1 + math.sin(angle_rad) * u2
    components = magnitude * direction

    # Resolve unit
    resolved_unit = None
    if isinstance(unit, str):
        from ..core.unit import ureg
        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    elif unit is not None:
        resolved_unit = unit

    return _Vector(
        float(components[0]),
        float(components[1]),
        float(components[2]),
        unit=resolved_unit,
        name=name,
    )


def create_vector_direction_angles(
    magnitude: float,
    alpha: float | EllipsisType | None = None,
    beta: float | EllipsisType | None = None,
    gamma: float | EllipsisType | None = None,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
    signs: tuple[int, int, int] | None = None,
) -> _Vector | _VectorWithUnknowns:
    """
    Create a vector using magnitude and coordinate direction angles.

    This factory function provides a convenient way to define 3D vectors using
    coordinate direction angles:
    - alpha: angle from +x axis
    - beta: angle from +y axis
    - gamma: angle from +z axis

    The conversion formulas are:
    - u = magnitude * cos(alpha)
    - v = magnitude * cos(beta)
    - w = magnitude * cos(gamma)

    Note: The angles must satisfy: cos²α + cos²β + cos²γ = 1
    At least 2 of the 3 angles must be provided. The third will be calculated.

    Args:
        magnitude: Vector magnitude
        alpha: Angle from +x axis (optional if other two provided, use ... for unknown)
        beta: Angle from +y axis (optional if other two provided, use ... for unknown)
        gamma: Angle from +z axis (optional if other two provided, use ... for unknown)
        unit: Unit for magnitude
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional vector name
        cos_signs: Signs for direction cosines (cos_α, cos_β, cos_γ) as (-1, 1, 1) etc.
                   Use to resolve sign ambiguity when calculating missing angles.

    Returns:
        _Vector object with u, v, w components

    Raises:
        ValueError: If angles don't satisfy the constraint or fewer than 2 provided

    Examples:
        >>> from qnty.spatial import create_vector_direction_angles
        >>>
        >>> # Vector with magnitude 100N, alpha=60 deg, beta=45 deg, gamma=120 deg
        >>> v = create_vector_direction_angles(magnitude=100, alpha=60, beta=45, gamma=120, unit="N")
        >>>
        >>> # Vector with two angles (third calculated)
        >>> v2 = create_vector_direction_angles(magnitude=100, alpha=60, beta=45, unit="N")
        >>>
        >>> # Vector with unknown angle (returns _VectorWithUnknowns for solving)
        >>> v3 = create_vector_direction_angles(magnitude=60, alpha=..., beta=60, gamma=60, unit="lbf")
    """
    import math

    mag_val = float(magnitude)

    # Check for ellipsis (unknown angle that needs solving)
    has_unknown = alpha is ... or beta is ... or gamma is ...

    # Convert angles to radians (treat ellipsis as None for calculation)
    def to_radians(angle_val):
        if angle_val is None or angle_val is ...:
            return None
        if angle_unit.lower() in ("degree", "degrees", "deg"):
            return math.radians(float(angle_val))
        elif angle_unit.lower() in ("radian", "radians", "rad"):
            return float(angle_val)
        else:
            raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    alpha_rad = to_radians(alpha)
    beta_rad = to_radians(beta)
    gamma_rad = to_radians(gamma)

    # Calculate missing angle from constraint cos²α + cos²β + cos²γ = 1
    # Use cos_signs to determine sign of calculated cosine (default positive)
    sign_alpha = signs[0] if signs else 1
    sign_beta = signs[1] if signs else 1
    sign_gamma = signs[2] if signs else 1

    if alpha_rad is None and beta_rad is not None and gamma_rad is not None:
        cos_alpha_sq = 1 - math.cos(beta_rad) ** 2 - math.cos(gamma_rad) ** 2
        if cos_alpha_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_alpha = sign_alpha * math.sqrt(cos_alpha_sq)
        alpha_rad = math.acos(cos_alpha)
    elif beta_rad is None and alpha_rad is not None and gamma_rad is not None:
        cos_beta_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(gamma_rad) ** 2
        if cos_beta_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_beta = sign_beta * math.sqrt(cos_beta_sq)
        beta_rad = math.acos(cos_beta)
    elif gamma_rad is None and alpha_rad is not None and beta_rad is not None:
        cos_gamma_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(beta_rad) ** 2
        if cos_gamma_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_gamma = sign_gamma * math.sqrt(cos_gamma_sq)
        gamma_rad = math.acos(cos_gamma)
    elif alpha_rad is None or beta_rad is None or gamma_rad is None:
        raise ValueError("Must provide at least 2 of the 3 coordinate direction angles")

    # Validate the constraint
    sum_cos_sq = math.cos(alpha_rad) ** 2 + math.cos(beta_rad) ** 2 + math.cos(gamma_rad) ** 2
    if abs(sum_cos_sq - 1.0) > 1e-6:
        raise ValueError(f"Direction angles must satisfy cos²α + cos²β + cos²γ = 1, got {sum_cos_sq}")

    # Resolve unit
    resolved_unit = None
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian components using direction cosines
    u = mag_val * math.cos(alpha_rad)
    v = mag_val * math.cos(beta_rad)
    w = mag_val * math.cos(gamma_rad)

    # If there was an unknown angle (ellipsis), return _VectorWithUnknowns
    # to indicate this needs solving (due to sign ambiguity in sqrt)
    if has_unknown:
        # Track which angle was unknown
        unknowns = {}
        if alpha is ...:
            unknowns["alpha"] = "alpha"
        if beta is ...:
            unknowns["beta"] = "beta"
        if gamma is ...:
            unknowns["gamma"] = "gamma"

        result = _VectorWithUnknowns(
            u=u,
            v=v,
            w=w,
            unit=resolved_unit,
            unknowns=unknowns,
            name=name,
        )
        # Store the computed angles for reference (positive sqrt solution)
        result._alpha_rad = alpha_rad
        result._beta_rad = beta_rad
        result._gamma_rad = gamma_rad
        return result

    return _Vector(u, v, w, unit=resolved_unit, name=name)
