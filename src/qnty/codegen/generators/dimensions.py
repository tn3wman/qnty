#!/usr/bin/env python3
"""
Script to validate and update dimension.py with all discovered dimensions.

Step 3 of the unit consolidation process: Ensure all dimensions from the parsed
units are defined in dimension.py and add any missing ones.
"""

import json
import re
from pathlib import Path

# Configuration constants
BASE_DIMENSIONS = [
    ('DIMENSIONLESS', {}),
    ('AMOUNT', {'amount': 1}),
    ('CURRENT', {'current': 1}),
    ('LENGTH', {'length': 1}),
    ('LUMINOSITY', {'luminosity': 1}),
    ('MASS', {'mass': 1}),
    ('TEMPERATURE', {'temp': 1}),
    ('TIME', {'time': 1}),
]


DIMENSION_SYMBOLS = {
    'length': 'L',
    'mass': 'M',
    'time': 'T',
    'current': 'A',
    'temp': 'Θ',
    'amount': 'N',
    'luminosity': 'J',
}


def load_json_data(file_path: Path) -> dict:
    """Load JSON data from file."""
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


def save_json_data(data: dict, file_path: Path) -> None:
    """Save data to JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def save_text_file(content: str, file_path: Path) -> None:
    """Save text content to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def calculate_signature_value(dims: dict[str, int]) -> int | float:
    """Calculate the actual signature value for a dimension specification."""
    if not dims:
        return 1  # Dimensionless
    
    # Prime number mapping for base dimensions
    prime_map = {
        'length': 2,
        'mass': 3,
        'time': 5,
        'current': 7,
        'temp': 11,
        'amount': 13,
        'luminosity': 17,
        'luminous_intensity': 17,  # Map to luminosity
    }
    
    signature = 1
    for dim_name, power in dims.items():
        if power != 0:
            if dim_name == 'luminous_intensity':
                dim_name = 'luminosity'
            if dim_name in prime_map:
                signature *= prime_map[dim_name] ** power
    
    return signature

def format_dimension_signature(dims: dict[str, int], use_optimized: bool = False) -> str:
    """Format dimension dictionary as DimensionSignature constructor."""
    if not dims:
        # Special case for dimensionless - use its own prime number
        return "DimensionSignature(BaseDimension.DIMENSIONLESS)"
    
    if use_optimized:
        # Use pre-computed signature value for better performance
        signature_value = calculate_signature_value(dims)
        return f"DimensionSignature({signature_value})"
    else:
        # Use create() method to ensure exact compatibility with tests
        params = []
        for dim_name, power in sorted(dims.items()):
            if power != 0:
                # Map luminous_intensity to luminosity to match BaseDimension enum
                if dim_name == 'luminous_intensity':
                    dim_name = 'luminosity'
                params.append(f"{dim_name}={power}")
        
        return f"DimensionSignature.create({', '.join(params)})"


def create_dimension_comment(dims: dict[str, int]) -> str:
    """Create a descriptive comment for a dimension specification."""
    if not dims:
        return "  # Dimensionless"
    
    dim_parts = []
    for base_dim, power in sorted(dims.items()):
        if power != 0:
            if base_dim == 'luminous_intensity':
                base_dim = 'luminosity'
            symbol = DIMENSION_SYMBOLS.get(base_dim, base_dim[0].upper())
            
            if power == 1:
                dim_parts.append(symbol)
            else:
                dim_parts.append(f"{symbol}^{power}")
    
    return f"  # {' '.join(dim_parts)}" if dim_parts else "  # Dimensionless"


def extract_dimensions_from_parsed_data(parsed_data: dict) -> dict[str, dict[str, int]]:
    """Extract all unique dimensions from parsed data."""
    return {field_name.upper(): field_data['dimensions']
            for field_name, field_data in parsed_data.items()}


def read_existing_dimensions(file_path: Path) -> set[str]:
    """Read existing dimension definitions from dimension.py file."""
    if not file_path.exists():
        return set()
    
    content = file_path.read_text(encoding='utf-8')
    dimension_pattern = r'^([A-Z_]+)\s*=\s*DimensionSignature\.create\('
    return {match.group(1) for match in re.finditer(dimension_pattern, content, re.MULTILINE)}



