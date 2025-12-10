"""
Shared problem definitions for parallelogram law tests.

This module provides problem class definitions that can be reused across
different test modules (e.g., solver tests, report generation tests).

Each problem class defines:
- name: Human-readable problem name
- Vector definitions using the parallelogram_solver API
- expected: Expected solution values (from textbook/oracle)
- report: Expected content for report generation tests (optional)
- generate_debug_reports: If True, generates MD/PDF reports for this problem

NOTE: This file is being migrated to use the new parallelogram_solver.py.
Currently only Problem 2-1 is fully migrated. Other problems are commented out.
"""

import re
from pathlib import Path

from qnty.coordinates.oblique import Oblique

# Import vector creation functions from new vectors2 module
from qnty.linalg.vectors2 import create_resultant_polar, create_vector_from_ratio, create_vector_resultant, create_vectors_polar

# Import from the new parallelogram_solver module
from qnty.problems.statics.parallelogram_solver import (
    solve_class,
)

# Output directory for debug reports
DEBUG_REPORT_DIR = Path(__file__).parent / "report_debug"

# Output directory for golden files (used by snapshot tests)
GOLDEN_DIR = Path(__file__).parent / "golden"


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

    # Solve the problem using the new solver
    problem = solve_class(problem_class, output_unit="N")

    if not problem.is_solved:
        print(f"WARNING: {problem_class.name} failed to solve")
        return

    # Generate markdown report
    md_path = DEBUG_REPORT_DIR / f"{safe_name}.md"
    problem.generate_report(str(md_path), format="markdown")
    print(f"Generated: {md_path}")

    # Generate PDF report
    pdf_path = DEBUG_REPORT_DIR / f"{safe_name}.pdf"
    try:
        problem.generate_report(str(pdf_path), format="pdf")
        print(f"Generated: {pdf_path}")
    except Exception as e:
        print(f"WARNING: PDF generation failed for {problem_class.name}: {e}")

# region // Parallelogram Law Problems

class Chapter2Problem1:
    name = "Problem 2-1"
    generate_debug_reports = False
    F_1 = create_vectors_polar(450, "N", 60, wrt="+x")
    F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
    F_R = create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = create_vectors_polar(450, "N", 60, wrt="+x")
        F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
        F_R = create_vectors_polar(497.014, "N", 155.192, wrt="+x")

class Chapter2Problem2:
    name = "Problem 2-2"
    generate_debug_reports = False
    F_1 = create_vectors_polar(..., "N", ..., wrt="+x")
    F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
    F_R = create_resultant_polar(
        F_1, F_2,
        magnitude=500, unit="N", angle=0, wrt="+y"
    )

    class expected:
        F_1 = create_vectors_polar(960, "N", 45.2, wrt="+x")
        F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
        F_R = create_vectors_polar(500, "N", 0, wrt="+y")

class Chapter2Problem3:
    name = "Problem 2-3"
    generate_debug_reports = True
    F_1 = create_vectors_polar(250, "N", -30, wrt="+y")
    F_2 = create_vectors_polar(375, "N", -45, wrt="+x")
    F_R = create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = create_vectors_polar(250, "N", -30, wrt="+y")
        F_2 = create_vectors_polar(375, "N", -45, wrt="+x")
        F_R = create_vectors_polar(393.2, "N", 352.9, wrt="+x")

class Chapter2Problem4:
    name = "Problem 2-4"
    generate_debug_reports = True
    F_AB = create_vectors_polar(..., "N", -45, wrt="-y")
    F_AC = create_vectors_polar(..., "N", -30, wrt="+x")
    F_R = create_resultant_polar(
        F_AB, F_AC,
        magnitude=500, unit="N", angle=0, wrt="-y"
    )

    class expected:
        F_AB = create_vectors_polar(448, "N", 225, wrt="+x")
        F_AC = create_vectors_polar(366, "N", -30, wrt="+x")
        F_R = create_vectors_polar(500, "N", 0, wrt="-y")

