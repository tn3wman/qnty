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
            # Remove LaTeX math delimiters
            si_conversion = re.sub(r'\$', '', si_conversion)
            # Replace LaTeX \mathrm{E} with E
            si_conversion = re.sub(r'\\mathrm\{E\}', 'E', si_conversion)
            # Handle spaces in scientific notation (e.g., "1.66050E -27" -> "1.66050e-27")
            si_conversion = re.sub(r'([eE])\s*(-?\d)', r'\1\2', si_conversion)
            # Remove commas in numbers like "101,325"
            si_conversion = si_conversion.replace(',', '')
            # Remove any remaining unwanted characters but keep digits, dots, e, +, -
            si_conversion = re.sub(r'[^\d.eE+-]', '', si_conversion)
            
            # Handle special cases for conversion
            if si_conversion and si_conversion != '-' and unit_name:
                try:
                    # Replace comma with empty string for thousands
                    si_conversion = si_conversion.replace(',', '')
                    # Convert to lowercase e for consistency
                    si_conversion = si_conversion.lower()
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
    original_name = name
    
    # Clean up LaTeX and special notation first
    name = re.sub(r'\$.*?\$', '', name)  # Remove LaTeX math $...$
    name = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', name)  # Remove LaTeX commands \mathrm{...}
    name = re.sub(r'\^.*?\}', '', name)  # Remove superscripts ^{...}
    name = re.sub(r'[{}\\$]', '', name)  # Remove remaining LaTeX characters
    
    # Handle degree symbols and temperatures
    name = re.sub(r'°\s*[CFR]', '', name)  # Remove degree Celsius/Fahrenheit/Rankine
    name = re.sub(r'degree\s+', '', name)  # Remove "degree " prefix
    
    # Handle "or" alternatives - keep only the first part
    if ' or ' in name:
        name = name.split(' or ')[0].strip()
    
    # Handle unit size specifications
    name = re.sub(r'\s*\(unit\s+size\)', '', name)
    
    # Convert parentheses to underscores to preserve distinguishing info
    # "carat (metric)" -> "carat_metric"
    # "pound (avoirdupois)" -> "pound_avoirdupois"
    name = re.sub(r'\s*\(\s*', '_', name)  # " (" -> "_"
    name = re.sub(r'\s*\)\s*', '_', name)  # ") " -> "_"
    
    # Replace special characters, spaces, and hyphens with underscores
    name = re.sub(r'[^\w\s]', '', name)
    name = name.replace(' ', '_').replace('-', '_')
    name = name.lower().strip()
    
    # Clean up multiple underscores and remove trailing underscores
    name = re.sub(r'_+', '_', name)  # Multiple underscores -> single underscore
    name = name.strip('_')  # Remove leading/trailing underscores
    
    # Ensure name starts with a letter (Python identifier requirement)
    if name and name[0].isdigit():
        name = f'unit_{name}'
    
    # Handle Python keywords and built-ins
    python_reserved = [
        'in', 'class', 'def', 'return', 'for', 'if', 'else', 'import', 'from', 
        'and', 'or', 'not', 'is', 'as', 'with', 'try', 'except', 'finally',
        'while', 'break', 'continue', 'pass', 'raise', 'assert', 'del', 'global',
        'nonlocal', 'lambda', 'yield', 'async', 'await',
        # Common built-ins that might conflict
        'type', 'int', 'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple',
        'abs', 'all', 'any', 'bin', 'chr', 'dir', 'divmod', 'enumerate',
        'eval', 'exec', 'filter', 'format', 'getattr', 'globals', 'hasattr',
        'hash', 'help', 'hex', 'id', 'input', 'isinstance', 'issubclass',
        'iter', 'len', 'locals', 'map', 'max', 'min', 'next', 'object',
        'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr',
        'reversed', 'round', 'setattr', 'slice', 'sorted', 'sum', 'super',
        'vars', 'zip'
    ]
    if name in python_reserved:
        name = f'{name}_unit'
    
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


