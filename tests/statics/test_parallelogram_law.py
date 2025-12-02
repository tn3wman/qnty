"""
Comprehensive tests for parallelogram law problems using the new parallelogram_solver.

These tests validate:
- Force vector addition using parallelogram law
- Resultant force magnitude and direction
- Report generation (known/unknown variables tables)

Uses the new solver: qnty.problems.statics.parallelogram_solver
"""

import pytest

from qnty.linalg.vector2 import Vector
from qnty.problems.statics.parallelogram_solver import (
    ParallelogramLawProblem,
    solve_class,
)

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


def assert_vectors_close(actual: Vector, expected: Vector, rtol: float = 0.01, name: str = ""):
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

    # Compare each expected vector with actual result
    expected = problem_class.expected
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue

        expected_vec = getattr(expected, attr_name)
        if not isinstance(expected_vec, Vector):
            continue

        # Get actual vector from the solved problem's vectors dict
        actual_vec = problem.vectors.get(attr_name)
        assert actual_vec is not None, f"Expected vector '{attr_name}' not found in problem.vectors. Available: {list(problem.vectors.keys())}"

        # Compare
        assert_vectors_close(actual_vec, expected_vec, rtol=rtol, name=attr_name)


# @pytest.mark.skip(reason="DTO serialization not yet implemented in new solver")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_dto_json_serializable(problem_class):
#     """Test that the result can be converted to JSON-serializable DTO."""
#     # NOTE: The new parallelogram_solver doesn't have DTO support yet
#     pytest.skip("DTO serialization not yet implemented in new solver")


# =============================================================================
# Report generation tests
# =============================================================================


# def _find_report_variable(variables_data: list[dict], symbol: str) -> dict | None:
#     """Find a variable by symbol in the report data."""
#     for var in variables_data:
#         if var.get("symbol") == symbol:
#             return var
#     return None


# @pytest.mark.skip(reason="Report tests need to be migrated to new parallelogram_report system")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_report_known_variables(problem_class):
#     """Test that report known variables match expected values."""
#     pytest.skip("Report tests need to be migrated to new parallelogram_report system")

#     # Create and solve the problem
#     class DynamicProblem(ParallelogramLawProblem):
#         name = getattr(problem_class, 'name', 'Test Problem')

#     for attr_name in dir(problem_class):
#         if attr_name.startswith('_'):
#             continue
#         attr = getattr(problem_class, attr_name)
#         if isinstance(attr, _Vector):
#             setattr(DynamicProblem, attr_name, attr)

#     problem = DynamicProblem()
#     problem.is_solved = True

#     # Build report IR and get known variables data
#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     known_data = builder._get_known_variable_data()

#     # Check each expected known variable
#     expected_known = problem_class.report.known_variables
#     for attr_name in dir(expected_known):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_known, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         actual = _find_report_variable(known_data, expected["symbol"])
#         assert actual is not None, f"Known variable '{expected['symbol']}' not found in report"

#         # Check unit
#         assert actual.get("unit") == expected["unit"], (
#             f"Known variable '{expected['symbol']}' unit mismatch: "
#             f"expected '{expected['unit']}', got '{actual.get('unit')}'"
#         )

#         # Check magnitude (as string, with tolerance for float comparison)
#         if "mag" in expected:
#             actual_mag = float(actual.get("magnitude", 0))
#             expected_mag = float(expected["mag"])
#             assert abs(actual_mag - expected_mag) < 0.1, (
#                 f"Known variable '{expected['symbol']}' magnitude mismatch: "
#                 f"expected {expected_mag}, got {actual_mag}"
#             )

#         # Check angle
#         if "angle" in expected:
#             actual_angle = float(actual.get("angle", 0))
#             expected_angle = float(expected["angle"])
#             assert abs(actual_angle - expected_angle) < 0.1, (
#                 f"Known variable '{expected['symbol']}' angle mismatch: "
#                 f"expected {expected_angle}, got {actual_angle}"
#             )

