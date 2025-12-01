"""
Shared utilities for vector diagram generation.

This module provides common functions used by both plotting and reporting
vector diagram modules to avoid code duplication.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch

if TYPE_CHECKING:
    from typing import Protocol

    from ...spatial import _Vector

    class VectorDiagramProtocol(Protocol):
        """Protocol for VectorDiagram classes."""

        def add_vector(self, force: Any, color: str, label: str, show_angle: bool) -> None: ...
        def add_resultant(self, force: Any, color: str, label: str) -> None: ...
        def save(self, output_path: str | Path) -> Path: ...


def compute_vector_bounds(
    vectors: list[dict],
    resultant: dict | None,
    scale_factor: float,
) -> tuple[float, float, float, float]:
    """
    Compute the bounding box for all vectors in a diagram.

    Args:
        vectors: List of vector data dictionaries with 'magnitude' and 'angle' keys
        resultant: Optional resultant vector dictionary with same keys
        scale_factor: Scale factor to apply to magnitudes

    Returns:
        Tuple of (max_x, min_x, max_y, min_y) bounds
    """
    max_x, min_x, max_y, min_y = 0.0, 0.0, 0.0, 0.0

    for vec_data in vectors:
        mag = vec_data["magnitude"]
        angle = vec_data["angle"]
        scaled_mag = mag * scale_factor
        x = scaled_mag * np.cos(angle)
        y = scaled_mag * np.sin(angle)
        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)

    if resultant:
        mag = resultant["magnitude"]
        angle = resultant["angle"]
        scaled_mag = mag * scale_factor
        x = scaled_mag * np.cos(angle)
        y = scaled_mag * np.sin(angle)
        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)

    return max_x, min_x, max_y, min_y


# Color palette for force vectors
FORCE_COLORS = ["#E74C3C", "#3498DB", "#F39C12", "#9B59B6", "#1ABC9C", "#E67E22"]
RESULTANT_COLOR = "#27AE60"


def extract_force_data(force: Any) -> tuple[float, float] | None:
    """
    Extract magnitude and angle values from a force vector.

    Args:
        force: Force vector with is_known, magnitude, and angle attributes

    Returns:
        Tuple of (magnitude, angle_rad) or None if force is not fully known
    """
    if not force.is_known or force.magnitude is None or force.angle is None:
        return None

    mag = force.magnitude.value if force.magnitude.value else 0.0
    angle_rad = force.angle.value if force.angle.value else 0.0
    return mag, angle_rad


def build_vector_data(
    force: Any,
    color: str,
    label: str | None,
    linewidth: float,
    show_angle: bool = True,
) -> dict | None:
    """
    Build a vector data dictionary for diagram rendering.

    Args:
        force: Force vector object
        color: Arrow color
        label: Label for vector (uses force.name if None)
        linewidth: Arrow line width
        show_angle: Whether to show angle annotation

    Returns:
        Dictionary with force data or None if force is not fully known
    """
    extracted = extract_force_data(force)
    if extracted is None:
        return None

    mag, angle_rad = extracted
    return {"force": force, "magnitude": mag, "angle": angle_rad, "color": color, "label": label or force.name, "show_angle": show_angle, "linewidth": linewidth}


def build_resultant_data(
    force: Any,
    color: str,
    label: str | None,
    linewidth: float,
) -> dict | None:
    """
    Build a resultant data dictionary for diagram rendering.

    Args:
        force: Resultant force vector object
        color: Arrow color
        label: Label for resultant (uses force.name if None)
        linewidth: Arrow line width

    Returns:
        Dictionary with resultant data or None if force is not fully known
    """
    extracted = extract_force_data(force)
    if extracted is None:
        return None

    mag, angle_rad = extracted
    return {"force": force, "magnitude": mag, "angle": angle_rad, "color": color, "label": label or force.name, "linewidth": linewidth}


def draw_axes(ax: Any, xlim_min: float, xlim_max: float, ylim_min: float, ylim_max: float) -> None:
    """
    Draw coordinate axes spanning the entire plot.

    Args:
        ax: Matplotlib axes object
        xlim_min: Minimum x limit
        xlim_max: Maximum x limit
        ylim_min: Minimum y limit
        ylim_max: Maximum y limit
    """
    # Origin marker
    ax.plot(0, 0, "ko", markersize=8, zorder=5)

    # X-axis spanning entire width
    ax.annotate("", xy=(xlim_max * 0.95, 0), xytext=(xlim_min * 0.95, 0), arrowprops={"arrowstyle": "->", "lw": 2, "color": "black"}, zorder=1)

    # Y-axis spanning entire height
    ax.annotate("", xy=(0, ylim_max * 0.95), xytext=(0, ylim_min * 0.95), arrowprops={"arrowstyle": "->", "lw": 2, "color": "black"}, zorder=1)


def draw_components(ax: Any, x: float, y: float, color: str) -> None:
    """
    Draw component projections (dashed lines).

    Args:
        ax: Matplotlib axes object
        x: X coordinate of vector tip
        y: Y coordinate of vector tip
        color: Color for the component lines
    """
    # X-component (vertical dashed line from tip to x-axis)
    ax.plot([x, x], [0, y], color=color, linestyle=":", linewidth=1.5, alpha=0.6)

    # Y-component (horizontal dashed line from tip to y-axis)
    ax.plot([0, x], [y, y], color=color, linestyle=":", linewidth=1.5, alpha=0.6)

    # Labels for components
    ax.text(x, -0.3, f"{x:.1f}", fontsize=9, ha="center", color=color)
    ax.text(-0.3, y, f"{y:.1f}", fontsize=9, va="center", color=color)


def get_unit_string(vectors: list[dict], resultant: dict | None) -> str:
    """
    Get unit string from first vector or resultant.

    Args:
        vectors: List of vector data dictionaries
        resultant: Optional resultant dictionary

    Returns:
        Unit symbol string or empty string if no unit found
    """
    if vectors and len(vectors) > 0:
        force = vectors[0]["force"]
        if force.magnitude and force.magnitude.preferred:
            return force.magnitude.preferred.symbol
    if resultant:
        force = resultant["force"]
        if force.magnitude and force.magnitude.preferred:
            return force.magnitude.preferred.symbol
    return ""


def format_label_for_legend(label: str) -> str:
    """
    Format label for legend using LaTeX subscript notation.

    Converts underscores to subscripts: F_1 -> $F_{1}$

    Args:
        label: Label string

    Returns:
        LaTeX formatted label string
    """
    if "_" in label:
        parts = label.split("_", 1)
        if len(parts) == 2:
            base, subscript = parts
            return f"${base}_{{{subscript}}}$"
    return label


def format_vector_label(force: Any, label: str, include_magnitude_bars: bool = False) -> str:
    """
    Format vector label with LaTeX notation and magnitude.

    Args:
        force: Force vector object with magnitude attribute
        label: Label string for the vector
        include_magnitude_bars: If True, format as $|F_1|$ = 450 N, else as $F_1$ = 450 N

    Returns:
        Formatted string like "$F_1$ = 450 N" or "$|F_1|$ = 450 N"
    """
    # Format the force name with LaTeX subscripts
    if include_magnitude_bars:
        if "_" in label:
            parts = label.split("_", 1)
            if len(parts) == 2:
                base, subscript = parts
                latex_label = f"$|{base}_{{{subscript}}}|$"
            else:
                latex_label = f"$|{label}|$"
        else:
            latex_label = f"$|{label}|$"
    else:
        latex_label = format_label_for_legend(label)

    # Get magnitude and unit
    if force.magnitude and force.magnitude.value is not None:
        mag_value = force.magnitude.value
        if force.magnitude.preferred:
            mag_value = mag_value / force.magnitude.preferred.si_factor
            unit = force.magnitude.preferred.symbol
        else:
            unit = "N"

        return f"{latex_label} = {mag_value:.0f} {unit}"
    else:
        return latex_label


def populate_force_diagram(
    diagram: Any,
    problem: Any,
) -> None:
    """
    Populate a VectorDiagram with forces from a problem.

    This shared function adds all known forces and resultants from a problem
    to a VectorDiagram instance, using a consistent color palette.

    Args:
        diagram: VectorDiagram instance to populate
        problem: VectorEquilibriumProblem instance with forces attribute
    """
    color_idx = 0

    # Add known forces
    for name, force in problem.forces.items():
        if force.is_resultant:
            continue  # Handle resultants separately

        if force.is_known and force.magnitude and force.angle:
            diagram.add_vector(force, color=FORCE_COLORS[color_idx % len(FORCE_COLORS)], label=name, show_angle=True)
            color_idx += 1

    # Add resultant (if present)
    for name, force in problem.forces.items():
        if force.is_resultant and force.is_known:
            diagram.add_resultant(force, color=RESULTANT_COLOR, label=name)
            break


def create_force_diagram(problem: Any, output_path: str | Path, diagram_class: type, title: str | None = None, show_components: bool = False, **kwargs) -> Path:
    """
    Create vector diagram from a VectorEquilibriumProblem.

    This is a shared factory function used by both plotting and reporting modules.
    It creates a diagram using the specified diagram class, populates it with
    forces from the problem, and saves it.

    Args:
        problem: VectorEquilibriumProblem instance (must be solved)
        output_path: Output file path
        diagram_class: The VectorDiagram class to use (e.g., plotting.VectorDiagram or reporting.VectorDiagram)
        title: Diagram title (uses problem.name if None)
        show_components: Whether to show component projections
        **kwargs: Additional arguments for VectorDiagram

    Returns:
        Path to saved diagram

    Examples:
        >>> from qnty.extensions.plotting.vector_diagram import VectorDiagram
        >>> problem = Problem_2_1()
        >>> problem.solve()
        >>> create_force_diagram(problem, "diagram.png", VectorDiagram)
    """
    title = title or problem.name
    diagram = diagram_class(title=title, show_components=show_components, **kwargs)
    populate_force_diagram(diagram, problem)
    return diagram.save(output_path)


class VectorDiagramBase:
    """
    Base class for vector diagrams providing shared functionality.

    This class contains the common implementation for VectorDiagram classes
    in both plotting and reporting modules. Subclasses can override specific
    methods to customize behavior (e.g., angle annotation style, label formatting).
    """

    def __init__(self, title: str = "Vector Diagram", figsize: tuple[float, float] = (10, 10), show_grid: bool = True, show_components: bool = False, origin: tuple[float, float] = (0, 0)):
        """
        Initialize vector diagram.

        Args:
            title: Diagram title
            figsize: Figure size in inches (width, height)
            show_grid: Whether to show grid
            show_components: Whether to show component projections
            origin: Origin point (x, y) for vectors
        """
        self.title = title
        self.figsize = figsize
        self.show_grid = show_grid
        self.show_components = show_components
        self.origin = origin

        # Storage for vectors
        self.vectors: list[dict] = []
        self.resultant: dict | None = None

        # Auto-scale parameters (computed when drawing)
        self.max_magnitude: float = 0.0

    def add_vector(self, force: _Vector, color: str = "blue", label: str | None = None, show_angle: bool = True, linewidth: float = 2.5) -> None:
        """
        Add a force vector to the diagram.

        Args:
            force: ForceVector to add
            color: Arrow color
            label: Label for vector (uses force.name if None)
            show_angle: Whether to show angle annotation
            linewidth: Arrow line width
        """
        vec_data = build_vector_data(force, color, label, linewidth, show_angle)
        if vec_data is None:
            return

        self.vectors.append(vec_data)
        if vec_data["magnitude"] > self.max_magnitude:
            self.max_magnitude = vec_data["magnitude"]

    def add_resultant(self, force: _Vector, color: str = "green", label: str | None = None, linewidth: float = 3.0) -> None:
        """
        Add resultant force vector (drawn with dashed line).

        Args:
            force: Resultant ForceVector
            color: Arrow color
            label: Label for resultant
            linewidth: Arrow line width
        """
        res_data = build_resultant_data(force, color, label, linewidth)
        if res_data is None:
            return

        self.resultant = res_data
        if res_data["magnitude"] > self.max_magnitude:
            self.max_magnitude = res_data["magnitude"]

    def save(self, output_path: str | Path, dpi: int = 300, bbox_inches: str = "tight") -> Path:
        """
        Generate and save the vector diagram.

        Args:
            output_path: Output file path (png, pdf, svg supported)
            dpi: Resolution for raster formats
            bbox_inches: Bounding box setting

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)

        # Hook for subclasses to reset state before drawing
        self._pre_save_hook()

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)

        # Set title
        ax.set_title(self.title, fontsize=16, fontweight="bold", pad=20)

        # Calculate scale factor and determine plot bounds
        scale_factor = 1.0
        max_x, min_x, max_y, min_y = 0.0, 0.0, 0.0, 0.0

        if self.max_magnitude > 0:
            scale_factor = 8.0 / self.max_magnitude  # Scale to ~8 units
            max_x, min_x, max_y, min_y = compute_vector_bounds(self.vectors, self.resultant, scale_factor)

        # Draw regular vectors
        for vec_data in self.vectors:
            self._draw_vector(ax, vec_data, scale_factor)

        # Draw resultant (if present)
        if self.resultant:
            self._draw_resultant(ax, self.resultant, scale_factor)

        # Set equal aspect ratio
        ax.set_aspect("equal", adjustable="box")

        # Configure grid
        if self.show_grid:
            ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.5, zorder=0)

        # Set limits with padding - ensure we show all quadrants with vectors
        # Always show at least a small margin even if vectors are in only one quadrant
        margin = 1.5
        xlim_min = min(min_x - margin, -1.0)
        xlim_max = max(max_x + margin, 1.0)
        ylim_min = min(min_y - margin, -1.0)
        ylim_max = max(max_y + margin, 1.0)

        ax.set_xlim(xlim_min, xlim_max)
        ax.set_ylim(ylim_min, ylim_max)

        # Draw coordinate axes AFTER setting limits so they span properly
        self._draw_axes(ax, xlim_min, xlim_max, ylim_min, ylim_max)

        # Get unit from first vector for axis labels
        unit_str = self._get_unit_string()

        # Transform axis ticks to show actual force magnitudes
        if unit_str and self.max_magnitude > 0:
            # Get current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Convert scaled positions back to actual force magnitudes
            unit_scale = self.max_magnitude / 8.0  # Inverse of scale_factor

            # Set tick positions explicitly, then set labels
            ax.set_xticks(xticks)
            ax.set_yticks(yticks)
            ax.set_xticklabels([f"{x * unit_scale:.0f}" for x in xticks])
            ax.set_yticklabels([f"{y * unit_scale:.0f}" for y in yticks])

            # Axis labels with units
            ax.set_xlabel(f"x-component ({unit_str})", fontsize=12, fontweight="bold")
            ax.set_ylabel(f"y-component ({unit_str})", fontsize=12, fontweight="bold")
        else:
            ax.set_xlabel("x", fontsize=12, fontweight="bold")
            ax.set_ylabel("y", fontsize=12, fontweight="bold")

        # Add legend
        ax.legend(loc="best", fontsize=11, framealpha=0.9, fancybox=True, shadow=True)

        # Save figure
        plt.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
        plt.close(fig)

        return output_path

    def _pre_save_hook(self) -> None:
        """Hook for subclasses to reset state before drawing. Default is no-op."""
        pass

    def _get_unit_string(self) -> str:
        """Get unit string from first vector."""
        return get_unit_string(self.vectors, self.resultant)

    def _format_label_for_legend(self, label: str) -> str:
        """Format label for legend using LaTeX."""
        return format_label_for_legend(label)

    def _format_vector_label(self, force: Any, label: str) -> str:
        """
        Format vector label with LaTeX notation and magnitude.

        Subclasses can override to change formatting (e.g., include magnitude bars).
        """
        return format_vector_label(force, label, include_magnitude_bars=False)

    def _draw_axes(self, ax, xlim_min: float, xlim_max: float, ylim_min: float, ylim_max: float) -> None:
        """Draw coordinate axes spanning the entire plot."""
        draw_axes(ax, xlim_min, xlim_max, ylim_min, ylim_max)

    def _draw_vector(self, ax, vec_data: dict, scale_factor: float) -> None:
        """Draw a force vector."""
        mag = vec_data["magnitude"]
        angle = vec_data["angle"]
        color = vec_data["color"]
        label = vec_data["label"]
        show_angle = vec_data["show_angle"]
        linewidth = vec_data["linewidth"]
        force = vec_data["force"]

        # Calculate scaled magnitude
        scaled_mag = mag * scale_factor

        # Calculate endpoint
        x_end = scaled_mag * math.cos(angle)
        y_end = scaled_mag * math.sin(angle)

        # Draw vector arrow with larger, more visible arrowhead
        arrow = FancyArrowPatch(
            (0, 0),
            (x_end, y_end),
            arrowstyle="->,head_width=0.4,head_length=0.6",
            mutation_scale=20,  # Makes arrowhead larger
            color=color,
            linewidth=linewidth,
            label=self._format_label_for_legend(label),
            zorder=3,
        )
        ax.add_patch(arrow)

        # Format label with LaTeX and magnitude
        formatted_label = self._format_vector_label(force, label)

        # Add label near the tip
        label_offset = 0.5
        label_x = x_end + label_offset * math.cos(angle)
        label_y = y_end + label_offset * math.sin(angle)
        ax.text(
            label_x,
            label_y,
            formatted_label,
            fontsize=11,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": color, "linewidth": 2, "alpha": 0.9},
        )

        # Show angle annotation
        if show_angle:
            self._draw_angle_annotation(ax, angle, min(scaled_mag * 0.3, 2.0), color, label)

        # Show components if requested
        if self.show_components:
            self._draw_components(ax, x_end, y_end, color)

    def _draw_resultant(self, ax, res_data: dict, scale_factor: float) -> None:
        """Draw resultant vector with dashed line."""
        mag = res_data["magnitude"]
        angle = res_data["angle"]
        color = res_data["color"]
        label = res_data["label"]
        linewidth = res_data["linewidth"]
        force = res_data["force"]

        # Calculate scaled magnitude
        scaled_mag = mag * scale_factor

        # Calculate endpoint
        x_end = scaled_mag * math.cos(angle)
        y_end = scaled_mag * math.sin(angle)

        # Draw dashed vector arrow with larger, more visible arrowhead
        arrow = FancyArrowPatch(
            (0, 0),
            (x_end, y_end),
            arrowstyle="->,head_width=0.5,head_length=0.7",
            mutation_scale=20,  # Makes arrowhead larger
            color=color,
            linewidth=linewidth,
            linestyle="--",
            label=self._format_label_for_legend(label),
            zorder=4,
        )
        ax.add_patch(arrow)

        # Format label with LaTeX and magnitude
        formatted_label = self._format_vector_label(force, label)

        # Add label near the tip
        label_offset = 0.6
        label_x = x_end + label_offset * math.cos(angle)
        label_y = y_end + label_offset * math.sin(angle)
        ax.text(
            label_x,
            label_y,
            formatted_label,
            fontsize=12,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
            bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": color, "linewidth": 2.5, "alpha": 0.95},
        )

        # Always show angle for resultant
        self._draw_angle_annotation(ax, angle, min(scaled_mag * 0.25, 2.0), color, label)

    def _draw_angle_annotation(self, ax, angle: float, radius: float, color: str, label: str = "") -> None:
        """
        Draw angle arc and label.

        Subclasses can override this for different angle annotation styles
        (e.g., with or without overlap detection).
        """
        # Convert angle to degrees
        angle_deg = math.degrees(angle)

        # Ensure angle is positive and within [0, 360)
        while angle_deg < 0:
            angle_deg += 360
        while angle_deg >= 360:
            angle_deg -= 360

        # Draw arc from x-axis to vector
        arc = Arc((0, 0), 2 * radius, 2 * radius, angle=0, theta1=0, theta2=angle_deg, color=color, linewidth=1.5, linestyle=":", zorder=2)
        ax.add_patch(arc)

        # Calculate label position at midpoint of arc using normalized angle
        if angle_deg > 120:
            label_angle_deg = angle_deg * 0.85
        elif angle_deg < 30:
            label_angle_deg = angle_deg / 2
            radius = radius * 1.5
        else:
            label_angle_deg = angle_deg / 2

        # Convert to radians for positioning
        label_angle_rad = math.radians(label_angle_deg)
        label_radius = radius * 1.2
        label_x = label_radius * math.cos(label_angle_rad)
        label_y = label_radius * math.sin(label_angle_rad)

        # Create label with angle name if provided
        if label:
            label_text = f"θ_{label} = {angle_deg:.1f}°"
        else:
            label_text = f"{angle_deg:.1f}°"

        ax.text(label_x, label_y, label_text, fontsize=10, color=color, ha="center", va="center", bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7})

    def _draw_components(self, ax, x: float, y: float, color: str) -> None:
        """Draw component projections (dashed lines)."""
        draw_components(ax, x, y, color)