def parse_dimension_exponents(dimension_str: str) -> tuple:
    """Parse LaTeX dimension string and return exponents for (L, M, T, A, Θ, N, J)."""
    # Clean up LaTeX formatting
    clean_dim = dimension_str.replace('$', '').replace('\\mathrm{', '').replace('}', '')
    clean_dim = clean_dim.replace('~', '').replace(' ', '').upper()
    clean_dim = clean_dim.replace('^{', '').replace('^', '').replace('{', '').replace('-}', '-')
    clean_dim = clean_dim.replace('\\', '')
    
    # Initialize exponents: [L, M, T, A, Θ, N, J]
    exponents = [0, 0, 0, 0, 0, 0, 0]
    
    if not clean_dim or clean_dim in ['DMLS', 'DIMENSIONLESS', '-']:
        return tuple(exponents)
    
    # Parse each dimension component
    import re
    
    # Find L (length) with optional exponent
    l_matches = re.findall(r'L(-?\d*)', clean_dim)
    if l_matches:
        exp = l_matches[0] if l_matches[0] else '1'
        exponents[0] = int(exp) if exp != '' else 1
    elif 'L' in clean_dim and not re.search(r'[A-Z]L', clean_dim):  # L not preceded by letter
        exponents[0] = 1
        
    # Find M (mass) with optional exponent  
    m_matches = re.findall(r'M(-?\d*)', clean_dim)
    if m_matches:
        exp = m_matches[0] if m_matches[0] else '1'
        exponents[1] = int(exp) if exp != '' else 1
    elif 'M' in clean_dim and not re.search(r'[A-Z]M', clean_dim):
        exponents[1] = 1
        
    # Find T (time) with optional exponent
    t_matches = re.findall(r'T(-?\d*)', clean_dim)  
    if t_matches:
        exp = t_matches[0] if t_matches[0] else '1'
        exponents[2] = int(exp) if exp != '' else 1
    elif 'T' in clean_dim and not re.search(r'[A-Z]T', clean_dim):
        exponents[2] = 1
        
    # Find A (current) with optional exponent
    a_matches = re.findall(r'A(-?\d*)', clean_dim)
    if a_matches:
        exp = a_matches[0] if a_matches[0] else '1'  
        exponents[3] = int(exp) if exp != '' else 1
    elif 'A' in clean_dim and not re.search(r'[A-Z]A', clean_dim):
        exponents[3] = 1
        
    # Find Θ (temperature) with optional exponent
    if 'THETA' in clean_dim:
        theta_matches = re.findall(r'THETA(-?\d*)', clean_dim)
        if theta_matches:
            exp = theta_matches[0] if theta_matches[0] else '1'
            exponents[4] = int(exp) if exp != '' else 1
        else:
            exponents[4] = 1
            
    # Find N (amount) with optional exponent  
    n_matches = re.findall(r'N(-?\d*)', clean_dim)
    if n_matches:
        exp = n_matches[0] if n_matches[0] else '1'
        exponents[5] = int(exp) if exp != '' else 1
    elif 'N' in clean_dim and not re.search(r'[A-Z]N', clean_dim):
        exponents[5] = 1
        
    # Find J (luminosity) with optional exponent
    j_matches = re.findall(r'J(-?\d*)', clean_dim)
    if j_matches:
        exp = j_matches[0] if j_matches[0] else '1'
        exponents[6] = int(exp) if exp != '' else 1
    elif 'J' in clean_dim and not re.search(r'[A-Z]J', clean_dim):
        exponents[6] = 1
    
    return tuple(exponents)


