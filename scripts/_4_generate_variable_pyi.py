#!/usr/bin/env python3
"""
Script to generate comprehensive variables.pyi type stub file.

This script generates complete type hints for all 105 variable types in the
consolidated variables system, providing full IDE autocomplete and type checking
support for the fluent API with dimension-specific unit properties.

Uses the same source of truth as the consolidated variables system.
"""

import json
import sys
from pathlib import Path

# Add src/qnty to the path to import prefix system
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qnty.prefixes import PREFIXABLE_UNITS, StandardPrefixes


def load_json_data(file_path: Path) -> dict:
    """Load JSON data from file."""
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def save_text_file(content: str, file_path: Path) -> None:
    """Save text content to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def convert_to_class_name(field_name: str) -> str:
    """Convert field name to PascalCase class name."""
    words = field_name.split('_')
    return ''.join(word.capitalize() for word in words)


def convert_unit_name_to_property(unit_name: str) -> str:
    """Convert unit name to property name without automatic pluralization."""
    import re
    
    # Replace any characters that are not valid Python identifiers with underscores
    property_name = re.sub(r'[^a-zA-Z0-9_]', '_', unit_name)
    
    # Remove leading/trailing underscores and collapse multiple underscores
    property_name = re.sub(r'^_+|_+$', '', property_name)
    property_name = re.sub(r'_+', '_', property_name)
    
    # Ensure it starts with a letter or underscore (valid Python identifier)
    if property_name and property_name[0].isdigit():
        property_name = f"_{property_name}"
    
    # Handle empty property names
    if not property_name:
        property_name = "unit"
    
    # Handle Python reserved words
    reserved_words = {'class', 'def', 'if', 'else', 'for', 'while', 'import', 'from', 'as', 'in'}
    if property_name in reserved_words:
        property_name = f"{property_name}_unit"
    
    return property_name


def identify_base_units_needing_prefixes(parsed_data: dict) -> dict:
    """Identify base SI units that should have prefixes generated."""
    base_units = {}
    
    # Look through all units to find base SI units that are in PREFIXABLE_UNITS
    for field_name, field_data in parsed_data.items():
        for unit_data in field_data['units']:
            unit_name = unit_data['normalized_name']
            if unit_name in PREFIXABLE_UNITS:
                # This is a base unit that should have prefixes
                # Store all occurrences of the unit, not just the last one
                if unit_name not in base_units:
                    base_units[unit_name] = []
                
                base_units[unit_name].append({
                    'unit_data': unit_data,
                    'field_name': field_name,
                    'prefixes': PREFIXABLE_UNITS[unit_name]
                })
    
    return base_units


def generate_prefixed_unit_data(base_unit_data: dict, prefix: StandardPrefixes, field_name: str, field_data: dict) -> dict:
    """Generate unit data for a prefixed variant of a base unit."""
    prefix_def = prefix.value
    
    # Apply prefix to name and symbol
    prefixed_name = prefix_def.apply_to_name(base_unit_data['normalized_name'])
    # Use the field's si_base_unit instead of unit-level data
    prefixed_symbol = prefix_def.apply_to_symbol(field_data.get('si_base_unit', base_unit_data.get('notation', '')))
    
    # Calculate new SI factor
    base_factor = base_unit_data.get('si_conversion', 1.0)
    new_factor = base_factor * prefix_def.factor
    
    # Create new unit data using new structure
    return {
        'name': prefix_def.apply_to_name(base_unit_data['name']),
        'normalized_name': prefixed_name,
        'notation': prefixed_symbol,
        'si_conversion': new_factor,
        'imperial_conversion': base_unit_data.get('imperial_conversion', 1.0),
        'aliases': [prefixed_symbol] if prefixed_symbol else [],
        'generated_from_prefix': True  # Mark as generated for identification
    }


def augment_parsed_data_with_prefixes(parsed_data: dict) -> dict:
    """Add missing prefixed units to the parsed data."""
    # Make a deep copy to avoid modifying the original
    augmented_data = {}
    for key, value in parsed_data.items():
        augmented_data[key] = {
            'field': value['field'],
            'normalized_field': value['normalized_field'],
            'dimensions': value.get('dimensions', {}),
            'units': list(value['units'])  # Copy the units list
        }
    
    # Find base units that need prefixes
    base_units = identify_base_units_needing_prefixes(parsed_data)
    
    # Track existing unit names to avoid duplicates
    existing_units = set()
    for field_data in augmented_data.values():
        for unit in field_data['units']:
            existing_units.add(unit['normalized_name'])
    
    # Generate and add missing prefixed units
    generated_count = 0
    for unit_name, base_entries in base_units.items():
        # Process each field where this unit appears
        for base_info in base_entries:
            base_unit = base_info['unit_data']
            field_name = base_info['field_name']
            prefixes = base_info['prefixes']
            
            for prefix in prefixes:
                if prefix == StandardPrefixes.NONE:
                    continue  # Skip NONE prefix
                    
                prefix_def = prefix.value
                prefixed_name = prefix_def.apply_to_name(unit_name)
                
                # Only add if it doesn't already exist globally
                if prefixed_name not in existing_units:
                    prefixed_unit = generate_prefixed_unit_data(base_unit, prefix, field_name, augmented_data[field_name])
                    augmented_data[field_name]['units'].append(prefixed_unit)
                    existing_units.add(prefixed_name)
                    generated_count += 1
    
    print(f"Generated {generated_count} missing prefixed units for type stubs")
    return augmented_data


def generate_consolidated_pyi(parsed_data: dict, dimension_mapping: dict) -> str:
    """Generate the variables.pyi type stub content."""
    
    lines = [
        '"""',
        'Type stubs for consolidated variables module - Complete Edition.',
        '',
        'Provides complete type hints for IDE autocomplete and type checking',
        'for the fluent API with dimension-specific unit properties for all',
        f'{len([f for f in parsed_data.values() if f.get("units")])} variable types with {sum(len(f.get("units", [])) for f in parsed_data.values())} total units.',
        '',
        'Auto-generated from the same source of truth as consolidated_new.py.',
        '"""',
        '',
        'from typing import Any',
        'from .dimension import DimensionSignature',
        'from .variable import TypeSafeSetter',
        'from .variable_types.typed_variable import TypedVariable',
        '',
        '# ' + '=' * 76,
        '# SPECIAL DIMENSIONLESS VARIABLE',
        '# ' + '=' * 76,
        '',
        'class DimensionlessSetter(TypeSafeSetter):',
        '    """Dimensionless-specific setter with only dimensionless units."""',
        '    ',
        '    def __init__(self, variable: Dimensionless, value: float) -> None: ...',
        '    ',
        '    @property',
        '    def dimensionless(self) -> Dimensionless: ...',
        '    ',
        '    @property',
        '    def unitless(self) -> Dimensionless: ...',
        '',
        '',
        'class Dimensionless(TypedVariable):',
        '    """Type-safe dimensionless variable with expression capabilities."""',
        '',
        '    _setter_class: type[TypeSafeSetter] | None',
        '    _expected_dimension: DimensionSignature | None',
        '    _default_unit_property: str | None',
        '    ',
        '    def __init__(self, *args, is_known: bool = True) -> None: ...',
        '    ',
        '    def set(self, value: float) -> DimensionlessSetter:',
        '        """',
        '        Create a dimensionless setter for fluent unit assignment.',
        '        ',
        '        Example:',
        '            dimensionless.set(1.0).dimensionless',
        '            dimensionless.set(2.5).unitless',
        '        """',
        '        ...',
        '',
        '',
    ]
    
    # Generate type stubs for each field
    sorted_fields = sorted(parsed_data.items())
    fields_with_units = [(k, v) for k, v in sorted_fields if v.get('units')]
    
    for field_name, field_data in fields_with_units:
        class_name = convert_to_class_name(field_name)
        setter_name = f"{class_name}Setter"
        display_name = field_data.get('field', class_name)
        
        # Generate section header
        lines.extend([
            '# ' + '=' * 76,
            f'# {display_name.upper()}',
            '# ' + '=' * 76,
            ''
        ])
        
        # Generate setter class
        lines.extend([
            f'class {setter_name}(TypeSafeSetter):',
            f'    """{display_name}-specific setter with only {display_name.lower()} unit properties."""',
            '    ',
            f'    def __init__(self, variable: {class_name}, value: float) -> None: ...',
            '    ',
            f'    # All {display_name.lower()} unit properties - provides fluent API with full type hints'
        ])
        
        # Add property stubs for each unit
        added_properties = set()  # Track properties already added to avoid duplicates
        
        for unit_data in field_data['units']:
            unit_name = unit_data['name']
            property_name = convert_unit_name_to_property(unit_name)
            aliases = unit_data.get('aliases', [])
            
            # Add the primary property if not already added
            if property_name not in added_properties:
                lines.extend([
                    '    @property',
                    f'    def {property_name}(self) -> {class_name}: ...'
                ])
                added_properties.add(property_name)
            
            # Add alias properties
            for alias in aliases:
                alias_property = convert_unit_name_to_property(alias)
                # Only add if it's different from the main property and not already added
                if alias_property != property_name and alias_property not in added_properties:
                    lines.extend([
                        '    @property',
                        f'    def {alias_property}(self) -> {class_name}: ...'
                    ])
                    added_properties.add(alias_property)
        
        lines.append('')
        
        # Generate variable class
        lines.extend([
            f'class {class_name}(TypedVariable):',
            f'    """Type-safe {display_name.lower()} variable with expression capabilities."""',
            '    ',
            '    _setter_class: type[TypeSafeSetter] | None',
            '    _expected_dimension: DimensionSignature | None',
            '    _default_unit_property: str | None',
            '    ',
            '    def __init__(self, *args, is_known: bool = True) -> None: ...',
            '    ',
            f'    def set(self, value: float) -> {setter_name}:',
            '        """',
            f'        Create a {display_name.lower()} setter for fluent unit assignment.',
            '        ',
            '        Example:'
        ])
        
        # Add example usage with first few units
        sample_units = field_data['units'][:3]
        for unit_data in sample_units:
            property_name = convert_unit_name_to_property(unit_data['name'])
            lines.append(f'            {class_name.lower()}.set(100).{property_name}')
        
        lines.extend([
            '        """',
            '        ...',
            ''
        ])
    
    # Generate module-level definitions
    lines.extend([
        '# ' + '=' * 76,
        '# Module-level definitions',
        '# ' + '=' * 76,
        '',
        'VARIABLE_DEFINITIONS: dict[str, dict[str, Any]]',
        '',
        'def create_setter_class(class_name: str, variable_name: str, definition: dict[str, Any]) -> type: ...',
        '',
        'def create_variable_class(class_name: str, definition: dict[str, Any], setter_class: type) -> type: ...',
        '',
        'def get_consolidated_variable_modules() -> list[Any]: ...',
        '',
        '# All classes are defined above - no additional exports needed in type stubs',
    ])
    
    lines.append('')
    
    return '\n'.join(lines) + '\n'


