"""
Parallelogram Law Example - Using Problem Facade for Reflex Integration

This example demonstrates the recommended "single-import" facade pattern
for integrating Qnty with frontend frameworks like Reflex.

The facade pattern provides:
- Type aliases that work with Pylance (problem.Vector, problem.Solution)
- Factory methods for creating objects (problem.create_vector())
- Solve method directly on the problem class (problem.solve())

This is the cleanest API for Reflex integration!
"""

import json
from dataclasses import asdict

# Single import - everything you need for parallelogram law problems
from qnty.integration import parallelogram_law

# =============================================================================
# Simulated Reflex State using Facade Pattern
# =============================================================================

class AppState:
    """
    Simulates a Reflex State class using the facade pattern.

    In a real Reflex app:

        import reflex as rx
        from qnty.integration import parallelogram_law

        class AppState(rx.State):
            # Type aliases work in annotations (Pylance compatible)
            vectors: list[parallelogram_law.Vector] = []
            result: parallelogram_law.Solution | None = None
            ...
    """

    def __init__(self):
        # Type hints use the facade's type aliases
        # These ARE valid types for Pylance/mypy!
        self.vectors: list[parallelogram_law.Vector] = []
        self.result: parallelogram_law.Solution | None = None

        # Configuration
        self.output_unit: str = "N"
        self.output_angle_unit: str = "degree"

    def add_vector_polar(
        self,
        magnitude: float,
        angle: float,
        name: str | None = None,
    ) -> None:
        """Add a vector using polar coordinates."""
        vec_name = name or f"F_{len(self.vectors) + 1}"

        # Use facade's create_vector factory method
        self.vectors.append(
            parallelogram_law.create_vector(
                magnitude=magnitude,
                angle=angle,
                unit=self.output_unit,
                name=vec_name,
            )
        )

    def add_vector_cartesian(
        self,
        u: float,
        v: float,
        w: float = 0.0,
        name: str | None = None,
    ) -> None:
        """Add a vector using Cartesian components."""
        vec_name = name or f"F_{len(self.vectors) + 1}"

        # Use facade's create_vector factory method
        self.vectors.append(
            parallelogram_law.create_vector(
                u=u,
                v=v,
                w=w,
                unit=self.output_unit,
                name=vec_name,
            )
        )

    def solve(self) -> None:
        """Solve the problem - uses facade's solve method directly."""
        # Simple API: just pass vectors, facade handles the rest
        self.result = parallelogram_law.solve(
            vectors=self.vectors,
            output_unit=self.output_unit,
            output_angle_unit=self.output_angle_unit,
        )

    def clear(self) -> None:
        """Clear all vectors and results."""
        self.vectors = []
        self.result = None


# =============================================================================
# Main Example
# =============================================================================

