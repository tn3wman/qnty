"""
Comprehensive tests for position vectors and forces along lines using problems 2-86 to 2-105 from textbook.

These tests validate:
- Position vector creation from points
- Unit vector computation (direction cosines)
- Force directed along a line (F = |F| * û)
- Coordinate direction angles (α, β, γ)
- Resultant force calculation
"""

from calendar import c
import math

import pytest

from qnty.core.quantity import Q
from qnty.problems.position_vector import PositionVectorProblem
from qnty.spatial import (
    ForceVector,
    _Point,
    _Vector,
    create_point_cartesian,
    create_point_from_ratio,
    create_point_polar,
    create_point_spherical,
    create_vector_along,
    create_vector_cartesian,
    create_vector_from_points,
)
from qnty.spatial.plane import create_plane_rotated_y
from qnty.spatial.points import create_point_along
from qnty.spatial.vectors import create_point_at_midpoint, create_vector_direction_angles, create_vector_in_plane, create_vector_polar, create_vector_resultant, create_vector_resultant_cartesian, create_vector_spherical, create_vector_with_magnitude

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
    A = create_point_polar(r=150, angle=30, plane="xy", wrt="-x", unit="mm")
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
    r_AB = create_vector_with_magnitude(A, B, magnitude=9, unit="m", name="r_AB")
    F = create_vector_cartesian(u=350, v=-250, w=-450, unit="N")

    # Expected values
    class expected:
        A = create_point_cartesian(x=-5.06, y=3.61, z=6.51, unit="m")
        B = create_point_cartesian(x=0, y=0, z=0, unit="m")

class Chapter2Problem90(PositionVectorProblem):
    name = "Problem 2-90"
    description = """
    The 8-m-long cable is anchored to the ground at A. If x = 4 m and y = 2 m, determine the coordinate z to the highest point of attachment along the column.
    """

    # Points
    A = create_point_cartesian(x=4, y=2, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0, z=..., unit="m")
    r_AB = create_vector_with_magnitude(A, B, magnitude=8, unit="m", name="r_AB")

    # Expected values
    class expected:
        B = create_point_cartesian(x=0, y=0, z=6.63, unit="m")

# TODO: This requires some more advanced logic (x=y)
class Chapter2Problem91(PositionVectorProblem):
    name = "Problem 2-91"
    description = """
    The 8-m-long cable is anchored to the ground at A. If z = 5 m, determine the location + x, + y of point A. Choose a value such that x = y.
    """

    # Points
    A = create_point_cartesian(x=4, y=2, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0, z=..., unit="m")
    r_AB = create_vector_with_magnitude(A, B, magnitude=8, unit="m", name="r_AB")

    # Expected values
    class expected:
        B = create_point_cartesian(x=0, y=0, z=6.63, unit="m")

