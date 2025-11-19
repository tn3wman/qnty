"""
Simple Force Vector Example: Finding the Resultant Force

This example demonstrates how to find the resultant (sum) of multiple known forces
using the component method. This is one of the most common problems in statics.

Problem:
    Two forces act on a bracket:
    - F_1 = 400 N at 30° from the positive x-axis
    - F_2 = 800 N at 45° from the negative y-axis

    Find: The magnitude and direction of the resultant force F_R
"""

from qnty.solving.component_solver import ComponentSolver
from qnty.spatial.force_vector import ForceVector


def main():
    print("=" * 70)
    print("Simple Force Vector Example: Finding the Resultant Force")
    print("=" * 70)
    print()

    # Define the known forces
    F_1 = ForceVector(
        magnitude=400,
        unit="N",
        angle=30,
        wrt="+x",
        name="F_1",
        description="First force at 30° from +x axis"
    )

    F_2 = ForceVector(
        magnitude=800,
        unit="N",
        angle=45,
        wrt="-y",
        name="F_2",
        description="Second force at 45° from -y axis"
    )

    # Define the unknown resultant force
    F_R = ForceVector.unknown(
        name="F_R",
        is_resultant=True,
        description="Resultant force (to be calculated)"
    )

    print("Given Forces:")
    print(f"  F_1 = {F_1.magnitude.value:.0f} N at {F_1.angle_in('degree'):.1f}°")
    print(f"  F_2 = {F_2.magnitude.value:.0f} N at {F_2.angle_in('degree', wrt='-y'):.1f}° from -y")
    print()

    # Create solver and solve
    solver = ComponentSolver()
    forces = [F_1, F_2, F_R]
    solution = solver.solve(forces)

    # Extract results
    resultant = solution["F_R"]

    print("Solution:")
    print("-" * 70)

    # Display component breakdown
    F_1_x, F_1_y = F_1.get_components_in_system()
    F_2_x, F_2_y = F_2.get_components_in_system()

    print(f"  F_1 components: F_1x = {F_1_x.value:.1f} N, F_1y = {F_1_y.value:.1f} N")
    print(f"  F_2 components: F_2x = {F_2_x.value:.1f} N, F_2y = {F_2_y.value:.1f} N")
    print()

    # Sum of components
    sum_x = F_1_x.value + F_2_x.value
    sum_y = F_1_y.value + F_2_y.value
    print(f"  ΣFx = {sum_x:.1f} N")
    print(f"  ΣFy = {sum_y:.1f} N")
    print()

    # Final resultant
    print(f"  Resultant Force:")
    print(f"    Magnitude: F_R = {resultant.magnitude.value:.1f} N")
    print(f"    Direction: θ = {resultant.angle_in('degree'):.1f}° (counterclockwise from +x)")
    print()

    print("=" * 70)
    print("This example shows the basic component method for finding resultants:")
    print("  1. Break each force into x and y components")
    print("  2. Sum all x-components to get ΣFx")
    print("  3. Sum all y-components to get ΣFy")
    print("  4. Calculate magnitude: |F_R| = √(ΣFx² + ΣFy²)")
    print("  5. Calculate direction: θ = arctan(ΣFy / ΣFx)")
    print("=" * 70)


if __name__ == "__main__":
    main()
