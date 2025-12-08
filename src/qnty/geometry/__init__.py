"""
Geometry module for qnty.
"""

from .parallelogram import (
    Parallelogram,
    ParallelogramAngle,
    ParallelogramCase,
    ParallelogramSide,
    from_vectors as from_vectors_parallelogram,
    from_vectors_dynamic as from_vectors_dynamic_parallelogram,
)
from .triangle import Triangle, TriangleAngle, TriangleSide, from_vectors

__all__ = [
    # Parallelogram (preferred for parallelogram law problems)
    "Parallelogram",
    "ParallelogramAngle",
    "ParallelogramCase",
    "ParallelogramSide",
    "from_vectors_parallelogram",
    "from_vectors_dynamic_parallelogram",
    # Triangle (kept for future use)
    "Triangle",
    "TriangleAngle",
    "TriangleSide",
    "from_vectors",
]
