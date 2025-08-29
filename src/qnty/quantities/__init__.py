"""
Quantities Package with Auto-Discovery and Registration
=======================================================

Automatically discovers and registers all quantity modules, providing
a unified system for physical quantities with units, variables, and setters.
"""

import importlib
import pkgutil

# Import all classes for public API
# Import base classes for extensibility
from .base import QuantityModule, QuantityRegistry, quantity_registry
from .dimensionless import Dimensionless, DimensionlessSetter, DimensionlessUnits
from .length import Length, LengthSetter, LengthUnits
from .pressure import Pressure, PressureSetter, PressureUnits

# Auto-discover and register all quantity modules
for _importer, modname, _ispkg in pkgutil.iter_modules(__path__):
    if modname not in ['__init__', 'base']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register quantity module if it has the QUANTITY_MODULE attribute
        if hasattr(module, 'QUANTITY_MODULE'):
            quantity_module = module.QUANTITY_MODULE
            quantity_registry.register_quantity(modname.capitalize(), quantity_module)



__all__ = [
    # Variable classes
    'Length',
    'Pressure',
    'Dimensionless',
    # Setter classes
    'LengthSetter',
    'PressureSetter',
    'DimensionlessSetter',
    # Units classes
    'LengthUnits',
    'PressureUnits',
    'DimensionlessUnits',
    # Base classes for extensibility
    'QuantityModule',
    'QuantityRegistry',
    # Global registry
    'quantity_registry',
]
