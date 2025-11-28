"""
Shared problem definitions for parallelogram law tests.

This module provides problem class definitions that can be reused across
different test modules (e.g., solver tests, report generation tests).

Each problem class defines:
- name: Human-readable problem name
- Vector definitions using the unified parallelogram_law API
- expected: Expected solution values (from textbook/oracle)
- report: Expected content for report generation tests (optional)
- generate_debug_reports: If True, generates MD/PDF reports for this problem
"""

from pathlib import Path

from qnty.problems.statics import parallelogram_law as pl

# Output directory for debug reports
DEBUG_REPORT_DIR = Path(__file__).parent / "report_debug"


def generate_debug_reports_for_problem(problem_class) -> None:
    """Generate debug reports (MD and PDF) for a single problem class.

    Only generates if the problem has generate_debug_reports = True.

    Args:
        problem_class: A problem fixture class with name, vectors, etc.
    """
    if not getattr(problem_class, 'generate_debug_reports', False):
        return

    # Create output directory if needed
    DEBUG_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a safe filename from problem name
    safe_name = problem_class.name.lower().replace(" ", "_").replace("-", "_")
    safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")

    # Solve the problem
    result = pl.solve_class(problem_class, output_unit="N")

    if not result.success:
        print(f"WARNING: {problem_class.name} failed to solve: {result.error}")
        return

    # Generate markdown report
    md_path = DEBUG_REPORT_DIR / f"{safe_name}.md"
    result.generate_report(md_path, format="markdown")
    print(f"Generated: {md_path}")

    # Generate PDF report
    pdf_path = DEBUG_REPORT_DIR / f"{safe_name}.pdf"
    try:
        result.generate_report(pdf_path, format="pdf")
        print(f"Generated: {pdf_path}")
    except Exception as e:
        print(f"WARNING: PDF generation failed for {problem_class.name}: {e}")

# region // Parallelogram Law Problems

class Chapter2Problem1:
    name = "Problem 2-1"

    F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        F_R = pl.create_vector_polar(magnitude=497.014, unit="N", angle=155.192, wrt="+x")

    class report:
        """Expected content for report generation tests."""

        class known_variables:
            """Expected known variables table data."""
            F_1 = {
                "symbol": "F_1", "unit": "N",
                "x": 225.0, "y": 389.7, "mag": 450, "angle": 60, "wrt": "+x"
            }
            F_2 = {
                "symbol": "F_2", "unit": "N",
                "x": -676.1, "y": -181.2, "mag": 700, "angle": 15, "wrt": "-x"
            }

        class unknown_variables:
            """Expected unknown variables table data."""
            F_R = {
                "symbol": "F_R", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": "?", "reference": "+x",
            }

        class equations:
            """Expected equations used in the solution."""
            eq_1 = "|F_R|² = |F_1|² + |F_2|² + 2·|F_1|·|F_2|·cos(∠(F_1,F_2))"
            eq_2 = "sin(∠(F_1,F_R))/|F_2| = sin(∠(F_1,F_2))/|F_R|"
            count = 2

        class steps:
            """Expected solution steps."""
            step_1 = {
                "target": "∠(F_1,F_2)",
                "final_line": "= 45°",
            }
            step_2 = {
                "target": "|F_R| using Eq 1",
                "final_line": "= 497.0 N",
            }
            step_3 = {
                "target": "∠(F_1,F_R) using Eq 2",
                "final_line": "= 95.2°",
            }
            step_4 = {
                "target": "∠(x,F_R) with respect to +x",
                "final_line": "= 155.2°",
            }
            count = 4

        class results:
            """Expected final results in the Summary of Results table."""
            F_R = {
                "symbol": "F_R",
                "unit": "N",
                "x": -451.1,
                "y": 208.5,
                "magnitude": 497.0,
                "angle": 155.2,
                "reference": "+x",
            }

