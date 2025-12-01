"""
Problem Facade Pattern for simplified API access.

Provides a single-import experience for each problem type, bundling:
- Type definitions (DTOs) as type aliases
- Factory methods for creating inputs
- Solve function
- Documentation

Usage:
    from qnty.integration import parallelogram_law

    # Type aliases work in annotations (Pylance/mypy compatible)
    vectors: list[parallelogram_law.Vector] = []
    result: parallelogram_law.Solution | None = None

    # Create vectors using factory
    v1 = parallelogram_law.create_vector(magnitude=100, angle=30, unit="N", name="F1")

    # Solve using the facade
    result = parallelogram_law.solve(vectors=[v1, v2])
"""

from __future__ import annotations

from typing import Literal

from .dto import (
    PointDTO,
    ProblemInputDTO,
    QuantityDTO,
    SolutionDTO,
    SolutionStepDTO,
    VectorDTO,
)
from .solver_service import solve_problem

# =============================================================================
# Shared Factory Functions
# =============================================================================


def _create_vector_dto(
    *,
    u: float = 0.0,
    v: float = 0.0,
    w: float = 0.0,
    magnitude: float | None = None,
    angle: float | None = None,
    angle_unit: str = "degree",
    angle_wrt: str = "+x",
    plane: str = "xy",
    unit: str = "N",
    name: str | None = None,
    is_known: bool = True,
    is_resultant: bool = False,
) -> VectorDTO:
    """
    Create a VectorDTO with the given parameters.

    This shared function is used by all facade classes to create vectors,
    avoiding code duplication across equilibrium, component_method, etc.
    """
    return VectorDTO(
        u=u,
        v=v,
        w=w,
        unit=unit,
        name=name,
        magnitude=magnitude,
        angle=angle,
        angle_unit=angle_unit,
        angle_wrt=angle_wrt,
        plane=plane,
        is_known=is_known,
        is_resultant=is_resultant,
    )


def _create_point_dto(
    *,
    x: float,
    y: float,
    z: float = 0.0,
    unit: str = "m",
    name: str | None = None,
) -> PointDTO:
    """
    Create a PointDTO with the given parameters.

    This shared function is used by all facade classes to create points.
    """
    return PointDTO(x=x, y=y, z=z, unit=unit, name=name)


ProblemType = Literal["parallelogram_law", "equilibrium", "component_method"]


def _create_input_dto(
    problem_type: ProblemType,
    *,
    vectors: list[VectorDTO] | None = None,
    points: list[PointDTO] | None = None,
    output_unit: str = "N",
    output_angle_unit: str = "degree",
    name: str | None = None,
    description: str | None = None,
) -> ProblemInputDTO:
    """
    Create a ProblemInputDTO for the specified problem type.

    This shared function is used by all facade classes to create input DTOs.
    """
    return ProblemInputDTO(
        problem_type=problem_type,
        vectors=vectors or [],
        points=points or [],
        output_unit=output_unit,
        output_angle_unit=output_angle_unit,
        name=name,
        description=description,
    )


def _solve_problem(
    problem_type: ProblemType,
    *,
    vectors: list[VectorDTO] | None = None,
    points: list[PointDTO] | None = None,
    input_dto: ProblemInputDTO | None = None,
    output_unit: str = "N",
    output_angle_unit: str = "degree",
) -> SolutionDTO:
    """
    Solve a problem of the specified type.

    This shared function is used by all facade classes to solve problems.
    """
    if input_dto is not None:
        return solve_problem(input_dto)

    dto = ProblemInputDTO(
        problem_type=problem_type,
        vectors=vectors or [],
        points=points or [],
        output_unit=output_unit,
        output_angle_unit=output_angle_unit,
    )
    return solve_problem(dto)


def _make_create_input(problem_type: ProblemType):
    """Factory for create_input methods bound to a specific problem type."""

    def create_input(
        *,
        vectors: list[VectorDTO] | None = None,
        points: list[PointDTO] | None = None,
        output_unit: str = "N",
        output_angle_unit: str = "degree",
        name: str | None = None,
        description: str | None = None,
    ) -> ProblemInputDTO:
        """Create an input specification for this problem."""
        return _create_input_dto(
            problem_type,
            vectors=vectors,
            points=points,
            output_unit=output_unit,
            output_angle_unit=output_angle_unit,
            name=name,
            description=description,
        )

    return staticmethod(create_input)


def _make_solve(problem_type: ProblemType):
    """Factory for solve methods bound to a specific problem type."""

    def solve(
        *,
        vectors: list[VectorDTO] | None = None,
        points: list[PointDTO] | None = None,
        input_dto: ProblemInputDTO | None = None,
        output_unit: str = "N",
        output_angle_unit: str = "degree",
    ) -> SolutionDTO:
        """Solve the problem and return results."""
        return _solve_problem(
            problem_type,
            vectors=vectors,
            points=points,
            input_dto=input_dto,
            output_unit=output_unit,
            output_angle_unit=output_angle_unit,
        )

    return staticmethod(solve)


