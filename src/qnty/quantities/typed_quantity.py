"""
Typed Variable Base Class
=========================

Base class that provides common constructor logic for all typed variables,
handling both the original syntax and the new value/unit/name syntax.
"""

from ..cache_manager import get_cache_manager
from ..generated.dimensions import DimensionSignature
from .expression_quantity import ExpressionQuantity
from .quantity import TypeSafeSetter


class TypedQuantity(ExpressionQuantity):
    """
    Base class for typed variables with common constructor logic.

    Subclasses need to define:
    - _setter_class: The setter class to use
    - _expected_dimension: The expected dimension
    - _default_unit_property: The default unit property name for fallback
    """

    _setter_class: type[TypeSafeSetter] | None = None
    _expected_dimension: DimensionSignature | None = None
    _default_unit_property: str | None = None

    # Pre-computed unit mappings for common units (override in subclasses for better performance)
    _unit_mappings: dict[str, str] = {}

    @classmethod
    def _find_unit_property(cls, setter: TypeSafeSetter, unit: str) -> str | None:
        """Find unit property with optimized lookup and unified caching."""
        if cls._setter_class is None:
            return None

        cache_manager = get_cache_manager()
        
        # Ultra-fast path: Check pre-computed mappings first
        if unit in cls._unit_mappings:
            return cls._unit_mappings[unit]

        # Fast path: Check unified cache
        cached_property = cache_manager.get_unit_property(cls._setter_class, unit)
        if cached_property is not None:
            return cached_property
            
        # Check validation cache to avoid redundant work
        validation_result = cache_manager.get_validation_result(cls._setter_class, unit)
        if validation_result is not None:
            if validation_result and hasattr(setter, unit):
                cache_manager.cache_unit_property(cls._setter_class, unit, unit)
                return unit
            elif not validation_result:
                return None

        # Slow path: Try all variants and cache results
        for unit_variant in [unit, unit + "s", unit[:-1] if unit.endswith("s") else None]:
            if unit_variant and hasattr(setter, unit_variant):
                cache_manager.cache_unit_property(cls._setter_class, unit, unit_variant)
                cache_manager.cache_validation_result(cls._setter_class, unit, True)
                return unit_variant

        # Cache miss - remember that this unit doesn't exist
        cache_manager.cache_unit_property(cls._setter_class, unit, None)
        cache_manager.cache_validation_result(cls._setter_class, unit, False)
        return None

    @classmethod
    def _get_available_units_error(cls, unit: str) -> str:
        """Generate helpful error message with available units."""
        if cls._setter_class is None:
            return f"Unit '{unit}' not found for {cls.__name__}. Setter class not defined."

        cache_manager = get_cache_manager()
        available_units = cache_manager.get_available_units(cls._setter_class)
        
        if available_units is None:
            # Create dummy setter to get available units
            dummy_var = object.__new__(cls)
            dummy_var._setter_class = cls._setter_class
            dummy_var._expected_dimension = cls._expected_dimension
            dummy_setter = cls._setter_class(dummy_var, 0.0)

            # Extract and cache available units
            unit_properties = [attr for attr in dir(dummy_setter) if not attr.startswith("_") and attr not in ("value", "variable")]
            available_units = sorted(unit_properties)
            cache_manager.cache_available_units(cls._setter_class, available_units)
        display_units = ", ".join(available_units[:10])
        if len(available_units) > 10:
            display_units += f" ... and {len(available_units) - 10} more"

        return f"Unit '{unit}' not found for {cls.__name__}. Available units: {display_units}"

    def __init__(self, *args, is_known: bool = True, _bypass_validation: bool = False):
        """
        Flexible constructor supporting multiple syntaxes.

        Single argument: TypedVariable("name")
        Three arguments: TypedVariable(value, "unit", "name")
        Two arguments (Dimensionless only): TypedVariable(value, "name")
        """
        if not _bypass_validation and (self._setter_class is None or self._expected_dimension is None):
            raise NotImplementedError("Subclass must define _setter_class and _expected_dimension")

        is_dimensionless = self.__class__.__name__ == "Dimensionless"

        # Handle different argument patterns
        if len(args) == 1:
            # Original syntax: Variable("name")
            super().__init__(args[0], self._expected_dimension, is_known=is_known)

        elif len(args) == 2 and is_dimensionless:
            # Special case for Dimensionless: (value, "name")
            value, name = args
            super().__init__(name, self._expected_dimension, is_known=is_known)
            if self._setter_class is not None:
                setter = self._setter_class(self, value)
                getattr(setter, "dimensionless", None)  # type: ignore

        elif len(args) == 3:
            # New syntax: Variable(value, "unit", "name")
            if is_dimensionless:
                raise ValueError(f"{self.__class__.__name__} expects either 1 argument (name) or 2 arguments (value, name), got {len(args)}")

            value, unit, name = args
            super().__init__(name, self._expected_dimension, is_known=is_known)

            # Fast path for pre-computed units
            if not _bypass_validation and unit in self._unit_mappings and self._setter_class is not None:
                setter = self._setter_class(self, value)
                getattr(setter, self._unit_mappings[unit])
            else:
                # Standard path with unit lookup
                if self._setter_class is not None:
                    setter = self._setter_class(self, value)
                    unit_prop = self._find_unit_property(setter, unit)

                    if unit_prop:
                        getattr(setter, unit_prop)
                    elif not _bypass_validation:
                        raise ValueError(self._get_available_units_error(unit))

        else:
            # Error messages
            if is_dimensionless:
                raise ValueError(f"{self.__class__.__name__} expects either 1 argument (name) or 2 arguments (value, name), got {len(args)}")
            else:
                raise ValueError(f"{self.__class__.__name__} expects either 1 argument (name) or 3 arguments (value, unit, name), got {len(args)}")

    @classmethod
    def from_value(cls, value: float, unit: str, name: str, is_known: bool = True):
        """
        Optimized factory method for creating variables with known values.
        Bypasses complex constructor logic for better performance.
        """
        instance = cls.__new__(cls)
        # Direct initialization without checks
        ExpressionQuantity.__init__(instance, name, instance._expected_dimension, is_known=is_known)

        # Fast path for setting value using shared lookup logic
        if instance._setter_class is None:
            raise NotImplementedError("Subclass must define _setter_class")

        setter = instance._setter_class(instance, value)
        unit_prop = cls._find_unit_property(setter, unit)

        if unit_prop:
            getattr(setter, unit_prop)
        else:
            raise ValueError(cls._get_available_units_error(unit))

        return instance

    @classmethod
    def create_unknown(cls, name: str):
        """Fast factory method for creating unknown variables."""
        return cls(name, is_known=False)

    @classmethod
    def create_bulk(cls, variable_specs: list[tuple[float, str, str]]) -> list:
        """Bulk creation method for multiple variables with same type."""
        if cls._setter_class is None:
            raise NotImplementedError("Subclass must define _setter_class")

        variables = []
        for value, unit, name in variable_specs:
            # Use fast path creation if possible
            if unit in cls._unit_mappings:
                var = cls._create_with_fast_unit_lookup(value, unit, name)
            else:
                var = cls.from_value(value, unit, name)
            variables.append(var)

        return variables

    @classmethod
    def _create_with_fast_unit_lookup(cls, value: float, unit: str, name: str, is_known: bool = True):
        """Ultra-fast constructor bypassing complex lookup when unit mappings are pre-computed."""
        if unit in cls._unit_mappings and cls._setter_class is not None:
            # Ultra-fast path: direct property access
            instance = cls.__new__(cls)
            ExpressionQuantity.__init__(instance, name, cls._expected_dimension, is_known=is_known)

            setter = cls._setter_class(instance, value)
            unit_prop = cls._unit_mappings[unit]
            getattr(setter, unit_prop)

            return instance
        else:
            # Fall back to standard constructor
            return cls(value, unit, name, is_known=is_known)
