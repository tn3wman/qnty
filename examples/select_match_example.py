"""
Example: Using SelectVariable and match_expr for ASME Bolt Load Calculations
=============================================================================

This example demonstrates how to use the SelectVariable and match_expr features
to implement engineering calculations that vary based on categorical selections,
such as gasket types in ASME BPVC Section VIII Division 2.
"""

import math
from dataclasses import dataclass

from qnty import Dimensionless, Force, Length, Pressure, Problem
from qnty.algebra import SelectOption, SelectVariable, equation, match_expr


# Step 1: Define your option types as frozen dataclasses
@dataclass(frozen=True)
class GasketType(SelectOption):
    """
    ASME gasket classification options.

    These options are immutable and can be enumerated for UI generation.
    """
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"


# Step 2: Create a Problem class that uses SelectVariable
class BoltLoadCalculation(Problem):
    """
    Calculate design bolt loads per ASME BPVC Section VIII Division 2, 4.16.6.

    The formula for W_o (design bolt load for operating condition) depends on
    the gasket type:
    - Non-self-energized: W_o = 0.785*G²*P + 2*b*π*G*m*P  (Equation 4.16.4)
    - Self-energized: W_o = 0.785*G²*P  (Equation 4.16.5)
    """

    name = "ASME Bolt Load Calculation with Gasket Selection"

    # Input: Gasket selection
    gasket_type = SelectVariable(
        "Gasket Type",
        GasketType,
        GasketType.non_self_energized  # Default selection
    )

    # Input: Design parameters
    P = Pressure("Design Pressure").set(100).psi
    G = Length("Gasket Reaction Location").set(3).inch
    b = Length("Effective Gasket Seating Width").set(0.15).inch
    m = Dimensionless("Gasket Factor m").set(2.0).dimensionless

    # Output: Bolt load (varies by gasket type)
    W_o = Force("Design Bolt Load W_o")

    # Equation with match expression
    pi = math.pi
    W_o_eqn = equation(
        W_o,
        match_expr(
            gasket_type,
            GasketType.non_self_energized, 0.785 * G**2 * P + 2 * b * pi * G * m * P,
            GasketType.self_energized, 0.785 * G**2 * P
        )
    )


def main():
    """Demonstrate the select/match functionality."""

    print("=" * 70)
    print("ASME Bolt Load Calculation with Gasket Type Selection")
    print("=" * 70)
    print()

    # Create the problem
    problem = BoltLoadCalculation()

    # Show all available gasket options (useful for UI generation)
    print("Available Gasket Types:")
    for name, value in problem.gasket_type.get_options():
        print(f"  - {name}: {value}")
    print()

    # Solve with default selection (non-self-energized)
    print(f"Current Selection: {problem.gasket_type.value}")
    problem.solve()
    print(f"Design Bolt Load (W_o): {problem.W_o}")
    print()

    # Change to self-energized gasket
    print("Switching to self-energized gasket...")
    problem.gasket_type.select(GasketType.self_energized)
    print(f"Current Selection: {problem.gasket_type.value}")
    problem.solve()
    print(f"Design Bolt Load (W_o): {problem.W_o}")
    print()

    # Compare the results
    problem.gasket_type.select(GasketType.non_self_energized)
    problem.solve()
    W_o_non_self = problem.W_o.value

    problem.gasket_type.select(GasketType.self_energized)
    problem.solve()
    W_o_self = problem.W_o.value

    print("=" * 70)
    print("Comparison:")
    print(f"  Non-self-energized gasket: {W_o_non_self:.2f} N")
    print(f"  Self-energized gasket:     {W_o_self:.2f} N")
    print(f"  Difference:                {W_o_non_self - W_o_self:.2f} N")
    print(f"  Reduction:                 {(1 - W_o_self/W_o_non_self)*100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
