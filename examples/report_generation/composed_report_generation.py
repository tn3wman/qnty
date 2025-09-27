"""
Enhanced pipe thickness calculation example demonstrating output unit specification.

This shows how to specify desired output units for unknown variables that will be
reflected in both terminal output and report generation.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from qnty import Dimensionless, Length, Pressure, Problem, cond_expr, min_expr
from qnty.algebra import equation, geq, gt, lt
from qnty.extensions.reporting import generate_report
from qnty.problems.rules import add_rule


# Define a composed problem that includes another problem as a sub-component
class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    P = Pressure("Design Pressure").set(90).pound_force_per_square_inch
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).pound_force_per_square_inch
    E = Dimensionless("Quality Factor").set(0.8).dimensionless
    W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless

    Y = Dimensionless("Y Coefficient").set(0.4).dimensionless

    T = Length("Wall Thickness")
    d = Length("Inside Diameter")
    t = Length("Pressure Design Thickness")
    t_m = Length("Minimum Required Thickness")
    P_max = Pressure("Pressure, Maximum")

    # Equations
    T_eqn = equation(T, T_bar * (1 - U_m))
    d_eqn = equation(d, D - 2 * T)
    t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = equation(t_m, t + c)
    P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    # ASME B31.3 Section 304.1.1 Y coefficient logic
    # Explicit handling of both conditions per ASME B31.3
    Y_eqn = equation(Y,
        cond_expr(
            lt(t, D / 6),
            Y,  # Table value for t < D/6
            cond_expr(
                geq(t, D / 6),
                (d + 2 * c) / (D + d + 2 * c),  # Calculated for t >= D/6
                Y,  # Fallback (should not be reached)
            ),
        )
    )

    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    thick_wall_check = add_rule(
        geq(t, D / 6),
        "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

    pressure_ratio_check = add_rule(
        gt(P, (S * E) * 0.385),
        "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )


def create_straight_pipe_internal():
    return StraightPipeInternal()


class PipeBends(Problem):
    s = create_straight_pipe_internal()

    s.Y.set(0.4).dimensionless

    R_1 = Length("Bend Radius").set(5).inch
    I_i = Dimensionless("Intrados Correction Factor")
    I_e = Dimensionless("Extrados Correction Factor")
    t_i = Length("Design Thickness, Inside Bend")
    t_e = Length("Design Thickness, Outside Bend")
    t_m_i = Length("Minimum Required Thickness, Inside Bend")
    t_m_e = Length("Minimum Required Thickness, Outside Bend")
    P_max_i = Pressure("Maximum Pressure, Inside Bend")
    P_max_e = Pressure("Maximum Pressure, Outside Bend")
    P_max = Pressure("Maximum Allowable Pressure")

    # Equations
    I_i_eqn = equation(I_i, (4 * (R_1 / s.D) - 1) / (4 * (R_1 / s.D) - 2))
    I_e_eqn = equation(I_e, (4 * (R_1 / s.D) + 1) / (4 * (R_1 / s.D) + 2))

    t_i_eqn = equation(t_i, (s.P * s.D) / (2 * ((s.S * s.E * s.W / I_i) + s.P * s.Y)))
    t_e_eqn = equation(t_e, (s.P * s.D) / (2 * ((s.S * s.E * s.W / I_e) + s.P * s.Y)))

    t_m_i_eqn = equation(t_m_i, t_i + s.c)
    t_m_e_eqn = equation(t_m_e, t_e + s.c)

    P_max_i_eqn = equation(P_max_i, 2 * s.E * s.S * s.W * s.T / (I_i * (s.D - 2 * s.Y * s.T)))

    P_max_e_eqn = equation(P_max_e, 2 * s.E * s.S * s.W * s.T / (I_e * (s.D - 2 * s.Y * s.T)))

    P_max_eqn = equation(P_max, min_expr(P_max_i, P_max_e, s.P_max))


def create_pipe_bends():
    return PipeBends()


def demonstrate_report_gen():
    """Demonstrate the output unit specification feature."""

    print("="*80)
    print("ENHANCED PIPE THICKNESS CALCULATION")
    print("Demonstrating Output Unit Specification Feature")
    print("="*80)

    print("\nCreating pipe thickness problem with custom output units...")
    problem = create_pipe_bends()

    print(f"\nProblem: {problem.name}")
    print(f"Description: {problem.description}")
    print(f"Number of equations: {len(problem.equations)}")
    print(f"Known variables: {len(problem.get_known_variables())}")
    print(f"Unknown variables: {len(problem.get_unknown_variables())}")

    # Show the output unit specifications
    print("\nOutput unit specifications:")
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
        markdown_path = output_dir / "composed_problem_report.md"
        generate_report(problem, markdown_path, format="markdown")
        print(f"[SUCCESS] Markdown report saved to: {markdown_path}")

        # Generate LaTeX report
        print("\nGenerating LaTeX report...")
        latex_path = output_dir / "composed_problem_report.tex"
        generate_report(problem, latex_path, format="latex")
        print(f"[SUCCESS] LaTeX report saved to: {latex_path}")

        # Try to generate PDF report
        print("\nGenerating PDF report...")
        try:
            pdf_path = output_dir / "composed_problem_report.pdf"
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

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demonstrate_report_gen()
