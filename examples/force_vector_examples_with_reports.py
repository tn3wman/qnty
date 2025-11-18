"""
Complete vector equilibrium example with PDF report generation.

Demonstrates how VectorEquilibriumProblem integrates with qnty's
built-in report generation system to create professional PDF reports
with step-by-step calculations.
"""

from pathlib import Path
from qnty.problems.vector_equilibrium import ParallelogramLaw
from qnty.spatial.force_vector import ForceVector
from qnty.extensions.reporting import generate_report

# Create reports directory
REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# =============================================================================
# EXAMPLE 1: Simple Cable Problem with Report
# =============================================================================

class Problem1(ParallelogramLaw):
    name = "Problem 1"
    description = """
    If $\\theta=60^{\\circ}$ and $F=450 \\mathrm{~N}$, determine the magnitude of the resultant force and its direction, measured counterclockwise from the positive $x$ axis.
    """

    # Define known forces
    F_1 = ForceVector(
        magnitude=450,
        angle=60,
        unit="N",
        name="F 1",
        description="Force 1"
    )

    F_2 = ForceVector(
        magnitude=700,
        angle=195,
        unit="N",
        name="F 2",
        description="Force 2"
    )

    # Define unknown resultant
    F_R = ForceVector.unknown("Resultant Force", is_resultant=True)


def example_1_with_pdf_report():
    """Generate PDF report for cable problem."""


    # Create and solve problem
    problem = Problem1()
    solution = problem.solve()

    # Display results
    F_R = solution["F_R"]
    print(f"\nProblem: {problem.name}")
    print(f"Solved: {F_R}")

    try:
        # Generate PDF report (requires pdflatex)
        output_file = REPORTS_DIR / "cable_force_report.pdf"
        generate_report(problem, output_file, format="pdf")
        print(f"\n✓ PDF report generated: {output_file}")
        print("  (Open with a PDF viewer to see formatted report)")
    except Exception as e:
        print(f"\n⚠ PDF generation failed: {e}")
        print("  Falling back to Markdown format...")

        # Generate markdown as fallback
        output_file = REPORTS_DIR / "cable_force_report_fallback.md"
        generate_report(problem, output_file, format="markdown")
        print(f"  ✓ Markdown report generated instead: {output_file}")

    print()





# =============================================================================
# RUN ALL EXAMPLES
# =============================================================================

def run_all_examples():
    """Run all examples with report generation."""
    examples = [
        ("Example 1", example_1_with_pdf_report),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            print()

if __name__ == "__main__":
    run_all_examples()
