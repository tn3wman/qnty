"""
Comprehensive tests for position vectors and forces along lines using problems 2-86 to 2-105 from textbook.

These tests validate:
- Position vector creation from points
- Unit vector computation (direction cosines)
- Force directed along a line (F = |F| * �)
- Coordinate direction angles (�, �, �)
- Resultant force calculation
"""

import math

import pytest

from qnty.core.quantity import Q
from qnty.core.quantity_catalog import Force
from qnty.problems.position_vector import PositionVectorProblem
from qnty.spatial.force_vector import ForceVector
from qnty.spatial.point import Point
from qnty.spatial.point_cartesian import PointCartesian
from qnty.spatial.point_direction_ratios import PointDirectionRatios
from qnty.spatial.point_polar import PointPolar
from qnty.spatial.point_spherical import PointSpherical
from qnty.spatial.position_vector import PositionVector

# Problem definitions - single source of truth
POSITION_VECTOR_PROBLEMS = {
    "problem_2_86": {
        "name": "Problem 2-86",
        "description": """
        Determine the length of the connecting rod AB by first formulating a Cartesian position vector from A to B and then determining its magnitude.
        """,
        "points": {
            # Point A: 150mm from origin at 210° from +x (or 30° below -x axis)
            "A": PointPolar(dist=150, angle=30, plane="xy", wrt="-x", unit="mm"),
            # Point B: on y-axis at 300mm
            "B": PointCartesian(y=300, unit="mm"),
        },
        "position_vectors": {
            "r_AB": {
                "from": "A",
                "to": "B",
            },
        },
        "expected": {
            "r_AB": {
                "magnitude": 397,
                "x": 129.90,
                "y": 375,
                "z": 0,
                "unit": "mm",
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_87": {
        "name": "Problem 2-87",
        "description": """
        Express force F as a Cartesian vector; then determine its coordinate direction angles.
        """,
        "points": {
            # A at origin (top of structure)
            "A": PointSpherical(
                dist=10, unit="ft",
                theta=30, theta_wrt="+y",
                phi=70, phi_wrt="xy"
            ),
            "B": PointCartesian(x=5, y=-7, unit="ft"),
        },
        "position_vectors": {
            "r_AB": {
                "from": "A",
                "to": "B",
            },
        },
        "forces": {
            "F": {
                "from": "A",
                "to": "B",
                "magnitude": 135,
                "unit": "lbf",
            },
        },
        "expected": {
            "r_AB": {
                "magnitude": 15.25,
                "unit": "ft",
                "x": 6.710,
                "y": -9.962,
                "z": -9.397,
            },
            "F": {
                "magnitude": 135,
                "unit": "lbf",
                "x": 59.4,
                "y": -88.2,
                "z": -83.2,
                "alpha": 63.9,
                "beta": 131,
                "gamma": 128,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_88": {
        "name": "Problem 2-88",
        "description": """
        Express each of the forces in Cartesian vector form and determine the magnitude and coordinate direction angles of the resultant force.
        """,
        "points": {
            # A at origin (top of structure)
            "A": PointCartesian(x=0, y=4, z=0, unit="ft"),
            "B": PointCartesian(x=2, z=-6, unit="ft"),
            "C": PointDirectionRatios(
                dist=2.5, unit="ft", ratio_component="x",
                x=-5, y=0, z=12
            ),
        },
        "position_vectors": {
            "r_AC": {
                "from": "A",
                "to": "C",
            },
            "r_AB": {
                "from": "A",
                "to": "B",
            },
        },
        "forces": {
            "F_1": {
                "from": "A",
                "to": "C",
                "magnitude": 80,
                "unit": "lbf",
            },
            "F_2": {
                "from": "A",
                "to": "B",
                "magnitude": 50,
                "unit": "lbf",
            },
            "F_R": ForceVector.unknown(
                name="F_R",
                unit="lbf",
                is_resultant=True,
            )
        },
        "expected": {
            "r_AC": {
                "unit": "ft",
                "x": -2.5,
                "y": -4,
                "z": 6,
            },
            "r_AB": {
                "unit": "ft",
                "x": 2,
                "y": -4,
                "z": -6,
            },
            "F_1": {
                "unit": "lbf",
                "x": -26.2,
                "y": -41.9,
                "z": 62.9,
            },
            "F_2": {
                "unit": "lbf",
                "x": 13.4,
                "y": -26.7,
                "z": -40.1,
            },
            "F_R": {
                "magnitude": 73.5,
                "unit": "lbf",
                "alpha": 100,
                "beta": 159,
                "gamma": 71.9,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_89": {
        "name": "Problem 2-89",
        "description": """
        If F=350i - 250j - 450k N and cable is 9 m long, determine the x, y, z coordinates of point A.
        """,
        "points": {
            "A": Point.unknown(unit="m", distance=9),  # Unknown point 9m from B
            "B": PointCartesian(x=0, y=0, z=0, unit="m"),  # Origin
        },
        "position_vectors": {
            "r_AB": {
                "from": "A",
                "to": "B",
                "distance": 9,
            },
        },
        "force_vectors": {
            "F_1": ForceVector(x=350, y=-250, z=-450, unit="N", name="F_1"),
        },
        "expected": {
            "A": {
                "unit": "m",
                "x": -5.06,
                "y": 3.61,
                "z": 6.51,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_90": {
        "name": "Problem 2-90",
        "description": """
        The 8-m-long cable is anchored to the ground at A. If x = 4 m and y = 2 m, determine the coordinate z to the highest point of attachment along the column.
        """,
        "points": {
            "A": PointCartesian(x=4, y=2, z=0, unit="m"),  # Ground anchor
            "B": PointCartesian(x=0, y=0, z=..., unit="m"),  # Top of column, z unknown
        },
        "position_vectors": {
            "r_AB": {
                "from": "A",
                "to": "B",
                "magnitude": 8,  # Cable length
                "unit": "m",
            },
        },
        "expected": {
            "B": {
                "unit": "m",
                "z": 6.63,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_93": {
        "name": "Problem 2-93",
        "description": """
        If F_B = 560 N and F_C = 700 N, determine the magnitude and coordinate direction
        angles of the resultant force acting on the flag pole.
        """,
        "points": {
            "A": Point(0, 0, 6, unit="m"),  # Top of pole
            "B": Point(2, -3, 0, unit="m"),
            "C": Point(3, 2, 0, unit="m"),
        },
        "forces": {
            "F_B": {
                "from": "A",
                "to": "B",
                "magnitude": 560,
                "unit": "N",
            },
            "F_C": {
                "from": "A",
                "to": "C",
                "magnitude": 700,
                "unit": "N",
            },
        },
        "solve_resultant": True,
        "expected": {
            "F_B": {
                "magnitude": 560,
                "unit": "N",
                "x": 160,
                "y": -240,
                "z": -480,
            },
            "F_C": {
                "magnitude": 700,
                "unit": "N",
                "x": 300,
                "y": 200,
                "z": -600,
            },
            "F_R": {
                "magnitude": 1175,
                "unit": "N",
                "x": 460,
                "y": -40,
                "z": -1080,
                "alpha": 66.9,
                "beta": 92.0,
                "gamma": 157,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_95": {
        "name": "Problem 2-95",
        "description": """
        The plate is suspended using the three cables which exert the forces shown.
        Express each force as a Cartesian vector.
        """,
        "points": {
            # Point A (on plate)
            "A": Point(0, 0, 0, unit="ft"),
            # Points B, C, D (cable anchor points) - derived from solution
            # r_BA = {-5i + 6j + 14k} so B = A + (-5, 6, 14) = (-5, 6, 14)
            "B": Point(-5, 6, 14, unit="ft"),
            # r_CA = {3i + 3j + 14k} so C = (3, 3, 14)
            "C": Point(3, 3, 14, unit="ft"),
            # r_DA = {-2i - 6j + 14k} so D = (-2, -6, 14)
            "D": Point(-2, -6, 14, unit="ft"),
        },
        "forces": {
            "F_BA": {
                "from": "A",
                "to": "B",
                "magnitude": 350,
                "unit": "lbf",
            },
            "F_CA": {
                "from": "A",
                "to": "C",
                "magnitude": 500,
                "unit": "lbf",
            },
            "F_DA": {
                "from": "A",
                "to": "D",
                "magnitude": 400,
                "unit": "lbf",
            },
        },
        "expected": {
            "F_BA": {
                "unit": "lbf",
                "x": -109,
                "y": 131,
                "z": 306,
            },
            "F_CA": {
                "unit": "lbf",
                "x": 103,
                "y": 103,
                "z": 479,
            },
            "F_DA": {
                "unit": "lbf",
                "x": -52.1,
                "y": -156,
                "z": 365,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_99": {
        "name": "Problem 2-99",
        "description": """
        The load at A creates a force of 60 lb in wire AB. Express this force as a
        Cartesian vector acting on A and directed toward B as shown.
        """,
        "points": {
            "A": Point(0, 0, -10, unit="ft"),
            # B = (5*sin(30°), 5*cos(30°), 0)
            "B": Point(5 * math.sin(math.radians(30)), 5 * math.cos(math.radians(30)), 0, unit="ft"),
        },
        "forces": {
            "F": {
                "from": "A",
                "to": "B",
                "magnitude": 60,
                "unit": "lbf",
            },
        },
        "expected": {
            "F": {
                "unit": "lbf",
                "x": 13.4,
                "y": 23.2,
                "z": 53.7,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
    "problem_2_100": {
        "name": "Problem 2-100",
        "description": """
        Determine the magnitude and coordinate direction angles of the resultant force
        acting at point A on the post.
        """,
        "points": {
            "A": Point(0, 0, 3, unit="m"),
            "B": Point(2, 4, 0, unit="m"),
            "C": Point(-3, -4, 0, unit="m"),
        },
        "forces": {
            "F_AB": {
                "from": "A",
                "to": "B",
                "magnitude": 200,
                "unit": "N",
            },
            "F_AC": {
                "from": "A",
                "to": "C",
                "magnitude": 150,
                "unit": "N",
            },
        },
        "solve_resultant": True,
        "expected": {
            "F_AB": {
                "unit": "N",
                "x": 74.3,
                "y": 148.6,
                "z": -111.4,
            },
            "F_AC": {
                "unit": "N",
                "x": -77.2,
                "y": -102.9,
                "z": -77.2,
            },
            "F_R": {
                "magnitude": 194,
                "unit": "N",
                "alpha": 91.1,
                "beta": 76.3,
                "gamma": 166,
            },
        },
        "debug": {
            "print_results": False,
            "assert_values": True
        },
    },
}


def assert_quantity_close(actual, expected_value: float, unit: str, name: str, rtol: float = 0.01):
    """Assert a Quantity is close to expected value using Quantity.is_close().

    Args:
        actual: Actual Quantity object
        expected_value: Expected numeric value
        unit: Unit string for the expected value
        name: Description for error messages
        rtol: Relative tolerance (default 1%)
    """
    if actual is None:
        raise AssertionError(f"{name} is None")

    expected = Q(expected_value, unit)
    assert actual.is_close(expected, rtol=rtol), f"{name}: expected {expected_value} {unit}, got {actual}"


def assert_angle_close(actual, expected_deg: float, name: str, rtol: float = 0.01):
    """Assert an angle Quantity is close to expected value in degrees.

    Args:
        actual: Actual angle Quantity (stored in radians internally)
        expected_deg: Expected value in degrees
        name: Description for error messages
        rtol: Relative tolerance (default 1%)
    """
    if actual is None:
        raise AssertionError(f"{name} is None")

    expected = Q(expected_deg, "degree")
    assert actual.is_close(expected, rtol=rtol), f"{name}: expected {expected_deg} deg, got {actual}"


@pytest.mark.parametrize("problem_key", list(POSITION_VECTOR_PROBLEMS.keys()))
def test_position_vector_problem(problem_key):
    """Test position vector problems using PositionVectorProblem solver."""
    spec = POSITION_VECTOR_PROBLEMS[problem_key]

    if spec["debug"]["print_results"]:
        print(f"\n{'=' * 80}")
        print(f"Testing: {spec['name']}")
        print(f"{'=' * 80}")
        print(spec["description"])

    points = spec["points"]
    expected = spec["expected"]

    # Test position vectors if specified
    if "position_vectors" in spec:
        for pv_name, pv_spec in spec["position_vectors"].items():
            from_name = pv_spec["from"]
            to_name = pv_spec["to"]

            # Create position vector
            r = PositionVector.from_points(points[from_name], points[to_name], name=pv_name)

            if spec["debug"]["print_results"]:
                print(f"\n{pv_name}: {r}")

            if spec["debug"]["assert_values"] and pv_name in expected:
                exp = expected[pv_name]
                unit = exp.get("unit", "m")

                # Use Quantity-based comparisons
                if "x" in exp:
                    assert_quantity_close(r.x, exp["x"], unit, f"{pv_name} x")
                if "y" in exp:
                    assert_quantity_close(r.y, exp["y"], unit, f"{pv_name} y")
                if "z" in exp:
                    assert_quantity_close(r.z, exp["z"], unit, f"{pv_name} z")
                if "magnitude" in exp:
                    assert_quantity_close(r.magnitude, exp["magnitude"], unit, f"{pv_name} magnitude")

    # Test forces along lines - use PositionVectorProblem with ComponentSolver
    if "forces" in spec or "force_vectors" in spec:
        # Check if we need to solve for resultant
        solve_resultant = spec.get("solve_resultant", False)

        # Separate force specs (dicts) from ForceVector objects (like resultants)
        force_specs = {}
        force_vectors = spec.get("force_vectors", {}).copy()

        # Get forces from "forces" key (old style)
        if "forces" in spec:
            for force_name, force_data in spec["forces"].items():
                if isinstance(force_data, dict) and "from" in force_data and "to" in force_data:
                    force_specs[force_name] = force_data
                elif isinstance(force_data, ForceVector):
                    force_vectors[force_name] = force_data

        # Create dynamic problem class
        class_attrs = {
            "name": spec["name"],
            "description": spec["description"],
        }

        # Add points
        class_attrs.update(points)

        # Add force specs (dict with from/to/magnitude)
        class_attrs.update(force_specs)

        # Add ForceVector objects (like resultants)
        class_attrs.update(force_vectors)

        # Add unknown resultant if needed
        if solve_resultant and "F_R" not in force_vectors:
            # Get unit from first force spec
            first_spec = next(iter(force_specs.values()))
            class_attrs["F_R"] = ForceVector.unknown(
                name="F_R",
                unit=first_spec["unit"],
                is_resultant=True,
            )

        # Create and solve problem
        ProblemClass = type(f"Problem_{problem_key}", (PositionVectorProblem,), class_attrs)
        problem = ProblemClass()
        solved_forces = problem.solve()

        if spec["debug"]["print_results"]:
            for force_name, F in solved_forces.items():
                print(f"\n{force_name}:")
                if F.x and F.y and F.z:
                    print(f"  Components: {{{F.x}i + {F.y}j + {F.z}k}}")
                if F.magnitude:
                    print(f"  Magnitude: {F.magnitude}")

        # Verify all forces
        if spec["debug"]["assert_values"]:
            # Include force specs, plus F_R if solving resultant or if F_R was explicitly provided
            forces_to_verify = list(force_specs.keys())
            if solve_resultant or "F_R" in force_vectors:
                forces_to_verify.append("F_R")

            for force_name in forces_to_verify:
                if force_name not in expected:
                    continue

                F = solved_forces.get(force_name)
                if F is None:
                    continue

                exp = expected[force_name]
                unit = exp.get("unit", "N")

                if "magnitude" in exp:
                    assert_quantity_close(F.magnitude, exp["magnitude"], unit, f"{force_name} magnitude")
                if "x" in exp:
                    assert_quantity_close(F.x, exp["x"], unit, f"{force_name} x")
                if "y" in exp:
                    assert_quantity_close(F.y, exp["y"], unit, f"{force_name} y")
                if "z" in exp:
                    assert_quantity_close(F.z, exp["z"], unit, f"{force_name} z")
                if "alpha" in exp:
                    assert_angle_close(F.alpha, exp["alpha"], f"{force_name} alpha")
                if "beta" in exp:
                    assert_angle_close(F.beta, exp["beta"], f"{force_name} beta")
                if "gamma" in exp:
                    assert_angle_close(F.gamma, exp["gamma"], f"{force_name} gamma")

            # Verify solved points
            for point_name in problem.solved_points:
                if point_name not in expected:
                    continue

                solved_point = problem.solved_points[point_name]
                exp = expected[point_name]
                unit = exp.get("unit", "m")

                if spec["debug"]["print_results"]:
                    coords = solved_point.to_array()
                    print(f"\n{point_name}: ({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}) {unit}")

                if "x" in exp:
                    assert_quantity_close(solved_point.x, exp["x"], unit, f"{point_name} x")
                if "y" in exp:
                    assert_quantity_close(solved_point.y, exp["y"], unit, f"{point_name} y")
                if "z" in exp:
                    assert_quantity_close(solved_point.z, exp["z"], unit, f"{point_name} z")


if __name__ == "__main__":
    # Run tests with detailed output
    for problem_key in POSITION_VECTOR_PROBLEMS.keys():
        problem = POSITION_VECTOR_PROBLEMS[problem_key]
        problem["debug"]["print_results"] = True
        test_position_vector_problem(problem_key)
        problem["debug"]["print_results"] = False
