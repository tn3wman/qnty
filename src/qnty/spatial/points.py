"""
Factory functions for creating Point objects.

Provides convenient factory functions for creating _Point objects
with various coordinate specifications.
"""

from __future__ import annotations

from types import EllipsisType

import numpy as np

from ..core.unit import Unit
from .point import _Point


class _PointWithUnknowns(_Point):
    """
    _Point subclass that tracks unknown coordinates.

    Supports ellipsis (...) for marking coordinates as unknown,
    and provides methods to lock/unlock coordinates for solving.
    """

    __slots__ = ("_unknowns", "_name")

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        unit: Unit | None,
        unknowns: dict[str, str],
        name: str | None = None,
    ):
        super().__init__(x, y, z, unit=unit)
        self._unknowns = unknowns
        self._name = name

    @property
    def unknowns(self) -> dict[str, str]:
        """Dictionary of unknown coordinates."""
        return self._unknowns

    @property
    def has_unknowns(self) -> bool:
        """Check if point has any unknown coordinates."""
        return len(self._unknowns) > 0

    @property
    def name(self) -> str | None:
        """Point name."""
        return self._name

    def set_coordinate(self, coord: str, value: float) -> None:
        """
        Set a coordinate value (lock it as known).

        Args:
            coord: Coordinate name ('x', 'y', or 'z')
            value: Value in current unit
        """
        if coord not in ('x', 'y', 'z'):
            raise ValueError(f"Invalid coordinate '{coord}', must be 'x', 'y', or 'z'")

        # Remove from unknowns if present
        if coord in self._unknowns:
            del self._unknowns[coord]

        # Update internal coordinates
        idx = {'x': 0, 'y': 1, 'z': 2}[coord]

        # Convert value to SI
        if self._unit is not None:
            self._coords[idx] = value * self._unit.si_factor
        else:
            self._coords[idx] = value

    def unlock_coordinate(self, coord: str) -> None:
        """
        Unlock a coordinate (make it unknown to solve for).

        Args:
            coord: Coordinate name ('x', 'y', or 'z')
        """
        if coord not in ('x', 'y', 'z'):
            raise ValueError(f"Invalid coordinate '{coord}', must be 'x', 'y', or 'z'")

        # Add to unknowns
        self._unknowns[coord] = coord

        # Set coordinate to 0 (placeholder)
        idx = {'x': 0, 'y': 1, 'z': 2}[coord]
        self._coords[idx] = 0.0

    def to_cartesian(self) -> _Point:
        """Convert to Cartesian _Point."""
        return self

    def to_unit(self, unit: Unit | str) -> _PointWithUnknowns:
        """
        Convert to different display unit.

        Args:
            unit: Target unit for display

        Returns:
            New _PointWithUnknowns with coordinates in target unit
        """
        if isinstance(unit, str):
            from ..core.unit import ureg

            resolved = ureg.resolve(unit, dim=self._dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # Get coordinates in new unit
        coords = self.to_array()

        # Create new point with converted values
        result = _PointWithUnknowns(
            x=coords[0],
            y=coords[1],
            z=coords[2],
            unit=unit,
            unknowns=self._unknowns.copy(),
            name=self._name
        )
        return result

    def __str__(self) -> str:
        """String representation."""
        coords = self.to_array()
        unit_str = f" {self._unit.symbol}" if self._unit else ""

        # Format coordinates, showing '...' for unknowns
        x_str = "..." if "x" in self._unknowns else f"{coords[0]:.6g}"
        y_str = "..." if "y" in self._unknowns else f"{coords[1]:.6g}"
        z_str = "..." if "z" in self._unknowns else f"{coords[2]:.6g}"

        return f"_Point({x_str}, {y_str}, {z_str}{unit_str})"


def create_point_cartesian(
    x: float | EllipsisType = 0.0,
    y: float | EllipsisType = 0.0,
    z: float | EllipsisType = 0.0,
    unit: Unit | str | None = None,
    name: str | None = None,
) -> _Point | _PointWithUnknowns:
    """
    Create a point using Cartesian coordinates.

    This factory function provides a convenient way to create _Point objects
    with explicit x, y, z coordinates. Unspecified coordinates default to zero.

    Use ellipsis (...) to mark coordinates as unknown for solving.

    Args:
        x: X coordinate (default 0.0), use ... for unknown
        y: Y coordinate (default 0.0), use ... for unknown
        z: Z coordinate (default 0.0), use ... for unknown
        unit: Length unit for coordinates
        name: Optional point name

    Returns:
        _Point or _PointWithUnknowns object with the specified coordinates

    Examples:
        >>> from qnty.spatial import create_point_cartesian
        >>>
        >>> # Point with all coordinates
        >>> A = create_point_cartesian(x=2, y=-3, z=6, unit="m")
        >>>
        >>> # Point with default z=0
        >>> B = create_point_cartesian(x=5, y=10, unit="ft")
        >>>
        >>> # Point with unknown z coordinate
        >>> C = create_point_cartesian(x=4, y=2, z=..., unit="m")
    """
    # Resolve unit if string
    if isinstance(unit, str):
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.length)
        if resolved is None:
            raise ValueError(f"Unknown length unit '{unit}'")
        unit = resolved

    # Track unknowns
    unknowns: dict[str, str] = {}

    # Handle ellipsis for unknown coordinates
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0

    if x is ...:
        unknowns["x"] = "x"
    else:
        x_val = float(x)

    if y is ...:
        unknowns["y"] = "y"
    else:
        y_val = float(y)

    if z is ...:
        unknowns["z"] = "z"
    else:
        z_val = float(z)

    # If there are unknowns, return _PointWithUnknowns
    if unknowns:
        return _PointWithUnknowns(x_val, y_val, z_val, unit=unit, unknowns=unknowns, name=name)

    # Otherwise return simple _Point
    return _Point(x_val, y_val, z_val, unit=unit)


