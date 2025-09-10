"""
Documentation Generation Helper
==============================

Shared functions for generating consistent documentation across
quantities.py and quantities.pyi files.
"""

try:
    from .data_processor import get_unit_names_and_aliases
except ImportError:
    # Handle standalone execution
    from .data_processor import get_unit_names_and_aliases


def generate_class_docstring(class_name: str, display_name: str, units: list, is_dimensionless: bool = False) -> list[str]:
    """Generate comprehensive class docstring for quantity classes."""
    # Get example units for documentation
    example_units = []
    for unit in units[:3]:  # Take first 3 units as examples
        primary_name, _ = get_unit_names_and_aliases(unit)
        example_units.append(f'"{primary_name}"')

    unit_examples = ", ".join(example_units) if example_units else '"unit"'

    lines = [
        '    """',
        f"    Type-safe {display_name} quantity with expression capabilities.",
        "    ",
    ]

    if is_dimensionless:
        lines.extend(
            [
                "    Constructor Options:",
                "    -------------------",
                f'    - {class_name}("variable_name") -> Create unknown {display_name}',
                f'    - {class_name}(value, "variable_name") -> Create known {display_name}',
                "    ",
                "    Examples:",
                "    ---------",
                f'    >>> unknown = {class_name}("efficiency")  # Unknown {display_name}',
                f'    >>> known = {class_name}(0.85, "thermal_efficiency")  # Known {display_name}',
            ]
        )
    else:
        lines.extend(
            [
                "    Constructor Options:",
                "    -------------------",
                f'    - {class_name}("variable_name") -> Create unknown {display_name}',
                f'    - {class_name}(value, "unit", "variable_name") -> Create known {display_name}',
                "    ",
                "    Examples:",
                "    ---------",
                f'    >>> unknown = {class_name}("pressure")  # Unknown {display_name}',
                f'    >>> known = {class_name}(100, {unit_examples.split(",")[0] if unit_examples else "unit"}, "inlet_pressure")  # Known {display_name}',
                "    ",
                f"    Available units: {unit_examples}",
            ]
        )

    lines.append('    """')
    return lines


def generate_init_method(class_name: str, display_name: str, is_dimensionless: bool = False, stub_only: bool = False) -> list[str]:
    """Generate __init__ method supporting both old and new constructor syntax."""
    lines = []

    if is_dimensionless:
        lines.append("    def __init__(self, name_or_value: str | int | float, name_or_unit: str | int | float | None = None):")
        if not stub_only:
            lines.extend(
                [
                    '        """',
                    f"        Initialize {display_name} quantity with flexible syntax.",
                    "        ",
                    "        Constructor Patterns:",
                    "        --------------------",
                    f"        - {class_name}(\"name\") -> Unknown {display_name}",
                    f"        - {class_name}(\"name\", value) -> Known {display_name} (NEW)",
                    f"        - {class_name}(value, \"name\") -> Known {display_name} (OLD, backward compatibility)",
                    "        ",
                    "        Args:",
                    "            name_or_value: Variable name (str) or value (int/float)",
                    "            name_or_unit: Variable name (str) or value (int/float), depending on first arg",
                    '        """',
                    "        if isinstance(name_or_value, str):",
                    "            # NEW syntax: name first",
                    "            if name_or_unit is None:",
                    "                # Unknown variable",
                    "                super().__init__(name_or_value, is_known=False)",
                    "            else:",
                    "                # Known variable",
                    "                super().__init__(name_or_unit, name_or_value, is_known=True)",
                    "        else:",
                    "            # OLD syntax: value first (backward compatibility)",
                    "            if name_or_unit is None:",
                    '                raise ValueError("Variable name required")',
                    "            super().__init__(name_or_value, name_or_unit, is_known=True)",
                    "        self.set_arithmetic_mode('expression')",
                ]
            )
        else:
            lines.append("        ...")
    else:
        lines.append("    def __init__(self, name_or_value: str | int | float, unit_or_name: str | None = None, name_or_value2: str | int | float | None = None):")
        if not stub_only:
            lines.extend(
                [
                    '        """',
                    f"        Initialize {display_name} quantity with flexible syntax.",
                    "        ",
                    "        Constructor Patterns:",
                    "        --------------------",
                    f"        - {class_name}(\"name\") -> Unknown {display_name}",
                    f"        - {class_name}(\"name\", \"unit\") -> Unknown {display_name} with unit preference (NEW)",
                    f"        - {class_name}(\"name\", \"unit\", value) -> Known {display_name} (NEW)",
                    f"        - {class_name}(value, \"unit\", \"name\") -> Known {display_name} (OLD, backward compatibility)",
                    "        ",
                    "        Args:",
                    "            name_or_value: Variable name (str) or value (int/float)",
                    "            unit_or_name: Unit string or variable name, depending on usage",
                    "            name_or_value2: Variable name (str) or value (int/float) for 3-arg patterns",
                    '        """',
                    "        if isinstance(name_or_value, str) and (name_or_value2 is None or isinstance(name_or_value2, (int, float))):",
                    "            # NEW syntax: name first",
                    "            if unit_or_name is None:",
                    "                # Pattern: Length(\"name\")",
                    "                super().__init__(name_or_value, is_known=False)",
                    "            elif name_or_value2 is None:",
                    "                # Pattern: Length(\"name\", \"unit\")",
                    "                super().__init__(name_or_value, is_known=False)",
                    "                self._set_preferred_unit(unit_or_name)",
                    "            else:",
                    "                # Pattern: Length(\"name\", \"unit\", value)",
                    "                super().__init__(name_or_value2, unit_or_name, name_or_value, is_known=True)",
                    "        elif isinstance(name_or_value, (int, float)):",
                    "            # OLD syntax: value first (backward compatibility)",
                    "            if unit_or_name is None or name_or_value2 is None:",
                    '                raise ValueError("Unit and name required for value-first syntax")',
                    "            super().__init__(name_or_value, unit_or_name, name_or_value2, is_known=True)",
                    "        else:",
                    '            raise ValueError("Invalid constructor arguments")',
                    "        self.set_arithmetic_mode('expression')",
                ]
            )
        else:
            lines.append("        ...")

    return lines


