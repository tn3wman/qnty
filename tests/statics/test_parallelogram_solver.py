"""
Comprehensive tests for parallelogram law problems using the new parallelogram_solver.

These tests validate:
- Force vector addition using parallelogram law
- Resultant force magnitude and direction
- Report generation (known/unknown variables tables)

Uses the new solver: qnty.problems.statics.parallelogram_solver
"""

import pytest

from qnty.linalg.vector2 import Vector, VectorUnknown
from qnty.problems.statics.parallelogram_solver import solve_class

# Import problem fixtures
from tests.statics._problem_fixtures import (
    GOLDEN_DIR,
    PARALLELOGRAM_LAW_PROBLEMS,
    PROBLEMS_EXPECT_FAIL,
    PROBLEMS_WITH_GOLDEN_FILES,
    get_golden_base,
    normalize_report,
)

# =============================================================================
# Helper functions for assertions
# =============================================================================


def assert_vectors_close(actual: Vector | VectorUnknown, expected: Vector, rtol: float = 0.01, name: str = ""):
    """
    Assert that two polar vectors are close within tolerance.

    Compares vectors by magnitude and angle (from the same wrt axis).

    Args:
        actual: Actual vector from solve result
        expected: Expected vector (from textbook/oracle)
        rtol: Relative tolerance (default 1%)
        name: Name of the vector for error messages
    """
    assert isinstance(actual, Vector), f"{name}: expected Vector, got {type(actual)}"
    assert isinstance(expected, Vector), f"{name}: expected Vector for comparison, got {type(expected)}"

    # Compare magnitudes
    actual_mag = actual.magnitude.value
    expected_mag = expected.magnitude.value
    assert actual_mag is not None, f"{name}: actual magnitude is None"
    assert expected_mag is not None, f"{name}: expected magnitude is None"

    mag_close = abs(actual_mag - expected_mag) <= rtol * abs(expected_mag)
    assert mag_close, (
        f"{name}: magnitude not close enough.\n"
        f"  Actual:   {actual_mag}\n"
        f"  Expected: {expected_mag}\n"
        f"  Tolerance: {rtol * 100}%"
    )

    # Compare angles
    actual_angle = actual.angle.value
    expected_angle = expected.angle.value
    assert actual_angle is not None, f"{name}: actual angle is None"
    assert expected_angle is not None, f"{name}: expected angle is None"

    # Angle tolerance in radians (convert rtol to absolute tolerance for angles)
    angle_atol = 0.1  # About 5.7 degrees tolerance
    angle_close = abs(actual_angle - expected_angle) <= angle_atol
    assert angle_close, (
        f"{name}: angle not close enough.\n"
        f"  Actual:   {actual_angle} rad\n"
        f"  Expected: {expected_angle} rad\n"
        f"  Tolerance: {angle_atol} rad"
    )

    # Compare wrt reference
    assert actual.wrt == expected.wrt, (
        f"{name}: wrt reference mismatch.\n"
        f"  Actual:   {actual.wrt}\n"
        f"  Expected: {expected.wrt}"
    )


# =============================================================================
# Problem class lists for parameterized testing
# =============================================================================

PROBLEM_CLASSES = PARALLELOGRAM_LAW_PROBLEMS

PROBLEM_CLASSES_EXPECT_FAIL = PROBLEMS_EXPECT_FAIL


