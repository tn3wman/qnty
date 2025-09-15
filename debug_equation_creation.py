#!/usr/bin/env python3

"""Debug the equation creation process to see when T_bar_r becomes header.c."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# First, let me check what happens during simple class definition
print("=== SIMPLE VARIABLE TEST ===")

class SimpleTest:
    # Define variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    print(f"Class-level T_bar_r ID: {id(T_bar_r)}")
    print(f"Class-level T_bar_r name: '{T_bar_r.name}'")

    # Create equation
    print("Creating equation...")
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)
    print("Equation created")

print("\n=== COMPOSED PROBLEM TEST ===")

class ComposedTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    print(f"After header creation - header.c ID: {id(header.c)}")
    print(f"After header creation - header.c name: '{header.c.name}'")

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    print(f"Class-level T_bar_r ID: {id(T_bar_r)}")
    print(f"Class-level T_bar_r name: '{T_bar_r.name}'")

    # Check if T_bar_r and header.c are somehow the same
    print(f"T_bar_r is header.c: {T_bar_r is header.c}")
    print(f"T_bar_r == header.c: {T_bar_r == header.c}")

    # Create equation
    print("Creating equation...")
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)
    print("Equation created")

    # Examine the equation immediately after creation
    print(f"Equation RHS: {t_c_r_eqn.rhs}")

    # Check what variable is in the equation
    if hasattr(t_c_r_eqn.rhs, 'right'):
        from qnty.algebra.nodes import VariableReference
        if isinstance(t_c_r_eqn.rhs.right, VariableReference):
            eq_var = t_c_r_eqn.rhs.right.variable
            print(f"Equation variable ID: {id(eq_var)}")
            print(f"Equation variable name: '{eq_var.name}'")
            print(f"Is T_bar_r: {eq_var is T_bar_r}")
            print(f"Is header.c: {eq_var is header.c}")

print("\n=== INSTANTIATION TEST ===")

# Now test what happens when we instantiate the class
def test_instantiation():
    print("Instantiating ComposedTest...")
    try:
        instance = ComposedTest()
        print("Instantiation completed successfully")

        print(f"Instance T_bar_r ID: {id(instance.T_bar_r)}")
        print(f"Instance header.c ID: {id(instance.header.c)}")

        # Find the equation in the instance
        target_eq = None
        for eq in instance.equations:
            if "Reinforcement" in eq.name:
                target_eq = eq
                break

        if target_eq:
            print(f"Instance equation: {target_eq}")
            if hasattr(target_eq.rhs, 'right'):
                from qnty.algebra.nodes import VariableReference
                if isinstance(target_eq.rhs.right, VariableReference):
                    instance_var = target_eq.rhs.right.variable
                    print(f"Instance equation variable ID: {id(instance_var)}")
                    print(f"Instance equation variable name: '{instance_var.name}'")
                    print(f"Is instance T_bar_r: {instance_var is instance.T_bar_r}")
                    print(f"Is instance header.c: {instance_var is instance.header.c}")
    except Exception as e:
        print(f"Error during instantiation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_instantiation()