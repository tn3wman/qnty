"""
Converters between DTOs and Qnty domain objects.

Provides functions to convert between JSON-serializable DTOs and
the high-performance internal Qnty objects (_Vector, _Point, Quantity).

These converters are the bridge between frontend state management
and the core computational engine.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..utils.shared_utilities import convert_coords_to_unit
from .dto import PointDTO, QuantityDTO, VectorDTO

if TYPE_CHECKING:
    from ..core.quantity import Quantity
    from ..spatial.point import _Point
    from ..spatial.vector import _Vector


def vector_to_dto(
    vec: "_Vector",
    output_unit: str | None = None,
    output_angle_unit: str = "degree",
) -> VectorDTO:
    """
    Convert an internal _Vector to a JSON-serializable VectorDTO.

    Args:
        vec: Internal _Vector object to convert
        output_unit: Desired unit for output (uses vector's unit if None)
        output_angle_unit: Unit for angle output ("degree" or "radian")

    Returns:
        VectorDTO with all fields populated

    Examples:
        >>> from qnty.spatial.vectors import create_vector_polar
        >>> vec = create_vector_polar(magnitude=100, angle=30, unit="N", name="F1")
        >>> dto = vector_to_dto(vec, output_unit="N")
        >>> dto.magnitude  # approximately 100.0
        >>> dto.angle  # approximately 30.0
    """
    from ..core.unit import ureg

    # Determine output unit
    if output_unit is None:
        if vec._unit is not None:
            output_unit = vec._unit.symbol
        else:
            output_unit = "N"  # Default

    # Get coordinates in SI (internal storage)
    coords_si = vec._coords.copy()

    # Convert to output unit
    target_unit = ureg.resolve(output_unit)
    coords_output = convert_coords_to_unit(list(coords_si), target_unit)

    # Calculate magnitude
    magnitude = math.sqrt(sum(c**2 for c in coords_output))

    # Calculate angle in xy-plane (from +x axis)
    angle: float | None = None
    if abs(coords_output[0]) > 1e-12 or abs(coords_output[1]) > 1e-12:
        angle_rad = math.atan2(coords_output[1], coords_output[0])
        if output_angle_unit.lower() in ("degree", "degrees", "deg"):
            angle = math.degrees(angle_rad)
        else:
            angle = angle_rad

    # Get original angle info if available (for reporting)
    original_angle = getattr(vec, "_original_angle", None)
    original_wrt = getattr(vec, "_original_wrt", "+x")

    return VectorDTO(
        u=coords_output[0],
        v=coords_output[1],
        w=coords_output[2] if len(coords_output) > 2 else 0.0,
        unit=output_unit,
        name=getattr(vec, "name", None),
        magnitude=magnitude,
        angle=original_angle if original_angle is not None else angle,
        angle_unit=output_angle_unit,
        angle_wrt=original_wrt,
        plane="xy",  # Default for 2D
        is_known=getattr(vec, "is_known", True),
        is_resultant=getattr(vec, "is_resultant", False),
    )


def dto_to_vector(dto: VectorDTO) -> "_Vector":
    """
    Convert a VectorDTO to an internal _Vector for computation.

    If the DTO has polar coordinates (magnitude and angle), those are used.
    Otherwise, Cartesian components (u, v, w) are used.

    Args:
        dto: VectorDTO to convert

    Returns:
        Internal _Vector object

    Raises:
        ValueError: If unit cannot be resolved

    Examples:
        >>> dto = VectorDTO(u=0, v=0, magnitude=100, angle=30, unit="N", name="F1")
        >>> vec = dto_to_vector(dto)
        >>> vec.magnitude  # Returns Quantity with value ~100
    """
    from ..spatial.vectors import create_vector_cartesian, create_vector_polar

    if dto.is_polar_input():
        # Create from polar coordinates
        return create_vector_polar(
            magnitude=dto.magnitude,  # type: ignore (checked by is_polar_input)
            unit=dto.unit,
            angle=dto.angle,  # type: ignore (checked by is_polar_input)
            angle_unit=dto.angle_unit,
            wrt=dto.angle_wrt,
            plane=dto.plane,
            name=dto.name,
        )
    else:
        # Create from Cartesian components
        return create_vector_cartesian(
            u=dto.u,
            v=dto.v,
            w=dto.w,
            unit=dto.unit,
            name=dto.name,
        )


def point_to_dto(point: "_Point", output_unit: str | None = None) -> PointDTO:
    """
    Convert an internal _Point to a JSON-serializable PointDTO.

    Args:
        point: Internal _Point object to convert
        output_unit: Desired unit for output (uses point's unit if None)

    Returns:
        PointDTO with coordinates in the specified unit

    Examples:
        >>> from qnty.spatial.points import create_point_cartesian
        >>> pt = create_point_cartesian(x=3, y=4, z=0, unit="m", name="A")
        >>> dto = point_to_dto(pt, output_unit="m")
        >>> dto.x, dto.y  # (3.0, 4.0)
    """
    from ..core.unit import ureg

    # Determine output unit
    if output_unit is None:
        if point._unit is not None:
            output_unit = point._unit.symbol
        else:
            output_unit = "m"  # Default

    # Get coordinates in SI (internal storage)
    coords_si = point._coords.copy()

    # Convert to output unit
    target_unit = ureg.resolve(output_unit)
    coords_output = convert_coords_to_unit(list(coords_si), target_unit)

    return PointDTO(
        x=coords_output[0],
        y=coords_output[1],
        z=coords_output[2] if len(coords_output) > 2 else 0.0,
        unit=output_unit,
        name=getattr(point, "name", None),
    )


def dto_to_point(dto: PointDTO) -> "_Point":
    """
    Convert a PointDTO to an internal _Point for computation.

    Args:
        dto: PointDTO to convert

    Returns:
        Internal _Point object

    Raises:
        ValueError: If unit cannot be resolved

    Examples:
        >>> dto = PointDTO(x=3.0, y=4.0, z=0.0, unit="m", name="A")
        >>> point = dto_to_point(dto)
    """
    from ..spatial.points import create_point_cartesian

    return create_point_cartesian(
        x=dto.x,
        y=dto.y,
        z=dto.z,
        unit=dto.unit,
        name=dto.name,
    )


def quantity_to_dto(qty: "Quantity", output_unit: str | None = None) -> QuantityDTO:
    """
    Convert a Quantity to a JSON-serializable QuantityDTO.

    Args:
        qty: Internal Quantity object to convert
        output_unit: Desired unit for output (uses quantity's preferred unit if None)

    Returns:
        QuantityDTO with value in the specified unit

    Examples:
        >>> from qnty import Force
        >>> f = Force("F").set(100).newton
        >>> dto = quantity_to_dto(f, output_unit="N")
        >>> dto.value  # 100.0
    """
    from ..core.unit import ureg

    # Determine output unit
    if output_unit is None:
        if qty.preferred is not None:
            output_unit = qty.preferred.symbol
        else:
            # Try to get SI unit for dimension
            si_unit = ureg.si_unit_for(qty.dim)
            output_unit = si_unit.symbol if si_unit else "unknown"

    # Get value in output unit
    target_unit = ureg.resolve(output_unit)
    if target_unit is not None and qty.value is not None:
        value = qty.magnitude(target_unit)
    else:
        value = qty.value if qty.value is not None else 0.0

    # Get dimension name
    dim_name = qty.dim.name if qty.dim else None

    return QuantityDTO(
        value=value,
        unit=output_unit,
        name=qty.name,
        dimension=dim_name,
    )


def dto_to_quantity(dto: QuantityDTO) -> "Quantity":
    """
    Convert a QuantityDTO to an internal Quantity.

    Note: This requires knowing the dimension type to create the correct
    Quantity subclass. If dimension is not specified, creates a generic
    Quantity.

    Args:
        dto: QuantityDTO to convert

    Returns:
        Internal Quantity object

    Raises:
        ValueError: If unit cannot be resolved
    """
    from ..core.quantity import Quantity
    from ..core.unit import ureg

    # Resolve unit to get dimension
    unit = ureg.resolve(dto.unit)
    if unit is None:
        raise ValueError(f"Unknown unit: {dto.unit}")

    return Quantity(
        name=dto.name or "quantity",
        dim=unit.dim,
        value=dto.value * unit.si_factor,  # Store in SI
        preferred=unit,
    )
