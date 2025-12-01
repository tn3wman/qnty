"""
Vector helper utilities for force and angle quantity creation.

This module provides helper functions for creating force and angle quantities,
and for updating vector properties. These utilities are shared across
solver classes to reduce code duplication.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

    from ..core.dimension import Dimension
    from ..core.quantity import Quantity
    from ..core.unit import Unit
    from .vector import _Vector


class VectorUpdateHelper:
    """
    Helper class for updating vector properties with less boilerplate.

    This class provides convenient methods for creating force and angle
    quantities, and for updating vector coordinates and polar properties.
    Uses lazy-loaded imports to avoid circular dependencies.

    Examples:
        >>> helper = VectorUpdateHelper()
        >>> force_qty = helper.create_force_quantity("F_x", 100.0, unit)
        >>> angle_qty = helper.create_angle_quantity("theta", 0.785)  # 45 degrees in radians
        >>> helper.update_force_from_polar(force_vector, 100.0, 0.785, unit)
    """

    def __init__(self):
        """Initialize with lazy-loaded references to avoid circular imports."""
        self._dim = None
        self._ureg = None
        self._degree_unit = None

    @property
    def dim(self):
        """Lazily load dimension catalog."""
        if self._dim is None:
            from ..core.dimension_catalog import dim
            self._dim = dim
        return self._dim

    @property
    def ureg(self):
        """Lazily load unit registry."""
        if self._ureg is None:
            from ..core.unit import ureg
            self._ureg = ureg
        return self._ureg

    @property
    def degree_unit(self):
        """Lazily resolve degree unit."""
        if self._degree_unit is None:
            self._degree_unit = self.ureg.resolve("degree", dim=self.dim.D)
        return self._degree_unit

    def create_force_quantity(self, name: str, value: float, unit: Unit | None = None) -> Quantity:
        """
        Create a force Quantity with the given value in SI units.

        Args:
            name: Name for the quantity
            value: Value in SI units (Newtons)
            unit: Preferred display unit (optional)

        Returns:
            Quantity with force dimension
        """
        from ..core.quantity import Quantity
        return Quantity(name=name, dim=self.dim.force, value=value, preferred=unit)

    def create_angle_quantity(self, name: str, value: float) -> Quantity:
        """
        Create an angle Quantity with the given value in radians.

        Args:
            name: Name for the quantity
            value: Value in radians

        Returns:
            Quantity with angle dimension, displayed in degrees
        """
        from ..core.quantity import Quantity
        return Quantity(name=name, dim=self.dim.D, value=value, preferred=self.degree_unit)

    def update_force_coords(self, force: _Vector, x: float, y: float, z: float = 0.0, unit: Unit | None = None) -> None:
        """
        Update force coordinates from x, y, z values in SI units.

        Args:
            force: Vector to update
            x: X component in SI units
            y: Y component in SI units
            z: Z component in SI units (default 0)
            unit: Preferred display unit
        """
        from .vector import _Vector

        x_qty = self.create_force_quantity(f"{force.name}_x", x, unit)
        y_qty = self.create_force_quantity(f"{force.name}_y", y, unit)
        z_qty = self.create_force_quantity(f"{force.name}_z", z, unit)
        force._coords = _Vector.from_quantities(x_qty, y_qty, z_qty)._coords

    def update_force_from_polar(self, force: _Vector, magnitude: float, angle: float, unit: Unit | None = None) -> None:
        """
        Update force from magnitude and angle (radians), computing coordinates.

        Args:
            force: Vector to update
            magnitude: Magnitude in SI units
            angle: Angle in radians from +x axis
            unit: Preferred display unit
        """
        x = magnitude * math.cos(angle)
        y = magnitude * math.sin(angle)
        self.update_force_coords(force, x, y, 0.0, unit)
        force._magnitude = self.create_force_quantity(f"{force.name}_magnitude", magnitude, unit)
        force._angle = self.create_angle_quantity(f"{force.name}_angle", angle)
        force.is_known = True

    def set_force_magnitude(self, force: _Vector, value: float, unit: Unit | None = None) -> None:
        """
        Set force magnitude.

        Args:
            force: Vector to update
            value: Magnitude in SI units
            unit: Preferred display unit
        """
        force._magnitude = self.create_force_quantity(f"{force.name}_magnitude", value, unit)

    def set_force_angle(self, force: _Vector, value: float) -> None:
        """
        Set force angle in radians.

        Args:
            force: Vector to update
            value: Angle in radians
        """
        force._angle = self.create_angle_quantity(f"{force.name}_angle", value)


def compute_missing_direction_angle(
    alpha_rad: float | None,
    beta_rad: float | None,
    gamma_rad: float | None,
) -> tuple[float, float, float]:
    """
    Compute the missing direction angle from the constraint cos²α + cos²β + cos²γ = 1.

    Given at least 2 of the 3 coordinate direction angles, calculates the missing one.
    All angles are in radians.

    Args:
        alpha_rad: Angle from +x axis in radians (or None if unknown)
        beta_rad: Angle from +y axis in radians (or None if unknown)
        gamma_rad: Angle from +z axis in radians (or None if unknown)

    Returns:
        Tuple of (alpha_rad, beta_rad, gamma_rad) with all values computed

    Raises:
        ValueError: If angles don't satisfy the constraint or fewer than 2 provided
    """
    if alpha_rad is None and beta_rad is not None and gamma_rad is not None:
        cos_alpha_sq = 1 - math.cos(beta_rad) ** 2 - math.cos(gamma_rad) ** 2
        if cos_alpha_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_alpha = math.sqrt(cos_alpha_sq)
        alpha_rad = math.acos(cos_alpha)
    elif beta_rad is None and alpha_rad is not None and gamma_rad is not None:
        cos_beta_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(gamma_rad) ** 2
        if cos_beta_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_beta = math.sqrt(cos_beta_sq)
        beta_rad = math.acos(cos_beta)
    elif gamma_rad is None and alpha_rad is not None and beta_rad is not None:
        cos_gamma_sq = 1 - math.cos(alpha_rad) ** 2 - math.cos(beta_rad) ** 2
        if cos_gamma_sq < 0:
            raise ValueError("Invalid angle combination: cos²α + cos²β + cos²γ > 1")
        cos_gamma = math.sqrt(cos_gamma_sq)
        gamma_rad = math.acos(cos_gamma)
    elif alpha_rad is None or beta_rad is None or gamma_rad is None:
        raise ValueError("Must provide at least 2 of the 3 coordinate direction angles")

    return alpha_rad, beta_rad, gamma_rad


def compute_direction_cosines(alpha_rad: float, beta_rad: float, gamma_rad: float) -> tuple[float, float, float]:
    """
    Compute direction cosines from coordinate direction angles.

    Args:
        alpha_rad: Angle from +x axis in radians
        beta_rad: Angle from +y axis in radians
        gamma_rad: Angle from +z axis in radians

    Returns:
        Tuple of (cos(alpha), cos(beta), cos(gamma))
    """
    return (math.cos(alpha_rad), math.cos(beta_rad), math.cos(gamma_rad))


def validate_direction_cosines(alpha_rad: float, beta_rad: float, gamma_rad: float, tolerance: float = 1e-6) -> None:
    """
    Validate that direction angles satisfy the constraint cos²α + cos²β + cos²γ = 1.

    Args:
        alpha_rad: Angle from +x axis in radians
        beta_rad: Angle from +y axis in radians
        gamma_rad: Angle from +z axis in radians
        tolerance: Allowed deviation from 1.0 (default 1e-6)

    Raises:
        ValueError: If angles don't satisfy the constraint within tolerance
    """
    sum_cos_sq = math.cos(alpha_rad) ** 2 + math.cos(beta_rad) ** 2 + math.cos(gamma_rad) ** 2
    if abs(sum_cos_sq - 1.0) > tolerance:
        raise ValueError(f"Direction angles must satisfy cos²α + cos²β + cos²γ = 1, got {sum_cos_sq}")


def init_coords_from_unit(
    x: float,
    y: float,
    z: float,
    unit: "Unit | None",
) -> tuple["NDArray", "Dimension | None", "Unit | None"]:
    """
    Initialize coordinate array and dimension/unit from input values.

    This is a shared utility for _Vector and _Point initialization that
    handles unit conversion to SI and dimension tracking.

    Args:
        x: X/U coordinate value in the specified unit
        y: Y/V coordinate value in the specified unit
        z: Z/W coordinate value in the specified unit
        unit: Unit for all coordinates (if None, assumes SI units)

    Returns:
        Tuple of (coords_array, dimension, unit) where:
        - coords_array: numpy array of coordinates in SI units
        - dimension: The dimension from the unit, or None if unitless
        - unit: The original unit, or None if unitless
    """
    import numpy as np

    if unit is None:
        return np.array([x, y, z], dtype=float), None, None

    si_values = unit.si_factor * np.array([x, y, z], dtype=float) + unit.si_offset
    return si_values, unit.dim, unit


# Global helper instance for convenience
vector_helper = VectorUpdateHelper()
