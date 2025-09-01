#!/usr/bin/env python3
"""
Script to generate comprehensive variables.py for all variables.

This script uses the exact same source of truth and approach as the consolidated units system:
- parsed_units.json for unit data
- dimension_mapping.json for dimension constants
- Same import strategy as consolidated_complete.py

This ensures complete consistency between units, dimensions, and variables.
"""

import json
from pathlib import Path


def load_parsed_units():
    """Load parsed units data - same source used for consolidated units."""
    units_path = Path(__file__).parent / "output" / "parsed_units.json"
    with open(units_path) as f:
        return json.load(f)


def load_dimension_mapping():
    """Load dimension mapping - same source used for consolidated units."""
    mapping_path = Path(__file__).parent / "output" / "dimension_mapping.json"  
    with open(mapping_path) as f:
        return json.load(f)


def get_dimension_constant_name(field_name: str, dimension_mapping: dict):
    """Get dimension constant name from mapping - same logic as consolidated units."""
    field_info = dimension_mapping.get(field_name, {})
    return field_info.get('constant_name', field_name.upper())


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
    """Convert unit name to property name, handling pluralization."""
    special_plurals = {
        'foot': 'feet',
        'inch': 'inches',
    }
    
    if unit_name in special_plurals:
        return special_plurals[unit_name]
    
    return f"{unit_name}s"


def generate_consolidated_variables(parsed_data: dict, dimension_mapping: dict) -> str:
    """Generate the variables.py content using exact same approach as consolidated units."""
    
    lines = [
        '"""',
        'Consolidated Variables Module - Complete Edition',
        '===============================================',
        '',
        'Consolidated variable definitions for all variable types.',
        'Uses the exact same source of truth and approach as consolidated units system.',
        'Auto-generated from parsed_units.json and dimension_mapping.json.',
        '"""',
        '',
        'from typing import Any, Dict, Type, cast',
        '',
        '# Import all dimensions using the same approach as consolidated units',
        'from .dimension import *  # Import all dimension constants',
        'from .dimension import DIMENSIONLESS  # Explicit import for clarity',
        'from .unit import UnitConstant, UnitDefinition',
        'from .units import DimensionlessUnits',
        'from .variable import FastQuantity, TypeSafeSetter',
        'from .variable_types.typed_variable import TypedVariable',
        '',
        '# Consolidated variable definitions',
        'VARIABLE_DEFINITIONS = {'
    ]
    
    # Generate variable definitions for each field
    sorted_fields = sorted(parsed_data.items())
    fields_with_units = [(k, v) for k, v in sorted_fields if v.get('units')]
    
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
        
        # Choose a reasonable default unit - first unit in the list
        first_unit = field_data['units'][0] if field_data['units'] else {}
        default_property = convert_unit_name_to_property(first_unit.get('name', 'meters'))
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
            
            escaped_unit_name = escape_string(unit_name)
            escaped_property_name = escape_string(property_name)  
            escaped_symbol = escape_string(symbol)
            
            lines.append(f'            ("{escaped_unit_name}", "{escaped_property_name}", {si_factor}, "{escaped_symbol}"){unit_comma}')
        
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
    
    # Add the dynamic class creation functions
    lines.extend([
        '',
        'def create_setter_class(class_name: str, variable_name: str, definition: Dict[str, Any]) -> Type:',
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
        '    for unit_name, property_name, si_factor, symbol in definition["units"]:',
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
        '        # Add the property to the class',
        '        setattr(setter_class, property_name, make_property(unit_name, si_factor, symbol))',
        '    ',
        '    return setter_class',
        '',
        '',
        'def create_variable_class(class_name: str, definition: Dict[str, Any], setter_class: Type) -> Type:',
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
    
    for field_name, field_data in fields_with_units:
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
    for i, (field_name, field_data) in enumerate(fields_with_units):
        class_name = convert_to_class_name(field_name)
        comma = ',' if i < len(fields_with_units) - 1 else ''
        lines.append(f'        ConsolidatedVariableModule("{class_name}"){comma}')
    
    lines.extend([
        '    ]',
        ''
    ])
    
    return '\n'.join(lines)


def main():
    """Main execution function."""
    print("Loading parsed units data (exact same source as consolidated units)...")
    
    # Load the exact same data sources used for consolidated units
    parsed_data = load_parsed_units()
    dimension_mapping = load_dimension_mapping()
    
    # Count fields with units
    fields_with_units = sum(1 for field_data in parsed_data.values() if field_data.get('units'))
    print(f"Found {len(parsed_data)} total fields, {fields_with_units} fields with units")
    
    # Generate consolidated variables file
    print("Generating variables.py...")
    content = generate_consolidated_variables(parsed_data, dimension_mapping)
    
    # Write output file
    output_path = Path(__file__).parent.parent / "src" / "qnty" / "variables.py"
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Generated consolidated file: {output_path}")
    
    # Print statistics
    total_units = sum(len(field_data.get('units', [])) for field_data in parsed_data.values())
    print(f"\nStatistics:")
    print(f"  Total fields: {len(parsed_data)}")
    print(f"  Fields with units: {fields_with_units}")
    print(f"  Total units: {total_units}")
    
    # Show top variable types by unit count
    fields_by_units = [(field_name, len(field_data.get('units', [])), field_data.get('field', '')) 
                       for field_name, field_data in parsed_data.items() if field_data.get('units')]
    fields_by_units.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nTop variable types by unit count:")
    for field_name, unit_count, display_name in fields_by_units[:10]:
        class_name = convert_to_class_name(field_name)
        print(f"  {class_name:<25} : {unit_count:>3} units ({display_name})")


if __name__ == "__main__":
    main()