class Chapter2Problem5:
    name = "Problem 2-5"
    generate_debug_reports = True
    F_AB = create_vectors_polar(..., "lbf", 225, wrt="+x")
    F_AC = create_vectors_polar(..., "lbf", 330, wrt="+x")
    F_R = create_resultant_polar(
        F_AB, F_AC,
        magnitude=350, unit="lbf", angle=270, wrt="+x"
    )

    class expected:
        F_AB = create_vectors_polar(314, "lbf", 225, wrt="+x")
        F_AC = create_vectors_polar(256, "lbf", 330, wrt="+x")
        F_R = create_vectors_polar(350, "lbf", 270, wrt="+x")

class Chapter2Problem6:
    name = "Problem 2-6"
    generate_debug_reports = True
    cs = Oblique.from_angle_between(
        "u", "v", 0, 75
    )
    F_1 = create_vectors_polar(4000, "N", -30, wrt="+v", coordinate_system=cs)
    F_2 = create_vectors_polar(6000, "N", -30, wrt="+u", coordinate_system=cs)
    F_R = create_vector_resultant(
        F_1, F_2, wrt="+u",
        angle_dir="cw", coordinate_system=cs
    )

    class expected:
        cs = Oblique.from_angle_between("u", "v", 0, 75)
        F_1 = create_vectors_polar(4000, "N", -30, wrt="+v", coordinate_system=cs)
        F_2 = create_vectors_polar(6000, "N", -30, wrt="+u", coordinate_system=cs)
        F_R = create_vectors_polar(8026.41, "N", -1.22, wrt="+u", coordinate_system=cs)

class Chapter2Problem7:
    name = "Problem 2-7"
    generate_debug_reports = True
    cs = Oblique.from_angle_between("u", "v", 0, 75)
    F_1u = create_vectors_polar(..., "N", 0, wrt="+u", coordinate_system=cs)
    F_1v = create_vectors_polar(..., "N", 0, wrt="+v", coordinate_system=cs)
    F_1 = create_resultant_polar(
        F_1u, F_1v,
        magnitude=4000, unit="N", angle=-30, wrt="+v", coordinate_system=cs
    )

    class expected:
        cs = Oblique.from_angle_between("u", "v", 0, 75)
        F_1u = create_vectors_polar(2071, "N", 0, wrt="+u", coordinate_system=cs)
        F_1v = create_vectors_polar(2928, "N", 0, wrt="+v", coordinate_system=cs)
        F_1 = create_vectors_polar(4000, "N", -30, wrt="+v", coordinate_system=cs)

class Chapter2Problem8:
    name = "Problem 2-8"
    generate_debug_reports = True
    cs = Oblique.from_angle_between("u", "v", 0, 75)
    F_2u = create_vectors_polar(..., "N", 0, wrt="+u", coordinate_system=cs)
    F_2v = create_vectors_polar(..., "N", 0, wrt="+v", coordinate_system=cs)
    F_2 = create_resultant_polar(
        F_2u, F_2v,
        magnitude=6000, unit="N", angle=-30, wrt="+u"
    )

    class expected:
        cs = Oblique.from_angle_between("u", "v", 0, 75)
        F_2u = create_vectors_polar(6000, "N", 0, wrt="+u", coordinate_system=cs)
        F_2v = create_vectors_polar(-3106, "N", 0, wrt="+v", coordinate_system=cs)
        F_2 = create_vectors_polar(6000, "N", -30, wrt="+u", coordinate_system=cs)

class Chapter2Problem9:
    name = "Problem 2-9"
    generate_debug_reports = True
    F_A = create_vectors_polar(..., "lbf", ..., wrt="+x")
    F_B = create_vectors_polar(900, "lbf", 60, wrt="-y")
    F_R = create_resultant_polar(
        F_A, F_B,
        magnitude=1200, unit="lbf", angle=0, wrt="+x"
    )

    class expected:
        F_A = create_vectors_polar(615.94, "lbf", 46.936, wrt="+x")
        F_B = create_vectors_polar(900, "lbf", 60, wrt="-y")
        F_R = create_vectors_polar(1200, "lbf", 0, wrt="+x")

