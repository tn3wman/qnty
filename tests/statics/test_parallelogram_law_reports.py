"""
Snapshot tests for parallelogram law report generation.

These tests verify that generated reports (Markdown and LaTeX) match
golden truth files stored in the `golden/` directory. This ensures
report generation remains stable and any changes are intentional.

The golden files use placeholders for dynamic content:
- {{GENERATED_DATETIME}} - Full datetime in format "YYYY-MM-DD HH:MM:SS"
- {{GENERATED_DATE}} - Date in format "Month DD, YYYY"

These placeholders are substituted during comparison to allow for
time-independent testing.

To regenerate golden files when report generation changes intentionally:
    python tests/statics/_problem_fixtures.py --regenerate-golden
"""

import tempfile
from pathlib import Path

import pytest

from qnty.problems.statics import parallelogram_law as pl

# Import shared problem fixtures and utilities
from tests.statics._problem_fixtures import (
    GOLDEN_DIR,
    PROBLEMS_WITH_GOLDEN_FILES,
    get_golden_base,
    normalize_report,
)

# =============================================================================
# Test fixtures and utilities
# =============================================================================


def assert_reports_match(actual: str, expected: str, format_name: str = "report") -> None:
    """
    Assert that two reports match after normalization.

    Provides detailed diff information on failure.

    Args:
        actual: Generated report content
        expected: Expected (golden) report content
        format_name: Name of format for error messages
    """
    actual_normalized = normalize_report(actual)
    expected_normalized = normalize_report(expected)

    if actual_normalized != expected_normalized:
        # Find first difference for helpful error message
        actual_lines = actual_normalized.splitlines()
        expected_lines = expected_normalized.splitlines()

        first_diff_line = None
        for i, (a, e) in enumerate(zip(actual_lines, expected_lines, strict=False)):
            if a != e:
                first_diff_line = i + 1
                break

        if first_diff_line is None and len(actual_lines) != len(expected_lines):
            first_diff_line = min(len(actual_lines), len(expected_lines)) + 1

        # Build a helpful diff message
        msg_parts = [f"{format_name} does not match golden file."]

        if first_diff_line:
            msg_parts.append(f"First difference at line {first_diff_line}:")

            # Show context around the difference
            start = max(0, first_diff_line - 3)
            end = min(max(len(actual_lines), len(expected_lines)), first_diff_line + 2)

            msg_parts.append("\nExpected:")
            for i in range(start, min(end, len(expected_lines))):
                prefix = ">>> " if i == first_diff_line - 1 else "    "
                msg_parts.append(f"{prefix}{i+1}: {expected_lines[i]}")

            msg_parts.append("\nActual:")
            for i in range(start, min(end, len(actual_lines))):
                prefix = ">>> " if i == first_diff_line - 1 else "    "
                msg_parts.append(f"{prefix}{i+1}: {actual_lines[i]}")

        pytest.fail("\n".join(msg_parts))


# =============================================================================
# Parameterized tests for all problems
# =============================================================================


@pytest.mark.parametrize("problem_class", PROBLEMS_WITH_GOLDEN_FILES, ids=lambda p: p.name)
class TestParallelogramLawReports:
    """Parameterized snapshot tests for parallelogram law report generation."""

    @pytest.fixture
    def solved_result(self, problem_class):
        """Solve the problem and return the result."""
        return pl.solve_class(problem_class, output_unit="N")

    @pytest.fixture
    def golden_base(self, problem_class):
        """Get the golden file base name for this problem."""
        return get_golden_base(problem_class)

    def test_solve_succeeds(self, solved_result):
        """Verify the problem solves successfully."""
        assert solved_result.success, f"Solve failed: {solved_result.error}"

    def test_markdown_report_matches_golden(self, solved_result, golden_base):
        """Test that generated Markdown report matches golden file."""
        # Generate report to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = Path(f.name)

        try:
            solved_result.generate_report(temp_path, format="markdown")
            actual = temp_path.read_text(encoding="utf-8")
        finally:
            temp_path.unlink(missing_ok=True)

        # Load golden file
        golden_path = GOLDEN_DIR / f"{golden_base}.md"
        assert golden_path.exists(), f"Golden file not found: {golden_path}"
        expected = golden_path.read_text(encoding="utf-8")

        # Compare
        assert_reports_match(actual, expected, "Markdown report")

    def test_latex_report_matches_golden(self, solved_result, golden_base):
        """Test that generated LaTeX report matches golden file."""
        # Generate report to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            temp_path = Path(f.name)

        try:
            solved_result.generate_report(temp_path, format="latex")
            actual = temp_path.read_text(encoding="utf-8")
        finally:
            temp_path.unlink(missing_ok=True)

        # Load golden file
        golden_path = GOLDEN_DIR / f"{golden_base}.tex"
        assert golden_path.exists(), f"Golden file not found: {golden_path}"
        expected = golden_path.read_text(encoding="utf-8")

        # Compare
        assert_reports_match(actual, expected, "LaTeX report")


