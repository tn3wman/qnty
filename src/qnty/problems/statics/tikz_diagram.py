"""
TikZ diagram generation utilities for parallelogram law problems.

This module provides:
1. Data classes (DTOs) representing diagram elements - suitable for serialization
2. TikZ code generation functions
3. Helper functions for positioning and layout

The DTOs can be used to:
- Generate TikZ code for LaTeX reports
- Serialize to JSON for frontend diagram rendering
- Generate other diagram formats (matplotlib, SVG, etc.)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parallelogram_report import DiagramData, DiagramVector


# =============================================================================
# Data Transfer Objects (DTOs)
# =============================================================================


@dataclass
class Point:
    """A 2D point."""

    x: float
    y: float

    def scaled(self, scale: float) -> Point:
        """Return a new point scaled by the given factor."""
        return Point(self.x * scale, self.y * scale)


@dataclass
class TikZVector:
    """Data for rendering a vector in TikZ."""

    name: str  # e.g., "F_1"
    start: Point
    end: Point
    color: str  # TikZ color name, e.g., "vec_f1"
    style: str  # TikZ style, e.g., "vector" or "vector_translated"
    label: str  # LaTeX label, e.g., r"\vv{F_1} = 450\,\text{N}"
    label_position: str  # TikZ position, e.g., "below right"
    label_at: float  # Position along vector (0=start, 1=end)


@dataclass
class TikZAngleArc:
    """Data for rendering an angle arc in TikZ."""

    center: Point
    radius: float
    start_angle: float  # degrees
    end_angle: float  # degrees
    color: str
    style: str  # e.g., "thin" or "thick"
    label: str  # e.g., "$60^\\circ$"
    label_position: Point
    label_anchor: str  # TikZ anchor, e.g., "west"


@dataclass
class TikZInteriorAngleArc:
    """Data for rendering an interior angle arc (used in force triangle).

    Unlike TikZAngleArc which uses anchor-based positioning, this uses
    direct coordinate placement with optional font size.
    """

    center: Point
    radius: float
    start_angle: float  # degrees
    end_angle: float  # degrees
    color: str  # e.g., "orange", "purple", "cyan"
    label: str  # e.g., "$95^\\circ$"
    label_position: Point
    font_size: str = "\\footnotesize"


@dataclass
class TikZAxis:
    """Data for rendering a coordinate axis."""

    start: Point
    end: Point
    label: str  # e.g., "$+x$"
    label_position: str  # e.g., "right"


@dataclass
class TikZVertex:
    """A named vertex/coordinate in TikZ."""

    name: str  # e.g., "A", "B", "C", "D"
    point: Point


@dataclass
class TikZDiagram:
    """Complete diagram data for TikZ rendering."""

    vectors: list[TikZVector] = field(default_factory=list)
    angle_arcs: list[TikZAngleArc] = field(default_factory=list)
    interior_angle_arcs: list[TikZInteriorAngleArc] = field(default_factory=list)
    axes: list[TikZAxis] = field(default_factory=list)
    vertices: list[TikZVertex] = field(default_factory=list)
    origin: Point = field(default_factory=lambda: Point(0, 0))
    scale: float = 1.0

    def to_dict(self) -> dict:
        """Convert to a dictionary for JSON serialization."""
        return {
            "vectors": [
                {
                    "name": v.name,
                    "start": {"x": v.start.x, "y": v.start.y},
                    "end": {"x": v.end.x, "y": v.end.y},
                    "color": v.color,
                    "style": v.style,
                    "label": v.label,
                    "label_position": v.label_position,
                    "label_at": v.label_at,
                }
                for v in self.vectors
            ],
            "angle_arcs": [
                {
                    "center": {"x": a.center.x, "y": a.center.y},
                    "radius": a.radius,
                    "start_angle": a.start_angle,
                    "end_angle": a.end_angle,
                    "color": a.color,
                    "style": a.style,
                    "label": a.label,
                    "label_position": {"x": a.label_position.x, "y": a.label_position.y},
                    "label_anchor": a.label_anchor,
                }
                for a in self.angle_arcs
            ],
            "interior_angle_arcs": [
                {
                    "center": {"x": a.center.x, "y": a.center.y},
                    "radius": a.radius,
                    "start_angle": a.start_angle,
                    "end_angle": a.end_angle,
                    "color": a.color,
                    "label": a.label,
                    "label_position": {"x": a.label_position.x, "y": a.label_position.y},
                    "font_size": a.font_size,
                }
                for a in self.interior_angle_arcs
            ],
            "axes": [
                {
                    "start": {"x": a.start.x, "y": a.start.y},
                    "end": {"x": a.end.x, "y": a.end.y},
                    "label": a.label,
                    "label_position": a.label_position,
                }
                for a in self.axes
            ],
            "vertices": [
                {
                    "name": v.name,
                    "point": {"x": v.point.x, "y": v.point.y},
                }
                for v in self.vertices
            ],
            "origin": {"x": self.origin.x, "y": self.origin.y},
            "scale": self.scale,
        }


# =============================================================================
# Helper Functions
# =============================================================================


def get_ref_axis_angle(wrt: str) -> float:
    """Get the absolute angle (degrees) of a reference axis.

    Args:
        wrt: Reference axis string, e.g., "+x", "-x", "+y", "-y"

    Returns:
        Angle in degrees from positive x-axis
    """
    ref_angles = {"+x": 0, "-x": 180, "+y": 90, "-y": 270}
    return ref_angles.get(wrt, 0)


def get_label_anchor_for_angle(mid_angle: float) -> str:
    """Determine optimal TikZ anchor position based on angle.

    The anchor is the point on the label that attaches to the coordinate.
    We want the anchor to be towards the origin, so the label extends outward.

    Args:
        mid_angle: Angle in degrees (0-360)

    Returns:
        TikZ anchor string (compass direction)
    """
    mid_angle = mid_angle % 360
    if 315 <= mid_angle or mid_angle < 45:
        return "west"  # Arc on right, anchor on west (left side of label)
    elif 45 <= mid_angle < 135:
        return "south"  # Arc on top, anchor on south (bottom of label)
    elif 135 <= mid_angle < 225:
        return "east"  # Arc on left, anchor on east (right side of label)
    else:
        return "north"  # Arc on bottom, anchor on north (top of label)


def get_vector_label_position(angle_deg: float) -> str:
    """Get TikZ label position based on vector direction.

    For vectors pointing into different quadrants, we place the label
    on the opposite side to avoid overlap with the parallelogram interior.

    Args:
        angle_deg: Vector angle in degrees from +x axis

    Returns:
        TikZ position string
    """
    angle = angle_deg % 360
    if 0 <= angle < 90:
        return "below right"
    elif 90 <= angle < 180:
        return "above left"
    elif 180 <= angle < 270:
        return "above left"
    else:
        return "below right"


def compute_arc_label_position(
    center: Point,
    arc_start: float,
    arc_end: float,
    radius: float,
    label_offset: float = 0.35,
) -> tuple[Point, str]:
    """Compute label position and anchor for an angle arc.

    Args:
        center: Center point of the arc
        arc_start: Start angle in degrees
        arc_end: End angle in degrees
        radius: Arc radius
        label_offset: Additional offset from arc to label

    Returns:
        Tuple of (label_position, anchor)
    """
    mid_angle = (arc_start + arc_end) / 2
    label_r = radius + label_offset
    label_x = center.x + label_r * math.cos(math.radians(mid_angle))
    label_y = center.y + label_r * math.sin(math.radians(mid_angle))
    anchor = get_label_anchor_for_angle(mid_angle)
    return Point(label_x, label_y), anchor


# =============================================================================
# TikZ Code Generation
# =============================================================================


def render_tikz_vector(vec: TikZVector) -> str:
    """Render a single vector as TikZ code.

    Args:
        vec: Vector data

    Returns:
        TikZ draw command string
    """
    start = f"({vec.start.x:.3f},{vec.start.y:.3f})"
    end = f"({vec.end.x:.3f},{vec.end.y:.3f})"
    label_part = f"node[{vec.label_position},pos={vec.label_at}] {{{vec.label}}}"
    return f"  \\draw[{vec.style},{vec.color}] {start} -- {end} {label_part};"


def render_tikz_angle_arc(arc: TikZAngleArc) -> list[str]:
    """Render an angle arc as TikZ code.

    Args:
        arc: Angle arc data

    Returns:
        List of TikZ command strings (arc and label)
    """
    lines = []
    # Draw the arc
    center = f"({arc.center.x:.3f},{arc.center.y:.3f})"
    lines.append(
        f"  \\draw[{arc.color},{arc.style}] {center} "
        f"++({arc.start_angle}:{arc.radius:.3f}) "
        f"arc ({arc.start_angle}:{arc.end_angle}:{arc.radius:.3f});"
    )
    # Draw the label
    label_pos = f"({arc.label_position.x:.3f},{arc.label_position.y:.3f})"
    lines.append(f"  \\node[{arc.color},anchor={arc.label_anchor}] at {label_pos} {{{arc.label}}};")
    return lines


def render_tikz_interior_angle_arc(arc: TikZInteriorAngleArc) -> list[str]:
    """Render an interior angle arc as TikZ code.

    Args:
        arc: Interior angle arc data

    Returns:
        List of TikZ command strings (arc and label)
    """
    lines = []
    # Draw the arc
    center = f"({arc.center.x:.3f},{arc.center.y:.3f})"
    lines.append(
        f"  \\draw[{arc.color},thick] {center} "
        f"++({arc.start_angle:.1f}:{arc.radius:.3f}) "
        f"arc ({arc.start_angle:.1f}:{arc.end_angle:.1f}:{arc.radius:.3f});"
    )
    # Draw the label with font size
    label_pos = f"({arc.label_position.x:.3f},{arc.label_position.y:.3f})"
    lines.append(f"  \\node[{arc.color},font={arc.font_size}] at {label_pos} {{{arc.label}}};")
    return lines


def render_tikz_axes(axes: list[TikZAxis]) -> list[str]:
    """Render coordinate axes as TikZ code.

    Args:
        axes: List of axis data

    Returns:
        List of TikZ draw command strings
    """
    lines = []
    for axis in axes:
        start = f"({axis.start.x:.3f},{axis.start.y:.3f})"
        end = f"({axis.end.x:.3f},{axis.end.y:.3f})"
        lines.append(f"  \\draw[->,gray] {start} -- {end} node[{axis.label_position}] {{{axis.label}}};")
    return lines


# =============================================================================
# Diagram Builders
# =============================================================================


def build_reference_angle_arc(
    vec: DiagramVector | None,
    origin: Point,
    base_radius: float,
    radius_multiplier: float,
    color: str,
) -> TikZAngleArc | None:
    """Build an angle arc showing vector's angle from its reference axis.

    Args:
        vec: Vector data with angle_ref, angle_wrt, angle_deg
        origin: Origin point for the arc
        base_radius: Base radius for scaling
        radius_multiplier: Multiplier for this arc's radius
        color: TikZ color for the arc

    Returns:
        TikZAngleArc or None if angle is negligible
    """
    if vec is None or abs(vec.angle_ref) <= 0.5:
        return None

    ref_angle = get_ref_axis_angle(vec.angle_wrt)
    arc_radius = base_radius * radius_multiplier

    label_pos, anchor = compute_arc_label_position(origin, ref_angle, vec.angle_deg, arc_radius)

    return TikZAngleArc(
        center=origin,
        radius=arc_radius,
        start_angle=ref_angle,
        end_angle=vec.angle_deg,
        color=color,
        style="thin",
        label=f"${vec.angle_ref:.0f}^\\circ$",
        label_position=label_pos,
        label_anchor=anchor,
    )


def build_coordinate_axes(origin: Point, axis_length: float) -> list[TikZAxis]:
    """Build the four coordinate axes.

    Args:
        origin: Origin point
        axis_length: Length of each axis from origin

    Returns:
        List of four TikZAxis objects
    """
    return [
        TikZAxis(origin, Point(origin.x + axis_length, origin.y), "$+x$", "right"),
        TikZAxis(origin, Point(origin.x - axis_length, origin.y), "$-x$", "left"),
        TikZAxis(origin, Point(origin.x, origin.y + axis_length), "$+y$", "above"),
        TikZAxis(origin, Point(origin.x, origin.y - axis_length), "$-y$", "below"),
    ]


def build_problem_setup_diagram(data: DiagramData, scale: float = 0.55) -> TikZDiagram:
    """Build TikZ diagram data for the Problem Setup view.

    Shows vectors F1 and F2 with their reference angle arcs.

    Args:
        data: Diagram data from ReportData
        scale: TikZ scale factor

    Returns:
        TikZDiagram with vectors and angle arcs
    """
    from ...equations.base import latex_name

    diagram = TikZDiagram(scale=scale)

    # Get vertices and vectors from data
    v_dict = {v.name: v for v in data.vertices}
    vec_dict = {v.name: v for v in data.vectors}

    A = v_dict.get("A")
    B = v_dict.get("B")
    C = v_dict.get("C")
    D = v_dict.get("D")

    if A is None or B is None or C is None or D is None:
        return diagram

    # Scale coordinates
    s = data.scale
    origin = Point(A.x * s, A.y * s)
    b_pt = Point(B.x * s, B.y * s)
    c_pt = Point(C.x * s, C.y * s)
    d_pt = Point(D.x * s, D.y * s)

    diagram.origin = origin

    # Store named vertices for TikZ coordinate definitions
    diagram.vertices = [
        TikZVertex("A", origin),
        TikZVertex("B", b_pt),
        TikZVertex("C", c_pt),
        TikZVertex("D", d_pt),
    ]

    # Get vector names and data
    f1_name = B.vector_name or "F_1"
    f2_name = C.vector_name or "F_2"
    f1_vec = vec_dict.get(f1_name)
    f2_vec = vec_dict.get(f2_name)

    # Compute axis length
    f1_len = math.sqrt(b_pt.x**2 + b_pt.y**2)
    f2_len = math.sqrt(c_pt.x**2 + c_pt.y**2)
    d_len = math.sqrt(d_pt.x**2 + d_pt.y**2)
    axis_len = max(f1_len, f2_len, d_len, 1.0)

    # Build axes
    diagram.axes = build_coordinate_axes(origin, axis_len)

    # Build magnitude labels
    def mag_label(vec: DiagramVector | None) -> str:
        if vec is None:
            return ""
        return f"{vec.magnitude:.0f}\\,\\text{{{vec.unit}}}"

    # Build vectors
    f1_label = latex_name(f1_name)
    f2_label = latex_name(f2_name)
    f1_pos = get_vector_label_position(f1_vec.angle_deg) if f1_vec else "below right"
    f2_pos = get_vector_label_position(f2_vec.angle_deg) if f2_vec else "above left"

    diagram.vectors = [
        TikZVector(
            name=f1_name,
            start=origin,
            end=b_pt,
            color="vec_f1",
            style="vector",
            label=f"$\\vv{{{f1_label}}} = {mag_label(f1_vec)}$",
            label_position=f1_pos,
            label_at=1,
        ),
        TikZVector(
            name=f2_name,
            start=origin,
            end=c_pt,
            color="vec_f2",
            style="vector",
            label=f"$\\vv{{{f2_label}}} = {mag_label(f2_vec)}$",
            label_position=f2_pos,
            label_at=1,
        ),
        # Translated vectors (dashed)
        TikZVector(
            name=f"{f2_name}_translated",
            start=b_pt,
            end=d_pt,
            color="vec_translated",
            style="vector_translated",
            label="",
            label_position="",
            label_at=0,
        ),
        TikZVector(
            name=f"{f1_name}_translated",
            start=c_pt,
            end=d_pt,
            color="vec_translated",
            style="vector_translated",
            label="",
            label_position="",
            label_at=0,
        ),
    ]

    # Build angle arcs
    arc_radius_base = axis_len * 0.5
    if f1_arc := build_reference_angle_arc(f1_vec, origin, arc_radius_base, 0.7, "vec_f1"):
        diagram.angle_arcs.append(f1_arc)
    if f2_arc := build_reference_angle_arc(f2_vec, origin, arc_radius_base, 1.0, "vec_f2"):
        diagram.angle_arcs.append(f2_arc)

    return diagram


def render_problem_setup_tikz(diagram: TikZDiagram) -> str:
    """Render the Problem Setup TikZ diagram code.

    Args:
        diagram: TikZ diagram data

    Returns:
        Complete TikZ picture code (with leading newline for LaTeX embedding)
    """
    # Leading newline for proper LaTeX spacing when embedded
    lines = ["", f"\\begin{{tikzpicture}}[scale={diagram.scale},baseline=(current bounding box.north)]"]

    # Named coordinates (A, B, C, D)
    for vertex in diagram.vertices:
        lines.append(f"  \\coordinate ({vertex.name}) at ({vertex.point.x:.3f},{vertex.point.y:.3f});")

    # Axes
    lines.extend(render_tikz_axes(diagram.axes))

    # Vectors (translated ones first, then main ones)
    translated = [v for v in diagram.vectors if "translated" in v.name]
    main = [v for v in diagram.vectors if "translated" not in v.name]

    # Create a mapping from point coordinates to vertex names for symbolic references
    vertex_map: dict[tuple[float, float], str] = {}
    for vertex in diagram.vertices:
        key = (round(vertex.point.x, 3), round(vertex.point.y, 3))
        vertex_map[key] = vertex.name

    def get_vertex_name(pt: Point) -> str:
        """Get the vertex name for a point, or format coordinates if not a vertex."""
        key = (round(pt.x, 3), round(pt.y, 3))
        if key in vertex_map:
            return f"({vertex_map[key]})"
        return f"({pt.x:.3f},{pt.y:.3f})"

    lines.append("  % Draw parallelogram sides (translated vectors - dashed)")
    for vec in translated:
        start = get_vertex_name(vec.start)
        end = get_vertex_name(vec.end)
        lines.append(f"  \\draw[{vec.style},{vec.color}] {start} -- {end};")

    lines.append("  % Draw main vectors")
    for vec in main:
        start = get_vertex_name(vec.start)
        end = get_vertex_name(vec.end)
        label_part = f"node[{vec.label_position},pos={vec.label_at}] {{{vec.label}}}"
        lines.append(f"  \\draw[{vec.style},{vec.color}] {start} -- {end} {label_part};")

    # Angle arcs
    for arc in diagram.angle_arcs:
        lines.extend(render_tikz_angle_arc(arc))

    # Origin point - use vertex name if available
    origin_name = get_vertex_name(diagram.origin)
    lines.append(f"  \\fill {origin_name} circle (2pt) node[below left] {{$O$}};")
    lines.append("\\end{tikzpicture}")

    return "\n".join(lines)


def get_arc_angles(start_angle: float, end_angle: float) -> tuple[float, float]:
    """Compute arc start and end angles for the shorter sweep direction.

    Given two angles, returns (start, end) such that the arc sweeps in
    the shorter direction.

    Args:
        start_angle: First angle in degrees
        end_angle: Second angle in degrees

    Returns:
        Tuple of (start, end) angles, possibly adjusted for shorter sweep
    """
    start = start_angle % 360
    end = end_angle % 360
    ccw_sweep = (end - start) % 360
    if ccw_sweep == 0:
        ccw_sweep = 360
    cw_sweep = 360 - ccw_sweep
    if ccw_sweep <= cw_sweep:
        if end < start:
            end += 360
        return start, end
    else:
        if start < end:
            start += 360
        return end, start


def build_force_triangle_diagram(data: DiagramData, scale: float = 0.55) -> TikZDiagram:
    """Build TikZ diagram data for the Force Triangle (Results) view.

    Shows the parallelogram with F1, F2, FR vectors and interior angles.

    Args:
        data: Diagram data from ReportData
        scale: TikZ scale factor

    Returns:
        TikZDiagram with vectors, translated sides, and interior angle arcs
    """
    from ...equations.base import latex_name

    diagram = TikZDiagram(scale=scale)

    # Get vertices and vectors from data
    v_dict = {v.name: v for v in data.vertices}
    vec_dict = {v.name: v for v in data.vectors}

    A = v_dict.get("A")
    B = v_dict.get("B")
    C = v_dict.get("C")
    D = v_dict.get("D")

    if A is None or B is None or C is None or D is None:
        return diagram

    # Scale coordinates
    s = data.scale
    origin = Point(A.x * s, A.y * s)
    b_pt = Point(B.x * s, B.y * s)
    c_pt = Point(C.x * s, C.y * s)
    d_pt = Point(D.x * s, D.y * s)

    diagram.origin = origin

    # Store named vertices for TikZ coordinate definitions
    diagram.vertices = [
        TikZVertex("A", origin),
        TikZVertex("B", b_pt),
        TikZVertex("C", c_pt),
        TikZVertex("D", d_pt),
    ]

    # Get vector names and data
    f1_name = B.vector_name or "F_1"
    f2_name = C.vector_name or "F_2"
    fr_name = D.vector_name or "F_R"
    f1_vec = vec_dict.get(f1_name)
    f2_vec = vec_dict.get(f2_name)
    fr_vec = vec_dict.get(fr_name)

    # Compute axis length
    f1_len = math.sqrt(b_pt.x**2 + b_pt.y**2)
    f2_len = math.sqrt(c_pt.x**2 + c_pt.y**2)
    d_len = math.sqrt(d_pt.x**2 + d_pt.y**2)
    axis_len = max(f1_len, f2_len, d_len, 1.0)

    # Build axes
    diagram.axes = build_coordinate_axes(origin, axis_len)

    # Build magnitude label (only for FR in force triangle)
    def mag_label(vec: DiagramVector | None) -> str:
        if vec is None:
            return ""
        return f"{vec.magnitude:.0f}\\,\\text{{{vec.unit}}}"

    fr_mag = mag_label(fr_vec)

    # Vector label positions
    f1_angle = f1_vec.angle_deg if f1_vec else 60
    f2_angle = f2_vec.angle_deg if f2_vec else 195
    fr_angle = fr_vec.angle_deg if fr_vec else 155

    f1_pos = get_vector_label_position(f1_angle)
    f2_pos = get_vector_label_position(f2_angle)
    fr_pos = get_vector_label_position(fr_angle)

    # LaTeX labels
    f1_label = latex_name(f1_name)
    f2_label = latex_name(f2_name)
    fr_label = latex_name(fr_name)

    # Build vectors
    diagram.vectors = [
        # Translated vectors (dashed) - same as problem setup
        TikZVector(
            name=f"{f2_name}_translated",
            start=b_pt,
            end=d_pt,
            color="vec_translated",
            style="vector_translated",
            label="",
            label_position="",
            label_at=0,
        ),
        TikZVector(
            name=f"{f1_name}_translated",
            start=c_pt,
            end=d_pt,
            color="vec_translated",
            style="vector_translated",
            label="",
            label_position="",
            label_at=0,
        ),
        # Main vectors - F1 and F2 without magnitude, FR with magnitude
        TikZVector(
            name=f1_name,
            start=origin,
            end=b_pt,
            color="vec_f1",
            style="vector",
            label=f"$\\vv{{{f1_label}}}$",
            label_position=f1_pos,
            label_at=1,
        ),
        TikZVector(
            name=f2_name,
            start=origin,
            end=c_pt,
            color="vec_f2",
            style="vector",
            label=f"$\\vv{{{f2_label}}}$",
            label_position=f2_pos,
            label_at=1,
        ),
        TikZVector(
            name=fr_name,
            start=origin,
            end=d_pt,
            color="vec_fr",
            style="vector",
            label=f"$\\vv{{{fr_label}}} = {fr_mag}$",
            label_position=fr_pos,
            label_at=1,
        ),
    ]

    # Build interior angle arcs
    arc_r_small = 0.6
    arc_label_offset = 0.5

    # Get interior angles from data
    interior_angles = data.interior_angles
    angle_at_origin = interior_angles[0].value_deg if len(interior_angles) > 0 else 0
    angle_at_f1_tip = interior_angles[1].value_deg if len(interior_angles) > 1 else 0
    angle_at_fr_tip = interior_angles[2].value_deg if len(interior_angles) > 2 else 0

    # Arc at origin (A): angle between F1 and FR (orange)
    if angle_at_origin > 0:
        f1_ang = f1_vec.angle_deg if f1_vec else 0
        fr_ang = fr_vec.angle_deg if fr_vec else 0
        arc_start, arc_end = get_arc_angles(f1_ang, fr_ang)
        arc_mid = (arc_start + arc_end) / 2
        label_x = origin.x + (arc_r_small + arc_label_offset) * math.cos(math.radians(arc_mid))
        label_y = origin.y + (arc_r_small + arc_label_offset) * math.sin(math.radians(arc_mid))
        diagram.interior_angle_arcs.append(
            TikZInteriorAngleArc(
                center=origin,
                radius=arc_r_small,
                start_angle=arc_start,
                end_angle=arc_end,
                color="orange",
                label=f"${angle_at_origin:.0f}^\\circ$",
                label_position=Point(label_x, label_y),
            )
        )

    # Arc at B (F1 tip): angle between incoming F1 and outgoing to D (purple)
    if angle_at_f1_tip > 0:
        f1_incoming = ((f1_vec.angle_deg if f1_vec else 0) + 180) % 360
        bd_angle = math.degrees(math.atan2(d_pt.y - b_pt.y, d_pt.x - b_pt.x)) % 360
        arc_start, arc_end = get_arc_angles(f1_incoming, bd_angle)
        arc_mid = (arc_start + arc_end) / 2
        label_x = b_pt.x + (arc_r_small + arc_label_offset) * math.cos(math.radians(arc_mid))
        label_y = b_pt.y + (arc_r_small + arc_label_offset) * math.sin(math.radians(arc_mid))
        diagram.interior_angle_arcs.append(
            TikZInteriorAngleArc(
                center=b_pt,
                radius=arc_r_small,
                start_angle=arc_start,
                end_angle=arc_end,
                color="purple",
                label=f"${angle_at_f1_tip:.0f}^\\circ$",
                label_position=Point(label_x, label_y),
            )
        )

    # Arc at D (FR tip): angle at the apex (cyan)
    if angle_at_fr_tip > 0:
        bd_angle = math.degrees(math.atan2(b_pt.y - d_pt.y, b_pt.x - d_pt.x)) % 360
        fr_back = ((fr_vec.angle_deg if fr_vec else 0) + 180) % 360
        arc_start, arc_end = get_arc_angles(bd_angle, fr_back)
        arc_mid = (arc_start + arc_end) / 2
        label_x = d_pt.x + (arc_r_small + arc_label_offset) * math.cos(math.radians(arc_mid))
        label_y = d_pt.y + (arc_r_small + arc_label_offset) * math.sin(math.radians(arc_mid))
        diagram.interior_angle_arcs.append(
            TikZInteriorAngleArc(
                center=d_pt,
                radius=arc_r_small,
                start_angle=arc_start,
                end_angle=arc_end,
                color="cyan",
                label=f"${angle_at_fr_tip:.0f}^\\circ$",
                label_position=Point(label_x, label_y),
            )
        )

    return diagram


def render_force_triangle_tikz(diagram: TikZDiagram) -> str:
    """Render the Force Triangle TikZ diagram code.

    Args:
        diagram: TikZ diagram data

    Returns:
        Complete TikZ picture code (with leading newline for LaTeX embedding)
    """
    # Leading newline for proper LaTeX spacing when embedded
    lines = ["", f"\\begin{{tikzpicture}}[scale={diagram.scale},baseline=(current bounding box.north)]"]

    # Named coordinates (A, B, C, D)
    for vertex in diagram.vertices:
        lines.append(f"  \\coordinate ({vertex.name}) at ({vertex.point.x:.3f},{vertex.point.y:.3f});")

    # Axes
    lines.extend(render_tikz_axes(diagram.axes))

    # Create a mapping from point coordinates to vertex names for symbolic references
    vertex_map: dict[tuple[float, float], str] = {}
    for vertex in diagram.vertices:
        key = (round(vertex.point.x, 3), round(vertex.point.y, 3))
        vertex_map[key] = vertex.name

    def get_vertex_name(pt: Point) -> str:
        """Get the vertex name for a point, or format coordinates if not a vertex."""
        key = (round(pt.x, 3), round(pt.y, 3))
        if key in vertex_map:
            return f"({vertex_map[key]})"
        return f"({pt.x:.3f},{pt.y:.3f})"

    # Vectors (translated ones first, then main ones)
    translated = [v for v in diagram.vectors if "translated" in v.name]
    main = [v for v in diagram.vectors if "translated" not in v.name]

    # Translated vectors
    for vec in translated:
        start = get_vertex_name(vec.start)
        end = get_vertex_name(vec.end)
        lines.append(f"  \\draw[{vec.style},{vec.color}] {start} -- {end};")

    # Main vectors
    for vec in main:
        start = get_vertex_name(vec.start)
        end = get_vertex_name(vec.end)
        label_part = f"node[{vec.label_position},pos={vec.label_at}] {{{vec.label}}}"
        lines.append(f"  \\draw[{vec.style},{vec.color}] {start} -- {end} {label_part};")

    # Interior angle arcs
    for arc in diagram.interior_angle_arcs:
        lines.extend(render_tikz_interior_angle_arc(arc))

    # Origin point - use vertex name if available
    origin_name = get_vertex_name(diagram.origin)
    lines.append(f"  \\fill {origin_name} circle (2pt) node[below left] {{$O$}};")
    lines.append("\\end{tikzpicture}")

    return "\n".join(lines)