class Chapter2Problem10:
    name = "Problem 2-10"
    generate_debug_reports = True
    F_1 = create_vectors_polar(800, "lbf", -40, wrt="+y")
    F_2 = create_vectors_polar(500, "lbf", -35, wrt="+x")
    F_R = create_vector_resultant(F_1, F_2)

    class expected:
        F_1 = create_vectors_polar(800, "lbf", -40, wrt="+y")
        F_2 = create_vectors_polar(500, "lbf", -35, wrt="+x")
        F_R = create_vectors_polar(979.655, "lbf", 19.440, wrt="+x")

class Chapter2Problem11:
    name = "Problem 2-11"
    generate_debug_reports = True
    F_A = create_vectors_polar(8000, "N", -60, wrt="+y")
    F_B = create_vectors_polar(6000, "N", 40, wrt="-y")
    F_R = create_vector_resultant(F_A, F_B, angle_dir="cw")

    class expected:
        F_A = create_vectors_polar(8000, "N", -60, wrt="+y")
        F_B = create_vectors_polar(6000, "N", 40, wrt="-y")
        F_R = create_vectors_polar(10800, "N", -3.16, wrt="+x")

class Chapter2Problem12:
    name = "Problem 2-12"
    generate_debug_reports = True
    F_A = create_vectors_polar(8000, "N", ..., wrt="+y")
    F_B = create_vectors_polar(6000, "N", 40, wrt="-y")
    F_R = create_resultant_polar(
        F_A, F_B,
        magnitude=..., unit="N", angle=0, wrt="+x"
    )

    class expected:
        F_A = create_vectors_polar(8000, "N", -54.9, wrt="+y")
        F_B = create_vectors_polar(6000, "N", 40, wrt="-y")
        F_R = create_vectors_polar(10400, "N", 0, wrt="+x")


class Chapter2Problem13:
    name = "Problem 2-13"
    generate_debug_reports = True
    cs = Oblique.from_angle_between("a", "b", 0, 40)
    F_a = create_vectors_polar(..., "lbf", 0, wrt="+a", coordinate_system=cs)
    F_b = create_vectors_polar(..., "lbf", 0, wrt="-b", coordinate_system=cs)
    F = create_resultant_polar(
        F_a, F_b,
        magnitude=20, unit="lbf", angle=80, wrt="-b", coordinate_system=cs
    )

    class expected:
        cs = Oblique.from_angle_between("a", "b", 0, 40)
        F_a = create_vectors_polar(30.6, "lbf", 0, wrt="+a", coordinate_system=cs)
        F_b = create_vectors_polar(26.9, "lbf", 0, wrt="-b", coordinate_system=cs)
        F = create_vectors_polar(20, "lbf", 80, wrt="-b", coordinate_system=cs)


class Chapter2Problem14:
    name = "Problem 2-14"
    generate_debug_reports = True
    cs = Oblique.from_angle_between("a", "b", 0, 40)
    F_a = create_vectors_polar(30, "lbf", 0, wrt="+a", coordinate_system=cs)
    F_b = create_vectors_polar(..., "lbf", 0, wrt="b", coordinate_system=cs)
    F = create_resultant_polar(
        F_a, F_b,
        magnitude=..., unit="lbf", angle=80, wrt="b", coordinate_system=cs
    )

    class expected:
        cs = Oblique.from_angle_between("a", "b", 0, 40)
        F_a = create_vectors_polar(30, "lbf", 0, wrt="+a", coordinate_system=cs)
        F_b = create_vectors_polar(-26.4, "lbf", 0, wrt="b", coordinate_system=cs)
        F = create_vectors_polar(-19.6, "lbf", 80, wrt="b", coordinate_system=cs)


