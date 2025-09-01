#!/usr/bin/env python3
"""
Script to validate and update dimension.py with all discovered dimensions.

Step 3 of the unit consolidation process: Ensure all dimensions from the parsed
units are defined in dimension.py and add any missing ones.
"""

import json
import re
from pathlib import Path

# Configuration constants
BASE_DIMENSIONS = [
    ('DIMENSIONLESS', {}),
    ('AMOUNT', {'amount': 1}),
    ('CURRENT', {'current': 1}),
    ('LENGTH', {'length': 1}),
    ('LUMINOSITY', {'luminosity': 1}),
    ('MASS', {'mass': 1}),
    ('TEMPERATURE', {'temp': 1}),
    ('TIME', {'time': 1}),
]


DIMENSION_SYMBOLS = {
    'length': 'L',
    'mass': 'M',
    'time': 'T',
    'current': 'A',
    'temp': 'Θ',
    'amount': 'N',
    'luminosity': 'J',
}


def load_json_data(file_path: Path) -> dict:
    """Load JSON data from file."""
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def save_json_data(data: dict, file_path: Path) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def save_text_file(content: str, file_path: Path) -> None:
    """Save text content to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def format_dimension_signature(dims: dict[str, int]) -> str:
    """Format dimension dictionary as DimensionSignature.create() call."""
    if not dims:
        return "DimensionSignature.create()"
    
    params = []
    for dim_name, power in sorted(dims.items()):
        if power != 0:
            # Map luminous_intensity to luminosity to match BaseDimension enum
            if dim_name == 'luminous_intensity':
                dim_name = 'luminosity'
            params.append(f"{dim_name}={power}")
    
    return f"DimensionSignature.create({', '.join(params)})"


def create_dimension_comment(dims: dict[str, int]) -> str:
    """Create a descriptive comment for a dimension specification."""
    if not dims:
        return "  # Dimensionless"
    
    dim_parts = []
    for base_dim, power in sorted(dims.items()):
        if power != 0:
            if base_dim == 'luminous_intensity':
                base_dim = 'luminosity'
            symbol = DIMENSION_SYMBOLS.get(base_dim, base_dim[0].upper())
            
            if power == 1:
                dim_parts.append(symbol)
            else:
                dim_parts.append(f"{symbol}^{power}")
    
    return f"  # {' '.join(dim_parts)}" if dim_parts else "  # Dimensionless"


def extract_dimensions_from_parsed_data(parsed_data: dict) -> dict[str, dict[str, int]]:
    """Extract all unique dimensions from parsed data."""
    return {field_name.upper(): field_data['dimensions']
            for field_name, field_data in parsed_data.items()}


def read_existing_dimensions(file_path: Path) -> set[str]:
    """Read existing dimension definitions from dimension.py file."""
    if not file_path.exists():
        return set()
    
    content = file_path.read_text(encoding='utf-8')
    dimension_pattern = r'^([A-Z_]+)\s*=\s*DimensionSignature\.create\('
    return {match.group(1) for match in re.finditer(dimension_pattern, content, re.MULTILINE)}



def generate_file_header() -> list[str]:
    """Generate the standard header for dimension.py."""
    return [
        '"""',
        'Dimension System',
        '================',
        '',
        'Compile-time dimensional analysis using type system for ultra-fast operations.',
        '"""',
        '',
        'from dataclasses import dataclass',
        'from enum import IntEnum',
        'from typing import final',
        '',
        '',
        'class BaseDimension(IntEnum):',
        '    """Base dimensions as prime numbers for efficient bit operations."""',
        '    LENGTH = 2',
        '    MASS = 3',
        '    TIME = 5',
        '    CURRENT = 7',
        '    TEMPERATURE = 11',
        '    AMOUNT = 13',
        '    LUMINOSITY = 17',
        '',
        '',
        '@final',
        '@dataclass(frozen=True)',
        'class DimensionSignature:',
        '    """Immutable dimension signature for zero-cost dimensional analysis."""',
        '    ',
        '    # Store as bit pattern for ultra-fast comparison',
        '    _signature: int = 1',
        '    ',
        '    @classmethod',
        '    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):',
        '        """Create dimension from exponents."""',
        '        signature = 1',
        '        if length != 0:',
        '            signature *= BaseDimension.LENGTH ** length',
        '        if mass != 0:',
        '            signature *= BaseDimension.MASS ** mass',
        '        if time != 0:',
        '            signature *= BaseDimension.TIME ** time',
        '        if current != 0:',
        '            signature *= BaseDimension.CURRENT ** current',
        '        if temp != 0:',
        '            signature *= BaseDimension.TEMPERATURE ** temp',
        '        if amount != 0:',
        '            signature *= BaseDimension.AMOUNT ** amount',
        '        if luminosity != 0:',
        '            signature *= BaseDimension.LUMINOSITY ** luminosity',
        '        ',
        '        return cls(signature)',
        '    ',
        '    def __mul__(self, other):',
        '        return DimensionSignature(self._signature * other._signature)',
        '    ',
        '    def __truediv__(self, other):',
        '        return DimensionSignature(self._signature // other._signature)',
        '    ',
        '    def __pow__(self, power):',
        '        return DimensionSignature(self._signature ** power)',
        '    ',
        '    def is_compatible(self, other):',
        '        """Ultra-fast dimensional compatibility check."""',
        '        return self._signature == other._signature',
        '    ',
        '    def __eq__(self, other):',
        '        """Fast equality check for dimensions."""',
        '        return isinstance(other, DimensionSignature) and self._signature == other._signature',
        '    ',
        '    def __hash__(self):',
        '        """Enable dimensions as dictionary keys."""',
        '        return hash(self._signature)',
        '',
        '',
        '# Pre-defined dimension constants (alphabetically ordered)',
    ]


