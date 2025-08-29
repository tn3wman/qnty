"""
Automatic Unit and Variable Generator
======================================

This script automatically generates unit and variable classes from markdown data files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def parse_markdown_table(file_path: str) -> Tuple[str, List[Dict[str, str]]]:
    """Parse a markdown table file and extract unit data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the title
    title_match = re.match(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(file_path).stem
    
    # Parse the table
    lines = content.split('\n')
    units = []
    
    for line in lines[5:]:  # Skip header lines
        if not line.strip() or line.startswith('|---'):
            continue
            
        parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last elements
        if len(parts) >= 7:
            unit_name = parts[1]
            notation = parts[2]
            si_dimension = parts[3]
            si_conversion = parts[4]
            si_unit = parts[5] if len(parts) > 5 else ""
            
            # Clean up conversion factors
            si_conversion = re.sub(r'[\$\\]|mathrm\{E\}', 'e', si_conversion)
            si_conversion = re.sub(r'[^\d.e+-]', '', si_conversion)
            
            # Handle special cases for conversion
            if si_conversion and si_conversion != '-':
                try:
                    # Replace comma with empty string for thousands
                    si_conversion = si_conversion.replace(',', '')
                    float(si_conversion)  # Validate it's a number
                    units.append({
                        'name': unit_name,
                        'notation': notation,
                        'dimension': si_dimension,
                        'conversion': si_conversion,
                        'si_unit': si_unit
                    })
                except ValueError:
                    continue
    
    return title, units


def sanitize_name(name: str) -> str:
    """Convert a unit name to a valid Python identifier."""
    # Remove parenthetical content
    name = re.sub(r'\([^)]*\)', '', name)
    # Replace special characters and spaces
    name = re.sub(r'[^\w\s]', '', name)
    name = name.replace(' ', '_').replace('-', '_')
    name = name.lower().strip()
    
    # Handle Python keywords
    if name in ['in', 'class', 'def', 'return', 'for', 'if', 'else', 'import', 'from']:
        name = f'{name}_'
    
    # Common temperature unit names
    if 'celsius' in name:
        return 'celsius'
    elif 'fahrenheit' in name:
        return 'fahrenheit'
    elif 'kelvin' in name:
        return 'kelvin'
    elif 'rankine' in name:
        return 'rankine'
    elif 'réaumur' in name or 'reaumur' in name:
        return 'reaumur'
    
    return name


def get_dimension_for_type(dimension_str: str, unit_type: str) -> str:
    """Determine the appropriate dimension constant based on the dimension string."""
    dimension_str = dimension_str.upper()
    
    # Check for common dimension patterns
    if 'DMLS' in dimension_str or 'DIMENSIONLESS' in dimension_str:
        return 'DIMENSIONLESS'
    elif dimension_str == 'T':
        return 'TIME'
    elif dimension_str == 'L':
        return 'LENGTH'
    elif dimension_str == 'M':
        return 'MASS'
    elif 'THETA' in dimension_str or 'Θ' in dimension_str or 'temperature' in unit_type.lower():
        return 'TEMPERATURE'
    elif 'L^2 T^-2' in dimension_str.replace(' ', '') or 'L2T-2' in dimension_str.replace(' ', ''):
        # Could be energy or absorbed dose
        if 'absorbed' in unit_type.lower() or 'radiation' in unit_type.lower():
            return 'ABSORBED_DOSE'
        else:
            return 'ENERGY'
    elif 'LT^-2' in dimension_str.replace(' ', '') or 'LT-2' in dimension_str.replace(' ', ''):
        return 'ACCELERATION'
    elif 'ML^-1T^-2' in dimension_str.replace(' ', '') or 'ML-1T-2' in dimension_str.replace(' ', ''):
        return 'PRESSURE'
    elif 'L^2' in dimension_str.replace(' ', '') or 'L2' in dimension_str.replace(' ', ''):
        return 'AREA'
    elif 'L^3' in dimension_str.replace(' ', '') or 'L3' in dimension_str.replace(' ', ''):
        return 'VOLUME'
    elif 'MLT^-2' in dimension_str.replace(' ', '') or 'MLT-2' in dimension_str.replace(' ', ''):
        return 'FORCE'
    elif 'ML^2T^-2' in dimension_str.replace(' ', '') or 'ML2T-2' in dimension_str.replace(' ', ''):
        return 'ENERGY'
    elif 'ML^2T^-3' in dimension_str.replace(' ', '') or 'ML2T-3' in dimension_str.replace(' ', ''):
        return 'POWER'
    else:
        # Default for known types
        if 'volume' in unit_type.lower():
            return 'VOLUME'
        elif 'mass' in unit_type.lower():
            return 'MASS'
        elif 'force' in unit_type.lower():
            return 'FORCE'
        elif 'energy' in unit_type.lower() or 'heat' in unit_type.lower() or 'work' in unit_type.lower():
            return 'ENERGY'
        elif 'power' in unit_type.lower():
            return 'POWER'
        return 'DIMENSIONLESS'


def generate_unit_module(title: str, units: List[Dict[str, str]], output_dir: str) -> str:
    """Generate a unit module file."""
    # Create class name from title
    class_base = ''.join(word.capitalize() for word in title.replace(',', '').split())
    if 'Angle' in class_base:
        class_base = 'Angle'
    elif 'Absorbed' in class_base and 'Dose' in class_base:
        class_base = 'AbsorbedDose'
    
    file_name = sanitize_name(title.replace(',', '_'))
    
    # Get dimension
    dimension = get_dimension_for_type(units[0]['dimension'] if units else 'DIMENSIONLESS', title)
    
    # Generate unit class declarations
    unit_declarations = []
    aliases = []
    unit_definitions = []
    
    for unit in units[:8]:  # Limit to most common units
        unit_name = sanitize_name(unit['name'])
        if not unit_name:
            continue
            
        unit_declarations.append(f"    {unit_name}: 'UnitConstant'")
        
        # Create a short alias if possible
        notation = unit['notation']
        if notation and len(notation) <= 5 and not any(c in notation for c in ['$', '{', '}', '^', '\\', '(', ')']):
            alias = re.sub(r'[^\w]', '', notation)
            if alias and alias != unit_name and alias not in ['in']:
                aliases.append(f"    {alias}: 'UnitConstant'")
        
        # Add unit definition
        # Clean up symbol
        symbol = notation
        if symbol:
            # Remove LaTeX commands and special characters
            symbol = re.sub(r'\\mathrm{([^}]+)}', r'\1', symbol)
            symbol = re.sub(r'[\${}\\^_]', '', symbol)
            symbol = re.sub(r'circ', '°', symbol)
            symbol = symbol.strip()
        
        # Use common abbreviations for known units
        if 'kelvin' in unit_name:
            symbol = 'K'
        elif 'celsius' in unit_name:
            symbol = '°C'
        elif 'fahrenheit' in unit_name:
            symbol = '°F'
        elif 'rankine' in unit_name:
            symbol = '°R'
        elif 'reaumur' in unit_name:
            symbol = '°Ré'
        elif not symbol:
            symbol = unit_name[:3]
            
        unit_definitions.append(
            f'            UnitDefinition("{unit_name}", "{symbol}", {dimension}, {unit["conversion"]}),')
    
    content = f'''"""
{class_base} Units Module
{'=' * (len(class_base) + 13)}

Complete {title.lower()} unit definitions and constants.
"""

from ..dimension import {dimension}
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class {class_base}Units:
    """Type-safe {title.lower()} unit constants."""
    # Explicit declarations for type checking
{chr(10).join(unit_declarations)}
    
    # Common aliases
{chr(10).join(aliases) if aliases else "    pass"}


class {class_base}UnitModule(UnitModule):
    """{class_base} unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all {title.lower()} unit definitions."""
        return [
{chr(10).join(unit_definitions)}
        ]
    
    def get_units_class(self):
        return {class_base}Units


# Register this module for auto-discovery
UNIT_MODULE = {class_base}UnitModule()'''
    
    # Write the file
    output_path = os.path.join(output_dir, f'{file_name}.py')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return class_base


def generate_variable_module(class_base: str, title: str, units: List[Dict[str, str]], output_dir: str) -> None:
    """Generate a variable module file."""
    file_name = sanitize_name(title.replace(',', '_'))
    dimension = get_dimension_for_type(units[0]['dimension'] if units else 'DIMENSIONLESS', title)
    
    # Generate setter properties
    setter_properties = []
    setter_aliases = []
    
    for unit in units[:8]:  # Limit to most common units
        unit_name = sanitize_name(unit['name'])
        if not unit_name:
            continue
            
        # Create property name (usually plural)
        prop_name = unit_name
        if not prop_name.endswith('s'):
            prop_name += 's' if not prop_name.endswith('y') else ''
            if prop_name.endswith('ys'):
                prop_name = prop_name[:-2] + 'ies'
        
        setter_properties.append(f'''    @property
    def {prop_name}(self) -> '{class_base}':
        self.variable.quantity = FastQuantity(self.value, {class_base}Units.{unit_name})
        return cast('{class_base}', self.variable)''')
        
        # Add alias if applicable
        notation = unit['notation']
        if notation and len(notation) <= 5 and not any(c in notation for c in ['$', '{', '}', '^', '\\', '(', ')']):
            alias = re.sub(r'[^\w]', '', notation)
            if alias and alias != unit_name and alias not in ['in']:
                setter_aliases.append(f'''    @property
    def {alias}(self) -> '{class_base}':
        return self.{prop_name}''')
    
    # Get default unit
    default_unit = 'seconds' if 'time' in title.lower() else (
        sanitize_name(units[0]['name']) + 's' if units else 'units'
    )
    
    content = f'''"""
{class_base} Variable Module
{'=' * (len(class_base) + 17)}

Type-safe {title.lower()} variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import {dimension}
from ..units import {class_base}Units
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class {class_base}Setter(TypeSafeSetter):
    """{class_base}-specific setter with only {title.lower()} units."""
    
    def __init__(self, variable: '{class_base}', value: float):
        super().__init__(variable, value)
    
    # Only {title.lower()} units available - compile-time safe!
{chr(10).join(setter_properties)}
    
    # Short aliases for convenience
{chr(10).join(setter_aliases) if setter_aliases else "    pass"}


class {class_base}(TypedVariable):
    """Type-safe {title.lower()} variable with expression capabilities."""
    
    _setter_class = {class_base}Setter
    _expected_dimension = {dimension}
    _default_unit_property = "{default_unit}"
    
    def set(self, value: float) -> {class_base}Setter:
        """Create a {title.lower()} setter for this variable with proper type annotation."""
        return {class_base}Setter(self, value)


class {class_base}Module(VariableModule):
    """{class_base} variable module definition."""
    
    def get_variable_class(self):
        return {class_base}
    
    def get_setter_class(self):
        return {class_base}Setter
    
    def get_expected_dimension(self):
        return {dimension}


# Register this module for auto-discovery
VARIABLE_MODULE = {class_base}Module()'''
    
    # Write the file
    output_path = os.path.join(output_dir, f'{file_name}.py')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_init_files(class_bases: List[str], file_names: List[str]):
    """Update __init__.py files to include new modules."""
    print(f"  Generated classes: {', '.join(class_bases)}")
    print("  Note: Please manually update __init__.py files to export these new modules")


def main():
    """Main function to generate units from data files."""
    data_dir = r'C:\Projects\qnty\data\out_tables'
    units_dir = r'C:\Projects\qnty\src\qnty\units'
    variables_dir = r'C:\Projects\qnty\src\qnty\variables'
    
    # List of data files to process
    data_files = [
        'temperature.md',
        # 'mass.md',
        # 'length.md',
        # 'pressure.md',
        # 'volume.md',
        # 'force.md',
        # 'energy_heat_work.md',
        # 'power_thermal_duty.md',
        # Add more as needed
    ]
    
    class_bases = []
    file_names = []
    
    for data_file in data_files:
        file_path = os.path.join(data_dir, data_file)
        if not os.path.exists(file_path):
            print(f"Skipping {data_file} - file not found")
            continue
        
        print(f"Processing {data_file}...")
        title, units = parse_markdown_table(file_path)
        
        if units:
            # Generate unit module
            class_base = generate_unit_module(title, units, units_dir)
            class_bases.append(class_base)
            
            # Generate variable module
            generate_variable_module(class_base, title, units, variables_dir)
            
            file_name = sanitize_name(title.replace(',', '_'))
            file_names.append(file_name)
            
            print(f"  Generated {class_base}Units and {class_base} variable")
    
    # Update __init__.py files
    if class_bases:
        print("\nUpdating __init__.py files...")
        update_init_files(class_bases, file_names)
    
    print("\nGeneration complete!")


if __name__ == '__main__':
    main()