class Chapter2Problem15:
    name = "Problem 2-15"
    generate_debug_reports = True
    F_BA = create_vectors_polar(650, "lbf", 60, wrt="-x")
    F_BC = create_vectors_polar(500, "lbf", -45, wrt="+x")
    F_R = create_vector_resultant(F_BA, F_BC, wrt=F_BA)

    class expected:
        F_BA = create_vectors_polar(650, "lbf", 60, wrt="-x")
        F_BC = create_vectors_polar(500, "lbf", -45, wrt="+x")
        F_R = create_vectors_polar(916.91, "lbf", 31.8, wrt=F_BA)


class Chapter2Problem16:
    name = "Problem 2-16"
    generate_debug_reports = True
    F_BA = create_vectors_polar(650, "lbf", ..., wrt="-x")
    F_BC = create_vectors_polar(..., "lbf", -45, wrt="+x")
    F_R = create_resultant_polar(
        F_BA, F_BC,
        magnitude=850, unit="lbf", angle=30, wrt=F_BA
    )

    class expected:
        F_BA = create_vectors_polar(650, "lbf", 33.5, wrt="-x")
        F_BC = create_vectors_polar(434, "lbf", -45, wrt="+x")
        F_R = create_vectors_polar(850, "lbf", 30, wrt=F_BA)

class Chapter2Problem17:
    name = "Problem 2-17"
    generate_debug_reports = True
    # F_1 = create_vectors_polar(30, "N", -36.87, wrt="-x")
    F_1 = create_vector_from_ratio(30, "N", -4, 3)
    F_2 = create_vectors_polar(20, "N", -20, wrt="-y")
    F_3 = create_vectors_polar(50, "N", 0, wrt="+x")
    F_R = create_vector_resultant(F_1, F_2, F_3, angle_dir="cw")

    class expected:
        F_1 = create_vectors_polar(30, "N", -36.87, wrt="-x")
        F_2 = create_vectors_polar(20, "N", -20, wrt="-y")
        F_3 = create_vectors_polar(50, "N", 0, wrt="+x")
        F_R = create_vectors_polar(19.2, "N", -2.37, wrt="+x")

class Chapter2Problem18:
    # Same as Problem 2-17 (Book solves in a different order than 2-17 but not doing that here)
    name = "Problem 2-18"
    generate_debug_reports = True
    F_1 = create_vectors_polar(30, "N", -36.87, wrt="-x")
    F_2 = create_vectors_polar(20, "N", -20, wrt="-y")
    F_3 = create_vectors_polar(50, "N", 0, wrt="+x")
    F_R = create_vector_resultant(F_1, F_2, F_3, angle_dir="cw")

    class expected:
        F_1 = create_vectors_polar(30, "N", -36.87, wrt="-x")
        F_2 = create_vectors_polar(20, "N", -20, wrt="-y")
        F_3 = create_vectors_polar(50, "N", 0, wrt="+x")
        F_R = create_vectors_polar(19.2, "N", -2.37, wrt="+x")

class Chapter2Problem19:
    name = "Problem 2-19"
    generate_debug_reports = True
    F_AB = create_vectors_polar(..., "lbf", ..., wrt="+x")
    F_AC = create_vectors_polar(500, "lbf", -40, wrt=F_AB)
    F_R = create_resultant_polar(
        F_AB, F_AC,
        magnitude=400, unit="lbf", angle=0, wrt="-x"
    )

    class expected:
        F_AB = create_vectors_polar(-621.15, "lbf", -53.46, wrt="+x")
        F_AC = create_vectors_polar(500, "lbf", -93.46, wrt="+x")
        F_R = create_vectors_polar(400, "lbf", 0, wrt="-x")

