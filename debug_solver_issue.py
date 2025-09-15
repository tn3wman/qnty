#!/usr/bin/env python3
"""
Debug script to reproduce the exact solver issue in composed problems.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

from qnty import Pressure
from qnty.algebra import equation
from qnty.problems.composition import ConfigurableVariable, SubProblemProxy

class SimpleProblem:
    """Mock problem class like StraightPipeInternal"""
    def __init__(self):
        self.variables = {}
        self.equations = []
        self.P = Pressure("Design Pressure")
        self.P._symbol = "P"
        self.variables["P"] = self.P

def create_simple_problem():
    return SimpleProblem()

print("=== Reproducing the exact solver issue ===")

# Create composed problem scenario exactly like in the test
P = Pressure("Design Pressure").set(90).psi
P._symbol = "P"

# Create sub-problem and proxy
branch = create_simple_problem()
branch_proxy = SubProblemProxy(branch, "branch")

# Get the proxied variable and mark as unknown
branch_P = branch_proxy.P
branch_P.value = None  # Mark as unknown

print(f"branch_P type: {type(branch_P)}")
print(f"branch_P.symbol: {branch_P.symbol}")
print(f"branch_P._variable.symbol: {branch_P._variable.symbol}")
print(f"branch_P.name: {branch_P.name}")

# Create equation: branch_P = P
branch_P_eqn = equation(branch_P, P)
print(f"Created equation: {branch_P_eqn}")

# Check what variables the equation thinks it has
variables_in_equation = branch_P_eqn.variables
print(f"Variables in equation: {variables_in_equation}")

# This is the key issue: the solver creates working_vars with the wrong key structure
# Let's simulate what the solver does
working_vars = {
    "P": P,
    "branch_P": branch_P._variable  # The solver stores the actual variable, not the proxy
}

print(f"Working vars keys: {list(working_vars.keys())}")

# Now let's trace through what happens in VariableReference.get_variables()
print(f"=== Debugging VariableReference ===")
from qnty.algebra.nodes import VariableReference

# Check the LHS of the equation (should be a VariableReference)
lhs = branch_P_eqn.lhs
print(f"LHS type: {type(lhs)}")
if isinstance(lhs, VariableReference):
    print(f"LHS.variable: {lhs.variable}")
    print(f"LHS.variable.symbol: {lhs.variable.symbol}")
    print(f"LHS.name: {lhs.name}")
    print(f"LHS.get_variables(): {lhs.get_variables()}")

# Now let's see what happens when we call solve_for
print(f"=== Testing solve_for ===")
try:
    # This should fail with "Variable 'branch_P' not found in equation"
    result = branch_P_eqn.solve_for("branch_P", working_vars)
    print(f"SUCCESS: {result}")
except Exception as e:
    print(f"ERROR: {e}")

    # Let's debug the issue further
    print(f"=== Debugging the issue ===")
    print(f"Target var 'branch_P' in equation.variables? {'branch_P' in branch_P_eqn.variables}")
    print(f"Equation variables: {branch_P_eqn.variables}")

    # Check what name the VariableReference is actually using
    if isinstance(lhs, VariableReference):
        actual_name = lhs.name
        print(f"VariableReference.name returns: {actual_name!r}")
        print(f"This name in equation.variables? {actual_name in branch_P_eqn.variables}")
        print(f"This name in working_vars? {actual_name in working_vars}")