"""
Units Package with Auto-Discovery and Registration
=================================================

Automatically discovers and registers all unit modules, then populates
their unit constant classes.
"""

import importlib
import pkgutil
from ..unit import registry

# Auto-discover and register all unit modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    if modname not in ['__init__', 'base']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register definitions to global registry (modules may have pre-populated some)
        if hasattr(module, 'UNIT_MODULE'):
            module.UNIT_MODULE.register_to_registry(registry)

# Finalize registry after all registrations
registry.finalize_registration()

# Export unit classes for public API
from .length import LengthUnits
from .pressure import PressureUnits  
from .dimensionless import DimensionlessUnits

__all__ = ['LengthUnits', 'PressureUnits', 'DimensionlessUnits']