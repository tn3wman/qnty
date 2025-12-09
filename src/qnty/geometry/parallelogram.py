"""
Parallelogram geometry module for parallelogram law vector addition.

The Parallelogram Law states that if two vectors F₁ and F₂ act at a common point,
their resultant R = F₁ + F₂ is given by the diagonal of the parallelogram formed
by the two vectors.

Geometry:
                    C ─────────────── D
                   /│               /
                  / │              /
             F₂  /  │ R          / F₂ (translated)
                /   │            /
               /    │           /
              A ────────────── B
                    F₁

Vertices:
    A: Common origin (tail of F₁, F₂, and R)
    B: Tip of F₁
    C: Tip of F₂
    D: Tip of R (opposite corner from A)

Sides:
    AB = F₁ (first component)
    AC = F₂ (second component)
    AD = R  (resultant diagonal)
    BD = F₂ (translated copy)
    CD = F₁ (translated copy)

Architecture:
    The Parallelogram class provides:
    1. Visual geometry - 4 vertices, edges, coordinates for drawing
    2. Delegation to Triangle for computation (Law of Cosines, Law of Sines)

    This separation reflects the mathematical reality:
    - Parallelograms are for VISUALIZING vector addition
    - Triangles are for COMPUTING vector addition (trigonometric laws apply to triangles)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .triangle import Triangle, TriangleCase

if TYPE_CHECKING:
    from ..core.quantity import Quantity
    from ..linalg.vector2 import Vector, VectorUnknown


@dataclass
class Vertex:
    """
    A vertex of the parallelogram with coordinates for drawing.

    Attributes:
        name: Vertex label (A, B, C, or D)
        x: X coordinate (computed from vector components)
        y: Y coordinate (computed from vector components)
        vector_tip: Name of vector that ends at this vertex (if any)
    """
    name: str
    x: float = 0.0
    y: float = 0.0
    vector_tip: str | None = None


@dataclass
class Edge:
    """
    An edge of the parallelogram connecting two vertices.

    Attributes:
        start: Starting vertex
        end: Ending vertex
        vector_name: Name of the vector this edge represents
        is_diagonal: True if this is the resultant diagonal
        is_translated: True if this is a translated copy (BD or CD)
    """
    start: Vertex
    end: Vertex
    vector_name: str | None = None
    is_diagonal: bool = False
    is_translated: bool = False


@dataclass
class Parallelogram:
    """
    A parallelogram formed by two vectors with a common origin.

    This class provides:
    1. Visual geometry for drawing (vertices, edges, coordinates)
    2. Delegation to Triangle for all computation

    The parallelogram has vertices A, B, C, D where:
        A: Common origin (tail of F₁, F₂, and R)
        B: Tip of F₁
        C: Tip of F₂
        D: Tip of R (opposite corner)

    For computation, the force triangle ABD (or equivalently ACD) is used:
        - Side AB = F₁
        - Side BD = F₂ (translated)
        - Side AD = R (diagonal/resultant)
    """

    # Input vectors
    vec_1: Vector | VectorUnknown  # F₁: first component
    vec_2: Vector | VectorUnknown  # F₂: second component
    vec_r: Vector | VectorUnknown | None = None  # R: resultant

    # Vertices (populated in __post_init__)
    vertex_a: Vertex = field(init=False)  # Origin
    vertex_b: Vertex = field(init=False)  # Tip of F₁
    vertex_c: Vertex = field(init=False)  # Tip of F₂
    vertex_d: Vertex = field(init=False)  # Tip of R (opposite corner)

    # Internal triangle for computation
    _triangle: Triangle = field(init=False, repr=False)

    def __post_init__(self):
        """Initialize vertices and the computational triangle."""
        self._build_triangle()
        self._compute_vertices()

    def _build_triangle(self):
        """Build the internal Triangle for computation."""
        self._triangle = Triangle(
            vec_1=self.vec_1,
            vec_2=self.vec_2,
            vec_r=self.vec_r,
        )

    def _compute_vertices(self):
        """
        Compute vertex coordinates from vector components.

        Places origin A at (0, 0) and computes B, C, D based on
        vector magnitudes and directions.
        """
        import math

        # Origin at (0, 0)
        self.vertex_a = Vertex(name="A", x=0.0, y=0.0)

        # B = tip of F₁
        mag_1 = self._get_magnitude(self.vec_1)
        dir_1 = self._get_direction_degrees(self.vec_1)
        if mag_1 is not None and dir_1 is not None:
            self.vertex_b = Vertex(
                name="B",
                x=mag_1 * math.cos(math.radians(dir_1)),
                y=mag_1 * math.sin(math.radians(dir_1)),
                vector_tip=self.vec_1.name,
            )
        else:
            self.vertex_b = Vertex(name="B", vector_tip=self.vec_1.name)

        # C = tip of F₂
        mag_2 = self._get_magnitude(self.vec_2)
        dir_2 = self._get_direction_degrees(self.vec_2)
        if mag_2 is not None and dir_2 is not None:
            self.vertex_c = Vertex(
                name="C",
                x=mag_2 * math.cos(math.radians(dir_2)),
                y=mag_2 * math.sin(math.radians(dir_2)),
                vector_tip=self.vec_2.name,
            )
        else:
            self.vertex_c = Vertex(name="C", vector_tip=self.vec_2.name)

        # D = tip of R = B + C (parallelogram rule)
        # D is also A + F₁ + F₂ = (0,0) + B + C
        if self.vec_r is not None:
            mag_r = self._get_magnitude(self.vec_r)
            dir_r = self._get_direction_degrees(self.vec_r)
            if mag_r is not None and dir_r is not None:
                self.vertex_d = Vertex(
                    name="D",
                    x=mag_r * math.cos(math.radians(dir_r)),
                    y=mag_r * math.sin(math.radians(dir_r)),
                    vector_tip=self.vec_r.name,
                )
            else:
                # Compute from B + C if resultant direction unknown
                self.vertex_d = Vertex(
                    name="D",
                    x=self.vertex_b.x + self.vertex_c.x,
                    y=self.vertex_b.y + self.vertex_c.y,
                    vector_tip=getattr(self.vec_r, 'name', 'R'),
                )
        else:
            # No resultant yet - compute from B + C
            self.vertex_d = Vertex(
                name="D",
                x=self.vertex_b.x + self.vertex_c.x,
                y=self.vertex_b.y + self.vertex_c.y,
                vector_tip="R",
            )

    def _get_magnitude(self, vec: Vector | VectorUnknown) -> float | None:
        """Extract magnitude value from a vector."""
        if vec is None:
            return None
        mag = vec.magnitude
        if mag is ... or mag is None:
            return None
        if hasattr(mag, 'value'):
            return mag.value
        return float(mag)

    def _get_direction_degrees(self, vec: Vector | VectorUnknown) -> float | None:
        """Get absolute direction in degrees from a vector."""
        if vec is None:
            return None
        if vec.angle is ... or vec.angle is None:
            return None

        from ..equations.angle_finder import get_absolute_angle
        try:
            abs_angle = get_absolute_angle(vec)
            return abs_angle.to_unit.degree.magnitude()
        except (AttributeError, TypeError, ValueError):
            return None

    # =========================================================================
    # Properties for drawing
    # =========================================================================

    @property
    def vertices(self) -> tuple[Vertex, Vertex, Vertex, Vertex]:
        """All four vertices in order: A, B, C, D."""
        return (self.vertex_a, self.vertex_b, self.vertex_c, self.vertex_d)

    @property
    def edges(self) -> list[Edge]:
        """
        All edges of the parallelogram for drawing.

        Returns edges in drawing order:
        1. AB (F₁)
        2. AC (F₂)
        3. AD (R - diagonal)
        4. BD (F₂ translated)
        5. CD (F₁ translated)
        """
        return [
            Edge(self.vertex_a, self.vertex_b, self.vec_1.name, is_diagonal=False),
            Edge(self.vertex_a, self.vertex_c, self.vec_2.name, is_diagonal=False),
            Edge(self.vertex_a, self.vertex_d,
                 self.vec_r.name if self.vec_r else "R", is_diagonal=True),
            Edge(self.vertex_b, self.vertex_d, self.vec_2.name, is_translated=True),
            Edge(self.vertex_c, self.vertex_d, self.vec_1.name, is_translated=True),
        ]

    @property
    def bounding_box(self) -> tuple[float, float, float, float]:
        """
        Bounding box for the parallelogram (for scaling drawings).

        Returns:
            Tuple of (min_x, min_y, max_x, max_y)
        """
        xs = [v.x for v in self.vertices]
        ys = [v.y for v in self.vertices]
        return (min(xs), min(ys), max(xs), max(ys))

    # =========================================================================
    # Delegation to Triangle for computation
    # =========================================================================

    @property
    def triangle(self) -> Triangle:
        """The underlying force triangle used for computation."""
        return self._triangle

    def classify(self) -> TriangleCase:
        """Classify the problem (SAS, SSS, etc.) - delegates to Triangle."""
        return self._triangle.classify()

    def get_sas_configuration(self) -> dict[str, Any] | None:
        """Get SAS configuration if applicable - delegates to Triangle."""
        return self._triangle.get_sas_configuration()

    def get_included_angle_step(self, included_angle) -> dict[str, Any] | None:
        """Generate solution step for included angle - delegates to Triangle."""
        return self._triangle.get_included_angle_step(included_angle)

    def compute_unknown_direction(self, unknown_side, known_angle) -> Quantity | None:
        """Compute direction of unknown side - delegates to Triangle."""
        return self._triangle.compute_unknown_direction(unknown_side, known_angle)

    # =========================================================================
    # Convenience accessors (forward to triangle)
    # =========================================================================

    @property
    def side_a(self):
        """Side a of the force triangle (F₂)."""
        return self._triangle.side_a

    @property
    def side_b(self):
        """Side b of the force triangle (R)."""
        return self._triangle.side_b

    @property
    def side_c(self):
        """Side c of the force triangle (F₁)."""
        return self._triangle.side_c

    @property
    def angle_A(self):
        """Interior angle at vertex A."""
        return self._triangle.angle_A

    @property
    def angle_B(self):
        """Interior angle at vertex B (junction)."""
        return self._triangle.angle_B

    @property
    def angle_C(self):
        """Interior angle at vertex C."""
        return self._triangle.angle_C

    @property
    def sides(self):
        """All three triangle sides."""
        return self._triangle.sides

    @property
    def angles(self):
        """All three triangle angles."""
        return self._triangle.angles

    @property
    def known_sides(self) -> int:
        """Count of known side magnitudes."""
        return self._triangle.known_sides

    @property
    def known_angles(self) -> int:
        """Count of known angles."""
        return self._triangle.known_angles

    def __repr__(self) -> str:
        verts = f"A={self.vertex_a.x:.1f},{self.vertex_a.y:.1f}"
        verts += f" B={self.vertex_b.x:.1f},{self.vertex_b.y:.1f}"
        verts += f" D={self.vertex_d.x:.1f},{self.vertex_d.y:.1f}"
        case = self.classify().name
        return f"Parallelogram({verts}, case={case})"


def from_vectors(
    vec_1: Vector | VectorUnknown,
    vec_2: Vector | VectorUnknown,
    vec_r: Vector | VectorUnknown | None = None
) -> Parallelogram:
    """
    Create a Parallelogram from vectors.

    Args:
        vec_1: First component vector F₁
        vec_2: Second component vector F₂
        vec_r: Resultant vector R (can be VectorUnknown if unknown)

    Returns:
        Parallelogram with vertices computed and triangle ready for solving
    """
    return Parallelogram(vec_1=vec_1, vec_2=vec_2, vec_r=vec_r)


def from_vectors_dynamic(
    vectors: dict[str, Vector | VectorUnknown],
) -> Parallelogram:
    """
    Create a Parallelogram using automatic role assignment.

    Identifies which vector is the resultant (marked with _is_resultant=True)
    and assigns the other two as components.

    Args:
        vectors: Dictionary mapping vector names to Vector/VectorUnknown objects.
                 Must contain exactly 3 vectors, with exactly 1 marked as resultant.

    Returns:
        Parallelogram with vectors assigned appropriately

    Raises:
        ValueError: If not exactly 3 vectors, or no resultant marker
    """
    from ..linalg.vector2 import Vector, VectorUnknown

    # Separate resultant from components
    resultant = None
    components = []

    for _name, vec in vectors.items():
        if isinstance(vec, Vector | VectorUnknown):
            if getattr(vec, '_is_resultant', False):
                if resultant is not None:
                    raise ValueError("Multiple vectors marked as resultant")
                resultant = vec
            else:
                components.append(vec)

    if resultant is None:
        raise ValueError("No vector marked as resultant (_is_resultant=True)")

    if len(components) != 2:
        raise ValueError(f"Expected 2 component vectors, got {len(components)}")

    return Parallelogram(
        vec_1=components[0],
        vec_2=components[1],
        vec_r=resultant,
    )