#         # Check X component (with tolerance)
#         if "x" in expected:
#             actual_x = float(actual.get("x", 0))
#             expected_x = float(expected["x"])
#             assert abs(actual_x - expected_x) < 1.0, (
#                 f"Known variable '{expected['symbol']}' X component mismatch: "
#                 f"expected {expected_x}, got {actual_x}"
#             )

#         # Check Y component (with tolerance)
#         if "y" in expected:
#             actual_y = float(actual.get("y", 0))
#             expected_y = float(expected["y"])
#             assert abs(actual_y - expected_y) < 1.0, (
#                 f"Known variable '{expected['symbol']}' Y component mismatch: "
#                 f"expected {expected_y}, got {actual_y}"
#             )

#         # Check reference
#         if "wrt" in expected:
#             assert actual.get("reference") == expected["wrt"], (
#                 f"Known variable '{expected['symbol']}' reference mismatch: "
#                 f"expected '{expected['wrt']}', got '{actual.get('reference')}'"
#             )


# @pytest.mark.skip(reason="Report tests need to be migrated to new parallelogram_report system")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_report_unknown_variables(problem_class):
#     """Test that report unknown variables match expected values."""
#     pytest.skip("Report tests need to be migrated to new parallelogram_report system")

#     # Create and solve the problem
#     class DynamicProblem(ParallelogramLawProblem):
#         name = getattr(problem_class, 'name', 'Test Problem')

#     for attr_name in dir(problem_class):
#         if attr_name.startswith('_'):
#             continue
#         attr = getattr(problem_class, attr_name)
#         if isinstance(attr, _Vector):
#             setattr(DynamicProblem, attr_name, attr)

#     problem = DynamicProblem()
#     problem.is_solved = True

#     # Build report IR and get unknown variables data
#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     unknown_data = builder._get_unknown_variable_data()

#     # Check each expected unknown variable
#     expected_unknown = problem_class.report.unknown_variables
#     for attr_name in dir(expected_unknown):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_unknown, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         actual = _find_report_variable(unknown_data, expected["symbol"])
#         assert actual is not None, f"Unknown variable '{expected['symbol']}' not found in report"

#         # Check that X, Y, magnitude, and angle are "?" for unknowns
#         if expected.get("x") == "?":
#             assert actual.get("x") == "?", (
#                 f"Unknown variable '{expected['symbol']}' X should be '?', got '{actual.get('x')}'"
#             )
#         if expected.get("y") == "?":
#             assert actual.get("y") == "?", (
#                 f"Unknown variable '{expected['symbol']}' Y should be '?', got '{actual.get('y')}'"
#             )
#         if expected.get("magnitude") == "?":
#             assert actual.get("magnitude") == "?", (
#                 f"Unknown variable '{expected['symbol']}' magnitude should be '?', got '{actual.get('magnitude')}'"
#             )
#         if expected.get("angle") == "?":
#             assert actual.get("angle") == "?", (
#                 f"Unknown variable '{expected['symbol']}' angle should be '?', got '{actual.get('angle')}'"
#             )

#         # Check reference (should still be known for resultant)
#         if "reference" in expected:
#             assert actual.get("reference") == expected["reference"], (
#                 f"Unknown variable '{expected['symbol']}' reference mismatch: "
#                 f"expected '{expected['reference']}', got '{actual.get('reference')}'"
#             )


# @pytest.mark.skip(reason="Report tests need to be migrated to new parallelogram_report system")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_report_equations(problem_class):
#     """Test that report equations match expected equations."""
#     pytest.skip("Report tests need to be migrated to new parallelogram_report system")
#     assert result.success, f"Solve failed: {result.error}"

#     # Get the problem from the result (it has solving_history populated)
#     problem = result._problem
#     assert problem is not None, "Result._problem should be populated"

#     # Build report IR and get equations
#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     equation_list = builder._format_equation_list()

#     # Check equation count
#     expected_equations = problem_class.report.equations
#     expected_count = getattr(expected_equations, 'count', 0)
#     assert len(equation_list) == expected_count, (
#         f"Expected {expected_count} equations, got {len(equation_list)}"
#     )

#     # Verify each expected equation matches exactly (in order)
#     # eq_1 should match equation_list[0], eq_2 should match equation_list[1], etc.
#     for i in range(1, expected_count + 1):
#         attr_name = f'eq_{i}'
#         expected_eq = getattr(expected_equations, attr_name, None)
#         if expected_eq is None:
#             continue

