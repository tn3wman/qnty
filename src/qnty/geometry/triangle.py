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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from ..core.quantity import Q, Quantity
from ..linalg.vector2 import Vector, VectorUnknown


class TriangleCase(Enum):
    """Classification of triangle solving cases based on known quantities."""
    SAS = auto()  # Two sides + included angle → Law of Cosines
    SSS = auto()  # Three sides → Law of Cosines for angles
    ASA = auto()  # Two angles + included side → Angle sum + Law of Sines
    AAS = auto()  # Two angles + non-included side → Angle sum + Law of Sines
    SSA = auto()  # Two sides + non-included angle → Law of Sines (ambiguous)
    UNKNOWN = auto()  # Cannot determine case or insufficient information


@dataclass
class TriangleSide:
    """
    Represents one side of a triangle.

    Attributes:
        magnitude: Length of the side as a Quantity, or ... if unknown
        is_known: Whether the magnitude is known
        name: Optional name for this side (e.g., "F_1", "F_R")
    """

    magnitude: Quantity | type(...)  # Can be Quantity or ellipsis
    is_known: bool
    name: str | None = None


@dataclass
class TriangleAngle:
    """
    Represents one interior angle of a triangle.

    Attributes:
        angle: The interior angle as a Quantity
        is_known: Whether the angle is known
        opposite_side: Name of the side opposite to this angle
    """

    angle: Quantity | None
    is_known: bool
    opposite_side: str | None = None


