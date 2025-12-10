"""
Triangle geometry module for assembling vectors into triangles.

In the parallelogram law, two vectors are placed tail-to-tip to form a triangle:
- Vector 1 starts at point A (tail) and ends at point B (tip)
- Vector 2 starts at point B (tail of V2 = tip of V1) and ends at point C (tip)
- The resultant goes from point A (tail of V1) to point C (tip of V2)

This module provides the Triangle class that:
1. Takes two input vectors and assembles them tail-to-tip
2. Computes the three interior angles of the triangle
3. Tracks which sides/angles are known vs unknown
4. Classifies the triangle case (SAS, SSS, ASA, AAS, SSA) for solving

## Vertex-Based Model

The key insight is to model the triangle with explicit vertices and track
which direction each side goes "from" each vertex. This eliminates special
cases for computing interior angles.

Vertices:
    A: Common start of component 1 (C1) and resultant (R)
    B: End of C1, start of component 2 (C2)
    C: Common end of C2 and R

For each vertex, we can compute the interior angle by:
    1. Get the outgoing direction from that vertex for each adjacent side
    2. Compute the absolute difference in directions
    3. The interior angle is this difference (no special cases!)

This works because "outgoing direction from vertex" naturally handles:
    - Tail-to-tip: direction is the vector's direction
    - Tip at vertex: direction is (vector's direction + 180°)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from types import EllipsisType
from typing import Any

from ..core.quantity import Q, Quantity
from ..linalg.vector2 import Vector, VectorUnknown

# =============================================================================
# Angle Constants and Helpers
# =============================================================================

# Pre-computed angle constants to avoid repeated instantiation
_ZERO_ANGLE = None
_HALF_ROTATION = None
_FULL_ROTATION = None


def _get_angle_constants() -> tuple[Quantity, Quantity, Quantity]:
    """
    Get cached angle constants (0°, 180°, 360°).

    Returns lazily-initialized constants to avoid import-time issues
    while preventing repeated object creation.
    """
    global _ZERO_ANGLE, _HALF_ROTATION, _FULL_ROTATION
    if _ZERO_ANGLE is None or _HALF_ROTATION is None or _FULL_ROTATION is None:
        _ZERO_ANGLE = Q(0, "degree")
        _HALF_ROTATION = Q(180, "degree")
        _FULL_ROTATION = Q(360, "degree")
    return _ZERO_ANGLE, _HALF_ROTATION, _FULL_ROTATION


def _normalize_angle(angle: Quantity) -> Quantity:
    """
    Normalize an angle to the range [0, 360) degrees.

    Uses efficient modulo-style normalization instead of while loops.

    Args:
        angle: Angle as a Quantity (in degrees)

    Returns:
        Normalized angle in range [0, 360) as a Quantity
    """
    zero, _, full = _get_angle_constants()

    # Normalize to [0, 360) using Quantity comparison operators
    while angle >= full:
        angle = angle - full
    while angle < zero:
        angle = angle + full

    return angle


def _get_interior_angle(angle: Quantity) -> Quantity:
    """
    Convert an angle difference to an interior angle (0-180°).

    The interior angle is the smaller of the two possible angles
    formed by two directions.

    Args:
        angle: Angle difference as a Quantity (should be normalized to [0, 360))

    Returns:
        Interior angle (0-180°) as a Quantity
    """
    _, half, full = _get_angle_constants()

    if angle > half:
        angle = full - angle

    return angle


def _get_adjacent_sides(triangle: Triangle, vertex: Vertex) -> list[TriangleSide]:
    """
    Get the two sides adjacent to a given vertex.

    Args:
        triangle: The Triangle instance
        vertex: The vertex to find adjacent sides for

    Returns:
        List of TriangleSide objects adjacent to the vertex (0-2 items)
    """
    adjacent = []
    for side in (triangle.side_a, triangle.side_b, triangle.side_c):
        if side.start == vertex or side.end == vertex:
            adjacent.append(side)
    return adjacent


# SAS configuration definitions: (side1, side2, included_angle, unknown_side, unknown_angle1, unknown_angle2)
# Each tuple defines a valid SAS configuration for the triangle
SAS_CONFIGURATIONS = (
    # sides a,b with angle_C (at vertex C, between a and b) -> solve for side_c
    ("side_a", "side_b", "angle_C", "side_c", "angle_A", "angle_B"),
    # sides a,c with angle_B (at vertex B, between a and c) -> solve for side_b
    ("side_a", "side_c", "angle_B", "side_b", "angle_A", "angle_C"),
    # sides b,c with angle_A (at vertex A, between b and c) -> solve for side_a
    ("side_b", "side_c", "angle_A", "side_a", "angle_B", "angle_C"),
)


def _check_sas_configuration(triangle: Triangle) -> tuple[str, str, str, str, str, str] | None:
    """
    Check if the triangle has a valid SAS configuration.

    Args:
        triangle: The Triangle instance to check

    Returns:
        Tuple of (side1_name, side2_name, included_angle_name, unknown_side_name,
                  unknown_angle1_name, unknown_angle2_name) if SAS, None otherwise
    """
    for config in SAS_CONFIGURATIONS:
        side1_name, side2_name, angle_name, *_ = config
        side1 = getattr(triangle, side1_name)
        side2 = getattr(triangle, side2_name)
        angle = getattr(triangle, angle_name)

        if side1.is_known and side2.is_known and angle.is_known:
            return config
    return None


class TriangleCase(Enum):
    """Classification of triangle solving cases based on known quantities."""
    SAS = auto()  # Two sides + included angle → Law of Cosines
    SSS = auto()  # Three sides → Law of Cosines for angles
    ASA = auto()  # Two angles + included side → Angle sum + Law of Sines
    AAS = auto()  # Two angles + non-included side → Angle sum + Law of Sines
    SSA = auto()  # Two sides + non-included angle → Law of Sines (ambiguous)
    UNKNOWN = auto()  # Cannot determine case or insufficient information


class Vertex(Enum):
    """
    Triangle vertices in parallelogram law configuration.

    Standard configuration for vector addition C1 + C2 = R:
        A: Common start of component 1 (C1) and resultant (R)
        B: End of C1, start of component 2 (C2) - the "junction"
        C: Common end of C2 and resultant (R)

    Interior angles are named by their vertex:
        angle_A: at vertex A (opposite side_a = C1)
        angle_B: at vertex B (opposite side_b = C2)
        angle_C: at vertex C (opposite side_c = R)
    """
    A = "A"  # Common start of C1 and R
    B = "B"  # End of C1, start of C2 (junction)
    C = "C"  # Common end of C2 and R


# Side configuration: (start_vertex, end_vertex)
# Defines how each side maps to triangle vertices - must be after Vertex class
SIDE_VERTEX_MAP: dict[str, tuple[Vertex, Vertex]] = {}  # Populated after class definitions

# Angle configuration: (vertex, opposite_side_attr)
# Defines how each angle maps to vertices and opposite sides
ANGLE_VERTEX_MAP: dict[str, tuple[Vertex, str]] = {}  # Populated after class definitions


@dataclass
class TriangleSide:
    """
    Represents one side of a triangle with explicit vertex endpoints.

    Attributes:
        magnitude: Length of the side as a Quantity, or ... if unknown
        is_known: Whether the magnitude is known
        name: Optional name for this side (e.g., "F_1", "F_R")
        direction: Absolute direction of the vector (from start to end) as Quantity
        start: Starting vertex of this side
        end: Ending vertex of this side
    """

    magnitude: Quantity | EllipsisType  # Can be Quantity or ellipsis (...)
    is_known: bool
    name: str | None = None
    direction: Quantity | None = None  # Absolute direction as Quantity
    start: Vertex | None = None
    end: Vertex | None = None

    def direction_from(self, vertex: Vertex) -> Quantity | None:
        """
        Get the outgoing direction as seen from a vertex.

        This is the key method that eliminates special cases:
        - If vertex is the start: return direction (going away from vertex)
        - If vertex is the end: return direction + 180° (reversed direction)

        Args:
            vertex: The vertex to get direction from

        Returns:
            Outgoing direction as Quantity, or None if vertex is not adjacent
        """
        if self.direction is None:
            return None
        if vertex == self.start:
            return self.direction
        elif vertex == self.end:
            # Add 180° and normalize to [0, 360)
            _, half, _ = _get_angle_constants()
            result = self.direction + half
            return _normalize_angle(result)
        return None


@dataclass
class TriangleAngle:
    """
    Represents one interior angle of a triangle.

    Attributes:
        angle: The interior angle as a Quantity
        is_known: Whether the angle is known
        opposite_side: Name of the side opposite to this angle
        vertex: The vertex where this angle is located
    """

    angle: Quantity | None
    is_known: bool
    opposite_side: str | None = None
    vertex: Vertex | None = None


@dataclass
class Triangle:
    """
    A triangle formed by assembling vectors using explicit vertex geometry.

    The triangle has three vertices (A, B, C) with standard configuration:
        A: Common start of component 1 (C1) and resultant (R)
        B: End of C1, start of component 2 (C2) - the "junction"
        C: Common end of C2 and resultant (R)

    Using STANDARD triangle notation where side_x is OPPOSITE vertex X:
        side_a: connects B-C (opposite vertex A) = C2
        side_b: connects A-C (opposite vertex B) = R (resultant)
        side_c: connects A-B (opposite vertex C) = C1

    Interior angles at their respective vertices:
        angle_A: at vertex A, opposite side_a, between C1 (outgoing to B) and R (outgoing to C)
        angle_B: at vertex B, opposite side_b, between C1 (incoming from A) and C2 (outgoing to C)
        angle_C: at vertex C, opposite side_c, between C2 (incoming from B) and R (incoming from A)

    For parallelogram law problems:
        - C1 + C2 = R
        - When C1 and C2 are known, angle_B (at junction) is computable
        - angle_B is opposite side_b (the resultant R)
        - This gives SAS: sides c (C1), a (C2), angle_B → solve for side_b (R)
    """

    # The original vectors (can be Vector or VectorUnknown)
    vec_1: Vector | VectorUnknown  # C1: from A to B = side_c
    vec_2: Vector | VectorUnknown  # C2: from B to C = side_a
    vec_r: Vector | VectorUnknown | None = None  # R: from A to C = side_b

    # Sides using standard notation (side_x is OPPOSITE vertex X)
    side_a: TriangleSide = field(init=False)  # C2 (from B to C) - opposite vertex A
    side_b: TriangleSide = field(init=False)  # R  (from A to C) - opposite vertex B
    side_c: TriangleSide = field(init=False)  # C1 (from A to B) - opposite vertex C

    # Interior angles - at their respective vertices, opposite their named sides
    angle_A: TriangleAngle = field(init=False)  # At vertex A, opposite side_a (C2)
    angle_B: TriangleAngle = field(init=False)  # At vertex B, opposite side_b (R)
    angle_C: TriangleAngle = field(init=False)  # At vertex C, opposite side_c (C1)

    def __post_init__(self):
        """Assemble the triangle from the input vectors."""
        self._assemble_sides()
        self._compute_interior_angles()

    def _assemble_sides(self):
        """
        Set up the triangle sides from vector magnitudes with vertex information.

        Uses STANDARD triangle notation where side_x is OPPOSITE vertex X:
            side_a = C2 (vec_2): from B to C, opposite vertex A
            side_b = R  (vec_r): from A to C, opposite vertex B
            side_c = C1 (vec_1): from A to B, opposite vertex C
        """
        # Vector-to-side mapping: (side_attr, vec_attr)
        side_assignments = [
            ("side_c", self.vec_1),  # C1: from A to B
            ("side_a", self.vec_2),  # C2: from B to C
            ("side_b", self.vec_r),  # R:  from A to C (may be None)
        ]

        for side_attr, vec in side_assignments:
            side = self._create_side_from_vector(vec, side_attr)
            setattr(self, side_attr, side)

    def _create_side_from_vector(
        self, vec: Vector | VectorUnknown | None, side_attr: str
    ) -> TriangleSide:
        """
        Create a TriangleSide from a vector using the vertex map.

        Args:
            vec: The Vector, VectorUnknown, or None
            side_attr: The side attribute name (e.g., "side_a")

        Returns:
            A TriangleSide with appropriate vertices from SIDE_VERTEX_MAP
        """
        from ..equations.angle_finder import get_effective_direction
        from ..linalg.vector2 import VectorUnknown

        start, end = SIDE_VERTEX_MAP[side_attr]

        if vec is None:
            # No vector provided - create placeholder
            return TriangleSide(
                magnitude=...,
                is_known=False,
                name="R",
                direction=None,
                start=start,
                end=end,
            )

        # Extract magnitude and known status
        if isinstance(vec, VectorUnknown) and vec.magnitude is ...:
            mag: Quantity | EllipsisType = ...
            is_known = False
        else:
            # At this point, vec.magnitude is Quantity (either Vector always has Quantity,
            # or VectorUnknown with non-ellipsis magnitude)
            mag = vec.magnitude
            # Type narrowing: if we're here, mag is Quantity not EllipsisType
            if mag is ...:
                # This branch is unreachable, but satisfies the type checker
                is_known = False
            else:
                is_known = mag.value is not None and mag.value != 0

        # Get direction (effective direction accounts for negative magnitude)
        direction: Quantity | None = None
        if not (isinstance(vec, VectorUnknown) and vec.angle is ...):
            try:
                direction = get_effective_direction(vec)
            except (AttributeError, TypeError):
                pass

        return TriangleSide(
            magnitude=mag,
            is_known=is_known,
            name=vec.name,
            direction=direction,
            start=start,
            end=end,
        )

    def _get_vector_for_side(self, side: TriangleSide) -> Vector | VectorUnknown | None:
        """Get the original vector corresponding to a triangle side."""
        if side is self.side_a:
            return self.vec_2  # side_a = C2 (vec_2)
        elif side is self.side_b:
            return self.vec_r  # side_b = R (vec_r)
        elif side is self.side_c:
            return self.vec_1  # side_c = C1 (vec_1)
        return None

    def _check_relative_angle_at_vertex(
        self, vertex: Vertex, side1: TriangleSide, side2: TriangleSide
    ) -> Quantity | None:
        """
        Check if the interior angle at a vertex is directly specified by a relative angle.

        This handles the case where one vector's angle is defined relative to another
        vector (wrt=another_vector). If both vectors meet at the same vertex and one
        references the other as its wrt, the relative angle IS the interior angle.

        For example:
        - F_BA starts at vertex A, has unknown absolute direction
        - F_R starts at vertex A, has angle=30° with wrt=F_BA
        - The interior angle at A is 30° (the relative angle between them)

        Args:
            vertex: The vertex where we're computing the interior angle
            side1: First side adjacent to the vertex
            side2: Second side adjacent to the vertex

        Returns:
            The interior angle as a Quantity if found via relative reference, else None
        """
        # Get the original vectors for these sides
        vec1 = self._get_vector_for_side(side1)
        vec2 = self._get_vector_for_side(side2)

        if vec1 is None or vec2 is None:
            return None

        # Check if vec1's wrt references vec2
        # Note: We check both identity (is) and equivalence (same magnitude/name)
        # because vectors may be copied with wrt pointing to original objects
        if hasattr(vec1, 'wrt') and self._vectors_are_same(vec1.wrt, vec2):
            # vec1's angle is relative to vec2
            angle = vec1.angle
            if angle is not ... and angle is not None:
                # Return absolute value of the angle
                zero, _, _ = _get_angle_constants()
                if angle < zero:
                    return zero - angle
                return angle

        # Check if vec2's wrt references vec1
        if hasattr(vec2, 'wrt') and self._vectors_are_same(vec2.wrt, vec1):
            # vec2's angle is relative to vec1
            angle = vec2.angle
            if angle is not ... and angle is not None:
                # Return absolute value of the angle
                zero, _, _ = _get_angle_constants()
                if angle < zero:
                    return zero - angle
                return angle

        return None

    def _vectors_are_same(self, vec_a: Any, vec_b: Any) -> bool:
        """
        Check if two vectors refer to the same logical vector.

        This handles the case where vectors are copied but wrt still points
        to the original object. Two vectors are considered the same if:
        1. They are the same object (identity), OR
        2. They are both vectors with equal magnitudes

        Args:
            vec_a: First vector (or wrt value, could be string)
            vec_b: Second vector

        Returns:
            True if they refer to the same logical vector
        """
        # Direct identity check
        if vec_a is vec_b:
            return True

        # If vec_a is a string (axis reference), it's not the same as a vector
        if isinstance(vec_a, str):
            return False

        # Both must be vector types
        if not isinstance(vec_a, (Vector, VectorUnknown)):
            return False
        if not isinstance(vec_b, (Vector, VectorUnknown)):
            return False

        # Compare by magnitude - two vectors with the same magnitude
        # and wrt pointing to each other are likely the same logical vector
        # This handles the case where vectors are copied during problem setup
        mag_a = vec_a.magnitude
        mag_b = vec_b.magnitude

        # Handle ellipsis
        if mag_a is ... or mag_b is ...:
            # If both have ellipsis magnitude, compare by other properties
            if mag_a is ... and mag_b is ...:
                # Both unknown magnitude - compare by name if available
                return getattr(vec_a, 'name', None) == getattr(vec_b, 'name', None) and \
                       getattr(vec_a, 'name', None) is not None
            return False

        # Compare magnitudes using Quantity equality
        try:
            return mag_a == mag_b
        except (AttributeError, TypeError):
            return False

    def _compute_interior_angle_at_vertex(self, vertex: Vertex) -> Quantity | None:
        """
        Compute interior angle at a vertex using the vertex-based model.

        The interior angle at a vertex is the angle between the two sides
        meeting at that vertex, measured INSIDE the triangle.

        For the parallelogram law triangle (R = V1 + V2):
        - Vertex A: where V1 and R both START (origin)
        - Vertex B: where V1 ENDS and V2 STARTS (junction)
        - Vertex C: where V2 and R both END (tip)

        The interior angle is computed by considering the "outgoing" direction
        from the vertex along each edge, then finding the angle between them.
        For edges that END at the vertex, the outgoing direction is the
        reverse of the edge direction (direction + 180°).

        Special case: If one vector's wrt references the other vector at this
        vertex (e.g., F_R measured 30° from F_BA), then the interior angle
        is directly the relative angle between them.

        Args:
            vertex: The vertex to compute the angle at

        Returns:
            The interior angle as a Quantity, or None if cannot be computed
        """
        # Get the two sides adjacent to this vertex
        adjacent_sides = _get_adjacent_sides(self, vertex)

        if len(adjacent_sides) != 2:
            return None

        side1, side2 = adjacent_sides

        # Check for relative angle case: one vector references the other as wrt
        # This happens when e.g., F_R is defined as "30° from F_BA"
        relative_angle = self._check_relative_angle_at_vertex(vertex, side1, side2)
        if relative_angle is not None:
            return relative_angle

        if side1.direction is None or side2.direction is None:
            return None

        zero, half, full = _get_angle_constants()

        # Get outgoing direction from this vertex for each side
        # If the side starts at this vertex, outgoing = side.direction
        # If the side ends at this vertex, outgoing = side.direction + 180°
        if side1.start == vertex:
            out1 = side1.direction
        else:
            out1 = side1.direction + half

        if side2.start == vertex:
            out2 = side2.direction
        else:
            out2 = side2.direction + half

        # Normalize both to [0, 360)
        out1 = _normalize_angle(out1)
        out2 = _normalize_angle(out2)

        # Compute the signed angle from out1 to out2 (counterclockwise positive)
        # This tells us which direction we turn when going around the triangle
        signed_diff = out2 - out1

        # Normalize to (-180, 180]
        while signed_diff > half:
            signed_diff = signed_diff - full
        while signed_diff <= Q(-180, "degree"):
            signed_diff = signed_diff + full

        # The interior angle is the absolute value of the signed difference
        # because interior angles are always positive and < 180°
        if signed_diff < zero:
            interior = zero - signed_diff
        else:
            interior = signed_diff

        return interior

    def _compute_interior_angles(self):
        """
        Compute the interior angles using the vertex-based model.

        This method computes all three interior angles and ensures they
        sum to 180°. If the initial computation yields angles that don't
        sum to 180° (which can happen in certain parallelogram law configurations),
        we adjust the angles to form a valid triangle.

        The key insight is that for the parallelogram law triangle:
        - The angle at A (origin) is always correct: |dir(V1) - dir(R)|
        - The angles at B and C may need to be supplemented if they sum to > 180°

        This is because the "outgoing directions" approach can compute the
        exterior angle instead of the interior angle at junction vertices.
        """
        # First pass: compute angles using the vertex-based model
        computed_angles = {}
        for angle_attr, (vertex, opposite_side_attr) in ANGLE_VERTEX_MAP.items():
            angle_qty = self._compute_interior_angle_at_vertex(vertex)
            computed_angles[angle_attr] = (angle_qty, vertex, opposite_side_attr)

        # Check if angles sum to 180°
        zero, half, _ = _get_angle_constants()
        angle_sum = zero
        all_known = True
        for _angle_attr, (angle_qty, _, _) in computed_angles.items():
            if angle_qty is not None:
                angle_sum = angle_sum + angle_qty
            else:
                all_known = False

        # If all angles are known and they don't sum to 180°, we need to correct them
        # This happens when some angles are exterior angles instead of interior
        if all_known:
            tolerance = Q(1, "degree")  # Allow small floating point errors
            expected_sum = Q(180, "degree")

            # Check if we're significantly off from 180°
            diff = angle_sum - expected_sum
            if diff < zero:
                diff = zero - diff

            if diff > tolerance:
                # Angles don't sum to 180° - need to correct
                # The angle at A (origin) is always correct because both sides start there
                # The angles at B and C may be exterior angles (should be supplemented)

                angle_A_qty = computed_angles["angle_A"][0]

                if angle_A_qty is not None:
                    # The angles at B and C should be equal in many cases (isoceles)
                    # or we can use the constraint that they must sum to (180 - A)
                    angle_B_qty = computed_angles["angle_B"][0]
                    angle_C_qty = computed_angles["angle_C"][0]

                    if angle_B_qty is not None and angle_C_qty is not None:
                        # Check if supplementing both B and C gives valid result
                        supp_B = half - angle_B_qty
                        supp_C = half - angle_C_qty

                        new_sum = angle_A_qty + supp_B + supp_C

                        # Check if supplemented angles sum correctly
                        new_diff = new_sum - expected_sum
                        if new_diff < zero:
                            new_diff = zero - new_diff

                        if new_diff < tolerance:
                            # Supplementing B and C works
                            computed_angles["angle_B"] = (supp_B, computed_angles["angle_B"][1], computed_angles["angle_B"][2])
                            computed_angles["angle_C"] = (supp_C, computed_angles["angle_C"][1], computed_angles["angle_C"][2])

        # Create TriangleAngle objects
        for angle_attr, (angle_qty, vertex, opposite_side_attr) in computed_angles.items():
            # Special naming for angle_B (the junction angle)
            if angle_attr == "angle_B" and angle_qty is not None:
                angle_qty.name = f"\\angle(\\vec{{{self.vec_1.name}}}, \\vec{{{self.vec_2.name}}})"

            opposite_side = getattr(self, opposite_side_attr)
            triangle_angle = TriangleAngle(
                angle=angle_qty,
                is_known=angle_qty is not None,
                opposite_side=opposite_side.name,
                vertex=vertex,
            )
            setattr(self, angle_attr, triangle_angle)

    @property
    def sides(self) -> tuple[TriangleSide, TriangleSide, TriangleSide]:
        """All three sides as a tuple."""
        return (self.side_a, self.side_b, self.side_c)

    @property
    def angles(self) -> tuple[TriangleAngle, TriangleAngle, TriangleAngle]:
        """All three angles as a tuple."""
        return (self.angle_A, self.angle_B, self.angle_C)

    @property
    def known_sides(self) -> int:
        """Count of known side magnitudes."""
        return sum(1 for s in self.sides if s.is_known)

    @property
    def known_angles(self) -> int:
        """Count of known interior angles."""
        return sum(1 for a in self.angles if a.is_known)

    def _is_side_resultant(self, side: TriangleSide) -> bool:
        """
        Check if a side represents the resultant vector.

        Args:
            side: The TriangleSide to check

        Returns:
            True if this side is the resultant, False otherwise
        """
        # side_b is always the resultant in our triangle configuration
        if side is self.side_b:
            return True

        # Also check the _is_resultant flag on the original vectors if available
        if self.vec_r is not None and side.name == self.vec_r.name:
            return getattr(self.vec_r, '_is_resultant', False)

        return False

    def _classify_asa_aas(self) -> TriangleCase:
        """
        Classify between ASA and AAS when we have 2+ angles and 1+ side.

        ASA: The known side is between the two known angles (included side)
        AAS: The known side is opposite one of the known angles (non-included)

        The included side for angles at vertices X and Y is the side opposite
        the third vertex Z (which connects X and Y).
        """
        # ASA configurations: (angle1, angle2, included_side)
        # If both angles are known and the included side is known, it's ASA
        asa_configs = [
            ("angle_A", "angle_B", "side_c"),  # angle_A and angle_B -> side_c connects them
            ("angle_A", "angle_C", "side_b"),  # angle_A and angle_C -> side_b connects them
            ("angle_B", "angle_C", "side_a"),  # angle_B and angle_C -> side_a connects them
        ]

        for angle1_attr, angle2_attr, included_side_attr in asa_configs:
            angle1 = getattr(self, angle1_attr)
            angle2 = getattr(self, angle2_attr)
            included_side = getattr(self, included_side_attr)

            if angle1.is_known and angle2.is_known and included_side.is_known:
                return TriangleCase.ASA

        # If we have 2 angles and 1 side but it's not ASA, it's AAS
        return TriangleCase.AAS

    def classify(self) -> TriangleCase:
        """
        Classify the triangle solving case based on known sides and angles.

        The classification determines which solving strategy to use:
        - SAS: Two sides and included angle known → Law of Cosines for third side
        - SSS: Three sides known → Law of Cosines for angles
        - ASA: Two angles and included side → Angle sum + Law of Sines
        - AAS: Two angles and non-included side → Angle sum + Law of Sines
        - SSA: Two sides and non-included angle → Law of Sines (ambiguous case)
        - UNKNOWN: Cannot determine or insufficient information

        With the vertex model:
        - angle_A at vertex A is between side_b and side_c (included for b,c)
        - angle_B at vertex B is between side_a and side_c (included for a,c)
        - angle_C at vertex C is between side_a and side_b (included for a,b)

        Returns:
            TriangleCase enum indicating the solving strategy
        """
        sides = self.known_sides
        angles = self.known_angles

        # SSS: All three sides known
        if sides == 3:
            return TriangleCase.SSS

        # SAS: Two sides + included angle between them
        if sides == 2 and angles >= 1:
            if _check_sas_configuration(self) is not None:
                return TriangleCase.SAS
            # If we have 2 sides and 1 angle but it's not included, it's SSA
            return TriangleCase.SSA

        # ASA or AAS: Two angles + one side
        if angles >= 2 and sides >= 1:
            return self._classify_asa_aas()

        # SSA: Two sides + non-included angle
        if sides == 2 and angles == 1:
            # We have two sides and one angle, but the angle is not between those sides
            return TriangleCase.SSA

        # One side only with one angle (need more info)
        if sides == 1 and angles >= 1:
            return TriangleCase.UNKNOWN

        return TriangleCase.UNKNOWN

    def get_sas_configuration(self) -> dict[str, Any] | None:
        """
        Get the SAS configuration if this is an SAS triangle.

        Returns a dictionary with:
        - known_side_1: First known side (TriangleSide)
        - known_side_2: Second known side (TriangleSide)
        - included_angle: The angle between the two known sides (TriangleAngle)
        - unknown_side: The side to solve for (TriangleSide)
        - unknown_angle_1: First angle to potentially solve (TriangleAngle)
        - unknown_angle_2: Second angle to potentially solve (TriangleAngle)

        Returns None if not an SAS configuration.
        """
        config = _check_sas_configuration(self)
        if config is None:
            return None

        side1_name, side2_name, angle_name, unknown_name, unk_angle1, unk_angle2 = config
        return {
            "known_side_1": getattr(self, side1_name),
            "known_side_2": getattr(self, side2_name),
            "included_angle": getattr(self, angle_name),
            "unknown_side": getattr(self, unknown_name),
            "unknown_angle_1": getattr(self, unk_angle1),
            "unknown_angle_2": getattr(self, unk_angle2),
        }

    def get_included_angle_step(self, included_angle: TriangleAngle) -> dict[str, Any] | None:
        """
        Generate a solution step showing how the included angle was determined.

        For SAS problems, the included angle between two vectors is computed from
        their directions. This method generates a step that shows the calculation
        explicitly so users understand where the angle used in Law of Cosines comes from.

        The calculation accounts for the vertex geometry:
        - The interior angle at a vertex is between the two sides meeting there
        - For sides that END at the vertex, we use the reverse direction (+180°)
        - This ensures we compute the interior (not exterior) angle

        Args:
            included_angle: The TriangleAngle representing the included angle

        Returns:
            A solution step dictionary, or None if the step cannot be generated
        """
        from ..equations.base import SolutionStepBuilder, angle_notation, format_angle, latex_name

        if included_angle.angle is None:
            return None

        # The included angle is at a vertex where two sides meet
        vertex = included_angle.vertex
        if vertex is None:
            return None

        # Get the two sides that form this angle
        adjacent_sides = _get_adjacent_sides(self, vertex)
        if len(adjacent_sides) != 2:
            return None

        side1, side2 = adjacent_sides

        if side1.direction is None or side2.direction is None:
            return None

        # Get vector names for display
        side1_name = side1.name or "V_1"
        side2_name = side2.name or "V_2"

        # Sort names alphanumerically for consistent output (e.g., F_1 before F_2)
        # Also swap sides to match
        if side1_name > side2_name:
            side1_name, side2_name = side2_name, side1_name
            side1, side2 = side2, side1

        # Match side names to original vectors to get correct reference info
        def get_vector_info(side_name: str) -> tuple[str, Quantity] | None:
            """Get (wrt, angle) for the vector matching this side name."""
            if self.vec_1.name == side_name:
                if self.vec_1.angle is ...:
                    return None
                return (self.vec_1.wrt, self.vec_1.angle)
            elif self.vec_2.name == side_name:
                if self.vec_2.angle is ...:
                    return None
                return (self.vec_2.wrt, self.vec_2.angle)
            elif self.vec_r is not None and self.vec_r.name == side_name:
                if self.vec_r.angle is ...:
                    return None
                return (self.vec_r.wrt, self.vec_r.angle)
            return None

        side1_info = get_vector_info(side1_name)
        side2_info = get_vector_info(side2_name)

        if side1_info is None or side2_info is None:
            return None

        side1_ref, side1_angle = side1_info
        side2_ref, side2_angle = side2_info

        # Convert to degrees for display
        side1_angle_deg = side1_angle.to_unit.degree
        side2_angle_deg = side2_angle.to_unit.degree
        result_angle_deg = included_angle.angle.to_unit.degree

        # Format reference axes (strip leading + for cleaner display)
        # Handle wrt being either a string axis or a Vector object
        from ..linalg.vector2 import Vector as VectorClass, VectorUnknown as VectorUnknownClass

        def format_ref_display(ref: str | VectorClass | VectorUnknownClass) -> str:
            """Format a wrt reference for display."""
            if isinstance(ref, (VectorClass, VectorUnknownClass)):
                return ref.name or "ref"
            # String reference
            return ref.lstrip("+") if ref.startswith("+") else ref

        side1_ref_display = format_ref_display(side1_ref)
        side2_ref_display = format_ref_display(side2_ref)

        # Build the target name using the vector names from the sides (already sorted)
        target = angle_notation(side1_name, side2_name)

        # Get the angle values relative to their reference axes
        side1_angle_val = side1_angle_deg.magnitude()
        side2_angle_val = side2_angle_deg.magnitude()
        result_val = result_angle_deg.magnitude()

        # Get absolute directions (from +x axis) for clearer geometric reasoning
        side1_abs_deg = side1.direction.to_unit.degree.magnitude()
        side2_abs_deg = side2.direction.to_unit.degree.magnitude()

        # Format angle values, handling negatives with parentheses
        def fmt_angle_val(val: float) -> str:
            if val < 0:
                return f"({val:.0f}^{{\\circ}})"
            return f"{val:.0f}^{{\\circ}}"

        # Build the angle expressions using the reference axes
        side1_expr = f"\\angle(\\vec{{{side1_ref_display}}}, \\vec{{{latex_name(side1_name)}}})"
        side2_expr = f"\\angle(\\vec{{{side2_ref_display}}}, \\vec{{{latex_name(side2_name)}}})"

        # Try different formulas to find one that matches the computed result
        tolerance = 1.0

        # Formula 1: Sum of relative angles (when both angles "add up")
        sum_rel = abs(side1_angle_val) + abs(side2_angle_val)

        # Formula 2: Difference of relative angles
        diff_rel = abs(abs(side1_angle_val) - abs(side2_angle_val))

        # Formula 3: Using absolute directions
        abs_diff = abs(side1_abs_deg - side2_abs_deg)
        if abs_diff > 180:
            abs_diff = 360 - abs_diff

        if abs(sum_rel - result_val) < tolerance:
            # Sum of relative angles formula
            substitution = (
                f"{target} &= |{side1_expr}| + |{side2_expr}| \\\\\n"
                f"&= |{fmt_angle_val(side1_angle_val)}| + |{fmt_angle_val(side2_angle_val)}| \\\\\n"
                f"&= {format_angle(result_angle_deg, precision=0)} \\\\"
            )
        elif abs(diff_rel - result_val) < tolerance:
            # Difference of relative angles formula
            # Use single absolute value around the difference, not nested absolute values
            substitution = (
                f"{target} &= |{side1_expr} - {side2_expr}| \\\\\n"
                f"&= |{fmt_angle_val(side1_angle_val)} - {fmt_angle_val(side2_angle_val)}| \\\\\n"
                f"&= {format_angle(result_angle_deg, precision=0)} \\\\"
            )
        elif abs(abs_diff - result_val) < tolerance:
            # Absolute direction difference formula
            substitution = (
                f"{target} &= |\\angle(+x, \\vec{{{latex_name(side1_name)}}}) - \\angle(+x, \\vec{{{latex_name(side2_name)}}})| \\\\\n"
                f"&= |{side1_abs_deg:.0f}^{{\\circ}} - {side2_abs_deg:.0f}^{{\\circ}}| \\\\\n"
                f"&= {format_angle(result_angle_deg, precision=0)} \\\\"
            )
        else:
            # Fallback: Show the geometric construction with reference angles
            # This happens when the angle is computed using the full vertex geometry
            substitution = (
                f"{target} &= |{side1_expr}| + |{side2_expr}| \\\\\n"
                f"&= |{fmt_angle_val(side1_angle_val)}| + |{fmt_angle_val(side2_angle_val)}| \\\\\n"
                f"&= {abs(side1_angle_val):.0f}^{{\\circ}} + {abs(side2_angle_val):.0f}^{{\\circ}} \\\\\n"
                f"&= {format_angle(result_angle_deg, precision=0)} \\\\"
            )

        step = SolutionStepBuilder(
            target=target,
            method="Interior Angle at Vertex",
            description="Compute the interior angle between the two known vectors at their junction",
            substitution=substitution,
        )

        return step.build()

    def compute_unknown_direction(self, unknown_side: TriangleSide, known_angle_at_vertex: TriangleAngle) -> Quantity | None:
        """
        Compute the direction of an unknown side using vertex geometry.

        Given an unknown side and a known interior angle at one of its vertices,
        compute the direction of the unknown side.

        The direction is computed by:
        1. Find the vertex where the unknown side starts or ends
        2. Find the other (known) side at that vertex
        3. Use the interior angle to compute two candidate outgoing directions (±)
        4. Use the triangle angle sum rule to select the geometrically consistent direction

        The key insight is that we can validate each candidate direction by computing
        what the third angle (angle_C) would be if that direction were correct. The
        correct direction will give angle_C = 180° - angle_A - angle_B.

        Args:
            unknown_side: The side whose direction we want to compute
            known_angle_at_vertex: The interior angle at one of the unknown side's vertices

        Returns:
            The absolute direction of the unknown side as a Quantity, or None if cannot be computed
        """
        from ..core import Q

        _, half, _ = _get_angle_constants()

        vertex = known_angle_at_vertex.vertex
        if vertex is None:
            return None

        # Get the two sides at this vertex
        sides_at_vertex = _get_adjacent_sides(self, vertex)

        if len(sides_at_vertex) != 2:
            return None

        # Find the known side (not the unknown one)
        known_side = None
        for side in sides_at_vertex:
            if side is not unknown_side and side.direction is not None:
                known_side = side
                break

        if known_side is None:
            return None

        # Get the outgoing direction from this vertex for the known side
        known_dir_from_vertex = known_side.direction_from(vertex)
        if known_dir_from_vertex is None:
            return None

        # The interior angle tells us the angle between the two outgoing directions
        interior_angle = known_angle_at_vertex.angle
        if interior_angle is None:
            return None

        # The unknown side's outgoing direction is known_dir ± interior_angle
        # Compute and normalize both possible directions
        dir_plus = _normalize_angle(known_dir_from_vertex + interior_angle)
        dir_minus = _normalize_angle(known_dir_from_vertex - interior_angle)

        # Determine which direction is geometrically consistent using the triangle angle sum rule.
        # We know angle_A and angle_B. The correct direction will give an angle_C such that:
        #   angle_A + angle_B + angle_C = 180°
        #
        # To compute angle_C for a candidate direction:
        # 1. Find the third vertex (C) where the unknown side meets the other known side
        # 2. Compute the interior angle at C from the arriving directions of both sides

        # Find the third vertex (not the vertex where known_angle_at_vertex is located)
        # For the unknown side, this is the OTHER endpoint
        third_vertex = unknown_side.end if vertex == unknown_side.start else unknown_side.start

        if third_vertex is None:
            # Fallback to heuristic
            if self._is_side_resultant(unknown_side):
                chosen_dir = dir_plus
            else:
                chosen_dir = dir_minus
            # Convert from outgoing direction at vertex to absolute direction
            if vertex == unknown_side.start:
                return chosen_dir
            elif vertex == unknown_side.end:
                return _normalize_angle(chosen_dir - half)
            return None

        # Find the other side at the third vertex (not the unknown side)
        sides_at_third = _get_adjacent_sides(self, third_vertex)
        other_side_at_third = None
        for side in sides_at_third:
            if side is not unknown_side:
                other_side_at_third = side
                break

        if other_side_at_third is None or other_side_at_third.direction is None:
            # Fallback to heuristic if we can't verify geometrically
            if self._is_side_resultant(unknown_side):
                chosen_dir = dir_plus
            else:
                chosen_dir = dir_minus
        else:
            # Get the outgoing direction of the other side at the third vertex
            other_dir_at_third = other_side_at_third.direction_from(third_vertex)

            if other_dir_at_third is None:
                # Fallback
                if self._is_side_resultant(unknown_side):
                    chosen_dir = dir_plus
                else:
                    chosen_dir = dir_minus
            else:
                # Compute expected angle_C from the triangle angle sum rule
                # angle_C = 180° - angle_A - angle_B
                # We need to find angle_A and angle_B
                # known_angle_at_vertex is one of them (angle_A or angle_B depending on vertex)
                # We need to find the other known angle

                known_angle_value = known_angle_at_vertex.angle
                other_known_angle = None

                # Find the other known interior angle (at the junction vertex B)
                for angle in (self.angle_A, self.angle_B, self.angle_C):
                    if angle is not known_angle_at_vertex and angle.is_known and angle.angle is not None:
                        other_known_angle = angle.angle
                        break

                if other_known_angle is None or known_angle_value is None:
                    # Can't verify, use heuristic
                    if self._is_side_resultant(unknown_side):
                        chosen_dir = dir_plus
                    else:
                        chosen_dir = dir_minus
                else:
                    # Expected angle_C
                    expected_angle_C = Q(180, "degree") - known_angle_value - other_known_angle

                    # Compute what angle_C would be for each candidate direction
                    # The outgoing direction at the third vertex for the unknown side
                    # depends on whether the third vertex is the start or end

                    # For dir_plus candidate:
                    if third_vertex == unknown_side.end:
                        # unknown side arrives at third vertex, outgoing = direction + 180
                        unknown_outgoing_plus = _normalize_angle(dir_plus + half)
                    else:
                        # unknown side leaves from third vertex, outgoing = direction
                        unknown_outgoing_plus = dir_plus

                    # Compute angle between the two outgoing directions at third vertex
                    angle_diff_plus = other_dir_at_third - unknown_outgoing_plus
                    zero, _, _ = _get_angle_constants()
                    if angle_diff_plus < zero:
                        angle_diff_plus = zero - angle_diff_plus
                    angle_diff_plus = _normalize_angle(angle_diff_plus)
                    angle_C_plus = _get_interior_angle(angle_diff_plus)

                    # For dir_minus candidate:
                    if third_vertex == unknown_side.end:
                        unknown_outgoing_minus = _normalize_angle(dir_minus + half)
                    else:
                        unknown_outgoing_minus = dir_minus

                    angle_diff_minus = other_dir_at_third - unknown_outgoing_minus
                    if angle_diff_minus < zero:
                        angle_diff_minus = zero - angle_diff_minus
                    angle_diff_minus = _normalize_angle(angle_diff_minus)
                    angle_C_minus = _get_interior_angle(angle_diff_minus)

                    # Compare with expected angle_C to choose the correct direction
                    # Use a tolerance of 1° for comparison
                    tolerance = Q(1, "degree")

                    diff_plus = expected_angle_C - angle_C_plus
                    if diff_plus < zero:
                        diff_plus = zero - diff_plus

                    diff_minus = expected_angle_C - angle_C_minus
                    if diff_minus < zero:
                        diff_minus = zero - diff_minus

                    if diff_plus < tolerance:
                        chosen_dir = dir_plus
                    elif diff_minus < tolerance:
                        chosen_dir = dir_minus
                    else:
                        # Neither matches exactly, pick the closer one
                        if diff_plus < diff_minus:
                            chosen_dir = dir_plus
                        else:
                            chosen_dir = dir_minus

        # Convert from outgoing direction at vertex to absolute direction
        if vertex == unknown_side.start:
            # Outgoing direction IS the absolute direction
            return chosen_dir
        elif vertex == unknown_side.end:
            # Outgoing direction is absolute + 180, so absolute = outgoing - 180
            return _normalize_angle(chosen_dir - half)

        return None

    def __repr__(self) -> str:
        sides = f"sides: a={self.side_a.name}, b={self.side_b.name}, c={self.side_c.name}"
        angle_c_str = f"{self.angle_C.angle.to_unit.degree}" if self.angle_C.angle else "?"
        classification = self.classify().name
        angles = f"angle_C={angle_c_str}"
        return f"Triangle({sides}, {angles}, case={classification})"


def from_vectors(
    vec_1: Vector,
    vec_2: Vector,
    vec_r: Vector | VectorUnknown | None = None
) -> Triangle:
    """
    Create a triangle from two vectors placed tail-to-tip.

    Args:
        vec_1: First vector (from vertex A to vertex B)
        vec_2: Second vector (from vertex B to vertex C)
        vec_r: Optional resultant vector (from vertex A to vertex C).
               Can be a VectorUnknown if the resultant is unknown.

    Returns:
        Triangle with sides and angles computed from the vectors
    """
    return Triangle(vec_1=vec_1, vec_2=vec_2, vec_r=vec_r)


# Populate vertex maps now that all classes are defined
SIDE_VERTEX_MAP.update({
    "side_a": (Vertex.B, Vertex.C),  # C2: from B to C, opposite vertex A
    "side_b": (Vertex.A, Vertex.C),  # R:  from A to C, opposite vertex B
    "side_c": (Vertex.A, Vertex.B),  # C1: from A to B, opposite vertex C
})

ANGLE_VERTEX_MAP.update({
    "angle_A": (Vertex.A, "side_a"),
    "angle_B": (Vertex.B, "side_b"),
    "angle_C": (Vertex.C, "side_c"),
})


# =============================================================================
# Dependency-Based Triangle Builder
# =============================================================================


@dataclass
class VectorAnalysis:
    """
    Analysis of a single vector's known/unknown status.

    Used by the dependency-based triangle builder to determine which
    vectors can form a computable interior angle.
    """

    name: str
    vector: Vector | VectorUnknown
    is_resultant: bool
    magnitude_known: bool
    angle_known: bool

    @property
    def is_fully_known(self) -> bool:
        """Check if both magnitude and angle are known."""
        return self.magnitude_known and self.angle_known

    def __repr__(self) -> str:
        mag = "M" if self.magnitude_known else "m"
        ang = "A" if self.angle_known else "a"
        role = "R" if self.is_resultant else "C"
        return f"{self.name}[{role}:{mag}{ang}]"


@dataclass
class TriangleAssignment:
    """
    Assignment of vectors to triangle roles based on dependency analysis.

    The key insight is that we assign vectors based on which interior angle
    is computable. The side OPPOSITE that computable angle becomes side_c,
    and the two vectors that form the angle become vec_1 and vec_2.

    This ensures that Triangle._compute_interior_angles() will always have
    vectors with known angles to work with.
    """

    # The vector analysis objects for each triangle role
    side_a_analysis: VectorAnalysis  # Vector whose magnitude is side_a
    side_b_analysis: VectorAnalysis  # Vector whose magnitude is side_b
    side_c_analysis: VectorAnalysis  # Vector opposite the computable angle

    # The actual vectors in order for Triangle constructor
    # vec_1 and vec_2 are the vectors that form the computable angle
    vec_1: Vector | VectorUnknown  # Forms angle_C with vec_2
    vec_2: Vector | VectorUnknown  # Forms angle_C with vec_1
    vec_r: Vector | VectorUnknown  # Opposite angle_C (the "unknown" side)


def _analyze_vector(name: str, vec: Vector | VectorUnknown) -> VectorAnalysis:
    """
    Analyze a vector for known/unknown status.

    Args:
        name: Name of the vector
        vec: The Vector or VectorUnknown to analyze

    Returns:
        VectorAnalysis with known/unknown status for magnitude and angle
    """
    from ..linalg.vector2 import VectorUnknown

    is_resultant = getattr(vec, "_is_resultant", False)

    if isinstance(vec, VectorUnknown):
        mag_known = vec.magnitude is not ...
        angle_known = vec.angle is not ...
    else:
        mag_known = vec.magnitude.value is not None
        angle_known = vec.angle.value is not None

    return VectorAnalysis(name, vec, is_resultant, mag_known, angle_known)


def from_vectors_dynamic(
    vectors: dict[str, Vector | VectorUnknown],
) -> Triangle:
    """
    Create a Triangle using dependency analysis to determine vector assignments.

    For parallelogram law, the geometry is:
        - C1 (component 1) goes from A to B
        - C2 (component 2) goes from B to C
        - R (resultant) goes from A to C
        - C1 + C2 = R

    This function:
    1. Identifies which vector is the resultant (has `_is_resultant=True`)
    2. Assigns the two components as vec_1 (C1) and vec_2 (C2)
    3. Assigns the resultant as vec_r (R)
    4. Verifies that an interior angle can be computed

    Args:
        vectors: Dictionary mapping vector names to Vector/VectorUnknown objects.
                 Must contain exactly 3 vectors, with exactly 1 marked as resultant.

    Returns:
        Triangle with vectors assigned based on parallelogram law geometry

    Raises:
        ValueError: If not exactly 3 vectors, or if no interior angle is computable
    """
    from ..linalg.vector2 import Vector, VectorUnknown

    # Analyze all vectors
    analyses: list[VectorAnalysis] = []
    for name, vec in vectors.items():
        if isinstance(vec, Vector | VectorUnknown):
            analyses.append(_analyze_vector(name, vec))

    if len(analyses) != 3:
        raise ValueError(f"Expected 3 vectors, got {len(analyses)}")

    # Separate resultant from components
    resultant_analysis: VectorAnalysis | None = None
    component_analyses: list[VectorAnalysis] = []

    for analysis in analyses:
        if analysis.is_resultant:
            if resultant_analysis is not None:
                raise ValueError("Multiple vectors marked as resultant")
            resultant_analysis = analysis
        else:
            component_analyses.append(analysis)

    if resultant_analysis is None:
        raise ValueError("No vector marked as resultant (_is_resultant=True)")

    if len(component_analyses) != 2:
        raise ValueError(f"Expected 2 component vectors, got {len(component_analyses)}")

    # Verify that the problem is solvable:
    # Option 1: At least 2 vectors with known directions (can compute interior angle)
    # Option 2: All 3 magnitudes known (SSS case - use Law of Cosines for angles)
    known_dir_count = sum(1 for a in analyses if a.angle_known)
    known_mag_count = sum(1 for a in analyses if a.magnitude_known)

    if known_dir_count < 2 and known_mag_count < 3:
        raise ValueError(
            "Cannot solve - need either at least 2 vectors with known angles, "
            "or all 3 magnitudes known (SSS). "
            f"Vectors: {analyses}"
        )

    # Assign components as vec_1 (C1) and vec_2 (C2)
    # The order matters for consistent naming, but doesn't affect the geometry
    vec_1_analysis = component_analyses[0]
    vec_2_analysis = component_analyses[1]

    # Create triangle with proper parallelogram law geometry:
    # - vec_1 (C1): A→B = side_c
    # - vec_2 (C2): B→C = side_a
    # - vec_r (R):  A→C = side_b
    return Triangle(
        vec_1=vec_1_analysis.vector,
        vec_2=vec_2_analysis.vector,
        vec_r=resultant_analysis.vector,
    )
