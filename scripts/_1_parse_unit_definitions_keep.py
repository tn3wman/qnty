#!/usr/bin/env python3
"""
Script to parse the combined unit definitions file and extract all unit data.

Step 2 of the unit consolidation process: Analyze and parse all unit definitions
from the combined markdown file, handling various formats and edge cases.
"""

import json
import re
from typing import Any


def normalize_field_name(field_name: str) -> str:
    """Convert field name to Python-compatible identifier."""
    # Handle special cases and clean up
    name = field_name.lower()
    
    # Remove special characters and replace with underscores
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '_', name)
    
    # Handle specific patterns
    name = name.replace('__', '_')
    name = name.strip('_')
    
    # Handle specific field name corrections
    corrections = {
        'angle_plane': 'angle_plane',
        'angle_solid': 'angle_solid',
        'power_per_unit_mass_or_specific_power': 'power_per_unit_mass',
        'power_per_unit_volume_or_power_density': 'power_per_unit_volume',
        'activiation_energy': 'activation_energy',  # Fix typo
        'absorbed_radiation_dose': 'absorbed_dose',
    }
    
    return corrections.get(name, name)


def normalize_unit_name(unit_name: str) -> str:
    """Convert unit name to Python-compatible identifier."""
    name = unit_name.lower()
    
    # Handle parentheses - extract content in parentheses as suffix
    parentheses_pattern = r'(.+?)\s*\(([^)]+)\)'
    match = re.match(parentheses_pattern, name)
    if match:
        base_name, suffix = match.groups()
        # Clean suffix
        suffix = re.sub(r'[^\w\s]', '', suffix)
        suffix = re.sub(r'\s+', '_', suffix)
        name = f"{base_name}_{suffix}".strip('_')
    
    # Clean up remaining characters
    name = re.sub(r'[^\w\s]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    # Handle specific unit name corrections
    corrections = {
        'kilogram_mol_or_kmol': 'kilogram_mol',
        'mole_gram': 'mole',
        'pound_mole': 'pound_mole',
        'lb_mol_or_mole': 'pound_mole',
    }
    
    return corrections.get(name, name)


def parse_si_dimension(si_dim_str: str) -> dict[str, int]:
    """Parse LaTeX SI dimension string into dimension components."""
    if not si_dim_str or si_dim_str.strip() in ['Dmls', 'dimensionless', '-']:
        return {}  # Dimensionless
    
    # First handle special case where exponent is separated like "T ${ }^{-2}$"
    # Combine these into a single token
    import re
    si_dim_str = re.sub(r'([LMTIKJN])\s*\$\{\s*\}\^\{([^}]+)\}\$', r'\1^\2', si_dim_str)
    si_dim_str = re.sub(r'([LMTIKJN])\s*\{\s*\}\^\{([^}]+)\}', r'\1^\2', si_dim_str)
    
    # Remove LaTeX formatting but keep the structure
    clean_dim = si_dim_str.replace('$', '').replace('\\mathrm{', '').replace('\\', '')
    clean_dim = clean_dim.replace('~', ' ')
    
    # Map LaTeX dimension symbols to our dimension names
    dimension_map = {
        'L': 'length',
        'M': 'mass',
        'T': 'time',
        'A': 'current',
        'θ': 'temp',
        'theta': 'temp',  # Text version
        '0': 'temp',  # Sometimes 0 is used instead of θ
        'N': 'amount',
        'J': 'luminous_intensity'
    }
    
    # Initialize dimensions
    dimensions = {}
    
    # Handle special compound dimension notations first
    # TAN^{-1} = Time * Ampere (current) * Amount^{-1}
    # (The exponent applies only to N, not the whole compound)
    if 'TAN' in clean_dim:
        # Extract power if present (e.g., TAN^{-1} or {TAN}^{-1})
        import re
        match = re.search(r'\{?TAN\}?\^?\{?(-?\d+)?\}?', clean_dim)
        if match:
            power_str = match.group(1)
            n_power = int(power_str) if power_str else 1
            # T and A have power 1, N has the specified power
            dimensions['time'] = 1
            dimensions['current'] = 1
            dimensions['amount'] = n_power
        else:
            # No power specified, all have power 1
            dimensions['time'] = 1
            dimensions['current'] = 1
            dimensions['amount'] = 1
        clean_dim = re.sub(r'\{?TAN\}?\^?\{?-?\d*\}?', '', clean_dim).strip()
    
    if 'TLM' in clean_dim:
        # TLM^{-1} = Time * Length * Mass^{-1}
        # (The exponent applies only to M, not the whole compound)
        import re
        match = re.search(r'\{?TLM\}?\^?\{?(-?\d+)?\}?', clean_dim)
        if match:
            power_str = match.group(1)
            m_power = int(power_str) if power_str else 1
            # T and L have power 1, M has the specified power
            dimensions['time'] = 1
            dimensions['length'] = 1
            dimensions['mass'] = m_power
        else:
            # No power specified, all have power 1
            dimensions['time'] = 1
            dimensions['length'] = 1
            dimensions['mass'] = 1
        clean_dim = re.sub(r'\{?TLM\}?\^?\{?-?\d*\}?', '', clean_dim).strip()
    
    # Split by spaces to handle compound dimensions like "ML^{-1} T^{-2}"
    parts = clean_dim.split()
    
    for part in parts:
        # Remove any remaining braces
        part = part.replace('{', '').replace('}', '')
        
        # Skip if this part was already handled as compound dimension
        if not part:
            continue
            
        # Parse compound dimensions like ML^-2 where only the last symbol gets the power
        # First, collect all dimension symbols before any power notation
        symbols_found = []
        i = 0
        while i < len(part):
            found_symbol = False
            for symbol, name in dimension_map.items():
                if part[i:].startswith(symbol):
                    symbols_found.append((symbol, name))
                    i += len(symbol)
                    found_symbol = True
                    break
            
            if not found_symbol:
                # Hit a non-dimension character (likely power notation)
                break
        
        # Now look for power notation after the dimension symbols
        power = 1  # Default power
        if i < len(part):
            if part[i] == '^':
                # Has explicit power with ^
                i += 1
                power_str = ''
                # Handle negative sign
                if i < len(part) and part[i] == '-':
                    power_str = '-'
                    i += 1
                # Collect digits
                while i < len(part) and part[i].isdigit():
                    power_str += part[i]
                    i += 1
                if power_str and power_str != '-':
                    power = int(power_str)
            elif part[i] == '-':
                # Handle case like "ML-2" (without ^)
                i += 1
                power_str = '-'
                while i < len(part) and part[i].isdigit():
                    power_str += part[i]
                    i += 1
                if power_str != '-':
                    power = int(power_str)
            elif part[i].isdigit():
                # Handle case like "ML2" (without ^ or -)
                power_str = ''
                while i < len(part) and part[i].isdigit():
                    power_str += part[i]
                    i += 1
                power = int(power_str)
        
        # Apply the power to the dimensions
        # For compound dimensions, only the LAST symbol gets the power
        for idx, (_, name) in enumerate(symbols_found):
            if idx == len(symbols_found) - 1:
                # Last symbol gets the power
                symbol_power = power
            else:
                # Earlier symbols get power 1
                symbol_power = 1
            
            # Add to dimensions
            if symbol_power != 0:
                if name in dimensions:
                    dimensions[name] += symbol_power
                else:
                    dimensions[name] = symbol_power
    
    return dimensions


def parse_conversion_factor(factor_str: str) -> float:
    """Parse conversion factor, handling scientific notation and commas."""
    if not factor_str:
        return 1.0
    
    # Clean the string - remove LaTeX formatting, commas, spaces
    clean_str = factor_str.replace('$', '').replace('\\mathrm{', '').replace('}', '')
    clean_str = clean_str.replace('\\', '').replace(',', '').replace(' ', '').strip()
    
    # Handle scientific notation like 1.00E+05, 1.0E-10, etc.
    sci_pattern = r'([0-9.]+)E([+-]?[0-9]+)'
    match = re.search(sci_pattern, clean_str, re.IGNORECASE)
    if match:
        base = float(match.group(1))
        exp = int(match.group(2))
        return base * (10 ** exp)
    
    # Handle negative numbers (like -4.19E+03)
    if clean_str.startswith('-'):
        try:
            return float(clean_str)
        except ValueError:
            pass
    
    try:
        return float(clean_str)
    except ValueError:
        print(f"Warning: Could not parse conversion factor '{factor_str}', using 1.0")
        return 1.0


def extract_aliases_from_notation(notation: str, unit_name: str) -> list[str]:
    """Extract possible aliases from the notation field."""
    aliases = []
    
    if not notation:
        return aliases
    
    # Remove LaTeX formatting
    clean_notation = notation.replace('$', '').replace('\\mathrm{', '').replace('}', '')
    clean_notation = clean_notation.replace('\\', '').strip()
    
    # Common alias patterns
    if ' or ' in clean_notation.lower():
        parts = clean_notation.split(' or ')
        aliases.extend([p.strip() for p in parts if p.strip() != unit_name])
    
    # Single letter symbols (like 'm', 'Pa', 'Hz')
    if len(clean_notation) <= 4 and clean_notation.isalpha():
        aliases.append(clean_notation)
    
    return aliases


def parse_markdown_table_row(row: str) -> tuple[str, str, str, str, str, str, str, str] | None:
    """Parse a single markdown table row."""
    if not row.strip() or '|' not in row:
        return None
    
    # Split by | and clean up
    parts = [part.strip() for part in row.split('|')]
    
    # Remove first/last empty elements if they exist
    if parts and not parts[0]:
        parts = parts[1:]
    if parts and not parts[-1]:
        parts = parts[:-1]
    
    # We expect 8 columns: field, unit_name, notation, si_dimension, si_factor, si_unit, us_factor, us_unit
    if len(parts) < 8:
        return None
        
    # Skip header rows
    if 'Application/field' in parts[0] or '---' in row or 'Conversion factor' in parts[0]:
        return None
    
    # Ensure we have exactly 8 parts, pad with empty strings if needed
    while len(parts) < 8:
        parts.append('')
    return (parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])


