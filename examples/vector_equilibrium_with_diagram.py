"""
Vector equilibrium examples with automatic diagram generation.

Demonstrates how to create professional engineering reports with
vector diagrams automatically included in PDF and Markdown outputs.
"""

from pathlib import Path
from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector
from qnty.extensions.reporting import generate_report

# Create reports directory
REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# =============================================================================
# EXAMPLE 1: Simple Two-Force Problem
# =============================================================================

class TwoForceProblem(VectorEquilibriumProblem):
    """
    Find resultant of two forces.

    Given:
    - F1 = 450 N at 60°
    - F2 = 700 N at 195°

    Find: Resultant force FR
    """
    name = "Two Force Resultant"
    description = "Determine the magnitude and direction of the resultant of two forces"

    F_1 = ForceVector(magnitude=450, angle=60, unit="N", name="F_1", description="Force 1")
    F_2 = ForceVector(magnitude=700, angle=195, unit="N", name="F_2", description="Force 2")
    F_R = ForceVector.unknown("F_R", is_resultant=True)


def example_1_two_forces():
    """Generate report with diagram for two-force problem."""
    print("="*80)
    print("EXAMPLE 1: Two Force Resultant")
    print("="*80)

    # Solve problem
    problem = TwoForceProblem()
    solution = problem.solve()

    # Display results
    FR = solution['F_R']
    print(f"\nResultant Force:")
    print(f"  Magnitude: {FR.magnitude}")
    print(f"  Direction: {FR.angle}")

    # Generate report with diagram
    output_file = REPORTS_DIR / "two_force_resultant.pdf"
    generate_report(problem, output_file, format="pdf")
    print(f"\nReport generated: {output_file}")
    print("  (Includes vector diagram showing forces and angles)")
    print()


# =============================================================================
# EXAMPLE 2: Three-Force Equilibrium
# =============================================================================

class ThreeForceProblem(VectorEquilibriumProblem):
    """
    Three forces in equilibrium.

    Given three forces acting on a point, find the resultant.
    This demonstrates a more complex scenario with forces at various angles.
    """
    name = "Three Force Equilibrium"
    description = "Find the resultant of three forces acting at a point"

    F_1 = ForceVector(magnitude=250, angle=90, unit="lbf", name="F_1", description="Vertical force")
    F_2 = ForceVector(magnitude=375, angle=30, unit="lbf", name="F_2", description="Angled force")
    F_3 = ForceVector(magnitude=375, angle=225, unit="lbf", name="F_3", description="Diagonal force")
    F_R = ForceVector.unknown("F_R", is_resultant=True)


def example_2_three_forces():
    """Generate report with diagram for three-force problem."""
    print("="*80)
    print("EXAMPLE 2: Three Force Equilibrium")
    print("="*80)

    # Solve problem
    problem = ThreeForceProblem()
    solution = problem.solve()

    # Display results
    FR = solution['F_R']
    print(f"\nResultant Force:")
    print(f"  Magnitude: {FR.magnitude}")
    print(f"  Direction: {FR.angle}")
    print(f"  X-component: {FR.x}")
    print(f"  Y-component: {FR.y}")

    # Generate both PDF and Markdown
    pdf_file = REPORTS_DIR / "three_force_equilibrium.pdf"
    md_file = REPORTS_DIR / "three_force_equilibrium.md"

    generate_report(problem, pdf_file, format="pdf")
    print(f"\nPDF Report: {pdf_file}")

    generate_report(problem, md_file, format="markdown")
    print(f"Markdown Report: {md_file}")

    print("\nBoth reports include the vector diagram automatically!")
    print()


# =============================================================================
# EXAMPLE 3: Horizontal and Vertical Forces
# =============================================================================

class HorizontalVerticalProblem(VectorEquilibriumProblem):
    """
    Forces in cardinal directions.

    Demonstrates forces aligned with coordinate axes.
    """
    name = "Cardinal Direction Forces"
    description = "Forces aligned with coordinate axes (0°, 90°, 180°, 270°)"

    F_East = ForceVector(magnitude=500, angle=0, unit="N", name="F_East", description="Eastward force")
    F_North = ForceVector(magnitude=300, angle=90, unit="N", name="F_North", description="Northward force")
    F_West = ForceVector(magnitude=200, angle=180, unit="N", name="F_West", description="Westward force")
    F_R = ForceVector.unknown("F_R", is_resultant=True)


def example_3_cardinal_forces():
    """Generate report with diagram for cardinal direction forces."""
    print("="*80)
    print("EXAMPLE 3: Cardinal Direction Forces")
    print("="*80)

    # Solve problem
    problem = HorizontalVerticalProblem()
    solution = problem.solve()

    # Display results
    FR = solution['F_R']
    print(f"\nResultant Force:")
    print(f"  Magnitude: {FR.magnitude}")
    print(f"  Direction: {FR.angle}")

    # Generate report
    output_file = REPORTS_DIR / "cardinal_forces.pdf"
    generate_report(problem, output_file, format="pdf")
    print(f"\nReport generated: {output_file}")
    print()


# =============================================================================
# Run all examples
# =============================================================================

def run_all_examples():
    """Run all vector equilibrium examples with diagrams."""
    print("\n" + "="*80)
    print("VECTOR EQUILIBRIUM EXAMPLES WITH AUTOMATIC DIAGRAMS")
    print("="*80)
    print("\nThese examples demonstrate:")
    print("  • Automatic vector diagram generation")
    print("  • Properly scaled and labeled force vectors")
    print("  • Angle annotations with arcs")
    print("  • Integration into PDF and Markdown reports")
    print()

    examples = [
        example_1_two_forces,
        example_2_three_forces,
        example_3_cardinal_forces,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"ERROR in {example.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print("="*80)
    print("ALL EXAMPLES COMPLETE!")
    print("="*80)
    print(f"\nReports saved to: {REPORTS_DIR}")
    print("\nNOTE: To include diagrams, matplotlib must be installed:")
    print("  pip install matplotlib>=3.7.0")
    print("\n  OR")
    print("\n  pip install qnty[reporting]")
    print()


if __name__ == "__main__":
    run_all_examples()
