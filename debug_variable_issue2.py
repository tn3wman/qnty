#!/usr/bin/env python3
"""
Debug script to demonstrate the exact issue from the composed problem.
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
        self.P = Pressure("Design Pressure").set(90).psi
        self.P._symbol = "P"
        self.variables["P"] = self.P

def create_simple_problem():
    return SimpleProblem()

# Create a composed problem scenario
print("=== Creating composed problem scenario ===")

# System-level variable
P = Pressure("Design Pressure").set(90).psi
P._symbol = "P"
print(f"System P.symbol = {P.symbol!r}")

# Sub-problems with proxy
header = create_simple_problem()
branch = create_simple_problem()

# Create proxy for branch sub-problem
branch_proxy = SubProblemProxy(branch, "branch")
print(f"Created branch proxy")

# Access P through the proxy (this creates a ConfigurableVariable)
branch_P_from_proxy = branch_proxy.P
print(f"branch_P_from_proxy type: {type(branch_P_from_proxy)}")
print(f"branch_P_from_proxy.symbol = {branch_P_from_proxy.symbol!r}")

# Mark branch.P as unknown (like in the composed problem)
branch_P_from_proxy.value = None

# Create the equation: branch.P = P
try:
    print("=== Creating equation ===")
    branch_P_eqn = equation(branch_P_from_proxy, P)
    print(f"Created equation: {branch_P_eqn}")

    # Get variables from equation
    variables_in_equation = branch_P_eqn.variables
    print(f"Variables in equation: {variables_in_equation}")

    # Create the variable_values dict that the solver would have
    variable_values = {
        "P": P,
        "branch_P": branch_P_from_proxy._variable if hasattr(branch_P_from_proxy, '_variable') else branch_P_from_proxy
    }

    print(f"Available variable_values keys: {list(variable_values.keys())}")

    # Check each variable in the equation
    for var_name in variables_in_equation:
        print(f"Checking variable '{var_name}':")
        print(f"  - Is in variable_values: {var_name in variable_values}")
        if var_name in variable_values:
            var_obj = variable_values[var_name]
            print(f"  - Variable object: {var_obj}")
            print(f"  - Variable symbol: {getattr(var_obj, 'symbol', 'NO SYMBOL')}")
            print(f"  - Variable name: {getattr(var_obj, 'name', 'NO NAME')}")
            print(f"  - Variable value: {getattr(var_obj, 'value', 'NO VALUE')}")

    # Try to solve
    print("=== Attempting to solve ===")
    result = branch_P_eqn.solve_for("branch_P", variable_values)
    print(f"Successfully solved: {result}")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()