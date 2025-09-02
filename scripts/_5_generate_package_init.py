#!/usr/bin/env python3
"""
Script to generate __init__.py file with explicit variable imports.

This script generates the main package __init__.py file with explicit imports
for all variable types, eliminating linter warnings from star imports while
maintaining the same public API.

Uses the same source of truth as the consolidated variables system.
"""

import json
from pathlib import Path


def load_parsed_units():
    """Load parsed units data - same source used for consolidated variables."""
    units_path = Path(__file__).parent / "input" / "unit_data.json"
    with open(units_path) as f:
        return json.load(f)


def convert_to_class_name(field_name: str) -> str:
    """Convert field name to PascalCase class name."""
    words = field_name.split('_')
    return ''.join(word.capitalize() for word in words)


def generate_init_file(parsed_data: dict) -> str:
    """Generate the __init__.py file content with explicit imports."""
    
    # Get all variable class names
    variable_names = []
    for field_name, field_data in parsed_data.items():
        if field_data.get('units'):
            class_name = convert_to_class_name(field_name)
            variable_names.append(class_name)
    
    # Sort for consistent output
    variable_names.sort()
    
    # Common variables that should be highlighted in __all__
    common_variables = [
        'Dimensionless', 'Length', 'Pressure', 'Temperature', 'Time', 'Mass',
        'Volume', 'Area', 'Force', 'EnergyHeatWork', 'PowerThermalDuty'
    ]
    
    lines = [
        '"""',
        'Qnty - High-Performance Unit System for Engineering',
        '====================================================',
        '',
        'A fast, type-safe unit system library for Python with dimensional safety',
        'and optimized unit conversions for engineering calculations.',
        '"""',
        '',
        'from .dimension import BaseDimension, DimensionSignature',
        'from .equation import Equation',
        'from .expression import Expression',
        'from .unit import registry',
        'from .units import register_all_units',
        'from .variable import FastQuantity, TypeSafeSetter, TypeSafeVariable',
    ]
    
    # Generate explicit variable imports
    lines.append('from .variables import (')
    for i, var_name in enumerate(variable_names):
        if i == len(variable_names) - 1:
            lines.append(f'    {var_name}')  # No comma on last item
        else:
            lines.append(f'    {var_name},')
    lines.append(')')
    lines.append('')
    
    # Register all units
    lines.extend([
        '# Register all units to the global registry',
        'register_all_units(registry)',
        '',
        '# Finalize registry after all registrations',
        'registry.finalize_registration()',
        '',
    ])
    
    # Generate __all__ with common variables first, then all others
    lines.append('# Define public API')
    lines.append('__all__ = [')
    
    # Common variables section
    lines.append('    # Core variable types (most commonly used)')
    common_line = '    '
    for _i, var_name in enumerate(common_variables):
        if var_name in variable_names:  # Only include if it exists
            if len(common_line) + len(f'"{var_name}", ') > 80:
                lines.append(common_line.rstrip())
                common_line = '    '
            common_line += f'"{var_name}", '
    if common_line.strip():
        lines.append(common_line.rstrip())
    
    lines.append('')
    lines.append('    # Core classes for advanced usage')
    lines.append('    "FastQuantity", "TypeSafeVariable", "TypeSafeSetter",')
    lines.append('    "DimensionSignature", "BaseDimension",')
    lines.append('    "Expression", "Equation",')
    lines.append('')
    
    # All other variables section (excluding common ones already listed)
    other_variables = [v for v in variable_names if v not in common_variables]
    if other_variables:
        lines.append(f'    # All other variable types ({len(other_variables)} additional types)')
        other_line = '    '
        for _i, var_name in enumerate(other_variables):
            if len(other_line) + len(f'"{var_name}", ') > 80:
                lines.append(other_line.rstrip())
                other_line = '    '
            other_line += f'"{var_name}", '
        if other_line.strip():
            lines.append(other_line.rstrip())
    
    lines.append(']')
    lines.append('')
    
    return '\n'.join(lines) + '\n'


def main():
    """Main execution function."""
    print("Loading parsed units data for __init__.py generation...")
    
    # Load the same data source used for consolidated variables
    parsed_data = load_parsed_units()
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in parsed_data.values() if field_data.get('units'))
    
    print(f"Found {fields_with_units} variable types to export")
    
    # Generate __init__.py file
    print("Generating __init__.py...")
    content = generate_init_file(parsed_data)
    
    # Write output file
    output_path = Path(__file__).parent.parent / "src" / "qnty" / "__init__.py"
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Generated __init__.py file: {output_path}")
    
    # Print statistics
    lines_count = len(content.splitlines())
    print("\nStatistics:")
    print(f"  Total variable types: {fields_with_units}")
    print(f"  Generated lines: {lines_count}")
    
    print("\n✅ Clean __init__.py generated with explicit imports!")


if __name__ == "__main__":
    main()
