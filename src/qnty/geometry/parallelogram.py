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

Key angles (all measured at the common origin A):
    θ₁₂ = angle between F₁ and F₂
    θ₁ᵣ = angle between F₁ and R
    θ₂ᵣ = angle between F₂ and R

This model is simpler than the Triangle model because:
1. All vectors share a common tail at vertex A
2. The angle between any two vectors is simply the difference in their absolute directions
3. No need for "outgoing direction from vertex" logic or direction reversal
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from types import EllipsisType
from typing import TYPE_CHECKING, Any

from ..core.quantity import Q, Quantity
from ..linalg.vector2 import Vector, VectorUnknown

if TYPE_CHECKING:
    pass


class ParallelogramCase(Enum):
    """Classification of parallelogram solving cases based on known quantities."""
    SAS = auto()    # Two sides (components) + angle between them → Law of Cosines for resultant
    SSS = auto()    # Three sides → Law of Cosines for angles
    ASA = auto()    # Two angles + one side → Law of Sines for other sides
    AAS = auto()    # Two angles + non-included side → Angle sum + Law of Sines
    SSA = auto()    # Two sides + non-included angle → Law of Sines (ambiguous)
    UNKNOWN = auto()  # Cannot determine case or insufficient information


@dataclass
class ParallelogramSide:
    """
    Represents one side (vector) of the parallelogram.

    All sides originate from the common vertex A (origin).

    Attributes:
        magnitude: Length of the side as a Quantity, or ... if unknown
        is_known: Whether the magnitude is known
        name: Name for this side (e.g., "F_1", "F_R")
        direction: Absolute direction of the vector (from +x axis) as Quantity
        is_resultant: Whether this side is the resultant (diagonal)
        wrt: Reference axis for the relative angle (e.g., "+x", "-y")
        relative_angle: Angle relative to the reference axis
    """
    magnitude: Quantity | EllipsisType
    is_known: bool
    name: str | None = None
    direction: Quantity | None = None
    is_resultant: bool = False
    wrt: str = "+x"
    relative_angle: Quantity | None = None


@dataclass
class ParallelogramAngle:
    """
    Represents an angle between two sides at the common origin.

    In a parallelogram, all relevant angles are at the origin vertex A.

    Attributes:
        angle: The angle as a Quantity
        is_known: Whether the angle is known
        side1_name: Name of the first side forming this angle
        side2_name: Name of the second side forming this angle
    """
    angle: Quantity | None
    is_known: bool
    side1_name: str | None = None
    side2_name: str | None = None


def _normalize_angle(angle: Quantity) -> Quantity:
    """
    Normalize an angle to the range [0, 360) degrees.
    """
    zero = Q(0, "degree")
    full = Q(360, "degree")

    while angle >= full:
        angle = angle - full
    while angle < zero:
        angle = angle + full

    return angle


def _get_interior_angle(angle: Quantity) -> Quantity:
    """
    Convert an angle difference to an interior angle (0-180°).
    """
    half = Q(180, "degree")
    full = Q(360, "degree")

    if angle > half:
        angle = full - angle

    return angle


