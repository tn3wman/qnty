"""
Data Transfer Objects (DTOs) for Qnty integration with frontend frameworks.

These dataclasses provide JSON-serializable representations of Qnty's core
objects (vectors, points, quantities) for use with frameworks like Reflex,
FastAPI, or any system requiring serializable state.

All DTOs use standard Python dataclasses and primitive types to ensure
compatibility with JSON serialization and frontend state management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class PointDTO:
    """
    JSON-serializable Point data.

    Represents a point in 3D space with coordinates and unit information.

    Attributes:
        x: X-coordinate value
        y: Y-coordinate value
        z: Z-coordinate value (default 0.0 for 2D problems)
        unit: Unit string for coordinates (e.g., "m", "ft", "mm")
        name: Optional name/label for the point

    Examples:
        >>> point = PointDTO(x=3.0, y=4.0, z=0.0, unit="m", name="A")
        >>> # Serializes to: {"x": 3.0, "y": 4.0, "z": 0.0, "unit": "m", "name": "A"}
    """

    x: float
    y: float
    z: float = 0.0
    unit: str = "m"
    name: str | None = None


@dataclass
class VectorDTO:
    """
    JSON-serializable Vector data.

    Represents a vector with both Cartesian and optional polar representations.
    When creating vectors, you can specify either:
    - Cartesian components (u, v, w)
    - Polar coordinates (magnitude, angle, angle_wrt, plane)

    The solver will compute the missing representation.

    Attributes:
        u: First Cartesian component (x-direction)
        v: Second Cartesian component (y-direction)
        w: Third Cartesian component (z-direction, default 0.0)
        unit: Unit string for the vector (e.g., "N", "lbf", "kN")
        name: Optional name/label for the vector

        magnitude: Optional magnitude for polar input
        angle: Optional angle for polar input
        angle_unit: Unit for angle ("degree" or "radian")
        angle_wrt: Reference axis for angle ("+x", "-x", "+y", "-y")
        plane: Plane for 2D polar vectors ("xy", "xz", "yz")

        is_known: Whether the vector value is known (True) or to be solved (False)
        is_resultant: Whether this vector is the sum of other vectors

    Examples:
        >>> # Cartesian input
        >>> v1 = VectorDTO(u=100.0, v=200.0, w=0.0, unit="N", name="F1")

        >>> # Polar input (magnitude and angle)
        >>> v2 = VectorDTO(
        ...     u=0, v=0, w=0,  # Will be computed
        ...     magnitude=450.0,
        ...     angle=60.0,
        ...     angle_wrt="+x",
        ...     unit="N",
        ...     name="F1"
        ... )
    """

    # Cartesian representation (always present after solving)
    u: float
    v: float
    w: float = 0.0
    unit: str = "N"
    name: str | None = None

    # Optional polar representation (for input convenience)
    magnitude: float | None = None
    angle: float | None = None
    angle_unit: str = "degree"
    angle_wrt: str = "+x"
    plane: str = "xy"

    # Flags
    is_known: bool = True
    is_resultant: bool = False

    def is_polar_input(self) -> bool:
        """Check if this DTO was created with polar coordinates."""
        return self.magnitude is not None and self.angle is not None


@dataclass
class QuantityDTO:
    """
    JSON-serializable Quantity data.

    Represents a scalar quantity with value, unit, and dimensional information.

    Attributes:
        value: Numeric value of the quantity
        unit: Unit string (e.g., "N", "m", "kg")
        name: Optional name/label
        dimension: Dimension name (e.g., "Force", "Length", "Mass")

    Examples:
        >>> q = QuantityDTO(value=100.0, unit="N", name="Applied Force", dimension="Force")
    """

    value: float
    unit: str
    name: str | None = None
    dimension: str | None = None


@dataclass
class SolutionStepDTO:
    """
    A single step in the solution process.

    Attributes:
        description: Human-readable description of what was computed
        formula: Mathematical formula used (LaTeX or plain text)
        result: Computed result as a string
        details: Optional additional details or intermediate values
    """

    description: str
    formula: str | None = None
    result: str | None = None
    details: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, step_dict: dict) -> "SolutionStepDTO":
        """Create a SolutionStepDTO from a dictionary."""
        return cls(
            description=step_dict.get("description", ""),
            formula=step_dict.get("formula"),
            result=step_dict.get("result"),
            details=step_dict.get("details", {}),
        )


@dataclass
class SolutionDTO:
    """
    Solution results from a problem solver.

    Contains the solved vectors, scalar quantities, solution steps,
    and any error information.

    Attributes:
        success: Whether the solution was successful
        vectors: Dictionary mapping vector names to their solved VectorDTO
        quantities: Dictionary mapping quantity names to their solved QuantityDTO
        steps: List of solution steps for display/reporting
        error: Error message if success is False

    Examples:
        >>> # Successful solution
        >>> solution = SolutionDTO(
        ...     success=True,
        ...     vectors={"F_R": VectorDTO(u=500, v=300, unit="N", name="F_R")},
        ...     steps=[SolutionStepDTO(description="Sum components", result="F_R = 583 N")]
        ... )

        >>> # Failed solution
        >>> solution = SolutionDTO(success=False, error="Insufficient constraints")
    """

    success: bool
    vectors: dict[str, VectorDTO] = field(default_factory=dict)
    quantities: dict[str, QuantityDTO] = field(default_factory=dict)
    steps: list[SolutionStepDTO] = field(default_factory=list)
    error: str | None = None


@dataclass
class ProblemInputDTO:
    """
    Input data for a problem solver.

    Collects all vectors, points, and configuration needed to solve
    a specific problem type.

    Attributes:
        problem_type: Type of problem to solve:
            - "parallelogram_law": Sum vectors using parallelogram law
            - "equilibrium": Solve force equilibrium (sum = 0)
            - "component_method": Resolve vectors into components
        vectors: List of input vectors
        points: List of input points (for position-dependent problems)
        output_unit: Preferred unit for force/vector results
        output_angle_unit: Preferred unit for angle results
        name: Optional problem name
        description: Optional problem description

    Examples:
        >>> input_dto = ProblemInputDTO(
        ...     problem_type="parallelogram_law",
        ...     vectors=[
        ...         VectorDTO(u=0, v=0, magnitude=450, angle=60, unit="N", name="F1"),
        ...         VectorDTO(u=0, v=0, magnitude=700, angle=-15, unit="N", name="F2"),
        ...     ],
        ...     output_unit="N",
        ...     output_angle_unit="degree",
        ... )
    """

    problem_type: Literal["parallelogram_law", "equilibrium", "component_method"]
    vectors: list[VectorDTO] = field(default_factory=list)
    points: list[PointDTO] = field(default_factory=list)
    output_unit: str = "N"
    output_angle_unit: str = "degree"
    name: str | None = None
    description: str | None = None


# Type alias for problem types
ProblemType = Literal["parallelogram_law", "equilibrium", "component_method"]