class Chapter2Problem20:
    name = "Problem 2-20"
    generate_debug_reports = True
    F_AB = create_vectors_polar(-600, "lbf", -30, wrt="+x")
    F_AC = create_vectors_polar(..., "lbf", ..., wrt=F_AB)
    F_R = create_resultant_polar(
        F_AB, F_AC,
        magnitude=400, unit="lbf", angle=0, wrt="-x"
    )

    class expected:
        F_AB = create_vectors_polar(-600, "lbf", -30, wrt="+x")
        F_AC = create_vectors_polar(322.97, "lbf", -68.3, wrt="+x")
        F_R = create_vectors_polar(400, "lbf", 0, wrt="-x")

class Chapter2Problem21:
    name = "Problem 2-21"
    generate_debug_reports = True
    F_1 = create_vectors_polar(400, "N", 90, wrt="F_2")
    F_2 = create_vectors_polar(200, "N", 150, wrt="-y")
    F_3 = create_vectors_polar(300, "N", 0, wrt="-y")
    F_R = create_vector_resultant(F_1, F_2, F_3)

    class expected:
        F_1 = create_vectors_polar(400, "N", 240, wrt="-y")
        F_2 = create_vectors_polar(200, "N", 150, wrt="-y")
        F_3 = create_vectors_polar(300, "N", 0, wrt="-y")
        F_R = create_vectors_polar(257.05, "N", 163.45, wrt="+x")

class Chapter2Problem22:
    name = "Problem 2-22"
    generate_debug_reports = True
    F_1 = create_vectors_polar(400, "N", 90, wrt="F_2")
    F_2 = create_vectors_polar(200, "N", 150, wrt="-y")
    F_3 = create_vectors_polar(300, "N", 0, wrt="-y")
    F_R = create_vector_resultant(F_1, F_2, F_3)

    class expected:
        F_1 = create_vectors_polar(400, "N", 90, wrt="F_2")
        F_2 = create_vectors_polar(200, "N", 150, wrt="-y")
        F_3 = create_vectors_polar(300, "N", 0, wrt="-y")
        F_R = create_vectors_polar(257.05, "N", 163.45, wrt="+x")

class Chapter2Problem23:
    name = "Problem 2-23"
    generate_debug_reports = True
    F_1 = create_vectors_polar(400, "N", ..., wrt="+x")
    F_2 = create_vectors_polar(600, "N", ..., wrt="+x")
    F_R = create_resultant_polar(
        F_1, F_2,
        magnitude=800, unit="N", angle=..., wrt="+x"
    )

    class expected:
        F_1 = create_vectors_polar(400, "N", 75.5, wrt="F_2")
        F_2 = create_vectors_polar(600, "N", -75.5, wrt="F_1")
        F_R = create_vectors_polar(800, "N", 0, wrt="+x")

class Chapter2Problem24:
    pass

class Chapter2Problem25:
    name = "Problem 2-25"
    generate_debug_reports = True
    F_1 = create_vectors_polar(30, "lbf", ..., wrt="+x")
    F_2 = create_vectors_polar(40, "lbf", ..., wrt="+x")
    F_R = create_resultant_polar(
        F_1, F_2,
        magnitude=60, unit="lbf", angle=0, wrt="+x"
    )

    class expected:
        F_1 = create_vectors_polar(30, "lbf", 36.3, wrt="+x")
        F_2 = create_vectors_polar(40, "lbf", -26.4, wrt="+x")
        F_R = create_vectors_polar(60, "lbf", 0, wrt="+x")

class Chapter2Problem26:
    name = "Problem 2-26"
    generate_debug_reports = True
    F_A = create_vectors_polar(..., "N", ..., wrt="+x")
    F_B = create_vectors_polar(800, "N", -30, wrt="+x")
    F_R = create_resultant_polar(
        F_A, F_B,
        magnitude=1250, unit="N", angle=0, wrt="+x"
    )

    class expected:
        F_A = create_vectors_polar(686, "N", -54.3, wrt="+y")
        F_B = create_vectors_polar(800, "N", -30, wrt="+x")
        F_R = create_vectors_polar(1250, "N", 0, wrt="+x")

