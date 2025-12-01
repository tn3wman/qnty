"""
Solver service for frontend integration.

Provides a clean API for solving engineering problems using DTOs.
This service acts as the bridge between frontend state and the
Qnty computational engine.

The main entry point is `solve_problem()` which takes a ProblemInputDTO
and returns a SolutionDTO with all results in JSON-serializable form.
"""

from __future__ import annotations

import math
import traceback
from typing import TYPE_CHECKING

from .converters import dto_to_vector, vector_to_dto
from .dto import (
    ProblemInputDTO,
    QuantityDTO,
    SolutionDTO,
    SolutionStepDTO,
    VectorDTO,
)

if TYPE_CHECKING:
    from ..spatial.vector import _Vector
    from ..spatial.vectors import _VectorWithUnknowns


def solve_problem(input_dto: ProblemInputDTO) -> SolutionDTO:
    """
    Solve a problem from DTO input and return DTO output.

    This is the main API entry point for frontend integration.
    It dispatches to the appropriate solver based on problem_type.

    Args:
        input_dto: Problem input containing vectors, points, and configuration

    Returns:
        SolutionDTO with success status, solved values, and solution steps

    Examples:
        >>> from qnty.integration import ProblemInputDTO, VectorDTO, solve_problem
        >>>
        >>> # Create input
        >>> input_dto = ProblemInputDTO(
        ...     problem_type="parallelogram_law",
        ...     vectors=[
        ...         VectorDTO(u=0, v=0, magnitude=450, angle=60, unit="N", name="F1"),
        ...         VectorDTO(u=0, v=0, magnitude=700, angle=-15, unit="N", name="F2"),
        ...     ],
        ...     output_unit="N",
        ... )
        >>>
        >>> # Solve
        >>> result = solve_problem(input_dto)
        >>> if result.success:
        ...     print(f"F_R = {result.vectors['F_R'].magnitude:.2f} N")
    """
    try:
        if input_dto.problem_type == "parallelogram_law":
            return _solve_parallelogram_law(input_dto)
        elif input_dto.problem_type == "equilibrium":
            return _solve_equilibrium(input_dto)
        elif input_dto.problem_type == "component_method":
            return _solve_component_method(input_dto)
        else:
            return SolutionDTO(
                success=False,
                error=f"Unknown problem type: {input_dto.problem_type}",
            )
    except Exception as e:
        return SolutionDTO(
            success=False,
            error=f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
        )


def _solve_parallelogram_law(input_dto: ProblemInputDTO) -> SolutionDTO:
    """
    Solve a parallelogram law (vector addition) problem.

    Computes the resultant of all input vectors using vector addition.
    Uses algebraic methods (law of cosines/sines) for exact solutions.

    Args:
        input_dto: Problem input with vectors to sum

    Returns:
        SolutionDTO with resultant vector and solution steps
    """
    from ..problems.parallelogram_law import ParallelogramLawProblem
    from ..spatial.vectors import create_vector_resultant

    if not input_dto.vectors:
        return SolutionDTO(success=False, error="No vectors provided")

    # Convert DTOs to internal vectors
    vectors: list[_Vector] = []
    for dto in input_dto.vectors:
        vec = dto_to_vector(dto)
        vectors.append(vec)

    # Create dynamic problem class with vectors as class attributes
    class DynamicProblem(ParallelogramLawProblem):
        pass

    # Set class attributes before instantiation
    for vec in vectors:
        name = vec.name or f"F_{len([v for v in vectors if v.name])+1}"
        setattr(DynamicProblem, name, vec)

    # Add resultant placeholder
    resultant = create_vector_resultant(*vectors, name="F_R")
    setattr(DynamicProblem, "F_R", resultant)

    # Instantiate and solve (ParallelogramLawProblem solves on init)
    problem = DynamicProblem(
        name=input_dto.name or "Parallelogram Law Problem",
        description=input_dto.description or "",
    )

    # Extract results
    result_vectors: dict[str, VectorDTO] = {}

    # Get resultant
    fr = getattr(problem, "F_R", None)
    if fr is not None:
        result_vectors["F_R"] = vector_to_dto(
            fr,
            output_unit=input_dto.output_unit,
            output_angle_unit=input_dto.output_angle_unit,
        )

    # Also include input vectors with their computed Cartesian components
    for vec in vectors:
        if vec.name:
            result_vectors[vec.name] = vector_to_dto(
                vec,
                output_unit=input_dto.output_unit,
                output_angle_unit=input_dto.output_angle_unit,
            )

    # Build solution steps from problem's solution_steps
    steps = _extract_solution_steps(problem)

    return SolutionDTO(
        success=True,
        vectors=result_vectors,
        steps=steps,
    )


