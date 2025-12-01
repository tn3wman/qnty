"""
Vector diagram visualization for statics problems.

Generates properly scaled and labeled vector diagrams for force vectors,
including angles, components, and resultants. Diagrams can be saved as
images for inline display or file output.
"""

from __future__ import annotations

from pathlib import Path

from ..diagram_utils import (
    VectorDiagramBase,
    populate_force_diagram,
)


class VectorDiagram(VectorDiagramBase):
    """
    Generate scaled vector diagrams for statics problems (plotting version).

    This version uses simpler angle labels without overlap detection,
    suitable for interactive plotting scenarios. It does not use magnitude
    bars in vector labels (e.g., F_1 = 450 N instead of |F_1| = 450 N).

    Creates professional-quality diagrams with:
    - Scaled vector arrows
    - Coordinate axes
    - Angle annotations
    - Force labels
    - Optional component projections
    - Grid (optional)

    Examples:
        >>> diagram = VectorDiagram(title="Cable Forces")
        >>> diagram.add_vector(F1, color='red', label='F₁')
        >>> diagram.add_vector(F2, color='blue', label='F₂')
        >>> diagram.add_resultant(FR, color='green', label='FR')
        >>> diagram.save("diagram.png")
    """
    pass


def create_force_diagram(
    problem,
    output_path: str | Path,
    title: str | None = None,
    show_components: bool = False,
    **kwargs
) -> Path:
    """
    Create vector diagram from a VectorEquilibriumProblem.

    Args:
        problem: VectorEquilibriumProblem instance (must be solved)
        output_path: Output file path
        title: Diagram title (uses problem.name if None)
        show_components: Whether to show component projections
        **kwargs: Additional arguments for VectorDiagram

    Returns:
        Path to saved diagram

    Examples:
        >>> problem = Problem_2_1()
        >>> problem.solve()
        >>> create_force_diagram(problem, "diagram.png")
    """
    title = title or problem.name
    diagram = VectorDiagram(title=title, show_components=show_components, **kwargs)
    populate_force_diagram(diagram, problem)
    return diagram.save(output_path)
