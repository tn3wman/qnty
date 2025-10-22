"""
Demonstration of AngleReference feature for ForceVector.

This example shows how to use the angle reference system to specify
angles measured in different ways (clockwise vs counterclockwise,
from different reference axes).

Based on engineering statics textbook Problem 2-6, which asks for
the resultant direction "measured clockwise from the positive u axis".
"""

import math

from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.angle_reference import AngleDirection, AngleReference
from qnty.spatial.coordinate_system import CoordinateSystem
from qnty.spatial.force_vector import ForceVector


def example_1_standard_ccw_from_x():
    """
    Example 1: Standard angle reference (CCW from +x-axis).

    This is the default behavior - angles measured counterclockwise
    from the positive x-axis.
    """
    print("=" * 70)
    print("Example 1: Standard Reference (CCW from +x-axis)")
    print("=" * 70)

    # Create a force at 60° counterclockwise from +x-axis
    F1 = ForceVector(magnitude=450, angle=60, unit="N", name="F1")

    print(f"Force F1: {F1.magnitude.value:.1f} N at {math.degrees(F1.angle.value):.1f}°")
    print(f"  Angle reference: {F1.angle_reference}")
    print(f"  X-component: {F1.x.value:.2f} N")
    print(f"  Y-component: {F1.y.value:.2f} N")
    print()


def example_2_clockwise_from_x():
    """
    Example 2: Clockwise from +x-axis (using wrt parameter).

    Some problems specify angles measured clockwise from the +x-axis.
    This is equivalent to measuring negative angles in the standard system.
    """
    print("=" * 70)
    print("Example 2: Clockwise from +x-axis (using wrt='cw:+x')")
    print("=" * 70)

    # Create a force at 30° clockwise from +x-axis using the wrt parameter
    # (This is the same as 330° counterclockwise from +x in standard notation)
    F2 = ForceVector(magnitude=500, angle=30, unit="N", name="F2", wrt="cw:+x")

    print(f"Force F2: {F2.magnitude.value:.1f} N at 30° CW from +x")
    print(f"  Angle reference: {F2.angle_reference}")
    print(f"  Internal angle (CCW from +x): {math.degrees(F2.angle.value):.1f}°")
    print(f"  X-component: {F2.x.value:.2f} N")
    print(f"  Y-component: {F2.y.value:.2f} N")
    print()


def example_3_ccw_from_y():
    """
    Example 3: Counterclockwise from +y-axis (using wrt parameter).

    Some problems use the vertical axis as reference.
    """
    print("=" * 70)
    print("Example 3: Counterclockwise from +y-axis (using wrt='+y')")
    print("=" * 70)

    # Create a force at 45° counterclockwise from +y-axis using wrt parameter
    # (This is 135° counterclockwise from +x in standard notation)
    F3 = ForceVector(magnitude=600, angle=45, unit="N", name="F3", wrt="+y")

    print(f"Force F3: {F3.magnitude.value:.1f} N at 45° CCW from +y")
    print(f"  Angle reference: {F3.angle_reference}")
    print(f"  Internal angle (CCW from +x): {math.degrees(F3.angle.value):.1f}°")
    print(f"  X-component: {F3.x.value:.2f} N")
    print(f"  Y-component: {F3.y.value:.2f} N")
    print()


