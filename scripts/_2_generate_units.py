#!/usr/bin/env python3
"""
Script to generate a new consolidated.py with all units from parsed data.

Step 4 of the unit consolidation process: Create a comprehensive consolidated.py
file with all 810+ units organized by dimension.
"""

import json
import re
from pathlib import Path

# Configuration constants
DIMENSION_NAME_MAP = {
    'energy_heat_work': 'ENERGY',
    'force_body': 'FORCE_BODY',
    'power_thermal_duty': 'POWER',
    'absorbed_dose': 'ABSORBED_DOSE',
    'activation_energy': 'ACTIVATION_ENERGY',
    'amount_of_substance': 'AMOUNT_OF_SUBSTANCE',
    'angle_plane': 'PLANE_ANGLE',
    'angle_solid': 'SOLID_ANGLE',
    'angular_acceleration': 'ANGULAR_ACCELERATION',
    'angular_momentum': 'ANGULAR_MOMENTUM',
    'area_per_unit_volume': 'AREA_PER_UNIT_VOLUME',
    'atomic_weight': 'ATOMIC_WEIGHT',
    'electric_field_strength': 'ELECTRIC_FIELD_STRENGTH',
    'electrical_conductance': 'ELECTRICAL_CONDUCTANCE',
    'electrical_permittivity': 'ELECTRICAL_PERMITTIVITY',
    'electrical_resistivity': 'ELECTRICAL_RESISTIVITY',
    'energy_flux': 'ENERGY_FLUX',
    'energy_per_unit_area': 'ENERGY_PER_UNIT_AREA',
    'force_per_unit_mass': 'FORCE_PER_UNIT_MASS',
    'frequency_voltage_ratio': 'FREQUENCY_VOLTAGE_RATIO',
    'fuel_consumption': 'FUEL_CONSUMPTION',
    'heat_of_combustion': 'HEAT_OF_COMBUSTION',
    'heat_of_fusion': 'HEAT_OF_FUSION',
    'heat_of_vaporization': 'HEAT_OF_VAPORIZATION',
    'heat_transfer_coefficient': 'HEAT_TRANSFER_COEFFICIENT',
    'kinetic_energy_of_turbulence': 'KINETIC_ENERGY_OF_TURBULENCE',
    'linear_mass_density': 'LINEAR_MASS_DENSITY',
    'linear_momentum': 'LINEAR_MOMENTUM',
    'luminance_self': 'LUMINANCE',
    'luminous_flux': 'LUMINOUS_FLUX',
    'luminous_intensity': 'LUMINOUS_INTENSITY',
    'magnetic_field': 'MAGNETIC_FIELD_STRENGTH',
    'magnetic_flux': 'MAGNETIC_FLUX',
    'magnetic_induction_field_strength': 'MAGNETIC_FLUX_DENSITY',
    'magnetic_moment': 'MAGNETIC_DIPOLE_MOMENT',
    'magnetic_permeability': 'PERMEABILITY',
    'magnetomotive_force': 'MAGNETOMOTIVE_FORCE',
    'mass_density': 'DENSITY',
    'mass_flow_rate': 'MASS_FLOW_RATE',
    'mass_flux': 'MASS_FLUX',
    'mass_fraction_of_i': 'MASS_FRACTION',
    'mass_transfer_coefficient': 'MASS_TRANSFER_COEFFICIENT',
    'molality_of_solute_i': 'MOLALITY',
    'molar_concentration_by_mass': 'MOLAR_CONCENTRATION_BY_MASS',
    'molar_flow_rate': 'MOLAR_FLOW_RATE',
    'molar_flux': 'MOLAR_FLUX',
    'molar_heat_capacity': 'MOLAR_HEAT_CAPACITY',
    'molarity_of_i': 'MOLARITY',
    'mole_fraction_of_i': 'MOLE_FRACTION',
    'moment_of_inertia': 'MOMENT_OF_INERTIA',
    'momentum_flow_rate': 'MOMENTUM_FLOW_RATE',
    'momentum_flux': 'MOMENTUM_FLUX',
    'normality_of_solution': 'NORMALITY',
    'particle_density': 'PARTICLE_DENSITY',
    'photon_emission_rate': 'PHOTON_EMISSION_RATE',
    'power_per_unit_mass': 'POWER_PER_UNIT_MASS',
    'power_per_unit_volume': 'POWER_PER_UNIT_VOLUME',
    'radiation_dose_equivalent': 'DOSE_EQUIVALENT',
    'radiation_exposure': 'RADIATION_EXPOSURE',
    'second_moment_of_area': 'SECOND_MOMENT_OF_AREA',
    'second_radiation_constant_planck': 'SECOND_RADIATION_CONSTANT',
    'specific_enthalpy': 'SPECIFIC_ENTHALPY',
    'specific_gravity': 'SPECIFIC_GRAVITY',
    'specific_heat_capacity_constant_pressure': 'SPECIFIC_HEAT_CAPACITY',
    'specific_length': 'SPECIFIC_LENGTH',
    'specific_surface': 'SPECIFIC_SURFACE',
    'specific_volume': 'SPECIFIC_VOLUME',
    'surface_mass_density': 'SURFACE_MASS_DENSITY',
    'surface_tension': 'SURFACE_TENSION',
    'thermal_conductivity': 'THERMAL_CONDUCTIVITY',
    'turbulence_energy_dissipation_rate': 'TURBULENCE_ENERGY_DISSIPATION_RATE',
    'velocity_angular': 'ANGULAR_VELOCITY',
    'velocity_linear': 'VELOCITY',
    'viscosity_dynamic': 'DYNAMIC_VISCOSITY',
    'viscosity_kinematic': 'KINEMATIC_VISCOSITY',
    'volume_fraction_of_i': 'VOLUME_FRACTION',
    'volumetric_calorific_heating_value': 'VOLUMETRIC_CALORIFIC_HEATING_VALUE',
    'volumetric_coefficient_of_expansion': 'VOLUMETRIC_COEFFICIENT_OF_EXPANSION',
    'volumetric_flow_rate': 'VOLUMETRIC_FLOW_RATE',
    'volumetric_flux': 'VOLUMETRIC_FLUX',
    'volumetric_mass_flow_rate': 'VOLUMETRIC_MASS_FLOW_RATE',
}


