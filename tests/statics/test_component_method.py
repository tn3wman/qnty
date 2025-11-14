"""
Comprehensive tests for ComponentSolver using problems 2-32 to 2-44 from textbook.

These tests validate the Cartesian/Component method for solving force equilibrium
problems using scalar notation: ΣFx = 0, ΣFy = 0.
"""

import math

import pytest

from qnty.solving.component_solver import ComponentSolver
from qnty.spatial.force_vector import ForceVector

# Problem definitions - single source of truth
COMPONENT_METHOD_PROBLEMS = {
    "problem_2_32": {
        "name": "Problem 2-32",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=200, unit="N",
                angle=-45, wrt="+y",
                name="F_1", description="Force 1 at 45° from +x"
            ),
            "F_2": ForceVector(
                magnitude=-150, unit="N",
                angle=-30, wrt="+x",
                name="F_2", description="Force 2 at 30° from -x"
            ),
            "F_R": ForceVector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 200, "unit": "N",
                "angle": -45, "wrt": "+y"
            },
            "F_2": {
                "magnitude": -150, "unit": "N",
                "angle": -30, "wrt": "+x"
            },
            "F_R": {
                "magnitude": 217, "unit": "N",
                "angle": 87, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_33": {
        "name": "Problem 2-33",
        "description": """
        Determine the magnitude of the resultant force and its direction, measured clockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=400, unit="N",
                angle=30, wrt="+x",
                name="F_1", description="Force 1"
            ),
            "F_2": ForceVector(
                magnitude=800, unit="N",
                angle=45, wrt="-y",
                name="F_2", description="Force 2"
            ),
            "F_R": ForceVector.unknown(
                name="F_R", is_resultant=True, description="Resultant Force"
            )
        },
        "expected": {
            "F_1": {
                "magnitude": 400, "unit": "N",
                "angle": 30, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 800, "unit": "N",
                "angle": 45, "wrt": "-y"
            },
            "F_R": {
                "magnitude": 983, "unit": "N",
                "angle": -21.8, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_40": {
        "name": "Problem 2-40",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        This is actually the same as problem 2-32 but with different labeling.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=150, unit="N",
                angle=30, wrt="-x",
                name="F_1", description="Force 1 at 30° from -x"
            ),
            "F_2": ForceVector(
                magnitude=200, unit="N",
                angle=45, wrt="+x",
                name="F_2", description="Force 2 at 45° from +x"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 150, "unit": "N",
                "angle": 30, "wrt": "-x"
            },
            "F_2": {
                "magnitude": 200, "unit": "N",
                "angle": 45, "wrt": "+x"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_41": {
        "name": "Problem 2-41",
        "description": """
        Determine the magnitude of the resultant force and its direction,
        measured counterclockwise from the positive x axis.
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=4000, unit="N",
                angle=0, wrt="+x",
                name="F_1", description="Force 1 along +x axis (4 kN)"
            ),
            "F_2": ForceVector(
                magnitude=5000, unit="N",
                angle=45, wrt="+x",
                name="F_2", description="Force 2 at 45° from +x (5 kN)"
            ),
            "F_3": ForceVector(
                magnitude=8000, unit="N",
                angle=15, wrt="+y",
                name="F_3", description="Force 3 at 15° from +y toward -x (8 kN)"
            ),
        },
        "expected": {
            "F_1": {
                "magnitude": 4000, "unit": "N",
                "angle": 0, "wrt": "+x"
            },
            "F_2": {
                "magnitude": 5000, "unit": "N",
                "angle": 45, "wrt": "+x"
            },
            "F_3": {
                "magnitude": 8000, "unit": "N",
                "angle": 15, "wrt": "+y"
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
}


# Debug control functions
def enable_debug(problem_name, print_results=True, assert_values=True):
    """Enable debug output for a specific problem."""
    if problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def disable_debug(problem_name):
    """Disable debug output for a specific problem."""
    if problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": False,
            "assert_values": True
        }


def set_debug_all(print_results=True, assert_values=True):
    """Set debug settings for all problems."""
    for problem_name in COMPONENT_METHOD_PROBLEMS:
        COMPONENT_METHOD_PROBLEMS[problem_name]["debug"] = {
            "print_results": print_results,
            "assert_values": assert_values
        }


def solve_component_problem(problem_name):
    """Solve a component method problem and return the solution."""
    spec = COMPONENT_METHOD_PROBLEMS[problem_name]

    # Create solver
    solver = ComponentSolver()

    # Get forces dict
    forces_dict = spec["forces"]

    # Separate known forces from unknown resultant
    known_forces = []
    resultant_name = None
    for force_name, force in forces_dict.items():
        if hasattr(force, 'is_resultant') and force.is_resultant:
            resultant_name = force_name
        else:
            known_forces.append(force)

    # Solve for resultant using only known forces
    resultant = solver.solve_resultant(known_forces, force_unit="N")

    # Get component sums (also only from known forces)
    sum_x, sum_y, _ = solver.sum_components(known_forces)

    # Get solution steps
    steps = solver.get_solution_steps()

    # Update the forces dict with the computed resultant
    if resultant_name:
        forces_dict[resultant_name] = resultant

    return {
        "forces": forces_dict,
        "resultant": resultant,
        "sum_x": sum_x,
        "sum_y": sum_y,
        "steps": steps,
    }


