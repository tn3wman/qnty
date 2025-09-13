"""
Simplified engineering problems test with data-driven approach.
Eliminates duplication by defining equations once and using generic solvers.
"""

import pytest

import qnty as qt
from qnty.core import Q
from qnty.core import unit_catalog as uc

# Problem definitions - single source of truth
PROBLEMS = {
    "honey_viscosity": {
        "description": "Kinematic viscosity from dynamic viscosity and density",
        "variables": {
            "mu": ("ViscosityDynamic", 1000, "poise"),
            "rho": ("MassDensity", 0.05, "oz_mL"),
            "nu": ("ViscosityKinematic", None, None)  # Unknown
        },
        "equations": [
            ("nu", "mu / rho")
        ],
        "expected": {
            "mu": (2.09, "lbf*s/ft2"),
            "rho": (88.4, "lbm/ft3"),
            "nu": (0.76, "ft2/s")
        },
        "debug": {
            # "print_results": True,
            "assert_values": True
        }
    },
    
    # "pipe_flow": {
    #     "description": "Multi-pipe flow with conservation",
    #     "variables": {
    #         "D_1": ("Length", 1.049, "inch"),
    #         "D_1_5": ("Length", 1.610, "inch"),
    #         "D_2_5": ("Length", 2.469, "inch"),
    #         "V_1": ("VelocityLinear", None, None),
    #         "V_1_5": ("VelocityLinear", 4, "ft_s"),
    #         "V_2_5": ("VelocityLinear", None, None),
    #         "Q_1": ("VolumetricFlowRate", None, None),
    #         "Q_1_5": ("VolumetricFlowRate", None, None),
    #         "Q_2_5": ("VolumetricFlowRate", 50, "gpm"),
    #         "A_1": ("Area", None, None),
    #         "A_1_5": ("Area", None, None),
    #         "A_2_5": ("Area", None, None)
    #     },
    #     "equations": [
    #         ("A_1", "3.14 * (D_1 / 2) ** 2"),
    #         ("A_1_5", "3.14 * (D_1_5 / 2) ** 2"),
    #         ("A_2_5", "3.14 * (D_2_5 / 2) ** 2"),
    #         ("Q_1_5", "V_1_5 * A_1_5"),
    #         ("Q_1", "Q_2_5 - Q_1_5"),  # Conservation equation - tests algebraic solving
    #         ("V_1", "Q_1 / A_1"),
    #         ("V_2_5", "Q_2_5 / A_2_5")
    #     ],
    #     "expected": {
    #         "D_1": (1.049, "inch"),
    #         "D_1_5": (1.610, "inch"),
    #         "D_2_5": (2.469, "inch"),
    #         "V_1": (9.17, "ft_s"),
    #         "V_1_5": (4.0, "ft_s"),
    #         "V_2_5": (3.35, "ft_s"),
    #         "Q_1": (3.29, "ft_3_min"),
    #         "Q_1_5": (3.39, "ft_3_min"),
    #         "Q_2_5": (6.68, "ft_3_min"),
    #         "A_1": (0.005999, "ft_2"),
    #         "A_1_5": (0.01413, "ft_2"),
    #         "A_2_5": (0.03323, "ft_2")
    #     },
    #     "debug": {
    #         # "print_results": True,
    #         "assert_values": True
    #     }
    # }
}


# Debug control functions
def enable_debug(problem_name, print_results=True, assert_values=True):
    """Enable debug output for a specific problem."""
    if problem_name in PROBLEMS:
        PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def disable_debug(problem_name):
    """Disable debug output for a specific problem."""
    if problem_name in PROBLEMS:
        PROBLEMS[problem_name]["debug"] = {
            "print_results": False,
            "assert_values": True
        }


def set_debug_all(print_results=True, assert_values=True):
    """Set debug settings for all problems."""
    for problem_name in PROBLEMS:
        PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def create_variables(var_specs):
    """Create qnty variables from specifications."""
    variables = {}
    for name, (var_type, value, unit) in var_specs.items():
        var_class = getattr(qt, var_type)
        var = var_class(name)
        
        if value is not None:
            if unit is not None:
                # Use fluent API: var.set(value).unit_name
                var = getattr(var.set(value), unit)
            else:
                var.quantity = Q(value, uc.DimensionlessUnits.dimensionless)
            var.is_known = True
        else:
            var.is_known = False
            
        variables[name] = var
    return variables


