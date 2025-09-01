#!/usr/bin/env python3
"""
Script to validate and update dimension.py with all discovered dimensions.

Step 3 of the unit consolidation process: Ensure all dimensions from the parsed
units are defined in dimension.py and add any missing ones.
"""

import json
import re
from pathlib import Path
from typing import Dict, Set, Tuple


def load_parsed_units(file_path: str) -> Dict:
    """Load the parsed units data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_all_dimensions(parsed_data: Dict) -> Dict[str, Dict[str, int]]:
    """Extract all unique dimensions from parsed data, including dimensionless."""
    dimensions = {}
    
    for field_name, field_data in parsed_data.items():
        # Include ALL fields, even those with empty dimensions (dimensionless)
        # Use the field name as the dimension name
        dimensions[field_name.upper()] = field_data['dimensions']
    
    return dimensions


def format_dimension_signature(dims: Dict[str, int]) -> str:
    """Format dimension dictionary as DimensionSignature.create() call."""
    if not dims:
        return "DimensionSignature.create()"  # Dimensionless
    
    # Build the parameter list - fix luminous_intensity to luminosity
    params = []
    for dim_name, power in sorted(dims.items()):
        if power != 0:
            # Map luminous_intensity to luminosity to match BaseDimension enum
            if dim_name == 'luminous_intensity':
                dim_name = 'luminosity'
            params.append(f"{dim_name}={power}")
    
    return f"DimensionSignature.create({', '.join(params)})"


def read_dimension_file(file_path: str) -> Tuple[str, Set[str]]:
    """Read the current dimension.py file and extract existing dimensions."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all existing dimension definitions
    dimension_pattern = r'^([A-Z_]+)\s*=\s*DimensionSignature\.create\('
    existing_dims = set()
    
    for match in re.finditer(dimension_pattern, content, re.MULTILINE):
        existing_dims.add(match.group(1))
    
    return content, existing_dims


def generate_dimension_definitions(dimensions: Dict[str, Dict[str, int]], existing_dims: Set[str]) -> str:
    """Generate dimension definition code."""
    lines = []
    
    # Sort dimensions alphabetically
    sorted_dims = sorted(dimensions.items())
    
    # Find new dimensions
    new_dims = []
    updated_dims = []
    
    for dim_name, dim_spec in sorted_dims:
        if dim_name not in existing_dims:
            new_dims.append((dim_name, dim_spec))
        else:
            updated_dims.append((dim_name, dim_spec))
    
    # Generate new dimension definitions
    if new_dims:
        lines.append("# New dimensions discovered from unit definitions")
        for dim_name, dim_spec in new_dims:
            signature = format_dimension_signature(dim_spec)
            lines.append(f"{dim_name} = {signature}")
        lines.append("")
    
    return '\n'.join(lines)


def generate_complete_dimension_file(all_dimensions: Dict[str, Dict[str, int]]) -> str:
    """Generate a complete new dimension.py file with all dimensions alphabetically ordered."""
    
    lines = []
    
    # File header
    lines.extend([
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
    ])
    
    # Add base dimensions first
    base_dimensions = [
        ('DIMENSIONLESS', {}),
        ('AMOUNT', {'amount': 1}),
        ('CURRENT', {'current': 1}),
        ('LENGTH', {'length': 1}),
        ('LUMINOSITY', {'luminosity': 1}),
        ('MASS', {'mass': 1}),
        ('TEMPERATURE', {'temp': 1}),
        ('TIME', {'time': 1}),
    ]
    
    # Add all discovered dimensions
    discovered_dims = []
    for dim_name, dim_spec in all_dimensions.items():
        # Skip if it's already a base dimension
        if dim_name.upper() not in [bd[0] for bd in base_dimensions]:
            discovered_dims.append((dim_name.upper(), dim_spec))
    
    # Combine and sort all dimensions alphabetically
    all_dims = base_dimensions + discovered_dims
    all_dims.sort(key=lambda x: x[0])
    
    # Generate dimension constants
    for dim_name, dim_spec in all_dims:
        signature = format_dimension_signature(dim_spec)
        
        # Add descriptive comment for complex dimensions
        if dim_spec:
            # Create dimension signature string for comment
            dim_parts = []
            for base_dim, power in sorted(dim_spec.items()):
                if power != 0:
                    if base_dim == 'luminous_intensity':
                        base_dim = 'luminosity'
                    dim_symbol = base_dim[0].upper()  # L, M, T, A, Θ, N, J
                    if base_dim == 'temp':
                        dim_symbol = 'Θ'
                    elif base_dim == 'amount':
                        dim_symbol = 'N'
                    elif base_dim == 'luminosity':
                        dim_symbol = 'J'
                    elif base_dim == 'current':
                        dim_symbol = 'A'
                        
                    if power == 1:
                        dim_parts.append(dim_symbol)
                    else:
                        dim_parts.append(f"{dim_symbol}^{power}")
            
            comment = f"  # {' '.join(dim_parts)}" if dim_parts else "  # Dimensionless"
        else:
            comment = "  # Dimensionless"
            
        lines.append(f"{dim_name} = {signature}{comment}")
    
    return '\n'.join(lines)


