"""
Parallelogram Law - Unified API for Vector Addition.

This module provides a single API that works for both:
- Code-based engineering analysis with report generation
- Frontend integration (Reflex, FastAPI) with JSON-serializable DTOs

The key insight is that the same vector operations are needed for both use cases;
only the output format differs. This module provides rich Result objects that can
be used directly in code OR converted to DTOs for serialization.

Example (Code-based analysis):
    >>> from qnty.problems.statics import parallelogram_law
    >>>
    >>> # Create vectors
    >>> F_1 = parallelogram_law.vector(magnitude=450, angle=60, unit="N", name="F_1")
    >>> F_2 = parallelogram_law.vector(magnitude=700, angle=-15, unit="N", name="F_2")
    >>>
    >>> # Solve
    >>> result = parallelogram_law.solve(F_1, F_2)
    >>>
    >>> # Access rich objects
    >>> print(f"Resultant: {result.resultant.magnitude}")
    >>> print(f"Direction: {result.resultant.angle}")
    >>>
    >>> # Generate report
    >>> result.generate_report("output.pdf")

Example (Reflex UI):
    >>> import reflex as rx
    >>> from qnty.problems.statics import parallelogram_law
    >>>
    >>> class AppState(rx.State):
    ...     # Use DTO types for state (JSON-serializable)
    ...     vectors: list[parallelogram_law.VectorDTO] = []
    ...     result: parallelogram_law.ResultDTO | None = None
    ...
    ...     def add_vector(self, magnitude: float, angle: float):
    ...         # Create vector and immediately convert to DTO for storage
    ...         v = parallelogram_law.vector(magnitude=magnitude, angle=angle, unit="N")
    ...         self.vectors.append(parallelogram_law.to_vector_dto(v))
    ...
    ...     def solve(self):
    ...         # Convert DTOs back to vectors, solve, convert result to DTO
    ...         vectors = [parallelogram_law.from_vector_dto(d) for d in self.vectors]
    ...         result = parallelogram_law.solve(*vectors)
    ...         self.result = result.to_dto()
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from ...integration.converters import dto_to_vector
from ...integration.dto import (
    PointDTO,
    ProblemInputDTO,
    QuantityDTO,
    SolutionDTO,
    SolutionStepDTO,
    VectorDTO,
)
from ...spatial.coordinate_system import CoordinateSystem
from ...spatial.vector import _Vector
from ...spatial.vectors import (
    create_vector_cartesian,
    create_vector_polar,
    create_vector_resultant,
    create_vector_resultant_polar,
)

if TYPE_CHECKING:
    from ...core.quantity import Quantity


# =============================================================================
# Coordinate System Factory Functions
# =============================================================================


def create_coord_angle_between(
    axis1_label: str,
    axis2_label: str,
    angle_between: float,
    axis1_angle: float = 0,
) -> CoordinateSystem:
    """
    Create a non-orthogonal coordinate system by specifying the angle between axes.

    This is a convenience wrapper for CoordinateSystem.from_angle_between().

    Args:
        axis1_label: Label for the first axis (e.g., "u")
        axis2_label: Label for the second axis (e.g., "v")
        angle_between: Angle between the two axes in degrees
        axis1_angle: Angle of axis1 from +x in degrees (default: 0)

    Returns:
        CoordinateSystem with the specified axes

    Examples:
        >>> # Create u-v system with 75° between axes
        >>> uv = create_coord_angle_between("u", "v", angle_between=75)
        >>> # u is at 0° (aligned with +x), v is at 75°
    """
    return CoordinateSystem.from_angle_between(
        axis1_label, axis2_label,
        axis1_angle=axis1_angle,
        angle_between=angle_between
    )


# =============================================================================
# Result DTO (for UI serialization)
# =============================================================================


@dataclass
class ResultDTO:
    """
    JSON-serializable result from parallelogram law solve.

    This is the DTO version of Result, suitable for frontend state.
    All fields are JSON-serializable primitives or nested DTOs.
    """

    success: bool
    resultant: VectorDTO | None = None
    vectors: dict[str, VectorDTO] = field(default_factory=dict)
    steps: list[SolutionStepDTO] = field(default_factory=list)
    error: str | None = None


# =============================================================================
# Result Class (rich object for code-based use)
# =============================================================================


class Result:
    """
    Result from parallelogram law solve.

    Provides both rich object access (for code-based analysis) and
    DTO conversion (for frontend integration).

    Attributes:
        success: Whether the solve succeeded
        resultant: The resultant vector (rich _Vector object)
        vectors: Dict of all vectors by name (rich _Vector objects)
        steps: Solution steps for reporting

    Methods:
        to_dto(): Convert to JSON-serializable ResultDTO
        generate_report(): Generate PDF, LaTeX, or Markdown report
    """

    def __init__(
        self,
        success: bool,
        resultant: _Vector | None = None,
        vectors: dict[str, _Vector] | None = None,
        steps: list[dict] | None = None,
        error: str | None = None,
        output_unit: str = "N",
        output_angle_unit: str = "degree",
        problem: Any | None = None,
    ):
        self.success = success
        self.resultant = resultant
        self.vectors = vectors or {}
        self._steps = steps or []
        self.error = error
        self._output_unit = output_unit
        self._output_angle_unit = output_angle_unit
        self._problem = problem

    def to_dto(
        self,
        output_unit: str | None = None,
        output_angle_unit: str | None = None,
    ) -> ResultDTO:
        """
        Convert to JSON-serializable ResultDTO.

        Use this when you need to store the result in frontend state
        (Reflex, FastAPI response, etc.)

        Args:
            output_unit: Override the output unit for force/vector magnitudes.
                         If None, uses the unit specified at solve() time.
                         Examples: "N", "kN", "lbf", "kip"
            output_angle_unit: Override the output unit for angles.
                               If None, uses the angle unit specified at solve() time.
                               Examples: "degree", "radian"

        Returns:
            ResultDTO with all values as JSON-serializable types,
            converted to the specified output units.

        Examples:
            >>> result = parallelogram_law.solve(F_1, F_2)
            >>> # Get result in Newtons (default)
            >>> dto_n = result.to_dto()
            >>> # Get result in kilo-Newtons for display
            >>> dto_kn = result.to_dto(output_unit="kN")
            >>> # Get result in pounds-force for US display
            >>> dto_lbf = result.to_dto(output_unit="lbf")
        """
        # Use provided units or fall back to solve-time defaults
        unit = output_unit if output_unit is not None else self._output_unit
        angle_unit = output_angle_unit if output_angle_unit is not None else self._output_angle_unit

        # Convert resultant
        resultant_dto = None
        if self.resultant is not None:
            resultant_dto = _vector_to_dto(self.resultant, unit, angle_unit)

        # Convert all vectors
        vectors_dto = {}
        for name, vec in self.vectors.items():
            vectors_dto[name] = _vector_to_dto(vec, unit, angle_unit)

        # Convert steps
        steps_dto = []
        for step in self._steps:
            if isinstance(step, dict):
                steps_dto.append(SolutionStepDTO.from_dict(step))

        return ResultDTO(
            success=self.success,
            resultant=resultant_dto,
            vectors=vectors_dto,
            steps=steps_dto,
            error=self.error,
        )

    def get_resultant_in(
        self,
        unit: str,
        angle_unit: str = "degree",
    ) -> tuple[float, float | None] | None:
        """
        Get the resultant magnitude and angle in specified units.

        This is a convenience method for frontend display where you need
        the numeric values directly without going through the full DTO.

        Args:
            unit: Unit for magnitude (e.g., "N", "kN", "lbf")
            angle_unit: Unit for angle (default "degree")

        Returns:
            Tuple of (magnitude, angle) in the specified units,
            or None if no resultant exists. Angle may be None for 3D vectors.

        Examples:
            >>> result = parallelogram_law.solve(F_1, F_2)
            >>> mag, angle = result.get_resultant_in("kN")
            >>> print(f"Resultant: {mag:.2f} kN at {angle:.1f}°")
        """
        if self.resultant is None:
            return None

        dto = _vector_to_dto(self.resultant, unit, angle_unit)
        return (dto.magnitude, dto.angle) if dto.magnitude is not None else None

    def get_vector_in(
        self,
        name: str,
        unit: str,
        angle_unit: str = "degree",
    ) -> VectorDTO | None:
        """
        Get a specific vector converted to the specified units.

        Args:
            name: Name of the vector (e.g., "F_1", "F_R")
            unit: Unit for magnitude (e.g., "N", "kN", "lbf")
            angle_unit: Unit for angle (default "degree")

        Returns:
            VectorDTO with values in the specified units,
            or None if vector not found.

        Examples:
            >>> result = parallelogram_law.solve(F_1, F_2)
            >>> f1_dto = result.get_vector_in("F_1", "lbf")
            >>> print(f"F_1: {f1_dto.magnitude:.2f} lbf")
        """
        vec = self.vectors.get(name)
        if vec is None:
            return None
        return _vector_to_dto(vec, unit, angle_unit)

    def generate_report(
        self,
        output_path: str | Path,
        format: Literal["markdown", "latex", "pdf"] = "pdf",
    ) -> None:
        """
        Generate a report (Markdown, LaTeX, or PDF).

        Args:
            output_path: Path for output file.
            format: Output format - 'markdown', 'latex', or 'pdf'.

        Raises:
            ValueError: If the problem was not solved successfully.
            RuntimeError: If no problem instance is available for report generation.

        Examples:
            >>> result = parallelogram_law.solve(F_1, F_2)
            >>> result.generate_report("report.pdf")
            >>> result.generate_report("report.md", format="markdown")
        """
        if not self.success:
            raise ValueError("Cannot generate report for unsuccessful solve. Check result.error for details.")

        if self._problem is None:
            raise RuntimeError(
                "No problem instance available for report generation. "
                "This may occur if the Result was created manually without a problem."
            )

        # Mark problem as solved for the report generator
        self._problem.is_solved = True

        # Import and use the report generator
        from ...extensions.reporting import generate_report as _generate_report

        _generate_report(self._problem, output_path, format=format)

    @property
    def steps(self) -> list[SolutionStepDTO]:
        """Get solution steps as DTOs."""
        return self.to_dto().steps


# =============================================================================
# Helper Functions (internal)
# =============================================================================


def _vector_to_dto(
    vec: _Vector, output_unit: str = "N", output_angle_unit: str = "degree"
) -> VectorDTO:
    """Convert internal _Vector to VectorDTO.

    Uses Qnty's built-in unit conversion via Quantity.magnitude(unit) method.
    """
    # Get component quantities and convert using Qnty's unit system
    u_qty = vec.u
    v_qty = vec.v
    w_qty = vec.w

    # Convert components to output unit using Qnty's .magnitude(unit) method
    u_output = u_qty.magnitude(output_unit)
    v_output = v_qty.magnitude(output_unit)
    w_output = w_qty.magnitude(output_unit)

    # Get magnitude in output unit using Qnty's conversion
    mag_qty = vec.magnitude
    magnitude = mag_qty.magnitude(output_unit) if mag_qty else math.sqrt(u_output**2 + v_output**2 + w_output**2)

    # Calculate angle in xy-plane
    angle: float | None = None
    if abs(u_output) > 1e-12 or abs(v_output) > 1e-12:
        angle_rad = math.atan2(v_output, u_output)
        if output_angle_unit.lower() in ("degree", "degrees", "deg"):
            angle = math.degrees(angle_rad)
        else:
            angle = angle_rad

    # Get original angle info if available
    original_angle = getattr(vec, "_original_angle", None)
    if original_angle is not None and hasattr(original_angle, "value"):
        angle = original_angle.value
        if output_angle_unit.lower() in ("degree", "degrees", "deg"):
            # Convert from radians if stored in radians
            pass  # Assume already in degrees for now

    original_wrt = getattr(vec, "_original_wrt", "+x")

    return VectorDTO(
        u=u_output,
        v=v_output,
        w=w_output,
        unit=output_unit,
        name=getattr(vec, "name", None),
        magnitude=magnitude,
        angle=angle,
        angle_unit=output_angle_unit,
        angle_wrt=original_wrt,
        plane="xy",
        is_known=getattr(vec, "is_known", True),
        is_resultant=getattr(vec, "is_resultant", False),
    )


# Use dto_to_vector from integration.converters for DTO-to-vector conversion
_dto_to_vector = dto_to_vector


# =============================================================================
# Public API - The Unified Interface
# =============================================================================


# Type aliases for UI (Pylance-compatible)
Vector = VectorDTO
Point = PointDTO
Quantity = QuantityDTO
Solution = ResultDTO  # Alias for consistency


# def vector(
#     *,
#     magnitude: float | None = None,
#     angle: float | None = None,
#     u: float | None = None,
#     v: float | None = None,
#     w: float = 0.0,
#     unit: str = "N",
#     angle_unit: str = "degree",
#     angle_wrt: str = "+x",
#     plane: str = "xy",
#     name: str | None = None,
# ) -> _Vector:
#     """
#     Create a vector for the parallelogram law problem.