def verify_component_results(solution, expected, debug_config, capsys, test_name):
    """Verify component method results match expected values and optionally print them."""
    print_results = debug_config.get("print_results", False)
    assert_values = debug_config.get("assert_values", True)

    forces_dict = solution["forces"]
    resultant = solution["resultant"]
    sum_x = solution["sum_x"]
    sum_y = solution["sum_y"]
    steps = solution["steps"]

    # Verify individual forces match expected (they should be unchanged)
    for force_name, expected_values in expected.items():
        if force_name not in forces_dict:
            if print_results:
                print(f"Warning: {force_name} not found in solution")
            continue

        force = forces_dict[force_name]
        expected_mag = expected_values["magnitude"]
        expected_ang_deg = expected_values["angle"]
        expected_wrt = expected_values.get("wrt", "+x")

        # Convert magnitude from SI to preferred unit for comparison
        if force.magnitude.preferred:
            actual_mag_in_preferred = force.magnitude.value / force.magnitude.preferred.si_factor
        else:
            actual_mag_in_preferred = force.magnitude.value

        # Create the expected angle reference from wrt
        expected_angle_ref = ForceVector.parse_wrt(expected_wrt, force.coordinate_system)

        # Convert actual angle to the expected wrt system for comparison
        actual_ang_in_wrt = expected_angle_ref.from_standard(force.angle.value, angle_unit="degree")

        # Normalize angles to [0, 360) range for comparison
        actual_ang_in_wrt = actual_ang_in_wrt % 360
        expected_ang_deg_normalized = expected_ang_deg % 360

        # Only assert if enabled for this problem
        if assert_values:
            assert pytest.approx(expected_mag, rel=0.01) == actual_mag_in_preferred, \
                f"{force_name} magnitude: got {actual_mag_in_preferred}, expected {expected_mag}"
            assert pytest.approx(expected_ang_deg_normalized, rel=0.01) == actual_ang_in_wrt, \
                f"{force_name} angle (wrt {expected_wrt}): got {actual_ang_in_wrt}°, expected {expected_ang_deg_normalized}°"

    # Get actual resultant values
    assert resultant.magnitude is not None and resultant.magnitude.value is not None
    assert resultant.angle is not None and resultant.angle.value is not None
    actual_magnitude = resultant.magnitude.value
    actual_angle = math.degrees(resultant.angle.value)

    # Determine unit for display (check first force)
    first_force = next(iter(forces_dict.values()))
    if first_force.magnitude.preferred:
        display_unit = first_force.magnitude.preferred.symbol
    else:
        display_unit = "N"

    # Use values as-is (already in SI units)
    sum_x_display = sum_x
    sum_y_display = sum_y
    actual_magnitude_display = actual_magnitude

    # Print results if enabled
    if print_results:
        with capsys.disabled():
            print(f"\n{test_name} results:")

            # Print individual forces
            for force_name in sorted(forces_dict.keys()):
                force = forces_dict[force_name]

                # Get expected wrt for this force (if specified)
                force_expected = expected.get(force_name, {})
                display_wrt = force_expected.get("wrt", "+x")

                # Create angle reference for display
                display_angle_ref = ForceVector.parse_wrt(display_wrt, force.coordinate_system)

                # Convert angle to display wrt system
                actual_ang_in_wrt = display_angle_ref.from_standard(force.angle.value, angle_unit="degree")
                actual_ang_in_wrt = actual_ang_in_wrt % 360

                # Convert magnitude from SI to preferred unit for display
                if force.magnitude.preferred:
                    mag_value_in_preferred = force.magnitude.value / force.magnitude.preferred.si_factor
                    mag_unit = force.magnitude.preferred.symbol
                else:
                    mag_value_in_preferred = force.magnitude.value
                    mag_unit = "SI"

                # Format wrt for display
                wrt_display = f" wrt {display_wrt}" if display_wrt != "+x" else ""
                print(f"  {force_name}: magnitude={mag_value_in_preferred:.3f} {mag_unit}, angle={actual_ang_in_wrt:.3f}°{wrt_display}")

            # Print component sums and resultant
            print("\n  Component Method Results:")
            print(f"    ΣFx = {sum_x_display:.3f} {display_unit}")
            print(f"    ΣFy = {sum_y_display:.3f} {display_unit}")
            print(f"    FR = {actual_magnitude_display:.3f} {display_unit}")
            print(f"    θ = {actual_angle:.2f}°")

            if steps:
                print("\n  Solution steps:")
                for step in steps:
                    print(f"    {step}")

            # Show assertion status
            if not assert_values:
                print(f"  [NOTE: Assertions disabled for {test_name}]")


# Single parameterized test for all component method problems
@pytest.mark.parametrize("problem_name", list(COMPONENT_METHOD_PROBLEMS.keys()))
def test_component_method_problem(problem_name, capsys):
    """Test all component method problems."""
    problem_spec = COMPONENT_METHOD_PROBLEMS[problem_name]
    solution = solve_component_problem(problem_name)
    expected = problem_spec["expected"]
    debug_config = problem_spec.get("debug", {"print_results": False, "assert_values": True})
    verify_component_results(solution, expected, debug_config, capsys, problem_name)


# Example of how easy it is to add a new problem:
#
# COMPONENT_METHOD_PROBLEMS["problem_2_42"] = {
#     "name": "Problem 2-42",
#     "description": "New problem description...",
#     "forces": {
#         "F_1": ForceVector(
#             magnitude=100, unit="N",
#             angle=30, wrt="+x",
#             name="F_1", description="Force 1"
#         ),
#         "F_2": ForceVector(
#             magnitude=200, unit="N",
#             angle=120, wrt="+x",
#             name="F_2", description="Force 2"
#         ),
#     },
#     "expected": {
#         "F_1": {"magnitude": 100, "angle": 30, "unit": "N", "wrt": "+x"},
#         "F_2": {"magnitude": 200, "angle": 120, "unit": "N", "wrt": "+x"},
#     },
#     "debug": {"print_results": False, "assert_values": True},
# }
# That's it! The test will automatically pick up the new problem.