class Chapter2Problem92(PositionVectorProblem):
    """Problem 2-92: Forces along lines with resultant."""

    name = "Problem 2-92"
    description = """
    Express each of the forces in Cartesian vector form and determine the magnitude and coordinate direction angles of the resultant force.
    """

    # Points
    A = create_point_cartesian(x=0, y=-0.75, z=3, unit="m")
    B = create_point_polar(r=2, angle=40, unit="m")
    C = create_point_cartesian(x=2, y=-1, z=0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force vectors along position vectors
    F_AB = create_vector_along(r_AB, magnitude=250, unit="N", name="F_AB")
    F_AC = create_vector_along(r_AC, magnitude=400, unit="N", name="F_AC")

    F_R = create_vector_resultant(F_AB, F_AC, name="F_R")

    # Expected values
    class expected:
        # pass
        F_AB = create_vector_cartesian(u=97.3, v=129, w=-191, unit="N")
        F_AC = create_vector_cartesian(u=221, v=-27.7, w=-332, unit="N")

        F_R = create_vector_cartesian(u=318.7, v=101.7, w=-522.6, unit="N")
        # F_R_magnitude = Q(620, "N")
        # F_R_alpha = Q(59.1, "deg")
        # F_R_beta = Q(80.6, "deg")
        # F_R_gamma = Q(147, "deg")

        assert are_close_enough(F_R.magnitude, Q(620, "N"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(59.1, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(80.6, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(147, "deg"), rtol=0.01)



class Chapter2Problem93(PositionVectorProblem):
    name = "Problem 2-93"
    description = """
    If F_B = 560 N and F_C = 700 N, determine the magnitude and coordinate direction angles of the resultant force acting on the flag pole.
    """

    # Points
    A = create_point_cartesian(x=0, y=0, z=6, unit="m")  # Top of pole
    B = create_point_cartesian(x=2, y=-3, z=0, unit="m")
    C = create_point_cartesian(x=3, y=2, z=0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_B = create_vector_along(r_AB, magnitude=560, unit="N", name="F_B")
    F_C = create_vector_along(r_AC, magnitude=700, unit="N", name="F_C")

    F_R = create_vector_resultant(F_B, F_C, name="F_R")

    # Expected values
    class expected:
        F_B = create_vector_cartesian(u=160, v=-240, w=-480, unit="N")
        F_C = create_vector_cartesian(u=300, v=200, w=-600, unit="N")
        F_R = create_vector_cartesian(u=460, v=-40, w=-1080, unit="N")

        assert are_close_enough(F_R.magnitude, Q(1175, "N"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(66.9, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(92.0, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(157, "deg"), rtol=0.01)

class Chapter2Problem94(PositionVectorProblem):
    name = "Problem 2-94"
    description = """
    If F_B = 700 N, and F_C = 560 N, determine the magnitude and coordinate direction angles of the resultant force acting on the flag pole.
    """

    # Points
    A = create_point_cartesian(x=0, y=0, z=6, unit="m")
    B = create_point_cartesian(x=2, y=-3, z=0, unit="m")
    C = create_point_cartesian(x=3, y=2, z=0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_B = create_vector_along(r_AB, magnitude=700, unit="N", name="F_B")
    F_C = create_vector_along(r_AC, magnitude=560, unit="N", name="F_C")

    F_R = create_vector_resultant(F_B, F_C, name="F_R")

    # Expected values
    class expected:
        F_B = create_vector_cartesian(u=200, v=-300, w=-600, unit="N")
        F_C = create_vector_cartesian(u=240, v=160, w=-480, unit="N")
        F_R = create_vector_cartesian(u=440, v=-140, w=-1080, unit="N")

        assert are_close_enough(F_R.magnitude, Q(1175, "N"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(68, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(97, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(157, "deg"), rtol=0.01)

class Chapter2Problem95(PositionVectorProblem):
    name = "Problem 2-95"
    description = """
    The plate is suspended using the three cables which exert the forces shown. Express each force as a Cartesian vector.
    """

    # Points
    A = create_point_cartesian(x=0, y=0, z=14, unit="ft")  # On plate
    B = create_point_cartesian(x=5, y=-6, z=0, unit="ft")
    C = create_point_cartesian(x=-3, y=-3, z=0, unit="ft")
    D = create_point_cartesian(x=2, y=6, z=0, unit="ft")

    # Computed values
    r_BA = create_vector_from_points(B, A, name="r_BA")
    r_CA = create_vector_from_points(C, A, name="r_CA")
    r_DA = create_vector_from_points(D, A, name="r_DA")

    # Force magnitudes
    F_BA = create_vector_along(r_BA, magnitude=350, unit="lbf", name="F_BA")
    F_CA = create_vector_along(r_CA, magnitude=500, unit="lbf", name="F_CA")
    F_DA = create_vector_along(r_DA, magnitude=400, unit="lbf", name="F_DA")

    # Expected values
    class expected:
        F_BA = create_vector_cartesian(u=-109, v=131, w=306, unit="lbf")
        F_CA = create_vector_cartesian(u=103, v=103, w=479, unit="lbf")
        F_DA = create_vector_cartesian(u=-52.1, v=-156, w=365, unit="lbf")

class Chapter2Problem96(PositionVectorProblem):
    name = "Problem 2-96"
    description = """
    The three supporting cables exert the forces shown on the sign. Represent each force as a Cartesian vector.
    """

    # Points
    A = create_point_cartesian(x=5, y=0, z=0, unit="m")  # On plate
    B = create_point_cartesian(x=0, y=2, z=3, unit="m")
    C = create_point_cartesian(x=0, y=-2, z=3, unit="m")
    D = create_point_cartesian(x=2, y=0, z=0, unit="m")
    E = create_point_cartesian(x=0, y=0, z=3, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")
    r_DE = create_vector_from_points(D, E, name="r_DE")

    # Force magnitudes
    F_B = create_vector_along(r_AB, magnitude=400, unit="N", name="F_B")
    F_C = create_vector_along(r_AC, magnitude=400, unit="N", name="F_C")
    F_E = create_vector_along(r_DE, magnitude=350, unit="N", name="F_E")

    # Expected values
    class expected:
        F_B = create_vector_cartesian(u=-324.4, v=129.7, w=194.7, unit="N")
        F_C = create_vector_cartesian(u=-324.4, v=-129.7, w=194.7, unit="N")
        F_E = create_vector_cartesian(u=-194, v=0, w=291, unit="N")

class Chapter2Problem97(PositionVectorProblem):
    name = "Problem 2-97"
    description = """
    Determine the magnitude and coordinate direction angles of the resultant force of the two forces acting on the sign at point A.
    """

    # Points
    A = create_point_cartesian(x=5, y=0, z=0, unit="m")  # On plate
    B = create_point_cartesian(x=0, y=2, z=3, unit="m")
    C = create_point_cartesian(x=0, y=-2, z=3, unit="m")
    D = create_point_cartesian(x=2, y=0, z=0, unit="m")
    E = create_point_cartesian(x=0, y=0, z=3, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")
    r_DE = create_vector_from_points(D, E, name="r_DE")

    # Force magnitudes
    F_B = create_vector_along(r_AB, magnitude=400, unit="N", name="F_B")
    F_C = create_vector_along(r_AC, magnitude=400, unit="N", name="F_C")
    F_E = create_vector_along(r_DE, magnitude=350, unit="N", name="F_E")

    F_R_CB = create_vector_resultant(F_B, F_C, name="F_R_CB")

    # Expected values
    class expected:
        F_B = create_vector_cartesian(u=-324.4, v=129.7, w=194.7, unit="N")
        F_C = create_vector_cartesian(u=-324.4, v=-129.7, w=194.7, unit="N")
        F_E = create_vector_cartesian(u=-194, v=0, w=291, unit="N")

        F_R_CB = create_vector_cartesian(u=-648.8, v=0, w=389.4, unit="N")

        assert are_close_enough(F_R_CB.magnitude, Q(757, "N"), rtol=0.01)
        assert are_close_enough(F_R_CB.alpha, Q(149, "deg"), rtol=0.01)
        assert are_close_enough(F_R_CB.beta, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R_CB.gamma, Q(59, "deg"), rtol=0.01)

class Chapter2Problem98(PositionVectorProblem):
    name = "Problem 2-98"
    description = """
    The force F has a magnitude of 80 lb and acts at the midpoint C of the thin rod. Express the force as a Cartesian vector.
    """

    # Points
    A = create_point_cartesian(x=3, y=-2, z=0, unit="ft")
    B = create_point_cartesian(x=0, y=0, z=6, unit="ft")
    C = create_point_at_midpoint(A, B, name="C")
    O = create_point_cartesian(x=0, y=0, z=0, unit="ft")

    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_CO = create_vector_from_points(C, O, name="r_CO")

    F = create_vector_along(r_CO, magnitude=80, unit="lbf", name="F")


    # Expected values
    class expected:
        F = create_vector_cartesian(u=-34.3, v=22.9, w=-68.6, unit="lbf")

class Chapter2Problem99(PositionVectorProblem):
    name = "Problem 2-99"
    description = """
    The load at A creates a force of 60 lb in wire AB. Express this force as a
    Cartesian vector acting on A and directed toward B as shown.
    """

    # Points
    A = create_point_cartesian(x=0, y=0, z=-10, unit="ft")
    B = create_point_polar(r=5, angle=-30, plane="xy", wrt="+y", unit="ft")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force magnitude
    F = create_vector_along(r_AB, magnitude=60, unit="lbf", name="F")

    # Expected values
    class expected:
        F = create_vector_cartesian(u=13.4, v=23.2, w=53.7, unit="lbf")


class Chapter2Problem100(PositionVectorProblem):
    name = "Problem 2-100"
    description = """
    Determine the magnitude and coordinate direction angles of the resultant force acting at point A on the post.
    """

    # Points
    A = create_point_cartesian(x=0, y=0, z=3, unit="m")
    B = create_point_cartesian(x=2, y=4, z=0, unit="m")
    C = create_point_cartesian(x=-3, y=-4, z=0, unit="m")

    # Computed values
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force magnitudes
    F_AB = create_vector_along(r_AB, magnitude=200, unit="N", name="F_AB")
    F_AC = create_vector_along(r_AC, magnitude=150, unit="N", name="F_AC")

    F_R = create_vector_resultant(F_AB, F_AC, name="F_R")

    # Expected values
    class expected:
        F_AB = create_vector_cartesian(u=74.3, v=148.6, w=-111.4, unit="N")
        F_AC = create_vector_cartesian(u=-77.2, v=-102.9, w=-77.2, unit="N")

        F_R = create_vector_cartesian(u=-2.9, v=45.7, w=-188.6, unit="N")

        assert are_close_enough(F_R.magnitude, Q(194, "N"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(91.1, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(76.3, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(166, "deg"), rtol=0.01)


class Chapter2Problem101(PositionVectorProblem):
    name = "Problem 2-101"
    description = """
    The two mooring cables exert forces on the stern of a ship as shown.
    Represent each force as a Cartesian vector and determine the magnitude
    and coordinate direction angles of the resultant.
    """

    # Points - C is at stern (origin), A and B are mooring points
    A = create_point_cartesian(x=50, y=10, z=-30, unit="ft")
    B = create_point_cartesian(x=50, y=50, z=-30, unit="ft")
    C = create_point_cartesian(x=0, y=0, z=0, unit="ft")

    # Position vectors from C to mooring points
    r_CA = create_vector_from_points(C, A, name="r_CA")
    r_CB = create_vector_from_points(C, B, name="r_CB")

    # Forces along cables
    F_A = create_vector_along(r_CA, magnitude=200, unit="lbf", name="F_A")
    F_B = create_vector_along(r_CB, magnitude=150, unit="lbf", name="F_B")

    # Resultant force
    F_R = create_vector_resultant(F_A, F_B, name="F_R")

    # Expected values
    class expected:
        F_A = create_vector_cartesian(u=169, v=33.8, w=-101, unit="lbf")
        F_B = create_vector_cartesian(u=97.6, v=97.6, w=-58.6, unit="lbf")

        F_R = create_vector_cartesian(u=266.67, v=131.45, w=-160.00, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(338, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(37.8, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(67.1, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(118, "deg"), rtol=0.01)


class Chapter2Problem102(PositionVectorProblem):
    name = "Problem 2-102"
    description = """
    The engine of the lightweight plane is supported by struts that are connected to the space truss that makes up the structure of the plane. The anticipated loading in two of the struts is shown. Express each of these forces as a Cartesian vector.
    """

    A = create_point_cartesian(x=3, y=2.5, z=3, unit="ft")
    B = create_point_cartesian(x=0, y=3, z=2.5, unit="ft")
    C = create_point_cartesian(x=0, y=3, z=0, unit="ft")
    D = create_point_cartesian(x=3, y=2.5, z=0.5, unit="ft")

    # Position vectors
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_CD = create_vector_from_points(C, D, name="r_CD")


    # Forces along struts
    F_1 = create_vector_along(r_CD, magnitude=400, unit="lbf", name="F_1")
    F_2 = create_vector_along(r_AB, magnitude=600, unit="lbf", name="F_2")

    # Expected values
    class expected:
        F_1 = create_vector_cartesian(u=389, v=-64.9, w=64.9, unit="lbf")
        F_2 = create_vector_cartesian(u=-584, v=97.3, w=-97.3, unit="lbf")


class Chapter2Problem103(PositionVectorProblem):
    name = "Problem 2-103"
    description = """
    Determine the magnitude and coordinate direction angles of the resultant force.
    """

    A = create_point_cartesian(x=0, y=-2, z=4, unit="ft")
    B = create_point_cartesian(x=1.5, y=-3, z=0, unit="ft")
    C = create_point_polar(r=2, angle=20, plane="xy", wrt="+y", unit="ft")

    # Position vectors
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Forces along cables
    F_AB = create_vector_along(r_AB, magnitude=20, unit="lbf", name="F_AB")
    F_AC = create_vector_along(r_AC, magnitude=40, unit="lbf", name="F_AC")

    # Resultant force
    F_R = create_vector_resultant(F_AB, F_AC, name="F_R")

    # Expected values
    class expected:
        F_AB = create_vector_cartesian(u=6.838, v=-4.558, w=-18.23, unit="lbf")
        F_AC = create_vector_cartesian(u=-4.874, v=27.64, w=-28.50, unit="lbf")

        F_R = create_vector_cartesian(u=1.964, v=23.08, w=-46.73, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(52.2, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(87.8, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(63.7, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(154, "deg"), rtol=0.01)


class Chapter2Problem104(PositionVectorProblem):
    name = "Problem 2-104"
    description = """
    If the force in each cable tied to the bin is 70 lb, determine the magnitude
    and coordinate direction angles of the resultant force.
    """

    # Points - O at bin center (height 6), A/B/C/D at ground corners
    A = create_point_cartesian(x=3, y=-2, z=0, unit="ft")
    B = create_point_cartesian(x=3, y=2, z=0, unit="ft")
    C = create_point_cartesian(x=-3, y=2, z=0, unit="ft")
    D = create_point_cartesian(x=-3, y=-2, z=0, unit="ft")
    E = create_point_cartesian(x=0, y=0, z=6, unit="ft")

    # Position vectors from O to cable attachment points
    r_EA = create_vector_from_points(E, A, name="r_EA")
    r_EB = create_vector_from_points(E, B, name="r_EB")
    r_EC = create_vector_from_points(E, C, name="r_EC")
    r_ED = create_vector_from_points(E, D, name="r_ED")

    # Forces along cables (each 70 lb)
    F_A = create_vector_along(r_EA, magnitude=70, unit="lbf", name="F_A")
    F_B = create_vector_along(r_EB, magnitude=70, unit="lbf", name="F_B")
    F_C = create_vector_along(r_EC, magnitude=70, unit="lbf", name="F_C")
    F_D = create_vector_along(r_ED, magnitude=70, unit="lbf", name="F_D")

    # Resultant force
    F_R = create_vector_resultant(F_A, F_B, F_C, F_D, name="F_R")

    # Expected values
    class expected:
        F_A = create_vector_cartesian(u=30, v=-20, w=-60, unit="lbf")
        F_B = create_vector_cartesian(u=30, v=20, w=-60, unit="lbf")
        F_C = create_vector_cartesian(u=-30, v=20, w=-60, unit="lbf")
        F_D = create_vector_cartesian(u=-30, v=-20, w=-60, unit="lbf")

        F_R = create_vector_cartesian(u=0, v=0, w=-240, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(240, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(180, "deg"), rtol=0.01)


class Chapter2Problem105(PositionVectorProblem):
    name = "Problem 2-105"
    description = """
    If the resultant of the four forces is F_R = {-360k} lb, determine the tension
    developed in each cable. Due to symmetry, the tension in the four cables is the same.
    """

    # Points - O at top (height 6), A/B/C/D at ground corners
    A = create_point_cartesian(x=3, y=-2, z=0, unit="ft")
    B = create_point_cartesian(x=3, y=2, z=0, unit="ft")
    C = create_point_cartesian(x=-3, y=2, z=0, unit="ft")
    D = create_point_cartesian(x=-3, y=-2, z=0, unit="ft")
    Origin = create_point_cartesian(x=0, y=0, z=6, unit="ft")

    # Position vectors from O to cable attachment points
    r_OA = create_vector_from_points(Origin, A, name="r_OA")
    r_OB = create_vector_from_points(Origin, B, name="r_OB")
    r_OC = create_vector_from_points(Origin, C, name="r_OC")
    r_OD = create_vector_from_points(Origin, D, name="r_OD")

    # Forces along cables (each with unknown magnitude F = 105 lb)
    F_A = create_vector_along(r_OA, magnitude=105, unit="lbf", name="F_A")
    F_B = create_vector_along(r_OB, magnitude=105, unit="lbf", name="F_B")
    F_C = create_vector_along(r_OC, magnitude=105, unit="lbf", name="F_C")
    F_D = create_vector_along(r_OD, magnitude=105, unit="lbf", name="F_D")

    # Resultant force
    F_R = create_vector_resultant(F_A, F_B, F_C, F_D, name="F_R")

    # Expected values
    class expected:
        # Unit vectors: u_A = (3/7)i - (2/7)j - (6/7)k
        # F_A = 105 * u_A = {45, -30, -90} lb
        F_A = create_vector_cartesian(u=45, v=-30, w=-90, unit="lbf")
        F_B = create_vector_cartesian(u=45, v=30, w=-90, unit="lbf")
        F_C = create_vector_cartesian(u=-45, v=30, w=-90, unit="lbf")
        F_D = create_vector_cartesian(u=-45, v=-30, w=-90, unit="lbf")

        F_R = create_vector_cartesian(u=0, v=0, w=-360, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(360, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(180, "deg"), rtol=0.01)


class Chapter2Problem106(PositionVectorProblem):
    name = "Problem 2-106"
    description = """
    Express the force F in Cartesian vector form if it acts at the midpoint B of the rod.
    """


    A = create_point_cartesian(x=0, y=0, z=4, unit="m")
    C = create_point_cartesian(x=-3, y=4, z=0, unit="m")
    D = create_point_cartesian(x=4, y=6, z=0, unit="m")

    # B is at midpoint of rod AC
    B = create_point_at_midpoint(A, C, name="B")

    # Position vector from B to D
    r_BD = create_vector_from_points(B, D, name="r_BD")

    # Force along r_BD with magnitude 600 N
    F = create_vector_along(r_BD, magnitude=600, unit="N", name="F")

    # Expected values
    class expected:
        # B = midpoint = (-1.5, 2, -2) m
        # r_BD = D - B = (4-(-1.5), 6-2, -4-(-2)) = (5.5, 4, -2) m
        # |r_BD| = sqrt(5.5^2 + 4^2 + 2^2) = sqrt(50.25) = 7.0887 m
        # F = 600 * r_BD / |r_BD| = {466, 339, -169} N
        F = create_vector_cartesian(u=466, v=339, w=-169, unit="N")


class Chapter2Problem107(PositionVectorProblem):
    name = "Problem 2-107"
    description = """
    Express force F in Cartesian vector form if point B is located 3 m along the rod from end C.
    """

    # Points - A at origin, C at end of rod, D is target point
    A = create_point_cartesian(x=0, y=0, z=4, unit="m")
    C = create_point_cartesian(x=-3, y=4, z=0, unit="m")
    D = create_point_cartesian(x=4, y=6, z=0, unit="m")

    # B is 3 m along rod from C toward A
    B = create_point_along(C, A, distance=3, unit="m", name="B")

    # Position vector from B to D
    r_BD = create_vector_from_points(B, D, name="r_BD")

    # Force along r_BD with magnitude 600 N
    F = create_vector_along(r_BD, magnitude=600, unit="N", name="F")

    # Expected values
    class expected:
        F = create_vector_cartesian(u=476, v=329, w=-159, unit="N")


class Chapter2Problem108(PositionVectorProblem):
    name = "Problem 2-108"
    description = """
    The chandelier is supported by three chains which are concurrent at point O. If the force in each chain has a magnitude of 60 lb, express each force as a Cartesian vector and determine the magnitude and coordinate direction angles
    of the resultant force.
    """

    # Points - O at top (z=6), A/B/C at attachment points (z=0)
    # A: at angle 30° from +x axis (4cos30, -4sin30, 0) = (3.464, -2, 0)
    # B: at angle 30° from -x axis (-4cos30, -4sin30, 0) = (-3.464, -2, 0)
    # C: on +y axis (0, 4, 0)
    O = create_point_cartesian(x=0, y=0, z=6, unit="ft")

    # A = create_point_cartesian(x=4*math.cos(math.radians(30)), y=-4*math.sin(math.radians(30)), z=0, unit="ft")
    # B = create_point_cartesian(x=-4*math.cos(math.radians(30)), y=-4*math.sin(math.radians(30)), z=0, unit="ft")
    A = create_point_polar(r=4, angle=-120, plane="xy", wrt="+y", unit="ft")
    B = create_point_polar(r=4, angle=120, plane="xy", wrt="+y", unit="ft")
    C = create_point_cartesian(x=0, y=4, z=0, unit="ft")

    # Position vectors from O to attachment points
    r_OA = create_vector_from_points(O, A, name="r_OA")
    r_OB = create_vector_from_points(O, B, name="r_OB")
    r_OC = create_vector_from_points(O, C, name="r_OC")

    # Forces along chains (each 60 lb)
    F_A = create_vector_along(r_OA, magnitude=60, unit="lbf", name="F_A")
    F_B = create_vector_along(r_OB, magnitude=60, unit="lbf", name="F_B")
    F_C = create_vector_along(r_OC, magnitude=60, unit="lbf", name="F_C")

    # Resultant force
    F_R = create_vector_resultant(F_A, F_B, F_C, name="F_R")

    # Expected values
    class expected:
        F_A = create_vector_cartesian(u=28.8, v=-16.6, w=-49.9, unit="lbf")
        F_B = create_vector_cartesian(u=-28.8, v=-16.6, w=-49.9, unit="lbf")
        F_C = create_vector_cartesian(u=0, v=33.3, w=-49.9, unit="lbf")

        F_R = create_vector_cartesian(u=0, v=0, w=-149.8, unit="lbf")

        assert are_close_enough(F_R.magnitude, Q(150, "lbf"), rtol=0.01)
        assert are_close_enough(F_R.alpha, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.beta, Q(90, "deg"), rtol=0.01)
        assert are_close_enough(F_R.gamma, Q(180, "deg"), rtol=0.01)

class Chapter2Problem109(PositionVectorProblem):
    name = "Problem 2-109"
    description = """
    The chandelier is supported by three chains which are concurrent at point O. If the resultant force at O has a magnitude of 130 lb and is directed along the negative z axis, determine the force in each chain.
    """

    # Points - O at top (z=6), A/B/C at attachment points (z=0)
    O = create_point_cartesian(x=0, y=0, z=6, unit="ft")

    A = create_point_polar(r=4, angle=-120, plane="xy", wrt="+y", unit="ft")
    B = create_point_polar(r=4, angle=120, plane="xy", wrt="+y", unit="ft")
    C = create_point_cartesian(x=0, y=4, z=0, unit="ft")

    # Position vectors from O to attachment points
    r_OA = create_vector_from_points(O, A, name="r_OA")
    r_OB = create_vector_from_points(O, B, name="r_OB")
    r_OC = create_vector_from_points(O, C, name="r_OC")

    # Forces along chains with unknown magnitudes (to be solved)
    F_A = create_vector_along(r_OA, magnitude=..., unit="lbf", name="F_A")
    F_B = create_vector_along(r_OB, magnitude=..., unit="lbf", name="F_B")
    F_C = create_vector_along(r_OC, magnitude=..., unit="lbf", name="F_C")

    # Known resultant force as constraint for inverse solving
    F_R = create_vector_resultant_cartesian(
        F_A, F_B, F_C, u=0, v=0, w=-130, unit="lbf", name="F_R"
    )

    # Expected values - force magnitude F = 52.1 lb for each chain
    class expected:
        # F = 52.1 lb, unit vector for each direction scaled by F
        # u_OA = (3.464/7.21, -2/7.21, -6/7.21) = (0.480, -0.277, -0.832)
        # u_OB = (-3.464/7.21, -2/7.21, -6/7.21) = (-0.480, -0.277, -0.832)
        # u_OC = (0, 4/7.21, -6/7.21) = (0, 0.555, -0.832)
        F_A = create_vector_cartesian(u=25.0, v=-14.4, w=-43.3, unit="lbf")
        F_B = create_vector_cartesian(u=-25.0, v=-14.4, w=-43.3, unit="lbf")
        F_C = create_vector_cartesian(u=0, v=28.9, w=-43.3, unit="lbf")

        # Verify resultant
        F_R = create_vector_cartesian(u=0, v=0, w=-130, unit="lbf")

        # Force magnitude (same for all due to symmetry)
        # assert are_close_enough(F_A.magnitude, Q(52.1, "lbf"), rtol=0.01)


class Chapter2Problem110(PositionVectorProblem):
    name = "Problem 2-110"
    description = """
    The window is held open by chain AB. Determine the length of the chain, and express the 50-lb force acting at A along the chain as a Cartesian vector and determine its coordinate direction angles.
    """

    # Points - A is on window (cylindrical coords), B is on wall
    # A = (5*cos(40°), 8, 5*sin(40°)) ft = (3.830, 8.00, 3.214) ft
    # B = (0, 5, 12) ft
    A = create_point_polar(
        r=5, angle=-40, plane="xz", wrt="+x", unit="ft", offset=8
    )
    B = create_point_cartesian(
        x=0, y=5, z=12, unit="ft"
    )

    # Position vector from A to B
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force along chain with magnitude 50 lb
    F = create_vector_along(
        r_AB, magnitude=50, unit="lbf", name="F"
    )

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-3.830, v=-3.00, w=8.786, unit="ft")
        F = create_vector_cartesian(u=-19.1, v=-14.9, w=43.7, unit="lbf")

        # Direction angles: α=112°, β=107°, γ=29.0°
        assert are_close_enough(r_AB.magnitude, Q(10.0, "ft"), rtol=0.01)
        assert are_close_enough(F.alpha, Q(112, "deg"), rtol=0.01)
        assert are_close_enough(F.beta, Q(107, "deg"), rtol=0.01)
        assert are_close_enough(F.gamma, Q(29.0, "deg"), rtol=0.01)


class Chapter2Problem111(PositionVectorProblem):
    name = "Problem 2-111"
    description = """
    The window is held open by cable AB. Determine the length of the cable and express the 30-N force acting at A along the cable as a Cartesian vector.
    """
    
    A = create_point_polar(
        r=300, angle=30, plane="xz", wrt="+x", unit="mm", offset=500
    )
    # Point B is on wall at (0, 150, 250) mm
    B = create_point_cartesian(
        x=0, y=150, z=250, unit="mm"
    )

    # Position vector from A to B
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force along cable with magnitude 30 N
    F = create_vector_along(
        r_AB, magnitude=30, unit="N", name="F"
    )

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-259.81, v=-350, w=400, unit="mm")
        F = create_vector_cartesian(u=-13.2, v=-17.7, w=20.3, unit="N")

        # Magnitude of position vector
        assert are_close_enough(r_AB.magnitude, Q(592, "mm"), rtol=0.01)


class Chapter2Problem113(PositionVectorProblem):
    name = "Problem 2-113"
    description = """
    Determine the magnitudes of the components of F=600 N acting along and perpendicular to segment DE of the pipe assembly.
    """

    # Points on pipe assembly
    A = create_point_cartesian(x=0, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=2, z=0, unit="m")
    C = create_point_cartesian(x=2, y=2, z=-2, unit="m")
    D = create_point_cartesian(x=4, y=2, z=-2, unit="m")
    E = create_point_cartesian(x=4, y=5, z=-2, unit="m")


    # Position vectors
    r_EB = create_vector_from_points(E, B, name="r_EB")
    r_ED = create_vector_from_points(E, D, name="r_ED")

    # Force along EB with magnitude 600 N
    F_EB = create_vector_along(r_EB, magnitude=600, unit="N", name="F")

    # Get unit vector along ED
    u_ED = r_ED.unit_vector()

    # Component parallel to ED: F · u_ED (dot product)
    F_parallel = F_EB.dot(u_ED)

    # Component perpendicular to ED: |F × u_ED| (cross product magnitude)
    F_perpendicular = F_EB.cross(u_ED).magnitude

    # Expected values
    class expected:
        r_EB = create_vector_cartesian(u=-4, v=-3, w=2, unit="m")
        r_ED = create_vector_cartesian(u=0, v=-3, w=0, unit="m")
        F_EB = create_vector_cartesian(u=-445.66, v=-334.25, w=222.83, unit="N")

        F_parallel = Q(334, "N")
        F_perpendicular = Q(498, "N")

        # Magnitude checks
        assert are_close_enough(r_EB.magnitude, Q(5.385, "m"), rtol=0.01)


class Chapter2Problem114(PositionVectorProblem):
    name = "Problem 2-114"
    description = """
    Determine the angle θ between the two cables.
    """

    # Points
    A = create_point_cartesian(x=2, y=-3, z=3, unit="m")
    B = create_point_cartesian(x=0, y=3, z=0, unit="m")
    C = create_point_cartesian(x=-2, y=3, z=4, unit="m")

    # Position vectors from A
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Angle between cables using dot product
    theta = r_AB.angle_between(r_AC)

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-2, v=6, w=-3, unit="m")
        r_AC = create_vector_cartesian(u=-4, v=6, w=1, unit="m")
        theta = Q(36.4, "deg")


class Chapter2Problem115(PositionVectorProblem):
    name = "Problem 2-115"
    description = """
    Determine the magnitude of the projection of the force F_1 along cable AC.
    """

    # Points (same as Problem 2-114)
    A = create_point_cartesian(x=2, y=-3, z=3, unit="m")
    B = create_point_cartesian(x=0, y=3, z=0, unit="m")
    C = create_point_cartesian(x=-2, y=3, z=4, unit="m")

    # Position vectors from A
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force F_1 = 70 N along AB
    F_1 = create_vector_along(r_AB, magnitude=70, unit="N", name="F_1")

    # Projection of F_1 along AC: F_1 · u_AC
    F_1_AC = F_1.dot(r_AC.unit_vector())

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-2, v=6, w=-3, unit="m")
        r_AC = create_vector_cartesian(u=-4, v=6, w=1, unit="m")
        F_1 = create_vector_cartesian(u=-20, v=60, w=-30, unit="N")
        F_1_AC = Q(56.3, "N")


class Chapter2Problem116(PositionVectorProblem):
    name = "Problem 2-116"
    description = """
    Determine the angle θ between the y axis of the pole and the wire AB.
    """

    # Point A is at top of pole (0, 3, 0), B is at (2, 2, -2)
    A = create_point_cartesian(x=0, y=3, z=0, unit="ft")
    B = create_point_cartesian(x=2, y=2, z=-2, unit="ft")
    C = create_point_cartesian(x=0, y=0, z=0, unit="ft")

    # r_AC represents the y-axis direction (pole axis pointing down)
    r_AC = create_vector_from_points(A, C, name="r_AC")
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Angle between y-axis and wire AB
    theta = r_AC.angle_between(r_AB)

    # Expected values
    class expected:
        r_AC = create_vector_cartesian(u=0, v=-3, w=0, unit="ft")
        r_AB = create_vector_cartesian(u=2, v=-1, w=-2, unit="ft")
        theta = Q(70.5, "deg")


class Chapter2Problem117(PositionVectorProblem):
    name = "Problem 2-117"
    description = """
    Determine the magnitudes of the components of force F = {60i + 12j - 40k} N
    acting along and perpendicular to the axis of rod AB which is directed from
    point A(0,0,0) to point B(-3,-0.75,1) m. Also, find the projection along
    rod AC which is directed from A to C(-3,1,1.5) m.
    """

    A = create_point_cartesian(x=3, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=-0.75, z=1, unit="m")
    C = create_point_cartesian(x=0, y=1, z=1.5, unit="m")

    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force vector
    F = create_vector_cartesian(u=60, v=12, w=-40, unit="N")

  

    # Projections of F along AB and AC
    F_AB = F.dot(r_AB.unit_vector())
    F_AC = F.dot(r_AC.unit_vector())

    # Expected values
    class expected:
        F = create_vector_cartesian(u=60, v=12, w=-40, unit="N")
        r_AB = create_vector_cartesian(u=-3, v=-0.75, w=1, unit="m")
        r_AC = create_vector_cartesian(u=-3, v=1, w=1.5, unit="m")
        F_AB = Q(-70.5, "N")
        F_AC = Q(-65.1, "N")

class Chapter2Problem118(PositionVectorProblem):
    name = "Problem 2-118"
    description = """
    Determine the angle u between cables AB and AC.
    """

    A = create_point_cartesian(x=3, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=-0.75, z=1, unit="m")
    C = create_point_cartesian(x=0, y=1, z=1.5, unit="m")

    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force vector
    F = create_vector_cartesian(u=60, v=12, w=-40, unit="N")

    theta = r_AB.angle_between(r_AC)

    # Expected values
    class expected:
        F = create_vector_cartesian(u=60, v=12, w=-40, unit="N")
        r_AB = create_vector_cartesian(u=-3, v=-0.75, w=1, unit="m")
        r_AC = create_vector_cartesian(u=-3, v=1, w=1.5, unit="m")
        theta = Q(31, "deg")


class Chapter2Problem119(PositionVectorProblem):
    name = "Problem 2-119"
    description = """
    A force of F = {-40k} lb acts at the end of the pipe. Determine the magnitudes
    of the components F_1 and F_2 which are directed along the pipe's axis and
    perpendicular to it.
    """

    O = create_point_cartesian(x=0, y=0, z=0, unit="ft")
    A = create_point_cartesian(x=3, y=5, z=-3, unit="ft")

    # Pipe axis direction from O to A: r_OA = {3i + 5j - 3k}
    r_OA = create_vector_from_points(O, A, name="r_OA")

    # Force at end of pipe
    F = create_vector_cartesian(u=0, v=0, w=-40, unit="lbf", from_point=A)

    # Component along pipe axis: F_1 = F · u_OA
    F_1 = F.dot(r_OA.unit_vector())

    # Component perpendicular to pipe axis: F_2 = sqrt(F^2 - F_1^2)
    # Using cross product magnitude: F_2 = |F × u_OA|
    F_2 = F.cross(r_OA.unit_vector()).magnitude

    # Expected values
    class expected:
        r_OA = create_vector_cartesian(u=3, v=5, w=-3, unit="ft")
        F = create_vector_cartesian(u=0, v=0, w=-40, unit="lbf")
        F_1 = Q(18.3, "lbf")
        F_2 = Q(35.6, "lbf")


class Chapter2Problem120(PositionVectorProblem):
    name = "Problem 2-120"
    description = """
    Two cables exert forces on the pipe. Determine the magnitude of the projected
    component of F_1 along the line of action of F_2.
    """

    F_1 = create_vector_spherical(
        magnitude=30, unit="lbf",
        theta=-30, theta_wrt="+y",
        phi=-30, phi_wrt="xy"
    )

    F_2 = create_vector_direction_angles(
        magnitude=60, unit="lbf",
        alpha=..., beta=60, gamma=60,
        signs=(-1, 1, 1),
    )

    F_1_F2 = F_1.dot(F_2.unit_vector())

    # Expected values
    class expected:
        F_1 = create_vector_cartesian(u=12.990, v=22.5, w=-15.0, unit="lbf")
        F_1_F2 = Q(-5.44, "lbf")


class Chapter2Problem121(PositionVectorProblem):
    name = "Problem 2-121"
    description = """
    Determine the angle θ between the two cables attached to the pipe.
    """

    F_1 = create_vector_spherical(
        magnitude=30, unit="lbf",
        theta=-30, theta_wrt="+y",
        phi=-30, phi_wrt="xy"
    )

    F_2 = create_vector_direction_angles(
        magnitude=60, unit="lbf",
        alpha=..., beta=60, gamma=60,
        signs=(-1, 1, 1),
    )

    F_1_F2 = F_1.dot(F_2.unit_vector())

    # Angle between cables
    theta = F_1.angle_between(F_2)

    # Expected values
    class expected:
        # F_1 = create_vector_cartesian(u=0.4330, v=0.75, w=-0.5, unit="")
        # F_2 = create_vector_cartesian(u=-0.7071, v=0.5, w=0.5, unit="")
        theta = Q(100, "deg")


class Chapter2Problem122(PositionVectorProblem):
    name = "Problem 2-122"
    description = """
    Determine the angle θ between the cables AB and AC.
    """

    # Points
    A = create_point_cartesian(x=6, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=-1, z=2, unit="m")
    C = create_point_cartesian(x=0, y=1, z=3, unit="m")

    # Position vectors
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Angle between cables
    theta = r_AB.angle_between(r_AC)

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-6, v=-1, w=2, unit="m")
        r_AC = create_vector_cartesian(u=-6, v=1, w=3, unit="m")
        theta = Q(19.2, "deg")


class Chapter2Problem123(PositionVectorProblem):
    name = "Problem 2-123"
    description = """
    Determine the magnitude of the projected component of the force
    F = {400i - 200j + 500k} N acting along the cable BA.
    """

    # Points
    A = create_point_cartesian(x=6, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=-1, z=2, unit="m")

    # Position vector from B to A
    r_BA = create_vector_from_points(B, A, name="r_BA")

    # Force vector
    F = create_vector_cartesian(u=400, v=-200, w=500, unit="N")

    # Projection of F along BA: F · u_BA
    F_BA = F.dot(r_BA.unit_vector())

    # Expected values
    class expected:
        r_BA = create_vector_cartesian(u=6, v=1, w=-2, unit="m")
        F = create_vector_cartesian(u=400, v=-200, w=500, unit="N")
        F_BA = Q(187, "N")


class Chapter2Problem124(PositionVectorProblem):
    name = "Problem 2-124"
    description = """
    Determine the magnitude of the projected component of the force
    F = {400i - 200j + 500k} N acting along the cable CA.
    """

    # Points
    A = create_point_cartesian(x=6, y=0, z=0, unit="m")
    C = create_point_cartesian(x=0, y=1, z=3, unit="m")

    # Position vector from C to A
    r_CA = create_vector_from_points(C, A, name="r_CA")

    # Force vector
    F = create_vector_cartesian(u=400, v=-200, w=500, unit="N")

    # Projection of F along CA: F · u_CA
    F_CA = F.dot(r_CA.unit_vector())

    # Expected values
    class expected:
        r_CA = create_vector_cartesian(u=6, v=-1, w=-3, unit="m")
        F = create_vector_cartesian(u=400, v=-200, w=500, unit="N")
        F_CA = Q(162, "N")


class Chapter2Problem125(PositionVectorProblem):
    name = "Problem 2-125"
    description = """
    Determine the magnitude of the projection of force F = 600 N along the u axis.
    """

    # Points
    O = create_point_cartesian(x=0, y=0, z=0, unit="m")
    A = create_point_cartesian(x=-2, y=4, z=4, unit="m")

    # Position vector from O to A
    r_OA = create_vector_from_points(O, A, name="r_OA")

    # Force along OA with magnitude 600 N
    F = create_vector_along(r_OA, magnitude=600, unit="N", name="F")

    # u axis direction: u = sin(30°)i + cos(30°)j
    u_axis = create_vector_polar(magnitude=1, angle=60, unit="", name="u_axis")

    # Projection of F along u axis: F · u_axis
    F_u = F.dot(u_axis)

    # Expected values
    class expected:
        r_OA = create_vector_cartesian(u=-2, v=4, w=4, unit="m")
        F = create_vector_cartesian(u=-200, v=400, w=400, unit="N")
        F_u = Q(246, "N")


class Chapter2Problem126(PositionVectorProblem):
    name = "Problem 2-126"
    description = """
    Determine the magnitude of the projected component of the 100-lb force
    acting along the axis BC of the pipe.
    """

    # Points - B at origin, A at (-3, 0, 0), C at (6, 4, -2)
    # Force direction from A towards a point that gives r = {-6, 8, 2}
    A = create_point_cartesian(x=-3, y=0, z=0, unit="ft")
    B = create_point_cartesian(x=0, y=0, z=0, unit="ft")
    C = create_point_cartesian(x=6, y=4, z=-2, unit="ft")
    D = create_point_cartesian(x=0, y=12, z=0, unit="ft")  # for direction only

    # Position vector from B to C
    r_CD = create_vector_from_points(C, D, name="r_CD")
    r_BC = create_vector_from_points(B, C, name="r_BC")

    # Force direction vector (from A toward point giving {-6, 8, 2})
    F = create_vector_along(r_CD, magnitude=100, unit="lbf", name="F")

    # Projection of F along BC: F · u_BC
    F_BC = F.dot(r_BC.unit_vector())

    # Expected values
    class expected:
        r_BC = create_vector_cartesian(u=6, v=4, w=-2, unit="ft")
        F = create_vector_cartesian(u=-58.83, v=78.45, w=19.61, unit="lbf")
        F_BC = Q(-10.5, "lbf")


class Chapter2Problem127(PositionVectorProblem):
    name = "Problem 2-127"
    description = """
    Determine the angle θ between pipe segments BA and BC.
    """

    # Points
    A = create_point_cartesian(x=-3, y=0, z=0, unit="ft")
    B = create_point_cartesian(x=0, y=0, z=0, unit="ft")
    C = create_point_cartesian(x=6, y=4, z=-2, unit="ft")

    # Position vectors
    r_BA = create_vector_from_points(B, A, name="r_BA")
    r_BC = create_vector_from_points(B, C, name="r_BC")

    # Angle between pipe segments
    theta = r_BA.angle_between(r_BC)

    # Expected values
    class expected:
        r_BA = create_vector_cartesian(u=-3, v=0, w=0, unit="ft")
        r_BC = create_vector_cartesian(u=6, v=4, w=-2, unit="ft")
        theta = Q(143, "deg")


class Chapter2Problem128(PositionVectorProblem):
    name = "Problem 2-128"
    description = """
    Determine the angle θ between BA and BC.
    """

    # Points
    A = create_point_cartesian(x=0, y=-2, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0, z=0, unit="m")
    C = create_point_cartesian(x=3, y=4, z=-1, unit="m")

    # Position vectors
    r_BA = create_vector_from_points(B, A, name="r_BA")
    r_BC = create_vector_from_points(B, C, name="r_BC")

    # Angle between BA and BC
    theta = r_BA.angle_between(r_BC)

    # Expected values
    class expected:
        r_BA = create_vector_cartesian(u=0, v=-2, w=0, unit="m")
        r_BC = create_vector_cartesian(u=3, v=4, w=-1, unit="m")
        theta = Q(142, "deg")

class Chapter2Problem129(PositionVectorProblem):
    name = "Problem 2-129"
    description = """
    Determine the magnitude of the projected component of the 3 kN force acting along the axis BC of the pipe.
    """

    # Points
    A = create_point_cartesian(x=0, y=-2, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0, z=0, unit="m")
    C = create_point_cartesian(x=3, y=4, z=-1, unit="m")
    D = create_point_cartesian(x=8, y=0, z=0, unit="m")  # for direction only

    # Position vectors
    r_BC = create_vector_from_points(B, C, name="r_BC")
    r_CD = create_vector_from_points(C, D, name="r_CD")

    F = create_vector_along(r_CD, magnitude=3000, unit="N", name="F")

    # Projection of F along BC: F · u_BC
    F_BC = F.dot(r_BC.unit_vector())

    # Expected values
    class expected:
        r_BC = create_vector_cartesian(u=3, v=4, w=-1, unit="m")
        r_CD = create_vector_cartesian(u=5, v=-4, w=1, unit="m")
        F_BC = Q(-182, "N")


class Chapter2Problem130(PositionVectorProblem):
    name = "Problem 2-130"
    description = """
    Determine the angles θ and φ made between the axes OA of the flag pole
    and AB and AC, respectively, of each cable.
    """

    O = create_point_cartesian(x=0, y=0, z=0, unit="m")
    A = create_point_cartesian(x=0, y=4, z=3, unit="m")
    B = create_point_cartesian(x=1.5, y=0, z=6, unit="m")
    C = create_point_cartesian(x=-2, y=0, z=4, unit="m")

    # Position vectors from A
    r_AO = create_vector_from_points(A, O, name="r_AO")
    r_AB = create_vector_from_points(A, B, name="r_AB")
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Angles between pole axis and cables
    theta = r_AO.angle_between(r_AB)
    phi = r_AO.angle_between(r_AC)

    # Expected values
    class expected:
        r_AO = create_vector_cartesian(u=0, v=-4, w=-3, unit="m")
        r_AB = create_vector_cartesian(u=1.5, v=-4, w=3, unit="m")
        r_AC = create_vector_cartesian(u=-2, v=-4, w=1, unit="m")
        theta = Q(74.4, "deg")
        phi = Q(55.4, "deg")


class Chapter2Problem131(PositionVectorProblem):
    name = "Problem 2-131"
    description = """
    Determine the magnitudes of the components of F acting along and
    perpendicular to segment BC of the pipe assembly.
    """

    # Points on pipe assembly
    # B at (3, 4, 0), C at (7, 6, -4)
    B = create_point_cartesian(x=3, y=4, z=0, unit="ft")
    C = create_point_cartesian(x=7, y=6, z=-4, unit="ft")

    # Position vector from C to B (direction along BC)
    r_BC = create_vector_from_points(B, C, name="r_BC")

    # Force vector F = {30i - 45j + 50k} lb
    F = create_vector_cartesian(u=30, v=-45, w=50, unit="lbf", from_point=C)

    # Component parallel to BC: F · u_BC
    F_parallel = F.dot(r_BC.unit_vector())

    # Component perpendicular to BC: |F × u_BC|
    F_perpendicular = F.cross(r_BC.unit_vector()).magnitude

    # Expected values
    class expected:
        r_BC = create_vector_cartesian(u=4, v=2, w=-4, unit="ft")
        F = create_vector_cartesian(u=30, v=-45, w=50, unit="lbf")
        F_parallel = Q(-28.3, "lbf")
        F_perpendicular = Q(68.0, "lbf")


class Chapter2Problem132(PositionVectorProblem):
    name = "Problem 2-132"
    description = """
    Determine the magnitude of the projected component of F along AC.
    Express this component as a Cartesian vector.
    """

    # Points
    # A at origin, C at (7, 6, -4) ft
    A = create_point_cartesian(x=0, y=0, z=0, unit="ft")
    C = create_point_cartesian(x=7, y=6, z=-4, unit="ft")

    # Position vector from A to C
    r_AC = create_vector_from_points(A, C, name="r_AC")

    # Force vector F = {30i - 45j + 50k} lb
    F = create_vector_cartesian(u=30, v=-45, w=50, unit="lbf", from_point=C)

    # Projection of F along AC: F · u_AC
    F_AC = F.dot(r_AC.unit_vector())

    F_AC = create_vector_along(r_AC, magnitude=F_AC, name="F_AC")

    # Expected values
    class expected:
        r_AC = create_vector_cartesian(u=7, v=6, w=-4, unit="ft")
        F = create_vector_cartesian(u=30, v=-45, w=50, unit="lbf")
        F_AC = create_vector_cartesian(u=-18.0, v=-15.4, w=10.3, unit="lbf")


class Chapter2Problem133(PositionVectorProblem):
    name = "Problem 2-133"
    description = """
    Determine the angle θ between the pipe segments BA and BC.
    """

    # Points
    # B at (3, 4, 0), A at (0, 0, 0), C at (7, 6, -4) ft
    A = create_point_cartesian(x=0, y=0, z=0, unit="ft")
    B = create_point_cartesian(x=3, y=4, z=0, unit="ft")
    C = create_point_cartesian(x=7, y=6, z=-4, unit="ft")

    # Position vectors from B
    r_BA = create_vector_from_points(B, A, name="r_BA")
    r_BC = create_vector_from_points(B, C, name="r_BC")

    # Angle between pipe segments
    theta = r_BA.angle_between(r_BC)

    # Expected values
    class expected:
        r_BA = create_vector_cartesian(u=-3, v=-4, w=0, unit="ft")
        r_BC = create_vector_cartesian(u=4, v=2, w=-4, unit="ft")
        theta = Q(132, "deg")


class Chapter2Problem134(PositionVectorProblem):
    """
    Problem 2-134: Angle between force F and diagonal AB of crate.

    If the force F=100 N lies in the plane DBEC, which is parallel to the x-z plane,
    and makes an angle of 10° with the extended line DB as shown, determine the
    angle that F makes with the diagonal AB of the crate.
    """
    name = "Problem 2-134"
    description = """
    Determine the angle θ that F makes with the diagonal AB of the crate.
    F = 100 N lies in plane DBEC (parallel to x-z plane), 10° with extended line DB.
    """

    # Points on crate - A at (0.5, 0, 0), B at (0, 0.2, 0.2) m
    A = create_point_cartesian(x=0.5, y=0, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0.2, z=0.2, unit="m")

    # Position vector from A to B
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force vector F = -100cos(10°)i + 100sin(10°)k
    # F lies in plane parallel to x-z, at 10° from -x direction
    F = create_vector_polar(
        magnitude=100, unit="N",
        angle=10, plane="xz", wrt="-x",
        # from_point=B,
    )


    # Angle between F and AB
    theta = F.angle_between(r_AB)

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-0.5, v=0.2, w=0.2, unit="m")
        F = create_vector_cartesian(u=-98.48, v=0, w=17.36, unit="N")
        theta = Q(23.4, "deg")


class Chapter2Problem135(PositionVectorProblem):
    name = "Problem 2-135"
    description = """
    Determine the magnitudes of the components of force F=90 lb acting parallel
    and perpendicular to diagonal AB of the crate.
    """

    # Points on crate - A at (1.5, 0, 0), B at (0, 3, 1) ft
    A = create_point_cartesian(x=1.5, y=0, z=0, unit="ft")
    B = create_point_cartesian(x=0, y=3, z=1, unit="ft")

    # Position vector from A to B
    r_AB = create_vector_from_points(A, B, name="r_AB")

    # Force vector F = 90(-cos60°sin45° i + cos60°cos45° j + sin60° k)
    # = {-31.82i + 31.82j + 77.94k} lb
    F = create_vector_spherical(
        magnitude=90, unit="lbf",
        theta=45, theta_wrt="+y",
        phi=60, phi_wrt="xy",
        # from_point=B,
    )
    

    # Component parallel to AB: F · u_AB
    F_parallel = F.dot(r_AB.unit_vector())

    # Component perpendicular to AB: |F × u_AB|
    F_perpendicular = F.cross(r_AB.unit_vector()).magnitude

    # Expected values
    class expected:
        r_AB = create_vector_cartesian(u=-1.5, v=3, w=1, unit="ft")
        F = create_vector_cartesian(u=-31.82, v=31.82, w=77.94, unit="lbf")
        F_parallel = Q(63.2, "lbf")
        F_perpendicular = Q(64.1, "lbf")


class Chapter2Problem136(PositionVectorProblem):
    name = "Problem 2-136"
    description = """
    Determine the magnitudes of the projected components of the force F=300 N
    acting along the x and y axes.
    """

    # Force vector F = -300sin30°sin30° i + 300cos30° j + 300sin30°cos30° k
    # F = {-75i + 259.81j + 129.90k} N
# Define the inclined plane (-30° from +z toward +x)

    A = create_point_polar(
        r=300, angle=-30, plane="xz", wrt="+z", unit="mm", offset=(-300, 300, 0)
    )

    plane = create_plane_rotated_y(
        angle=-30, name="inclined_plane",
        start_plane="zy")

    # Define force F at 30° from +y axis within the plane
    F = create_vector_in_plane(
        plane,
        magnitude=300,
        angle=30,
        from_axis="+y",
        unit="N",
        name="F"
    )

    # F = create_vector_cartesian(
    #     u=-300 * math.sin(math.radians(30)) * math.sin(math.radians(30)),
    #     v=300 * math.cos(math.radians(30)),
    #     w=300 * math.sin(math.radians(30)) * math.cos(math.radians(30)),
    #     unit="N",
    #     name="F"
    # )

    # Unit vectors for x and y axes
    u_x = create_vector_cartesian(u=1, v=0, w=0, unit="")
    u_y = create_vector_cartesian(u=0, v=1, w=0, unit="")

    # Projections along axes (magnitudes)
    F_x = F.dot(u_x)
    F_y = F.dot(u_y)

    # Expected values
    class expected:
        F = create_vector_cartesian(u=-75, v=259.81, w=129.90, unit="N")
        F_x = Q(-75, "N")
        F_y = Q(260, "N")

class Chapter2Problem137(PositionVectorProblem):
    name = "Problem 2-137"
    description = """
    Determine the magnitude of the projected component of the force F = 300 N acting along line OA.
    """

    # Force vector F = -300sin30°sin30° i + 300cos30° j + 300sin30°cos30° k
    # F = {-75i + 259.81j + 129.90k} N
# Define the inclined plane (-30° from +z toward +x)
    O = create_point_cartesian(x=0, y=0, z=0, unit="m")
    A = create_point_polar(
        r=300, angle=-30, plane="xz", wrt="+z", unit="mm", offset=(-300, 300, 0)
    )
    
    plane = create_plane_rotated_y(
        angle=-30, name="inclined_plane",
        start_plane="zy")

    # Define force F at 30° from +y axis within the plane
    F = create_vector_in_plane(
        plane,
        magnitude=300,
        angle=30,
        from_axis="+y",
        unit="N",
        name="F"
    )

    r_OA = create_vector_from_points(
        O,
        A,
    )

    # Projections along axes (magnitudes)
    F_OA = F.dot(r_OA.unit_vector())

    # Expected values
    class expected:
        F = create_vector_cartesian(u=-75, v=259.81, w=129.90, unit="N")
        F_OA = Q(242, "N")


class Chapter2Problem138(PositionVectorProblem):
    """
    Problem 2-138: Angle between two cables
    """

    name = "Problem 2-138"
    description = """
    Determine the angle θ between the two cables.
    """

    # Position vectors from A to C and A to B
    # r_AC = {2i - 8j + 10k} ft
    # r_AB = {-6i + 2j + 4k} ft
    r_AC = create_vector_cartesian(u=2, v=-8, w=10, unit="ft", name="r_AC")
    r_AB = create_vector_cartesian(u=-6, v=2, w=4, unit="ft", name="r_AB")

    # Angle between vectors using dot product
    # θ = cos⁻¹(r_AC · r_AB / (|r_AC| |r_AB|))
    theta = r_AC.angle_between(r_AB)

    # Expected values
    class expected:
        theta = Q(82.9, "degree")


class Chapter2Problem139(PositionVectorProblem):
    """
    Problem 2-139: Projected component of force along cable direction
    """

    name = "Problem 2-139"
    description = """
    Determine the projected component of the force F=12 lb acting in the
    direction of cable AC. Express the result as a Cartesian vector.
    """

    # Position vectors
    # r_AC = {2i - 8j + 10k} ft
    # r_AB = {-6i + 2j + 4k} ft
    r_AC = create_vector_cartesian(u=2, v=-8, w=10, unit="ft", name="r_AC")
    r_AB = create_vector_cartesian(u=-6, v=2, w=4, unit="ft", name="r_AB")

    # Force along AB with magnitude 12 lb
    F_AB = create_vector_along(r_AB, magnitude=12, unit="lbf", name="F_AB")

    # Unit vector along AC
    u_AC = r_AC.unit_vector()

    # Projected component magnitude: F_AB · u_AC
    proj_mag = F_AB.dot(u_AC)

    # Projected vector: (F_AB · u_AC) * u_AC
    proj_F_AB = create_vector_along(r_AC, magnitude=proj_mag, name="Proj_F_AB")

    # Expected values
    class expected:
        F_AB = create_vector_cartesian(u=-9.621, v=3.207, w=6.414, unit="lbf")
        proj_mag = Q(1.48, "lbf")
        proj_F_AB = create_vector_cartesian(u=0.229, v=-0.916, w=1.15, unit="lbf")


# =============================================================================
# Collect all problem classes for parametrized testing
# =============================================================================

PROBLEM_CLASSES = [
    Chapter2Problem106,
    Chapter2Problem107,
    Chapter2Problem108,
    Chapter2Problem109,
    Chapter2Problem110,
    Chapter2Problem111,
    Chapter2Problem113,
    Chapter2Problem114,
    Chapter2Problem115,
    Chapter2Problem116,
    Chapter2Problem117,
    Chapter2Problem118,
    Chapter2Problem119,
    Chapter2Problem120,
    Chapter2Problem121,
    Chapter2Problem122,
    Chapter2Problem123,
    Chapter2Problem124,
    Chapter2Problem125,
    Chapter2Problem126,
    Chapter2Problem127,
    Chapter2Problem128,
    Chapter2Problem129,
    Chapter2Problem130,
    Chapter2Problem131,
    Chapter2Problem132,
    Chapter2Problem133,
    Chapter2Problem134,
    Chapter2Problem135,
    Chapter2Problem136,
    Chapter2Problem137,
    Chapter2Problem138,
    Chapter2Problem139,
]


# =============================================================================
# Test function
# =============================================================================

@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_problems(problem_class):
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

        # Compare Quantity values (scalar results like F_parallel, F_perpendicular)
        elif hasattr(exp_val, 'value') and hasattr(exp_val, 'dim'):
            actual = getattr(source, attr_name, None)
            if actual is None:
                raise AssertionError(f"{attr_name} not found in problem class")

            assert are_close_enough(actual, exp_val, rtol=rtol), \
                f"{attr_name}: expected {exp_val}, got {actual}"


if __name__ == "__main__":
    # Run all tests
    for problem_class in PROBLEM_CLASSES:
        print(f"Testing {problem_class.name}...")
        test_problems(problem_class)
        print(f"✓ {problem_class.name} passed")
    print("\nAll tests passed!")
