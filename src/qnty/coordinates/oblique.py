"""
Oblique coordinate system - non-orthogonal axes at arbitrary angles.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core.quantity import Q, Quantity
from .coordinate_system import CoordinateSystem


@dataclass
class Oblique(CoordinateSystem):
    """
    Non-orthogonal (oblique) coordinate system where axes are not perpendicular.

    Useful for problems where geometry fits naturally into a skewed system,
    such as forces along non-perpendicular directions.

    Attributes:
        axis1_label: Label for first axis (e.g., "u")
        axis2_label: Label for second axis (e.g., "v")
        axis1_angle: Angle of first axis from positive x-axis as Quantity
        axis2_angle: Angle of second axis from positive x-axis as Quantity
    """

    @classmethod
    def from_angle_between(
        cls,
        axis1_label: str,
        axis2_label: str,
        axis1_angle: float,
        angle_between: float,
        angle_unit: str = "degree",
    ) -> Oblique:
        """
        Create an oblique coordinate system by specifying the angle between axes.

        Args:
            axis1_label: Label for first axis
            axis2_label: Label for second axis
            axis1_angle: Angle of first axis from positive x-axis
            angle_between: Angle between the two axes (counterclockwise from axis1 to axis2)
            angle_unit: Unit for angles (default "degree")

        Returns:
            Oblique coordinate system instance
        """
        axis1_qty = Q(axis1_angle, angle_unit)
        angle_between_qty = Q(angle_between, angle_unit)
        axis2_qty = axis1_qty + angle_between_qty

        return cls(
            axis1_label=axis1_label,
            axis2_label=axis2_label,
            axis1_angle=axis1_qty,
            axis2_angle=axis2_qty,
        )

    def __repr__(self) -> str:
        return f"Oblique({self.axis1_label}, {self.axis2_label})"
