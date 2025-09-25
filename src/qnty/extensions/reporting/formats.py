"""
Format-specific report generators for Markdown, LaTeX, and PDF.
"""

from __future__ import annotations

import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from .base import ReportGenerator


class MarkdownReportGenerator(ReportGenerator):
    """Generate reports in Markdown format."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a Markdown report."""
        output_path = Path(output_path)

        # Build the report content
        content = []

        # Title and header
        content.append(f"# Engineering Calculation Report: {self.problem.name}")
        content.append("")
        content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")

        if self.problem.description:
            content.append(f"**Description:** {self.problem.description}")
            content.append("")

        # Known variables table
        content.append("## 1. Known Variables")
        content.append("")
        known_vars, _ = self._format_variable_table_data()

        if known_vars:
            content.append("| Symbol | Name | Value | Unit |")
            content.append("|--------|------|-------|------|")
            for var in known_vars:
                content.append(f"| {var['symbol']} | {var['name']} | {var['value']} | {var['unit']} |")
        else:
            content.append("*No known variables*")
        content.append("")

        # Unknown variables table
        content.append("## 2. Unknown Variables (To Calculate)")
        content.append("")
        _, unknown_vars = self._format_variable_table_data()

        if unknown_vars:
            content.append("| Symbol | Name | Unit |")
            content.append("|--------|------|------|")
            for var in unknown_vars:
                content.append(f"| {var['symbol']} | {var['name']} | {var['unit']} |")
        else:
            content.append("*No unknown variables*")
        content.append("")

        # Equations
        content.append("## 3. Equations Used")
        content.append("")
        equations = self._format_equation_list()
        for i, eq in enumerate(equations, 1):
            content.append(f"{i}. `{eq}`")
        content.append("")

        # Solution steps
        content.append("## 4. Step-by-Step Solution")
        content.append("")
        steps = self._extract_solution_steps()

        if steps:
            for i, step in enumerate(steps, 1):
                # Use the target variable name (now contains just the variable)
                content.append(f"### Step {i}: Solve for {step.equation_name}")
                content.append("")

                # Show the original equation with indentation
                content.append("    **Equation:**")
                content.append("    ```")
                content.append(f"    {step.equation_str}")
                content.append("    ```")
                content.append("")

                # Show the substituted equation if different
                if step.substituted_equation and step.substituted_equation != step.equation_str:
                    content.append("    **Substitution:**")
                    content.append("    ```")
                    content.append(f"    {step.substituted_equation}")
                    content.append("    ```")
                    content.append("")

                # Format result as variable = value unit with indentation and large font
                content.append("    **Result:**")
                content.append("    ```")
                content.append(f"    {step.equation_name} = {step.result_value} {step.result_unit}")
                content.append("    ```")
                content.append("")
        else:
            content.append("*No detailed solution steps available*")
            content.append("")

        # Final results summary
        content.append("## 5. Summary of Results")
        content.append("")
        results = self._format_final_results()

        if results:
            content.append("| Variable | Name | Final Value | Unit |")
            content.append("|----------|------|-------------|------|")
            for res in results:
                content.append(f"| {res['symbol']} | {res['name']} | {res['value']} | {res['unit']} |")
        else:
            content.append("*No results to summarize*")

        content.append("")
        content.append("---")
        content.append("*Report generated using qnty library*")

        # Write to file
        output_path.write_text("\n".join(content), encoding="utf-8")