def load_json_data(file_path: Path) -> dict:
    """Load JSON data from file."""
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def save_text_file(content: str, file_path: Path) -> None:
    """Save text content to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def sanitize_python_name(name: str) -> str:
    """Convert name to valid Python identifier."""
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Ensure it doesn't start with a number
    if sanitized[0].isdigit():
        sanitized = '_' + sanitized
    
    # Remove double underscores and trailing underscores
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    
    return sanitized


def get_dimension_constant_name(field_name: str) -> str:
    """Get the dimension constant name for a field."""
    return DIMENSION_NAME_MAP.get(field_name, field_name.upper())


def group_units_by_dimension(parsed_data: dict) -> dict[str, list]:
    """Each field gets its own entry - no grouping by dimension signature.
    This preserves all fields like absorbed_dose, acceleration, etc."""
    groups = {}
    
    for field_name, field_data in parsed_data.items():
        if not field_data['units']:
            continue
        
        # Each field gets its own entry
        field_info = {
            'field_name': field_name,
            'field_display': field_data['field'],
            'dimensions': field_data['dimensions'],
            'dimension_constant': get_dimension_constant_name(field_name),
            'units': field_data['units']
        }
        
        # Use field name as the key to preserve all fields
        groups[field_name] = [field_info]
    
    return groups


def generate_unit_definition(unit_data: dict) -> dict:
    """Generate a unit definition dictionary."""
    # Extract aliases from notation and other sources
    aliases = set(unit_data.get('aliases', []))
    
    # Add symbol as alias if different from name
    if unit_data.get('notation'):
        notation = unit_data['notation']
        # Clean notation for alias
        clean_notation = re.sub(r'\$.*?\$', '', notation)  # Remove LaTeX
        clean_notation = re.sub(r'[^\w\s/\-\.]', '', clean_notation)  # Keep basic chars
        clean_notation = clean_notation.strip()
        if clean_notation and clean_notation != unit_data['name']:
            aliases.add(clean_notation)
    
    return {
        "name": unit_data['normalized_name'],
        "symbol": unit_data.get('si_metric', {}).get('unit', unit_data.get('notation', '')),
        "si_factor": unit_data.get('si_metric', {}).get('conversion_factor', 1.0),
        "aliases": list(aliases),
        "full_name": unit_data['name'],
        "notation": unit_data.get('notation', ''),
        "english_us": unit_data.get('english_us', {}),
    }


def escape_string(s: str) -> str:
    """Escape both backslashes and quotes in string fields."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def generate_file_header(parsed_data: dict, grouped_units: dict, dimension_constants: set[str]) -> list[str]:
    """Generate the file header with imports and documentation."""
    # Create explicit dimension imports instead of star import
    dimension_imports = sorted(dimension_constants)
    import_lines = []
    
    # Break into multiple lines if there are many imports
    if len(dimension_imports) > 10:
        import_lines.append('from .dimension import (')
        for i, dim in enumerate(dimension_imports):
            if i == len(dimension_imports) - 1:
                import_lines.append(f'    {dim}')  # No comma on last import
            else:
                import_lines.append(f'    {dim},')
        import_lines.append(')')
    else:
        imports_str = ', '.join(dimension_imports)
        import_lines.append(f'from .dimension import {imports_str}')
    
    header_lines = [
        '"""',
        'Comprehensive Consolidated Units Module',
        '=======================================',
        '',
        'Auto-generated consolidated unit definitions for all engineering units.',
        f'Contains {sum(len(field_data["units"]) for field_data in parsed_data.values())} units',
        f'across {len(parsed_data)} fields organized into {len(grouped_units)} dimensional groups.',
        '',
        'Generated from the complete NIST unit tables and engineering references.',
        '"""',
        '',
    ]
    
    header_lines.extend(import_lines)
    header_lines.extend([
        '',
        '# Comprehensive unit definitions organized by dimensional signature',
        'UNIT_DEFINITIONS = {',
        ''
    ])
    
    return header_lines


