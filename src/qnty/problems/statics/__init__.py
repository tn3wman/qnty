"""
Statics problem modules with unified API.

Each module provides a single-import experience that works for both:
- Code-based engineering analysis with report generation
- Frontend integration with JSON-serializable DTOs

Example:
    >>> from qnty.problems.statics import parallelogram_law
    >>>
    >>> # Create vectors
    >>> F_1 = parallelogram_law.vector(magnitude=450, angle=60, unit="N")
    >>> F_2 = parallelogram_law.vector(magnitude=700, angle=-15, unit="N")
    >>>
    >>> # Solve
    >>> result = parallelogram_law.solve(F_1, F_2)
    >>>
    >>> # Code-based: access rich objects
    >>> print(result.resultant.magnitude)
    >>>
    >>> # UI-based: convert to DTO
    >>> dto = result.to_dto()
"""

from . import _old_parallelogram_law

__all__ = [
    "_old_parallelogram_law",
]
