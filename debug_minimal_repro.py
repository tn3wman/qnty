#!/usr/bin/env python3

"""Minimal reproduction to isolate the T_bar_r -> header.c substitution bug."""

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

class MinimalReproduction(Problem):
    """Minimal reproduction of the variable substitution bug."""

    # Create a sub-problem
    header = create_straight_pipe_internal()

    # Define our own T_bar_r variable
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create the problematic equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_minimal_reproduction():
    problem = MinimalReproduction()

    # Set up header values
    problem.header.c.set(2.5).millimeter

    print("=== MINIMAL REPRODUCTION ===")
    print(f"T_bar_r: '{problem.T_bar_r.name}' = {problem.T_bar_r.value} (ID: {id(problem.T_bar_r)})")
    print(f"header.c: '{problem.header.c.name}' = {problem.header.c.value} (ID: {id(problem.header.c)})")

    # Find the equation
    target_equation = None
    for eq in problem.equations:
        if "Weld Throat, Reinforcement" in eq.name:
            target_equation = eq
            break

    if target_equation:
        print(f"\nEquation: {target_equation}")
        print(f"RHS: {target_equation.rhs}")

        # Check what variable is in the RHS
        if hasattr(target_equation.rhs, 'right'):
            from qnty.algebra.nodes import VariableReference
            if isinstance(target_equation.rhs.right, VariableReference):
                rhs_var = target_equation.rhs.right.variable
                print(f"RHS variable: '{rhs_var.name}' = {rhs_var.value} (ID: {id(rhs_var)})")

                # Is it T_bar_r or something else?
                if id(rhs_var) == id(problem.T_bar_r):
                    print("✓ RHS correctly references T_bar_r")
                else:
                    print("✗ RHS references wrong variable!")
                    print(f"  Expected T_bar_r ID: {id(problem.T_bar_r)}")
                    print(f"  Actual variable ID: {id(rhs_var)}")

    # Test solve
    try:
        problem.solve()
        print(f"\nAfter solving:")
        print(f"t_c_r.value: {problem.t_c_r.value}")
        expected = 0.5 * problem.T_bar_r.value
        print(f"Expected (0.5 * T_bar_r): {expected}")
        print(f"Match: {abs(problem.t_c_r.value - expected) < 1e-10}")
    except Exception as e:
        print(f"Solve failed: {e}")

if __name__ == "__main__":
    test_minimal_reproduction()