#         actual_eq = equation_list[i - 1]
#         assert actual_eq == expected_eq, (
#             f"Equation {i} mismatch:\n"
#             f"  Expected: {expected_eq!r}\n"
#             f"  Actual:   {actual_eq!r}"
#         )


# @pytest.mark.skip(reason="Report tests need to be migrated to new parallelogram_report system")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_report_steps(problem_class):
#     """Test that solution steps match expected step data."""
#     pytest.skip("Report tests need to be migrated to new parallelogram_report system")
#     assert result.success, f"Solve failed: {result.error}"

#     # Get the problem from the result (it has solving_history populated)
#     problem = result._problem
#     assert problem is not None, "Result._problem should be populated"

#     # Build report IR and get solution steps
#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     steps = builder._extract_solution_steps()

#     # Check step count
#     expected_steps = problem_class.report.steps
#     expected_count = getattr(expected_steps, 'count', 0)
#     assert len(steps) == expected_count, (
#         f"Expected {expected_count} steps, got {len(steps)}"
#     )

#     # Check each step
#     for i in range(1, expected_count + 1):
#         expected_step = getattr(expected_steps, f'step_{i}', None)
#         if expected_step is None:
#             continue

#         actual_step = steps[i - 1]  # Convert to 0-based index

#         # Check target (equation_name) matches exactly
#         if "target" in expected_step:
#             assert actual_step.equation_name == expected_step["target"], (
#                 f"Step {i} target mismatch:\n"
#                 f"  Expected: {expected_step['target']!r}\n"
#                 f"  Actual:   {actual_step.equation_name!r}"
#             )

#         # Check that the final line of substituted_equation contains expected result
#         if "final_line" in expected_step and actual_step.substituted_equation:
#             # Get the last line of the substituted equation
#             lines = actual_step.substituted_equation.strip().split('\n')
#             actual_final_line = lines[-1].strip() if lines else ""
#             expected_final = expected_step["final_line"]

#             assert actual_final_line == expected_final, (
#                 f"Step {i} final result mismatch:\n"
#                 f"  Expected: {expected_final!r}\n"
#                 f"  Actual:   {actual_final_line!r}\n"
#                 f"  Full substituted: {actual_step.substituted_equation!r}"
#             )


# @pytest.mark.skip(reason="Report tests need to be migrated to new parallelogram_report system")
# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES, ids=lambda c: c.name)
# def test_report_results(problem_class):
#     """Test that Summary of Results table matches expected values."""
#     pytest.skip("Report tests need to be migrated to new parallelogram_report system")
#     assert result.success, f"Solve failed: {result.error}"

#     # Get the problem from the result (it has solving_history populated)
#     problem = result._problem
#     assert problem is not None, "Result._problem should be populated"

#     # Build report IR and get results table
#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     results_table = builder._build_vector_results_table()

#     assert results_table is not None, "Results table should not be None for vector problems"

#     # Check each expected result
#     expected_results = problem_class.report.results
#     for attr_name in dir(expected_results):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_results, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         # Find the row matching the expected symbol
#         found_row = None
#         for row in results_table.rows:
#             if row.cells[0] == expected["symbol"]:
#                 found_row = row
#                 break

#         assert found_row is not None, (
#             f"Result '{expected['symbol']}' not found in results table"
#         )

#         # The results table has columns: Vector, Fₓ, Fᵧ, |F|, θ, Reference
#         # Cells order: [symbol, fx, fy, magnitude, angle, reference]

#         # Check X component (index 1)
#         if "x" in expected:
#             try:
#                 actual_x = float(found_row.cells[1])
#                 expected_x = float(expected["x"])
#                 assert abs(actual_x - expected_x) < 1.0, (
#                     f"Result '{expected['symbol']}' X component mismatch: "
#                     f"expected {expected_x}, got {actual_x}"
#                 )
#             except ValueError:
#                 pass  # Non-numeric value

