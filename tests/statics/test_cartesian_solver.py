"""
Tests for rectangular method problems using the rectangular_solver.

These tests validate:
- Vector resolution into x and y components using rectangular (Cartesian) method
- Expected values are from textbook solutions (Hibbeler Statics)

Uses the solver: qnty.problems.statics.rectangular_solver
"""

import pytest

from qnty.linalg.vector2 import Vector, VectorUnknown
from qnty.problems.statics.cartesian_solver import solve_class
from tests.statics._problem_fixtures import RECTANGULAR_PROBLEMS

# =============================================================================
# Helper functions for assertions
# =============================================================================


def assert_components_close(actual: Vector, expected: Vector, rtol: float = 0.01, name: str = ""):
    """
    Assert that two vectors have close x and y components.

    Args:
        actual: Actual vector from solve result
        expected: Expected vector (from textbook/oracle, created via create_vectors_cartesian)
        rtol: Relative tolerance (default 1%)
        name: Name of the vector for error messages
    """
    actual_x = actual.x.magnitude()
    actual_y = actual.y.magnitude()
    expected_x = expected.x.magnitude()
    expected_y = expected.y.magnitude()

    # Compare x-components
    if expected_x == 0:
        assert abs(actual_x) < 1.0, f"{name}: x-component expected ~0, got {actual_x}"
    else:
        x_close = abs(actual_x - expected_x) <= rtol * abs(expected_x)
        assert x_close, (
            f"{name}: x-component not close enough.\n"
            f"  Actual:   {actual_x}\n"
            f"  Expected: {expected_x}\n"
            f"  Tolerance: {rtol * 100}%"
        )

    # Compare y-components
    if expected_y == 0:
        assert abs(actual_y) < 1.0, f"{name}: y-component expected ~0, got {actual_y}"
    else:
        y_close = abs(actual_y - expected_y) <= rtol * abs(expected_y)
        assert y_close, (
            f"{name}: y-component not close enough.\n"
            f"  Actual:   {actual_y}\n"
            f"  Expected: {expected_y}\n"
            f"  Tolerance: {rtol * 100}%"
        )


# =============================================================================
# Test functions
# =============================================================================


@pytest.mark.parametrize("problem_class", RECTANGULAR_PROBLEMS, ids=lambda c: c.name)
def test_rectangular_problem(problem_class):
    """Test rectangular method problem by comparing x/y components with expected values."""
    rtol = 0.01

    # Solve using the rectangular solver
    problem = solve_class(problem_class, output_unit="N")

    assert problem.result is not None, "Solve failed"
    assert len(problem.result.components) > 0, "No components resolved"

    # Get expected values
    expected = problem_class.expected

    # Compare each vector's components with expected
    for comp in problem.result.components:
        vec_name = comp.vector_name

        # Get expected vector (created via create_vectors_cartesian)
        expected_vec = getattr(expected, vec_name, None)
        if expected_vec is None:
            continue

        # Get actual vector from problem class
        actual_vec = None
        for attr_name in dir(problem_class):
            if attr_name.startswith('_'):
                continue
            attr = getattr(problem_class, attr_name)
            if isinstance(attr, (Vector, VectorUnknown)) and (attr.name == vec_name or attr_name == vec_name):
                actual_vec = attr
                break

        assert actual_vec is not None, f"Could not find actual vector {vec_name}"

        # For unknown vectors, use the solved component values
        if isinstance(actual_vec, VectorUnknown) and (actual_vec.magnitude is ... or actual_vec.angle is ...):
            # Compare solved component values with expected
            actual_x = comp.x_component.magnitude()
            actual_y = comp.y_component.magnitude()
            expected_x = expected_vec.x.magnitude()
            expected_y = expected_vec.y.magnitude()

            # Compare x-components
            if expected_x == 0:
                assert abs(actual_x) < 1.0, f"{vec_name}: x-component expected ~0, got {actual_x}"
            else:
                x_close = abs(actual_x - expected_x) <= rtol * abs(expected_x)
                assert x_close, (
                    f"{vec_name}: x-component not close enough.\n"
                    f"  Actual:   {actual_x}\n"
                    f"  Expected: {expected_x}\n"
                    f"  Tolerance: {rtol * 100}%"
                )

            # Compare y-components
            if expected_y == 0:
                assert abs(actual_y) < 1.0, f"{vec_name}: y-component expected ~0, got {actual_y}"
            else:
                y_close = abs(actual_y - expected_y) <= rtol * abs(expected_y)
                assert y_close, (
                    f"{vec_name}: y-component not close enough.\n"
                    f"  Actual:   {actual_y}\n"
                    f"  Expected: {expected_y}\n"
                    f"  Tolerance: {rtol * 100}%"
                )
        else:
            # For known vectors, compare using the vector's x/y properties
            assert_components_close(actual_vec, expected_vec, rtol=rtol, name=vec_name)
