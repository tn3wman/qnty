"""
Dimension System
================

Compile-time dimensional analysis using type system for ultra-fast operations.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import final


class BaseDimension(IntEnum):
    """Base dimensions as prime numbers for efficient bit operations."""
    LENGTH = 2
    MASS = 3
    TIME = 5
    CURRENT = 7
    TEMPERATURE = 11
    AMOUNT = 13
    LUMINOSITY = 17


@final
@dataclass(frozen=True)
class DimensionSignature:
    """Immutable dimension signature for zero-cost dimensional analysis."""
    
    # Store as bit pattern for ultra-fast comparison
    _signature: int = 1
    
    @classmethod
    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):
        """Create dimension from exponents."""
        signature = 1
        if length != 0:
            signature *= BaseDimension.LENGTH ** length
        if mass != 0:
            signature *= BaseDimension.MASS ** mass
        if time != 0:
            signature *= BaseDimension.TIME ** time
        if current != 0:
            signature *= BaseDimension.CURRENT ** current
        if temp != 0:
            signature *= BaseDimension.TEMPERATURE ** temp
        if amount != 0:
            signature *= BaseDimension.AMOUNT ** amount
        if luminosity != 0:
            signature *= BaseDimension.LUMINOSITY ** luminosity
        
        return cls(signature)
    
    def __mul__(self, other):
        return DimensionSignature(self._signature * other._signature)
    
    def __truediv__(self, other):
        return DimensionSignature(self._signature // other._signature)
    
    def __pow__(self, power):
        return DimensionSignature(self._signature ** power)
    
    def is_compatible(self, other):
        """Ultra-fast dimensional compatibility check."""
        return self._signature == other._signature
    
    def __eq__(self, other):
        """Fast equality check for dimensions."""
        return isinstance(other, DimensionSignature) and self._signature == other._signature
    
    def __hash__(self):
        """Enable dimensions as dictionary keys."""
        return hash(self._signature)


# Pre-defined dimension constants
DIMENSIONLESS = DimensionSignature.create()
LENGTH = DimensionSignature.create(length=1)
MASS = DimensionSignature.create(mass=1)
TIME = DimensionSignature.create(time=1)
CURRENT = DimensionSignature.create(current=1)
TEMPERATURE = DimensionSignature.create(temp=1)
AMOUNT = DimensionSignature.create(amount=1)
LUMINOSITY = DimensionSignature.create(luminosity=1)
AREA = DimensionSignature.create(length=2)
VOLUME = DimensionSignature.create(length=3)
VELOCITY = DimensionSignature.create(length=1, time=-1)
ACCELERATION = DimensionSignature.create(length=1, time=-2)
FORCE = DimensionSignature.create(mass=1, length=1, time=-2)
PRESSURE = DimensionSignature.create(mass=1, length=-1, time=-2)
ENERGY = DimensionSignature.create(mass=1, length=2, time=-2)
ABSORBED_DOSE = DimensionSignature.create(length=2, time=-2)  # L^2 T^-2 (Gray, rad)

# Complex dimension constants
POWER = DimensionSignature.create(mass=1, length=2, time=-3)  # ML^2 T^-3 (Watt)
LENGTH_TEMPERATURE = DimensionSignature.create(length=1, temp=1)  # L θ (Second Radiation Constant)
MASS_TRANSFER_COEFFICIENT = DimensionSignature.create(length=-2, mass=1, time=-1)  # L^-2 M T^-1
HEAT_TRANSFER_COEFFICIENT = DimensionSignature.create(mass=1, time=-3, current=-1, temp=-1)  # M T^-3 A^-1 Θ^-1
WAVENUMBER = DimensionSignature.create(length=-1)  # L^-1
SPECIFIC_VOLUME = DimensionSignature.create(length=3, mass=-1)  # L^3 M^-1
MOLALITY = DimensionSignature.create()  # Molality
MOLARITY = DimensionSignature.create()  # Molarity
MAGNETIC_PERMEABILITY = DimensionSignature.create(length=2, mass=1, time=-2, current=-2)  # L^2 M T^-2 A^-2
POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY = DimensionSignature.create(length=-1, mass=1, time=-3)  # L^-1 M T^-3
ELECTRICAL_CONDUCTANCE = DimensionSignature.create(length=-2, mass=-1, time=3, current=2)  # L^-2 M^-1 T^3 A^2
MOMENT_OF_INERTIA = DimensionSignature.create(length=2, mass=1)  # L^2 M
MASS_DENSITY = DimensionSignature.create(length=-3, mass=1)  # L^-3 M
ENERGY_FLUX = DimensionSignature.create(mass=1, time=-3)  # M T^-3
ELECTRICAL_PERMITTIVITY = DimensionSignature.create(length=-3, mass=-1, time=4, current=2)  # L^-3 M^-1 T^4 A^2
FREQUENCY_VOLTAGE_RATIO = DimensionSignature.create(length=-2, mass=-1, time=3, current=1)  # L^-2 M^-1 T^3 A
SPECIFIC_SURFACE = DimensionSignature.create(length=2, mass=-1)  # L^2 M^-1
SECOND_RADIATION_CONSTANT_PLANCK = DimensionSignature.create(length=1, time=1, current=1, temp=1)  # L T A Θ
MAGNETIC_INDUCTION_FIELD_STRENGTH = DimensionSignature.create(mass=1, time=-2, current=-1)  # M T^-2 A^-1
CONCENTRATION = DimensionSignature.create(length=-3, mass=1)  # L^-3 M
MOLAR_FLUX = DimensionSignature.create(length=-2, time=-1, amount=1)  # L^-2 T^-1 N
VOLUMETRIC_COEFFICIENT_OF_EXPANSION = DimensionSignature.create(length=-3, mass=1, time=1, current=-1, temp=-1)  # L^-3 M T A^-1 Θ^-1
ELECTRIC_CAPACITANCE = DimensionSignature.create(length=-2, mass=-1, time=4, current=2)  # L^-2 M^-1 T^4 A^2
ENERGY_PER_UNIT_AREA = DimensionSignature.create(mass=1, time=-2)  # M T^-2
MASS_FLOW_RATE = DimensionSignature.create(mass=1, time=-1)  # M T^-1
SPECIFIC_LENGTH = DimensionSignature.create(length=1, mass=-1)  # L M^-1
ANGULAR_VELOCITY = DimensionSignature.create(time=-1)  # T^-1
MASS_FLUX = DimensionSignature.create(length=-2, mass=1, time=-1)  # L^-2 M T^-1
SURFACE_TENSION = DimensionSignature.create(mass=1, time=-2)  # M T^-2
DYNAMIC_FLUIDITY = DimensionSignature.create(length=1, mass=-1, time=1)  # L M^-1 T
POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER = DimensionSignature.create(length=2, time=-3)  # L^2 T^-3
ILLUMINANCE = DimensionSignature.create(length=-2, luminosity=1)  # L^-2 J
TURBULENCE_ENERGY_DISSIPATION_RATE = DimensionSignature.create(length=2, time=-3)  # L^2 T^-3
ELECTRIC_FIELD = DimensionSignature.create()  # Electric Field
DYNAMIC_VISCOSITY = DimensionSignature.create(length=-1, mass=1, time=-1)  # L^-1 M T^-1
RADIATION_EXPOSURE = DimensionSignature.create(mass=-1, time=1, current=1)  # M^-1 T A
MOLAR_HEAT_CAPACITY = DimensionSignature.create(length=2, time=-2, current=-1, temp=-1, amount=-1)  # L^2 T^-2 A^-1 Θ^-1 N^-1
MAGNETIC_FIELD = DimensionSignature.create(length=-1, current=1)  # L^-1 A
ACTIVATION_ENERGY = DimensionSignature.create(length=2, time=-2, amount=-1)  # L^2 T^-2 N^-1
KINEMATIC_VISCOSITY = DimensionSignature.create(length=2, time=-1)  # L^2 T^-1
ANGULAR_ACCELERATION = DimensionSignature.create(time=-2)  # T^-2
ELECTRIC_INDUCTANCE = DimensionSignature.create(length=2, mass=1, time=-2, current=-2)  # L^2 M T^-2 A^-2
FORCE_BODY = DimensionSignature.create(length=1, mass=1, time=-2)  # L M T^-2
PARTICLE_DENSITY = DimensionSignature.create(length=-3)  # L^-3
NORMALITY = DimensionSignature.create()  # Normality
SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE = DimensionSignature.create(length=2, mass=1, time=-2, current=-1, temp=-1)  # L^2 M T^-2 A^-1 Θ^-1
FUEL_CONSUMPTION = DimensionSignature.create(length=-2)  # L^-2
RADIOACTIVITY = DimensionSignature.create(time=-1)  # T^-1
ELECTRIC_RESISTANCE = DimensionSignature.create(length=2, mass=1, time=-3, current=-2)  # L^2 M T^-3 A^-2
MOLAR_FLOW_RATE = DimensionSignature.create(time=-1, amount=1)  # T^-1 N
VOLUMETRIC_FLUX = DimensionSignature.create(length=1, time=-1)  # L T^-1
VOLUMETRIC_MASS_FLOW_RATE = DimensionSignature.create(length=-3, mass=1, time=-1)  # L^-3 M T^-1
MAGNETIC_MOMENT = DimensionSignature.create(length=2, current=1)  # L^2 A
MAGNETIC_FLUX = DimensionSignature.create(length=2, mass=1, time=-2, current=-1)  # L^2 M T^-2 A^-1
LINEAR_MOMENTUM = DimensionSignature.create(length=1, mass=1, time=-1)  # L M T^-1
LUMINANCE = DimensionSignature.create()  # Luminance
ATOMIC_WEIGHT = DimensionSignature.create(mass=1, amount=-1)  # M N^-1
ELECTRIC_DIPOLE_MOMENT = DimensionSignature.create(length=1, time=1, current=1)  # L T A
ANGULAR_MOMENTUM = DimensionSignature.create(length=2, mass=1, time=-1)  # L^2 M T^-1
VOLUMETRIC_FLOW_RATE = DimensionSignature.create(length=3, time=-1)  # L^3 T^-1
SECOND_MOMENT_OF_AREA = DimensionSignature.create(length=4)  # L^4
AREA_PER_UNIT_VOLUME = DimensionSignature.create(length=-1)  # L^-1
ELECTRIC_POTENTIAL = DimensionSignature.create(length=2, mass=1, time=-3, current=-1)  # L^2 M T^-3 A^-1
ELECTRICAL_RESISTIVITY = DimensionSignature.create(length=3, mass=1, time=-3, current=-2)  # L^3 M T^-3 A^-2
PHOTON_EMISSION_RATE = DimensionSignature.create(length=-2, time=-1)  # L^-2 T^-1
ELECTRIC_CHARGE = DimensionSignature.create(time=1, current=1, amount=-1)  # T A N^-1

THERMAL_CONDUCTIVITY = DimensionSignature.create(mass=1, length=1, time=-3, temp=-1)  # MLT^-3 θ^-1