def generate_dimension_comment(field_info: dict) -> str:
    """Generate a descriptive comment for a dimension field."""
    comment = f"# {field_info['field_display']}"
    dims = field_info['dimensions']
    
    if dims:
        dim_parts = []
        for dim_name, power in sorted(dims.items()):
            if power == 1:
                dim_parts.append(dim_name.upper())
            else:
                dim_parts.append(f"{dim_name.upper()}^{power}")
        comment += f" - {' '.join(dim_parts)}"
    else:
        comment += " - Dimensionless"
    
    return comment


def get_dimension_constant(field_info: dict, dimension_mapping: dict) -> str:
    """Get the dimension constant name for a field."""
    dims = field_info['dimensions']
    semantic_name = field_info['field_name']
    
    if not dims:
        return "DIMENSIONLESS"
    
    # Use the dimension constant from the field's mapping
    if semantic_name in dimension_mapping:
        return dimension_mapping[semantic_name]['constant_name']
    else:
        # Fallback to generated constant name
        return semantic_name.upper()


def generate_unit_entries(field_list: list) -> list[str]:
    """Generate unit entry lines for a field list."""
    lines = []
    
    # Collect all units from all fields in this dimension
    all_units = []
    for field_info in field_list:
        for unit_data in field_info['units']:
            unit_def = generate_unit_definition(unit_data)
            all_units.append(unit_def)
    
    # Sort units by name for consistency
    all_units.sort(key=lambda x: x['name'])
    
    # Remove duplicates (same name)
    seen_names = set()
    unique_units = []
    for unit in all_units:
        if unit['name'] not in seen_names:
            unique_units.append(unit)
            seen_names.add(unit['name'])
    
    # Generate unit entries
    for j, unit_def in enumerate(unique_units):
        comma = ',' if j < len(unique_units) - 1 else ''
        
        lines.extend([
            '            {',
            f'                "name": "{escape_string(unit_def["name"])}",',
            f'                "symbol": "{escape_string(unit_def["symbol"])}",',
            f'                "si_factor": {unit_def["si_factor"]},',
            f'                "full_name": "{escape_string(unit_def["full_name"])}",',
            f'                "notation": "{escape_string(unit_def["notation"])}",',
            f'                "aliases": {unit_def["aliases"]},',
            f'            }}{comma}',
        ])
    
    return lines