#     Can specify either:
#     - Polar: magnitude and angle
#     - Cartesian: u, v, w components

#     Args:
#         magnitude: Vector magnitude (for polar input)
#         angle: Angle from reference axis (for polar input)
#         u: X-component (for Cartesian input)
#         v: Y-component (for Cartesian input)
#         w: Z-component (default 0 for 2D)
#         unit: Unit for force ("N", "lbf", "kN", etc.)
#         angle_unit: "degree" or "radian"
#         angle_wrt: Reference axis ("+x", "-x", "+y", "-y")
#         plane: Plane for 2D vectors ("xy", "xz", "yz")
#         name: Vector name/label

#     Returns:
#         _Vector object (rich, not DTO)

#     Examples:
#         >>> # Polar input
#         >>> F_1 = vector(magnitude=450, angle=60, unit="N", name="F_1")

#         >>> # Cartesian input
#         >>> F_2 = vector(u=100, v=200, unit="N", name="F_2")
#     """
#     if magnitude is not None and angle is not None:
#         return create_vector_polar(
#             magnitude=magnitude,
#             unit=unit,
#             angle=angle,
#             angle_unit=angle_unit,
#             wrt=angle_wrt,
#             plane=plane,
#             name=name,
#         )
#     elif u is not None or v is not None:
#         return create_vector_cartesian(
#             u=u or 0.0,
#             v=v or 0.0,
#             w=w,
#             unit=unit,
#             name=name,
#         )
#     else:
#         raise ValueError("Must specify either (magnitude, angle) or (u, v) components")


