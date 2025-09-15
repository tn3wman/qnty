#!/usr/bin/env python3

"""Debug the h303 test issue after applying the retrofitting fix."""

from tests.test_composed_problem import create_welded_branch_connection

def debug_h303():
    problem = create_welded_branch_connection()

    # For system
    problem.P.set(3450000).pascal

    # For header
    problem.header.D.set(406.4).millimeter
    problem.header.T_bar.set(12.70).millimeter
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).millimeter
    problem.header.S.set(99300000).pascal
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless

    # For run
    problem.branch.D.set(168.3).millimeter
    problem.branch.T_bar.set(7.11).millimeter
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).millimeter
    problem.branch.S.set(99300000).pascal
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    # For reinforcement
    problem.beta.set(60).degree
    problem.D_r.set(305).millimeter
    problem.T_bar_r.set(12.7).millimeter
    problem.S_r.set(99300000).pascal

    problem.z_b.set(10).millimeter
    problem.z_r.set(10).millimeter

    print("=== H303 DEBUG ===")
    print(f"Before solve:")
    print(f"  T_bar_r.value = {problem.T_bar_r.value}")
    print(f"  header.c.value = {problem.header.c.value}")
    print(f"  branch.c.value = {problem.branch.c.value}")

    # Check the d_1 equation
    d_1_eq = None
    for eq in problem.equations:
        if "d_1" in str(eq):
            d_1_eq = eq
            print(f"  d_1 equation: {eq}")
            break

    problem.solve()

    print(f"After solve:")
    print(f"  d_1.value = {problem.d_1.value}")
    print(f"  Expected d_1 = 185.742 mm = 0.185742 m")
    print(f"  Actual d_1 = {problem.d_1.value} m")

if __name__ == "__main__":
    debug_h303()