def generate_unit_definitions_section(grouped_units: dict, dimension_mapping: dict) -> list[str]:
    """Generate the UNIT_DEFINITIONS section."""
    lines = []
    
    for i, (_, field_list) in enumerate(sorted(grouped_units.items())):
        field_info = field_list[0]
        semantic_name = field_info['field_name']
        
        # Create descriptive comment
        comment = generate_dimension_comment(field_info)
        
        # Determine dimension constant
        dimension_const = get_dimension_constant(field_info, dimension_mapping)
        
        lines.append(f'    "{semantic_name}": {{')
        lines.append(f'        {comment}')
        lines.append(f'        "dimension": {dimension_const},')
        lines.append('        "units": [')
        
        # Generate unit entries
        unit_lines = generate_unit_entries(field_list)
        lines.extend(unit_lines)
        
        lines.append('        ],')
        lines.append('        "aliases": {}')
        
        # Close this dimension group
        comma = ',' if i < len(grouped_units) - 1 else ''
        lines.append(f'    }}{comma}')
        lines.append('')
    
    return lines


def generate_helper_functions() -> list[str]:
    """Generate helper functions for unit class creation and registration."""
    return [
        '',
        'def create_unit_class(class_name: str, dimension_data: dict) -> type:',
        '    """Dynamically create a unit class with all unit constants as attributes."""',
        '    from .unit import UnitConstant, UnitDefinition',
        '    ',
        '    # Create a new class dynamically',
        '    unit_class = type(class_name, (), {})',
        '    ',
        '    # Get the dimension',
        '    dimension = dimension_data["dimension"]',
        '    ',
        '    # Create UnitDefinition and UnitConstant for each unit',
        '    for unit_data in dimension_data["units"]:',
        '        unit_def = UnitDefinition(',
        '            name=unit_data["name"],',
        '            symbol=unit_data["symbol"],',
        '            dimension=dimension,',
        '            si_factor=unit_data["si_factor"],',
        '            si_offset=0.0',
        '        )',
        '        unit_constant = UnitConstant(unit_def)',
        '        ',
        '        # Set as class attribute',
        '        setattr(unit_class, unit_data["name"], unit_constant)',
        '        ',
        '        # Add aliases',
        '        for alias in unit_data.get("aliases", []):',
        '            if alias and not hasattr(unit_class, alias):',
        '                setattr(unit_class, alias, unit_constant)',
        '    ',
        '    return unit_class',
        '',
        '',
        'def register_all_units(registry):',
        '    """Register all unit definitions to the given registry."""',
        '    from .unit import UnitDefinition',
        '    ',
        '    for dimension_data in UNIT_DEFINITIONS.values():',
        '        dimension = dimension_data["dimension"]',
        '        ',
        '        for unit_data in dimension_data["units"]:',
        '            unit_def = UnitDefinition(',
        '                name=unit_data["name"],',
        '                symbol=unit_data["symbol"],',
        '                dimension=dimension,',
        '                si_factor=unit_data["si_factor"],',
        '                si_offset=0.0',
        '            )',
        '            ',
        '            if unit_def.name not in registry.units:',
        '                registry.register_unit(unit_def)',
        '',
        ''
    ]


def generate_unit_classes(grouped_units: dict) -> list[str]:
    """Generate unit class definitions."""
    lines = ['# Create unit classes dynamically for ALL dimensions']
    
    for field_list in grouped_units.values():
        for field_info in field_list:
            field_name = field_info['field_name']
            # Convert field name to class name (e.g., "energy_heat_work" -> "EnergyHeatWorkUnits")
            class_name = ''.join(word.capitalize() for word in field_name.split('_')) + 'Units'
            lines.append(f'{class_name} = create_unit_class("{class_name}", UNIT_DEFINITIONS["{field_name}"])')
    
    return lines


