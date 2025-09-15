#!/usr/bin/env python3

"""Debug by adding logging to the canonicalization process."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# Monkey patch the _canonicalize_expression method to add logging
from qnty.problems.composition import CompositionMixin

original_canonicalize = CompositionMixin._canonicalize_expression

def debug_canonicalize_expression(self, expr):
    from qnty.algebra.nodes import VariableReference

    if isinstance(expr, VariableReference):
        var = expr.variable

        # Special focus on the problematic variable
        is_target_var = 'Thickness, Reinforcement' in var.name or 'Mechanical Allowances' in var.name

        if is_target_var:
            print(f"\n=== CANONICALIZE DEBUG (TARGET VARIABLE) ===")
            print(f"Processing variable: '{var.name}' (ID: {id(var)})")
        elif 'thickness' in var.name.lower() or 'reinforcement' in var.name.lower() or 'allowances' in var.name.lower():
            print(f"\n=== CANONICALIZE DEBUG (RELATED) ===")
            print(f"Processing variable: '{var.name}' (ID: {id(var)})")
        else:
            # Skip logging for unrelated variables
            return original_canonicalize(self, expr)

        if hasattr(var, 'name'):
            # First priority: Check if there's a system-level variable with this name
            print("Checking system-level variables...")
            for attr_name in dir(self):
                if not attr_name.startswith('_'):
                    attr_value = getattr(self, attr_name, None)
                    if (attr_value and hasattr(attr_value, 'name') and
                        hasattr(attr_value, 'value')):
                        name_match = attr_value.name == var.name
                        if name_match:
                            print(f"  SYSTEM MATCH: {attr_name} -> '{attr_value.name}' = {attr_value.value} (ID: {id(attr_value)})")
                            if id(var) != id(attr_value):
                                print(f"    *** SUBSTITUTING: {id(var)} -> {id(attr_value)} ***")
                                return VariableReference(attr_value)
                            else:
                                print(f"    Same object, no substitution")
                                return expr

                    # Also check sub-problem attributes
                    if hasattr(attr_value, '__dict__'):
                        for sub_attr_name in dir(attr_value):
                            if not sub_attr_name.startswith('_'):
                                try:
                                    sub_attr_value = getattr(attr_value, sub_attr_name, None)
                                    if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                        hasattr(sub_attr_value, 'value')):
                                        name_match = sub_attr_value.name == var.name
                                        if name_match:
                                            print(f"  SUB-PROBLEM MATCH: {attr_name}.{sub_attr_name} -> '{sub_attr_value.name}' = {sub_attr_value.value} (ID: {id(sub_attr_value)})")
                                            if id(var) != id(sub_attr_value):
                                                print(f"    *** SUBSTITUTING: {id(var)} -> {id(sub_attr_value)} ***")
                                                return VariableReference(sub_attr_value)
                                            else:
                                                print(f"    Same object, no substitution")
                                                return expr
                                except (AttributeError, TypeError):
                                    continue

    return original_canonicalize(self, expr)

# Apply the monkey patch
CompositionMixin._canonicalize_expression = debug_canonicalize_expression

class DebugReproduction(Problem):
    """Debug version with logging."""

    # Create a sub-problem
    header = create_straight_pipe_internal()

    # Define our own T_bar_r variable
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create the problematic equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_debug_reproduction():
    print("Creating DebugReproduction...")
    problem = DebugReproduction()
    problem.header.c.set(2.5).millimeter
    print("DebugReproduction created.\n")

if __name__ == "__main__":
    test_debug_reproduction()