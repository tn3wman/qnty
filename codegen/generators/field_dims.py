#!/usr/bin/env python3
"""
Dimension generator for qnty library.

This script generates the dimensions.py file from unit_data.json, creating
all necessary dimension signatures programmatically without hardcoding.
"""

import json
from pathlib import Path
from typing import Any

from qnty.dimensions import BASE_DIMENSIONS, DIMENSION_SYMBOLS, PRIME_MAP, DimensionConfig


class DimensionGenerator:
    """Generator for dimensions.py file."""

    def __init__(self, data_path: Path, output_path: Path, out_dir: Path):
        """Initialize with paths."""
        self.data_path = data_path
        self.output_path = output_path
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

        # Load unit data
        with open(self.data_path, encoding="utf-8") as f:
            self.unit_data: dict[str, Any] = json.load(f)

        # Track all discovered dimensions
        self.all_dimensions: dict[str, dict[str, int]] = {}

    def calculate_signature(self, dims: dict[str, int]) -> float:
        """Calculate prime factorization signature for dimensions."""
        if not dims:
            return 1.0

        signature = 1.0

        for dim_name, power in dims.items():
            if power != 0 and dim_name in PRIME_MAP:
                signature *= PRIME_MAP[dim_name] ** power

        return signature


    def format_dimension_comment(self, dims: dict[str, int]) -> str:
        """Create readable comment for a dimension."""
        if not dims:
            return "Dimensionless"

        parts = []
        for dim, power in sorted(dims.items()):
            if power != 0:
                symbol = DIMENSION_SYMBOLS.get(dim, dim[0].upper())
                if power == 1:
                    parts.append(symbol)
                else:
                    parts.append(f"{symbol}^{power}")

        return " ".join(parts) if parts else "Dimensionless"

    def extract_all_dimensions(self) -> None:
        """Extract all unique dimensions from unit data."""
        # Add base dimensions
        for name, config in BASE_DIMENSIONS.items():
            self.all_dimensions[name] = dict(config.params)

        # Extract from unit data
        for field_name, field_data in self.unit_data.items():
            dims = field_data.get("dimensions", {})
            name = field_name.upper()

            # Skip if it's a base dimension
            if name not in BASE_DIMENSIONS:
                self.all_dimensions[name] = dims

        # No longer need signatures cache since imported from core


    def generate_header(self) -> list[str]:
        """Generate the file header."""
        lines = [
            '"""',
            "Dimension System",
            "================",
            "",
            "Compile-time dimensional analysis using type system for ultra-fast operations.",
            "",
            "This file contains dimension constants for all engineering fields.",
            '"""',
            "",
            "from .signature import DimensionSignature",
            "",
        ]
        return lines

    def generate_base_dimension_class(self) -> list[str]:
        """Skip generating BaseDimension - imported from core."""
        return []

    def generate_dimension_signature_class(self) -> list[str]:
        """Skip generating DimensionSignature - imported from core."""
        return []

    def generate_dimension_constants(self) -> list[str]:
        """Generate dimension constant definitions."""
        lines = []

        # Generate signature lookup dictionary
        lines.append("# Dimension signature constants - computed from prime factorization")
        lines.append("_SIGNATURES: dict[str, int | float] = {")

        for field_name in sorted(self.unit_data.keys()):
            field_data = self.unit_data[field_name]
            dims = field_data.get("dimensions", {})
            const_name = field_name.upper()
            
            signature = self.calculate_signature(dims)
            comment = self.format_dimension_comment(dims)

            if signature == int(signature):
                sig_str = str(int(signature))
            else:
                sig_str = f"{signature:.10g}"

            lines.append(f'    "{const_name}": {sig_str},  # {comment}')

        lines.append("}")
        lines.append("")

        # Generate all dimension constants programmatically to avoid duplication
        lines.append("# Generate all dimension constants programmatically to avoid duplication")
        lines.append("for _name, _signature in _SIGNATURES.items():")
        lines.append("    globals()[_name] = DimensionSignature(_signature)")
        lines.append("")

        return lines

    def generate_pyi_content(self) -> str:
        """Generate the .pyi stub file content."""
        lines = [
            '"""',
            "Type stubs for field_dims module.",
            "",
            "This file provides type information for the dynamically generated dimension constants.",
            '"""',
            "",
            "from .signature import DimensionSignature",
            "",
            "# Dimension signature constants lookup",
            "_SIGNATURES: dict[str, int | float]",
            "",
            "# Lazy loading cache",
            "_dimension_cache: dict[str, DimensionSignature]",
            "",
            "# Module attribute access function",
            "def __getattr__(name: str) -> DimensionSignature: ...",
            "",
            "# All dynamically generated dimension constants",
        ]
        
        # Add all dimension constants
        for field_name in sorted(self.unit_data.keys()):
            const_name = field_name.upper()
            lines.append(f"{const_name}: DimensionSignature")
        
        lines.extend([
            "",
            "# Module exports",
            "__all__: list[str]",
            ""
        ])
        
        return "\n".join(lines)

    def generate(self) -> None:
        """Generate the complete field_dims.py and field_dims.pyi files."""
        # Extract all dimensions from data
        self.extract_all_dimensions()

        # Build the .py file content
        lines = []
        lines.extend(self.generate_header())
        lines.extend(self.generate_dimension_constants())

        # Write the .py file with newline at end
        content = "\n".join(lines) + "\n"
        self.output_path.write_text(content, encoding="utf-8")
        print(f"Generated {self.output_path}")
        
        # Generate and write the .pyi file
        pyi_path = self.output_path.with_suffix('.pyi')
        pyi_content = self.generate_pyi_content()
        pyi_path.write_text(pyi_content, encoding="utf-8")
        print(f"Generated {pyi_path}")

        # Save metadata to out directory
        metadata = {
            "total_dimensions": len(self.all_dimensions),
            "generated_dimensions": sorted(self.unit_data.keys()),
            "base_dimensions": list(BASE_DIMENSIONS.keys()),
            "signatures_cached": 0,  # No longer generated
        }

        metadata_path = self.out_dir / "dimension_metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        print(f"Saved metadata to {metadata_path}")


def main() -> None:
    """Main entry point."""
    # Set up paths
    generator_dir = Path(__file__).parent
    data_path = generator_dir / "data" / "unit_data.json"
    # Changed to output to the correct location
    output_path = generator_dir.parent.parent / "src" / "qnty" / "dimensions" / "field_dims.py"
    out_dir = generator_dir / "out"

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run generator
    generator = DimensionGenerator(data_path, output_path, out_dir)
    generator.generate()

    print("\nDimension generation complete!")
    print(f"  - Total dimensions: {len(generator.all_dimensions)}")

if __name__ == "__main__":
    main()
