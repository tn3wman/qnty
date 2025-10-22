"""
Comprehensive examples for VectorEquilibriumProblem class.

Demonstrates different usage patterns for solving 2D statics problems:
1. Class inheritance pattern (recommended)
2. Programmatic construction pattern
3. Different input formats (magnitude+angle, components)
4. Real engineering problems from textbooks
"""

from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector
from qnty.core import u


# =============================================================================
# EXAMPLE 1: Class Inheritance Pattern (Textbook Problem 2-1)
# =============================================================================
# Problem: If θ=60° and F=450 N, determine the magnitude of the resultant
# force and its direction, measured counterclockwise from the positive x axis.
# Given: F1 = 700 N at 60°, F2 = 450 N at 105°

class Problem_2_1(VectorEquilibriumProblem):
    """
    Textbook Problem 2-1: Find resultant of two cable forces.

    Most concise way to define a problem - just declare forces as class attributes.
    """
    name = "Textbook Problem 2-1: Cable Forces"
    description = "Find resultant of two forces acting at a point"

    # Define known forces
    F1 = ForceVector(magnitude=700, angle=60, unit="N", name="F1", description="Cable A force")
    F2 = ForceVector(magnitude=450, angle=105, unit="N", name="F2", description="Cable B force")

    # Define unknown resultant
    FR = ForceVector.unknown("FR", is_resultant=True)


