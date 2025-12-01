"""
Parallelogram Law - Unified API Example

This example demonstrates the UNIFIED API that works identically for:
- Code-based engineering analysis
- Frontend integration (Reflex, FastAPI, etc.)

The key insight: same syntax, different output formats.

    # SAME CODE for both use cases
    from qnty.problems.statics import parallelogram_law

    F_1 = parallelogram_law.vector(magnitude=450, angle=60, unit="N", name="F_1")
    F_2 = parallelogram_law.vector(magnitude=700, angle=-15, unit="N", name="F_2")
    result = parallelogram_law.solve(F_1, F_2)

    # For code: use rich objects directly
    print(result.resultant.magnitude)

    # For UI: convert to DTO
    dto = result.to_dto()  # JSON-serializable
"""

import json
from dataclasses import asdict

# THE UNIFIED IMPORT - works for both code and UI
from qnty.problems.statics import parallelogram_law


def main():
    print("=" * 70)
    print("Parallelogram Law - UNIFIED API")
    print("Same syntax for code-based analysis AND frontend integration")
    print("=" * 70)

    # =========================================================================
    # Example 1: Basic Usage (identical for code and UI)
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 1: Basic vector addition")
    print("-" * 70)

    # Create vectors - SAME syntax for both use cases
    F_1 = parallelogram_law.create_vector_polar(magnitude=450, angle=60, unit="N", name="F_1")
    F_2 = parallelogram_law.create_vector_polar(magnitude=700, angle=-15, unit="N", name="F_2")

    print(f"\n  F_1: {F_1.name} = 450 N at 60°")
    print(f"  F_2: {F_2.name} = 700 N at -15°")

    # Solve - SAME syntax for both use cases
    result = parallelogram_law.solve(F_1, F_2)

    print("\n  Result (code-based access):")
    if result.success and result.resultant:
        # Code-based: access rich _Vector objects directly
        print(f"    result.resultant = {result.resultant}")
        print(f"    result.vectors.keys() = {list(result.vectors.keys())}")

    print("\n  Result (UI-based access via DTO):")
    # UI-based: convert to JSON-serializable DTO
    dto = result.to_dto()
    if dto.resultant:
        print(f"    dto.resultant.magnitude = {dto.resultant.magnitude:.3f}")
        print(f"    dto.resultant.angle = {dto.resultant.angle:.3f}°")
        print(f"    dto.resultant.u = {dto.resultant.u:.3f}")
        print(f"    dto.resultant.v = {dto.resultant.v:.3f}")

    # =========================================================================
    # Example 2: JSON Serialization (for frontend state)
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 2: JSON serialization for frontend")
    print("-" * 70)

    # The DTO is fully JSON-serializable
    dto = result.to_dto()
    json_str = json.dumps(asdict(dto), indent=2, default=str)
    print("\n  result.to_dto() as JSON (truncated):")
    print("  " + json_str[:400].replace("\n", "\n  ") + "...")

    # =========================================================================
    # Example 3: Simulated Reflex State
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 3: Simulated Reflex State")
    print("-" * 70)

    class SimulatedReflexState:
        """
        In real Reflex:

            import reflex as rx
            from qnty.problems.statics import parallelogram_law

            class AppState(rx.State):
                vectors: list[parallelogram_law.Vector] = []
                result: parallelogram_law.ResultDTO | None = None

                def add_vector(self, magnitude: float, angle: float):
                    v = parallelogram_law.vector(magnitude=magnitude, angle=angle, unit="N")
                    self.vectors.append(parallelogram_law.to_vector_dto(v))

                def solve(self):
                    vecs = [parallelogram_law.from_vector_dto(d) for d in self.vectors]
                    result = parallelogram_law.solve(*vecs)
                    self.result = result.to_dto()
        """

        def __init__(self):
            # Store DTOs (JSON-serializable)
            self.vectors: list[parallelogram_law.Vector] = []
            self.result: parallelogram_law.ResultDTO | None = None

        def add_vector(self, magnitude: float, angle: float, name: str):
            # Create vector and convert to DTO for storage
            v = parallelogram_law.create_vector_polar(magnitude=magnitude, angle=angle, unit="N", name=name)
            self.vectors.append(parallelogram_law.to_vector_dto(v))

        def solve(self):
            # Convert DTOs back to vectors, solve, convert result to DTO
            vecs = [parallelogram_law.from_vector_dto(d) for d in self.vectors]
            result = parallelogram_law.solve(*vecs)
            self.result = result.to_dto()

    # Use it like Reflex
    state = SimulatedReflexState()
    state.add_vector(magnitude=100, angle=0, name="F_1")
    state.add_vector(magnitude=100, angle=90, name="F_2")
    state.solve()

    print("\n  State vectors (as DTOs):")
    for v in state.vectors:
        print(f"    {v.name}: {v.magnitude} N at {v.angle}°")

    print("\n  State result:")
    if state.result and state.result.resultant:
        print(f"    Resultant: {state.result.resultant.magnitude:.3f} N at {state.result.resultant.angle:.1f}°")

    # =========================================================================
    # Example 4: Type hints work with Pylance
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 4: Type hints (Pylance-compatible)")
    print("-" * 70)

    print("""
    # These type aliases work in annotations:

    from qnty.problems.statics import parallelogram_law

    # For UI state (JSON-serializable DTOs)
    vectors: list[parallelogram_law.Vector] = []      # VectorDTO
    result: parallelogram_law.ResultDTO | None = None  # ResultDTO

    # The vector() function returns rich _Vector objects
    v = parallelogram_law.vector(...)  # _Vector (for computation)

    # Convert between them as needed
    dto = parallelogram_law.to_vector_dto(v)   # _Vector -> VectorDTO
    vec = parallelogram_law.from_vector_dto(dto)  # VectorDTO -> _Vector
    """)

    # =========================================================================
    # Example 5: Frontend Unit Conversion Workflow
    # =========================================================================
    print("-" * 70)
    print("Example 5: Frontend Unit Conversion Workflow")
    print("-" * 70)

    print("""
    Frontend sends:
    - User input: magnitude=450, unit="N", angle=60
    - User selects display unit: "lbf" (pounds-force)

    Backend workflow:
    1. Create vectors with user's input units (converted to SI internally)
    2. Solve the problem (all calculations in SI)
    3. Return results in user's selected display unit
    """)

    # Simulate frontend input (user enters values in Newtons)
    F_1 = parallelogram_law.create_vector_polar(magnitude=450, angle=60, unit="N", name="F_1")
    F_2 = parallelogram_law.create_vector_polar(magnitude=700, angle=-15, unit="N", name="F_2")

    # Solve (internally uses SI)
    result = parallelogram_law.solve(F_1, F_2)

    print("\n  Same result, different display units:")
    print()

    # Method 1: to_dto() with output_unit parameter
    dto_n = result.to_dto(output_unit="N")
    dto_lbf = result.to_dto(output_unit="lbf")

    if dto_n.resultant and dto_lbf.resultant:
        print(f"    In Newtons:      F_R = {dto_n.resultant.magnitude:.2f} N at {dto_n.resultant.angle:.1f} deg")
        print(f"    In pounds-force: F_R = {dto_lbf.resultant.magnitude:.2f} lbf at {dto_lbf.resultant.angle:.1f} deg")

    # Method 2: get_resultant_in() for quick access
    print("\n  Quick access with get_resultant_in():")
    result_n = result.get_resultant_in("N")
    result_lbf = result.get_resultant_in("lbf")
    if result_n and result_lbf:
        mag_n, _ = result_n
        mag_lbf, _ = result_lbf
        print(f"    {mag_n:.2f} N = {mag_lbf:.2f} lbf")

    # Method 3: get_vector_in() for specific vectors
    print("\n  Get specific vector in different unit:")
    f1_lbf = result.get_vector_in("F_1", "lbf")
    if f1_lbf and f1_lbf.magnitude:
        print(f"    F_1: {f1_lbf.magnitude:.2f} lbf (originally 450 N)")

    # =========================================================================
    # Example 6: Code-based analysis with multiple problems
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 6: Code-based analysis")
    print("-" * 70)

    # Solve multiple problems programmatically
    problems = [
        {"F1": (100, 0), "F2": (100, 90)},
        {"F1": (200, 45), "F2": (150, 135)},
        {"F1": (500, 30), "F2": (300, 120), "F3": (400, -60)},
    ]

    print("\n  Batch analysis:")
    for i, p in enumerate(problems):
        vectors = [
            parallelogram_law.create_vector_polar(magnitude=mag, angle=ang, unit="N", name=name)
            for name, (mag, ang) in p.items()
        ]
        result = parallelogram_law.solve(*vectors, output_unit="N")

        if result.success and result.resultant:
            # Access rich objects for detailed analysis
            dto = result.to_dto()
            if dto.resultant:
                print(f"    Problem {i+1}: {len(vectors)} vectors -> "
                      f"F_R = {dto.resultant.magnitude:.2f} N at {dto.resultant.angle:.1f}°")

    # =========================================================================
    # Example 7: The Key Benefit - ONE API to learn
    # =========================================================================
    print("\n" + "-" * 70)
    print("Example 7: The unified API benefit")
    print("-" * 70)

    print("""
    BEFORE (two separate APIs to learn):

        # For code:
        from qnty.problems.parallelogram_law import ParallelogramLawProblem
        from qnty.spatial.vectors import create_vector_polar, create_vector_resultant

        class MyProblem(ParallelogramLawProblem):
            F_1 = create_vector_polar(magnitude=450, angle=60, unit="N")
            F_2 = create_vector_polar(magnitude=700, angle=-15, unit="N")
            F_R = create_vector_resultant(F_1, F_2)

        # For UI:
        from qnty.integration import parallelogram_law

        v1 = parallelogram_law.create_vector(magnitude=450, angle=60, unit="N")
        result = parallelogram_law.solve(vectors=[v1, v2])

    AFTER (ONE unified API):

        from qnty.problems.statics import parallelogram_law

        F_1 = parallelogram_law.vector(magnitude=450, angle=60, unit="N")
        F_2 = parallelogram_law.vector(magnitude=700, angle=-15, unit="N")
        result = parallelogram_law.solve(F_1, F_2)

        # For code: use result directly
        print(result.resultant.magnitude)

        # For UI: convert to DTO
        dto = result.to_dto()
    """)

    print("=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
