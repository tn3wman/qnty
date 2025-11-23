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
from qnty.spatial.vectors import create_point_at_midpoint, create_vector_resultant, create_vector_with_magnitude

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


# =============================================================================
# Collect all problem classes for parametrized testing
# =============================================================================

PROBLEM_CLASSES = [
    Chapter2Problem86,
    Chapter2Problem87,
    Chapter2Problem88,
    Chapter2Problem89,
    Chapter2Problem90,
    # Chapter2Problem91,
    Chapter2Problem92,
    Chapter2Problem93,
    Chapter2Problem94,
    Chapter2Problem95,
    Chapter2Problem96,
    Chapter2Problem97,
    Chapter2Problem98,
    Chapter2Problem99,
    Chapter2Problem100,
    Chapter2Problem101,
    Chapter2Problem102,
    Chapter2Problem103,
    Chapter2Problem104,
    Chapter2Problem105,
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


if __name__ == "__main__":
    # Run all tests
    for problem_class in PROBLEM_CLASSES:
        print(f"Testing {problem_class.name}...")
        test_problems(problem_class)
        print(f"✓ {problem_class.name} passed")
    print("\nAll tests passed!")