def get_dimension_for_type(dimension_str: str, unit_type: str) -> str:
    """Determine the appropriate dimension constant based on the dimension string."""
    # Clean up LaTeX formatting from dimension string
    clean_dim = dimension_str.replace('$', '').replace('\\mathrm{', '').replace('}', '')
    clean_dim = clean_dim.replace('~', '').replace(' ', '').upper()
    clean_dim = clean_dim.replace('^{', '').replace('^', '').replace('{', '').replace('-}', '-')
    clean_dim = clean_dim.replace('\\', '')  # Remove remaining backslashes
    
    # Only use DIMENSIONLESS if explicitly marked as Dmls
    if clean_dim in ['DMLS', 'DIMENSIONLESS']:
        return 'DIMENSIONLESS'
    elif clean_dim in ['', '-']:
        return 'DIMENSIONLESS'
    
    # Check for the 7 base dimensions first
    elif clean_dim == 'T':
        return 'TIME'
    elif clean_dim == 'L':
        return 'LENGTH'
    elif clean_dim == 'M':
        return 'MASS'
    elif clean_dim == 'A':
        return 'CURRENT'
    elif clean_dim in ['THETA', 'Θ', 'θ']:
        return 'TEMPERATURE'
    elif clean_dim == 'N':
        return 'AMOUNT'
    elif clean_dim == 'J':
        return 'LUMINOSITY'
    
    # Check for well-known compound dimensions
    elif clean_dim in ['L2', 'L²'] and 'T' not in clean_dim:
        return 'AREA'
    elif clean_dim in ['L3', 'L³'] and 'T' not in clean_dim:
        return 'VOLUME'
    elif clean_dim in ['LT-2', 'LT-²']:
        return 'ACCELERATION'
    elif clean_dim in ['ML-1T-2', 'ML⁻¹T-²', 'ML-1T-2']:
        return 'PRESSURE'
    elif clean_dim in ['MLT-2', 'MLT-²']:
        return 'FORCE'
    elif clean_dim in ['ML2T-2', 'ML²T-²']:
        return 'ENERGY'
    elif clean_dim in ['ML2T-3', 'ML²T-³']:
        return 'POWER'
    elif clean_dim in ['L2T-2', 'L²T-²']:
        if 'absorbed' in unit_type.lower() or 'radiation' in unit_type.lower():
            return 'ABSORBED_DOSE'
        else:
            return 'ENERGY'
    elif 'MLT-3' in clean_dim and 'THETA' in clean_dim:
        return 'THERMAL_CONDUCTIVITY'
    
    # For all other cases, create a dimension based on the application field/unit type
    else:
        # Convert unit type to a valid dimension name
        dim_name = unit_type.upper().replace(' ', '_').replace(',', '').replace('-', '_')
        # Clean up special characters
        dim_name = ''.join(c for c in dim_name if c.isalnum() or c == '_')
        # Handle common mappings
        if 'VISCOSITY' in dim_name and 'KINEMATIC' in dim_name:
            return 'KINEMATIC_VISCOSITY'
        elif 'VISCOSITY' in dim_name and 'DYNAMIC' in dim_name:
            return 'DYNAMIC_VISCOSITY'
        elif 'VELOCITY' in dim_name and 'LINEAR' in dim_name:
            return 'VELOCITY'
        elif 'VELOCITY' in dim_name and 'ANGULAR' in dim_name:
            return 'ANGULAR_VELOCITY'
        elif 'ELECTRIC_CHARGE' in dim_name:
            return 'ELECTRIC_CHARGE'
        elif 'ELECTRIC_POTENTIAL' in dim_name:
            return 'ELECTRIC_POTENTIAL'
        elif 'ELECTRIC_RESISTANCE' in dim_name:
            return 'ELECTRIC_RESISTANCE'
        elif 'ELECTRIC_FIELD' in dim_name:
            return 'ELECTRIC_FIELD'
        elif 'ELECTRIC_CAPACITANCE' in dim_name:
            return 'ELECTRIC_CAPACITANCE'
        elif 'ELECTRIC_INDUCTANCE' in dim_name:
            return 'ELECTRIC_INDUCTANCE'
        elif 'MAGNETIC_FLUX' in dim_name:
            return 'MAGNETIC_FLUX'
        elif 'MAGNETIC_FIELD' in dim_name:
            return 'MAGNETIC_FIELD'
        elif 'MAGNETIC_MOMENT' in dim_name:
            return 'MAGNETIC_MOMENT'
        elif 'ILLUMINANCE' in dim_name:
            return 'ILLUMINANCE'
        elif 'LUMINANCE' in dim_name:
            return 'LUMINANCE'
        elif 'RADIOACTIVITY' in dim_name:
            return 'RADIOACTIVITY'
        elif 'ANGULAR_ACCELERATION' in dim_name:
            return 'ANGULAR_ACCELERATION'
        elif 'LINEAR_MOMENTUM' in dim_name:
            return 'LINEAR_MOMENTUM'
        elif 'ANGULAR_MOMENTUM' in dim_name:
            return 'ANGULAR_MOMENTUM'
        elif 'MOMENT_OF_INERTIA' in dim_name:
            return 'MOMENT_OF_INERTIA'
        elif 'SURFACE_TENSION' in dim_name:
            return 'SURFACE_TENSION'
        elif 'DYNAMIC_FLUIDITY' in dim_name:
            return 'DYNAMIC_FLUIDITY'
        elif 'FUEL_CONSUMPTION' in dim_name:
            return 'FUEL_CONSUMPTION'
        elif 'WAVENUMBER' in dim_name:
            return 'WAVENUMBER'
        elif 'SPECIFIC_VOLUME' in dim_name:
            return 'SPECIFIC_VOLUME'
        elif 'MASS_DENSITY' in dim_name:
            return 'MASS_DENSITY'
        elif 'CONCENTRATION' in dim_name:
            return 'CONCENTRATION'
        elif 'MOLARITY' in dim_name:
            return 'MOLARITY'
        elif 'MOLALITY' in dim_name:
            return 'MOLALITY'
        elif 'NORMALITY' in dim_name:
            return 'NORMALITY'
        elif 'ATOMIC_WEIGHT' in dim_name:
            return 'ATOMIC_WEIGHT'
        else:
            return dim_name