def generate_file_header() -> list[str]:
    """Generate the optimized header for dimension.py with performance improvements."""
    return [
        '"""',
        'Dimension System',
        '================',
        '',
        'Compile-time dimensional analysis using type system for ultra-fast operations.',
        '"""',
        '',
        'from dataclasses import dataclass',
        'from enum import IntEnum',
        'from typing import ClassVar, final',
        '',
        '',
        'class BaseDimension(IntEnum):',
        '    """Base dimensions as prime numbers for efficient bit operations."""',
        '    LENGTH = 2',
        '    MASS = 3',
        '    TIME = 5',
        '    CURRENT = 7',
        '    TEMPERATURE = 11',
        '    AMOUNT = 13',
        '    LUMINOSITY = 17',
        '    DIMENSIONLESS = 1  # Must be 1 to act as multiplicative identity',
        '',
        '',
        '@final',
        '@dataclass(frozen=True, slots=True)',
        'class DimensionSignature:',
        '    """Immutable dimension signature for zero-cost dimensional analysis."""',
        '    ',
        '    # Store as bit pattern for ultra-fast comparison',
        '    _signature: int | float = 1',
        '    ',
        '    # Pre-computed signature cache for common dimensions (expanded for better hit rate)',
        '    _COMMON_SIGNATURES: ClassVar[dict[tuple[int, ...], int | float]] = {',
        '        # Base dimensions',
        '        (1, 0, 0, 0, 0, 0, 0): 2,     # LENGTH',
        '        (0, 1, 0, 0, 0, 0, 0): 3,     # MASS',
        '        (0, 0, 1, 0, 0, 0, 0): 5,     # TIME',
        '        (0, 0, 0, 1, 0, 0, 0): 7,     # CURRENT',
        '        (0, 0, 0, 0, 1, 0, 0): 11,    # TEMPERATURE',
        '        (0, 0, 0, 0, 0, 1, 0): 13,    # AMOUNT',
        '        (0, 0, 0, 0, 0, 0, 1): 17,    # LUMINOSITY',
        '        # Common compound dimensions',
        '        (2, 0, 0, 0, 0, 0, 0): 4,     # AREA (L^2)',
        '        (3, 0, 0, 0, 0, 0, 0): 8,     # VOLUME (L^3)',
        '        (1, 1, -2, 0, 0, 0, 0): 0.24, # FORCE (L M T^-2)',
        '        (-1, 1, -2, 0, 0, 0, 0): 0.06, # PRESSURE (L^-1 M T^-2) - CORRECTED',
        '        (1, 0, -1, 0, 0, 0, 0): 0.4,   # VELOCITY (L T^-1)',
        '        (1, 0, -2, 0, 0, 0, 0): 0.08,  # ACCELERATION (L T^-2)',
        '        # Additional common patterns for better cache hit rate',
        '        (4, 0, 0, 0, 0, 0, 0): 16,    # L^4 (second moment of area)',
        '        (-3, 1, 0, 0, 0, 0, 0): 0.375, # L^-3 M (mass density)',
        '        (-2, 1, 0, 0, 0, 0, 0): 0.75,  # L^-2 M (surface mass density)',
        '        (-1, 1, 0, 0, 0, 0, 0): 1.5,   # L^-1 M (linear mass density)',
        '        (1, 1, -1, 0, 0, 0, 0): 1.2,   # L M T^-1 (linear momentum)',
        '        (2, 1, -2, 0, 0, 0, 0): 0.48,  # L^2 M T^-2 (energy)',
        '        (0, 1, -1, 0, 0, 0, 0): 0.6,   # M T^-1 (mass flow rate)',
        '        (0, 1, -2, 0, 0, 0, 0): 0.12,  # M T^-2 (energy per unit area)',
        '        (0, 0, -1, 0, 0, 0, 0): 0.2,   # T^-1 (frequency)',
        '        (-2, 0, 0, 0, 0, 0, 0): 0.25,  # L^-2 (fuel consumption)',
        '        (-1, 0, 0, 0, 0, 0, 0): 0.5,   # L^-1 (wavenumber)',
        '    }',
        '    ',
        '    # Instance cache for interning common dimensions (memory optimization)',
        '    _INSTANCE_CACHE: ClassVar[dict[int | float, "DimensionSignature"]] = {}',
        '    ',
        '    def __new__(cls, signature: int | float = 1):',
        '        """Optimized constructor with instance interning for common signatures."""',
        '        # Fast path: check if we already have this exact instance (interning)',
        '        if signature in cls._INSTANCE_CACHE:',
        '            return cls._INSTANCE_CACHE[signature]',
        '        ',
        '        # Create new instance using object.__new__ for dataclass compatibility',
        '        instance = object.__new__(cls)',
        '        ',
        '        # Intern common signatures to save memory and improve equality checks',
        '        signature_list = [1, 2, 3, 4, 5, 7, 8, 11, 13, 16, 17, 0.06, 0.08, 0.12, 0.2, 0.24, 0.25, 0.375, 0.4, 0.48, 0.5, 0.6, 0.75, 1.2, 1.5]',
        '        if signature in signature_list:',
        '            cls._INSTANCE_CACHE[signature] = instance',
        '        ',
        '        return instance',
        '    ',
        '    @classmethod',
        '    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):',
        '        """Create dimension from exponents with optimized lookup."""',
        '        # Ultra-fast path: check cache first',
        '        key = (length, mass, time, current, temp, amount, luminosity)',
        '        if key in cls._COMMON_SIGNATURES:',
        '            return cls(cls._COMMON_SIGNATURES[key])  # Uses __new__ interning',
        '        ',
        '        # Fast path: avoid computation for zero case',
        '        if not any([length, mass, time, current, temp, amount, luminosity]):',
        '            return cls(1)  # Dimensionless',
        '        ',
        '        # Optimized computation path (reduced function calls)',
        '        signature = 1',
        '        if length != 0:',
        '            signature *= BaseDimension.LENGTH ** length',
        '        if mass != 0:',
        '            signature *= BaseDimension.MASS ** mass',
        '        if time != 0:',
        '            signature *= BaseDimension.TIME ** time',
        '        if current != 0:',
        '            signature *= BaseDimension.CURRENT ** current',
        '        if temp != 0:',
        '            signature *= BaseDimension.TEMPERATURE ** temp',
        '        if amount != 0:',
        '            signature *= BaseDimension.AMOUNT ** amount',
        '        if luminosity != 0:',
        '            signature *= BaseDimension.LUMINOSITY ** luminosity',
        '        ',
        '        return cls(signature)',
        '    ',
        '    def __mul__(self, other):',
        '        """Optimized multiplication with fast paths for common cases."""',
        '        result_sig = self._signature * other._signature',
        '        return DimensionSignature(result_sig)',
        '    ',
        '    def __truediv__(self, other):',
        '        """Optimized division with fast paths."""', 
        '        result_sig = self._signature / other._signature',
        '        return DimensionSignature(result_sig)',
        '    ',
        '    def __pow__(self, power):',
        '        """Optimized power operation."""',
        '        if power == 1:',
        '            return self  # No computation needed',
        '        if power == 0:',
        '            return DimensionSignature(1)  # Dimensionless',
        '        return DimensionSignature(self._signature ** power)',
        '    ',
        '    def is_compatible(self, other):',
        '        """Ultra-fast dimensional compatibility check."""',
        '        return self._signature == other._signature',
        '    ',
        '    def __eq__(self, other):',
        '        """Optimized equality check with fast paths."""',
        '        # Fast path: identity check (same object)',
        '        if self is other:',
        '            return True',
        '        # Standard path: type and signature check', 
        '        return isinstance(other, DimensionSignature) and self._signature == other._signature',
        '    ',
        '    def __hash__(self):',
        '        """Optimized hash with caching for common signatures."""',
        '        # Hash is based solely on signature for consistency',
        '        return hash(self._signature)',
        '',
        '',
        '# Pre-defined dimension constants (optimized with pre-computed signatures)',
    ]


