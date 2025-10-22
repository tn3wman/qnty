"""
Example demonstrating SelectVariable.set() usage with type safety.

This shows how to use SelectVariable in Problems with proper type checking.
"""

from dataclasses import dataclass

from qnty import Dimensionless, Force, Length, Pressure, Problem
from qnty.algebra import SelectOption, SelectVariable, equation, match_expr


@dataclass(frozen=True)
class FlangeType(SelectOption):
    """ASME flange types for calculations."""
    integral_welded_slip: str = "integral_welded_slip"
    loose_type_lap_with_hub: str = "loose_type_lap_with_hub"
    loose_type_lap_without_hub: str = "loose_type_lap_without_hub"
    reverse_integral_type: str = "reverse_integral_type"
    reverse_loose_type: str = "reverse_loose_type"


@dataclass(frozen=True)
class GasketType(SelectOption):
    """ASME gasket types for bolt load calculations."""
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"


class SimpleFlangeCalculation(Problem):
    """Simplified flange calculation demonstrating SelectVariable usage."""

    name = "Simple Flange Calculation"
    description = "Demonstrates SelectVariable.set() with type safety"

    # Define select variables with initial values
    flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    # Define some basic parameters
    G = Length("Location of Gasket Reaction").set(3).inch
    P = Pressure("Design Pressure").set(100).pound_force_per_square_inch
    b = Length("Effective Gasket Width").set(0.15).inch
    m = Dimensionless("Gasket Factor").set(2.0).dimensionless

    # Calculate bolt load based on gasket type
    W_o = Force("Design Bolt Load", is_known=False)
    pi = 3.14159

    W_o_eqn = equation(
        W_o,
        match_expr(
            gasket_type,
            GasketType.non_self_energized, 0.785 * G**2 * P + 2 * b * pi * G * m * P,
            GasketType.self_energized, 0.785 * G**2 * P,
        ),
    )


def main():
    """Demonstrate SelectVariable.set() usage."""

    print("=" * 60)
    print("SelectVariable.set() Demonstration")
    print("=" * 60)
    print()

    # Create problem instance
    problem = SimpleFlangeCalculation()

    # Display initial state
    print("Initial Configuration:")
    print(f"  {problem.flange_type}")
    print(f"  {problem.gasket_type}")
    print()

    # Solve with initial configuration
    problem.solve()
    print(f"Initial Result: {problem.W_o.to_unit.pound_force}")
    print()

    # ============================================================
    # CORRECT USAGE: Using .set() with proper class attributes
    # ============================================================
    print("-" * 60)
    print("✓ CORRECT: Using .set() with FlangeType attributes")
    print("-" * 60)
    problem.flange_type.set(FlangeType.integral_welded_slip)
    print(f"  {problem.flange_type}")
    print()

    problem.gasket_type.set(GasketType.self_energized)
    print(f"  {problem.gasket_type}")
    problem.solve()
    print(f"Result with self-energized gasket: {problem.W_o.to_unit.pound_force}")
    print()

    # ============================================================
    # INCORRECT USAGE: Trying to use strings (will raise TypeError)
    # ============================================================
    print("-" * 60)
    print("✗ INCORRECT: Trying to use string values")
    print("-" * 60)
    try:
        problem.flange_type.set("loose_type_lap_with_hub")
        print("  ERROR: This should have raised TypeError!")
    except TypeError as e:
        print(f"  ✓ Caught TypeError as expected:")
        print(f"    {e}")
    print()

    # ============================================================
    # INCORRECT USAGE: Trying to mix SelectOption types (will raise TypeError)
    # ============================================================
    print("-" * 60)
    print("✗ INCORRECT: Trying to mix SelectOption types")
    print("-" * 60)
    try:
        # Try to set flange_type with a GasketType option
        problem.flange_type.set(GasketType.non_self_energized)
        print("  ERROR: This should have raised TypeError!")
    except TypeError as e:
        print(f"  ✓ Caught TypeError as expected:")
        print(f"    {e}")
    print()

    # ============================================================
    # DEMONSTRATING ALL VALID OPTIONS
    # ============================================================
    print("-" * 60)
    print("Setting all valid FlangeType options:")
    print("-" * 60)
    for option_name in problem.flange_type.get_option_names():
        option_value = getattr(FlangeType, option_name)
        problem.flange_type.set(option_value)
        print(f"  ✓ Set to {option_name}: {problem.flange_type.value}")
    print()

    # ============================================================
    # COMPARISON: select() vs set()
    # ============================================================
    print("-" * 60)
    print("Comparison: select() vs set()")
    print("-" * 60)

    # select() allows strings (legacy, less type-safe)
    print("Using select() with string value:")
    problem.gasket_type.select("non_self_energized")
    print(f"  {problem.gasket_type}")

    # set() requires proper class attributes (type-safe)
    print("\nUsing set() with class attribute:")
    problem.gasket_type.set(GasketType.self_energized)
    print(f"  {problem.gasket_type}")

    # set() rejects strings
    print("\nTrying set() with string value:")
    try:
        problem.gasket_type.set("non_self_energized")
    except TypeError as e:
        print(f"  ✗ Rejected: {e}")

    print()
    print("=" * 60)
    print("Recommendation: Use .set() for type safety!")
    print("=" * 60)


if __name__ == "__main__":
    main()