def main():
    """Run the example simulation."""
    print("=" * 70)
    print("Parallelogram Law Example - Facade Pattern")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Show the clean API
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("The Facade Pattern API")
    print("-" * 70)

    print("""
    # Single import gives you everything
    from qnty.integration import parallelogram_law

    # Type aliases work in annotations (Pylance compatible!)
    vectors: list[parallelogram_law.Vector] = []
    result: parallelogram_law.Solution | None = None

    # Create vectors with factory method
    v1 = parallelogram_law.create_vector(magnitude=100, angle=30, unit="N", name="F1")

    # Solve with convenience method
    result = parallelogram_law.solve(vectors=[v1, v2])
    """)

    # -------------------------------------------------------------------------
    # Example 1: Basic usage
    # -------------------------------------------------------------------------
    print("-" * 70)
    print("Example 1: Basic vector addition")
    print("-" * 70)

    state = AppState()

    # Add vectors using polar coordinates
    state.add_vector_polar(magnitude=450.0, angle=60.0, name="F_1")
    state.add_vector_polar(magnitude=700.0, angle=-15.0, name="F_2")

    print("\nInput vectors:")
    for v in state.vectors:
        print(f"  {v.name}: {v.magnitude} {v.unit} at {v.angle}° wrt {v.angle_wrt}")

    # Solve
    state.solve()

    print("\nResults:")
    if state.result and state.result.success:
        fr = state.result.vectors.get("F_R")
        if fr:
            print(f"  F_R = {fr.magnitude:.3f} {fr.unit} at {fr.angle:.3f}°")
            print(f"  Components: ({fr.u:.3f}, {fr.v:.3f}) {fr.unit}")
    else:
        print(f"  Error: {state.result.error if state.result else 'No result'}")

    # -------------------------------------------------------------------------
    # Example 2: Using the facade directly (no state class needed)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Example 2: Direct facade usage (no state class)")
    print("-" * 70)

    # Create vectors directly with facade
    F1 = parallelogram_law.create_vector(magnitude=100, angle=0, unit="N", name="F1")
    F2 = parallelogram_law.create_vector(magnitude=100, angle=90, unit="N", name="F2")

    # Solve directly
    result = parallelogram_law.solve(vectors=[F1, F2], output_unit="N")

    print("\n  F1 = 100 N at 0°")
    print("  F2 = 100 N at 90°")
    if result.success:
        fr = result.vectors["F_R"]
        print(f"  F_R = {fr.magnitude:.3f} N at {fr.angle:.1f}°")

    # -------------------------------------------------------------------------
    # Example 3: Different problem types with same pattern
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Example 3: Other problem types use same pattern")
    print("-" * 70)

    from qnty.integration import component_method, equilibrium

    # Equilibrium check
    F1 = equilibrium.create_vector(u=100, v=0, unit="N", name="F1")
    F2 = equilibrium.create_vector(u=-100, v=0, unit="N", name="F2")
    result = equilibrium.solve(vectors=[F1, F2])
    print(f"\n  Equilibrium check: {'PASS' if result.success else 'FAIL'}")

    # Component method
    F = component_method.create_vector(magnitude=100, angle=30, unit="N", name="F")
    result = component_method.solve(vectors=[F])
    if result.success:
        f_components = result.vectors["F"]
        print(f"  100N at 30° -> Fx={f_components.u:.2f}, Fy={f_components.v:.2f}")

    # -------------------------------------------------------------------------
    # Example 4: Full Input control
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Example 4: Full control with create_input()")
    print("-" * 70)

    # Create a full input specification
    input_spec = parallelogram_law.create_input(
        vectors=[
            parallelogram_law.create_vector(magnitude=200, angle=45, unit="N", name="F1"),
            parallelogram_law.create_vector(magnitude=150, angle=135, unit="N", name="F2"),
        ],
        output_unit="lbf",
        output_angle_unit="degree",
        name="Custom Problem",
        description="Two forces at 90 degrees",
    )

    # Solve with input specification
    result = parallelogram_law.solve(input_dto=input_spec)

    if result.success:
        fr = result.vectors["F_R"]
        print(f"\n  Result in lbf: F_R = {fr.magnitude:.3f} {fr.unit} at {fr.angle:.1f}°")

    # -------------------------------------------------------------------------
    # Example 5: JSON serialization works seamlessly
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Example 5: Everything is JSON-serializable")
    print("-" * 70)

    # Create a vector
    v = parallelogram_law.create_vector(magnitude=100, angle=45, unit="N", name="test")

    # Serialize to JSON
    json_str = json.dumps(asdict(v), indent=2)
    print(f"\n  Vector as JSON:\n{json_str}")

    # -------------------------------------------------------------------------
    # Example 6: Type hints for IDE support
    # -------------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("Example 6: Type aliases for IDE autocomplete")
    print("-" * 70)

    print("""
    # Your IDE will provide autocomplete for these type aliases:

    parallelogram_law.Vector      # = VectorDTO
    parallelogram_law.Solution    # = SolutionDTO
    parallelogram_law.Point       # = PointDTO
    parallelogram_law.Input       # = ProblemInputDTO

    # Factory methods
    parallelogram_law.create_vector(...)   # Returns VectorDTO
    parallelogram_law.create_point(...)    # Returns PointDTO
    parallelogram_law.create_input(...)    # Returns ProblemInputDTO

    # Solve
    parallelogram_law.solve(...)           # Returns SolutionDTO
    """)

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