class Chapter2Problem2:
    name = "Problem 2-2"

    F_1 = pl.create_vector_polar(magnitude=..., unit="N", angle=..., wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
    F_R = pl.create_vector_resultant_polar(
        F_1, F_2,
        magnitude=500, unit="N", angle=0, wrt="+y"
    )

    class expected:
        F_1 = pl.create_vector_polar(magnitude=960, unit="N", angle=45.2, wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        F_R = pl.create_vector_polar(magnitude=500, unit="N", angle=0, wrt="+y")

    class report:
        """Expected content for report generation tests."""

        class known_variables:
            """Expected known variables table data."""
            F_2 = {
                "symbol": "F_2", "unit": "N",
                "x": -676.1, "y": -181.2, "mag": 700, "angle": 15, "wrt": "-x"
            }
            F_R = {
                "symbol": "F_R", "unit": "N",
                "x": 0.0, "y": 500.0, "mag": 500, "angle": 0, "wrt": "+y"
            }

        class unknown_variables:
            """Expected unknown variables table data."""
            F_1 = {
                "symbol": "F_1", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": "?", "reference": "+x",
            }

        class equations:
            """Expected equations used in the solution."""
            eq_1 = "|F_1|² = |F_2|² + |F_R|² - 2·|F_2|·|F_R|·cos(∠(F_2,F_R))"
            eq_2 = "sin(∠(F_R,F_1))/|F_2| = sin(∠(F_2,F_R))/|F_1|"
            count = 2

        class steps:
            """Expected solution steps."""
            step_1 = {
                "target": "∠(F_2,F_R)",
                "final_line": "= 105°",
            }
            step_2 = {
                "target": "|F_1| using Eq 1",
                "final_line": "= 959.8 N",
            }
            step_3 = {
                "target": "∠(F_R,F_1) using Eq 2",
                "final_line": "= 44.8°",
            }
            step_4 = {
                "target": "∠(x,F_1) with respect to +x",
                "final_line": "= 45.2°",
            }
            count = 4

        class results:
            """Expected final results in the Summary of Results table."""
            F_1 = {
                "symbol": "F_1",
                "unit": "N",
                "x": 676.1,
                "y": 681.2,
                "magnitude": 959.8,
                "angle": 45.2,
                "reference": "+x",
            }

# There are 139 problems in Chapter 2
# TODO: Fix report generation
class Chapter2Problem3:
    name = "Problem 2-3"
    generate_debug_reports = True  # Set to True to generate MD/PDF for debugging

    F_1 = pl.create_vector_polar(magnitude=250, unit="N", angle=-30, wrt="+y")
    F_2 = pl.create_vector_polar(magnitude=375, unit="N", angle=-45, wrt="+x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=250, unit="N", angle=-30, wrt="+y")
        F_2 = pl.create_vector_polar(magnitude=375, unit="N", angle=-45, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=393.2, unit="N", angle=352.9, wrt="+x")

class Chapter2Problem4:
    pass

class Chapter2Problem5:
    pass

class Chapter2Problem6:
    pass

class Chapter2Problem7:
    pass

class Chapter2Problem8:
    pass

class Chapter2Problem9:
    pass

class Chapter2Problem10:
    pass

class Chapter2Problem11:
    pass

class Chapter2Problem12:
    pass

class Chapter2Problem13:
    pass

class Chapter2Problem14:
    pass

class Chapter2Problem15:
    pass

class Chapter2Problem16:
    pass

class Chapter2Problem17:
    pass

class Chapter2Problem18:
    pass

class Chapter2Problem19:
    pass

class Chapter2Problem20:
    pass

class Chapter2Problem21:
    pass

class Chapter2Problem22:
    pass

class Chapter2Problem23:
    pass

class Chapter2Problem24:
    pass

class Chapter2Problem25:
    pass

class Chapter2Problem26:
    pass

class Chapter2Problem27:
    pass

class Chapter2Problem28:
    pass

class Chapter2Problem29:
    pass

class Chapter2Problem30:
    pass

class Chapter2Problem31:
    pass

class Chapter2Problem32:
    pass

class Chapter2Problem33:
    pass

class Chapter2Problem34:
    pass

class Chapter2Problem35:
    pass

class Chapter2Problem36:
    pass

class Chapter2Problem37:
    pass

class Chapter2Problem38:
    pass

class Chapter2Problem39:
    pass

class Chapter2Problem40:
    pass

class Chapter2Problem41:
    pass

class Chapter2Problem42:
    pass

class Chapter2Problem43:
    pass

class Chapter2Problem44:
    pass

class Chapter2Problem45:
    pass

class Chapter2Problem46:
    pass

class Chapter2Problem47:
    pass

class Chapter2Problem48:
    pass

class Chapter2Problem49:
    pass

class Chapter2Problem50:
    pass









# =============================================================================
# Problem 2-1 Mixed Units (Variant)
# =============================================================================


class Chapter2Problem1MixedUnits:
    name = "Problem 2-1 (Mixed Units)"

    # Input vectors using unified API
    F_1 = pl.create_vector_polar(magnitude=101.164, unit="lbf", angle=60, wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=0.261799, angle_unit="radian", wrt="-x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    # Expected values (from textbook)
    class expected:
        F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=1.0472, angle_unit="radian", wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        F_R = pl.create_vector_polar(magnitude=111.733, unit="lbf", angle=155.192, wrt="+x")


# =============================================================================
# Problem 2-1 WRONG (for test validation)
# =============================================================================

class Chapter2Problem1_WRONG:
    """
    Copy of Problem 2-1 with INTENTIONALLY WRONG expected values.

    This class is used to verify that the tests actually detect incorrect values.
    Each section has deliberately wrong data that should cause the corresponding
    test to fail.
    """

    name = "Problem 2-1 WRONG (expect failures)"

    # Input vectors - same as correct problem
    F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    # WRONG expected values
    class expected:
        F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        # WRONG: magnitude should be 497.014, angle should be 155.192
        F_R = pl.create_vector_polar(magnitude=999.0, unit="N", angle=45.0, wrt="+x")

    class report:
        """WRONG expected content for report generation tests."""

        class known_variables:
            """WRONG known variables - wrong component values."""
            F_1 = {
                "symbol": "F_1", "unit": "N",
                # WRONG: x should be 225.0, y should be 389.7
                "x": 999.0, "y": 999.0, "mag": 450, "angle": 60, "wrt": "+x"
            }
            F_2 = {
                "symbol": "F_2", "unit": "N",
                "x": -676.1, "y": -181.2, "mag": 700, "angle": 15, "wrt": "-x"
            }

        class unknown_variables:
            """WRONG unknown variables - wrong reference."""
            F_R = {
                "symbol": "F_R", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": "?",
                # WRONG: reference should be "+x"
                "reference": "-y",
            }

        class equations:
            """WRONG equations - wrong equation strings."""
            # WRONG: should be "|F_R|² = |F_1|² + |F_2|² + 2·|F_1|·|F_2|·cos(∠(F_1,F_2))"
            eq_1 = "WRONG EQUATION ONE"
            # WRONG: should be "sin(∠(F_1,F_R))/|F_2| = sin(∠(F_1,F_2))/|F_R|"
            eq_2 = "WRONG EQUATION TWO"
            count = 2

        class steps:
            """WRONG steps - wrong targets and final lines."""
            step_1 = {
                # WRONG: target should be "∠(F_1,F_2)"
                "target": "WRONG TARGET",
                # WRONG: final_line should be "= 45°"
                "final_line": "= 999°",
            }
            step_2 = {
                "target": "|F_R| using Eq 1",
                # WRONG: final_line should be "= 497.0 N"
                "final_line": "= 999.0 N",
            }
            step_3 = {
                "target": "∠(F_1,F_R) using Eq 2",
                "final_line": "= 95.2°",
            }
            step_4 = {
                "target": "θ_F_R with respect to +x",
                "final_line": "= 155.2°",
            }
            count = 4

        class results:
            """WRONG results - wrong values."""
            F_R = {
                "symbol": "F_R",
                "unit": "N",
                # WRONG: x should be -451.1
                "x": 999.0,
                # WRONG: y should be 208.5
                "y": 999.0,
                # WRONG: magnitude should be 497.0
                "magnitude": 999.0,
                # WRONG: angle should be 155.2
                "angle": 999.0,
                "reference": "+x",
            }


# =============================================================================
# Problem lists for parameterized tests
# =============================================================================

# All problems for iteration
PARALLELOGRAM_LAW_PROBLEMS = [
    Chapter2Problem1,
    Chapter2Problem1MixedUnits,
    Chapter2Problem2,
    Chapter2Problem3,
]

PROBLEMS_EXPECT_FAIL = [Chapter2Problem1_WRONG]

# All problem classes (for debug report generation)
ALL_PROBLEM_CLASSES = [
    Chapter2Problem1,
    Chapter2Problem1MixedUnits,
    Chapter2Problem2,
    Chapter2Problem3,
]


def generate_all_debug_reports() -> None:
    """Generate debug reports for all problems that have generate_debug_reports = True."""
    for problem_class in ALL_PROBLEM_CLASSES:
        generate_debug_reports_for_problem(problem_class)


# =============================================================================
# Run as script to generate debug reports
# =============================================================================

if __name__ == "__main__":
    print(f"Generating debug reports to: {DEBUG_REPORT_DIR}")
    generate_all_debug_reports()
    print("Done!")