class LatexReportGenerator(ReportGenerator):
    """Generate reports in LaTeX format."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a LaTeX report."""
        output_path = Path(output_path)

        # Build the LaTeX document
        content = []

        # Document preamble
        content.append(r"\documentclass[11pt,a4paper]{article}")
        content.append(r"\usepackage{amsmath}")
        content.append(r"\usepackage{amssymb}")
        content.append(r"\usepackage{booktabs}")
        content.append(r"\usepackage{longtable}")
        content.append(r"\usepackage{geometry}")
        content.append(r"\geometry{margin=1in}")
        content.append(r"\usepackage{hyperref}")
        content.append(r"\usepackage{enumitem}")  # For customized list environments
        content.append("")
        content.append(r"\title{Engineering Calculation Report: " + self._escape_latex(self.problem.name) + "}")
        content.append(r"\date{" + datetime.now().strftime("%B %d, %Y") + "}")
        content.append("")
        content.append(r"\begin{document}")
        content.append(r"\maketitle")
        content.append("")

        if self.problem.description:
            content.append(r"\section*{Description}")
            content.append(self._escape_latex(self.problem.description))
            content.append("")

        # Known variables
        content.append(r"\section{Known Variables}")
        content.append("")
        known_vars, _ = self._format_variable_table_data()

        if known_vars:
            content.append(r"\begin{longtable}{llll}")
            content.append(r"\toprule")
            content.append(r"Symbol & Name & Value & Unit \\")
            content.append(r"\midrule")
            content.append(r"\endhead")

            for var in known_vars:
                content.append(f"${self._format_latex_variable(var['symbol'])}$ & {self._escape_latex(var['name'])} & {self._escape_latex(var['value'])} & {self._escape_latex(var['unit'])} \\\\")

            content.append(r"\bottomrule")
            content.append(r"\end{longtable}")
        else:
            content.append(r"\textit{No known variables}")
        content.append("")

        # Unknown variables
        content.append(r"\section{Unknown Variables (To Calculate)}")
        content.append("")
        _, unknown_vars = self._format_variable_table_data()

        if unknown_vars:
            content.append(r"\begin{longtable}{lll}")
            content.append(r"\toprule")
            content.append(r"Symbol & Name & Unit \\")
            content.append(r"\midrule")
            content.append(r"\endhead")

            for var in unknown_vars:
                content.append(f"${self._format_latex_variable(var['symbol'])}$ & {self._escape_latex(var['name'])} & {self._escape_latex(var['unit'])} \\\\")

            content.append(r"\bottomrule")
            content.append(r"\end{longtable}")
        else:
            content.append(r"\textit{No unknown variables}")
        content.append("")

        # Equations
        content.append(r"\section{Equations Used}")
        content.append("")
        content.append(r"\begin{enumerate}")
        equations = self._format_equation_list()
        for eq in equations:
            # Try to convert to LaTeX math if possible
            latex_eq = self._to_latex_math(eq)
            content.append(r"\item $" + r"\Large " + latex_eq + "$")
        content.append(r"\end{enumerate}")
        content.append("")

        # Solution steps
        content.append(r"\section{Step-by-Step Solution}")
        content.append("")
        steps = self._extract_solution_steps()

        if steps:
            # Start one enumerate environment for all steps with custom label
            content.append(r"\begin{enumerate}[label=\textbf{Step \arabic*:},leftmargin=2cm]")

            for i, step in enumerate(steps, 1):
                # Format equation name properly for LaTeX
                formatted_eq_name = step.equation_name
                if "=" in formatted_eq_name:
                    # This is an equation like "T = T_bar * (1 - U_m)"
                    parts = formatted_eq_name.split("=", 1)
                    if len(parts) == 2:
                        lhs = parts[0].strip()
                        rhs = parts[1].strip()
                        formatted_eq_name = f"${self._format_latex_variable(lhs)} = {self._to_latex_math(rhs)}$"
                    else:
                        formatted_eq_name = self._escape_latex(formatted_eq_name)
                else:
                    # Just a variable name
                    formatted_eq_name = f"${self._format_latex_variable(formatted_eq_name)}$"

                # Create step item - the label will automatically add "Step X:"
                content.append(r"\item \textbf{Solve for $" + self._format_latex_variable(step.equation_name) + "$}")
                content.append("")

                # Use description list for equation components with proper line breaks
                content.append(r"\begin{description}[leftmargin=2cm]")

                # Show the original equation
                content.append(r"\item[\textbf{Equation:}] \mbox{}")
                content.append("")
                original_latex_eq = self._to_latex_math(step.equation_str)
                # Add alignment marker at equals sign
                aligned_eq = original_latex_eq.replace(" = ", " &= ")
                content.append(r"\begin{aligned}")
                content.append(r"\Large " + aligned_eq)
                content.append(r"\end{aligned}")
                content.append("")

                # Show the substituted equation if different
                if step.substituted_equation and step.substituted_equation != step.equation_str:
                    content.append(r"\item[\textbf{Substitution:}] \mbox{}")
                    content.append("")
                    # Protect spaces in values like "90 psi" by replacing them with LaTeX space commands
                    latex_eq = self._to_latex_math(step.substituted_equation)
                    # Replace spaces between numbers and units with protected spaces
                    import re
                    latex_eq = re.sub(r'([0-9\.e\-\+]+)\s+([a-zA-Z]+)', r'\1\\,\\text{\2}', latex_eq)
                    # Add alignment marker at equals sign
                    aligned_eq = latex_eq.replace(" = ", " &= ")
                    content.append(r"\begin{aligned}")
                    content.append(r"\Large " + aligned_eq)
                    content.append(r"\end{aligned}")
                    content.append("")

                # Format result as variable = value unit
                content.append(r"\item[\textbf{Result:}] \mbox{}")
                content.append("")
                result_eq = self._format_latex_variable(step.equation_name) + " = " + self._escape_latex(str(step.result_value)) + r"\," + self._escape_latex(step.result_unit)
                # Add alignment marker at equals sign
                aligned_result = result_eq.replace(" = ", " &= ")
                content.append(r"\begin{aligned}")
                content.append(r"\Large " + aligned_result)
                content.append(r"\end{aligned}")
                content.append("")

                content.append(r"\end{description}")
                content.append("")

            # Close the enumerate environment
            content.append(r"\end{enumerate}")
            content.append("")
        else:
            content.append(r"\textit{No detailed solution steps available}")
        content.append("")

        # Summary
        content.append(r"\section{Summary of Results}")
        content.append("")
        results = self._format_final_results()

        if results:
            content.append(r"\begin{longtable}{llll}")
            content.append(r"\toprule")
            content.append(r"Variable & Name & Final Value & Unit \\")
            content.append(r"\midrule")
            content.append(r"\endhead")

            for res in results:
                content.append(f"${self._format_latex_variable(res['symbol'])}$ & {self._escape_latex(res['name'])} & {self._escape_latex(res['value'])} & {self._escape_latex(res['unit'])} \\\\")

            content.append(r"\bottomrule")
            content.append(r"\end{longtable}")
        else:
            content.append(r"\textit{No results to summarize}")

        content.append("")
        content.append(r"\end{document}")

        # Write to file
        output_path.write_text("\n".join(content), encoding="utf-8")

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not isinstance(text, str):
            text = str(text)

        # Special handling for _bar pattern (should be overline)
        # Don't escape these - we'll handle them in _format_latex_variable
        if "_bar" in text:
            return text

        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text

    def _format_latex_variable(self, var_symbol: str) -> str:
        """Format a variable symbol for LaTeX with proper handling of special patterns."""
        if not isinstance(var_symbol, str):
            var_symbol = str(var_symbol)

        # Handle _bar pattern - should be overline
        if var_symbol.endswith("_bar"):
            base_var = var_symbol[:-4]  # Remove "_bar"
            return f"\\overline{{{base_var}}}"

        # Handle other underscore patterns as subscripts
        if "_" in var_symbol:
            parts = var_symbol.split("_", 1)  # Split on first underscore only
            base = parts[0]
            subscript = parts[1]
            return f"{base}_{{{subscript}}}"

        # No special formatting needed
        return var_symbol

    def _to_latex_math(self, equation_str: str) -> str:
        r"""
        Convert equation string to properly formatted LaTeX math.

        This handles:
        1. Equations with assignment (e.g., "P = (a * b) / c" -> "P = \frac{a \cdot b}{c}")
        2. Pure expressions (e.g., "(a * b) / c" -> "\frac{a \cdot b}{c}")
        3. Complex nested expressions
        4. Variable name formatting with proper subscripts/overlines
        """
        import re

        # Clean up the input
        result = equation_str.strip()

        # Replace common operators first (before parsing structure)
        result = result.replace("==", "=")
        result = result.replace("sqrt(", r"\sqrt{")

        # Parse equation structure: check if it's an assignment (var = expression)
        assignment_match = re.match(r'^([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*(.+)$', result)

        if assignment_match:
            # This is an assignment equation like "P_max = ..."
            lhs_var = assignment_match.group(1)
            rhs_expr = assignment_match.group(2)

            # Format the LHS variable
            formatted_lhs = self._format_latex_variable(lhs_var)

            # Format the RHS expression
            formatted_rhs = self._format_expression(rhs_expr)

            return f"{formatted_lhs} = {formatted_rhs}"
        else:
            # This is a pure expression, format it directly
            return self._format_expression(result)

    def _format_expression(self, expr: str) -> str:
        r"""
        Format a mathematical expression (RHS of equation or standalone expression).

        Handles:
        - Fractions: (a*b)/(c*d) -> \frac{a \cdot b}{c \cdot d}
        - Multiplication: * -> \cdot
        - Variables: T_bar -> \overline{T}, P_max -> P_{max}
        - Functions: sqrt, sin, cos, etc.
        - Parentheses and complex nesting
        """
        import re

        expr = expr.strip()

        # Handle fractions by finding division operations at the right level
        # We need to be careful about parentheses nesting
        expr = self._convert_fractions(expr)

        # Replace multiplication operators
        expr = expr.replace("*", r" \cdot ")

        # Format variable names
        expr = self._format_variables_in_expression(expr)

        # Handle mathematical functions
        expr = self._format_math_functions(expr)

        return expr

    def _convert_fractions(self, expr: str) -> str:
        r"""
        Convert division operations to LaTeX fractions intelligently.

        Examples:
        - "a / b" -> "\frac{a}{b}"
        - "(a * b) / (c + d)" -> "\frac{a \cdot b}{c + d}"
        - "2 * (a / b) + c" -> "2 \cdot \frac{a}{b} + c"
        """
        # Handle the main division in the expression
        if "/" not in expr:
            return expr

        # Find the main division (not inside parentheses) - take the first one
        paren_level = 0
        division_pos = -1

        for i, char in enumerate(expr):
            if char == '(':
                paren_level += 1
            elif char == ')':
                paren_level -= 1
            elif char == '/' and paren_level == 0:
                division_pos = i
                break  # Take the first top-level division

        if division_pos == -1:
            return expr

        # Extract left and right parts
        left_part = expr[:division_pos].strip()
        right_part = expr[division_pos + 1:].strip()

        # Clean up parentheses if they wrap the entire expression
        if left_part.startswith('(') and left_part.endswith(')'):
            left_part = left_part[1:-1].strip()
        if right_part.startswith('(') and right_part.endswith(')'):
            right_part = right_part[1:-1].strip()

        return f"\\frac{{{left_part}}}{{{right_part}}}"


    def _format_variables_in_expression(self, expr: str) -> str:
        """Format variable names in an expression, preserving LaTeX commands."""
        import re

        def replace_variable(match):
            var_name = match.group(0)
            # Don't replace LaTeX commands
            if any(cmd in var_name.lower() for cmd in ['frac', 'sqrt', 'cdot', 'overline']):
                return var_name
            return self._format_latex_variable(var_name)

        # Pattern to match variable names, but not LaTeX commands
        var_pattern = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'

        # Split by backslash to avoid replacing LaTeX commands
        parts = expr.split('\\')

        # Format variables in the first part (before any LaTeX commands)
        parts[0] = re.sub(var_pattern, replace_variable, parts[0])

        # For subsequent parts, be more careful
        for i in range(1, len(parts)):
            if parts[i]:
                # Don't replace if this part starts with a LaTeX command
                if not any(parts[i].startswith(cmd) for cmd in ['frac{', 'sqrt{', 'cdot', 'overline{']):
                    # Find content after the command and format variables there
                    # This is a simplified approach - for more complex cases, we'd need a proper parser
                    parts[i] = re.sub(var_pattern, replace_variable, parts[i])

        return '\\'.join(parts)

    def _format_math_functions(self, expr: str) -> str:
        """Format mathematical functions for LaTeX."""
        # Handle common mathematical functions
        functions = {
            'sin': r'\sin',
            'cos': r'\cos',
            'tan': r'\tan',
            'log': r'\log',
            'ln': r'\ln',
            'exp': r'\exp'
        }

        for func, latex_func in functions.items():
            # Replace function calls like sin(x) with \sin{x}
            expr = expr.replace(f'{func}(', f'{latex_func}{{')

        return expr


