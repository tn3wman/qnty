#!/usr/bin/env python3
"""
Script to generate comprehensive variables.py for all variables.

This script uses the exact same source of truth and approach as the consolidated units system:
- unit_data.json for unit data
- dimension_mapping.json for dimension constants
- Same import strategy as consolidated_complete.py

This ensures complete consistency between units, dimensions, and variables.
"""

import json
import sys
from pathlib import Path

# Add src/qnty to the path to import prefix system
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import prefixes directly to avoid circular import
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "qnty"))
from qnty.units.prefixes import PREFIXABLE_UNITS, StandardPrefixes


def load_json_data(file_path: Path) -> dict:
    """Load JSON data from file."""
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def save_text_file(content: str, file_path: Path) -> None:
    """Save text content to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_dimension_constant_name(field_name: str, dimension_mapping: dict):
    """Get dimension constant name from mapping - same logic as consolidated units."""
    field_info = dimension_mapping.get(field_name, {})
    return field_info.get('constant_name', field_name.upper())


def convert_to_class_name(field_name: str) -> str:
    """Convert field name to PascalCase class name."""
    words = field_name.split('_')
    return ''.join(word.capitalize() for word in words)


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
    
    print(f"Generated {generated_count} missing prefixed units for variables")
    return augmented_data


def convert_unit_name_to_property(unit_name: str) -> str:
    """Convert unit name to property name without automatic pluralization."""
    # Use unit name as-is for property name
    # Replace any characters that are not valid Python identifiers
    property_name = (unit_name.replace('-', '_')
                              .replace(' ', '_')
                              .replace('.', '_')
                              .replace('(', '_')
                              .replace(')', '_')
                              .replace(',', '_')
                              .replace("'", '_')
                              .replace('"', '_')
                              .replace('/', '_')
                              .replace('\\', '_')
                              .replace('°', '_degree_')
                              .replace('²', '_square_')
                              .replace('³', '_cubic_')
                              .replace('μ', 'u')
                              .replace('Ω', 'ohm')
                              .replace('$', '_')
                              .replace('{', '_')
                              .replace('}', '_')
                              .replace('[', '_')
                              .replace(']', '_')
                              .replace('=', '_eq_')
                              .replace('+', '_plus_')
                              .replace('*', '_star_')
                              .replace('&', '_and_')
                              .replace('%', '_percent_')
                              .replace('#', '_hash_')
                              .replace('@', '_at_')
                              .replace('!', '_excl_')
                              .replace('?', '_quest_')
                              .replace('<', '_lt_')
                              .replace('>', '_gt_')
                              .replace('^', '_power_')
                              .replace('~', '_tilde_')
                              .replace('`', '_backtick_')
                              .replace('|', '_pipe_'))
    
    # Remove consecutive underscores and leading/trailing underscores
    import re
    property_name = re.sub(r'_+', '_', property_name).strip('_')
    
    # Handle Python reserved words and other edge cases
    reserved_words = {'class', 'def', 'if', 'else', 'for', 'while', 'import', 'from', 'as', 'in', 'or', 'and', 'not'}
    if property_name in reserved_words:
        property_name = f"{property_name}_unit"
    
    # Ensure it starts with letter or underscore (valid Python identifier)
    if property_name and not (property_name[0].isalpha() or property_name[0] == '_'):
        property_name = f"unit_{property_name}"
    
    return property_name


def generate_consolidated_variables(parsed_data: dict, dimension_mapping: dict) -> str:
    """Generate the variables.py content with static class definitions for performance."""
    
    # Collect all dimension constants used in the file
    dimension_constants = set()
    sorted_fields = sorted(parsed_data.items())
    fields_with_units = [(k, v) for k, v in sorted_fields if v.get('units')]
    
    for field_name, _ in fields_with_units:
        dimension_constant = get_dimension_constant_name(field_name, dimension_mapping)
        dimension_constants.add(dimension_constant)
    
    # Always include DIMENSIONLESS for the handcrafted Dimensionless class
    dimension_constants.add('DIMENSIONLESS')
    
    # Generate explicit dimension imports
    if dimension_constants:
        sorted_constants = sorted(dimension_constants)
        if len(sorted_constants) > 10:
            import_lines = ['from .dimension import (']
            for const in sorted_constants:
                import_lines.append(f'    {const},')  # Always add comma, even on last import
            import_lines.append(')')
        else:
            imports_str = ', '.join(sorted_constants)
            import_lines = [f'from .dimension import {imports_str}']
    else:
        import_lines = ['from .dimension import DIMENSIONLESS']
    
    lines = [
        '"""',
        'Optimized Variables Module - Static Class Edition',
        '================================================',
        '',
        'Static variable class definitions for maximum import performance.',
        'Uses static class generation instead of dynamic type() calls.',
        'Auto-generated from unit_data.json and dimension_mapping.json.',
        '"""',
        '',
        'from typing import TYPE_CHECKING',
        ''
    ]
    lines.extend(import_lines)
    lines.extend([
        'from . import units',
        'from .variable import FastQuantity, TypeSafeSetter',
        'from .variable_types.typed_variable import TypedVariable',
        '',
        'if TYPE_CHECKING:',
        '    pass',
        '',
        ''
    ])
    # Generate static setter and variable classes for maximum performance
    
    # Helper function to escape strings properly for Python
    def escape_string(s):
        return s.replace("\\", "\\\\").replace('"', '\\"')
    
    # Generate all setter classes first
    lines.append('# ===== SETTER CLASSES =====')
    lines.append('# Static setter class definitions with __slots__ optimization')
    lines.append('')
    
    for field_name, field_data in fields_with_units:
        class_name = convert_to_class_name(field_name)
        setter_class_name = f"{class_name}Setter"
        dimension_constant = get_dimension_constant_name(field_name, dimension_mapping)
        units_class_name = f"{class_name}Units"
        
        lines.append(f'class {setter_class_name}(TypeSafeSetter):')
        lines.append(f'    """{class_name}-specific setter with optimized unit properties."""')
        lines.append(f'    __slots__ = ()')
        lines.append(f'    ')
        
        # Generate property for each unit, avoiding duplicates
        generated_properties = set()
        
        for unit_data in field_data['units']:
            unit_name = unit_data['name']
            property_name = convert_unit_name_to_property(unit_name)
            
            # Skip if this property name was already generated
            if property_name in generated_properties:
                continue
            
            generated_properties.add(property_name)
            
            lines.append(f'    @property')
            lines.append(f'    def {property_name}(self):')
            lines.append(f'        """Set value using {unit_name} units."""')
            lines.append(f'        unit_const = units.{units_class_name}.{property_name}')
            lines.append(f'        self.variable.quantity = FastQuantity(self.value, unit_const)')
            lines.append(f'        return self.variable')
            lines.append(f'    ')
            
            # Add alias properties, checking for duplicates
            aliases = unit_data.get('aliases', [])
            for alias in aliases:
                alias_property = convert_unit_name_to_property(alias)
                # Only add if different from main property, doesn't conflict, and not already generated
                if (alias_property != property_name and 
                    alias_property.isidentifier() and 
                    alias_property not in generated_properties):
                    generated_properties.add(alias_property)
                    lines.append(f'    @property')
                    lines.append(f'    def {alias_property}(self):')
                    lines.append(f'        """Set value using {alias} units (alias for {unit_name})."""')
                    lines.append(f'        return self.{property_name}')
                    lines.append(f'    ')
        
        lines.append('')
    
    # Generate all variable classes
    lines.append('# ===== VARIABLE CLASSES =====')  
    lines.append('# Static variable class definitions with __slots__ optimization')
    lines.append('')
    
    for field_name, field_data in fields_with_units:
        class_name = convert_to_class_name(field_name)
        setter_class_name = f"{class_name}Setter"
        dimension_constant = get_dimension_constant_name(field_name, dimension_mapping)
        
        lines.append(f'class {class_name}(TypedVariable):')
        lines.append(f'    """Type-safe {class_name.lower()} variable with expression capabilities."""')
        lines.append(f'    __slots__ = ()')
        lines.append(f'    _setter_class = {setter_class_name}')
        lines.append(f'    _expected_dimension = {dimension_constant}')
        lines.append(f'    ')
        lines.append(f'    def set(self, value: float) -> {setter_class_name}:')
        lines.append(f'        """Create a setter for this variable."""')
        lines.append(f'        return {setter_class_name}(self, value)')
        lines.append(f'    ')
        lines.append('')
    
    # Add utility function for completeness
    lines.extend([
        '# Utility functions',
        'def convert_unit_name_to_property(unit_name: str) -> str:',
        '    """Convert unit name to property name without automatic pluralization."""',
        '    import re',
        '    property_name = (unit_name.replace("-", "_")',
        '                              .replace(" ", "_")',
        '                              .replace(".", "_")',
        '                              .replace("(", "_")',
        '                              .replace(")", "_")',
        '                              .replace(",", "_")',
        '                              .replace("\'", "_")',
        '                              .replace("\\\"", "_")',
        '                              .replace("/", "_")',
        '                              .replace("\\\\", "_")',
        '                              .replace("°", "_degree_")',
        '                              .replace("²", "_square_")',
        '                              .replace("³", "_cubic_")',
        '                              .replace("μ", "u")',
        '                              .replace("Ω", "ohm")',
        '                              .replace("$", "_")',
        '                              .replace("{", "_")',
        '                              .replace("}", "_")',
        '                              .replace("[", "_")',
        '                              .replace("]", "_")',
        '                              .replace("=", "_eq_")',
        '                              .replace("+", "_plus_")',
        '                              .replace("*", "_star_")',
        '                              .replace("&", "_and_")',
        '                              .replace("%", "_percent_")',
        '                              .replace("#", "_hash_")',
        '                              .replace("@", "_at_")',
        '                              .replace("!", "_excl_")',
        '                              .replace("?", "_quest_")',
        '                              .replace("<", "_lt_")',
        '                              .replace(">", "_gt_")',
        '                              .replace("^", "_power_")',
        '                              .replace("~", "_tilde_")',
        '                              .replace("`", "_backtick_")',
        '                              .replace("|", "_pipe_"))',
        '    property_name = re.sub(r"_+", "_", property_name).strip("_")',
        '    reserved_words = {"class", "def", "if", "else", "for", "while", "import", "from", "as", "in", "or", "and", "not"}',
        '    if property_name in reserved_words:',
        '        property_name = f"{property_name}_unit"',
        '    if property_name and not (property_name[0].isalpha() or property_name[0] == "_"):',
        '        property_name = f"unit_{property_name}"',
        '    return property_name',
        '',
    ])
    
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
    output_file = src_path / "variables.py"
    
    print("Loading parsed units data (exact same source as consolidated units)...")
    
    # Load the exact same data sources used for consolidated units
    parsed_data = load_json_data(parsed_file)
    dimension_mapping = load_json_data(dimension_file)
    
    print(f"Loaded {len(parsed_data)} fields with units")
    
    # Augment data with missing prefixed units (same as units generation)
    print("\nAugmenting data with missing prefixed units...")
    augmented_data = augment_parsed_data_with_prefixes(parsed_data)
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in augmented_data.values() if field_data.get('units'))
    print(f"Found {len(augmented_data)} total fields, {fields_with_units} fields with units")
    
    # Generate consolidated variables file
    print("Generating variables.py...")
    content = generate_consolidated_variables(augmented_data, dimension_mapping)
    
    # Write output file
    save_text_file(content, output_file)
    print(f"Generated consolidated file: {output_file}")
    
    # Auto-fix imports with ruff after generation
    import subprocess
    try:
        subprocess.run(['ruff', 'check', '--fix', str(output_file)], 
                      capture_output=True, check=False)
        print("Auto-applied ruff import fixes")
    except FileNotFoundError:
        print("Note: ruff not found - imports may need manual fixing")
    
    # Print statistics
    original_total = sum(len(field_data.get('units', [])) for field_data in parsed_data.values())
    augmented_total = sum(len(field_data.get('units', [])) for field_data in augmented_data.values())
    print("\nStatistics:")
    print(f"  Total fields: {len(augmented_data)}")
    print(f"  Fields with units: {fields_with_units}")
    print(f"  Original units: {original_total}")
    print(f"  Total units (with prefixes): {augmented_total}")
    print(f"  Generated prefixed units: {augmented_total - original_total}")
    
    # Show top variable types by unit count
    fields_by_units = [(field_name, len(field_data.get('units', [])), field_data.get('field', ''))
                       for field_name, field_data in augmented_data.items() if field_data.get('units')]
    fields_by_units.sort(key=lambda x: x[1], reverse=True)
    
    print("\nTop variable types by unit count:")
    for field_name, unit_count, display_name in fields_by_units[:10]:
        class_name = convert_to_class_name(field_name)
        print(f"  {class_name:<25} : {unit_count:>3} units ({display_name})")


if __name__ == "__main__":
    main()