class Chapter2Problem27:
    name = "Problem 2-27"
    generate_debug_reports = True
    F_A = create_vectors_polar(750, "N", -45, wrt="+y")
    F_B = create_vectors_polar(800, "N", -30, wrt="+x")
    F_R = create_vector_resultant(F_A, F_B)

    class expected:
        F_A = create_vectors_polar(750, "N", -45, wrt="+y")
        F_B = create_vectors_polar(800, "N", -30, wrt="+x")
        F_R = create_vectors_polar(1230, "N", 6.08, wrt="+x")

class Chapter2Problem28:
    name = "Problem 2-28"
    generate_debug_reports = True
    F_1 = create_vectors_polar(8000, "N", 0, wrt="-y")
    F_2 = create_vectors_polar(6000, "N", 0, wrt="+x")
    F_3 = create_vectors_polar(..., "N", 30, wrt="-y")
    F_R = create_resultant_polar(
        F_1, F_2, F_3,
        magnitude=..., unit="N", angle=90, wrt="F_3"
    )

    class expected:
        F_1 = create_vectors_polar(8000, "N", 0, wrt="-y")
        F_2 = create_vectors_polar(6000, "N", 0, wrt="+x")
        F_3 = create_vectors_polar(1196, "N", 30, wrt="-y")
        F_R = create_vectors_polar(9928, "N", 90, wrt="F_3")

class Chapter2Problem29:
    name = "Problem 2-29"
    generate_debug_reports = True
    F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
    F_B = create_vectors_polar(..., "N", ..., wrt="+x")
    F_R = create_resultant_polar(
        F_A, F_B,
        magnitude=3000, unit="N", angle=0, wrt="+x")

    class expected:
        F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
        F_B = create_vectors_polar(1615, "N", -38.3, wrt="+x")
        F_R = create_vectors_polar(3000, "N", 0, wrt="+x")

class Chapter2Problem30:
    name = "Problem 2-30"
    generate_debug_reports = True
    F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
    F_B = create_vectors_polar(3000, "N", -45, wrt="+x")
    F_R = create_vector_resultant(F_A, F_B)

    class expected:
        F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
        F_B = create_vectors_polar(3000, "N", -45, wrt="+x")
        F_R = create_vectors_polar(4013, "N", -16.2, wrt="+x")

class Chapter2Problem31:
    name = "Problem 2-31"
    generate_debug_reports = True
    F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
    F_B = create_vectors_polar(..., "N", -90, wrt="F_R")
    F_R = create_resultant_polar(
        F_A, F_B,
        magnitude=..., unit="N", angle=0, wrt="+x"
    )

    class expected:
        F_A = create_vectors_polar(2000, "N", 30, wrt="+x")
        F_B = create_vectors_polar(1000, "N", -90, wrt="+x")
        F_R = create_vectors_polar(1730, "N", 0, wrt="+x")

# endregion // Parallelogram Law Problems

# =============================================================================
# Problem 2-1 Mixed Units (Variant)
# =============================================================================

class Chapter2Problem1MixedUnits:
    name = "Problem 2-1 (Mixed Units)"

    # Input vectors using unified API
    F_1 = create_vectors_polar(101.164, "lbf", 60, wrt="+x")
    F_2 = create_vectors_polar(700, "N", 0.261799, "radian", wrt="-x")
    F_R = create_vector_resultant(F_1, F_2)

    # Expected values (from textbook)
    class expected:
        F_1 = create_vectors_polar(450, "N", 1.0472, "radian", wrt="+x")
        F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
        F_R = create_vectors_polar(111.733, "lbf", 155.192, wrt="+x")

# =============================================================================
# Problem 2-1 WRONG (for test validation)
# =============================================================================

