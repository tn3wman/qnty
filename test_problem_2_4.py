"""Test Problem 2-4 report generation with partially known forces."""
from pathlib import Path
from qnty.extensions.reporting import generate_report
from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector


class Problem_2_4(VectorEquilibriumProblem):
    """Problem 2-4: Known angles, unknown magnitudes."""
    name = "Problem 2-4: Find Force Components"
    description = """
    The vertical force F acts downward at A on the two-membered frame.
    Determine the magnitudes of the two components of F directed along the axes of AB and AC.
    Set F = 500 N.
    """

    F_AB = ForceVector.unknown("F_AB", angle=225, unit="N")  # Known angle, unknown magnitude
    F_AC = ForceVector.unknown("F_AC", angle=330, unit="N")  # Known angle, unknown magnitude
    F = ForceVector(
        magnitude=500, angle=270, unit="N",
        name="F", description="Resultant (vertical downward)",
        is_resultant=True
    )


if __name__ == "__main__":
    problem = Problem_2_4()
    problem.solve()

    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    md_file = reports_dir / "problem_2_4_test.md"
    generate_report(problem, md_file, format="markdown")
    print(f"Report generated: {md_file}")

    # Read and print the unknown variables section
    content = md_file.read_text()
    lines = content.split('\n')
    in_unknown = False
    for i, line in enumerate(lines):
        if '## 2. Unknown Variables' in line:
            in_unknown = True
        if in_unknown:
            print(line)
            if i > 0 and lines[i-1].startswith('##') and not line.startswith('##'):
                break