def _solve_equilibrium(input_dto: ProblemInputDTO) -> SolutionDTO:
    """
    Solve a force equilibrium problem.

    For equilibrium problems, the sum of all forces equals zero.
    This solver can find unknown force magnitudes or directions.

    Args:
        input_dto: Problem input with forces (some may be unknown)

    Returns:
        SolutionDTO with solved forces
    """
    # For now, implement basic equilibrium as sum = 0
    # More complex equilibrium solving will be added later

    if not input_dto.vectors:
        return SolutionDTO(success=False, error="No vectors provided")

    # Convert DTOs to internal vectors
    vectors: list[_Vector] = []
    for dto in input_dto.vectors:
        vec = dto_to_vector(dto)
        vectors.append(vec)

    # Check if all vectors are known - if so, verify equilibrium
    all_known = all(v.is_known for v in vectors)

    if all_known:
        # Verify equilibrium by summing components
        sum_u = sum(v._coords[0] for v in vectors)
        sum_v = sum(v._coords[1] for v in vectors)
        sum_w = sum(v._coords[2] for v in vectors)

        tolerance = 1e-6
        is_equilibrium = (
            abs(sum_u) < tolerance and abs(sum_v) < tolerance and abs(sum_w) < tolerance
        )

        result_vectors = {
            v.name: vector_to_dto(v, input_dto.output_unit, input_dto.output_angle_unit)
            for v in vectors
            if v.name
        }

        steps = [
            SolutionStepDTO(
                description="Sum of x-components",
                formula="ΣFx = 0",
                result=f"ΣFx = {sum_u:.6f}",
            ),
            SolutionStepDTO(
                description="Sum of y-components",
                formula="ΣFy = 0",
                result=f"ΣFy = {sum_v:.6f}",
            ),
            SolutionStepDTO(
                description="Sum of z-components",
                formula="ΣFz = 0",
                result=f"ΣFz = {sum_w:.6f}",
            ),
            SolutionStepDTO(
                description="Equilibrium check",
                result=f"{'Equilibrium satisfied' if is_equilibrium else 'NOT in equilibrium'}",
            ),
        ]

        return SolutionDTO(
            success=is_equilibrium,
            vectors=result_vectors,
            steps=steps,
            error=None if is_equilibrium else "Forces are not in equilibrium",
        )
    else:
        # TODO: Implement solving for unknowns
        return SolutionDTO(
            success=False,
            error="Solving equilibrium with unknowns not yet implemented in DTO layer",
        )