class Chapter2Problem1_WRONG:
    name = "Problem 2-1 WRONG (expect failures)"

    # Input vectors - same as correct problem
    F_1 = create_vectors_polar(450, "N", 60, wrt="+x")
    F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
    F_R = create_vector_resultant(F_1, F_2)

    # WRONG expected values
    class expected:
        F_1 = create_vectors_polar(450, "N", 60, wrt="+x")
        F_2 = create_vectors_polar(700, "N", 15, wrt="-x")
        F_R = create_vectors_polar(999.0, "N", 45.0, wrt="+x")

# =============================================================================
# Problem lists for parameterized tests
# =============================================================================

PARALLELOGRAM_LAW_PROBLEMS = [
    Chapter2Problem1,
    # Chapter2Problem1MixedUnits,
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
    Chapter2Problem12,
    Chapter2Problem13,
    Chapter2Problem14,
    Chapter2Problem15,
    Chapter2Problem16,
    Chapter2Problem17,
    Chapter2Problem18,
    Chapter2Problem19,
    Chapter2Problem20,
    Chapter2Problem21,
    Chapter2Problem22,
    Chapter2Problem23,
    # # Problem 24: Symbolic problem
    Chapter2Problem25,
    Chapter2Problem26,
    Chapter2Problem27,
    Chapter2Problem28,
    Chapter2Problem29,
    Chapter2Problem30,
    Chapter2Problem31,
]

PROBLEMS_EXPECT_FAIL = [
    Chapter2Problem1_WRONG
]

# All problem classes (for debug report generation)
ALL_PROBLEM_CLASSES = [
    Chapter2Problem1,
    # Chapter2Problem1MixedUnits,
    Chapter2Problem2,
    # Chapter2Problem3,
    # Chapter2Problem4,
    # Chapter2Problem5,
    # Chapter2Problem6,
    # Chapter2Problem7,
    # Chapter2Problem8,
    # Chapter2Problem9,
    # Chapter2Problem10,
    # Chapter2Problem11,
    # Chapter2Problem12,
    # Chapter2Problem13,
    # Chapter2Problem14,
    # Chapter2Problem15,
    # Chapter2Problem16,
    # Chapter2Problem17,
    # Chapter2Problem18,
    # Chapter2Problem19,
    # Chapter2Problem20,
    # Chapter2Problem21,
    # Chapter2Problem22,
    # Chapter2Problem23,
    # # Chapter2Problem24,  # Symbolic problem - skipped
    # Chapter2Problem25,
    # Chapter2Problem26,
    # Chapter2Problem27,
    # Chapter2Problem29,
    # Chapter2Problem30,
    # Chapter2Problem31,
]

PROBLEMS_WITH_GOLDEN_FILES = [
    Chapter2Problem1,
    Chapter2Problem2,
    # Chapter2Problem3,
    # Chapter2Problem4,
    # Chapter2Problem5,
    # Chapter2Problem6,
    # Chapter2Problem7,
    # Chapter2Problem8,
    # Chapter2Problem9,
    # Chapter2Problem10,
    # Chapter2Problem11,
    # Chapter2Problem12,
    # Chapter2Problem13,
    # Chapter2Problem14,
    # Chapter2Problem15,
    # Chapter2Problem16,
    # Chapter2Problem17,
]


def generate_all_debug_reports() -> None:
    """Generate debug reports for all problems that have generate_debug_reports = True."""
    for problem_class in ALL_PROBLEM_CLASSES:
        generate_debug_reports_for_problem(problem_class)


# =============================================================================
# Golden file utilities (for snapshot tests)
# =============================================================================


def get_golden_base(problem_class) -> str:
    """
    Derive golden file base name from problem class name.

    Examples:
        "Problem 2-1" -> "problem_2_1_report"
        "Problem 2-3" -> "problem_2_3_report"
    """
    name = problem_class.name.lower().replace(" ", "_").replace("-", "_")
    return f"{name}_report"


