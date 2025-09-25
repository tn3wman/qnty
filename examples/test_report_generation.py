"""
Test script for demonstrating report generation feature.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.algebra import equation
from qnty.extensions.reporting import generate_report


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure according to ASME B31.3."

    # Known variables (given values)
    P = Pressure("Design Pressure").set(90).pound_force_per_square_inch
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).pound_force_per_square_inch
    E = Dimensionless("Quality Factor").set(0.8).dimensionless
    W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless
    Y = Dimensionless("Y Coefficient").set(0.4).dimensionless

    # Unknown variables (to be calculated)
    T = Length("Wall Thickness")
    d = Length("Inside Diameter")
    t = Length("Pressure Design Thickness")
    t_m = Length("Minimum Required Thickness")
    P_max = Pressure("Maximum Pressure")

    # Engineering equations
    T_eqn = equation(T, T_bar * (1 - U_m))
    d_eqn = equation(d, D - 2 * T)
    t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = equation(t_m, t + c)
    P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))


def test_report_generation():
    """Test report generation in different formats."""

    print("Creating engineering problem...")
    problem = StraightPipeInternal()

    print(f"\nProblem: {problem.name}")
    print(f"Description: {problem.description}")
    print(f"Number of equations: {len(problem.equations)}")
    print(f"Known variables: {len(problem.get_known_variables())}")
    print(f"Unknown variables: {len(problem.get_unknown_variables())}")

    print("\nSolving problem...")
    try:
        solution = problem.solve()
        print("[SUCCESS] Problem solved successfully!")

        print("\nSolved values:")
        for symbol, var in problem.variables.items():
            if symbol not in problem.get_known_variables():
                print(f"  {symbol}: {var.value:.6g} {var.preferred if hasattr(var, 'preferred') else ''}")

        # Create output directory if it doesn't exist
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        # Generate Markdown report
        print("\nGenerating Markdown report...")
        markdown_path = output_dir / "pipe_thickness_report.md"
        generate_report(problem, markdown_path, format="markdown")
        print(f"[SUCCESS] Markdown report saved to: {markdown_path}")

        # Generate LaTeX report
        print("\nGenerating LaTeX report...")
        latex_path = output_dir / "pipe_thickness_report.tex"
        generate_report(problem, latex_path, format="latex")
        print(f"[SUCCESS] LaTeX report saved to: {latex_path}")

        # Try to generate PDF report (requires tectonic)
        print("\nGenerating PDF report...")
        try:
            pdf_path = output_dir / "pipe_thickness_report.pdf"
            generate_report(problem, pdf_path, format="pdf")
            print(f"[SUCCESS] PDF report saved to: {pdf_path}")
        except Exception as e:
            print(f"[FAILED] PDF generation failed: {e}")
            print("  (This is expected if tectonic is not properly configured)")

        print("\n[SUCCESS] Report generation test completed successfully!")

        # Display a sample of the Markdown report
        print("\n" + "="*60)
        print("Sample of generated Markdown report:")
        print("="*60)
        with open(markdown_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print("".join(lines[:50]))  # Show first 50 lines
            if len(lines) > 50:
                print("... (report continues)")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_report_generation()