#!/usr/bin/env python3

"""Debug the canonicalization step that incorrectly replaces T_bar_r with header.c."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# Monkey patch the _canonicalize_expression method with very detailed logging
from qnty.problems.composition import CompositionMixin

original_canonicalize = CompositionMixin._canonicalize_expression

def debug_canonicalize_expression(self, expr):
    from qnty.algebra.nodes import VariableReference

    if isinstance(expr, VariableReference):
        var = expr.variable

        # Only debug variables related to weld throat reinforcement equation
        is_target = (hasattr(var, 'symbol') and
                    ('T_bar_r' in getattr(var, 'symbol', '') or 'header_c' in getattr(var, 'symbol', '') or
                     'reinforcement' in getattr(var, 'name', '').lower() or 'allowances' in getattr(var, 'name', '').lower()))

        if is_target:
            print(f"\n=== CANONICALIZATION DEBUG ===")
            print(f"Processing: '{var.name}' (symbol: {getattr(var, 'symbol', 'NO_SYMBOL')}, ID: {id(var)})")

            if hasattr(var, 'name'):
                # First priority: Check system-level variables
                print("Checking system-level variables for name matches...")
                for attr_name in dir(self):
                    if not attr_name.startswith('_'):
                        attr_value = getattr(self, attr_name, None)
                        if (attr_value and hasattr(attr_value, 'name') and
                            hasattr(attr_value, 'value')):
                            name_match = attr_value.name == var.name
                            if name_match:
                                print(f"  SYSTEM MATCH: {attr_name}")
                                print(f"    Original: '{var.name}' (ID: {id(var)})")
                                print(f"    Match:    '{attr_value.name}' (ID: {id(attr_value)})")
                                if id(var) != id(attr_value):
                                    print(f"    *** SUBSTITUTION! ***")
                                    return VariableReference(attr_value)
                                else:
                                    print(f"    Same object, no substitution")
                                    return expr

                # Check sub-problem attributes
                print("Checking sub-problem attributes for name matches...")
                for attr_name in dir(self):
                    if not attr_name.startswith('_'):
                        attr_value = getattr(self, attr_name, None)
                        if hasattr(attr_value, '__dict__'):
                            for sub_attr_name in dir(attr_value):
                                if not sub_attr_name.startswith('_'):
                                    try:
                                        sub_attr_value = getattr(attr_value, sub_attr_name, None)
                                        if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                            hasattr(sub_attr_value, 'value')):
                                            name_match = sub_attr_value.name == var.name
                                            if name_match:
                                                print(f"  SUB-PROBLEM MATCH: {attr_name}.{sub_attr_name}")
                                                print(f"    Original: '{var.name}' (ID: {id(var)})")
                                                print(f"    Match:    '{sub_attr_value.name}' (ID: {id(sub_attr_value)})")
                                                if id(var) != id(sub_attr_value):
                                                    print(f"    *** SUBSTITUTION! ***")
                                                    return VariableReference(sub_attr_value)
                                                else:
                                                    print(f"    Same object, no substitution")
                                                    return expr
                                    except (AttributeError, TypeError):
                                        continue

                # Second priority: Check self.variables
                print("Checking self.variables for name matches...")
                for symbol, canonical_var in self.variables.items():
                    if hasattr(canonical_var, 'name'):
                        name_match = canonical_var.name == var.name
                        if name_match:
                            print(f"  VARIABLES MATCH: {symbol}")
                            print(f"    Original: '{var.name}' (ID: {id(var)})")
                            print(f"    Match:    '{canonical_var.name}' (ID: {id(canonical_var)})")
                            if id(var) != id(canonical_var):
                                print(f"    *** SUBSTITUTION! ***")
                                return VariableReference(canonical_var)
                            else:
                                print(f"    Same object, no substitution")
                                return expr

                print("No matches found - returning original")

    return original_canonicalize(self, expr)

# Apply the monkey patch
CompositionMixin._canonicalize_expression = debug_canonicalize_expression

class CanonicalizationTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_canonicalization():
    print("=== CANONICALIZATION TEST ===")
    print("Creating CanonicalizationTest instance...")

    problem = CanonicalizationTest()

    print("CanonicalizationTest instance created")

    # Examine the final result
    target_eq = None
    for eq in problem.equations:
        if "Reinforcement" in eq.name:
            target_eq = eq
            break

    if target_eq:
        print(f"\nFinal equation: {target_eq}")

if __name__ == "__main__":
    test_canonicalization()