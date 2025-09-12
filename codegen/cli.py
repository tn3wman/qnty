#!/usr/bin/env python3
"""
Code Generation CLI
==================

Command-line interface for generating all qnty files in the correct dependency order:
1. dimensions.py - Base dimensional constants
2. units.py - Unit class definitions
3. setters.py - Setter classes with unit properties
4. quantities.py - Quantity classes
5. quantities.pyi - Type stubs for IDE support

Can be run from IDE or command line:
- From command line: python cli.py
- From IDE: Run this file directly
"""

import subprocess
import sys
from pathlib import Path


def run_generator(generator_name: str, script_path: Path) -> tuple[bool, str]:
    """Run a single generator script and return success status with output."""
    try:
        print(f"\n{'=' * 60}")
        print(f"Running {generator_name}...")
        print(f"{'=' * 60}")

        # Run the generator script as a module to allow relative imports
        # Run from codegen directory with generators.module_name path
        module_name = f"generators.{script_path.stem}"
        result = subprocess.run(
            [sys.executable, "-m", module_name],
            capture_output=True,
            text=True,
            cwd=script_path.parents[1],  # Run from codegen directory
        )

        # Print the output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(f"STDERR: {result.stderr}")

        if result.returncode == 0:
            print(f"SUCCESS: {generator_name} completed successfully")
            return True, result.stdout
        else:
            print(f"FAILED: {generator_name} failed with return code {result.returncode}")
            return False, result.stderr

    except Exception as e:
        error_msg = f"Error running {generator_name}: {str(e)}"
        print(error_msg)
        return False, error_msg


def main() -> int:
    """Main CLI function that runs all generators in dependency order."""
    print("Qnty Code Generation Pipeline")
    print("============================")
    print("Generating all files in dependency order...")

    # Get the generators subdirectory
    script_dir = Path(__file__).parent / "generators"

    # Define generators in dependency order
    generators: list[tuple[str, str]] = [
        ("Field Dimensions Generator", "field_dims.py"),
        ("Field Units Generator", "field_units.py"),
        ("Field Converters Generator", "field_converters.py"),
        ("Field Setters Generator", "field_setter.py"),
        ("Field Variables Generator", "field_vars.py"),
    ]

    # Track results
    success_count = 0
    total_count = len(generators)
    failed_generators = []

    # Run each generator in order
    for generator_name, script_name in generators:
        script_path = script_dir / script_name

        if not script_path.exists():
            print(f"FAILED: {generator_name}: Script not found at {script_path}")
            failed_generators.append(generator_name)
            continue

        success, output = run_generator(generator_name, script_path)
        if success:
            success_count += 1
        else:
            failed_generators.append(generator_name)
            print(f"Output: {output}")

    # Print final summary
    print(f"\n{'=' * 60}")
    print("GENERATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Successful: {success_count}/{total_count}")

    if failed_generators:
        print(f"Failed: {', '.join(failed_generators)}")
        return 1
    else:
        print("SUCCESS: All generators completed successfully!")
        print("\nGenerated files:")
        print("  - src/qnty/dimensions/field_dims.py")
        print("  - src/qnty/units/units.py")
        print("  - src/qnty/units/converters.py")
        print("  - src/qnty/quantities/field_setter.py")
        print("  - src/qnty/quantities/field_vars.py")
        print("  - src/qnty/quantities/field_vars.pyi")
        return 0


if __name__ == "__main__":
    exit_code = main()

    # If running from IDE, pause so user can see results
    if hasattr(sys, "ps1") or "idlelib" in sys.modules or "IPython" in sys.modules:
        input("\nPress Enter to continue...")

    sys.exit(exit_code)