def generate_compatibility_section(parsed_data: dict, grouped_units: dict) -> list[str]:
    """Generate backward compatibility section."""
    return [
        '',
        '# Create standalone DimensionlessUnits class for backward compatibility',
        'class DimensionlessUnits:',
        '    """Standalone dimensionless units class."""',
        '    from .unit import UnitConstant, UnitDefinition',
        '    ',
        '    # Standard dimensionless unit',
        '    dimensionless_def = UnitDefinition(',
        '        name="dimensionless",',
        '        symbol="",',
        '        dimension=DIMENSIONLESS,',
        '        si_factor=1.0,',
        '        si_offset=0.0',
        '    )',
        '    dimensionless = UnitConstant(dimensionless_def)',
        '',
        '',
        '# Module-level function for compatibility with existing code',
        'def get_consolidated_modules():',
        '    """Return a list of module-like objects for consolidated units."""',
        '    class ConsolidatedModule:',
        '        """Mock module object for compatibility with existing registration system."""',
        '        ',
        '        def __init__(self, dimension_type: str):',
        '            self.dimension_type = dimension_type',
        '            self.dimension_data = UNIT_DEFINITIONS[dimension_type]',
        '        ',
        '        def register_to_registry(self, registry):',
        '            """Register units for this dimension to the registry."""',
        '            from .unit import UnitDefinition',
        '            dimension = self.dimension_data["dimension"]',
        '            ',
        '            for unit_data in self.dimension_data["units"]:',
        '                unit_def = UnitDefinition(',
        '                    name=unit_data["name"],',
        '                    symbol=unit_data["symbol"],',
        '                    dimension=dimension,',
        '                    si_factor=unit_data["si_factor"],',
        '                    si_offset=unit_data.get("si_offset", 0.0)',
        '                )',
        '                ',
        '                if unit_def.name not in registry.units:',
        '                    registry.register_unit(unit_def)',
        '    ',
        '    return [',
        '        ConsolidatedModule(dimension_name) for dimension_name in UNIT_DEFINITIONS',
        '    ]',
        '',
        '',
        '# Statistics',
        f'TOTAL_UNITS = {sum(len(field_data["units"]) for field_data in parsed_data.values())}',
        f'TOTAL_FIELDS = {len(parsed_data)}',
        f'TOTAL_DIMENSIONS = {len(grouped_units)}',
    ]


def generate_consolidated_file(parsed_data: dict, dimension_mapping: dict) -> str:
    """Generate the complete consolidated.py file content."""
    # Group units by dimension
    grouped_units = group_units_by_dimension(parsed_data)
    
    # Collect all dimension constants used in the file
    dimension_constants = set()
    for field_list in grouped_units.values():
        for field_info in field_list:
            dim_constant = get_dimension_constant(field_info, dimension_mapping)
            dimension_constants.add(dim_constant)
    
    # Build the complete file using helper functions
    lines = []
    lines.extend(generate_file_header(parsed_data, grouped_units, dimension_constants))
    lines.extend(generate_unit_definitions_section(grouped_units, dimension_mapping))
    lines.append('}')
    lines.append('')
    lines.extend(generate_helper_functions())
    lines.extend(generate_unit_classes(grouped_units))
    lines.extend(generate_compatibility_section(parsed_data, grouped_units))
    
    return '\n'.join(lines) + '\n'


def main():
    """Main function to generate consolidated.py"""
    # Setup paths using pathlib
    base_path = Path(__file__).parent.parent
    scripts_input_path = Path(__file__).parent / "input"
    scripts_output_path = Path(__file__).parent / "output"
    src_path = base_path / "src" / "qnty"
    
    parsed_file = scripts_input_path / "parsed_units.json"
    dimension_file = scripts_output_path / "dimension_mapping.json"
    output_file = src_path / "units.py"
    
    # Load data
    parsed_data = load_json_data(parsed_file)
    dimension_mapping = load_json_data(dimension_file)
    
    print(f"Loaded {len(parsed_data)} fields with units")
    print(f"Loaded {len(dimension_mapping)} dimension mappings")
    
    # Generate the consolidated file
    print("\nGenerating comprehensive consolidated.py...")
    content = generate_consolidated_file(parsed_data, dimension_mapping)
    
    # Write the file
    save_text_file(content, output_file)
    print(f"Generated units file: {output_file}")
    
    # Statistics
    total_units = sum(len(field_data['units']) for field_data in parsed_data.values())
    grouped_units = group_units_by_dimension(parsed_data)
    
    print("\nStatistics:")
    print(f"  Total units: {total_units}")
    print(f"  Total fields: {len(parsed_data)}")
    print(f"  Dimensional groups: {len(grouped_units)}")
    
    print("\nTop dimensional groups by unit count:")
    group_counts = [(len([u for f in fields for u in f['units']]), dim_key, fields)
                   for dim_key, fields in grouped_units.items()]
    group_counts.sort(reverse=True)
    
    for count, dim_key, fields in group_counts[:10]:
        field_names = [f['field_display'] for f in fields]
        print(f"  {dim_key:30s}: {count:3d} units ({', '.join(field_names[:2])}{'...' if len(field_names) > 2 else ''})")


if __name__ == "__main__":
    main()
