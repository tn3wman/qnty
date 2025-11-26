"""
Parallelogram Law Example - Simulating a Reflex UI

This example demonstrates how to use qnty's unified parallelogram_law API
in a way that's compatible with a Reflex web UI where users can:
- Change input values (magnitudes, angles)
- Select different units
- Get results in their preferred units
- Generate solution reports

The example simulates user interactions by:
1. Creating a problem with initial values
2. "Changing" values (simulating UI input)
3. Getting results in different units
4. Generating a PDF report
"""

from pathlib import Path
from typing import Literal

from qnty.problems.statics import parallelogram_law

# =============================================================================
# Simulated Reflex State
# =============================================================================

class ProblemState:
    """
    Simulates a Reflex State class that would manage the UI state.

    In a real Reflex app, this would be:

        class ProblemState(rx.State):
            f1_magnitude: float = 450.0
            f1_unit: str = "N"
            f1_angle: float = 60.0
            ...
    """

    def __init__(self):
        # Input values (what user enters in UI)
        # Problem 2-1 from textbook: Two forces acting on a hook
        self.f1_magnitude: float = 450.0
        self.f1_unit: str = "N"
        self.f1_angle: float = 60.0
        self.f1_wrt: str = "+x"  # Angle measured from +x axis

        self.f2_magnitude: float = 700.0
        self.f2_unit: str = "N"
        self.f2_angle: float = 15.0
        self.f2_wrt: str = "-x"  # Angle measured from -x axis (15° below -x)

        # Output unit preferences
        self.result_force_unit: str = "N"
        self.result_angle_unit: str = "degree"

        # Computed results (updated after solve)
        self.fr_magnitude: float | None = None
        self.fr_angle: float | None = None
        self.fr_components: tuple[float, float] | None = None

        # Result object
        self._result: parallelogram_law.Result | None = None

    def solve(self) -> None:
        """
        Solve the problem with current input values.

        This is the event handler that would be called when the user
        clicks "Solve" in the UI.
        """
        # Create vectors using the unified API
        F_1 = parallelogram_law.create_vector_polar(
            magnitude=self.f1_magnitude,
            angle=self.f1_angle,
            unit=self.f1_unit,
            name="F_1",
            wrt=self.f1_wrt,
        )

        F_2 = parallelogram_law.create_vector_polar(
            magnitude=self.f2_magnitude,
            angle=self.f2_angle,
            unit=self.f2_unit,
            name="F_2",
            wrt=self.f2_wrt,
        )

        # Solve using the unified API
        self._result = parallelogram_law.solve(F_1, F_2)

        # Extract results in user's preferred units
        self._update_results()

    def _update_results(self) -> None:
        """Update result values from the solved problem."""
        if self._result is None or not self._result.success:
            return

        # Get results in user's preferred unit using to_dto
        dto = self._result.to_dto(output_unit=self.result_force_unit)

        if dto.resultant:
            self.fr_magnitude = dto.resultant.magnitude
            self.fr_angle = dto.resultant.angle
            self.fr_components = (dto.resultant.u, dto.resultant.v)

    def set_result_unit(self, unit: str) -> None:
        """
        Change the output unit for force results.

        This simulates user changing unit dropdown in UI.
        """
        self.result_force_unit = unit
        self._update_results()

    def generate_report(
        self,
        output_path: str | Path,
        format: Literal["markdown", "latex", "pdf"] = "pdf",
    ) -> None:
        """
        Generate a report of the solution.

        This would be triggered by a "Generate Report" button.

        Args:
            output_path: Path for the output file.
            format: Output format - 'markdown', 'latex', or 'pdf'.
        """
        if self._result is None:
            raise ValueError("Must solve problem before generating report")

        self._result.generate_report(output_path, format=format)


# =============================================================================
# Main Example
# =============================================================================

def main():
    """Run the example simulation."""
    print("=" * 60)
    print("Parallelogram Law Example - Reflex UI Simulation")
    print("=" * 60)

    # Create state (simulates Reflex State initialization)
    state = ProblemState()

    print("\n1. Initial Input Values:")
    print(f"   F_1: {state.f1_magnitude} {state.f1_unit} at {state.f1_angle}°")
    print(f"   F_2: {state.f2_magnitude} {state.f2_unit} at {state.f2_angle}°")

    # Solve the problem (simulates clicking "Solve" button)
    print("\n2. Solving problem...")
    state.solve()

    print("\n3. Results (in Newtons):")
    print(f"   F_R magnitude: {state.fr_magnitude:.3f} {state.result_force_unit}")
    print(f"   F_R angle: {state.fr_angle:.3f}°")
    if state.fr_components:
        print(f"   F_R components: ({state.fr_components[0]:.3f}, {state.fr_components[1]:.3f}) {state.result_force_unit}")

    # Change output unit (simulates user selecting different unit in dropdown)
    print("\n4. Changing output unit to 'lbf'...")
    state.set_result_unit("lbf")

    print("\n5. Results (in lbf):")
    print(f"   F_R magnitude: {state.fr_magnitude:.3f} {state.result_force_unit}")
    print(f"   F_R angle: {state.fr_angle:.3f}°")
    if state.fr_components:
        print(f"   F_R components: ({state.fr_components[0]:.3f}, {state.fr_components[1]:.3f}) {state.result_force_unit}")

    # Change back to N for report
    state.set_result_unit("N")

    # Generate reports
    print("\n6. Generating reports...")
    output_dir = Path(__file__).parent / "reports"
    output_dir.mkdir(exist_ok=True)

    # Generate markdown report
    md_path = output_dir / "problem_2_1_report.md"
    try:
        state.generate_report(md_path, format="markdown")
        print(f"   Markdown report saved to: {md_path}")
    except Exception as e:
        print(f"   Markdown report failed: {e}")

    # Generate PDF report
    report_path = output_dir / "problem_2_1_report.pdf"
    try:
        state.generate_report(report_path, format="pdf")
        print(f"   PDF report saved to: {report_path}")
    except Exception as e:
        print(f"   PDF report failed: {e}")

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)

    # Demonstrate multiple instances (important for Reflex)
    print("\n7. Testing multiple instances (for concurrent users)...")

    state2 = ProblemState()
    state2.f1_magnitude = 500.0
    state2.f1_angle = 45.0
    state2.solve()

    print(f"   State 1 F_R: {state.fr_magnitude:.3f} N")
    print(f"   State 2 F_R: {state2.fr_magnitude:.3f} N")
    print("   (Different values confirm instance isolation)")


if __name__ == "__main__":
    main()