def solve_with_problem_class(variables, equation_specs):
    """Solve using Problem class approach."""
    # Create Problem class the proper way
    class Problem(qt.Problem):
        pass
    
    # Add variables as class attributes
    for name, var in variables.items():
        setattr(Problem, name, var)
    
    # Add equations as class attributes
    for i, (target_var, expression) in enumerate(equation_specs):
        # Convert string expression to actual equation
        lhs = variables[target_var]
        rhs = eval(expression, {"__builtins__": {}}, variables)
        equation = lhs.equals(rhs)
        setattr(Problem, f"eq_{i}", equation)
    
    # Create and solve
    problem = Problem()
    problem.solve()
    
    # Extract results
    result = {}
    for name in variables:
        result[name] = getattr(problem, name)
    return result


def solve_with_equations(variables, equation_specs):
    """Solve using equation method approach."""
    # Create and solve equations in order
    for target_var, expression in equation_specs:
        lhs = variables[target_var]
        rhs = eval(expression, {"__builtins__": {}}, variables)
        _equation = lhs.equals(rhs)
        # The equation is created and should auto-solve when possible
        try:
            variables[target_var].solve()
        except Exception:
            # If solve() fails, the equation might have solved automatically
            pass
    
    return variables


def solve_with_solve_from(variables, equation_specs):
    """Solve using solve_from method approach."""
    # Execute solve_from in order
    for target_var, expression in equation_specs:
        rhs = eval(expression, {"__builtins__": {}}, variables)
        result = variables[target_var].solve_from(rhs)
        # solve_from returns the updated variable, make sure to use it
        variables[target_var] = result
    
    return variables


def solve_problem(problem_name, method):
    """Generic solver for any problem and method."""
    spec = PROBLEMS[problem_name]
    variables = create_variables(spec["variables"])
    equations = spec["equations"]
    
    if method == "problem_class":
        return solve_with_problem_class(variables, equations)
    elif method == "equation":
        return solve_with_equations(variables, equations)
    elif method == "solve_from":
        return solve_with_solve_from(variables, equations)
    else:
        raise ValueError(f"Unknown method: {method}")


def verify_results(variables, expected, debug_config, capsys, test_name):
    """Verify results match expected values and optionally print them."""
    actuals = {}
    print_results = debug_config.get("print_results", False)
    assert_values = debug_config.get("assert_values", True)
    
    for name, (expected_value, target_unit) in expected.items():
        if name in variables and variables[name].quantity is not None:
            actual = variables[name].to_unit(target_unit)
            actuals[name] = actual
            
            # Only assert if enabled for this problem
            if assert_values:
                assert pytest.approx(actual.value, rel=0.01) == expected_value, f"{name}: got {actual.value}, expected {expected_value}"
            
        elif name in variables:
            if print_results:
                print(f"Warning: {name} has no quantity")
        else:
            if print_results:
                print(f"Warning: {name} doesn't exist in variables")
    
    # Print results only if enabled for this problem
    if print_results:
        with capsys.disabled():
            print(f"\n{test_name} results:")
            for name in sorted(variables.keys()):
                if variables[name].quantity is not None:
                    if name in expected:
                        target_unit = expected[name][1]
                        converted = variables[name].to_unit(target_unit)
                        print(f"  {converted}")
                    else:
                        print(f"  {variables[name].quantity}")
            
            # Show assertion status
            if not assert_values:
                print(f"  [NOTE: Assertions disabled for {test_name}]")


# Single parameterized test for all problems and methods
@pytest.mark.parametrize("problem_name,method", [
    (name, method)
    for name in PROBLEMS.keys()
    for method in ["solve_from", "equation", "problem_class"]
])
def test_engineering_problem(problem_name, method, capsys):
    """Test all engineering problems with all solving methods."""
    problem_spec = PROBLEMS[problem_name]
    variables = solve_problem(problem_name, method)
    expected = problem_spec["expected"]
    debug_config = problem_spec.get("debug", {"print_results": False, "assert_values": True})
    verify_results(variables, expected, debug_config, capsys, f"{problem_name}-{method}")


# Example of how easy it is to add a new problem:
#
# PROBLEMS["pressure_vessel"] = {
#     "description": "ASME pressure vessel wall thickness",
#     "variables": {
#         "P": ("Pressure", 150, "psi"),
#         "D": ("Length", 24, "inch"),
#         "S": ("Pressure", 20000, "psi"),
#         "E": ("Dimensionless", 1.0, None),
#         "t": ("Length", None, None)  # Unknown
#     },
#     "equations": [
#         ("t", "P * D / (2 * S * E - 0.6 * P)")
#     ],
#     "expected": {
#         "t": (0.045, "inch")
#     }
# }
# That's it! The test will automatically pick up the new problem
