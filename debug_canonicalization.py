#!/usr/bin/env python3

"""Debug script to trace the canonicalization issue step by step."""

from tests.test_composed_problem import create_welded_branch_connection
from qnty.algebra.nodes import VariableReference

def debug_canonicalization():
    print("Starting debug_canonicalization...")
    problem = create_welded_branch_connection()
    print("Problem created successfully")

    # Set up the problem just like in the test
    print("Setting up problem parameters...")
    problem.P.set(2068000).pascal
    problem.header.D.set(219.1).millimeter
    problem.header.T_bar.set(8.18).millimeter
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).millimeter
    problem.header.S.set(110000000).pascal
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless
    problem.branch.D.set(114.3).millimeter
    problem.branch.T_bar.set(6.02).millimeter
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).millimeter
    problem.branch.S.set(110000000).pascal
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    # Find the original t_c_r_eqn equation
    print("Looking for t_c_r_eqn equation...")
    original_equation = None
    for eq in problem.equations:
        print(f"  Found equation: {eq.name}")
        if "Weld Throat, Reinforcement" in eq.name:
            original_equation = eq
            break

    if original_equation:
        print("=== ORIGINAL EQUATION ===")
        print(f"Equation: {original_equation}")
        print(f"RHS: {original_equation.rhs}")

        # Extract the variable reference from the RHS (should be T_bar_r)
        rhs_var_ref = None
        if hasattr(original_equation.rhs, 'right') and isinstance(original_equation.rhs.right, VariableReference):
            rhs_var_ref = original_equation.rhs.right
            original_var = rhs_var_ref.variable

            print(f"\nOriginal variable in RHS:")
            print(f"  Variable: {original_var}")
            print(f"  Name: '{original_var.name}'")
            print(f"  Value: {original_var.value}")
            print(f"  ID: {id(original_var)}")

            print(f"\nChecking if original variable is T_bar_r:")
            print(f"  Is same as T_bar_r? {id(original_var) == id(problem.T_bar_r)}")
            print(f"  T_bar_r name: '{problem.T_bar_r.name}'")
            print(f"  T_bar_r ID: {id(problem.T_bar_r)}")

            print(f"\n=== TESTING CANONICALIZATION LOGIC ===")
            # Manually run the canonicalization logic

            # First priority: Check system-level variables
            print("First priority - System level variables:")
            for attr_name in dir(problem):
                if not attr_name.startswith('_'):
                    attr_value = getattr(problem, attr_name, None)
                    if (attr_value and hasattr(attr_value, 'name') and
                        hasattr(attr_value, 'value') and  # Must be a variable
                        attr_value.name == original_var.name):
                        print(f"  MATCH FOUND: {attr_name} -> '{attr_value.name}' = {attr_value.value}")
                        if id(original_var) != id(attr_value):
                            print(f"    Would substitute! Original ID: {id(original_var)} != New ID: {id(attr_value)}")
                        else:
                            print(f"    Same object, no substitution needed")

            # Check sub-problem attributes
            print("\nSub-problem attributes:")
            for attr_name in dir(problem):
                if not attr_name.startswith('_'):
                    attr_value = getattr(problem, attr_name, None)
                    if hasattr(attr_value, '__dict__'):
                        for sub_attr_name in dir(attr_value):
                            if not sub_attr_name.startswith('_'):
                                try:
                                    sub_attr_value = getattr(attr_value, sub_attr_name, None)
                                    if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                        hasattr(sub_attr_value, 'value') and  # Must be a variable
                                        sub_attr_value.name == original_var.name):
                                        print(f"  MATCH FOUND: {attr_name}.{sub_attr_name} -> '{sub_attr_value.name}' = {sub_attr_value.value}")
                                        if id(original_var) != id(sub_attr_value):
                                            print(f"    Would substitute! Original ID: {id(original_var)} != New ID: {id(sub_attr_value)}")
                                        else:
                                            print(f"    Same object, no substitution needed")
                                except (AttributeError, TypeError):
                                    continue

            # Now test actual canonicalization
            print(f"\n=== ACTUAL CANONICALIZATION RESULT ===")
            canonicalized_expr = problem._canonicalize_expression(rhs_var_ref)
            if canonicalized_expr != rhs_var_ref:
                new_var = canonicalized_expr.variable
                print(f"SUBSTITUTION OCCURRED!")
                print(f"  Original var: '{original_var.name}' = {original_var.value} (ID: {id(original_var)})")
                print(f"  New var: '{new_var.name}' = {new_var.value} (ID: {id(new_var)})")
            else:
                print(f"No substitution occurred")

if __name__ == "__main__":
    debug_canonicalization()