def example_1_class_inheritance():
    """Solve using class inheritance pattern."""
    print("=" * 80)
    print("EXAMPLE 1: Class Inheritance Pattern")
    print("=" * 80)

    # Instantiate and solve
    problem = Problem_2_1()
    solution = problem.solve()

    # Access results
    FR = solution["FR"]
    print(f"\nProblem: {problem.name}")
    print(f"Given:")
    print(f"  F1 = 700 N at 60°")
    print(f"  F2 = 450 N at 105°")
    print(f"\nResult:")
    print(f"  FR = {FR}")
    print(f"  Magnitude: {FR.magnitude}")
    print(f"  Direction: {FR.angle}")

    # View solution steps
    print(f"\nSolution Steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"  Step {i}: {step}")

    print()


# =============================================================================
# EXAMPLE 2: Programmatic Construction Pattern
# =============================================================================

def example_2_programmatic():
    """Solve same problem using programmatic construction."""
    print("=" * 80)
    print("EXAMPLE 2: Programmatic Construction Pattern")
    print("=" * 80)

    # Create problem instance
    problem = VectorEquilibriumProblem(
        name="Cable Forces (Programmatic)",
        description="Same problem as Example 1, but constructed programmatically"
    )

    # Add forces programmatically
    problem.add_force(ForceVector(magnitude=700, angle=60, unit="N", name="F1"))
    problem.add_force(ForceVector(magnitude=450, angle=105, unit="N", name="F2"))
    problem.add_force(ForceVector.unknown("FR", is_resultant=True))

    # Solve
    solution = problem.solve()

    # Results
    FR = solution["FR"]
    print(f"\nResult: {FR}")
    print(f"Magnitude: {FR.magnitude.value / u.N.si_factor:.1f} N")
    print(f"Direction: {FR.angle.value * 180 / 3.14159:.1f}°")
    print()


# =============================================================================
# EXAMPLE 3: Component Form (Textbook Problem 2-27)
# =============================================================================
# Problem: Two forces act on a particle. Find the resultant.
# Given: F1 has components Fx=750sin(45°), Fy=750cos(45°)
#        F2 has components Fx=800cos(30°), Fy=-800sin(30°)

class Problem_2_27(VectorEquilibriumProblem):
    """
    Textbook Problem 2-27: Forces given as components.

    Demonstrates using component form instead of magnitude+angle.
    """
    name = "Textbook Problem 2-27: Component Form"
    description = "Find resultant when forces are given as x,y components"

    # Define forces using components (calculated from angles)
    import math
    F1 = ForceVector.from_components(
        x=750 * math.sin(math.radians(45)),
        y=750 * math.cos(math.radians(45)),
        unit="N",
        name="F1"
    )

    F2 = ForceVector.from_components(
        x=800 * math.cos(math.radians(30)),
        y=-800 * math.sin(math.radians(30)),
        unit="N",
        name="F2"
    )

    # Unknown resultant
    FR = ForceVector.unknown("FR", is_resultant=True)


def example_3_component_form():
    """Solve using component form."""
    print("=" * 80)
    print("EXAMPLE 3: Component Form")
    print("=" * 80)

    problem = Problem_2_27()
    solution = problem.solve()

    FR = solution["FR"]
    print(f"\nProblem: {problem.name}")
    print(f"Given forces by components:")
    print(f"  F1 = {problem.F1}")
    print(f"  F2 = {problem.F2}")
    print(f"\nResultant:")
    print(f"  {FR}")
    print(f"  Components: Fx={FR.x}, Fy={FR.y}")
    print()


# =============================================================================
# EXAMPLE 4: Mixed Format - Using u.N fluent API
# =============================================================================

def example_4_fluent_api():
    """Use qnty's fluent API with force units."""
    print("=" * 80)
    print("EXAMPLE 4: Fluent API with Unit References")
    print("=" * 80)

    problem = VectorEquilibriumProblem("Support Cables")

    # Use unit objects from catalog
    problem.add_force(ForceVector(magnitude=1200, angle=0, unit=u.lb, name="Horizontal"))
    problem.add_force(ForceVector(magnitude=900, angle=30, unit=u.lb, name="Cable"))
    problem.add_force(ForceVector.unknown("Support", is_resultant=False))

    solution = problem.solve()

    support = solution["Support"]
    print(f"\nRequired support force:")
    print(f"  {support}")
    print()


# =============================================================================
# EXAMPLE 5: Three Forces at Equilibrium
# =============================================================================

class ThreeForceEquilibrium(VectorEquilibriumProblem):
    """
    Three forces in equilibrium - find the unknown third force.

    Demonstrates equilibrium solving where ΣF = 0.
    """
    name = "Three Force Equilibrium"
    description = "Find the third force that maintains equilibrium"

    F1 = ForceVector(magnitude=500, angle=0, unit="N", name="F1", description="Horizontal force")
    F2 = ForceVector(magnitude=300, angle=90, unit="N", name="F2", description="Vertical force")
    F3 = ForceVector.unknown("F3", is_resultant=False)  # Force needed for equilibrium


def example_5_equilibrium():
    """Solve three-force equilibrium."""
    print("=" * 80)
    print("EXAMPLE 5: Three Force Equilibrium (ΣF = 0)")
    print("=" * 80)

    problem = ThreeForceEquilibrium()
    solution = problem.solve()

    F3 = solution["F3"]
    print(f"\nGiven:")
    print(f"  F1 = 500 N at 0° (horizontal)")
    print(f"  F2 = 300 N at 90° (vertical)")
    print(f"  Find F3 such that ΣF = 0")
    print(f"\nSolution:")
    print(f"  F3 = {F3}")
    print(f"  This force maintains equilibrium")
    print()


# =============================================================================
# EXAMPLE 6: Real-World Engineering Problem
# =============================================================================

class SuspensionCableProblem(VectorEquilibriumProblem):
    """
    Real-world: Bridge suspension cable analysis.

    A cable support has two tension forces. Find the resultant
    load on the anchor point.
    """
    name = "Bridge Suspension Cable Analysis"
    description = "Determine resultant load on cable anchor"

    # Left cable: 15 kN at 45° above horizontal
    cable_left = ForceVector(
        magnitude=15,
        angle=45,
        unit="N",
        name="Left Cable",
        description="Tension in left cable"
    )

    # Right cable: 12 kN at 60° above horizontal
    cable_right = ForceVector(
        magnitude=12,
        angle=60,
        unit="N",
        name="Right Cable",
        description="Tension in right cable"
    )

    # Resultant on anchor
    anchor_load = ForceVector.unknown("Anchor Load", is_resultant=True)


def example_6_real_world():
    """Solve real engineering problem."""
    print("=" * 80)
    print("EXAMPLE 6: Real-World Engineering Problem")
    print("=" * 80)

    problem = SuspensionCableProblem()
    solution = problem.solve()

    anchor = solution["Anchor Load"]

    print(f"\n{problem.name}")
    print(f"{problem.description}")
    print(f"\nGiven:")
    print(f"  Left cable: 15 kN at 45°")
    print(f"  Right cable: 12 kN at 60°")
    print(f"\nDesign Requirement:")
    print(f"  Anchor must support: {anchor}")

    # Additional analysis
    if anchor.magnitude:
        mag_kn = anchor.magnitude.value / u.kN.si_factor
        angle_deg = anchor.angle.value * 180 / 3.14159

        print(f"\nDesign Values:")
        print(f"  Resultant Force: {mag_kn:.2f} kN")
        print(f"  Direction: {angle_deg:.1f}° from horizontal")
        print(f"  Horizontal Component: {anchor.x}")
        print(f"  Vertical Component: {anchor.y}")

        # Safety factor calculation
        if mag_kn > 0:
            anchor_capacity = 35.0  # kN
            safety_factor = anchor_capacity / mag_kn
            print(f"\n  Anchor Capacity: {anchor_capacity} kN")
            print(f"  Safety Factor: {safety_factor:.2f}")
            print(f"  Status: {'ACCEPTABLE' if safety_factor >= 2.0 else 'REVIEW REQUIRED'}")

    print()


# =============================================================================
# EXAMPLE 7: Alternative Constructor Methods
# =============================================================================

def example_7_constructor_methods():
    """Demonstrate different ForceVector constructor methods."""
    print("=" * 80)
    print("EXAMPLE 7: Alternative Constructor Methods")
    print("=" * 80)

    print("\n1. From magnitude and angle (default):")
    F1 = ForceVector(magnitude=500, angle=30, unit="N")
    print(f"   {F1}")

    print("\n2. Using from_magnitude_angle classmethod:")
    F2 = ForceVector.from_magnitude_angle(magnitude=500, angle=30, unit="N")
    print(f"   {F2}")

    print("\n3. From components using from_components:")
    F3 = ForceVector.from_components(x=300, y=400, unit="N")
    print(f"   {F3}")

    print("\n4. Unknown force using unknown classmethod:")
    F4 = ForceVector.unknown("Mystery Force")
    print(f"   {F4}")

    print("\n5. Using different angle units (radians):")
    import math
    F5 = ForceVector(magnitude=1000, angle=math.pi/4, unit="lb", angle_unit="radian")
    print(f"   {F5}")

    print()


# =============================================================================
# EXAMPLE 8: Generating Reports
# =============================================================================

def example_8_report_generation():
    """Generate detailed report from solution."""
    print("=" * 80)
    print("EXAMPLE 8: Report Generation")
    print("=" * 80)

    problem = Problem_2_1()
    solution = problem.solve()

    # Generate report content
    report = problem.generate_report_content()

    print(f"\nReport Content:")
    print(f"Title: {report['title']}")
    print(f"Type: {report['problem_type']}")
    print(f"\nGiven:")
    for item in report['given']:
        print(f"  • {item}")
    print(f"\nFind:")
    for item in report['find']:
        print(f"  • {item}")
    print(f"\nSolution Steps:")
    for i, step in enumerate(report['solution_steps'], 1):
        print(f"  {i}. {step}")
    print(f"\nResults:")
    for item in report['results']:
        print(f"  • {item}")

    print("\n(Note: Full PDF report generation with LaTeX equations")
    print(" can be added using qnty's reporting extensions)")
    print()


# =============================================================================
# RUN ALL EXAMPLES
# =============================================================================

def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        # ("Class Inheritance Pattern", example_1_class_inheritance),
        # ("Programmatic Construction", example_2_programmatic),
        # ("Component Form", example_3_component_form),
        # ("Fluent API", example_4_fluent_api),
        # ("Three Force Equilibrium", example_5_equilibrium),
        # ("Real-World Engineering", example_6_real_world),
        # ("Constructor Methods", example_7_constructor_methods),
        ("Report Generation", example_8_report_generation),
    ]

    print("\n" + "=" * 80)
    print("VECTOR EQUILIBRIUM PROBLEM EXAMPLES")
    print("Comprehensive demonstration of usage patterns")
    print("=" * 80 + "\n")

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            print()

    print("=" * 80)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_all_examples()
