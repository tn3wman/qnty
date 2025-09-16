#!/usr/bin/env python3
"""
Standalone script to generate dimension_catalog.pyi stub file.

This script reads the dimension_catalog.py file and generates a corresponding
.pyi stub file with all dimensions and aliases in alphabetical order.
"""

import sys
from pathlib import Path


def generate_dimension_stubs(
    catalog_path: str = "src/qnty/core/dimension_catalog.py",
    output_path: str = "src/qnty/core/dimension_catalog.pyi"
) -> None:
    """Generate .pyi stub file by parsing the file directly and following write_dimensions_stub format"""

    # Convert to Path objects for better handling
    catalog_file = Path(catalog_path)
    output_file = Path(output_path)

    if not catalog_file.exists():
        raise FileNotFoundError(f"Catalog file not found: {catalog_file}")

    # Parse the catalog file to extract dimension names and aliases
    dimensions = set()
    aliases = {}

    with open(catalog_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all variable assignments (dimensions)
    import re

    # Pattern to match dimension assignments like "FORCE = add_derived(" or "Θ = add_dimension("
    # Include Unicode characters like Θ
    dimension_pattern = r'^([A-ZΘ]\w*)\s*=\s*add_(?:dimension|derived)\s*\('
    matches = re.findall(dimension_pattern, content, re.MULTILINE)
    dimensions.update(matches)

    # Pattern to match aliases in add_derived calls
    alias_pattern = r'aliases=\(\s*([^)]+)\s*\)'

    # Also find the dimension name for each aliases= block
    lines = content.split('\n')
    current_dimension = None

    for line in lines:
        line = line.strip()
        # Check if this line starts a dimension definition
        dim_match = re.match(dimension_pattern, line)
        if dim_match:
            current_dimension = dim_match.group(1)
        # Check if this line contains aliases
        elif 'aliases=' in line and current_dimension:
            # Extract aliases from this line
            alias_match = re.search(alias_pattern, line)
            if alias_match:
                alias_str = alias_match.group(1)
                # Parse the aliases (they're in quotes)
                alias_names = re.findall(r'"([^"]+)"', alias_str)
                for alias in alias_names:
                    aliases[alias] = current_dimension

    # Generate stub content following write_dimensions_stub pattern exactly
    stub_content = []
    stub_content.append("from typing import Final")
    stub_content.append("")
    stub_content.append("from .dimension import Dimension")
    stub_content.append("")
    stub_content.append("class Dimensions:")

    # Add canonical dimensions in alphabetical order
    for name in sorted(dimensions):
        stub_content.append(f"    {name}: Final[Dimension]")

    # Add aliases in alphabetical order
    for alias, canonical in sorted(aliases.items()):
        stub_content.append(f"    {alias}: Final[Dimension]  # alias for {canonical}")

    stub_content.append("")
    stub_content.append("dim: Final[Dimensions]")

    # Write the stub file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(stub_content))
        f.write('\n')  # Final newline

    print(f"Generated stub file: {output_file}")
    print(f"  Canonical dimensions: {len(dimensions)}")
    print(f"  Aliases: {len(aliases)}")


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate dimension_catalog.pyi stub file"
    )
    parser.add_argument(
        "--catalog",
        default="src/qnty/core/dimension_catalog.py",
        help="Path to dimension_catalog.py file (default: %(default)s)"
    )
    parser.add_argument(
        "--output",
        default="src/qnty/core/dimension_catalog.pyi",
        help="Output path for .pyi file (default: %(default)s)"
    )

    args = parser.parse_args()

    try:
        generate_dimension_stubs(args.catalog, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()