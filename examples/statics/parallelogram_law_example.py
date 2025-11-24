"""
Parallelogram Law Example - Simulating a Reflex UI

This example demonstrates how to use qnty's ParallelogramLawProblem
with the new _Vector-based approach in a way that's compatible with
a Reflex web UI where users can:
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

from qnty.extensions.reporting import generate_report
from qnty.problems.parallelogram_law import ParallelogramLawProblem
from qnty.spatial.vectors import create_vector_polar, create_vector_resultant

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
        self.f1_magnitude: float = 450.0
        self.f1_unit: str = "N"
        self.f1_angle: float = 60.0
        self.f1_angle_ref: str = "+x"

        self.f2_magnitude: float = 700.0
        self.f2_unit: str = "N"
        self.f2_angle: float = 15.0
        self.f2_angle_ref: str = "-x"

        # Output unit preferences
        self.result_force_unit: str = "N"
        self.result_angle_unit: str = "degree"

        # Computed results (updated after solve)
        self.fr_magnitude: float | None = None
        self.fr_angle: float | None = None
        self.fr_components: tuple[float, float, float] | None = None

        # Problem instance
        self._problem: ParallelogramLawProblem | None = None

    def solve(self) -> None:
        """
        Solve the problem with current input values.

        This is the event handler that would be called when the user
        clicks "Solve" in the UI.
        """
        # Create problem class dynamically with current values
        # In Reflex, this would be triggered by an event handler

        class DynamicProblem(ParallelogramLawProblem):
            name = "Problem 2-1"
            description = """
            Determine the magnitude of the resultant force and its direction,
            measured counterclockwise from the positive x axis.
            """

            F_1 = create_vector_polar(
                magnitude=self.f1_magnitude,
                unit=self.f1_unit,
                angle=self.f1_angle,
                wrt=self.f1_angle_ref,
            )

            F_2 = create_vector_polar(
                magnitude=self.f2_magnitude,
                unit=self.f2_unit,
                angle=self.f2_angle,
                wrt=self.f2_angle_ref,
            )

            F_R = create_vector_resultant(F_1, F_2)

        # Instantiate and compute
        self._problem = DynamicProblem()

        # Extract results in user's preferred units
        self._update_results()

    def _update_results(self) -> None:
        """Update result values from the solved problem."""
        if self._problem is None:
            return

        fr = self._problem.F_R

        # Get magnitude in user's preferred unit
        self.fr_magnitude = fr.magnitude_in(self.result_force_unit)

        # Get angle in user's preferred unit and reference
        self.fr_angle = fr.angle_in(self.result_angle_unit, wrt="+x")

        # Get components in user's preferred unit
        components = fr.to_array()
        if fr._unit:
            # Convert from SI to display unit
            from qnty.core.unit import ureg
            unit = ureg.resolve(self.result_force_unit)
            if unit:
                factor = unit.si_factor
                components = [c / factor for c in components]
        self.fr_components = tuple(components)

    def set_result_unit(self, unit: str) -> None:
        """
        Change the output unit for force results.

        This simulates user changing unit dropdown in UI.
        """
        self.result_force_unit = unit
        self._update_results()

    def generate_report(self, output_path: str | Path) -> None:
        """
        Generate a PDF report of the solution.

        This would be triggered by a "Generate Report" button.
        """
        if self._problem is None:
            raise ValueError("Must solve problem before generating report")

        # Mark problem as solved for report generator
        self._problem.is_solved = True

        generate_report(self._problem, output_path, format="pdf")


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
    print(f"   F_1: {state.f1_magnitude} {state.f1_unit} at {state.f1_angle}° wrt {state.f1_angle_ref}")
    print(f"   F_2: {state.f2_magnitude} {state.f2_unit} at {state.f2_angle}° wrt {state.f2_angle_ref}")

    # Solve the problem (simulates clicking "Solve" button)
    print("\n2. Solving problem...")
    state.solve()

    print("\n3. Results (in Newtons):")
    print(f"   F_R magnitude: {state.fr_magnitude:.3f} {state.result_force_unit}")
    print(f"   F_R angle: {state.fr_angle:.3f}° (wrt +x)")
    if state.fr_components:
        print(f"   F_R components: ({state.fr_components[0]:.3f}, {state.fr_components[1]:.3f}, {state.fr_components[2]:.3f}) {state.result_force_unit}")

    # Change output unit (simulates user selecting different unit in dropdown)
    print("\n4. Changing output unit to 'lbf'...")
    state.set_result_unit("lbf")

    print("\n5. Results (in lbf):")
    print(f"   F_R magnitude: {state.fr_magnitude:.3f} {state.result_force_unit}")
    print(f"   F_R angle: {state.fr_angle:.3f}° (wrt +x)")
    if state.fr_components:
        print(f"   F_R components: ({state.fr_components[0]:.3f}, {state.fr_components[1]:.3f}, {state.fr_components[2]:.3f}) {state.result_force_unit}")

    # Change back to N for report
    state.set_result_unit("N")

    # Generate PDF report
    print("\n6. Generating PDF report...")
    output_dir = Path(__file__).parent / "reports"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "problem_2_1_report.pdf"

    # Generate markdown report first (easier to review)
    md_path = output_dir / "problem_2_1_report.md"
    try:
        generate_report(state._problem, md_path, format="markdown")
        print(f"   Markdown report saved to: {md_path}")
    except Exception as e:
        print(f"   Markdown report failed: {e}")

    # Then generate PDF report
    try:
        state.generate_report(report_path)
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
