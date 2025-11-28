"""
Parallelogram Law Inverse Example - Problem 2-2

This example demonstrates the inverse parallelogram law problem where:
- The resultant force F_R is KNOWN (magnitude and direction)
- One component force F_2 is KNOWN
- The other component force F_1 is UNKNOWN (solve for magnitude and direction)

Problem 2-2 from Hibbeler's Engineering Mechanics: Statics:
"If the magnitude of the resultant force is to be 500 N, directed along
the positive y axis, determine the magnitude of force F and its direction theta."

Given:
- F_R = 500 N along +y axis
- F_2 = 700 N at 15 degrees from -x axis
- F_1 = ? (unknown magnitude and angle)

Solution (from textbook):
- F_1 = 960 N at 45.2 degrees from +x axis
"""

from pathlib import Path
from typing import Literal

from qnty.problems.statics import parallelogram_law as pl


class InverseProblemState:
    """
    State for inverse parallelogram law problem.

    In the inverse problem, we know the resultant and want to find
    an unknown component force.
    """

    def __init__(self):
        # F_1: Unknown force (what we want to solve for)
        # Using ellipsis (...) to indicate unknown values
        self.f1_magnitude = ...  # Unknown
        self.f1_angle = ...      # Unknown
        self.f1_unit: str = "N"
        self.f1_wrt: str = "+x"

        # F_2: Known force (700 N at 15 degrees from -x axis)
        self.f2_magnitude: float = 700.0
        self.f2_angle: float = 15.0
        self.f2_unit: str = "N"
        self.f2_wrt: str = "-x"

        # F_R: Known resultant (constraint)
        # 500 N along +y axis (i.e., 0 degrees from +y)
        self.fr_magnitude: float = 500.0
        self.fr_angle: float = 0.0  # 0 degrees from +y = 90 degrees from +x
        self.fr_unit: str = "N"
        self.fr_wrt: str = "+y"

        # Output unit preferences
        self.result_force_unit: str = "N"
        self.result_angle_unit: str = "degree"

        # Solved results
        self.solved_f1_magnitude: float | None = None
        self.solved_f1_angle: float | None = None
        self.solved_f1_components: tuple[float, float] | None = None

        # Result object
        self._result: pl.Result | None = None

    def solve(self) -> None:
        """
        Solve the inverse problem.

        Creates F_1 with unknown magnitude/angle, F_2 as known,
        and F_R as a known resultant constraint.
        """
        # F_1: Unknown force (use ellipsis for unknowns)
        F_1 = pl.create_vector_polar(
            magnitude=...,  # Unknown
            angle=...,      # Unknown
            unit=self.f1_unit,
            wrt=self.f1_wrt,
            name="F_1",
        )

        # F_2: Known force
        F_2 = pl.create_vector_polar(
            magnitude=self.f2_magnitude,
            angle=self.f2_angle,
            unit=self.f2_unit,
            wrt=self.f2_wrt,
            name="F_2",
        )

        # F_R: Known resultant (as a constraint)
        # This tells the solver: F_1 + F_2 = F_R
        F_R = pl.create_vector_resultant_polar(
            F_1, F_2,
            magnitude=self.fr_magnitude,
            angle=self.fr_angle,
            unit=self.fr_unit,
            wrt=self.fr_wrt,
            name="F_R",
        )

        # Define the problem class dynamically
        class Problem2_2:
            name = "Problem 2-2"

        Problem2_2.F_1 = F_1
        Problem2_2.F_2 = F_2
        Problem2_2.F_R = F_R

        # Solve using solve_class
        self._result = pl.solve_class(Problem2_2, output_unit=self.result_force_unit)

        # Extract solved F_1 values
        self._update_results()

    def _update_results(self) -> None:
        """Extract the solved F_1 values from the result."""
        if self._result is None or not self._result.success:
            return

        # Get F_1 from the solved vectors
        f1_vec = self._result.vectors.get("F_1")
        if f1_vec is None:
            return

        # Get as DTO in user's preferred unit
        f1_dto = self._result.get_vector_in("F_1", self.result_force_unit)
        if f1_dto:
            self.solved_f1_magnitude = f1_dto.magnitude
            self.solved_f1_angle = f1_dto.angle
            self.solved_f1_components = (f1_dto.u, f1_dto.v)

    def set_result_unit(self, unit: str) -> None:
        """Change the output unit for force results."""
        self.result_force_unit = unit
        self._update_results()

    def generate_report(
        self,
        output_path: str | Path,
        format: Literal["markdown", "latex", "pdf"] = "pdf",
    ) -> None:
        """Generate a report of the solution."""
        if self._result is None:
            raise ValueError("Must solve problem before generating report")

        self._result.generate_report(output_path, format=format)


def main():
    """Run the inverse parallelogram law example."""
    print("=" * 70)
    print("Parallelogram Law INVERSE Example - Problem 2-2")
    print("=" * 70)
    print()
    print("Problem: Find F_1 (magnitude and direction) given:")
    print("  - F_R = 500 N along +y axis (known resultant)")
    print("  - F_2 = 700 N at 15 deg from -x axis (known)")
    print("  - F_1 = ? (unknown)")
    print()
    print("Expected solution (from textbook):")
    print("  - F_1 = 960 N at 45.2 deg from +x axis")
    print()

    # Create state
    state = InverseProblemState()

    print("1. Input Values:")
    print(f"   F_1: magnitude={state.f1_magnitude}, angle={state.f1_angle} (UNKNOWN)")
    print(f"   F_2: {state.f2_magnitude} {state.f2_unit} at {state.f2_angle} deg from {state.f2_wrt}")
    print(f"   F_R: {state.fr_magnitude} {state.fr_unit} at {state.fr_angle} deg from {state.fr_wrt} (CONSTRAINT)")

    # Solve
    print("\n2. Solving inverse problem...")
    state.solve()

    if state._result and state._result.success:
        print("\n3. SOLVED! Results:")
        print(f"   F_1 magnitude: {state.solved_f1_magnitude:.1f} {state.result_force_unit}")
        print(f"   F_1 angle: {state.solved_f1_angle:.1f} deg from +x")
        if state.solved_f1_components:
            print(f"   F_1 components: ({state.solved_f1_components[0]:.1f}, {state.solved_f1_components[1]:.1f}) {state.result_force_unit}")

        # Compare with expected
        print("\n4. Comparison with textbook solution:")
        expected_mag = 960.0
        expected_angle = 45.2
        mag_error = abs(state.solved_f1_magnitude - expected_mag) / expected_mag * 100
        angle_error = abs(state.solved_f1_angle - expected_angle)
        print(f"   Expected magnitude: {expected_mag} N, Got: {state.solved_f1_magnitude:.1f} N (error: {mag_error:.2f}%)")
        print(f"   Expected angle: {expected_angle} deg, Got: {state.solved_f1_angle:.1f} deg (error: {angle_error:.2f} deg)")

        # Generate reports
        print("\n5. Generating reports...")
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(exist_ok=True)

        # Generate markdown report
        md_path = output_dir / "problem_2_2_inverse_report.md"
        try:
            state.generate_report(md_path, format="markdown")
            print(f"   Markdown report saved to: {md_path}")
        except Exception as e:
            print(f"   Markdown report failed: {e}")

        # Generate PDF report
        pdf_path = output_dir / "problem_2_2_inverse_report.pdf"
        try:
            state.generate_report(pdf_path, format="pdf")
            print(f"   PDF report saved to: {pdf_path}")
        except Exception as e:
            print(f"   PDF report failed: {e}")

    else:
        print("\n3. FAILED!")
        if state._result:
            print(f"   Error: {state._result.error}")

    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
