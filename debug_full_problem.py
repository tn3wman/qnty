#!/usr/bin/env python3
"""
Debug script using the actual Problem class to reproduce the issue.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

from qnty import Pressure, Problem
from qnty.algebra import equation

class StraightPipeInternal(Problem):
    name = "Simple Pipe Problem"
    description = "Simple test problem"

    P = Pressure("Design Pressure").set(90).psi

def create_straight_pipe_internal():
    return StraightPipeInternal()

class WeldedBranchConnection(Problem):
    """Composed problem that reproduces the issue."""

    name = "Composed Branch Connection Analysis"
    description = "Test composed problem"

    # System-level variable
    P = Pressure("Design Pressure").set(90).psi

    # Sub-problems
    header = create_straight_pipe_internal()
    branch = create_straight_pipe_internal()

    # Mark branch.P as unknown and share system pressure
    header.P.value = None
    branch.P.value = None
    header_P_eqn = equation(header.P, P)
    branch_P_eqn = equation(branch.P, P)

def test_composed_problem():
    """Test the composed problem to reproduce the issue."""
    print("=== Creating composed problem ===")
    problem = WeldedBranchConnection()

    print(f"Problem variables: {list(problem.variables.keys())}")
    print(f"Problem equations: {len(problem.equations)}")

    # Look at the problematic equation
    branch_P_eqn = None
    for eq in problem.equations:
        if "branch_P" in str(eq):
            branch_P_eqn = eq
            break

    if branch_P_eqn:
        print(f"Found branch_P equation: {branch_P_eqn}")
        print(f"Equation variables: {branch_P_eqn.variables}")
        print(f"Equation name: {branch_P_eqn.name}")

        # Check if the variable exists in problem.variables
        for var_name in branch_P_eqn.variables:
            print(f"Variable '{var_name}' in problem.variables: {var_name in problem.variables}")
            if var_name in problem.variables:
                var_obj = problem.variables[var_name]
                print(f"  Variable object: {var_obj}")
                print(f"  Variable symbol: {var_obj.symbol}")
                print(f"  Variable value: {var_obj.value}")

    print("=== Attempting to solve ===")
    try:
        problem.solve()
        print(f"SUCCESS: Problem is_solved = {problem.is_solved}")
    except Exception as e:
        print(f"ERROR during solve: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_composed_problem()