def _solve_component_method(input_dto: ProblemInputDTO) -> SolutionDTO:
    """
    Solve using the component method.

    Resolves all vectors into Cartesian components and provides
    component-wise summation.

    Args:
        input_dto: Problem input with vectors

    Returns:
        SolutionDTO with component breakdown
    """
    if not input_dto.vectors:
        return SolutionDTO(success=False, error="No vectors provided")

    # Convert DTOs to internal vectors
    vectors: list[_Vector] = []
    for dto in input_dto.vectors:
        vec = dto_to_vector(dto)
        vectors.append(vec)

    # Get component values in output unit
    from ..core.unit import ureg

    target_unit = ureg.resolve(input_dto.output_unit)
    si_factor = target_unit.si_factor if target_unit else 1.0

    # Build results
    result_vectors: dict[str, VectorDTO] = {}
    steps: list[SolutionStepDTO] = []

    total_u, total_v, total_w = 0.0, 0.0, 0.0

    for vec in vectors:
        # Get components in output unit
        u = vec._coords[0] / si_factor
        v = vec._coords[1] / si_factor
        w = vec._coords[2] / si_factor

        total_u += u
        total_v += v
        total_w += w

        name = vec.name or "Vector"
        result_vectors[name] = vector_to_dto(
            vec, input_dto.output_unit, input_dto.output_angle_unit
        )

        # Add step showing components
        steps.append(
            SolutionStepDTO(
                description=f"Components of {name}",
                result=f"{name}_x = {u:.4f}, {name}_y = {v:.4f}, {name}_z = {w:.4f} {input_dto.output_unit}",
            )
        )

    # Add totals
    steps.append(
        SolutionStepDTO(
            description="Sum of x-components",
            formula="ΣFx",
            result=f"{total_u:.4f} {input_dto.output_unit}",
        )
    )
    steps.append(
        SolutionStepDTO(
            description="Sum of y-components",
            formula="ΣFy",
            result=f"{total_v:.4f} {input_dto.output_unit}",
        )
    )
    steps.append(
        SolutionStepDTO(
            description="Sum of z-components",
            formula="ΣFz",
            result=f"{total_w:.4f} {input_dto.output_unit}",
        )
    )

    # Calculate resultant
    resultant_mag = math.sqrt(total_u**2 + total_v**2 + total_w**2)
    resultant_angle = (
        math.degrees(math.atan2(total_v, total_u))
        if abs(total_u) > 1e-12 or abs(total_v) > 1e-12
        else 0.0
    )

    result_vectors["F_R"] = VectorDTO(
        u=total_u,
        v=total_v,
        w=total_w,
        unit=input_dto.output_unit,
        name="F_R",
        magnitude=resultant_mag,
        angle=resultant_angle,
        angle_unit=input_dto.output_angle_unit,
        is_resultant=True,
    )

    steps.append(
        SolutionStepDTO(
            description="Resultant magnitude",
            formula="F_R = √(ΣFx² + ΣFy² + ΣFz²)",
            result=f"{resultant_mag:.4f} {input_dto.output_unit}",
        )
    )
    steps.append(
        SolutionStepDTO(
            description="Resultant direction",
            formula="θ = atan2(ΣFy, ΣFx)",
            result=f"{resultant_angle:.4f}°",
        )
    )

    return SolutionDTO(
        success=True,
        vectors=result_vectors,
        steps=steps,
    )


def _extract_solution_steps(problem) -> list[SolutionStepDTO]:
    """Extract solution steps from a Problem instance."""
    steps: list[SolutionStepDTO] = []

    # Check for solution_steps attribute
    if hasattr(problem, "solution_steps"):
        for step in problem.solution_steps:
            if isinstance(step, dict):
                steps.append(SolutionStepDTO.from_dict(step))
            elif isinstance(step, str):
                steps.append(SolutionStepDTO(description=step))

    return steps


# Convenience functions for common operations


def sum_vectors(
    vectors: list[VectorDTO],
    output_unit: str = "N",
    output_angle_unit: str = "degree",
) -> SolutionDTO:
    """
    Convenience function to sum vectors.

    Args:
        vectors: List of VectorDTOs to sum
        output_unit: Unit for result
        output_angle_unit: Unit for angles

    Returns:
        SolutionDTO with resultant

    Examples:
        >>> from qnty.integration import VectorDTO, sum_vectors
        >>> v1 = VectorDTO(u=100, v=0, unit="N", name="F1")
        >>> v2 = VectorDTO(u=0, v=100, unit="N", name="F2")
        >>> result = sum_vectors([v1, v2])
        >>> result.vectors["F_R"].magnitude  # ~141.4
    """
    input_dto = ProblemInputDTO(
        problem_type="parallelogram_law",
        vectors=vectors,
        output_unit=output_unit,
        output_angle_unit=output_angle_unit,
    )
    return solve_problem(input_dto)


def get_components(
    vectors: list[VectorDTO],
    output_unit: str = "N",
) -> SolutionDTO:
    """
    Convenience function to get vector components.

    Args:
        vectors: List of VectorDTOs to analyze
        output_unit: Unit for results

    Returns:
        SolutionDTO with component breakdown

    Examples:
        >>> from qnty.integration import VectorDTO, get_components
        >>> v = VectorDTO(u=0, v=0, magnitude=100, angle=30, unit="N", name="F")
        >>> result = get_components([v])
        >>> result.vectors["F"].u  # ~86.6
        >>> result.vectors["F"].v  # ~50.0
    """
    input_dto = ProblemInputDTO(
        problem_type="component_method",
        vectors=vectors,
        output_unit=output_unit,
    )
    return solve_problem(input_dto)