def normalize_report(content: str) -> str:
    """
    Normalize a report by replacing dynamic content with placeholders.

    This allows comparison between generated reports (with actual dates)
    and golden files (with placeholders).

    Args:
        content: Raw report content

    Returns:
        Normalized content with dates replaced by placeholders
    """
    # Replace datetime format: "2025-11-28 10:32:10"
    content = re.sub(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        "{{GENERATED_DATETIME}}",
        content
    )

    # Replace date format: "November 28, 2025"
    content = re.sub(
        r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}",
        "{{GENERATED_DATE}}",
        content
    )

    return content


def _get_problem_unit(problem_class) -> str:
    """Get the output unit for a problem class from its vector definitions."""
    # Check F_R first, then F_AB, then default to N
    for attr in ["F_R", "F_AB", "F_AC"]:
        if hasattr(problem_class, attr):
            vec = getattr(problem_class, attr)
            if hasattr(vec, "_unit") and vec._unit:
                return vec._unit.symbol
    return "N"


def regenerate_golden_files() -> None:
    """
    Regenerate golden files for all problems in PROBLEMS_WITH_GOLDEN_FILES.

    Run this when report generation changes intentionally:
        python tests/statics/_problem_fixtures.py --regenerate-golden

    WARNING: This will overwrite the golden files. Only run this when
    you've verified the new output is correct.
    """
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    for problem_class in PROBLEMS_WITH_GOLDEN_FILES:
        golden_base = get_golden_base(problem_class)
        output_unit = _get_problem_unit(problem_class)

        # Solve using the new solver (returns a ParallelogramLawProblem instance)
        problem = solve_class(problem_class, output_unit)

        if not problem.is_solved:
            print(f"WARNING: {problem_class.name} failed to solve")
            continue

        # Generate markdown
        md_path = GOLDEN_DIR / f"{golden_base}.md"
        problem.generate_report(str(md_path), format="markdown")

        # Normalize the file (replace dates with placeholders)
        content = md_path.read_text(encoding="utf-8")
        content = normalize_report(content)
        md_path.write_text(content, encoding="utf-8")
        print(f"Regenerated: {md_path}")

        # Generate LaTeX
        tex_path = GOLDEN_DIR / f"{golden_base}.tex"
        problem.generate_report(str(tex_path), format="latex")

        # Normalize the file
        content = tex_path.read_text(encoding="utf-8")
        content = normalize_report(content)
        tex_path.write_text(content, encoding="utf-8")
        print(f"Regenerated: {tex_path}")


# =============================================================================
# Run as script to generate reports
# =============================================================================

if __name__ == "__main__":
    import sys

    def show_menu():
        """Show interactive menu and get user choice."""
        print("\n" + "=" * 50)
        print("Problem Fixtures - Report Generation")
        print("=" * 50)
        print("\nOptions:")
        print("  1. Regenerate golden files (for snapshot tests)")
        print("  2. Generate debug reports (MD/PDF)")
        print("  3. Exit")
        print("")
        return input("Enter choice (1-3): ").strip()

    # Check for command-line arguments first
    if len(sys.argv) > 1:
        if sys.argv[1] == "--regenerate-golden":
            print(f"Regenerating golden files to: {GOLDEN_DIR}")
            regenerate_golden_files()
            print("Done!")
        elif sys.argv[1] == "--debug":
            print(f"Generating debug reports to: {DEBUG_REPORT_DIR}")
            generate_all_debug_reports()
            print("Done!")
        else:
            print("Usage:")
            print("  python _problem_fixtures.py --regenerate-golden  # Regenerate golden files")
            print("  python _problem_fixtures.py --debug              # Generate debug reports")
            print("  python _problem_fixtures.py                      # Interactive menu")
    else:
        # Interactive mode
        choice = show_menu()

        if choice == "1":
            print(f"\nRegenerating golden files to: {GOLDEN_DIR}")
            regenerate_golden_files()
            print("\nDone!")
        elif choice == "2":
            print(f"\nGenerating debug reports to: {DEBUG_REPORT_DIR}")
            generate_all_debug_reports()
            print("\nDone!")
        elif choice == "3":
            print("Exiting.")
        else:
            print(f"Invalid choice: {choice}")