def main():
    """Main execution function."""
    # Setup paths using pathlib
    base_path = Path(__file__).parent.parent
    scripts_input_path = Path(__file__).parent / "input"
    scripts_output_path = Path(__file__).parent / "output"
    src_path = base_path / "src" / "qnty"
    
    parsed_file = scripts_input_path / "unit_data.json"
    dimension_file = scripts_output_path / "dimension_mapping.json"
    output_file = src_path / "variables.pyi"
    
    print("Loading parsed units data for type stub generation...")
    
    # Load the same data sources used for consolidated variables
    parsed_data = load_json_data(parsed_file)
    dimension_mapping = load_json_data(dimension_file)
    
    print(f"Loaded {len(parsed_data)} fields with units")
    
    # Augment data with missing prefixed units (same as variables generation)
    print("\nAugmenting data with missing prefixed units...")
    augmented_data = augment_parsed_data_with_prefixes(parsed_data)
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in augmented_data.values() if field_data.get('units'))
    original_total = sum(len(field_data.get('units', [])) for field_data in parsed_data.values())
    total_units = sum(len(field_data.get('units', [])) for field_data in augmented_data.values())
    
    print(f"Found {len(augmented_data)} total fields, {fields_with_units} fields with units")
    print(f"Original units: {original_total}")
    print(f"Total units (with prefixes): {total_units}")
    print(f"Generated prefixed units: {total_units - original_total}")
    
    # Generate type stub file
    print("Generating variables.pyi...")
    content = generate_consolidated_pyi(augmented_data, dimension_mapping)
    
    # Write output file
    save_text_file(content, output_file)
    print(f"Generated type stub file: {output_file}")
    
    # Print statistics
    lines_count = len(content.splitlines())
    print("\nStatistics:")
    print(f"  Total variable types: {fields_with_units}")
    print(f"  Total units: {total_units}")
    print(f"  Generated lines: {lines_count:,}")
    
    # Show top variable types by unit count
    fields_by_units = [(field_name, len(field_data.get('units', [])), field_data.get('field', ''))
                       for field_name, field_data in parsed_data.items() if field_data.get('units')]
    fields_by_units.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop variable types by unit property count:")
    for field_name, unit_count, display_name in fields_by_units[:10]:
        class_name = convert_to_class_name(field_name)
        print(f"  {class_name:<25} : {unit_count:>3} properties ({display_name})")
    
    print("\n✅ Complete type stub generated with full IDE support!")


if __name__ == "__main__":
    main()
