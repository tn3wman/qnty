#!/usr/bin/env python3
"""
Debug the exact test case that fails.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

# Monkey patch the solve_for method to add debugging
from qnty.algebra.equation import Equation

original_solve_for = Equation.solve_for

def debug_solve_for(self, target_var: str, variable_values):
    print(f"=== SOLVE_FOR DEBUG ===")
    print(f"Target var: {target_var!r}")
    print(f"Equation: {self}")
    print(f"Equation variables: {self.variables}")
    print(f"Variable_values keys: {list(variable_values.keys())}")
    print(f"Target var in equation.variables: {target_var in self.variables}")

    if target_var not in self.variables:
        print(f"ERROR: Variable '{target_var}' not found in equation")
        print(f"Looking for possible name mismatches...")

        # Check each variable_values key to see if any relate to the target
        for var_key in variable_values.keys():
            if target_var in var_key or var_key in target_var:
                print(f"  Possible match: {var_key}")

        # Check the LHS and RHS of the equation
        print(f"LHS: {self.lhs} (type: {type(self.lhs)})")
        print(f"RHS: {self.rhs} (type: {type(self.rhs)})")

        from qnty.algebra.nodes import VariableReference
        if isinstance(self.lhs, VariableReference):
            print(f"LHS.name: {self.lhs.name!r}")
            print(f"LHS.variable: {self.lhs.variable}")
            print(f"LHS.variable.symbol: {getattr(self.lhs.variable, 'symbol', 'NO SYMBOL')}")

    return original_solve_for(self, target_var, variable_values)

# Apply the patch
Equation.solve_for = debug_solve_for

# Now run the actual test
from tests.test_composed_problem import create_welded_branch_connection

problem = create_welded_branch_connection()

# Set the test data
problem.P.set(2068000).pascal

# For header
problem.header.D.set(219.1).mm
problem.header.T_bar.set(8.18).mm
problem.header.U_m.set(0.125).dimensionless
problem.header.c.set(2.5).mm
problem.header.S.set(110000000).pascal
problem.header.E.set(1).dimensionless
problem.header.W.set(1).dimensionless
problem.header.Y.set(0.4).dimensionless

# For branch
problem.branch.D.set(114.3).mm
problem.branch.T_bar.set(6.02).mm
problem.branch.U_m.set(0.125).dimensionless
problem.branch.c.set(2.5).mm
problem.branch.S.set(110000000).pascal
problem.branch.E.set(1).dimensionless
problem.branch.W.set(1).dimensionless
problem.branch.Y.set(0.4).dimensionless

print("=== Starting solve ===")
try:
    problem.solve()
    print(f"SUCCESS: {problem.is_solved}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()