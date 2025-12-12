"""
Factory functions for creating Vector objects.

Supports both polar (magnitude/angle) and cartesian (x/y) representations.
"""

from __future__ import annotations

from types import EllipsisType

from ..algebra.functions import atan2, cos, sin, sqrt
from ..coordinates import Cartesian, CoordinateSystem
from ..core.quantity import Q
from ..equations.angle_reference import AngleDirection
from .vector2 import Vector, VectorUnknown


def create_vectors_polar(
    magnitude: float | EllipsisType,
    magnitude_unit: str,
    angle: float | EllipsisType,
    angle_unit: str = "degree",
    wrt: str | Vector | VectorUnknown = "+x",
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
        wrt: The reference for angle measurement - either an axis string (e.g., "+x", "-y")
            or another Vector (for angles measured relative to another vector's direction)
        coordinate_system: The coordinate system (default: Cartesian)
        name: Optional name for the vector

    Returns:
        Vector if all values are known, VectorUnknown if any value is ...

    Examples:
        >>> from qnty.linalg.vectors2 import create_vectors_polar
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
        >>>
        >>> # Vector measured relative to another vector
        >>> F_ref = create_vectors_polar(200, "N", 45, name="F_ref")
        >>> F5 = create_vectors_polar(100, "N", 30, wrt=F_ref, name="F_5")
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
        # Create Quantities
        mag_qty = Q(magnitude, magnitude_unit)
        angle_qty = Q(angle, angle_unit)

        # Try to compute absolute angle from +x axis to get x, y components
        # For simple axis references (like "+x", "-y"), compute the reference angle
        x_qty = None
        y_qty = None

        if isinstance(wrt, str):
            try:
                ref_angle = coordinate_system.get_axis_angle(wrt)
                abs_angle = ref_angle + angle_qty

                # Compute x, y components from absolute angle
                x_result = mag_qty * cos(abs_angle)
                y_result = mag_qty * sin(abs_angle)

                # Ensure we have Quantity objects (not Expressions)
                from ..algebra.nodes import Expression
                if isinstance(x_result, Expression):
                    x_result = x_result.evaluate({})
                if isinstance(y_result, Expression):
                    y_result = y_result.evaluate({})

                # Convert back to original unit (multiplication converts to SI)
                x_qty = x_result.to_unit(magnitude_unit)
                y_qty = y_result.to_unit(magnitude_unit)
            except ValueError:
                # wrt is a string like "F_2" which is a vector name, not an axis
                # We'll compute x, y lazily when they're accessed
                pass

        # If x, y couldn't be computed, create placeholder values
        # These will be computed later via get_absolute_angle when x/y are accessed
        if x_qty is None or y_qty is None:
            # For vectors with wrt reference to another vector, we can't compute x, y
            # until we know the reference vector's direction. Use placeholders.
            # The x/y properties in Vector will need to fall back to computing from angle.
            x_qty = Q(0.0, magnitude_unit)  # Placeholder
            y_qty = Q(0.0, magnitude_unit)  # Placeholder

        return Vector(
            _x=x_qty,  # type: ignore[arg-type]
            _y=y_qty,  # type: ignore[arg-type]
            _z=None,
            magnitude=mag_qty,
            angle=angle_qty,
            wrt=wrt,
            coordinate_system=coordinate_system,
            name=name,
        )


def create_vector_resultant(
    *vectors: Vector | VectorUnknown,
    wrt: str | Vector | VectorUnknown | None = None,
    angle_dir: AngleDirection | str = AngleDirection.COUNTERCLOCKWISE,
    coordinate_system: CoordinateSystem | None = None,
    name: str = "F_R",
) -> VectorUnknown:
    """
    Create a resultant vector placeholder from component vectors.

    This function creates a VectorUnknown with both magnitude and angle
    unknown (represented by ellipsis ...). The component vectors are stored
    so the solver can compute the actual values by summing them.

    Args:
        *vectors: Variable number of vectors to sum
        wrt: The reference for angle measurement - either an axis string (e.g., "+x", "+u"),
            another Vector, or None. If None, defaults to the first axis of the coordinate
            system (e.g., "+x" for Cartesian, "+u" for Oblique with axis1_label="u").
        angle_dir: Direction for measuring the resultant angle - clockwise (CW) or
            counterclockwise (CCW) from the reference axis. Accepts AngleDirection enum
            or strings: "counterclockwise", "ccw", "clockwise", "cw".
            Default: AngleDirection.COUNTERCLOCKWISE
        coordinate_system: The coordinate system for the resultant. If None, uses the
            coordinate system from the first vector, or Cartesian if no vectors provided.
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
        >>>
        >>> # Create resultant with angle measured clockwise from +y axis
        >>> F_R = create_vector_resultant(F_1, F_2, wrt="+y", angle_dir="cw")
    """
    # Normalize angle_dir to AngleDirection enum
    if isinstance(angle_dir, str):
        angle_dir_lower = angle_dir.lower()
        if angle_dir_lower in ("counterclockwise", "ccw"):
            angle_dir = AngleDirection.COUNTERCLOCKWISE
        elif angle_dir_lower in ("clockwise", "cw"):
            angle_dir = AngleDirection.CLOCKWISE
        else:
            raise ValueError(f"Unknown angle_dir: {angle_dir}. Use 'counterclockwise', 'ccw', 'clockwise', or 'cw'")

    # Determine coordinate system
    if coordinate_system is None:
        # Get coordinate system from first vector if available
        coordinate_system = Cartesian()
        if vectors:
            first_vec = vectors[0]
            if hasattr(first_vec, "coordinate_system") and first_vec.coordinate_system is not None:
                coordinate_system = first_vec.coordinate_system

    # Determine wrt (reference axis) - default to first axis of coordinate system
    if wrt is None:
        wrt = f"+{coordinate_system.axis1_label}"

    # Create the resultant with unknown magnitude and angle
    resultant = VectorUnknown(
        magnitude=...,
        angle=...,
        wrt=wrt,
        coordinate_system=coordinate_system,
        name=name,
        _is_resultant=True,
    )

    # Store component vectors for later computation
    resultant._component_vectors = list(vectors)  # type: ignore[attr-defined]

    # Store angle direction for solver to use when reporting the result
    resultant._angle_dir = angle_dir  # type: ignore[attr-defined]

    return resultant


def create_resultant_polar(
    *vectors: Vector | VectorUnknown,
    magnitude: float | EllipsisType,
    unit: str,
    angle: float | EllipsisType,
    angle_unit: str = "degree",
    wrt: str | Vector | VectorUnknown = "+x",
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
        wrt: The reference for angle measurement - either an axis string (e.g., "+x", "-y")
            or another Vector (for angles measured relative to another vector's direction)
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
        # Create Quantities
        mag_qty = Q(magnitude, unit)
        angle_qty = Q(angle, angle_unit)

        # Compute x, y components from angle
        if isinstance(wrt, str):
            ref_angle = coordinate_system.get_axis_angle(wrt)
            abs_angle = ref_angle + angle_qty
        else:
            abs_angle = angle_qty

        x_qty = mag_qty * cos(abs_angle)
        y_qty = mag_qty * sin(abs_angle)

        # Ensure we have Quantity objects
        from ..algebra.nodes import Expression
        if isinstance(x_qty, Expression):
            x_qty = x_qty.evaluate({})
        if isinstance(y_qty, Expression):
            y_qty = y_qty.evaluate({})

        resultant = Vector(
            _x=x_qty,  # type: ignore[arg-type]
            _y=y_qty,  # type: ignore[arg-type]
            _z=None,
            magnitude=mag_qty,
            angle=angle_qty,
            wrt=wrt,
            coordinate_system=coordinate_system,
            name=name,
            _is_resultant=True,
        )

    # Store component vectors for later computation
    resultant._component_vectors = list(vectors)  # type: ignore[attr-defined]

    return resultant


def create_vectors_cartesian(
    x: float,
    y: float,
    z: float = 0.0,
    unit: str = 'N',
    name: str | None = None,
) -> Vector:
    """
    Create a vector using Cartesian (rectangular) components.

    This factory function creates a Vector from x, y (and optionally z) components.
    The magnitude and angle are computed automatically for backward compatibility.

    Args:
        x: The x-component value (coefficient of i unit vector)
        y: The y-component value (coefficient of j unit vector)
        unit: The unit for components (e.g., "N", "lbf", "m")
        z: The z-component value (coefficient of k unit vector) - None for 2D vectors
        name: Optional name for the vector

    Returns:
        Vector with stored components and computed magnitude/angle

    Examples:
        >>> from qnty.linalg.vectors2 import create_vectors_cartesian
        >>>
        >>> # Create 2D vector {200i + 346j} N
        >>> F_1 = create_vectors_cartesian(200, 346, "N", name="F_1")
        >>> print(F_1.x)  # 200 N
        >>> print(F_1.y)  # 346 N
        >>>
        >>> # Create 3D vector {50i + 40j + 30k} N
        >>> F_2 = create_vectors_cartesian(50, 40, "N", z=30, name="F_2")
        >>> print(F_2.x)  # 50 N
        >>> print(F_2.y)  # 40 N
        >>> print(F_2.z)  # 30 N
    """
    # Create Quantities for the components
    x_qty = Q(x, unit)
    y_qty = Q(y, unit)
    z_qty = Q(z, unit) if z is not None else None

    # Compute magnitude
    if z_qty is not None:
        # 3D: sqrt(x² + y² + z²)
        mag_result = sqrt(x_qty * x_qty + y_qty * y_qty + z_qty * z_qty)
        # For 3D, angle is not meaningful in the 2D polar sense
        angle_qty = Q(0.0, "degree")
    else:
        # 2D: sqrt(x² + y²)
        mag_result = sqrt(x_qty * x_qty + y_qty * y_qty)
        # Compute angle: atan2(y, x) returns radians
        angle_result = atan2(y_qty, x_qty)
        # Ensure we have Quantity objects (not Expressions)
        from ..algebra.nodes import Expression
        if isinstance(angle_result, Expression):
            angle_qty = angle_result.evaluate({})
        else:
            angle_qty = angle_result

    # Ensure magnitude is a Quantity (not Expression)
    from ..algebra.nodes import Expression
    if isinstance(mag_result, Expression):
        mag_qty = mag_result.evaluate({})
    else:
        mag_qty = mag_result

    return Vector(
        _x=x_qty,
        _y=y_qty,
        _z=z_qty,
        magnitude=mag_qty,  # type: ignore[arg-type]
        angle=angle_qty,  # type: ignore[arg-type]
        wrt="+x",
        coordinate_system=Cartesian(),
        name=name,
    )


def create_vector_from_ratio(
    magnitude: float,
    unit: str,
    u: float,
    v: float,
    coordinate_system: CoordinateSystem | None = None,
    name: str | None = None,
) -> Vector:
    """
    Create a 2D vector using magnitude and direction ratios.

    This factory function provides a convenient way to define vectors using direction
    ratios, which are common in statics problems where directions are given
    as integer ratios (like 3-4-5, 5-12-13, 8-15-17 right triangles).

    The ratios define the relative proportions in each direction. The vector
    has the specified magnitude along that direction.

    Args:
        magnitude: Vector magnitude
        u: First component ratio (positive or negative, typically x-direction)
        v: Second component ratio (positive or negative, typically y-direction)
        unit: Unit for vector magnitude (e.g., "N", "lbf", "m")
        coordinate_system: The coordinate system (default: Cartesian)
        name: Optional vector name

    Returns:
        Vector object with computed angle and reference axis

    Raises:
        ValueError: If ratios are both zero

    Examples:
        >>> from qnty.linalg.vectors2 import create_vector_from_ratio
        >>>
        >>> # Vector with magnitude 130N in direction 5-12 (like a 5-12-13 triangle)
        >>> F = create_vector_from_ratio(magnitude=130, u=5, v=12, unit="N")
        >>> # Angle will be computed from the dominant axis
        >>>
        >>> # Vector pointing in negative x and positive y direction
        >>> F2 = create_vector_from_ratio(magnitude=100, u=-3, v=4, unit="N")
    """
    from ..equations.angle_finder import angle_from_ratio

    if coordinate_system is None:
        coordinate_system = Cartesian()

    angle, wrt = angle_from_ratio(
        u, v,
        axis1_label=coordinate_system.axis1_label,
        axis2_label=coordinate_system.axis2_label,
    )

    # Create magnitude Quantity
    mag_qty = Q(magnitude, unit)

    # Compute x, y from the direction ratios
    # For direction ratios u:v, the unit vector is (u, v) / sqrt(u² + v²)
    # So the components are: x = mag * u / sqrt(u² + v²), y = mag * v / sqrt(u² + v²)
    ratio_mag = (u * u + v * v) ** 0.5
    x_val = magnitude * u / ratio_mag
    y_val = magnitude * v / ratio_mag

    x_qty = Q(x_val, unit)
    y_qty = Q(y_val, unit)

    return Vector(
        _x=x_qty,
        _y=y_qty,
        _z=None,
        magnitude=mag_qty,
        angle=angle,
        wrt=wrt,
        coordinate_system=coordinate_system,
        name=name,
    )


def create_vectors_direction_angles(
    magnitude: float,
    unit: str,
    alpha: float,
    beta: float,
    gamma: float,
    angle_unit: str = "degree",
    name: str | None = None,
    validate: bool = True,
) -> Vector:
    """
    Create a 3D vector from magnitude and direction angles (α, β, γ).

    Direction angles are the angles from the positive x, y, and z axes
    respectively. The components are computed as:
        x = magnitude * cos(α)
        y = magnitude * cos(β)
        z = magnitude * cos(γ)

    The direction cosines must satisfy: cos²α + cos²β + cos²γ = 1

    Args:
        magnitude: The magnitude of the vector
        unit: The unit for magnitude (e.g., "N", "lbf", "m")
        alpha: Direction angle from +x axis
        beta: Direction angle from +y axis
        gamma: Direction angle from +z axis
        angle_unit: The unit for angles (default: "degree")
        name: Optional name for the vector
        validate: If True, warn when direction cosine constraint is violated

    Returns:
        Vector with computed x, y, z components

    Examples:
        >>> from qnty.linalg.vectors2 import create_vectors_direction_angles
        >>>
        >>> # Vector aligned with x-axis: α=0°, β=90°, γ=90°
        >>> F = create_vectors_direction_angles(100, "N", 0, 90, 90, name="F_x")
        >>> print(F.x)  # 100 N
        >>> print(F.y)  # 0 N
        >>> print(F.z)  # 0 N
        >>>
        >>> # Vector with equal projections: α=β=γ≈54.74°
        >>> F = create_vectors_direction_angles(100, "N", 54.74, 54.74, 54.74, name="F_eq")
    """
    import warnings

    # Create angle Quantities
    alpha_qty = Q(alpha, angle_unit)
    beta_qty = Q(beta, angle_unit)
    gamma_qty = Q(gamma, angle_unit)

    # Compute direction cosines
    cos_alpha = cos(alpha_qty)
    cos_beta = cos(beta_qty)
    cos_gamma = cos(gamma_qty)

    # Ensure we have numeric values
    from ..algebra.nodes import Expression
    if isinstance(cos_alpha, Expression):
        cos_alpha = cos_alpha.evaluate({})
    if isinstance(cos_beta, Expression):
        cos_beta = cos_beta.evaluate({})
    if isinstance(cos_gamma, Expression):
        cos_gamma = cos_gamma.evaluate({})

    # Validate direction cosine constraint: cos²α + cos²β + cos²γ = 1
    if validate:
        cos_alpha_val = cos_alpha.magnitude() if hasattr(cos_alpha, 'magnitude') else float(cos_alpha)
        cos_beta_val = cos_beta.magnitude() if hasattr(cos_beta, 'magnitude') else float(cos_beta)
        cos_gamma_val = cos_gamma.magnitude() if hasattr(cos_gamma, 'magnitude') else float(cos_gamma)

        cos_sq_sum = cos_alpha_val**2 + cos_beta_val**2 + cos_gamma_val**2
        if not (0.99 < cos_sq_sum < 1.01):
            warnings.warn(
                f"Direction cosine constraint violated: cos²α + cos²β + cos²γ = {cos_sq_sum:.4f} ≠ 1. "
                f"The direction angles α={alpha}°, β={beta}°, γ={gamma}° may be invalid.",
                stacklevel=2,
            )

    # Compute components: x = mag * cos(α), y = mag * cos(β), z = mag * cos(γ)
    mag_qty = Q(magnitude, unit)

    x_result = mag_qty * cos_alpha
    y_result = mag_qty * cos_beta
    z_result = mag_qty * cos_gamma

    # Ensure we have Quantity objects
    if isinstance(x_result, Expression):
        x_result = x_result.evaluate({})
    if isinstance(y_result, Expression):
        y_result = y_result.evaluate({})
    if isinstance(z_result, Expression):
        z_result = z_result.evaluate({})

    # Get scalar values for create_vectors_cartesian
    x_val = x_result.magnitude() if hasattr(x_result, 'magnitude') else float(x_result)
    y_val = y_result.magnitude() if hasattr(y_result, 'magnitude') else float(y_result)
    z_val = z_result.magnitude() if hasattr(z_result, 'magnitude') else float(z_result)

    return create_vectors_cartesian(x_val, y_val, unit, z=z_val, name=name)
