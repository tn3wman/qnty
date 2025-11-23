"""
Plane class for 3D spatial calculations.

Provides Plane object and factory functions for creating planes
oriented around coordinate axes.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.unit import Unit


class Plane:
    """
    A plane in 3D space defined by a point and a normal vector.

    The plane equation is: n · (r - p) = 0
    where n is the normal vector, r is any point on the plane, and p is a reference point.

    Attributes:
        normal: Unit normal vector (numpy array of shape (3,))
        point: A point on the plane (numpy array of shape (3,), in SI units)
        unit: Optional unit for the point coordinates
        name: Optional name for the plane
    """

    __slots__ = ("_normal", "_point", "_unit", "name")

    def __init__(
        self,
        normal: np.ndarray,
        point: np.ndarray | None = None,
        unit: Unit | None = None,
        name: str | None = None,
    ):
        """
        Initialize a plane with a normal vector and optional point.

        Args:
            normal: Normal vector (will be normalized)
            point: A point on the plane (default: origin)
            unit: Unit for point coordinates
            name: Optional plane name
        """
        # Normalize the normal vector
        normal = np.asarray(normal, dtype=float)
        mag = np.linalg.norm(normal)
        if mag == 0:
            raise ValueError("Normal vector cannot be zero")
        self._normal = normal / mag

        # Default point is origin
        if point is None:
            self._point = np.zeros(3)
        else:
            self._point = np.asarray(point, dtype=float)

        self._unit = unit
        self.name = name

    @property
    def normal(self) -> np.ndarray:
        """Unit normal vector of the plane."""
        return self._normal

    @property
    def point(self) -> np.ndarray:
        """A point on the plane (in SI units)."""
        return self._point

    @property
    def unit(self) -> Unit | None:
        """Unit for point coordinates."""
        return self._unit

    def distance_to_point(self, point: np.ndarray) -> float:
        """
        Calculate signed distance from a point to the plane.

        Positive distance means the point is on the side of the normal.

        Args:
            point: Point coordinates (in same units as plane)

        Returns:
            Signed distance to the plane
        """
        point = np.asarray(point, dtype=float)
        return np.dot(self._normal, point - self._point)

    def project_point(self, point: np.ndarray) -> np.ndarray:
        """
        Project a point onto the plane.

        Args:
            point: Point coordinates

        Returns:
            Projected point on the plane
        """
        point = np.asarray(point, dtype=float)
        dist = self.distance_to_point(point)
        return point - dist * self._normal

    def contains_point(self, point: np.ndarray, tol: float = 1e-9) -> bool:
        """
        Check if a point lies on the plane.

        Args:
            point: Point coordinates
            tol: Tolerance for distance check

        Returns:
            True if point is on the plane
        """
        return abs(self.distance_to_point(point)) < tol

    def __str__(self) -> str:
        """String representation."""
        name_str = f"'{self.name}' " if self.name else ""
        unit_str = f" {self._unit.symbol}" if self._unit else ""
        n = self._normal
        p = self._point
        return f"Plane({name_str}normal=[{n[0]:.4g}, {n[1]:.4g}, {n[2]:.4g}], point=[{p[0]:.4g}, {p[1]:.4g}, {p[2]:.4g}]{unit_str})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()


def create_plane_rotated_x(
    angle: float,
    point: tuple[float, float, float] | np.ndarray | None = None,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
) -> Plane:
    """
    Create a plane rotated around the x-axis by a given angle.

    The plane starts as the xy-plane (normal = +z) and rotates around
    the x-axis. Positive angles rotate the normal from +z toward +y.

    Args:
        angle: Rotation angle around x-axis
        point: A point on the plane (default: origin)
        unit: Unit for point coordinates
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional plane name

    Returns:
        Plane object with rotated normal

    Examples:
        >>> from qnty.spatial import create_plane_rotated_x
        >>>
        >>> # Plane rotated 45° around x-axis
        >>> p = create_plane_rotated_x(angle=45, name="inclined")
        >>>
        >>> # Plane rotated 90° (becomes xz-plane with normal +y)
        >>> p2 = create_plane_rotated_x(angle=90)
    """
    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Rotation around x-axis
    # Starting normal: [0, 0, 1] (z-axis)
    # After rotation: normal_y = sin(angle), normal_z = cos(angle)
    normal = np.array([0.0, math.sin(angle_rad), math.cos(angle_rad)])

    # Resolve unit
    resolved_unit = _resolve_unit(unit)

    # Convert point to numpy array
    point_arr = _convert_point(point, resolved_unit)

    return Plane(normal, point_arr, resolved_unit, name)


def create_plane_rotated_y(
    angle: float,
    point: tuple[float, float, float] | np.ndarray | None = None,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
    start_plane: str = "xy",
) -> Plane:
    """
    Create a plane rotated around the y-axis by a given angle.

    Args:
        angle: Rotation angle around y-axis
        point: A point on the plane (default: origin)
        unit: Unit for point coordinates
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional plane name
        start_plane: Starting plane orientation:
            - "xy": starts with normal = +z, rotates toward -x (default)
            - "zy": starts with normal = +x, rotates toward +z

    Returns:
        Plane object with rotated normal

    Examples:
        >>> from qnty.spatial import create_plane_rotated_y
        >>>
        >>> # xy-plane rotated 30° around y-axis (normal goes from +z toward -x)
        >>> p = create_plane_rotated_y(angle=30, name="slope")
        >>>
        >>> # zy-plane rotated -30° around y-axis (normal goes from +x toward +z)
        >>> p2 = create_plane_rotated_y(angle=-30, start_plane="zy")
    """
    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Rotation around y-axis
    if start_plane.lower() == "xy":
        # Starting normal: [0, 0, 1] (z-axis)
        # After rotation: normal_x = -sin(angle), normal_z = cos(angle)
        normal = np.array([-math.sin(angle_rad), 0.0, math.cos(angle_rad)])
    elif start_plane.lower() == "zy":
        # Starting normal: [1, 0, 0] (x-axis)
        # After rotation: normal_x = cos(angle), normal_z = -sin(angle)
        # Positive angle rotates normal from +x toward -z (consistent with right-hand rule)
        normal = np.array([math.cos(angle_rad), 0.0, -math.sin(angle_rad)])
    else:
        raise ValueError(f"Invalid start_plane '{start_plane}'. Must be 'xy' or 'zy'")

    # Resolve unit
    resolved_unit = _resolve_unit(unit)

    # Convert point to numpy array
    point_arr = _convert_point(point, resolved_unit)

    return Plane(normal, point_arr, resolved_unit, name)


def create_plane_rotated_z(
    angle: float,
    point: tuple[float, float, float] | np.ndarray | None = None,
    unit: Unit | str | None = None,
    angle_unit: str = "degree",
    name: str | None = None,
) -> Plane:
    """
    Create a plane rotated around the z-axis by a given angle.

    The plane starts as the xz-plane (normal = +y) and rotates around
    the z-axis. Positive angles rotate the normal from +y toward -x.

    Args:
        angle: Rotation angle around z-axis
        point: A point on the plane (default: origin)
        unit: Unit for point coordinates
        angle_unit: Angle unit ("degree" or "radian")
        name: Optional plane name

    Returns:
        Plane object with rotated normal

    Examples:
        >>> from qnty.spatial import create_plane_rotated_z
        >>>
        >>> # Plane rotated 60° around z-axis
        >>> p = create_plane_rotated_z(angle=60, name="angled")
        >>>
        >>> # Plane rotated 90° (becomes yz-plane with normal -x)
        >>> p2 = create_plane_rotated_z(angle=90)
    """
    # Convert angle to radians
    if angle_unit.lower() in ("degree", "degrees", "deg"):
        angle_rad = math.radians(float(angle))
    elif angle_unit.lower() in ("radian", "radians", "rad"):
        angle_rad = float(angle)
    else:
        raise ValueError(f"Invalid angle_unit '{angle_unit}'. Use 'degree' or 'radian'")

    # Rotation around z-axis
    # Starting normal: [0, 1, 0] (y-axis)
    # After rotation: normal_x = -sin(angle), normal_y = cos(angle)
    normal = np.array([-math.sin(angle_rad), math.cos(angle_rad), 0.0])

    # Resolve unit
    resolved_unit = _resolve_unit(unit)

    # Convert point to numpy array
    point_arr = _convert_point(point, resolved_unit)

    return Plane(normal, point_arr, resolved_unit, name)


def _resolve_unit(unit: Unit | str | None) -> Unit | None:
    """Resolve unit string to Unit object."""
    if isinstance(unit, str):
        from ..core.unit import ureg

        resolved = ureg.resolve(unit)
        if resolved is None:
            raise ValueError(f"Unknown unit '{unit}'")
        return resolved
    return unit


def _convert_point(
    point: tuple[float, float, float] | np.ndarray | None,
    unit: Unit | None,
) -> np.ndarray:
    """Convert point to numpy array in SI units."""
    if point is None:
        return np.zeros(3)

    point_arr = np.asarray(point, dtype=float)

    # Convert to SI if unit provided
    if unit is not None:
        point_arr = point_arr * unit.si_factor

    return point_arr
