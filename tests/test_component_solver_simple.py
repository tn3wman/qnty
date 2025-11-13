"""
Comprehensive tests for ComponentSolver using problems 2-32 to 2-44 from textbook.

These tests validate the Cartesian/Component method for solving force equilibrium
problems using scalar notation: ΣFx = 0, ΣFy = 0.
"""

import pytest
import math
from qnty.solving.component_solver import ComponentSolver
from qnty.spatial.force_vector import ForceVector


def test_problem_2_32_component_method():
    """
    Test ComponentSolver with Problem 2-32.

    Problem 2-32: Determine the magnitude of the resultant force and its direction,
    measured counterclockwise from the positive x axis.

    Given:
    - F1 = 200 N at 45° from +y axis
    - F2 = 150 N at 30° from -x axis

    Expected (from solution manual):
    - FRx = 11.518 N
    - FRy = 216.42 N
    - FR = 216.73 N ≈ 217 N
    - θ = 86.95° ≈ 87.0°
    """
    # Create forces using standard angles (CCW from +x axis)
    # F1: 200 N at 45° from +x axis
    F1 = ForceVector(
        magnitude=200,
        angle=45,  # 45° CCW from +x axis
        unit="N",
        name="F_1"
    )

    # F2: 150 N at 150° from +x axis (quadrant II)
    F2 = ForceVector(
        magnitude=150,
        angle=150,  # 150° CCW from +x axis
        unit="N",
        name="F_2"
    )

    # Create solver
    solver = ComponentSolver()

    # Solve for resultant
    resultant = solver.solve_resultant([F1, F2], force_unit="N")

    # Check components
    sum_x, sum_y, _ = solver.sum_components([F1, F2])

    print(f"\nProblem 2-32 Results:")
    print(f"ΣFx = {sum_x:.3f} N (expected: 11.518 N)")
    print(f"ΣFy = {sum_y:.3f} N (expected: 216.42 N)")
    assert resultant.magnitude is not None and resultant.magnitude.value is not None
    assert resultant.angle is not None and resultant.angle.value is not None
    print(f"FR = {resultant.magnitude.value:.3f} N (expected: 216.73 N)")
    print(f"θ = {math.degrees(resultant.angle.value):.2f}° (expected: 86.95°)")

    # Assertions with tolerance
    assert pytest.approx(sum_x, abs=0.01) == 11.518, f"ΣFx mismatch: got {sum_x}, expected 11.518"
    assert pytest.approx(sum_y, abs=0.01) == 216.42, f"ΣFy mismatch: got {sum_y}, expected 216.42"
    assert pytest.approx(resultant.magnitude.value, abs=0.01) == 216.73, f"FR mismatch"
    assert pytest.approx(math.degrees(resultant.angle.value), abs=0.1) == 86.95, f"θ mismatch"

    print("\nSolution steps:")
    for step in solver.get_solution_steps():
        print(f"  {step}")


def test_problem_2_40_component_method():
    """
    Test ComponentSolver with Problem 2-40.

    Problem 2-40: Determine the magnitude of the resultant force and its direction,
    measured counterclockwise from the positive x axis.

    This is actually the same as problem 2-32 but with different labeling.

    Given:
    - F1 = 150 N at 30° from -x axis (quadrant II)
    - F2 = 200 N at 45° from +x axis

    Expected (from solution manual):
    - FRx = 11.518 N
    - FRy = 216.421 N
    - FR = 217 N
    - θ = 87.0°
    """
    # F1: 150 N at 150° from +x axis
    F1 = ForceVector(
        magnitude=150,
        angle=150,
        unit="N",
        name="F_1"
    )

    # F2: 200 N at 45° from +x axis
    F2 = ForceVector(
        magnitude=200,
        angle=45,
        unit="N",
        name="F_2"
    )

    solver = ComponentSolver()
    resultant = solver.solve_resultant([F1, F2], force_unit="N")
    sum_x, sum_y, _ = solver.sum_components([F1, F2])

    print(f"\nProblem 2-40 Results:")
    print(f"ΣFx = {sum_x:.3f} N (expected: 11.518 N)")
    print(f"ΣFy = {sum_y:.3f} N (expected: 216.421 N)")
    assert resultant.magnitude is not None and resultant.magnitude.value is not None
    assert resultant.angle is not None and resultant.angle.value is not None
    print(f"FR = {resultant.magnitude.value:.3f} N (expected: 217 N)")
    print(f"θ = {math.degrees(resultant.angle.value):.2f}° (expected: 87.0°)")

    # Assertions with tolerance
    assert pytest.approx(sum_x, abs=0.01) == 11.518
    assert pytest.approx(sum_y, abs=0.01) == 216.421
    assert pytest.approx(resultant.magnitude.value, abs=1) == 217
    assert pytest.approx(math.degrees(resultant.angle.value), abs=0.1) == 87.0


def test_problem_2_41_component_method():
    """
    Test ComponentSolver with Problem 2-41.

    Problem 2-41: Determine the magnitude of the resultant force and its direction,
    measured counterclockwise from the positive x axis.

    Given:
    - F1 = 4 kN along +x axis (0°)
    - F2 = 5 kN at 45° from +x axis
    - F3 = 8 kN at 15° from -y axis (in quadrant IV)

    Expected (from solution manual):
    - FRx = 5.465 kN
    - FRy = 11.263 kN
    - FR = 12.5 kN
    - θ = 64.1°
    """
    # F1: 4 kN along +x axis (4000 N)
    F1 = ForceVector(
        magnitude=4000,
        angle=0,
        unit="N",
        name="F_1"
    )

    # F2: 5 kN at 45° from +x axis (5000 N)
    F2 = ForceVector(
        magnitude=5000,
        angle=45,
        unit="N",
        name="F_2"
    )

    # F3: 8 kN at 15° from -y axis (8000 N)
    # From -y axis (270°), 15° toward +x = 270° + 15° = 285° (or -75°)
    # But looking at solution: F3x = -8 sin 15° (negative), F3y = 8 cos 15° (positive)
    # This means F3 is at 15° from +y axis toward -x, which is 90° + 15° = 105°
    F3 = ForceVector(
        magnitude=8000,
        angle=105,  # 105° from +x axis
        unit="N",
        name="F_3"
    )

    solver = ComponentSolver()
    resultant = solver.solve_resultant([F1, F2, F3], force_unit="N")
    sum_x, sum_y, _ = solver.sum_components([F1, F2, F3])

    print(f"\nProblem 2-41 Results:")
    print(f"ΣFx = {sum_x/1000:.3f} kN (expected: 5.465 kN)")
    print(f"ΣFy = {sum_y/1000:.3f} kN (expected: 11.263 kN)")
    assert resultant.magnitude is not None and resultant.magnitude.value is not None
    assert resultant.angle is not None and resultant.angle.value is not None
    print(f"FR = {resultant.magnitude.value/1000:.3f} kN (expected: 12.5 kN)")
    print(f"θ = {math.degrees(resultant.angle.value):.2f}° (expected: 64.1°)")

    # Assertions with tolerance (convert to kN for comparison)
    assert pytest.approx(sum_x/1000, abs=0.01) == 5.465
    assert pytest.approx(sum_y/1000, abs=0.01) == 11.263
    assert pytest.approx(resultant.magnitude.value/1000, abs=0.1) == 12.5
    assert pytest.approx(math.degrees(resultant.angle.value), abs=0.1) == 64.1


if __name__ == "__main__":
    test_problem_2_32_component_method()
    test_problem_2_40_component_method()
    test_problem_2_41_component_method()