def example_4_problem_2_6():
    """
    Example 4: Textbook Problem 2-6 simulation (using wrt parameter).

    Problem: Determine the magnitude of the resultant force F_R = F_1 + F_2
    and its direction, measured clockwise from the positive u axis.

    Given:
    - u-v coordinate system with 75° between axes
    - F_1 = 4 kN at 45° from +x (or 45° from +u since u is at 0°)
    - F_2 = 6 kN at 330° from +x

    Expected answer:
    - F_R = 8.03 kN at 1.22° clockwise from +u axis
    """
    print("=" * 70)
    print("Example 4: Textbook Problem 2-6 (using wrt='cw:u')")
    print("=" * 70)
    print("Given:")
    print("  - u-v coordinate system with 75° between axes")
    print("  - F_1 = 4 kN at 45° (standard CCW from +x)")
    print("  - F_2 = 6 kN at 330° (standard CCW from +x)")
    print("Find:")
    print("  - Resultant F_R magnitude and direction")
    print("  - Direction measured CLOCKWISE from positive u axis")
    print()

    # Create u-v coordinate system
    uv_system = CoordinateSystem.from_angle_between("u", "v", axis1_angle=0, angle_between=75)

    # Create the problem using wrt='cw:u' for the result
    class Problem_2_6(VectorEquilibriumProblem):
        """Problem 2-6: Two forces with u-v coordinate system."""

        F_1 = ForceVector(magnitude=4000, angle=45, unit="N", name="F_1", coordinate_system=uv_system)
        F_2 = ForceVector(magnitude=6000, angle=330, unit="N", name="F_2", coordinate_system=uv_system)
        F_R = ForceVector.unknown("F_R", is_resultant=True, coordinate_system=uv_system, wrt="cw:u")

    # Solve
    problem = Problem_2_6()
    solution = problem.solve()

    # Display results
    F_R = solution["F_R"]
    print("Solution:")
    if F_R.magnitude and F_R.magnitude.value is not None:
        print(f"  F_R magnitude: {F_R.magnitude.value / 1000:.3f} kN")

    # The internal angle is stored as standard (CCW from +x)
    if F_R.angle and F_R.angle.value is not None:
        standard_angle_deg = math.degrees(F_R.angle.value)
        print(f"  F_R angle (CCW from +x): {standard_angle_deg:.2f}°")

        # Convert to the desired reference system (CW from +u)
        cw_from_u_angle = F_R.angle_reference.from_standard(F_R.angle.value, angle_unit="degree")
        print(f"  F_R angle (CW from +u): {cw_from_u_angle:.2f}°")

    print()
    print("Expected from textbook: F_R = 8.03 kN at 1.22° CW from +u")
    print()


def example_5_custom_reference():
    """
    Example 5: Custom reference axis at arbitrary angle.

    Demonstrates using a reference axis at any arbitrary angle.
    """
    print("=" * 70)
    print("Example 5: Custom Reference Axis at 30°")
    print("=" * 70)

    # Create angle reference: CCW from a custom axis at 30° from +x
    ref_custom = AngleReference(axis_angle=30, direction=AngleDirection.COUNTERCLOCKWISE, axis_label="custom30")

    # Create a force at 60° CCW from the custom axis
    # (This is 90° CCW from +x in standard notation)
    F5 = ForceVector(magnitude=700, angle=60, unit="N", name="F5", angle_reference=ref_custom)

    print(f"Force F5: {F5.magnitude.value:.1f} N at 60° CCW from custom axis (at 30°)")
    print(f"  Angle reference: {F5.angle_reference}")
    print(f"  Internal angle (CCW from +x): {math.degrees(F5.angle.value):.1f}°")
    print(f"  X-component: {F5.x.value:.2f} N")
    print(f"  Y-component: {F5.y.value:.2f} N")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("ANGLE REFERENCE SYSTEM DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstration shows how to specify angles in different ways:")
    print("  - Counterclockwise (CCW) vs Clockwise (CW)")
    print("  - From different reference axes (+x, +y, -x, -y, custom)")
    print("  - Engineering statics convention: CCW is positive, CW is negative")
    print()

    example_1_standard_ccw_from_x()
    example_2_clockwise_from_x()
    example_3_ccw_from_y()
    example_4_problem_2_6()
    example_5_custom_reference()

    print("=" * 70)
    print("Summary:")
    print("=" * 70)
    print("The AngleReference system allows you to:")
    print("  1. Specify angles in the way they appear in textbook problems")
    print("  2. Internally convert to standard form (CCW from +x) for calculations")
    print("  3. Convert back to any reference system for reporting results")
    print()
    print("Usage (simple wrt parameter):")
    print("  force = ForceVector(magnitude=100, angle=30, unit='N', wrt='cw:+x')")
    print("  force = ForceVector(magnitude=100, angle=45, unit='N', wrt='+y')")
    print("  force = ForceVector(magnitude=100, angle=30, unit='N', wrt='cw:u')")
    print()
    print("Usage (explicit AngleReference):")
    print("  ref = AngleReference.from_axis('+x', direction='clockwise')")
    print("  force = ForceVector(magnitude=100, angle=30, unit='N', angle_reference=ref)")
    print("=" * 70)


if __name__ == "__main__":
    main()
