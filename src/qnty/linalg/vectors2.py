"""
Factory functions for creating Vector objects.
"""

from __future__ import annotations

from types import EllipsisType

from ..coordinates import Cartesian, CoordinateSystem
from ..core.quantity import Q
from .vector2 import Vector, VectorUnknown


def create_vectors_polar(
    magnitude: float | EllipsisType,
    magnitude_unit: str,
    angle: float | EllipsisType,
    angle_unit: str = "degree",
    wrt: str = "+x",
    coordinate_system: CoordinateSystem | None = None,
    name: str | None = None,
) -> Vector | VectorUnknown:
    """
    Create a vector using polar coordinates.

    Args:
        magnitude: The magnitude value, or ... for unknown
        magnitude_unit: The unit for magnitude (e.g., "N", "lbf", "m")
        angle: The angle value, or ... for unknown
        angle_unit: The unit for angle (default: "degree")
        wrt: The axis the angle is measured from (default: "+x")
        coordinate_system: The coordinate system (default: Cartesian)
        name: Optional name for the vector

    Returns:
        Vector if all values are known, VectorUnknown if any value is ...

    Examples:
        >>> from qnty.spatial.vectors2 import create_vectors_polar
        >>>
        >>> # Simple vector in standard Cartesian coordinates
        >>> F = create_vectors_polar(100, "N", 30, name="F_1")
        >>>
        >>> # Vector measured from +y axis
        >>> F2 = create_vectors_polar(100, "N", 45, wrt="+y", name="F_2")
        >>>
        >>> # Vector with unknown magnitude
        >>> F3 = create_vectors_polar(..., "N", 30, name="F_3")
        >>>
        >>> # Vector with unknown angle
        >>> F4 = create_vectors_polar(100, "N", ..., name="F_4")
    """
    if coordinate_system is None:
        coordinate_system = Cartesian()

    # Check if any values are unknown (ellipsis)
    magnitude_is_unknown = magnitude is ...
    angle_is_unknown = angle is ...

    if magnitude_is_unknown or angle_is_unknown:
        return VectorUnknown(
            magnitude=... if magnitude_is_unknown else Q(magnitude, magnitude_unit),  # type: ignore[arg-type]
            angle=... if angle_is_unknown else Q(angle, angle_unit),  # type: ignore[arg-type]
            wrt=wrt,
            coordinate_system=coordinate_system,
            name=name,
        )
    else:
        return Vector(
            magnitude=Q(magnitude, magnitude_unit),  # type: ignore[arg-type]
            angle=Q(angle, angle_unit),  # type: ignore[arg-type]
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
        _is_resultant=True,
    )

    # Store component vectors for later computation
    resultant._component_vectors = list(vectors)  # type: ignore[attr-defined]

    return resultant


def create_resultant_polar(
    *vectors: Vector | VectorUnknown,
    magnitude: float | EllipsisType,
    unit: str,
    angle: float | EllipsisType,
    angle_unit: str = "degree",
    wrt: str = "+x",
    coordinate_system: CoordinateSystem | None = None,
    name: str = "F_R",
) -> Vector | VectorUnknown:
    """
    Create a resultant vector with known or unknown magnitude/angle from component vectors.

    This function creates a resultant vector (either Vector or VectorUnknown depending
    on whether magnitude/angle are known) while also storing the component vectors
    that make up this resultant.

    Args:
        *vectors: Variable number of component vectors that sum to this resultant
        magnitude: The magnitude value, or ... for unknown
        unit: The unit for magnitude (e.g., "N", "lbf", "m")
        angle: The angle value, or ... for unknown
        angle_unit: The unit for angle (default: "degree")
        wrt: The axis the angle is measured from (default: "+x")
        coordinate_system: The coordinate system (default: Cartesian)
        name: Name for the resultant vector (default "F_R")

    Returns:
        Vector if all values are known, VectorUnknown if any value is ...
        Both types will have _component_vectors attribute set.

    Examples:
        >>> from qnty.linalg.vectors2 import create_vectors_polar, create_resultant_polar
        >>>
        >>> # Define component vectors (with unknowns)
        >>> F_1 = create_vectors_polar(..., "N", 30, name="F_1")
        >>> F_2 = create_vectors_polar(..., "N", 60, name="F_2")
        >>>
        >>> # Create a known resultant from unknown components
        >>> F_R = create_resultant_polar(F_1, F_2, magnitude=500, unit="N", angle=0, wrt="+y")
        >>>
        >>> # Create an unknown resultant from known components
        >>> F_1 = create_vectors_polar(100, "N", 30, name="F_1")
        >>> F_2 = create_vectors_polar(200, "N", 60, name="F_2")
        >>> F_R = create_resultant_polar(F_1, F_2, magnitude=..., unit="N", angle=..., wrt="+x")
    """
    if coordinate_system is None:
        # Get coordinate system from first vector if available
        coordinate_system = Cartesian()
        if vectors:
            first_vec = vectors[0]
            if hasattr(first_vec, "coordinate_system") and first_vec.coordinate_system is not None:
                coordinate_system = first_vec.coordinate_system

    # Check if any values are unknown (ellipsis)
    magnitude_is_unknown = magnitude is ...
    angle_is_unknown = angle is ...

    if magnitude_is_unknown or angle_is_unknown:
        resultant: Vector | VectorUnknown = VectorUnknown(
            magnitude=... if magnitude_is_unknown else Q(magnitude, unit),  # type: ignore[arg-type]
            angle=... if angle_is_unknown else Q(angle, angle_unit),  # type: ignore[arg-type]
            wrt=wrt,
            coordinate_system=coordinate_system,
            name=name,
            _is_resultant=True,
        )
    else:
        resultant = Vector(
            magnitude=Q(magnitude, unit),  # type: ignore[arg-type]
            angle=Q(angle, angle_unit),  # type: ignore[arg-type]
            wrt=wrt,
            coordinate_system=coordinate_system,
            name=name,
            _is_resultant=True,
        )

    # Store component vectors for later computation
    resultant._component_vectors = list(vectors)  # type: ignore[attr-defined]

    return resultant