def generate_dimension_constants(all_dimensions: dict[str, dict[str, int]]) -> list[str]:
    """Generate dimension constant definitions with lazy loading for performance."""
    lines = []
    
    # Get base dimension names for filtering
    base_dimension_names = {bd[0] for bd in BASE_DIMENSIONS}
    
    # Add discovered dimensions (excluding base dimensions)
    discovered_dims = [
        (dim_name.upper(), dim_spec)
        for dim_name, dim_spec in all_dimensions.items()
        if dim_name.upper() not in base_dimension_names
    ]
    
    # Combine and sort all dimensions alphabetically
    all_dims = BASE_DIMENSIONS + discovered_dims
    all_dims.sort(key=lambda x: x[0])
    
    # Generate a lookup dictionary for pre-computed signatures
    lines.append('# Pre-computed dimension signature lookup for ultra-fast lazy loading')
    lines.append('_DIMENSION_SIGNATURES = {')
    for dim_name, dim_spec in all_dims:
        signature_value = calculate_signature_value(dim_spec) if dim_spec else 'BaseDimension.DIMENSIONLESS'
        comment = create_dimension_comment(dim_spec)
        lines.append(f'    "{dim_name}": {signature_value},  {comment}')
    lines.append('}')
    lines.append('')
    
    # Generate lazy loading cache
    lines.append('# Lazy loading cache for dimension constants (optimized for import performance)')
    lines.append('_dimension_cache: dict[str, DimensionSignature] = {}')
    lines.append('')
    
    # Define commonly used dimensions explicitly for IDE support
    # Map from desired constant names to data field names
    explicit_dimension_mapping = {
        "DIMENSIONLESS": "DIMENSIONLESS",
        "LENGTH": "LENGTH", 
        "MASS": "MASS",
        "TIME": "TIME",
        "CURRENT": "CURRENT",
        "TEMPERATURE": "TEMPERATURE",
        "AMOUNT": "AMOUNT",
        "LUMINOSITY": "LUMINOSITY", 
        "AREA": "AREA",
        "VOLUME": "VOLUME",
        "VELOCITY": "VELOCITY_LINEAR",  # Map to velocity_linear field
        "ACCELERATION": "ACCELERATION",
        "FORCE": "FORCE",
        "PRESSURE": "PRESSURE", 
        "ENERGY": "ENERGY_HEAT_WORK",  # Map to energy_heat_work field
        "ENERGY_HEAT_WORK": "ENERGY_HEAT_WORK"
    }
    
    explicitly_defined_dimensions = list(explicit_dimension_mapping.keys())
    
    # Generate module-level __getattr__ for lazy loading
    lines.append('def __getattr__(name: str) -> DimensionSignature:')
    lines.append('    """Lazy loading of dimension constants for optimal import performance."""')
    lines.append('    # Skip attributes that are explicitly defined in the module')
    lines.append('    # This prevents conflicts with explicitly defined dimension constants')
    lines.append('    if name in {')
    for dim_name in explicitly_defined_dimensions:
        lines.append(f'        "{dim_name}",')
    lines.append('    }:')
    lines.append('        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")')
    lines.append('')
    lines.append('    if name in _DIMENSION_SIGNATURES:')
    lines.append('        if name not in _dimension_cache:')
    lines.append('            _dimension_cache[name] = DimensionSignature(_DIMENSION_SIGNATURES[name])')
    lines.append('        return _dimension_cache[name]')
    lines.append('    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")')
    lines.append('')
    
    # Generate explicit dimension constant definitions
    lines.append('# Explicitly define the most commonly used dimension constants for IDE support')
    lines.append('# These are created dynamically by __getattr__, but explicit definitions help IDE autocomplete')
    
    # Define base and derived dimensions using the mapping
    for const_name, field_name in explicit_dimension_mapping.items():
        if const_name == "ENERGY_HEAT_WORK":
            continue  # Handle this separately as an alias
        
        if field_name in [bd[0] for bd in BASE_DIMENSIONS]:
            # Get spec from BASE_DIMENSIONS
            dim_spec = next(bd[1] for bd in BASE_DIMENSIONS if bd[0] == field_name)
            signature_value = calculate_signature_value(dim_spec) if dim_spec else 1
            comment = create_dimension_comment(dim_spec)
            lines.append(f'{const_name} = DimensionSignature({signature_value}){comment}')
        elif field_name in all_dimensions:
            # Get spec from all_dimensions using the mapped field name
            dim_spec = all_dimensions[field_name]
            signature_value = calculate_signature_value(dim_spec)
            comment = create_dimension_comment(dim_spec)
            lines.append(f'{const_name} = DimensionSignature({signature_value}){comment}')
    
    # Add aliases
    lines.append('')
    lines.append('# Common aliases for backward compatibility')
    lines.append('ENERGY_HEAT_WORK = ENERGY')
    lines.append('')
    
    # Generate clean __all__ list with only explicitly defined symbols
    lines.append('# Export list for module (enables proper IDE autocomplete)')
    lines.append('# Only include explicitly defined symbols to avoid Pylance warnings')
    lines.append('# All dimension constants are still available via __getattr__ for dynamic loading')
    lines.append('__all__ = [')
    lines.append('    # Base classes')
    lines.append('    "BaseDimension",')
    lines.append('    "DimensionSignature",')
    lines.append('    # Commonly used dimensions (explicitly defined for IDE support)')
    for dim_name in explicitly_defined_dimensions:
        lines.append(f'    "{dim_name}",')
    lines.append(']')
    lines.append('')
    
    # Add explanatory note about dynamic loading
    lines.append('# Note: All other dimension constants (ABSORBED_DOSE, ELECTRIC_CHARGE, etc.)')
    lines.append('# are available via dynamic loading through __getattr__ but are not listed in __all__')
    lines.append('# to avoid IDE warnings. They can still be imported and used normally:')
    lines.append('#   from qnty.dimension import ABSORBED_DOSE  # Works fine')
    lines.append('#   import qnty.dimension as dim; dim.ABSORBED_DOSE  # Works fine')
    
    return lines