@dataclass
class Triangle:
    """
    A triangle formed by assembling two vectors tail-to-tip.

    The triangle has three vertices:
    - A: tail of vector 1
    - B: tip of vector 1 = tail of vector 2
    - C: tip of vector 2

    Sides are named alphanumerically to match vector names:
    - side_a: vector 1 (F_1) - from A to B
    - side_b: vector 2 (F_2) - from B to C
    - side_c: resultant (F_R) - from A to C

    Interior angles are opposite their corresponding sides:
    - angle_A: opposite side_a (at vertex between side_b and side_c)
    - angle_B: opposite side_b (at vertex between side_a and side_c)
    - angle_C: opposite side_c (at vertex between side_a and side_b)

    The interior angles sum to the straight angle of the coordinate system.
    """

    # The original vectors (can be Vector or VectorUnknown)
    vec_1: Vector | VectorUnknown
    vec_2: Vector | VectorUnknown
    vec_r: Vector | VectorUnknown | None = None

    # Sides of the triangle (magnitudes) - alphanumeric order
    side_a: TriangleSide = field(init=False)  # Vector 1 (F_1) magnitude
    side_b: TriangleSide = field(init=False)  # Vector 2 (F_2) magnitude
    side_c: TriangleSide = field(init=False)  # Resultant (F_R) magnitude

    # Interior angles - opposite their corresponding sides
    angle_A: TriangleAngle = field(init=False)  # Opposite side_a
    angle_B: TriangleAngle = field(init=False)  # Opposite side_b
    angle_C: TriangleAngle = field(init=False)  # Opposite side_c (where V1 tip meets V2 tail)

    def __post_init__(self):
        """Assemble the triangle from the input vectors."""
        self._assemble_sides()
        self._compute_interior_angles()

    def _assemble_sides(self):
        """Set up the triangle sides from vector magnitudes (alphanumeric order)."""
        from ..linalg.vector2 import VectorUnknown

        def get_magnitude_and_known(vec):
            """Extract magnitude and known status from a Vector or VectorUnknown."""
            if isinstance(vec, VectorUnknown):
                if vec.magnitude is ...:
                    return ..., False
                else:
                    mag = vec.magnitude
                    return mag, (mag.value is not None and mag.value != 0)
            else:
                mag = vec.magnitude
                return mag, (mag.value is not None and mag.value != 0)

        # Side a = vector 1 (F_1) - from A to B
        v1_mag, v1_known = get_magnitude_and_known(self.vec_1)
        self.side_a = TriangleSide(
            magnitude=v1_mag,
            is_known=v1_known,
            name=self.vec_1.name,
        )

        # Side b = vector 2 (F_2) - from B to C
        v2_mag, v2_known = get_magnitude_and_known(self.vec_2)
        self.side_b = TriangleSide(
            magnitude=v2_mag,
            is_known=v2_known,
            name=self.vec_2.name,
        )

        # Side c = resultant (F_R) - from A to C
        if self.vec_r is not None:
            vr_mag, vr_known = get_magnitude_and_known(self.vec_r)
            self.side_c = TriangleSide(
                magnitude=vr_mag,
                is_known=vr_known,
                name=self.vec_r.name,
            )
        else:
            # No resultant provided - create placeholder with ellipsis
            self.side_c = TriangleSide(
                magnitude=...,
                is_known=False,
                name="R",
            )

    def _compute_interior_angles(self):
        """
        Compute the interior angles of the triangle from vector directions.

        The triangle is formed by:
        - vec_1 and vec_2: the two vectors with known directions
        - vec_r: the third vector (opposite the computable angle)

        The interior angle computation depends on the geometric relationship:

        Case 1: Both vec_1 and vec_2 are component vectors (tail-to-tip)
            - They meet at a junction where vec_1 ends and vec_2 starts
            - Interior angle = 180° - |dir_diff|

        Case 2: One is a component, one is the resultant (share a vertex)
            - If both START at the same vertex: angle = |dir_diff|
            - If both END at the same vertex: angle = |dir_diff|
            - The interior angle is simply the absolute difference in directions
        """
        from ..equations.angle_finder import get_absolute_angle

        # Get absolute directions of the vectors (as Quantities)
        abs_dir_v1 = get_absolute_angle(self.vec_1)
        abs_dir_v2 = get_absolute_angle(self.vec_2)

        # Direction difference (all Quantity arithmetic)
        dir_diff = abs_dir_v2 - abs_dir_v1

        # Make positive (absolute value)
        zero_angle = Q(0, "degree")
        if (dir_diff - zero_angle).value < 0:
            dir_diff = zero_angle - dir_diff

        # Normalize to within one full rotation
        full_rotation = Q(360, "degree")
        half_rotation = Q(180, "degree")

        while (dir_diff - full_rotation).value > 0:
            dir_diff = dir_diff - full_rotation

        # If greater than half rotation, use the supplementary angle
        if (dir_diff - half_rotation).value > 0:
            dir_diff = full_rotation - dir_diff

        # Determine the geometric relationship
        v1_is_resultant = getattr(self.vec_1, "_is_resultant", False)
        v2_is_resultant = getattr(self.vec_2, "_is_resultant", False)

        # Case 1: Both are components (tail-to-tip configuration)
        # Interior angle at junction = 180 - dir_diff
        if not v1_is_resultant and not v2_is_resultant:
            angle_C = half_rotation - dir_diff
        # Case 2: One is resultant, one is component (share a vertex)
        # Interior angle = dir_diff (the direct angle between them)
        else:
            angle_C = dir_diff
        # Set a proper LaTeX name for the angle (used in equation display)
        angle_C.name = f"\\angle(\\vec{{{self.vec_1.name}}}, \\vec{{{self.vec_2.name}}})"

        self.angle_C = TriangleAngle(
            angle=angle_C,
            is_known=True,  # Computable from vector directions
            opposite_side=self.side_c.name,
        )

        # Angles A and B depend on the side lengths - initially unknown
        # They will be computed when solving the triangle
        self.angle_A = TriangleAngle(
            angle=None,
            is_known=False,
            opposite_side=self.side_a.name,
        )

        self.angle_B = TriangleAngle(
            angle=None,
            is_known=False,
            opposite_side=self.side_b.name,
        )

    @property
    def known_sides(self) -> int:
        """Count of known side magnitudes."""
        return sum(1 for s in [self.side_a, self.side_b, self.side_c] if s.is_known)

    @property
    def known_angles(self) -> int:
        """Count of known interior angles."""
        return sum(1 for a in [self.angle_A, self.angle_B, self.angle_C] if a.is_known)

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

        The "included angle" is angle_C (opposite side_c, the resultant), which
        is computed from the vector directions when both V1 and V2 have known angles.

        Returns:
            TriangleCase enum indicating the solving strategy
        """
        sides = self.known_sides
        angles = self.known_angles

        # SSS: All three sides known
        if sides == 3:
            return TriangleCase.SSS

        # SAS: Two sides + included angle
        # The included angle is angle_C (at vertex C, opposite the resultant)
        if sides == 2 and self.angle_C.is_known:
            # Check that we have sides a and b (not c)
            if self.side_a.is_known and self.side_b.is_known:
                return TriangleCase.SAS
            # If we have one component side and the resultant, check which angle we have
            # This would be a different configuration - needs more analysis
            # For now, return SSA as it's two sides with a non-included angle
            return TriangleCase.SSA

        # ASA or AAS: Two angles + one side
        if angles >= 2:
            if sides >= 1:
                # Determine if ASA or AAS based on which side is known
                # ASA: The known side is between the two known angles
                # AAS: The known side is not between the two known angles
                if self.angle_A.is_known and self.angle_B.is_known:
                    # Both component angles known - need third angle
                    # If side_c (resultant) is known, it's the included side → ASA
                    if self.side_c.is_known:
                        return TriangleCase.ASA
                    return TriangleCase.AAS
                if self.angle_A.is_known and self.angle_C.is_known:
                    # If side_b (opposite angle_B) is known, it's not included → AAS
                    if self.side_b.is_known:
                        return TriangleCase.AAS
                    # If side_a (opposite angle_A) is known, it's not included → AAS
                    if self.side_a.is_known:
                        return TriangleCase.AAS
                    return TriangleCase.ASA
                if self.angle_B.is_known and self.angle_C.is_known:
                    if self.side_a.is_known:
                        return TriangleCase.AAS
                    if self.side_b.is_known:
                        return TriangleCase.AAS
                    return TriangleCase.ASA
                return TriangleCase.ASA  # Default to ASA if we have 2 angles + 1 side

        # SSA: Two sides + non-included angle
        if sides == 2 and angles == 1:
            # We have two sides and one angle, but the angle is not between those sides
            return TriangleCase.SSA

        # One side only with one angle (need more info)
        if sides == 1 and angles >= 1:
            return TriangleCase.UNKNOWN

        return TriangleCase.UNKNOWN

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


def _find_computable_interior_angle(
    analyses: list[VectorAnalysis],
) -> tuple[VectorAnalysis, tuple[VectorAnalysis, VectorAnalysis]] | None:
    """
    Find which vector is opposite a computable interior angle.

    In a triangle, an interior angle can only be computed if BOTH vectors
    that form it have known directions (angles). This function finds such
    a pair and returns the vector opposite the computable angle.

    Args:
        analyses: List of VectorAnalysis for all 3 vectors

    Returns:
        Tuple of (opposite_vector_analysis, (forming_vec_1, forming_vec_2))
        or None if no interior angle is computable
    """
    for i, opposite in enumerate(analyses):
        # The other two vectors form the angle opposite this one
        others = [a for j, a in enumerate(analyses) if j != i]
        if len(others) == 2 and others[0].angle_known and others[1].angle_known:
            return opposite, (others[0], others[1])
    return None


def from_vectors_dynamic(
    vectors: dict[str, Vector | VectorUnknown],
) -> Triangle:
    """
    Create a Triangle using dependency analysis to determine vector assignments.

    This factory function analyzes the known/unknown status of each vector's
    magnitude and angle to determine the optimal assignment of vectors to
    triangle roles. The key insight is:

    1. An interior angle can only be computed if BOTH vectors forming it
       have known directions (angles)
    2. The side OPPOSITE that computable angle is what we typically solve for
    3. By assigning vectors dynamically, we can handle any combination of
       knowns/unknowns

    Args:
        vectors: Dictionary mapping vector names to Vector/VectorUnknown objects.
                 Must contain exactly 3 vectors.

    Returns:
        Triangle with vectors assigned based on dependency analysis

    Raises:
        ValueError: If not exactly 3 vectors, or if no interior angle is computable

    Example:
        >>> # Problem where F_1 is unknown, F_2 and F_R are known
        >>> vectors = {"F_1": vec_unknown, "F_2": vec_known, "F_R": resultant}
        >>> triangle = from_vectors_dynamic(vectors)
        >>> # Triangle will be built with F_2 and F_R forming angle_C,
        >>> # and F_1 opposite (as side_c)
    """
    from ..linalg.vector2 import Vector, VectorUnknown

    # Analyze all vectors
    analyses: list[VectorAnalysis] = []
    for name, vec in vectors.items():
        if isinstance(vec, (Vector, VectorUnknown)):
            analyses.append(_analyze_vector(name, vec))

    if len(analyses) != 3:
        raise ValueError(f"Expected 3 vectors, got {len(analyses)}")

    # Find which interior angle is computable
    result = _find_computable_interior_angle(analyses)
    if result is None:
        raise ValueError(
            "Cannot compute any interior angle - need at least 2 vectors with known angles. "
            f"Vectors: {analyses}"
        )

    opposite_vec, forming_vecs = result

    # Build the triangle assignment:
    # - vec_1 and vec_2 are the vectors that form the computable angle
    # - vec_r (side_c) is the vector opposite the computable angle
    assignment = TriangleAssignment(
        side_a_analysis=forming_vecs[0],
        side_b_analysis=forming_vecs[1],
        side_c_analysis=opposite_vec,
        vec_1=forming_vecs[0].vector,
        vec_2=forming_vecs[1].vector,
        vec_r=opposite_vec.vector,
    )

    # Create triangle with the assigned vectors
    # vec_1 and vec_2 form angle_C, vec_r is opposite angle_C
    return Triangle(
        vec_1=assignment.vec_1,
        vec_2=assignment.vec_2,
        vec_r=assignment.vec_r,
    )