def parse_combined_units_file(file_path: str) -> dict[str, Any]:
    """Parse the combined units file and extract all unit definitions."""
    
    print(f"Parsing combined units file: {file_path}")
    
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections by the markdown headers
    sections = re.split(r'\n## ([^\n]+)\n', content)
    
    parsed_data = {}
    
    for i in range(1, len(sections), 2):  # Skip first empty section, then take pairs
        if i + 1 >= len(sections):
            break
            
        field_name = sections[i].strip()
        section_content = sections[i + 1]
        
        # Skip if this is not a valid field section
        if not field_name:
            continue
            
        normalized_field = normalize_field_name(field_name)
        
        print(f"Processing field: {field_name} -> {normalized_field}")
        
        # Parse the table in this section
        lines = section_content.split('\n')
        units = []
        
        for line in lines:
            row_data = parse_markdown_table_row(line)
            if not row_data:
                continue
                
            _, unit_name, notation, si_dimension, si_factor, si_unit, us_factor, us_unit = row_data
            
            # Skip empty rows or header-like rows
            if not unit_name or unit_name.lower() in ['unit name', '']:
                continue
            
            # Parse the data
            normalized_unit_name = normalize_unit_name(unit_name)
            parsed_dimensions = parse_si_dimension(si_dimension)
            parsed_si_factor = parse_conversion_factor(si_factor)
            aliases = extract_aliases_from_notation(notation, unit_name)
            
            unit_data = {
                'field': field_name,
                'name': unit_name,
                'normalized_name': normalized_unit_name,
                'notation': notation,
                'si_dimension': si_dimension,
                'parsed_dimensions': parsed_dimensions,
                'si_metric': {
                    'conversion_factor': parsed_si_factor,
                    'unit': si_unit
                },
                'english_us': {
                    'conversion_factor': parse_conversion_factor(us_factor),
                    'unit': us_unit
                },
                'aliases': aliases
            }
            
            units.append(unit_data)
            print(f"  - {unit_name} -> {normalized_unit_name} (SI factor: {parsed_si_factor})")
        
        if units:
            parsed_data[normalized_field] = {
                'field': field_name,
                'normalized_field': normalized_field,
                'units': units,
                'dimensions': units[0]['parsed_dimensions'] if units else {}
            }
    
    return parsed_data


