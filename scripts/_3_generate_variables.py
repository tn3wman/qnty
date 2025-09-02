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

from qnty.prefixes import PREFIXABLE_UNITS, StandardPrefixes


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
    prefixed_symbol = prefix_def.apply_to_symbol(base_unit_data.get('si_metric', {}).get('unit', base_unit_data.get('notation', '')))
    
    # Calculate new SI factor
    base_factor = base_unit_data.get('si_metric', {}).get('conversion_factor', 1.0)
    new_factor = base_factor * prefix_def.factor
    
    # Create new unit data
    return {
        'name': prefix_def.apply_to_name(base_unit_data['name']),
        'normalized_name': prefixed_name,
        'notation': prefixed_symbol,
        'si_metric': {
            'conversion_factor': new_factor,
            'unit': base_unit_data.get('si_metric', {}).get('unit', base_unit_data.get('notation', ''))
        },
        'english_us': base_unit_data.get('english_us', {}),
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
    property_name = unit_name.replace('-', '_').replace(' ', '_').replace('.', '_')
    
    # Handle Python reserved words and other edge cases
    reserved_words = {'class', 'def', 'if', 'else', 'for', 'while', 'import', 'from', 'as', 'in'}
    if property_name in reserved_words:
        property_name = f"{property_name}_unit"
    
    return property_name


def generate_consolidated_variables(parsed_data: dict, dimension_mapping: dict) -> str:
    """Generate the variables.py content using exact same approach as consolidated units."""
    
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
            for i, const in enumerate(sorted_constants):
                if i == len(sorted_constants) - 1:
                    import_lines.append(f'    {const}')  # No comma on last import
                else:
                    import_lines.append(f'    {const},')
            import_lines.append(')')
        else:
            imports_str = ', '.join(sorted_constants)
            import_lines = [f'from .dimension import {imports_str}']
    else:
        import_lines = ['from .dimension import DIMENSIONLESS']
    
    lines = [
        '"""',
        'Consolidated Variables Module - Complete Edition',
        '===============================================',
        '',
        'Consolidated variable definitions for all variable types.',
        'Uses the exact same source of truth and approach as consolidated units system.',
        'Auto-generated from unit_data.json and dimension_mapping.json.',
        '"""',
        '',
        'from typing import Any, cast',
        ''
    ]
    lines.extend(import_lines)
    lines.extend([
        'from .unit import UnitConstant, UnitDefinition',
        'from .units import DimensionlessUnits',
        'from .variable import FastQuantity, TypeSafeSetter',
        'from .variable_types.typed_variable import TypedVariable',
        '',
        '# Consolidated variable definitions',
        'VARIABLE_DEFINITIONS = {'
    ])
    
    # Generate variable definitions for each field
    # (fields_with_units already computed above)
    
    for i, (field_name, field_data) in enumerate(fields_with_units):
        comma = ',' if i < len(fields_with_units) - 1 else ''
        
        class_name = convert_to_class_name(field_name)
        dimension_constant = get_dimension_constant_name(field_name, dimension_mapping)
        display_name = field_data.get('field', class_name)
        
        lines.append(f'    "{class_name}": {{')
        lines.append(f'        "dimension": {dimension_constant},')
        
        # Helper function to escape strings properly for Python
        def escape_string(s):
            return s.replace("\\", "\\\\").replace('"', '\\"')
        
        # Choose the SI unit (conversion factor = 1.0) as default
        si_unit = None
        for unit in field_data['units']:
            if unit.get('si_metric', {}).get('conversion_factor', 0) == 1.0:
                si_unit = unit
                break
        
        # Fallback to first unit if no SI unit found
        default_unit = si_unit or (field_data['units'][0] if field_data['units'] else {})
        default_unit_name = default_unit.get('name', 'dimensionless')
        default_property = convert_unit_name_to_property(default_unit_name)
        escaped_default_property = escape_string(default_property)
        lines.append(f'        "default_unit": "{escaped_default_property}",')
        
        lines.append('        "units": [')
        
        # Add all units for this field
        for j, unit_data in enumerate(field_data['units']):
            unit_comma = ',' if j < len(field_data['units']) - 1 else ''
            unit_name = unit_data['name']
            property_name = convert_unit_name_to_property(unit_name)
            si_factor = unit_data.get('si_metric', {}).get('conversion_factor', 1.0)
            symbol = unit_data.get('si_metric', {}).get('unit', unit_name)
            aliases = unit_data.get('aliases', [])
            
            escaped_unit_name = escape_string(unit_name)
            escaped_property_name = escape_string(property_name)
            escaped_symbol = escape_string(symbol)
            escaped_aliases = [escape_string(alias) for alias in aliases]
            
            lines.append(f'            ("{escaped_unit_name}", "{escaped_property_name}", {si_factor}, "{escaped_symbol}", {escaped_aliases}){unit_comma}')
        
        lines.append('        ],')
        lines.append(f'        "field_name": "{field_name}",')
        escaped_display_name = escape_string(display_name)
        lines.append(f'        "display_name": "{escaped_display_name}",')
        lines.append(f'    }}{comma}')
    
    lines.append('}')
    lines.append('')
    
    # Add special Dimensionless variable first (not auto-generated)
    lines.extend([
        '# Special Dimensionless variable - handcrafted for proper behavior',
        'class DimensionlessSetter(TypeSafeSetter):',
        '    """Dimensionless-specific setter with only dimensionless units."""',
        '    ',
        '    def __init__(self, variable: \'Dimensionless\', value: float):',
        '        super().__init__(variable, value)',
        '    ',
        '    # Dimensionless units',
        '    @property',
        '    def dimensionless(self) -> \'Dimensionless\':',
        '        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)',
        '        return cast(\'Dimensionless\', self.variable)',
        '    ',
        '    # Common alias for no units',
        '    @property',
        '    def unitless(self) -> \'Dimensionless\':',
        '        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)',
        '        return cast(\'Dimensionless\', self.variable)',
        '',
        '',
        'class Dimensionless(TypedVariable):',
        '    """Type-safe dimensionless variable with expression capabilities."""',
        '',
        '    _setter_class = DimensionlessSetter',
        '    _expected_dimension = DIMENSIONLESS',
        '    _default_unit_property = "dimensionless"',
        '    ',
        '    def set(self, value: float) -> DimensionlessSetter:',
        '        """Create a dimensionless setter for this variable with proper type annotation."""',
        '        return DimensionlessSetter(self, value)',
        '',
        '',
    ])
    
    # Add the utility function needed for dynamic alias creation
    lines.extend([
        '',
        'def convert_unit_name_to_property(unit_name: str) -> str:',
        '    """Convert unit name to property name without automatic pluralization."""',
        '    # Use unit name as-is for property name',
        '    # Replace any characters that are not valid Python identifiers',
        '    property_name = unit_name.replace(\'-\', \'_\').replace(\' \', \'_\').replace(\'.\', \'_\')',
        '    ',
        '    # Handle Python reserved words and other edge cases',
        '    reserved_words = {\'class\', \'def\', \'if\', \'else\', \'for\', \'while\', \'import\', \'from\', \'as\', \'in\'}',
        '    if property_name in reserved_words:',
        '        property_name = f"{property_name}_unit"',
        '    ',
        '    return property_name',
        '',
        '',
        'def create_setter_class(class_name: str, variable_name: str, definition: dict[str, Any]) -> type:',
        '    """Dynamically create a setter class with unit properties."""',
        '    ',
        '    # Create base setter class',
        '    setter_class = type(',
        '        class_name,',
        '        (TypeSafeSetter,),',
        '        {',
        '            \'__init__\': lambda self, variable, value: TypeSafeSetter.__init__(self, variable, value),',
        '            \'__doc__\': f"{variable_name}-specific setter with only {variable_name.lower()} units."',
        '        }',
        '    )',
        '    ',
        '    # Add properties for each unit using unit data directly',
        '    for unit_name, property_name, si_factor, symbol, aliases in definition["units"]:',
        '        # Create a unit definition from the consolidated data',
        '        def make_property(unit_nm, si_fac, sym):',
        '            def getter(self):',
        '                # Create unit definition and constant from consolidated unit data',
        '                unit_def = UnitDefinition(',
        '                    name=unit_nm,',
        '                    symbol=sym,',
        '                    dimension=definition["dimension"],',
        '                    si_factor=si_fac',
        '                )',
        '                unit_const = UnitConstant(unit_def)',
        '                self.variable.quantity = FastQuantity(self.value, unit_const)',
        '                return self.variable  # type: ignore',
        '            return property(getter)',
        '        ',
        '        # Add the primary property to the class',
        '        setattr(setter_class, property_name, make_property(unit_name, si_factor, symbol))',
        '        ',
        '        # Add alias properties',
        '        for alias in aliases:',
        '            # Convert alias to valid property name',
        '            alias_property = convert_unit_name_to_property(alias)',
        '            # Only add if it\'s different from the main property and doesn\'t already exist',
        '            if alias_property != property_name and not hasattr(setter_class, alias_property):',
        '                setattr(setter_class, alias_property, make_property(unit_name, si_factor, symbol))',
        '    ',
        '    return setter_class',
        '',
        '',
        'def create_variable_class(class_name: str, definition: dict[str, Any], setter_class: type) -> type:',
        '    """Dynamically create a variable class."""',
        '    ',
        '    # Create the variable class',
        '    variable_class = type(',
        '        class_name,',
        '        (TypedVariable,),',
        '        {',
        '            \'_setter_class\': setter_class,',
        '            \'_expected_dimension\': definition["dimension"],',
        '            \'_default_unit_property\': definition["default_unit"],',
        '            \'__doc__\': f"Type-safe {class_name.lower()} variable with expression capabilities.",',
        '            \'set\': lambda self, value: setter_class(self, value)',
        '        }',
        '    )',
        '    ',
        '    # Add type hint for set method',
        '    variable_class.set.__annotations__ = {\'value\': float, \'return\': setter_class}',
        '    ',
        '    return variable_class',
        '',
        '',
        '# Create all variable and setter classes dynamically',
        'for var_name, var_def in VARIABLE_DEFINITIONS.items():',
        '    # Create setter class',
        '    setter_name = f"{var_name}Setter"',
        '    setter_class = create_setter_class(setter_name, var_name, var_def)',
        '    ',
        '    # Create variable class',
        '    variable_class = create_variable_class(var_name, var_def, setter_class)',
        '    ',
        '    # Export them to module namespace',
        '    globals()[setter_name] = setter_class',
        '    globals()[var_name] = variable_class',
        '',
    ])
    
    # Generate individual exports for easier access
    lines.extend([
        '# Individual exports for easier import',
        '# Special Dimensionless class is already defined above',
        '',
    ])
    
    for field_name, _ in fields_with_units:
        class_name = convert_to_class_name(field_name)
        setter_name = f"{class_name}Setter"
        lines.append(f'{setter_name} = globals()[\'{setter_name}\']')
        lines.append(f'{class_name} = globals()[\'{class_name}\']')
    
    lines.extend([
        '',
        '',
        '# Module registration compatibility',
        'def get_consolidated_variable_modules():',
        '    """Return module-like objects for consolidated variables."""',
        '    ',
        '    class ConsolidatedVariableModule:',
        '        """Mock module object for compatibility with existing registration system."""',
        '        ',
        '        def __init__(self, var_name: str):',
        '            self.var_name = var_name',
        '            self.definition = VARIABLE_DEFINITIONS[var_name]',
        '            self.variable_class = globals()[var_name]',
        '            self.setter_class = globals()[f"{var_name}Setter"]',
        '        ',
        '        def get_variable_class(self):',
        '            return self.variable_class',
        '        ',
        '        def get_setter_class(self):',
        '            return self.setter_class',
        '        ',
        '        def get_expected_dimension(self):',
        '            return self.definition["dimension"]',
        '    ',
        '    return ['
    ])
    
    # Add all variable modules to the list
    for i, (field_name, _) in enumerate(fields_with_units):
        class_name = convert_to_class_name(field_name)
        comma = ',' if i < len(fields_with_units) - 1 else ''
        lines.append(f'        ConsolidatedVariableModule("{class_name}"){comma}')
    
    lines.extend([
        '    ]',
        ''
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
