"""
Intermediate Representation for unified report generation.

This module provides format-agnostic report structures that can be
rendered to both Markdown and LaTeX, ensuring consistency between formats.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class TableAlignment(Enum):
    """Column alignment for tables."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    DECIMAL = "decimal"  # For numeric columns with decimal alignment


@dataclass
class TableColumn:
    """Definition of a table column."""
    header: str
    alignment: TableAlignment = TableAlignment.LEFT


@dataclass
class TableRow:
    """A row of table data."""
    cells: list[str]
    is_header: bool = False


@dataclass
class Table:
    """A table in the report."""
    columns: list[TableColumn]
    rows: list[TableRow]
    caption: str | None = None


@dataclass
class Equation:
    """An equation to display."""
    text: str
    is_latex: bool = False  # If True, text is already in LaTeX format


@dataclass
class SolutionStep:
    """A step in the solution process."""
    step_number: int
    title: str
    equation: str
    substituted: str | None = None
    result_var: str = ""
    result_value: str = ""
    result_unit: str = ""


@dataclass
class Section:
    """A section of the report."""
    title: str
    level: int = 1  # 1 = top level, 2 = subsection, etc.
    content: list[str | Table | Equation | SolutionStep | Section] = field(default_factory=list)


@dataclass
class ReportIR:
    """Intermediate Representation of a complete report."""
    title: str
    generated_date: datetime
    description: str | None = None
    sections: list[Section] = field(default_factory=list)
    diagram_path: Path | None = None

    def add_section(self, title: str, level: int = 1) -> Section:
        """Add a new section and return it for adding content."""
        section = Section(title=title, level=level)
        self.sections.append(section)
        return section


class ReportRenderer:
    """Base class for rendering ReportIR to a specific format."""

    def render(self, report: ReportIR, output_path: Path) -> None:
        """Render the report to the output path."""
        raise NotImplementedError


