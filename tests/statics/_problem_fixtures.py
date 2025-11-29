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
                "final_line": "= 497.0\\ \\text{N}",
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

class Chapter2Problem3:
    name = "Problem 2-3"
    F_1 = pl.create_vector_polar(magnitude=250, unit="N", angle=-30, wrt="+y")
    F_2 = pl.create_vector_polar(magnitude=375, unit="N", angle=-45, wrt="+x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=250, unit="N", angle=-30, wrt="+y")
        F_2 = pl.create_vector_polar(magnitude=375, unit="N", angle=-45, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=393.2, unit="N", angle=352.9, wrt="+x")

    class report:
        class known_variables:
            """Expected known variables table data."""
            F_1 = {
                "symbol": "F_1", "unit": "N",
                "x": 125.0, "y": 216.5, "mag": 250, "angle": -30, "wrt": "+y"
            }
            F_2 = {
                "symbol": "F_2", "unit": "N",
                "x": 265.2, "y": -265.2, "mag": 375, "angle": -45, "wrt": "+x"
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
            eq_2 = "sin(∠(F_2,F_R))/|F_1| = sin(∠(F_1,F_2))/|F_R|"
            count = 2

        class steps:
            """Expected solution steps."""
            step_1 = {
                "target": "∠(F_1,F_2)",
                "final_line": "= 75°",
            }
            step_2 = {
                "target": "|F_R| using Eq 1",
                "final_line": "= 393.2\\ \\text{N}",
            }
            step_3 = {
                "target": "∠(F_2,F_R) using Eq 2",
                "final_line": "= 37.9°",
            }
            step_4 = {
                "target": "∠(x,F_R) with respect to +x",
                "final_line": "= 352.9°",
            }
            count = 4

        class results:
            """Expected final results in the Summary of Results table."""
            F_R = {
                "symbol": "F_R",
                "unit": "N",
                "x": 390.2,
                "y": -48.7,
                "magnitude": 393.2,
                "angle": 352.9,
                "reference": "+x",
            }

class Chapter2Problem4:
    name = "Problem 2-4"
    F_AB = pl.create_vector_polar(magnitude=..., unit="N", angle=-45, wrt="-y")
    F_AC = pl.create_vector_polar(magnitude=..., unit="N", angle=-30, wrt="+x")
    F_R = pl.create_vector_resultant_polar(
        F_AB, F_AC,
        magnitude=500, unit="N", angle=0, wrt="-y"
    )

    class expected:
        F_AB = pl.create_vector_polar(magnitude=448, unit="N", angle=-45, wrt="-y")
        F_AC = pl.create_vector_polar(magnitude=366, unit="N", angle=-30, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=500, unit="N", angle=0, wrt="-y")

    class report:
        """Expected content for report generation tests."""

        class known_variables:
            """Expected known variables table data."""
            F_R = {
                "symbol": "F_R", "unit": "N",
                "x": 0.0, "y": -500.0, "mag": 500, "angle": 0, "wrt": "-y"
            }

        class unknown_variables:
            """Expected unknown variables table data."""
            F_AB = {
                "symbol": "F_AB", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": -45, "reference": "-y",
            }
            F_AC = {
                "symbol": "F_AC", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": -30, "reference": "+x",
            }

        class equations:
            """Expected equations used in the solution."""
            eq_1 = "|F_{AB}|/sin(∠(F_{AC},F_{R})) = |F_{R}|/sin(∠(F_{AB},F_{AC}))"
            eq_2 = "|F_{AC}|/sin(∠(F_{AB},F_{R})) = |F_{R}|/sin(∠(F_{AB},F_{AC}))"
            count = 2

        class results:
            """Expected final results in the Summary of Results table."""
            F_AB = {
                "symbol": "F_AB",
                "unit": "N",
                "x": -316.2,
                "y": -316.2,
                "magnitude": 448.0,
                "angle": -45,
                "reference": "-y",
            }
            F_AC = {
                "symbol": "F_AC",
                "unit": "N",
                "x": 317.0,
                "y": -183.0,
                "magnitude": 366.0,
                "angle": -30,
                "reference": "+x",
            }

        # Additional report sections (steps, results) can be added as needed

class Chapter2Problem5:
    name = "Problem 2-5"
    F_AB = pl.create_vector_polar(magnitude=..., unit="lbf", angle=225, wrt="+x")
    F_AC = pl.create_vector_polar(magnitude=..., unit="lbf", angle=330, wrt="+x")
    F_R = pl.create_vector_resultant_polar(
        F_AB, F_AC,
        magnitude=350, unit="lbf", angle=270, wrt="+x"
    )

    class expected:
        F_AB = pl.create_vector_polar(magnitude=314, unit="lbf", angle=225, wrt="+x")
        F_AC = pl.create_vector_polar(magnitude=256, unit="lbf", angle=330, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=350, unit="lbf", angle=270, wrt="+x")

class Chapter2Problem6:
    name = "Problem 2-6"
    coordinate_system = pl.create_coord_angle_between(
        "u", "v", angle_between=75
    )
    F_1 = pl.create_vector_polar(magnitude=4000, unit="N", angle=-30, wrt="+v")
    F_2 = pl.create_vector_polar(magnitude=6000, unit="N", angle=-30, wrt="+u")
    F_R = pl.create_vector_resultant(F_1, F_2, angle_dir="cw")

    class expected:
        F_1 = pl.create_vector_polar(magnitude=4000, unit="N", angle=-30, wrt="+v")
        F_2 = pl.create_vector_polar(magnitude=6000, unit="N", angle=-30, wrt="+u")
        F_R = pl.create_vector_polar(magnitude=8026, unit="N", angle=-1.22, wrt="+u")

class Chapter2Problem7:
    name = "Problem 2-7"
    generate_debug_reports = True
    coordinate_system = pl.create_coord_angle_between(
        "u", "v", angle_between=75
    )
    F_1u = pl.create_vector_polar(magnitude=..., unit="N", angle=0, wrt="+u")
    F_1v = pl.create_vector_polar(magnitude=..., unit="N", angle=0, wrt="+v")
    F_1 = pl.create_vector_resultant_polar(
        F_1u, F_1v,
        magnitude=4000, unit="N", angle=-30, wrt="+v"
    )

    class expected:
        F_1u = pl.create_vector_polar(magnitude=2071, unit="N", angle=0, wrt="+u")
        F_1v = pl.create_vector_polar(magnitude=2928, unit="N", angle=0, wrt="+v")
        F_1 = pl.create_vector_polar(magnitude=4000, unit="N", angle=-30, wrt="+v")

class Chapter2Problem8:
    name = "Problem 2-8"
    generate_debug_reports = True
    coordinate_system = pl.create_coord_angle_between(
        "u", "v", angle_between=75
    )
    F_2u = pl.create_vector_polar(magnitude=..., unit="N", angle=0, wrt="+u")
    F_2v = pl.create_vector_polar(magnitude=..., unit="N", angle=0, wrt="+v")
    F_2 = pl.create_vector_resultant_polar(
        F_2u, F_2v,
        magnitude=6000, unit="N", angle=-30, wrt="+u"
    )

    class expected:
        F_2u = pl.create_vector_polar(magnitude=6000, unit="N", angle=0, wrt="+u")
        F_2v = pl.create_vector_polar(magnitude=-3106, unit="N", angle=0, wrt="+v")
        F_2 = pl.create_vector_polar(magnitude=6000, unit="N", angle=-30, wrt="+u")

class Chapter2Problem9:
    """
    If the resultant force acting on the support is to be 1200 lb, directed horizontally to the right,
    determine the force F in rope A and the corresponding angle theta.
    """
    name = "Problem 2-9"

    F_A = pl.create_vector_polar(magnitude=..., unit="lbf", angle=..., wrt="+x")
    F_B = pl.create_vector_polar(magnitude=900, unit="lbf", angle=330, wrt="+x")
    F_R = pl.create_vector_resultant_polar(F_A, F_B, magnitude=1200, unit="lbf", angle=0, wrt="+x")

    class expected:
        F_A = pl.create_vector_polar(magnitude=615.94, unit="lbf", angle=46.936, wrt="+x")
        F_B = pl.create_vector_polar(magnitude=900, unit="lbf", angle=330, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=1200, unit="lbf", angle=0, wrt="+x")

class Chapter2Problem10:
    """
    Determine the magnitude of the resultant force and its direction,
    measured counterclockwise from the positive x axis.
    """
    name = "Problem 2-10"

    F_1 = pl.create_vector_polar(magnitude=800, unit="lbf", angle=-40, wrt="+y")
    F_2 = pl.create_vector_polar(magnitude=500, unit="lbf", angle=-35, wrt="+x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=800, unit="lbf", angle=-40, wrt="+y")
        F_2 = pl.create_vector_polar(magnitude=500, unit="lbf", angle=-35, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=979.655, unit="lbf", angle=19.440, wrt="+x")

class Chapter2Problem11:
    """
    The plate is subjected to the two forces at A and B as shown. If theta = 60°,
    determine the magnitude of the resultant of these two forces and its direction
    measured clockwise from the horizontal.
    """
    name = "Problem 2-11"

    F_A = pl.create_vector_polar(magnitude=8000, unit="N", angle=-60, wrt="+y")
    F_B = pl.create_vector_polar(magnitude=6000, unit="N", angle=40, wrt="-y")
    F_R = pl.create_vector_resultant(F_A, F_B)

    class expected:
        F_A = pl.create_vector_polar(magnitude=8000, unit="N", angle=-60, wrt="+y")
        F_B = pl.create_vector_polar(magnitude=6000, unit="N", angle=40, wrt="-y")
        F_R = pl.create_vector_polar(magnitude=10800, unit="N", angle=-3.16, wrt="+x")

class Chapter2Problem12:
    """
    Determine the angle of theta for connecting member A to the plate so that the
    resultant force of F_A and F_B is directed horizontally to the right. Also, what is
    the magnitude of the resultant force?

    NOTE: This problem has a resultant with unknown magnitude but known angle (0° wrt +x).
    The current API may need extension to support this case. Skipped for now.
    """
    pass

    # TODO: Implement when API supports unknown magnitude with known angle for resultant
    # F_A = pl.create_vector_polar(magnitude=8000, unit="N", angle=..., wrt="+y")
    # F_B = pl.create_vector_polar(magnitude=6000, unit="N", angle=40, wrt="-y")
    # F_R = pl.create_vector_resultant_polar(F_A, F_B, magnitude=..., unit="N", angle=0, wrt="+x")
    #
    # class expected:
    #     F_A = pl.create_vector_polar(magnitude=8000, unit="N", angle=-54.9, wrt="+y")
    #     F_B = pl.create_vector_polar(magnitude=6000, unit="N", angle=40, wrt="-y")
    #     F_R = pl.create_vector_polar(magnitude=10400, unit="N", angle=0, wrt="+x")

class Chapter2Problem13:
    """
    NOTE: Problems 13-14 use non-orthogonal coordinate systems (40° between axes).
    These require CoordinateSystem support which is not yet migrated.
    """
    pass

class Chapter2Problem14:
    pass

class Chapter2Problem15:
    """
    Force F acts on the frame such that its component acting along member is 650 lb,
    directed from towards, and the component acting along member is 500 lb, directed
    from towards. Determine the magnitude of F and its direction u. Set f = 60°.
    """
    name = "Problem 2-15"

    F_AB = pl.create_vector_polar(magnitude=650, unit="lbf", angle=60, wrt="-x")
    F_BC = pl.create_vector_polar(magnitude=500, unit="lbf", angle=-45, wrt="+x")
    F_R = pl.create_vector_resultant(F_AB, F_BC)

    class expected:
        F_AB = pl.create_vector_polar(magnitude=650, unit="lbf", angle=60, wrt="-x")
        F_BC = pl.create_vector_polar(magnitude=500, unit="lbf", angle=-45, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=916.91, unit="lbf", angle=91.8, wrt="-x")

class Chapter2Problem16:
    """
    NOTE: Uses force-relative reference (wrt="+F_R"). Skipped for now.
    """
    pass

class Chapter2Problem17:
    """
    Determine the magnitude and direction of the resultant of the three forces by first
    finding the resultant F' = F1 + F2 and then forming FR = F' + F3.
    """
    name = "Problem 2-17"

    F_1 = pl.create_vector_polar(magnitude=30, unit="N", angle=-36.87, wrt="-x")
    F_2 = pl.create_vector_polar(magnitude=20, unit="N", angle=-20, wrt="-y")
    F_3 = pl.create_vector_polar(magnitude=50, unit="N", angle=0, wrt="+x")
    F_R = pl.create_vector_resultant(F_1, F_2, F_3)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=30, unit="N", angle=-36.87, wrt="-x")
        F_2 = pl.create_vector_polar(magnitude=20, unit="N", angle=-20, wrt="-y")
        F_3 = pl.create_vector_polar(magnitude=50, unit="N", angle=0, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=19.2, unit="N", angle=-2.37, wrt="+x")

class Chapter2Problem18:
    """
    Determine the magnitude and direction of the resultant of the three forces by first
    finding the resultant F' = F2 + F3 and then forming FR = F' + F1.
    (Same result as 2-17, just different order of operations)
    """
    name = "Problem 2-18"

    F_1 = pl.create_vector_polar(magnitude=30, unit="N", angle=-36.87, wrt="-x")
    F_2 = pl.create_vector_polar(magnitude=20, unit="N", angle=-20, wrt="-y")
    F_3 = pl.create_vector_polar(magnitude=50, unit="N", angle=0, wrt="+x")
    F_R = pl.create_vector_resultant(F_1, F_2, F_3)

    class expected:
        F_1 = pl.create_vector_polar(magnitude=30, unit="N", angle=-36.87, wrt="-x")
        F_2 = pl.create_vector_polar(magnitude=20, unit="N", angle=-20, wrt="-y")
        F_3 = pl.create_vector_polar(magnitude=50, unit="N", angle=0, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=19.2, unit="N", angle=-2.37, wrt="+x")

class Chapter2Problem19:
    """
    NOTE: Uses force-relative reference (wrt="+F_AB"). Skipped for now.
    """
    pass

class Chapter2Problem20:
    """
    NOTE: Uses force-relative reference (wrt="-F_AB"). Skipped for now.
    """
    pass

class Chapter2Problem21:
    """
    NOTE: Uses force-relative reference (wrt="+F_2"). Skipped for now.
    """
    pass

class Chapter2Problem22:
    """
    NOTE: Uses force-relative reference (wrt="+F_2"). Skipped for now.
    """
    pass

class Chapter2Problem23:
    """
    NOTE: Complex angle relationships between forces (angle between F_1 and F_2).
    May need special handling. Skipped for now.
    """
    pass

class Chapter2Problem24:
    """
    NOTE: Problem 2-24 is symbolic according to original test file.
    """
    pass

class Chapter2Problem25:
    """
    If F1 = 30 lb and F2 = 40 lb, determine the angles u and f so that the resultant
    force is directed along the positive x axis and has a magnitude of FR = 60 lb.
    """
    name = "Problem 2-25"

    F_1 = pl.create_vector_polar(magnitude=30, unit="lbf", angle=..., wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=40, unit="lbf", angle=..., wrt="+x")
    F_R = pl.create_vector_resultant_polar(F_1, F_2, magnitude=60, unit="lbf", angle=0, wrt="+x")

    class expected:
        F_1 = pl.create_vector_polar(magnitude=30, unit="lbf", angle=36.3, wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=40, unit="lbf", angle=-26.4, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=60, unit="lbf", angle=0, wrt="+x")

class Chapter2Problem26:
    """
    Determine the magnitude and direction u of FA so that the resultant force is
    directed along the positive x axis and has a magnitude of 1250 N.
    """
    name = "Problem 2-26"

    F_A = pl.create_vector_polar(magnitude=..., unit="N", angle=..., wrt="+x")
    F_B = pl.create_vector_polar(magnitude=800, unit="N", angle=-30, wrt="+x")
    F_R = pl.create_vector_resultant_polar(F_A, F_B, magnitude=1250, unit="N", angle=0, wrt="+x")

    class expected:
        F_A = pl.create_vector_polar(magnitude=686, unit="N", angle=-54.3, wrt="+y")
        F_B = pl.create_vector_polar(magnitude=800, unit="N", angle=-30, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=1250, unit="N", angle=0, wrt="+x")

class Chapter2Problem27:
    """
    Determine the magnitude and direction, measured counterclockwise from the positive
    x axis, of the resultant force acting on the ring at O, if FA = 750 N and u = 45°.
    """
    name = "Problem 2-27"

    F_A = pl.create_vector_polar(magnitude=750, unit="N", angle=-45, wrt="+y")
    F_B = pl.create_vector_polar(magnitude=800, unit="N", angle=-30, wrt="+x")
    F_R = pl.create_vector_resultant(F_A, F_B)

    class expected:
        F_A = pl.create_vector_polar(magnitude=750, unit="N", angle=-45, wrt="+y")
        F_B = pl.create_vector_polar(magnitude=800, unit="N", angle=-30, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=1230, unit="N", angle=6.08, wrt="+x")

class Chapter2Problem28:
    """
    NOTE: Uses force-relative reference (wrt="+F_3"). Skipped for now.
    """
    pass

class Chapter2Problem29:
    """
    If the resultant force of the two tugboats is FR, directed along the positive x axis,
    determine the required magnitude of force FB and its direction u.
    """
    name = "Problem 2-29"

    F_A = pl.create_vector_polar(magnitude=2000, unit="N", angle=30, wrt="+x")
    F_B = pl.create_vector_polar(magnitude=..., unit="N", angle=..., wrt="+x")
    F_R = pl.create_vector_resultant_polar(F_A, F_B, magnitude=3000, unit="N", angle=0, wrt="+x")

    class expected:
        F_A = pl.create_vector_polar(magnitude=2000, unit="N", angle=30, wrt="+x")
        F_B = pl.create_vector_polar(magnitude=1615, unit="N", angle=-38.3, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=3000, unit="N", angle=0, wrt="+x")

class Chapter2Problem30:
    """
    If FA = 2000 N and FB = 3000 N at 45° below horizontal, determine the magnitude
    of the resultant force of the two tugboats and its direction measured clockwise
    from the positive x axis.
    """
    name = "Problem 2-30"

    F_A = pl.create_vector_polar(magnitude=2000, unit="N", angle=30, wrt="+x")
    F_B = pl.create_vector_polar(magnitude=3000, unit="N", angle=-45, wrt="+x")
    F_R = pl.create_vector_resultant(F_A, F_B)

    class expected:
        F_A = pl.create_vector_polar(magnitude=2000, unit="N", angle=30, wrt="+x")
        F_B = pl.create_vector_polar(magnitude=3000, unit="N", angle=-45, wrt="+x")
        F_R = pl.create_vector_polar(magnitude=4013, unit="N", angle=-16.2, wrt="+x")

class Chapter2Problem31:
    """
    NOTE: Uses force-relative reference (wrt="+F_R"). Skipped for now.
    """
    pass

# endregion // Parallelogram Law Problems

# region // Rectangular Component Problems

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

# All problems for iteration (only includes fully migrated problems)
PARALLELOGRAM_LAW_PROBLEMS = [
    Chapter2Problem1,
    Chapter2Problem1MixedUnits,
    Chapter2Problem2,
    Chapter2Problem3,
    Chapter2Problem4,
    Chapter2Problem5,
    Chapter2Problem6,
    Chapter2Problem7,
    Chapter2Problem8,

    Chapter2Problem9,
    Chapter2Problem10,
    Chapter2Problem11,
    # Problem 12: Unknown resultant magnitude with known angle - not yet supported
    # Problems 13-14: Non-orthogonal coordinate systems (40° between axes) - not yet supported
    Chapter2Problem15,
    # Problem 16: Force-relative reference (wrt="+F_R") - not yet supported
    Chapter2Problem17,
    Chapter2Problem18,
    # Problems 19-22: Force-relative references - not yet supported
    # Problem 23: Complex angle relationships - not yet supported
    # Problem 24: Symbolic problem
    # Chapter2Problem25,
    Chapter2Problem26,
    Chapter2Problem27,
    # Problem 28: Force-relative reference - not yet supported
    Chapter2Problem29,
    Chapter2Problem30,
    # Problem 31: Force-relative reference - not yet supported
]

PROBLEMS_EXPECT_FAIL = [
    Chapter2Problem1_WRONG
]

# All problem classes (for debug report generation)
ALL_PROBLEM_CLASSES = [
    Chapter2Problem1,
    Chapter2Problem1MixedUnits,
    Chapter2Problem2,
    Chapter2Problem3,
    Chapter2Problem4,
    Chapter2Problem5,
    Chapter2Problem6,
    Chapter2Problem7,
    Chapter2Problem8,

    Chapter2Problem9,
    Chapter2Problem10,
    Chapter2Problem11,
    Chapter2Problem15,
    Chapter2Problem17,
    Chapter2Problem18,
    # Chapter2Problem25,
    Chapter2Problem26,
    Chapter2Problem27,
    Chapter2Problem29,
    Chapter2Problem30,
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
