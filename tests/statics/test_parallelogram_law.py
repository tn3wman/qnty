"""
Comprehensive tests for parallelogram law problems using the unified API.

These tests validate:
- Force vector addition using parallelogram law
- Resultant force magnitude and direction
- JSON serialization for frontend integration
- Report generation (known/unknown variables tables)

Uses the unified API: qnty.problems.statics.parallelogram_law
"""

import pytest

from qnty.problems.statics import parallelogram_law as pl
from qnty.spatial.vector import _Vector

# =============================================================================
# Helper functions for assertions
# =============================================================================


def assert_vectors_close(actual: _Vector, expected: _Vector, rtol: float = 0.01, name: str = ""):
    """
    Assert that two vectors are close within tolerance.

    Compares vectors using their is_close method which handles
    magnitude and direction comparison.

    Args:
        actual: Actual vector from solve result
        expected: Expected vector (from textbook/oracle)
        rtol: Relative tolerance (default 1%)
        name: Name of the vector for error messages
    """
    assert isinstance(actual, _Vector), f"{name}: expected _Vector, got {type(actual)}"
    assert isinstance(expected, _Vector), f"{name}: expected _Vector for comparison, got {type(expected)}"

    assert actual.is_close(expected, rtol=rtol), (
        f"{name}: vectors not close enough.\n"
        f"  Actual:   {actual}\n"
        f"  Expected: {expected}"
    )


# =============================================================================
# Problem class definitions using Unified API
# =============================================================================


class Chapter2Problem1:
    name = "Problem 2-1"

    # Input vectors using unified API
    F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
    F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
    F_R = pl.create_vector_resultant(F_1, F_2)

    # Expected values (from textbook)
    class expected:
        F_1 = pl.create_vector_polar(magnitude=450, unit="N", angle=60, wrt="+x")
        F_2 = pl.create_vector_polar(magnitude=700, unit="N", angle=15, wrt="-x")
        F_R = pl.create_vector_polar(magnitude=497.014, unit="N", angle=155.192, wrt="+x")

    class report:
        """Expected content for report generation tests."""

        class known_variables:
            """Expected known variables table data."""
            F_1 = {
                "symbol": "F_1", "unit": "N",
                "x": 225.0, "y": 389.7, "mag": 450, "angle": 60, "wrt": "+x"
            }
            F_2 = {
                "symbol": "F_2", "unit": "N",
                "x": -676.1, "y": -181.2, "mag": 700, "angle": 15, "wrt": "-x"
            }

        class unknown_variables:
            """Expected unknown variables table data."""
            F_R = {
                "symbol": "F_R", "unit": "N",
                "x": "?", "y": "?", "magnitude": "?", "angle": "?", "reference": "+x",
            }


# =============================================================================
# List of all problem classes for parameterized testing
# =============================================================================

PROBLEM_CLASSES = [
    Chapter2Problem1,
]


# =============================================================================
# Test functions
# =============================================================================


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_problem(problem_class):
    """Test parallelogram law problem by comparing all expected vectors."""
    rtol = 0.01

    # Solve using the class - preserves attribute names
    result = pl.solve_class(problem_class, output_unit="N")

    assert result.success, f"Solve failed: {result.error}"

    # Compare each expected vector with actual result
    expected = problem_class.expected
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue

        expected_vec = getattr(expected, attr_name)
        if not isinstance(expected_vec, _Vector):
            continue

        # Get actual vector from result
        actual_vec = result.vectors.get(attr_name)
        assert actual_vec is not None, f"Expected vector '{attr_name}' not found in result.vectors. Available: {list(result.vectors.keys())}"

        # Compare
        assert_vectors_close(actual_vec, expected_vec, rtol=rtol, name=attr_name)


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_dto_json_serializable(problem_class):
    """Test that the result can be converted to JSON-serializable DTO."""
    import json
    from dataclasses import asdict

    result = pl.solve_class(problem_class, output_unit="N")
    dto = result.to_dto()

    # Should not raise
    json_str = json.dumps(asdict(dto), default=str)
    assert json_str is not None
    assert "resultant" in json_str
    assert dto.success is True


# =============================================================================
# Report generation tests
# =============================================================================


