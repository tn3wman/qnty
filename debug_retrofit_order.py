#!/usr/bin/env python3

"""Debug the order of variables in self.variables to confirm the retrofitting bug."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# Monkey patch _retrofit_expression to show the matching logic
from qnty.problems.composition import CompositionMixin

original_retrofit_expression = CompositionMixin._retrofit_expression

def debug_retrofit_expression(self, expr):
    from qnty.algebra.nodes import VariableReference, Constant, BinaryOperation

    if isinstance(expr, Constant):
        constant_value = expr.value
        print(f"\n=== RETROFIT EXPRESSION DEBUG ===")
        print(f"Processing constant: {constant_value}")

        if hasattr(constant_value, 'value'):
            print(f"Constant value: {constant_value.value} (unit: {getattr(constant_value, 'unit', 'dimensionless')})")
            print(f"Looking for matching variables...")

            # Check all variables for matches
            for symbol, var in self.variables.items():
                if (hasattr(var, 'value') and var.value is not None):
                    # Check dimensional compatibility first
                    if hasattr(var, 'dim') and hasattr(constant_value, 'dim'):
                        if var.dim != constant_value.dim:
                            continue  # Skip if dimensions don't match

                    # Check if values are approximately equal
                    try:
                        if abs(var.value - constant_value.value) < 1e-10:
                            print(f"  MATCH FOUND: {symbol} -> '{var.name}' = {var.value}")
                            print(f"    *** WILL SUBSTITUTE CONSTANT WITH THIS VARIABLE ***")
                            return VariableReference(var)
                        else:
                            print(f"  No match: {symbol} -> '{var.name}' = {var.value} (diff: {abs(var.value - constant_value.value)})")
                    except (TypeError, ValueError):
                        continue
            print("  No matching variables found")

    return original_retrofit_expression(self, expr)

# Apply patch
CompositionMixin._retrofit_expression = debug_retrofit_expression

class RetrofitTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_retrofit():
    print("=== RETROFIT TEST ===")
    print("Creating RetrofitTest instance...")

    problem = RetrofitTest()

    print("RetrofitTest instance created")

    # Show the variables order
    print(f"\nVariables in problem.variables (in iteration order):")
    for i, (symbol, var) in enumerate(problem.variables.items()):
        if hasattr(var, 'name') and hasattr(var, 'value'):
            print(f"  {i}: {symbol} -> '{var.name}' = {var.value}")
            if 'T_bar_r' in symbol or 'header_c' in symbol:
                print(f"      *** TARGET VARIABLE ***")

if __name__ == "__main__":
    test_retrofit()