"""
Enhanced pipe thickness calculation example demonstrating output unit specification.

This shows how to specify desired output units for unknown variables that will be
reflected in both terminal output and report generation.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.algebra import equation
from qnty.extensions.reporting import generate_report


class PipeThicknessWithOutputUnits(Problem):
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

    # Unknown variables with specified output units
    T = Length("Wall Thickness").output_unit("inch")  # Result in inches instead of meters
    d = Length("Inside Diameter").output_unit("inch")  # Result in inches instead of meters
    t = Length("Pressure Design Thickness").output_unit("inch")  # Result in inches
    t_m = Length("Minimum Required Thickness").output_unit("inch")  # Result in inches
    P_max = Pressure("Maximum Pressure").output_unit("psi")  # Result in psi instead of Pa

    # Engineering equations
    T_eqn = equation(T, T_bar * (1 - U_m))
    d_eqn = equation(d, D - 2 * T)
    t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = equation(t_m, t + c)
    P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))


def demonstrate_output_units():
    """Demonstrate the output unit specification feature."""

    print("="*80)
    print("ENHANCED PIPE THICKNESS CALCULATION")
    print("Demonstrating Output Unit Specification Feature")
    print("="*80)

    print("\nCreating pipe thickness problem with custom output units...")
    problem = PipeThicknessWithOutputUnits()

    print(f"\nProblem: {problem.name}")
    print(f"Description: {problem.description}")
    print(f"Number of equations: {len(problem.equations)}")
    print(f"Known variables: {len(problem.get_known_variables())}")
    print(f"Unknown variables: {len(problem.get_unknown_variables())}")

    # Show the output unit specifications
    print(f"\nOutput unit specifications:")
    output_units_specified = False
    for symbol, var in problem.variables.items():
        if hasattr(var, '_output_unit') and var._output_unit:
            print(f"  {symbol} ({var.name}): will display in '{var._output_unit.symbol}'")
            output_units_specified = True

    if not output_units_specified:
        print("  No output units specified - will use SI units (meters, Pa)")

    print("\nSolving problem...")
    try:
        solution = problem.solve()
        print("[SUCCESS] Problem solved successfully!")

        print("\nSOLVED VALUES (in specified output units):")
        print("-" * 60)
        for symbol, var in problem.variables.items():
            if symbol not in problem.get_known_variables():
                # Show both the display value and the underlying SI value
                si_value = f"{var.value:.6g}" if var.value else "N/A"
                print(f"  {symbol:8} ({var.name:30}): {str(var):>12} (SI: {si_value})")

        print("\n" + "="*80)
        print("GENERATING REPORTS...")
        print("="*80)

        # Create output directory if it doesn't exist
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        # Generate Markdown report
        print("\nGenerating Markdown report...")
        markdown_path = output_dir / "pipe_thickness_output_units.md"
        generate_report(problem, markdown_path, format="markdown")
        print(f"[SUCCESS] Markdown report saved to: {markdown_path}")

        # Generate LaTeX report
        print("\nGenerating LaTeX report...")
        latex_path = output_dir / "pipe_thickness_output_units.tex"
        generate_report(problem, latex_path, format="latex")
        print(f"[SUCCESS] LaTeX report saved to: {latex_path}")

        # Try to generate PDF report
        print("\nGenerating PDF report...")
        try:
            pdf_path = output_dir / "pipe_thickness_output_units.pdf"
            generate_report(problem, pdf_path, format="pdf")
            print(f"[SUCCESS] PDF report saved to: {pdf_path}")
        except Exception as e:
            print(f"[INFO] PDF generation skipped: {e}")

        # Show a sample of the results from the report
        print(f"\n" + "="*80)
        print("SAMPLE FROM GENERATED REPORT")
        print("="*80)
        with open(markdown_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Show the summary section
            if "## 5. Summary of Results" in content:
                summary_start = content.find("## 5. Summary of Results")
                summary_end = content.find("---", summary_start)
                if summary_end != -1:
                    print(content[summary_start:summary_end].strip())

        print(f"\n" + "="*80)
        print("KEY BENEFITS OF OUTPUT UNIT SPECIFICATION:")
        print("="*80)
        print("+ Results display in engineering-friendly units (inches, psi)")
        print("+ Calculations still performed in SI units for accuracy")
        print("+ Reports automatically show values in specified units")
        print("+ Terminal output uses desired units")
        print("+ No performance impact - conversion happens only at display time")
        print("+ Fully backward compatible - existing code works unchanged")

        print(f"\n" + "="*80)
        print("USAGE EXAMPLE:")
        print("="*80)
        print("# Instead of:")
        print("T = Length('Wall Thickness')  # Would show: 0.00326707 m")
        print()
        print("# Use:")
        print("T = Length('Wall Thickness').output_unit('inch')  # Shows: 0.128625 in")
        print("="*80)

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demonstrate_output_units()