# =============================================================================
# Parallelogram Law Problem Facade
# =============================================================================


class parallelogram_law:
    """
    Parallelogram Law Problem - Vector Addition.

    Computes the resultant of multiple vectors using the parallelogram law
    (vector addition). This is the fundamental operation for combining forces,
    velocities, or any other vector quantities.

    Type Aliases (for type hints):
        parallelogram_law.Vector   -> VectorDTO
        parallelogram_law.Point    -> PointDTO
        parallelogram_law.Solution -> SolutionDTO
        parallelogram_law.Input    -> ProblemInputDTO

    Example:
        >>> from qnty.integration import parallelogram_law
        >>>
        >>> # Type hints work correctly
        >>> vectors: list[parallelogram_law.Vector] = []
        >>> result: parallelogram_law.Solution | None = None
        >>>
        >>> # Create vectors
        >>> F1 = parallelogram_law.create_vector(magnitude=450, angle=60, unit="N", name="F1")
        >>> F2 = parallelogram_law.create_vector(magnitude=700, angle=-15, unit="N", name="F2")
        >>>
        >>> # Solve
        >>> result = parallelogram_law.solve(vectors=[F1, F2])

    For Reflex Integration:
        >>> import reflex as rx
        >>> from qnty.integration import parallelogram_law
        >>>
        >>> class AppState(rx.State):
        ...     vectors: list[parallelogram_law.Vector] = []
        ...     result: parallelogram_law.Solution | None = None
        ...
        ...     def add_vector(self, mag: float, angle: float):
        ...         self.vectors.append(parallelogram_law.create_vector(
        ...             magnitude=mag, angle=angle, unit="N",
        ...             name=f"F_{len(self.vectors)+1}"
        ...         ))
        ...
        ...     def solve(self):
        ...         self.result = parallelogram_law.solve(vectors=self.vectors)
    """

    # Type aliases - these work in type annotations!
    Vector = VectorDTO
    Point = PointDTO
    Quantity = QuantityDTO
    Solution = SolutionDTO
    SolutionStep = SolutionStepDTO
    Input = ProblemInputDTO

    # Problem configuration
    problem_type: str = "parallelogram_law"
    default_output_unit: str = "N"
    default_angle_unit: str = "degree"

    # Use shared factory functions
    create_vector = staticmethod(_create_vector_dto)
    create_point = staticmethod(_create_point_dto)
    create_input = _make_create_input("parallelogram_law")
    solve = _make_solve("parallelogram_law")


# =============================================================================
# Equilibrium Problem Facade
# =============================================================================


class equilibrium:
    """
    Force Equilibrium Problem.

    Checks if forces are in equilibrium (sum to zero) or solves for
    unknown forces to achieve equilibrium.

    Type Aliases:
        equilibrium.Vector   -> VectorDTO
        equilibrium.Solution -> SolutionDTO

    Example:
        >>> from qnty.integration import equilibrium
        >>>
        >>> F1 = equilibrium.create_vector(u=100, v=0, unit="N", name="F1")
        >>> F2 = equilibrium.create_vector(u=-100, v=0, unit="N", name="F2")
        >>> result = equilibrium.solve(vectors=[F1, F2])
        >>> print(f"In equilibrium: {result.success}")
    """

    Vector = VectorDTO
    Point = PointDTO
    Quantity = QuantityDTO
    Solution = SolutionDTO
    SolutionStep = SolutionStepDTO
    Input = ProblemInputDTO

    problem_type: str = "equilibrium"
    default_output_unit: str = "N"
    default_angle_unit: str = "degree"

    # Use shared factory functions
    create_vector = staticmethod(_create_vector_dto)
    create_point = staticmethod(_create_point_dto)
    create_input = _make_create_input("equilibrium")
    solve = _make_solve("equilibrium")


# =============================================================================
# Component Method Problem Facade
# =============================================================================


class component_method:
    """
    Component Method - Vector Decomposition.

    Resolves vectors into their Cartesian components and computes
    component-wise sums.

    Type Aliases:
        component_method.Vector   -> VectorDTO
        component_method.Solution -> SolutionDTO

    Example:
        >>> from qnty.integration import component_method
        >>>
        >>> F = component_method.create_vector(magnitude=100, angle=30, unit="N", name="F")
        >>> result = component_method.solve(vectors=[F])
        >>> print(f"Fx = {result.vectors['F'].u:.2f} N")
    """

    Vector = VectorDTO
    Point = PointDTO
    Quantity = QuantityDTO
    Solution = SolutionDTO
    SolutionStep = SolutionStepDTO
    Input = ProblemInputDTO

    problem_type: str = "component_method"
    default_output_unit: str = "N"
    default_angle_unit: str = "degree"

    # Use shared factory functions
    create_vector = staticmethod(_create_vector_dto)
    create_point = staticmethod(_create_point_dto)
    create_input = _make_create_input("component_method")
    solve = _make_solve("component_method")
