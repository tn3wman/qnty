import pytest

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.algebra import equation


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new simplified syntax
    P = Pressure("Design Pressure").set(90).psi
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).psi
    E = Dimensionless("Quality Factor").set(0.8).dimensionless
    W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless

    Y = Dimensionless("Y Coefficient").set(0.4).dimensionless  # Default value; will be updated by equation

    # Unknown variables - using new simplified syntax
    T = Length("Wall Thickness")
    d = Length("Inside Diameter")
    t = Length("Pressure Design Thickness")
    t_m = Length("Minimum Required Thickness")
    P_max = Pressure("Pressure, Maximum")

    # Equations
    T_eqn = equation(T, T_bar * (1 - U_m))
    d_eqn = equation(d, D - 2 * T)
    t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = equation(t_m, t + c)
    P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))


def debug_test():
    problem = StraightPipeInternal()

    print("Variables before solving:")
    for var_name in ["P", "D", "T", "P_max"]:
        var = getattr(problem, var_name)
        print(f"  {var_name}: value={var.value}, preferred={var.preferred}")

    problem.solve()

    print("\nVariables after solving:")
    for var_name in ["P", "D", "T", "P_max"]:
        var = getattr(problem, var_name)
        print(f"  {var_name}: value={var.value}, preferred={var.preferred}")

    # Let's also check what the test expects vs what we get
    print(f"\nTest comparison:")
    print(f"  P: expected=90, got={getattr(problem, 'P').value}")
    print(f"  T: expected=0.128625 in, got={getattr(problem, 'T').value} (should be ~0.128625 if converted from meters)")

if __name__ == "__main__":
    debug_test()