def _find_report_variable(variables_data: list[dict], symbol: str) -> dict | None:
    """Find a variable by symbol in the report data."""
    for var in variables_data:
        if var.get("symbol") == symbol:
            return var
    return None


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_report_known_variables(problem_class):
    """Test that report known variables match expected values."""
    if not hasattr(problem_class, 'report') or not hasattr(problem_class.report, 'known_variables'):
        pytest.skip("Problem class does not define report.known_variables")

    from qnty.extensions.reporting.report_ir import ReportBuilder
    from qnty.problems.parallelogram_law import ParallelogramLawProblem

    # Create and solve the problem
    class DynamicProblem(ParallelogramLawProblem):
        name = getattr(problem_class, 'name', 'Test Problem')

    for attr_name in dir(problem_class):
        if attr_name.startswith('_'):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, _Vector):
            setattr(DynamicProblem, attr_name, attr)

    problem = DynamicProblem()
    problem.is_solved = True

    # Build report IR and get known variables data
    builder = ReportBuilder(
        problem=problem,
        known_variables=problem.get_known_variables(),
        equations=problem.equations,
        solving_history=getattr(problem, "solving_history", []),
        diagram_path=None
    )
    known_data = builder._get_known_variable_data()

    # Check each expected known variable
    expected_known = problem_class.report.known_variables
    for attr_name in dir(expected_known):
        if attr_name.startswith('_'):
            continue
        expected = getattr(expected_known, attr_name)
        if not isinstance(expected, dict):
            continue

        actual = _find_report_variable(known_data, expected["symbol"])
        assert actual is not None, f"Known variable '{expected['symbol']}' not found in report"

        # Check unit
        assert actual.get("unit") == expected["unit"], (
            f"Known variable '{expected['symbol']}' unit mismatch: "
            f"expected '{expected['unit']}', got '{actual.get('unit')}'"
        )

        # Check magnitude (as string, with tolerance for float comparison)
        if "mag" in expected:
            actual_mag = float(actual.get("magnitude", 0))
            expected_mag = float(expected["mag"])
            assert abs(actual_mag - expected_mag) < 0.1, (
                f"Known variable '{expected['symbol']}' magnitude mismatch: "
                f"expected {expected_mag}, got {actual_mag}"
            )

        # Check angle
        if "angle" in expected:
            actual_angle = float(actual.get("angle", 0))
            expected_angle = float(expected["angle"])
            assert abs(actual_angle - expected_angle) < 0.1, (
                f"Known variable '{expected['symbol']}' angle mismatch: "
                f"expected {expected_angle}, got {actual_angle}"
            )

        # Check X component (with tolerance)
        if "x" in expected:
            actual_x = float(actual.get("x", 0))
            expected_x = float(expected["x"])
            assert abs(actual_x - expected_x) < 1.0, (
                f"Known variable '{expected['symbol']}' X component mismatch: "
                f"expected {expected_x}, got {actual_x}"
            )

        # Check Y component (with tolerance)
        if "y" in expected:
            actual_y = float(actual.get("y", 0))
            expected_y = float(expected["y"])
            assert abs(actual_y - expected_y) < 1.0, (
                f"Known variable '{expected['symbol']}' Y component mismatch: "
                f"expected {expected_y}, got {actual_y}"
            )

        # Check reference
        if "wrt" in expected:
            assert actual.get("reference") == expected["wrt"], (
                f"Known variable '{expected['symbol']}' reference mismatch: "
                f"expected '{expected['wrt']}', got '{actual.get('reference')}'"
            )


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_report_unknown_variables(problem_class):
    """Test that report unknown variables match expected values."""
    if not hasattr(problem_class, 'report') or not hasattr(problem_class.report, 'unknown_variables'):
        pytest.skip("Problem class does not define report.unknown_variables")

    from qnty.extensions.reporting.report_ir import ReportBuilder
    from qnty.problems.parallelogram_law import ParallelogramLawProblem

    # Create and solve the problem
    class DynamicProblem(ParallelogramLawProblem):
        name = getattr(problem_class, 'name', 'Test Problem')

    for attr_name in dir(problem_class):
        if attr_name.startswith('_'):
            continue
        attr = getattr(problem_class, attr_name)
        if isinstance(attr, _Vector):
            setattr(DynamicProblem, attr_name, attr)

    problem = DynamicProblem()
    problem.is_solved = True

    # Build report IR and get unknown variables data
    builder = ReportBuilder(
        problem=problem,
        known_variables=problem.get_known_variables(),
        equations=problem.equations,
        solving_history=getattr(problem, "solving_history", []),
        diagram_path=None
    )
    unknown_data = builder._get_unknown_variable_data()

    # Check each expected unknown variable
    expected_unknown = problem_class.report.unknown_variables
    for attr_name in dir(expected_unknown):
        if attr_name.startswith('_'):
            continue
        expected = getattr(expected_unknown, attr_name)
        if not isinstance(expected, dict):
            continue

        actual = _find_report_variable(unknown_data, expected["symbol"])
        assert actual is not None, f"Unknown variable '{expected['symbol']}' not found in report"

        # Check that X, Y, magnitude, and angle are "?" for unknowns
        if expected.get("x") == "?":
            assert actual.get("x") == "?", (
                f"Unknown variable '{expected['symbol']}' X should be '?', got '{actual.get('x')}'"
            )
        if expected.get("y") == "?":
            assert actual.get("y") == "?", (
                f"Unknown variable '{expected['symbol']}' Y should be '?', got '{actual.get('y')}'"
            )
        if expected.get("magnitude") == "?":
            assert actual.get("magnitude") == "?", (
                f"Unknown variable '{expected['symbol']}' magnitude should be '?', got '{actual.get('magnitude')}'"
            )
        if expected.get("angle") == "?":
            assert actual.get("angle") == "?", (
                f"Unknown variable '{expected['symbol']}' angle should be '?', got '{actual.get('angle')}'"
            )

        # Check reference (should still be known for resultant)
        if "reference" in expected:
            assert actual.get("reference") == expected["reference"], (
                f"Unknown variable '{expected['symbol']}' reference mismatch: "
                f"expected '{expected['reference']}', got '{actual.get('reference')}'"
            )
