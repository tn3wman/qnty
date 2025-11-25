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
        """Expected content for report generation tests."""

        class unknown_variables:
            """Expected unknown variables table data.

            Each entry represents a row in the unknown variables table with:
            - symbol: Variable name/symbol
            - magnitude: Expected magnitude value (or "?" if unknown before solve)
            - angle: Expected angle value in degrees (or "?" if unknown before solve)
            - unit: Expected unit symbol
            - reference: Angle reference (e.g., "+x", "-x")
            """
            F_R = {
                "symbol": "F_R",
                "magnitude": "?",
                "angle": "?",
                "unit": "N",
                "reference": "+x",
            }

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


# =============================================================================
# Report generation tests
# =============================================================================

# List of problem classes that have report expectations defined
REPORT_TEST_CLASSES = [
    Chapter2Problem1,
]


@pytest.mark.parametrize("problem_class", REPORT_TEST_CLASSES, ids=lambda c: c.name)
def test_report_unknown_variables_table(problem_class):
    """Test that the unknown variables table in reports matches expected data.

    This test verifies that the ReportBuilder generates the correct unknown
    variables table data before solving. The same data is used for both
    LaTeX and Markdown output, ensuring consistency.
    """
    from qnty.extensions.reporting.report_ir import ReportBuilder

    # Instantiate problem (this triggers vector extraction but not solving)
    problem = problem_class()

    # Get the report expectations
    report_expectations = getattr(problem_class, 'report', None)
    if report_expectations is None:
        pytest.skip("No report expectations defined")

    unknown_vars_expected = getattr(report_expectations, 'unknown_variables', None)
    if unknown_vars_expected is None:
        pytest.skip("No unknown_variables expectations defined")

    # Build the report IR to get the unknown variables table data
    # Note: We need to provide minimal data since problem isn't solved yet
    builder = ReportBuilder(
        problem=problem,
        known_variables={},  # Will be populated from problem.variables
        equations=[],
        solving_history=[],
        diagram_path=None
    )

    # Get the unknown variable data directly
    unknown_data = builder._get_unknown_variable_data()

    # Convert to dict keyed by symbol for easier comparison
    actual_by_symbol = {row['symbol']: row for row in unknown_data}

    # Compare each expected unknown variable
    for attr_name in dir(unknown_vars_expected):
        if attr_name.startswith('_'):
            continue

        expected_row = getattr(unknown_vars_expected, attr_name)
        if not isinstance(expected_row, dict):
            continue

        symbol = expected_row['symbol']
        assert symbol in actual_by_symbol, \
            f"Expected unknown variable '{symbol}' not found in report. " \
            f"Found: {list(actual_by_symbol.keys())}"

        actual_row = actual_by_symbol[symbol]

        # Compare each field
        for field in ['symbol', 'magnitude', 'angle', 'unit', 'reference']:
            if field in expected_row:
                assert actual_row.get(field) == expected_row[field], \
                    f"Unknown variable '{symbol}' field '{field}': " \
                    f"expected '{expected_row[field]}', got '{actual_row.get(field)}'"
