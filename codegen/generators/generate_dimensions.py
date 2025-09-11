#!/usr/bin/env python3
"""
Dimension generator for qnty library.

This script generates the dimensions.py and dimensions.pyi files from unit_data.json,
creating all necessary dimension constants programmatically.
"""

import json
from pathlib import Path
from typing import Any


class DimensionGenerator:
    """Generator for dimensions.py and dimensions.pyi files."""
    
    # Map dimension names to their position in the 7-tuple
    # (L, M, T, I, Θ, N, J) = (Length, Mass, Time, Current, Temperature, Amount, Luminosity)
    DIMENSION_MAP = {
        "length": 0,
        "mass": 1,
        "time": 2,
        "current": 3,
        "temperature": 4,
        "amount": 5,
        "luminosity": 6
    }

    def __init__(self, data_path: Path, output_dir: Path):
        """Initialize with paths."""
        self.data_path = data_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load unit data
        with open(self.data_path, encoding="utf-8") as f:
            self.unit_data: dict[str, Any] = json.load(f)

        # Track all discovered dimensions
        self.all_dimensions: dict[str, tuple[int, ...]] = {}

    def dims_to_tuple(self, dims: dict[str, int]) -> tuple[int, ...]:
        """Convert dimension dict to 7-tuple."""
        result = [0] * 7
        for dim_name, power in dims.items():
            if dim_name in self.DIMENSION_MAP:
                result[self.DIMENSION_MAP[dim_name]] = power
        return tuple(result)

    def format_dimension_comment(self, dims: dict[str, int]) -> str:
        """Create readable comment for a dimension."""
        if not dims or all(v == 0 for v in dims.values()):
            return "Dimensionless"

        symbols = {
            "length": "L",
            "mass": "M",
            "time": "T",
            "current": "I",
            "temperature": "Θ",
            "amount": "N",
            "luminosity": "J"
        }
        
        parts = []
        for dim, power in sorted(dims.items()):
            if power != 0 and dim in symbols:
                symbol = symbols[dim]
                if power == 1:
                    parts.append(symbol)
                else:
                    parts.append(f"{symbol}^{power}")

        return " ".join(parts) if parts else "Dimensionless"

    def extract_all_dimensions(self) -> None:
        """Extract all unique dimensions from unit data."""
        # Add dimensionless
        self.all_dimensions["DIMENSIONLESS"] = (0, 0, 0, 0, 0, 0, 0)
        
        # Extract from unit data
        for field_name, field_data in self.unit_data.items():
            dims = field_data.get("dimensions", {})
            name = field_name.upper()
            dim_tuple = self.dims_to_tuple(dims)
            self.all_dimensions[name] = dim_tuple

    def generate_py_content(self) -> str:
        """Generate the dimensions.py file content."""
        lines = [
            '"""',
            "Dimension System",
            "================",
            "",
            "This file contains dimension constants for all engineering fields.",
            "",
            "THIS FILE IS AUTO-GENERATED - DO NOT EDIT MANUALLY",
            "changes will be overwritten",
            "see codegen/generate_dimensions.py",
            '"""',
            "",
            "from .base import Dimension",
            "",
        ]
        
        # Generate dimension constants sorted by name
        for const_name in sorted(self.all_dimensions.keys()):
            dim_tuple = self.all_dimensions[const_name]
            
            # Find the original dims dict for comment
            field_name = const_name.lower()
            if field_name in self.unit_data:
                dims = self.unit_data[field_name].get("dimensions", {})
            else:
                dims = {}
            
            comment = self.format_dimension_comment(dims)
            if comment and comment != "Dimensionless":
                comment = f"  # {comment}"
            else:
                comment = ""
            
            lines.append(f"{const_name} = Dimension({dim_tuple}){comment}")
        
        return "\n".join(lines) + "\n"

    def generate_pyi_content(self) -> str:
        """Generate the dimensions.pyi stub file content."""
        lines = [
            '"""',
            "Dimension System Stub",
            "=====================",
            "",
            "This file contains dimension constants for all engineering fields.",
            "",
            "THIS FILE IS AUTO-GENERATED - DO NOT EDIT MANUALLY",
            "changes will be overwritten",
            "see codegen/generate_dimensions.py",
            '"""',
            "",
            "from .base import Dimension",
            "",
            "# All dynamically generated dimension constants",
        ]
        
        # Add all dimension constants sorted by name
        for const_name in sorted(self.all_dimensions.keys()):
            lines.append(f"{const_name}: Dimension")
        
        return "\n".join(lines) + "\n"

    def generate(self) -> None:
        """Generate the complete dimensions.py and dimensions.pyi files."""
        # Extract all dimensions from data
        self.extract_all_dimensions()

        # Generate and write the .py file
        py_path = self.output_dir / "dimensions.py"
        py_content = self.generate_py_content()
        py_path.write_text(py_content, encoding="utf-8")
        print(f"Generated {py_path}")
        
        # Generate and write the .pyi file
        pyi_path = self.output_dir / "dimensions.pyi"
        pyi_content = self.generate_pyi_content()
        pyi_path.write_text(pyi_content, encoding="utf-8")
        print(f"Generated {pyi_path}")

        print("\nDimension generation complete!")
        print(f"  - Total dimensions: {len(self.all_dimensions)}")


def main() -> None:
    """Main entry point."""
    # Set up paths
    generator_dir = Path(__file__).parent
    data_path = generator_dir / "data" / "unit_data.json"
    output_dir = generator_dir.parent.parent / "src" / "qnty" / "dimensions"

    # Run generator
    generator = DimensionGenerator(data_path, output_dir)
    generator.generate()



if __name__ == "__main__":
    main()