# def point(
#     *,
#     x: float,
#     y: float,
#     z: float = 0.0,
#     unit: str = "m",
#     name: str | None = None,
# ) -> PointDTO:
#     """
#     Create a point (for position vectors).

#     Args:
#         x: X-coordinate
#         y: Y-coordinate
#         z: Z-coordinate (default 0)
#         unit: Length unit
#         name: Point name/label

#     Returns:
#         PointDTO (JSON-serializable)
#     """
#     return PointDTO(x=x, y=y, z=z, unit=unit, name=name)


# def resultant(*vectors: _Vector, name: str = "F_R") -> _Vector:
#     """
#     Create a resultant vector (sum of input vectors).

#     The resultant will be computed when solve() is called.

#     Args:
#         vectors: Input vectors to sum
#         name: Name for the resultant vector

#     Returns:
#         _Vector placeholder for the resultant
#     """
#     return create_vector_resultant(*vectors, name=name)


def _apply_coordinate_system(vec: _Vector, coord_sys: CoordinateSystem) -> _Vector:
    """
    Apply a coordinate system to a vector with deferred coordinate resolution.

    When a vector is created with a custom axis reference (like wrt="+v"), the
    Cartesian components cannot be computed until the coordinate system is known.
    This function computes the actual components using the coordinate system.

    Args:
        vec: Vector with _needs_coordinate_system=True
        coord_sys: The coordinate system to apply

    Returns:
        New vector with computed Cartesian components
    """
    import math

    from ...spatial.vectors import _VectorWithUnknowns

    if not getattr(vec, '_needs_coordinate_system', False):
        return vec

    # Get the deferred values
    magnitude = getattr(vec, '_deferred_magnitude', None)
    angle_rad = getattr(vec, '_deferred_angle_rad', None)
    wrt = getattr(vec, '_original_wrt', '+x')

    if magnitude is None or angle_rad is None:
        return vec

    # Parse the wrt to get the base axis angle
    wrt_stripped = wrt.lstrip('+-')
    is_negative = wrt.startswith('-')

    # Find the axis angle from the coordinate system
    # Only the axes defined in the coordinate system are valid
    valid_axes = {coord_sys.axis1_label, coord_sys.axis2_label}
    if wrt_stripped not in valid_axes:
        raise ValueError(
            f"Invalid wrt axis '{wrt}' for coordinate system with axes "
            f"'{coord_sys.axis1_label}' and '{coord_sys.axis2_label}'. "
            f"Valid options: {[f'+{a}' for a in valid_axes] + [f'-{a}' for a in valid_axes]}"
        )

    if wrt_stripped == coord_sys.axis1_label:
        base_angle_rad = coord_sys.axis1_angle
        if is_negative:
            base_angle_rad += math.pi
    else:  # wrt_stripped == coord_sys.axis2_label
        base_angle_rad = coord_sys.axis2_angle
        if is_negative:
            base_angle_rad += math.pi

    # Compute the total angle (base + input angle)
    total_angle_rad = base_angle_rad + angle_rad

    # Compute Cartesian components
    u = magnitude * math.cos(total_angle_rad)
    v = magnitude * math.sin(total_angle_rad)
    w = 0.0

    # Check if the input vector is a _VectorWithUnknowns (has component vectors, constraints, etc.)
    if isinstance(vec, _VectorWithUnknowns):
        # Create a _VectorWithUnknowns to preserve all the special attributes
        new_vec = _VectorWithUnknowns(
            u=u, v=v, w=w,
            unit=vec._unit,
            unknowns=vec._unknowns.copy(),
            component_vectors=vec._component_vectors,  # Preserve component vectors (will be updated later)
            name=vec.name,
        )
        new_vec.is_known = vec.is_known
        new_vec.is_resultant = vec.is_resultant
        new_vec._is_constraint = vec._is_constraint
        new_vec.angle_dir = getattr(vec, 'angle_dir', None)
        # Preserve polar specification for reporting
        if hasattr(vec, '_polar_magnitude'):
            new_vec._polar_magnitude = vec._polar_magnitude
        if hasattr(vec, '_polar_angle_rad'):
            new_vec._polar_angle_rad = vec._polar_angle_rad
        # Clear the deferred flag since we've resolved it
        new_vec._needs_coordinate_system = False
    else:
        # Create new vector with computed components
        new_vec = _Vector(
            u=u, v=v, w=w,
            unit=vec._unit,
            name=vec.name,
            is_known=vec.is_known,
            is_resultant=vec.is_resultant,
            coordinate_system=coord_sys,
        )

    # Preserve original angle info for reporting
    new_vec._original_angle = math.degrees(angle_rad)
    new_vec._original_wrt = wrt

    # Compute and store magnitude and angle
    new_vec._magnitude = vec._magnitude
    if new_vec._magnitude is None and vec._unit is not None:
        from ...core.quantity import Quantity
        new_vec._magnitude = Quantity.from_value(magnitude, vec._unit, name=f"{vec.name}_magnitude")
        new_vec._magnitude.preferred = vec._unit

    # Store the standard angle (from +x)
    from ...core.quantity import Quantity
    from ...core.unit_catalog import degree, radian
    new_vec._angle = Quantity.from_value(total_angle_rad, radian, name=f"{vec.name}_angle")
    new_vec._angle.preferred = degree

    return new_vec


