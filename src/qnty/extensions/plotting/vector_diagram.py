"""
Vector diagram visualization for statics problems.

Generates properly scaled and labeled vector diagrams for force vectors,
including angles, components, and resultants. Diagrams can be saved as
images for inline display or file output.
"""

from __future__ import annotations

from ..diagram_utils import (
    VectorDiagramBase,
    make_create_force_diagram,
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


# Create module-specific create_force_diagram using the factory
create_force_diagram = make_create_force_diagram(VectorDiagram)
