"""
Variables Package with Auto-Discovery and Registration
======================================================

Automatically discovers and registers all variable modules, providing
a clean API for type-safe engineering variables.
"""

import importlib
import pkgutil

from .base import VariableRegistry

# Create global variable registry
variable_registry = VariableRegistry()

# Auto-discover and register all variable modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    if modname not in ['__init__', 'base']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register variable module if it has the VARIABLE_MODULE attribute
        if hasattr(module, 'VARIABLE_MODULE'):
            var_module = module.VARIABLE_MODULE
            var_module.register_to_registry(variable_registry)

# Import all variable classes for public API
from .dimensionless import Dimensionless, DimensionlessSetter
from .length import Length, LengthSetter
from .pressure import Pressure, PressureSetter

# Also import base classes for extensibility
from .base import VariableModule, VariableRegistry

# Import TypeSafeSetter from variable module for backward compatibility
from ..variable import TypeSafeSetter

__all__ = [
    # Variable classes
    'Length',
    'Pressure', 
    'Dimensionless',
    # Setter classes
    'LengthSetter',
    'PressureSetter',
    'DimensionlessSetter',
    'TypeSafeSetter',  # For backward compatibility
    # Base classes for extensibility
    'VariableModule',
    'VariableRegistry',
    # Global registry
    'variable_registry',
]