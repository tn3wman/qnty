"""
Examples of how to refactor long parameter lists using parameter objects.

This module demonstrates the before/after patterns for methods that had
long parameter lists and how they can be improved with parameter objects.
"""

from .parameter_objects import VariableInitParams, DimensionCreateParams


class DimensionSignatureRefactoredExample:
    """
    Example of how DimensionSignature.create() would be refactored.
    
    BEFORE (7 parameters):
    create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0)
    
    AFTER (1 parameter object):
    create_from_params(cls, params: DimensionCreateParams)
    """
    
    @classmethod
    def create_from_params(cls, params: DimensionCreateParams) -> "DimensionSignatureRefactoredExample":
        """
        Create dimension from exponents using parameter object.
        
        Args:
            params: Dimension parameters containing all exponents
            
        Returns:
            New DimensionSignature instance
            
        Examples:
            # Simple dimensions
            length_dim = DimensionSignature.create_from_params(DimensionCreateParams.length_dimension())
            area_dim = DimensionSignature.create_from_params(DimensionCreateParams.area_dimension())
            
            # Complex dimensions
            pressure_params = DimensionCreateParams.pressure_dimension()
            pressure_dim = DimensionSignature.create_from_params(pressure_params)
            
            # Custom dimensions
            custom_params = DimensionCreateParams(length=2, mass=-1, time=3)
            custom_dim = DimensionSignature.create_from_params(custom_params)
        """
        # Check cache first using tuple conversion
        key = params.to_tuple()
        # ... rest of implementation would be similar to original
        
        # Fast path for dimensionless
        if params.is_dimensionless():
            return cls(1)
        
        # Compute signature using parameter object fields
        signature = 1
        if params.length != 0:
            signature *= 2**params.length  # BaseDimension.LENGTH
        if params.mass != 0:
            signature *= 3**params.mass    # BaseDimension.MASS
        # ... etc for other dimensions
        
        return cls(signature)
    
    # Keep original method for backward compatibility
    @classmethod  
    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):
        """Create dimension from exponents (legacy method)."""
        params = DimensionCreateParams(length, mass, time, current, temp, amount, luminosity)
        return cls.create_from_params(params)


class VariableRefactoredExample:
    """
    Example of how Variable.__init__() would be refactored.
    
    BEFORE (4 parameters):
    __init__(self, name_or_value, unit=None, name=None, is_known=True)
    
    AFTER (1 parameter object + convenience methods):
    __init__(self, params: VariableInitParams)
    """
    
    def __init__(self, params: VariableInitParams):
        """
        Initialize variable using parameter object.
        
        Args:
            params: Variable initialization parameters
            
        Examples:
            # Unknown variable
            unknown_params = VariableInitParams.from_name("pressure")
            pressure = Length(unknown_params)
            
            # Known variable with value and unit
            known_params = VariableInitParams.from_value_unit(100.0, "mm")
            length = Length(known_params)
            
            # Named variable with value
            named_params = VariableInitParams.from_name_with_value("beam_length", 10.5, "inches")
            beam = Length(named_params)
        """
        if params.unit is None and params.name is None:
            # Single argument: name only (unknown variable)
            super().__init__(params.name_or_value, is_known=params.is_known)
        elif params.unit is not None and params.name is not None:
            # Three arguments: value, unit, name (known variable)
            super().__init__(params.name_or_value, params.unit, params.name, is_known=params.is_known)
        else:
            raise ValueError("Must provide either just name (unknown) or value, unit, and name (known)")
    
    # Convenience class methods for common patterns
    @classmethod
    def unknown(cls, name: str) -> "VariableRefactoredExample":
        """Create an unknown variable with the given name."""
        params = VariableInitParams.from_name(name)
        return cls(params)
    
    @classmethod
    def known(cls, value: int | float, unit: str, name: str | None = None) -> "VariableRefactoredExample":
        """Create a known variable with value and unit."""
        params = VariableInitParams.from_value_unit(value, unit, name)
        return cls(params)
    
    # Keep original constructor for backward compatibility
    @classmethod
    def from_legacy_params(cls, name_or_value, unit=None, name=None, is_known=True) -> "VariableRefactoredExample":
        """Create variable using legacy parameter pattern."""
        params = VariableInitParams(name_or_value, unit, name, is_known)
        return cls(params)


# Usage examples showing improved readability
def usage_examples():
    """Examples showing how the parameter objects improve code readability."""
    
    # BEFORE: Hard to understand what each parameter does
    # dimension = DimensionSignature.create(1, 0, -2, 0, 0, 0, 0)  # What is this?
    # variable = SomeVariable("beam", "mm", "beam_length", True)   # Parameter confusion
    
    # AFTER: Clear intent and self-documenting
    acceleration_params = DimensionCreateParams.acceleration_dimension()
    dimension = DimensionSignatureRefactoredExample.create_from_params(acceleration_params)
    
    beam_params = VariableInitParams.from_name_with_value("beam_length", 10.5, "mm")
    variable = VariableRefactoredExample(beam_params)
    
    # Or using convenience methods
    unknown_pressure = VariableRefactoredExample.unknown("pressure")
    known_length = VariableRefactoredExample.known(25.4, "mm", "thickness")


def benefits_of_parameter_objects():
    """
    Benefits achieved by using parameter objects:
    
    1. **Readability**: Method calls become self-documenting
    2. **Maintainability**: Adding new parameters doesn't break existing calls
    3. **Type Safety**: Parameter objects can be validated
    4. **Reusability**: Parameter objects can be shared and reused
    5. **Testing**: Easier to create test fixtures with parameter objects
    6. **Factory Methods**: Enable rich factory methods for common patterns
    7. **Backward Compatibility**: Legacy methods can delegate to new ones
    
    BEFORE:
    create(length=1, mass=0, time=-2, current=0, temp=0, amount=0, luminosity=0)
    
    AFTER:  
    create_from_params(DimensionCreateParams.acceleration_dimension())
    
    The second form is much clearer about intent!
    """
    pass