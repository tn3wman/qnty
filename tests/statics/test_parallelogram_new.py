"""
Comprehensive tests for parallelogram law problems using class-based problem definitions.

These tests validate:
- Force vector addition using parallelogram law
- Resultant force magnitude and direction
- Unknown force resolution
"""

import pytest

from qnty.problems.parallelogram_law import ParallelogramLawProblem
from qnty.spatial.vector import _Vector
from qnty.spatial.vectors import create_vector_cartesian, create_vector_polar, create_vector_resultant

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


# =============================================================================
# Problem class definitions
# =============================================================================

class Chapter2Problem1(ParallelogramLawProblem):
    name = "Problem 2-1"
    description = """
    If theta=60 degrees and F=450 N, determine the magnitude of the resultant force
    and its direction, measured counterclockwise from the positive x axis.
    """

    F_1 = create_vector_polar(
        magnitude=450, unit="N",
        angle=60, wrt="+x",
    )

    F_2 = create_vector_polar(
        magnitude=700, unit="N",
        angle=15, wrt="-x",
    )

    F_R = create_vector_resultant(F_1, F_2)

    class expected:
        F_R = create_vector_polar(
            magnitude=497.014, unit="N",
            angle=155.192, wrt="+x",
        )

    class report:
        pass

class Chapter2Problem1Mixed(ParallelogramLawProblem):
    name = "Problem 2-1 (Mixed Units)"
    description = """
    If theta=60 degrees and F=450 N, determine the magnitude of the resultant force
    and its direction, measured counterclockwise from the positive x axis.
    """

    F_1 = create_vector_polar(
        magnitude=450, unit="N",
        angle=60, wrt="+x",
    )

    F_2 = create_vector_polar(
        magnitude=700, unit="N",
        angle=15, wrt="-x",
    )

    F_R = create_vector_resultant(F_1, F_2)

    class expected:
        F_R = create_vector_polar(
            magnitude=497.014, unit="N",
            angle=155.192, wrt="+x",
        )

    class report:
        pass

# =============================================================================
# List of all problem classes for parameterized testing
# =============================================================================

PROBLEM_CLASSES = [
    Chapter2Problem1,
]


# =============================================================================
# Test function
# =============================================================================

@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_problems(problem_class):
    """Test parallelogram law problem by comparing computed values against expected."""
    rtol = 0.01

    # Instantiate problem to compute resultants
    problem = problem_class()
    source = problem

    expected = problem_class.expected

    # Compare same-named attributes
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue

        exp_val = getattr(expected, attr_name)

        # Compare _Vectors
        if isinstance(exp_val, _Vector):
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

            # Compare using is_close method
            assert actual_vec.is_close(exp_val, rtol=rtol), \
                f"{attr_name}: expected {exp_val}, got {actual}"
