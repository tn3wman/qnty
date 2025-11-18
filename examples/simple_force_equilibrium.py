"""
Simple Force Vector Example: Solving for Unknown Forces in Equilibrium

This example demonstrates how to solve for unknown forces when you know
the desired resultant. This is common when designing structures or analyzing
forces needed to achieve a specific result.

Problem:
    A tugboat (F_A) pulls at 30° from the +x axis with F_A = 2000 N.
    A second tugboat (F_B) pulls with unknown magnitude and direction.

    Find: The magnitude and direction of F_B such that the resultant
          force is F_R = 3000 N along the positive x-axis.
"""

from qnty.problems.vector_equilibrium import ParallelogramLaw
from qnty.spatial.force_vector import ForceVector


class TugboatProblem(ParallelogramLaw):
    """
    Two tugboats pulling a barge. Given F_A and desired F_R, find F_B.

    This demonstrates the triangle method for solving force equilibrium problems.
    """

    name = "Tugboat Force Problem"
    description = """
    Two tugboats are pulling a barge. Tugboat A pulls with 2000 N at 30° from
    the positive x-axis. Determine the force F_B (magnitude and direction) that
    tugboat B must apply to create a resultant force of 3000 N along the
    positive x-axis.
    """

    # Known force from tugboat A
    F_A = ForceVector(
        magnitude=2000,
        unit="N",
        angle=30,
        wrt="+x",
        name="F_A",
        description="Force from tugboat A"
    )

    # Unknown force from tugboat B (to be solved)
    F_B = ForceVector.unknown(
        name="F_B",
        description="Force from tugboat B (unknown)"
    )

    # Known desired resultant
    F_R = ForceVector(
        magnitude=3000,
        unit="N",
        angle=0,
        wrt="+x",
        name="F_R",
        description="Desired resultant force along +x axis",
        is_resultant=True
    )


def main():
    print("=" * 70)
    print("Simple Force Equilibrium Example: Solving for Unknown Forces")
    print("=" * 70)
    print()

    # Create and solve the problem
    problem = TugboatProblem()

    print("Given:")
    print(f"  F_A = 2000 N at 30° from +x axis")
    print(f"  F_R = 3000 N along +x axis (desired resultant)")
    print(f"  F_B = ? (unknown)")
    print()

    print("Solving using the triangle method...")
    print("(F_A + F_B = F_R, so we solve for F_B)")
    print()

    solution = problem.solve()

    # Extract the solved force
    F_B_solved = solution["F_B"]

    print("Solution:")
    print("-" * 70)

    # Show all forces and their components
    F_A = problem.F_A
    F_A_x, F_A_y = F_A.get_components_in_system()

    print(f"  F_A components:")
    print(f"    F_Ax = {F_A_x.value:.1f} N")
    print(f"    F_Ay = {F_A_y.value:.1f} N")
    print()

    F_B_x, F_B_y = F_B_solved.get_components_in_system()
    print(f"  F_B (solved):")
    print(f"    Magnitude: {F_B_solved.magnitude.value:.1f} N")
    print(f"    Direction: {F_B_solved.angle_in('degree'):.1f}° from +x axis")
    print(f"    F_Bx = {F_B_x.value:.1f} N")
    print(f"    F_By = {F_B_y.value:.1f} N")
    print()

    # Verify the resultant
    F_R = problem.F_R
    F_R_x, F_R_y = F_R.get_components_in_system()
    print(f"  Resultant F_R (verification):")
    print(f"    ΣFx = F_Ax + F_Bx = {F_A_x.value:.1f} + {F_B_x.value:.1f} = {F_R_x.value:.1f} N")
    print(f"    ΣFy = F_Ay + F_By = {F_A_y.value:.1f} + ({F_B_y.value:.1f}) = {F_R_y.value:.1f} N")
    print(f"    Magnitude: {F_R.magnitude.value:.1f} N")
    print(f"    Direction: {F_R.angle_in('degree'):.1f}° from +x axis ✓")
    print()

    print("=" * 70)
    print("This example shows how to solve for unknown forces using equilibrium:")
    print("  Given: F_A (known) + F_B (unknown) = F_R (known)")
    print("  Method: Use component equilibrium equations")
    print("    ΣFx = 0  →  F_Ax + F_Bx = F_Rx")
    print("    ΣFy = 0  →  F_Ay + F_By = F_Ry")
    print("  Solve the system of equations for F_B magnitude and direction")
    print("=" * 70)


if __name__ == "__main__":
    main()
