"""
Example: Problem 2-2 - Solving for unknown force with known resultant.

Problem: If the magnitude of the resultant force is to be 500 N, directed
along the positive y-axis, and one force F_2 = 700 N at 195° is known,
determine the magnitude of force F_1 and its direction θ.

This demonstrates the pattern: F_1 (unknown) + F_2 (known) = F_R (known resultant)
"""

from pathlib import Path

from qnty.extensions.reporting import generate_report
from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector


class Problem_2_2(VectorEquilibriumProblem):
    """
    Solve for unknown force given known resultant and known force.

    Given:
    - F_R = 500 N at 90° (desired resultant, along positive y-axis)
    - F_2 = 700 N at 195° (known force)

    Find:
    - F_1: magnitude and direction θ
    """
    name = "Problem 2-2: Find Force with Known Resultant"
    description = """
    If the resultant force is to be 500 N directed along the positive y-axis,
    and F_2 = 700 N at 195°, determine the magnitude and direction of F_1.
    """

    # Unknown force to solve for (not a resultant - just a component force)
    F_1 = ForceVector.unknown("F_1")

    # Known force
    F_2 = ForceVector(
        magnitude=700,
        angle=195,  # measured counterclockwise from positive x-axis
        unit="N",
        name="F_2",
        description="Known force"
    )

    # Known resultant (what we want the sum to be)
    F_R = ForceVector(
        magnitude=500,
        angle=90,  # positive y-axis
        unit="N",
        name="F_R",
        description="Desired resultant force",
        is_resultant=True
    )


def main():
    # Create and solve the problem
    problem = Problem_2_2()
    solution = problem.solve()

    # Generate report
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    print("Generating reports...")
    pdf_file = reports_dir / "problem_2_2.pdf"
    md_file = reports_dir / "problem_2_2.md"
    tex_file = reports_dir / "problem_2_2.tex"

    try:
        generate_report(problem, pdf_file, format="pdf")
        print(f"  PDF: {pdf_file}")
    except Exception as e:
        print(f"  PDF generation skipped: {e}")

    try:
        generate_report(problem, md_file, format="markdown")
        print(f"  Markdown: {md_file}")
    except Exception as e:
        print(f"  Markdown generation skipped: {e}")

    try:
        generate_report(problem, tex_file, format="latex")
        print(f"  LaTeX: {tex_file}")
    except Exception as e:
        print(f"  LaTeX generation skipped: {e}")

if __name__ == "__main__":
    main()
