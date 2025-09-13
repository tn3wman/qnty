"""
Simplified quantity definition using metaclass to reduce boilerplate while maintaining type safety.
"""
import sys
from typing import Any, TypeVar, cast, overload

from .quantity import (
    FieldQuantity,
    FieldSetter,
    UnitApplier,
    UnitChanger,
    _get_namespace_dim,
    bind_quantity_namespace,
)
from .unit import Unit, UnitNamespace

D = TypeVar("D")

class QuantityMeta(type):
    """Metaclass that automatically creates the boilerplate for quantity classes."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # Only process subclasses of FieldQuantity, not FieldQuantity itself
        if bases and any(issubclass(b, FieldQuantity) for b in bases if b != FieldQuantity):
            # Get the unit namespace from class definition
            unit_ns = namespace.get('UNIT_NS')
            if unit_ns:
                # Create setter class
                setter_cls_name = f"{name}Setter"
                setter_cls = type(setter_cls_name, (FieldSetter,), {"__slots__": ()})
                namespace['SETTER_CLS'] = setter_cls
                
                # Create ToUnit and AsUnit inner classes
                to_unit_cls = type("ToUnit", (UnitApplier,), {"__slots__": ()})
                as_unit_cls = type("AsUnit", (UnitChanger,), {"__slots__": ()})
                namespace['ToUnit'] = to_unit_cls
                namespace['AsUnit'] = as_unit_cls
                
                # Add properties if not already defined
                if 'to_unit' not in namespace:
                    def to_unit_prop(self):
                        dim = _get_namespace_dim(self.UNIT_NS)
                        return self.ToUnit(self, dim)
                    namespace['to_unit'] = property(to_unit_prop)
                
                if 'as_unit' not in namespace:
                    def as_unit_prop(self):
                        dim = _get_namespace_dim(self.UNIT_NS)
                        return self.AsUnit(self, dim)
                    namespace['as_unit'] = property(as_unit_prop)
                
                # Add set method if not already defined
                if 'set' not in namespace:
                    def set_method(self, value: float, unit: Unit | str | None = None):
                        if unit is None:
                            return self.SETTER_CLS(self, value, _get_namespace_dim(self.UNIT_NS))
                        return FieldQuantity.set(self, value, unit)
                    namespace['set'] = set_method
        
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Bind namespace after class creation
        if hasattr(cls, 'UNIT_NS') and hasattr(cls, 'SETTER_CLS'):
            # Use cast for the entire class since it has dynamic attributes
            typed_cls = cast(Any, cls)
            bind_quantity_namespace(typed_cls, typed_cls.SETTER_CLS, typed_cls.UNIT_NS)
            # Store setter in module namespace for export
            if hasattr(cls, '__module__'):
                module = sys.modules[cls.__module__]
                setattr(module, typed_cls.SETTER_CLS.__name__, typed_cls.SETTER_CLS)
        
        return cls


class TypedFieldQuantity(FieldQuantity[D], metaclass=QuantityMeta):
    """Base class for typed field quantities with automatic boilerplate generation."""
    __slots__ = ()
    
    # These will be set by metaclass
    UNIT_NS: type[UnitNamespace]
    SETTER_CLS: type[FieldSetter]
    
    class ToUnit(UnitApplier):
        __slots__ = ()
    
    class AsUnit(UnitChanger):
        __slots__ = ()
    
    @property
    def to_unit(self) -> "ToUnit":
        ...
    
    @property
    def as_unit(self) -> "AsUnit":
        ...
    
    @overload
    def set(self, value: float) -> FieldSetter[D]: ...
    @overload
    def set(self, value: float, unit: Unit[D]) -> "TypedFieldQuantity[D]": ...
    @overload
    def set(self, value: float, unit: str) -> "TypedFieldQuantity[D]": ...
    def set(self, value: float, unit: Unit[D] | str | None = None) -> "FieldSetter[D] | TypedFieldQuantity[D]":
        # Implementation will be provided by metaclass
        raise NotImplementedError("Metaclass should provide implementation")

# Even simpler with a decorator that handles everything
def quantity(unit_namespace: type[UnitNamespace]):
    """
    Decorator to create a quantity class with absolute minimal boilerplate.
    
    Usage:
        @quantity(LengthUnits)
        class Length:
            pass
    """
    def wrapper(cls):
        # Get the class name to use as the type parameter
        class_name = cls.__name__
        
        # Create a new class that inherits from TypedFieldQuantity with the right type parameter
        # We need to create a new class because we can't modify the type parameter after class creation
        new_cls = type(
            class_name,
            (TypedFieldQuantity,),  # We'll handle the type parameter differently
            {
                "__slots__": getattr(cls, "__slots__", ()),
                "UNIT_NS": unit_namespace,
                "__module__": cls.__module__,
                "__qualname__": cls.__qualname__,
                "__doc__": cls.__doc__,
            }
        )
        
        # Copy any additional attributes from the original class
        for attr_name in dir(cls):
            if not attr_name.startswith("__"):
                setattr(new_cls, attr_name, getattr(cls, attr_name))
        
        return new_cls
    return wrapper
