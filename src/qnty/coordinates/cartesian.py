"""
Cartesian coordinate system - standard orthogonal (x, y) with 90° separation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..core.quantity import Q, Quantity
from .coordinate_system import CoordinateSystem


@dataclass
class Cartesian(CoordinateSystem):
    """
    Standard orthogonal Cartesian coordinate system with 90° separation.

    The axes are always perpendicular (90° apart). Only the labels can be customized.

    Attributes:
        axis1_label: Label for first axis (default "x")
        axis2_label: Label for second axis (default "y")
    """

    axis1_label: str = "x"
    axis2_label: str = "y"
    axis1_angle: Quantity = field(default_factory=lambda: Q(0.0, "degree"))
    axis2_angle: Quantity = field(default_factory=lambda: Q(90.0, "degree"))

    def __repr__(self) -> str:
        return f"Cartesian({self.axis1_label}, {self.axis2_label})"
