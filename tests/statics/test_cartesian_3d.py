"""
Comprehensive tests for 3D Cartesian vector problems using problems 2-60 to 2-85 from textbook.

These tests validate the 3D vector operations including:
- Coordinate direction angles (α, β, γ)
- Direction cosines (cos α, cos β, cos γ)
- Transverse and azimuth angles (φ, θ)
- 3D component resolution and resultant calculation
"""

import math

import pytest

from qnty.solving.component_solver import ComponentSolver
from qnty.spatial.force_vector import ForceVector

# Problem definitions - single source of truth
CARTESIAN_3D_PROBLEMS = {
    "problem_2_60": {
        "name": "Problem 2-60",
        "description": """
        The force F has a magnitude of 80 lb and acts within the octant shown.
        Determine the magnitudes of the x, y, z components of F.
        Given: F = 80 lb, α = 60°, β = 45°
        Find: Fx, Fy, Fz (and γ)
        """,
        "forces": {
            "F": ForceVector(
                magnitude=80,
                unit="lbf",
                alpha=60,
                beta=45,  # γ will be calculated from constraint
                name="F",
                description="Force F",
            ),
        },
        "expected": {
            "F": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 40.0,
                "y": 56.6,
                "z": 40.0,  # Components
                "alpha": 60.0,
                "beta": 45.0,
                "gamma": 60.0,  # Direction angles
            },
        },
        "debug": {"print_results": False, "assert_values": True},
    },
    "problem_2_61": {
        "name": "Problem 2-61",
        "description": """
        The bolt is subjected to the force F, which has components acting along the x, y, z axes as shown.
        If the magnitude of F is 80 N, and α=60° and γ=45°, determine the magnitudes of its components.

        Note: β = 120° means the y-component is negative (cos(120°) = -0.5)
        But the textbook asks for MAGNITUDES which are always positive.
        We construct using x,y,z components to get the right direction.
        """,
        "forces": {
            "F": ForceVector(
                # Fx = 80 cos(60°) = 40
                # Fy = 80 cos(120°) = -40  (negative!)
                # Fz = 80 cos(45°) = 56.57
                x=40.0,
                y=-40.0,
                z=56.57,
                unit="N",
                name="F",
                description="Force F on bolt",
            ),
        },
        "expected": {
            "F": {
                "magnitude": 80,
                "unit": "N",
                "x": 40.0,
                "y": -40.0,
                "z": 56.6,  # Actual signed components
                "alpha": 60.0,
                "beta": 120.0,
                "gamma": 45.0,  # Direction angles
            },
        },
        "debug": {"print_results": False, "assert_values": True},
    },
    "problem_2_63": {
        "name": "Problem 2-63",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force.
        F1 = 80 lb at angles defining components, F2 = 130 lb in -z direction

        Note: F1 is given using transverse/azimuth angles: φ=30°, θ=-40° from +x in x-y plane
        """,
        "forces": {
            "F_1": ForceVector(
                magnitude=80,
                unit="lbf",
                # Using phi (transverse from z) and theta (azimuth in x-y)
                # From textbook: F1 = 80 cos(30°) cos(40°) i - 80 cos(30°) sin(40°) j + 80 sin(30°) k
                # This means φ = 90° - 30° = 60° from +z, and θ = -40° in x-y plane (4th quadrant)
                phi=60,
                theta=-40,  # φ from +z axis down, θ in x-y plane (negative = clockwise from +x)
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(x=0, y=0, z=-130, unit="lbf", name="F_2", description="Force F2 in -z direction"),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "magnitude": 80,
                "unit": "lbf",
                "x": 53.1,
                "y": -44.5,
                "z": 40.0,  # From textbook solution
            },
            "F_2": {
                "x": 0,
                "y": 0,
                "z": -130,
            },
            "F_R": {
                "magnitude": 114,
                "unit": "lbf",  # Actually 113.6
                "x": 53.1,
                "y": -44.5,
                "z": -90.0,
                "alpha": 62.1,
                "beta": 113.0,
                "gamma": 142.0,  # Direction angles
            },
        },
        "debug": {"print_results": False, "assert_values": True},
    },
    "problem_2_65": {
        "name": "Problem 2-65",
        "description": """
        The screw eye is subjected to two forces.
        Express each force in Cartesian vector form and then determine the resultant force.
        Find the magnitude and coordinate direction angles of the resultant force.

        F1 = 300 N, F2 = 500 N with specified direction angles
        """,
        "forces": {
            "F_1": ForceVector(
                # From solution: F1 = {-106.07i + 106.07j + 259.81k} N
                # This gives α, β, γ that produce these components
                x=-106.07,
                y=106.07,
                z=259.81,
                unit="N",
                name="F_1",
                description="Force F1",
            ),
            "F_2": ForceVector(
                magnitude=500,
                unit="N",
                alpha=60,
                beta=45,
                gamma=120,  # Given in problem
                name="F_2",
                description="Force F2",
            ),
            "F_R": ForceVector.unknown(name="F_R", is_resultant=True, description="Resultant Force"),
        },
        "expected": {
            "F_1": {
                "x": -106.0,
                "y": 106.0,
                "z": 260.0,  # Rounded
            },
            "F_2": {
                "magnitude": 500,
                "unit": "N",
                "x": 250.0,
                "y": 353.6,
                "z": -250.0,  # cos(60°)=0.5, cos(45°)=0.707, cos(120°)=-0.5
            },
            "F_R": {
                "magnitude": 482,
                "unit": "N",  # Actually 481.73
                "x": 144.0,
                "y": 460.0,
                "z": 9.81,
                "alpha": 72.6,
                "beta": 17.4,
                "gamma": 88.8,  # Direction angles
            },
        },
        "debug": {"print_results": False, "assert_values": True},
    },
}


def assert_force_magnitude(force: ForceVector, expected_mag: float, tolerance: float = 0.5):
    """Assert force magnitude matches expected value."""
    assert force.magnitude is not None, f"Force {force.name} magnitude is None"
    assert force.magnitude.value is not None, f"Force {force.name} magnitude value is None"

    # Convert to display unit for comparison
    actual_mag = force.magnitude.value / force.magnitude.preferred.si_factor

    assert abs(actual_mag - expected_mag) < tolerance, f"Force {force.name} magnitude: expected {expected_mag}, got {actual_mag:.3f}"


def assert_force_component(component: float | None, expected: float, comp_name: str, force_name: str, tolerance: float = 0.5):
    """Assert force component matches expected value."""
    assert component is not None, f"Force {force_name} component {comp_name} is None"
    assert abs(component - expected) < tolerance, f"Force {force_name} {comp_name}: expected {expected}, got {component:.3f}"


def assert_direction_angle(angle_qty, expected_deg: float, angle_name: str, force_name: str, tolerance: float = 0.5):
    """Assert direction angle matches expected value in degrees."""
    assert angle_qty is not None, f"Force {force_name} angle {angle_name} is None"
    assert angle_qty.value is not None, f"Force {force_name} angle {angle_name} value is None"

    # Convert to degrees for comparison
    actual_deg = math.degrees(angle_qty.value)

    assert abs(actual_deg - expected_deg) < tolerance, f"Force {force_name} {angle_name}: expected {expected_deg}°, got {actual_deg:.1f}°"


@pytest.mark.parametrize("problem_key", list(CARTESIAN_3D_PROBLEMS.keys()))
def test_cartesian_3d_problem(problem_key):
    """Test 3D Cartesian vector problems."""
    problem = CARTESIAN_3D_PROBLEMS[problem_key]

    if problem["debug"]["print_results"]:
        print(f"\n{'=' * 80}")
        print(f"Testing: {problem['name']}")
        print(f"{'=' * 80}")
        print(problem["description"])

    # Extract forces
    forces = problem["forces"]
    expected = problem["expected"]

    # Create solver
    solver = ComponentSolver()

    # Check if this is a resultant problem
    has_unknown_resultant = any(f.is_resultant and not f.is_known for f in forces.values())

    if has_unknown_resultant:
        # Solve for resultant
        result = solver.solve(list(forces.values()))

        if problem["debug"]["print_results"]:
            print("\n--- Solution Steps ---")
            for step in solver.get_solution_steps():
                if "description" in step:
                    print(f"\n{step['description']}")
                if "equations" in step:
                    for eq in step["equations"]:
                        print(f"  {eq}")
                if "components" in step:
                    for comp in step["components"]:
                        print(f"  {comp}")

        # Verify results
        if problem["debug"]["assert_values"]:
            for force_name, expected_values in expected.items():
                solved_force = result[force_name]

                if problem["debug"]["print_results"]:
                    print(f"\n--- Verification: {force_name} ---")

                # Check magnitude if specified
                if "magnitude" in expected_values:
                    assert_force_magnitude(solved_force, expected_values["magnitude"])
                    if problem["debug"]["print_results"]:
                        mag_val = solved_force.magnitude.value / solved_force.magnitude.preferred.si_factor
                        print(f"  Magnitude: {mag_val:.3f} {expected_values.get('unit', 'N')} ✓")

                # Check components if specified
                if "x" in expected_values:
                    x_val = solved_force.x.value / solved_force.x.preferred.si_factor if solved_force.x else None
                    assert_force_component(x_val, expected_values["x"], "x", force_name)
                    if problem["debug"]["print_results"]:
                        print(f"  Fx: {x_val:.3f} {expected_values.get('unit', 'N')} ✓")

                if "y" in expected_values:
                    y_val = solved_force.y.value / solved_force.y.preferred.si_factor if solved_force.y else None
                    assert_force_component(y_val, expected_values["y"], "y", force_name)
                    if problem["debug"]["print_results"]:
                        print(f"  Fy: {y_val:.3f} {expected_values.get('unit', 'N')} ✓")

                if "z" in expected_values:
                    z_val = solved_force.z.value / solved_force.z.preferred.si_factor if solved_force.z else None
                    assert_force_component(z_val, expected_values["z"], "z", force_name)
                    if problem["debug"]["print_results"]:
                        print(f"  Fz: {z_val:.3f} {expected_values.get('unit', 'N')} ✓")

                # Check direction angles if specified
                if "alpha" in expected_values:
                    assert_direction_angle(solved_force.alpha, expected_values["alpha"], "α", force_name, tolerance=1.0)
                    if problem["debug"]["print_results"] and solved_force.alpha:
                        print(f"  α: {math.degrees(solved_force.alpha.value):.1f}° ✓")

                if "beta" in expected_values:
                    assert_direction_angle(solved_force.beta, expected_values["beta"], "β", force_name, tolerance=1.0)
                    if problem["debug"]["print_results"] and solved_force.beta:
                        print(f"  β: {math.degrees(solved_force.beta.value):.1f}° ✓")

                if "gamma" in expected_values:
                    assert_direction_angle(solved_force.gamma, expected_values["gamma"], "γ", force_name, tolerance=1.0)
                    if problem["debug"]["print_results"] and solved_force.gamma:
                        print(f"  γ: {math.degrees(solved_force.gamma.value):.1f}° ✓")

    else:
        # Just verify given forces have correct components
        if problem["debug"]["assert_values"]:
            for force_name, force in forces.items():
                if force_name in expected:
                    expected_values = expected[force_name]

                    if "x" in expected_values and force.x:
                        x_val = force.x.value / force.x.preferred.si_factor
                        assert_force_component(x_val, expected_values["x"], "x", force_name)

                    if "y" in expected_values and force.y:
                        y_val = force.y.value / force.y.preferred.si_factor
                        assert_force_component(y_val, expected_values["y"], "y", force_name)

                    if "z" in expected_values and force.z:
                        z_val = force.z.value / force.z.preferred.si_factor
                        assert_force_component(z_val, expected_values["z"], "z", force_name)

                    if "alpha" in expected_values and force.alpha:
                        assert_direction_angle(force.alpha, expected_values["alpha"], "α", force_name)

                    if "beta" in expected_values and force.beta:
                        assert_direction_angle(force.beta, expected_values["beta"], "β", force_name)

                    if "gamma" in expected_values and force.gamma:
                        assert_direction_angle(force.gamma, expected_values["gamma"], "γ", force_name)


if __name__ == "__main__":
    # Run tests with detailed output
    for problem_key in CARTESIAN_3D_PROBLEMS.keys():
        problem = CARTESIAN_3D_PROBLEMS[problem_key]
        problem["debug"]["print_results"] = True
        test_cartesian_3d_problem(problem_key)
        problem["debug"]["print_results"] = False
