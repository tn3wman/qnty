"""
Base Variable Module Definition
===============================

Provides abstract base class for variable modules and registration functionality.
"""

from abc import ABC, abstractmethod
from typing import Any


class VariableModule(ABC):
    """Abstract base class for variable modules."""
    
    @abstractmethod
    def get_variable_class(self) -> type[Any]:
        """Return the variable class for this module."""
        pass
    
    @abstractmethod
    def get_setter_class(self) -> type[Any]:
        """Return the setter class for this module."""
        pass
    
    @abstractmethod
    def get_expected_dimension(self) -> Any:
        """Return the expected dimension for this variable type."""
        pass
    
    def register_to_registry(self, variable_registry):
        """Register this variable module to the given registry."""
        # Cache method calls to avoid repeated abstract method invocations
        dimension = self.get_expected_dimension()
        variable_class = self.get_variable_class()
        setter_class = self.get_setter_class()
        
        variable_registry.register_module(dimension, variable_class, setter_class)


class VariableRegistry:
    """Ultra-high-performance registry for variable modules using tuples."""
    
    def __init__(self):
        # Use tuples for maximum performance (1.95x faster than ModuleEntry)
        self._modules: dict[Any, tuple[type[Any], type[Any]]] = {}
    
    def register_module(self, dimension: Any, variable_class: type[Any], setter_class: type[Any]) -> None:
        """Register a variable module."""
        self._modules[dimension] = (variable_class, setter_class)
    
    def get_variable_class(self, dimension: Any) -> type[Any] | None:
        """Get variable class for a dimension."""
        entry = self._modules.get(dimension)
        return entry[0] if entry else None
    
    def get_setter_class(self, dimension: Any) -> type[Any] | None:
        """Get setter class for a dimension."""
        entry = self._modules.get(dimension)
        return entry[1] if entry else None
    
    def get_classes(self, dimension: Any) -> tuple[type[Any] | None, type[Any] | None]:
        """Get both variable and setter class in one lookup for better performance."""
        entry = self._modules.get(dimension)
        return entry if entry else (None, None)