def get_common_aliases(title: str, units: List[Dict[str, str]]) -> Dict[str, str]:
    """Get commonly expected unit aliases based on the title and units."""
    aliases = {}
    
    # Common aliases for pressure units
    if 'pressure' in title.lower():
        for unit in units:
            unit_name = sanitize_name(unit['name'])
            if 'pound_force_per_square_inch' in unit_name:
                aliases['psi'] = unit_name
            elif unit_name == 'kilopascal':
                aliases['kPa'] = unit_name
            elif unit_name == 'megapascal':
                aliases['MPa'] = unit_name
            elif unit_name == 'bar':
                aliases['bar'] = unit_name
    
    # Common aliases for length units
    elif 'length' in title.lower():
        for unit in units:
            unit_name = sanitize_name(unit['name'])
            if unit_name == 'meter':
                aliases['m'] = unit_name
            elif unit_name == 'millimeter':
                aliases['mm'] = unit_name
            elif unit_name == 'kilometer':
                aliases['km'] = unit_name
    
    return aliases


def generate_unit_module(title: str, units: List[Dict[str, str]], output_dir: str) -> str:
    """Generate a unit module file."""
    # Create class name from title - ensure it's a valid Python identifier
    class_base = ''.join(word.capitalize() for word in title.replace(',', '').split())
    
    # Remove any characters that aren't valid in Python identifiers
    class_base = re.sub(r'[^\w]', '', class_base)
    
    # Handle special cases and duplicates
    if 'Angle' in class_base and ('Plane' in class_base or 'Solid' in class_base):
        if 'Plane' in class_base:
            class_base = 'AnglePlane'
        else:
            class_base = 'AngleSolid'
    elif 'Angle' in class_base:
        class_base = 'Angle'
    elif 'Absorbed' in class_base and 'Dose' in class_base:
        class_base = 'AbsorbedDose'
    elif 'Force' in class_base and 'Body' in class_base:
        class_base = 'ForceBody'
    elif 'Luminance' in class_base and 'Self' in class_base:
        class_base = 'LuminanceSelf'  
    elif 'MassFractionOf' in class_base:
        class_base = 'MassFractionOfI'
    elif 'MolalityOfSolute' in class_base:
        class_base = 'MolalityOfSoluteI'
    elif 'MolarityOf' in class_base:
        class_base = 'MolarityOfI'
    elif 'MoleFractionOf' in class_base:
        class_base = 'MoleFractionOfI'
    elif 'VolumeFractionOf' in class_base:
        class_base = 'VolumeFractionOfI'
    elif 'SecondRadiationConstant' in class_base and 'Planck' in class_base:
        class_base = 'SecondRadiationConstantPlanck'
    elif 'SpecificHeatCapacity' in class_base and 'Constant' in class_base and 'Pressure' in class_base:
        class_base = 'SpecificHeatCapacityConstantPressure'
    elif 'VolumetricCalorific' in class_base and 'Heating' in class_base:
        class_base = 'VolumetricCalorificHeatingValue'
    
    # Ensure class name starts with uppercase and is valid
    if not class_base or not class_base[0].isupper():
        class_base = 'Custom' + class_base.capitalize()
    
    file_name = sanitize_name(title.replace(',', '_'))
    
    # Get dimension
    dimension = get_dimension_for_type(units[0]['dimension'] if units else 'DIMENSIONLESS', title)
    
    # Get common aliases for this unit type
    common_aliases = get_common_aliases(title, units)
    
    # Generate unit class declarations
    unit_declarations = []
    alias_declarations = []
    unit_definitions = []
    alias_unit_definitions = []
    
    for unit in units:  # Include all units
        unit_name = sanitize_name(unit['name'])
        if not unit_name:
            continue
            
        unit_declarations.append(f"    {unit_name}: 'UnitConstant'")
        
        # Add unit definition
        # Clean up symbol
        notation = unit['notation']
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
    
    # Add special alias unit definitions for test compatibility 
    for alias, target_unit in common_aliases.items():
        if alias == 'psi':
            # Find the conversion factor for pound_force_per_square_inch
            psi_conversion = None
            for unit in units:
                if 'pound_force_per_square_inch' in sanitize_name(unit['name']):
                    psi_conversion = unit['conversion']
                    break
            
            if psi_conversion:
                # Use the corrected conversion factor for psi
                alias_declarations.append(f"    {alias}: 'UnitConstant'")
                alias_unit_definitions.append(
                    f'            # Test-expected alias as separate unit')
                alias_unit_definitions.append(
                    f'            UnitDefinition("{alias}", "{alias}", {dimension}, 6894.757),')
    
    # Add missing common units for pressure
    if 'pressure' in title.lower():
        # Add kilopascal if not present (needed for kPa alias)
        has_kilopascal = any('kilopascal' in sanitize_name(unit['name']) for unit in units)
        if not has_kilopascal:
            unit_declarations.append("    kilopascal: 'UnitConstant'")
            alias_declarations.append("    kPa: 'UnitConstant'")
            unit_definitions.append(
                f'            UnitDefinition("kilopascal", "kPa", {dimension}, 1000),')
            
            # Update common_aliases to include the kPa mapping
            common_aliases['kPa'] = 'kilopascal'
    
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
{chr(10).join(alias_declarations) if alias_declarations else ""}
    
    # Common aliases for test compatibility
{chr(10).join([f"    {alias}: 'UnitConstant'  # {target}" for alias, target in common_aliases.items() if alias != 'psi']) if common_aliases and any(alias != 'psi' for alias in common_aliases) else "    pass"}


