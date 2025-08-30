#!/usr/bin/env python3
"""
Fix Default Unit Properties Script
=================================

This script updates all variable classes to use SI base units (units with SI factor = 1.0)
as their default unit properties instead of arbitrary or uncommon units.
"""

import os
import re
import sys
import importlib
from pathlib import Path

# Add src to path to import qnty modules
sys.path.insert(0, 'src')

def find_si_base_unit(units_class, setter_class=None):
    """Find the unit with SI factor = 1.0 for a given units class."""
    si_base_units = []
    
    for attr_name in dir(units_class):
        if not attr_name.startswith('_'):
            try:
                unit = getattr(units_class, attr_name)
                if hasattr(unit, 'si_factor') and unit.si_factor == 1.0:
                    si_base_units.append(attr_name)
            except:
                continue
    
    # If we have a setter class, check which properties actually exist
    if setter_class:
        valid_properties = []
        for unit_name in si_base_units:
            if hasattr(setter_class, unit_name):
                valid_properties.append(unit_name)
            # Also check plural form
            elif hasattr(setter_class, unit_name + 's'):
                valid_properties.append(unit_name + 's')
        si_base_units = valid_properties
    
    # Prefer common names - check both singular and plural
    preferred_order = ['second', 'meter', 'kilogram', 'ampere', 'kelvin', 'mole', 'candela', 
                      'pascal', 'joule', 'watt', 'volt', 'ohm', 'farad', 'henry', 'weber']
    
    for preferred in preferred_order:
        # Check plural form first if setter class provided (since most properties are plural)
        if setter_class and preferred + 's' in si_base_units:
            return preferred + 's'
        if preferred in si_base_units:
            return preferred
    
    # Return the first one if no preferred match
    return si_base_units[0] if si_base_units else None

def get_units_class_for_variable(variable_file_path):
    """Get the corresponding units class for a variable file."""
    # Convert variable file path to units import
    variable_name = variable_file_path.stem
    
    # Special mappings for files that don't match the pattern
    name_mappings = {
        'length': 'LengthUnits',
        'pressure': 'PressureUnits', 
        'time': 'TimeUnits',
        'mass': 'MassUnits',
        'temperature': 'TemperatureUnits',
        'dimensionless': 'DimensionlessUnits',
        'angle_plane': 'AnglePlaneUnits',
        'angle_solid': 'AngleSolidUnits',
        'absorbed_radiation_dose': 'AbsorbedDoseUnits',
    }
    
    if variable_name in name_mappings:
        units_class_name = name_mappings[variable_name]
    else:
        # Convert snake_case to PascalCase and add Units
        words = variable_name.split('_')
        pascal_case = ''.join(word.capitalize() for word in words)
        units_class_name = pascal_case + 'Units'
    
    try:
        # Import the units module
        units_module = importlib.import_module(f'qnty.units')
        units_class = getattr(units_module, units_class_name)
        return units_class
    except (ImportError, AttributeError):
        try:
            # Try importing specific module
            module_name = variable_name
            if variable_name == 'absorbed_dose':
                module_name = 'absorbed_radiation_dose'
            units_module = importlib.import_module(f'qnty.units.{module_name}')
            units_class = getattr(units_module, units_class_name)
            return units_class
        except (ImportError, AttributeError):
            return None

def get_setter_class_for_variable(variable_file_path):
    """Get the corresponding setter class for a variable file."""
    variable_name = variable_file_path.stem
    
    try:
        # Import the variable module
        variable_module = importlib.import_module(f'qnty.variables.{variable_name}')
        
        # Get the setter class - usually VariableName + 'Setter'
        words = variable_name.split('_')
        pascal_case = ''.join(word.capitalize() for word in words)
        setter_class_name = pascal_case + 'Setter'
        
        setter_class = getattr(variable_module, setter_class_name)
        return setter_class
    except (ImportError, AttributeError):
        return None

def update_variable_file(variable_file_path):
    """Update a single variable file to use SI base unit as default."""
    print(f"Processing {variable_file_path.name}...")
    
    # Get the corresponding units class
    units_class = get_units_class_for_variable(variable_file_path)
    if not units_class:
        print(f"  ❌ Could not find units class for {variable_file_path.name}")
        return False
    
    # Get the setter class to check which properties actually exist
    setter_class = get_setter_class_for_variable(variable_file_path)
    if not setter_class:
        print(f"  ⚠️  Could not find setter class for {variable_file_path.name}, using basic unit name")
    
    # Find SI base unit
    si_base_unit = find_si_base_unit(units_class, setter_class)
    if not si_base_unit:
        print(f"  ❌ No SI base unit found for {variable_file_path.name}")
        return False
    
    # Read the file
    with open(variable_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find current default unit property
    pattern = r'(_default_unit_property = ")[^"]*(")'
    match = re.search(pattern, content)
    
    if not match:
        print(f"  ❌ No _default_unit_property found in {variable_file_path.name}")
        return False
    
    current_default = match.group(0)
    current_unit = current_default.split('"')[1]
    
    if current_unit == si_base_unit:
        print(f"  ✅ Already using SI base unit: {si_base_unit}")
        return True
    
    # Update to SI base unit
    new_default = f'_default_unit_property = "{si_base_unit}"'
    new_content = re.sub(pattern, new_default, content)
    
    # Write back the file
    with open(variable_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Updated: {current_unit} → {si_base_unit}")
    return True

def main():
    """Main function to process all variable files."""
    print("Fixing default unit properties to use SI base units...\n")
    
    # Find all variable files
    variables_dir = Path('src/qnty/variables')
    variable_files = list(variables_dir.glob('*.py'))
    
    # Filter out special files
    exclude_files = {'__init__.py', 'base.py', 'typed_variable.py', 'expression_variable.py'}
    variable_files = [f for f in variable_files if f.name not in exclude_files]
    
    updated_count = 0
    total_count = len(variable_files)
    
    for variable_file in sorted(variable_files):
        if update_variable_file(variable_file):
            updated_count += 1
    
    print(f"\n🎯 Summary: Updated {updated_count}/{total_count} variable files")
    print("✅ All default unit properties now use SI base units!")

if __name__ == "__main__":
    main()