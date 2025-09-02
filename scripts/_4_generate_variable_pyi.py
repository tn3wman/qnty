#!/usr/bin/env python3
"""
Script to generate comprehensive variables.pyi type stub file.

This script generates complete type hints for all 105 variable types in the
consolidated variables system, providing full IDE autocomplete and type checking
support for the fluent API with dimension-specific unit properties.

Uses the same source of truth as the consolidated variables system.
"""

import json
from pathlib import Path


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
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in parsed_data.values() if field_data.get('units'))
    total_units = sum(len(field_data.get('units', [])) for field_data in parsed_data.values())
    
    print(f"Found {len(parsed_data)} total fields, {fields_with_units} fields with units")
    print(f"Total units: {total_units}")
    
    # Generate type stub file
    print("Generating variables.pyi...")
    content = generate_consolidated_pyi(parsed_data, dimension_mapping)
    
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