class PdfReportGenerator(LatexReportGenerator):
    """Generate reports in PDF format using tectonic or system LaTeX."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a PDF report by first creating LaTeX then compiling to PDF."""
        output_path = Path(output_path)

        # Create a temporary LaTeX file
        import tempfile
        import os

        # Create temp file and close it immediately to avoid file locking issues
        fd, temp_path = tempfile.mkstemp(suffix=".tex", text=True)
        os.close(fd)
        tex_path = Path(temp_path)

        try:
            # Generate LaTeX content
            super().generate(tex_path)

            # Try different PDF compilation methods
            pdf_generated = False

            # Method 1: Try tectonic executable
            if not pdf_generated:
                pdf_generated = self._try_tectonic_binary(tex_path, output_path)

            # Method 2: Try system tectonic command
            if not pdf_generated:
                pdf_generated = self._try_system_tectonic(tex_path, output_path)

            # Method 3: Try pdflatex
            if not pdf_generated:
                pdf_generated = self._try_pdflatex(tex_path, output_path)

            # If no method worked, keep the LaTeX file and inform the user
            if not pdf_generated:
                # Copy LaTeX file to output location with .tex extension
                tex_output = output_path.with_suffix('.tex')
                import shutil
                shutil.copy2(tex_path, tex_output)

                raise RuntimeError(
                    f"PDF generation failed. LaTeX file saved to {tex_output}. "
                    "Please install tectonic (https://tectonic-typesetting.github.io/) "
                    "or a LaTeX distribution (TeX Live, MiKTeX) to generate PDFs."
                )
        finally:
            # Clean up temporary file
            if tex_path.exists():
                try:
                    tex_path.unlink()
                except Exception:
                    pass  # Ignore errors during cleanup

    def _try_tectonic_binary(self, tex_path: Path, output_path: Path) -> bool:
        """Try to use the bundled tectonic binary."""
        import platform

        # Determine the correct binary name based on platform
        system = platform.system().lower()
        if system == "windows":
            binary_name = "tectonic.exe"
        elif system == "darwin":  # macOS
            binary_name = "tectonic"
        else:  # Linux and others
            binary_name = "tectonic"

        tectonic_path = Path(__file__).parent / binary_name

        if not tectonic_path.exists():
            return False

        try:
            # Make sure it's executable on Unix-like systems
            if system != "windows":
                import os
                import stat
                st = os.stat(tectonic_path)
                os.chmod(tectonic_path, st.st_mode | stat.S_IEXEC)

            result = subprocess.run(
                [str(tectonic_path), str(tex_path), "-o", str(output_path.parent)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                # Rename the output file to the desired name
                generated_pdf = tex_path.with_suffix(".pdf")
                if generated_pdf.exists():
                    generated_pdf.rename(output_path)
                    return True
        except Exception:
            pass

        return False

    def _try_system_tectonic(self, tex_path: Path, output_path: Path) -> bool:
        """Try to use system-installed tectonic."""
        try:
            # Check if tectonic is available in PATH
            check_result = subprocess.run(
                ["tectonic", "--version"],
                capture_output=True,
                timeout=5
            )

            if check_result.returncode != 0:
                return False

            # Run tectonic
            result = subprocess.run(
                ["tectonic", str(tex_path), "-o", str(output_path.parent)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                # Rename the output file to the desired name
                generated_pdf = tex_path.with_suffix(".pdf")
                if generated_pdf.exists():
                    generated_pdf.rename(output_path)
                    return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return False

    def _try_pdflatex(self, tex_path: Path, output_path: Path) -> bool:
        """Try to use system-installed pdflatex."""
        try:
            # Check if pdflatex is available
            check_result = subprocess.run(
                ["pdflatex", "--version"],
                capture_output=True,
                timeout=5
            )

            if check_result.returncode != 0:
                return False

            # Run pdflatex (need to run twice for references)
            for _ in range(2):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(tex_path.parent), str(tex_path)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(tex_path.parent)
                )

            # Check if PDF was generated
            generated_pdf = tex_path.with_suffix(".pdf")
            if generated_pdf.exists():
                # Move to final location
                import shutil
                shutil.move(str(generated_pdf), str(output_path))

                # Clean up auxiliary files
                for ext in ['.aux', '.log', '.out']:
                    aux_file = tex_path.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()

                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return False
