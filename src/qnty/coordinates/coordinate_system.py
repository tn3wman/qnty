"""
Base CoordinateSystem class for 2D coordinate systems.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core.quantity import Q, Quantity


@dataclass
class CoordinateSystem:
    """
    Base class for 2D coordinate systems.

    All angles are stored as Quantity objects for dimensional safety.

    Attributes:
        axis1_label: Label for first axis (e.g., "x", "u")
        axis2_label: Label for second axis (e.g., "y", "v")
        axis1_angle: Angle of first axis from positive x-axis as Quantity
        axis2_angle: Angle of second axis from positive x-axis as Quantity
    """

    axis1_label: str
    axis2_label: str
    axis1_angle: Quantity
    axis2_angle: Quantity

    @property
    def angle_between(self) -> Quantity:
        """Angle between the two axes as a Quantity."""
        return self.axis2_angle - self.axis1_angle

    def get_axis_angle(self, axis: str) -> Quantity:
        """
        Get the angle of an axis by its label.

        Args:
            axis: Axis label with optional sign prefix ("+x", "-x", "u", "-v")

        Returns:
            Angle as Quantity from positive x-axis

        Raises:
            ValueError: If axis label not found
        """
        sign = 1
        axis_label = axis
        if axis.startswith("+"):
            axis_label = axis[1:]
        elif axis.startswith("-"):
            axis_label = axis[1:]
            sign = -1

        if axis_label == self.axis1_label:
            base_angle = self.axis1_angle
        elif axis_label == self.axis2_label:
            base_angle = self.axis2_angle
        else:
            raise ValueError(
                f"Unknown axis '{axis}' in coordinate system with axes '{self.axis1_label}', '{self.axis2_label}'"
            )

        if sign == -1:
            return base_angle + Q(180.0, "degree")
        return base_angle

    def __repr__(self) -> str:
        return f"CoordinateSystem({self.axis1_label}, {self.axis2_label})"
