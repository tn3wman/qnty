"""
Qnty Integration Module - Frontend Framework Integration.

This module provides a DTO-based API for integrating Qnty with frontend
frameworks like Reflex, FastAPI, Flask, or any system requiring
JSON-serializable state.

Key Components:
    - Problem Facades: Single-import access to problem types
    - DTOs: JSON-serializable dataclasses for vectors, points, quantities
    - Converters: Functions to convert between DTOs and internal objects
    - Solver Service: High-level API for solving problems

Recommended Usage (Facade Pattern):
    >>> import reflex as rx
    >>> from qnty.integration import parallelogram_law
    >>>
    >>> class AppState(rx.State):
    ...     # Type aliases work in annotations (Pylance compatible)
    ...     vectors: list[parallelogram_law.Vector] = []
    ...     result: parallelogram_law.Solution | None = None
    ...
    ...     def add_vector(self, magnitude: float, angle: float):
    ...         # Create vectors using factory method
    ...         self.vectors.append(parallelogram_law.create_vector(
    ...             magnitude=magnitude,
    ...             angle=angle,
    ...             unit="N",
    ...             name=f"F_{len(self.vectors)+1}",
    ...         ))
    ...
    ...     def solve(self):
    ...         # Solve using facade's solve method
    ...         self.result = parallelogram_law.solve(vectors=self.vectors)

Alternative Usage (Direct DTOs):
    >>> from qnty.integration import ProblemInputDTO, VectorDTO, solve_problem
    >>>
    >>> input_dto = ProblemInputDTO(
    ...     problem_type="parallelogram_law",
    ...     vectors=[VectorDTO(magnitude=100, angle=30, unit="N", name="F1")],
    ... )
    >>> result = solve_problem(input_dto)

Usage with FastAPI:
    >>> from fastapi import FastAPI
    >>> from qnty.integration import ProblemInputDTO, solve_problem
    >>>
    >>> app = FastAPI()
    >>>
    >>> @app.post("/solve")
    >>> def solve_endpoint(input_dto: ProblemInputDTO):
    ...     return solve_problem(input_dto)
"""

from .converters import (
    dto_to_point,
    dto_to_quantity,
    dto_to_vector,
    point_to_dto,
    quantity_to_dto,
    vector_to_dto,
)
from .dto import (
    PointDTO,
    ProblemInputDTO,
    ProblemType,
    QuantityDTO,
    SolutionDTO,
    SolutionStepDTO,
    VectorDTO,
)
from .solver_service import (
    get_components,
    solve_problem,
    sum_vectors,
)

# Problem Facades - single-import access to problem types
from .facade import (
    component_method,
    equilibrium,
    parallelogram_law,
)

__all__ = [
    # Problem Facades (recommended)
    "parallelogram_law",
    "equilibrium",
    "component_method",
    # DTOs
    "PointDTO",
    "VectorDTO",
    "QuantityDTO",
    "SolutionDTO",
    "SolutionStepDTO",
    "ProblemInputDTO",
    "ProblemType",
    # Converters
    "vector_to_dto",
    "dto_to_vector",
    "point_to_dto",
    "dto_to_point",
    "quantity_to_dto",
    "dto_to_quantity",
    # Solver service
    "solve_problem",
    "sum_vectors",
    "get_components",
]