def solve_class(
    problem_class: type,
    output_unit: str = "N",
    output_angle_unit: str = "degree",
) -> Result:
    """
    Solve a parallelogram law problem defined as a class.

    This preserves vector names from class attribute names.

    Args:
        problem_class: A class with vector attributes (F_1, F_2, F_R, etc.)
        output_unit: Unit for output values
        output_angle_unit: Unit for angles ("degree" or "radian")

    Returns:
        Result object with vectors keyed by their attribute names

    Examples:
        >>> class MyProblem:
        ...     F_1 = pl.create_vector_polar(magnitude=450, angle=60, unit="N")
        ...     F_2 = pl.create_vector_polar(magnitude=700, angle=15, wrt="-x", unit="N")
        ...     F_R = pl.create_vector_resultant(F_1, F_2)
        >>>
        >>> result = pl.solve_class(MyProblem)
        >>> print(result.vectors["F_1"])  # Access by attribute name
    """
    from ..parallelogram_law import ParallelogramLawProblem

    try:
        # Create a dynamic problem class that inherits from ParallelogramLawProblem
        # and copies all vector attributes from the input class
        # Use the problem class name as default, but allow override via 'name' attribute
        problem_name = getattr(problem_class, 'name', problem_class.__name__)

        # Get coordinate system from problem class (if defined)
        problem_coord_sys = getattr(problem_class, 'coordinate_system', None)

        class DynamicProblem(ParallelogramLawProblem):
            name = problem_name
            # Store coordinate system as class attribute so it's available during solve()
            coordinate_system = problem_coord_sys

        # Copy all _Vector attributes from problem_class to DynamicProblem
        # Apply coordinate system to vectors that need it
        # Build a mapping from old vectors to new (resolved) vectors
        vector_map: dict[int, _Vector] = {}  # Maps id(old_vec) -> new_vec

        for attr_name in dir(problem_class):
            if attr_name.startswith('_'):
                continue
            attr = getattr(problem_class, attr_name)
            if isinstance(attr, _Vector):
                old_id = id(attr)
                # Set the vector's name from the attribute name if not already set
                # (default name is "Vector" which should be overwritten)
                if attr.name is None or attr.name == "Vector":
                    attr.name = attr_name
                # Check if this vector needs coordinate system resolution
                if getattr(attr, '_needs_coordinate_system', False) and problem_coord_sys is not None:
                    attr = _apply_coordinate_system(attr, problem_coord_sys)
                elif problem_coord_sys is not None:
                    # Validate that vectors with standard axes don't use x/y when a custom coordinate system is defined
                    original_wrt = getattr(attr, '_original_wrt', None)
                    if original_wrt is not None:
                        wrt_stripped = original_wrt.lstrip('+-').lower()
                        valid_axes = {problem_coord_sys.axis1_label.lower(), problem_coord_sys.axis2_label.lower()}
                        if wrt_stripped not in valid_axes:
                            raise ValueError(
                                f"Vector '{attr.name or attr_name}' uses wrt='{original_wrt}' but problem defines "
                                f"coordinate system with axes '{problem_coord_sys.axis1_label}' and '{problem_coord_sys.axis2_label}'. "
                                f"Use wrt='+{problem_coord_sys.axis1_label}' or wrt='+{problem_coord_sys.axis2_label}' instead."
                            )
                vector_map[old_id] = attr
                setattr(DynamicProblem, attr_name, attr)

        # Update component_vectors references in resultant vectors
        for attr_name in dir(problem_class):
            if attr_name.startswith('_'):
                continue
            attr = getattr(DynamicProblem, attr_name, None)
            original_attr = getattr(problem_class, attr_name, None)
            if attr is not None and hasattr(attr, '_component_vectors') and attr._component_vectors:
                # Clone the vector if it's the same object as the original to avoid mutation
                # This can happen when vectors don't need coordinate system resolution
                if attr is original_attr:
                    attr = attr.clone()
                    setattr(DynamicProblem, attr_name, attr)
                    vector_map[id(original_attr)] = attr
                # Replace component_vectors with resolved versions
                new_components = []
                for cv in attr._component_vectors:
                    cv_id = id(cv)
                    if cv_id in vector_map:
                        new_components.append(vector_map[cv_id])
                    else:
                        new_components.append(cv)
                attr._component_vectors = new_components

                # Update _original_wrt if it references a vector (starts with @)
                # Now that component vectors have names, we can use those names
                original_wrt = getattr(attr, '_original_wrt', None)
                if original_wrt and original_wrt.startswith('@'):
                    # Find the referenced vector from component_vectors and use its name
                    wrt_vec_ref = getattr(attr, '_wrt_vector_ref', None)
                    if wrt_vec_ref is not None:
                        # Find the resolved version of this vector in vector_map
                        resolved_ref = vector_map.get(id(wrt_vec_ref), wrt_vec_ref)
                        if resolved_ref.name and resolved_ref.name != "Vector":
                            attr._original_wrt = f"@{resolved_ref.name}"
                            # Update the reference to point to the resolved vector
                            attr._wrt_vector_ref = resolved_ref

        # Instantiate and solve (coordinate_system is already set as class attribute)
        problem = DynamicProblem()

        # Extract results using attribute names from problem_class
        result_vectors = {}
        resultant_vec = None

        for attr_name in dir(problem_class):
            if attr_name.startswith('_'):
                continue
            original_attr = getattr(problem_class, attr_name)
            if isinstance(original_attr, _Vector):
                solved_vec = getattr(problem, attr_name, None)
                if solved_vec is not None:
                    result_vectors[attr_name] = solved_vec
                    if getattr(original_attr, 'is_resultant', False):
                        resultant_vec = solved_vec

        # Get solution steps
        steps = getattr(problem, "solution_steps", [])

        return Result(
            success=True,
            resultant=resultant_vec,
            vectors=result_vectors,
            steps=steps,
            output_unit=output_unit,
            output_angle_unit=output_angle_unit,
            problem=problem,
        )

    except Exception as e:
        import traceback

        return Result(
            success=False,
            error=f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
        )