def validate_dimensions(parsed_data: Dict) -> Dict[str, str]:
    """Validate that all parsed dimensions make sense."""
    issues = {}
    
    # Expected dimensions for common fields
    expected = {
        'pressure': {'mass': 1, 'length': -1, 'time': -2},
        'force': {'mass': 1, 'length': 1, 'time': -2},
        'energy_heat_work': {'mass': 1, 'length': 2, 'time': -2},
        'power_thermal_duty': {'mass': 1, 'length': 2, 'time': -3},
        'length': {'length': 1},
        'area': {'length': 2},
        'volume': {'length': 3},
        'mass': {'mass': 1},
        'time': {'time': 1},
        'velocity_linear': {'length': 1, 'time': -1},
        'acceleration': {'length': 1, 'time': -2},
        'temperature': {'temperature': 1},
    }
    
    for field_name, expected_dims in expected.items():
        if field_name in parsed_data:
            actual_dims = parsed_data[field_name]['dimensions']
            if actual_dims != expected_dims:
                issues[field_name] = f"Expected {expected_dims}, got {actual_dims}"
    
    return issues


def main():
    """Main function to validate and update dimensions."""
    
    # Load parsed units
    parsed_file = "/Users/tyler/Projects/qnty/data/parsed_units.json"
    parsed_data = load_parsed_units(parsed_file)
    
    print(f"Loaded {len(parsed_data)} fields with units")
    
    # Validate dimensions
    print("\nValidating dimensions...")
    issues = validate_dimensions(parsed_data)
    if issues:
        print("Validation issues found:")
        for field, issue in issues.items():
            print(f"  {field}: {issue}")
    else:
        print("All validated dimensions are correct!")
    
    # Extract all dimensions
    all_dimensions = extract_all_dimensions(parsed_data)
    print(f"\nFound {len(all_dimensions)} unique dimensions")
    
    # Read current dimension.py
    dimension_file = "/Users/tyler/Projects/qnty/src/qnty/dimension.py"
    current_content, existing_dims = read_dimension_file(dimension_file)
    print(f"Found {len(existing_dims)} existing dimension definitions")
    
    # Find new dimensions
    new_dimension_names = set(all_dimensions.keys()) - existing_dims
    if new_dimension_names:
        print(f"\nNew dimensions to add: {len(new_dimension_names)}")
        for name in sorted(new_dimension_names):
            dim_spec = all_dimensions[name]
            signature = format_dimension_signature(dim_spec)
            print(f"  {name} = {signature}")
    else:
        print("\nAll dimensions already defined!")
    
    # Generate complete new dimension.py file
    print(f"\nGenerating complete new dimension.py file...")
    complete_dimension_content = generate_complete_dimension_file(all_dimensions)
    
    # Save the complete dimension file
    dimension_file = "/Users/tyler/Projects/qnty/src/qnty/dimension.py"
    with open(dimension_file, 'w', encoding='utf-8') as f:
        f.write(complete_dimension_content)
    print(f"Complete dimension.py file saved to: {dimension_file}")
    
    # Also generate just the new definitions for comparison
    new_definitions = generate_dimension_definitions(all_dimensions, existing_dims)
    
    if new_definitions:
        output_file = "/Users/tyler/Projects/qnty/data/new_dimensions.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# New dimension definitions to add to dimension.py\n\n")
            f.write("from qnty.dimension import DimensionSignature\n\n")
            f.write(new_definitions)
        print(f"\nNew dimension definitions saved to: {output_file}")
        print("Review and add these to dimension.py as needed")
    
    # Create a comprehensive dimension mapping
    dimension_mapping = {}
    for field_name, field_data in parsed_data.items():
        # Include ALL fields, even dimensionless ones
        dimension_mapping[field_name] = {
            'field': field_data['field'],
            'dimensions': field_data['dimensions'],
            'signature': format_dimension_signature(field_data['dimensions']),
            'constant_name': field_name.upper()
        }
    
    # Save dimension mapping
    mapping_file = "/Users/tyler/Projects/qnty/data/dimension_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(dimension_mapping, f, indent=2)
    print(f"\nDimension mapping saved to: {mapping_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("DIMENSION SUMMARY")
    print("="*60)
    
    # Group by dimension type
    by_base_dims = {}
    for field_name, dims in all_dimensions.items():
        # Create a key from the dimensions
        dim_key = tuple(sorted((k, v) for k, v in dims.items()))
        if dim_key not in by_base_dims:
            by_base_dims[dim_key] = []
        by_base_dims[dim_key].append(field_name)
    
    print(f"\nGrouped by dimension signature ({len(by_base_dims)} unique):")
    for dim_spec, fields in sorted(by_base_dims.items(), key=lambda x: len(x[1]), reverse=True):
        dim_dict = dict(dim_spec) if dim_spec else {}
        print(f"\n  {format_dimension_signature(dim_dict)}")
        print(f"    Fields ({len(fields)}): {', '.join(sorted(fields)[:5])}")
        if len(fields) > 5:
            print(f"                 ... and {len(fields)-5} more")


if __name__ == "__main__":
    main()