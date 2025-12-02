"""
Factory functions for creating Vector objects.
"""

from __future__ import annotations

from ..coordinates import Cartesian, CoordinateSystem
from ..core.quantity import Q
from .vector2 import Vector, VectorUnknown


def create_vectors_polar(
    magnitude: float,
    magnitude_unit: str,
    angle: float,
    angle_unit: str = "degree",
    wrt: str = "+x",
    coordinate_system: CoordinateSystem | None = None,
    name: str | None = None,
) -> Vector:
    """
    Create a vector using polar coordinates.

    Args:
        magnitude: The magnitude value
        magnitude_unit: The unit for magnitude (e.g., "N", "lbf", "m")
        angle: The angle value
        angle_unit: The unit for angle (default: "degree")
        wrt: The axis the angle is measured from (default: "+x")
        coordinate_system: The coordinate system (default: Cartesian)
        name: Optional name for the vector

    Returns:
        Vector object with the specified magnitude and angle

    Examples:
        >>> from qnty.spatial.vectors2 import create_vectors_polar
        >>>
        >>> # Simple vector in standard Cartesian coordinates
        >>> F = create_vectors_polar(100, "N", 30, name="F_1")
        >>>
        >>> # Vector measured from +y axis
        >>> F2 = create_vectors_polar(100, "N", 45, wrt="+y", name="F_2")
    """
    if coordinate_system is None:
        coordinate_system = Cartesian()

    return Vector(
        magnitude=Q(magnitude, magnitude_unit),
        angle=Q(angle, angle_unit),
        wrt=wrt,
        coordinate_system=coordinate_system,
        name=name,
    )


def create_vector_resultant(
    *vectors: Vector | VectorUnknown,
    name: str = "F_R",
) -> VectorUnknown:
    """
    Create a resultant vector placeholder from component vectors.

    This function creates a VectorUnknown with both magnitude and angle
    unknown (represented by ellipsis ...). The component vectors are stored
    so the solver can compute the actual values by summing them.

    Args:
        *vectors: Variable number of vectors to sum
        name: Name for the resultant vector (default "F_R")

    Returns:
        VectorUnknown with unknown magnitude and angle, component vectors stored

    Examples:
        >>> from qnty.linalg.vectors2 import create_vectors_polar, create_vector_resultant
        >>>
        >>> # Define component vectors
        >>> F_1 = create_vectors_polar(450, "N", 60, wrt="+x", name="F_1")
        >>> F_2 = create_vectors_polar(700, "N", 15, wrt="-x", name="F_2")
        >>>
        >>> # Create resultant (magnitude and angle will be solved)
        >>> F_R = create_vector_resultant(F_1, F_2)
    """
    # Get coordinate system from first vector if available
    coordinate_system = Cartesian()
    if vectors:
        first_vec = vectors[0]
        if hasattr(first_vec, "coordinate_system") and first_vec.coordinate_system is not None:
            coordinate_system = first_vec.coordinate_system

    # Create the resultant with unknown magnitude and angle
    resultant = VectorUnknown(
        magnitude=...,
        angle=...,
        wrt="+x",
        coordinate_system=coordinate_system,
        name=name,
    )

    # Store component vectors for later computation
    resultant._component_vectors = list(vectors)  # type: ignore[attr-defined]

    return resultant