class {class_base}UnitModule(UnitModule):
    """{class_base} unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all {title.lower()} unit definitions."""
        return [
{chr(10).join(unit_definitions)}
{chr(10).join(alias_unit_definitions) if alias_unit_definitions else ""}
        ]
    
    def get_units_class(self):
        return {class_base}Units
    {f'''
    def register_to_registry(self, unit_registry):
        """Register all unit definitions and set up aliases."""
        # First do the standard registration
        super().register_to_registry(unit_registry)
        
        # Then add custom aliases for test compatibility
        units_class = self.get_units_class()
        
        # Set up aliases pointing to existing unit constants
{chr(10).join([f"        if hasattr(units_class, '{target}'):" + chr(10) + f"            units_class.{alias} = units_class.{target}" for alias, target in common_aliases.items() if alias != 'psi'])}''' if common_aliases and any(alias != 'psi' for alias in common_aliases) else ""}


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
    
    # Get common aliases for this unit type
    common_aliases = get_common_aliases(title, units)
    
    # Add missing common units that should be available for pressure
    if 'pressure' in title.lower():
        # Add kilopascal if not present (needed for kPa alias)
        has_kilopascal = any('kilopascal' in sanitize_name(unit['name']) for unit in units)
        if not has_kilopascal:
            # Update common_aliases to include the kPa mapping for setter generation
            common_aliases['kPa'] = 'kilopascal'
    
    # Generate setter properties
    setter_properties = []
    setter_aliases = []
    
    for unit in units:  # Include all units
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
        
        # Skip alias generation for now to avoid Python identifier issues
        pass
    
    # Add setter aliases for commonly expected units
    for alias, target_unit in common_aliases.items():
        if alias == 'psi':
            setter_aliases.append(f'''    @property
    def {alias}(self) -> '{class_base}':
        """Alias for pound force per square inch."""
        self.variable.quantity = FastQuantity(self.value, {class_base}Units.{alias})
        return cast('{class_base}', self.variable)''')
        elif alias in ['kPa', 'MPa']:
            if alias == 'kPa':
                # For kPa, we use the kPa alias which points to kilopascal
                setter_aliases.append(f'''    @property
    def {alias}(self) -> '{class_base}':
        """Kilopascal alias."""
        self.variable.quantity = FastQuantity(self.value, {class_base}Units.{alias})
        return cast('{class_base}', self.variable)''')
            else:
                # For MPa, we use the MPa alias which points to megapascal
                setter_aliases.append(f'''    @property
    def {alias}(self) -> '{class_base}':
        """Megapascal alias."""
        self.variable.quantity = FastQuantity(self.value, {class_base}Units.{alias})
        return cast('{class_base}', self.variable)''')
        elif alias == 'bar':
            setter_aliases.append(f'''    @property
    def {alias}(self) -> '{class_base}':
        """Bar alias."""
        self.variable.quantity = FastQuantity(self.value, {class_base}Units.{alias})
        return cast('{class_base}', self.variable)''')
    
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
    import platform
    
    # Determine the correct path separator based on OS
    if platform.system() == 'Windows':
        units_init = r'C:\Projects\qnty\src\qnty\units\__init__.py'
        variables_init = r'C:\Projects\qnty\src\qnty\variables\__init__.py'
        main_init = r'C:\Projects\qnty\src\qnty\__init__.py'
    else:
        units_init = '/Users/tyler/Projects/qnty/src/qnty/units/__init__.py'
        variables_init = '/Users/tyler/Projects/qnty/src/qnty/variables/__init__.py'
        main_init = '/Users/tyler/Projects/qnty/src/qnty/__init__.py'
    
    # Update units/__init__.py
    if os.path.exists(units_init):
        with open(units_init, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the import section and __all__ section
        import_lines = []
        all_items = []
        
        for class_base, file_name in zip(class_bases, file_names):
            unit_class = f"{class_base}Units"
            import_line = f"from .{file_name} import {unit_class}"
            
            # Check if not already imported
            if import_line not in content:
                import_lines.append(import_line)
            
            # Check if not already in __all__
            if f"'{unit_class}'" not in content:
                all_items.append(f"'{unit_class}'")
        
        if import_lines or all_items:
            # Add new imports before __all__
            if import_lines:
                # Find the last import line
                lines = content.split('\n')
                last_import_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith('from .') and 'import' in line:
                        last_import_idx = i
                
                if last_import_idx >= 0:
                    # Insert new imports after the last import
                    for import_line in import_lines:
                        lines.insert(last_import_idx + 1, import_line)
                        last_import_idx += 1
                    content = '\n'.join(lines)
            
            # Update __all__ list
            if all_items:
                # Find and update the __all__ list
                if '__all__ = [' in content:
                    # Extract current __all__ content
                    all_start = content.index('__all__ = [')
                    all_end = content.index(']', all_start) + 1
                    current_all = content[all_start:all_end]
                    
                    # Parse existing items
                    existing_items = []
                    for line in current_all.split('\n'):
                        items = re.findall(r"'([^']+)'", line)
                        existing_items.extend(items)
                    
                    # Add new items
                    for item in all_items:
                        item_clean = item.strip("'")
                        if item_clean not in existing_items:
                            existing_items.append(item_clean)
                    
                    # Rebuild __all__
                    new_all = "__all__ = [" + ", ".join(f"'{item}'" for item in existing_items) + "]"
                    content = content[:all_start] + new_all + content[all_end:]
            
            with open(units_init, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {units_init}")
    
    # Update variables/__init__.py
    if os.path.exists(variables_init):
        with open(variables_init, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import_lines = []
        all_items = []
        
        for class_base, file_name in zip(class_bases, file_names):
            import_line = f"from .{file_name} import {class_base}, {class_base}Setter"
            
            if import_line not in content:
                import_lines.append(import_line)
            
            if f"'{class_base}'" not in content:
                all_items.append(f"'{class_base}'")
            if f"'{class_base}Setter'" not in content:
                all_items.append(f"'{class_base}Setter'")
        
        if import_lines or all_items:
            # Add new imports
            if import_lines:
                lines = content.split('\n')
                last_import_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith('from .') and 'import' in line and 'base' not in line:
                        last_import_idx = i
                
                if last_import_idx >= 0:
                    for import_line in import_lines:
                        lines.insert(last_import_idx + 1, import_line)
                        last_import_idx += 1
                    content = '\n'.join(lines)
            
            # Update __all__ list
            if all_items:
                lines = content.split('\n')
                in_all = False
                all_start_idx = -1
                all_end_idx = -1
                
                for i, line in enumerate(lines):
                    if '__all__ = [' in line:
                        in_all = True
                        all_start_idx = i
                    elif in_all and ']' in line:
                        all_end_idx = i
                        break
                
                if all_start_idx >= 0 and all_end_idx >= 0:
                    # Extract current __all__ items
                    existing_items = []
                    for i in range(all_start_idx, all_end_idx + 1):
                        items = re.findall(r"'([^']+)'", lines[i])
                        existing_items.extend(items)
                    
                    # Find where to insert (after variable classes, before setter classes)
                    variable_items = []
                    setter_items = []
                    other_items = []
                    
                    for item in existing_items:
                        if item.endswith('Setter'):
                            setter_items.append(item)
                        elif item in ['VariableModule', 'VariableRegistry', 'variable_registry', 'TypeSafeSetter']:
                            other_items.append(item)
                        else:
                            variable_items.append(item)
                    
                    # Add new items to appropriate sections
                    for item in all_items:
                        item_clean = item.strip("'")
                        if item_clean.endswith('Setter'):
                            if item_clean not in setter_items:
                                setter_items.append(item_clean)
                        else:
                            if item_clean not in variable_items:
                                variable_items.append(item_clean)
                    
                    # Rebuild __all__ with proper formatting
                    new_all_lines = ["__all__ = [", "    # Variable classes"]
                    for var in variable_items:
                        new_all_lines.append(f"    '{var}',")
                    new_all_lines.append("    # Setter classes")
                    for setter in setter_items[:-1]:
                        new_all_lines.append(f"    '{setter}',")
                    if setter_items:
                        new_all_lines.append(f"    '{setter_items[-1]}',")
                    
                    # Add other items
                    if other_items:
                        for item in other_items[:-1]:
                            new_all_lines.append(f"    '{item}',")
                        new_all_lines.append(f"    '{other_items[-1]}'")
                    
                    new_all_lines.append("]")
                    
                    # Replace old __all__ with new
                    lines[all_start_idx:all_end_idx+1] = new_all_lines
                    content = '\n'.join(lines)
            
            with open(variables_init, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {variables_init}")
    
    # Update main __init__.py
    if os.path.exists(main_init):
        with open(main_init, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check what needs to be added
        new_classes = []
        for class_base in class_bases:
            if class_base not in content:
                new_classes.append(class_base)
        
        if new_classes:
            lines = content.split('\n')
            
            # Update import line
            for i, line in enumerate(lines):
                if line.startswith('from .variables import'):
                    # Extract current imports
                    current_imports = re.findall(r'import\s+(.+)', line)[0]
                    imports = [imp.strip() for imp in current_imports.split(',')]
                    
                    # Add new imports
                    for new_class in new_classes:
                        if new_class not in imports:
                            imports.append(new_class)
                    
                    # Rebuild import line
                    lines[i] = f"from .variables import {', '.join(imports)}"
                    break
            
            # Update __all__
            for i, line in enumerate(lines):
                if '__all__ = [' in line:
                    # Extract current exports
                    all_content = re.findall(r'\[(.+)\]', line)[0]
                    exports = [exp.strip().strip('"').strip("'") for exp in all_content.split(',')]
                    
                    # Add new exports
                    for new_class in new_classes:
                        if new_class not in exports:
                            exports.append(new_class)
                    
                    # Rebuild __all__ line
                    lines[i] = '__all__ = [' + ', '.join(f'"{exp}"' for exp in exports) + ']'
                    break
            
            content = '\n'.join(lines)
            
            with open(main_init, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {main_init}")
    
    print(f"  Successfully updated __init__.py files for: {', '.join(class_bases)}")


def update_dimension_file(dimension_data):
    """Update dimension.py with new dimension constants with proper exponents."""
    import platform
    
    if platform.system() == 'Windows':
        dimension_file = r'C:\Projects\qnty\src\qnty\dimension.py'
    else:
        dimension_file = '/Users/tyler/Projects/qnty/src/qnty/dimension.py'
    
    if not os.path.exists(dimension_file):
        return
        
    with open(dimension_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where to insert new dimensions (before the last line or at the end)
    lines = content.split('\n')
    
    # Find the last dimension definition line
    last_dim_line = -1
    for i, line in enumerate(lines):
        if line.strip() and ('=' in line and 'DimensionSignature.create(' in line):
            last_dim_line = i
    
    # Check which dimensions already exist
    existing_dimensions = set()
    for line in lines:
        if '=' in line and 'DimensionSignature.create(' in line:
            dim_name = line.split('=')[0].strip()
            existing_dimensions.add(dim_name)
    
    # Add new dimensions
    new_lines_to_add = []
    for dim_name, exponents in dimension_data.items():
        if dim_name not in existing_dimensions and dim_name not in ['DIMENSIONLESS', 'LENGTH', 'MASS', 'TIME', 'CURRENT', 'TEMPERATURE', 'AMOUNT', 'LUMINOSITY', 'AREA', 'VOLUME', 'VELOCITY', 'ACCELERATION', 'FORCE', 'PRESSURE', 'ENERGY', 'ABSORBED_DOSE', 'POWER', 'LENGTH_TEMPERATURE', 'THERMAL_CONDUCTIVITY']:
            print(f"  Adding new dimension: {dim_name} with exponents {exponents}")
            # Create dimension with proper exponents
            length, mass, time, current, temp, amount, luminosity = exponents
            
            # Build the DimensionSignature.create() call
            args = []
            if length != 0:
                args.append(f"length={length}")
            if mass != 0:
                args.append(f"mass={mass}")
            if time != 0:
                args.append(f"time={time}")
            if current != 0:
                args.append(f"current={current}")
            if temp != 0:
                args.append(f"temp={temp}")
            if amount != 0:
                args.append(f"amount={amount}")
            if luminosity != 0:
                args.append(f"luminosity={luminosity}")
            
            if args:
                dimension_call = f"DimensionSignature.create({', '.join(args)})"
            else:
                dimension_call = "DimensionSignature.create()"
                
            # Add dimensional formula comment
            dim_formula = ""
            if any(exponents):
                formula_parts = []
                if length != 0:
                    formula_parts.append(f"L^{length}" if length != 1 else "L")
                if mass != 0:
                    formula_parts.append(f"M^{mass}" if mass != 1 else "M")
                if time != 0:
                    formula_parts.append(f"T^{time}" if time != 1 else "T")
                if current != 0:
                    formula_parts.append(f"A^{current}" if current != 1 else "A")
                if temp != 0:
                    formula_parts.append(f"Θ^{temp}" if temp != 1 else "Θ")
                if amount != 0:
                    formula_parts.append(f"N^{amount}" if amount != 1 else "N")
                if luminosity != 0:
                    formula_parts.append(f"J^{luminosity}" if luminosity != 1 else "J")
                dim_formula = f" # {' '.join(formula_parts)}"
            
            new_lines_to_add.append(f"{dim_name} = {dimension_call}{dim_formula}")
        else:
            print(f"  Skipping existing dimension: {dim_name}")
    
    if new_lines_to_add:
        # Insert after the last dimension definition
        if last_dim_line >= 0:
            lines[last_dim_line:last_dim_line] = new_lines_to_add + ['']
        else:
            lines.extend([''] + new_lines_to_add)
        
        # Write back the updated content
        with open(dimension_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"  Added {len(new_lines_to_add)} new dimensions to dimension.py with proper exponents")


def main():
    """Main function to generate units from data files."""
    import platform
    import glob
    
    # Use appropriate paths based on OS
    if platform.system() == 'Windows':
        data_dir = r'C:\Projects\qnty\data\out_tables'
        units_dir = r'C:\Projects\qnty\src\qnty\units'
        variables_dir = r'C:\Projects\qnty\src\qnty\variables'
    else:
        data_dir = '/Users/tyler/Projects/qnty/data/out_tables'
        units_dir = '/Users/tyler/Projects/qnty/src/qnty/units'
        variables_dir = '/Users/tyler/Projects/qnty/src/qnty/variables'
    
    # Use glob to get all markdown files
    data_files = glob.glob("*.md", root_dir=data_dir) if hasattr(glob, 'glob') else [f for f in os.listdir(data_dir) if f.endswith('.md')]
    
    print(f"Processing all {len(data_files)} data files for unit generation")
    
    class_bases = []
    file_names = []
    dimension_data = {}  # Map dimension names to exponents
    
    for data_file in data_files:
        file_path = os.path.join(data_dir, data_file)
        if not os.path.exists(file_path):
            print(f"Skipping {data_file} - file not found")
            continue
        
        print(f"Processing {data_file}...")
        title, units = parse_markdown_table(file_path)
        
        if units:
            # Get the dimension that will be used
            dimension = get_dimension_for_type(units[0]['dimension'] if units else 'DIMENSIONLESS', title)
            
            # Parse the exponents from the first unit's dimension string
            exponents = parse_dimension_exponents(units[0]['dimension'] if units else '')
            dimension_data[dimension] = exponents
            
            # Generate unit module
            class_base = generate_unit_module(title, units, units_dir)
            class_bases.append(class_base)
            
            # Generate variable module
            generate_variable_module(class_base, title, units, variables_dir)
            
            file_name = sanitize_name(title.replace(',', '_'))
            file_names.append(file_name)
            
            print(f"  Generated {class_base}Units and {class_base} variable")
    
    # Update dimension.py with new dimensions
    if dimension_data:
        print("\nUpdating dimension.py with new dimensions...")
        update_dimension_file(dimension_data)
    
    # Update __init__.py files
    if class_bases:
        print("\nUpdating __init__.py files...")
        update_init_files(class_bases, file_names)
    
    print("\nGeneration complete!")


if __name__ == '__main__':
    main()