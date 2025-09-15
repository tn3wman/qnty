#!/usr/bin/env python3

"""Debug DelayedExpression resolution to find where T_bar_r becomes header.c."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# Monkey patch the DelayedExpression._resolve_operand method
from qnty.problems.composition import DelayedExpression

original_resolve_operand = DelayedExpression._resolve_operand

def debug_resolve_operand(self, operand, context):
    print(f"\n=== RESOLVE OPERAND DEBUG ===")
    print(f"Operand type: {type(operand)}")
    if hasattr(operand, 'symbol'):
        print(f"Operand symbol: '{operand.symbol}'")
    if hasattr(operand, 'name'):
        print(f"Operand name: '{operand.name}'")
    print(f"Operand ID: {id(operand)}")

    # Check if it's our target variable
    is_target = (hasattr(operand, 'name') and
                ('Thickness, Reinforcement' in operand.name or 'Mechanical Allowances' in operand.name))

    if is_target:
        print(f"*** TARGET VARIABLE DETECTED ***")

        # Show what's in the context
        if hasattr(operand, 'symbol'):
            symbol = operand.symbol
            print(f"Looking up symbol '{symbol}' in context...")
            if symbol in context:
                context_var = context[symbol]
                print(f"Found in context: '{context_var.name}' (ID: {id(context_var)})")
                if id(context_var) != id(operand):
                    print(f"*** CONTEXT SUBSTITUTION WILL OCCUR ***")
                    print(f"  Original: '{operand.name}' (ID: {id(operand)})")
                    print(f"  Context:  '{context_var.name}' (ID: {id(context_var)})")
            else:
                print(f"Symbol '{symbol}' NOT found in context")

    result = original_resolve_operand(self, operand, context)

    if is_target:
        print(f"Resolution result:")
        if hasattr(result, 'variable'):
            result_var = result.variable
            print(f"  Result variable: '{result_var.name}' (ID: {id(result_var)})")
        elif hasattr(result, 'name'):
            print(f"  Result: '{result.name}' (ID: {id(result)})")
        else:
            print(f"  Result type: {type(result)}")

    return result

# Apply the monkey patch
DelayedExpression._resolve_operand = debug_resolve_operand

class DelayedTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_delayed_resolution():
    print("=== DELAYED RESOLUTION TEST ===")
    print("Creating DelayedTest instance...")

    problem = DelayedTest()

    print("DelayedTest instance created")

    # Now examine the result
    target_eq = None
    for eq in problem.equations:
        if "Reinforcement" in eq.name:
            target_eq = eq
            break

    if target_eq:
        print(f"\nFinal equation: {target_eq}")
        if hasattr(target_eq.rhs, 'right'):
            from qnty.algebra.nodes import VariableReference
            if isinstance(target_eq.rhs.right, VariableReference):
                final_var = target_eq.rhs.right.variable
                print(f"Final variable: '{final_var.name}' (ID: {id(final_var)})")

if __name__ == "__main__":
    test_delayed_resolution()