def generate_dimension_constants(all_dimensions: dict[str, dict[str, int]]) -> list[str]:
    """Generate dimension constant definitions."""
    lines = []
    
    # Get base dimension names for filtering
    base_dimension_names = {bd[0] for bd in BASE_DIMENSIONS}
    
    # Add discovered dimensions (excluding base dimensions)
    discovered_dims = [
        (dim_name.upper(), dim_spec)
        for dim_name, dim_spec in all_dimensions.items()
        if dim_name.upper() not in base_dimension_names
    ]
    
    # Combine and sort all dimensions alphabetically
    all_dims = BASE_DIMENSIONS + discovered_dims
    all_dims.sort(key=lambda x: x[0])
    
    # Generate dimension constants
    for dim_name, dim_spec in all_dims:
        signature = format_dimension_signature(dim_spec)
        comment = create_dimension_comment(dim_spec)
        lines.append(f"{dim_name} = {signature}{comment}")
    
    return lines


def generate_complete_dimension_file(all_dimensions: dict[str, dict[str, int]]) -> str:
    """Generate a complete new dimension.py file."""
    lines = generate_file_header()
    lines.extend(generate_dimension_constants(all_dimensions))
    return '\n'.join(lines)


def create_dimension_mapping(parsed_data: dict) -> dict[str, dict]:
    """Create comprehensive dimension mapping from parsed data."""
    return {
        field_name: {
            'field': field_data['field'],
            'dimensions': field_data['dimensions'],
            'signature': format_dimension_signature(field_data['dimensions']),
            'constant_name': field_name.upper()
        }
        for field_name, field_data in parsed_data.items()
    }


def print_dimension_summary(all_dimensions: dict[str, dict[str, int]]) -> None:
    """Print a summary of dimensions grouped by signature."""
    print("\n" + "="*60)
    print("DIMENSION SUMMARY")
    print("="*60)
    
    # Group by dimension signature
    by_signature = {}
    for field_name, dims in all_dimensions.items():
        dim_key = tuple(sorted((k, v) for k, v in dims.items()))
        if dim_key not in by_signature:
            by_signature[dim_key] = []
        by_signature[dim_key].append(field_name)
    
    print(f"\nGrouped by dimension signature ({len(by_signature)} unique):")
    for dim_spec, fields in sorted(by_signature.items(), key=lambda x: len(x[1]), reverse=True):
        dim_dict = dict(dim_spec) if dim_spec else {}
        print(f"\n  {format_dimension_signature(dim_dict)}")
        print(f"    Fields ({len(fields)}): {', '.join(sorted(fields)[:5])}")
        if len(fields) > 5:
            print(f"                 ... and {len(fields)-5} more")


def main():
    """Main function to validate and update dimensions."""
    # Setup paths using pathlib
    base_path = Path(__file__).parent.parent
    src_path = base_path / "src" / "qnty"
    scripts_input_path = Path(__file__).parent / "input"
    scripts_output_path = Path(__file__).parent / "output"
    
    parsed_file = scripts_input_path / "parsed_units.json"
    dimension_file = src_path / "dimension.py"
    mapping_file = scripts_output_path / "dimension_mapping.json"
    
    # Ensure output directory exists
    scripts_output_path.mkdir(parents=True, exist_ok=True)
    
    # Load and process data
    parsed_data = load_json_data(parsed_file)
    print(f"Loaded {len(parsed_data)} fields with units")
    
    # Extract and process dimensions
    all_dimensions = extract_dimensions_from_parsed_data(parsed_data)
    existing_dims = read_existing_dimensions(dimension_file)
    
    print(f"\nFound {len(all_dimensions)} unique dimensions")
    print(f"Found {len(existing_dims)} existing dimension definitions")
    
    # Find and report new dimensions
    new_dimension_names = set(all_dimensions.keys()) - existing_dims
    if new_dimension_names:
        print(f"\nNew dimensions to add: {len(new_dimension_names)}")
        for name in sorted(new_dimension_names):
            dim_spec = all_dimensions[name]
            signature = format_dimension_signature(dim_spec)
            print(f"  {name} = {signature}")
    else:
        print("\nAll dimensions already defined!")
    
    # Generate and save files
    print("\nGenerating complete dimension.py file...")
    complete_content = generate_complete_dimension_file(all_dimensions)
    save_text_file(complete_content, dimension_file)
    print(f"Complete dimension.py file saved to: {dimension_file}")
    
    # Save dimension mapping
    dimension_mapping = create_dimension_mapping(parsed_data)
    save_json_data(dimension_mapping, mapping_file)
    print(f"Dimension mapping saved to: {mapping_file}")
    
    # Print summary
    print_dimension_summary(all_dimensions)


if __name__ == "__main__":
    main()
