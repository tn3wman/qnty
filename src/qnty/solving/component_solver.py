"""
Component/Cartesian method solver for 2D/3D force equilibrium problems.

This solver uses the rectangular component method (also known as scalar notation
or Cartesian vector method) to solve force equilibrium problems. This is the
standard method taught in engineering mechanics for problems with multiple forces.

Method:
1. Resolve each force into components: Fx, Fy, (Fz)
2. Sum components algebraically: ΣFx, ΣFy, (ΣFz)
3. For equilibrium: ΣFx = 0, ΣFy = 0, (ΣFz = 0)
4. For resultant: FR = √(ΣFx² + ΣFy² + ΣFz²)
5. Direction: θ = tan⁻¹(ΣFy/ΣFx) or direction cosines

This method is preferred over geometric/trigonometric methods when:
- More than 3 forces are present
- Forces are given in component form
- 3D problems (z-component)
"""

import math
from typing import Optional

from ..spatial.force_vector import ForceVector
from ..spatial.vector import Vector
from ..core.quantity import Quantity


class ComponentSolver:
    """
    Solves 2D/3D force equilibrium problems using the component/Cartesian method.

    This is the standard engineering mechanics approach using:
    - Scalar notation: ΣFx = 0, ΣFy = 0
    - Cartesian vectors: F = {Fx i + Fy j + Fz k}
    """

    def __init__(self):
        """Initialize the component solver."""
        self.solution_steps: list[dict] = []

    def resolve_force_components(self, force: ForceVector) -> tuple[float, float, float]:
        """
        Resolve a force into its x, y, z components in SI units.

        Args:
            force: ForceVector with magnitude and angle or with vector components

        Returns:
            Tuple of (Fx, Fy, Fz) in SI units (Newtons)

        Notes:
            - If force has a vector, use those components directly
            - If force has magnitude and angle, compute components
            - Returns values in SI units for consistent calculations
        """
        if force.vector is not None and force.x is not None and force.y is not None:
            # Force already has components
            fx = force.x.value if force.x.value is not None else 0.0
            fy = force.y.value if force.y.value is not None else 0.0
            fz = force.z.value if force.z and force.z.value is not None else 0.0
            return (fx, fy, fz)

        elif force.magnitude is not None and force.angle is not None:
            # Compute components from magnitude and angle
            mag = force.magnitude.value
            angle_rad = force.angle.value  # Already in radians (SI)

            if mag is None or angle_rad is None:
                raise ValueError(f"Force {force.name} has None magnitude or angle value")

            # 2D: Fx = F*cos(θ), Fy = F*sin(θ)
            fx = mag * math.cos(angle_rad)
            fy = mag * math.sin(angle_rad)
            fz = 0.0

            return (fx, fy, fz)

        else:
            raise ValueError(f"Force {force.name} must have either vector components or magnitude+angle")

    def sum_components(self, forces: list[ForceVector]) -> tuple[float, float, float]:
        """
        Sum the x, y, z components of all forces.

        Args:
            forces: List of ForceVector objects

        Returns:
            Tuple of (ΣFx, ΣFy, ΣFz) in SI units

        Notes:
            This implements the fundamental equilibrium equations:
            - ΣFx: Sum of all x-components
            - ΣFy: Sum of all y-components
            - ΣFz: Sum of all z-components
        """
        sum_x = 0.0
        sum_y = 0.0
        sum_z = 0.0

        for force in forces:
            fx, fy, fz = self.resolve_force_components(force)
            sum_x += fx
            sum_y += fy
            sum_z += fz

        return (sum_x, sum_y, sum_z)

    def calculate_resultant_magnitude(self, sum_x: float, sum_y: float, sum_z: float = 0.0) -> float:
        """
        Calculate the magnitude of the resultant force from components.

        Args:
            sum_x: Sum of x-components (SI units)
            sum_y: Sum of y-components (SI units)
            sum_z: Sum of z-components (SI units), default 0 for 2D

        Returns:
            Magnitude of resultant force: FR = √(ΣFx² + ΣFy² + ΣFz²)
        """
        return math.sqrt(sum_x**2 + sum_y**2 + sum_z**2)

    def calculate_resultant_angle_2d(self, sum_x: float, sum_y: float) -> float:
        """
        Calculate the angle of the resultant force in 2D (from positive x-axis, CCW).

        Args:
            sum_x: Sum of x-components (SI units)
            sum_y: Sum of y-components (SI units)

        Returns:
            Angle in radians, measured counterclockwise from +x axis
            Uses atan2 for correct quadrant determination
        """
        return math.atan2(sum_y, sum_x)

    def calculate_direction_cosines(self, sum_x: float, sum_y: float, sum_z: float,
                                   magnitude: float) -> tuple[float, float, float]:
        """
        Calculate the direction cosines for 3D resultant force.

        Args:
            sum_x, sum_y, sum_z: Component sums (SI units)
            magnitude: Magnitude of resultant force

        Returns:
            Tuple of (cos(α), cos(β), cos(γ)) where α, β, γ are angles
            from positive x, y, z axes respectively

        Notes:
            Direction cosines satisfy: cos²(α) + cos²(β) + cos²(γ) = 1
        """
        if magnitude == 0:
            return (0.0, 0.0, 0.0)

        cos_alpha = sum_x / magnitude  # Angle from +x axis
        cos_beta = sum_y / magnitude   # Angle from +y axis
        cos_gamma = sum_z / magnitude  # Angle from +z axis

        return (cos_alpha, cos_beta, cos_gamma)

    def solve_resultant(self, known_forces: list[ForceVector],
                       force_unit: Optional[str] = None) -> ForceVector:
        """
        Calculate the resultant of known forces using component method.

        Args:
            known_forces: List of known ForceVector objects
            force_unit: Preferred unit for the result (e.g., "N", "kN", "lb")

        Returns:
            ForceVector representing the resultant

        Notes:
            This is the standard component method:
            1. Resolve each force into components
            2. Sum components: ΣFx, ΣFy, ΣFz
            3. Calculate magnitude: FR = √(ΣFx² + ΣFy²)
            4. Calculate direction: θ = tan⁻¹(ΣFy/ΣFx)
        """
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        self.solution_steps = []

        # Step 1: Resolve each force into components
        self.solution_steps.append({
            "method": "Component Method (Scalar Notation)",
            "description": "Resolving forces into x and y components"
        })

        components_breakdown = []
        for force in known_forces:
            fx, fy, fz = self.resolve_force_components(force)

            # Get angle in degrees for display
            if force.angle and force.angle.value is not None:
                angle_deg = math.degrees(force.angle.value)
            else:
                angle_deg = math.degrees(math.atan2(fy, fx))

            components_breakdown.append(
                f"{force.name}: Fx = {fx:.3f} N, Fy = {fy:.3f} N"
            )

        self.solution_steps.append({
            "components": components_breakdown
        })

        # Step 2: Sum components
        sum_x, sum_y, sum_z = self.sum_components(known_forces)

        self.solution_steps.append({
            "description": "Summing force components algebraically",
            "equations": [
                f"→+ ΣFx = {sum_x:.3f} N",
                f"↑+ ΣFy = {sum_y:.3f} N"
            ]
        })

        # Step 3: Calculate resultant magnitude
        magnitude = self.calculate_resultant_magnitude(sum_x, sum_y, sum_z)

        # Step 4: Calculate resultant angle
        angle_rad = self.calculate_resultant_angle_2d(sum_x, sum_y)
        angle_deg = math.degrees(angle_rad)

        self.solution_steps.append({
            "description": "Calculating resultant magnitude and direction",
            "equations": [
                f"FR = √(ΣFx² + ΣFy²) = √({sum_x:.3f}² + {sum_y:.3f}²) = {magnitude:.3f} N",
                f"θ = tan⁻¹(ΣFy/ΣFx) = tan⁻¹({sum_y:.3f}/{sum_x:.3f}) = {angle_deg:.2f}°"
            ]
        })

        # Create result ForceVector
        result_unit = ureg.resolve(force_unit if force_unit else "N", dim=dim.force)
        degree_unit = ureg.resolve("degree", dim=dim.D)

        resultant = ForceVector(
            magnitude=magnitude,
            angle=angle_rad,  # Value is in radians (SI unit)
            unit=result_unit,
            angle_unit="radian",  # Specify that the input is in radians
            name="F_R",
            is_resultant=True,
            is_known=True
        )

        # Set preferred unit to degrees for display
        if resultant.angle and degree_unit:
            resultant.angle.preferred = degree_unit

        return resultant

    def get_solution_steps(self) -> list[dict]:
        """Get the solution steps for report generation."""
        return self.solution_steps