def solve(
    *vectors: _Vector,
    output_unit: str = "N",
    output_angle_unit: str = "degree",
    name: str | None = None,
) -> Result:
    """
    Solve the parallelogram law problem.

    Computes the resultant of all input vectors using vector addition.

    Args:
        *vectors: Vectors to add (can include a resultant placeholder)
        output_unit: Unit for output values
        output_angle_unit: Unit for angles ("degree" or "radian")
        name: Optional name for the problem (used in report title)

    Returns:
        Result object with:
        - .resultant: The computed resultant vector
        - .vectors: Dict of all vectors by name
        - .to_dto(): Convert to JSON-serializable ResultDTO

    Examples:
        >>> F_1 = vector(magnitude=100, angle=0, unit="N", name="F_1")
        >>> F_2 = vector(magnitude=100, angle=90, unit="N", name="F_2")
        >>>
        >>> result = solve(F_1, F_2)
        >>>
        >>> # Code: access rich objects
        >>> print(result.resultant.magnitude)
        >>>
        >>> # UI: convert to DTO
        >>> dto = result.to_dto()
    """
    from ..parallelogram_law import ParallelogramLawProblem

    if not vectors:
        return Result(success=False, error="No vectors provided")

    try:
        # Separate regular vectors from resultant placeholders
        input_vectors = []
        resultant_placeholder = None

        for vec in vectors:
            if getattr(vec, "is_resultant", False):
                resultant_placeholder = vec
            else:
                input_vectors.append(vec)

        if not input_vectors:
            return Result(success=False, error="No input vectors provided")

        # Create dynamic problem class with optional name
        problem_name = name or "Parallelogram Law Problem"

        class DynamicProblem(ParallelogramLawProblem):
            name = problem_name

        # Add vectors as class attributes
        for vec in input_vectors:
            attr_name = vec.name or f"F_{input_vectors.index(vec) + 1}"
            setattr(DynamicProblem, attr_name, vec)

        # Add resultant
        if resultant_placeholder is not None:
            setattr(DynamicProblem, resultant_placeholder.name or "F_R", resultant_placeholder)
        else:
            # Create resultant from input vectors
            res = create_vector_resultant(*input_vectors, name="F_R")
            setattr(DynamicProblem, "F_R", res)

        # Solve
        problem = DynamicProblem()

        # Extract results
        result_vectors = {}
        resultant_vec = None

        # Get resultant
        fr = getattr(problem, "F_R", None)
        if fr is not None:
            resultant_vec = fr
            result_vectors["F_R"] = fr

        # Get input vectors (they may have been modified/cloned)
        for vec in input_vectors:
            name = vec.name or f"F_{input_vectors.index(vec) + 1}"
            solved_vec = getattr(problem, name, vec)
            result_vectors[name] = solved_vec

        # Get solution steps
        steps = getattr(problem, "solution_steps", [])

        return Result(
            success=True,
            resultant=resultant_vec,
            vectors=result_vectors,
            steps=steps,
            output_unit=output_unit,
            output_angle_unit=output_angle_unit,
            problem=problem,
        )

    except Exception as e:
        import traceback

        return Result(
            success=False,
            error=f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
        )


# =============================================================================
# DTO Conversion Functions (for UI integration)
# =============================================================================


def to_vector_dto(
    vec: _Vector, output_unit: str = "N", output_angle_unit: str = "degree"
) -> VectorDTO:
    """
    Convert a vector to a JSON-serializable DTO.

    Use this to store vectors in frontend state.

    Args:
        vec: _Vector to convert
        output_unit: Unit for output values
        output_angle_unit: Unit for angles

    Returns:
        VectorDTO (JSON-serializable)
    """
    return _vector_to_dto(vec, output_unit, output_angle_unit)


def from_vector_dto(dto: VectorDTO) -> _Vector:
    """
    Convert a VectorDTO back to a rich _Vector.

    Use this to convert stored state back to vectors for computation.

    Args:
        dto: VectorDTO to convert

    Returns:
        _Vector (rich object)
    """
    return _dto_to_vector(dto)