def analyze_dimensions(parsed_data: dict[str, Any]) -> dict[str, dict[str, int]]:
    """Analyze all dimensions found in the data."""
    dimensions_found = {}
    
    for field_name, field_data in parsed_data.items():
        if field_data['dimensions']:
            dimensions_found[field_name] = field_data['dimensions']
            print(f"{field_name}: {field_data['dimensions']}")
    
    return dimensions_found


def main():
    """Main function to parse and analyze unit definitions."""
    
    combined_file = "/Users/tyler/Projects/qnty/data/combined_units.md"
    output_file = "/Users/tyler/Projects/qnty/data/parsed_units.json"
    
    # Parse the file
    parsed_data = parse_combined_units_file(combined_file)
    
    print(f"\\nParsed {len(parsed_data)} fields with units")
    
    # Analyze dimensions
    print("\nDimensions found:")
    dimensions_found = analyze_dimensions(parsed_data)
    
    # Count total units
    total_units = sum(len(field_data['units']) for field_data in parsed_data.values())
    print(f"\\nTotal units parsed: {total_units}")
    
    # Save parsed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\\nSaved parsed data to: {output_file}")
    
    # Show some statistics
    print("\nStatistics:")
    print(f"- Fields: {len(parsed_data)}")
    print(f"- Total units: {total_units}")
    print(f"- Unique dimensions: {len(dimensions_found)}")
    
    # Show fields with most units
    field_unit_counts = [(name, len(data['units'])) for name, data in parsed_data.items()]
    field_unit_counts.sort(key=lambda x: x[1], reverse=True)
    
    print("\nFields with most units:")
    for field, count in field_unit_counts[:10]:
        print(f"  {field}: {count} units")


if __name__ == "__main__":
    main()
