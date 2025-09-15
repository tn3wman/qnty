#!/usr/bin/env python3

"""Debug script to trace exact substitution logic."""

from tests.test_composed_problem import create_welded_branch_connection
from qnty.algebra.nodes import VariableReference, BinaryOperation

def debug_exact_substitution():
    problem = create_welded_branch_connection()

    # Set up problem parameters
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

    print("=== DEBUGGING EXACT SUBSTITUTION ===")

    # Get the exact variables
    print(f"T_bar_r: '{problem.T_bar_r.name}' = {problem.T_bar_r.value} (ID: {id(problem.T_bar_r)})")
    print(f"header.c: '{problem.header.c.name}' = {problem.header.c.value} (ID: {id(problem.header.c)})")

    # Find equation
    weld_equation = None
    for eq in problem.equations:
        if "Weld Throat, Reinforcement" in eq.name:
            weld_equation = eq
            break

    if weld_equation and isinstance(weld_equation.rhs, BinaryOperation):
        rhs_var_ref = weld_equation.rhs.right
        if isinstance(rhs_var_ref, VariableReference):
            original_var = rhs_var_ref.variable
            print(f"\nOriginal var in equation: '{original_var.name}' = {original_var.value} (ID: {id(original_var)})")

            print(f"\n=== CHECKING ALL VARIABLES IN PROBLEM ===")
            # Check all variables in self.variables for name matches
            for symbol, var in problem.variables.items():
                if hasattr(var, 'name'):
                    name_match = var.name == original_var.name
                    print(f"  {symbol}: '{var.name}' = {getattr(var, 'value', 'N/A')} (ID: {id(var)}) - Name match: {name_match}")
                    if name_match and id(var) != id(original_var):
                        print(f"    *** WOULD BE SUBSTITUTED! ***")

            print(f"\n=== MANUAL CANONICALIZATION TEST ===")
            # Test what canonicalization does manually
            print(f"Testing canonicalization on variable: '{original_var.name}'")

            # First: check system-level variables
            found_system_match = False
            for attr_name in dir(problem):
                if not attr_name.startswith('_'):
                    attr_value = getattr(problem, attr_name, None)
                    if (attr_value and hasattr(attr_value, 'name') and
                        hasattr(attr_value, 'value') and
                        attr_value.name == original_var.name):
                        print(f"  System match: {attr_name} -> '{attr_value.name}' = {attr_value.value} (ID: {id(attr_value)})")
                        if id(original_var) != id(attr_value):
                            print(f"    *** FIRST PRIORITY SUBSTITUTION! ***")
                            found_system_match = True
                            break

            # Second: check sub-problem attributes
            if not found_system_match:
                for attr_name in dir(problem):
                    if not attr_name.startswith('_'):
                        attr_value = getattr(problem, attr_name, None)
                        if hasattr(attr_value, '__dict__'):
                            for sub_attr_name in dir(attr_value):
                                if not sub_attr_name.startswith('_'):
                                    try:
                                        sub_attr_value = getattr(attr_value, sub_attr_name, None)
                                        if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                            hasattr(sub_attr_value, 'value') and
                                            sub_attr_value.name == original_var.name):
                                            print(f"  Sub-problem match: {attr_name}.{sub_attr_name} -> '{sub_attr_value.name}' = {sub_attr_value.value} (ID: {id(sub_attr_value)})")
                                            if id(original_var) != id(sub_attr_value):
                                                print(f"    *** SUB-PROBLEM SUBSTITUTION! ***")
                                    except (AttributeError, TypeError):
                                        continue

if __name__ == "__main__":
    debug_exact_substitution()