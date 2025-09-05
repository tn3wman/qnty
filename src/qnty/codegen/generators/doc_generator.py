"""
Documentation Generation Helper
==============================

Shared functions for generating consistent documentation across
quantities.py and quantities.pyi files.
"""

from .data_processor import get_unit_names_and_aliases


def generate_class_docstring(class_name: str, display_name: str, units: list, is_dimensionless: bool = False) -> list[str]:
    """Generate comprehensive class docstring for quantity classes."""
    # Get example units for documentation
    example_units = []
    for unit in units[:3]:  # Take first 3 units as examples
        primary_name, aliases = get_unit_names_and_aliases(unit)
        example_units.append(f'"{primary_name}"')
    
    unit_examples = ', '.join(example_units) if example_units else '"unit"'
    
    lines = [
        f'    """',
        f'    Type-safe {display_name} quantity with expression capabilities.',
        f'    ',
    ]
    
    if is_dimensionless:
        lines.extend([
            f'    Constructor Options:',
            f'    -------------------',
            f'    - {class_name}("variable_name") -> Create unknown {display_name}',
            f'    - {class_name}(value, "variable_name") -> Create known {display_name}',
            f'    ',
            f'    Examples:',
            f'    ---------',
            f'    >>> unknown = {class_name}("efficiency")  # Unknown {display_name}',
            f'    >>> known = {class_name}(0.85, "thermal_efficiency")  # Known {display_name}',
        ])
    else:
        lines.extend([
            f'    Constructor Options:',
            f'    -------------------',
            f'    - {class_name}("variable_name") -> Create unknown {display_name}',
            f'    - {class_name}(value, "unit", "variable_name") -> Create known {display_name}',
            f'    ',
            f'    Examples:',
            f'    ---------',
            f'    >>> unknown = {class_name}("pressure")  # Unknown {display_name}',
            f'    >>> known = {class_name}(100, {unit_examples.split(",")[0] if unit_examples else '"unit"'}, "inlet_pressure")  # Known {display_name}',
            f'    ',
            f'    Available units: {unit_examples}',
        ])
    
    lines.append(f'    """')
    return lines


def generate_init_method(class_name: str, display_name: str, is_dimensionless: bool = False, stub_only: bool = False) -> list[str]:
    """Generate __init__ method with proper type hints."""
    lines = []
    
    if is_dimensionless:
        lines.append(f'    def __init__(self, name_or_value: str | int | float, name: str | None = None, is_known: bool = True):')
        if not stub_only:
            lines.extend([
                f'        """',
                f'        Initialize {display_name} quantity.',
                f'        ',
                f'        Args:',
                f'            name_or_value: Variable name (str) if unknown, or value (int/float) if known',
                f'            name: Variable name (required if providing value)',
                f'            is_known: Whether the variable has a known value',
                f'        """',
                f'        if name is None:',
                f'            # Single argument: name only (unknown variable)',
                f'            super().__init__(name_or_value, is_known=is_known)',
                f'        else:',
                f'            # Two arguments: value and name (known variable)',
                f'            super().__init__(name_or_value, name, is_known=is_known)',
            ])
        else:
            lines.append(f' ...')
    else:
        lines.append(f'    def __init__(self, name_or_value: str | int | float, unit: str | None = None, name: str | None = None, is_known: bool = True):')
        if not stub_only:
            lines.extend([
                f'        """',
                f'        Initialize {display_name} quantity.',
                f'        ',
                f'        Args:',
                f'            name_or_value: Variable name (str) if unknown, or value (int/float) if known',
                f'            unit: Unit string (required if providing value)',
                f'            name: Variable name (required if providing value)',
                f'            is_known: Whether the variable has a known value',
                f'        """',
                f'        if unit is None and name is None:',
                f'            # Single argument: name only (unknown variable)',
                f'            super().__init__(name_or_value, is_known=is_known)',
                f'        elif unit is not None and name is not None:',
                f'            # Three arguments: value, unit, name (known variable)',
                f'            super().__init__(name_or_value, unit, name, is_known=is_known)',
                f'        else:',
                f'            raise ValueError("Must provide either just name (unknown) or value, unit, and name (known)")',
            ])
        else:
            lines.append(f' ...')
    
    return lines


def generate_set_method(setter_class_name: str, display_name: str, stub_only: bool = False) -> list[str]:
    """Generate set method with comprehensive documentation."""
    lines = [
        f'    def set(self, value: int | float) -> ts.{setter_class_name}:',
        f'        """',
        f'        Create a setter for this {display_name} quantity.',
        f'        ',
        f'        Args:',
        f'            value: The numeric value to set',
        f'        ',
        f'        Returns:',
        f'            {setter_class_name}: A setter with unit properties like .meters, .inches, etc.',
        f'        ',
        f'        Example:',
        f'            >>> length = Length("beam_length")',
        f'            >>> length.set(100).millimeters  # Sets to 100 mm',
        f'        """',
    ]
    
    if stub_only:
        lines.append(f'        ...')
    else:
        lines.append(f'        return ts.{setter_class_name}(self, value)')
    
    return lines