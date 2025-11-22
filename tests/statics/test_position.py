"""
Comprehensive tests for position vectors and forces along lines using problems 2-86 to 2-105 from textbook.

These tests validate:
- Position vector creation from points
- Unit vector computation (direction cosines)
- Force directed along a line (F = |F| * û)
- Coordinate direction angles (α, β, γ)
- Resultant force calculation
"""

import math

import pytest

from qnty.core.quantity import Q
from qnty.problems.position_vector import PositionVectorProblem
from qnty.spatial import ForceVector, _Point, _Vector, create_point_cartesian, create_point_from_ratio, create_point_polar, create_point_spherical, create_vector_cartesian, create_vector_from_points
from qnty.spatial.point import Point

# =============================================================================
# Helper functions for assertions
# =============================================================================

def are_close_enough(actual, expected, rtol: float = 0.01) -> bool:
    """Check if two quantities are close within tolerance.

    This is a unit-aware comparison that handles automatic unit conversion.
    Both quantities are compared in SI units internally.

    Args:
        actual: Actual Quantity object
        expected: Expected Quantity object
        rtol: Relative tolerance (default 1%)

    Returns:
        True if quantities are close enough, False otherwise

    Raises:
        TypeError: If dimensions don't match
        ValueError: If either quantity has no value
    """
    if actual.dim != expected.dim:
        raise TypeError(f"Cannot compare quantities with different dimensions: {actual.dim} vs {expected.dim}")

    if actual.value is None:
        raise ValueError(f"Quantity '{actual.name}' has no value")
    if expected.value is None:
        raise ValueError(f"Quantity '{expected.name}' has no value")

    # Compare in SI units (both .value properties are already in SI)
    diff = abs(actual.value - expected.value)
    max_val = max(abs(actual.value), abs(expected.value))

    if max_val == 0:
        return diff <= rtol

    return diff <= rtol * max_val


def assert_quantity_close(actual, expected, name: str, rtol: float = 0.01):
    """Assert two quantities are close using are_close_enough().

    Args:
        actual: Actual Quantity object
        expected: Expected Quantity object
        name: Description for error messages
        rtol: Relative tolerance (default 1%)
    """
    if actual is None:
        raise AssertionError(f"{name} is None")

    assert are_close_enough(actual, expected, rtol=rtol), \
        f"{name}: expected {expected}, got {actual}"


def assert_vector_components(actual_vector, expected_x, expected_y, expected_z, name: str, rtol: float = 0.01):
    """Assert vector x, y, z components match expected quantities."""
    if expected_x is not None:
        assert_quantity_close(actual_vector.x, expected_x, f"{name} x", rtol)
    if expected_y is not None:
        assert_quantity_close(actual_vector.y, expected_y, f"{name} y", rtol)
    if expected_z is not None:
        assert_quantity_close(actual_vector.z, expected_z, f"{name} z", rtol)


def assert_force_angles(actual_force, expected_alpha, expected_beta, expected_gamma, name: str, rtol: float = 0.01):
    """Assert force direction angles match expected quantities."""
    if expected_alpha is not None:
        assert_quantity_close(actual_force.alpha, expected_alpha, f"{name} α", rtol)
    if expected_beta is not None:
        assert_quantity_close(actual_force.beta, expected_beta, f"{name} β", rtol)
    if expected_gamma is not None:
        assert_quantity_close(actual_force.gamma, expected_gamma, f"{name} γ", rtol)


# =============================================================================
# Problem class definitions
# =============================================================================

class Chapter2Problem86(PositionVectorProblem):
    name = "Problem 2-86"
    description = """
    Determine the length of the connecting rod AB by first formulating
    a Cartesian position vector from A to B and then determining its magnitude.
    """

    # Points
    A = create_point_polar(dist=150, angle=30, plane="xy", wrt="-x", unit="mm")
    B = create_point_cartesian(y=300, unit="mm")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=129.90, v=375, w=0, unit="mm")

        # Mini test - validates expected values are self-consistent
        # assert are_close_enough(r_AB.magnitude, Q(397, "mm"), rtol=0.01)