# =============================================================================
# Test functions
# =============================================================================


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
def test_problem(problem_class):
    """Test parallelogram law problem by comparing all expected vectors."""
    rtol = 0.01

    # Solve using the new solver (returns ParallelogramLawProblem instance)
    problem = solve_class(problem_class, output_unit="N")

    assert problem.is_solved, "Solve failed"

    # Build context from expected vectors for resolving string name references (like wrt="F_2")
    expected = problem_class.expected
    expected_context = {}
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue
        attr = getattr(expected, attr_name)
        if isinstance(attr, (Vector, VectorUnknown)):
            expected_context[attr_name] = attr

    # Compare each expected vector with actual result
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue

        expected_vec = getattr(expected, attr_name)
        if not isinstance(expected_vec, Vector):
            continue

        # Get actual vector from the solved problem's vectors dict
        actual_vec = problem.vectors.get(attr_name)
        assert actual_vec is not None, f"Expected vector '{attr_name}' not found in problem.vectors. Available: {list(problem.vectors.keys())}"

        # Compare using Vector.is_close which compares magnitude and absolute angle with tolerance
        # Pass expected_context to resolve string name references in expected vectors
        assert actual_vec.is_close(expected_vec, rtol=rtol, context=expected_context), (
            f"{attr_name}: vectors not close.\n"
            f"  Actual:   {actual_vec}\n"
            f"  Expected: {expected_vec}"
        )

@pytest.mark.parametrize("problem_class", PROBLEMS_WITH_GOLDEN_FILES, ids=lambda c: c.name)
def test_report_markdown_matches_golden(problem_class, tmp_path):
    """Test that generated markdown report matches the golden file."""
    # Solve the problem
    problem = solve_class(problem_class, output_unit="N")
    assert problem.is_solved, "Problem failed to solve"

    # Generate markdown report to temp file
    md_path = tmp_path / "report.md"
    problem.generate_report(str(md_path), format="markdown")

    # Read and normalize generated report
    generated = md_path.read_text(encoding="utf-8")
    generated_normalized = normalize_report(generated)

    # Read golden file
    golden_base = get_golden_base(problem_class)
    golden_path = GOLDEN_DIR / f"{golden_base}.md"
    assert golden_path.exists(), f"Golden file not found: {golden_path}"
    golden = golden_path.read_text(encoding="utf-8")

    # Compare normalized content
    assert generated_normalized == golden, (
        f"Generated markdown does not match golden file.\n"
        f"Golden: {golden_path}\n"
        f"To update golden files, run: python tests/statics/_problem_fixtures.py --regenerate-golden"
    )


@pytest.mark.parametrize("problem_class", PROBLEMS_WITH_GOLDEN_FILES, ids=lambda c: c.name)
def test_report_latex_matches_golden(problem_class, tmp_path):
    """Test that generated LaTeX report matches the golden file."""
    # Solve the problem
    problem = solve_class(problem_class, output_unit="N")
    assert problem.is_solved, "Problem failed to solve"

    # Generate LaTeX report to temp file
    tex_path = tmp_path / "report.tex"
    problem.generate_report(str(tex_path), format="latex")

    # Read and normalize generated report
    generated = tex_path.read_text(encoding="utf-8")
    generated_normalized = normalize_report(generated)

    # Read golden file
    golden_base = get_golden_base(problem_class)
    golden_path = GOLDEN_DIR / f"{golden_base}.tex"
    assert golden_path.exists(), f"Golden file not found: {golden_path}"
    golden = golden_path.read_text(encoding="utf-8")

    # Compare normalized content
    assert generated_normalized == golden, (
        f"Generated LaTeX does not match golden file.\n"
        f"Golden: {golden_path}\n"
        f"To update golden files, run: python tests/statics/_problem_fixtures.py --regenerate-golden"
    )


# =============================================================================
# Tests that are EXPECTED TO FAIL (to verify test correctness)
# These use the WRONG problem class with intentionally incorrect expected values
# =============================================================================


@pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
@pytest.mark.xfail(reason="Intentionally wrong expected values to verify tests detect failures", strict=True)
def test_problem_EXPECT_FAIL(problem_class):
    """Test that WRONG expected vectors are detected as failures."""
    rtol = 0.01
    problem = solve_class(problem_class, output_unit="N")
    assert problem.is_solved, "Solve failed"

    expected = problem_class.expected
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue
        expected_vec = getattr(expected, attr_name)
        if not isinstance(expected_vec, Vector):
            continue
        actual_vec = problem.vectors.get(attr_name)
        assert actual_vec is not None
        assert_vectors_close(actual_vec, expected_vec, rtol=rtol, name=attr_name)
