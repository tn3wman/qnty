"""
ParticleDensity Units Module
============================

Complete particle density unit definitions and constants.
"""

from ..dimension import PARTICLE_DENSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ParticleDensityUnits:
    """Type-safe particle density unit constants."""
    # Explicit declarations for type checking
    particles_per_cubic_centimeter: 'UnitConstant'
    particles_per_cubic_foot: 'UnitConstant'
    particles_per_cubic_meter: 'UnitConstant'
    particles_per_gallon_us: 'UnitConstant'
    particles_per_liter: 'UnitConstant'
    particles_per_milliliter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ParticleDensityUnitModule(UnitModule):
    """ParticleDensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all particle density unit definitions."""
        return [
            UnitDefinition("particles_per_cubic_centimeter", "part/cm  3 or part/cc", PARTICLE_DENSITY, 10000),
            UnitDefinition("particles_per_cubic_foot", "part/ ft3 or part/cft", PARTICLE_DENSITY, 35.31),
            UnitDefinition("particles_per_cubic_meter", "part / m3", PARTICLE_DENSITY, 1),
            UnitDefinition("particles_per_gallon_us", "part/gal", PARTICLE_DENSITY, 264.14),
            UnitDefinition("particles_per_liter", "part/l", PARTICLE_DENSITY, 1000),
            UnitDefinition("particles_per_milliliter", "part/ml", PARTICLE_DENSITY, 10000),

        ]
    
    def get_units_class(self):
        return ParticleDensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ParticleDensityUnitModule()