class Chapter2Problem87(PositionVectorProblem):
    name = "Problem 2-87"
    description = """
    Express force F as a Cartesian vector; then determine its coordinate direction angles.
    """

    # Points
    A = create_point_spherical(
        r=10, unit="ft",
        theta=30, theta_wrt="+y",
        phi=70, phi_wrt="xy"
    )

    B = create_point_cartesian(x=5, y=-7, unit="ft")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    F = ForceVector.from_position_vector(r_AB, magnitude=135, unit="lbf", name="F")

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=6.710, v=-9.962, w=-9.397, unit="ft")
        F = create_vector_cartesian(u=59.4, v=-88.2, w=-83.2, unit="lbf")

        assert are_close_enough(F.alpha, Q(63.9, "deg"), rtol=0.01)
        assert are_close_enough(F.beta, Q(131, "deg"), rtol=0.01)
        assert are_close_enough(F.gamma, Q(128, "deg"), rtol=0.01)


class Chapter2Problem88(PositionVectorProblem):
    name = "Problem 2-88"
    description = """
    Express each of the forces in Cartesian vector form and determine
    the magnitude and coordinate direction angles of the resultant force.
    """

    # Points
    A = create_point_cartesian(x=0, y=4, z=0, unit="ft")
    B = create_point_cartesian(x=2, z=-6, unit="ft")
    C = create_point_from_ratio(
        dist=2.5, unit="ft", ratio_component="x",
        x=-5, y=0, z=12
    )

    # Computed values
    r_AC = create_vector_from_points(A, C, name="r_AC")
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force magnitudes
    F_1 = ForceVector.from_position_vector(
        r_AC, magnitude=80, unit="lbf", name="F_1"
    )
    F_2 = ForceVector.from_position_vector(
        r_AB, magnitude=50, unit="lbf", name="F_2"
    )

    F_R = ForceVector.resultant([F_1, F_2], name="F_R")

    # Expected values
    class expected:
        r_AC = create_vector_cartesian(u=-2.5, v=-4, w=6, unit="ft")
        r_AB = create_vector_cartesian(u=2, v=-4, w=-6, unit="ft")
        F_1 = create_vector_cartesian(u=-26.2, v=-41.9, w=62.9, unit="lbf")
        F_2 = create_vector_cartesian(u=13.4, v=-26.7, w=-40.1, unit="lbf")
        F_R = create_vector_cartesian(u=-12.8, v=-68.6, w=22.8, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(73.5, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(100, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(159, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(71.9, "deg"), rtol=0.01)

class Chapter2Problem89(PositionVectorProblem):
    name = "Problem 2-89"
    description = """
    Express each of the forces in Cartesian vector form and determine
    the magnitude and coordinate direction angles of the resultant force.
    """

    # Points
    A = create_point_cartesian(x=..., y=..., z=..., unit="m")
    B = create_point_cartesian(x=0, y=0, z=0, unit="m")
    r_AB = create_vector_from_points(A, B, magnitude=9, unit="m", name="r_AB")
    F = create_vector_cartesian(u=350, v=-250, w=-450, unit="N")

    # Expected values
    class expected:
        A = create_point_cartesian(x=-5.06, y=3.61, z=6.51, unit="m")
        B = create_point_cartesian(x=0, y=0, z=0, unit="m")


class Chapter2Problem92:
    """Problem 2-92: Forces along lines with resultant."""

    name = "Problem 2-92"
    description = """
    Express each of the forces in Cartesian vector form and determine
    the magnitude and coordinate direction angles of the resultant force.
    """

    # Points
    A = create_point_cartesian(x=0, y=-0.75, z=3, unit="m")
    B = create_point_polar(dist=2, angle=40, unit="m")
    C = create_point_cartesian(x=2, y=-1, z=0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_AB_magnitude = Q(250, "N")
    F_AC_magnitude = Q(400, "N")

    # Expected values
    class expected:
        F_AB = create_vector_cartesian(u=97.3, v=129, w=-191, unit="N")
        F_AC = create_vector_cartesian(u=221, v=-27.7, w=-332, unit="N")

        F_R = create_vector_cartesian(u=318.3, v=101.3, w=-523, unit="N")
        F_R_magnitude = Q(620, "N")
        F_R_alpha = Q(59.1, "deg")
        F_R_beta = Q(80.6, "deg")
        F_R_gamma = Q(147, "deg")


class Chapter2Problem93:
    """Problem 2-93: Resultant force on flag pole."""

    name = "Problem 2-93"
    description = """
    If F_B = 560 N and F_C = 700 N, determine the magnitude and coordinate
    direction angles of the resultant force acting on the flag pole.
    """

    # Points
    A = Point(0, 0, 6, unit="m")  # Top of pole
    B = Point(2, -3, 0, unit="m")
    C = Point(3, 2, 0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_B_magnitude = Q(560, "N")
    F_C_magnitude = Q(700, "N")

    # Expected values
    class expected:
        F_B = create_vector_cartesian(u=160, v=-240, w=-480, unit="N")
        F_C = create_vector_cartesian(u=300, v=200, w=-600, unit="N")

        F_R = create_vector_cartesian(u=460, v=-40, w=-1080, unit="N")
        F_R_magnitude = Q(1175, "N")
        F_R_alpha = Q(66.9, "deg")
        F_R_beta = Q(92.0, "deg")
        F_R_gamma = Q(157, "deg")


class Chapter2Problem95:
    """Problem 2-95: Plate suspended by three cables."""

    name = "Problem 2-95"
    description = """
    The plate is suspended using the three cables which exert the forces shown.
    Express each force as a Cartesian vector.
    """

    # Points
    A = Point(0, 0, 0, unit="ft")  # On plate
    B = Point(-5, 6, 14, unit="ft")
    C = Point(3, 3, 14, unit="ft")
    D = Point(-2, -6, 14, unit="ft")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")
    r_AD = create_vector_from_points(A, D, name="r_AD")

    # Force magnitudes
    F_BA_magnitude = Q(350, "lbf")
    F_CA_magnitude = Q(500, "lbf")
    F_DA_magnitude = Q(400, "lbf")

    # Expected values
    class expected:
        F_BA = create_vector_cartesian(u=-109, v=131, w=306, unit="lbf")
        F_CA = create_vector_cartesian(u=103, v=103, w=479, unit="lbf")
        F_DA = create_vector_cartesian(u=-52.1, v=-156, w=365, unit="lbf")


class Chapter2Problem99:
    """Problem 2-99: Force in wire AB."""

    name = "Problem 2-99"
    description = """
    The load at A creates a force of 60 lb in wire AB. Express this force as a
    Cartesian vector acting on A and directed toward B as shown.
    """

    # Points
    A = Point(0, 0, -10, unit="ft")
    B = Point(5 * math.sin(math.radians(30)), 5 * math.cos(math.radians(30)), 0, unit="ft")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force magnitude
    F_magnitude = Q(60, "lbf")

    # Expected values
    class expected:
        F = create_vector_cartesian(u=13.4, v=23.2, w=53.7, unit="lbf")


class Chapter2Problem100:
    """Problem 2-100: Resultant force on post."""

    name = "Problem 2-100"
    description = """
    Determine the magnitude and coordinate direction angles of the resultant force
    acting at point A on the post.
    """

    # Points
    A = Point(0, 0, 3, unit="m")
    B = Point(2, 4, 0, unit="m")
    C = Point(-3, -4, 0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_AB_magnitude = Q(200, "N")
    F_AC_magnitude = Q(150, "N")

    # Expected values
    class expected:
        F_AB = create_vector_cartesian(u=74.3, v=148.6, w=-111.4, unit="N")
        F_AC = create_vector_cartesian(u=-77.2, v=-102.9, w=-77.2, unit="N")

        F_R = create_vector_cartesian(u=-2.9, v=45.7, w=-188.6, unit="N")
        F_R_magnitude = Q(194, "N")
        F_R_alpha = Q(91.1, "deg")
        F_R_beta = Q(76.3, "deg")
        F_R_gamma = Q(166, "deg")


# =============================================================================
# Collect all problem classes for parametrized testing
# =============================================================================

PROBLEM_CLASSES = [
    Chapter2Problem86,
    Chapter2Problem87,
    Chapter2Problem88,
    Chapter2Problem89,
    Chapter2Problem92,
    Chapter2Problem93,
    Chapter2Problem95,
    Chapter2Problem99,
    Chapter2Problem100,
]


# =============================================================================
# Test function
# =============================================================================

@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_position_vector_problem(problem_class):
    """Test position vector problem by comparing computed values against expected."""
    rtol = 0.01

    # Check if problem needs to be solved (has unknowns)
    needs_solving = False
    for attr_name in dir(problem_class):
        if attr_name.startswith('_'):
            continue
        attr = getattr(problem_class, attr_name)
        # Check for create_point_cartesian with unknowns
        if hasattr(attr, 'has_unknowns') and attr.has_unknowns:
            needs_solving = True
            break
        # Check for PositionVector with magnitude constraint and unknowns
        if hasattr(attr, 'has_unknowns') and callable(getattr(attr, 'has_unknowns', None)):
            if attr.has_unknowns():
                needs_solving = True
                break

    # Instantiate and solve if needed
    if needs_solving:
        problem = problem_class()
        problem.solve()
        source = problem  # Get values from solved instance
    else:
        source = problem_class  # Get values from class

    expected = problem_class.expected

    # Compare same-named attributes
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue

        exp_val = getattr(expected, attr_name)

        # Compare vectors (_Vector, PositionVector, ForceVector)
        if hasattr(exp_val, '_vector') or isinstance(exp_val, _Vector):
            actual = getattr(source, attr_name, None)
            if actual is None:
                raise AssertionError(f"{attr_name} not found in problem class")

            # Get the underlying _Vector for comparison
            if hasattr(actual, '_vector'):
                actual_vec = actual._vector
            elif hasattr(actual, 'to_cartesian'):
                actual_vec = actual.to_cartesian()
            else:
                actual_vec = actual

            if isinstance(exp_val, _Vector):
                exp_vec = exp_val
            elif hasattr(exp_val, '_vector'):
                exp_vec = exp_val._vector
            elif hasattr(exp_val, 'to_cartesian'):
                exp_vec = exp_val.to_cartesian()
            else:
                exp_vec = exp_val

            assert actual_vec.is_close(exp_vec, rtol=rtol), \
                f"{attr_name}: expected {exp_val}, got {actual}"

        # Compare points (_Point and other point types)
        elif isinstance(exp_val, _Point):
            actual = getattr(source, attr_name, None)
            if actual is None:
                raise AssertionError(f"{attr_name} not found in problem class")

            # Convert both to _Point for comparison
            if hasattr(actual, 'to_cartesian'):
                actual_pt = actual.to_cartesian()
            else:
                actual_pt = actual
            exp_pt = exp_val

            # Compare coordinates using _Point's _coords
            actual_coords = actual_pt._coords
            exp_coords = exp_pt._coords
            for i, coord in enumerate(['x', 'y', 'z']):
                a = actual_coords[i]
                b = exp_coords[i]
                if b == 0:
                    ok = abs(a) <= rtol
                else:
                    ok = abs(a - b) / abs(b) <= rtol
                assert ok, f"{attr_name} {coord}: expected {b}, got {a}"


if __name__ == "__main__":
    # Run all tests
    for problem_class in PROBLEM_CLASSES:
        print(f"Testing {problem_class.name}...")
        test_position_vector_problem(problem_class)
        print(f"✓ {problem_class.name} passed")
    print("\nAll tests passed!")
