#!/usr/bin/env python3

"""Debug all equation processing steps to find where T_bar_r becomes header.c."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

# Monkey patch ALL the equation processing methods
from qnty.problems.composition import CompositionMixin

# 1. Patch _fix_equation_variable_references
original_fix_equation_references = CompositionMixin._fix_equation_variable_references

def debug_fix_equation_references(self, equation):
    print(f"\n=== FIX_EQUATION_VARIABLE_REFERENCES ===")
    print(f"Input equation: {equation}")

    result = original_fix_equation_references(self, equation)

    print(f"Output equation: {result}")
    if str(equation) != str(result):
        print("*** EQUATION CHANGED ***")

    return result

# 2. Patch _canonicalize_expression
original_canonicalize = CompositionMixin._canonicalize_expression

def debug_canonicalize_expression(self, expr):
    from qnty.algebra.nodes import VariableReference

    result = original_canonicalize(self, expr)

    # Only log if there's a change and it's relevant to our issue
    if expr != result and isinstance(expr, VariableReference) and isinstance(result, VariableReference):
        original_var = expr.variable
        new_var = result.variable

        is_relevant = (
            ('thickness' in getattr(original_var, 'name', '').lower() or
             'reinforcement' in getattr(original_var, 'name', '').lower() or
             'allowances' in getattr(original_var, 'name', '').lower()) or
            ('thickness' in getattr(new_var, 'name', '').lower() or
             'reinforcement' in getattr(new_var, 'name', '').lower() or
             'allowances' in getattr(new_var, 'name', '').lower())
        )

        if is_relevant:
            print(f"\n=== CANONICALIZE_EXPRESSION CHANGE ===")
            print(f"Original: '{original_var.name}' (symbol: {getattr(original_var, 'symbol', 'NO_SYMBOL')}, ID: {id(original_var)})")
            print(f"New:      '{new_var.name}' (symbol: {getattr(new_var, 'symbol', 'NO_SYMBOL')}, ID: {id(new_var)})")
            print("*** VARIABLE SUBSTITUTION ***")

    return result

# 3. Patch _canonicalize_all_equation_variables
original_canonicalize_all = CompositionMixin._canonicalize_all_equation_variables

def debug_canonicalize_all_equation_variables(self):
    print(f"\n=== CANONICALIZE_ALL_EQUATION_VARIABLES START ===")

    # Print equations before
    print("Equations BEFORE canonicalization:")
    for i, eq in enumerate(self.equations):
        if 'reinforcement' in eq.name.lower() or 'throat' in eq.name.lower():
            print(f"  {i}: {eq}")

    result = original_canonicalize_all(self)

    # Print equations after
    print("Equations AFTER canonicalization:")
    for i, eq in enumerate(self.equations):
        if 'reinforcement' in eq.name.lower() or 'throat' in eq.name.lower():
            print(f"  {i}: {eq}")

    print("=== CANONICALIZE_ALL_EQUATION_VARIABLES END ===")
    return result

# 4. Patch _retrofit_constants_to_variables
original_retrofit = CompositionMixin._retrofit_constants_to_variables

def debug_retrofit_constants_to_variables(self):
    print(f"\n=== RETROFIT_CONSTANTS_TO_VARIABLES START ===")

    # Print equations before
    print("Equations BEFORE retrofitting:")
    for i, eq in enumerate(self.equations):
        if 'reinforcement' in eq.name.lower() or 'throat' in eq.name.lower():
            print(f"  {i}: {eq}")

    result = original_retrofit(self)

    # Print equations after
    print("Equations AFTER retrofitting:")
    for i, eq in enumerate(self.equations):
        if 'reinforcement' in eq.name.lower() or 'throat' in eq.name.lower():
            print(f"  {i}: {eq}")

    print("=== RETROFIT_CONSTANTS_TO_VARIABLES END ===")
    return result

# Apply all patches
CompositionMixin._fix_equation_variable_references = debug_fix_equation_references
CompositionMixin._canonicalize_expression = debug_canonicalize_expression
CompositionMixin._canonicalize_all_equation_variables = debug_canonicalize_all_equation_variables
CompositionMixin._retrofit_constants_to_variables = debug_retrofit_constants_to_variables

class AllProcessingTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_all_processing():
    print("=== ALL EQUATION PROCESSING TEST ===")
    print("Creating AllProcessingTest instance...")

    problem = AllProcessingTest()

    print("AllProcessingTest instance created")

    # Examine the final result
    target_eq = None
    for eq in problem.equations:
        if "Reinforcement" in eq.name:
            target_eq = eq
            break

    if target_eq:
        print(f"\nFinal result: {target_eq}")

if __name__ == "__main__":
    test_all_processing()