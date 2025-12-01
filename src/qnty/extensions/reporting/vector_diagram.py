"""
Vector diagram visualization for statics problems.

Generates properly scaled and labeled vector diagrams for force vectors,
including angles, components, and resultants. Diagrams can be saved as
images for inclusion in PDF reports.
"""

from __future__ import annotations

import math
from typing import Any

from matplotlib.patches import Arc

from ...utils.shared_utilities import create_angle_arc
from ..diagram_utils import (
    VectorDiagramBase,
    format_vector_label,
    make_create_force_diagram,
)


class VectorDiagram(VectorDiagramBase):
    """
    Generate scaled vector diagrams for statics problems (reporting version).

    This version includes overlap detection for angle labels to produce
    cleaner diagrams suitable for PDF reports. It also uses magnitude bars
    in vector labels (e.g., |F_1| = 450 N).

    Creates professional-quality diagrams with:
    - Scaled vector arrows
    - Coordinate axes
    - Angle annotations with overlap detection
    - Force labels with magnitude bars
    - Optional component projections
    - Grid (optional)

    Examples:
        >>> diagram = VectorDiagram(title="Cable Forces")
        >>> diagram.add_vector(F1, color='red', label='F₁')
        >>> diagram.add_vector(F2, color='blue', label='F₂')
        >>> diagram.add_resultant(FR, color='green', label='FR')
        >>> diagram.save("diagram.png")
    """

    def __init__(self, *args, **kwargs):
        """Initialize with angle label overlap tracking."""
        super().__init__(*args, **kwargs)
        self.angle_label_positions: list[tuple[float, float, float, float]] = []  # (x, y, width, height)

    def _pre_save_hook(self) -> None:
        """Reset angle label tracking for this diagram."""
        self.angle_label_positions = []

    def _format_vector_label(self, force: Any, label: str) -> str:
        """Format vector label with magnitude bars (|F_1| = 450 N)."""
        return format_vector_label(force, label, include_magnitude_bars=True)

    def _check_label_overlap(self, x: float, y: float, width: float = 1.5, height: float = 0.5) -> bool:
        """
        Check if a label at position (x, y) would overlap with existing labels.

        Args:
            x: X position of label center
            y: Y position of label center
            width: Approximate label width
            height: Approximate label height

        Returns:
            True if overlap detected, False otherwise
        """
        # Check against all existing label positions
        for ex, ey, ew, eh in self.angle_label_positions:
            # Simple bounding box overlap check
            if abs(x - ex) < (width + ew) / 2 and abs(y - ey) < (height + eh) / 2:
                return True
        return False

    def _find_non_overlapping_position(self, angle_deg: float, base_radius: float, max_attempts: int = 8) -> tuple[float, float, float]:
        """
        Find a non-overlapping position for angle label.

        Tries different strategies:
        1. Different positions along the arc (midpoint, 1/3, 2/3, etc.)
        2. Different radii (closer or farther from origin)

        Args:
            angle_deg: Angle in degrees
            base_radius: Base radius to start with
            max_attempts: Maximum position attempts

        Returns:
            Tuple of (label_x, label_y, final_radius)
        """
        # Define candidate positions to try
        # Format: (arc_fraction, radius_multiplier)
        candidates = [
            (0.5, 1.2),  # Midpoint, normal distance (default)
            (0.33, 1.2),  # Earlier on arc
            (0.67, 1.2),  # Later on arc
            (0.5, 1.6),  # Midpoint, farther out
            (0.5, 0.9),  # Midpoint, closer in
            (0.25, 1.4),  # Very early, bit farther
            (0.75, 1.4),  # Very late, bit farther
            (0.4, 1.8),  # Fallback: far out
        ]

        for arc_frac, radius_mult in candidates[:max_attempts]:
            # Calculate position
            label_angle_deg = angle_deg * arc_frac

            label_angle_rad = math.radians(label_angle_deg)
            test_radius = base_radius * radius_mult
            label_x = test_radius * math.cos(label_angle_rad)
            label_y = test_radius * math.sin(label_angle_rad)

            # Check for overlap
            if not self._check_label_overlap(label_x, label_y):
                return label_x, label_y, test_radius

        # If all positions overlap, return the farthest one as last resort
        final_radius = base_radius * 2.0
        label_angle_rad = math.radians(angle_deg * 0.5)
        label_x = final_radius * math.cos(label_angle_rad)
        label_y = final_radius * math.sin(label_angle_rad)
        return label_x, label_y, final_radius

    def _draw_angle_annotation(self, ax, angle: float, radius: float, color: str, label: str = "") -> None:
        """Draw angle arc and label with theta notation, avoiding overlaps."""
        # Convert angle to degrees
        angle_deg = math.degrees(angle)

        # Ensure angle is positive and within [0, 360)
        while angle_deg < 0:
            angle_deg += 360
        while angle_deg >= 360:
            angle_deg -= 360

        # Draw arc from x-axis to vector
        arc = create_angle_arc(Arc, radius, angle_deg, color)
        ax.add_patch(arc)

        # Find non-overlapping position for label
        label_x, label_y, _ = self._find_non_overlapping_position(angle_deg, radius)

        # Format angle label with theta notation if label is provided
        if label:
            # Format label with subscript (e.g., F_1 becomes \theta_{F_1})
            if "_" in label:
                parts = label.split("_", 1)
                if len(parts) == 2:
                    base, subscript = parts
                    theta_label = f"$\\theta_{{{base}_{{{subscript}}}}}$ = {angle_deg:.1f}°"
                else:
                    theta_label = f"$\\theta_{{{label}}}$ = {angle_deg:.1f}°"
            else:
                theta_label = f"$\\theta_{{{label}}}$ = {angle_deg:.1f}°"
        else:
            # Fallback to just the angle
            theta_label = f"{angle_deg:.1f}°"

        # Estimate label size (approximate)
        label_width = 1.5 if label else 0.8
        label_height = 0.5

        # Add label
        ax.text(label_x, label_y, theta_label, fontsize=10, color=color, ha="center", va="center", bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7})

        # Record this label's position to avoid future overlaps
        self.angle_label_positions.append((label_x, label_y, label_width, label_height))


# Create module-specific create_force_diagram using the factory
create_force_diagram = make_create_force_diagram(VectorDiagram)
