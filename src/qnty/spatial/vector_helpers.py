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


# Global helper instance for convenience
vector_helper = VectorUpdateHelper()
