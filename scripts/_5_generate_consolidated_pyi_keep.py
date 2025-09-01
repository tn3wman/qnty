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


def load_parsed_units():
    """Load parsed units data - same source used for consolidated variables."""
    units_path = Path(__file__).parent / "output" / "parsed_units.json"
    with open(units_path) as f:
        return json.load(f)


def load_dimension_mapping():
    """Load dimension mapping - same source used for consolidated variables."""
    mapping_path = Path(__file__).parent / "output" / "dimension_mapping.json"  
    with open(mapping_path) as f:
        return json.load(f)


def convert_to_class_name(field_name: str) -> str:
    """Convert field name to PascalCase class name."""
    words = field_name.split('_')
    class_name = ''.join(word.capitalize() for word in words)
    
    # Handle specific naming conventions
    class_name_fixes = {
        'MassFractionOfI': 'MassFractionOfI',
        'MoleFractionOfI': 'MoleFractionOfI', 
        'VolumeFractionOfI': 'VolumeFractionOfI',
        'MolarityOfI': 'MolarityOfI',
        'MolalityOfSoluteI': 'MolalityOfSoluteI',
    }
    
    return class_name_fixes.get(class_name, class_name)


def convert_unit_name_to_property(unit_name: str) -> str:
    """Convert unit name to property name, handling pluralization and Python identifiers."""
    import re
    
    # Replace spaces and invalid characters with underscores
    property_name = re.sub(r'[^a-zA-Z0-9_]', '_', unit_name)
    
    # Remove leading/trailing underscores and collapse multiple underscores
    property_name = re.sub(r'^_+|_+$', '', property_name)
    property_name = re.sub(r'_+', '_', property_name)
    
    # Ensure it starts with a letter or underscore (valid Python identifier)
    if property_name and property_name[0].isdigit():
        property_name = f"_{property_name}"
    
    # Handle special pluralization cases for common units
    special_plurals = {
        'foot': 'feet',
        'inch': 'inches',
    }
    
    if property_name in special_plurals:
        return special_plurals[property_name]
    
    # Default pluralization (but ensure we don't add 's' if it already ends with 's')
    if property_name.endswith('s'):
        return property_name
    return f"{property_name}s"


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
        'from typing import Dict, Any, Type, List',
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
        '    def __init__(self, variable: \'Dimensionless\', value: float) -> None: ...',
        '    ',
        '    @property',
        '    def dimensionless(self) -> \'Dimensionless\': ...',
        '    ',
        '    @property',
        '    def unitless(self) -> \'Dimensionless\': ...',
        '',
        '',
        'class Dimensionless(TypedVariable):',
        '    """Type-safe dimensionless variable with expression capabilities."""',
        '',
        '    _setter_class: Type[TypeSafeSetter] | None',
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
            f'    def __init__(self, variable: \'{class_name}\', value: float) -> None: ...',
            '    ',
            f'    # All {display_name.lower()} unit properties - provides fluent API with full type hints'
        ])
        
        # Add property stubs for each unit
        for unit_data in field_data['units']:
            unit_name = unit_data['name']
            property_name = convert_unit_name_to_property(unit_name)
            
            lines.extend([
                '    @property',
                f'    def {property_name}(self) -> \'{class_name}\': ...'
            ])
        
        lines.append('')
        
        # Generate variable class
        lines.extend([
            f'class {class_name}(TypedVariable):',
            f'    """Type-safe {display_name.lower()} variable with expression capabilities."""',
            '    ',
            f'    _setter_class: Type[TypeSafeSetter] | None',
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
        'VARIABLE_DEFINITIONS: Dict[str, Dict[str, Any]]',
        '',
        'def create_setter_class(class_name: str, variable_name: str, definition: Dict[str, Any]) -> Type: ...',
        '',
        'def create_variable_class(class_name: str, definition: Dict[str, Any], setter_class: Type) -> Type: ...',
        '',
        'def get_consolidated_variable_modules() -> List[Any]: ...',
        '',
        '# All classes are defined above - no additional exports needed in type stubs',
    ])
    
    lines.append('')
    
    return '\n'.join(lines)


def main():
    """Main execution function."""
    print("Loading parsed units data for type stub generation...")
    
    # Load the same data sources used for consolidated variables
    parsed_data = load_parsed_units()
    dimension_mapping = load_dimension_mapping()
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in parsed_data.values() if field_data.get('units'))
    total_units = sum(len(field_data.get('units', [])) for field_data in parsed_data.values())
    
    print(f"Found {len(parsed_data)} total fields, {fields_with_units} fields with units")
    print(f"Total units: {total_units}")
    
    # Generate type stub file
    print("Generating variables.pyi...")
    content = generate_consolidated_pyi(parsed_data, dimension_mapping)
    
    # Write output file
    output_path = Path(__file__).parent.parent / "src" / "qnty" / "variables.pyi"
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Generated type stub file: {output_path}")
    
    # Print statistics
    lines_count = len(content.splitlines())
    print(f"\nStatistics:")
    print(f"  Total variable types: {fields_with_units}")
    print(f"  Total units: {total_units}")
    print(f"  Generated lines: {lines_count:,}")
    
    # Show top variable types by unit count
    fields_by_units = [(field_name, len(field_data.get('units', [])), field_data.get('field', '')) 
                       for field_name, field_data in parsed_data.items() if field_data.get('units')]
    fields_by_units.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop variable types by unit property count:")
    for field_name, unit_count, display_name in fields_by_units[:10]:
        class_name = convert_to_class_name(field_name)
        print(f"  {class_name:<25} : {unit_count:>3} properties ({display_name})")
    
    print(f"\n✅ Complete type stub generated with full IDE support!")


if __name__ == "__main__":
    main()