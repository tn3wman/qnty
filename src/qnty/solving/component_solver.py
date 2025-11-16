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

from ..core.quantity import Quantity
from ..spatial.force_vector import ForceVector
from ..spatial.vector import Vector


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

    def _resolve_force_relative_angles(self, forces_dict: dict[str, ForceVector], resolve_unknown_refs: bool = False) -> None:
        """
        Resolve force-relative angle references in the forces dictionary.

        Some forces may have angles defined relative to other forces (e.g., F_3 at 60° from F_2).
        This function resolves these relative constraints by computing the actual angles.

        Args:
            forces_dict: Dictionary of force_name -> ForceVector
            resolve_unknown_refs: If True, resolve references to unknown forces (for post-solve resolution)
        """
        import math

        from ..core.dimension_catalog import dim
        from ..core.quantity import Quantity

        # Identify forces with relative angle constraints
        forces_to_resolve = []
        for force_name, force in forces_dict.items():
            if hasattr(force, "_relative_to_force") and force._relative_to_force is not None:
                forces_to_resolve.append((force_name, force))

        # Resolve each relative constraint
        for force_name, force in forces_to_resolve:
            ref_force_name = force._relative_to_force
            if ref_force_name not in forces_dict:
                raise ValueError(f"Force {force_name} references unknown force {ref_force_name}")

            ref_force = forces_dict[ref_force_name]

            # Skip resolution if the reference force is unknown (will be computed later)
            # This handles cases where a known force references an unknown resultant
            if not ref_force.is_known and not resolve_unknown_refs:
                continue

            # Get the reference force's angle
            if ref_force.angle is None or ref_force.angle.value is None:
                if not resolve_unknown_refs:
                    continue  # Skip for now, will resolve after solving
                raise ValueError(f"Reference force {ref_force_name} must have a known angle")

            ref_angle_rad = ref_force.angle.value  # In radians, standard form (CCW from +x)

            # Add the relative angle offset
            actual_angle_rad = ref_angle_rad + force._relative_angle

            # Update the force's angle
            force._angle = Quantity(name=f"{force_name}_angle", dim=dim.D, value=actual_angle_rad, preferred=force._angle.preferred if force._angle else None)

            # Recompute the vector components with the resolved angle
            if force.magnitude and force.magnitude.value is not None:
                mag = force.magnitude.value
                x_val = mag * math.cos(actual_angle_rad)
                y_val = mag * math.sin(actual_angle_rad)
                z_val = 0.0

                # Create Quantities
                x_qty = Quantity(name=f"{force_name}_x", dim=dim.force, value=x_val, preferred=force.magnitude.preferred)
                y_qty = Quantity(name=f"{force_name}_y", dim=dim.force, value=y_val, preferred=force.magnitude.preferred)
                z_qty = Quantity(name=f"{force_name}_z", dim=dim.force, value=z_val, preferred=force.magnitude.preferred)
                force._vector = Vector.from_quantities(x_qty, y_qty, z_qty)

            # Clear the relative constraint since it's now resolved
            force._relative_to_force = None
            force._relative_angle = None

    def solve(self, forces: list[ForceVector], force_unit: str | None = None) -> dict[str, ForceVector]:
        """
        Solve a force system problem automatically detecting the problem type.

        Handles three types of problems:
        1. Normal: Given known forces, find the resultant (F_R = F_1 + F_2 + ...)
        2. Reverse: Given known forces and known resultant, find unknown force (F_unknown = F_R - Σ known forces)
        3. Constrained: Forces with relative angle constraints (e.g., F1 at angle θ from F_R)

        Args:
            forces: List of ForceVector objects (mix of known and unknown forces, may include resultant)
            force_unit: Preferred unit for results (e.g., "N", "kN", "lbf")

        Returns:
            Dictionary mapping force names to solved ForceVector objects

        Examples:
            >>> # Normal problem: Find resultant
            >>> F1 = ForceVector(magnitude=100, angle=30, unit="N", name="F1")
            >>> F2 = ForceVector(magnitude=200, angle=120, unit="N", name="F2")
            >>> FR = ForceVector.unknown("FR", is_resultant=True)
            >>> result = solver.solve([F1, F2, FR])
            >>> result["FR"]  # Computed resultant

            >>> # Reverse problem: Find unknown force
            >>> FA = ForceVector(magnitude=700, angle=-30, unit="N", name="FA")
            >>> FB = ForceVector.unknown("FB")
            >>> FR = ForceVector(magnitude=1500, angle=90, unit="N", name="FR", is_resultant=True)
            >>> result = solver.solve([FA, FB, FR])
            >>> result["FB"]  # Computed unknown force
        """
        # Build forces dictionary for reference resolution
        forces_dict = {force.name: force for force in forces}

        # Step 1: Resolve force-relative angle references for known forces referencing known forces
        self._resolve_force_relative_angles(forces_dict, resolve_unknown_refs=False)

        # Categorize forces
        known_forces = []
        unknown_forces = []
        constrained_forces = []  # Forces with relative angle constraints to unknown forces
        resultant = None

        for force in forces:
            if hasattr(force, "is_resultant") and force.is_resultant:
                resultant = force
            elif force.is_known:
                # Check if this force has an unresolved relative angle constraint
                if hasattr(force, "has_relative_angle") and force.has_relative_angle():
                    constrained_forces.append(force)
                else:
                    known_forces.append(force)
            else:
                unknown_forces.append(force)

        # Determine force unit from known forces if not specified
        if not force_unit:
            if known_forces and known_forces[0].magnitude and known_forces[0].magnitude.preferred:
                force_unit = known_forces[0].magnitude.preferred.symbol
            elif resultant and resultant.magnitude and resultant.magnitude.preferred:
                force_unit = resultant.magnitude.preferred.symbol

        # Build result dictionary
        result = {}
        for force in forces:
            result[force.name] = force

        # Case 1: Reverse/equilibrium problem - known resultant, solve for unknown force(s)
        # This includes cases where FR is known and we need to find unknown forces such that:
        # F1 + F2 + ... + F_unknown = FR
        if resultant and resultant.is_known and len(unknown_forces) > 0:
            for unknown_force in unknown_forces:
                solved_force = self.solve_unknown_force(known_forces, resultant, force_unit=force_unit, unknown_force_name=unknown_force.name)
                result[unknown_force.name] = solved_force

        # Case 2: Constrained equilibrium - unknown forces with known directions
        # Example: F2 has unknown magnitude but known angle, FR has unknown magnitude but known angle
        # We can solve for both magnitudes using equilibrium equations
        elif resultant and not resultant.is_known and len(unknown_forces) > 0:
            # Check if all unknowns have known angles (partially known)
            all_have_angles = all((f.angle is not None and f.angle.value is not None) or (hasattr(f, "is_resultant") and f.is_resultant) for f in unknown_forces + [resultant])

            if all_have_angles and len(unknown_forces) == 1 and resultant.angle is not None and resultant.angle.value is not None:
                # Special case: 1 unknown force + 1 unknown resultant, both with known angles
                # Solve using equilibrium: F1 + F2 + ... + F_unknown = F_R
                solved_unknown, solved_resultant = self.solve_constrained_equilibrium(known_forces, unknown_forces[0], resultant, force_unit=force_unit)
                result[unknown_forces[0].name] = solved_unknown
                result[resultant.name] = solved_resultant
            else:
                # Fall back to standard resultant solving
                solved_resultant = self.solve_resultant(known_forces, force_unit=force_unit)
                result[resultant.name] = solved_resultant

        # Case 3: Normal problem - known forces, solve for unknown resultant
        # Note: Constrained forces are temporarily excluded from known_forces
        # They will be resolved after the resultant is computed
        elif resultant and not resultant.is_known:
            solved_resultant = self.solve_resultant(known_forces, force_unit=force_unit)
            result[resultant.name] = solved_resultant

        # Case 4: No resultant specified - compute it anyway
        else:
            solved_resultant = self.solve_resultant(known_forces, force_unit=force_unit)
            result["F_R"] = solved_resultant

        # Step 3: Post-solve resolution of force-relative angles
        # Now that all unknowns are solved, resolve any remaining relative angle constraints
        # This handles cases like F1 at angle θ from F_R where F_R was unknown
        self._resolve_force_relative_angles(result, resolve_unknown_refs=True)

        return result

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
            - Forces with unresolved relative angle constraints cannot be resolved
            - Returns values in SI units for consistent calculations
        """
        # Check for unresolved relative angle constraint
        if hasattr(force, "has_relative_angle") and force.has_relative_angle():
            raise ValueError(f"Force {force.name} has an unresolved relative angle constraint. Cannot compute components until the referenced force is resolved.")

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

    def calculate_direction_cosines(self, sum_x: float, sum_y: float, sum_z: float, magnitude: float) -> tuple[float, float, float]:
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
        cos_beta = sum_y / magnitude  # Angle from +y axis
        cos_gamma = sum_z / magnitude  # Angle from +z axis

        return (cos_alpha, cos_beta, cos_gamma)

    def calculate_direction_angles_3d(self, sum_x: float, sum_y: float, sum_z: float, magnitude: float) -> tuple[float, float, float]:
        """
        Calculate the coordinate direction angles for 3D resultant force.

        Args:
            sum_x, sum_y, sum_z: Component sums (SI units)
            magnitude: Magnitude of resultant force

        Returns:
            Tuple of (alpha, beta, gamma) in radians where:
            - alpha: angle from +x axis [0, π]
            - beta: angle from +y axis [0, π]
            - gamma: angle from +z axis [0, π]

        Notes:
            Angles are computed from direction cosines:
            - cos(α) = sum_x / magnitude
            - cos(β) = sum_y / magnitude
            - cos(γ) = sum_z / magnitude
        """
        cos_alpha, cos_beta, cos_gamma = self.calculate_direction_cosines(sum_x, sum_y, sum_z, magnitude)

        # Clamp to [-1, 1] to handle numerical errors
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        cos_beta = max(-1.0, min(1.0, cos_beta))
        cos_gamma = max(-1.0, min(1.0, cos_gamma))

        alpha = math.acos(cos_alpha)
        beta = math.acos(cos_beta)
        gamma = math.acos(cos_gamma)

        return (alpha, beta, gamma)

    def solve_resultant(self, known_forces: list[ForceVector], force_unit: str | None = None) -> ForceVector:
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
        self.solution_steps.append({"method": "Component Method (Scalar Notation)", "description": "Resolving forces into x and y components"})

        components_breakdown = []
        for force in known_forces:
            fx, fy, fz = self.resolve_force_components(force)

            # Get angle in degrees for display
            if force.angle and force.angle.value is not None:
                angle_deg = math.degrees(force.angle.value)
            else:
                angle_deg = math.degrees(math.atan2(fy, fx))

            components_breakdown.append(f"{force.name}: Fx = {fx:.3f} N, Fy = {fy:.3f} N")

        self.solution_steps.append({"components": components_breakdown})

        # Step 2: Sum components
        sum_x, sum_y, sum_z = self.sum_components(known_forces)

        # Detect if this is a 3D problem (any z-component non-zero)
        is_3d = abs(sum_z) > 1e-10

        if is_3d:
            self.solution_steps.append({"description": "Summing force components algebraically (3D)", "equations": [f"→+ ΣFx = {sum_x:.3f} N", f"↑+ ΣFy = {sum_y:.3f} N", f"↗+ ΣFz = {sum_z:.3f} N"]})
        else:
            self.solution_steps.append({"description": "Summing force components algebraically", "equations": [f"→+ ΣFx = {sum_x:.3f} N", f"↑+ ΣFy = {sum_y:.3f} N"]})

        # Step 3: Calculate resultant magnitude
        magnitude = self.calculate_resultant_magnitude(sum_x, sum_y, sum_z)

        # Step 4: Calculate resultant direction
        result_unit = ureg.resolve(force_unit if force_unit else "N", dim=dim.force)
        degree_unit = ureg.resolve("degree", dim=dim.D)

        if is_3d:
            # 3D: Calculate direction angles α, β, γ
            alpha_rad, beta_rad, gamma_rad = self.calculate_direction_angles_3d(sum_x, sum_y, sum_z, magnitude)
            alpha_deg = math.degrees(alpha_rad)
            beta_deg = math.degrees(beta_rad)
            gamma_deg = math.degrees(gamma_rad)

            self.solution_steps.append(
                {
                    "description": "Calculating resultant magnitude and direction angles",
                    "equations": [
                        f"FR = √(ΣFx² + ΣFy² + ΣFz²) = √({sum_x:.3f}² + {sum_y:.3f}² + {sum_z:.3f}²) = {magnitude:.3f} N",
                        f"α = cos⁻¹(ΣFx/FR) = cos⁻¹({sum_x:.3f}/{magnitude:.3f}) = {alpha_deg:.2f}°",
                        f"β = cos⁻¹(ΣFy/FR) = cos⁻¹({sum_y:.3f}/{magnitude:.3f}) = {beta_deg:.2f}°",
                        f"γ = cos⁻¹(ΣFz/FR) = cos⁻¹({sum_z:.3f}/{magnitude:.3f}) = {gamma_deg:.2f}°",
                    ],
                }
            )

            # Create 3D ForceVector using components
            mag_qty = Quantity(name="F_R_magnitude", dim=dim.force, value=magnitude, preferred=result_unit)
            x_qty = Quantity(name="F_R_x", dim=dim.force, value=sum_x, preferred=result_unit)
            y_qty = Quantity(name="F_R_y", dim=dim.force, value=sum_y, preferred=result_unit)
            z_qty = Quantity(name="F_R_z", dim=dim.force, value=sum_z, preferred=result_unit)

            resultant = ForceVector(x=x_qty, y=y_qty, z=z_qty, unit=result_unit, name="F_R", is_resultant=True, is_known=True)

        else:
            # 2D: Calculate angle θ from +x axis
            angle_rad = self.calculate_resultant_angle_2d(sum_x, sum_y)
            angle_deg = math.degrees(angle_rad)

            self.solution_steps.append(
                {
                    "description": "Calculating resultant magnitude and direction",
                    "equations": [f"FR = √(ΣFx² + ΣFy²) = √({sum_x:.3f}² + {sum_y:.3f}²) = {magnitude:.3f} N", f"θ = tan⁻¹(ΣFy/ΣFx) = tan⁻¹({sum_y:.3f}/{sum_x:.3f}) = {angle_deg:.2f}°"],
                }
            )

            # Create Quantities in SI units
            mag_qty = Quantity(name="F_R_magnitude", dim=dim.force, value=magnitude)
            ang_qty = Quantity(name="F_R_angle", dim=dim.D, value=angle_rad)

            # Set preferred units for display
            mag_qty.preferred = result_unit
            ang_qty.preferred = degree_unit

            # Create 2D ForceVector from magnitude and angle
            resultant = ForceVector(magnitude=mag_qty, angle=ang_qty, unit=result_unit, name="F_R", is_resultant=True, is_known=True)

        return resultant

    def solve_constrained_equilibrium(
        self, known_forces: list[ForceVector], unknown_force: ForceVector, unknown_resultant: ForceVector, force_unit: str | None = None
    ) -> tuple[ForceVector, ForceVector]:
        """
        Solve for unknown force and resultant magnitudes when both have known directions.

        This handles constrained equilibrium problems where:
        - Known forces: F1, F2, ... (fully known)
        - Unknown force: F_unknown (magnitude unknown, angle known)
        - Unknown resultant: F_R (magnitude unknown, angle known)
        - Equilibrium: F1 + F2 + ... + F_unknown = F_R

        Args:
            known_forces: List of fully known ForceVector objects
            unknown_force: ForceVector with unknown magnitude but known angle
            unknown_resultant: Resultant ForceVector with unknown magnitude but known angle
            force_unit: Preferred unit for results

        Returns:
            Tuple of (solved_unknown_force, solved_resultant)

        Notes:
            Uses the two equilibrium equations:
            - ΣFx = 0: F1x + F2x + ... + F_unknown_x = FRx
            - ΣFy = 0: F1y + F2y + ... + F_unknown_y = FRy

            With F_unknown_x = |F_unknown| * cos(θ_unknown) and FRx = |FR| * cos(θ_R)
            This gives 2 equations with 2 unknowns (|F_unknown| and |FR|)
        """
        import numpy as np

        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        self.solution_steps = []

        # Step 1: Get known components and angles
        self.solution_steps.append({"method": "Constrained Equilibrium Method", "description": "Solving for unknown magnitudes with known directions"})

        # Sum known forces
        sum_known_x, sum_known_y, _ = self.sum_components(known_forces)

        # Get angles (in radians) - validate they exist
        if unknown_force.angle is None or unknown_force.angle.value is None:
            raise ValueError(f"Unknown force {unknown_force.name} must have a known angle for constrained equilibrium")
        if unknown_resultant.angle is None or unknown_resultant.angle.value is None:
            raise ValueError(f"Unknown resultant {unknown_resultant.name} must have a known angle for constrained equilibrium")

        theta_unknown = unknown_force.angle.value
        theta_R = unknown_resultant.angle.value

        self.solution_steps.append(
            {
                "description": "Setting up equilibrium equations",
                "equations": [
                    f"ΣFx: {sum_known_x:.3f} + |F_unknown|*cos({math.degrees(theta_unknown):.1f}°) = |FR|*cos({math.degrees(theta_R):.1f}°)",
                    f"ΣFy: {sum_known_y:.3f} + |F_unknown|*sin({math.degrees(theta_unknown):.1f}°) = |FR|*sin({math.degrees(theta_R):.1f}°)",
                ],
            }
        )

        # Solve system of linear equations:
        # sum_known_x + |F_u| * cos(θ_u) = |FR| * cos(θ_R)
        # sum_known_y + |F_u| * sin(θ_u) = |FR| * sin(θ_R)
        #
        # Rearrange to matrix form: A * [|F_u|, |FR|]^T = b
        # [ cos(θ_u)  -cos(θ_R) ] [ |F_u| ]   [ -sum_known_x ]
        # [ sin(θ_u)  -sin(θ_R) ] [ |FR|  ] = [ -sum_known_y ]

        A = np.array([[math.cos(theta_unknown), -math.cos(theta_R)], [math.sin(theta_unknown), -math.sin(theta_R)]])
        b = np.array([-sum_known_x, -sum_known_y])

        # Solve for [|F_unknown|, |FR|]
        try:
            magnitudes = np.linalg.solve(A, b)
            mag_unknown = magnitudes[0]
            mag_R = magnitudes[1]
        except np.linalg.LinAlgError as err:
            raise ValueError("Cannot solve constrained equilibrium - system is singular. The unknown force and resultant may be parallel.") from err

        self.solution_steps.append({"description": "Solved for magnitudes", "results": [f"|F_unknown| = {mag_unknown:.3f} N", f"|FR| = {mag_R:.3f} N"]})

        # Create solved forces
        result_unit = ureg.resolve(force_unit if force_unit else "N", dim=dim.force)
        degree_unit = ureg.resolve("degree", dim=dim.D)

        # Solved unknown force
        from ..core.quantity import Quantity

        mag_unknown_qty = Quantity(name=f"{unknown_force.name}_magnitude", dim=dim.force, value=mag_unknown)
        mag_unknown_qty.preferred = result_unit

        ang_unknown_qty = Quantity(name=f"{unknown_force.name}_angle", dim=dim.D, value=theta_unknown)
        ang_unknown_qty.preferred = degree_unit

        solved_unknown = ForceVector(magnitude=mag_unknown_qty, angle=ang_unknown_qty, unit=result_unit, name=unknown_force.name, is_known=True)

        # Solved resultant
        mag_R_qty = Quantity(name=f"{unknown_resultant.name}_magnitude", dim=dim.force, value=mag_R)
        mag_R_qty.preferred = result_unit

        ang_R_qty = Quantity(name=f"{unknown_resultant.name}_angle", dim=dim.D, value=theta_R)
        ang_R_qty.preferred = degree_unit

        solved_resultant = ForceVector(magnitude=mag_R_qty, angle=ang_R_qty, unit=result_unit, name=unknown_resultant.name, is_resultant=True, is_known=True)

        return (solved_unknown, solved_resultant)

    def solve_unknown_force(self, known_forces: list[ForceVector], known_resultant: ForceVector, force_unit: str | None = None, unknown_force_name: str = "F_unknown") -> ForceVector:
        """
        Solve for an unknown force given known forces and a known resultant.

        This handles reverse problems where: F_A + F_B + ... + F_unknown = F_R
        Therefore: F_unknown = F_R - (F_A + F_B + ...)

        Args:
            known_forces: List of known ForceVector objects
            known_resultant: Known resultant ForceVector
            force_unit: Preferred unit for the result (e.g., "N", "kN", "lb")
            unknown_force_name: Name for the unknown force

        Returns:
            ForceVector representing the unknown force

        Notes:
            This is used for problems like: "Determine force F_B so that the
            resultant is directed along +y axis with magnitude 1500 N"
        """
        from ..core.dimension_catalog import dim
        from ..core.unit import ureg

        self.solution_steps = []

        # Step 1: Get resultant components
        self.solution_steps.append({"method": "Reverse Component Method", "description": "Solving for unknown force given known resultant"})

        R_x, R_y, R_z = self.resolve_force_components(known_resultant)

        # Step 2: Sum known forces
        sum_known_x, sum_known_y, sum_known_z = self.sum_components(known_forces)

        components_breakdown = []
        for force in known_forces:
            fx, fy, fz = self.resolve_force_components(force)
            components_breakdown.append(f"{force.name}: Fx = {fx:.3f} N, Fy = {fy:.3f} N")

        self.solution_steps.append({"components": components_breakdown})

        self.solution_steps.append({"description": "Resultant components", "equations": [f"F_R: Fx = {R_x:.3f} N, Fy = {R_y:.3f} N"]})

        # Step 3: Calculate unknown force components
        # F_unknown = F_R - Sum(known forces)
        unknown_x = R_x - sum_known_x
        unknown_y = R_y - sum_known_y
        unknown_z = R_z - sum_known_z

        self.solution_steps.append(
            {
                "description": "Solving for unknown force components",
                "equations": [
                    f"F_unknown_x = F_R_x - ΣF_known_x = {R_x:.3f} - {sum_known_x:.3f} = {unknown_x:.3f} N",
                    f"F_unknown_y = F_R_y - ΣF_known_y = {R_y:.3f} - {sum_known_y:.3f} = {unknown_y:.3f} N",
                ],
            }
        )

        # Step 4: Calculate magnitude and angle
        magnitude = self.calculate_resultant_magnitude(unknown_x, unknown_y, unknown_z)

        # Check if this is a 3D problem (non-zero z-component)
        is_3d = abs(unknown_z) > 1e-6 or abs(R_z) > 1e-6 or any(abs(self.resolve_force_components(f)[2]) > 1e-6 for f in known_forces)

        result_unit = ureg.resolve(force_unit if force_unit else "N", dim=dim.force)
        degree_unit = ureg.resolve("degree", dim=dim.D)

        if is_3d:
            # 3D problem - create force with x, y, z components
            self.solution_steps.append(
                {
                    "description": "Calculating unknown force magnitude and direction (3D)",
                    "equations": [
                        f"F_unknown = √(Fx² + Fy² + Fz²) = √({unknown_x:.3f}² + {unknown_y:.3f}² + {unknown_z:.3f}²) = {magnitude:.3f} N",
                    ],
                }
            )

            # Create component Quantities in SI units
            x_qty = Quantity(name=f"{unknown_force_name}_x", dim=dim.force, value=unknown_x, preferred=result_unit)
            y_qty = Quantity(name=f"{unknown_force_name}_y", dim=dim.force, value=unknown_y, preferred=result_unit)
            z_qty = Quantity(name=f"{unknown_force_name}_z", dim=dim.force, value=unknown_z, preferred=result_unit)

            # Create ForceVector from components
            unknown_force = ForceVector(x=x_qty, y=y_qty, z=z_qty, unit=result_unit, name=unknown_force_name, is_known=True)
        else:
            # 2D problem - create force with magnitude and angle
            angle_rad = self.calculate_resultant_angle_2d(unknown_x, unknown_y)
            angle_deg = math.degrees(angle_rad)

            self.solution_steps.append(
                {
                    "description": "Calculating unknown force magnitude and direction",
                    "equations": [
                        f"F_unknown = √(Fx² + Fy²) = √({unknown_x:.3f}² + {unknown_y:.3f}²) = {magnitude:.3f} N",
                        f"θ = tan⁻¹(Fy/Fx) = tan⁻¹({unknown_y:.3f}/{unknown_x:.3f}) = {angle_deg:.2f}°",
                    ],
                }
            )

            # Create Quantities in SI units
            mag_qty = Quantity(name=f"{unknown_force_name}_magnitude", dim=dim.force, value=magnitude, preferred=result_unit)
            ang_qty = Quantity(name=f"{unknown_force_name}_angle", dim=dim.D, value=angle_rad, preferred=degree_unit)

            # Create ForceVector from magnitude and angle
            unknown_force = ForceVector(magnitude=mag_qty, angle=ang_qty, unit=result_unit, name=unknown_force_name, is_known=True)

        return unknown_force

    def get_solution_steps(self) -> list[dict]:
        """Get the solution steps for report generation."""
        return self.solution_steps