class MarkdownRenderer(ReportRenderer):
    """Render ReportIR to Markdown format.

    Uses LaTeX math notation ($...$) which is supported by most Markdown renderers
    including GitHub, Jupyter, VS Code, and MathJax-enabled viewers.

    LaTeX is the single source of truth for math formatting - this class
    delegates to LaTeXRenderer for all math conversion, then expands custom
    macros (\\magn{}, \\vv{}) to standard LaTeX for Markdown compatibility.
    """

    def __init__(self):
        # Create a LaTeXRenderer instance to reuse its math conversion methods
        self._latex = LaTeXRenderer()

    def _expand_custom_macros(self, latex: str) -> str:
        r"""Expand custom LaTeX macros to standard LaTeX for Markdown compatibility.

        Markdown renderers (GitHub, MathJax, KaTeX) don't support custom macros
        defined in LaTeX preambles, so we need to expand:
        - \magn{...} → |...| (magnitude notation)
        - \vv{...} → \vec{...} (vector notation)
        """
        result = latex

        # Expand \vv{...} to \vec{...}
        # Need to handle nested braces properly
        def expand_vv(text):
            """Expand \vv{...} to \vec{...}, handling nested braces."""
            output = []
            i = 0
            while i < len(text):
                if text[i:i+4] == r'\vv{':
                    # Find matching closing brace
                    start = i + 4
                    depth = 1
                    j = start
                    while j < len(text) and depth > 0:
                        if text[j] == '{':
                            depth += 1
                        elif text[j] == '}':
                            depth -= 1
                        j += 1
                    inner = text[start:j-1]
                    # Recursively expand any nested \vv
                    inner = expand_vv(inner)
                    output.append(r'\vec{' + inner + '}')
                    i = j
                else:
                    output.append(text[i])
                    i += 1
            return ''.join(output)

        result = expand_vv(result)

        # Expand \magn{...} to |...|
        def expand_magn(text):
            r"""Expand \magn{...} to |...|, handling nested braces."""
            output = []
            i = 0
            while i < len(text):
                if text[i:i+6] == r'\magn{':
                    # Find matching closing brace
                    start = i + 6
                    depth = 1
                    j = start
                    while j < len(text) and depth > 0:
                        if text[j] == '{':
                            depth += 1
                        elif text[j] == '}':
                            depth -= 1
                        j += 1
                    inner = text[start:j-1]
                    # Recursively expand any nested \magn
                    inner = expand_magn(inner)
                    output.append('|' + inner + '|')
                    i = j
                else:
                    output.append(text[i])
                    i += 1
            return ''.join(output)

        result = expand_magn(result)

        return result

    def render(self, report: ReportIR, output_path: Path) -> None:
        """Render the report to Markdown."""
        lines = []

        # Title
        lines.append(f"# Engineering Calculation Report: {report.title}")
        lines.append("")
        lines.append(f"**Generated:** {report.generated_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Description
        if report.description:
            lines.append(f"**Description:** {report.description}")
            lines.append("")

        # Sections
        for section in report.sections:
            lines.extend(self._render_section(section))

        # Diagram
        if report.diagram_path and report.diagram_path.exists():
            lines.append("## Vector Diagram")
            lines.append("")
            lines.append(f"![Vector Diagram]({report.diagram_path.name})")
            lines.append("")
            lines.append("*Figure: Vector diagram showing all forces and their orientations*")
            lines.append("")

        # Disclaimer
        lines.extend(self._render_disclaimer(report.generated_date))

        output_path.write_text("\n".join(lines), encoding="utf-8")

    def _render_section(self, section: Section) -> list[str]:
        """Render a section to Markdown."""
        lines = []

        # Section header
        prefix = "#" * (section.level + 1)  # ## for level 1, ### for level 2, etc.
        lines.append(f"{prefix} {section.title}")
        lines.append("")

        # Content
        for item in section.content:
            if isinstance(item, str):
                # Numbered equations - wrap in LaTeX math
                lines.append(self._to_latex_inline(item))
                lines.append("")
            elif isinstance(item, Table):
                lines.extend(self._render_table(item))
            elif isinstance(item, Equation):
                latex = self._expand_custom_macros(self._latex._to_latex_math(item.text))
                lines.append(f"${latex}$")
                lines.append("")
            elif isinstance(item, SolutionStep):
                lines.extend(self._render_solution_step(item))
            elif isinstance(item, Section):
                lines.extend(self._render_section(item))

        return lines

    def _render_table(self, table: Table) -> list[str]:
        """Render a table to Markdown.

        Uses standard markdown tables with LaTeX math notation for headers.
        Headers with special characters (|, subscripts, Greek letters) are
        converted to proper LaTeX format for consistent rendering.
        """
        if not table.columns:
            return ["*No data*", ""]

        lines = []

        # Format headers for markdown - convert special notation to LaTeX
        formatted_headers = []
        for col in table.columns:
            formatted_headers.append(self._format_table_header_md(col.header))

        # Always use markdown table - LaTeX rendering in markdown tables
        # is widely supported (GitHub, VS Code, Jupyter, etc.)
        lines.extend(self._render_markdown_table(table, formatted_headers))

        lines.append("")
        return lines

    def _format_table_header_md(self, header: str) -> str:
        r"""Format a table header for Markdown with proper LaTeX notation.

        Converts:
        - |F| (N) → $|\vec{F}|$ (N)
        - Fₓ (N) → $F_x$ (N)
        - Fᵧ (N) → $F_y$ (N)
        - θ (deg) → $\theta$ (deg)
        """
        import re

        if not header:
            return ""

        result = header

        # Handle magnitude notation |F| (unit)
        magnitude_match = re.match(r'\|([A-Za-z]+)\|\s*\(([^)]+)\)', header)
        if magnitude_match:
            var = magnitude_match.group(1)
            unit = magnitude_match.group(2)
            return f"$\\|\\vec{{{var}}}\\|$ ({unit})"

        # Handle subscript notation Fₓ (unit), Fᵧ (unit), Fᵤ (unit), Fᵥ (unit)
        subscript_map = {"ₓ": "x", "ᵧ": "y", "ᵤ": "u", "ᵥ": "v", "ₙ": "n", "ₜ": "t", "₁": "1", "₂": "2", "₃": "3"}
        for unicode_sub, ascii_sub in subscript_map.items():
            if unicode_sub in result:
                sub_match = re.match(r'([A-Za-z]+)' + unicode_sub + r'\s*\(([^)]+)\)', result)
                if sub_match:
                    base = sub_match.group(1)
                    unit = sub_match.group(2)
                    return f"${base}_{ascii_sub}$ ({unit})"

        # Handle Greek letters θ (deg)
        greek_map = {"θ": r"\theta", "φ": r"\varphi", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma"}
        for greek, latex in greek_map.items():
            if result.startswith(greek):
                greek_match = re.match(greek + r'\s*\(([^)]+)\)', result)
                if greek_match:
                    unit = greek_match.group(1)
                    return f"${latex}$ ({unit})"
                return f"${latex}${result[1:]}"

        return result

    def _render_markdown_table(self, table: Table, formatted_headers: list[str]) -> list[str]:
        """Render a standard markdown table, centered to match PDF output."""
        lines = []

        # Wrap table in centered div for consistency with PDF layout
        lines.append('<div align="center">')
        lines.append("")

        # Header row
        header = "| " + " | ".join(formatted_headers) + " |"
        lines.append(header)

        # Separator row
        sep_parts = []
        for col in table.columns:
            if col.alignment == TableAlignment.LEFT:
                sep_parts.append(":---")
            elif col.alignment == TableAlignment.CENTER:
                sep_parts.append(":---:")
            elif col.alignment in (TableAlignment.RIGHT, TableAlignment.DECIMAL):
                sep_parts.append("---:")
            else:
                sep_parts.append("---")
        lines.append("| " + " | ".join(sep_parts) + " |")

        # Data rows
        for row in table.rows:
            if not row.is_header:
                converted_cells = []
                for i, cell in enumerate(row.cells):
                    if i == 0:  # First column is typically symbol/vector name
                        converted_cells.append(self._format_vector_symbol(cell))
                    else:
                        converted_cells.append(cell)
                row_text = "| " + " | ".join(converted_cells) + " |"
                lines.append(row_text)

        lines.append("")
        lines.append("</div>")

        return lines

    def _format_vector_symbol(self, symbol: str) -> str:
        """Format a vector symbol for Markdown using LaTeX."""
        # Convert F_1, F_R etc to LaTeX vector notation
        import re
        if re.match(r'^[A-Z]_', symbol):
            # It's a vector like F_1 or F_R
            # Format as scalar first, then wrap in \vec{} for Markdown
            # (We use \vec{} directly for Markdown instead of the \vv{} macro)
            latex = self._latex._format_latex_variable(symbol, as_vector=False)
            return f"$\\vec{{{latex}}}$"
        return symbol

    def _render_solution_step(self, step: SolutionStep) -> list[str]:
        """Render a solution step to Markdown.

        Uses the 'aligned' environment for multi-line equations with equal sign
        alignment. Note: KaTeX doesn't support flalign* for left-alignment of the
        block, so the block will be centered (standard for display math) but
        equations within are aligned at the = sign.
        """
        lines = []

        # Format title using LaTeX and expand custom macros
        title_latex = self._expand_custom_macros(self._latex._format_step_title(step.title))
        lines.append(f"**Step {step.step_number}: Solve for {title_latex}**")
        lines.append("")

        # Substitution/Calculation - this is the main content for solution steps
        if step.substituted:
            # Check if this is a multi-line calculation
            if "\n" in step.substituted:
                # Use aligned environment for equal sign alignment
                lines.append("$$")
                lines.append(r"\begin{aligned}")
                for sub_line in step.substituted.split("\n"):
                    latex_line = self._expand_custom_macros(self._latex._to_latex_math(sub_line.strip()))
                    if "=" in latex_line:
                        latex_line = latex_line.replace("=", "&=", 1)
                    lines.append(latex_line + r" \\")
                lines.append(r"\end{aligned}")
                lines.append("$$")
                lines.append("")
            elif step.substituted != step.equation:
                sub_latex = self._expand_custom_macros(self._latex._to_latex_math(step.substituted))
                lines.append(f"$${sub_latex}$$")
                lines.append("")

        return lines

    def _to_latex_inline(self, text: str) -> str:
        """Convert text with math to inline LaTeX format for Markdown.

        For numbered equations like "1. |F_R|² = ...", wraps the equation in $...$
        """
        import re
        # Check for numbered equation pattern
        match = re.match(r'^(\d+\.\s*)(.+)$', text)
        if match:
            number = match.group(1)
            equation = match.group(2)
            latex = self._expand_custom_macros(self._latex._to_latex_math(equation))
            return f"{number}${latex}$"
        return text

    def _render_disclaimer(self, generated_date: datetime) -> list[str]:
        """Render the disclaimer section."""
        current_date = generated_date.strftime("%B %d, %Y")

        return [
            "",
            "---",
            "",
            "## Disclaimer",
            "",
            "While every effort has been made to ensure the accuracy and reliability of the calculations provided, "
            + "we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. "
            + "Users must independently verify the results and assume full responsibility for any decisions or actions "
            + "taken based on its output. Use of this calculator is entirely at your own risk, and we expressly "
            + "disclaim any liability for errors or omissions in the information provided.",
            "",
            "**Report Details:**",
            f"- **Generated Date:** {current_date}",
            "- **Generated Using:** Qnty Library",
            "- **Version:** Beta (Independent verification required for production use)",
            "",
            "**Signatures:**",
            "",
            "| Role | Name | Signature | Date |",
            "|------|------|-----------|------|",
            "| Calculated By | _________________ | _________________ | _______ |",
            "| Reviewed By | _________________ | _________________ | _______ |",
            "| Approved By | _________________ | _________________ | _______ |",
            "",
            "*Report generated using qnty library*",
        ]


class LaTeXRenderer(ReportRenderer):
    """Render ReportIR to LaTeX format."""

    def render(self, report: ReportIR, output_path: Path) -> None:
        """Render the report to LaTeX."""
        lines = []

        # Preamble
        lines.extend(self._render_preamble(report))

        # Document body
        lines.append(r"\begin{document}")
        lines.append(r"\maketitle")
        lines.append("")

        # Description
        if report.description:
            lines.append(r"\section*{Description}")
            lines.append(r"\noindent")
            lines.append(r"\begin{minipage}{\textwidth}")
            lines.append(self._escape_latex(report.description))
            lines.append(r"\end{minipage}")
            lines.append(r"\par")
            lines.append("")

        # Sections
        for section in report.sections:
            lines.extend(self._render_section(section))

        # Diagram
        if report.diagram_path and report.diagram_path.exists():
            lines.append(r"\section{Vector Diagram}")
            lines.append(r"\begin{center}")
            lines.append(r"\includegraphics[width=0.8\textwidth]{" + str(report.diagram_path.name) + "}")
            lines.append(r"\end{center}")
            lines.append(r"\textit{Figure: Vector diagram showing all forces and their orientations}")
            lines.append("")

        # Disclaimer
        lines.extend(self._render_disclaimer(report.generated_date))

        lines.append(r"\end{document}")

        output_path.write_text("\n".join(lines), encoding="utf-8")

    def _render_preamble(self, report: ReportIR) -> list[str]:
        """Render the LaTeX document preamble."""
        return [
            r"\documentclass[11pt,a4paper]{article}",
            r"\usepackage{amsmath}",
            r"\usepackage{amssymb}",
            r"\usepackage{booktabs}",
            r"\usepackage{longtable}",
            r"\usepackage{geometry}",
            r"\geometry{margin=1in}",
            r"\usepackage{hyperref}",
            r"\usepackage{enumitem}",
            r"\usepackage{graphicx}",
            r"\usepackage{siunitx}",
            r"\usepackage{accents}",  # For vector notation
            r"\usepackage{changepage}",  # For adjustwidth environment
            "",
            r"% Vector notation: \vv{F} produces F with arrow over it",
            r"\newcommand{\vv}[1]{\vec{#1}}",
            r"% Magnitude notation: \magn{F} produces |F| with fixed-height bars",
            r"\newcommand{\magn}[1]{|#1|}",
            "",
            r"\title{Engineering Calculation Report: " + self._escape_latex(report.title) + "}",
            r"\date{" + report.generated_date.strftime("%B %d, %Y") + "}",
            "",
        ]

    def _render_section(self, section: Section) -> list[str]:
        """Render a section to LaTeX."""
        lines = []

        # Strip leading number pattern (e.g., "1. " or "2. ") from title
        # since LaTeX \section commands handle numbering automatically
        import re
        title = re.sub(r'^\d+\.\s*', '', section.title)

        # Section header
        if section.level == 1:
            lines.append(r"\section{" + self._escape_latex(title) + "}")
        elif section.level == 2:
            lines.append(r"\subsection{" + self._escape_latex(title) + "}")
        else:
            lines.append(r"\subsubsection{" + self._escape_latex(title) + "}")
        lines.append("")

        # Content - collect numbered equations to render in enumerate environment
        import re
        numbered_equations = []
        i = 0
        while i < len(section.content):
            item = section.content[i]
            if isinstance(item, str):
                # Check if this looks like a numbered equation (e.g., "1. F_R² = ...")
                eq_match = re.match(r'^(\d+)\.\s*(.+)$', item)
                if eq_match and '=' in item:
                    # Collect consecutive numbered equations
                    numbered_equations.append(eq_match.group(2))
                    i += 1
                    continue
                else:
                    # Flush any collected numbered equations first
                    if numbered_equations:
                        lines.extend(self._render_numbered_equations(numbered_equations))
                        numbered_equations = []
                    lines.append(self._escape_latex(item))
                    lines.append("")
            elif isinstance(item, Table):
                # Flush any collected numbered equations first
                if numbered_equations:
                    lines.extend(self._render_numbered_equations(numbered_equations))
                    numbered_equations = []
                lines.extend(self._render_table(item))
            elif isinstance(item, Equation):
                # Flush any collected numbered equations first
                if numbered_equations:
                    lines.extend(self._render_numbered_equations(numbered_equations))
                    numbered_equations = []
                latex_eq = self._to_latex_math(item.text) if not item.is_latex else item.text
                lines.append(r"\begin{enumerate}")
                lines.append(r"\item $\displaystyle\Large " + latex_eq + "$")
                lines.append(r"\end{enumerate}")
                lines.append("")
            elif isinstance(item, SolutionStep):
                # Flush any collected numbered equations first
                if numbered_equations:
                    lines.extend(self._render_numbered_equations(numbered_equations))
                    numbered_equations = []
                lines.extend(self._render_solution_step(item))
            elif isinstance(item, Section):
                # Flush any collected numbered equations first
                if numbered_equations:
                    lines.extend(self._render_numbered_equations(numbered_equations))
                    numbered_equations = []
                lines.extend(self._render_section(item))
            i += 1

        # Flush any remaining numbered equations
        if numbered_equations:
            lines.extend(self._render_numbered_equations(numbered_equations))

        return lines

    def _render_numbered_equations(self, equations: list[str]) -> list[str]:
        """Render a list of equations as a properly indented enumerate list."""
        lines = []
        lines.append(r"\begin{enumerate}")
        for eq_text in equations:
            latex_eq = self._to_latex_math(eq_text)
            lines.append(r"\item $\displaystyle " + latex_eq + "$")
        lines.append(r"\end{enumerate}")
        lines.append("")
        return lines

    def _render_table(self, table: Table) -> list[str]:
        """Render a table to LaTeX."""
        if not table.columns:
            return [r"\textit{No data}", ""]

        lines = []

        # Column spec
        col_spec = ""
        for col in table.columns:
            if col.alignment == TableAlignment.LEFT:
                col_spec += "l"
            elif col.alignment == TableAlignment.CENTER:
                col_spec += "c"
            elif col.alignment == TableAlignment.DECIMAL:
                col_spec += "S"  # siunitx decimal-aligned
            else:
                col_spec += "r"

        lines.append(r"\begin{longtable}{" + col_spec + "}")
        lines.append(r"\toprule")

        # Header row
        header_cells = []
        for col in table.columns:
            header = self._format_table_header(col.header)
            if col.alignment == TableAlignment.DECIMAL:
                # Wrap in braces for siunitx S columns
                header_cells.append("{" + header + "}")
            else:
                header_cells.append(header)
        lines.append(" & ".join(header_cells) + r" \\")
        lines.append(r"\midrule")
        lines.append(r"\endhead")

        # Data rows
        for row in table.rows:
            if not row.is_header:
                cells = []
                for i, cell in enumerate(row.cells):
                    # Check if this is a symbol column (first column usually)
                    if i == 0 and cell and not cell.startswith("$"):
                        # Format as math variable
                        cells.append("$" + self._format_latex_variable(cell) + "$")
                    else:
                        cells.append(self._escape_latex(cell))
                lines.append(" & ".join(cells) + r" \\")

        lines.append(r"\bottomrule")
        lines.append(r"\end{longtable}")
        lines.append("")

        return lines

    def _render_solution_step(self, step: SolutionStep) -> list[str]:
        """Render a solution step to LaTeX."""
        lines = []

        # Format the step title as math (handles Greek letters, subscripts, magnitude bars)
        title_latex = self._format_step_title(step.title)
        # Indent step under the section using a small left margin
        lines.append(r"\vspace{0.2em}")
        lines.append(r"\noindent\hspace{1em}\textbf{Step " + str(step.step_number) + ": Solve for " + title_latex + "}")
        lines.append(r"\vspace{0.1em}")
        lines.append("")

        # Wrap step content in adjustwidth for indentation
        lines.append(r"\begin{adjustwidth}{2em}{}")

        # Equation (only if provided)
        if step.equation:
            lines.append(r"\textbf{Equation:}")
            lines.append(r"\begin{equation*}")
            lines.append(self._to_latex_math(step.equation))
            lines.append(r"\end{equation*}")

        # Substitution/Calculation
        if step.substituted:
            # Check if this is a multi-line calculation with aligned equals signs
            if "\n" in step.substituted:
                # Only show label if there was also an equation
                if step.equation:
                    lines.append(r"\textbf{Substitution:}")
                # Use flalign* for left-aligned multi-line equations with indentation
                # The && at the end pushes the equation to the left
                # Add negative space to reduce flalign's default spacing
                lines.append(r"\vspace{-0.8em}")
                lines.append(r"\begin{flalign*}")
                sub_lines = step.substituted.split("\n")
                for i, sub_line in enumerate(sub_lines):
                    latex_line = self._to_latex_math(sub_line.strip())
                    # Add alignment on equals sign and left-align with quad indent
                    if "=" in latex_line:
                        # \quad for indentation, &= for alignment, && to push left
                        latex_line = r"\quad " + latex_line.replace("=", "&=", 1) + " &&"
                    else:
                        # Lines without = just get indented
                        latex_line = r"\quad & " + latex_line + " &&"
                    # Add line continuation except for last line
                    if i < len(sub_lines) - 1:
                        latex_line += r" \\"
                    lines.append(latex_line)
                lines.append(r"\end{flalign*}")
                lines.append(r"\vspace{-0.8em}")
            elif step.substituted != step.equation:
                lines.append(r"\textbf{Substitution:}")
                lines.append(r"\begin{equation*}")
                lines.append(self._to_latex_math(step.substituted))
                lines.append(r"\end{equation*}")

        # Result (only if provided and not None)
        if step.result_value and step.result_value != "None":
            lines.append(r"\textbf{Result:}")
            lines.append(r"\begin{equation*}")
            # Use _to_latex_math for result_var to handle angle notation ∠(F_1,F_2)
            result_var_latex = self._to_latex_math(step.result_var)
            result_latex = result_var_latex + " = " + step.result_value
            if step.result_unit:
                result_latex += r" \text{ " + self._escape_latex(step.result_unit) + "}"
            lines.append(result_latex)
            lines.append(r"\end{equation*}")

        lines.append(r"\end{adjustwidth}")
        lines.append("")

        return lines

    def _format_step_title(self, title: str) -> str:
        """Format a step title for LaTeX, handling math symbols properly.

        Converts variable names like |F_R|, φ, θ_F_R to proper LaTeX math mode.
        """
        if not title:
            return ""

        import re

        # Check for angle notation ∠(F_1,F_2) possibly followed by additional text
        angle_match = re.match(r'∠\(([^,]+),\s*([^)]+)\)(.*)', title)
        if angle_match:
            v1 = angle_match.group(1)
            v2 = angle_match.group(2)
            suffix = angle_match.group(3).strip()
            v1_formatted = self._format_latex_variable(v1, as_vector=True)
            v2_formatted = self._format_latex_variable(v2, as_vector=True)
            result = r"$\angle(" + v1_formatted + ", " + v2_formatted + r")$"
            if suffix:
                # Add the suffix as regular text (e.g., "using Eq 2")
                result += " " + self._escape_latex(suffix)
            return result

        # Check for magnitude notation |...| possibly followed by additional text
        magnitude_match = re.match(r'\|([^|]+)\|(.*)', title)
        if magnitude_match:
            inner = magnitude_match.group(1)
            suffix = magnitude_match.group(2).strip()
            result = r"$\magn{\vv{" + self._format_latex_variable(inner, as_vector=False) + r"}}$"
            if suffix:
                # Add the suffix as regular text (e.g., "using Eq 1")
                result += " " + self._escape_latex(suffix)
            return result

        # Check for Greek letters
        greek_map = {"θ": r"\theta", "φ": r"\varphi", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma"}
        for greek, latex in greek_map.items():
            if title.startswith(greek):
                # Handle subscripted Greek like θ_F_R possibly followed by text like "with respect to +x"
                if "_" in title:
                    rest = title[1:]  # Remove Greek letter, get _F_R with respect to +x
                    # Find where the subscript ends (at first space or end)
                    space_idx = rest.find(" ")
                    if space_idx != -1:
                        subscript_part = rest[:space_idx]  # _F_R
                        suffix = rest[space_idx:].strip()  # with respect to +x
                        subscript_latex = self._format_subscript_content(subscript_part)
                        return r"$" + latex + subscript_latex + r"$ " + self._escape_latex(suffix)
                    else:
                        subscript_latex = self._format_subscript_content(rest)
                        return r"$" + latex + subscript_latex + r"$"
                return r"$" + latex + r"$"

        # Check for force variables like F_R (show as magnitude in solve context)
        if title.startswith(("F_", "V_", "A_", "R_", "P_")):
            return r"$" + self._format_latex_variable(title, as_vector=False) + r"$"

        # Check for any variable with subscripts (e.g., x_1, y_max)
        if "_" in title:
            return r"$" + self._format_latex_variable(title, as_vector=False) + r"$"

        # Default: escape as text
        return self._escape_latex(title)

    def _format_subscript_content(self, text: str) -> str:
        """Format subscript content like _F_R for LaTeX.

        Input: _F_R (with leading underscore)
        Output: _{F_R} (proper LaTeX subscript with nested content)

        For angle subscripts like θ_{F_R}, the subscript F_R should render
        as a proper subscript showing F with R as a sub-subscript.
        """
        if not text.startswith("_"):
            return text

        subscript = text[1:]  # Remove leading underscore, get "F_R"

        # Handle nested subscripts like F_R
        # We want θ_{F_R} to display the subscript as "F_R" (F with subscript R)
        if "_" in subscript:
            parts = subscript.split("_", 1)
            base = parts[0]
            sub = parts[1]
            # Create nested subscript: F_{R}
            return "_{" + base + "_{" + sub + "}}"

        return "_{" + subscript + "}"

    def _render_disclaimer(self, generated_date: datetime) -> list[str]:
        """Render the disclaimer section."""
        current_date = generated_date.strftime("%B %d, %Y")

        return [
            r"\section*{Disclaimer}",
            r"\small",
            "While every effort has been made to ensure the accuracy and reliability of the calculations provided, "
            + "we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. "
            + "Users must independently verify the results and assume full responsibility for any decisions or actions "
            + "taken based on its output. Use of this calculator is entirely at your own risk, and we expressly "
            + "disclaim any liability for errors or omissions in the information provided.",
            "",
            r"\vspace{1em}",
            r"\noindent\textbf{Report Details:}",
            r"\begin{itemize}[nosep]",
            r"\item \textbf{Generated Date:} " + current_date,
            r"\item \textbf{Generated Using:} Qnty Library",
            r"\item \textbf{Version:} Beta (Independent verification required for production use)",
            r"\end{itemize}",
            "",
            r"\vspace{1em}",
            r"\noindent\textbf{Signatures:}",
            r"\begin{longtable}{llll}",
            r"\toprule",
            r"Role & Name & Signature & Date \\",
            r"\midrule",
            r"Calculated By & \rule{3cm}{0.4pt} & \rule{3cm}{0.4pt} & \rule{2cm}{0.4pt} \\",
            r"Reviewed By & \rule{3cm}{0.4pt} & \rule{3cm}{0.4pt} & \rule{2cm}{0.4pt} \\",
            r"Approved By & \rule{3cm}{0.4pt} & \rule{3cm}{0.4pt} & \rule{2cm}{0.4pt} \\",
            r"\bottomrule",
            r"\end{longtable}",
            "",
            r"\begin{center}",
            r"\textit{Report generated using qnty library}",
            r"\end{center}",
        ]

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""
        replacements = [
            ("\\", r"\textbackslash{}"),
            ("&", r"\&"),
            ("%", r"\%"),
            ("$", r"\$"),
            ("#", r"\#"),
            ("_", r"\_"),
            ("{", r"\{"),
            ("}", r"\}"),
            ("~", r"\textasciitilde{}"),
            ("^", r"\textasciicircum{}"),
        ]
        result = text
        for old, new in replacements:
            result = result.replace(old, new)
        return result

    def _format_table_header(self, header: str) -> str:
        """Format a table header with proper LaTeX notation for vectors and magnitudes.

        Handles special notation like:
        - |F| → $|\\vec{F}|$
        - Fₓ → $F_x$
        - Fᵧ → $F_y$
        - θ → $\\theta$
        """
        if not header:
            return ""

        import re

        # Check for magnitude notation like "|F| (N)"
        magnitude_match = re.match(r'\|([A-Za-z]+)\|\s*\(([^)]+)\)', header)
        if magnitude_match:
            var = magnitude_match.group(1)
            unit = magnitude_match.group(2)
            return r"$\magn{\vv{" + var + r"}}$ (" + self._escape_latex(unit) + ")"

        # Check for subscript notation like "Fₓ (N)", "Fᵧ (N)", "Fᵤ (N)", "Fᵥ (N)"
        subscript_map = {"ₓ": "x", "ᵧ": "y", "ᵤ": "u", "ᵥ": "v", "ₙ": "n", "ₜ": "t", "₁": "1", "₂": "2", "₃": "3"}
        for unicode_sub, ascii_sub in subscript_map.items():
            if unicode_sub in header:
                # Parse pattern like "Fₓ (unit)"
                sub_match = re.match(r'([A-Za-z]+)' + unicode_sub + r'\s*\(([^)]+)\)', header)
                if sub_match:
                    base = sub_match.group(1)
                    unit = sub_match.group(2)
                    return r"$" + base + "_{" + ascii_sub + r"}$ (" + self._escape_latex(unit) + ")"

        # Check for Greek letters like "θ (deg)"
        greek_map = {"θ": r"\theta", "φ": r"\varphi", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma"}
        for greek, latex in greek_map.items():
            if header.startswith(greek):
                # Parse pattern like "θ (deg)"
                greek_match = re.match(greek + r'\s*\(([^)]+)\)', header)
                if greek_match:
                    unit = greek_match.group(1)
                    return r"$" + latex + r"$ (" + self._escape_latex(unit) + ")"
                # Just the Greek letter
                return r"$" + latex + r"$" + self._escape_latex(header[1:])

        # Default: escape as regular text
        return self._escape_latex(header)

    def _is_vector_symbol(self, name: str) -> bool:
        """Check if a variable name represents a vector quantity.

        Vector symbols typically start with F (force), v (velocity), a (acceleration),
        r (position), etc. and have subscripts like F_1, F_R, v_A.
        Angles (θ, φ) and their subscripted forms are NOT vectors.
        """
        if not name:
            return False

        # Strip magnitude bars if present
        if name.startswith("|") and name.endswith("|"):
            name = name[1:-1]

        # Angles are not vectors
        if name.startswith(("θ", "φ", "α", "β", "γ", r"\theta", r"\varphi", r"\alpha", r"\beta", r"\gamma")):
            return False

        # Common vector variable patterns (force, velocity, acceleration, position, etc.)
        # Check base letter before any subscript
        base = name.split("_")[0] if "_" in name else name
        vector_bases = {"F", "v", "a", "r", "p", "V", "A", "R", "P"}  # Common vector symbols

        return base in vector_bases

    def _format_latex_variable(self, name: str, as_vector: bool | None = None) -> str:
        """Format a variable name for LaTeX math mode.

        Args:
            name: The variable name to format
            as_vector: If True, format as vector with arrow. If False, format as scalar.
                      If None, auto-detect based on the variable name.
        """
        if not name:
            return ""

        # Handle magnitude notation |F_R| - magnitude is a scalar, but we show the vector inside
        if name.startswith("|") and name.endswith("|"):
            inner = name[1:-1]
            # Format inner as vector (with arrow) inside magnitude bars
            inner_formatted = self._format_latex_variable(inner, as_vector=True)
            return r"\magn{" + inner_formatted + "}"

        # Determine if this should be formatted as a vector
        is_vector = as_vector if as_vector is not None else self._is_vector_symbol(name)

        # Handle Greek letters
        greek_map = {"θ": r"\theta", "φ": r"\varphi", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma"}
        for greek, latex in greek_map.items():
            if name.startswith(greek):
                name = latex + name[1:]
                break

        # Handle subscripts
        if "_" in name:
            parts = name.split("_", 1)
            base = parts[0]
            subscript = parts[1] if len(parts) > 1 else ""

            # Recursively format the subscript in case it has nested underscores
            if "_" in subscript:
                subscript = self._format_latex_variable(subscript, as_vector=False).replace("_", r"\_")

            # Multi-character subscripts need braces
            if len(subscript) > 1:
                formatted = f"{base}_{{{subscript}}}"
            else:
                formatted = f"{base}_{subscript}"

            # Add vector arrow if this is a vector
            if is_vector:
                return r"\vv{" + formatted + "}"
            return formatted

        # No subscript - simple variable
        if is_vector:
            return r"\vv{" + name + "}"
        return name

    def _to_latex_math(self, text: str) -> str:
        """Convert equation text to LaTeX math notation.

        In equations, force variables (F_1, F_2, F_R) typically represent magnitudes
        (scalar values) when they appear:
        - Squared (F²)
        - In arithmetic operations (+, -, *, /)
        - With trig functions

        Vector notation (with arrows) is used in tables to identify the vector,
        but equations typically work with magnitudes. We use |F| notation
        to explicitly show magnitude when clarity is needed.
        """
        if not text:
            return ""

        import re

        result = text

        # Handle Greek letters first (before subscript processing)
        greek_map = {"θ": r"\theta", "φ": r"\varphi", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma"}
        for greek, latex in greek_map.items():
            result = result.replace(greek, latex)

        # Handle angle symbol ∠ for "angle between vectors" notation
        # Also add vector arrows to the vectors inside the angle notation
        def angle_replacer(match):
            v1 = match.group(1)
            v2 = match.group(2)
            # Format each vector with subscript and arrow
            v1_formatted = self._format_latex_variable(v1, as_vector=True)
            v2_formatted = self._format_latex_variable(v2, as_vector=True)
            return r"\angle(" + v1_formatted + ", " + v2_formatted + ")"

        result = re.sub(r'∠\(([^,]+),\s*([^)]+)\)', angle_replacer, result)

        # Handle explicit magnitude notation |...| BEFORE variable processing
        # This captures magnitude expressions and formats them properly
        def magnitude_replacer(match):
            inner = match.group(1)
            # Check if inner is a vector-like variable
            inner_base = inner.split("_")[0] if "_" in inner else inner
            inner_base = inner_base.lstrip("\\")  # Remove backslash for checking
            vector_bases = {"F", "v", "a", "r", "p", "V", "A", "R", "P"}
            if inner_base in vector_bases:
                # Format inner with vector arrow inside magnitude bars
                return r"\magn{\vv{" + inner + "}}"
            return r"\magn{" + inner + "}"

        result = re.sub(r'\|([^|]+)\|', magnitude_replacer, result)

        # Handle nested subscripts like F_R or θ_F_R
        # In equation context, F_R represents the magnitude (scalar), not the vector
        # Only explicit |F_R| or table contexts should show vector arrows
        def subscript_replacer(match):
            base = match.group(1)
            subscript = match.group(2)

            # Check if subscript itself has an underscore (nested case like F_1 in θ_F_1)
            # We want θ_{F_1} to render as theta with "F₁" as subscript
            if '_' in subscript:
                # For nested subscripts: F_1 -> F_1 (keep underscore, LaTeX handles it)
                # The outer braces group it as a single subscript unit
                # Inner underscores create sub-subscripts in LaTeX
                pass  # Keep subscript as-is, braces will handle grouping

            # Multi-character subscripts need braces
            if len(subscript) > 1:
                formatted = f"{base}_{{{subscript}}}"
            else:
                formatted = f"{base}_{subscript}"

            return formatted

        # Match: word character or backslash+word (for \theta etc) followed by _something
        # But NOT if already inside a \vv{} or \magn{} command
        result = re.sub(r'(?<!\\vv\{)(?<!\\magn\{)(\\?[A-Za-z]+)_([A-Za-z0-9_]+)', subscript_replacer, result)

        # Replace superscript ² with ^2
        result = result.replace("²", "^2")

        # Replace common operators
        result = result.replace("·", r" \cdot ")
        result = result.replace("*", r" \cdot ")
        result = result.replace("**", "^")

        # Replace trig functions (need to handle already-converted \theta etc)
        # Handle inverse trig functions first (sin⁻¹, cos⁻¹, tan⁻¹)
        result = result.replace('sin⁻¹(', r'\sin^{-1}(')
        result = result.replace('cos⁻¹(', r'\cos^{-1}(')
        result = result.replace('tan⁻¹(', r'\tan^{-1}(')
        # Then regular trig functions
        result = re.sub(r'(?<!\\)sin\(', r'\\sin(', result)
        result = re.sub(r'(?<!\\)cos\(', r'\\cos(', result)
        result = re.sub(r'(?<!\\)tan\(', r'\\tan(', result)

        # Handle sqrt - need to track balanced parentheses
        def replace_sqrt(text):
            """Replace sqrt(...) with \\sqrt{...}, handling nested parentheses."""
            output = []
            i = 0
            while i < len(text):
                if text[i:i+5] == 'sqrt(':
                    # Find the matching closing parenthesis
                    start = i + 5
                    depth = 1
                    j = start
                    while j < len(text) and depth > 0:
                        if text[j] == '(':
                            depth += 1
                        elif text[j] == ')':
                            depth -= 1
                        j += 1
                    # j now points to one past the closing paren
                    inner = text[start:j-1]
                    output.append(r'\sqrt{' + inner + '}')
                    i = j
                else:
                    output.append(text[i])
                    i += 1
            return ''.join(output)

        result = replace_sqrt(result)

        # Handle fractions (a/b -> \frac{a}{b})
        # Need to identify the numerator and denominator properly
        def find_balanced_braces(text, start):
            """Find the end of balanced braces starting at start (which should be '{')."""
            if start >= len(text) or text[start] != '{':
                return start
            depth = 1
            i = start + 1
            while i < len(text) and depth > 0:
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                i += 1
            return i

        def replace_fractions(text):
            """Replace a/b patterns with \\frac{a}{b}."""
            output = []
            i = 0
            while i < len(text):
                if text[i] == '/':
                    # Find the numerator (go backwards)
                    # Could be: sin(...), |...|, \magn{...}, a single term, or parenthesized expression
                    num_end = i
                    num_start = i - 1

                    if num_start >= 0:
                        # Check for closing paren/bracket
                        if text[num_start] == ')':
                            # Find matching open paren
                            depth = 1
                            num_start -= 1
                            while num_start >= 0 and depth > 0:
                                if text[num_start] == ')':
                                    depth += 1
                                elif text[num_start] == '(':
                                    depth -= 1
                                num_start -= 1
                            num_start += 1
                            # Check if preceded by function name like \sin
                            while num_start > 0 and (text[num_start-1].isalpha() or text[num_start-1] == '\\'):
                                num_start -= 1
                        elif text[num_start] == '|':
                            # Find matching open |
                            num_start -= 1
                            while num_start >= 0 and text[num_start] != '|':
                                num_start -= 1
                        elif text[num_start] == '}':
                            # Find matching open { and include preceding command
                            depth = 1
                            num_start -= 1
                            while num_start >= 0 and depth > 0:
                                if text[num_start] == '}':
                                    depth += 1
                                elif text[num_start] == '{':
                                    depth -= 1
                                num_start -= 1
                            num_start += 1
                            # Include preceding command like \magn
                            while num_start > 0 and (text[num_start-1].isalpha() or text[num_start-1] == '\\'):
                                num_start -= 1
                        else:
                            # Single term - go back to start of term
                            while num_start > 0 and (text[num_start-1].isalnum() or text[num_start-1] in '_\\{}^'):
                                num_start -= 1

                    # Find the denominator (go forwards)
                    den_start = i + 1
                    den_end = den_start

                    if den_end < len(text):
                        if text[den_start] == '|':
                            # Find matching close |
                            den_end += 1
                            while den_end < len(text) and text[den_end] != '|':
                                den_end += 1
                            den_end += 1  # Include the closing |
                        elif text[den_start] == '(':
                            # Find matching close paren
                            depth = 1
                            den_end += 1
                            while den_end < len(text) and depth > 0:
                                if text[den_end] == '(':
                                    depth += 1
                                elif text[den_end] == ')':
                                    depth -= 1
                                den_end += 1
                        elif text[den_start] == '\\':
                            # LaTeX command like \sin(...) or \magn{...}
                            den_end += 1
                            while den_end < len(text) and text[den_end].isalpha():
                                den_end += 1
                            # Check for {...} argument
                            if den_end < len(text) and text[den_end] == '{':
                                den_end = find_balanced_braces(text, den_end)
                            # Check for (...) argument
                            elif den_end < len(text) and text[den_end] == '(':
                                depth = 1
                                den_end += 1
                                while den_end < len(text) and depth > 0:
                                    if text[den_end] == '(':
                                        depth += 1
                                    elif text[den_end] == ')':
                                        depth -= 1
                                    den_end += 1
                        else:
                            # Single term (include decimal point for numbers like 700.000)
                            while den_end < len(text) and (text[den_end].isalnum() or text[den_end] in '_\\{}^.'):
                                den_end += 1

                    numerator = text[num_start:num_end]
                    denominator = text[den_start:den_end]

                    # Remove what we've already added that's part of numerator
                    output_str = ''.join(output)
                    if output_str.endswith(numerator):
                        output = list(output_str[:-len(numerator)])

                    output.append(r'\frac{' + numerator + '}{' + denominator + '}')
                    i = den_end
                else:
                    output.append(text[i])
                    i += 1
            return ''.join(output)

        result = replace_fractions(result)

        # Handle degree symbol
        result = result.replace("°", r"^{\circ}")

        return result


class ReportBuilder:
    """Builds a ReportIR from a Problem and its solving data.

    This is the single source of truth for report content.
    Both Markdown and LaTeX renderers use the IR produced by this builder.
    """

    def __init__(
        self,
        problem,
        known_variables: dict,
        equations: list,
        solving_history: list,
        diagram_path: Path | None = None
    ):
        self.problem = problem
        self.known_variables = known_variables
        self.equations = equations
        self.solving_history = solving_history
        self.diagram_path = diagram_path

    def _get_default_reference_axis(self) -> str:
        """Get the default reference axis for unknown vectors.

        If the problem has a custom coordinate system, use its primary axis.
        Otherwise default to '+x'.
        """
        coord_sys = getattr(self.problem, 'coordinate_system', None)
        if coord_sys is not None and hasattr(coord_sys, 'axis1_label'):
            return f"+{coord_sys.axis1_label}"
        return "+x"

    def _convert_angle_for_display(self, angle_deg: float, vec_obj: object | None = None) -> float:
        """Convert angle based on the vector's angle_dir setting.

        Args:
            angle_deg: Angle in degrees (standard CCW convention, 0-360)
            vec_obj: Vector object that may have angle_dir attribute

        Returns:
            Converted angle based on angle_dir:
            - "ccw" (default): 0 to 360, counterclockwise from reference
            - "cw": Negative for clockwise angles (e.g., 358.8° -> -1.2°)
            - "signed": -180 to 180 range
        """
        # Get angle_dir from vector first, then fall back to problem
        angle_dir = None
        if vec_obj is not None:
            angle_dir = getattr(vec_obj, 'angle_dir', None)
        if angle_dir is None:
            angle_dir = getattr(self.problem, 'angle_dir', None)

        if angle_dir == "cw":
            # Convert to clockwise: if angle > 180, show as negative
            # e.g., 358.8° CCW = -1.2° (which is 1.2° CW)
            if angle_deg > 180:
                return angle_deg - 360
            return angle_deg
        elif angle_dir == "signed":
            # Convert to signed range: -180 to 180
            if angle_deg > 180:
                return angle_deg - 360
            return angle_deg
        else:
            # Default: CCW, 0-360
            return angle_deg

    def build(self) -> ReportIR:
        """Build the complete report intermediate representation."""
        report = ReportIR(
            title=self.problem.name,
            generated_date=datetime.now(),
            description=getattr(self.problem, 'description', None),
            diagram_path=self.diagram_path
        )

        # Add sections
        self._add_known_variables_section(report)
        self._add_unknown_variables_section(report)
        self._add_equations_section(report)
        self._add_solution_steps_section(report)
        self._add_results_section(report)

        return report

    def _add_known_variables_section(self, report: ReportIR) -> None:
        """Add the known variables section."""
        section = report.add_section("1. Known Variables")
        table = self._build_known_variables_table()
        if table:
            section.content.append(table)
        else:
            section.content.append("*No known variables*")

    def _add_unknown_variables_section(self, report: ReportIR) -> None:
        """Add the unknown variables section."""
        section = report.add_section("2. Unknown Variables")
        table = self._build_unknown_variables_table()
        if table:
            section.content.append(table)
        else:
            section.content.append("*No unknown variables*")

    def _add_equations_section(self, report: ReportIR) -> None:
        """Add the equations section."""
        section = report.add_section("3. Equations Used")
        equations = self._format_equation_list()
        for i, eq in enumerate(equations, 1):
            section.content.append(f"{i}. {eq}")

    def _add_solution_steps_section(self, report: ReportIR) -> None:
        """Add the solution steps section."""
        section = report.add_section("4. Step-by-Step Solution")
        steps = self._extract_solution_steps()

        if steps:
            for i, step_data in enumerate(steps, 1):
                # Strip "using Eq N" suffix from result_var (keep it only in title)
                result_var = step_data.equation_name
                if " using Eq " in result_var:
                    result_var = result_var.split(" using Eq ")[0]

                step = SolutionStep(
                    step_number=i,
                    title=step_data.equation_name,
                    equation=step_data.equation_str,
                    substituted=step_data.substituted_equation,
                    result_var=result_var,
                    result_value=step_data.result_value,
                    result_unit=step_data.result_unit
                )
                section.content.append(step)
        else:
            section.content.append("*No detailed solution steps available*")

    def _add_results_section(self, report: ReportIR) -> None:
        """Add the results summary section."""
        section = report.add_section("5. Summary of Results")

        if self._is_vector_equilibrium_problem():
            table = self._build_vector_results_table()
        else:
            table = self._build_standard_results_table()

        if table:
            section.content.append(table)
        else:
            section.content.append("*No results to summarize*")

    def _is_vector_equilibrium_problem(self) -> bool:
        """Check if problem is a VectorEquilibriumProblem or ParallelogramLawProblem.

        Detection is based on presence of 'forces' attribute with force vectors.
        """
        # Check for forces attribute (used by ParallelogramLawProblem and VectorEquilibriumProblem)
        if hasattr(self.problem, 'forces') and self.problem.forces:
            return True

        # Also check class hierarchy as fallback
        class_names = [cls.__name__ for cls in self.problem.__class__.__mro__]
        return 'VectorEquilibriumProblem' in class_names or 'ParallelogramLawProblem' in class_names

    def _build_known_variables_table(self) -> Table | None:
        """Build the known variables table."""
        known_data = self._get_known_variable_data()
        if not known_data:
            return None

        # Check if this is vector equilibrium format
        if known_data and 'magnitude' in known_data[0]:
            return self._build_force_table(known_data)
        else:
            return self._build_standard_known_table(known_data)

    def _build_unknown_variables_table(self) -> Table | None:
        """Build the unknown variables table."""
        unknown_data = self._get_unknown_variable_data()
        if not unknown_data:
            return None

        # Check if this is vector equilibrium format
        if unknown_data and 'magnitude' in unknown_data[0]:
            return self._build_force_table(unknown_data)
        else:
            return self._build_standard_unknown_table(unknown_data)

    def _get_axis_labels(self) -> tuple[str, str]:
        """Get the axis labels for table headers.

        Returns (axis1_label, axis2_label) based on the coordinate system.
        Defaults to ('x', 'y') for standard Cartesian coordinates.
        """
        coord_sys = getattr(self.problem, 'coordinate_system', None)
        if coord_sys is not None:
            axis1 = getattr(coord_sys, 'axis1_label', 'x')
            axis2 = getattr(coord_sys, 'axis2_label', 'y')
            return (axis1, axis2)
        return ('x', 'y')

    def _get_components_in_coordinate_system(self, vec_obj, si_factor: float = 1.0) -> tuple[str, str]:
        """Get vector components in the problem's coordinate system.

        For non-orthogonal coordinate systems (like u-v with 75° between axes),
        this converts the Cartesian x-y components to the custom coordinate system.

        Args:
            vec_obj: The vector object with _coords or u/v attributes
            si_factor: SI conversion factor for the unit

        Returns:
            Tuple of (component1_str, component2_str) formatted as strings with 1 decimal place.
            Returns ("?", "?") if components cannot be determined.
        """
        if vec_obj is None:
            return ("?", "?")

        # Get Cartesian x-y coordinates
        x_val = None
        y_val = None

        if hasattr(vec_obj, '_coords') and vec_obj._coords is not None and len(vec_obj._coords) >= 2:
            x_val = vec_obj._coords[0]
            y_val = vec_obj._coords[1]
        elif hasattr(vec_obj, 'u') and vec_obj.u and vec_obj.u.value is not None:
            # vec_obj.u and vec_obj.v store Cartesian x and y (confusingly named)
            x_val = vec_obj.u.value
            if hasattr(vec_obj, 'v') and vec_obj.v and vec_obj.v.value is not None:
                y_val = vec_obj.v.value

        if x_val is None or y_val is None:
            return ("?", "?")

        # Check if we have a non-orthogonal coordinate system
        coord_sys = getattr(self.problem, 'coordinate_system', None)
        if coord_sys is not None and not coord_sys.is_orthogonal:
            # Convert Cartesian x-y to the custom coordinate system
            comp1, comp2 = coord_sys.from_cartesian(x_val, y_val)
            # Avoid -0.0 display by using abs() for very small values
            comp1_display = comp1 / si_factor
            comp2_display = comp2 / si_factor
            if abs(comp1_display) < 0.05:
                comp1_display = abs(comp1_display)
            if abs(comp2_display) < 0.05:
                comp2_display = abs(comp2_display)
            return (f"{comp1_display:.1f}", f"{comp2_display:.1f}")
        else:
            # Standard orthogonal system - just use x and y directly
            # Avoid -0.0 display by using abs() for very small values
            x_display = x_val / si_factor
            y_display = y_val / si_factor
            if abs(x_display) < 0.05:
                x_display = abs(x_display)
            if abs(y_display) < 0.05:
                y_display = abs(y_display)
            return (f"{x_display:.1f}", f"{y_display:.1f}")

    def _build_force_table(self, data: list[dict]) -> Table:
        """Build a table for force vectors with component, Magnitude, Angle, Reference columns.

        Uses proper vector notation:
        - Symbol column shows vector with arrow (e.g., F̄₁)
        - Magnitude column header indicates |F̄| notation
        - Component headers use the coordinate system axes (e.g., Fᵤ, Fᵥ for u-v system)
        """
        unit = data[0].get('unit', 'unit') if data else 'unit'
        axis1, axis2 = self._get_axis_labels()

        # Build subscript characters for axis labels
        subscript_map = {'x': 'ₓ', 'y': 'ᵧ', 'u': 'ᵤ', 'v': 'ᵥ', 'n': 'ₙ', 't': 'ₜ'}
        sub1 = subscript_map.get(axis1.lower(), f'_{axis1}')
        sub2 = subscript_map.get(axis2.lower(), f'_{axis2}')

        columns = [
            TableColumn("Vector", TableAlignment.LEFT),
            TableColumn(f"F{sub1} ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"F{sub2} ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"|F| ({unit})", TableAlignment.DECIMAL),
            TableColumn("θ (deg)", TableAlignment.DECIMAL),
            TableColumn("Reference", TableAlignment.LEFT),
        ]

        rows = []
        for var in data:
            rows.append(TableRow([
                var['symbol'],
                var.get('x', ''),
                var.get('y', ''),
                var['magnitude'],
                var['angle'],
                var.get('reference', ''),
            ]))

        return Table(columns=columns, rows=rows)

    def _build_standard_known_table(self, data: list[dict]) -> Table:
        """Build a standard known variables table."""
        columns = [
            TableColumn("Symbol", TableAlignment.LEFT),
            TableColumn("Name", TableAlignment.LEFT),
            TableColumn("Value", TableAlignment.DECIMAL),
            TableColumn("Unit", TableAlignment.LEFT),
        ]

        rows = []
        for var in data:
            rows.append(TableRow([
                var['symbol'],
                var['name'],
                var['value'],
                var['unit'],
            ]))

        return Table(columns=columns, rows=rows)

    def _build_standard_unknown_table(self, data: list[dict]) -> Table:
        """Build a standard unknown variables table."""
        columns = [
            TableColumn("Symbol", TableAlignment.LEFT),
            TableColumn("Name", TableAlignment.LEFT),
            TableColumn("Unit", TableAlignment.LEFT),
        ]

        rows = []
        for var in data:
            rows.append(TableRow([
                var['symbol'],
                var['name'],
                var['unit'],
            ]))

        return Table(columns=columns, rows=rows)

    def _build_vector_results_table(self) -> Table | None:
        """Build results table for vector equilibrium problems.

        Shows solved unknowns - vectors that were originally unknown but now have
        computed values. This includes:
        - For forward problems: the resultant (F_R)
        - For inverse problems: the unknown component force (e.g., F_1)

        Uses proper vector notation:
        - Vector column shows vector with arrow
        - Magnitude column uses |F| notation
        """
        import math

        # Get original variable states to determine what was originally unknown
        original_var_states = getattr(self.problem, '_original_variable_states', {})

        # Find all vector-related variables by looking for *_mag and *_angle pairs
        vector_names = set()
        for var_name in self.problem.variables:
            if var_name.endswith('_mag'):
                vector_names.add(var_name[:-4])  # Remove '_mag' suffix
            elif var_name.endswith('_angle'):
                vector_names.add(var_name[:-6])  # Remove '_angle' suffix

        if not vector_names:
            return None

        # Determine unit from any vector's magnitude variable
        unit = "N"
        for vec_name in vector_names:
            mag_var = self.problem.variables.get(f"{vec_name}_mag")
            if mag_var and hasattr(mag_var, 'preferred') and mag_var.preferred:
                unit = mag_var.preferred.symbol
                break

        # Get axis labels from coordinate system
        axis1, axis2 = self._get_axis_labels()

        # Build subscript characters for axis labels
        subscript_map = {'x': 'ₓ', 'y': 'ᵧ', 'u': 'ᵤ', 'v': 'ᵥ', 'n': 'ₙ', 't': 'ₜ'}
        sub1 = subscript_map.get(axis1.lower(), f'_{axis1}')
        sub2 = subscript_map.get(axis2.lower(), f'_{axis2}')

        columns = [
            TableColumn("Vector", TableAlignment.LEFT),
            TableColumn(f"F{sub1} ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"F{sub2} ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"|F| ({unit})", TableAlignment.DECIMAL),
            TableColumn("θ (deg)", TableAlignment.DECIMAL),
            TableColumn("Reference", TableAlignment.LEFT),
        ]

        rows = []

        for vec_name in sorted(vector_names):
            mag_var = self.problem.variables.get(f"{vec_name}_mag")
            angle_var = self.problem.variables.get(f"{vec_name}_angle")

            if mag_var is None:
                continue

            # Determine if this vector was originally unknown
            mag_was_known = original_var_states.get(f"{vec_name}_mag", True)
            angle_was_known = original_var_states.get(f"{vec_name}_angle", True) if angle_var else True
            was_originally_unknown = not (mag_was_known and angle_was_known)

            # Only show vectors that were originally unknown (solved unknowns)
            if not was_originally_unknown:
                continue

            # Get vector object for additional data
            vec_obj = getattr(self.problem, vec_name, None)

            # Get unit's SI factor for display conversion
            si_factor = 1.0
            if vec_obj and hasattr(vec_obj, '_unit') and vec_obj._unit:
                si_factor = vec_obj._unit.si_factor

            # Get magnitude
            magnitude = "?"
            if mag_var.value is not None:
                if hasattr(mag_var, 'magnitude') and callable(mag_var.magnitude):
                    try:
                        magnitude = f"{mag_var.magnitude():.1f}"
                    except (ValueError, AttributeError):
                        magnitude = f"{mag_var.value:.1f}"
                else:
                    magnitude = f"{mag_var.value:.1f}"

            # Get reference axis - use problem's coordinate system if available
            # Note: Don't fall back to angle_reference if problem has a coordinate system,
            # as angle_reference defaults to +x which may not match the coordinate system
            ref = self._get_default_reference_axis()
            if vec_obj is not None and hasattr(vec_obj, '_original_wrt') and vec_obj._original_wrt:
                ref = vec_obj._original_wrt
            elif getattr(self.problem, 'coordinate_system', None) is None:
                # Only use angle_reference fallback if no custom coordinate system
                if vec_obj is not None and hasattr(vec_obj, 'angle_reference') and vec_obj.angle_reference:
                    if hasattr(vec_obj.angle_reference, 'axis_label'):
                        ref = vec_obj.angle_reference.axis_label

            # Get angle in degrees
            angle = "?"

            # First check if there's an original input angle we should preserve
            # (for vectors defined with known angles, like in inverse problems)
            if vec_obj is not None and hasattr(vec_obj, '_polar_angle_rad') and vec_obj._polar_angle_rad is not None:
                # Use the original input angle (preserves the sign convention from problem definition)
                angle = f"{math.degrees(vec_obj._polar_angle_rad):.1f}"
            elif angle_var is not None and angle_var.value is not None:
                angle_deg = angle_var.value * 180 / math.pi
                angle_deg = angle_deg % 360
                # Apply angle_dir conversion for solved unknowns
                angle_deg = self._convert_angle_for_display(angle_deg, vec_obj)
                angle = f"{angle_deg:.1f}"
            elif vec_obj is not None and hasattr(vec_obj, '_coords') and vec_obj._coords is not None:
                # Calculate angle from coordinates
                coords = vec_obj._coords
                if len(coords) >= 2:
                    angle_rad = math.atan2(coords[1], coords[0])
                    angle_deg = angle_rad * 180 / math.pi
                    if angle_deg < 0:
                        angle_deg += 360
                    # Apply angle_dir conversion for solved unknowns
                    angle_deg = self._convert_angle_for_display(angle_deg, vec_obj)
                    angle = f"{angle_deg:.1f}"

            # Get components in the coordinate system (handles non-orthogonal systems)
            fx, fy = self._get_components_in_coordinate_system(vec_obj, si_factor)

            rows.append(TableRow([vec_name, fx, fy, magnitude, angle, ref]))

        if not rows:
            return None

        return Table(columns=columns, rows=rows)

    def _build_standard_results_table(self) -> Table | None:
        """Build standard results summary table."""
        results = self._get_final_results()
        if not results:
            return None

        columns = [
            TableColumn("Variable", TableAlignment.LEFT),
            TableColumn("Name", TableAlignment.LEFT),
            TableColumn("Final Value", TableAlignment.DECIMAL),
            TableColumn("Unit", TableAlignment.LEFT),
        ]

        rows = []
        for res in results:
            rows.append(TableRow([
                res['symbol'],
                res['name'],
                res['value'],
                res['unit'],
            ]))

        return Table(columns=columns, rows=rows)

    def _get_known_variable_data(self) -> list[dict]:
        """Get known variable data formatted for tables.

        This reuses the logic from ReportGenerator._format_variable_table_data().
        """
        # Use specialized formatting for vector equilibrium problems
        if self._is_vector_equilibrium_problem():
            known, _ = self._get_force_variable_data()
            return known

        known_data = []
        for symbol, var in self.known_variables.items():
            # Use Quantity.magnitude() for proper unit conversion
            if hasattr(var, 'magnitude') and callable(var.magnitude):
                try:
                    value = var.magnitude()
                    value_str = f"{value:.1f}"
                except (ValueError, AttributeError):
                    value_str = f"{var.value:.1f}" if var.value is not None else "N/A"
            else:
                value_str = f"{var.value:.1f}" if var.value is not None else "N/A"

            # Get unit string
            if hasattr(var, 'preferred') and var.preferred:
                unit_str = var.preferred.symbol
            else:
                unit_str = ""

            known_data.append({
                "symbol": symbol,
                "name": getattr(var, "name", symbol),
                "value": value_str,
                "unit": unit_str
            })

        return known_data

    def _get_unknown_variable_data(self) -> list[dict]:
        """Get unknown variable data formatted for tables."""
        # Use specialized formatting for vector equilibrium problems
        if self._is_vector_equilibrium_problem():
            _, unknown = self._get_force_variable_data()
            return unknown

        unknown_data = []
        for symbol, var in self.problem.variables.items():
            if symbol not in self.known_variables:
                # Get unit string
                if hasattr(var, 'preferred') and var.preferred:
                    unit_str = var.preferred.symbol
                else:
                    unit_str = ""

                unknown_data.append({
                    "symbol": symbol,
                    "name": getattr(var, "name", symbol),
                    "unit": unit_str
                })

        return unknown_data

    def _get_force_variable_data(self) -> tuple[list[dict], list[dict]]:
        """Get force vector data formatted for tables.

        Returns (known_forces, unknown_forces).
        """
        known_data = []
        unknown_data = []

        forces = getattr(self.problem, 'forces', {})
        original_force_states = getattr(self.problem, '_original_force_states', {})

        # If forces dict is empty, look for _Vector attributes on the problem
        if not forces:
            return self._get_vector_variable_data()


        for force_name, force_obj in forces.items():
            mag_var = self.problem.variables.get(f"{force_name}_mag")
            angle_var = self.problem.variables.get(f"{force_name}_angle")

            if mag_var is None or angle_var is None:
                continue

            # Determine original known state
            force_was_originally_known = original_force_states.get(force_name, getattr(force_obj, 'is_known', True))
            original_var_states = getattr(self.problem, '_original_variable_states', {})
            mag_was_originally_known = original_var_states.get(f"{force_name}_mag_known", force_was_originally_known)
            angle_was_originally_known = original_var_states.get(f"{force_name}_angle_known", force_was_originally_known)

            # Get magnitude using proper qnty unit handling
            if mag_was_originally_known:
                if hasattr(mag_var, 'magnitude') and callable(mag_var.magnitude):
                    try:
                        mag_value = mag_var.magnitude()
                        mag_str = f"{mag_value:.1f}"
                    except (ValueError, AttributeError):
                        mag_str = "?"
                else:
                    mag_str = "?"
                mag_unit = mag_var.preferred.symbol if hasattr(mag_var, 'preferred') and mag_var.preferred else ""
            else:
                mag_str = "?"
                mag_unit = mag_var.preferred.symbol if hasattr(mag_var, 'preferred') and mag_var.preferred else ""

            # Get angle
            if angle_was_originally_known and angle_var.value is not None:
                import math
                angle_deg = angle_var.value * 180.0 / math.pi
                angle_deg = angle_deg % 360
                angle_str = f"{angle_deg:.1f}"
            else:
                angle_str = "?"

            # Get components in the coordinate system - only for originally known forces
            x_str = "?"
            y_str = "?"
            was_originally_known = mag_was_originally_known and angle_was_originally_known

            # Only populate components for forces that were originally known
            if was_originally_known:
                # Get SI factor for unit conversion
                si_factor = 1.0
                if hasattr(force_obj, '_unit') and force_obj._unit:
                    si_factor = force_obj._unit.si_factor
                x_str, y_str = self._get_components_in_coordinate_system(force_obj, si_factor)

            # Get angle reference
            reference_str = ""
            if hasattr(force_obj, 'angle_reference') and force_obj.angle_reference is not None:
                ref = force_obj.angle_reference
                if hasattr(ref, 'axis_label'):
                    reference_str = ref.axis_label

            force_data = {
                "symbol": force_name,
                "name": getattr(force_obj, 'name', force_name),
                "magnitude": mag_str,
                "angle": angle_str,
                "unit": mag_unit,
                "x": x_str,
                "y": y_str,
                "reference": reference_str
            }

            if was_originally_known:
                known_data.append(force_data)
            else:
                unknown_data.append(force_data)

        return known_data, unknown_data

    def _get_vector_variable_data(self) -> tuple[list[dict], list[dict]]:
        """Get vector data from _Vector attributes when forces dict is empty.

        Returns (known_vectors, unknown_vectors).
        """
        known_data = []
        unknown_data = []
        original_var_states = getattr(self.problem, '_original_variable_states', {})

        # Find all vector-related variables by looking for *_mag and *_angle pairs
        vector_names = set()
        for var_name in self.problem.variables:
            if var_name.endswith('_mag'):
                vector_names.add(var_name[:-4])  # Remove '_mag' suffix
            elif var_name.endswith('_angle'):
                vector_names.add(var_name[:-6])  # Remove '_angle' suffix

        for vec_name in sorted(vector_names):
            mag_var = self.problem.variables.get(f"{vec_name}_mag")
            angle_var = self.problem.variables.get(f"{vec_name}_angle")

            if mag_var is None:
                continue

            # Get the vector object for checking polar angle info
            vec_obj = getattr(self.problem, vec_name, None)

            # Determine original known state
            mag_was_known = original_var_states.get(f"{vec_name}_mag", True)
            # Check if angle was originally known either from _original_variable_states
            # or from having _polar_angle_rad set (for vectors with unknown magnitude but known angle)
            angle_was_known = original_var_states.get(f"{vec_name}_angle", True) if angle_var else True
            # Also check for _polar_angle_rad which indicates angle was specified at creation time
            if vec_obj is not None and hasattr(vec_obj, '_polar_angle_rad') and vec_obj._polar_angle_rad is not None:
                angle_was_known = True

            # Get magnitude using proper qnty unit handling
            if mag_was_known and mag_var.value is not None:
                if hasattr(mag_var, 'magnitude') and callable(mag_var.magnitude):
                    try:
                        mag_value = mag_var.magnitude()
                        mag_str = f"{mag_value:.1f}"
                    except (ValueError, AttributeError):
                        mag_str = "?"
                else:
                    mag_str = "?"
            else:
                mag_str = "?"

            mag_unit = mag_var.preferred.symbol if hasattr(mag_var, 'preferred') and mag_var.preferred else ""

            # Get angle in degrees - only show value if angle was originally known
            angle_str = ""

            # If angle was not originally known, show "?" regardless of computed value
            if not angle_was_known:
                angle_str = "?"
            # First try to use original angle from create_vector_polar (for fully known vectors)
            elif vec_obj is not None and hasattr(vec_obj, '_original_angle') and vec_obj._original_angle is not None:
                angle_str = f"{vec_obj._original_angle:.1f}"
            # Check for _polar_angle_rad (for vectors with unknown magnitude but known angle)
            elif vec_obj is not None and hasattr(vec_obj, '_polar_angle_rad') and vec_obj._polar_angle_rad is not None:
                import math
                # _polar_angle_rad stores the input angle in radians (before wrt conversion)
                # For display, we want to show the original input angle
                angle_deg = math.degrees(vec_obj._polar_angle_rad)
                angle_str = f"{angle_deg:.1f}"
            elif angle_var is not None and angle_var.value is not None:
                import math
                angle_deg = angle_var.value * 180.0 / math.pi
                angle_deg = angle_deg % 360
                angle_str = f"{angle_deg:.1f}"
            elif vec_obj is not None and hasattr(vec_obj, '_angle') and vec_obj._angle is not None:
                # Get angle from vector object directly
                import math
                angle_val = vec_obj._angle
                # Handle if _angle is a Quantity
                if hasattr(angle_val, 'value'):
                    angle_val = angle_val.value
                if angle_val is not None:
                    angle_deg = float(angle_val) * 180.0 / math.pi
                    angle_deg = angle_deg % 360
                    angle_str = f"{angle_deg:.1f}"
                else:
                    angle_str = "?"
            elif vec_obj is not None and hasattr(vec_obj, '_coords') and vec_obj._coords is not None:
                # Compute angle from coordinates
                import math
                coords = vec_obj._coords
                if len(coords) >= 2:
                    angle_rad = math.atan2(coords[1], coords[0])
                    angle_deg = math.degrees(angle_rad)
                    if angle_deg < 0:
                        angle_deg += 360
                    angle_str = f"{angle_deg:.1f}"
                else:
                    angle_str = "?"
            else:
                angle_str = "?"

            # Get components in the coordinate system - only for originally known vectors
            x_str = "?"
            y_str = "?"
            was_originally_known = mag_was_known and angle_was_known

            # Only populate components for vectors that were originally known
            if was_originally_known and vec_obj is not None:
                # Get SI factor for unit conversion
                si_factor = 1.0
                if hasattr(vec_obj, '_unit') and vec_obj._unit:
                    si_factor = vec_obj._unit.si_factor
                x_str, y_str = self._get_components_in_coordinate_system(vec_obj, si_factor)

            # Get angle reference - prefer original wrt from create_vector_polar
            # Use problem's coordinate system default if no reference is found
            # Note: Don't fall back to angle_reference if problem has a coordinate system,
            # as angle_reference defaults to +x which may not match the coordinate system
            reference_str = self._get_default_reference_axis()
            if vec_obj is not None and hasattr(vec_obj, '_original_wrt') and vec_obj._original_wrt is not None:
                reference_str = vec_obj._original_wrt
            elif getattr(self.problem, 'coordinate_system', None) is None:
                # Only use angle_reference fallback if no custom coordinate system
                if vec_obj is not None and hasattr(vec_obj, 'angle_reference') and vec_obj.angle_reference is not None:
                    ref = vec_obj.angle_reference
                    if hasattr(ref, 'axis_label'):
                        reference_str = ref.axis_label

            vector_data = {
                "symbol": vec_name,
                "name": getattr(vec_obj, 'name', vec_name) if vec_obj else vec_name,
                "magnitude": mag_str,
                "angle": angle_str,
                "unit": mag_unit,
                "x": x_str,
                "y": y_str,
                "reference": reference_str
            }

            if was_originally_known:
                known_data.append(vector_data)
            else:
                unknown_data.append(vector_data)

        return known_data, unknown_data

    def _format_equation_list(self) -> list[str]:
        """Format equations for display in solving order."""
        if self.solving_history:
            equation_strs = []
            used_equations = set()

            for step_data in self.solving_history:
                equation_str = step_data.get("equation_str", "")
                if equation_str and equation_str not in used_equations:
                    equation_strs.append(equation_str)
                    used_equations.add(equation_str)

            for eq in self.equations:
                eq_str = str(eq)
                if eq_str not in used_equations:
                    equation_strs.append(eq_str)

            return equation_strs

        return [str(eq) for eq in self.equations]

    def _extract_solution_steps(self) -> list:
        """Extract solution steps from solving history.

        Returns a list of step data objects with equation_name, equation_str,
        substituted_equation, result_value, result_unit.
        """
        from dataclasses import dataclass

        @dataclass
        class StepData:
            equation_name: str
            equation_str: str
            substituted_equation: str | None
            result_value: str
            result_unit: str

        steps = []
        for step_data in self.solving_history:
            # Extract target variable name
            equation_str = step_data.get("equation_str", "")
            target = step_data.get("target_variable", "")
            if not target and "=" in equation_str:
                target = equation_str.split("=")[0].strip()

            # Get result value and unit
            result_value = step_data.get("result_value", "")
            result_unit = step_data.get("result_unit", "")

            # Use equation_inline for step rendering (may be empty even if equation_str exists)
            # This allows equations to appear in "Equations Used" but not inline in the step
            equation_inline = step_data.get("equation_inline", equation_str)

            steps.append(StepData(
                equation_name=target,
                equation_str=equation_inline,  # Use inline version for step rendering
                substituted_equation=step_data.get("substituted_equation"),
                result_value=str(result_value),
                result_unit=str(result_unit)
            ))

        return steps

    def _get_final_results(self) -> list[dict]:
        """Get final results for all solved variables."""
        results = []

        for symbol, var in self.problem.variables.items():
            if symbol not in self.known_variables and var.value is not None:
                # Use Quantity.magnitude() for proper unit conversion
                if hasattr(var, 'magnitude') and callable(var.magnitude):
                    try:
                        value = var.magnitude()
                        value_str = f"{value:.1f}"
                    except (ValueError, AttributeError):
                        value_str = f"{var.value:.1f}"
                else:
                    value_str = f"{var.value:.1f}"

                # Get unit string
                if hasattr(var, 'preferred') and var.preferred:
                    unit_str = var.preferred.symbol
                else:
                    unit_str = ""

                results.append({
                    "symbol": symbol,
                    "name": getattr(var, "name", symbol),
                    "value": value_str,
                    "unit": unit_str
                })

        return results
