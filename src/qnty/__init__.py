# Import all variables from the consolidated system
from .variables import *



"""
Units Package with Auto-Discovery and Registration
=================================================

Automatically discovers and registers all unit modules, then populates
their unit constant classes.
"""

import importlib
import pkgutil

from .unit import registry
from .units import register_all_units

# Register consolidated units first
register_all_units(registry)

# Auto-discover and register remaining unit modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    # Skip consolidated units and base modules
    if modname not in ['__init__', 'base', 'consolidated', 'length', 'pressure', 'area']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register definitions to global registry (modules may have pre-populated some)
        if hasattr(module, 'UNIT_MODULE'):
            module.UNIT_MODULE.register_to_registry(registry)

# Finalize registry after all registrations
registry.finalize_registration()

"""
Variables Package with Auto-Discovery and Registration
======================================================

Automatically discovers and registers all variable modules, providing
a clean API for type-safe engineering variables.
"""

import importlib
import pkgutil

from .variable_types.base import VariableRegistry

# Create global variable registry
variable_registry = VariableRegistry()

# Note: Consolidated variables are now in parent ../variables.py
# This package contains implementation details for variable types

# Auto-discover and register remaining variable modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    # Skip consolidated modules and base
    if modname not in ['__init__', 'base', 'consolidated', 'consolidated_new', 'length', 'pressure', 'area']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register variable module if it has the VARIABLE_MODULE attribute
        if hasattr(module, 'VARIABLE_MODULE'):
            var_module = module.VARIABLE_MODULE
            var_module.register_to_registry(variable_registry)



# For backward compatibility, provide common variables in __all__
__all__ = [
    # Most commonly used variables
    "Dimensionless", "Length", "Pressure", "Temperature", "Time", "Mass", "Volume", "Area", "Force", 
    "EnergyHeatWork", "PowerThermalDuty", "VelocityLinear", "Acceleration", "MassDensity", "ViscosityDynamic",
    # All 105 variable types are available via consolidated_new import above
]
