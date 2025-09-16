#!/usr/bin/env python3
"""
Lightweight demo of the new solve() function and the simplified Quantity API.

This example avoids legacy equals()/solve_from() patterns and uses:
- Quantity.set(...).unit for known values
- algebra.solve(target, expression) for solving
"""

from qnty import Dimensionless, Length
from qnty.algebra import solve


def demo_simple_solve():
    # T = T_bar * (1 - U_m)
    T_bar = Length("T_bar").set(0.147).inch
    U_m = Dimensionless("U_m").set(0.125).dimensionless
    T = Length("T")

    solve(T, T_bar * (1 - U_m))
    expected_in = 0.147 * (1 - 0.125)
    assert T.to_unit.inch.value is not None
    assert abs(T.to_unit.inch.value - expected_in) < 1e-6


def demo_sequential_solve():
    # Given D, compute T first, then d = D - 2*T
    D = Length("D").set(10.0).inch
    T_bar = Length("T_bar").set(0.147).inch
    U_m = Dimensionless("U_m").set(0.125).dimensionless
    T = Length("T")
    d = Length("d")

    solve(T, T_bar * (1 - U_m))
    solve(d, D - 2 * T)

    expected_T_in = 0.147 * (1 - 0.125)
    expected_d_in = 10.0 - 2 * expected_T_in
    assert T.to_unit.inch.value is not None
    assert d.to_unit.inch.value is not None
    assert abs(T.to_unit.inch.value - expected_T_in) < 1e-6
    assert abs(d.to_unit.inch.value - expected_d_in) < 1e-6


def main():
    demo_simple_solve()
    demo_sequential_solve()
    print("solve_methods_demo: OK")


if __name__ == "__main__":
    main()
