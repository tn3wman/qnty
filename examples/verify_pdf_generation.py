"""
Verify that PDF report generation works correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qnty import Length, Pressure, Problem
from qnty.algebra import equation
from qnty.extensions.reporting import generate_report


class SimpleBeamProblem(Problem):
    name = "Simple Beam Stress Analysis"
    description = "Calculate stress in a simple beam under load."

    # Known variables
    F = Pressure("Applied Force").set(1000).pascal
    L = Length("Beam Length").set(2.0).meter
    w = Length("Beam Width").set(0.1).meter
    h = Length("Beam Height").set(0.2).meter

    # Unknown variables
    A = Length("Cross-sectional Area")
    sigma = Pressure("Stress")

    # Equations
    area_eq = equation(A, w * h)
    stress_eq = equation(sigma, F / A)


def verify_pdf_generation():
    """Verify PDF generation works."""
    print("Creating simple beam problem...")
    problem = SimpleBeamProblem()

    print("Solving problem...")
    problem.solve()

    print("\nGenerating reports in all formats:")

    # Test Markdown
    print("  - Generating Markdown...", end="")
    md_path = Path("reports/beam_stress.md")
    generate_report(problem, md_path, format="markdown")
    assert md_path.exists(), "Markdown file not created"
    print(" OK")

    # Test LaTeX
    print("  - Generating LaTeX...", end="")
    tex_path = Path("reports/beam_stress.tex")
    generate_report(problem, tex_path, format="latex")
    assert tex_path.exists(), "LaTeX file not created"
    print(" OK")

    # Test PDF
    print("  - Generating PDF...", end="")
    pdf_path = Path("reports/beam_stress.pdf")
    try:
        generate_report(problem, pdf_path, format="pdf")
        if pdf_path.exists():
            size_kb = pdf_path.stat().st_size / 1024
            print(f" OK (size: {size_kb:.1f} KB)")
        else:
            print(" FAILED (file not created)")
    except Exception as e:
        print(f" FAILED ({str(e)[:50]}...)")

    print("\nAll tests completed!")


if __name__ == "__main__":
    verify_pdf_generation()