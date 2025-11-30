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
"""

import re
import tempfile
from pathlib import Path

import pytest

from qnty.problems.statics import parallelogram_law as pl

# Import shared problem fixtures
from tests.statics._problem_fixtures import PROBLEMS_WITH_GOLDEN_FILES

# =============================================================================
# Test fixtures and utilities
# =============================================================================

GOLDEN_DIR = Path(__file__).parent / "golden"

def get_golden_base(problem_class) -> str:
    """
    Derive golden file base name from problem class name.

    Examples:
        "Problem 2-1" -> "problem_2_1_report"
        "Problem 2-3" -> "problem_2_3_report"
    """
    # e.g., "Problem 2-1" -> "problem_2_1_report"
    name = problem_class.name.lower().replace(" ", "_").replace("-", "_")
    return f"{name}_report"


def normalize_report(content: str) -> str:
    """
    Normalize a report by replacing dynamic content with placeholders.

    This allows comparison between generated reports (with actual dates)
    and golden files (with placeholders).

    Args:
        content: Raw report content

    Returns:
        Normalized content with dates replaced by placeholders
    """
    # Replace datetime format: "2025-11-28 10:32:10"
    content = re.sub(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        "{{GENERATED_DATETIME}}",
        content
    )

    # Replace date format: "November 28, 2025"
    content = re.sub(
        r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}",
        "{{GENERATED_DATE}}",
        content
    )

    return content


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


# =============================================================================
# Utility for regenerating golden files
# =============================================================================


def _get_problem_unit(problem_class) -> str:
    """Get the output unit for a problem class from its vector definitions."""
    # Check F_R first, then F_AB, then default to N
    for attr in ["F_R", "F_AB", "F_AC"]:
        if hasattr(problem_class, attr):
            vec = getattr(problem_class, attr)
            if hasattr(vec, "_unit") and vec._unit:
                return vec._unit.symbol
    return "N"


def regenerate_golden_files():
    """
    Utility function to regenerate golden files for all problems.

    Run this when report generation changes intentionally:
        python tests/report_generation/statics/test_parallelogram_law_reports.py --regenerate

    WARNING: This will overwrite the golden files. Only run this when
    you've verified the new output is correct.
    """
    for problem_class in PROBLEMS_WITH_GOLDEN_FILES:
        golden_base = get_golden_base(problem_class)
        output_unit = _get_problem_unit(problem_class)
        result = pl.solve_class(problem_class, output_unit=output_unit)

        # Generate markdown
        md_path = GOLDEN_DIR / f"{golden_base}.md"
        result.generate_report(md_path, format="markdown")

        # Normalize the file (replace dates with placeholders)
        content = md_path.read_text(encoding="utf-8")
        content = normalize_report(content)
        md_path.write_text(content, encoding="utf-8")
        print(f"Regenerated: {md_path}")

        # Generate LaTeX
        tex_path = GOLDEN_DIR / f"{golden_base}.tex"
        result.generate_report(tex_path, format="latex")

        # Normalize the file
        content = tex_path.read_text(encoding="utf-8")
        content = normalize_report(content)
        tex_path.write_text(content, encoding="utf-8")
        print(f"Regenerated: {tex_path}")


if __name__ == "__main__":
    # Allow running as script to regenerate golden files
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--regenerate":
        regenerate_golden_files()
    else:
        print("Usage: python test_parallelogram_law_reports.py --regenerate")
        print("       pytest test_parallelogram_law_reports.py")
