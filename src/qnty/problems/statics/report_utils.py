"""
Shared utilities for report generation in statics problems.

This module provides common functions used by both cartesian_report.py
and parallelogram_report.py to avoid code duplication.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def format_reference(ref: str) -> str:
    """
    Format reference axis for consistent display in LaTeX/Markdown.

    Uses math mode with explicit + or - to ensure consistent sizing and alignment.
    E.g., "+x" -> "$+x$", "-y" -> "$-y$"
    """
    if not ref:
        return "$+x$"
    # Ensure the sign is explicit
    if ref[0] not in "+-":
        ref = "+" + ref
    return f"${ref}$"


def convert_to_latex_macros(eq: str) -> str:
    """Convert equation string to use LaTeX macros."""
    result = eq
    # Convert |\vec{X}| to \magn{\vv{X}}
    result = re.sub(r"\|\\vec\{([^}]+)\}\|", r"\\magn{\\vv{\1}}", result)
    # Convert standalone \vec{X} to \vv{X}
    result = re.sub(r"\\vec\{([^}]+)\}", r"\\vv{\1}", result)
    return result


def format_substitution_md(sub: str) -> list[str]:
    """Format substitution for Markdown aligned environment."""
    if not sub:
        return []
    result = []
    for line in sub.strip().split("\n"):
        line = line.strip()
        if line.endswith("\\\\"):
            line = line[:-2].strip()
        if line:
            result.append(f"{line} \\\\")
    return result


def clean_latex_alignment_markers(lines: list[str]) -> list[str]:
    """
    Clean LaTeX alignment markers from substitution lines.

    Removes trailing \\\\, alignment markers (&=, &), and leading =.
    Returns cleaned line parts.
    """
    result_parts = []
    for line in lines:
        line = line.strip()
        if line.endswith("\\\\"):
            line = line[:-2].strip()
        # Remove alignment markers (&=, &)
        line = line.replace("&=", "=").replace("& =", "=").replace("&", "")
        # Remove leading = (which comes from the alignment)
        line = line.strip()
        if line.startswith("="):
            line = line[1:].strip()
        if line:
            result_parts.append(line.strip())
    return result_parts


def compile_latex_to_pdf(latex_content: str, output_path: Path) -> None:
    """
    Compile LaTeX content to PDF using tectonic.

    Args:
        latex_content: The LaTeX source content
        output_path: The desired output PDF path

    Raises:
        RuntimeError: If tectonic is not available
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write(latex_content)
        tex_path = Path(f.name)

    try:
        # Try tectonic first (use .exe on Windows)
        tectonic_name = "tectonic.exe" if sys.platform == "win32" else "tectonic"
        tectonic_path = Path(__file__).parent.parent.parent / "extensions" / "reporting" / tectonic_name
        if tectonic_path.exists():
            result = subprocess.run(
                [str(tectonic_path), str(tex_path), "-o", str(output_path.parent)],
                capture_output=True,
                timeout=60,
            )
            if result.returncode == 0:
                generated = output_path.parent / (tex_path.stem + ".pdf")
                if generated.exists() and generated != output_path:
                    output_path.unlink(missing_ok=True)
                    generated.rename(output_path)
                return

        raise RuntimeError("PDF generation requires tectonic. Install it or use latex format.")
    finally:
        tex_path.unlink(missing_ok=True)


def format_component_term(val: float, is_first: bool, precision: int = 1) -> str:
    """
    Format a component value as a term in a sum expression.

    Args:
        val: The numeric value
        is_first: Whether this is the first term (no leading +)
        precision: Decimal places

    Returns:
        Formatted string like "+123.4" or "-56.7" or "123.4" (for first term)
    """
    if val >= 0:
        return f"+{val:.{precision}f}" if not is_first else f"{val:.{precision}f}"
    else:
        return f"{val:.{precision}f}"


def format_component_terms(vals: list[float], precision: int = 1) -> list[str]:
    """
    Format a list of component values as terms in a sum expression.

    Args:
        vals: List of numeric values
        precision: Decimal places

    Returns:
        List of formatted strings
    """
    terms = []
    for i, val in enumerate(vals):
        terms.append(format_component_term(val, is_first=(i == 0), precision=precision))
    return terms
