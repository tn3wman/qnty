"""
Common equation module for engineering problem solving.

This module provides reusable equation classes that generate solution steps
dynamically when invoked. Each equation encapsulates both the mathematical
computation and the step-by-step solution documentation.

Example usage for Problem 2-1:
    >>> from qnty.equations import LawOfCosines, LawOfSines, AngleBetween, AngleSum
    >>>
    >>> # Step 1: Calculate angle between forces
    >>> angle_eq = AngleBetween(
    ...     target="∠(F_1,F_2)",
    ...     vec1_name="F_1", vec1_angle_deg=60.0, vec1_ref="x",
    ...     vec2_name="F_2", vec2_angle_deg=15.0, vec2_ref="-x",
    ... )
    >>> angle_between, step1 = angle_eq.solve()  # 45°
    >>>
    >>> # Step 2: Law of Cosines for resultant magnitude
    >>> loc = LawOfCosines(
    ...     target="|F_R| using Eq 1",
    ...     side_a_name="F_1", side_a_value=450.0,
    ...     side_b_name="F_2", side_b_value=700.0,
    ...     angle_name="∠(F_1,F_2)", angle_deg=45.0,
    ...     unit="N"
    ... )
    >>> F_R, step2 = loc.solve()  # 497.0 N
    >>>
    >>> # Step 3: Law of Sines for angle
    >>> los = LawOfSines(
    ...     target="∠(F_1,F_R) using Eq 2",
    ...     angle_name="∠(F_1,F_R)",
    ...     opposite_side_name="F_2", opposite_side_value=700.0,
    ...     known_angle_name="∠(F_1,F_2)", known_angle_deg=45.0,
    ...     known_side_name="F_R", known_side_value=497.0,
    ... )
    >>> angle_F1_FR, step3 = los.solve()  # 95.2°
    >>>
    >>> # Step 4: Final angle calculation
    >>> angle_sum = AngleSum(
    ...     target="∠(x,F_R) with respect to +x",
    ...     base_angle_name="∠(x,F_1)", base_angle_deg=60.0,
    ...     offset_angle_name="∠(F_1,F_R)", offset_angle_deg=95.2,
    ... )
    >>> theta_R, step4 = angle_sum.solve()  # 155.2°
"""

from .angle_finder import AngleBetween, AngleSum
from .base import SolutionStepBuilder
from .law_of_cosines import LawOfCosines
from .law_of_sines import LawOfSines

__all__ = [
    "LawOfCosines",
    "LawOfSines",
    "AngleBetween",
    "AngleSum",
    "SolutionStepBuilder",
]
