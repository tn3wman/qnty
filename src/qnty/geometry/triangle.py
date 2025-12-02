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
from typing import TYPE_CHECKING

from ..core.quantity import Q, Quantity

if TYPE_CHECKING:
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

    # The original vectors
    vec_1: Vector
    vec_2: Vector
    vec_r: Vector | None = None

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

        The key insight: when vectors are placed tail-to-tip, the interior angle
        at vertex C (where V1 tip meets V2 tail) is related to the directions
        of V1 and V2 in their coordinate systems.

        With alphanumeric ordering:
        - angle_A is opposite side_a (F_1) - unknown until solved
        - angle_B is opposite side_b (F_2) - unknown until solved
        - angle_C is opposite side_c (F_R) - computed from vector directions
        """
        from ..equations.angle_finder import get_absolute_angle

        # Get absolute directions of the vectors (as Quantities)
        abs_dir_v1 = get_absolute_angle(self.vec_1)
        abs_dir_v2 = get_absolute_angle(self.vec_2)

        # Get the straight angle from the coordinate system
        # This is the sum of the two axis angles (angle_between gives the separation)
        coord_sys = self.vec_1.coordinate_system
        straight_angle = coord_sys.axis1_angle + coord_sys.axis2_angle + coord_sys.angle_between

        # Direction difference (all Quantity arithmetic)
        dir_diff = abs_dir_v2 - abs_dir_v1

        # Interior angle at C (where V1 tip meets V2 tail): straight_angle - |dir_diff|
        # We need absolute value - check if negative by comparing to zero
        zero_angle = Q(0, "degree")
        if (dir_diff - zero_angle).value < 0:
            dir_diff = zero_angle - dir_diff  # Make positive

        # Normalize to within one full rotation
        full_rotation = Q(360, "degree")
        half_rotation = Q(180, "degree")

        # Keep subtracting full rotation until within range
        while (dir_diff - full_rotation).value > 0:
            dir_diff = dir_diff - full_rotation

        # If greater than half rotation, use the supplementary angle
        if (dir_diff - half_rotation).value > 0:
            dir_diff = full_rotation - dir_diff

        # Interior angle at C (opposite side_c which is the resultant)
        angle_C = half_rotation - dir_diff
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
