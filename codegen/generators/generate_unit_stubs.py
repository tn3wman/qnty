#!/usr/bin/env python3
"""
Standalone script to generate unit_catalog.pyi stub file.

This script reads the unit_catalog.py file and generates a corresponding
.pyi stub file with all units and aliases in alphabetical order.
"""

import sys
from pathlib import Path


def generate_unit_stubs(
    catalog_path: str = "src/qnty/core/unit_catalog.py",
    output_path: str = "src/qnty/core/unit_catalog.pyi"
) -> None:
    """Generate .pyi stub file by calling the existing write_units_stub function"""

    # Convert to Path objects for better handling
    catalog_file = Path(catalog_path)
    output_file = Path(output_path)

    if not catalog_file.exists():
        raise FileNotFoundError(f"Catalog file not found: {catalog_file}")

    # Import the unit module to access registries
    # We need to add the src directory to the path temporarily
    src_path = catalog_file.parent.parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        import tempfile

        # Import the unit module properly through the package
        # This will load all the catalogs and populate registries
        from qnty.core.unit import write_units_stub, _unit_registry, _unit_aliases

        # Parse the catalog file to get UnitNamespace classes
        namespaces = set()
        with open(catalog_file, 'r', encoding='utf-8') as f:
            content = f.read()

        import re
        namespace_pattern = r'^class\s+(\w+Units)\s*\(UnitNamespace\):'
        namespace_matches = re.findall(namespace_pattern, content, re.MULTILINE)
        namespaces.update(namespace_matches)

        # Create a temporary file for the write_units_stub output
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pyi') as temp_file:
            temp_path = temp_file.name

        try:
            # Call the existing write_units_stub function
            write_units_stub(temp_path)

            # Read the generated stub and modify it
            with open(temp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Modify the import to use relative import and add UnitNamespace classes
            stub_content = []
            stub_content.append("from typing import Final")
            stub_content.append("")
            stub_content.append("from .unit import Unit, UnitNamespace")
            stub_content.append("")

            # Add UnitNamespace classes first
            for namespace in sorted(namespaces):
                stub_content.append(f"class {namespace}(UnitNamespace): ...")
                stub_content.append("")

            # Add the Units class content from write_units_stub output
            # Skip the first few lines (imports and empty lines)
            in_class = False
            for line in lines:
                if line.startswith("class Units:"):
                    in_class = True
                    stub_content.append(line.rstrip())
                elif in_class or line.startswith("u:"):
                    # Check if this is a unit/alias declaration
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#") and ":" in stripped and not stripped.startswith("u:"):
                        # Extract the identifier name
                        identifier = stripped.split(":")[0].strip()
                        # Only include if it's a valid Python identifier
                        if identifier.isidentifier() and identifier.isascii():
                            stub_content.append(line.rstrip())
                    else:
                        # Not a declaration line (empty line, comment, or u: line)
                        stub_content.append(line.rstrip())

            # Write the final stub file
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(stub_content))
                f.write('\n')  # Final newline

            print(f"Generated stub file: {output_file}")
            print(f"  Canonical units: {len(_unit_registry)}")
            print(f"  Aliases: {len(_unit_aliases)}")
            print(f"  Namespaces: {len(namespaces)}")

        finally:
            # Clean up temp file
            import os
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    finally:
        # Clean up the path modification
        if str(src_path) in sys.path:
            sys.path.remove(str(src_path))


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate unit_catalog.pyi stub file"
    )
    parser.add_argument(
        "--catalog",
        default="src/qnty/core/unit_catalog.py",
        help="Path to unit_catalog.py file (default: %(default)s)"
    )
    parser.add_argument(
        "--output",
        default="src/qnty/core/unit_catalog.pyi",
        help="Output path for .pyi file (default: %(default)s)"
    )

    args = parser.parse_args()

    try:
        generate_unit_stubs(args.catalog, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()