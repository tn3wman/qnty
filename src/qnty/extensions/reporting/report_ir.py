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
    content: list[str | Table | Equation | SolutionStep | "Section"] = field(default_factory=list)


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
    """Render ReportIR to Markdown format."""

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
                lines.append(item)
                lines.append("")
            elif isinstance(item, Table):
                lines.extend(self._render_table(item))
            elif isinstance(item, Equation):
                lines.append(f"`{item.text}`")
                lines.append("")
            elif isinstance(item, SolutionStep):
                lines.extend(self._render_solution_step(item))
            elif isinstance(item, Section):
                lines.extend(self._render_section(item))

        return lines

    def _render_table(self, table: Table) -> list[str]:
        """Render a table to Markdown."""
        if not table.columns:
            return ["*No data*", ""]

        lines = []

        # Header row
        header = "| " + " | ".join(col.header for col in table.columns) + " |"
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
                row_text = "| " + " | ".join(row.cells) + " |"
                lines.append(row_text)

        lines.append("")
        return lines

    def _render_solution_step(self, step: SolutionStep) -> list[str]:
        """Render a solution step to Markdown."""
        lines = []

        lines.append(f"### Step {step.step_number}: Solve for {step.title}")
        lines.append("")

        # Equation
        lines.append("    **Equation:**")
        lines.append("    ```")
        lines.append(f"    {step.equation}")
        lines.append("    ```")
        lines.append("")

        # Substitution
        if step.substituted and step.substituted != step.equation:
            lines.append("    **Substitution:**")
            lines.append("    ```")
            lines.append(f"    {step.substituted}")
            lines.append("    ```")
            lines.append("")

        # Result
        lines.append("    **Result:**")
        lines.append("    ```")
        lines.append(f"    {step.result_var} = {step.result_value} {step.result_unit}")
        lines.append("    ```")
        lines.append("")

        return lines

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
            "",
            r"\title{Engineering Calculation Report: " + self._escape_latex(report.title) + "}",
            r"\date{" + report.generated_date.strftime("%B %d, %Y") + "}",
            "",
        ]

    def _render_section(self, section: Section) -> list[str]:
        """Render a section to LaTeX."""
        lines = []

        # Section header
        if section.level == 1:
            lines.append(r"\section{" + self._escape_latex(section.title) + "}")
        elif section.level == 2:
            lines.append(r"\subsection{" + self._escape_latex(section.title) + "}")
        else:
            lines.append(r"\subsubsection{" + self._escape_latex(section.title) + "}")
        lines.append("")

        # Content
        for item in section.content:
            if isinstance(item, str):
                lines.append(self._escape_latex(item))
                lines.append("")
            elif isinstance(item, Table):
                lines.extend(self._render_table(item))
            elif isinstance(item, Equation):
                latex_eq = self._to_latex_math(item.text) if not item.is_latex else item.text
                lines.append(r"\begin{enumerate}")
                lines.append(r"\item $\displaystyle\Large " + latex_eq + "$")
                lines.append(r"\end{enumerate}")
                lines.append("")
            elif isinstance(item, SolutionStep):
                lines.extend(self._render_solution_step(item))
            elif isinstance(item, Section):
                lines.extend(self._render_section(item))

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
            if col.alignment == TableAlignment.DECIMAL:
                # Wrap in braces for siunitx S columns
                header_cells.append("{" + self._escape_latex(col.header) + "}")
            else:
                header_cells.append(self._escape_latex(col.header))
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

        lines.append(r"\subsection*{Step " + str(step.step_number) + ": Solve for " + self._escape_latex(step.title) + "}")
        lines.append("")

        # Equation
        lines.append(r"\textbf{Equation:}")
        lines.append(r"\begin{equation*}")
        lines.append(self._to_latex_math(step.equation))
        lines.append(r"\end{equation*}")

        # Substitution
        if step.substituted and step.substituted != step.equation:
            lines.append(r"\textbf{Substitution:}")
            lines.append(r"\begin{equation*}")
            lines.append(self._to_latex_math(step.substituted))
            lines.append(r"\end{equation*}")

        # Result
        lines.append(r"\textbf{Result:}")
        lines.append(r"\begin{equation*}")
        result_latex = self._format_latex_variable(step.result_var) + " = " + step.result_value
        if step.result_unit:
            result_latex += r" \text{ " + self._escape_latex(step.result_unit) + "}"
        lines.append(result_latex)
        lines.append(r"\end{equation*}")
        lines.append("")

        return lines

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

    def _format_latex_variable(self, name: str) -> str:
        """Format a variable name for LaTeX math mode."""
        if not name:
            return ""

        # Handle subscripts
        if "_" in name:
            parts = name.split("_", 1)
            base = parts[0]
            subscript = parts[1] if len(parts) > 1 else ""

            # Multi-character subscripts need braces
            if len(subscript) > 1:
                return f"{base}_{{{subscript}}}"
            else:
                return f"{base}_{subscript}"

        return name

    def _to_latex_math(self, text: str) -> str:
        """Convert equation text to LaTeX math notation."""
        if not text:
            return ""

        result = text

        # Replace common operators
        result = result.replace("*", r" \cdot ")
        result = result.replace("sqrt(", r"\sqrt{")
        result = result.replace("sin(", r"\sin(")
        result = result.replace("cos(", r"\cos(")
        result = result.replace("tan(", r"\tan(")
        result = result.replace("**", "^")

        # Handle variable names with subscripts
        import re
        result = re.sub(r'([A-Za-z]+)_(\w+)', r'\1_{\2}', result)

        # Close sqrt braces
        result = result.replace(r"\sqrt{", r"\sqrt{").replace(")", "}")

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
        section = report.add_section("2. Unknown Variables (To Calculate)")
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
                step = SolutionStep(
                    step_number=i,
                    title=step_data.equation_name,
                    equation=step_data.equation_str,
                    substituted=step_data.substituted_equation,
                    result_var=step_data.equation_name,
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

    def _build_force_table(self, data: list[dict]) -> Table:
        """Build a table for force vectors with X, Y, Magnitude, Angle, Reference columns."""
        unit = data[0].get('unit', 'unit') if data else 'unit'

        columns = [
            TableColumn("Symbol", TableAlignment.LEFT),
            TableColumn(f"X ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"Y ({unit})", TableAlignment.DECIMAL),
            TableColumn(f"Magnitude ({unit})", TableAlignment.DECIMAL),
            TableColumn("Angle (deg)", TableAlignment.DECIMAL),
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
        """Build results table for vector equilibrium problems."""
        if not hasattr(self.problem, 'forces'):
            return None

        columns = [
            TableColumn("Symbol", TableAlignment.LEFT),
            TableColumn("Magnitude (N)", TableAlignment.DECIMAL),
            TableColumn("Angle (deg)", TableAlignment.DECIMAL),
            TableColumn("F_x (N)", TableAlignment.DECIMAL),
            TableColumn("F_y (N)", TableAlignment.DECIMAL),
        ]

        rows = []
        for _force_name, force in self.problem.forces.items():
            symbol = force.name

            # Get magnitude using proper qnty unit handling
            if force.magnitude and force.magnitude.value is not None:
                magnitude = f"{force.magnitude.magnitude():.6g}"
            else:
                magnitude = "?"

            # Get angle in degrees
            if force.angle and force.angle.value is not None:
                import math
                angle_deg = force.angle.value * 180 / math.pi
                angle_deg = angle_deg % 360
                angle = f"{angle_deg:.6g}"
            else:
                angle = "?"

            # Get components using proper qnty unit handling
            if hasattr(force, 'u') and force.u and force.u.value is not None:
                fx = f"{force.u.magnitude():.6g}"
            else:
                fx = "?"

            if hasattr(force, 'v') and force.v and force.v.value is not None:
                fy = f"{force.v.magnitude():.6g}"
            else:
                fy = "?"

            rows.append(TableRow([symbol, magnitude, angle, fx, fy]))

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
                    value_str = f"{value:.6g}"
                except (ValueError, AttributeError):
                    value_str = f"{var.value:.6g}" if var.value is not None else "N/A"
            else:
                value_str = f"{var.value:.6g}" if var.value is not None else "N/A"

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
                        mag_str = f"{mag_value:.6g}"
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
                angle_str = f"{angle_deg:.6g}"
            else:
                angle_str = "?"

            # Get X and Y components using proper qnty unit handling
            x_str = ""
            y_str = ""
            was_originally_known = mag_was_originally_known and angle_was_originally_known

            if hasattr(force_obj, 'u') and hasattr(force_obj, 'v') and force_obj._coords is not None:
                if was_originally_known or (mag_var.value is not None and angle_var.value is not None):
                    try:
                        u_qty = force_obj.u
                        v_qty = force_obj.v
                        if u_qty is not None and u_qty.value is not None:
                            x_str = f"{u_qty.magnitude():.6g}"
                        if v_qty is not None and v_qty.value is not None:
                            y_str = f"{v_qty.magnitude():.6g}"
                    except (ValueError, AttributeError):
                        pass

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

            # Determine original known state
            mag_was_known = original_var_states.get(f"{vec_name}_mag", True)
            angle_was_known = original_var_states.get(f"{vec_name}_angle", True) if angle_var else True

            # Get magnitude using proper qnty unit handling
            if mag_was_known and mag_var.value is not None:
                if hasattr(mag_var, 'magnitude') and callable(mag_var.magnitude):
                    try:
                        mag_value = mag_var.magnitude()
                        mag_str = f"{mag_value:.6g}"
                    except (ValueError, AttributeError):
                        mag_str = "?"
                else:
                    mag_str = "?"
            else:
                mag_str = "?"

            mag_unit = mag_var.preferred.symbol if hasattr(mag_var, 'preferred') and mag_var.preferred else ""

            # Get angle in degrees - only show value if angle was originally known
            angle_str = ""
            vec_obj = getattr(self.problem, vec_name, None)

            # If angle was not originally known, show "?" regardless of computed value
            if not angle_was_known:
                angle_str = "?"
            # First try to use original angle from create_vector_polar
            elif vec_obj is not None and hasattr(vec_obj, '_original_angle') and vec_obj._original_angle is not None:
                angle_str = f"{vec_obj._original_angle:.6g}"
            elif angle_var is not None and angle_var.value is not None:
                import math
                angle_deg = angle_var.value * 180.0 / math.pi
                angle_deg = angle_deg % 360
                angle_str = f"{angle_deg:.6g}"
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
                    angle_str = f"{angle_deg:.6g}"
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
                    angle_str = f"{angle_deg:.6g}"
                else:
                    angle_str = "?"
            else:
                angle_str = "?"

            # Get X and Y components
            x_str = ""
            y_str = ""
            was_originally_known = mag_was_known and angle_was_known

            # Try to get vector object to extract components (vec_obj already retrieved above)
            if vec_obj is not None and hasattr(vec_obj, 'u') and hasattr(vec_obj, 'v'):
                angle_has_value = (angle_var is not None and angle_var.value is not None) or (hasattr(vec_obj, '_angle') and vec_obj._angle is not None)
                if was_originally_known or (mag_var.value is not None and angle_has_value):
                    try:
                        u_qty = vec_obj.u
                        v_qty = vec_obj.v
                        if u_qty is not None and u_qty.value is not None:
                            x_str = f"{u_qty.magnitude():.6g}"
                        if v_qty is not None and v_qty.value is not None:
                            y_str = f"{v_qty.magnitude():.6g}"
                    except (ValueError, AttributeError):
                        pass

            # Get angle reference - prefer original wrt from create_vector_polar
            reference_str = ""
            if vec_obj is not None and hasattr(vec_obj, '_original_wrt') and vec_obj._original_wrt is not None:
                reference_str = vec_obj._original_wrt
            elif vec_obj is not None and hasattr(vec_obj, 'angle_reference') and vec_obj.angle_reference is not None:
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

            steps.append(StepData(
                equation_name=target,
                equation_str=equation_str,
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
                        value_str = f"{value:.6g}"
                    except (ValueError, AttributeError):
                        value_str = f"{var.value:.6g}"
                else:
                    value_str = f"{var.value:.6g}"

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