@dataclass
class Parallelogram:
    """
    A parallelogram formed by two vectors with a common origin.

    The parallelogram has vertices A, B, C, D where:
        A: Common origin (tail of F₁, F₂, and R)
        B: Tip of F₁
        C: Tip of F₂
        D: Tip of R (opposite corner)

    Sides (vectors from origin A):
        side_1: First component vector F₁ (from A to B)
        side_2: Second component vector F₂ (from A to C)
        side_r: Resultant vector R (from A to D, the diagonal)

    Angles (all at origin A):
        angle_12: Between F₁ and F₂
        angle_1r: Between F₁ and R
        angle_2r: Between F₂ and R

    Key property: angle_12 = angle_1r + angle_2r (R lies between F₁ and F₂)
    """

    # The original vectors
    vec_1: Vector | VectorUnknown  # F₁: first component
    vec_2: Vector | VectorUnknown  # F₂: second component
    vec_r: Vector | VectorUnknown | None = None  # R: resultant

    # Sides (populated in __post_init__)
    side_1: ParallelogramSide = field(init=False)  # F₁
    side_2: ParallelogramSide = field(init=False)  # F₂
    side_r: ParallelogramSide = field(init=False)  # R

    # Angles at origin (populated in __post_init__)
    angle_12: ParallelogramAngle = field(init=False)  # Between F₁ and F₂
    angle_1r: ParallelogramAngle = field(init=False)  # Between F₁ and R
    angle_2r: ParallelogramAngle = field(init=False)  # Between F₂ and R

    def __post_init__(self):
        """Initialize sides and compute angles."""
        self._assemble_sides()
        self._compute_angles()

    def _assemble_sides(self):
        """Create ParallelogramSide objects from the input vectors."""
        from ..equations.angle_finder import get_absolute_angle

        def create_side(vec: Vector | VectorUnknown | None, is_resultant: bool = False) -> ParallelogramSide:
            if vec is None:
                return ParallelogramSide(
                    magnitude=...,
                    is_known=False,
                    name="R",
                    direction=None,
                    is_resultant=is_resultant,
                    wrt="+x",
                    relative_angle=None,
                )

            # Extract magnitude and known status
            if isinstance(vec, VectorUnknown) and vec.magnitude is ...:
                mag: Quantity | EllipsisType = ...
                mag_known = False
            else:
                mag = vec.magnitude
                if mag is ...:
                    mag_known = False
                else:
                    mag_known = mag.value is not None and mag.value != 0

            # Get direction
            direction: Quantity | None = None
            relative_angle: Quantity | None = None
            if not (isinstance(vec, VectorUnknown) and vec.angle is ...):
                try:
                    direction = get_absolute_angle(vec)
                    relative_angle = vec.angle
                except (AttributeError, TypeError, ValueError):
                    pass

            return ParallelogramSide(
                magnitude=mag,
                is_known=mag_known,
                name=vec.name,
                direction=direction,
                is_resultant=is_resultant or getattr(vec, '_is_resultant', False),
                wrt=vec.wrt,
                relative_angle=relative_angle,
            )

        self.side_1 = create_side(self.vec_1, is_resultant=False)
        self.side_2 = create_side(self.vec_2, is_resultant=False)
        self.side_r = create_side(self.vec_r, is_resultant=True)

    def _compute_angles(self):
        """
        Compute interior angles of the FORCE TRIANGLE (not the parallelogram).

        The force triangle has vertices:
            A: Origin (tail of F₁, F₂, and R)
            B: Junction (tip of F₁, tail of translated F₂)
            C: Tip of resultant (tip of translated F₂)

        Key insight: The interior angle at B (junction) is what we use in Law of Cosines.
        At the junction:
            - F₁ ENDS at B, so its "outgoing" direction from B is F₁_dir + 180°
            - F₂ STARTS at B, so its "outgoing" direction from B is F₂_dir

        The interior angle at B = |(F₁_dir + 180°) - F₂_dir|, normalized to [0, 180].

        The angles angle_1r and angle_2r are at vertices A and C respectively,
        computed using similar vertex-based geometry.
        """
        half = Q(180, "degree")

        def compute_junction_angle(
            ending_side: ParallelogramSide,
            starting_side: ParallelogramSide
        ) -> ParallelogramAngle:
            """Compute interior angle at junction where ending_side ends and starting_side starts."""
            if ending_side.direction is None or starting_side.direction is None:
                return ParallelogramAngle(
                    angle=None,
                    is_known=False,
                    side1_name=ending_side.name,
                    side2_name=starting_side.name,
                )

            # At junction: ending_side's outgoing direction = its direction + 180°
            # starting_side's outgoing direction = its direction
            outgoing_ending = _normalize_angle(ending_side.direction + half)
            outgoing_starting = starting_side.direction

            # Difference of outgoing directions
            diff = outgoing_ending - outgoing_starting
            diff = _normalize_angle(diff)

            # Convert to interior angle [0, 180]
            angle = _get_interior_angle(diff)

            return ParallelogramAngle(
                angle=angle,
                is_known=True,
                side1_name=ending_side.name,
                side2_name=starting_side.name,
            )

        def compute_origin_angle(
            side_a: ParallelogramSide,
            side_b: ParallelogramSide
        ) -> ParallelogramAngle:
            """Compute interior angle at origin where both sides start."""
            if side_a.direction is None or side_b.direction is None:
                return ParallelogramAngle(
                    angle=None,
                    is_known=False,
                    side1_name=side_a.name,
                    side2_name=side_b.name,
                )

            # At origin: both sides start here, so outgoing directions = their directions
            diff = side_a.direction - side_b.direction
            diff = _normalize_angle(diff)
            angle = _get_interior_angle(diff)

            return ParallelogramAngle(
                angle=angle,
                is_known=True,
                side1_name=side_a.name,
                side2_name=side_b.name,
            )

        def compute_tip_angle(
            ending_side_1: ParallelogramSide,
            ending_side_2: ParallelogramSide
        ) -> ParallelogramAngle:
            """Compute interior angle at tip where both sides end."""
            if ending_side_1.direction is None or ending_side_2.direction is None:
                return ParallelogramAngle(
                    angle=None,
                    is_known=False,
                    side1_name=ending_side_1.name,
                    side2_name=ending_side_2.name,
                )

            # At tip: both sides end here, so outgoing directions = their directions + 180°
            outgoing_1 = _normalize_angle(ending_side_1.direction + half)
            outgoing_2 = _normalize_angle(ending_side_2.direction + half)

            diff = outgoing_1 - outgoing_2
            diff = _normalize_angle(diff)
            angle = _get_interior_angle(diff)

            return ParallelogramAngle(
                angle=angle,
                is_known=True,
                side1_name=ending_side_1.name,
                side2_name=ending_side_2.name,
            )

        # angle_12: Interior angle at junction B (F₁ ends, F₂ starts)
        # This is the angle used in Law of Cosines: c² = a² + b² - 2ab·cos(θ)
        self.angle_12 = compute_junction_angle(self.side_1, self.side_2)

        # angle_1r: Interior angle at origin A (between F₁ and R, both start here)
        self.angle_1r = compute_origin_angle(self.side_1, self.side_r)

        # angle_2r: Interior angle at tip C (between F₂ and R, both end here)
        self.angle_2r = compute_tip_angle(self.side_2, self.side_r)

    @property
    def sides(self) -> tuple[ParallelogramSide, ParallelogramSide, ParallelogramSide]:
        """All three sides (F₁, F₂, R) as a tuple."""
        return (self.side_1, self.side_2, self.side_r)

    @property
    def angles(self) -> tuple[ParallelogramAngle, ParallelogramAngle, ParallelogramAngle]:
        """All three angles as a tuple."""
        return (self.angle_12, self.angle_1r, self.angle_2r)

    @property
    def known_sides(self) -> int:
        """Count of known side magnitudes."""
        return sum(1 for s in self.sides if s.is_known)

    @property
    def known_angles(self) -> int:
        """Count of known angles."""
        return sum(1 for a in self.angles if a.is_known)

    def classify(self) -> ParallelogramCase:
        """
        Classify the problem based on known quantities.

        For parallelogram law problems:
        - SAS: Two components known (magnitudes + directions) → solve for resultant
        - ASA: Two directions known + resultant magnitude → solve for component magnitudes
        - SSA: One component + resultant known, other component's direction known → solve
        - SSS: All magnitudes known → solve for directions/angles

        Returns:
            ParallelogramCase enum indicating the solving strategy
        """
        sides = self.known_sides
        angles = self.known_angles

        # SSS: All three magnitudes known
        if sides == 3:
            return ParallelogramCase.SSS

        # SAS: Two sides known + angle between them known
        # This is the typical case when both components are fully specified
        if sides == 2 and self.angle_12.is_known:
            # Check which two sides are known
            if self.side_1.is_known and self.side_2.is_known and not self.side_r.is_known:
                return ParallelogramCase.SAS
            elif self.side_1.is_known and self.side_r.is_known and not self.side_2.is_known:
                return ParallelogramCase.SAS
            elif self.side_2.is_known and self.side_r.is_known and not self.side_1.is_known:
                return ParallelogramCase.SAS

        # ASA: Two angles known + one side known (typically the resultant)
        # This happens when both component directions are known but magnitudes unknown
        if angles >= 2 and sides >= 1:
            # Check if the known side is between the two known angles
            # In our case, if angle_1r and angle_2r are known, and side_r is known
            if self.angle_1r.is_known and self.angle_2r.is_known and self.side_r.is_known:
                return ParallelogramCase.ASA
            # Or if angle_12 is known along with one angle to resultant
            if self.angle_12.is_known and (self.angle_1r.is_known or self.angle_2r.is_known):
                if self.side_1.is_known or self.side_2.is_known or self.side_r.is_known:
                    return ParallelogramCase.ASA

        # SSA: Two sides + one angle (not between those sides)
        if sides == 2 and angles >= 1:
            return ParallelogramCase.SSA

        # AAS: Two angles + one side (not between the angles)
        if angles >= 2 and sides >= 1:
            return ParallelogramCase.AAS

        return ParallelogramCase.UNKNOWN

    def get_sas_configuration(self) -> dict[str, Any] | None:
        """
        Get the SAS configuration if this is an SAS case.

        Returns a dictionary with:
        - known_side_1: First known side (ParallelogramSide)
        - known_side_2: Second known side (ParallelogramSide)
        - included_angle: The angle between the two known sides (ParallelogramAngle)
        - unknown_side: The side to solve for (ParallelogramSide)

        Returns None if not an SAS configuration.
        """
        if self.classify() != ParallelogramCase.SAS:
            return None

        # Find the two known sides and the unknown side
        known_sides = [s for s in self.sides if s.is_known]
        unknown_sides = [s for s in self.sides if not s.is_known]

        if len(known_sides) != 2 or len(unknown_sides) != 1:
            return None

        known_side_1 = known_sides[0]
        known_side_2 = known_sides[1]
        unknown_side = unknown_sides[0]

        # Find the angle between the two known sides
        included_angle = None
        for angle in self.angles:
            names = {angle.side1_name, angle.side2_name}
            if known_side_1.name in names and known_side_2.name in names:
                included_angle = angle
                break

        if included_angle is None or not included_angle.is_known:
            return None

        return {
            "known_side_1": known_side_1,
            "known_side_2": known_side_2,
            "included_angle": included_angle,
            "unknown_side": unknown_side,
        }

    def get_included_angle_step(self, included_angle: ParallelogramAngle) -> dict[str, Any] | None:
        """
        Generate a solution step showing how the included angle was determined.

        For parallelogram law, the angle between two vectors at the origin is
        simply the difference of their absolute directions:
            θ = |direction₁ - direction₂|

        Args:
            included_angle: The ParallelogramAngle representing the angle between vectors

        Returns:
            A solution step dictionary, or None if the step cannot be generated
        """
        from ..equations.base import SolutionStepBuilder, angle_notation, format_angle, latex_name

        if included_angle.angle is None:
            return None

        # Get the two sides that form this angle
        side1_name = included_angle.side1_name
        side2_name = included_angle.side2_name

        if side1_name is None or side2_name is None:
            return None

        # Find the actual side objects
        side1 = None
        side2 = None
        for side in self.sides:
            if side.name == side1_name:
                side1 = side
            elif side.name == side2_name:
                side2 = side

        if side1 is None or side2 is None:
            return None

        if side1.direction is None or side2.direction is None:
            return None

        # Sort names alphanumerically for consistent output
        if side1_name > side2_name:
            side1_name, side2_name = side2_name, side1_name
            side1, side2 = side2, side1

        # Get absolute directions in degrees
        side1_abs_deg = side1.direction.to_unit.degree.magnitude()
        side2_abs_deg = side2.direction.to_unit.degree.magnitude()
        result_angle_deg = included_angle.angle.to_unit.degree

        # Build the target name
        target = angle_notation(side1_name, side2_name)

        # For parallelogram law, the formula is simple:
        # θ = |direction₁ - direction₂| (normalized to interior angle)
        substitution = (
            f"{target} &= |\\angle(+x, \\vec{{{latex_name(side1_name)}}}) - "
            f"\\angle(+x, \\vec{{{latex_name(side2_name)}}})| \\\\\n"
            f"&= |{side1_abs_deg:.0f}^{{\\circ}} - {side2_abs_deg:.0f}^{{\\circ}}| \\\\\n"
            f"&= {format_angle(result_angle_deg, precision=0)} \\\\"
        )

        step = SolutionStepBuilder(
            target=target,
            method="Angle Between Vectors",
            description="Compute the angle between the two vectors at their common origin",
            substitution=substitution,
        )

        return step.build()

    def compute_unknown_direction(
        self,
        unknown_side: ParallelogramSide,
        known_angle: ParallelogramAngle
    ) -> Quantity | None:
        """
        Compute the direction of an unknown side using a known angle.

        In a parallelogram, if we know:
        - The direction of one side (e.g., F₁)
        - The angle between that side and another (e.g., angle_1r)

        Then the direction of the other side is:
            direction_r = direction_1 ± angle_1r

        The sign depends on whether the unknown is CCW (+) or CW (-) from the known.

        Args:
            unknown_side: The side whose direction we want to compute
            known_angle: The angle from a known side to the unknown side

        Returns:
            The absolute direction of the unknown side as a Quantity, or None
        """
        # Find the known side in the angle
        known_side = None
        for side in self.sides:
            if side.direction is not None and side is not unknown_side:
                if side.name in {known_angle.side1_name, known_angle.side2_name}:
                    known_side = side
                    break

        if known_side is None or known_side.direction is None:
            return None

        if known_angle.angle is None:
            return None

        # Try both + and - to find which gives a valid configuration
        dir_plus = _normalize_angle(known_side.direction + known_angle.angle)
        dir_minus = _normalize_angle(known_side.direction - known_angle.angle)

        # If the unknown side is the resultant, it should be "between" the two components
        # Use geometric validation to pick the correct direction
        if unknown_side.is_resultant:
            # The resultant should be between the two components
            # This typically means we pick the direction that makes sense geometrically
            # For now, we'll use a simple heuristic: resultant is usually CCW from comp1
            return dir_plus
        else:
            # For component sides, use the opposite convention
            return dir_minus

    def __repr__(self) -> str:
        sides = f"F1={self.side_1.name}, F2={self.side_2.name}, R={self.side_r.name}"
        angle = f"angle_12={self.angle_12.angle}" if self.angle_12.angle else "angle_12=?"
        case = self.classify().name
        return f"Parallelogram({sides}, {angle}, case={case})"


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
        Parallelogram with sides and angles computed from the vectors
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
    # Separate resultant from components
    resultant = None
    components = []

    for name, vec in vectors.items():
        if isinstance(vec, (Vector, VectorUnknown)):
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

    # Create parallelogram with components as vec_1, vec_2 and resultant as vec_r
    return Parallelogram(
        vec_1=components[0],
        vec_2=components[1],
        vec_r=resultant,
    )