#         # Check Y component (index 2)
#         if "y" in expected:
#             try:
#                 actual_y = float(found_row.cells[2])
#                 expected_y = float(expected["y"])
#                 assert abs(actual_y - expected_y) < 1.0, (
#                     f"Result '{expected['symbol']}' Y component mismatch: "
#                     f"expected {expected_y}, got {actual_y}"
#                 )
#             except ValueError:
#                 pass

#         # Check magnitude (index 3)
#         if "magnitude" in expected:
#             try:
#                 actual_mag = float(found_row.cells[3])
#                 expected_mag = float(expected["magnitude"])
#                 assert abs(actual_mag - expected_mag) < 1.0, (
#                     f"Result '{expected['symbol']}' magnitude mismatch: "
#                     f"expected {expected_mag}, got {actual_mag}"
#                 )
#             except ValueError:
#                 pass

#         # Check angle (index 4)
#         if "angle" in expected:
#             try:
#                 actual_angle = float(found_row.cells[4])
#                 expected_angle = float(expected["angle"])
#                 assert abs(actual_angle - expected_angle) < 1.0, (
#                     f"Result '{expected['symbol']}' angle mismatch: "
#                     f"expected {expected_angle}, got {actual_angle}"
#                 )
#             except ValueError:
#                 pass

#         # Check reference (index 5)
#         if "reference" in expected:
#             assert found_row.cells[5] == expected["reference"], (
#                 f"Result '{expected['symbol']}' reference mismatch: "
#                 f"expected '{expected['reference']}', got '{found_row.cells[5]}'"
#             )


# =============================================================================
# Golden file report tests
# =============================================================================





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
    result = pl.solve_class(problem_class, output_unit="N")
    assert result.success, f"Solve failed: {result.error}"

    expected = problem_class.expected
    for attr_name in dir(expected):
        if attr_name.startswith('_'):
            continue
        expected_vec = getattr(expected, attr_name)
        if not isinstance(expected_vec, _Vector):
            continue
        actual_vec = result.vectors.get(attr_name)
        assert actual_vec is not None
        assert_vectors_close(actual_vec, expected_vec, rtol=rtol, name=attr_name)


# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
# @pytest.mark.xfail(reason="Intentionally wrong known_variables to verify tests detect failures", strict=True)
# def test_report_known_variables_EXPECT_FAIL(problem_class):
#     """Test that WRONG known variables are detected as failures."""
#     from qnty.extensions.reporting.report_ir import ReportBuilder
#     from qnty.problems.parallelogram_law import ParallelogramLawProblem

#     class DynamicProblem(ParallelogramLawProblem):
#         name = getattr(problem_class, 'name', 'Test Problem')

#     for attr_name in dir(problem_class):
#         if attr_name.startswith('_'):
#             continue
#         attr = getattr(problem_class, attr_name)
#         if isinstance(attr, _Vector):
#             setattr(DynamicProblem, attr_name, attr)

#     problem = DynamicProblem()
#     problem.is_solved = True

#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     known_data = builder._get_known_variable_data()

#     expected_known = problem_class.report.known_variables
#     for attr_name in dir(expected_known):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_known, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         actual = _find_report_variable(known_data, expected["symbol"])
#         assert actual is not None

#         if "x" in expected:
#             actual_x = float(actual.get("x", 0))
#             expected_x = float(expected["x"])
#             assert abs(actual_x - expected_x) < 1.0


# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
# @pytest.mark.xfail(reason="Intentionally wrong unknown_variables to verify tests detect failures", strict=True)
# def test_report_unknown_variables_EXPECT_FAIL(problem_class):
#     """Test that WRONG unknown variables are detected as failures."""
#     from qnty.extensions.reporting.report_ir import ReportBuilder
#     from qnty.problems.parallelogram_law import ParallelogramLawProblem

#     class DynamicProblem(ParallelogramLawProblem):
#         name = getattr(problem_class, 'name', 'Test Problem')

#     for attr_name in dir(problem_class):
#         if attr_name.startswith('_'):
#             continue
#         attr = getattr(problem_class, attr_name)
#         if isinstance(attr, _Vector):
#             setattr(DynamicProblem, attr_name, attr)