def create_point_from_ratio(
    dist: float,
    x: float,
    y: float,
    z: float = 0.0,
    ratio_component: str = "hyp",
    unit: Unit | str | None = None,
) -> _Point:
    """
    Create a point using distance and direction ratios.

    This factory function provides a convenient way to define points using direction
    ratios, which are common in statics problems where directions are given
    as integer ratios (like 3-4-5, 5-12-13, 8-15-17 right triangles).

    The ratios define the relative proportions in each direction. The point
    is placed at the specified distance along that direction.

    Args:
        dist: Distance value corresponding to the ratio_component
        x: X direction ratio (positive or negative)
        y: Y direction ratio (positive or negative)
        z: Z direction ratio (positive or negative)
        ratio_component: Which component dist corresponds to:
            - "hyp": dist is the total distance (hypotenuse/magnitude)
            - "x": dist corresponds to the x ratio
            - "y": dist corresponds to the y ratio
            - "z": dist corresponds to the z ratio
        unit: Length unit for distance

    Returns:
        _Point object with computed coordinates

    Raises:
        ValueError: If ratio_component is invalid or ratios are all zero

    Examples:
        >>> from qnty.spatial import create_point_from_ratio
        >>>
        >>> # Point where 2.5ft corresponds to x-ratio of -5, with z-ratio of 12
        >>> A = create_point_from_ratio(
        ...     dist=2.5, ratio_component="x",
        ...     x=-5, y=0, z=12, unit="ft"
        ... )
        >>> # Coordinates: (-2.5, 0, 6) ft
        >>>
        >>> # Point at total distance 13m with ratios 5-12
        >>> B = create_point_from_ratio(
        ...     dist=13, ratio_component="hyp",
        ...     x=5, y=0, z=12, unit="m"
        ... )
        >>> # Coordinates: (5, 0, 12) m
    """
    import math

    # Validate ratio_component
    valid_components = {"hyp", "x", "y", "z"}
    ratio_component_lower = ratio_component.lower()
    if ratio_component_lower not in valid_components:
        raise ValueError(f"Invalid ratio_component '{ratio_component}'. Must be one of: {valid_components}")

    # Validate ratios aren't all zero
    if x == 0 and y == 0 and z == 0:
        raise ValueError("Direction ratios cannot all be zero")

    # Resolve unit
    resolved_unit: Unit | None = None
    if isinstance(unit, str):
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.length)
        if resolved is None:
            raise ValueError(f"Unknown length unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian coordinates
    rx, ry, rz = float(x), float(y), float(z)
    dist_val = float(dist)

    # Compute the magnitude of the ratio vector
    ratio_magnitude = math.sqrt(rx**2 + ry**2 + rz**2)

    # Determine the scale factor based on which component dist corresponds to
    if ratio_component_lower == "hyp":
        scale = dist_val / ratio_magnitude
    elif ratio_component_lower == "x":
        if rx == 0:
            raise ValueError("Cannot use ratio_component='x' when x ratio is 0")
        scale = dist_val / abs(rx)
    elif ratio_component_lower == "y":
        if ry == 0:
            raise ValueError("Cannot use ratio_component='y' when y ratio is 0")
        scale = dist_val / abs(ry)
    else:  # z
        if rz == 0:
            raise ValueError("Cannot use ratio_component='z' when z ratio is 0")
        scale = dist_val / abs(rz)

    # Scale the ratios to get coordinates
    x_coord = rx * scale
    y_coord = ry * scale
    z_coord = rz * scale

    return _Point(x_coord, y_coord, z_coord, unit=resolved_unit)


def create_point_polar(
    dist: float,
    angle: float,
    plane: str = "xy",
    wrt: str = "+x",
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
) -> _Point:
    """
    Create a point using polar coordinates in a plane.

    This factory function provides a convenient way to define points using polar
    coordinates within a specific plane (xy, xz, or yz).

    Args:
        dist: Distance from origin
        angle: Angle measured from reference axis (CCW positive)
        plane: Plane containing the point ("xy", "xz", "yz")
        wrt: Reference axis for angle ("+x", "-x", "+y", "-y", "+z", "-z")
        unit: Length unit for distance
        angle_unit: Angle unit ("degree" or "radian")

    Returns:
        _Point object with computed coordinates

    Raises:
        ValueError: If plane or wrt is invalid

    Examples:
        >>> from qnty.spatial import create_point_polar
        >>>
        >>> # Point at 150mm, 30° from -x axis in xy plane
        >>> A = create_point_polar(dist=150, angle=30, plane="xy", wrt="-x", unit="mm")
        >>>
        >>> # Point at 5ft, 30° from +x axis in xy plane
        >>> B = create_point_polar(dist=5, angle=30, plane="xy", wrt="+x", unit="ft")
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
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.length)
        if resolved is None:
            raise ValueError(f"Unknown length unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian coordinates
    dist_val = float(dist)

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

    # Compute coordinates based on plane
    if plane_lower == "xy":
        x = dist_val * math.cos(total_angle_rad)
        y = dist_val * math.sin(total_angle_rad)
        z = 0.0
    elif plane_lower == "xz":
        x = dist_val * math.cos(total_angle_rad)
        y = 0.0
        z = dist_val * math.sin(total_angle_rad)
    else:  # yz
        x = 0.0
        y = dist_val * math.cos(total_angle_rad)
        z = dist_val * math.sin(total_angle_rad)

    return _Point(x, y, z, unit=resolved_unit)


def create_point_spherical(
    r: float,
    theta: float = 0.0,
    phi: float = 0.0,
    theta_wrt: str = "+x",
    phi_wrt: str = "+z",
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
) -> _Point:
    """
    Create a point using spherical coordinates.

    This factory function provides a convenient way to define points using:
    - dist: Distance from origin
    - theta: Transverse angle in xy-plane (CCW from theta_wrt axis)
    - phi: Azimuth angle from z-axis (CW from phi_wrt toward xy-plane)

    Args:
        dist: Distance from origin
        theta: Transverse angle in xy-plane (CCW from theta_wrt axis)
        phi: Azimuth angle (CW from phi_wrt axis, toward xy-plane)
        theta_wrt: Reference axis for theta ("+x", "-x", "+y", "-y")
        phi_wrt: Reference for phi ("+z", "-z", "xy")
            - "+z": angle measured from +z axis toward xy-plane
            - "-z": angle measured from -z axis toward xy-plane
            - "xy": angle measured from xy-plane (+phi toward +z, -phi toward -z)
        unit: Length unit for distance
        angle_unit: Angle unit ("degree" or "radian")

    Returns:
        _Point object with computed coordinates

    Raises:
        ValueError: If theta_wrt or phi_wrt is invalid

    Examples:
        >>> from qnty.spatial import create_point_spherical
        >>>
        >>> # Point at 10m, theta=30° from +x in xy-plane, phi=60° from +z
        >>> A = create_point_spherical(dist=10, theta=30, phi=60, unit="m")
        >>>
        >>> # With custom reference axes
        >>> B = create_point_spherical(dist=5, theta=45, phi=30, theta_wrt="+y", phi_wrt="-z", unit="ft")
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
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        resolved = ureg.resolve(unit, dim=dim.length)
        if resolved is None:
            raise ValueError(f"Unknown length unit '{unit}'")
        resolved_unit = resolved
    else:
        resolved_unit = unit

    # Compute Cartesian coordinates
    dist_val = float(r)
    x = dist_val * math.sin(phi_rad) * math.cos(theta_rad)
    y = dist_val * math.sin(phi_rad) * math.sin(theta_rad)
    z = dist_val * math.cos(phi_rad)

    return _Point(x, y, z, unit=resolved_unit)