def generate_converter_stub_classes(_: dict) -> list[str]:
    """Generate converter stub classes for type hints."""
    # Use the base converter classes without specific type overrides to avoid conflicts
    return [
        "# ===== CONVERTER TYPE STUBS =====",
        "# Unit conversion handled by base ToUnitConverter and AsUnitConverter classes",
        "# with dynamic __getattr__ for unit method type hints",
        "",
    ]


def _is_valid_identifier(name: str) -> bool:
    """Check if a name is a valid Python identifier."""
    import keyword

    return name.isidentifier() and not keyword.iskeyword(name) and not name.startswith("_")


def generate_converter_methods(_: str, __: bool = False) -> list[str]:
    """Generate to_unit and as_unit property methods with proper type hints."""
    # Don't generate converter method overrides to avoid type conflicts
    # The base FieldQnty class provides these properties with proper functionality
    # and the correct generic typing that works with all specific converter classes
    return []


def generate_set_method(setter_class_name: str, display_name: str, stub_only: bool = False) -> list[str]:
    """Generate set method with comprehensive documentation."""
    if stub_only:
        lines = [
            "    @overload",
            f"    def set(self, value: float, unit: str) -> Self: ...",
            "    @overload", 
            f"    def set(self, value: float, unit: None = None) -> field_setter.{setter_class_name}: ...",
            f"    def set(self, value: float, unit: str | None = None) -> Self | field_setter.{setter_class_name}:",
        ]
    else:
        lines = [
            f"    def set(self, value: float, unit: str | None = None) -> 'Self | field_setter.{setter_class_name}':",
            '        """',
            f"        Create a setter for this {display_name} quantity.",
            "        ",
            "        Args:",
            "            value: The numeric value to set",
            "            unit: Optional unit string (for compatibility with base class)",
            "        ",
            "        Returns:",
            f"            {setter_class_name}: A setter with unit properties like .meters, .inches, etc.",
            "        ",
            "        Example:",
            '            >>> length = Length("beam_length")',
            "            >>> length.set(100).millimeters  # Sets to 100 mm",
            '        """',
        ]

    if stub_only:
        lines.append("        ...")
    else:
        lines.extend([
            "        if unit is not None:",
            "            # Direct setting with unit",
            f"            setter = field_setter.{setter_class_name}(self, value)",
            "            # Get the unit property and call it to set the value",
            "            if hasattr(setter, unit):",
            "                getattr(setter, unit)",
            "            else:",
            "                from ..utils.unit_suggestions import create_unit_validation_error",
            "                raise create_unit_validation_error(unit, self.__class__.__name__)",
            "            return self",
            "        else:",
            f"            return field_setter.{setter_class_name}(self, value)"
        ])

    return lines


def generate_value_unit_properties(display_name: str, stub_only: bool = False) -> list[str]:
    """Generate value and unit property methods for direct access."""
    lines = []
    
    # Value property
    lines.append("    @property")
    lines.append("    def value(self) -> float | None:")
    if stub_only:
        lines.append("        ...")
    else:
        lines.extend([
            '        """',
            f"        Get the numeric value of this {display_name}.",
            "        ",
            "        Returns:",
            "            The numeric value if known, None if unknown",
            "        ",
            "        Example:",
            '            >>> length = Length(100, "mm", "beam_length")',
            "            >>> length.value  # Returns 100.0",
            '        """',
            "        return self.quantity.value if self.quantity is not None else None"
        ])
    
    lines.append("")
    
    # Unit property
    lines.append("    @property")
    lines.append("    def unit(self) -> str | None:")
    if stub_only:
        lines.append("        ...")
    else:
        lines.extend([
            '        """',
            f"        Get the unit symbol of this {display_name}.",
            "        ",
            "        Returns:",
            "            The unit symbol if known, None if unknown",
            "        ",
            "        Example:",
            '            >>> length = Length(100, "mm", "beam_length")',
            '            >>> length.unit  # Returns "mm"',
            '        """',
            "        return self.quantity.unit.symbol if self.quantity is not None else None"
        ])
    
    return lines
