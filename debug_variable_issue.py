#!/usr/bin/env python3
"""
Debug script to demonstrate the "Variable 'branch_P' not found in equation" issue.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

from qnty import Pressure
from qnty.algebra import equation
from qnty.problems.composition import ConfigurableVariable

# Create test variables
P = Pressure("Design Pressure").set(90).psi
branch_P = Pressure("Branch Pressure")

# Print their properties
print(f"P.symbol = {P.symbol!r}")
print(f"P.name = {P.name!r}")
print(f"branch_P.symbol = {branch_P.symbol!r}")
print(f"branch_P.name = {branch_P.name!r}")

# Create a ConfigurableVariable (like SubProblemProxy does)
configurablevar = ConfigurableVariable(
    symbol="branch_P",
    name="Branch Pressure (Branch)",
    quantity=None,
    is_known=False,
    proxy=None,
    original_symbol="P",
    original_variable=branch_P
)

print(f"configurablevar.symbol = {configurablevar.symbol!r}")
print(f"configurablevar.name = {configurablevar.name!r}")
print(f"configurablevar._variable.symbol = {configurablevar._variable.symbol!r}")
print(f"configurablevar._variable.name = {configurablevar._variable.name!r}")

# Try to create an equation using the problematic pattern from the composed problem
try:
    # This creates an equation: branch_P = P
    branch_P_eqn = equation(configurablevar, P)
    print(f"Created equation: {branch_P_eqn}")

    # Try to get the variables from this equation
    variables = branch_P_eqn.variables
    print(f"Variables in equation: {variables}")

    # Create a simple variable_values dict
    variable_values = {
        "P": P,
        "branch_P": configurablevar._variable  # This is the actual variable that gets stored
    }

    print(f"Available variable_values keys: {list(variable_values.keys())}")

    # Try to solve for branch_P
    result = branch_P_eqn.solve_for("branch_P", variable_values)
    print(f"Successfully solved: {result}")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()