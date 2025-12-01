"""
Format-specific report generators for Markdown, LaTeX, and PDF.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ...utils.shared_utilities import escape_latex
from .base import ReportGenerator


def _is_vector_equilibrium_problem(problem) -> bool:
    """Check if problem is a VectorEquilibriumProblem."""
    # Avoid circular import by checking class name in MRO
    class_names = [cls.__name__ for cls in problem.__class__.__mro__]
    return "VectorEquilibriumProblem" in class_names


def _generate_diagram_if_needed(problem, output_dir: Path) -> Path | None:
    """Generate vector diagram for VectorEquilibriumProblem if applicable."""
    if not _is_vector_equilibrium_problem(problem):
        return None

    try:
        from .vector_diagram import create_force_diagram

        # Generate diagram in same directory as report
        # Sanitize filename - remove problematic characters
        safe_name = problem.name.replace(" ", "_").replace(":", "").replace("/", "_").replace("\\", "_")
        diagram_path = output_dir / f"{safe_name}_diagram.png"
        return create_force_diagram(problem, diagram_path, show_components=False)
    except Exception as e:
        # Log but don't fail if diagram generation not available
        import logging

        logging.debug(f"Could not generate diagram: {e}")
        return None


def _handle_generated_pdf_output(tex_path: Path, output_path: Path) -> bool:
    """
    Handle moving the generated PDF to the desired output location.

    Tectonic and similar tools output PDFs with the same basename as the input .tex file.
    This function handles renaming/moving the generated PDF to the desired output path.

    Args:
        tex_path: Path to the input .tex file (used to determine generated PDF name)
        output_path: Desired final output path for the PDF

    Returns:
        True if the PDF was found and successfully moved/renamed, False otherwise
    """
    temp_pdf_name = tex_path.stem + ".pdf"
    generated_pdf = output_path.parent / temp_pdf_name
    if generated_pdf.exists():
        if generated_pdf != output_path:
            # Remove existing output file if it exists (Windows requires this)
            if output_path.exists():
                output_path.unlink()
            generated_pdf.rename(output_path)
        return True
    return False


def _build_report_ir(generator: ReportGenerator, diagram_path: Path | None):
    """
    Build the report intermediate representation (IR) from a generator.

    This consolidates the repeated ReportBuilder instantiation pattern.

    Args:
        generator: ReportGenerator instance with problem, known_variables, equations, solving_history
        diagram_path: Optional path to the generated diagram

    Returns:
        Built report IR
    """
    from .report_ir import ReportBuilder

    builder = ReportBuilder(
        problem=generator.problem,
        known_variables=generator.known_variables,
        equations=generator.equations,
        solving_history=generator.solving_history,
        diagram_path=diagram_path,
    )
    return builder.build()


class MarkdownReportGenerator(ReportGenerator):
    """Generate reports in Markdown format using the unified IR system."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a Markdown report."""
        from .report_ir import MarkdownRenderer

        output_path = Path(output_path)

        # Generate vector diagram if applicable
        diagram_path = _generate_diagram_if_needed(self.problem, output_path.parent)

        # Build the report IR and render
        report_ir = _build_report_ir(self, diagram_path)
        renderer = MarkdownRenderer()
        renderer.render(report_ir, output_path)

    def _format_disclaimer(self) -> list[str]:
        """Disclaimer is handled by the MarkdownRenderer."""
        return []


class LatexReportGenerator(ReportGenerator):
    """Generate reports in LaTeX format using the unified IR system."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a LaTeX report."""
        from .report_ir import LaTeXRenderer

        output_path = Path(output_path)

        # Generate vector diagram if applicable
        diagram_path = _generate_diagram_if_needed(self.problem, output_path.parent)

        # Build the report IR and render
        report_ir = _build_report_ir(self, diagram_path)
        renderer = LaTeXRenderer()
        renderer.render(report_ir, output_path)

    # Keep helper methods for backward compatibility with PdfReportGenerator
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        return escape_latex(text)

    def _format_disclaimer(self) -> list[str]:
        """Disclaimer is handled by the LaTeXRenderer."""
        return []


class PdfReportGenerator(LatexReportGenerator):
    """Generate reports in PDF format using tectonic or system LaTeX."""

    def generate(self, output_path: str | Path) -> None:
        """Generate a PDF report by first creating LaTeX then compiling to PDF."""
        output_path = Path(output_path)

        # Create a temporary LaTeX file
        import os
        import tempfile

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
                tex_output = output_path.with_suffix(".tex")
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

        # Also try without extension (for binaries downloaded without .exe)
        if not tectonic_path.exists():
            tectonic_path_no_ext = Path(__file__).parent / "tectonic"
            if tectonic_path_no_ext.exists():
                tectonic_path = tectonic_path_no_ext
            else:
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
                timeout=60,
            )

            if result.returncode == 0:
                # Tectonic outputs to the directory specified by -o with the same basename as the tex file
                # So if tex_path is /tmp/tmpXXX.tex and -o is /reports, PDF will be /reports/tmpXXX.pdf
                if _handle_generated_pdf_output(tex_path, output_path):
                    return True
        except Exception:
            pass

        return False

    def _try_system_tectonic(self, tex_path: Path, output_path: Path) -> bool:
        """Try to use system-installed tectonic."""
        try:
            # Check if tectonic is available in PATH
            check_result = subprocess.run(["tectonic", "--version"], capture_output=True, timeout=5)

            if check_result.returncode != 0:
                return False

            # Run tectonic
            result = subprocess.run(
                ["tectonic", str(tex_path), "-o", str(output_path.parent)],
                capture_output=True,
                timeout=60,
            )

            if result.returncode == 0:
                # Tectonic outputs to the directory specified by -o with the same basename as the tex file
                if _handle_generated_pdf_output(tex_path, output_path):
                    return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return False

    def _try_pdflatex(self, tex_path: Path, output_path: Path) -> bool:
        """Try to use system-installed pdflatex."""
        try:
            # Check if pdflatex is available
            check_result = subprocess.run(["pdflatex", "--version"], capture_output=True, timeout=5)

            if check_result.returncode != 0:
                return False

            # Run pdflatex (need to run twice for references)
            for _ in range(2):
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(tex_path.parent), str(tex_path)], capture_output=True, timeout=60, cwd=str(tex_path.parent))

            # Check if PDF was generated
            generated_pdf = tex_path.with_suffix(".pdf")
            if generated_pdf.exists():
                # Move to final location
                import shutil

                shutil.move(str(generated_pdf), str(output_path))

                # Clean up auxiliary files
                for ext in [".aux", ".log", ".out"]:
                    aux_file = tex_path.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()

                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return False