def generate_complete_dimension_file(all_dimensions: dict[str, dict[str, int]]) -> str:
    """Generate a complete new dimension.py file."""
    lines = generate_file_header()
    lines.extend(generate_dimension_constants(all_dimensions))
    return '\n'.join(lines) + '\n'  # Add newline at end of file


def create_dimension_mapping(parsed_data: dict) -> dict[str, dict]:
    """Create comprehensive dimension mapping from parsed data."""
    return {
        field_name: {
            'field': field_data['field'],
            'dimensions': field_data['dimensions'],
            'signature': format_dimension_signature(field_data['dimensions'], use_optimized=True),
            'constant_name': field_name.upper()
        }
        for field_name, field_data in parsed_data.items()
    }


def print_dimension_summary(all_dimensions: dict[str, dict[str, int]]) -> None:
    """Print a summary of dimensions grouped by signature."""
    print("\n" + "="*60)
    print("DIMENSION SUMMARY")
    print("="*60)
    
    # Group by dimension signature
    by_signature = {}
    for field_name, dims in all_dimensions.items():
        dim_key = tuple(sorted((k, v) for k, v in dims.items()))
        if dim_key not in by_signature:
            by_signature[dim_key] = []
        by_signature[dim_key].append(field_name)
    
    print(f"\nGrouped by dimension signature ({len(by_signature)} unique):")
    for dim_spec, fields in sorted(by_signature.items(), key=lambda x: len(x[1]), reverse=True):
        dim_dict = dict(dim_spec) if dim_spec else {}
        print(f"\n  {format_dimension_signature(dim_dict)}")
        print(f"    Fields ({len(fields)}): {', '.join(sorted(fields)[:5])}")
        if len(fields) > 5:
            print(f"                 ... and {len(fields)-5} more")


