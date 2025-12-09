"""
Geometry module for qnty.

Provides geometric models for vector addition problems:

- Triangle: The computational engine for solving (Law of Cosines, Law of Sines)
- Parallelogram: Visual model that wraps Triangle, provides coordinates for drawing

Architecture:
    Parallelogram (visualization) → delegates to → Triangle (computation)

This reflects the mathematical reality that parallelograms visualize vector
addition, but triangles provide the mathematical framework for solving.
"""

from .parallelogram import (
    Edge,
    Parallelogram,
    Vertex,
)
from .parallelogram import (
    from_vectors as from_vectors_parallelogram,
)
from .parallelogram import (
    from_vectors_dynamic as from_vectors_dynamic_parallelogram,
)
from .triangle import (
    Triangle,
    TriangleAngle,
    TriangleCase,
    TriangleSide,
    from_vectors,
    from_vectors_dynamic,
)

__all__ = [
    # Parallelogram (visual model, wraps Triangle)
    "Parallelogram",
    "Vertex",
    "Edge",
    "from_vectors_parallelogram",
    "from_vectors_dynamic_parallelogram",
    # Triangle (computational engine)
    "Triangle",
    "TriangleAngle",
    "TriangleCase",
    "TriangleSide",
    "from_vectors",
    "from_vectors_dynamic",
]