#     problem = DynamicProblem()
#     problem.is_solved = True

#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     unknown_data = builder._get_unknown_variable_data()

#     expected_unknown = problem_class.report.unknown_variables
#     for attr_name in dir(expected_unknown):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_unknown, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         actual = _find_report_variable(unknown_data, expected["symbol"])
#         assert actual is not None

#         if "reference" in expected:
#             assert actual.get("reference") == expected["reference"]


# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
# @pytest.mark.xfail(reason="Intentionally wrong equations to verify tests detect failures", strict=True)
# def test_report_equations_EXPECT_FAIL(problem_class):
#     """Test that WRONG equations are detected as failures."""
#     from qnty.extensions.reporting.report_ir import ReportBuilder

#     result = pl.solve_class(problem_class, output_unit="N")
#     assert result.success

#     problem = result._problem
#     assert problem is not None

#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     equation_list = builder._format_equation_list()

#     expected_equations = problem_class.report.equations
#     expected_count = getattr(expected_equations, 'count', 0)
#     assert len(equation_list) == expected_count

#     for i in range(1, expected_count + 1):
#         attr_name = f'eq_{i}'
#         expected_eq = getattr(expected_equations, attr_name, None)
#         if expected_eq is None:
#             continue
#         actual_eq = equation_list[i - 1]
#         assert actual_eq == expected_eq


# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
# @pytest.mark.xfail(reason="Intentionally wrong steps to verify tests detect failures", strict=True)
# def test_report_steps_EXPECT_FAIL(problem_class):
#     """Test that WRONG steps are detected as failures."""
#     from qnty.extensions.reporting.report_ir import ReportBuilder

#     result = pl.solve_class(problem_class, output_unit="N")
#     assert result.success

#     problem = result._problem
#     assert problem is not None

#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     steps = builder._extract_solution_steps()

#     expected_steps = problem_class.report.steps
#     expected_count = getattr(expected_steps, 'count', 0)
#     assert len(steps) == expected_count

#     for i in range(1, expected_count + 1):
#         expected_step = getattr(expected_steps, f'step_{i}', None)
#         if expected_step is None:
#             continue

#         actual_step = steps[i - 1]

#         if "target" in expected_step:
#             assert actual_step.equation_name == expected_step["target"]

#         if "final_line" in expected_step and actual_step.substituted_equation:
#             lines = actual_step.substituted_equation.strip().split('\n')
#             actual_final_line = lines[-1].strip() if lines else ""
#             assert actual_final_line == expected_step["final_line"]


# @pytest.mark.parametrize("problem_class", PROBLEM_CLASSES_EXPECT_FAIL, ids=lambda c: c.name)
# @pytest.mark.xfail(reason="Intentionally wrong results to verify tests detect failures", strict=True)
# def test_report_results_EXPECT_FAIL(problem_class):
#     """Test that WRONG results are detected as failures."""
#     from qnty.extensions.reporting.report_ir import ReportBuilder

#     result = pl.solve_class(problem_class, output_unit="N")
#     assert result.success

#     problem = result._problem
#     assert problem is not None

#     builder = ReportBuilder(
#         problem=problem,
#         known_variables=problem.get_known_variables(),
#         equations=problem.equations,
#         solving_history=getattr(problem, "solving_history", []),
#         diagram_path=None
#     )
#     results_table = builder._build_vector_results_table()
#     assert results_table is not None

#     expected_results = problem_class.report.results
#     for attr_name in dir(expected_results):
#         if attr_name.startswith('_'):
#             continue
#         expected = getattr(expected_results, attr_name)
#         if not isinstance(expected, dict):
#             continue

#         found_row = None
#         for row in results_table.rows:
#             if row.cells[0] == expected["symbol"]:
#                 found_row = row
#                 break

#         assert found_row is not None

#         if "x" in expected:
#             actual_x = float(found_row.cells[1])
#             expected_x = float(expected["x"])
#             assert abs(actual_x - expected_x) < 1.0

#         if "magnitude" in expected:
#             actual_mag = float(found_row.cells[3])
#             expected_mag = float(expected["magnitude"])
#             assert abs(actual_mag - expected_mag) < 1.0