def main():
    """Main function to validate and update dimensions."""
    # Setup paths using pathlib
    base_path = Path(__file__).parent.parent
    src_path = base_path / "src" / "qnty"
    scripts_input_path = Path(__file__).parent / "input"
    scripts_output_path = Path(__file__).parent / "output"
    
    parsed_file = scripts_input_path / "unit_data.json"
    dimension_file = src_path / "dimension.py"
    mapping_file = scripts_output_path / "dimension_mapping.json"
    
    # Ensure output directory exists
    scripts_output_path.mkdir(parents=True, exist_ok=True)
    
    # Load and process data
    parsed_data = load_json_data(parsed_file)
    print(f"Loaded {len(parsed_data)} fields with units")
    
    # Extract and process dimensions
    all_dimensions = extract_dimensions_from_parsed_data(parsed_data)
    existing_dims = read_existing_dimensions(dimension_file)
    
    print(f"\nFound {len(all_dimensions)} unique dimensions")
    print(f"Found {len(existing_dims)} existing dimension definitions")
    
    # Find and report new dimensions
    new_dimension_names = set(all_dimensions.keys()) - existing_dims
    if new_dimension_names:
        print(f"\nNew dimensions to add: {len(new_dimension_names)}")
        for name in sorted(new_dimension_names):
            dim_spec = all_dimensions[name]
            signature = format_dimension_signature(dim_spec)
            print(f"  {name} = {signature}")
    else:
        print("\nAll dimensions already defined!")
    
    # Generate and save files
    print("\nGenerating complete dimension.py file...")
    complete_content = generate_complete_dimension_file(all_dimensions)
    save_text_file(complete_content, dimension_file)
    print(f"Complete dimension.py file saved to: {dimension_file}")
    
    # Save dimension mapping
    dimension_mapping = create_dimension_mapping(parsed_data)
    save_json_data(dimension_mapping, mapping_file)
    print(f"Dimension mapping saved to: {mapping_file}")
    
    # Print summary
    print_dimension_summary(all_dimensions)


if __name__ == "__main__":
    main()
